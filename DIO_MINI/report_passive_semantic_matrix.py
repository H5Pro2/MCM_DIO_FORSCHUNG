"""Build a passive semantic matrix from Mini-DIO syntax clusters.

The report combines the meaning-space and neighbor reports. It treats syntax
families as passive nodes and near/same meaning relations as passive edges.

Diagnostic only: no runtime memory, no action influence.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import deque
from pathlib import Path


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

EDGE_STATES = {
    "passive_same_meaning_island",
    "passive_near_meaning_neighbor",
}


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value or default)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(float(value or default))
    except Exception:
        return default


def _mean(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def _node_state(row: dict) -> str:
    candidate_loaded = str(row.get("candidate_loaded", "") or "").lower() == "true"
    episodes = _safe_int(row.get("episode_count"))
    reife = str(row.get("candidate_passive_reife_state", "") or "")
    if candidate_loaded and reife:
        return "semantic_core_candidate"
    if episodes >= 4:
        return "recurring_raw_semantic_trace"
    if episodes >= 2:
        return "raw_semantic_trace"
    return "single_contact_trace"


def _node_sentence(row: dict) -> str:
    family = str(row.get("symbol_family", "") or "")
    state = str(row.get("matrix_node_state", "") or "")
    if state == "semantic_core_candidate":
        return f"{family}: gereifter Kern einer passiven Bedeutungsinsel."
    if state == "recurring_raw_semantic_trace":
        return f"{family}: wiederkehrende rohe Syntaxspur im Bedeutungsraum."
    if state == "raw_semantic_trace":
        return f"{family}: rohe Syntaxspur mit erster Wiederkehr."
    return f"{family}: einzelner passiver Kontakt."


def _edge_sentence(row: dict) -> str:
    left = str(row.get("left_family", "") or "")
    right = str(row.get("right_family", "") or "")
    state = str(row.get("neighbor_state", "") or "")
    if state == "passive_same_meaning_island":
        return f"{left}+{right}: gleiche passive Bedeutungsinsel."
    if state == "passive_near_meaning_neighbor":
        return f"{left}+{right}: nahe passive Bedeutungsnachbarschaft."
    return f"{left}+{right}: keine Matrixkante."


def _select_edges(rows: list[dict], min_similarity: float) -> list[dict]:
    edges: list[dict] = []
    for row in rows:
        state = str(row.get("neighbor_state", "") or "")
        similarity = _safe_float(row.get("meaning_similarity"))
        if state not in EDGE_STATES or similarity < min_similarity:
            continue
        left = str(row.get("left_family", "") or "")
        right = str(row.get("right_family", "") or "")
        if not left or not right or left == right:
            continue
        item = {
            "left_family": left,
            "right_family": right,
            "neighbor_state": state,
            "meaning_similarity": round(similarity, 6),
            "sense_similarity": round(_safe_float(row.get("sense_similarity")), 6),
            "mcm_similarity": round(_safe_float(row.get("mcm_similarity")), 6),
            "hearing_similarity": round(_safe_float(row.get("hearing_similarity")), 6),
            "temporal_similarity": round(_safe_float(row.get("temporal_similarity")), 6),
            "neuro_similarity": round(_safe_float(row.get("neuro_similarity")), 6),
            "reflection_similarity": round(_safe_float(row.get("reflection_similarity")), 6),
            "reife_similarity": round(_safe_float(row.get("reife_similarity")), 6),
            "matrix_edge_state": "passive_semantic_matrix_edge",
            **BOUNDARY,
        }
        item["dio_matrix_edge_sentence"] = _edge_sentence(item)
        edges.append(item)
    edges.sort(key=lambda row: (-_safe_float(row.get("meaning_similarity")), row["left_family"], row["right_family"]))
    return edges


def _build_graph(edges: list[dict]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {}
    for edge in edges:
        left = str(edge.get("left_family", "") or "")
        right = str(edge.get("right_family", "") or "")
        graph.setdefault(left, set()).add(right)
        graph.setdefault(right, set()).add(left)
    return graph


def _connected_components(graph: dict[str, set[str]]) -> list[list[str]]:
    seen: set[str] = set()
    components: list[list[str]] = []
    for start in sorted(graph):
        if start in seen:
            continue
        queue = deque([start])
        seen.add(start)
        component: list[str] = []
        while queue:
            node = queue.popleft()
            component.append(node)
            for neighbor in sorted(graph.get(node, set())):
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        components.append(sorted(component))
    components.sort(key=lambda item: (-len(item), item[0] if item else ""))
    return components


def _build_nodes(rows: list[dict]) -> dict[str, dict]:
    nodes: dict[str, dict] = {}
    for row in rows:
        family = str(row.get("symbol_family", "") or "")
        if not family:
            continue
        item = {
            "symbol_family": family,
            "episode_count": _safe_int(row.get("episode_count")),
            "source_count": _safe_int(row.get("source_count")),
            "candidate_loaded": str(row.get("candidate_loaded", "") or ""),
            "candidate_passive_reife_state": str(row.get("candidate_passive_reife_state", "") or ""),
            "dominant_action": str(row.get("dominant_action", "") or ""),
            "dominant_neuro_tone": str(row.get("dominant_neuro_tone", "") or ""),
            "dominant_temporal_state": str(row.get("dominant_temporal_state", "") or ""),
            "avg_sehen_form_flow": round(_safe_float(row.get("avg_sehen_form_flow")), 6),
            "avg_hoeren_energy_tone": round(_safe_float(row.get("avg_hoeren_energy_tone")), 6),
            "avg_fuehlen_mcm_coherence": round(_safe_float(row.get("avg_fuehlen_mcm_coherence")), 6),
            "avg_observation_learning_pressure": round(_safe_float(row.get("avg_observation_learning_pressure")), 6),
            "candidate_meaning_preservation_rate": round(
                _safe_float(row.get("candidate_meaning_preservation_rate")), 6
            ),
            "candidate_stable_recurrence_rate": round(_safe_float(row.get("candidate_stable_recurrence_rate")), 6),
            "candidate_variant_capacity_rate": round(_safe_float(row.get("candidate_variant_capacity_rate")), 6),
            "candidate_temporal_fragility": round(_safe_float(row.get("candidate_temporal_fragility")), 6),
            **BOUNDARY,
        }
        item["matrix_node_state"] = _node_state(item)
        item["dio_matrix_node_sentence"] = _node_sentence(item)
        nodes[family] = item
    return nodes


def _summarize_islands(components: list[list[str]], nodes: dict[str, dict], edges: list[dict]) -> list[dict]:
    edge_index: dict[frozenset[str], dict] = {
        frozenset([str(edge.get("left_family", "")), str(edge.get("right_family", ""))]): edge for edge in edges
    }
    summaries: list[dict] = []
    for index, component in enumerate(components, start=1):
        core_nodes = [
            node for node in component if nodes.get(node, {}).get("matrix_node_state") == "semantic_core_candidate"
        ]
        raw_nodes = [node for node in component if node not in core_nodes]
        similarities: list[float] = []
        for i, left in enumerate(component):
            for right in component[i + 1 :]:
                edge = edge_index.get(frozenset([left, right]))
                if edge:
                    similarities.append(_safe_float(edge.get("meaning_similarity")))
        if core_nodes and raw_nodes:
            island_state = "core_with_raw_extensions"
        elif core_nodes:
            island_state = "core_only_island"
        elif len(component) > 1:
            island_state = "raw_semantic_island"
        else:
            island_state = "isolated_trace"
        row = {
            "island_id": f"dio_semantic_island_{index}",
            "island_state": island_state,
            "family_count": len(component),
            "families": "|".join(component),
            "core_families": "|".join(core_nodes) if core_nodes else "-",
            "raw_families": "|".join(raw_nodes) if raw_nodes else "-",
            "edge_count": len(similarities),
            "avg_meaning_similarity": round(_mean(similarities), 6),
            "max_meaning_similarity": round(max(similarities) if similarities else 0.0, 6),
            **BOUNDARY,
        }
        if island_state == "core_with_raw_extensions":
            row["dio_semantic_island_sentence"] = (
                f"{row['island_id']}: gereifter Kern mit rohen Erweiterungen; passive Matrixbildung."
            )
        elif island_state == "raw_semantic_island":
            row["dio_semantic_island_sentence"] = (
                f"{row['island_id']}: rohe Bedeutungsinsel ohne eigene Reife."
            )
        elif island_state == "core_only_island":
            row["dio_semantic_island_sentence"] = (
                f"{row['island_id']}: einzelner gereifter Kern ohne sichtbare Erweiterung."
            )
        elif island_state == "isolated_trace":
            row["dio_semantic_island_sentence"] = (
                f"{row['island_id']}: isolierte passive Syntaxspur."
            )
        else:
            row["dio_semantic_island_sentence"] = f"{row['island_id']}: {island_state}."
        summaries.append(row)
    return summaries


def build_matrix(meaning_rows: list[dict], neighbor_rows: list[dict], min_similarity: float) -> tuple[list[dict], list[dict], list[dict]]:
    nodes = _build_nodes(meaning_rows)
    edges = _select_edges(neighbor_rows, min_similarity)
    graph = _build_graph(edges)
    for family in nodes:
        graph.setdefault(family, set())
    components = _connected_components(graph)
    islands = _summarize_islands(components, nodes, edges)
    node_rows = sorted(nodes.values(), key=lambda row: (-_safe_int(row.get("episode_count")), row["symbol_family"]))
    return node_rows, edges, islands


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
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


def write_outputs(nodes: list[dict], edges: list[dict], islands: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "passive_semantic_matrix_nodes.csv", nodes, ["symbol_family", "matrix_node_state"])
    _write_csv(output_dir / "passive_semantic_matrix_edges.csv", edges, ["left_family", "right_family"])
    _write_csv(output_dir / "passive_semantic_matrix_islands.csv", islands, ["island_id", "island_state"])
    (output_dir / "passive_semantic_matrix.json").write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_semantic_matrix.v1",
                "boundary": BOUNDARY,
                "nodes": nodes,
                "edges": edges,
                "islands": islands,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Mini-DIO passive Semantikmatrix",
        "",
        "Ziel: wachsende Bedeutungsinseln aus emergenten Erlebnisspuren sichtbar machen.",
        "",
        "## Grenze",
        "- Nur Bericht.",
        "- Keine Runtime-Rueckfuehrung.",
        "- Keine Handlung.",
        "- Kein Gate.",
        "- Kein Entry.",
        "- Keine Richtung.",
        "",
        "## Inseln",
    ]
    for row in islands[:40]:
        lines.append(f"- {row['dio_semantic_island_sentence']} families={row['families']}")
    lines.extend(["", "## Knoten"])
    for row in nodes[:40]:
        lines.append(f"- {row['dio_matrix_node_sentence']} episodes={row['episode_count']}")
    lines.extend(["", "## Kanten"])
    for row in edges[:40]:
        lines.append(f"- {row['dio_matrix_edge_sentence']} similarity={row['meaning_similarity']}")
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive Mini-DIO semantic matrix report")
    parser.add_argument("--meaning-space", required=True, type=Path)
    parser.add_argument("--neighbors", required=True, type=Path)
    parser.add_argument("--min-similarity", type=float, default=0.96)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    meaning_rows = _read_csv(args.meaning_space)
    neighbor_rows = _read_csv(args.neighbors)
    nodes, edges, islands = build_matrix(meaning_rows, neighbor_rows, float(args.min_similarity))
    write_outputs(nodes, edges, islands, args.output_dir)
    print(
        json.dumps(
            {
                "nodes": len(nodes),
                "edges": len(edges),
                "islands": len(islands),
                "output_dir": str(args.output_dir),
                **BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
