"""Inspect executed and suppressed contacts in DIO mini episode files."""

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


def collect_episode_paths(debug_root: Path) -> list[Path]:
    if debug_root.name == "episodes.csv":
        return [debug_root]
    return sorted(debug_root.glob("dio_mini_lauf_*/episodes.csv"))


def _contact_kind(row: dict) -> str:
    action = str(row.get("action", "WAIT") or "WAIT").upper()
    raw_action = str(row.get("raw_action", "WAIT") or "WAIT").upper()
    phase_active = _safe_int(row.get("phase_active", 0))
    reward = _safe_float(row.get("reward", 0.0))
    best_reward = _safe_float(row.get("best_reward_training", 0.0))
    if action in TRADE_ACTIONS and reward > 0.0:
        return "positive_executed_contact"
    if action in TRADE_ACTIONS:
        return "burdened_executed_contact"
    if raw_action in TRADE_ACTIONS and phase_active:
        return "held_same_episode_contact"
    if raw_action in TRADE_ACTIONS:
        return "unexecuted_raw_contact"
    if best_reward > 0.0:
        return "observed_potential"
    return "quiet_wait"


def analyze(debug_root: Path) -> tuple[list[dict], list[dict]]:
    rows = []
    summary: dict[str, dict] = {}
    for path in collect_episode_paths(debug_root):
        run_text = path.parent.name.rsplit("_", 1)[-1]
        run = _safe_int(run_text, 0)
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                action = str(row.get("action", "WAIT") or "WAIT").upper()
                raw_action = str(row.get("raw_action", "WAIT") or "WAIT").upper()
                kind = _contact_kind(row)
                item = {
                    "run": run,
                    "tick": _safe_int(row.get("tick", 0)),
                    "timestamp_ms": row.get("timestamp_ms", ""),
                    "family": row.get("symbol_family", "-"),
                    "action": action,
                    "raw_action": raw_action,
                    "kind": kind,
                    "reward": round(_safe_float(row.get("reward", 0.0)), 6),
                    "best_action_training": row.get("best_action_training", "WAIT"),
                    "best_reward_training": round(_safe_float(row.get("best_reward_training", 0.0)), 6),
                    "phase_active": _safe_int(row.get("phase_active", 0)),
                    "phase_age": _safe_int(row.get("phase_age", 0)),
                    "episode_relation": row.get("episode_relation", "-"),
                    "episode_binding_pressure": round(_safe_float(row.get("episode_binding_pressure", 0.0)), 6),
                    "episode_release_pressure": round(_safe_float(row.get("episode_release_pressure", 0.0)), 6),
                    "trade_readiness": round(_safe_float(row.get("trade_readiness", 0.0)), 6),
                    "mature_transfer": round(_safe_float(row.get("mature_transfer", 0.0)), 6),
                }
                rows.append(item)
                record = summary.setdefault(
                    kind,
                    {
                        "kind": kind,
                        "count": 0,
                        "executed": 0,
                        "reward_sum": 0.0,
                        "max_reward": -999.0,
                    },
                )
                record["count"] += 1
                if action in TRADE_ACTIONS:
                    record["executed"] += 1
                record["reward_sum"] += item["reward"]
                record["max_reward"] = max(record["max_reward"], item["reward"])
    max_positive_reward = max((row["reward"] for row in rows if row["action"] in TRADE_ACTIONS and row["reward"] > 0.0), default=0.0)
    for row in rows:
        if row["action"] in TRADE_ACTIONS and max_positive_reward > 0.0:
            row["relative_positive_reward"] = round(max(0.0, row["reward"]) / max_positive_reward, 6)
        else:
            row["relative_positive_reward"] = 0.0
    summary_rows = []
    for record in summary.values():
        count = max(1, _safe_int(record["count"]))
        summary_rows.append(
            {
                "kind": record["kind"],
                "count": record["count"],
                "executed": record["executed"],
                "reward_sum": round(record["reward_sum"], 6),
                "avg_reward": round(record["reward_sum"] / count, 6),
                "max_reward": round(record["max_reward"], 6),
            }
        )
    summary_rows.sort(key=lambda item: (item["executed"], item["count"], item["max_reward"]), reverse=True)
    rows.sort(key=lambda item: (item["run"], item["tick"]))
    return rows, summary_rows


def write_outputs(rows: list[dict], summary_rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_episode_contacts.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "dio_mini_episode_contact_summary.json").write_text(
        json.dumps(summary_rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    if rows:
        with (output_dir / "dio_mini_episode_contacts.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    if summary_rows:
        with (output_dir / "dio_mini_episode_contact_summary.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(summary_rows[0].keys()))
            writer.writeheader()
            writer.writerows(summary_rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze DIO mini episode contacts")
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    rows, summary_rows = analyze(Path(args.debug_root))
    write_outputs(rows, summary_rows, Path(args.output_dir))
    for row in summary_rows:
        print(
            f"{row['kind']}: count={row['count']} executed={row['executed']} "
            f"avg_reward={row['avg_reward']:.4f} max_reward={row['max_reward']:.4f}"
        )


if __name__ == "__main__":
    main()
