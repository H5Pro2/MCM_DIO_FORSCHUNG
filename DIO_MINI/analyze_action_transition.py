"""Analyze passive transition from observation to action in DIO mini runs.

The report does not change memory or motorics. It reads episodes.csv files and
summarizes how families move from observation pressure into executed contact.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


TRADE_ACTIONS = ("LONG", "SHORT")
SENSOR_FIELDS = (
    "sehen_form_flow",
    "sehen_form_stability",
    "sehen_form_change",
    "hoeren_energy_tone",
    "hoeren_energy_shift",
    "fuehlen_mcm_coherence",
    "fuehlen_mcm_tension",
    "fuehlen_mcm_asymmetry",
)
PRESSURE_FIELDS = (
    "trade_readiness",
    "associative_trade",
    "observation_trade_signal",
    "observation_trade_readiness",
    "maturity_gap",
    "mature_transfer",
    "observation_learning_pressure",
)


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
    return sorted(debug_root.glob("dio_mini_lauf_*/episodes.csv"))


def _empty_family(family: str) -> dict:
    return {
        "family": family,
        "runs": set(),
        "rows": 0,
        "executed_rows": 0,
        "observed_rows": 0,
        "raw_trade_rows": 0,
        "first_observed_run": 0,
        "first_observed_tick": 0,
        "first_executed_run": 0,
        "first_executed_tick": 0,
        "reward_sum": 0.0,
        "best_reward_sum": 0.0,
        "executed_reward_sum": 0.0,
        "observed_best_reward_sum": 0.0,
        "observation_learning_sum": 0.0,
        "sensor_observed": {field: 0.0 for field in SENSOR_FIELDS},
        "sensor_executed": {field: 0.0 for field in SENSOR_FIELDS},
        "pressure_observed": {field: 0.0 for field in PRESSURE_FIELDS},
        "pressure_executed": {field: 0.0 for field in PRESSURE_FIELDS},
    }


def _classify(record: dict) -> str:
    executed = _safe_int(record.get("executed_rows", 0))
    observed = _safe_int(record.get("observed_rows", 0))
    reward = _safe_float(record.get("reward_sum", 0.0))
    first_obs = _safe_int(record.get("first_observed_run", 0))
    first_exec = _safe_int(record.get("first_executed_run", 0))
    if executed > 0 and observed > 0 and first_obs and first_exec and first_obs <= first_exec:
        if reward > 0.0:
            return "observation_to_positive_action"
        return "observation_to_burdened_action"
    if executed > 0 and reward > 0.0:
        return "direct_positive_action"
    if executed > 0 and reward < 0.0:
        return "direct_burdened_action"
    if observed > 0:
        return "held_observation"
    return "quiet_family"


def analyze(debug_root: Path) -> tuple[list[dict], dict]:
    families: dict[str, dict] = {}
    for path in _episode_paths(debug_root):
        run = _safe_int(path.parent.name.rsplit("_", 1)[-1], 0)
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                family = str(row.get("symbol_family", "-") or "-")
                record = families.setdefault(family, _empty_family(family))
                action = str(row.get("action", "WAIT") or "WAIT").upper()
                raw_action = str(row.get("raw_action", "WAIT") or "WAIT").upper()
                best_action = str(row.get("best_action_training", "WAIT") or "WAIT").upper()
                tick = _safe_int(row.get("tick", 0))
                executed = action in TRADE_ACTIONS
                observed = action == "WAIT" and best_action in TRADE_ACTIONS
                raw_trade = raw_action in TRADE_ACTIONS
                record["runs"].add(run)
                record["rows"] += 1
                record["reward_sum"] += _safe_float(row.get("reward", 0.0))
                record["best_reward_sum"] += _safe_float(row.get("best_reward_training", 0.0))
                if raw_trade:
                    record["raw_trade_rows"] += 1
                if observed:
                    record["observed_rows"] += 1
                    record["observed_best_reward_sum"] += _safe_float(row.get("best_reward_training", 0.0))
                    if not record["first_observed_run"]:
                        record["first_observed_run"] = run
                        record["first_observed_tick"] = tick
                    for field in SENSOR_FIELDS:
                        record["sensor_observed"][field] += _safe_float(row.get(field, 0.0))
                    for field in PRESSURE_FIELDS:
                        record["pressure_observed"][field] += _safe_float(row.get(field, 0.0))
                    record["observation_learning_sum"] += _safe_float(row.get("observation_learning_pressure", 0.0))
                if executed:
                    record["executed_rows"] += 1
                    record["executed_reward_sum"] += _safe_float(row.get("reward", 0.0))
                    if not record["first_executed_run"]:
                        record["first_executed_run"] = run
                        record["first_executed_tick"] = tick
                    for field in SENSOR_FIELDS:
                        record["sensor_executed"][field] += _safe_float(row.get(field, 0.0))
                    for field in PRESSURE_FIELDS:
                        record["pressure_executed"][field] += _safe_float(row.get(field, 0.0))

    rows = []
    overview_counts: dict[str, int] = {}
    overview_reward: dict[str, float] = {}
    for record in families.values():
        observed = max(1, _safe_int(record.get("observed_rows", 0)))
        executed = max(1, _safe_int(record.get("executed_rows", 0)))
        classification = _classify(record)
        overview_counts[classification] = overview_counts.get(classification, 0) + 1
        overview_reward[classification] = overview_reward.get(classification, 0.0) + _safe_float(record.get("reward_sum", 0.0))
        row = {
            "family": record["family"],
            "classification": classification,
            "run_count": len(record["runs"]),
            "rows": record["rows"],
            "executed_rows": record["executed_rows"],
            "observed_rows": record["observed_rows"],
            "raw_trade_rows": record["raw_trade_rows"],
            "first_observed_run": record["first_observed_run"],
            "first_observed_tick": record["first_observed_tick"],
            "first_executed_run": record["first_executed_run"],
            "first_executed_tick": record["first_executed_tick"],
            "reward_sum": round(record["reward_sum"], 6),
            "executed_reward_sum": round(record["executed_reward_sum"], 6),
            "observed_best_reward_sum": round(record["observed_best_reward_sum"], 6),
            "avg_observation_learning_pressure": round(record["observation_learning_sum"] / observed, 6),
        }
        for field in SENSOR_FIELDS:
            row[f"observed_{field}"] = round(record["sensor_observed"][field] / observed, 6)
            row[f"executed_{field}"] = round(record["sensor_executed"][field] / executed, 6)
        for field in PRESSURE_FIELDS:
            row[f"observed_{field}"] = round(record["pressure_observed"][field] / observed, 6)
            row[f"executed_{field}"] = round(record["pressure_executed"][field] / executed, 6)
        rows.append(row)
    rows.sort(
        key=lambda item: (
            item["classification"] == "observation_to_positive_action",
            item["classification"] == "direct_positive_action",
            item["reward_sum"],
            item["executed_rows"],
            item["observed_rows"],
        ),
        reverse=True,
    )
    overview = {
        "debug_root": str(debug_root),
        "class_counts": overview_counts,
        "class_reward_sum": {key: round(value, 6) for key, value in sorted(overview_reward.items())},
        "top_observation_to_action": [
            row["family"] for row in rows if row["classification"] == "observation_to_positive_action"
        ][:8],
        "top_direct_action": [row["family"] for row in rows if row["classification"] == "direct_positive_action"][:8],
        "held_observation": [row["family"] for row in rows if row["classification"] == "held_observation"][:8],
    }
    return rows, overview


def write_outputs(rows: list[dict], overview: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_action_transition.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "dio_mini_action_transition_overview.json").write_text(
        json.dumps(overview, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    if rows:
        with (output_dir / "dio_mini_action_transition.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    lines = ["# DIO Mini Action Transition", ""]
    lines.append("## Classes")
    for key, value in sorted(dict(overview.get("class_counts", {}) or {}).items()):
        reward = dict(overview.get("class_reward_sum", {}) or {}).get(key, 0.0)
        lines.append(f"- {key}: {value}, reward {reward}")
    lines.append("")
    lines.append("## Observation To Action")
    for family in overview.get("top_observation_to_action", []) or []:
        lines.append(f"- {family}")
    lines.append("")
    lines.append("## Direct Action")
    for family in overview.get("top_direct_action", []) or []:
        lines.append(f"- {family}")
    lines.append("")
    lines.append("## Held Observation")
    for family in overview.get("held_observation", []) or []:
        lines.append(f"- {family}")
    lines.append("")
    (output_dir / "dio_mini_action_transition.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze DIO mini action transition")
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    rows, overview = analyze(Path(args.debug_root))
    write_outputs(rows, overview, Path(args.output_dir))
    print(json.dumps(overview, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
