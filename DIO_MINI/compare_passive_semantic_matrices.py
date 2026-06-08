"""Compare two passive Mini-DIO semantic matrix reports.

Diagnostic only: no runtime memory and no action influence.
"""

from __future__ import annotations

import argparse
import csv
import json
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


def _edge_key(row: dict) -> str:
    left = str(row.get("left_family", "") or "")
    right = str(row.get("right_family", "") or "")
    return "|".join(sorted([left, right]))


def _load_matrix(root: Path) -> dict:
    nodes = _read_csv(root / "passive_semantic_matrix_nodes.csv")
    edges = _read_csv(root / "passive_semantic_matrix_edges.csv")
    islands = _read_csv(root / "passive_semantic_matrix_islands.csv")
    return {
        "root": str(root),
        "nodes": nodes,
        "edges": edges,
        "islands": islands,
        "node_families": {str(row.get("symbol_family", "") or "") for row in nodes},
        "edge_keys": {_edge_key(row) for row in edges},
    }


def compare(reference: dict, candidate: dict) -> tuple[list[dict], list[dict]]:
    ref_nodes = reference["node_families"]
    cand_nodes = candidate["node_families"]
    ref_edges = reference["edge_keys"]
    cand_edges = candidate["edge_keys"]

    shared_nodes = sorted(ref_nodes & cand_nodes)
    missing_nodes = sorted(ref_nodes - cand_nodes)
    new_nodes = sorted(cand_nodes - ref_nodes)
    shared_edges = sorted(ref_edges & cand_edges)
    missing_edges = sorted(ref_edges - cand_edges)
    new_edges = sorted(cand_edges - ref_edges)

    ref_sim = [_safe_float(row.get("avg_meaning_similarity")) for row in reference["islands"]]
    cand_sim = [_safe_float(row.get("avg_meaning_similarity")) for row in candidate["islands"]]

    summary = [
        {
            "metric": "node_count_reference",
            "value": len(ref_nodes),
            **BOUNDARY,
        },
        {
            "metric": "node_count_candidate",
            "value": len(cand_nodes),
            **BOUNDARY,
        },
        {
            "metric": "shared_node_count",
            "value": len(shared_nodes),
            **BOUNDARY,
        },
        {
            "metric": "node_reproduction_rate",
            "value": round(len(shared_nodes) / max(1, len(ref_nodes)), 6),
            **BOUNDARY,
        },
        {
            "metric": "edge_count_reference",
            "value": len(ref_edges),
            **BOUNDARY,
        },
        {
            "metric": "edge_count_candidate",
            "value": len(cand_edges),
            **BOUNDARY,
        },
        {
            "metric": "shared_edge_count",
            "value": len(shared_edges),
            **BOUNDARY,
        },
        {
            "metric": "edge_reproduction_rate",
            "value": round(len(shared_edges) / max(1, len(ref_edges)), 6),
            **BOUNDARY,
        },
        {
            "metric": "island_count_reference",
            "value": len(reference["islands"]),
            **BOUNDARY,
        },
        {
            "metric": "island_count_candidate",
            "value": len(candidate["islands"]),
            **BOUNDARY,
        },
        {
            "metric": "avg_island_similarity_reference",
            "value": round(_mean(ref_sim), 6),
            **BOUNDARY,
        },
        {
            "metric": "avg_island_similarity_candidate",
            "value": round(_mean(cand_sim), 6),
            **BOUNDARY,
        },
    ]

    details = []
    for kind, values in [
        ("shared_node", shared_nodes),
        ("missing_node", missing_nodes),
        ("new_node", new_nodes),
        ("shared_edge", shared_edges),
        ("missing_edge", missing_edges),
        ("new_edge", new_edges),
    ]:
        for value in values:
            details.append({"kind": kind, "value": value, **BOUNDARY})

    return summary, details


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


def write_outputs(summary: list[dict], details: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "passive_semantic_matrix_compare_summary.csv", summary, ["metric", "value"])
    _write_csv(output_dir / "passive_semantic_matrix_compare_details.csv", details, ["kind", "value"])
    payload = {"schema": "dio_mini_passive_semantic_matrix_compare.v1", "boundary": BOUNDARY, "summary": summary, "details": details}
    (output_dir / "passive_semantic_matrix_compare.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    lookup = {row["metric"]: row["value"] for row in summary}
    lines = [
        "# Mini-DIO passive Semantikmatrix Vergleich",
        "",
        "## Grenze",
        "- Nur Bericht.",
        "- Keine Runtime-Rueckfuehrung.",
        "- Keine Handlung.",
        "- Kein Gate.",
        "- Kein Entry.",
        "",
        "## Befund",
        f"- node_reproduction_rate: {lookup.get('node_reproduction_rate')}",
        f"- edge_reproduction_rate: {lookup.get('edge_reproduction_rate')}",
        f"- reference_edges: {lookup.get('edge_count_reference')}",
        f"- candidate_edges: {lookup.get('edge_count_candidate')}",
        f"- reference_islands: {lookup.get('island_count_reference')}",
        f"- candidate_islands: {lookup.get('island_count_candidate')}",
    ]
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare passive Mini-DIO semantic matrices")
    parser.add_argument("--reference", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    reference = _load_matrix(args.reference)
    candidate = _load_matrix(args.candidate)
    summary, details = compare(reference, candidate)
    write_outputs(summary, details, args.output_dir)
    print(json.dumps({"summary": summary, "details": len(details), "output_dir": str(args.output_dir), **BOUNDARY}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
