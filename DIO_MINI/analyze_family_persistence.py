"""Track selected DIO mini families across a debug phase."""

from __future__ import annotations

import argparse
import csv
import json
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


def analyze(debug_root: Path, families: list[str]) -> list[dict]:
    wanted = {str(family).strip() for family in families if str(family).strip()}
    records: dict[tuple[str, int], dict] = {}
    for path in collect_episode_paths(debug_root):
        run = _safe_int(path.parent.name.rsplit("_", 1)[-1], 0)
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                family = str(row.get("symbol_family", "-") or "-")
                if wanted and family not in wanted:
                    continue
                action = str(row.get("action", "WAIT") or "WAIT").upper()
                raw_action = str(row.get("raw_action", "WAIT") or "WAIT").upper()
                record = records.setdefault(
                    (family, run),
                    {
                        "family": family,
                        "run": run,
                        "rows": 0,
                        "executed": 0,
                        "raw_trade_pressure": 0,
                        "held_same_episode": 0,
                        "observed_potential": 0,
                        "reward_sum": 0.0,
                        "max_trade_readiness": 0.0,
                        "max_mature_transfer": 0.0,
                    },
                )
                record["rows"] += 1
                if action in ("LONG", "SHORT"):
                    record["executed"] += 1
                if raw_action in ("LONG", "SHORT"):
                    record["raw_trade_pressure"] += 1
                if _safe_int(row.get("phase_active", 0)) > 0:
                    record["held_same_episode"] += 1
                if action == "WAIT" and str(row.get("best_action_training", "WAIT") or "WAIT").upper() in ("LONG", "SHORT"):
                    record["observed_potential"] += 1
                record["reward_sum"] += _safe_float(row.get("reward", 0.0))
                record["max_trade_readiness"] = max(record["max_trade_readiness"], _safe_float(row.get("trade_readiness", 0.0)))
                record["max_mature_transfer"] = max(record["max_mature_transfer"], _safe_float(row.get("mature_transfer", 0.0)))
    rows = []
    for record in records.values():
        rows.append(
            {
                "family": record["family"],
                "run": record["run"],
                "rows": record["rows"],
                "executed": record["executed"],
                "raw_trade_pressure": record["raw_trade_pressure"],
                "held_same_episode": record["held_same_episode"],
                "observed_potential": record["observed_potential"],
                "reward_sum": round(record["reward_sum"], 6),
                "max_trade_readiness": round(record["max_trade_readiness"], 6),
                "max_mature_transfer": round(record["max_mature_transfer"], 6),
            }
        )
    rows.sort(key=lambda item: (item["family"], item["run"]))
    return rows


def summarize(rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = {}
    for row in rows:
        grouped.setdefault(str(row.get("family", "-") or "-"), []).append(row)
    output = []
    for family, items in grouped.items():
        items = sorted(items, key=lambda item: _safe_int(item.get("run", 0)))
        first = items[0]
        last = items[-1]
        executed_runs = sum(1 for item in items if _safe_int(item.get("executed", 0)) > 0)
        observed_runs = sum(1 for item in items if _safe_int(item.get("observed_potential", 0)) > 0)
        held_runs = sum(1 for item in items if _safe_int(item.get("held_same_episode", 0)) > 0)
        raw_runs = sum(1 for item in items if _safe_int(item.get("raw_trade_pressure", 0)) > 0)
        transition = "stable_observation"
        if _safe_int(first.get("executed", 0)) == 0 and _safe_int(last.get("executed", 0)) > 0:
            transition = "observation_to_execution"
        elif _safe_int(first.get("executed", 0)) > 0 and _safe_int(last.get("executed", 0)) == 0:
            transition = "execution_to_nonexecution"
        elif executed_runs == len(items):
            transition = "persistent_execution"
        elif executed_runs > 0 and observed_runs > 0:
            transition = "mixed_observation_execution"
        elif raw_runs > 0 and held_runs > 0:
            transition = "raw_pressure_held"
        output.append(
            {
                "family": family,
                "run_count": len(items),
                "first_run": first.get("run", 0),
                "last_run": last.get("run", 0),
                "executed_runs": executed_runs,
                "observed_runs": observed_runs,
                "held_runs": held_runs,
                "raw_runs": raw_runs,
                "reward_sum": round(sum(_safe_float(item.get("reward_sum", 0.0)) for item in items), 6),
                "max_trade_readiness": round(max(_safe_float(item.get("max_trade_readiness", 0.0)) for item in items), 6),
                "max_mature_transfer": round(max(_safe_float(item.get("max_mature_transfer", 0.0)) for item in items), 6),
                "transition": transition,
            }
        )
    output.sort(
        key=lambda item: (
            item["transition"] == "observation_to_execution",
            item["executed_runs"],
            item["observed_runs"],
            item["reward_sum"],
        ),
        reverse=True,
    )
    return output


def write_outputs(rows: list[dict], summary_rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_family_persistence.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "dio_mini_family_persistence_summary.json").write_text(
        json.dumps(summary_rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    if rows:
        with (output_dir / "dio_mini_family_persistence.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    if summary_rows:
        with (output_dir / "dio_mini_family_persistence_summary.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(summary_rows[0].keys()))
            writer.writeheader()
            writer.writerows(summary_rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze selected DIO mini family persistence")
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--family", action="append", default=[])
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    rows = analyze(Path(args.debug_root), args.family)
    summary_rows = summarize(rows)
    write_outputs(rows, summary_rows, Path(args.output_dir))
    for row in summary_rows[:16]:
        print(
            f"family={row['family']} transition={row['transition']} runs={row['run_count']} "
            f"executed_runs={row['executed_runs']} observed_runs={row['observed_runs']} reward={row['reward_sum']:.4f}"
        )


if __name__ == "__main__":
    main()
