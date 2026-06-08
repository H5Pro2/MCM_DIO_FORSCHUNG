"""Build a passive cortex view for DIO_MINI.

The cortex view joins:
- passive family file rows,
- passive reflection timeline rows,
- current debug-world episode rows.

It is a report only. It does not write memory and it is not imported by the
mini motor path.
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


def _read_csv_by_family(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    result = {}
    for row in rows:
        family = str(row.get("family", "") or "")
        if family:
            result[family] = dict(row)
    return result


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


def _current_world_by_family(rows: list[dict]) -> dict[str, dict]:
    grouped: dict[str, dict] = {}
    for row in rows:
        family = str(row.get("symbol_family", "") or "")
        if not family:
            continue
        item = grouped.setdefault(
            family,
            {
                "current_seen_count": 0,
                "current_executed_count": 0,
                "current_observed_potential_count": 0,
                "current_held_pressure_count": 0,
                "current_reward_sum": 0.0,
                "current_best_reward_sum": 0.0,
                "current_actions": {},
                "current_states": {},
                "last_run": "",
                "last_tick": "",
            },
        )
        action = str(row.get("action", "WAIT") or "WAIT").upper()
        state = _episode_state(row)
        item["current_seen_count"] += 1
        item["current_reward_sum"] += _safe_float(row.get("reward", 0.0))
        item["current_best_reward_sum"] += _safe_float(row.get("best_reward_training", 0.0))
        item["current_actions"][action] = int(item["current_actions"].get(action, 0) or 0) + 1
        item["current_states"][state] = int(item["current_states"].get(state, 0) or 0) + 1
        if action in ("LONG", "SHORT"):
            item["current_executed_count"] += 1
        if state == "observed_trade_potential":
            item["current_observed_potential_count"] += 1
        if state == "held_trade_pressure":
            item["current_held_pressure_count"] += 1
        item["last_run"] = str(row.get("run", "") or "")
        item["last_tick"] = str(row.get("tick", "") or "")
    return grouped


def _format_counts(counts: dict) -> str:
    if not counts:
        return "-"
    return "|".join(f"{key}:{value}" for key, value in sorted(counts.items()))


def _cortex_sentence(row: dict) -> str:
    family = str(row.get("family", "") or "-")
    timeline_state = str(row.get("timeline_state", "") or "-")
    current_seen = _safe_int(row.get("current_seen_count", 0))
    current_executed = _safe_int(row.get("current_executed_count", 0))
    current_observed = _safe_int(row.get("current_observed_potential_count", 0))
    current_reward = _safe_float(row.get("current_reward_sum", 0.0))
    if current_seen <= 0:
        return f"{family}: gespeicherte Akte vorhanden, in dieser Debug-Welt nicht gesehen."
    if "conflict" in timeline_state:
        return (
            f"{family}: alte Akte hat Konfliktspur; aktuelle Welt sieht {current_seen} Kontakte, "
            f"{current_executed} Handlungen, reward={current_reward:.6f}."
        )
    if "reconfirmed" in timeline_state:
        return (
            f"{family}: getragene Akte; aktuelle Welt sieht {current_seen} Kontakte, "
            f"{current_executed} Handlungen und {current_observed} beobachtete Potenziale."
        )
    if "quiet" in timeline_state:
        return f"{family}: stille Akte; aktuelle Welt sieht {current_seen} Kontakte ohne tragende Zeitlinie."
    return f"{family}: aktuelle Welt sieht {current_seen} Kontakte; Aktenlage bleibt offen."


def build_rows(
    family_file: Path,
    timeline_file: Path,
    debug_root: Path,
    selected_families: set[str] | None = None,
) -> list[dict]:
    family_rows = _read_csv_by_family(family_file)
    timeline_rows = _read_csv_by_family(timeline_file)
    current_rows = _current_world_by_family(_iter_episode_rows(debug_root))

    families = set(family_rows)
    families.update(timeline_rows)
    families.update(current_rows)
    if selected_families:
        families &= selected_families

    rows = []
    for family in sorted(families):
        family_row = dict(family_rows.get(family, {}) or {})
        timeline_row = dict(timeline_rows.get(family, {}) or {})
        current = dict(current_rows.get(family, {}) or {})
        row = {
            "family": family,
            "family_count": _safe_int(family_row.get("family_count", 0)),
            "strongest_action_trace": str(
                family_row.get("strongest_action_trace", family_row.get("best_action_memory", "-")) or "-"
            ),
            "reflection_map_states": str(family_row.get("reflection_map_states", "-") or "-"),
            "timeline_state": str(timeline_row.get("timeline_state", "-") or "-"),
            "timeline": str(timeline_row.get("timeline", "-") or "-"),
            "stored_passive_sentence": str(family_row.get("passive_sentence", "") or ""),
            "timeline_passive_sentence": str(timeline_row.get("passive_sentence", "") or ""),
            "current_seen_count": _safe_int(current.get("current_seen_count", 0)),
            "current_executed_count": _safe_int(current.get("current_executed_count", 0)),
            "current_observed_potential_count": _safe_int(current.get("current_observed_potential_count", 0)),
            "current_held_pressure_count": _safe_int(current.get("current_held_pressure_count", 0)),
            "current_reward_sum": round(_safe_float(current.get("current_reward_sum", 0.0)), 6),
            "current_best_reward_sum": round(_safe_float(current.get("current_best_reward_sum", 0.0)), 6),
            "current_actions": _format_counts(dict(current.get("current_actions", {}) or {})),
            "current_states": _format_counts(dict(current.get("current_states", {}) or {})),
            "last_run": str(current.get("last_run", "") or ""),
            "last_tick": str(current.get("last_tick", "") or ""),
        }
        row["cortex_sentence"] = _cortex_sentence(row)
        rows.append(row)

    rows.sort(
        key=lambda item: (
            -_safe_int(item.get("current_seen_count", 0)),
            str(item.get("timeline_state", "")) not in ("mixed_reconfirmed_and_conflict", "reconfirmed_stable"),
            str(item.get("family", "")),
        )
    )
    return rows


def write_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "dio_mini_passive_cortex_view.csv"
    json_path = output_dir / "dio_mini_passive_cortex_view.json"
    md_path = output_dir / "dio_mini_passive_cortex_view.md"
    fields = [
        "family",
        "family_count",
        "strongest_action_trace",
        "reflection_map_states",
        "timeline_state",
        "current_seen_count",
        "current_executed_count",
        "current_observed_potential_count",
        "current_held_pressure_count",
        "current_reward_sum",
        "current_best_reward_sum",
        "current_actions",
        "current_states",
        "last_run",
        "last_tick",
        "timeline",
        "stored_passive_sentence",
        "timeline_passive_sentence",
        "cortex_sentence",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Passive Cortex View", ""]
    if not rows:
        lines.append("Keine Familien gelesen.")
    for row in rows:
        lines.extend(
            [
                f"## {row['family']}",
                f"- cortex_sentence: {row['cortex_sentence']}",
                f"- timeline_state: {row['timeline_state']}",
                f"- strongest_action_trace: {row['strongest_action_trace']}",
                f"- current seen/executed/observed/held: {row['current_seen_count']} / {row['current_executed_count']} / {row['current_observed_potential_count']} / {row['current_held_pressure_count']}",
                f"- current_reward_sum: {float(row['current_reward_sum']):.6f}",
                f"- current_actions: {row['current_actions']}",
                f"- current_states: {row['current_states']}",
                f"- timeline: {row['timeline']}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive DIO_MINI cortex view")
    parser.add_argument("--family-file", required=True)
    parser.add_argument("--timeline-file", required=True)
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--family", action="append", default=[])
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    selected = {str(item).strip() for item in args.family if str(item).strip()}
    rows = build_rows(
        Path(args.family_file),
        Path(args.timeline_file),
        Path(args.debug_root),
        selected_families=selected or None,
    )
    write_outputs(rows, Path(args.output_dir))
    print(f"families={len(rows)}")
    for row in rows[:16]:
        print(
            f"{row['family']} cortex_seen={row['current_seen_count']} "
            f"timeline={row['timeline_state']} reward={row['current_reward_sum']}"
        )


if __name__ == "__main__":
    main()
