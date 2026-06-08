"""Track one passive text island through maps and family meaning spaces.

Diagnostic only. The report follows a text-island symbol across labelled
inner maps and joins its current families with same-label meaning-space rows.
It does not write runtime memory and does not influence Mini-DIO action.
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


def _parse_label_path(raw: str) -> tuple[str, Path]:
    if "=" not in raw:
        path = Path(raw)
        return path.stem, path
    label, path = raw.split("=", 1)
    return label.strip(), Path(path.strip())


def _families(raw: str) -> list[str]:
    return [item for item in str(raw or "").split("|") if item]


def _mean(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def _span(values: list[float]) -> float:
    if not values:
        return 0.0
    return max(values) - min(values)


def build_lineage(
    text_island: str,
    map_sources: list[tuple[str, Path]],
    meaning_sources: list[tuple[str, Path]],
) -> tuple[list[dict], list[dict], list[dict]]:
    meaning_by_label = {
        label: {str(row.get("symbol_family", "") or ""): row for row in _read_csv(path)}
        for label, path in meaning_sources
    }
    map_rows: list[dict] = []
    family_rows: list[dict] = []

    for label, path in map_sources:
        found = {}
        for row in _read_csv(path):
            if str(row.get("text_island_symbol", "") or "") == text_island:
                found = row
                break
        families = _families(str(found.get("families", "") or "")) if found else []
        meaning_lookup = meaning_by_label.get(label, {})
        linked = [meaning_lookup.get(family, {}) for family in families]
        mcm = [_safe_float(item.get("avg_fuehlen_mcm_coherence")) for item in linked if item]
        hearing = [_safe_float(item.get("avg_hoeren_energy_tone")) for item in linked if item]
        seeing = [_safe_float(item.get("avg_sehen_form_flow")) for item in linked if item]
        neuro = [_safe_float(item.get("avg_mini_neuro_balance")) for item in linked if item]
        pressure = [_safe_float(item.get("avg_observation_learning_pressure")) for item in linked if item]

        map_rows.append(
            {
                "label": label,
                "text_island_symbol": text_island,
                "seen": 1 if found else 0,
                "inner_map_state": str(found.get("inner_map_state", "") or "absent"),
                "text_island_maturity_state": str(found.get("text_island_maturity_state", "") or "absent"),
                "semantic_maturity_score": found.get("semantic_maturity_score", "0"),
                "stability_pressure": found.get("stability_pressure", "0"),
                "variation_bearing": found.get("variation_bearing", "0"),
                "drift_pressure": found.get("drift_pressure", "0"),
                "rawness": found.get("rawness", "1"),
                "recurrence_count": found.get("recurrence_count", "0"),
                "family_count": len(families),
                "families": "|".join(families),
                "avg_family_mcm_coherence": round(_mean(mcm), 9),
                "span_family_mcm_coherence": round(_span(mcm), 9),
                "avg_family_hearing_tone": round(_mean(hearing), 9),
                "span_family_hearing_tone": round(_span(hearing), 9),
                "avg_family_seeing_flow": round(_mean(seeing), 9),
                "span_family_seeing_flow": round(_span(seeing), 9),
                "avg_family_neuro_balance": round(_mean(neuro), 9),
                "span_family_neuro_balance": round(_span(neuro), 9),
                "avg_observation_learning_pressure": round(_mean(pressure), 9),
                **PASSIVE_BOUNDARY,
            }
        )
        for family, item in zip(families, linked):
            family_rows.append(
                {
                    "label": label,
                    "text_island_symbol": text_island,
                    "symbol_family": family,
                    "family_seen_in_meaning_space": 1 if item else 0,
                    "episode_count": item.get("episode_count", ""),
                    "source_count": item.get("source_count", ""),
                    "dominant_action": item.get("dominant_action", ""),
                    "dominant_neuro_tone": item.get("dominant_neuro_tone", ""),
                    "dominant_temporal_state": item.get("dominant_temporal_state", ""),
                    "avg_sehen_form_flow": item.get("avg_sehen_form_flow", ""),
                    "avg_hoeren_energy_tone": item.get("avg_hoeren_energy_tone", ""),
                    "avg_fuehlen_mcm_coherence": item.get("avg_fuehlen_mcm_coherence", ""),
                    "avg_mini_neuro_balance": item.get("avg_mini_neuro_balance", ""),
                    "avg_observation_learning_pressure": item.get("avg_observation_learning_pressure", ""),
                    "dio_cluster_sentence": item.get("dio_cluster_sentence", ""),
                    **PASSIVE_BOUNDARY,
                }
            )

    scores = [_safe_float(row.get("semantic_maturity_score")) for row in map_rows]
    seen_count = sum(_safe_int(row.get("seen")) for row in map_rows)
    family_sets = [set(_families(str(row.get("families", "") or ""))) for row in map_rows if _safe_int(row.get("seen"))]
    stable_family_set = set.intersection(*family_sets) if family_sets else set()
    union_family_set = set.union(*family_sets) if family_sets else set()
    family_stability = len(stable_family_set) / max(1, len(union_family_set))
    summary = [
        {
            "summary_group": "lineage",
            "state": "seen_count",
            "count": seen_count,
            **PASSIVE_BOUNDARY,
        },
        {
            "summary_group": "lineage",
            "state": "score_delta_first_last",
            "value": round((scores[-1] if scores else 0.0) - (scores[0] if scores else 0.0), 9),
            **PASSIVE_BOUNDARY,
        },
        {
            "summary_group": "lineage",
            "state": "family_stability",
            "value": round(family_stability, 9),
            "stable_families": "|".join(sorted(stable_family_set)),
            "all_families": "|".join(sorted(union_family_set)),
            **PASSIVE_BOUNDARY,
        },
    ]
    return map_rows, family_rows, summary


def write_outputs(map_rows: list[dict], family_rows: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "passive_text_island_lineage_lupe.csv", map_rows, ["label", "text_island_symbol", "seen"])
    _write_csv(
        output_dir / "passive_text_island_lineage_lupe_families.csv",
        family_rows,
        ["label", "text_island_symbol", "symbol_family", "episode_count"],
    )
    _write_csv(output_dir / "passive_text_island_lineage_lupe_summary.csv", summary, ["summary_group", "state", "count", "value"])
    payload = {
        "schema": "dio_mini_passive_text_island_lineage_lupe.v1",
        "boundary": dict(PASSIVE_BOUNDARY),
        "lineage": map_rows,
        "families": family_rows,
        "summary": summary,
    }
    (output_dir / "passive_text_island_lineage_lupe.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    lines = [
        "# Mini-DIO Passive Text-Island Lineage Lupe",
        "",
        "## Grenze",
        "- Nur Diagnose.",
        "- Keine Runtime-Lesung.",
        "- Keine Handlung.",
        "- Kein Gate.",
        "- Kein Entry.",
        "- Keine Richtung.",
        "",
        "## Verlauf",
    ]
    for row in map_rows:
        lines.append(
            f"- {row.get('label')}: {row.get('inner_map_state')}; "
            f"score={row.get('semantic_maturity_score')}; families={row.get('families') or '-'}"
        )
    lines.extend(["", "## Summary"])
    for row in summary:
        lines.append(f"- {row.get('summary_group')}:{row.get('state')} = {row.get('count', row.get('value', ''))}")
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Track one passive text island through labelled maps.")
    parser.add_argument("--text-island", required=True)
    parser.add_argument("--map", action="append", required=True, help="label=path")
    parser.add_argument("--meaning-space", action="append", required=True, help="label=path")
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    map_sources = [_parse_label_path(raw) for raw in args.map]
    meaning_sources = [_parse_label_path(raw) for raw in args.meaning_space]
    map_rows, family_rows, summary = build_lineage(args.text_island, map_sources, meaning_sources)
    write_outputs(map_rows, family_rows, summary, args.output_dir)
    print(
        json.dumps(
            {
                "output_dir": str(args.output_dir),
                "text_island": args.text_island,
                "summary": summary,
                **PASSIVE_BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
