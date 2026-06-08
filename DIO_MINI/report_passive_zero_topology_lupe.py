"""Inspect passive zero-topology candidates in Mini-DIO semantic islands.

This report treats "0-form" as a diagnostic topology idea, not as a rule:
an island may have a bridge-like center, peripheral members, open edges, and
group zones without being a fully connected clique.

Passive only. No runtime memory, no action, no gate, no entry, no direction.
Designed for controlled datasets first, not for long-run claims.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict, deque
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


def _families(value: object) -> list[str]:
    text = str(value or "").strip()
    if not text or text == "-":
        return []
    return [item.strip() for item in text.split("|") if item.strip() and item.strip() != "-"]


def _edge_key(left: str, right: str) -> str:
    return "|".join(sorted([left, right]))


def _components(nodes: list[str], edges: set[str]) -> list[list[str]]:
    node_set = set(nodes)
    graph: dict[str, set[str]] = {node: set() for node in node_set}
    for edge in edges:
        left, right = edge.split("|", 1)
        if left in node_set and right in node_set:
            graph[left].add(right)
            graph[right].add(left)
    seen: set[str] = set()
    groups: list[list[str]] = []
    for node in sorted(node_set):
        if node in seen:
            continue
        queue: deque[str] = deque([node])
        seen.add(node)
        group: list[str] = []
        while queue:
            current = queue.popleft()
            group.append(current)
            for other in sorted(graph[current]):
                if other not in seen:
                    seen.add(other)
                    queue.append(other)
        groups.append(sorted(group))
    return groups


def _classify_topology(
    *,
    family_count: int,
    possible_edges: int,
    edge_count: int,
    center_count: int,
    center_degree: int,
    periphery_group_count: int,
    periphery_edge_count: int,
) -> str:
    if family_count <= 1:
        return "single_trace_no_zero_topology"
    if edge_count >= possible_edges:
        return "closed_clique_not_open_zero_form"
    if center_count == 1 and center_degree >= max(2, family_count - 2) and periphery_group_count >= 1:
        if periphery_edge_count > 0:
            return "open_zero_form_with_periphery_expansion"
        return "open_zero_form_bridge_center"
    if center_count > 1 and edge_count < possible_edges:
        return "multi_center_open_field"
    if edge_count > 0:
        return "partial_open_island"
    return "uncoupled_field"


def build_report(matrix_dir: Path, density_dir: Path | None = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    islands = _read_csv(matrix_dir / "passive_semantic_matrix_islands.csv")
    edges = _read_csv(matrix_dir / "passive_semantic_matrix_edges.csv")
    density_rows = _read_csv((density_dir or matrix_dir) / "passive_semantic_density.csv")
    density_by_island = {str(row.get("island_id", "") or ""): row for row in density_rows}

    edge_set = {
        _edge_key(str(row.get("left_family", "") or ""), str(row.get("right_family", "") or ""))
        for row in edges
        if row.get("left_family") and row.get("right_family")
    }

    rows: list[dict[str, Any]] = []
    for island in islands:
        island_id = str(island.get("island_id", "") or "")
        members = sorted(_families(island.get("families")))
        if not members:
            continue
        member_set = set(members)
        local_edges = {
            edge
            for edge in edge_set
            if all(part in member_set for part in edge.split("|", 1))
        }
        degree: dict[str, int] = defaultdict(int)
        for edge in local_edges:
            left, right = edge.split("|", 1)
            degree[left] += 1
            degree[right] += 1
        max_degree = max([degree.get(member, 0) for member in members] or [0])
        centers = sorted(member for member in members if degree.get(member, 0) == max_degree and max_degree > 0)
        center = centers[0] if len(centers) == 1 else "-"
        periphery = [member for member in members if member != center]
        periphery_edges = {
            edge
            for edge in local_edges
            if center == "-" or center not in edge.split("|", 1)
        }
        periphery_groups = _components(periphery, periphery_edges) if periphery else []
        possible_edges = max(0, len(members) * (len(members) - 1) // 2)
        local_edge_density = len(local_edges) / max(1, possible_edges)
        density = density_by_island.get(island_id, {})
        topology_state = _classify_topology(
            family_count=len(members),
            possible_edges=possible_edges,
            edge_count=len(local_edges),
            center_count=len(centers),
            center_degree=max_degree,
            periphery_group_count=len(periphery_groups),
            periphery_edge_count=len(periphery_edges),
        )
        rows.append(
            {
                "island_id": island_id,
                "topology_state": topology_state,
                "family_count": len(members),
                "center_family": center,
                "center_candidates": "|".join(centers) if centers else "-",
                "center_degree": max_degree,
                "periphery_count": len(periphery),
                "periphery_group_count": len(periphery_groups),
                "periphery_groups": ";".join("|".join(group) for group in periphery_groups) if periphery_groups else "-",
                "edge_count": len(local_edges),
                "possible_edge_count": possible_edges,
                "local_edge_density": round(local_edge_density, 6),
                "open_edge_count": max(0, possible_edges - len(local_edges)),
                "semantic_density": round(_safe_float(density.get("semantic_density")), 6),
                "variant_attraction": round(_safe_float(density.get("variant_attraction")), 6),
                "island_growth": round(_safe_float(density.get("island_growth")), 6),
                "semantic_vorticity": round(_safe_float(density.get("semantic_vorticity")), 6),
                "families": "|".join(members),
                "mcm_form_anchor_reading": _reading(topology_state),
                **BOUNDARY,
            }
        )

    priority = {
        "open_zero_form_with_periphery_expansion": 0,
        "open_zero_form_bridge_center": 1,
        "multi_center_open_field": 2,
        "partial_open_island": 3,
        "closed_clique_not_open_zero_form": 4,
        "uncoupled_field": 5,
        "single_trace_no_zero_topology": 6,
    }
    rows.sort(
        key=lambda row: (
            priority.get(str(row.get("topology_state")), 99),
            -_safe_float(row.get("semantic_density")),
            str(row.get("island_id", "")),
        )
    )
    summary_counts: dict[str, int] = defaultdict(int)
    for row in rows:
        summary_counts[str(row.get("topology_state", ""))] += 1
    summary = [
        {
            "metric": key,
            "value": value,
            **BOUNDARY,
        }
        for key, value in sorted(summary_counts.items())
    ]
    summary.extend(
        [
            {"metric": "island_count", "value": len(rows), **BOUNDARY},
            {
                "metric": "zero_topology_candidate_count",
                "value": sum(
                    1
                    for row in rows
                    if str(row.get("topology_state")) in {"open_zero_form_with_periphery_expansion", "open_zero_form_bridge_center"}
                ),
                **BOUNDARY,
            },
        ]
    )
    return rows, summary


def _reading(state: str) -> str:
    if state == "open_zero_form_with_periphery_expansion":
        return "Offene Zentrum-Peripherie-Form mit neuer Randkopplung; passive 0-Topologie-Kandidatur."
    if state == "open_zero_form_bridge_center":
        return "Offene Zentrum-Peripherie-Form; Stabilitaet laeuft ueber Brueckenzentrum, nicht ueber Vollvernetzung."
    if state == "multi_center_open_field":
        return "Offenes Feld mit mehreren moeglichen Zentren; Zentrum noch nicht eindeutig verdichtet."
    if state == "partial_open_island":
        return "Teilinsel mit Kopplung, aber ohne klare Zentrum-Peripherie-Lesart."
    if state == "closed_clique_not_open_zero_form":
        return "Geschlossene Clique; starke Direktvernetzung, aber keine offene 0-Form."
    if state == "uncoupled_field":
        return "Insel ohne sichtbare Kanten; keine getragene Topologie."
    return "Einzelspur; keine Topologie pruefbar."


def write_outputs(rows: list[dict[str, Any]], summary: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "passive_zero_topology_lupe.csv", rows, ["island_id", "topology_state"])
    _write_csv(output_dir / "passive_zero_topology_lupe_summary.csv", summary, ["metric", "value"])
    (output_dir / "passive_zero_topology_lupe.json").write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_zero_topology_lupe.v1",
                "boundary": BOUNDARY,
                "rows": rows,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Passive Zero Topology Lupe",
        "",
        "Passive Diagnose fuer kontrollierte Datensaetze. Keine Aussage ueber lange Laeufe.",
        "Keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry, keine Richtung.",
        "",
        "## Summary",
        "",
    ]
    for row in summary:
        lines.append(f"- {row['metric']}: {row['value']}")
    lines.extend(["", "## Top Candidates", ""])
    for row in rows[:20]:
        lines.append(
            f"- {row['island_id']}: {row['topology_state']}; center={row['center_family']}; "
            f"groups={row['periphery_group_count']}; members={row['families']}"
        )
    (output_dir / "passive_zero_topology_lupe.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive zero-topology lupe")
    parser.add_argument("--matrix-dir", required=True, type=Path)
    parser.add_argument("--density-dir", type=Path, default=None)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    rows, summary = build_report(args.matrix_dir, args.density_dir)
    write_outputs(rows, summary, args.output_dir)
    print(
        json.dumps(
            {
                "rows": len(rows),
                "summary": {str(row["metric"]): row["value"] for row in summary},
                **BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
