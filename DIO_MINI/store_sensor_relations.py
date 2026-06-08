"""Store passive DIO mini sensor-family relations in semantic memory."""

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
        return int(value)
    except Exception:
        return default


def store_sensor_relations(memory_path: Path, relation_path: Path, max_relations: int = 128) -> list[dict]:
    memory = SemanticMemory(memory_path, max_symbols=getattr(Config, "DIO_MINI_MAX_EPISODES", 2048))
    memory.max_sensor_relations = max(1, int(max_relations))
    memory.load()
    rows = []
    with relation_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if len(rows) >= memory.max_sensor_relations:
                break
            left_family = str(row.get("left_family", "-") or "-")
            right_family = str(row.get("right_family", "-") or "-")
            left_phase = str(row.get("left_phase", "-") or "-")
            right_phase = str(row.get("right_phase", "-") or "-")
            relation_key = f"{left_phase}:{left_family}<->{right_phase}:{right_family}"
            summary = {
                "left_family": left_family,
                "right_family": right_family,
                "left_phase": left_phase,
                "right_phase": right_phase,
                "relation_kind": str(row.get("relation_kind", "-") or "-"),
                "sensor_relation_trace": _safe_float(row.get("sensor_relation_trace", 0.0)),
                "sensor_distance": _safe_float(row.get("sensor_distance", 0.0)),
                "visual_mcm_gap": _safe_float(row.get("visual_mcm_gap", 0.0)),
                "tone_tension_gap": _safe_float(row.get("tone_tension_gap", 0.0)),
                "left_reward": _safe_float(row.get("left_reward", 0.0)),
                "right_reward": _safe_float(row.get("right_reward", 0.0)),
                "left_executed": _safe_int(row.get("left_executed", 0)),
                "right_executed": _safe_int(row.get("right_executed", 0)),
            }
            memory.set_sensor_relation_summary(relation_key, summary)
            rows.append({"relation_key": relation_key, **summary})
    memory.save()
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Store passive DIO mini sensor-family relations")
    parser.add_argument("--memory", required=True)
    parser.add_argument("--relations", required=True)
    parser.add_argument("--max-relations", type=int, default=128)
    args = parser.parse_args()

    rows = store_sensor_relations(Path(args.memory), Path(args.relations), max_relations=max(1, int(args.max_relations)))
    for row in rows[:12]:
        print(
            f"stored_sensor_relation={row['relation_key']} kind={row['relation_kind']} "
            f"trace={row['sensor_relation_trace']:.4f} passive_only=1"
        )


if __name__ == "__main__":
    main()
