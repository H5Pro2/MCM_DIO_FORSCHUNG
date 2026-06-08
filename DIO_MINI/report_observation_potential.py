"""Report observed but unexecuted DIO_MINI family potential."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.report_episode_binding import _binding_state, _float, _iter_rows


def _collect(debug_root: Path) -> list[dict]:
    families: dict[str, dict] = {}
    for row in _iter_rows(debug_root):
        binding_state = _binding_state(row)
        family = str(row.get("symbol_family", "") or "-")
        best_action = str(row.get("best_action_training", "WAIT") or "WAIT").upper()
        best_reward = _float(row, "best_reward_training")
        item = families.setdefault(
            family,
            {
                "symbol_family": family,
                "count": 0,
                "best_reward_sum": 0.0,
                "best_reward_max": 0.0,
                "long_count": 0,
                "short_count": 0,
                "executed_aligned_count": 0,
                "executed_aligned_reward": 0.0,
                "runs": set(),
                "ticks": [],
            },
        )
        if binding_state == "observed_not_bound":
            item["count"] += 1
            item["best_reward_sum"] += best_reward
            item["best_reward_max"] = max(float(item["best_reward_max"]), best_reward)
            if best_action == "LONG":
                item["long_count"] += 1
            elif best_action == "SHORT":
                item["short_count"] += 1
            item["runs"].add(str(row.get("run", "")))
            item["ticks"].append(str(row.get("tick", "")))
        elif binding_state == "executed_aligned":
            item["executed_aligned_count"] += 1
            item["executed_aligned_reward"] += _float(row, "reward")

    rows = []
    for item in families.values():
        count = int(item["count"] or 0)
        if count <= 0:
            continue
        long_count = int(item["long_count"] or 0)
        short_count = int(item["short_count"] or 0)
        if long_count > short_count:
            dominant = "LONG"
        elif short_count > long_count:
            dominant = "SHORT"
        else:
            dominant = "MIXED"
        rows.append(
            {
                "symbol_family": item["symbol_family"],
                "count": count,
                "best_reward_sum": round(float(item["best_reward_sum"]), 6),
                "best_reward_avg": round(float(item["best_reward_sum"]) / max(1, count), 6),
                "best_reward_max": round(float(item["best_reward_max"]), 6),
                "dominant_best_action": dominant,
                "long_count": long_count,
                "short_count": short_count,
                "executed_aligned_count": int(item["executed_aligned_count"] or 0),
                "executed_aligned_reward": round(float(item["executed_aligned_reward"]), 6),
                "observation_to_execution_state": _observation_to_execution_state(
                    count,
                    int(item["executed_aligned_count"] or 0),
                    float(item["executed_aligned_reward"] or 0.0),
                ),
                "runs": ",".join(sorted(name for name in item["runs"] if name)),
                "ticks": ",".join(item["ticks"][:20]),
            }
        )
    rows.sort(key=lambda item: (-float(item["best_reward_sum"]), -int(item["count"]), item["symbol_family"]))
    return rows


def _write(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "dio_mini_observation_potential.csv"
    json_path = output_dir / "dio_mini_observation_potential.json"
    md_path = output_dir / "dio_mini_observation_potential.md"
    fields = [
        "symbol_family",
        "count",
        "best_reward_sum",
        "best_reward_avg",
        "best_reward_max",
        "dominant_best_action",
        "long_count",
        "short_count",
        "executed_aligned_count",
        "executed_aligned_reward",
        "observation_to_execution_state",
        "runs",
        "ticks",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Observation Potential", ""]
    if not rows:
        lines.append("Kein Beobachtungspotential gefunden.")
    for row in rows[:20]:
        lines.extend(
            [
                f"## {row['symbol_family']}",
                f"- count: {row['count']}",
                f"- best_reward_sum: {float(row['best_reward_sum']):.6f}",
                f"- best_reward_avg: {float(row['best_reward_avg']):.6f}",
                f"- best_reward_max: {float(row['best_reward_max']):.6f}",
                f"- dominant_best_action: {row['dominant_best_action']}",
                f"- long_count: {row['long_count']}",
                f"- short_count: {row['short_count']}",
                f"- executed_aligned_count: {row['executed_aligned_count']}",
                f"- executed_aligned_reward: {float(row['executed_aligned_reward']):.6f}",
                f"- observation_to_execution_state: {row['observation_to_execution_state']}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def _observation_to_execution_state(observed_count: int, executed_count: int, executed_reward: float) -> str:
    if executed_count <= 0:
        return "observed_only"
    if executed_reward > 0.0:
        return "observation_later_confirmed"
    return "observation_later_executed_without_reward"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    rows = _collect(Path(args.debug_root))
    _write(rows, Path(args.output_dir))
    print(f"families={len(rows)}")
    for row in rows[:10]:
        print(
            f"{row['symbol_family']} count={row['count']} "
            f"best={row['best_reward_sum']} action={row['dominant_best_action']}"
        )


if __name__ == "__main__":
    main()
