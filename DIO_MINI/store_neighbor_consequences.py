"""Store passive DIO mini neighbor-consequence relations in semantic memory.

This persists the consequence-bound similarity map as a diagnostic artifact.
It does not affect action selection.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from config import Config
from DIO_MINI.semantic_memory import SemanticMemory


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
        return int(float(value))
    except Exception:
        return default


def store_neighbor_consequences(memory_path: Path, relation_path: Path, max_relations: int = 128) -> list[dict]:
    memory = SemanticMemory(memory_path, max_symbols=getattr(Config, "DIO_MINI_MAX_EPISODES", 2048))
    memory.max_neighbor_consequences = max(1, int(max_relations))
    memory.load()
    rows = []
    with relation_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if len(rows) >= memory.max_neighbor_consequences:
                break
            target_family = str(row.get("target_family", "-") or "-")
            reference_family = str(row.get("reference_family", "-") or "-")
            relation_key = f"{target_family}->{reference_family}"
            summary = {
                "target_family": target_family,
                "reference_family": reference_family,
                "neighbor_consequence_state": str(row.get("neighbor_consequence_state", "-") or "-"),
                "sensor_distance": _safe_float(row.get("sensor_distance", 0.0)),
                "sensor_similarity": _safe_float(row.get("sensor_similarity", 0.0)),
                "target_reward_sum": _safe_float(row.get("target_reward_sum", 0.0)),
                "reference_reward_sum": _safe_float(row.get("reference_reward_sum", 0.0)),
                "target_executed_rows": _safe_int(row.get("target_executed_rows", 0)),
                "target_observed_rows": _safe_int(row.get("target_observed_rows", 0)),
                "reference_executed_rows": _safe_int(row.get("reference_executed_rows", 0)),
                "reference_observed_rows": _safe_int(row.get("reference_observed_rows", 0)),
                "target_class": str(row.get("target_class", "-") or "-"),
                "reference_class": str(row.get("reference_class", "-") or "-"),
                "target_phases": str(row.get("target_phases", "-") or "-"),
                "reference_phases": str(row.get("reference_phases", "-") or "-"),
            }
            memory.set_neighbor_consequence_summary(relation_key, summary)
            rows.append({"relation_key": relation_key, **summary})
    memory.save()
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Store passive DIO mini neighbor consequences")
    parser.add_argument("--memory", required=True)
    parser.add_argument("--relations", required=True)
    parser.add_argument("--max-relations", type=int, default=128)
    args = parser.parse_args()

    rows = store_neighbor_consequences(
        Path(args.memory),
        Path(args.relations),
        max_relations=max(1, int(args.max_relations)),
    )
    for row in rows[:12]:
        print(
            f"stored_neighbor_consequence={row['relation_key']} "
            f"state={row['neighbor_consequence_state']} "
            f"similarity={row['sensor_similarity']:.4f} passive_only=1"
        )


if __name__ == "__main__":
    main()
