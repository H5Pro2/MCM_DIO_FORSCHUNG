"""Inspect one passive Mini-DIO cluster island.

The report compares two syntax families from a meaning-space CSV and, when
available, their neighbor relation. It separates shared carried traces from
drift traces.

Diagnostic only: no runtime memory, no action influence.
"""

from __future__ import annotations

import argparse
import csv
import json
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

TRACE_FIELDS = {
    "sehen": [
        "avg_sehen_form_flow",
        "avg_sehen_form_stability",
        "avg_sehen_form_change",
    ],
    "hoeren": [
        "avg_hoeren_energy_tone",
        "avg_hoeren_energy_shift",
    ],
    "fuehlen_mcm": [
        "avg_fuehlen_mcm_coherence",
        "avg_fuehlen_mcm_tension",
        "avg_fuehlen_mcm_asymmetry",
    ],
    "zeit_nachhall": [
        "avg_mini_recurrence_strength",
        "avg_mini_afterimage",
        "avg_mini_time_distance",
        "avg_mini_temporal_form_distance",
        "avg_mini_temporal_trust_support",
        "avg_mini_temporal_caution_support",
    ],
    "neuro": [
        "avg_mini_focus_tone",
        "avg_mini_trust_tone",
        "avg_mini_caution_tone",
        "avg_mini_strain_tone",
        "avg_mini_relief_tone",
        "avg_mini_observation_tone",
        "avg_mini_neuro_support",
        "avg_mini_neuro_load",
        "avg_mini_neuro_balance",
    ],
    "reflexion": [
        "avg_reflection_context_carry",
        "avg_reflection_context_strain",
        "avg_reflection_context_alignment",
        "avg_reflection_world_support",
        "avg_reflection_current_support",
    ],
    "reife_kontext": [
        "candidate_meaning_preservation_rate",
        "candidate_stable_recurrence_rate",
        "candidate_variant_capacity_rate",
        "candidate_temporal_fragility",
    ],
}


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


def _distance(left: dict, right: dict, fields: list[str]) -> float:
    if not fields:
        return 0.0
    return sum(abs(_safe_float(left.get(field)) - _safe_float(right.get(field))) for field in fields) / len(fields)


def _similarity(distance: float) -> float:
    return 1.0 / (1.0 + (float(distance) * float(distance) * 8.0))


def _read_family(rows: list[dict], family: str) -> dict:
    for row in rows:
        if str(row.get("symbol_family", "") or "") == family:
            return dict(row)
    return {}


def _read_neighbor(rows: list[dict], left_family: str, right_family: str) -> dict:
    for row in rows:
        left = str(row.get("left_family", "") or "")
        right = str(row.get("right_family", "") or "")
        if {left, right} == {left_family, right_family}:
            return dict(row)
    return {}


def _trace_state(distance: float) -> str:
    sim = _similarity(distance)
    if sim >= 0.98:
        return "gemeinsame_spur"
    if sim >= 0.90:
        return "nahe_spur"
    if sim >= 0.78:
        return "driftende_spur"
    return "getrennte_spur"


def build_lupe(meaning_rows: list[dict], neighbor_rows: list[dict], left_family: str, right_family: str) -> tuple[list[dict], list[dict]]:
    left = _read_family(meaning_rows, left_family)
    right = _read_family(meaning_rows, right_family)
    if not left or not right:
        return [], []
    neighbor = _read_neighbor(neighbor_rows, left_family, right_family)

    traces: list[dict] = []
    for group, fields in TRACE_FIELDS.items():
        distance = _distance(left, right, fields)
        similarity = _similarity(distance)
        field_rows = []
        for field in fields:
            left_value = _safe_float(left.get(field))
            right_value = _safe_float(right.get(field))
            field_rows.append(
                {
                    "trace_group": group,
                    "field": field,
                    "left_family": left_family,
                    "right_family": right_family,
                    "left_value": round(left_value, 6),
                    "right_value": round(right_value, 6),
                    "abs_delta": round(abs(left_value - right_value), 6),
                    "trace_state": _trace_state(abs(left_value - right_value)),
                    **BOUNDARY,
                }
            )
        traces.extend(field_rows)
        traces.append(
            {
                "trace_group": group,
                "field": "__group_summary__",
                "left_family": left_family,
                "right_family": right_family,
                "left_value": "",
                "right_value": "",
                "abs_delta": round(distance, 6),
                "trace_similarity": round(similarity, 6),
                "trace_state": _trace_state(distance),
                **BOUNDARY,
            }
        )

    overview = [
        {
            "left_family": left_family,
            "right_family": right_family,
            "left_symbol_count": left.get("symbol_count", ""),
            "right_symbol_count": right.get("symbol_count", ""),
            "left_episode_count": left.get("episode_count", ""),
            "right_episode_count": right.get("episode_count", ""),
            "left_reife_state": left.get("candidate_passive_reife_state", ""),
            "right_reife_state": right.get("candidate_passive_reife_state", ""),
            "left_recurrence_symbol": left.get("candidate_recurrence_maturity_symbol", ""),
            "right_recurrence_symbol": right.get("candidate_recurrence_maturity_symbol", ""),
            "neighbor_state": neighbor.get("neighbor_state", ""),
            "meaning_similarity": neighbor.get("meaning_similarity", ""),
            "sense_similarity": neighbor.get("sense_similarity", ""),
            "mcm_similarity": neighbor.get("mcm_similarity", ""),
            "hearing_similarity": neighbor.get("hearing_similarity", ""),
            "temporal_similarity": neighbor.get("temporal_similarity", ""),
            "neuro_similarity": neighbor.get("neuro_similarity", ""),
            "reflection_similarity": neighbor.get("reflection_similarity", ""),
            "reife_similarity": neighbor.get("reife_similarity", ""),
            "shared_reading": _shared_reading(left, right, neighbor),
            **BOUNDARY,
        }
    ]
    return overview, traces


