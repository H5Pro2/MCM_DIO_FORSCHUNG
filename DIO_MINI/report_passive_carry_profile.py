"""Build a passive carry profile for stable Mini-DIO situational traces.

The report compares one carried reference family against nearby or strongly
kipping families. It is diagnostic only and must not be read by Mini-DIO for
runtime, action, gates, entries, or direction.
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


PROFILE_FIELDS = [
    "symbol_family",
    "contrast_group",
    "trace_carry_state",
    "visible_probe_count",
    "carried_probe_count",
    "kipp_probe_count",
    "carry_ratio",
    "sensory_field_distance",
    "sehen_flow_delta",
    "hoeren_energy_delta",
    "mcm_coherence_delta",
    "mcm_tension_delta",
    "mcm_asymmetry_delta",
    "direction_support_state",
    "left_dominant_best_action",
    "right_dominant_best_action",
    "best_reward_training_delta",
    "trade_readiness_delta",
    "lived_support_drop_count",
    "direction_flip_count",
    "neuro_tone_reorganizes_count",
    "no_visible_kipp_count",
    "left_text_island_symbol",
    "right_text_island_symbol",
    "dominant_kipp_state",
]


CONTRAST_FIELDS = [
    "reference_family",
    "family",
    "contrast_group",
    "trace_state",
    "profile_distance",
    "carry_ratio_gap",
    "sensory_distance_gap",
    "mcm_coherence_gap",
    "mcm_tension_gap",
    "mcm_asymmetry_gap",
    "lived_support_drop_gap",
    "neuro_tone_reorganizes_gap",
    "text_island_same",
    "contrast_reading",
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


def _profile_row(row: dict[str, str]) -> dict[str, Any]:
    result = {field: row.get(field, "") for field in PROFILE_FIELDS}
    result.update(PASSIVE_FLAGS)
    return result


def _text_island_same(row: dict[str, str]) -> bool:
    left = str(row.get("left_text_island_symbol", "") or row.get("left_text_island", "") or "")
    right = str(row.get("right_text_island_symbol", "") or row.get("right_text_island", "") or "")
    return bool(left and right and left == right)


def _profile_distance(reference: dict[str, str], row: dict[str, str]) -> float:
    weights = {
        "carry_ratio": 1.0,
        "sensory_field_distance": 0.8,
        "mcm_coherence_delta": 0.5,
        "mcm_tension_delta": 0.5,
        "mcm_asymmetry_delta": 0.5,
        "lived_support_drop_count": 0.7,
        "neuro_tone_reorganizes_count": 0.7,
    }
    total = 0.0
    for field, weight in weights.items():
        total += abs(_safe_float(row.get(field)) - _safe_float(reference.get(field))) * weight
    if _text_island_same(row) != _text_island_same(reference):
        total += 0.2
    return total


def _contrast_reading(reference: dict[str, str], row: dict[str, str]) -> str:
    carry_gap = _safe_float(reference.get("carry_ratio")) - _safe_float(row.get("carry_ratio"))
    support_gap = _safe_float(row.get("lived_support_drop_count")) - _safe_float(reference.get("lived_support_drop_count"))
    neuro_gap = _safe_float(row.get("neuro_tone_reorganizes_count")) - _safe_float(reference.get("neuro_tone_reorganizes_count"))
    visible_gap = _safe_int(reference.get("visible_probe_count")) - _safe_int(row.get("visible_probe_count"))
    contrast_group = str(row.get("contrast_group", "") or "")
    if carry_gap <= 0.05:
        if contrast_group == "single_probe_carried_trace" or visible_gap > 0:
            return "weak_carried_like_reference_needs_more_world_contact"
        return "carried_like_reference"
    if carry_gap > 0.5 and support_gap <= 0.5 and neuro_gap <= 0.5:
        return "less_carried_by_missing_tragedauer"
    if support_gap > 0.5 and neuro_gap > 0.5:
        return "less_carried_by_support_and_neuro_tone"
    if support_gap > 0.5:
        return "less_carried_by_lived_support"
    if neuro_gap > 0.5:
        return "less_carried_by_neuro_tone"
    return "less_carried_without_single_break"


def build_report(rows: list[dict[str, str]], family: str, topn: int) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    by_family = {str(row.get("family", "") or ""): row for row in rows}
    if not by_family or "" in by_family:
        by_family = {str(row.get("symbol_family", "") or ""): row for row in rows}
    if family not in by_family:
        raise ValueError(f"Reference family not found: {family}")
    reference = by_family[family]
    profile_rows = [_profile_row(reference)]

    contrast_rows: list[dict[str, Any]] = []
    candidates = [row for row in rows if row is not reference]
    candidates.sort(key=lambda row: (_profile_distance(reference, row), str(row.get("family", ""))))
    for row in candidates[: max(1, topn)]:
        contrast = {
            "reference_family": family,
            "family": row.get("symbol_family", "") or row.get("family", ""),
            "contrast_group": row.get("contrast_group", ""),
            "trace_state": row.get("trace_carry_state", "") or row.get("trace_state", ""),
            "profile_distance": round(_profile_distance(reference, row), 9),
            "carry_ratio_gap": round(_safe_float(reference.get("carry_ratio")) - _safe_float(row.get("carry_ratio")), 9),
            "sensory_distance_gap": round(_safe_float(row.get("sensory_field_distance")) - _safe_float(reference.get("sensory_field_distance")), 9),
            "mcm_coherence_gap": round(_safe_float(row.get("mcm_coherence_delta")) - _safe_float(reference.get("mcm_coherence_delta")), 9),
            "mcm_tension_gap": round(_safe_float(row.get("mcm_tension_delta")) - _safe_float(reference.get("mcm_tension_delta")), 9),
            "mcm_asymmetry_gap": round(_safe_float(row.get("mcm_asymmetry_delta")) - _safe_float(reference.get("mcm_asymmetry_delta")), 9),
            "lived_support_drop_gap": _safe_int(row.get("lived_support_drop_count")) - _safe_int(reference.get("lived_support_drop_count")),
            "neuro_tone_reorganizes_gap": _safe_int(row.get("neuro_tone_reorganizes_count")) - _safe_int(reference.get("neuro_tone_reorganizes_count")),
            "text_island_same": _text_island_same(row),
            "contrast_reading": _contrast_reading(reference, row),
            **PASSIVE_FLAGS,
        }
        contrast_rows.append(contrast)

    summary = {
        "reference_family": family,
        "reference_contrast_group": reference.get("contrast_group", ""),
        "reference_trace_state": reference.get("trace_carry_state", "") or reference.get("trace_state", ""),
        "reference_visible_probe_count": _safe_int(reference.get("visible_probe_count")),
        "reference_carried_probe_count": _safe_int(reference.get("carried_probe_count")),
        "reference_carry_ratio": _safe_float(reference.get("carry_ratio")),
        "reference_text_island": reference.get("left_text_island_symbol", "") or reference.get("left_text_island", ""),
        "contrast_count": len(contrast_rows),
        "nearest_contrast_family": contrast_rows[0]["family"] if contrast_rows else "-",
        "nearest_contrast_reading": contrast_rows[0]["contrast_reading"] if contrast_rows else "-",
        **PASSIVE_FLAGS,
    }
    return summary, profile_rows, contrast_rows


def write_report(output_dir: Path, summary: dict[str, Any], profile_rows: list[dict[str, Any]], contrast_rows: list[dict[str, Any]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "passive_carry_profile_reference.csv", profile_rows, PROFILE_FIELDS + list(PASSIVE_FLAGS))
    _write_csv(output_dir / "passive_carry_profile_contrast.csv", contrast_rows, CONTRAST_FIELDS + list(PASSIVE_FLAGS))
    (output_dir / "passive_carry_profile.json").write_text(
        json.dumps({"summary": summary, "reference": profile_rows, "contrast": contrast_rows}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    lines = [
        "# Passive Carry Profile",
        "",
        "Passive Diagnose. Keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry-Signal, kein Richtungssignal.",
        "",
        "## Referenz",
        "",
        f"- Familie: {summary['reference_family']}",
        f"- Gruppe: {summary['reference_contrast_group']}",
        f"- Trace: {summary['reference_trace_state']}",
        f"- Sichtbare Proben: {summary['reference_visible_probe_count']}",
        f"- Getragene Proben: {summary['reference_carried_probe_count']}",
        f"- Carry-Ratio: {summary['reference_carry_ratio']:.9f}",
        f"- Textinsel: {summary['reference_text_island']}",
        "",
        "## Nächste Gegenlagen",
        "",
    ]
    for row in contrast_rows[:10]:
        lines.append(
            "- {family}: {reading}; gruppe={group}; profile_distance={distance}; carry_gap={carry_gap}; "
            "support_gap={support}; neuro_gap={neuro}".format(
                family=row["family"],
                reading=row["contrast_reading"],
                group=row["contrast_group"],
                distance=row["profile_distance"],
                carry_gap=row["carry_ratio_gap"],
                support=row["lived_support_drop_gap"],
                neuro=row["neuro_tone_reorganizes_gap"],
            )
        )
    text = "\n".join(lines) + "\n"
    (output_dir / "passive_carry_profile.md").write_text(text, encoding="utf-8")
    (output_dir / "passive_carry_profile.txt").write_text(
        "\n".join(
            f"{row['family']}: {row['contrast_reading']} distance={row['profile_distance']}"
            for row in contrast_rows[:20]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive carry profile")
    parser.add_argument("--carry-contrast", type=Path, required=True)
    parser.add_argument("--family", default="dio_11vr")
    parser.add_argument("--topn", type=int, default=20)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    rows = _read_csv(args.carry_contrast)
    summary, profile_rows, contrast_rows = build_report(rows, args.family, args.topn)
    write_report(args.output_dir, summary, profile_rows, contrast_rows)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
