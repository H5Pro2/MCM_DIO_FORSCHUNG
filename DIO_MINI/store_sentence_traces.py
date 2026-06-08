"""Store passive DIO_MINI sentence traces in semantic memory."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from DIO_MINI.semantic_memory import SemanticMemory


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
        "contact_symbol": row.get("contact_symbol", ""),
        "contact_lage_state": row.get("contact_lage_state", ""),
        "symbol_family": row.get("symbol_family", ""),
        "episode_contact_state": row.get("episode_contact_state", ""),
        "count": _int(row.get("count")),
        "reward_sum": _float(row.get("reward_sum")),
        "actions": row.get("actions", ""),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory", required=True)
    parser.add_argument("--traces", required=True)
    parser.add_argument("--max-sentence-traces", type=int, default=128)
    args = parser.parse_args()

    memory = SemanticMemory(args.memory)
    memory.load()
    with Path(args.traces).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            sentence_symbol = str(row.get("sentence_symbol", "") or "").strip()
            if not sentence_symbol:
                continue
            payload = _payload(row)
            memory.store_sentence_trace(sentence_symbol, payload)
            print(
                f"stored_sentence_trace={sentence_symbol} "
                f"state={payload['episode_contact_state']} passive_only=1"
            )
    memory.compact_sentence_traces(args.max_sentence_traces)
    memory.save()


if __name__ == "__main__":
    main()
