"""Analyze DIO mini syntax family condensation.

This is diagnostic only. It reads episode CSV files and reports how DIO's own
syntax words condense into families across runs.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


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


def collect_episode_paths(debug_root: Path) -> list[Path]:
    return sorted(debug_root.glob("dio_mini_lauf_*/episodes.csv"))


def analyze(debug_root: Path) -> list[dict]:
    families: dict[str, dict] = {}
    for path in collect_episode_paths(debug_root):
        run_text = path.parent.name.rsplit("_", 1)[-1]
        run = _safe_int(run_text, 0)
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                family = str(row.get("symbol_family", "-") or "-")
                symbol = str(row.get("symbol", "-") or "-")
                action = str(row.get("action", "WAIT") or "WAIT").upper()
                raw_action = str(row.get("raw_action", "WAIT") or "WAIT").upper()
                best_action = str(row.get("best_action_training", "WAIT") or "WAIT").upper()
                record = families.setdefault(
                    family,
                    {
                        "family": family,
                        "runs": set(),
                        "symbols": set(),
                        "rows": 0,
                        "actions": defaultdict(int),
                        "raw_actions": defaultdict(int),
                        "best_actions": defaultdict(int),
                        "reward_sum": 0.0,
                        "observation_learning_events": 0,
                        "observation_pressure_sum": 0.0,
                    },
                )
                record["runs"].add(run)
                record["symbols"].add(symbol)
                record["rows"] += 1
                record["actions"][action] += 1
                record["raw_actions"][raw_action] += 1
                record["best_actions"][best_action] += 1
                record["reward_sum"] += _safe_float(row.get("reward", 0.0))
                observation_pressure = _safe_float(row.get("observation_learning_pressure", 0.0))
                if observation_pressure > 0.0:
                    record["observation_learning_events"] += 1
                    record["observation_pressure_sum"] += observation_pressure
    rows = []
    for record in families.values():
        rows.append(
            {
                "family": record["family"],
                "runs": ",".join(str(run) for run in sorted(record["runs"])),
                "run_count": len(record["runs"]),
                "symbol_count": len(record["symbols"]),
                "rows": record["rows"],
                "symbols_per_row": round(len(record["symbols"]) / max(1, record["rows"]), 6),
                "executed_long": int(record["actions"].get("LONG", 0)),
                "executed_short": int(record["actions"].get("SHORT", 0)),
                "executed_wait": int(record["actions"].get("WAIT", 0)),
                "raw_long": int(record["raw_actions"].get("LONG", 0)),
                "raw_short": int(record["raw_actions"].get("SHORT", 0)),
                "best_long": int(record["best_actions"].get("LONG", 0)),
                "best_short": int(record["best_actions"].get("SHORT", 0)),
                "reward_sum": round(float(record["reward_sum"]), 6),
                "avg_reward": round(float(record["reward_sum"]) / max(1, record["rows"]), 6),
                "observation_learning_events": int(record["observation_learning_events"]),
                "avg_observation_pressure": round(
                    float(record["observation_pressure_sum"]) / max(1, record["observation_learning_events"]),
                    6,
                ),
            }
        )
    rows.sort(key=lambda item: (item["run_count"], item["rows"], abs(item["reward_sum"])), reverse=True)
    return rows


def write_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_syntax_families.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    if rows:
        with (output_dir / "dio_mini_syntax_families.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze DIO mini syntax families")
    parser.add_argument("--debug-root", default="debug")
    parser.add_argument("--output-dir", default="debug")
    args = parser.parse_args()

    rows = analyze(Path(args.debug_root))
    write_outputs(rows, Path(args.output_dir))
    for row in rows[:12]:
        print(
            f"family={row['family']} runs={row['run_count']} rows={row['rows']} "
            f"symbols={row['symbol_count']} reward={row['reward_sum']:.4f}"
        )


if __name__ == "__main__":
    main()
