"""Classify passive inner spacetime traces across Mini-DIO stages.

Inner spacetime is used as a diagnostic term only:

- inner space: family proximity, edge coupling, island membership
- inner time: visibility, drift, disappearance, or recurrence across stages

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
    if not label:
        raise ValueError(f"Stage label is empty: {value}")
    return label, Path(parts[1].strip()), Path(parts[2].strip())


def _families(value: object) -> list[str]:
    text = str(value or "").strip()
    if not text or text == "-":
        return []
    return [item.strip() for item in text.split("|") if item.strip() and item.strip() != "-"]


def _family_row(rows: list[dict[str, str]], family: str) -> dict[str, str]:
    for row in rows:
        if str(row.get("symbol_family", "") or "") == family:
            return row
    return {}


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


def _island_count(rows: list[dict[str, str]], family: str) -> int:
    return sum(1 for row in rows if family in _families(row.get("families")))


def _vector(row: dict[str, str]) -> list[float]:
    return [_safe_float(row.get(field)) for field in VECTOR_FIELDS]


def _distance(left: list[float], right: list[float]) -> float:
    if not left or not right:
        return 0.0
    total = 0.0
    for a, b in zip(left, right):
        total += (a - b) * (a - b)
    return math.sqrt(total / max(1, min(len(left), len(right))))


def _mean(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def _classify(
    *,
    stage_count: int,
    visible_count: int,
    coupled_count: int,
    island_count: int,
    max_coupled_degree: int,
    missing_count: int,
    avg_drift: float,
) -> str:
    if visible_count == 0:
        return "spacetime_absent"
    if visible_count < stage_count and missing_count > 0 and coupled_count == 0:
        return "spacetime_fading_trace"
    if visible_count == stage_count and coupled_count == 0 and island_count > 0:
        return "spacetime_latent_persistent_trace"
    if visible_count == stage_count and coupled_count == stage_count and max_coupled_degree > 0 and avg_drift <= 0.004:
        return "spacetime_stable_coupled_core"
    if coupled_count > 0 and coupled_count < visible_count:
        return "spacetime_intermittent_coupling_trace"
    if visible_count == stage_count and avg_drift > 0.004:
        return "spacetime_visible_drift_trace"
    if visible_count == stage_count:
        return "spacetime_stable_visible_trace"
    return "spacetime_open_trace"


def _reading(state: str) -> str:
    return {
        "spacetime_absent": "Spur ist in den beobachteten Stufen nicht sichtbar.",
        "spacetime_fading_trace": "Spur verliert Sichtbarkeit und wirkt auslaufend.",
        "spacetime_latent_persistent_trace": "Spur bleibt ueber Zeit sichtbar, aber ohne aktuelle Kopplung.",
        "spacetime_stable_coupled_core": "Spur bleibt sichtbar und gekoppelt; stabiler Kernkandidat.",
        "spacetime_intermittent_coupling_trace": "Spur koppelt nur zeitweise; moegliche Reorganisation.",
        "spacetime_visible_drift_trace": "Spur bleibt sichtbar, driftet aber im inneren Vektorraum.",
        "spacetime_stable_visible_trace": "Spur bleibt sichtbar und relativ ruhig, aber ohne starke Kernlesart.",
        "spacetime_open_trace": "Spur ist offen und braucht weitere Folgeweltpruefung.",
    }.get(state, "Unbekannte Raumzeit-Lesart.")


def _all_families(loaded_stages: list[dict[str, Any]]) -> list[str]:
    result: set[str] = set()
    for stage in loaded_stages:
        for row in stage["meaning"]:
            family = str(row.get("symbol_family", "") or "")
            if family:
                result.add(family)
    return sorted(result)


def build_report(stages: list[tuple[str, Path, Path]], families: list[str], base_families: list[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    timeline_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    loaded_stages = []
    for label, meaning_path, matrix_dir in stages:
        loaded_stages.append(
            {
                "label": label,
                "meaning": _read_csv(meaning_path),
                "edges": _edge_lookup(_read_csv(matrix_dir / "passive_semantic_matrix_edges.csv")),
                "islands": _read_csv(matrix_dir / "passive_semantic_matrix_islands.csv"),
            }
        )

    if not families:
        families = _all_families(loaded_stages)

    for family in families:
        previous_visible_row: dict[str, str] = {}
        drifts: list[float] = []
        visible_count = 0
        coupled_stage_count = 0
        island_stage_count = 0
        max_coupled_degree = 0
        missing_count = 0

        for index, stage in enumerate(loaded_stages):
            row = _family_row(stage["meaning"], family)
            visible = bool(row)
            if visible:
                visible_count += 1
            else:
                missing_count += 1
            attached: list[str] = []
            for base in base_families:
                if stage["edges"].get(_edge_key(family, base)):
                    attached.append(base)
            if attached:
                coupled_stage_count += 1
                max_coupled_degree = max(max_coupled_degree, len(attached))
            island_count = _island_count(stage["islands"], family) if visible else 0
            if island_count:
                island_stage_count += 1
            drift = _distance(_vector(previous_visible_row), _vector(row)) if previous_visible_row and row else 0.0
            if previous_visible_row and row:
                drifts.append(drift)
            if row:
                previous_visible_row = row
            timeline_rows.append(
                {
                    "stage_index": index,
                    "stage_label": stage["label"],
                    "family": family,
                    "visible": visible,
                    "attached_base_families": "|".join(attached) if attached else "-",
                    "coupled_degree": len(attached),
                    "island_count": island_count,
                    "vector_drift_from_previous_visible": round(drift, 9),
                    "episode_count": _safe_int(row.get("episode_count")) if row else 0,
                    "dominant_neuro_tone": str(row.get("dominant_neuro_tone", "") or "-") if row else "-",
                    "dominant_temporal_state": str(row.get("dominant_temporal_state", "") or "-") if row else "-",
                    **BOUNDARY,
                }
            )

        avg_drift = _mean(drifts)
        state = _classify(
            stage_count=len(loaded_stages),
            visible_count=visible_count,
            coupled_count=coupled_stage_count,
            island_count=island_stage_count,
            max_coupled_degree=max_coupled_degree,
            missing_count=missing_count,
            avg_drift=avg_drift,
        )
        summary_rows.append(
            {
                "family": family,
                "base_families": "|".join(base_families) if base_families else "-",
                "stage_count": len(loaded_stages),
                "visible_count": visible_count,
                "missing_count": missing_count,
                "coupled_stage_count": coupled_stage_count,
                "island_stage_count": island_stage_count,
                "max_coupled_degree": max_coupled_degree,
                "avg_vector_drift": round(avg_drift, 9),
                "max_vector_drift": round(max(drifts) if drifts else 0.0, 9),
                "inner_spacetime_state": state,
                "inner_spacetime_reading": _reading(state),
                **BOUNDARY,
            }
        )
    return timeline_rows, summary_rows


def _state_distribution(summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: dict[str, int] = {}
    for row in summary:
        state = str(row.get("inner_spacetime_state", "") or "")
        counts[state] = counts.get(state, 0) + 1
    total = max(1, len(summary))
    return [
        {
            "inner_spacetime_state": state,
            "family_count": count,
            "family_rate": round(count / total, 9),
            **BOUNDARY,
        }
        for state, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def write_outputs(timeline: list[dict[str, Any]], summary: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    distribution = _state_distribution(summary)
    _write_csv(output_dir / "passive_inner_spacetime_timeline.csv", timeline, ["stage_label", "family"])
    _write_csv(output_dir / "passive_inner_spacetime_summary.csv", summary, ["family", "inner_spacetime_state"])
    _write_csv(output_dir / "passive_inner_spacetime_distribution.csv", distribution, ["inner_spacetime_state", "family_count"])
    (output_dir / "passive_inner_spacetime_lupe.json").write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_inner_spacetime_lupe.v1",
                "boundary": BOUNDARY,
                "timeline": timeline,
                "summary": summary,
                "distribution": distribution,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Passive Inner Spacetime Lupe",
        "",
        "Passive Diagnose. Innere Raumzeit meint hier relatives Bedeutungsraum-Zeit-Gefuege.",
        "Keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry, keine Richtung.",
        "",
        "## Summary",
        "",
    ]
    for row in distribution:
        lines.append(f"- {row['inner_spacetime_state']}: {row['family_count']} families ({row['family_rate']})")
    lines.extend(["", "## Families", ""])
    for row in summary:
        lines.append(
            f"- {row['family']}: {row['inner_spacetime_state']}; "
            f"visible={row['visible_count']}/{row['stage_count']}; "
            f"coupled={row['coupled_stage_count']}; islands={row['island_stage_count']}; "
            f"avg_drift={row['avg_vector_drift']}"
        )
    lines.extend(["", "## Timeline", ""])
    for row in timeline:
        lines.append(
            f"- {row['stage_label']} / {row['family']}: visible={row['visible']}; "
            f"attached={row['attached_base_families']}; island_count={row['island_count']}; "
            f"drift={row['vector_drift_from_previous_visible']}"
        )
    (output_dir / "passive_inner_spacetime_lupe.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive inner spacetime lupe")
    parser.add_argument("--stage", action="append", required=True, help="LABEL=passive_cluster_meaning_space.csv=semantic_matrix_dir")
    parser.add_argument("--family", action="append", default=[], help="Family to inspect. Omit for automatic all-family scan.")
    parser.add_argument("--base-family", action="append", default=[])
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    timeline, summary = build_report(
        [_parse_stage(raw) for raw in args.stage],
        families=list(args.family),
        base_families=list(args.base_family),
    )
    write_outputs(timeline, summary, args.output_dir)
    print(
        json.dumps(
            {
                "timeline_rows": len(timeline),
                "summary": summary,
                **BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
