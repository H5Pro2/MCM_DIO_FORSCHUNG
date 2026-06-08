"""Analyze passive timing consequence stored in DIO mini semantic memory."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


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


def _action_rows(scope: str, records: dict) -> list[dict]:
    rows = []
    for name, record in sorted(records.items()):
        if not isinstance(record, dict):
            continue
        for action in TRADE_ACTIONS:
            state = dict(dict(record.get("actions", {}) or {}).get(action, {}) or {})
            count = _safe_int(state.get("count", 0))
            if count <= 0:
                continue
            reward_sum = _safe_float(state.get("reward_sum", 0.0))
            timing_sum = _safe_float(state.get("timing_improvement_sum", 0.0))
            rows.append(
                {
                    "scope": scope,
                    "name": name,
                    "action": action,
                    "count": count,
                    "reward_sum": round(reward_sum, 6),
                    "avg_reward": round(reward_sum / max(1, count), 6),
                    "trust": round(_safe_float(state.get("trust", 0.0)), 6),
                    "caution": round(_safe_float(state.get("caution", 0.0)), 6),
                    "timing_improvement_sum": round(timing_sum, 6),
                    "avg_timing_improvement": round(timing_sum / max(1, count), 6),
                    "last_timing_improvement": round(_safe_float(state.get("last_timing_improvement", 0.0)), 6),
                }
            )
    rows.sort(
        key=lambda item: (
            item["avg_timing_improvement"],
            -item["avg_reward"],
            item["count"],
        ),
        reverse=True,
    )
    return rows


def analyze(memory_path: Path) -> dict:
    data = json.loads(memory_path.read_text(encoding="utf-8"))
    family_rows = _action_rows("family", dict(data.get("families", {}) or {}))
    symbol_rows = _action_rows("symbol", dict(data.get("symbols", {}) or {}))
    return {
        "memory": str(memory_path),
        "runs": _safe_int(data.get("runs", 0)),
        "family_rows": family_rows,
        "symbol_rows": symbol_rows,
    }


def write_outputs(result: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_timing_memory.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    family_rows = list(result.get("family_rows", []) or [])
    symbol_rows = list(result.get("symbol_rows", []) or [])
    if family_rows:
        with (output_dir / "dio_mini_timing_memory_families.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(family_rows[0].keys()))
            writer.writeheader()
            writer.writerows(family_rows)
    if symbol_rows:
        with (output_dir / "dio_mini_timing_memory_symbols.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(symbol_rows[0].keys()))
            writer.writeheader()
            writer.writerows(symbol_rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze passive DIO mini timing memory")
    parser.add_argument("--memory", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    result = analyze(Path(args.memory))
    write_outputs(result, Path(args.output_dir))
    for row in list(result.get("family_rows", []) or [])[:12]:
        print(
            f"family={row['name']} action={row['action']} count={row['count']} "
            f"avg_reward={row['avg_reward']:.4f} avg_timing={row['avg_timing_improvement']:.6f}"
        )


if __name__ == "__main__":
    main()
