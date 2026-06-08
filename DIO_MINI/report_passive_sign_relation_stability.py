"""Report stability of passive sign relations across relation diagnostics.

This diagnostic reads one or more passive_sign_relations.csv files and checks
whether related signs recur as neighbors across outputs. It is not runtime
memory and does not influence Mini-DIO action.
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
        return float(value or default)
    except Exception:
        return default


def _source_label(path: Path) -> str:
    name = path.parent.name or path.stem
    name = name.replace("dio_mini_passive_sign_relations_", "")
    return name or path.stem


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


def _stability_state(source_count: int, avg_score: float, max_score: float) -> str:
    if source_count <= 0:
        return "not_seen"
    if source_count == 1:
        return "single_passive_relation"
    if avg_score >= 0.55:
        return "recurring_strong_passive_relation"
    if max_score >= 0.55:
        return "recurring_mixed_passive_relation"
    return "recurring_weak_passive_relation"


def build_stability(relation_paths: list[Path], target_family: str) -> tuple[list[dict], list[dict]]:
    relations: dict[str, dict] = {}
    total_sources = 0

    for path in relation_paths:
        rows = _read_csv(path)
        if not rows:
            continue
        source = _source_label(path)
        total_sources += 1
        seen_in_source: set[str] = set()
        for row in rows:
            if str(row.get("target_family", "") or "") != target_family:
                continue
            related = str(row.get("related_family", "") or "")
            if not related:
                continue
            seen_in_source.add(related)
            item = relations.setdefault(
                related,
                {
                    "target_family": target_family,
                    "related_family": related,
                    "relation_sources": set(),
                    "relation_states": set(),
                    "related_sign_states": set(),
                    "scores": [],
                    "field_overlaps": [],
                    "action_overlaps": [],
                    "source_overlaps": [],
                },
            )
            item["relation_sources"].add(source)
            item["relation_states"].add(str(row.get("relation_state", "") or "-"))
            item["related_sign_states"].add(str(row.get("related_sign_state", "") or "-"))
            item["scores"].append(_safe_float(row.get("relation_score")))
            item["field_overlaps"].append(_safe_float(row.get("field_overlap")))
            item["action_overlaps"].append(_safe_float(row.get("action_overlap")))
            item["source_overlaps"].append(_safe_float(row.get("source_overlap")))

    detail: list[dict] = []
    groups: dict[str, dict] = {}
    for item in relations.values():
        source_count = len(item["relation_sources"])
        scores = list(item["scores"])
        avg_score = sum(scores) / max(1, len(scores))
        max_score = max(scores) if scores else 0.0
        min_score = min(scores) if scores else 0.0
        state = _stability_state(source_count, avg_score, max_score)
        row = {
            "target_family": target_family,
            "related_family": item["related_family"],
            "relation_stability_state": state,
            "relation_source_count": source_count,
            "available_relation_sources": total_sources,
            "relation_sources": "|".join(sorted(item["relation_sources"])),
            "relation_states": "|".join(sorted(item["relation_states"])),
            "related_sign_states": "|".join(sorted(item["related_sign_states"])),
            "avg_relation_score": round(avg_score, 6),
            "max_relation_score": round(max_score, 6),
            "min_relation_score": round(min_score, 6),
            "avg_field_overlap": round(sum(item["field_overlaps"]) / max(1, len(item["field_overlaps"])), 6),
            "avg_action_overlap": round(sum(item["action_overlaps"]) / max(1, len(item["action_overlaps"])), 6),
            "avg_source_overlap": round(sum(item["source_overlaps"]) / max(1, len(item["source_overlaps"])), 6),
            "passive_only": True,
            "writes_runtime_memory": False,
            "read_by_mini_dio": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
            "is_entry_signal": False,
            "is_direction_signal": False,
        }
        detail.append(row)
        group = groups.setdefault(
            state,
            {
                "relation_stability_state": state,
                "relation_count": 0,
                "families": [],
                "avg_score_sum": 0.0,
            },
        )
        group["relation_count"] += 1
        group["families"].append(item["related_family"])
        group["avg_score_sum"] += avg_score

    detail.sort(
        key=lambda row: (
            -int(row["relation_source_count"]),
            -float(row["avg_relation_score"]),
            str(row["related_family"]),
        )
    )
    summary = [
        {
            "relation_stability_state": group["relation_stability_state"],
            "relation_count": int(group["relation_count"]),
            "avg_relation_score": round(float(group["avg_score_sum"]) / max(1, int(group["relation_count"])), 6),
            "families": "|".join(sorted(group["families"])),
            "passive_only": True,
            "influences_action": False,
        }
        for group in groups.values()
    ]
    summary.sort(key=lambda row: (-int(row["relation_count"]), str(row["relation_stability_state"])))
    return detail, summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(rows: list[dict], summary: list[dict], output_dir: Path, target_family: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "passive_sign_relation_stability.csv"
    summary_path = output_dir / "passive_sign_relation_stability_summary.csv"
    json_path = output_dir / "passive_sign_relation_stability.json"
    md_path = output_dir / "passive_sign_relation_stability.md"
    _write_csv(detail_path, rows, ["target_family", "related_family", "relation_stability_state"])
    _write_csv(summary_path, summary, ["relation_stability_state", "relation_count"])
    payload = {
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
        "target_family": target_family,
        "relations": rows,
        "summary": summary,
    }
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    lines = [
        "# Passive Sign Relation Stability",
        "",
        "## Grenze",
        "- passiv",
        "- keine Runtime-Lesung",
        "- keine Handlung",
        "- keine Richtung",
        "",
        f"Target: `{target_family}`",
        "",
        "## Summary",
    ]
    for row in summary:
        lines.append(
            f"- {row['relation_stability_state']}: count={row['relation_count']} "
            f"avg={row['avg_relation_score']} {row['families']}"
        )
    lines.extend(["", "## Relations"])
    for row in rows[:16]:
        lines.append(
            f"- {row['related_family']}: {row['relation_stability_state']} "
            f"sources={row['relation_source_count']}/{row['available_relation_sources']} "
            f"avg={row['avg_relation_score']} max={row['max_relation_score']} "
            f"fields={row['avg_field_overlap']} actions={row['avg_action_overlap']}"
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive sign relation stability")
    parser.add_argument("--relations", nargs="+", required=True)
    parser.add_argument("--target-family", default="dio_0x52")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    paths = _expand_patterns(args.relations)
    rows, summary = build_stability(paths, args.target_family)
    write_outputs(rows, summary, Path(args.output_dir), args.target_family)
    print(f"relation_sources={len(paths)} relations={len(rows)} summary_rows={len(summary)}")


if __name__ == "__main__":
    main()
