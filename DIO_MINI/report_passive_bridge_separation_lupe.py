"""Inspect passive bridge separation between two controlled stages.

The report compares selected syntax families across two meaning-space and edge
matrices. It is diagnostic only: no runtime memory, no action, no entry, no
gate, no direction signal.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


BOUNDARY = {
    "passive_only": True,
    "writes_runtime_memory": False,
    "read_by_mini_dio": False,
    "influences_action": False,
    "is_gate": False,
    "is_motoric": False,
    "is_entry_signal": False,
    "is_direction_signal": False,
}

SENSE_FIELDS = {
    "sehen": ["avg_sehen_form_flow", "avg_sehen_form_stability", "avg_sehen_form_change"],
    "hoeren": ["avg_hoeren_energy_tone", "avg_hoeren_energy_shift"],
    "fuehlen_mcm": ["avg_fuehlen_mcm_coherence", "avg_fuehlen_mcm_tension", "avg_fuehlen_mcm_asymmetry"],
    "zeit": [
        "avg_mini_recurrence_strength",
        "avg_mini_afterimage",
        "avg_mini_time_distance",
        "avg_mini_temporal_form_distance",
    ],
    "neuro": ["avg_mini_neuro_support", "avg_mini_neuro_load", "avg_mini_neuro_balance"],
}


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value if value not in (None, "") else default)
    except Exception:
        return default
    if result != result:
        return default
    return result


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


def _group_delta(left: dict[str, str], right: dict[str, str], fields: list[str]) -> float:
    if not left or not right or not fields:
        return 0.0
    return sum(abs(_safe_float(left.get(field)) - _safe_float(right.get(field))) for field in fields) / len(fields)


def _edge_state(left_edges: dict[tuple[str, str], dict[str, str]], right_edges: dict[tuple[str, str], dict[str, str]], left: str, right: str) -> str:
    before = _edge_key(left, right) in left_edges
    after = _edge_key(left, right) in right_edges
    if before and after:
        return "edge_carried"
    if before and not after:
        return "edge_lost"
    if not before and after:
        return "edge_new"
    return "edge_absent"


def _family_state(left: dict[str, str], right: dict[str, str], edge_loss_count: int, edge_gain_count: int) -> str:
    if left and not right:
        return "family_not_carried"
    if not left and right:
        return "family_newly_visible"
    if not left and not right:
        return "family_absent"
    if edge_loss_count and not edge_gain_count:
        return "family_visible_but_decoupled"
    if edge_gain_count and not edge_loss_count:
        return "family_newly_coupled"
    if edge_loss_count and edge_gain_count:
        return "family_rewired"
    return "family_carried"


def build_report(
    left_label: str,
    right_label: str,
    left_meaning: Path,
    right_meaning: Path,
    left_edges_csv: Path,
    right_edges_csv: Path,
    families: list[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    left_rows = _read_csv(left_meaning)
    right_rows = _read_csv(right_meaning)
    left_edges = _edge_lookup(_read_csv(left_edges_csv))
    right_edges = _edge_lookup(_read_csv(right_edges_csv))

    family_rows: list[dict[str, Any]] = []
    pair_rows: list[dict[str, Any]] = []
    edge_changes_by_family = {family: {"lost": 0, "new": 0, "carried": 0} for family in families}

    for index, left_family in enumerate(families):
        for right_family in families[index + 1 :]:
            state = _edge_state(left_edges, right_edges, left_family, right_family)
            if state == "edge_lost":
                edge_changes_by_family[left_family]["lost"] += 1
                edge_changes_by_family[right_family]["lost"] += 1
            elif state == "edge_new":
                edge_changes_by_family[left_family]["new"] += 1
                edge_changes_by_family[right_family]["new"] += 1
            elif state == "edge_carried":
                edge_changes_by_family[left_family]["carried"] += 1
                edge_changes_by_family[right_family]["carried"] += 1
            right_edge = right_edges.get(_edge_key(left_family, right_family), {})
            left_edge = left_edges.get(_edge_key(left_family, right_family), {})
            pair_rows.append(
                {
                    "left_label": left_label,
                    "right_label": right_label,
                    "left_family": left_family,
                    "right_family": right_family,
                    "edge_transition": state,
                    "left_meaning_similarity": round(_safe_float(left_edge.get("meaning_similarity")), 9),
                    "right_meaning_similarity": round(_safe_float(right_edge.get("meaning_similarity")), 9),
                    "left_mcm_similarity": round(_safe_float(left_edge.get("mcm_similarity")), 9),
                    "right_mcm_similarity": round(_safe_float(right_edge.get("mcm_similarity")), 9),
                    "left_hearing_similarity": round(_safe_float(left_edge.get("hearing_similarity")), 9),
                    "right_hearing_similarity": round(_safe_float(right_edge.get("hearing_similarity")), 9),
                    **BOUNDARY,
                }
            )

    for family in families:
        left = _family_row(left_rows, family)
        right = _family_row(right_rows, family)
        changes = edge_changes_by_family[family]
        row: dict[str, Any] = {
            "family": family,
            "left_visible": bool(left),
            "right_visible": bool(right),
            "edge_lost_count": changes["lost"],
            "edge_new_count": changes["new"],
            "edge_carried_count": changes["carried"],
            "family_transition": _family_state(left, right, changes["lost"], changes["new"]),
            "left_text_hint": str(left.get("dominant_neuro_tone", "") or "-") if left else "-",
            "right_text_hint": str(right.get("dominant_neuro_tone", "") or "-") if right else "-",
        }
        for group, fields in SENSE_FIELDS.items():
            row[f"{group}_stage_delta"] = round(_group_delta(left, right, fields), 9)
        row.update(BOUNDARY)
        family_rows.append(row)

    summary_counts: dict[str, int] = {}
    for row in family_rows:
        state = str(row["family_transition"])
        summary_counts[state] = summary_counts.get(state, 0) + 1
    edge_counts: dict[str, int] = {}
    for row in pair_rows:
        state = str(row["edge_transition"])
        edge_counts[state] = edge_counts.get(state, 0) + 1
    summary = [
        {
            "left_label": left_label,
            "right_label": right_label,
            "family_count": len(families),
            "family_transition_counts": "|".join(f"{key}:{value}" for key, value in sorted(summary_counts.items())),
            "edge_transition_counts": "|".join(f"{key}:{value}" for key, value in sorted(edge_counts.items())),
            **BOUNDARY,
        }
    ]
    return family_rows, pair_rows, summary


def _write_csv(path: Path, rows: list[dict[str, Any]], fallback_fields: list[str]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fields:
                fields.append(key)
    if not fields:
        fields = fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(family_rows: list[dict[str, Any]], pair_rows: list[dict[str, Any]], summary: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "passive_bridge_separation_families.csv", family_rows, ["family"])
    _write_csv(output_dir / "passive_bridge_separation_pairs.csv", pair_rows, ["left_family", "right_family"])
    _write_csv(output_dir / "passive_bridge_separation_summary.csv", summary, ["left_label", "right_label"])
    (output_dir / "passive_bridge_separation_lupe.json").write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_bridge_separation_lupe.v1",
                "boundary": BOUNDARY,
                "families": family_rows,
                "pairs": pair_rows,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Passive Bridge Separation Lupe",
        "",
        "Passive Diagnose. Keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry, keine Richtung.",
        "",
        "## Summary",
        "",
    ]
    for row in summary:
        lines.append(f"- {row['left_label']} -> {row['right_label']}: {row['family_transition_counts']}; edges={row['edge_transition_counts']}")
    lines.extend(["", "## Families", ""])
    for row in family_rows:
        lines.append(
            f"- {row['family']}: {row['family_transition']}; lost={row['edge_lost_count']}; "
            f"new={row['edge_new_count']}; carried={row['edge_carried_count']}; "
            f"sehen_delta={row['sehen_stage_delta']}; hoeren_delta={row['hoeren_stage_delta']}; "
            f"mcm_delta={row['fuehlen_mcm_stage_delta']}"
        )
    lines.extend(["", "## Pairs", ""])
    for row in pair_rows:
        lines.append(f"- {row['left_family']} <-> {row['right_family']}: {row['edge_transition']}")
    (output_dir / "passive_bridge_separation_lupe.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect passive bridge separation between two stages.")
    parser.add_argument("--left-label", required=True)
    parser.add_argument("--right-label", required=True)
    parser.add_argument("--left-meaning-space", required=True)
    parser.add_argument("--right-meaning-space", required=True)
    parser.add_argument("--left-edges", required=True)
    parser.add_argument("--right-edges", required=True)
    parser.add_argument("--family", action="append", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    family_rows, pair_rows, summary = build_report(
        args.left_label,
        args.right_label,
        Path(args.left_meaning_space),
        Path(args.right_meaning_space),
        Path(args.left_edges),
        Path(args.right_edges),
        args.family,
    )
    write_outputs(family_rows, pair_rows, summary, Path(args.output_dir))
    print(
        json.dumps(
            {
                "families": len(family_rows),
                "pairs": len(pair_rows),
                "summary": summary,
                **BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
