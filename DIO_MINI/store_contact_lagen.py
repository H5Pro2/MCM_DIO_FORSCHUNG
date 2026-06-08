"""Store passive DIO_MINI contact-lage protocol rows in semantic memory."""

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


def _split(value: object) -> list[str]:
    text = str(value or "").strip()
    if not text:
        return []
    return [item.strip() for item in text.split(",") if item.strip()]


def _row_payload(row: dict) -> dict:
    return {
        "contact_lage_state": row.get("contact_lage_state", ""),
        "debug_root": row.get("debug_root", ""),
        "runs": _int(row.get("runs")),
        "trades_total": _int(row.get("trades_total")),
        "reward_total": _float(row.get("reward_total")),
        "contact_reward_sum": _float(row.get("contact_reward_sum")),
        "direct_positive_action": _int(row.get("direct_positive_action")),
        "observation_to_positive_action": _int(row.get("observation_to_positive_action")),
        "held_observation": _int(row.get("held_observation")),
        "quiet_family": _int(row.get("quiet_family")),
        "top_direct_action": _split(row.get("top_direct_action")),
        "top_observation_to_action": _split(row.get("top_observation_to_action")),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory", required=True)
    parser.add_argument("--protocol", required=True)
    parser.add_argument("--max-contact-lagen", type=int, default=64)
    args = parser.parse_args()

    memory = SemanticMemory(args.memory)
    memory.load()
    with Path(args.protocol).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            contact_id = str(row.get("contact_id", "") or "").strip()
            if not contact_id:
                continue
            payload = _row_payload(row)
            memory.store_contact_lage(contact_id, payload)
            print(
                f"stored_contact_lage={contact_id} "
                f"state={payload['contact_lage_state']} passive_only=1"
            )
    memory.compact_contact_lagen(args.max_contact_lagen)
    memory.save()


if __name__ == "__main__":
    main()
