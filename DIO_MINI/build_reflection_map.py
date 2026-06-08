"""Build a reflection map from DIO mini family relations.

The map is diagnostic memory material. It does not change trading behavior.
It separates supportive family relations from conflict relations so DIO's
language can be inspected without turning similarity into an action rule.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.analyze_family_relations import analyze as analyze_relations


TRADE_ACTIONS = ("LONG", "SHORT")


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _relation_score(row: dict, relation_type: str) -> float:
    similarity = _safe_float(row.get("similarity", 0.0))
    if relation_type == "support":
        alignment = max(
            abs(_safe_float(row.get("long_alignment", 0.0))),
            abs(_safe_float(row.get("short_alignment", 0.0))),
        )
    elif relation_type == "conflict":
        alignment = abs(_safe_float(row.get("cross_alignment", 0.0)))
    else:
        alignment = 0.0
    return similarity * (1.0 + alignment)


def _empty_family_record(family: str) -> dict:
    return {
        "family": family,
        "relation_count": 0,
        "support_count": 0,
        "conflict_count": 0,
        "neutral_count": 0,
        "best_support_family": "-",
        "best_support_action": "-",
        "best_support_similarity": 0.0,
        "best_support_score": 0.0,
        "best_conflict_family": "-",
        "best_conflict_actions": "-",
        "best_conflict_similarity": 0.0,
        "best_conflict_score": 0.0,
    }


def _classify(row: dict) -> str:
    left_action = str(row.get("left_action", "-") or "-")
    right_action = str(row.get("right_action", "-") or "-")
    if left_action in TRADE_ACTIONS and right_action in TRADE_ACTIONS:
        return "support" if left_action == right_action else "conflict"
    return "neutral"


def _apply_relation(record: dict, other_family: str, row: dict, relation_type: str, own_action: str, other_action: str) -> None:
    record["relation_count"] += 1
    record[f"{relation_type}_count"] += 1
    if relation_type == "support":
        score = _relation_score(row, "support")
        if score > _safe_float(record.get("best_support_score", 0.0)):
            record["best_support_family"] = other_family
            record["best_support_action"] = own_action if own_action == other_action else f"{own_action}/{other_action}"
            record["best_support_similarity"] = _safe_float(row.get("similarity", 0.0))
            record["best_support_score"] = score
    elif relation_type == "conflict":
        score = _relation_score(row, "conflict")
        if score > _safe_float(record.get("best_conflict_score", 0.0)):
            record["best_conflict_family"] = other_family
            record["best_conflict_actions"] = f"{own_action}/{other_action}"
            record["best_conflict_similarity"] = _safe_float(row.get("similarity", 0.0))
            record["best_conflict_score"] = score


def build_map(memory_path: Path) -> list[dict]:
    rows = analyze_relations(memory_path)
    families: dict[str, dict] = {}
    for row in rows:
        left = str(row.get("left_family", "-") or "-")
        right = str(row.get("right_family", "-") or "-")
        left_action = str(row.get("left_action", "-") or "-")
        right_action = str(row.get("right_action", "-") or "-")
        relation_type = _classify(row)
        left_record = families.setdefault(left, _empty_family_record(left))
        right_record = families.setdefault(right, _empty_family_record(right))
        _apply_relation(left_record, right, row, relation_type, left_action, right_action)
        _apply_relation(right_record, left, row, relation_type, right_action, left_action)
    output = []
    for record in families.values():
        relation_count = max(1, _safe_int(record.get("relation_count", 0), 0))
        record["support_ratio"] = round(_safe_int(record.get("support_count", 0), 0) / relation_count, 6)
        record["conflict_ratio"] = round(_safe_int(record.get("conflict_count", 0), 0) / relation_count, 6)
        record["best_support_similarity"] = round(_safe_float(record.get("best_support_similarity", 0.0)), 6)
        record["best_support_score"] = round(_safe_float(record.get("best_support_score", 0.0)), 6)
        record["best_conflict_similarity"] = round(_safe_float(record.get("best_conflict_similarity", 0.0)), 6)
        record["best_conflict_score"] = round(_safe_float(record.get("best_conflict_score", 0.0)), 6)
        output.append(record)
    output.sort(
        key=lambda item: (
            _safe_float(item.get("best_support_score", 0.0)),
            _safe_float(item.get("best_conflict_score", 0.0)),
            _safe_int(item.get("relation_count", 0)),
        ),
        reverse=True,
    )
    return output


def write_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_reflection_map.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    if rows:
        with (output_dir / "dio_mini_reflection_map.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build DIO mini reflection map")
    parser.add_argument("--memory", default="bot_memory/dio_mini_sensor_transfer_memory.json")
    parser.add_argument("--output-dir", default="debug/dio_mini_reflection_map")
    args = parser.parse_args()

    rows = build_map(Path(args.memory))
    write_outputs(rows, Path(args.output_dir))
    for row in rows[:12]:
        print(
            f"family={row['family']} support={row['best_support_family']} "
            f"support_score={row['best_support_score']:.4f} conflict={row['best_conflict_family']} "
            f"conflict_score={row['best_conflict_score']:.4f}"
        )


if __name__ == "__main__":
    main()
