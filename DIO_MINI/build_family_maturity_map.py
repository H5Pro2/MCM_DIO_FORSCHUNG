"""Build a passive compact maturity map for DIO mini families."""

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
        return int(value)
    except Exception:
        return default


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _notes(row: dict) -> str:
    notes = []
    if _safe_int(row.get("phase_count", 0)) > 1:
        notes.append("weltuebergreifend")
    if _safe_int(row.get("executed_runs", row.get("executed", 0))) > 0:
        notes.append("ausgefuehrt")
    if _safe_int(row.get("observed_runs", row.get("observed_potential", 0))) > 0:
        notes.append("beobachtet")
    if _safe_int(row.get("held_runs", 0)) > 0:
        notes.append("nachhall_gehalten")
    if _safe_float(row.get("reward_sum", 0.0)) > 0.0:
        notes.append("positive_konsequenz")
    if _safe_float(row.get("reward_sum", 0.0)) < 0.0:
        notes.append("belastete_konsequenz")
    if _safe_int(row.get("bearing_neighbor_count", 0)) > 0:
        notes.append("sensorische_nachbarn")
    if _safe_int(row.get("same_family_relation_count", 0)) > 0:
        notes.append("gleiche_familie_ueber_phasen")
    return "|".join(notes) if notes else "ruhige_spur"


def build_map(persistence_csv: Path, sensor_csv: Path, relation_csv: Path) -> list[dict]:
    persistence_rows = _read_csv(persistence_csv)
    sensor_rows = _read_csv(sensor_csv)
    relation_rows = _read_csv(relation_csv)
    by_family: dict[str, dict] = {}

    for row in persistence_rows:
        family = str(row.get("family", "-") or "-")
        item = by_family.setdefault(family, {"family": family})
        item.update(
            {
                "phases": row.get("phases", "-"),
                "phase_count": _safe_int(row.get("phase_count", 0)),
                "dominant_transition": row.get("dominant_transition", "-"),
                "executed_runs": _safe_int(row.get("executed_runs", 0)),
                "observed_runs": _safe_int(row.get("observed_runs", 0)),
                "held_runs": _safe_int(row.get("held_runs", 0)),
                "raw_runs": _safe_int(row.get("raw_runs", 0)),
                "reward_sum": _safe_float(row.get("reward_sum", 0.0)),
                "max_trade_readiness": _safe_float(row.get("max_trade_readiness", 0.0)),
                "max_mature_transfer": _safe_float(row.get("max_mature_transfer", 0.0)),
            }
        )

    for row in sensor_rows:
        family = str(row.get("family", "-") or "-")
        item = by_family.setdefault(family, {"family": family})
        item.update(
            {
                "sensor_phases": row.get("phases", item.get("phases", "-")),
                "sensor_phase_count": _safe_int(row.get("phase_count", 0)),
                "sensor_rows": _safe_int(row.get("rows", 0)),
                "sensor_executed": _safe_int(row.get("executed", 0)),
                "sensor_observed": _safe_int(row.get("observed_potential", 0)),
                "avg_visual_mcm_alignment_trace": _safe_float(row.get("avg_visual_mcm_alignment_trace", 0.0)),
                "avg_tone_tension_resonance_trace": _safe_float(row.get("avg_tone_tension_resonance_trace", 0.0)),
            }
        )

    relation_counts: dict[str, dict] = {}
    for row in relation_rows:
        left = str(row.get("left_family", "-") or "-")
        right = str(row.get("right_family", "-") or "-")
        kind = str(row.get("relation_kind", "-") or "-")
        for family in (left, right):
            record = relation_counts.setdefault(
                family,
                {
                    "sensor_relation_count": 0,
                    "bearing_neighbor_count": 0,
                    "same_family_relation_count": 0,
                    "max_sensor_relation_trace": 0.0,
                },
            )
            record["sensor_relation_count"] += 1
            if kind == "bearing_sensor_neighbor":
                record["bearing_neighbor_count"] += 1
            if kind == "same_family_cross_phase":
                record["same_family_relation_count"] += 1
            record["max_sensor_relation_trace"] = max(
                record["max_sensor_relation_trace"],
                _safe_float(row.get("sensor_relation_trace", 0.0)),
            )

    rows = []
    for family, item in by_family.items():
        item.update(
            {
                "sensor_relation_count": 0,
                "bearing_neighbor_count": 0,
                "same_family_relation_count": 0,
                "max_sensor_relation_trace": 0.0,
                **relation_counts.get(family, {}),
            }
        )
        executed = max(1, _safe_int(item.get("executed_runs", item.get("sensor_executed", 0))))
        item["reward_per_executed_run"] = round(_safe_float(item.get("reward_sum", 0.0)) / executed, 6)
        item["trace_notes"] = _notes(item)
        rows.append(
            {
                "family": family,
                "trace_notes": item.get("trace_notes", "-"),
                "phases": item.get("phases", item.get("sensor_phases", "-")),
                "phase_count": _safe_int(item.get("phase_count", item.get("sensor_phase_count", 0))),
                "dominant_transition": item.get("dominant_transition", "-"),
                "executed_runs": _safe_int(item.get("executed_runs", item.get("sensor_executed", 0))),
                "observed_runs": _safe_int(item.get("observed_runs", item.get("sensor_observed", 0))),
                "held_runs": _safe_int(item.get("held_runs", 0)),
                "raw_runs": _safe_int(item.get("raw_runs", 0)),
                "reward_sum": round(_safe_float(item.get("reward_sum", 0.0)), 6),
                "reward_per_executed_run": item["reward_per_executed_run"],
                "avg_visual_mcm_alignment_trace": round(_safe_float(item.get("avg_visual_mcm_alignment_trace", 0.0)), 6),
                "avg_tone_tension_resonance_trace": round(_safe_float(item.get("avg_tone_tension_resonance_trace", 0.0)), 6),
                "sensor_relation_count": _safe_int(item.get("sensor_relation_count", 0)),
                "bearing_neighbor_count": _safe_int(item.get("bearing_neighbor_count", 0)),
                "same_family_relation_count": _safe_int(item.get("same_family_relation_count", 0)),
                "max_sensor_relation_trace": round(_safe_float(item.get("max_sensor_relation_trace", 0.0)), 6),
            }
        )

    rows.sort(
        key=lambda item: (
            item["phase_count"],
            item["reward_sum"],
            item["executed_runs"],
            item["bearing_neighbor_count"],
            item["same_family_relation_count"],
        ),
        reverse=True,
    )
    return rows


def write_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_family_maturity_map.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    if rows:
        with (output_dir / "dio_mini_family_maturity_map.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive DIO mini family maturity map")
    parser.add_argument("--persistence-csv", required=True)
    parser.add_argument("--sensor-csv", required=True)
    parser.add_argument("--relations-csv", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    rows = build_map(Path(args.persistence_csv), Path(args.sensor_csv), Path(args.relations_csv))
    write_outputs(rows, Path(args.output_dir))
    for row in rows[:16]:
        print(
            f"family={row['family']} notes={row['trace_notes']} phases={row['phase_count']} "
            f"reward={row['reward_sum']:.4f} sensor_neighbors={row['bearing_neighbor_count']}"
        )


if __name__ == "__main__":
    main()
