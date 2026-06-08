"""Report timing from DIO_MINI observation to confirmed execution."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.report_episode_binding import _binding_state, _float, _iter_rows


def _int(value: object, default: int = 0) -> int:
    try:
        return int(float(value))
    except Exception:
        return default


def _event_order(row: dict) -> tuple[int, int]:
    return (_int(row.get("run", 0)), _int(row.get("tick", 0)))


def _collect(debug_root: Path) -> list[dict]:
    events_by_family: dict[str, list[dict]] = {}
    for row in _iter_rows(debug_root):
        family = str(row.get("symbol_family", "") or "-")
        state_name = _binding_state(row)
        if state_name not in ("observed_not_bound", "executed_aligned"):
            continue
        event = {
            "run": str(row.get("run", "")),
            "tick": str(row.get("tick", "")),
            "order": _event_order(row),
            "state": state_name,
            "action": str(row.get("action", "WAIT") or "WAIT").upper(),
            "best_action_training": str(row.get("best_action_training", "WAIT") or "WAIT").upper(),
            "reward": _float(row, "reward"),
            "best_reward_training": _float(row, "best_reward_training"),
        }
        events_by_family.setdefault(family, []).append(event)

    rows: list[dict] = []
    for family, events in events_by_family.items():
        events.sort(key=lambda item: item["order"])
        observations = [item for item in events if item["state"] == "observed_not_bound"]
        executions = [item for item in events if item["state"] == "executed_aligned"]
        if not observations:
            continue
        first_observation = observations[0]
        later_executions = [item for item in executions if item["order"] > first_observation["order"]]
        if later_executions:
            first_execution = later_executions[0]
            maturation_state = "observation_matured_to_execution"
            run_lag = int(first_execution["order"][0]) - int(first_observation["order"][0])
            tick_lag = int(first_execution["order"][1]) - int(first_observation["order"][1])
        else:
            first_execution = None
            maturation_state = "observation_not_yet_executed"
            run_lag = ""
            tick_lag = ""
        rows.append(
            {
                "symbol_family": family,
                "maturation_state": maturation_state,
                "observation_count": len(observations),
                "execution_count": len(executions),
                "first_observation_run": first_observation["run"],
                "first_observation_tick": first_observation["tick"],
                "first_observation_best_action": first_observation["best_action_training"],
                "first_observation_best_reward": round(float(first_observation["best_reward_training"]), 6),
                "first_execution_run": first_execution["run"] if first_execution else "",
                "first_execution_tick": first_execution["tick"] if first_execution else "",
                "first_execution_action": first_execution["action"] if first_execution else "",
                "first_execution_reward": round(float(first_execution["reward"]), 6) if first_execution else 0.0,
                "run_lag": run_lag,
                "tick_lag": tick_lag,
                "observation_reward_potential_sum": round(
                    sum(float(item["best_reward_training"]) for item in observations),
                    6,
                ),
                "execution_reward_sum": round(sum(float(item["reward"]) for item in executions), 6),
            }
        )
    rows.sort(
        key=lambda item: (
            item["maturation_state"] != "observation_matured_to_execution",
            -float(item["observation_reward_potential_sum"]),
            item["symbol_family"],
        )
    )
    return rows


def _write(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "dio_mini_observation_maturation_timing.csv"
    json_path = output_dir / "dio_mini_observation_maturation_timing.json"
    md_path = output_dir / "dio_mini_observation_maturation_timing.md"
    fields = [
        "symbol_family",
        "maturation_state",
        "observation_count",
        "execution_count",
        "first_observation_run",
        "first_observation_tick",
        "first_observation_best_action",
        "first_observation_best_reward",
        "first_execution_run",
        "first_execution_tick",
        "first_execution_action",
        "first_execution_reward",
        "run_lag",
        "tick_lag",
        "observation_reward_potential_sum",
        "execution_reward_sum",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    matured = [row for row in rows if row["maturation_state"] == "observation_matured_to_execution"]
    open_rows = [row for row in rows if row["maturation_state"] != "observation_matured_to_execution"]
    lines = [
        "# DIO Mini Observation Maturation Timing",
        "",
        f"- matured: {len(matured)}",
        f"- open_observation: {len(open_rows)}",
        "",
    ]
    for row in rows[:20]:
        lines.extend(
            [
                f"## {row['symbol_family']}",
                f"- state: {row['maturation_state']}",
                f"- observation_count: {row['observation_count']}",
                f"- execution_count: {row['execution_count']}",
                f"- first_observation: run {row['first_observation_run']} tick {row['first_observation_tick']}",
                f"- first_execution: run {row['first_execution_run'] or '-'} tick {row['first_execution_tick'] or '-'}",
                f"- run_lag: {row['run_lag'] if row['run_lag'] != '' else '-'}",
                f"- tick_lag: {row['tick_lag'] if row['tick_lag'] != '' else '-'}",
                f"- observation_reward_potential_sum: {float(row['observation_reward_potential_sum']):.6f}",
                f"- execution_reward_sum: {float(row['execution_reward_sum']):.6f}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    rows = _collect(Path(args.debug_root))
    _write(rows, Path(args.output_dir))
    matured = [row for row in rows if row["maturation_state"] == "observation_matured_to_execution"]
    print(f"families={len(rows)} matured={len(matured)} open={len(rows) - len(matured)}")
    for row in rows[:10]:
        print(
            f"{row['symbol_family']} {row['maturation_state']} "
            f"obs={row['observation_count']} exec={row['execution_count']} "
            f"lag={row['run_lag']}/{row['tick_lag']}"
        )


if __name__ == "__main__":
    main()
