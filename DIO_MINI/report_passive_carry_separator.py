"""Separate stable carried traces from weak carried candidates.

This report is passive. It reads existing diagnostics and writes a comparison
between a stable reference family and follow-up candidates. Mini-DIO must not
read this report during runtime.
"""

from __future__ import annotations

import argparse
import csv
import json
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


FIELDS = [
    "reference_family",
    "candidate_family",
    "separator_state",
    "separator_reading",
    "reference_contrast_group",
    "candidate_contrast_group",
    "reference_trace_state",
    "candidate_trace_state",
    "reference_visible_probe_count",
    "candidate_visible_probe_count",
    "visible_probe_gap",
    "reference_carried_probe_count",
    "candidate_carried_probe_count",
    "carried_probe_gap",
    "reference_carry_ratio",
    "candidate_carry_ratio",
    "carry_ratio_gap",
    "reference_sensory_field_distance",
    "candidate_sensory_field_distance",
    "sensory_distance_gap",
    "reference_lived_support_drop_count",
    "candidate_lived_support_drop_count",
    "lived_support_drop_gap",
    "reference_neuro_tone_reorganizes_count",
    "candidate_neuro_tone_reorganizes_count",
    "neuro_tone_reorganizes_gap",
    "reference_text_island_symbol",
    "candidate_text_island_symbol",
    "text_island_same",
    "followup_reading",
    "followup_state",
]


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


def _family(row: dict[str, str]) -> str:
    return str(row.get("symbol_family", "") or row.get("family", "") or row.get("candidate_family", "") or "")


def _text_island(row: dict[str, str]) -> str:
    return str(row.get("right_text_island_symbol", "") or row.get("left_text_island_symbol", "") or "")


def _separator_state(reference: dict[str, str], candidate: dict[str, str], followup: dict[str, str] | None) -> str:
    ref_visible = _safe_int(reference.get("visible_probe_count"))
    cand_visible = _safe_int(candidate.get("visible_probe_count"))
    cand_carried = _safe_int(candidate.get("carried_probe_count"))
    cand_kipp = _safe_int(candidate.get("kipp_probe_count"))
    followup_reading = str((followup or {}).get("followup_reading", "") or "")
    if followup_reading == "candidate_not_visible_in_followup":
        return "not_reproduced"
    if cand_kipp > 0 or followup_reading == "kipped_in_followup":
        return "kipped_under_world_contact"
    if cand_visible >= 2 and cand_carried >= 2:
        return "stable_carried_trace"
    if cand_visible == 1 and cand_carried == 1 and ref_visible >= 2:
        return "weak_single_contact_keim"
    return "unclear_or_mixed_separator"


def _separator_reading(state: str) -> str:
    if state == "stable_carried_trace":
        return "wiederholter Weltkontakt traegt die Spur"
    if state == "weak_single_contact_keim":
        return "sichtbar und getragen, aber noch ohne Tragedauer"
    if state == "kipped_under_world_contact":
        return "sichtbar, aber Weltkontakt traegt die Spur nicht stabil"
    if state == "not_reproduced":
        return "im Folgeweltkontakt nicht erneut sichtbar"
    return "passiv uneindeutig, weitere Weltkontakte noetig"


