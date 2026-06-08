"""Report stability of passive fragment islands across island snapshots.

This diagnostic compares passive_fragment_islands.csv outputs. It is passive
only: no runtime memory, no action influence, no entry signal, no direction.
"""

from __future__ import annotations

import argparse
import csv
import glob
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


def _expand_patterns(patterns: list[str]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        matches = glob.glob(pattern)
        if matches:
            paths.extend(Path(match) for match in matches)
        else:
            paths.append(Path(pattern))
    unique = {str(path.resolve()): path for path in paths}
    return [unique[key] for key in sorted(unique)]


def _source_label(path: Path) -> str:
    name = path.parent.name or path.stem
    name = name.replace("dio_mini_passive_fragment_islands_", "")
    return name or path.stem


def _recent_same(values: list[str], count: int = 2) -> bool:
    if len(values) < count:
        return False
    return len(set(values[-count:])) == 1


def _stability_state(states: list[str], symbols: list[str], fragments: list[str], source_count: int, available: int) -> str:
    if source_count <= 0:
        return "not_seen"
    if source_count == 1:
        return "single_passive_fragment_island_trace"
    if (
        source_count == available
        and len(set(states)) == 1
        and len(set(symbols)) == 1
        and len(set(fragments)) == 1
    ):
        return "stable_passive_fragment_island"
    if source_count >= 2 and _recent_same(states) and _recent_same(fragments):
        return "recently_stable_passive_fragment_island"
    if source_count >= 2:
        return "drifting_passive_fragment_island"
    return "unstable_passive_fragment_trace"


def build_fragment_island_stability(island_paths: list[Path]) -> tuple[list[dict], list[dict]]:
    available_sources = len(island_paths)
    grouped: dict[tuple[str, str, str], dict] = {}

    for path in island_paths:
        source = _source_label(path)
        for row in _read_csv(path):
            target = str(row.get("target_family", "") or "")
            related = str(row.get("related_family", "") or "")
            group = str(row.get("fragment_group", "") or "")
            if not target or not group:
                continue
            key = (target, related, group)
            item = grouped.setdefault(
                key,
                {
                    "target_family": target,
                    "related_family": related,
                    "fragment_group": group,
                    "sources": [],
                    "island_symbols": [],
                    "island_states": [],
                    "fragments": [],
                    "fragment_counts": [],
                    "field_overlaps": [],
                    "relation_scores": [],
                    "sentences": [],
                },
            )
            item["sources"].append(source)
            item["island_symbols"].append(str(row.get("passive_fragment_island_symbol", "") or ""))
            item["island_states"].append(str(row.get("fragment_island_state", "") or ""))
            item["fragments"].append(str(row.get("fragments", "") or ""))
            item["fragment_counts"].append(int(_safe_float(row.get("fragment_count"))))
            item["field_overlaps"].append(_safe_float(row.get("latest_field_overlap")))
            item["relation_scores"].append(_safe_float(row.get("latest_relation_score")))
            item["sentences"].append(str(row.get("dio_sentence", "") or ""))

    rows: list[dict] = []
    groups: dict[str, dict] = {}
    for item in grouped.values():
        source_count = len(set(item["sources"]))
        latest_index = len(item["sources"]) - 1
        state = _stability_state(
            item["island_states"],
            item["island_symbols"],
            item["fragments"],
            source_count,
            available_sources,
        )
        row = {
            "target_family": item["target_family"],
            "related_family": item["related_family"],
            "fragment_group": item["fragment_group"],
            "fragment_island_stability_state": state,
            "island_source_count": source_count,
            "available_island_sources": available_sources,
            "sources": "|".join(item["sources"]),
            "latest_fragment_island_symbol": item["island_symbols"][latest_index] if latest_index >= 0 else "",
            "fragment_island_symbol_history": "|".join(item["island_symbols"]),
            "latest_fragment_island_state": item["island_states"][latest_index] if latest_index >= 0 else "",
            "fragment_island_state_history": "|".join(item["island_states"]),
            "latest_fragments": item["fragments"][latest_index] if latest_index >= 0 else "",
            "fragment_history": " || ".join(item["fragments"]),
            "latest_fragment_count": item["fragment_counts"][latest_index] if latest_index >= 0 else 0,
            "avg_fragment_count": round(sum(item["fragment_counts"]) / max(1, len(item["fragment_counts"])), 6),
            "latest_field_overlap": round(item["field_overlaps"][latest_index] if latest_index >= 0 else 0.0, 6),
            "avg_field_overlap": round(sum(item["field_overlaps"]) / max(1, len(item["field_overlaps"])), 6),
            "latest_relation_score": round(item["relation_scores"][latest_index] if latest_index >= 0 else 0.0, 6),
            "avg_relation_score": round(sum(item["relation_scores"]) / max(1, len(item["relation_scores"])), 6),
            "latest_sentence": item["sentences"][latest_index] if latest_index >= 0 else "",
            **BOUNDARY,
        }
        rows.append(row)
        summary_group = groups.setdefault(
            state,
            {
                "fragment_island_stability_state": state,
                "island_count": 0,
                "fragment_groups": [],
                "symbols": [],
            },
        )
        summary_group["island_count"] += 1
        summary_group["fragment_groups"].append(f"{item['target_family']}+{item['related_family']}:{item['fragment_group']}")
        if row["latest_fragment_island_symbol"]:
            summary_group["symbols"].append(row["latest_fragment_island_symbol"])

    rows.sort(
        key=lambda row: (
            row["fragment_island_stability_state"] != "stable_passive_fragment_island",
            row["fragment_island_stability_state"] != "recently_stable_passive_fragment_island",
            row["fragment_island_stability_state"] != "drifting_passive_fragment_island",
            -int(row["island_source_count"]),
            -int(row["latest_fragment_count"]),
            str(row["target_family"]),
            str(row["related_family"]),
            str(row["fragment_group"]),
        )
    )
    summary = [
        {
            "fragment_island_stability_state": group["fragment_island_stability_state"],
            "island_count": int(group["island_count"]),
            "fragment_groups": "|".join(sorted(group["fragment_groups"])),
            "latest_symbols": "|".join(sorted(set(group["symbols"]))),
            **BOUNDARY,
        }
        for group in groups.values()
    ]
    summary.sort(key=lambda row: (-int(row["island_count"]), str(row["fragment_island_stability_state"])))
    return rows, summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(rows: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "passive_fragment_island_stability.csv"
    summary_path = output_dir / "passive_fragment_island_stability_summary.csv"
    json_path = output_dir / "passive_fragment_island_stability.json"
    md_path = output_dir / "passive_fragment_island_stability.md"

    _write_csv(detail_path, rows, ["target_family", "related_family", "fragment_group"])
    _write_csv(summary_path, summary, ["fragment_island_stability_state", "island_count"])
    json_path.write_text(
        json.dumps(
            {
                "boundary": BOUNDARY,
                "islands": rows,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# Passive Fragment Island Stability",
        "",
        "## Grenze",
        "- passiv",
        "- keine Runtime-Lesung",
        "- keine Handlung",
        "- keine Richtung",
        "- kein Entry",
        "",
        "## Summary",
    ]
    for row in summary:
        lines.append(
            f"- {row['fragment_island_stability_state']}: {row['island_count']} "
            f"({row.get('fragment_groups', '')})"
        )
    lines.extend(["", "## Details"])
    for row in rows[:20]:
        lines.append(
            f"- {row['target_family']} + {row['related_family']} {row['fragment_group']}: "
            f"{row['fragment_island_stability_state']} latest={row['latest_fragment_island_symbol']} "
            f"fragments={row['latest_fragments']}"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fragment-islands", nargs="+", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    paths = _expand_patterns(args.fragment_islands)
    rows, summary = build_fragment_island_stability(paths)
    write_outputs(rows, summary, Path(args.output_dir))
    print(f"island_sources={len(paths)} islands={len(rows)} summary_rows={len(summary)}")
    for row in summary:
        print(f"{row['fragment_island_stability_state']}={row['island_count']}")


if __name__ == "__main__":
    main()
