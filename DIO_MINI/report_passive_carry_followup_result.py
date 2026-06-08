"""Evaluate passive follow-up candidates against a later carry contrast.

The report checks whether weakly carried Mini-DIO traces became multi-probe
carried, stayed weak, kipped, or disappeared in a later controlled comparison.
It is diagnostic only and must not be read by Mini-DIO for runtime, action,
gates, entries, or direction.
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
    "candidate_family",
    "prior_test_priority",
    "prior_profile_distance",
    "followup_state",
    "new_contrast_group",
    "new_trace_carry_state",
    "new_visible_probe_count",
    "new_carried_probe_count",
    "new_kipp_probe_count",
    "new_carry_ratio",
    "new_sensory_field_distance",
    "new_lived_support_drop_count",
    "new_neuro_tone_reorganizes_count",
    "new_text_island_same",
    "followup_reading",
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


def _family_key(row: dict[str, str]) -> str:
    return str(row.get("symbol_family", "") or row.get("family", "") or row.get("candidate_family", "") or "")


def _text_island_same(row: dict[str, str]) -> bool:
    left = str(row.get("left_text_island_symbol", "") or row.get("left_text_island", "") or "")
    right = str(row.get("right_text_island_symbol", "") or row.get("right_text_island", "") or "")
    return bool(left and right and left == right)


def _followup_reading(row: dict[str, str] | None) -> str:
    if row is None:
        return "candidate_not_visible_in_followup"
    group = str(row.get("contrast_group", "") or "")
    carry_ratio = _safe_float(row.get("carry_ratio"))
    visible = _safe_int(row.get("visible_probe_count"))
    carried = _safe_int(row.get("carried_probe_count"))
    kipped = _safe_int(row.get("kipp_probe_count"))
    if group == "multi_probe_carried_trace" or (visible >= 2 and carried >= 2 and carry_ratio >= 0.9):
        return "matured_to_multi_probe_carried"
    if group == "single_probe_carried_trace" or (visible == 1 and carried == 1):
        return "still_single_probe_carried"
    if kipped > 0 and carried > 0:
        return "partial_carry_with_kipp"
    if kipped > 0:
        return "kipped_in_followup"
    return "visible_but_unclassified"


def build_rows(candidates: list[dict[str, str]], new_contrast: list[dict[str, str]]) -> list[dict[str, Any]]:
    by_family = {_family_key(row): row for row in new_contrast if _family_key(row)}
    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        family = _family_key(candidate)
        new_row = by_family.get(family)
        rows.append(
            {
                "candidate_family": family,
                "prior_test_priority": candidate.get("test_priority", ""),
                "prior_profile_distance": candidate.get("profile_distance", ""),
                "followup_state": "visible" if new_row is not None else "missing",
                "new_contrast_group": new_row.get("contrast_group", "") if new_row else "-",
                "new_trace_carry_state": new_row.get("trace_carry_state", "") if new_row else "-",
                "new_visible_probe_count": new_row.get("visible_probe_count", "") if new_row else "0",
                "new_carried_probe_count": new_row.get("carried_probe_count", "") if new_row else "0",
                "new_kipp_probe_count": new_row.get("kipp_probe_count", "") if new_row else "0",
                "new_carry_ratio": new_row.get("carry_ratio", "") if new_row else "0",
                "new_sensory_field_distance": new_row.get("sensory_field_distance", "") if new_row else "",
                "new_lived_support_drop_count": new_row.get("lived_support_drop_count", "") if new_row else "0",
                "new_neuro_tone_reorganizes_count": new_row.get("neuro_tone_reorganizes_count", "") if new_row else "0",
                "new_text_island_same": _text_island_same(new_row) if new_row else False,
                "followup_reading": _followup_reading(new_row),
                **PASSIVE_FLAGS,
            }
        )
    return rows


def write_report(output_dir: Path, rows: list[dict[str, Any]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "passive_carry_followup_result.csv", rows, FIELDS + list(PASSIVE_FLAGS))
    counts: dict[str, int] = {}
    for row in rows:
        key = str(row.get("followup_reading", "unknown"))
        counts[key] = counts.get(key, 0) + 1
    summary = {
        "candidate_count": len(rows),
        "followup_counts": counts,
        "matured_candidates": [row["candidate_family"] for row in rows if row["followup_reading"] == "matured_to_multi_probe_carried"],
        "still_single_probe_candidates": [row["candidate_family"] for row in rows if row["followup_reading"] == "still_single_probe_carried"],
        "kipped_candidates": [row["candidate_family"] for row in rows if row["followup_reading"] == "kipped_in_followup"],
        "missing_candidates": [row["candidate_family"] for row in rows if row["followup_reading"] == "candidate_not_visible_in_followup"],
        **PASSIVE_FLAGS,
    }
    (output_dir / "passive_carry_followup_result.json").write_text(
        json.dumps({"summary": summary, "rows": rows}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    lines = [
        "# Passive Carry Follow-Up Result",
        "",
        "Passive Diagnose. Keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry-Signal, kein Richtungssignal.",
        "",
        f"- Kandidaten: {summary['candidate_count']}",
        f"- Ergebnisgruppen: {summary['followup_counts']}",
        "",
        "## Kandidaten",
        "",
    ]
    for row in rows:
        lines.append(
            "- {family}: {reading}; visible={visible}; carried={carried}; kipp={kipp}; ratio={ratio}".format(
                family=row["candidate_family"],
                reading=row["followup_reading"],
                visible=row["new_visible_probe_count"],
                carried=row["new_carried_probe_count"],
                kipp=row["new_kipp_probe_count"],
                ratio=row["new_carry_ratio"],
            )
        )
    text = "\n".join(lines) + "\n"
    (output_dir / "passive_carry_followup_result.md").write_text(text, encoding="utf-8")
    (output_dir / "passive_carry_followup_result.txt").write_text(
        "\n".join(f"{row['candidate_family']}: {row['followup_reading']}" for row in rows) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive carry follow-up result")
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--new-carry-contrast", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    candidates = _read_csv(args.candidates)
    new_contrast = _read_csv(args.new_carry_contrast)
    rows = build_rows(candidates, new_contrast)
    write_report(args.output_dir, rows)
    print(
        json.dumps(
            {
                "candidate_count": len(rows),
                "passive_only": True,
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
