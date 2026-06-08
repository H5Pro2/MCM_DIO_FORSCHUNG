"""Build passive neighbor relations between Mini-DIO meaning-space clusters.

The input is the CSV produced by report_passive_cluster_meaning_space.py.
The output describes which syntax families are close in carried meaning:
visual form, auditory energy, MCM feeling, temporal trace, neuro tone, and
passive recurrence context.

Diagnostic only: no runtime memory, no action influence.
"""

from __future__ import annotations

import argparse
import csv
import json
from itertools import combinations
from pathlib import Path


BOUNDARY = {
    "passive_only": True,
    "writes_runtime_memory": False,
    "read_by_mini_dio": False,
    "influences_action": False,
    "is_gate": False,
    "is_motoric": False,
    "is_entry_signal": False,
    "is_direction_signal": False,
}

SENSE_KEYS = [
    "avg_sehen_form_flow",
    "avg_sehen_form_stability",
    "avg_sehen_form_change",
    "avg_hoeren_energy_tone",
    "avg_hoeren_energy_shift",
    "avg_fuehlen_mcm_coherence",
    "avg_fuehlen_mcm_tension",
    "avg_fuehlen_mcm_asymmetry",
]

TEMPORAL_KEYS = [
    "avg_mini_recurrence_strength",
    "avg_mini_afterimage",
    "avg_mini_time_distance",
    "avg_mini_temporal_form_distance",
    "avg_mini_temporal_trust_support",
    "avg_mini_temporal_caution_support",
]

NEURO_KEYS = [
    "avg_mini_focus_tone",
    "avg_mini_trust_tone",
    "avg_mini_caution_tone",
    "avg_mini_strain_tone",
    "avg_mini_relief_tone",
    "avg_mini_observation_tone",
    "avg_mini_neuro_support",
    "avg_mini_neuro_load",
    "avg_mini_neuro_balance",
]

REFLECTION_KEYS = [
    "avg_reflection_context_carry",
    "avg_reflection_context_strain",
    "avg_reflection_context_alignment",
    "avg_reflection_world_support",
    "avg_reflection_current_support",
]

REIFE_KEYS = [
    "candidate_meaning_preservation_rate",
    "candidate_stable_recurrence_rate",
    "candidate_variant_capacity_rate",
    "candidate_temporal_fragility",
]


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value or default)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(float(value or default))
    except Exception:
        return default


def _distance(left: dict, right: dict, keys: list[str]) -> float:
    if not keys:
        return 0.0
    return sum(abs(_safe_float(left.get(key)) - _safe_float(right.get(key))) for key in keys) / len(keys)


def _similarity(distance: float) -> float:
    return 1.0 / (1.0 + (float(distance) * float(distance) * 8.0))


def _state_relation(left: str, right: str) -> str:
    left = str(left or "-")
    right = str(right or "-")
    if left == right:
        return "same_state"
    if "-" in {left, right} or "" in {left, right}:
        return "state_missing"
    return "state_drift"


def _neighbor_state(row: dict) -> str:
    meaning = _safe_float(row.get("meaning_similarity"))
    sense = _safe_float(row.get("sense_similarity"))
    field = _safe_float(row.get("mcm_similarity"))
    temporal = _safe_float(row.get("temporal_similarity"))
    reife_relation = str(row.get("reife_state_relation", "") or "")
    if meaning >= 0.96 and field >= 0.96 and reife_relation == "same_state":
        return "passive_same_meaning_island"
    if meaning >= 0.90 and sense >= 0.88 and field >= 0.88:
        return "passive_near_meaning_neighbor"
    if field >= 0.90 and temporal < 0.82:
        return "same_field_temporal_drift"
    if sense >= 0.90 and field < 0.82:
        return "same_form_different_field"
    if meaning >= 0.80:
        return "weak_meaning_kinship"
    return "distant_or_noise"


