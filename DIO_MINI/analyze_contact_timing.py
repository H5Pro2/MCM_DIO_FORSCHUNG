"""Analyze DIO mini executed contact timing against the controlled world.

Diagnostic only. It does not classify setups. It shows whether an executed
contact had a better reachable price inside the same future evaluation window.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.mini_world import load_candles


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


def _episode_paths(debug_root: Path) -> list[Path]:
    if debug_root.name == "episodes.csv":
        return [debug_root]
    return sorted(debug_root.glob("dio_mini_lauf_*/episodes.csv"))


def _entry_improvement(action: str, entry_price: float, better_entry: float) -> float:
    if entry_price <= 0.0:
        return 0.0
    if action == "LONG":
        return max(0.0, entry_price - better_entry) / entry_price
    if action == "SHORT":
        return max(0.0, better_entry - entry_price) / entry_price
    return 0.0


def analyze(debug_root: Path, data_path: Path) -> tuple[list[dict], list[dict]]:
    candles = load_candles(data_path)
    by_timestamp = {str(item["timestamp_ms"]): item for item in candles}
    rows = []
    for path in _episode_paths(debug_root):
        run = _safe_int(path.parent.name.rsplit("_", 1)[-1], 0)
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                action = str(row.get("action", "WAIT") or "WAIT").upper()
                if action not in TRADE_ACTIONS:
                    continue
                timestamp = str(row.get("timestamp_ms", "") or "")
                candle = by_timestamp.get(timestamp, {})
                entry_price = _safe_float(candle.get("close", 0.0))
                better_entry = _safe_float(row.get("better_entry_training", entry_price))
                improvement = _entry_improvement(action, entry_price, better_entry)
                rows.append(
                    {
                        "run": run,
                        "tick": _safe_int(row.get("tick", 0)),
                        "timestamp_ms": timestamp,
                        "family": row.get("symbol_family", "-"),
                        "action": action,
                        "entry_price": round(entry_price, 8),
                        "better_entry_training": round(better_entry, 8),
                        "entry_improvement_room": round(improvement, 6),
                        "reward": round(_safe_float(row.get("reward", 0.0)), 6),
                        "trade_readiness": round(_safe_float(row.get("trade_readiness", 0.0)), 6),
                        "mature_transfer": round(_safe_float(row.get("mature_transfer", 0.0)), 6),
                        "phase_age": _safe_int(row.get("phase_age", 0)),
                        "episode_relation": row.get("episode_relation", "-"),
                    }
                )
    summary_by_family: dict[str, dict] = {}
    for row in rows:
        family = str(row.get("family", "-") or "-")
        record = summary_by_family.setdefault(
            family,
            {
                "family": family,
                "count": 0,
                "reward_sum": 0.0,
                "improvement_sum": 0.0,
                "max_improvement_room": 0.0,
                "actions": {},
            },
        )
        record["count"] += 1
        record["reward_sum"] += _safe_float(row.get("reward", 0.0))
        record["improvement_sum"] += _safe_float(row.get("entry_improvement_room", 0.0))
        record["max_improvement_room"] = max(
            _safe_float(record["max_improvement_room"]),
            _safe_float(row.get("entry_improvement_room", 0.0)),
        )
        action = str(row.get("action", "-") or "-")
        record["actions"][action] = int(record["actions"].get(action, 0)) + 1
    summary_rows = []
    for record in summary_by_family.values():
        count = max(1, _safe_int(record["count"]))
        summary_rows.append(
            {
                "family": record["family"],
                "count": record["count"],
                "actions": ",".join(f"{key}:{value}" for key, value in sorted(record["actions"].items())),
                "reward_sum": round(_safe_float(record["reward_sum"]), 6),
                "avg_reward": round(_safe_float(record["reward_sum"]) / count, 6),
                "avg_entry_improvement_room": round(_safe_float(record["improvement_sum"]) / count, 6),
                "max_entry_improvement_room": round(_safe_float(record["max_improvement_room"]), 6),
            }
        )
    summary_rows.sort(
        key=lambda item: (
            item["avg_entry_improvement_room"],
            -item["avg_reward"],
            item["count"],
        ),
        reverse=True,
    )
    rows.sort(key=lambda item: (item["run"], item["tick"]))
    return rows, summary_rows


def write_outputs(rows: list[dict], summary_rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_contact_timing.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "dio_mini_contact_timing_summary.json").write_text(
        json.dumps(summary_rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    if rows:
        with (output_dir / "dio_mini_contact_timing.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    if summary_rows:
        with (output_dir / "dio_mini_contact_timing_summary.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(summary_rows[0].keys()))
            writer.writeheader()
            writer.writerows(summary_rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze DIO mini contact timing")
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--data", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    rows, summary_rows = analyze(Path(args.debug_root), Path(args.data))
    write_outputs(rows, summary_rows, Path(args.output_dir))
    for row in summary_rows[:12]:
        print(
            f"family={row['family']} count={row['count']} avg_reward={row['avg_reward']:.4f} "
            f"avg_improvement={row['avg_entry_improvement_room']:.6f}"
        )


if __name__ == "__main__":
    main()
