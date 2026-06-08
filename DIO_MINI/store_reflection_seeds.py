"""Store passive DIO_MINI reflection seeds in semantic memory."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from DIO_MINI.semantic_memory import SemanticMemory, make_reflection_seed_symbol


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


def _payload(row: dict) -> dict:
    return {
        "symbol_family": row.get("symbol_family", ""),
        "reflection_state": row.get("reflection_state", ""),
        "prior_observation_count": _int(row.get("prior_observation_count")),
        "prior_execution_count": _int(row.get("prior_execution_count")),
        "prior_observation_reward_potential_sum": _float(row.get("prior_observation_reward_potential_sum")),
        "prior_execution_reward_sum": _float(row.get("prior_execution_reward_sum")),
        "followup_seen_count": _int(row.get("followup_seen_count")),
        "followup_executed_aligned_count": _int(row.get("followup_executed_aligned_count")),
        "followup_executed_reward": _float(row.get("followup_executed_reward")),
        "followup_observed_count": _int(row.get("followup_observed_count")),
        "followup_observed_potential": _float(row.get("followup_observed_potential")),
        "followup_overheld_count": _int(row.get("followup_overheld_count")),
        "followup_overheld_potential": _float(row.get("followup_overheld_potential")),
        "followup_actions": row.get("followup_actions", ""),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory", required=True)
    parser.add_argument("--reflection-seeds", required=True)
    parser.add_argument("--max-reflection-seeds", type=int, default=64)
    args = parser.parse_args()

    memory = SemanticMemory(args.memory)
    memory.load()
    with Path(args.reflection_seeds).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            payload = _payload(row)
            if not payload["symbol_family"]:
                continue
            reflection_symbol = make_reflection_seed_symbol(payload)
            memory.store_reflection_seed(reflection_symbol, payload)
            print(
                f"stored_reflection_seed={reflection_symbol} "
                f"family={payload['symbol_family']} "
                f"state={payload['reflection_state']} passive_only=1"
            )
    memory.compact_reflection_seeds(args.max_reflection_seeds)
    memory.save()


if __name__ == "__main__":
    main()
