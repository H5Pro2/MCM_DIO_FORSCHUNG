"""Inspect selected passive emergent lifecycle candidates across stages.

This is a passive diagnostic lupe. It expands lifecycle candidates into
stage-by-stage meaning, sensory/MCM vector movement, island presence, and
coupling partners.

No runtime reads, no memory writes, no action, no gate, no entry, no direction.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any


PASSIVE_FLAGS = {
    "passive_only": True,
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
    "avg_sehen_form_change",
    "avg_hoeren_energy_tone",
    "avg_hoeren_energy_shift",
    "avg_fuehlen_mcm_coherence",
    "avg_fuehlen_mcm_tension",
    "avg_fuehlen_mcm_asymmetry",
    "avg_mini_recurrence_strength",
    "avg_mini_afterimage",
    "avg_mini_temporal_trust_support",
    "avg_mini_temporal_caution_support",
    "avg_mini_focus_tone",
    "avg_mini_trust_tone",
    "avg_mini_caution_tone",
    "avg_mini_strain_tone",
    "avg_mini_neuro_balance",
]


DETAIL_FIELDS = [
    "symbol_family",
    "stage",
    "stage_order",
    "found",
    "lifecycle_state",
    "lifecycle_reading",
    "episode_count",
    "source_count",
    "dominant_action",
    "dominant_neuro_tone",
    "dominant_temporal_state",
    "avg_sehen_form_flow",
    "avg_sehen_form_change",
    "avg_hoeren_energy_tone",
    "avg_hoeren_energy_shift",
    "avg_fuehlen_mcm_coherence",
    "avg_fuehlen_mcm_tension",
    "avg_fuehlen_mcm_asymmetry",
    "avg_mini_afterimage",
    "avg_mini_neuro_balance",
    "vector_drift_from_previous",
    "field_drift_from_previous",
    "sensory_drift_from_previous",
    "island_present",
    "island_id",
    "island_state",
    "island_family_count",
    "island_partners",
    "stage_reading",
]


SUMMARY_FIELDS = [
    "symbol_family",
    "lifecycle_state",
    "stage_count",
    "found_stage_count",
    "stage_trace",
    "avg_vector_drift",
    "max_vector_drift",
    "avg_field_drift",
    "avg_sensory_drift",
    "island_presence_count",
    "island_coupling_count",
    "partner_count",
    "partner_trace",
    "emergent_motion_reading",
]


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = list(fields)
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=ordered)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in ordered})


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        result = float(value if value not in (None, "") else default)
    except (TypeError, ValueError):
        return default
    if result != result:
        return default
    return result


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value if value not in (None, "") else default))
    except (TypeError, ValueError):
        return default


def _parse_stage(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise ValueError(f"Stage must be LABEL=path: {value}")
    label, path = value.split("=", 1)
    label = label.strip()
    if not label:
        raise ValueError(f"Stage label is empty: {value}")
    return label, Path(path.strip())


def _split_pipe(value: Any) -> list[str]:
    return sorted({item.strip() for item in str(value or "").split("|") if item.strip() and item.strip() != "-"})


def _vector(row: dict[str, str]) -> list[float]:
    return [_safe_float(row.get(field)) for field in VECTOR_FIELDS]


def _subvector(row: dict[str, str], fields: list[str]) -> list[float]:
    return [_safe_float(row.get(field)) for field in fields]


def _distance(left: list[float], right: list[float]) -> float:
    if not left or not right:
        return 0.0
    total = 0.0
    for a, b in zip(left, right):
        total += (a - b) * (a - b)
    return math.sqrt(total / max(1, min(len(left), len(right))))


def _mean(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def _family_index(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {str(row.get("symbol_family", "") or ""): row for row in rows if str(row.get("symbol_family", "") or "")}


def _island_membership(rows: list[dict[str, str]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        island_id = str(row.get("island_id", "") or "")
        families = _split_pipe(row.get("families"))
        if not island_id or not families:
            continue
        for family in families:
            result[family] = {
                "island_id": island_id,
                "island_state": str(row.get("island_state", "") or ""),
                "family_count": _safe_int(row.get("family_count"), len(families)),
                "partners": sorted(other for other in families if other != family),
            }
    return result


def _stage_reading(*, row: dict[str, str], drift: float, field_drift: float, sensory_drift: float, partners: list[str]) -> str:
    neuro = str(row.get("dominant_neuro_tone", "") or "-")
    temporal = str(row.get("dominant_temporal_state", "") or "-")
    if partners:
        return f"koppelt mit {'|'.join(partners)}; neuro={neuro}; zeit={temporal}"
    if drift > 0.18:
        return f"starke innere Variation ohne Kopplung; neuro={neuro}; zeit={temporal}"
    if sensory_drift > field_drift * 1.5 and sensory_drift > 0.05:
        return f"Variation kommt staerker aus Sehen/Hoeren; neuro={neuro}; zeit={temporal}"
    if field_drift > sensory_drift * 1.5 and field_drift > 0.05:
        return f"Variation kommt staerker aus MCM-Feldlage; neuro={neuro}; zeit={temporal}"
    return f"isolierte sichtbare Spur; neuro={neuro}; zeit={temporal}"


def _summary_reading(summary: dict[str, Any]) -> str:
    state = str(summary.get("lifecycle_state", ""))
    partners = _safe_int(summary.get("partner_count"))
    avg_drift = _safe_float(summary.get("avg_vector_drift"))
    if "reorganization" in state:
        return "Kopplung und Teilung sind sichtbar; Kandidat fuer echte Reorganisation."
    if "split" in state:
        return "Kopplung wechselt oder bricht; Kandidat fuer Drift/Split."
    if partners > 0:
        return "Emergente Variation hat Sozialkontakt zu anderen Inseln."
    if avg_drift > 0.12:
        return "Starke isolierte Variation; noch keine Verschmelzung."
    return "Isolierte Variation mit geringer Bewegung; weitere Weltkontakte noetig."


def build_report(
    *,
    lifecycle_rows: list[dict[str, str]],
    stages: list[tuple[str, list[dict[str, str]]]],
    island_stages: dict[str, list[dict[str, str]]],
    candidates: list[str],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    lifecycle_by_family = _family_index(lifecycle_rows)
    stage_indexes = [(label, _family_index(rows)) for label, rows in stages]
    island_indexes = {label: _island_membership(rows) for label, rows in island_stages.items()}
    detail_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for family in candidates:
        lifecycle = lifecycle_by_family.get(family, {})
        previous_vector: list[float] | None = None
        previous_field: list[float] | None = None
        previous_sensory: list[float] | None = None
        found_details: list[dict[str, Any]] = []
        all_partners: set[str] = set()
        for order, (stage_label, rows_by_family) in enumerate(stage_indexes, start=1):
            row = rows_by_family.get(family)
            if not row:
                detail = {
                    "symbol_family": family,
                    "stage": stage_label,
                    "stage_order": order,
                    "found": False,
                    "lifecycle_state": lifecycle.get("lifecycle_state", "-"),
                    "lifecycle_reading": lifecycle.get("lifecycle_reading", "-"),
                    "stage_reading": "nicht sichtbar",
                    **PASSIVE_FLAGS,
                }
                detail_rows.append(detail)
                continue

            vector = _vector(row)
            field = _subvector(row, ["avg_fuehlen_mcm_coherence", "avg_fuehlen_mcm_tension", "avg_fuehlen_mcm_asymmetry"])
            sensory = _subvector(row, ["avg_sehen_form_flow", "avg_sehen_form_change", "avg_hoeren_energy_tone", "avg_hoeren_energy_shift"])
            drift = _distance(previous_vector or vector, vector)
            field_drift = _distance(previous_field or field, field)
            sensory_drift = _distance(previous_sensory or sensory, sensory)
            previous_vector = vector
            previous_field = field
            previous_sensory = sensory
            membership = island_indexes.get(stage_label, {}).get(family, {})
            partners = list(membership.get("partners", []) or [])
            all_partners.update(partners)
            detail = {
                "symbol_family": family,
                "stage": stage_label,
                "stage_order": order,
                "found": True,
                "lifecycle_state": lifecycle.get("lifecycle_state", "-"),
                "lifecycle_reading": lifecycle.get("lifecycle_reading", "-"),
                "episode_count": _safe_int(row.get("episode_count")),
                "source_count": _safe_int(row.get("source_count")),
                "dominant_action": str(row.get("dominant_action", "") or "-"),
                "dominant_neuro_tone": str(row.get("dominant_neuro_tone", "") or "-"),
                "dominant_temporal_state": str(row.get("dominant_temporal_state", "") or "-"),
                "avg_sehen_form_flow": round(_safe_float(row.get("avg_sehen_form_flow")), 9),
                "avg_sehen_form_change": round(_safe_float(row.get("avg_sehen_form_change")), 9),
                "avg_hoeren_energy_tone": round(_safe_float(row.get("avg_hoeren_energy_tone")), 9),
                "avg_hoeren_energy_shift": round(_safe_float(row.get("avg_hoeren_energy_shift")), 9),
                "avg_fuehlen_mcm_coherence": round(_safe_float(row.get("avg_fuehlen_mcm_coherence")), 9),
                "avg_fuehlen_mcm_tension": round(_safe_float(row.get("avg_fuehlen_mcm_tension")), 9),
                "avg_fuehlen_mcm_asymmetry": round(_safe_float(row.get("avg_fuehlen_mcm_asymmetry")), 9),
                "avg_mini_afterimage": round(_safe_float(row.get("avg_mini_afterimage")), 9),
                "avg_mini_neuro_balance": round(_safe_float(row.get("avg_mini_neuro_balance")), 9),
                "vector_drift_from_previous": round(drift, 9),
                "field_drift_from_previous": round(field_drift, 9),
                "sensory_drift_from_previous": round(sensory_drift, 9),
                "island_present": bool(membership),
                "island_id": membership.get("island_id", "-"),
                "island_state": membership.get("island_state", "-"),
                "island_family_count": membership.get("family_count", 0),
                "island_partners": "|".join(partners) if partners else "-",
                **PASSIVE_FLAGS,
            }
            detail["stage_reading"] = _stage_reading(
                row=row,
                drift=drift,
                field_drift=field_drift,
                sensory_drift=sensory_drift,
                partners=partners,
            )
            detail_rows.append(detail)
            found_details.append(detail)

        vector_drifts = [_safe_float(row.get("vector_drift_from_previous")) for row in found_details[1:]]
        field_drifts = [_safe_float(row.get("field_drift_from_previous")) for row in found_details[1:]]
        sensory_drifts = [_safe_float(row.get("sensory_drift_from_previous")) for row in found_details[1:]]
        summary = {
            "symbol_family": family,
            "lifecycle_state": lifecycle.get("lifecycle_state", "-"),
            "stage_count": len(stages),
            "found_stage_count": len(found_details),
            "stage_trace": "|".join(str(row.get("stage", "")) for row in found_details),
            "avg_vector_drift": round(_mean(vector_drifts), 9),
            "max_vector_drift": round(max(vector_drifts) if vector_drifts else 0.0, 9),
            "avg_field_drift": round(_mean(field_drifts), 9),
            "avg_sensory_drift": round(_mean(sensory_drifts), 9),
            "island_presence_count": sum(1 for row in found_details if row.get("island_present")),
            "island_coupling_count": sum(1 for row in found_details if str(row.get("island_partners", "-")) != "-"),
            "partner_count": len(all_partners),
            "partner_trace": "|".join(sorted(all_partners)) if all_partners else "-",
            **PASSIVE_FLAGS,
        }
        summary["emergent_motion_reading"] = _summary_reading(summary)
        summary_rows.append(summary)

    detail_rows.sort(key=lambda row: (str(row["symbol_family"]), _safe_int(row.get("stage_order"))))
    summary_rows.sort(key=lambda row: (-_safe_float(row.get("max_vector_drift")), str(row["symbol_family"])))
    overall = {
        "candidate_count": len(candidates),
        "detail_count": len(detail_rows),
        "summary_count": len(summary_rows),
        "candidates": candidates,
        **PASSIVE_FLAGS,
    }
    return overall, detail_rows, summary_rows


def write_report(output_dir: Path, overall: dict[str, Any], detail_rows: list[dict[str, Any]], summary_rows: list[dict[str, Any]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "passive_emergent_candidate_lupe_detail.csv", detail_rows, DETAIL_FIELDS + list(PASSIVE_FLAGS))
    _write_csv(output_dir / "passive_emergent_candidate_lupe_summary.csv", summary_rows, SUMMARY_FIELDS + list(PASSIVE_FLAGS))
    (output_dir / "passive_emergent_candidate_lupe.json").write_text(
        json.dumps({"overall": overall, "summary": summary_rows, "detail": detail_rows}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    lines = [
        "# Passive Emergent Candidate Lupe",
        "",
        "Passive Diagnose. Keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry, keine Richtung.",
        "",
        "## Kandidaten",
        "",
    ]
    for row in summary_rows:
        lines.append(
            "- {family}: {state}; max_drift={max_drift}; field={field}; sensory={sensory}; partners={partners}; {reading}".format(
                family=row["symbol_family"],
                state=row["lifecycle_state"],
                max_drift=row["max_vector_drift"],
                field=row["avg_field_drift"],
                sensory=row["avg_sensory_drift"],
                partners=row["partner_trace"],
                reading=row["emergent_motion_reading"],
            )
        )
    lines.extend(["", "## Verlauf", ""])
    for row in detail_rows:
        if not row.get("found"):
            lines.append(f"- {row['symbol_family']} / {row['stage']}: nicht sichtbar")
            continue
        lines.append(
            "- {family} / {stage}: drift={drift}; field={field}; sensory={sensory}; "
            "island={island}; partners={partners}; {reading}".format(
                family=row["symbol_family"],
                stage=row["stage"],
                drift=row["vector_drift_from_previous"],
                field=row["field_drift_from_previous"],
                sensory=row["sensory_drift_from_previous"],
                island=row["island_id"],
                partners=row["island_partners"],
                reading=row["stage_reading"],
            )
        )
    (output_dir / "passive_emergent_candidate_lupe.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lifecycle", required=True, type=Path)
    parser.add_argument("--stage", action="append", required=True, help="LABEL=passive_cluster_meaning_space.csv")
    parser.add_argument("--island-stage", action="append", default=[], help="LABEL=passive_semantic_matrix_islands.csv")
    parser.add_argument("--candidate", action="append", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    stages = [(label, _read_csv(path)) for label, path in (_parse_stage(value) for value in args.stage)]
    island_stages = {label: _read_csv(path) for label, path in (_parse_stage(value) for value in args.island_stage)}
    overall, detail, summary = build_report(
        lifecycle_rows=_read_csv(args.lifecycle),
        stages=stages,
        island_stages=island_stages,
        candidates=args.candidate,
    )
    write_report(args.output_dir, overall, detail, summary)
    print(json.dumps(overall, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
