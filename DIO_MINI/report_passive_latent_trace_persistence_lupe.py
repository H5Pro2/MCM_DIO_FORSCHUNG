"""Track passive latent trace persistence across controlled Mini-DIO stages.

The report follows one syntax family through multiple meaning-space and
semantic-matrix stages. It separates:

- visible trace: family appears in meaning-space
- coupled trace: family has current matrix edges to the watched base families
- island trace: family is part of any current semantic island
- latent trace: visible without current coupling

Passive only. No runtime memory, no action, no gate, no entry, no direction.
Designed for controlled datasets first, not for long-run claims.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any


BOUNDARY = {
    "passive_only": True,
    "controlled_dataset_scope": True,
    "long_run_claim": False,
    "writes_runtime_memory": False,
    "read_by_mini_dio": False,
    "influences_action": False,
    "is_gate": False,
    "is_motoric": False,
    "is_entry_signal": False,
    "is_direction_signal": False,
}

VECTOR_FIELDS = [
    "avg_sehen_form_flow",
    "avg_sehen_form_stability",
    "avg_sehen_form_change",
    "avg_hoeren_energy_tone",
    "avg_hoeren_energy_shift",
    "avg_fuehlen_mcm_coherence",
    "avg_fuehlen_mcm_tension",
    "avg_fuehlen_mcm_asymmetry",
    "avg_mini_recurrence_strength",
    "avg_mini_afterimage",
    "avg_mini_time_distance",
    "avg_mini_temporal_form_distance",
    "avg_mini_focus_tone",
    "avg_mini_trust_tone",
    "avg_mini_caution_tone",
    "avg_mini_strain_tone",
    "avg_mini_neuro_balance",
]

SENSE_GROUPS = {
    "sehen": ["avg_sehen_form_flow", "avg_sehen_form_stability", "avg_sehen_form_change"],
    "hoeren": ["avg_hoeren_energy_tone", "avg_hoeren_energy_shift"],
    "fuehlen_mcm": ["avg_fuehlen_mcm_coherence", "avg_fuehlen_mcm_tension", "avg_fuehlen_mcm_asymmetry"],
    "zeit": ["avg_mini_recurrence_strength", "avg_mini_afterimage", "avg_mini_time_distance", "avg_mini_temporal_form_distance"],
    "neuro": ["avg_mini_focus_tone", "avg_mini_trust_tone", "avg_mini_caution_tone", "avg_mini_strain_tone", "avg_mini_neuro_balance"],
}


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _write_csv(path: Path, rows: list[dict[str, Any]], fallback_fields: list[str]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    if not fields:
        fields = fallback_fields
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value if value not in (None, "") else default)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(float(value if value not in (None, "") else default))
    except Exception:
        return default


def _parse_stage(value: str) -> tuple[str, Path, Path]:
    parts = value.split("=", 2)
    if len(parts) != 3:
        raise ValueError(f"Stage must be LABEL=meaning_space_csv=matrix_dir: {value}")
    label = parts[0].strip()
    meaning = Path(parts[1].strip())
    matrix = Path(parts[2].strip())
    if not label:
        raise ValueError(f"Stage label is empty: {value}")
    return label, meaning, matrix


def _family_row(rows: list[dict[str, str]], family: str) -> dict[str, str]:
    for row in rows:
        if str(row.get("symbol_family", "") or "") == family:
            return row
    return {}


def _families(value: object) -> list[str]:
    text = str(value or "").strip()
    if not text or text == "-":
        return []
    return [item.strip() for item in text.split("|") if item.strip() and item.strip() != "-"]


def _edge_key(left: str, right: str) -> tuple[str, str]:
    return tuple(sorted([left, right]))


def _edge_lookup(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    result: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        left = str(row.get("left_family", "") or "")
        right = str(row.get("right_family", "") or "")
        if left and right:
            result[_edge_key(left, right)] = row
    return result


def _islands_for_family(rows: list[dict[str, str]], family: str) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for row in rows:
        if family in _families(row.get("families")):
            result.append(row)
    return result


def _vector(row: dict[str, str]) -> list[float]:
    return [_safe_float(row.get(field)) for field in VECTOR_FIELDS]


def _distance(left: list[float], right: list[float]) -> float:
    if not left or not right:
        return 0.0
    total = 0.0
    for a, b in zip(left, right):
        total += (a - b) * (a - b)
    return math.sqrt(total / max(1, min(len(left), len(right))))


def _group_delta(left: dict[str, str], right: dict[str, str], fields: list[str]) -> float:
    if not left or not right:
        return 0.0
    total = 0.0
    for field in fields:
        total += abs(_safe_float(left.get(field)) - _safe_float(right.get(field)))
    return total / max(1, len(fields))


def _trace_state(*, visible: bool, coupled_count: int, island_count: int, previous_visible: bool | None) -> str:
    if not visible and previous_visible:
        return "trace_disappeared"
    if not visible:
        return "trace_absent"
    if coupled_count > 0 and island_count > 0:
        return "manifesting_coupled_trace"
    if coupled_count > 0:
        return "recoupled_edge_trace"
    if island_count > 0:
        return "island_visible_uncoupled_trace"
    return "latent_visible_uncoupled_trace"


def _reading(state: str) -> str:
    return {
        "trace_disappeared": "Spur war sichtbar und verschwindet in dieser Folgewelt.",
        "trace_absent": "Spur ist in dieser Folgewelt nicht sichtbar.",
        "manifesting_coupled_trace": "Spur ist sichtbar, in einer Insel und aktuell gekoppelt.",
        "recoupled_edge_trace": "Spur ist sichtbar und koppelt wieder, aber ohne stabile Inselzuordnung.",
        "island_visible_uncoupled_trace": "Spur ist in einer Insel sichtbar, aber nicht mit den beobachteten Basisfamilien gekoppelt.",
        "latent_visible_uncoupled_trace": "Spur ist sichtbar, aber ohne aktuelle Kopplung; latente Erinnerung statt Manifestation.",
    }.get(state, "Unbekannter Spurzustand.")


def build_report(stages: list[tuple[str, Path, Path]], family: str, base_families: list[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    previous_row: dict[str, str] = {}
    previous_visible: bool | None = None

    for index, (label, meaning_path, matrix_dir) in enumerate(stages):
        meaning_rows = _read_csv(meaning_path)
        edge_rows = _read_csv(matrix_dir / "passive_semantic_matrix_edges.csv")
        island_rows = _read_csv(matrix_dir / "passive_semantic_matrix_islands.csv")
        edge_lookup = _edge_lookup(edge_rows)
        row = _family_row(meaning_rows, family)
        visible = bool(row)
        islands = _islands_for_family(island_rows, family) if visible else []
        attached: list[str] = []
        edge_similarity_sum = 0.0
        for base in base_families:
            edge = edge_lookup.get(_edge_key(family, base), {})
            if edge:
                attached.append(base)
                edge_similarity_sum += _safe_float(edge.get("meaning_similarity"))
        coupled_count = len(attached)
        state = _trace_state(
            visible=visible,
            coupled_count=coupled_count,
            island_count=len(islands),
            previous_visible=previous_visible,
        )
        vector_drift = _distance(_vector(previous_row), _vector(row)) if previous_row and row else 0.0
        output: dict[str, Any] = {
            "stage_index": index,
            "stage_label": label,
            "family": family,
            "visible": visible,
            "trace_state": state,
            "trace_reading": _reading(state),
            "episode_count": _safe_int(row.get("episode_count")) if row else 0,
            "source_count": _safe_int(row.get("source_count")) if row else 0,
            "island_count": len(islands),
            "island_ids": "|".join(str(item.get("island_id", "") or "") for item in islands) if islands else "-",
            "attached_base_families": "|".join(attached) if attached else "-",
            "coupled_base_count": coupled_count,
            "avg_edge_meaning_similarity": round(edge_similarity_sum / max(1, coupled_count), 9) if coupled_count else 0.0,
            "vector_drift_from_previous_visible": round(vector_drift, 9),
            "dominant_neuro_tone": str(row.get("dominant_neuro_tone", "") or "-") if row else "-",
            "dominant_temporal_state": str(row.get("dominant_temporal_state", "") or "-") if row else "-",
            "dominant_action": str(row.get("dominant_action", "") or "-") if row else "-",
            **BOUNDARY,
        }
        for group, fields in SENSE_GROUPS.items():
            output[f"{group}_delta_from_previous_visible"] = round(_group_delta(previous_row, row, fields), 9) if previous_row and row else 0.0
        rows.append(output)
        if row:
            previous_row = row
        previous_visible = visible

    visible_count = sum(1 for row in rows if row["visible"])
    coupled_count = sum(1 for row in rows if row["coupled_base_count"])
    latent_states = {"latent_visible_uncoupled_trace", "island_visible_uncoupled_trace"}
    latent_count = sum(1 for row in rows if row["trace_state"] in latent_states)
    manifesting_count = sum(1 for row in rows if row["trace_state"] == "manifesting_coupled_trace")
    disappeared_count = sum(1 for row in rows if row["trace_state"] == "trace_disappeared")
    summary_state = "latent_trace"
    if manifesting_count:
        summary_state = "manifesting_trace"
    elif visible_count and not coupled_count:
        summary_state = "persistent_latent_trace"
    elif disappeared_count and not visible_count:
        summary_state = "fading_trace"
    elif coupled_count:
        summary_state = "intermittent_coupling_trace"

    summary = [
        {
            "family": family,
            "base_families": "|".join(base_families) if base_families else "-",
            "stage_count": len(rows),
            "visible_count": visible_count,
            "coupled_stage_count": coupled_count,
            "latent_visible_count": latent_count,
            "manifesting_count": manifesting_count,
            "disappeared_count": disappeared_count,
            "summary_state": summary_state,
            "summary_reading": _summary_reading(summary_state),
            **BOUNDARY,
        }
    ]
    return rows, summary


def _summary_reading(state: str) -> str:
    return {
        "manifesting_trace": "Die Spur erreicht mindestens eine manifestierende Kopplung.",
        "persistent_latent_trace": "Die Spur bleibt sichtbar, ohne aktuell zu koppeln; latenter Bedeutungsrest.",
        "fading_trace": "Die Spur verliert Sichtbarkeit und laeuft aus.",
        "intermittent_coupling_trace": "Die Spur koppelt sporadisch, aber nicht durchgehend stabil.",
        "latent_trace": "Die Spur ist noch nicht eindeutig klassifiziert.",
    }.get(state, "Keine stabile Lesart.")


def write_outputs(rows: list[dict[str, Any]], summary: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "passive_latent_trace_persistence_timeline.csv", rows, ["stage_label", "family", "trace_state"])
    _write_csv(output_dir / "passive_latent_trace_persistence_summary.csv", summary, ["family", "summary_state"])
    (output_dir / "passive_latent_trace_persistence_lupe.json").write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_latent_trace_persistence_lupe.v1",
                "boundary": BOUNDARY,
                "timeline": rows,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Passive Latent Trace Persistence Lupe",
        "",
        "Passive Diagnose. Keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry, keine Richtung.",
        "Kontrollierter Datensatz-Kontext; keine Langlauf-Behauptung.",
        "",
        "## Summary",
        "",
    ]
    for row in summary:
        lines.append(
            f"- {row['family']}: {row['summary_state']}; visible={row['visible_count']}/{row['stage_count']}; "
            f"coupled={row['coupled_stage_count']}; latent={row['latent_visible_count']}; "
            f"manifesting={row['manifesting_count']}"
        )
    lines.extend(["", "## Timeline", ""])
    for row in rows:
        lines.append(
            f"- {row['stage_label']}: {row['trace_state']}; visible={row['visible']}; "
            f"attached={row['attached_base_families']}; islands={row['island_ids']}; "
            f"drift={row['vector_drift_from_previous_visible']}"
        )
    (output_dir / "passive_latent_trace_persistence_lupe.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive latent trace persistence lupe")
    parser.add_argument("--stage", action="append", required=True, help="LABEL=passive_cluster_meaning_space.csv=semantic_matrix_dir")
    parser.add_argument("--family", required=True)
    parser.add_argument("--base-family", action="append", default=[])
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    rows, summary = build_report(
        [_parse_stage(raw) for raw in args.stage],
        family=args.family,
        base_families=list(args.base_family),
    )
    write_outputs(rows, summary, args.output_dir)
    print(
        json.dumps(
            {
                "timeline_rows": len(rows),
                "summary": summary,
                **BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
