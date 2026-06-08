"""Analyze DIO mini memory growth without changing memory.

This report is intentionally passive. It helps decide whether memory growth is
real episodic development or only accumulation of weak traces.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ACTION_NAMES = ("WAIT", "LONG", "SHORT")
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


def _read_memory(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def _action_state(record: dict, action: str) -> dict:
    return dict(dict(record.get("actions", {}) or {}).get(action, {}) or {})


def _observation_state(record: dict, action: str) -> dict:
    return dict(dict(record.get("observations", {}) or {}).get(action, {}) or {})


def _family_metrics(family: str, record: dict, symbols_by_family: dict[str, int]) -> dict:
    action_count = 0
    trade_action_count = 0
    observation_count = 0
    trade_observation_count = 0
    reward_sum = 0.0
    observation_reward_sum = 0.0
    trust_sum = 0.0
    caution_sum = 0.0
    max_trust = 0.0
    max_caution = 0.0
    for action in ACTION_NAMES:
        state = _action_state(record, action)
        count = _safe_int(state.get("count", 0))
        reward = _safe_float(state.get("reward_sum", 0.0))
        trust = _safe_float(state.get("trust", 0.0))
        caution = _safe_float(state.get("caution", 0.0))
        action_count += count
        reward_sum += reward
        trust_sum += trust
        caution_sum += caution
        max_trust = max(max_trust, trust)
        max_caution = max(max_caution, caution)
        if action in TRADE_ACTIONS:
            trade_action_count += count
        obs = _observation_state(record, action)
        obs_count = _safe_int(obs.get("count", 0))
        observation_count += obs_count
        observation_reward_sum += _safe_float(obs.get("reward_sum", 0.0))
        if action in TRADE_ACTIONS:
            trade_observation_count += obs_count
    net_pressure = trust_sum - caution_sum
    symbol_count = int(symbols_by_family.get(family, 0))
    classification = _classify_family(
        count=_safe_int(record.get("count", 0)),
        trade_action_count=trade_action_count,
        trade_observation_count=trade_observation_count,
        reward_sum=reward_sum,
        observation_reward_sum=observation_reward_sum,
        max_trust=max_trust,
        max_caution=max_caution,
        symbol_count=symbol_count,
    )
    return {
        "family": family,
        "classification": classification,
        "count": _safe_int(record.get("count", 0)),
        "symbol_count": symbol_count,
        "action_count": action_count,
        "trade_action_count": trade_action_count,
        "observation_count": observation_count,
        "trade_observation_count": trade_observation_count,
        "reward_sum": round(reward_sum, 6),
        "observation_reward_sum": round(observation_reward_sum, 6),
        "trust_sum": round(trust_sum, 6),
        "caution_sum": round(caution_sum, 6),
        "net_pressure": round(net_pressure, 6),
        "max_trust": round(max_trust, 6),
        "max_caution": round(max_caution, 6),
    }


def _classify_family(
    *,
    count: int,
    trade_action_count: int,
    trade_observation_count: int,
    reward_sum: float,
    observation_reward_sum: float,
    max_trust: float,
    max_caution: float,
    symbol_count: int,
) -> str:
    if trade_action_count > 0 and reward_sum > 0.0 and max_trust >= max_caution:
        return "executed_positive_trace"
    if trade_action_count > 0 and reward_sum < 0.0:
        return "executed_burden_trace"
    if trade_action_count > 0:
        return "executed_mixed_trace"
    if trade_observation_count > 0 and observation_reward_sum > 0.0:
        return "observed_positive_trace"
    if trade_observation_count > 0 and observation_reward_sum < 0.0:
        return "observed_burden_trace"
    if symbol_count > 1 or count > 1:
        return "repeated_quiet_trace"
    return "single_quiet_trace"


def _symbols_by_family(memory: dict) -> dict[str, int]:
    output: dict[str, int] = {}
    for symbol, record in dict(memory.get("symbols", {}) or {}).items():
        if not isinstance(record, dict):
            continue
        family = str(record.get("syntax_family", "") or str(symbol)[:8])
        output[family] = output.get(family, 0) + 1
    return output


def analyze_memory(memory_path: Path, previous_path: Path | None = None) -> tuple[list[dict], dict]:
    memory = _read_memory(memory_path)
    previous = _read_memory(previous_path) if previous_path else {}
    families = dict(memory.get("families", {}) or {})
    previous_families = set(dict(previous.get("families", {}) or {}).keys())
    symbol_family_counts = _symbols_by_family(memory)
    rows = []
    for family, record in families.items():
        if not isinstance(record, dict):
            continue
        row = _family_metrics(str(family), record, symbol_family_counts)
        row["new_since_previous"] = bool(previous_families and family not in previous_families)
        rows.append(row)
    rows.sort(
        key=lambda item: (
            item["classification"] == "executed_positive_trace",
            item["reward_sum"],
            item["trade_action_count"],
            item["observation_count"],
            item["count"],
        ),
        reverse=True,
    )
    class_counts: dict[str, int] = {}
    class_reward: dict[str, float] = {}
    new_class_counts: dict[str, int] = {}
    for row in rows:
        cls = str(row.get("classification", "-") or "-")
        class_counts[cls] = class_counts.get(cls, 0) + 1
        class_reward[cls] = class_reward.get(cls, 0.0) + _safe_float(row.get("reward_sum", 0.0))
        if row.get("new_since_previous"):
            new_class_counts[cls] = new_class_counts.get(cls, 0) + 1
    overview = {
        "memory": str(memory_path),
        "previous_memory": str(previous_path) if previous_path else "",
        "bytes": memory_path.stat().st_size if memory_path.exists() else 0,
        "symbols": len(memory.get("symbols", {}) or {}),
        "families": len(memory.get("families", {}) or {}),
        "relations": len(memory.get("relations", {}) or {}),
        "sensor_relations": len(memory.get("sensor_relations", {}) or {}),
        "new_families_since_previous": sum(1 for row in rows if row.get("new_since_previous")),
        "class_counts": class_counts,
        "new_class_counts": new_class_counts,
        "class_reward_sum": {key: round(value, 6) for key, value in sorted(class_reward.items())},
        "top_executed_positive": [
            row["family"] for row in rows if row["classification"] == "executed_positive_trace"
        ][:10],
        "top_observed_positive": [
            row["family"] for row in rows if row["classification"] == "observed_positive_trace"
        ][:10],
        "burden_traces": [
            row["family"]
            for row in rows
            if row["classification"] in ("executed_burden_trace", "observed_burden_trace")
        ][:10],
        "compact_candidate_count": sum(1 for row in rows if row["classification"] == "single_quiet_trace"),
    }
    return rows, overview


def write_outputs(rows: list[dict], overview: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_memory_growth.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "dio_mini_memory_growth_overview.json").write_text(
        json.dumps(overview, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    if rows:
        with (output_dir / "dio_mini_memory_growth.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    lines = ["# DIO Mini Memory Growth", ""]
    lines.append("## Overview")
    lines.append(f"- symbols: {overview.get('symbols', 0)}")
    lines.append(f"- families: {overview.get('families', 0)}")
    lines.append(f"- relations: {overview.get('relations', 0)}")
    lines.append(f"- sensor_relations: {overview.get('sensor_relations', 0)}")
    lines.append(f"- new_families_since_previous: {overview.get('new_families_since_previous', 0)}")
    lines.append(f"- compact_candidate_count: {overview.get('compact_candidate_count', 0)}")
    lines.append("")
    lines.append("## Classes")
    for key, value in sorted(dict(overview.get("class_counts", {}) or {}).items()):
        reward = dict(overview.get("class_reward_sum", {}) or {}).get(key, 0.0)
        new_count = dict(overview.get("new_class_counts", {}) or {}).get(key, 0)
        lines.append(f"- {key}: {value}, reward {reward}, new {new_count}")
    lines.append("")
    lines.append("## Top Executed Positive")
    for family in overview.get("top_executed_positive", []) or []:
        lines.append(f"- {family}")
    lines.append("")
    lines.append("## Top Observed Positive")
    for family in overview.get("top_observed_positive", []) or []:
        lines.append(f"- {family}")
    lines.append("")
    lines.append("## Burden Traces")
    for family in overview.get("burden_traces", []) or []:
        lines.append(f"- {family}")
    lines.append("")
    (output_dir / "dio_mini_memory_growth.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze DIO mini memory growth")
    parser.add_argument("--memory", required=True)
    parser.add_argument("--previous-memory", default="")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    previous = Path(args.previous_memory) if args.previous_memory else None
    rows, overview = analyze_memory(Path(args.memory), previous)
    write_outputs(rows, overview, Path(args.output_dir))
    print(json.dumps(overview, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