def _sentence(row: dict) -> str:
    left = str(row.get("left_family", "") or "")
    right = str(row.get("right_family", "") or "")
    state = str(row.get("neighbor_state", "") or "")
    if state == "passive_same_meaning_island":
        return f"{left}+{right}: gleiche passive Bedeutungsinsel, ohne Handlung."
    if state == "passive_near_meaning_neighbor":
        return f"{left}+{right}: nahe Sinnspur; Form, Feld und Energie liegen beieinander."
    if state == "same_field_temporal_drift":
        return f"{left}+{right}: aehnliche Feldwirkung, aber zeitlich driftend."
    if state == "same_form_different_field":
        return f"{left}+{right}: aehnliche Form, aber anderes inneres Feld."
    if state == "weak_meaning_kinship":
        return f"{left}+{right}: schwache Verwandtschaft im Bedeutungsraum."
    return f"{left}+{right}: keine tragende passive Naehe sichtbar."


def build_neighbors(rows: list[dict], families: set[str], topn: int) -> tuple[list[dict], list[dict]]:
    selected_rows = [row for row in rows if not families or str(row.get("symbol_family", "") or "") in families]
    reference_rows = rows
    pairs: list[dict] = []

    if families:
        iterator = (
            (left, right)
            for left in selected_rows
            for right in reference_rows
            if str(left.get("symbol_family", "") or "") != str(right.get("symbol_family", "") or "")
        )
    else:
        iterator = combinations(reference_rows, 2)

    seen: set[tuple[str, str]] = set()
    for left, right in iterator:
        left_family = str(left.get("symbol_family", "") or "")
        right_family = str(right.get("symbol_family", "") or "")
        if not left_family or not right_family:
            continue
        key = tuple(sorted([left_family, right_family]))
        if key in seen:
            continue
        seen.add(key)
        sense_distance = _distance(left, right, SENSE_KEYS)
        mcm_distance = _distance(
            left,
            right,
            ["avg_fuehlen_mcm_coherence", "avg_fuehlen_mcm_tension", "avg_fuehlen_mcm_asymmetry"],
        )
        hearing_distance = _distance(left, right, ["avg_hoeren_energy_tone", "avg_hoeren_energy_shift"])
        temporal_distance = _distance(left, right, TEMPORAL_KEYS)
        neuro_distance = _distance(left, right, NEURO_KEYS)
        reflection_distance = _distance(left, right, REFLECTION_KEYS)
        reife_distance = _distance(left, right, REIFE_KEYS)
        total_distance = (
            (sense_distance * 0.24)
            + (mcm_distance * 0.22)
            + (hearing_distance * 0.12)
            + (temporal_distance * 0.14)
            + (neuro_distance * 0.14)
            + (reflection_distance * 0.08)
            + (reife_distance * 0.06)
        )
        row = {
            "left_family": left_family,
            "right_family": right_family,
            "left_episodes": _safe_int(left.get("episode_count")),
            "right_episodes": _safe_int(right.get("episode_count")),
            "left_reife_state": str(left.get("candidate_passive_reife_state", "") or ""),
            "right_reife_state": str(right.get("candidate_passive_reife_state", "") or ""),
            "reife_state_relation": _state_relation(
                str(left.get("candidate_passive_reife_state", "") or ""),
                str(right.get("candidate_passive_reife_state", "") or ""),
            ),
            "left_neuro_tone": str(left.get("dominant_neuro_tone", "") or ""),
            "right_neuro_tone": str(right.get("dominant_neuro_tone", "") or ""),
            "neuro_tone_relation": _state_relation(
                str(left.get("dominant_neuro_tone", "") or ""),
                str(right.get("dominant_neuro_tone", "") or ""),
            ),
            "left_action": str(left.get("dominant_action", "") or ""),
            "right_action": str(right.get("dominant_action", "") or ""),
            "action_relation": _state_relation(
                str(left.get("dominant_action", "") or ""),
                str(right.get("dominant_action", "") or ""),
            ),
            "sense_distance": round(sense_distance, 6),
            "sense_similarity": round(_similarity(sense_distance), 6),
            "mcm_distance": round(mcm_distance, 6),
            "mcm_similarity": round(_similarity(mcm_distance), 6),
            "hearing_distance": round(hearing_distance, 6),
            "hearing_similarity": round(_similarity(hearing_distance), 6),
            "temporal_distance": round(temporal_distance, 6),
            "temporal_similarity": round(_similarity(temporal_distance), 6),
            "neuro_distance": round(neuro_distance, 6),
            "neuro_similarity": round(_similarity(neuro_distance), 6),
            "reflection_distance": round(reflection_distance, 6),
            "reflection_similarity": round(_similarity(reflection_distance), 6),
            "reife_distance": round(reife_distance, 6),
            "reife_similarity": round(_similarity(reife_distance), 6),
            "meaning_distance": round(total_distance, 6),
            "meaning_similarity": round(_similarity(total_distance), 6),
            **BOUNDARY,
        }
        row["neighbor_state"] = _neighbor_state(row)
        row["dio_neighbor_sentence"] = _sentence(row)
        pairs.append(row)

    pairs.sort(
        key=lambda row: (
            -_safe_float(row.get("meaning_similarity")),
            str(row.get("left_family", "")),
            str(row.get("right_family", "")),
        )
    )
    if topn > 0:
        pairs = pairs[:topn]

    groups: dict[str, dict] = {}
    for row in pairs:
        state = str(row.get("neighbor_state", "") or "-")
        group = groups.setdefault(
            state,
            {
                "neighbor_state": state,
                "pair_count": 0,
                "families": set(),
                "max_meaning_similarity": 0.0,
                "avg_meaning_similarity_sum": 0.0,
            },
        )
        group["pair_count"] += 1
        group["families"].add(str(row.get("left_family", "") or ""))
        group["families"].add(str(row.get("right_family", "") or ""))
        sim = _safe_float(row.get("meaning_similarity"))
        group["max_meaning_similarity"] = max(float(group["max_meaning_similarity"]), sim)
        group["avg_meaning_similarity_sum"] += sim

    summary = []
    for group in groups.values():
        pair_count = max(1, int(group["pair_count"]))
        summary.append(
            {
                "neighbor_state": group["neighbor_state"],
                "pair_count": pair_count,
                "family_count": len(group["families"]),
                "families": "|".join(sorted(group["families"])),
                "max_meaning_similarity": round(float(group["max_meaning_similarity"]), 6),
                "avg_meaning_similarity": round(float(group["avg_meaning_similarity_sum"]) / pair_count, 6),
                **BOUNDARY,
            }
        )
    summary.sort(key=lambda row: (-int(row["pair_count"]), str(row["neighbor_state"])))
    return pairs, summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(pairs: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    pairs_path = output_dir / "passive_cluster_neighbors.csv"
    summary_path = output_dir / "passive_cluster_neighbors_summary.csv"
    json_path = output_dir / "passive_cluster_neighbors.json"
    md_path = output_dir / "README.md"
    _write_csv(pairs_path, pairs, ["left_family", "right_family", "neighbor_state"])
    _write_csv(summary_path, summary, ["neighbor_state", "pair_count"])
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_cluster_neighbors.v1",
                "boundary": BOUNDARY,
                "pairs": pairs,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# Mini-DIO passive Cluster-Nachbarschaften",
        "",
        "Ziel: emergente Bedeutungsinseln zwischen Syntax-Clustern sichtbar machen.",
        "",
        "## Grenze",
        "- Nur Bericht.",
        "- Keine Runtime-Rueckfuehrung.",
        "- Keine Handlung.",
        "- Kein Gate.",
        "- Kein Trainingsmemory.",
        "",
        "## Summary",
    ]
    for row in summary:
        lines.append(
            f"- {row['neighbor_state']}: pairs={row['pair_count']} "
            f"max_similarity={row['max_meaning_similarity']}"
        )
    lines.extend(["", "## Naechste Nachbarn"])
    for row in pairs[:30]:
        lines.append(
            f"- {row['dio_neighbor_sentence']} "
            f"similarity={row['meaning_similarity']}"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive Mini-DIO cluster neighbor report")
    parser.add_argument("--meaning-space", required=True, type=Path)
    parser.add_argument("--family", nargs="*", default=[])
    parser.add_argument("--topn", type=int, default=120)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    rows = _read_csv(args.meaning_space)
    pairs, summary = build_neighbors(rows, set(args.family or []), max(0, int(args.topn)))
    write_outputs(pairs, summary, args.output_dir)
    print(
        json.dumps(
            {
                "pairs": len(pairs),
                "summary_states": len(summary),
                "output_dir": str(args.output_dir),
                **BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
