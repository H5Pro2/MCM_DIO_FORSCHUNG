"""Analyze passive sensor-neighborhood between DIO mini families.

This tool compares family-level seeing/hearing/feeling signatures. It does not
change memory, motorics, or action scores.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


SENSE_FIELDS = (
    "sehen_form_flow",
    "sehen_form_stability",
    "sehen_form_change",
    "hoeren_energy_tone",
    "hoeren_energy_shift",
    "fuehlen_mcm_coherence",
    "fuehlen_mcm_tension",
    "fuehlen_mcm_asymmetry",
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
        return int(float(value))
    except Exception:
        return default


def _read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _vector_from_row(row: dict) -> tuple[list[float], int]:
    executed = _safe_int(row.get("executed_rows", 0))
    observed = _safe_int(row.get("observed_rows", 0))
    prefix = "executed" if executed > 0 else "observed"
    weight = max(1, executed if executed > 0 else observed)
    return [_safe_float(row.get(f"{prefix}_{field}", 0.0)) for field in SENSE_FIELDS], weight


def _family_vectors(rows: list[dict]) -> dict[str, dict]:
    acc: dict[str, dict] = {}
    for row in rows:
        family = str(row.get("family", "-") or "-")
        if family == "-":
            continue
        vector, weight = _vector_from_row(row)
        record = acc.setdefault(
            family,
            {
                "family": family,
                "vector_sum": [0.0 for _ in SENSE_FIELDS],
                "weight": 0,
                "phases": set(),
                "reward_sum": 0.0,
                "executed_rows": 0,
                "observed_rows": 0,
            },
        )
        for index, value in enumerate(vector):
            record["vector_sum"][index] += value * weight
        record["weight"] += weight
        record["phases"].add(str(row.get("phase", "-") or "-"))
        record["reward_sum"] += _safe_float(row.get("reward_sum", 0.0))
        record["executed_rows"] += _safe_int(row.get("executed_rows", 0))
        record["observed_rows"] += _safe_int(row.get("observed_rows", 0))
    result = {}
    for family, record in acc.items():
        weight = max(1, int(record["weight"]))
        result[family] = {
            "family": family,
            "vector": [round(value / weight, 6) for value in record["vector_sum"]],
            "phases": sorted(record["phases"]),
            "reward_sum": round(record["reward_sum"], 6),
            "executed_rows": int(record["executed_rows"]),
            "observed_rows": int(record["observed_rows"]),
        }
    return result


def _distance(left: list[float], right: list[float]) -> float:
    return math.sqrt(sum((float(a) - float(b)) ** 2 for a, b in zip(left, right)) / max(1, len(SENSE_FIELDS)))


def build_neighbors(rows: list[dict], targets: set[str], references: set[str], top: int) -> tuple[list[dict], dict]:
    vectors = _family_vectors(rows)
    neighbor_rows = []
    for target in sorted(targets):
        target_record = vectors.get(target)
        if not target_record:
            continue
        candidates = []
        for reference in sorted(references):
            ref_record = vectors.get(reference)
            if not ref_record or reference == target:
                continue
            dist = _distance(target_record["vector"], ref_record["vector"])
            candidates.append(
                {
                    "target_family": target,
                    "reference_family": reference,
                    "sensor_distance": round(dist, 6),
                    "sensor_similarity": round(max(0.0, 1.0 - dist), 6),
                    "target_reward_sum": target_record["reward_sum"],
                    "reference_reward_sum": ref_record["reward_sum"],
                    "target_phases": ",".join(target_record["phases"]),
                    "reference_phases": ",".join(ref_record["phases"]),
                    "target_executed_rows": target_record["executed_rows"],
                    "reference_executed_rows": ref_record["executed_rows"],
                    "target_observed_rows": target_record["observed_rows"],
                    "reference_observed_rows": ref_record["observed_rows"],
                }
            )
        candidates.sort(key=lambda item: (item["sensor_distance"], -item["reference_reward_sum"]))
        neighbor_rows.extend(candidates[: max(1, int(top))])
    overview = {
        "targets": sorted(targets),
        "references": sorted(references),
        "top_neighbors": neighbor_rows[: max(1, int(top)) * max(1, len(targets))],
    }
    return neighbor_rows, overview


def _write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(rows: list[dict], overview: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_family_sense_neighbors.json").write_text(
        json.dumps(rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "dio_mini_family_sense_neighbors_overview.json").write_text(
        json.dumps(overview, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    _write_csv(output_dir / "dio_mini_family_sense_neighbors.csv", rows)
    lines = ["# DIO Mini Family Sense Neighbors", ""]
    current = None
    for row in rows:
        if row["target_family"] != current:
            current = row["target_family"]
            lines.append(f"## {current}")
        lines.append(
            f"- {row['reference_family']}: distance={row['sensor_distance']}, "
            f"similarity={row['sensor_similarity']}, reference_reward={row['reference_reward_sum']}"
        )
    lines.append("")
    (output_dir / "dio_mini_family_sense_neighbors.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze passive DIO mini family sense neighbors")
    parser.add_argument("--phase-rows", required=True)
    parser.add_argument("--target", action="append", required=True)
    parser.add_argument("--reference", action="append", required=True)
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    rows = _read_rows(Path(args.phase_rows))
    neighbor_rows, overview = build_neighbors(rows, set(args.target), set(args.reference), args.top)
    write_outputs(neighbor_rows, overview, Path(args.output_dir))
    for row in neighbor_rows[: max(1, int(args.top)) * max(1, len(set(args.target)))]:
        print(
            f"{row['target_family']} -> {row['reference_family']} "
            f"distance={row['sensor_distance']:.6f} similarity={row['sensor_similarity']:.6f}"
        )


if __name__ == "__main__":
    main()
