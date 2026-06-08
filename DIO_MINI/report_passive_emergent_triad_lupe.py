"""Inspect a passive emergent three-family island.

The report decomposes a semantic island into node roles and pair relations.
It is diagnostic only: no runtime memory, no action, no entry, no gate.
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

VECTOR_FIELDS = {
    "sehen": ["avg_sehen_form_flow", "avg_sehen_form_stability", "avg_sehen_form_change"],
    "hoeren": ["avg_hoeren_energy_tone", "avg_hoeren_energy_shift"],
    "fuehlen_mcm": ["avg_fuehlen_mcm_coherence", "avg_fuehlen_mcm_tension", "avg_fuehlen_mcm_asymmetry"],
    "zeit_nachhall": [
        "avg_mini_recurrence_strength",
        "avg_mini_afterimage",
        "avg_mini_time_distance",
        "avg_mini_temporal_form_distance",
        "avg_mini_temporal_trust_support",
        "avg_mini_temporal_caution_support",
    ],
    "neuro": [
        "avg_mini_focus_tone",
        "avg_mini_trust_tone",
        "avg_mini_caution_tone",
        "avg_mini_strain_tone",
        "avg_mini_relief_tone",
        "avg_mini_observation_tone",
        "avg_mini_neuro_support",
        "avg_mini_neuro_load",
        "avg_mini_neuro_balance",
    ],
    "reflexion": [
        "avg_reflection_context_carry",
        "avg_reflection_context_strain",
        "avg_reflection_context_alignment",
        "avg_reflection_world_support",
        "avg_reflection_current_support",
    ],
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


def _density_for_members(rows: list[dict[str, str]], members: list[str]) -> dict[str, str]:
    target = set(members)
    for row in rows:
        if set(_families(row.get("families"))) == target:
            return row
    return {}


def _containing_island_for_members(rows: list[dict[str, str]], members: list[str]) -> dict[str, str]:
    target = set(members)
    candidates: list[dict[str, str]] = []
    for row in rows:
        families = set(_families(row.get("families")))
        if target and target.issubset(families):
            candidates.append(row)
    if not candidates:
        return {}
    return sorted(candidates, key=lambda item: len(_families(item.get("families"))))[0]


def _distance(row: dict[str, str], centroid: dict[str, float], fields: list[str]) -> float:
    if not fields:
        return 0.0
    return sum(abs(_safe_float(row.get(field)) - centroid.get(field, 0.0)) for field in fields) / len(fields)


def _centroid(rows: list[dict[str, str]], fields: list[str]) -> dict[str, float]:
    result: dict[str, float] = {}
    for field in fields:
        result[field] = sum(_safe_float(row.get(field)) for row in rows) / max(1, len(rows))
    return result


def _node_role(edge_count: int, avg_distance: float, member_count: int) -> str:
    if member_count <= 1:
        return "single_trace"
    if edge_count >= member_count - 1 and avg_distance <= 0.010:
        return "bridge_core"
    if edge_count >= member_count - 1:
        return "structural_bridge"
    if edge_count > 0 and avg_distance <= 0.014:
        return "close_partner"
    if edge_count > 0:
        return "loose_partner"
    return "uncoupled_member"


def _triad_reading(edge_count: int, possible_edges: int, roles: list[str]) -> str:
    if possible_edges <= 0:
        return "single_or_empty_island"
    if edge_count == possible_edges:
        return "closed_triad_density"
    if "bridge_core" in roles or "structural_bridge" in roles:
        return "bridge_held_open_triad"
    if edge_count > 0:
        return "partial_coupling_triad"
    return "uncoupled_triad"


def build_report(
    label: str,
    meaning_space: Path,
    edges_csv: Path,
    density_csv: Path,
    members: list[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    meaning_rows = _read_csv(meaning_space)
    edge_rows = _read_csv(edges_csv)
    density_rows = _read_csv(density_csv)
    family_rows = {family: _family_row(meaning_rows, family) for family in members}
    present_members = [family for family, row in family_rows.items() if row]
    present_rows = [family_rows[family] for family in present_members]
    edge_by_key = _edge_lookup(edge_rows)

    pair_rows: list[dict[str, Any]] = []
    edge_count_by_family = {family: 0 for family in members}
    similarity_sum_by_family = {family: 0.0 for family in members}
    similarity_count_by_family = {family: 0 for family in members}

    for index, left in enumerate(members):
        for right in members[index + 1 :]:
            edge = edge_by_key.get(_edge_key(left, right), {})
            exists = bool(edge)
            if exists:
                edge_count_by_family[left] += 1
                edge_count_by_family[right] += 1
                sim = _safe_float(edge.get("meaning_similarity"))
                similarity_sum_by_family[left] += sim
                similarity_sum_by_family[right] += sim
                similarity_count_by_family[left] += 1
                similarity_count_by_family[right] += 1
            pair_rows.append(
                {
                    "stage": label,
                    "left_family": left,
                    "right_family": right,
                    "edge_visible": exists,
                    "meaning_similarity": round(_safe_float(edge.get("meaning_similarity")), 9) if exists else 0.0,
                    "sense_similarity": round(_safe_float(edge.get("sense_similarity")), 9) if exists else 0.0,
                    "mcm_similarity": round(_safe_float(edge.get("mcm_similarity")), 9) if exists else 0.0,
                    "hearing_similarity": round(_safe_float(edge.get("hearing_similarity")), 9) if exists else 0.0,
                    "temporal_similarity": round(_safe_float(edge.get("temporal_similarity")), 9) if exists else 0.0,
                    "neuro_similarity": round(_safe_float(edge.get("neuro_similarity")), 9) if exists else 0.0,
                    "reflection_similarity": round(_safe_float(edge.get("reflection_similarity")), 9) if exists else 0.0,
                    **BOUNDARY,
                }
            )

    all_fields = [field for fields in VECTOR_FIELDS.values() for field in fields]
    center = _centroid(present_rows, all_fields)
    node_rows: list[dict[str, Any]] = []
    for family in members:
        row = family_rows.get(family, {})
        found = bool(row)
        group_distances = {
            group: round(_distance(row, _centroid(present_rows, fields), fields), 9) if found and present_rows else 0.0
            for group, fields in VECTOR_FIELDS.items()
        }
        avg_distance = round(_distance(row, center, all_fields), 9) if found and present_rows else 0.0
        edge_count = edge_count_by_family.get(family, 0)
        avg_pair_similarity = similarity_sum_by_family.get(family, 0.0) / max(1, similarity_count_by_family.get(family, 0))
        node_rows.append(
            {
                "stage": label,
                "symbol_family": family,
                "family_found": found,
                "edge_count": edge_count,
                "avg_pair_similarity": round(avg_pair_similarity, 9),
                "centroid_distance": avg_distance,
                "node_role": _node_role(edge_count, avg_distance, max(1, len(present_members))) if found else "not_visible",
                "dominant_neuro_tone": str(row.get("dominant_neuro_tone", "") or "-"),
                "dominant_temporal_state": str(row.get("dominant_temporal_state", "") or "-"),
                "best_action_counts": str(row.get("best_action_counts", "") or "-"),
                "avg_observation_learning_pressure": round(_safe_float(row.get("avg_observation_learning_pressure")), 9),
                **{f"{group}_centroid_distance": value for group, value in group_distances.items()},
                **BOUNDARY,
            }
        )

    exact_density = _density_for_members(density_rows, present_members)
    containing_density = _containing_island_for_members(density_rows, present_members)
    density = exact_density or containing_density
    container_members = _families(containing_density.get("families")) if containing_density else []
    extra_members = sorted(set(container_members) - set(present_members))
    possible_edges = max(0, len(present_members) * (len(present_members) - 1) // 2)
    visible_edges = sum(1 for row in pair_rows if row["edge_visible"])
    summary = [
        {
            "stage": label,
            "requested_members": "|".join(members),
            "present_members": "|".join(present_members) if present_members else "-",
            "container_members": "|".join(container_members) if container_members else "-",
            "container_extra_members": "|".join(extra_members) if extra_members else "-",
            "container_state": "exact_triad_island" if exact_density else ("expanded_containing_island" if containing_density else "no_containing_island"),
            "present_count": len(present_members),
            "visible_edge_count": visible_edges,
            "possible_edge_count": possible_edges,
            "triad_reading": _triad_reading(visible_edges, possible_edges, [str(row["node_role"]) for row in node_rows]),
            "semantic_density": round(_safe_float(density.get("semantic_density")), 9),
            "variant_attraction": round(_safe_float(density.get("variant_attraction")), 9),
            "island_growth": round(_safe_float(density.get("island_growth")), 9),
            "island_fragmentation": round(_safe_float(density.get("island_fragmentation")), 9),
            "semantic_vorticity": round(_safe_float(density.get("semantic_vorticity")), 9),
            **BOUNDARY,
        }
    ]
    return node_rows, pair_rows, summary


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


def write_outputs(node_rows: list[dict[str, Any]], pair_rows: list[dict[str, Any]], summary: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "passive_emergent_triad_lupe_nodes.csv", node_rows, ["stage", "symbol_family"])
    _write_csv(output_dir / "passive_emergent_triad_lupe_pairs.csv", pair_rows, ["stage", "left_family", "right_family"])
    _write_csv(output_dir / "passive_emergent_triad_lupe_summary.csv", summary, ["stage"])
    (output_dir / "passive_emergent_triad_lupe.json").write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_emergent_triad_lupe.v1",
                "boundary": BOUNDARY,
                "nodes": node_rows,
                "pairs": pair_rows,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Passive Emergent Triad Lupe",
        "",
        "Passive Diagnose. Keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry, keine Richtung.",
        "",
        "## Summary",
        "",
    ]
    for row in summary:
        lines.append(
            f"- {row['stage']}: {row['triad_reading']}; members={row['present_members']}; "
            f"edges={row['visible_edge_count']}/{row['possible_edge_count']}; density={row['semantic_density']}"
        )
    lines.extend(["", "## Nodes", ""])
    for row in node_rows:
        lines.append(
            f"- {row['stage']} / {row['symbol_family']}: {row['node_role']}; "
            f"edges={row['edge_count']}; centroid={row['centroid_distance']}; "
            f"mcm={row['fuehlen_mcm_centroid_distance']}; hoeren={row['hoeren_centroid_distance']}"
        )
    lines.extend(["", "## Pairs", ""])
    for row in pair_rows:
        lines.append(
            f"- {row['stage']} / {row['left_family']} <-> {row['right_family']}: "
            f"edge={row['edge_visible']}; meaning={row['meaning_similarity']}; "
            f"mcm={row['mcm_similarity']}; hearing={row['hearing_similarity']}"
        )
    (output_dir / "passive_emergent_triad_lupe.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive emergent triad lupe")
    parser.add_argument("--label", required=True)
    parser.add_argument("--meaning-space", required=True, type=Path)
    parser.add_argument("--edges", required=True, type=Path)
    parser.add_argument("--density", required=True, type=Path)
    parser.add_argument("--member", action="append", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    nodes, pairs, summary = build_report(args.label, args.meaning_space, args.edges, args.density, list(args.member))
    write_outputs(nodes, pairs, summary, args.output_dir)
    print(
        json.dumps(
            {
                "label": args.label,
                "members": list(args.member),
                "node_rows": len(nodes),
                "pair_rows": len(pairs),
                "summary_rows": len(summary),
                **BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
