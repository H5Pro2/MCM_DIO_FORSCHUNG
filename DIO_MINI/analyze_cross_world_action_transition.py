"""Aggregate DIO mini action-transition behavior across controlled worlds."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.analyze_action_transition import analyze as analyze_action_transition


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def parse_phase(text: str) -> tuple[str, Path]:
    parts = str(text or "").split(":", 1)
    if len(parts) != 2:
        raise ValueError(f"Phase must use name:path format, got {text!r}")
    return parts[0].strip() or "phase", Path(parts[1].strip())


def _classify_world(record: dict) -> str:
    class_counts = dict(record.get("class_counts", {}) or {})
    direct = _safe_int(class_counts.get("direct_positive_action", 0))
    transition = _safe_int(class_counts.get("observation_to_positive_action", 0))
    held = _safe_int(class_counts.get("held_observation", 0))
    burden = _safe_int(class_counts.get("direct_burdened_action", 0)) + _safe_int(
        class_counts.get("observation_to_burdened_action", 0)
    )
    phase_count = len(record.get("phases", set()) or set())
    reward = _safe_float(record.get("reward_sum", 0.0))
    if burden > 0 and reward < 0.0:
        return "burdened_action_pattern"
    if phase_count > 1 and direct > 0 and transition > 0 and reward > 0.0:
        return "matured_action_pattern"
    if phase_count > 1 and transition > 0 and reward > 0.0:
        return "observation_maturing_pattern"
    if phase_count > 1 and direct > 0 and reward > 0.0:
        return "direct_mature_pattern"
    if direct > 0 and reward > 0.0:
        return "local_direct_action"
    if transition > 0 and reward > 0.0:
        return "local_observation_to_action"
    if held > 0:
        return "held_observation_pattern"
    return "quiet_pattern"


def build_cross_world(phases: list[tuple[str, Path]]) -> tuple[list[dict], list[dict]]:
    phase_rows = []
    families: dict[str, dict] = {}
    for phase_name, debug_root in phases:
        rows, _overview = analyze_action_transition(debug_root)
        for row in rows:
            phase_row = {"phase": phase_name, **row}
            phase_rows.append(phase_row)
            family = str(row.get("family", "-") or "-")
            record = families.setdefault(
                family,
                {
                    "family": family,
                    "phases": set(),
                    "class_counts": {},
                    "rows": 0,
                    "executed_rows": 0,
                    "observed_rows": 0,
                    "raw_trade_rows": 0,
                    "reward_sum": 0.0,
                    "executed_reward_sum": 0.0,
                    "observed_best_reward_sum": 0.0,
                    "max_executed_trade_readiness": 0.0,
                    "max_observed_trade_readiness": 0.0,
                    "max_executed_mature_transfer": 0.0,
                    "max_observed_mature_transfer": 0.0,
                },
            )
            classification = str(row.get("classification", "quiet_pattern") or "quiet_pattern")
            record["phases"].add(phase_name)
            record["class_counts"][classification] = int(record["class_counts"].get(classification, 0)) + 1
            record["rows"] += _safe_int(row.get("rows", 0))
            record["executed_rows"] += _safe_int(row.get("executed_rows", 0))
            record["observed_rows"] += _safe_int(row.get("observed_rows", 0))
            record["raw_trade_rows"] += _safe_int(row.get("raw_trade_rows", 0))
            record["reward_sum"] += _safe_float(row.get("reward_sum", 0.0))
            record["executed_reward_sum"] += _safe_float(row.get("executed_reward_sum", 0.0))
            record["observed_best_reward_sum"] += _safe_float(row.get("observed_best_reward_sum", 0.0))
            record["max_executed_trade_readiness"] = max(
                record["max_executed_trade_readiness"],
                _safe_float(row.get("executed_trade_readiness", 0.0)),
            )
            record["max_observed_trade_readiness"] = max(
                record["max_observed_trade_readiness"],
                _safe_float(row.get("observed_trade_readiness", 0.0)),
            )
            record["max_executed_mature_transfer"] = max(
                record["max_executed_mature_transfer"],
                _safe_float(row.get("executed_mature_transfer", 0.0)),
            )
            record["max_observed_mature_transfer"] = max(
                record["max_observed_mature_transfer"],
                _safe_float(row.get("observed_mature_transfer", 0.0)),
            )

    world_rows = []
    for record in families.values():
        phases = sorted(record["phases"])
        class_counts = dict(record["class_counts"])
        row = {
            "family": record["family"],
            "phases": ",".join(phases),
            "phase_count": len(phases),
            "action_transition_class": _classify_world(record),
            "class_counts": json.dumps(class_counts, sort_keys=True),
            "direct_positive_action": int(class_counts.get("direct_positive_action", 0)),
            "observation_to_positive_action": int(class_counts.get("observation_to_positive_action", 0)),
            "held_observation": int(class_counts.get("held_observation", 0)),
            "burdened_action": int(class_counts.get("direct_burdened_action", 0))
            + int(class_counts.get("observation_to_burdened_action", 0)),
            "rows": record["rows"],
            "executed_rows": record["executed_rows"],
            "observed_rows": record["observed_rows"],
            "raw_trade_rows": record["raw_trade_rows"],
            "reward_sum": round(record["reward_sum"], 6),
            "executed_reward_sum": round(record["executed_reward_sum"], 6),
            "observed_best_reward_sum": round(record["observed_best_reward_sum"], 6),
            "max_executed_trade_readiness": round(record["max_executed_trade_readiness"], 6),
            "max_observed_trade_readiness": round(record["max_observed_trade_readiness"], 6),
            "max_executed_mature_transfer": round(record["max_executed_mature_transfer"], 6),
            "max_observed_mature_transfer": round(record["max_observed_mature_transfer"], 6),
        }
        world_rows.append(row)
    world_rows.sort(
        key=lambda item: (
            item["action_transition_class"] == "matured_action_pattern",
            item["action_transition_class"] == "observation_maturing_pattern",
            item["action_transition_class"] == "direct_mature_pattern",
            item["phase_count"],
            item["reward_sum"],
            item["executed_rows"],
        ),
        reverse=True,
    )
    return phase_rows, world_rows


def _write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(phase_rows: list[dict], world_rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    overview_counts: dict[str, int] = {}
    overview_reward: dict[str, float] = {}
    for row in world_rows:
        cls = str(row.get("action_transition_class", "-") or "-")
        overview_counts[cls] = overview_counts.get(cls, 0) + 1
        overview_reward[cls] = overview_reward.get(cls, 0.0) + _safe_float(row.get("reward_sum", 0.0))
    overview = {
        "class_counts": overview_counts,
        "class_reward_sum": {key: round(value, 6) for key, value in sorted(overview_reward.items())},
        "top_matured_action": [
            row["family"] for row in world_rows if row["action_transition_class"] == "matured_action_pattern"
        ][:8],
        "top_observation_maturing": [
            row["family"] for row in world_rows if row["action_transition_class"] == "observation_maturing_pattern"
        ][:8],
        "top_direct_mature": [
            row["family"] for row in world_rows if row["action_transition_class"] == "direct_mature_pattern"
        ][:8],
        "held_observation": [
            row["family"] for row in world_rows if row["action_transition_class"] == "held_observation_pattern"
        ][:8],
    }
    (output_dir / "dio_mini_cross_world_action_transition_phase_rows.json").write_text(
        json.dumps(phase_rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "dio_mini_cross_world_action_transition_world_summary.json").write_text(
        json.dumps(world_rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "dio_mini_cross_world_action_transition_overview.json").write_text(
        json.dumps(overview, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    _write_csv(output_dir / "dio_mini_cross_world_action_transition_phase_rows.csv", phase_rows)
    _write_csv(output_dir / "dio_mini_cross_world_action_transition_world_summary.csv", world_rows)
    lines = ["# DIO Mini Cross World Action Transition", ""]
    lines.append("## Classes")
    for key, value in sorted(overview_counts.items()):
        lines.append(f"- {key}: {value}, reward {overview['class_reward_sum'].get(key, 0.0)}")
    lines.append("")
    lines.append("## Matured Action")
    for family in overview["top_matured_action"]:
        lines.append(f"- {family}")
    lines.append("")
    lines.append("## Observation Maturing")
    for family in overview["top_observation_maturing"]:
        lines.append(f"- {family}")
    lines.append("")
    lines.append("## Direct Mature")
    for family in overview["top_direct_mature"]:
        lines.append(f"- {family}")
    lines.append("")
    lines.append("## Held Observation")
    for family in overview["held_observation"]:
        lines.append(f"- {family}")
    lines.append("")
    (output_dir / "dio_mini_cross_world_action_transition.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze DIO mini action transitions across controlled worlds")
    parser.add_argument("--phase", action="append", required=True, help="name:path")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    phases = [parse_phase(item) for item in args.phase]
    phase_rows, world_rows = build_cross_world(phases)
    write_outputs(phase_rows, world_rows, Path(args.output_dir))
    for row in world_rows[:16]:
        print(
            f"family={row['family']} class={row['action_transition_class']} phases={row['phase_count']} "
            f"executed={row['executed_rows']} observed={row['observed_rows']} reward={row['reward_sum']:.4f}"
        )


if __name__ == "__main__":
    main()
