"""Report passive repeat stability for DIO_MINI debug runs.

The report reads repeated run episode files and summarizes whether symbol
families are repeatedly seen, executed, held, or only observed. It is a reader
only and must not be imported by the mini motor path.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _safe_float(value: object) -> float:
    try:
        return float(value or 0.0)
    except Exception:
        return 0.0


def _safe_int(value: object) -> int:
    try:
        return int(value or 0)
    except Exception:
        return 0


def _iter_episode_rows(debug_root: Path) -> list[dict]:
    rows = []
    for path in sorted(debug_root.glob("**/episodes.csv")):
        run_id = path.parent.name.replace("dio_mini_lauf_", "")
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                item = dict(row)
                item["run"] = run_id
                rows.append(item)
    return rows


def _episode_state(row: dict) -> str:
    action = str(row.get("action", "WAIT") or "WAIT").upper()
    raw_action = str(row.get("raw_action", action) or action).upper()
    best_action = str(row.get("best_action_training", "WAIT") or "WAIT").upper()
    best_reward = _safe_float(row.get("best_reward_training", 0.0))
    phase_active = str(row.get("phase_active", "0") or "0") in ("1", "true", "True")
    if action in ("LONG", "SHORT"):
        return "executed_aligned" if action == best_action else "executed_misaligned"
    if action == "WAIT" and raw_action in ("LONG", "SHORT") and phase_active:
        return "held_trade_pressure"
    if best_action in ("LONG", "SHORT") and best_reward > 0.0:
        return "observed_trade_potential"
    return "quiet"


def _format_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "-"
    return "|".join(f"{key}:{value}" for key, value in sorted(counts.items()))


def _passive_repeat_state(run_count: int, seen_runs: int, executed_runs: int, reward_sum: float, states: str) -> str:
    if seen_runs <= 0:
        return "repeat_not_seen"
    if executed_runs == run_count and reward_sum > 0.0:
        return "repeat_executed_carried"
    if executed_runs > 0 and reward_sum > 0.0:
        return "repeat_partly_carried"
    if "held_trade_pressure" in states and executed_runs <= 0:
        return "repeat_held_pressure"
    if "observed_trade_potential" in states and executed_runs <= 0:
        return "repeat_observed_potential"
    if executed_runs > 0 and reward_sum <= 0.0:
        return "repeat_executed_unresolved"
    return "repeat_seen_unclear"


def _sentence(row: dict) -> str:
    family = str(row.get("family", "") or "-")
    state = str(row.get("passive_repeat_state", "") or "-")
    if state == "repeat_executed_carried":
        return f"{family}: wurde in jedem Wiederholungslauf aktiv getragen."
    if state == "repeat_partly_carried":
        return f"{family}: wurde in einem Teil der Wiederholung getragen."
    if state == "repeat_held_pressure":
        return f"{family}: kehrt als gehaltene Handelsspannung wieder."
    if state == "repeat_observed_potential":
        return f"{family}: kehrt als beobachtetes Handelspotenzial wieder."
    if state == "repeat_not_seen":
        return f"{family}: wurde in diesen Wiederholungslaeufen nicht gesehen."
    return f"{family}: bleibt in der Wiederholung offen."


def build_rows(debug_root: Path, selected_families: set[str] | None = None) -> list[dict]:
    episode_rows = _iter_episode_rows(debug_root)
    runs = sorted({str(row.get("run", "") or "") for row in episode_rows if row.get("run")})
    run_count = len(runs)
    grouped: dict[str, dict] = {}

    for row in episode_rows:
        family = str(row.get("symbol_family", "") or "")
        if not family:
            continue
        if selected_families and family not in selected_families:
            continue
        run = str(row.get("run", "") or "")
        action = str(row.get("action", "WAIT") or "WAIT").upper()
        state = _episode_state(row)
        item = grouped.setdefault(
            family,
            {
                "family": family,
                "runs_seen": set(),
                "runs_executed": set(),
                "seen_count": 0,
                "executed_count": 0,
                "observed_potential_count": 0,
                "held_pressure_count": 0,
                "reward_sum": 0.0,
                "best_reward_sum": 0.0,
                "actions": {},
                "states": {},
                "first_run": run,
                "last_run": run,
            },
        )
        item["runs_seen"].add(run)
        item["seen_count"] += 1
        item["reward_sum"] += _safe_float(row.get("reward", 0.0))
        item["best_reward_sum"] += _safe_float(row.get("best_reward_training", 0.0))
        item["actions"][action] = int(item["actions"].get(action, 0) or 0) + 1
        item["states"][state] = int(item["states"].get(state, 0) or 0) + 1
        if action in ("LONG", "SHORT"):
            item["runs_executed"].add(run)
            item["executed_count"] += 1
        if state == "observed_trade_potential":
            item["observed_potential_count"] += 1
        if state == "held_trade_pressure":
            item["held_pressure_count"] += 1
        item["last_run"] = run

    rows = []
    for family, item in grouped.items():
        states = _format_counts(dict(item["states"]))
        row = {
            "family": family,
            "run_count": run_count,
            "seen_runs": len(item["runs_seen"]),
            "executed_runs": len(item["runs_executed"]),
            "seen_count": item["seen_count"],
            "executed_count": item["executed_count"],
            "observed_potential_count": item["observed_potential_count"],
            "held_pressure_count": item["held_pressure_count"],
            "reward_sum": round(float(item["reward_sum"]), 6),
            "best_reward_sum": round(float(item["best_reward_sum"]), 6),
            "actions": _format_counts(dict(item["actions"])),
            "states": states,
            "first_run": item["first_run"],
            "last_run": item["last_run"],
        }
        row["passive_repeat_state"] = _passive_repeat_state(
            run_count,
            int(row["seen_runs"]),
            int(row["executed_runs"]),
            float(row["reward_sum"]),
            states,
        )
        row["passive_sentence"] = _sentence(row)
        rows.append(row)

    rows.sort(
        key=lambda item: (
            str(item.get("passive_repeat_state", "")) != "repeat_executed_carried",
            -_safe_float(item.get("reward_sum", 0.0)),
            -_safe_int(item.get("seen_runs", 0)),
            str(item.get("family", "")),
        )
    )
    return rows


def write_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "dio_mini_repeat_stability.csv"
    json_path = output_dir / "dio_mini_repeat_stability.json"
    md_path = output_dir / "dio_mini_repeat_stability.md"
    fields = [
        "family",
        "passive_repeat_state",
        "run_count",
        "seen_runs",
        "executed_runs",
        "seen_count",
        "executed_count",
        "observed_potential_count",
        "held_pressure_count",
        "reward_sum",
        "best_reward_sum",
        "actions",
        "states",
        "first_run",
        "last_run",
        "passive_sentence",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Repeat Stability", ""]
    if not rows:
        lines.append("Keine wiederholten Familien gefunden.")
    for row in rows:
        lines.extend(
            [
                f"## {row['family']}",
                f"- state: {row['passive_repeat_state']}",
                f"- seen_runs / executed_runs: {row['seen_runs']} / {row['executed_runs']}",
                f"- seen / executed: {row['seen_count']} / {row['executed_count']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- actions: {row['actions']}",
                f"- states: {row['states']}",
                f"- passive_sentence: {row['passive_sentence']}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive DIO_MINI repeat stability report")
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--family", action="append", default=[])
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    selected = {str(item).strip() for item in args.family if str(item).strip()} or None
    rows = build_rows(Path(args.debug_root), selected_families=selected)
    write_outputs(rows, Path(args.output_dir))
    print(f"families={len(rows)}")
    for row in rows[:25]:
        print(
            f"{row['family']} state={row['passive_repeat_state']} "
            f"seen_runs={row['seen_runs']} executed_runs={row['executed_runs']} "
            f"reward={row['reward_sum']}"
        )


if __name__ == "__main__":
    main()
