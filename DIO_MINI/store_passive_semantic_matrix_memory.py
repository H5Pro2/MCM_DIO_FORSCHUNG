"""Store passive Mini-DIO semantic matrix development memory.

This file is diagnostic memory. It preserves how Mini-DIO's own syntax
families form, expand, drift, densify, and reorganize into text islands.
Mini-DIO must not read this memory for action, gates, entries, or direction.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import time
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


def _write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = list(fields)
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=ordered)
        writer.writeheader()
        writer.writerows(rows)


def _atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f"{path.name}.tmp.{os.getpid()}.{int(time.time() * 1000)}")
    temp_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temp_path, path)


def _load_memory(path: Path) -> dict:
    if not path.exists():
        return _empty_memory()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return _empty_memory()
    if not isinstance(payload, dict):
        return _empty_memory()
    memory = _empty_memory()
    memory.update(payload)
    memory["nodes"] = dict(memory.get("nodes", {}) or {})
    memory["edges"] = dict(memory.get("edges", {}) or {})
    memory["text_islands"] = dict(memory.get("text_islands", {}) or {})
    memory["sources"] = list(memory.get("sources", []) or [])
    memory["summary"] = dict(memory.get("summary", {}) or {})
    return memory


def _empty_memory() -> dict:
    return {
        "schema": "dio_mini_passive_semantic_matrix_memory.v1",
        "version": 1,
        "created_at": int(time.time()),
        "updated_at": int(time.time()),
        "boundary": dict(PASSIVE_BOUNDARY),
        "sources": [],
        "nodes": {},
        "edges": {},
        "text_islands": {},
        "summary": {},
    }


def _hash_base36(text: str) -> str:
    value = 2166136261
    for char in text:
        value ^= ord(char)
        value = (value * 16777619) & 0xFFFFFFFF
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    if value == 0:
        return "0"
    chars: list[str] = []
    while value:
        value, rest = divmod(value, 36)
        chars.append(alphabet[rest])
    return "".join(reversed(chars))


def _split_families(value: object) -> list[str]:
    if isinstance(value, (list, tuple, set)):
        return sorted({str(item).strip() for item in value if str(item).strip() and str(item).strip() != "-"})
    text = str(value or "").strip()
    if not text or text == "-":
        return []
    return sorted({item.strip() for item in text.split("|") if item.strip() and item.strip() != "-"})


def _edge_key(left: str, right: str) -> str:
    pair = sorted([str(left or ""), str(right or "")])
    return f"{pair[0]}|{pair[1]}"


def _text_island_symbol(families: list[str]) -> str:
    basis = "|".join(sorted(families))
    return f"dio_text_{_hash_base36(basis)[:10]}"


def _jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 1.0
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def _density_by_island(density_dir: Path | None) -> dict[str, dict]:
    if not density_dir:
        return {}
    rows = _read_csv(density_dir / "passive_semantic_density.csv")
    return {str(row.get("island_id", "") or ""): row for row in rows if row.get("island_id")}


def _memory_note(item: dict) -> str:
    return (
        f"{item['text_island_symbol']}: {item['development_state']}; "
        f"families={item['family_count']}; "
        f"density={item['semantic_density']:.6f}; "
        f"added={item['added_family_count']}; removed={item['removed_family_count']}; "
        "passiv, keine Handlung."
    )


def _match_text_island(memory: dict, families: list[str], min_overlap: float) -> tuple[str, float, dict | None]:
    incoming = set(families)
    best_symbol = ""
    best_score = 0.0
    best_item: dict | None = None
    for symbol, item in dict(memory.get("text_islands", {}) or {}).items():
        existing = set(_split_families(item.get("families", [])))
        score = _jaccard(incoming, existing)
        if score > best_score:
            best_symbol = str(symbol)
            best_score = score
            best_item = dict(item or {})
    if best_item is not None and best_score >= min_overlap:
        return best_symbol, best_score, best_item
    return _text_island_symbol(families), 0.0, None


def _development_state(previous: dict | None, added: set[str], removed: set[str], density_delta: float) -> str:
    if previous is None:
        return "emerging_text_island"
    if added and removed:
        return "reorganizing_text_island"
    if removed:
        return "drifting_text_island"
    if added:
        return "expanding_text_island"
    if density_delta > 0.0:
        return "densifying_text_island"
    return "recurring_text_island"


def _affordance(state: str) -> str:
    if state == "emerging_text_island":
        return "can_store_new_semantic_island"
    if state == "expanding_text_island":
        return "can_extend_existing_semantic_island"
    if state == "densifying_text_island":
        return "can_compact_semantic_density"
    if state == "drifting_text_island":
        return "can_observe_semantic_drift"
    if state == "reorganizing_text_island":
        return "can_relink_semantic_fragments"
    return "can_hold_recurrent_semantic_island"


def _update_average(old_value: object, old_count: int, new_value: float) -> float:
    old = _safe_float(old_value)
    count = max(0, int(old_count))
    return ((old * count) + new_value) / max(1, count + 1)


def update_memory(
    memory: dict,
    matrix_dir: Path,
    density_dir: Path | None,
    source_label: str,
    min_overlap: float,
    max_history: int,
) -> tuple[dict, list[dict]]:
    nodes = _read_csv(matrix_dir / "passive_semantic_matrix_nodes.csv")
    edges = _read_csv(matrix_dir / "passive_semantic_matrix_edges.csv")
    islands = _read_csv(matrix_dir / "passive_semantic_matrix_islands.csv")
    density = _density_by_island(density_dir)

    now = int(time.time())
    memory["updated_at"] = now
    source_record = {
        "source_label": source_label,
        "matrix_dir": str(matrix_dir),
        "density_dir": str(density_dir) if density_dir else "",
        "timestamp": now,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "island_count": len(islands),
        **PASSIVE_BOUNDARY,
    }
    memory.setdefault("sources", []).append(source_record)

    for row in nodes:
        family = str(row.get("symbol_family", "") or "").strip()
        if not family:
            continue
        record = dict(memory.setdefault("nodes", {}).get(family, {}) or {})
        observations = _safe_int(record.get("observations"))
        record.update(
            {
                "symbol_family": family,
                "observations": observations + 1,
                "first_seen_source": record.get("first_seen_source") or source_label,
                "last_seen_source": source_label,
                "last_matrix_node_state": row.get("matrix_node_state", ""),
                "last_dominant_neuro_tone": row.get("dominant_neuro_tone", ""),
                "last_temporal_state": row.get("dominant_temporal_state", ""),
                "episode_count_sum": _safe_int(record.get("episode_count_sum")) + _safe_int(row.get("episode_count")),
                **PASSIVE_BOUNDARY,
            }
        )
        for key in [
            "avg_sehen_form_flow",
            "avg_hoeren_energy_tone",
            "avg_fuehlen_mcm_coherence",
            "avg_observation_learning_pressure",
        ]:
            record[key] = round(_update_average(record.get(key), observations, _safe_float(row.get(key))), 9)
        memory["nodes"][family] = record

    for row in edges:
        left = str(row.get("left_family", "") or "").strip()
        right = str(row.get("right_family", "") or "").strip()
        if not left or not right:
            continue
        key = _edge_key(left, right)
        record = dict(memory.setdefault("edges", {}).get(key, {}) or {})
        observations = _safe_int(record.get("observations"))
        record.update(
            {
                "edge_key": key,
                "left_family": min(left, right),
                "right_family": max(left, right),
                "observations": observations + 1,
                "first_seen_source": record.get("first_seen_source") or source_label,
                "last_seen_source": source_label,
                "last_neighbor_state": row.get("neighbor_state", ""),
                "last_matrix_edge_state": row.get("matrix_edge_state", ""),
                **PASSIVE_BOUNDARY,
            }
        )
        for key_name in [
            "meaning_similarity",
            "sense_similarity",
            "mcm_similarity",
            "hearing_similarity",
            "temporal_similarity",
            "neuro_similarity",
        ]:
            record[f"avg_{key_name}"] = round(
                _update_average(record.get(f"avg_{key_name}"), observations, _safe_float(row.get(key_name))),
                9,
            )
        memory["edges"][key] = record

    island_updates: list[dict] = []
    for row in islands:
        families = _split_families(row.get("families"))
        if not families:
            continue
        source_island_id = str(row.get("island_id", "") or "")
        density_row = density.get(source_island_id, {})
        symbol, overlap, previous = _match_text_island(memory, families, min_overlap)
        previous_families = set(_split_families((previous or {}).get("families", [])))
        current_families = set(families)
        added = current_families - previous_families
        removed = previous_families - current_families
        observations = _safe_int((previous or {}).get("observations"))
        semantic_density = _safe_float(density_row.get("semantic_density"), _safe_float(row.get("avg_meaning_similarity")))
        density_delta = semantic_density - _safe_float((previous or {}).get("last_semantic_density"))
        state = _development_state(previous, added, removed, density_delta)
        history = list((previous or {}).get("history", []) or [])
        history.append(
            {
                "source_label": source_label,
                "source_island_id": source_island_id,
                "family_count": len(families),
                "semantic_density": round(semantic_density, 9),
                "variant_attraction": round(_safe_float(density_row.get("variant_attraction")), 9),
                "semantic_vorticity": round(_safe_float(density_row.get("semantic_vorticity")), 9),
                "development_state": state,
                "added_families": sorted(added),
                "removed_families": sorted(removed),
            }
        )
        history = history[-max(1, max_history) :]
        item = {
            "text_island_symbol": symbol,
            "source_island_id": source_island_id,
            "observations": observations + 1,
            "first_seen_source": (previous or {}).get("first_seen_source") or source_label,
            "last_seen_source": source_label,
            "families": sorted(current_families),
            "family_count": len(current_families),
            "added_family_count": len(added),
            "removed_family_count": len(removed),
            "match_overlap": round(overlap, 9),
            "development_state": state,
            "development_affordance": _affordance(state),
            "semantic_density": round(semantic_density, 9),
            "density_delta": round(density_delta, 9),
            "variant_attraction": round(_safe_float(density_row.get("variant_attraction")), 9),
            "semantic_vorticity": round(_safe_float(density_row.get("semantic_vorticity")), 9),
            "island_state": row.get("island_state", ""),
            "history": history,
            **PASSIVE_BOUNDARY,
        }
        item["memory_note"] = _memory_note(item)
        memory.setdefault("text_islands", {})[symbol] = item
        island_updates.append(item)

    memory["summary"] = {
        "source_count": len(memory.get("sources", []) or []),
        "node_count": len(memory.get("nodes", {}) or {}),
        "edge_count": len(memory.get("edges", {}) or {}),
        "text_island_count": len(memory.get("text_islands", {}) or {}),
        "last_source_label": source_label,
        **PASSIVE_BOUNDARY,
    }
    return memory, island_updates


def write_outputs(memory: dict, memory_path: Path, output_dir: Path | None, island_updates: list[dict]) -> None:
    _atomic_write_json(memory_path, memory)
    if not output_dir:
        return
    output_dir.mkdir(parents=True, exist_ok=True)
    text_islands = list(dict(memory.get("text_islands", {}) or {}).values())
    nodes = list(dict(memory.get("nodes", {}) or {}).values())
    edges = list(dict(memory.get("edges", {}) or {}).values())

    _write_csv(
        output_dir / "dio_mini_semantic_matrix_memory_text_islands.csv",
        text_islands,
        [
            "text_island_symbol",
            "development_state",
            "development_affordance",
            "observations",
            "family_count",
            "added_family_count",
            "removed_family_count",
            "semantic_density",
            "density_delta",
            "variant_attraction",
            "semantic_vorticity",
            "families",
        ],
    )
    _write_csv(
        output_dir / "dio_mini_semantic_matrix_memory_nodes.csv",
        nodes,
        ["symbol_family", "observations", "episode_count_sum", "last_matrix_node_state"],
    )
    _write_csv(
        output_dir / "dio_mini_semantic_matrix_memory_edges.csv",
        edges,
        ["edge_key", "left_family", "right_family", "observations", "avg_meaning_similarity"],
    )
    _write_csv(
        output_dir / "dio_mini_semantic_matrix_memory_last_update.csv",
        island_updates,
        [
            "text_island_symbol",
            "development_state",
            "development_affordance",
            "family_count",
            "added_family_count",
            "removed_family_count",
            "semantic_density",
            "memory_note",
        ],
    )

    lines = [
        "# DIO Mini Semantic Matrix Memory",
        "",
        f"- memory: `{memory_path}`",
        f"- text_islands: `{len(text_islands)}`",
        f"- nodes: `{len(nodes)}`",
        f"- edges: `{len(edges)}`",
        "",
        "## Grenze",
        "",
        "- passiv",
        "- keine Runtime-Lesung",
        "- keine Handlung",
        "- kein Gate",
        "- kein Entry",
        "- keine Richtung",
        "",
        "## Letzte Entwicklung",
        "",
    ]
    for item in island_updates[:40]:
        lines.append(f"- {item['memory_note']}")
    text = "\n".join(lines) + "\n"
    (output_dir / "dio_mini_semantic_matrix_memory.md").write_text(text, encoding="utf-8")
    (output_dir / "dio_mini_semantic_matrix_memory.txt").write_text(
        "\n".join(item["memory_note"] for item in island_updates) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Store passive Mini-DIO semantic matrix memory")
    parser.add_argument("--matrix-dir", type=Path, required=True)
    parser.add_argument("--density-dir", type=Path, default=None)
    parser.add_argument("--memory", type=Path, default=Path("bot_memory/dio_mini_semantic_matrix_memory.json"))
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--source-label", default="")
    parser.add_argument("--min-overlap", type=float, default=0.18)
    parser.add_argument("--max-history", type=int, default=24)
    args = parser.parse_args()

    source_label = str(args.source_label or args.matrix_dir.name)
    memory = _load_memory(args.memory)
    memory, island_updates = update_memory(
        memory,
        args.matrix_dir,
        args.density_dir,
        source_label,
        max(0.0, min(1.0, args.min_overlap)),
        max(1, args.max_history),
    )
    write_outputs(memory, args.memory, args.output_dir, island_updates)
    print(
        json.dumps(
            {
                "memory": str(args.memory),
                "text_islands": len(memory.get("text_islands", {}) or {}),
                "nodes": len(memory.get("nodes", {}) or {}),
                "edges": len(memory.get("edges", {}) or {}),
                "updated_islands": len(island_updates),
                **PASSIVE_BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
