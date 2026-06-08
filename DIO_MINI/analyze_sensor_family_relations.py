"""Find passive sensor-near DIO mini family relations."""

from __future__ import annotations

import argparse
import csv
import json
from itertools import combinations
from pathlib import Path


VECTOR_FIELDS = (
    "avg_sehen_form_flow",
    "avg_sehen_form_stability",
    "avg_sehen_form_change",
    "avg_hoeren_energy_tone",
    "avg_hoeren_energy_shift",
    "avg_fuehlen_mcm_coherence",
    "avg_fuehlen_mcm_tension",
    "avg_fuehlen_mcm_asymmetry",
)


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


def _read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _vector(row: dict) -> list[float]:
    return [_safe_float(row.get(field, 0.0)) for field in VECTOR_FIELDS]


def _distance(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 1.0
    return sum(abs(a - b) for a, b in zip(left, right)) / max(1, len(left))


def _relation_trace(distance: float) -> float:
    return max(0.0, min(1.0, 1.0 - float(distance)))


def analyze(sensor_csv: Path, min_relation_trace: float = 0.74) -> list[dict]:
    rows = _read_rows(sensor_csv)
    families = []
    for row in rows:
        family = str(row.get("family", "-") or "-")
        families.append(
            {
                "family": family,
                "phase": row.get("phase", row.get("phases", "-")),
                "phase_count": _safe_int(row.get("phase_count", 0)),
                "executed": _safe_int(row.get("executed", 0)),
                "positive_executed": _safe_int(row.get("positive_executed", 0)),
                "burdened_executed": _safe_int(row.get("burdened_executed", 0)),
                "observed_potential": _safe_int(row.get("observed_potential", 0)),
                "reward_sum": _safe_float(row.get("reward_sum", 0.0)),
                "visual_mcm": _safe_float(row.get("avg_visual_mcm_alignment_trace", 0.0)),
                "tone_tension": _safe_float(row.get("avg_tone_tension_resonance_trace", 0.0)),
                "vector": _vector(row),
            }
        )
    relations = []
    for left, right in combinations(families, 2):
        distance = _distance(left["vector"], right["vector"])
        trace = _relation_trace(distance)
        if trace < min_relation_trace:
            continue
        relation_kind = "quiet_sensor_neighbor"
        if left["family"] == right["family"] and (left["executed"] > 0 or right["executed"] > 0):
            relation_kind = "same_family_cross_phase"
        elif left["positive_executed"] > 0 and right["positive_executed"] > 0:
            relation_kind = "bearing_sensor_neighbor"
        elif (left["observed_potential"] > 0 and right["positive_executed"] > 0) or (
            right["observed_potential"] > 0 and left["positive_executed"] > 0
        ):
            relation_kind = "observation_to_bearing_neighbor"
        elif left["burdened_executed"] > 0 or right["burdened_executed"] > 0:
            relation_kind = "burdened_sensor_neighbor"
        relations.append(
            {
                "left_family": left["family"],
                "right_family": right["family"],
                "left_phase": left["phase"],
                "right_phase": right["phase"],
                "relation_kind": relation_kind,
                "left_phase_count": left["phase_count"],
                "right_phase_count": right["phase_count"],
                "left_executed": left["executed"],
                "right_executed": right["executed"],
                "left_positive_executed": left["positive_executed"],
                "right_positive_executed": right["positive_executed"],
                "left_burdened_executed": left["burdened_executed"],
                "right_burdened_executed": right["burdened_executed"],
                "left_observed": left["observed_potential"],
                "right_observed": right["observed_potential"],
                "left_reward": round(left["reward_sum"], 6),
                "right_reward": round(right["reward_sum"], 6),
                "sensor_relation_trace": round(trace, 6),
                "sensor_distance": round(distance, 6),
                "visual_mcm_gap": round(abs(left["visual_mcm"] - right["visual_mcm"]), 6),
                "tone_tension_gap": round(abs(left["tone_tension"] - right["tone_tension"]), 6),
            }
        )
    relations.sort(
        key=lambda item: (
            item["relation_kind"] == "same_family_cross_phase",
            item["relation_kind"] == "bearing_sensor_neighbor",
            item["relation_kind"] == "observation_to_bearing_neighbor",
            item["sensor_relation_trace"],
            item["left_phase_count"] + item["right_phase_count"],
            item["left_executed"] + item["right_executed"],
            item["left_reward"] + item["right_reward"],
        ),
        reverse=True,
    )
    return relations


def write_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_sensor_family_relations.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    if rows:
        with (output_dir / "dio_mini_sensor_family_relations.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze passive sensor-near DIO mini families")
    parser.add_argument("--sensor-csv", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--min-relation-trace", type=float, default=0.74)
    args = parser.parse_args()

    rows = analyze(Path(args.sensor_csv), min_relation_trace=float(args.min_relation_trace))
    write_outputs(rows, Path(args.output_dir))
    for row in rows[:20]:
        print(
            f"{row['left_family']} <-> {row['right_family']} "
            f"kind={row['relation_kind']} trace={row['sensor_relation_trace']:.4f} "
            f"phases={row['left_phase']}/{row['right_phase']} rewards={row['left_reward']:.4f}/{row['right_reward']:.4f} "
            f"exec={row['left_executed']}/{row['right_executed']}"
        )


if __name__ == "__main__":
    main()