def build_report(
    *,
    carry_rows: list[dict[str, str]],
    followup_rows: list[dict[str, str]],
    reference_family: str,
    candidate_families: list[str] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    carry_by_family = {_family(row): row for row in carry_rows if _family(row)}
    followup_by_family = {_family(row): row for row in followup_rows if _family(row)}
    if reference_family not in carry_by_family:
        raise ValueError(f"Reference family not found in carry contrast: {reference_family}")
    reference = carry_by_family[reference_family]

    families = candidate_families or [
        family
        for family, row in followup_by_family.items()
        if family != reference_family and str(row.get("followup_reading", "") or "")
    ]
    rows: list[dict[str, Any]] = []
    for family in families:
        candidate = carry_by_family.get(family, {})
        followup = followup_by_family.get(family)
        state = _separator_state(reference, candidate, followup) if candidate else "not_reproduced"
        ref_visible = _safe_int(reference.get("visible_probe_count"))
        cand_visible = _safe_int(candidate.get("visible_probe_count"))
        ref_carried = _safe_int(reference.get("carried_probe_count"))
        cand_carried = _safe_int(candidate.get("carried_probe_count"))
        ref_carry = _safe_float(reference.get("carry_ratio"))
        cand_carry = _safe_float(candidate.get("carry_ratio"))
        ref_support = _safe_int(reference.get("lived_support_drop_count"))
        cand_support = _safe_int(candidate.get("lived_support_drop_count"))
        ref_neuro = _safe_int(reference.get("neuro_tone_reorganizes_count"))
        cand_neuro = _safe_int(candidate.get("neuro_tone_reorganizes_count"))
        ref_text = _text_island(reference)
        cand_text = _text_island(candidate)
        rows.append(
            {
                "reference_family": reference_family,
                "candidate_family": family,
                "separator_state": state,
                "separator_reading": _separator_reading(state),
                "reference_contrast_group": reference.get("contrast_group", ""),
                "candidate_contrast_group": candidate.get("contrast_group", "-"),
                "reference_trace_state": reference.get("trace_carry_state", ""),
                "candidate_trace_state": candidate.get("trace_carry_state", "-"),
                "reference_visible_probe_count": ref_visible,
                "candidate_visible_probe_count": cand_visible,
                "visible_probe_gap": ref_visible - cand_visible,
                "reference_carried_probe_count": ref_carried,
                "candidate_carried_probe_count": cand_carried,
                "carried_probe_gap": ref_carried - cand_carried,
                "reference_carry_ratio": ref_carry,
                "candidate_carry_ratio": cand_carry,
                "carry_ratio_gap": round(ref_carry - cand_carry, 9),
                "reference_sensory_field_distance": _safe_float(reference.get("sensory_field_distance")),
                "candidate_sensory_field_distance": _safe_float(candidate.get("sensory_field_distance")),
                "sensory_distance_gap": round(
                    _safe_float(candidate.get("sensory_field_distance"))
                    - _safe_float(reference.get("sensory_field_distance")),
                    9,
                ),
                "reference_lived_support_drop_count": ref_support,
                "candidate_lived_support_drop_count": cand_support,
                "lived_support_drop_gap": cand_support - ref_support,
                "reference_neuro_tone_reorganizes_count": ref_neuro,
                "candidate_neuro_tone_reorganizes_count": cand_neuro,
                "neuro_tone_reorganizes_gap": cand_neuro - ref_neuro,
                "reference_text_island_symbol": ref_text,
                "candidate_text_island_symbol": cand_text,
                "text_island_same": bool(ref_text and cand_text and ref_text == cand_text),
                "followup_reading": (followup or {}).get("followup_reading", "-"),
                "followup_state": (followup or {}).get("followup_state", "-"),
                **PASSIVE_FLAGS,
            }
        )

    counts: dict[str, int] = {}
    for row in rows:
        counts[str(row["separator_state"])] = counts.get(str(row["separator_state"]), 0) + 1
    summary = {
        "reference_family": reference_family,
        "candidate_count": len(rows),
        "state_counts": counts,
        "reference_visible_probe_count": _safe_int(reference.get("visible_probe_count")),
        "reference_carried_probe_count": _safe_int(reference.get("carried_probe_count")),
        "reference_carry_ratio": _safe_float(reference.get("carry_ratio")),
        "reference_text_island_symbol": _text_island(reference),
        **PASSIVE_FLAGS,
    }
    rows.sort(key=lambda row: (str(row["separator_state"]), str(row["candidate_family"])))
    return summary, rows


def write_report(output_dir: Path, summary: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "passive_carry_separator.csv", rows, FIELDS + list(PASSIVE_FLAGS))
    (output_dir / "passive_carry_separator.json").write_text(
        json.dumps({"summary": summary, "rows": rows}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    lines = [
        "# Passive Carry Separator",
        "",
        "Passive Diagnose. Keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry, keine Richtung.",
        "",
        "## Referenz",
        "",
        f"- Familie: {summary['reference_family']}",
        f"- Sichtbare Proben: {summary['reference_visible_probe_count']}",
        f"- Getragene Proben: {summary['reference_carried_probe_count']}",
        f"- Carry-Ratio: {summary['reference_carry_ratio']:.9f}",
        f"- Textinsel: {summary['reference_text_island_symbol']}",
        "",
        "## Trennung",
        "",
    ]
    for key, value in sorted(summary["state_counts"].items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Kandidaten", ""])
    for row in rows:
        lines.append(
            "- {family}: {state}; {reading}; visible_gap={visible_gap}; carried_gap={carried_gap}; "
            "support_gap={support_gap}; neuro_gap={neuro_gap}; followup={followup}".format(
                family=row["candidate_family"],
                state=row["separator_state"],
                reading=row["separator_reading"],
                visible_gap=row["visible_probe_gap"],
                carried_gap=row["carried_probe_gap"],
                support_gap=row["lived_support_drop_gap"],
                neuro_gap=row["neuro_tone_reorganizes_gap"],
                followup=row["followup_reading"],
            )
        )
    (output_dir / "passive_carry_separator.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--carry-contrast", required=True, type=Path)
    parser.add_argument("--followup-result", required=True, type=Path)
    parser.add_argument("--reference-family", default="dio_11vr")
    parser.add_argument("--candidate-family", action="append", default=[])
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    summary, rows = build_report(
        carry_rows=_read_csv(args.carry_contrast),
        followup_rows=_read_csv(args.followup_result),
        reference_family=args.reference_family,
        candidate_families=args.candidate_family or None,
    )
    write_report(args.output_dir, summary, rows)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
