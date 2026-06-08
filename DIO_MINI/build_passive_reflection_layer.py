"""Build passive DIO_MINI reflection seeds from matured and reconfirmed families."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.report_episode_binding import _binding_state, _float, _iter_rows


def _read_matured(path: Path) -> dict[str, dict]:
    items: dict[str, dict] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            family = str(row.get("symbol_family", "") or "")
            if not family:
                continue
            if str(row.get("maturation_state", "") or "") != "observation_matured_to_execution":
                continue
            items[family] = dict(row)
    return items


def _read_followup(debug_root: Path) -> dict[str, dict]:
    families: dict[str, dict] = {}
    for row in _iter_rows(debug_root):
        family = str(row.get("symbol_family", "") or "")
        if not family:
            continue
        state_name = _binding_state(row)
        item = families.setdefault(
            family,
            {
                "followup_seen_count": 0,
                "followup_executed_aligned_count": 0,
                "followup_executed_reward": 0.0,
                "followup_observed_count": 0,
                "followup_observed_potential": 0.0,
                "followup_overheld_count": 0,
                "followup_overheld_potential": 0.0,
                "followup_actions": {},
            },
        )
        item["followup_seen_count"] += 1
        action = str(row.get("action", "WAIT") or "WAIT").upper()
        item["followup_actions"][action] = int(item["followup_actions"].get(action, 0) or 0) + 1
        if state_name == "executed_aligned":
            item["followup_executed_aligned_count"] += 1
            item["followup_executed_reward"] += _float(row, "reward")
        elif state_name == "observed_not_bound":
            item["followup_observed_count"] += 1
            item["followup_observed_potential"] += _float(row, "best_reward_training")
        elif state_name == "held_useful_impulse":
            item["followup_overheld_count"] += 1
            item["followup_overheld_potential"] += _float(row, "best_reward_training")
    return families


def _reflection_state(followup: dict) -> str:
    if int(followup.get("followup_executed_aligned_count", 0) or 0) > 0 and float(followup.get("followup_executed_reward", 0.0) or 0.0) > 0.0:
        return "reflection_seed_reconfirmed"
    if int(followup.get("followup_overheld_count", 0) or 0) > 0:
        return "reflection_seed_overheld"
    if int(followup.get("followup_observed_count", 0) or 0) > 0:
        return "reflection_seed_observed_again"
    return "reflection_seed_not_seen"


def _collect(maturation_path: Path, followup_debug_root: Path) -> list[dict]:
    matured = _read_matured(maturation_path)
    followup = _read_followup(followup_debug_root)
    rows = []
    for family, maturity in matured.items():
        follow = followup.get(family, {})
        actions = dict(follow.get("followup_actions", {}) or {})
        rows.append(
            {
                "symbol_family": family,
                "reflection_state": _reflection_state(follow),
                "prior_observation_count": int(float(maturity.get("observation_count", 0) or 0)),
                "prior_execution_count": int(float(maturity.get("execution_count", 0) or 0)),
                "prior_first_observation_run": maturity.get("first_observation_run", ""),
                "prior_first_observation_tick": maturity.get("first_observation_tick", ""),
                "prior_first_execution_run": maturity.get("first_execution_run", ""),
                "prior_first_execution_tick": maturity.get("first_execution_tick", ""),
                "prior_observation_reward_potential_sum": round(float(maturity.get("observation_reward_potential_sum", 0.0) or 0.0), 6),
                "prior_execution_reward_sum": round(float(maturity.get("execution_reward_sum", 0.0) or 0.0), 6),
                "followup_seen_count": int(follow.get("followup_seen_count", 0) or 0),
                "followup_executed_aligned_count": int(follow.get("followup_executed_aligned_count", 0) or 0),
                "followup_executed_reward": round(float(follow.get("followup_executed_reward", 0.0) or 0.0), 6),
                "followup_observed_count": int(follow.get("followup_observed_count", 0) or 0),
                "followup_observed_potential": round(float(follow.get("followup_observed_potential", 0.0) or 0.0), 6),
                "followup_overheld_count": int(follow.get("followup_overheld_count", 0) or 0),
                "followup_overheld_potential": round(float(follow.get("followup_overheld_potential", 0.0) or 0.0), 6),
                "followup_actions": ",".join(f"{key}:{actions[key]}" for key in sorted(actions)),
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
    csv_path = output_dir / "dio_mini_passive_reflection_layer.csv"
    json_path = output_dir / "dio_mini_passive_reflection_layer.json"
    md_path = output_dir / "dio_mini_passive_reflection_layer.md"
    fields = [
        "symbol_family",
        "reflection_state",
        "prior_observation_count",
        "prior_execution_count",
        "prior_first_observation_run",
        "prior_first_observation_tick",
        "prior_first_execution_run",
        "prior_first_execution_tick",
        "prior_observation_reward_potential_sum",
        "prior_execution_reward_sum",
        "followup_seen_count",
        "followup_executed_aligned_count",
        "followup_executed_reward",
        "followup_observed_count",
        "followup_observed_potential",
        "followup_overheld_count",
        "followup_overheld_potential",
        "followup_actions",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Passive Reflection Layer", ""]
    if not rows:
        lines.append("Keine Reflexionskeime gefunden.")
    for row in rows:
        lines.extend(
            [
                f"## {row['symbol_family']}",
                f"- state: {row['reflection_state']}",
                f"- prior observation/execution: {row['prior_observation_count']} / {row['prior_execution_count']}",
                f"- prior reward: obs {float(row['prior_observation_reward_potential_sum']):.6f} / exec {float(row['prior_execution_reward_sum']):.6f}",
                f"- followup seen: {row['followup_seen_count']}",
                f"- followup executed: {row['followup_executed_aligned_count']} / {float(row['followup_executed_reward']):.6f}",
                f"- followup observed: {row['followup_observed_count']} / {float(row['followup_observed_potential']):.6f}",
                f"- followup overheld: {row['followup_overheld_count']} / {float(row['followup_overheld_potential']):.6f}",
                f"- followup actions: {row['followup_actions'] or '-'}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--maturation-report", required=True)
    parser.add_argument("--followup-debug-root", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    rows = _collect(Path(args.maturation_report), Path(args.followup_debug_root))
    _write(rows, Path(args.output_dir))
    print(f"reflection_seeds={len(rows)}")
    for row in rows:
        print(
            f"{row['symbol_family']} {row['reflection_state']} "
            f"followup_exec={row['followup_executed_aligned_count']}/"
            f"{row['followup_executed_reward']}"
        )


if __name__ == "__main__":
    main()
