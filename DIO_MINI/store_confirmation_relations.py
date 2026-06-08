"""Store passive DIO mini confirmation relations in semantic memory.

This does not affect action selection. It persists the reflection map as a
learning artifact so later diagnostics can compare relation stability.
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
        return int(value)
    except Exception:
        return default


def _split_list(value: object) -> list[str]:
    return [item.strip() for item in str(value or "").split(",") if item.strip()]


def store_relations(memory_path: Path, relation_summary_path: Path) -> list[dict]:
    memory = SemanticMemory(memory_path, max_symbols=getattr(Config, "DIO_MINI_MAX_EPISODES", 2048))
    memory.load()
    rows = []
    with relation_summary_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            support_pair = str(row.get("support_pair", "-") or "-")
            summary = {
                "families": _split_list(row.get("families", "")),
                "phases": _split_list(row.get("phases", "")),
                "phase_count": _safe_int(row.get("phase_count", 0)),
                "rows": _safe_int(row.get("rows", 0)),
                "executed_local_confirmation": _safe_int(row.get("executed_local_confirmation", 0)),
                "observed_related_potential": _safe_int(row.get("observed_related_potential", 0)),
                "long_local": _safe_int(row.get("long_local", 0)),
                "short_local": _safe_int(row.get("short_local", 0)),
                "avg_local_confirmation": _safe_float(row.get("avg_local_confirmation", 0.0)),
                "max_local_confirmation": _safe_float(row.get("max_local_confirmation", 0.0)),
                "reward_sum": _safe_float(row.get("reward_sum", 0.0)),
            }
            memory.set_relation_summary(support_pair, summary)
            rows.append({"support_pair": support_pair, **summary})
    memory.save()
    rows.sort(
        key=lambda item: (
            item["executed_local_confirmation"],
            item["observed_related_potential"],
            item["phase_count"],
            item["max_local_confirmation"],
        ),
        reverse=True,
    )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Store passive DIO mini confirmation relations")
    parser.add_argument("--memory", required=True)
    parser.add_argument("--relation-summary", required=True)
    args = parser.parse_args()

    rows = store_relations(Path(args.memory), Path(args.relation_summary))
    for row in rows[:12]:
        print(
            f"stored_relation={row['support_pair']} phases={row['phase_count']} "
            f"executed={row['executed_local_confirmation']} passive_only=1"
        )


if __name__ == "__main__":
    main()
