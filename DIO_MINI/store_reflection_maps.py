"""Store passive DIO_MINI reflection-map snapshots in semantic memory."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from DIO_MINI.semantic_memory import SemanticMemory, make_reflection_map_symbol


def _int(value: object) -> int:
    try:
        return int(float(value))
    except Exception:
        return 0


def _float(value: object) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


def _payload(row: dict, source_probe: str) -> dict:
    return {
        "reflection_symbol": row.get("reflection_symbol", ""),
        "symbol_family": row.get("symbol_family", ""),
        "reflection_state": row.get("reflection_state", ""),
        "reflection_map_state": row.get("reflection_map_state", ""),
        "reflection_map_reason": row.get("reflection_map_reason", ""),
        "dio_sentence": row.get("dio_sentence", ""),
        "seen_count": _int(row.get("seen_count")),
        "executed_count": _int(row.get("executed_count")),
        "observed_count": _int(row.get("observed_count")),
        "reward_sum": _float(row.get("reward_sum")),
        "best_reward_sum": _float(row.get("best_reward_sum")),
        "actions": row.get("actions", ""),
        "runs": row.get("runs", ""),
        "source_probe": source_probe,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory", required=True)
    parser.add_argument("--reflection-map", required=True)
    parser.add_argument("--source-probe", default="")
    parser.add_argument("--max-reflection-maps", type=int, default=96)
    args = parser.parse_args()

    memory = SemanticMemory(args.memory)
    memory.load()
    stored = 0
    with Path(args.reflection_map).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            payload = _payload(row, args.source_probe)
            if not payload["symbol_family"] or not payload["reflection_map_state"]:
                continue
            reflection_map_symbol = make_reflection_map_symbol(payload)
            memory.store_reflection_map(reflection_map_symbol, payload)
            stored += 1
            print(
                f"stored_reflection_map={reflection_map_symbol} "
                f"family={payload['symbol_family']} "
                f"state={payload['reflection_map_state']} passive_only=1"
            )
    memory.compact_reflection_maps(args.max_reflection_maps)
    memory.save()
    print(f"stored_reflection_maps_total={stored}")


if __name__ == "__main__":
    main()
