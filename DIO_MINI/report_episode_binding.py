"""Report DIO_MINI episode binding and held trade impulses."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _float(row: dict, key: str) -> float:
    try:
        return float(row.get(key, 0.0) or 0.0)
    except Exception:
        return 0.0


def _iter_rows(debug_root: Path) -> list[dict]:
    rows = []
    for path in sorted(debug_root.glob("dio_mini_lauf_*/episodes.csv")):
        run_id = path.parent.name.replace("dio_mini_lauf_", "")
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                item = dict(row)
                item["run"] = run_id
                rows.append(item)
    return rows


def _binding_state(row: dict) -> str:
    action = str(row.get("action", "WAIT") or "WAIT").upper()
    raw_action = str(row.get("raw_action", action) or action).upper()
    best_action = str(row.get("best_action_training", "WAIT") or "WAIT").upper()
    phase_active = str(row.get("phase_active", "0") or "0") in ("1", "true", "True")
    best_reward = _float(row, "best_reward_training")
    if action == "WAIT" and raw_action in ("LONG", "SHORT") and phase_active:
        if raw_action == best_action and best_reward > 0.0:
            return "held_useful_impulse"
        if raw_action != best_action and best_action in ("LONG", "SHORT"):
            return "held_wrong_impulse"
        return "held_unclear_impulse"
    if action in ("LONG", "SHORT"):
        if action == best_action:
            return "executed_aligned"
        return "executed_misaligned"
    if best_action in ("LONG", "SHORT") and best_reward > 0.0:
        return "observed_not_bound"
    return "quiet"


def _binding_quality(state_name: str) -> str:
    if state_name == "held_useful_impulse":
        return "episode_binding_overholding"
    if state_name == "held_wrong_impulse":
        return "episode_binding_protective"
    if state_name == "held_unclear_impulse":
        return "episode_binding_unclear"
    if state_name == "observed_not_bound":
        return "observation_potential"
    if state_name == "executed_aligned":
        return "executed_contact_confirmed"
    if state_name == "executed_misaligned":
        return "executed_contact_misaligned"
    return "quiet"


def _summaries(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    detail = []
    overview: dict[str, dict] = {}
    for row in rows:
        state_name = _binding_state(row)
        quality_name = _binding_quality(state_name)
        action = str(row.get("action", "WAIT") or "WAIT").upper()
        raw_action = str(row.get("raw_action", action) or action).upper()
        best_action = str(row.get("best_action_training", "WAIT") or "WAIT").upper()
        best_reward = _float(row, "best_reward_training")
        unrealized_best_reward = 0.0
        if action != best_action and best_action in ("LONG", "SHORT") and best_reward > 0.0:
            unrealized_best_reward = best_reward
        held_impulse_potential = best_reward if state_name == "held_useful_impulse" else 0.0
        item = {
            "run": row.get("run", ""),
            "tick": row.get("tick", ""),
            "symbol_family": row.get("symbol_family", ""),
            "action": action,
            "raw_action": raw_action,
            "best_action_training": best_action,
            "binding_state": state_name,
            "binding_quality": quality_name,
            "episode_relation": row.get("episode_relation", ""),
            "phase_active": int(str(row.get("phase_active", "0") or "0") in ("1", "true", "True")),
            "phase_age": row.get("phase_age", ""),
            "phase_distance": _float(row, "phase_distance"),
            "episode_binding_pressure": _float(row, "episode_binding_pressure"),
            "episode_release_pressure": _float(row, "episode_release_pressure"),
            "score_wait": _float(row, "score_wait"),
            "score_long": _float(row, "score_long"),
            "score_short": _float(row, "score_short"),
            "reward": _float(row, "reward"),
            "best_reward_training": best_reward,
            "unrealized_best_reward": unrealized_best_reward,
            "held_impulse_potential": held_impulse_potential,
        }
        detail.append(item)
        overview_item = overview.setdefault(
            state_name,
            {
                "binding_state": state_name,
                "count": 0,
                "reward_sum": 0.0,
                "best_reward_sum": 0.0,
                "unrealized_best_reward_sum": 0.0,
                "held_impulse_potential_sum": 0.0,
                "qualities": set(),
                "families": set(),
            },
        )
        overview_item["count"] += 1
        overview_item["reward_sum"] += float(item["reward"])
        overview_item["best_reward_sum"] += float(item["best_reward_training"])
        overview_item["unrealized_best_reward_sum"] += float(item["unrealized_best_reward"])
        overview_item["held_impulse_potential_sum"] += float(item["held_impulse_potential"])
        overview_item["qualities"].add(str(item["binding_quality"]))
        overview_item["families"].add(str(item["symbol_family"]))
    overview_rows = []
    for item in overview.values():
        count = int(item["count"] or 0)
        overview_rows.append(
            {
                "binding_state": item["binding_state"],
                "count": count,
                "reward_sum": round(float(item["reward_sum"]), 6),
                "best_reward_sum": round(float(item["best_reward_sum"]), 6),
                "unrealized_best_reward_sum": round(float(item["unrealized_best_reward_sum"]), 6),
                "held_impulse_potential_sum": round(float(item["held_impulse_potential_sum"]), 6),
                "avg_reward": round(float(item["reward_sum"]) / max(1, count), 6),
                "qualities": ",".join(sorted(str(name) for name in item["qualities"] if name)),
                "families": ",".join(sorted(str(name) for name in item["families"] if name)),
            }
        )
    overview_rows.sort(key=lambda item: (-int(item["count"]), item["binding_state"]))
    return detail, overview_rows


def _write(detail: list[dict], overview: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_episode_binding_detail.csv"
    overview_csv = output_dir / "dio_mini_episode_binding_overview.csv"
    json_path = output_dir / "dio_mini_episode_binding_overview.json"
    md_path = output_dir / "dio_mini_episode_binding_overview.md"
    detail_fields = list(detail[0].keys()) if detail else [
        "run",
        "tick",
        "symbol_family",
        "action",
        "raw_action",
        "best_action_training",
        "binding_state",
    ]
    with detail_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)
    overview_fields = [
        "binding_state",
        "count",
        "reward_sum",
        "best_reward_sum",
        "unrealized_best_reward_sum",
        "held_impulse_potential_sum",
        "avg_reward",
        "qualities",
        "families",
    ]
    with overview_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=overview_fields)
        writer.writeheader()
        writer.writerows(overview)
    json_path.write_text(json.dumps(overview, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Episode Binding Overview", ""]
    if not overview:
        lines.append("Keine Episoden gefunden.")
    for row in overview:
        lines.extend(
            [
                f"## {row['binding_state']}",
                f"- count: {row['count']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- best_reward_sum: {float(row['best_reward_sum']):.6f}",
                f"- unrealized_best_reward_sum: {float(row['unrealized_best_reward_sum']):.6f}",
                f"- held_impulse_potential_sum: {float(row['held_impulse_potential_sum']):.6f}",
                f"- avg_reward: {float(row['avg_reward']):.6f}",
                f"- qualities: {row['qualities'] or '-'}",
                f"- families: {row['families'] or '-'}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    detail, overview = _summaries(_iter_rows(Path(args.debug_root)))
    _write(detail, overview, Path(args.output_dir))
    print(f"episodes={len(detail)} groups={len(overview)}")
    for row in overview:
        print(
            f"{row['binding_state']} count={row['count']} "
            f"reward={row['reward_sum']} best={row['best_reward_sum']}"
        )


if __name__ == "__main__":
    main()