def _shared_reading(left: dict, right: dict, neighbor: dict) -> str:
    left_family = str(left.get("symbol_family", "") or "")
    right_family = str(right.get("symbol_family", "") or "")
    meaning_similarity = _safe_float(neighbor.get("meaning_similarity"))
    mcm_similarity = _safe_float(neighbor.get("mcm_similarity"))
    hearing_similarity = _safe_float(neighbor.get("hearing_similarity"))
    left_reife = str(left.get("candidate_passive_reife_state", "") or "")
    right_reife = str(right.get("candidate_passive_reife_state", "") or "")
    if meaning_similarity >= 0.98 and mcm_similarity >= 0.99 and hearing_similarity >= 0.99:
        core = "gemeinsame Form-/MCM-/Energiespur"
    elif meaning_similarity >= 0.90:
        core = "nahe Bedeutungsnaehe"
    else:
        core = "schwache Bedeutungsnaehe"
    if left_reife and not right_reife:
        reife = f"{left_family} hat Reifekontext, {right_family} ist noch rohe Nachbarspur"
    elif left_reife == right_reife and left_reife:
        reife = "beide tragen denselben Reifekontext"
    else:
        reife = "Reifekontext driftet oder fehlt"
    return f"{left_family}+{right_family}: {core}; {reife}. Passive Insel-Lupe, keine Handlung."


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    if rows:
        fields = []
        for row in rows:
            for key in row.keys():
                if key not in fields:
                    fields.append(key)
    else:
        fields = fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(overview: list[dict], traces: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    overview_path = output_dir / "passive_cluster_island_lupe_overview.csv"
    traces_path = output_dir / "passive_cluster_island_lupe_traces.csv"
    json_path = output_dir / "passive_cluster_island_lupe.json"
    md_path = output_dir / "README.md"
    _write_csv(overview_path, overview, ["left_family", "right_family"])
    _write_csv(traces_path, traces, ["trace_group", "field"])
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_cluster_island_lupe.v1",
                "boundary": BOUNDARY,
                "overview": overview,
                "traces": traces,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# Mini-DIO passive Cluster-Insel-Lupe",
        "",
        "Ziel: eine emergente Bedeutungsinsel als gemeinsame und driftende Spur lesen.",
        "",
        "## Grenze",
        "- Nur Bericht.",
        "- Keine Runtime-Rueckfuehrung.",
        "- Keine Handlung.",
        "- Kein Gate.",
        "- Kein Trainingsmemory.",
        "",
        "## Insel",
    ]
    if overview:
        row = overview[0]
        lines.append(f"- {row['shared_reading']}")
        lines.append(f"- meaning_similarity: {row.get('meaning_similarity', '')}")
        lines.append(f"- mcm_similarity: {row.get('mcm_similarity', '')}")
        lines.append(f"- hearing_similarity: {row.get('hearing_similarity', '')}")
        lines.append(f"- reife_similarity: {row.get('reife_similarity', '')}")
    lines.extend(["", "## Spuren"])
    for row in traces:
        if row.get("field") == "__group_summary__":
            lines.append(
                f"- {row['trace_group']}: {row['trace_state']} "
                f"similarity={row.get('trace_similarity', '')}"
            )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive Mini-DIO cluster island lupe")
    parser.add_argument("--meaning-space", required=True, type=Path)
    parser.add_argument("--neighbors", required=True, type=Path)
    parser.add_argument("--left-family", required=True)
    parser.add_argument("--right-family", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    overview, traces = build_lupe(
        _read_csv(args.meaning_space),
        _read_csv(args.neighbors),
        args.left_family,
        args.right_family,
    )
    write_outputs(overview, traces, args.output_dir)
    print(
        json.dumps(
            {
                "overview_rows": len(overview),
                "trace_rows": len(traces),
                "output_dir": str(args.output_dir),
                **BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
