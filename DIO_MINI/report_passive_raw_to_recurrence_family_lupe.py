"""Inspect raw-to-stable-recurrence text islands against their families.

Diagnostic only. This report joins the passive reorganized-core lupe with the
variant meaning-space rows and separates single-family recurrence from
multi-family semantic condensation.
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


SENSE_FIELDS = [
    "avg_sehen_form_flow",
    "avg_sehen_form_stability",
    "avg_sehen_form_change",
    "avg_hoeren_energy_tone",
    "avg_hoeren_energy_shift",
    "avg_fuehlen_mcm_coherence",
    "avg_fuehlen_mcm_tension",
    "avg_fuehlen_mcm_asymmetry",
]

TEMPORAL_FIELDS = [
    "avg_mini_recurrence_strength",
    "avg_mini_afterimage",
    "avg_mini_temporal_form_distance",
    "avg_mini_temporal_trust_support",
    "avg_mini_temporal_caution_support",
]

NEURO_FIELDS = [
    "avg_mini_focus_tone",
    "avg_mini_trust_tone",
    "avg_mini_caution_tone",
    "avg_mini_strain_tone",
    "avg_mini_observation_tone",
    "avg_mini_neuro_support",
    "avg_mini_neuro_load",
    "avg_mini_neuro_balance",
]


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


def _families(raw: str) -> list[str]:
    return [item for item in str(raw or "").split("|") if item]


def _mean(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def _span(values: list[float]) -> float:
    if not values:
        return 0.0
    return max(values) - min(values)


def _mode(row: dict, family_count: int) -> str:
    if family_count <= 1:
        return "single_family_stable_recurrence"
    if _safe_float(row.get("family_overlap")) >= 0.75:
        return "multi_family_coherent_condensation"
    return "multi_family_fragmented_condensation"


def build_report(reorganized_rows: list[dict], meaning_rows: list[dict]) -> tuple[list[dict], list[dict]]:
    meaning_by_family = {str(row.get("symbol_family", "") or ""): row for row in meaning_rows}
    targets = [
        row
        for row in reorganized_rows
        if str(row.get("core_entry_mode", "") or "") == "new_raw_to_stable_recurrence"
    ]
    details: list[dict] = []
    family_rows: list[dict] = []

    for row in targets:
        families = _families(str(row.get("last_families", "") or ""))
        linked = [meaning_by_family.get(family, {}) for family in families]
        mode = _mode(row, len(families))
        episode_counts = [_safe_int(item.get("episode_count")) for item in linked if item]
        source_counts = [_safe_int(item.get("source_count")) for item in linked if item]
        observation_pressure = [
            _safe_float(item.get("avg_observation_learning_pressure")) for item in linked if item
        ]
        trade_readiness = [_safe_float(item.get("avg_trade_readiness")) for item in linked if item]
        mcm_coherence = [_safe_float(item.get("avg_fuehlen_mcm_coherence")) for item in linked if item]
        hearing_tone = [_safe_float(item.get("avg_hoeren_energy_tone")) for item in linked if item]
        seeing_flow = [_safe_float(item.get("avg_sehen_form_flow")) for item in linked if item]
        neuro_balance = [_safe_float(item.get("avg_mini_neuro_balance")) for item in linked if item]

        details.append(
            {
                "text_island_symbol": str(row.get("text_island_symbol", "") or ""),
                "family_recurrence_mode": mode,
                "family_count": len(families),
                "families": "|".join(families),
                "score_delta": row.get("score_delta", ""),
                "last_score": row.get("last_score", ""),
                "family_overlap": row.get("family_overlap", ""),
                "episode_count_sum": sum(episode_counts),
                "source_count_sum": sum(source_counts),
                "avg_observation_learning_pressure": round(_mean(observation_pressure), 9),
                "avg_trade_readiness": round(_mean(trade_readiness), 9),
                "avg_fuehlen_mcm_coherence": round(_mean(mcm_coherence), 9),
                "span_fuehlen_mcm_coherence": round(_span(mcm_coherence), 9),
                "avg_hoeren_energy_tone": round(_mean(hearing_tone), 9),
                "span_hoeren_energy_tone": round(_span(hearing_tone), 9),
                "avg_sehen_form_flow": round(_mean(seeing_flow), 9),
                "span_sehen_form_flow": round(_span(seeing_flow), 9),
                "avg_mini_neuro_balance": round(_mean(neuro_balance), 9),
                "span_mini_neuro_balance": round(_span(neuro_balance), 9),
                "dominant_family_sentence": " | ".join(
                    str(item.get("dio_cluster_sentence", "") or "") for item in linked if item
                ),
                "dio_text_island_sentence": (
                    f"{row.get('text_island_symbol', '')}: {mode}; "
                    f"families={'|'.join(families)}; passiv, keine Handlung."
                ),
                **PASSIVE_BOUNDARY,
            }
        )
        for family, item in zip(families, linked):
            family_rows.append(
                {
                    "text_island_symbol": str(row.get("text_island_symbol", "") or ""),
                    "family_recurrence_mode": mode,
                    "symbol_family": family,
                    "episode_count": item.get("episode_count", ""),
                    "source_count": item.get("source_count", ""),
                    "dominant_action": item.get("dominant_action", ""),
                    "dominant_neuro_tone": item.get("dominant_neuro_tone", ""),
                    "dominant_temporal_state": item.get("dominant_temporal_state", ""),
                    "dominant_reflection_state": item.get("dominant_reflection_state", ""),
                    "best_action_counts": item.get("best_action_counts", ""),
                    "avg_observation_learning_pressure": item.get("avg_observation_learning_pressure", ""),
                    "avg_trade_readiness": item.get("avg_trade_readiness", ""),
                    **{field: item.get(field, "") for field in SENSE_FIELDS + TEMPORAL_FIELDS + NEURO_FIELDS},
                    "dio_cluster_sentence": item.get("dio_cluster_sentence", ""),
                    **PASSIVE_BOUNDARY,
                }
            )

    mode_counts: dict[str, int] = {}
    for row in details:
        mode = str(row.get("family_recurrence_mode", "") or "unknown")
        mode_counts[mode] = mode_counts.get(mode, 0) + 1
    summary = [
        {
            "summary_group": "family_recurrence_mode",
            "state": key,
            "count": value,
            **PASSIVE_BOUNDARY,
        }
        for key, value in sorted(mode_counts.items(), key=lambda item: (-item[1], item[0]))
    ]
    summary.append(
        {
            "summary_group": "totals",
            "state": "new_raw_to_stable_recurrence",
            "count": len(details),
            "avg_episode_count_sum": round(_mean([_safe_float(row.get("episode_count_sum")) for row in details]), 9),
            "avg_observation_learning_pressure": round(
                _mean([_safe_float(row.get("avg_observation_learning_pressure")) for row in details]),
                9,
            ),
            "avg_trade_readiness": round(_mean([_safe_float(row.get("avg_trade_readiness")) for row in details]), 9),
            **PASSIVE_BOUNDARY,
        }
    )
    return details + family_rows, summary


def write_outputs(rows: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_rows = [row for row in rows if "families" in row]
    family_rows = [row for row in rows if "symbol_family" in row]
    _write_csv(
        output_dir / "passive_raw_to_recurrence_family_lupe.csv",
        detail_rows,
        [
            "text_island_symbol",
            "family_recurrence_mode",
            "family_count",
            "families",
            "score_delta",
            "episode_count_sum",
            "avg_observation_learning_pressure",
            "avg_trade_readiness",
        ],
    )
    _write_csv(
        output_dir / "passive_raw_to_recurrence_family_lupe_families.csv",
        family_rows,
        ["text_island_symbol", "family_recurrence_mode", "symbol_family", "episode_count", "source_count"],
    )
    _write_csv(
        output_dir / "passive_raw_to_recurrence_family_lupe_summary.csv",
        summary,
        ["summary_group", "state", "count", "avg_episode_count_sum", "avg_observation_learning_pressure"],
    )
    payload = {
        "schema": "dio_mini_passive_raw_to_recurrence_family_lupe.v1",
        "boundary": dict(PASSIVE_BOUNDARY),
        "summary": summary,
        "text_islands": detail_rows,
        "families": family_rows,
    }
    (output_dir / "passive_raw_to_recurrence_family_lupe.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    lines = [
        "# Mini-DIO Passive Raw-to-Recurrence Family Lupe",
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
        extra = ""
        if "avg_episode_count_sum" in row:
            extra = (
                f"; avg_episode_count_sum={row.get('avg_episode_count_sum')}; "
                f"avg_observation_learning_pressure={row.get('avg_observation_learning_pressure')}; "
                f"avg_trade_readiness={row.get('avg_trade_readiness')}"
            )
        lines.append(f"- {row.get('summary_group')}:{row.get('state')} = {row.get('count')}{extra}")
    lines.extend(["", "## Textinseln"])
    for row in detail_rows:
        lines.append(
            f"- {row.get('text_island_symbol')}: {row.get('family_recurrence_mode')}; "
            f"families={row.get('families')}; episodes={row.get('episode_count_sum')}"
        )
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect raw-to-recurrence text islands against families.")
    parser.add_argument("--reorganized-core", required=True, type=Path)
    parser.add_argument("--meaning-space", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    rows, summary = build_report(_read_csv(args.reorganized_core), _read_csv(args.meaning_space))
    write_outputs(rows, summary, args.output_dir)
    print(
        json.dumps(
            {
                "output_dir": str(args.output_dir),
                "summary": summary,
                **PASSIVE_BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
