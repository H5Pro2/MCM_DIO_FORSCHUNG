"""Report passive DIO_MINI reflection seeds from semantic memory."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.semantic_memory import SemanticMemory


def _rows(memory: SemanticMemory) -> list[dict]:
    seeds = memory.data.setdefault("reflection_seeds", {})
    if not isinstance(seeds, dict):
        return []
    rows = []
    for symbol, payload in seeds.items():
        item = dict(payload or {})
        item.setdefault("reflection_symbol", symbol)
        rows.append(
            {
                "reflection_symbol": str(item.get("reflection_symbol", symbol) or symbol),
                "symbol_family": str(item.get("symbol_family", "") or ""),
                "reflection_state": str(item.get("reflection_state", "") or ""),
                "prior_observation_count": int(item.get("prior_observation_count", 0) or 0),
                "prior_execution_count": int(item.get("prior_execution_count", 0) or 0),
                "prior_execution_reward_sum": round(float(item.get("prior_execution_reward_sum", 0.0) or 0.0), 6),
                "followup_seen_count": int(item.get("followup_seen_count", 0) or 0),
                "followup_executed_aligned_count": int(item.get("followup_executed_aligned_count", 0) or 0),
                "followup_executed_reward": round(float(item.get("followup_executed_reward", 0.0) or 0.0), 6),
                "followup_observed_count": int(item.get("followup_observed_count", 0) or 0),
                "followup_overheld_count": int(item.get("followup_overheld_count", 0) or 0),
                "followup_actions": str(item.get("followup_actions", "") or ""),
                "passive_only": int(item.get("passive_only", 0) or 0),
            }
        )
    rows.sort(
        key=lambda item: (
            item["reflection_state"] != "reflection_seed_reconfirmed",
            -float(item["followup_executed_reward"]),
            item["symbol_family"],
        )
    )
    return rows


def _write(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "dio_mini_reflection_seeds.csv"
    json_path = output_dir / "dio_mini_reflection_seeds.json"
    md_path = output_dir / "dio_mini_reflection_seeds.md"
    fields = [
        "reflection_symbol",
        "symbol_family",
        "reflection_state",
        "prior_observation_count",
        "prior_execution_count",
        "prior_execution_reward_sum",
        "followup_seen_count",
        "followup_executed_aligned_count",
        "followup_executed_reward",
        "followup_observed_count",
        "followup_overheld_count",
        "followup_actions",
        "passive_only",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Reflection Seeds", ""]
    if not rows:
        lines.append("Keine Reflexionskeime gespeichert.")
    for row in rows:
        lines.extend(
            [
                f"## {row['reflection_symbol']}",
                f"- family: {row['symbol_family']}",
                f"- state: {row['reflection_state']}",
                f"- prior observation/execution: {row['prior_observation_count']} / {row['prior_execution_count']}",
                f"- prior_execution_reward_sum: {float(row['prior_execution_reward_sum']):.6f}",
                f"- followup seen: {row['followup_seen_count']}",
                f"- followup executed: {row['followup_executed_aligned_count']} / {float(row['followup_executed_reward']):.6f}",
                f"- followup observed: {row['followup_observed_count']}",
                f"- followup overheld: {row['followup_overheld_count']}",
                f"- actions: {row['followup_actions'] or '-'}",
                f"- passive_only: {row['passive_only']}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    memory = SemanticMemory(args.memory)
    memory.load()
    rows = _rows(memory)
    _write(rows, Path(args.output_dir))
    print(f"reflection_seeds={len(rows)}")
    for row in rows:
        print(
            f"{row['reflection_symbol']} family={row['symbol_family']} "
            f"state={row['reflection_state']} reward={row['followup_executed_reward']}"
        )


if __name__ == "__main__":
    main()
