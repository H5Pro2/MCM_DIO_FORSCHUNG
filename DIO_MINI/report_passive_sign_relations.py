"""Report passive relations between Mini-DIO sign-memory entries.

This diagnostic reads passive_sign_memory.csv and builds relation candidates
between recurring signs. It is not runtime memory and does not influence action.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(float(value or default))
    except Exception:
        return default


def _split(value: object) -> set[str]:
    return {item.strip() for item in str(value or "").split("|") if item.strip()}


def _jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 1.0
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def _relation_state(score: float, target: dict, other: dict) -> str:
    target_state = str(target.get("sign_state", "") or "")
    other_state = str(other.get("sign_state", "") or "")
    if target_state == other_state and score >= 0.80:
        return "same_passive_sign_field"
    if other_state == "known_lage_direction_candidate" and score >= 0.60:
        return "direction_candidate_near_unripe_sign"
    if score >= 0.55:
        return "passive_sign_neighbor"
    return "weak_passive_sign_neighbor"


def build_relations(sign_rows: list[dict], target_family: str) -> tuple[list[dict], list[dict]]:
    by_family = {str(row.get("symbol_family", "") or ""): dict(row) for row in sign_rows}
    target = by_family.get(target_family)
    if not target:
        return [], []

    target_fields = _split(target.get("stable_fields"))
    target_actions = _split(target.get("validation_best_actions"))
    target_sources = _split(target.get("validation_sources_seen"))
    rows: list[dict] = []
    groups: dict[str, dict] = {}

    for other_family, other in sorted(by_family.items()):
        if other_family == target_family:
            continue
        other_fields = _split(other.get("stable_fields"))
        other_actions = _split(other.get("validation_best_actions"))
        other_sources = _split(other.get("validation_sources_seen"))
        field_overlap = _jaccard(target_fields, other_fields)
        action_overlap = _jaccard(target_actions, other_actions)
        source_overlap = _jaccard(target_sources, other_sources)
        state_match = 1.0 if str(target.get("sign_state", "")) == str(other.get("sign_state", "")) else 0.0
        score = (
            field_overlap * 0.42
            + action_overlap * 0.22
            + source_overlap * 0.16
            + state_match * 0.20
        )
        relation_state = _relation_state(score, target, other)
        item = {
            "target_family": target_family,
            "target_sign_symbol": str(target.get("passive_sign_symbol", "") or ""),
            "target_sign_state": str(target.get("sign_state", "") or ""),
            "related_family": other_family,
            "related_sign_symbol": str(other.get("passive_sign_symbol", "") or ""),
            "related_sign_state": str(other.get("sign_state", "") or ""),
            "relation_state": relation_state,
            "relation_score": round(score, 6),
            "field_overlap": round(field_overlap, 6),
            "action_overlap": round(action_overlap, 6),
            "source_overlap": round(source_overlap, 6),
            "target_sources": str(target.get("validation_sources_seen", "") or ""),
            "related_sources": str(other.get("validation_sources_seen", "") or ""),
            "target_best_actions": str(target.get("validation_best_actions", "") or ""),
            "related_best_actions": str(other.get("validation_best_actions", "") or ""),
            "target_observations": _safe_int(target.get("validation_observation_count")),
            "related_observations": _safe_int(other.get("validation_observation_count")),
            "passive_only": True,
            "writes_runtime_memory": False,
            "read_by_mini_dio": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
            "is_entry_signal": False,
            "is_direction_signal": False,
        }
        rows.append(item)
        group = groups.setdefault(
            relation_state,
            {
                "relation_state": relation_state,
                "relation_count": 0,
                "families": [],
                "avg_score_sum": 0.0,
            },
        )
        group["relation_count"] += 1
        group["families"].append(other_family)
        group["avg_score_sum"] += score

    rows.sort(key=lambda row: (-float(row["relation_score"]), str(row["related_family"])))
    summary = [
        {
            "relation_state": group["relation_state"],
            "relation_count": int(group["relation_count"]),
            "avg_relation_score": round(float(group["avg_score_sum"]) / max(1, int(group["relation_count"])), 6),
            "families": "|".join(sorted(group["families"])),
            "passive_only": True,
            "influences_action": False,
        }
        for group in groups.values()
    ]
    summary.sort(key=lambda row: (-int(row["relation_count"]), str(row["relation_state"])))
    return rows, summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(rows: list[dict], summary: list[dict], output_dir: Path, target_family: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "passive_sign_relations.csv"
    summary_path = output_dir / "passive_sign_relations_summary.csv"
    json_path = output_dir / "passive_sign_relations.json"
    md_path = output_dir / "passive_sign_relations.md"
    _write_csv(detail_path, rows, ["target_family", "related_family", "relation_state"])
    _write_csv(summary_path, summary, ["relation_state", "relation_count"])
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
                "target_family": target_family,
                "relations": rows,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Passive Sign Relations",
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
            f"- {row['relation_state']}: count={row['relation_count']} "
            f"avg={row['avg_relation_score']} {row['families']}"
        )
    lines.extend(["", "## Naechste Zeichen"])
    for row in rows[:12]:
        lines.append(
            f"- {row['related_family']}: {row['relation_state']} "
            f"score={row['relation_score']} fields={row['field_overlap']} "
            f"actions={row['action_overlap']} state={row['related_sign_state']}"
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive sign relations")
    parser.add_argument("--sign-memory", required=True)
    parser.add_argument("--target-family", default="dio_0x52")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    rows, summary = build_relations(_read_csv(Path(args.sign_memory)), args.target_family)
    write_outputs(rows, summary, Path(args.output_dir), args.target_family)
    print(f"relations={len(rows)} summary_rows={len(summary)}")


if __name__ == "__main__":
    main()
