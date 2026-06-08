"""Report stability of passive sign-cluster candidates.

This diagnostic compares passive_sign_cluster_candidates.csv snapshots. It is
passive only and never feeds Mini-DIO runtime or action logic.
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
from pathlib import Path


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
    name = name.replace("dio_mini_passive_sign_cluster_candidates_", "")
    name = name.replace("dio_0x52_", "")
    return name or path.stem


def _recent_same(values: list[str], count: int = 2) -> bool:
    if len(values) < count:
        return False
    return len(set(values[-count:])) == 1


def _cluster_stability_state(states: list[str], symbols: list[str], source_count: int, available: int) -> str:
    if source_count <= 0:
        return "not_seen"
    if source_count == 1:
        return "single_passive_cluster_trace"
    candidate_states = [state for state in states if state.startswith("passive_cluster_candidate")]
    if len(candidate_states) == source_count and len(set(states)) == 1 and len(set(symbols)) == 1 and source_count == available:
        return "stable_passive_cluster_candidate"
    if len(candidate_states) >= 2 and states[-1].startswith("passive_cluster_candidate") and _recent_same(states):
        return "recently_stable_passive_cluster_candidate"
    if len(candidate_states) >= 2 and states[-1].startswith("passive_cluster_candidate"):
        return "drifting_passive_cluster_candidate"
    if len(candidate_states) >= 1:
        return "unstable_passive_cluster_trace"
    return "not_cluster_across_sources"


def build_cluster_stability(cluster_paths: list[Path]) -> tuple[list[dict], list[dict]]:
    available_sources = len(cluster_paths)
    grouped: dict[tuple[str, str], dict] = {}

    for path in cluster_paths:
        source = _source_label(path)
        for row in _read_csv(path):
            target = str(row.get("target_family", "") or "")
            related = str(row.get("related_family", "") or "")
            if not target or not related:
                continue
            key = (target, related)
            item = grouped.setdefault(
                key,
                {
                    "target_family": target,
                    "related_family": related,
                    "sources": [],
                    "cluster_symbols": [],
                    "cluster_states": [],
                    "relation_states": [],
                    "field_overlaps": [],
                    "relation_scores": [],
                    "shared_fields": [],
                    "sentences": [],
                },
            )
            item["sources"].append(source)
            item["cluster_symbols"].append(str(row.get("passive_cluster_symbol", "") or ""))
            item["cluster_states"].append(str(row.get("cluster_candidate_state", "") or ""))
            item["relation_states"].append(str(row.get("relation_stability_state", "") or ""))
            item["field_overlaps"].append(_safe_float(row.get("avg_field_overlap")))
            item["relation_scores"].append(_safe_float(row.get("avg_relation_score")))
            item["shared_fields"].append(str(row.get("shared_field_trace", "") or ""))
            item["sentences"].append(str(row.get("dio_sentence", "") or ""))

    rows: list[dict] = []
    groups: dict[str, dict] = {}
    for item in grouped.values():
        source_count = len(set(item["sources"]))
        state = _cluster_stability_state(
            item["cluster_states"],
            item["cluster_symbols"],
            source_count,
            available_sources,
        )
        latest_index = len(item["sources"]) - 1
        row = {
            "target_family": item["target_family"],
            "related_family": item["related_family"],
            "cluster_stability_state": state,
            "cluster_source_count": source_count,
            "available_cluster_sources": available_sources,
            "sources": "|".join(item["sources"]),
            "latest_cluster_symbol": item["cluster_symbols"][latest_index] if latest_index >= 0 else "",
            "cluster_symbol_history": "|".join(item["cluster_symbols"]),
            "latest_cluster_candidate_state": item["cluster_states"][latest_index] if latest_index >= 0 else "",
            "cluster_candidate_state_history": "|".join(item["cluster_states"]),
            "relation_state_history": "|".join(item["relation_states"]),
            "avg_field_overlap": round(sum(item["field_overlaps"]) / max(1, len(item["field_overlaps"])), 6),
            "latest_field_overlap": round(item["field_overlaps"][latest_index] if latest_index >= 0 else 0.0, 6),
            "avg_relation_score": round(sum(item["relation_scores"]) / max(1, len(item["relation_scores"])), 6),
            "latest_relation_score": round(item["relation_scores"][latest_index] if latest_index >= 0 else 0.0, 6),
            "shared_field_history": " || ".join(item["shared_fields"]),
            "latest_sentence": item["sentences"][latest_index] if latest_index >= 0 else "",
            "passive_only": True,
            "writes_runtime_memory": False,
            "read_by_mini_dio": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
            "is_entry_signal": False,
            "is_direction_signal": False,
        }
        rows.append(row)
        group = groups.setdefault(
            state,
            {
                "cluster_stability_state": state,
                "cluster_count": 0,
                "families": [],
            },
        )
        group["cluster_count"] += 1
        group["families"].append(f"{item['target_family']}+{item['related_family']}")

    rows.sort(
        key=lambda row: (
            row["cluster_stability_state"] != "stable_passive_cluster_candidate",
            row["cluster_stability_state"] != "recently_stable_passive_cluster_candidate",
            row["cluster_stability_state"] != "drifting_passive_cluster_candidate",
            -int(row["cluster_source_count"]),
            -float(row["latest_field_overlap"]),
            -float(row["latest_relation_score"]),
            str(row["target_family"]),
            str(row["related_family"]),
        )
    )
    summary = [
        {
            "cluster_stability_state": group["cluster_stability_state"],
            "cluster_count": int(group["cluster_count"]),
            "families": "|".join(sorted(group["families"])),
            "passive_only": True,
            "influences_action": False,
        }
        for group in groups.values()
    ]
    summary.sort(key=lambda row: (-int(row["cluster_count"]), str(row["cluster_stability_state"])))
    return rows, summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(rows: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "passive_sign_cluster_stability.csv"
    summary_path = output_dir / "passive_sign_cluster_stability_summary.csv"
    json_path = output_dir / "passive_sign_cluster_stability.json"
    md_path = output_dir / "passive_sign_cluster_stability.md"
    _write_csv(detail_path, rows, ["target_family", "related_family", "cluster_stability_state"])
    _write_csv(summary_path, summary, ["cluster_stability_state", "cluster_count"])
    json_path.write_text(
        json.dumps(
            {
                "boundary": {
                    "passive_only": True,
                    "writes_runtime_memory": False,
                    "read_by_mini_dio": False,
                    "influences_action": False,
                    "is_gate": False,
                    "is_motoric": False,
                    "is_entry_signal": False,
                    "is_direction_signal": False,
                },
                "clusters": rows,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Passive Sign Cluster Stability",
        "",
        "## Grenze",
        "- passiv",
        "- keine Runtime-Lesung",
        "- keine Handlung",
        "- keine Richtung",
        "- kein Entry",
        "",
        "## Zusammenfassung",
    ]
    for row in summary:
        lines.append(
            f"- {row['cluster_stability_state']}: {row['cluster_count']} "
            f"({row.get('families', '')})"
        )
    lines.extend(["", "## Details"])
    for row in rows[:20]:
        lines.append(
            f"- {row['target_family']} + {row['related_family']}: "
            f"{row['cluster_stability_state']} latest={row['latest_cluster_symbol']} "
            f"state={row['latest_cluster_candidate_state']} field={row['latest_field_overlap']}"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cluster-candidates", nargs="+", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    paths = _expand_patterns(args.cluster_candidates)
    rows, summary = build_cluster_stability(paths)
    write_outputs(rows, summary, Path(args.output_dir))
    print(f"cluster_sources={len(paths)} clusters={len(rows)} summary_rows={len(summary)}")
    for row in rows[:8]:
        print(
            f"{row['target_family']}+{row['related_family']} "
            f"{row['cluster_stability_state']} {row['latest_cluster_symbol']}"
        )


if __name__ == "__main__":
    main()
