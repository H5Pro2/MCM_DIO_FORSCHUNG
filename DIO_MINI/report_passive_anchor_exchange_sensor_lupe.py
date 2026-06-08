"""Sensor lupe for passive anchor/exchange text islands.

The report joins anchor/exchange rows with left/right meaning-space families
and measures which sensory layer changes most visibly. Diagnostic only.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


PASSIVE_BOUNDARY = {
    "passive_only": True,
    "writes_runtime_memory": False,
    "read_by_mini_dio": False,
    "influences_action": False,
    "is_gate": False,
    "is_motoric": False,
    "is_entry_signal": False,
    "is_direction_signal": False,
}


LAYER_FIELDS = {
    "visual": ["avg_sehen_form_flow", "avg_sehen_form_stability", "avg_sehen_form_change"],
    "hearing": ["avg_hoeren_energy_tone", "avg_hoeren_energy_shift"],
    "feeling": ["avg_fuehlen_mcm_coherence", "avg_fuehlen_mcm_tension", "avg_fuehlen_mcm_asymmetry"],
    "neuro": [
        "avg_mini_neuro_balance",
        "avg_mini_focus_tone",
        "avg_mini_caution_tone",
        "avg_mini_strain_tone",
        "avg_mini_observation_tone",
    ],
}

OUTPUT_FIELDS = [
    "avg_sehen_form_flow",
    "avg_sehen_form_stability",
    "avg_sehen_form_change",
    "avg_hoeren_energy_tone",
    "avg_hoeren_energy_shift",
    "avg_fuehlen_mcm_coherence",
    "avg_fuehlen_mcm_tension",
    "avg_fuehlen_mcm_asymmetry",
    "avg_mini_neuro_balance",
    "avg_mini_focus_tone",
    "avg_mini_caution_tone",
    "avg_mini_strain_tone",
    "avg_mini_observation_tone",
]


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value if value not in (None, "") else default)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(fallback_fields)
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _families(raw: object) -> list[str]:
    return [item for item in str(raw or "").split("|") if item]


def _mean(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def _family_mean(rows: list[dict], fields: list[str]) -> float:
    values: list[float] = []
    for row in rows:
        for field in fields:
            values.append(_safe_float(row.get(field)))
    return _mean(values)


def _group_values(rows: list[dict], fields: list[str]) -> dict[str, float]:
    return {field: round(_family_mean(rows, [field]), 9) for field in fields}


def _layer_distance(left_rows: list[dict], right_rows: list[dict], layer: str) -> float:
    fields = LAYER_FIELDS[layer]
    if not left_rows or not right_rows:
        return 0.0
    return _mean(
        [
            abs(_family_mean(right_rows, [field]) - _family_mean(left_rows, [field]))
            for field in fields
        ]
    )


def _dominant_layer(deltas: dict[str, float]) -> str:
    if not deltas:
        return "unknown"
    ordered = sorted(deltas.items(), key=lambda item: item[1], reverse=True)
    if not ordered or ordered[0][1] <= 0.0:
        return "no_clear_sensor_delta"
    if len(ordered) > 1 and abs(ordered[0][1] - ordered[1][1]) < 0.002:
        return "mixed_sensor_delta"
    return f"{ordered[0][0]}_dominant_delta"


def build_report(anchor_rows: list[dict], left_meaning: list[dict], right_meaning: list[dict]) -> tuple[list[dict], list[dict]]:
    left_by_family = {str(row.get("symbol_family", "") or ""): row for row in left_meaning}
    right_by_family = {str(row.get("symbol_family", "") or ""): row for row in right_meaning}
    details: list[dict] = []

    for row in anchor_rows:
        if str(row.get("anchor_exchange_state", "") or "") != "anchor_exchange":
            continue
        anchor = _families(row.get("anchor_families"))
        removed = _families(row.get("removed_families"))
        added = _families(row.get("added_families"))
        left_anchor_rows = [left_by_family.get(family, {}) for family in anchor]
        right_anchor_rows = [right_by_family.get(family, {}) for family in anchor]
        removed_rows = [left_by_family.get(family, {}) for family in removed]
        added_rows = [right_by_family.get(family, {}) for family in added]
        left_anchor_rows = [item for item in left_anchor_rows if item]
        right_anchor_rows = [item for item in right_anchor_rows if item]
        removed_rows = [item for item in removed_rows if item]
        added_rows = [item for item in added_rows if item]
        exchange_distances = {
            layer: round(_layer_distance(removed_rows, added_rows, layer), 9)
            for layer in LAYER_FIELDS
        }
        anchor_shift_distances = {
            layer: round(_layer_distance(left_anchor_rows, right_anchor_rows, layer), 9)
            for layer in LAYER_FIELDS
        }
        removed_values = _group_values(removed_rows, OUTPUT_FIELDS)
        added_values = _group_values(added_rows, OUTPUT_FIELDS)
        anchor_left_values = _group_values(left_anchor_rows, OUTPUT_FIELDS)
        anchor_right_values = _group_values(right_anchor_rows, OUTPUT_FIELDS)
        dominant = _dominant_layer(exchange_distances)
        value_fields: dict[str, float] = {}
        for field in OUTPUT_FIELDS:
            value_fields[f"removed_{field}"] = removed_values[field]
            value_fields[f"added_{field}"] = added_values[field]
            value_fields[f"anchor_left_{field}"] = anchor_left_values[field]
            value_fields[f"anchor_right_{field}"] = anchor_right_values[field]
        details.append(
            {
                "text_island_symbol": row.get("text_island_symbol", ""),
                "sensor_exchange_state": dominant,
                "dominant_exchange_axis": dominant,
                "anchor_families": "|".join(anchor),
                "added_families": "|".join(added),
                "removed_families": "|".join(removed),
                "score_delta": row.get("score_delta", ""),
                "family_stability": row.get("family_stability", ""),
                "visual_exchange_distance": exchange_distances["visual"],
                "hearing_exchange_distance": exchange_distances["hearing"],
                "feeling_exchange_distance": exchange_distances["feeling"],
                "neuro_exchange_distance": exchange_distances["neuro"],
                "visual_anchor_shift_distance": anchor_shift_distances["visual"],
                "hearing_anchor_shift_distance": anchor_shift_distances["hearing"],
                "feeling_anchor_shift_distance": anchor_shift_distances["feeling"],
                "neuro_anchor_shift_distance": anchor_shift_distances["neuro"],
                "anchor_family_count": len(anchor),
                "removed_family_count": len(removed_rows),
                "added_family_count": len(added_rows),
                "dio_sensor_exchange_sentence": (
                    f"{row.get('text_island_symbol', '')}: {dominant}; "
                    f"anchor={'|'.join(anchor) or '-'}; added={'|'.join(added) or '-'}; "
                    f"removed={'|'.join(removed) or '-'}; passiv, keine Handlung."
                ),
                **value_fields,
                **PASSIVE_BOUNDARY,
            }
        )

    counts: dict[str, int] = {}
    for row in details:
        state = str(row.get("sensor_exchange_state", "") or "unknown")
        counts[state] = counts.get(state, 0) + 1
    summary = [
        {"summary_group": "sensor_exchange_state", "state": state, "count": count, **PASSIVE_BOUNDARY}
        for state, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]
    for layer in LAYER_FIELDS:
        summary.append(
            {
                "summary_group": "avg_exchange_distance",
                "state": layer,
                "value": round(_mean([_safe_float(row.get(f"{layer}_exchange_distance")) for row in details]), 9),
                **PASSIVE_BOUNDARY,
            }
        )
    for layer in LAYER_FIELDS:
        summary.append(
            {
                "summary_group": "avg_anchor_shift_distance",
                "state": layer,
                "value": round(_mean([_safe_float(row.get(f"{layer}_anchor_shift_distance")) for row in details]), 9),
                **PASSIVE_BOUNDARY,
            }
        )
    return details, summary


def write_outputs(details: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(
        output_dir / "passive_anchor_exchange_sensor_lupe.csv",
        details,
        [
            "text_island_symbol",
            "sensor_exchange_state",
            "anchor_families",
            "added_families",
            "removed_families",
            "visual_exchange_distance",
            "hearing_exchange_distance",
            "feeling_exchange_distance",
            "neuro_exchange_distance",
            "visual_anchor_shift_distance",
            "hearing_anchor_shift_distance",
            "feeling_anchor_shift_distance",
            "neuro_anchor_shift_distance",
        ],
    )
    _write_csv(
        output_dir / "passive_anchor_exchange_sensor_lupe_summary.csv",
        summary,
        ["summary_group", "state", "count", "value"],
    )
    payload = {
        "schema": "dio_mini_passive_anchor_exchange_sensor_lupe.v1",
        "boundary": dict(PASSIVE_BOUNDARY),
        "summary": summary,
        "details": details,
    }
    (output_dir / "passive_anchor_exchange_sensor_lupe.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    lines = [
        "# Mini-DIO Passive Anchor/Exchange Sensor Lupe",
        "",
        "## Grenze",
        "- Nur Diagnose.",
        "- Keine Runtime-Lesung.",
        "- Keine Handlung.",
        "- Kein Gate.",
        "- Kein Entry.",
        "- Keine Richtung.",
        "",
        "## Summary",
    ]
    for row in summary:
        lines.append(f"- {row.get('summary_group')}:{row.get('state')} = {row.get('count', row.get('value', ''))}")
    lines.extend(["", "## Details"])
    for row in details:
        lines.append(
            f"- {row.get('text_island_symbol')}: {row.get('sensor_exchange_state')}; "
            f"visual={row.get('visual_exchange_distance')}; hearing={row.get('hearing_exchange_distance')}; "
            f"feeling={row.get('feeling_exchange_distance')}; neuro={row.get('neuro_exchange_distance')}; "
            f"anchor_shift_visual={row.get('visual_anchor_shift_distance')}"
        )
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure passive sensor deltas for anchor/exchange text islands.")
    parser.add_argument("--anchor-exchange", required=True, type=Path)
    parser.add_argument("--left-meaning-space", required=True, type=Path)
    parser.add_argument("--right-meaning-space", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    details, summary = build_report(
        _read_csv(args.anchor_exchange),
        _read_csv(args.left_meaning_space),
        _read_csv(args.right_meaning_space),
    )
    write_outputs(details, summary, args.output_dir)
    print(
        json.dumps(
            {
                "output_dir": str(args.output_dir),
                "anchor_exchange_items": len(details),
                "summary": summary,
                **PASSIVE_BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
