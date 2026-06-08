"""Inspect whether latent spacetime traces form their own passive islands.

Input is the auto-scan summary from report_passive_inner_spacetime_lupe.py and
one or more semantic matrix stages. The report takes families in a selected
spacetime state, usually spacetime_latent_persistent_trace, and checks whether
they are isolated leftovers or form connected sub-islands outside the watched
core.

Passive only. No runtime memory, no action, no gate, no entry, no direction.
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


def _families(value: object) -> list[str]:
    text = str(value or "").strip()
    if not text or text == "-":
        return []
    return [item.strip() for item in text.split("|") if item.strip() and item.strip() != "-"]


def _parse_stage(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise ValueError(f"Stage must be LABEL=semantic_matrix_dir: {value}")
    label, raw_path = value.split("=", 1)
    label = label.strip()
    if not label:
        raise ValueError(f"Stage label is empty: {value}")
    return label, Path(raw_path.strip())


def _candidate_families(summary_path: Path, state: str, limit: int) -> list[str]:
    rows = _read_csv(summary_path)
    candidates = [
        row
        for row in rows
        if str(row.get("inner_spacetime_state", "") or "") == state
    ]
    candidates.sort(key=lambda row: (_safe_float(row.get("avg_vector_drift")), str(row.get("family", "") or "")))
    if limit > 0:
        candidates = candidates[:limit]
    return [str(row.get("family", "") or "") for row in candidates if row.get("family")]


def _components(nodes: set[str], edges: list[tuple[str, str]]) -> list[set[str]]:
    graph: dict[str, set[str]] = {node: set() for node in nodes}
    for left, right in edges:
        graph.setdefault(left, set()).add(right)
        graph.setdefault(right, set()).add(left)
    seen: set[str] = set()
    result: list[set[str]] = []
    for node in sorted(nodes):
        if node in seen:
            continue
        queue = deque([node])
        seen.add(node)
        component = {node}
        while queue:
            current = queue.popleft()
            for neighbor in graph.get(current, set()):
                if neighbor not in seen:
                    seen.add(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)
        result.append(component)
    result.sort(key=lambda item: (-len(item), sorted(item)[0] if item else ""))
    return result


def build_report(summary_path: Path, stages: list[tuple[str, Path]], state: str, limit: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    candidates = set(_candidate_families(summary_path, state, limit))
    stage_rows: list[dict[str, Any]] = []
    island_rows: list[dict[str, Any]] = []

    for label, matrix_dir in stages:
        edge_rows = _read_csv(matrix_dir / "passive_semantic_matrix_edges.csv")
        matrix_islands = _read_csv(matrix_dir / "passive_semantic_matrix_islands.csv")
        latent_edges: list[tuple[str, str]] = []
        edge_similarity_sum = 0.0
        for row in edge_rows:
            left = str(row.get("left_family", "") or "")
            right = str(row.get("right_family", "") or "")
            if left in candidates and right in candidates:
                latent_edges.append(tuple(sorted([left, right])))
                edge_similarity_sum += _safe_float(row.get("meaning_similarity"))

        connected_nodes = {family for edge in latent_edges for family in edge}
        components = _components(candidates, latent_edges)
        nontrivial = [component for component in components if len(component) > 1]
        latent_island_hits = 0
        largest_matrix_island = 0
        for island in matrix_islands:
            members = set(_families(island.get("families"))) & candidates
            if members:
                latent_island_hits += 1
                largest_matrix_island = max(largest_matrix_island, len(members))
        stage_rows.append(
            {
                "stage_label": label,
                "candidate_state": state,
                "candidate_count": len(candidates),
                "latent_edge_count": len(latent_edges),
                "connected_latent_family_count": len(connected_nodes),
                "isolated_latent_family_count": max(0, len(candidates) - len(connected_nodes)),
                "component_count": len(components),
                "nontrivial_component_count": len(nontrivial),
                "largest_component_size": max([len(component) for component in components] or [0]),
                "latent_matrix_island_hits": latent_island_hits,
                "largest_matrix_island_latent_count": largest_matrix_island,
                "avg_latent_edge_similarity": round(edge_similarity_sum / max(1, len(latent_edges)), 9) if latent_edges else 0.0,
                **BOUNDARY,
            }
        )
        for index, component in enumerate(nontrivial[:20], start=1):
            island_rows.append(
                {
                    "stage_label": label,
                    "component_rank": index,
                    "component_size": len(component),
                    "families": "|".join(sorted(component)),
                    **BOUNDARY,
                }
            )

    total_edges = sum(int(row["latent_edge_count"]) for row in stage_rows)
    total_nontrivial = sum(int(row["nontrivial_component_count"]) for row in stage_rows)
    summary_rows = [
        {
            "candidate_state": state,
            "candidate_count": len(candidates),
            "stage_count": len(stages),
            "total_latent_edge_count": total_edges,
            "total_nontrivial_component_count": total_nontrivial,
            "max_largest_component_size": max([int(row["largest_component_size"]) for row in stage_rows] or [0]),
            "max_largest_matrix_island_latent_count": max([int(row["largest_matrix_island_latent_count"]) for row in stage_rows] or [0]),
            "latent_island_reading": _reading(total_edges, total_nontrivial),
            **BOUNDARY,
        }
    ]
    return stage_rows, island_rows, summary_rows


def _reading(total_edges: int, total_nontrivial: int) -> str:
    if total_edges <= 0:
        return "Latente Spuren sind in dieser Sicht vor allem isolierter Nachhall."
    if total_nontrivial <= 0:
        return "Latente Spuren haben Kanten, bilden aber noch keine klaren Teilinseln."
    return "Latente Spuren bilden eigene verbundene Teilmuster ausserhalb der beobachteten Kernkopplung."


def write_outputs(stage_rows: list[dict[str, Any]], island_rows: list[dict[str, Any]], summary_rows: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "passive_latent_island_stage_summary.csv", stage_rows, ["stage_label"])
    _write_csv(output_dir / "passive_latent_island_components.csv", island_rows, ["stage_label", "component_rank"])
    _write_csv(output_dir / "passive_latent_island_summary.csv", summary_rows, ["candidate_state"])
    (output_dir / "passive_latent_island_lupe.json").write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_latent_island_lupe.v1",
                "boundary": BOUNDARY,
                "stage_summary": stage_rows,
                "components": island_rows,
                "summary": summary_rows,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Passive Latent Island Lupe",
        "",
        "Passive Diagnose. Prueft, ob latente Raumzeit-Spuren eigene Teilmuster bilden.",
        "Keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry, keine Richtung.",
        "",
        "## Summary",
        "",
    ]
    for row in summary_rows:
        lines.append(
            f"- {row['candidate_state']}: candidates={row['candidate_count']}; "
            f"edges={row['total_latent_edge_count']}; components={row['total_nontrivial_component_count']}; "
            f"largest={row['max_largest_component_size']}"
        )
    lines.extend(["", "## Stages", ""])
    for row in stage_rows:
        lines.append(
            f"- {row['stage_label']}: edges={row['latent_edge_count']}; "
            f"connected={row['connected_latent_family_count']}; isolated={row['isolated_latent_family_count']}; "
            f"nontrivial_components={row['nontrivial_component_count']}; largest={row['largest_component_size']}"
        )
    lines.extend(["", "## Top Components", ""])
    for row in island_rows[:40]:
        lines.append(f"- {row['stage_label']} #{row['component_rank']}: size={row['component_size']}; {row['families']}")
    (output_dir / "passive_latent_island_lupe.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive latent island lupe")
    parser.add_argument("--spacetime-summary", required=True, type=Path)
    parser.add_argument("--state", default="spacetime_latent_persistent_trace")
    parser.add_argument("--stage", action="append", required=True, help="LABEL=semantic_matrix_dir")
    parser.add_argument("--limit", type=int, default=0, help="Limit candidates by lowest avg drift. 0 means all.")
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    stage_rows, island_rows, summary_rows = build_report(
        args.spacetime_summary,
        [_parse_stage(raw) for raw in args.stage],
        args.state,
        args.limit,
    )
    write_outputs(stage_rows, island_rows, summary_rows, args.output_dir)
    print(
        json.dumps(
            {
                "stage_rows": len(stage_rows),
                "components": len(island_rows),
                "summary": summary_rows,
                **BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
