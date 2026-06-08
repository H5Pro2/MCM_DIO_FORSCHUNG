"""Inspect emergent partner islands around selected Mini-DIO families.

This report reads passive meaning-space and semantic-island diagnostics. It
shows whether a selected family is isolated or coupled with partners across
stages, and whether the coupling is driven more by sensory, MCM-field,
hearing, temporal, or neuro similarity.

Passive only. No runtime reads, no memory writes, no action, no gate, no entry,
no direction.
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


MEANING_FIELDS = [
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

SENSORY_FIELDS = [
    "avg_sehen_form_flow",
    "avg_sehen_form_change",
    "avg_hoeren_energy_tone",
    "avg_hoeren_energy_shift",
]

MCM_FIELDS = [
    "avg_fuehlen_mcm_coherence",
    "avg_fuehlen_mcm_tension",
    "avg_fuehlen_mcm_asymmetry",
]

NEURO_FIELDS = [
    "avg_mini_focus_tone",
    "avg_mini_trust_tone",
    "avg_mini_caution_tone",
    "avg_mini_strain_tone",
    "avg_mini_neuro_balance",
]


DETAIL_FIELDS = [
    "candidate_family",
    "stage",
    "candidate_found",
    "candidate_episode_count",
    "candidate_neuro_tone",
    "candidate_temporal_state",
    "candidate_island_id",
    "candidate_island_state",
    "candidate_island_family_count",
    "partner_family",
    "partner_found",
    "partner_episode_count",
    "partner_neuro_tone",
    "partner_temporal_state",
    "whole_distance",
    "sensory_distance",
    "mcm_distance",
    "neuro_distance",
    "same_neuro_tone",
    "same_temporal_state",
    "same_island",
    "partner_relation_state",
    "relation_reading",
]


SUMMARY_FIELDS = [
    "candidate_family",
    "stage_count",
    "visible_stage_count",
    "coupled_stage_count",
    "partner_count",
    "partner_trace",
    "avg_whole_distance",
    "avg_sensory_distance",
    "avg_mcm_distance",
    "avg_neuro_distance",
    "dominant_relation_state",
    "partner_lupe_reading",
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


def _index_meaning(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
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


def _vector(row: dict[str, str], fields: list[str]) -> list[float]:
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


def _relation_state(*, same_island: bool, whole: float, sensory: float, mcm: float, neuro: float) -> str:
    if not same_island:
        return "not_coupled_in_stage"
    if whole <= 0.02:
        return "tight_partner_coupling"
    if sensory <= mcm and sensory <= neuro:
        return "sensory_led_partner_coupling"
    if mcm <= sensory and mcm <= neuro:
        return "mcm_field_led_partner_coupling"
    return "neuro_led_partner_coupling"


def _relation_reading(state: str) -> str:
    return {
        "not_coupled_in_stage": "keine gemeinsame Insel in dieser Stage",
        "tight_partner_coupling": "sehr enge passive Bedeutungsnaehe",
        "sensory_led_partner_coupling": "Kopplung wird am staerksten durch Sehen/Hoeren getragen",
        "mcm_field_led_partner_coupling": "Kopplung wird am staerksten durch MCM-Feldnaehe getragen",
        "neuro_led_partner_coupling": "Kopplung wird am staerksten durch Neurotonnaehe getragen",
    }.get(state, "passiv uneindeutig")


def _summary_reading(row: dict[str, Any]) -> str:
    coupled = _safe_int(row.get("coupled_stage_count"))
    partners = _safe_int(row.get("partner_count"))
    whole = _safe_float(row.get("avg_whole_distance"))
    if coupled == 0:
        return "Keine Kopplungsinsel sichtbar."
    if partners >= 2 and whole <= 0.02:
        return "Mehrfachpartner mit sehr enger Bedeutungsnaehe; Reorganisationskandidat."
    if partners >= 2:
        return "Mehrfachpartner sichtbar; weitere Weltkontakte pruefen."
    return "Einzelpartner sichtbar; noch kein stabiles Inselgefuege."


def build_report(
    *,
    stages: list[tuple[str, list[dict[str, str]]]],
    island_stages: dict[str, list[dict[str, str]]],
    candidates: list[str],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    detail_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    stage_meanings = [(label, _index_meaning(rows)) for label, rows in stages]
    stage_islands = {label: _island_membership(rows) for label, rows in island_stages.items()}

    for candidate in candidates:
        candidate_details: list[dict[str, Any]] = []
        all_partners: set[str] = set()
        for stage_label, meaning in stage_meanings:
            candidate_row = meaning.get(candidate, {})
            membership = stage_islands.get(stage_label, {}).get(candidate, {})
            partners = list(membership.get("partners", []) or [])
            if not partners:
                detail = {
                    "candidate_family": candidate,
                    "stage": stage_label,
                    "candidate_found": bool(candidate_row),
                    "candidate_episode_count": _safe_int(candidate_row.get("episode_count")),
                    "candidate_neuro_tone": str(candidate_row.get("dominant_neuro_tone", "") or "-"),
                    "candidate_temporal_state": str(candidate_row.get("dominant_temporal_state", "") or "-"),
                    "candidate_island_id": membership.get("island_id", "-"),
                    "candidate_island_state": membership.get("island_state", "-"),
                    "candidate_island_family_count": membership.get("family_count", 0),
                    "partner_family": "-",
                    "partner_found": False,
                    "same_island": False,
                    "partner_relation_state": "not_coupled_in_stage",
                    "relation_reading": _relation_reading("not_coupled_in_stage"),
                    **PASSIVE_FLAGS,
                }
                detail_rows.append(detail)
                candidate_details.append(detail)
                continue
            for partner in partners:
                partner_row = meaning.get(partner, {})
                all_partners.add(partner)
                whole = _distance(_vector(candidate_row, MEANING_FIELDS), _vector(partner_row, MEANING_FIELDS))
                sensory = _distance(_vector(candidate_row, SENSORY_FIELDS), _vector(partner_row, SENSORY_FIELDS))
                mcm = _distance(_vector(candidate_row, MCM_FIELDS), _vector(partner_row, MCM_FIELDS))
                neuro = _distance(_vector(candidate_row, NEURO_FIELDS), _vector(partner_row, NEURO_FIELDS))
                state = _relation_state(same_island=True, whole=whole, sensory=sensory, mcm=mcm, neuro=neuro)
                detail = {
                    "candidate_family": candidate,
                    "stage": stage_label,
                    "candidate_found": bool(candidate_row),
                    "candidate_episode_count": _safe_int(candidate_row.get("episode_count")),
                    "candidate_neuro_tone": str(candidate_row.get("dominant_neuro_tone", "") or "-"),
                    "candidate_temporal_state": str(candidate_row.get("dominant_temporal_state", "") or "-"),
                    "candidate_island_id": membership.get("island_id", "-"),
                    "candidate_island_state": membership.get("island_state", "-"),
                    "candidate_island_family_count": membership.get("family_count", 0),
                    "partner_family": partner,
                    "partner_found": bool(partner_row),
                    "partner_episode_count": _safe_int(partner_row.get("episode_count")),
                    "partner_neuro_tone": str(partner_row.get("dominant_neuro_tone", "") or "-"),
                    "partner_temporal_state": str(partner_row.get("dominant_temporal_state", "") or "-"),
                    "whole_distance": round(whole, 9),
                    "sensory_distance": round(sensory, 9),
                    "mcm_distance": round(mcm, 9),
                    "neuro_distance": round(neuro, 9),
                    "same_neuro_tone": str(candidate_row.get("dominant_neuro_tone", "") or "") == str(partner_row.get("dominant_neuro_tone", "") or ""),
                    "same_temporal_state": str(candidate_row.get("dominant_temporal_state", "") or "") == str(partner_row.get("dominant_temporal_state", "") or ""),
                    "same_island": True,
                    "partner_relation_state": state,
                    "relation_reading": _relation_reading(state),
                    **PASSIVE_FLAGS,
                }
                detail_rows.append(detail)
                candidate_details.append(detail)

        coupled = [row for row in candidate_details if str(row.get("partner_family", "-")) != "-"]
        summary = {
            "candidate_family": candidate,
            "stage_count": len(stages),
            "visible_stage_count": sum(1 for row in candidate_details if row.get("candidate_found")),
            "coupled_stage_count": len({str(row.get("stage")) for row in coupled}),
            "partner_count": len(all_partners),
            "partner_trace": "|".join(sorted(all_partners)) if all_partners else "-",
            "avg_whole_distance": round(_mean([_safe_float(row.get("whole_distance")) for row in coupled]), 9),
            "avg_sensory_distance": round(_mean([_safe_float(row.get("sensory_distance")) for row in coupled]), 9),
            "avg_mcm_distance": round(_mean([_safe_float(row.get("mcm_distance")) for row in coupled]), 9),
            "avg_neuro_distance": round(_mean([_safe_float(row.get("neuro_distance")) for row in coupled]), 9),
            "dominant_relation_state": max(
                {str(row.get("partner_relation_state", "")) for row in coupled} or {"not_coupled_in_stage"},
                key=lambda state: sum(1 for row in coupled if str(row.get("partner_relation_state", "")) == state),
            ),
            **PASSIVE_FLAGS,
        }
        summary["partner_lupe_reading"] = _summary_reading(summary)
        summary_rows.append(summary)

    detail_rows.sort(key=lambda row: (str(row["candidate_family"]), str(row["stage"]), str(row["partner_family"])))
    summary_rows.sort(key=lambda row: (-_safe_int(row.get("partner_count")), str(row["candidate_family"])))
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
    _write_csv(output_dir / "passive_emergent_partner_lupe_detail.csv", detail_rows, DETAIL_FIELDS + list(PASSIVE_FLAGS))
    _write_csv(output_dir / "passive_emergent_partner_lupe_summary.csv", summary_rows, SUMMARY_FIELDS + list(PASSIVE_FLAGS))
    (output_dir / "passive_emergent_partner_lupe.json").write_text(
        json.dumps({"overall": overall, "summary": summary_rows, "detail": detail_rows}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    lines = [
        "# Passive Emergent Partner Lupe",
        "",
        "Passive Diagnose. Keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry, keine Richtung.",
        "",
        "## Zusammenfassung",
        "",
    ]
    for row in summary_rows:
        lines.append(
            "- {candidate}: partners={partners}; coupled_stages={coupled}; whole={whole}; "
            "sensory={sensory}; mcm={mcm}; neuro={neuro}; {reading}".format(
                candidate=row["candidate_family"],
                partners=row["partner_trace"],
                coupled=row["coupled_stage_count"],
                whole=row["avg_whole_distance"],
                sensory=row["avg_sensory_distance"],
                mcm=row["avg_mcm_distance"],
                neuro=row["avg_neuro_distance"],
                reading=row["partner_lupe_reading"],
            )
        )
    lines.extend(["", "## Details", ""])
    for row in detail_rows:
        lines.append(
            "- {candidate} / {stage} -> {partner}: {state}; whole={whole}; sensory={sensory}; "
            "mcm={mcm}; neuro={neuro}; {reading}".format(
                candidate=row["candidate_family"],
                stage=row["stage"],
                partner=row["partner_family"],
                state=row["partner_relation_state"],
                whole=row.get("whole_distance", ""),
                sensory=row.get("sensory_distance", ""),
                mcm=row.get("mcm_distance", ""),
                neuro=row.get("neuro_distance", ""),
                reading=row["relation_reading"],
            )
        )
    (output_dir / "passive_emergent_partner_lupe.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", action="append", required=True, help="LABEL=passive_cluster_meaning_space.csv")
    parser.add_argument("--island-stage", action="append", default=[], help="LABEL=passive_semantic_matrix_islands.csv")
    parser.add_argument("--candidate", action="append", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    stages = [(label, _read_csv(path)) for label, path in (_parse_stage(value) for value in args.stage)]
    island_stages = {label: _read_csv(path) for label, path in (_parse_stage(value) for value in args.island_stage)}
    overall, detail, summary = build_report(stages=stages, island_stages=island_stages, candidates=args.candidate)
    write_report(args.output_dir, overall, detail, summary)
    print(json.dumps(overall, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
