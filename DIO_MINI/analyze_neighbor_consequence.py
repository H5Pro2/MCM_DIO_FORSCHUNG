"""Attach passive consequence labels to DIO mini family-sense neighbors.

This reads a neighbor map and describes how each sensor-near relation behaved
in consequence terms. It does not change memory, motorics, or action scores.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


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
        return int(float(value))
    except Exception:
        return default


def _read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _world_index(rows: list[dict]) -> dict[str, dict]:
    return {str(row.get("family", "-") or "-"): row for row in rows}


def _relation_state(target: dict, reference: dict, neighbor: dict) -> str:
    target_reward = _safe_float(target.get("reward_sum", neighbor.get("target_reward_sum", 0.0)))
    reference_reward = _safe_float(reference.get("reward_sum", neighbor.get("reference_reward_sum", 0.0)))
    target_executed = _safe_int(target.get("executed_rows", neighbor.get("target_executed_rows", 0)))
    target_observed = _safe_int(target.get("observed_rows", neighbor.get("target_observed_rows", 0)))
    burdened = _safe_int(target.get("burdened_action", 0)) + _safe_int(reference.get("burdened_action", 0))
    if burdened > 0 or target_reward < 0.0:
        return "vorsichtige_verwandtschaft"
    if target_executed > 0 and target_reward > 0.0 and reference_reward > 0.0:
        return "reifende_verwandtschaft"
    if target_observed > 0 and target_executed == 0:
        return "beobachtete_verwandtschaft"
    if target_executed > 0 and target_reward == 0.0:
        return "unklare_verwandtschaft"
    return "offene_verwandtschaft"


def analyze(neighbor_rows: list[dict], world_rows: list[dict]) -> tuple[list[dict], dict]:
    world = _world_index(world_rows)
    rows = []
    for neighbor in neighbor_rows:
        target_family = str(neighbor.get("target_family", "-") or "-")
        reference_family = str(neighbor.get("reference_family", "-") or "-")
        target = world.get(target_family, {})
        reference = world.get(reference_family, {})
        state = _relation_state(target, reference, neighbor)
        rows.append(
            {
                "target_family": target_family,
                "reference_family": reference_family,
                "neighbor_consequence_state": state,
                "sensor_distance": round(_safe_float(neighbor.get("sensor_distance", 0.0)), 6),
                "sensor_similarity": round(_safe_float(neighbor.get("sensor_similarity", 0.0)), 6),
                "target_reward_sum": round(_safe_float(target.get("reward_sum", neighbor.get("target_reward_sum", 0.0))), 6),
                "reference_reward_sum": round(
                    _safe_float(reference.get("reward_sum", neighbor.get("reference_reward_sum", 0.0))), 6
                ),
                "target_executed_rows": _safe_int(target.get("executed_rows", neighbor.get("target_executed_rows", 0))),
                "target_observed_rows": _safe_int(target.get("observed_rows", neighbor.get("target_observed_rows", 0))),
                "reference_executed_rows": _safe_int(
                    reference.get("executed_rows", neighbor.get("reference_executed_rows", 0))
                ),
                "reference_observed_rows": _safe_int(
                    reference.get("observed_rows", neighbor.get("reference_observed_rows", 0))
                ),
                "target_class": str(target.get("action_transition_class", "-") or "-"),
                "reference_class": str(reference.get("action_transition_class", "-") or "-"),
                "target_phases": str(target.get("phases", neighbor.get("target_phases", "-")) or "-"),
                "reference_phases": str(reference.get("phases", neighbor.get("reference_phases", "-")) or "-"),
            }
        )
    rows.sort(
        key=lambda item: (
            item["neighbor_consequence_state"] == "reifende_verwandtschaft",
            item["neighbor_consequence_state"] == "beobachtete_verwandtschaft",
            item["neighbor_consequence_state"] == "vorsichtige_verwandtschaft",
            item["sensor_similarity"],
            item["target_reward_sum"],
        ),
        reverse=True,
    )
    counts: dict[str, int] = {}
    by_target: dict[str, list[dict]] = {}
    for row in rows:
        state = str(row["neighbor_consequence_state"])
        counts[state] = counts.get(state, 0) + 1
        by_target.setdefault(str(row["target_family"]), []).append(row)
    overview = {
        "state_counts": counts,
        "top_by_target": {
            family: values[:3]
            for family, values in sorted(by_target.items())
        },
    }
    return rows, overview


def _write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(rows: list[dict], overview: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_neighbor_consequence.json").write_text(
        json.dumps(rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "dio_mini_neighbor_consequence_overview.json").write_text(
        json.dumps(overview, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    _write_csv(output_dir / "dio_mini_neighbor_consequence.csv", rows)
    lines = ["# DIO Mini Neighbor Consequence", ""]
    lines.append("## States")
    for key, value in sorted(dict(overview.get("state_counts", {}) or {}).items()):
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Top By Target")
    for family, values in sorted(dict(overview.get("top_by_target", {}) or {}).items()):
        lines.append(f"### {family}")
        for row in values:
            lines.append(
                f"- {row['reference_family']}: {row['neighbor_consequence_state']}, "
                f"similarity={row['sensor_similarity']}, "
                f"target_reward={row['target_reward_sum']}, "
                f"reference_reward={row['reference_reward_sum']}"
            )
        lines.append("")
    (output_dir / "dio_mini_neighbor_consequence.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze passive DIO mini neighbor consequences")
    parser.add_argument("--neighbors", required=True)
    parser.add_argument("--world-summary", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    neighbor_rows = _read_rows(Path(args.neighbors))
    world_rows = _read_rows(Path(args.world_summary))
    rows, overview = analyze(neighbor_rows, world_rows)
    write_outputs(rows, overview, Path(args.output_dir))
    for key, value in sorted(dict(overview.get("state_counts", {}) or {}).items()):
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
