"""Compare passive world carrying memory with later Mini-DIO run metrics.

The report is diagnostic only. It checks whether a stored world-level carrying
state aligns with later observation, readiness, outcome, and inner-state traces.
It does not write memory and does not influence action.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _int(value: object, default: int = 0) -> int:
    try:
        return int(float(value))
    except Exception:
        return default


def _run_number(path: Path) -> int:
    try:
        return int(path.name.rsplit("_", 1)[-1])
    except Exception:
        return 0


def parse_world(raw: str) -> tuple[str, Path]:
    if "=" not in str(raw):
        raise SystemExit(f"--world must be label=debug_root, got: {raw}")
    label, path = str(raw).split("=", 1)
    label = label.strip()
    if not label:
        raise SystemExit(f"Empty world label: {raw}")
    return label, Path(path.strip())


def load_memory(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def load_episode_rows(debug_root: Path) -> list[dict]:
    rows: list[dict] = []
    for path in sorted(debug_root.glob("dio_mini_lauf_*/episodes.csv"), key=lambda item: _run_number(item.parent)):
        run = _run_number(path.parent)
        with path.open("r", newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                item = dict(row)
                item["run"] = run
                rows.append(item)
    return rows


def summarize_rows(rows: list[dict]) -> dict:
    trades = 0
    tp = 0
    sl = 0
    reward = 0.0
    wait = 0
    sums = {
        "trade_readiness": 0.0,
        "observation_trade_readiness": 0.0,
        "observation_learning_pressure": 0.0,
        "mini_neuro_balance": 0.0,
        "mini_neuro_support": 0.0,
        "mini_neuro_load": 0.0,
        "mini_temporal_trust_support": 0.0,
        "mini_temporal_caution_support": 0.0,
        "reflection_context_carry": 0.0,
        "reflection_context_strain": 0.0,
        "reflection_context_alignment": 0.0,
    }
    maxes = {key: 0.0 for key in sums}
    tone_counts: dict[str, int] = {}
    reflection_context_counts: dict[str, int] = {}
    families: set[str] = set()
    for row in rows:
        action = str(row.get("action", "") or "").upper()
        if action in ("LONG", "SHORT"):
            trades += 1
        if action == "WAIT":
            wait += 1
        outcome = str(row.get("outcome_event", "") or "")
        tp += 1 if outcome == "TP" else 0
        sl += 1 if outcome == "SL" else 0
        reward += _float(row.get("reward"))
        families.add(str(row.get("symbol_family", "-") or "-"))
        tone = str(row.get("mini_neuro_dominant_tone", "-") or "-")
        tone_counts[tone] = _int(tone_counts.get(tone)) + 1
        reflection_context = str(row.get("reflection_context_state", "-") or "-")
        reflection_context_counts[reflection_context] = _int(reflection_context_counts.get(reflection_context)) + 1
        for field in sums:
            value = _float(row.get(field))
            sums[field] += value
            maxes[field] = max(maxes[field], value)
    count = max(1, len(rows))
    result = {
        "episodes": len(rows),
        "families": len(families),
        "trades": trades,
        "tp": tp,
        "sl": sl,
        "wait": wait,
        "reward_sum": round(reward, 6),
        "tone_counts": tone_counts,
        "reflection_context_counts": reflection_context_counts,
    }
    for field in sums:
        result[f"avg_{field}"] = round(sums[field] / count, 6)
        result[f"max_{field}"] = round(maxes[field], 6)
    return result


def build_world_row(label: str, debug_root: Path, memory: dict) -> dict:
    rows = load_episode_rows(debug_root)
    run_summary = summarize_rows(rows)
    world_memory = dict((memory.get("worlds", {}) or {}).get(label, {}) or {})
    last = dict(world_memory.get("last", {}) or {})
    return {
        "world": label,
        "debug_root": str(debug_root),
        "memory_observations": _int(world_memory.get("observations")),
        "memory_mean_avg_carry": round(_float(world_memory.get("mean_avg_carry")), 6),
        "memory_mean_avg_carried_cos": round(_float(world_memory.get("mean_avg_carried_cos")), 6),
        "memory_best_max_carry": round(_float(world_memory.get("best_max_carry")), 6),
        "memory_best_max_carried_cos": round(_float(world_memory.get("best_max_carried_cos")), 6),
        "memory_last_positive_carried_cos_family_count": _int(last.get("positive_carried_cos_family_count")),
        "memory_last_avg_readiness": round(_float(last.get("avg_readiness")), 6),
        **run_summary,
    }


def write_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = sorted(rows, key=lambda row: (row["memory_mean_avg_carry"], row["avg_trade_readiness"]), reverse=True)
    report = {"worlds": rows}
    (output_dir / "passive_world_reife_followup.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    csv_rows = []
    for row in rows:
        item = dict(row)
        item["tone_counts"] = json.dumps(item.get("tone_counts", {}), sort_keys=True)
        item["reflection_context_counts"] = json.dumps(item.get("reflection_context_counts", {}), sort_keys=True)
        csv_rows.append(item)
    if csv_rows:
        with (output_dir / "passive_world_reife_followup.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(csv_rows[0].keys()))
            writer.writeheader()
            writer.writerows(csv_rows)
    lines = ["MINI DIO PASSIVE WORLD REIFE FOLLOWUP", ""]
    for row in rows:
        lines.append(
            f"{row['world']}: memory_avg_carry={row['memory_mean_avg_carry']:.6f} "
            f"memory_avg_cos={row['memory_mean_avg_carried_cos']:.6f} "
            f"episodes={row['episodes']} trades={row['trades']} tp={row['tp']} sl={row['sl']} "
            f"reward={row['reward_sum']:.6f} avg_readiness={row['avg_trade_readiness']:.6f} "
            f"avg_obs_pressure={row['avg_observation_learning_pressure']:.6f} "
            f"avg_balance={row['avg_mini_neuro_balance']:.6f} "
            f"avg_reflection_carry={row['avg_reflection_context_carry']:.6f} "
            f"avg_reflection_strain={row['avg_reflection_context_strain']:.6f} "
            f"reflection_contexts={json.dumps(row.get('reflection_context_counts', {}), sort_keys=True)}"
        )
    (output_dir / "passive_world_reife_followup_summary.txt").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Mini-DIO passive world reife followup")
    parser.add_argument("--memory", required=True)
    parser.add_argument("--world", action="append", required=True, help="label=debug_root")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    memory = load_memory(Path(args.memory))
    rows = [build_world_row(label, debug_root, memory) for label, debug_root in (parse_world(item) for item in args.world)]
    write_outputs(rows, Path(args.output))
    print(json.dumps({"worlds": len(rows)}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
