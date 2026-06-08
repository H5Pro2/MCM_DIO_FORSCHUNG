"""Compact passive maps in a DIO mini memory file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from config import Config
from DIO_MINI.semantic_memory import SemanticMemory


def compact_memory(memory_path: Path, max_sensor_relations: int = 128) -> dict:
    before_bytes = memory_path.stat().st_size if memory_path.exists() else 0
    memory = SemanticMemory(memory_path, max_symbols=getattr(Config, "DIO_MINI_MAX_EPISODES", 2048))
    memory.load()
    before = {
        "symbols": len(memory.data.get("symbols", {}) or {}),
        "families": len(memory.data.get("families", {}) or {}),
        "relations": len(memory.data.get("relations", {}) or {}),
        "sensor_relations": len(memory.data.get("sensor_relations", {}) or {}),
        "bytes": before_bytes,
    }
    compact_result = memory.compact_sensor_relations(max_relations=max_sensor_relations)
    memory.save()
    after_bytes = memory_path.stat().st_size if memory_path.exists() else 0
    after = {
        "symbols": len(memory.data.get("symbols", {}) or {}),
        "families": len(memory.data.get("families", {}) or {}),
        "relations": len(memory.data.get("relations", {}) or {}),
        "sensor_relations": len(memory.data.get("sensor_relations", {}) or {}),
        "bytes": after_bytes,
    }
    return {
        "memory": str(memory_path),
        "max_sensor_relations": max_sensor_relations,
        "before": before,
        "after": after,
        "compact_result": compact_result,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compact DIO mini memory passive maps")
    parser.add_argument("--memory", required=True)
    parser.add_argument("--max-sensor-relations", type=int, default=128)
    parser.add_argument("--report", default="")
    args = parser.parse_args()

    result = compact_memory(Path(args.memory), max_sensor_relations=max(1, int(args.max_sensor_relations)))
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
