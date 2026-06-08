"""Report passive semantic density in Mini-DIO semantic matrices.

This reads the passive semantic matrix outputs and estimates which islands
behave like semantic density centers: many nodes, many edges, high similarity,
and raw variants around core traces.

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


def _split_families(value: object) -> list[str]:
    text = str(value or "").strip()
    if not text or text == "-":
        return []
    return [part for part in text.split("|") if part and part != "-"]


def _clip(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, float(value)))


def _compare_lookup(path: Path | None) -> dict[str, float]:
    if path is None:
        return {}
    rows = _read_csv(path)
    return {str(row.get("metric", "") or ""): _safe_float(row.get("value")) for row in rows}


def _density_state(density: float, attraction: float, fragmentation: float) -> str:
    if density >= 0.72 and attraction >= 0.52 and fragmentation <= 0.34:
        return "passive_semantic_density_center"
    if density >= 0.52 and attraction >= 0.28:
        return "passive_growing_semantic_island"
    if fragmentation >= 0.62:
        return "passive_fragmented_semantic_field"
    if density >= 0.28:
        return "passive_raw_semantic_density"
    return "passive_low_density_trace"


def _sentence(row: dict) -> str:
    island_id = str(row.get("island_id", "") or "")
    state = str(row.get("density_state", "") or "")
    if state == "passive_semantic_density_center":
        return f"{island_id}: semantisches Dichtezentrum; Varianten koppeln an einen stabilen Inselraum."
    if state == "passive_growing_semantic_island":
        return f"{island_id}: wachsende Bedeutungsinsel mit sichtbarer Variantenanziehung."
    if state == "passive_fragmented_semantic_field":
        return f"{island_id}: fragmentiertes semantisches Feld; Naehe noch nicht gebunden."
    if state == "passive_raw_semantic_density":
        return f"{island_id}: rohe semantische Dichte ohne stabile Kernwirkung."
    return f"{island_id}: geringe passive Dichte."


def build_density(matrix_dir: Path, compare_summary: Path | None = None) -> tuple[list[dict], list[dict]]:
    islands = _read_csv(matrix_dir / "passive_semantic_matrix_islands.csv")
    nodes = _read_csv(matrix_dir / "passive_semantic_matrix_nodes.csv")
    edges = _read_csv(matrix_dir / "passive_semantic_matrix_edges.csv")
    compare = _compare_lookup(compare_summary)

    node_count = max(1, len(nodes))
    edge_count = max(1, len(edges))
    max_family_count = max([_safe_int(row.get("family_count")) for row in islands] or [1])
    max_edge_count = max([_safe_int(row.get("edge_count")) for row in islands] or [1])
    node_reproduction = compare.get("node_reproduction_rate", 0.0)
    edge_reproduction = compare.get("edge_reproduction_rate", 0.0)
    density_reproduction = _clip((node_reproduction * 0.45) + (edge_reproduction * 0.55))

    rows: list[dict] = []
    for island in islands:
        families = _split_families(island.get("families"))
        core_families = _split_families(island.get("core_families"))
        raw_families = _split_families(island.get("raw_families"))
        family_count = _safe_int(island.get("family_count"), len(families))
        local_edge_count = _safe_int(island.get("edge_count"))
        avg_similarity = _safe_float(island.get("avg_meaning_similarity"))
        max_similarity = _safe_float(island.get("max_meaning_similarity"))
        core_count = len(core_families)
        raw_count = len(raw_families)
        possible_edges = max(1, family_count * (family_count - 1) // 2)
        local_edge_density = _clip(local_edge_count / possible_edges)
        relative_family_mass = _clip(family_count / max(1, max_family_count))
        relative_edge_mass = _clip(local_edge_count / max(1, max_edge_count))
        core_ratio = _clip(core_count / max(1, family_count))
        raw_ratio = _clip(raw_count / max(1, family_count))
        variant_attraction = _clip((raw_ratio * 0.48) + (local_edge_density * 0.32) + (avg_similarity * 0.20))
        island_growth = _clip((relative_family_mass * 0.38) + (relative_edge_mass * 0.34) + (raw_ratio * 0.18) + (max_similarity * 0.10))
        island_fragmentation = _clip((1.0 - local_edge_density) * (1.0 - core_ratio) * (1.0 - min(avg_similarity, 1.0)))
        semantic_density = _clip(
            (relative_family_mass * 0.24)
            + (relative_edge_mass * 0.24)
            + (local_edge_density * 0.20)
            + (avg_similarity * 0.18)
            + (core_ratio * 0.08)
            + (density_reproduction * 0.06)
        )
        semantic_vorticity = _clip((variant_attraction * 0.42) + (island_growth * 0.32) + (island_fragmentation * 0.26))
        row = {
            "island_id": str(island.get("island_id", "") or ""),
            "island_state": str(island.get("island_state", "") or ""),
            "family_count": family_count,
            "core_count": core_count,
            "raw_count": raw_count,
            "edge_count": local_edge_count,
            "possible_edge_count": possible_edges,
            "local_edge_density": round(local_edge_density, 6),
            "avg_meaning_similarity": round(avg_similarity, 6),
            "max_meaning_similarity": round(max_similarity, 6),
            "semantic_density": round(semantic_density, 6),
            "variant_attraction": round(variant_attraction, 6),
            "island_growth": round(island_growth, 6),
            "island_fragmentation": round(island_fragmentation, 6),
            "density_reproduction": round(density_reproduction, 6),
            "semantic_vorticity": round(semantic_vorticity, 6),
            "families": "|".join(families),
            "core_families": "|".join(core_families) if core_families else "-",
            "raw_families": "|".join(raw_families) if raw_families else "-",
            **BOUNDARY,
        }
        row["density_state"] = _density_state(
            float(row["semantic_density"]),
            float(row["variant_attraction"]),
            float(row["island_fragmentation"]),
        )
        row["dio_semantic_density_sentence"] = _sentence(row)
        rows.append(row)

    rows.sort(
        key=lambda row: (
            -_safe_float(row.get("semantic_density")),
            -_safe_float(row.get("variant_attraction")),
            str(row.get("island_id", "")),
        )
    )

    summary = [
        {
            "metric": "matrix_node_count",
            "value": node_count,
            **BOUNDARY,
        },
        {
            "metric": "matrix_edge_count",
            "value": edge_count,
            **BOUNDARY,
        },
        {
            "metric": "matrix_island_count",
            "value": len(islands),
            **BOUNDARY,
        },
        {
            "metric": "density_reproduction",
            "value": round(density_reproduction, 6),
            **BOUNDARY,
        },
        {
            "metric": "max_semantic_density",
            "value": round(max([_safe_float(row.get("semantic_density")) for row in rows] or [0.0]), 6),
            **BOUNDARY,
        },
        {
            "metric": "max_variant_attraction",
            "value": round(max([_safe_float(row.get("variant_attraction")) for row in rows] or [0.0]), 6),
            **BOUNDARY,
        },
        {
            "metric": "max_semantic_vorticity",
            "value": round(max([_safe_float(row.get("semantic_vorticity")) for row in rows] or [0.0]), 6),
            **BOUNDARY,
        },
    ]
    return rows, summary


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


def write_outputs(rows: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "passive_semantic_density.csv", rows, ["island_id", "semantic_density"])
    _write_csv(output_dir / "passive_semantic_density_summary.csv", summary, ["metric", "value"])
    (output_dir / "passive_semantic_density.json").write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_semantic_density.v1",
                "boundary": BOUNDARY,
                "summary": summary,
                "islands": rows,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Mini-DIO passive semantische Dichte",
        "",
        "Ziel: Dichtezentren, Variantenanziehung und Inselwachstum passiv sichtbar machen.",
        "",
        "## Grenze",
        "- Nur Bericht.",
        "- Keine Runtime-Rueckfuehrung.",
        "- Keine Handlung.",
        "- Kein Gate.",
        "- Kein Entry.",
        "- Keine Richtung.",
        "",
        "## Summary",
    ]
    for row in summary:
        lines.append(f"- {row['metric']}: {row['value']}")
    lines.extend(["", "## Dichteste Inseln"])
    for row in rows[:20]:
        lines.append(
            f"- {row['dio_semantic_density_sentence']} "
            f"density={row['semantic_density']} attraction={row['variant_attraction']} "
            f"vorticity={row['semantic_vorticity']}"
        )
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive Mini-DIO semantic density")
    parser.add_argument("--matrix-dir", required=True, type=Path)
    parser.add_argument("--compare-summary", type=Path, default=None)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    rows, summary = build_density(args.matrix_dir, args.compare_summary)
    write_outputs(rows, summary, args.output_dir)
    print(
        json.dumps(
            {
                "islands": len(rows),
                "summary": len(summary),
                "output_dir": str(args.output_dir),
                **BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
