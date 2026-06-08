"""Build a passive reflection map from DIO_MINI memory and a debug run."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.semantic_memory import SemanticMemory


def _safe_float(value: object) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


def _safe_int(value: object) -> int:
    try:
        return int(float(value))
    except Exception:
        return 0


def _iter_episode_rows(debug_root: Path) -> list[dict]:
    rows: list[dict] = []
    for path in sorted(debug_root.glob("dio_mini_lauf_*/episodes.csv")):
        run_id = path.parent.name.replace("dio_mini_lauf_", "")
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                item = dict(row)
                item["run"] = run_id
                rows.append(item)
    return rows


def _reflection_seeds(memory: SemanticMemory) -> list[dict]:
    seeds = memory.data.setdefault("reflection_seeds", {})
    if not isinstance(seeds, dict):
        return []
    rows = []
    for symbol, seed in seeds.items():
        seed = dict(seed or {})
        rows.append(
            {
                "reflection_symbol": str(seed.get("reflection_symbol", symbol) or symbol),
                "symbol_family": str(seed.get("symbol_family", "") or ""),
                "reflection_state": str(seed.get("reflection_state", "") or ""),
                "prior_observation_count": _safe_int(seed.get("prior_observation_count")),
                "prior_execution_count": _safe_int(seed.get("prior_execution_count")),
                "prior_execution_reward_sum": _safe_float(seed.get("prior_execution_reward_sum")),
                "followup_seen_count": _safe_int(seed.get("followup_seen_count")),
                "followup_executed_aligned_count": _safe_int(seed.get("followup_executed_aligned_count")),
                "followup_executed_reward": _safe_float(seed.get("followup_executed_reward")),
                "followup_observed_count": _safe_int(seed.get("followup_observed_count")),
                "followup_overheld_count": _safe_int(seed.get("followup_overheld_count")),
                "passive_only": _safe_int(seed.get("passive_only")),
            }
        )
    return rows


def _episode_summary(matches: list[dict]) -> dict:
    executed = [row for row in matches if str(row.get("action", "WAIT") or "WAIT").upper() in ("LONG", "SHORT")]
    observed = [row for row in matches if str(row.get("action", "WAIT") or "WAIT").upper() == "WAIT"]
    reward_sum = sum(_safe_float(row.get("reward")) for row in executed)
    best_reward_sum = sum(_safe_float(row.get("best_reward_training")) for row in matches)
    actions = sorted({str(row.get("action", "") or "") for row in matches if row.get("action")})
    runs = sorted({str(row.get("run", "") or "") for row in matches if row.get("run")})
    return {
        "seen_count": len(matches),
        "executed_count": len(executed),
        "observed_count": len(observed),
        "reward_sum": reward_sum,
        "best_reward_sum": best_reward_sum,
        "actions": ",".join(actions),
        "runs": ",".join(runs),
        "positive_execution_count": sum(1 for row in executed if _safe_float(row.get("reward")) > 0.0),
        "negative_execution_count": sum(1 for row in executed if _safe_float(row.get("reward")) < 0.0),
    }


def _classify(seed: dict, episode: dict) -> tuple[str, str, str]:
    seen = int(episode["seen_count"])
    executed = int(episode["executed_count"])
    observed = int(episode["observed_count"])
    reward = float(episode["reward_sum"])
    positive = int(episode["positive_execution_count"])
    negative = int(episode["negative_execution_count"])

    if seen <= 0:
        return (
            "reflection_memory_quiet",
            "old_trace_not_active_in_current_world",
            "Ich kenne diese Spur, aber diese Welt ruft sie gerade nicht auf.",
        )
    if executed > 0 and negative > 0 and reward <= 0.0:
        return (
            "reflection_memory_conflict",
            "old_trace_seen_but_not_carried",
            "Ich erkenne eine alte Spur, aber der aktuelle Kontakt traegt sie nicht.",
        )
    if executed > 0 and positive > 0 and reward > 0.0 and observed <= 0:
        return (
            "reflection_memory_reconfirmed",
            "old_trace_seen_and_carried",
            "Ich erkenne eine alte Spur wieder und der Kontakt traegt.",
        )
    if executed > 0 and positive > 0 and reward > 0.0:
        return (
            "reflection_memory_partly_reconfirmed",
            "old_trace_carried_with_observation_residue",
            "Ich erkenne eine alte Spur wieder, aber sie bleibt nicht ganz ruhig.",
        )
    if observed > 0:
        return (
            "reflection_memory_observed",
            "old_trace_seen_without_action",
            "Ich sehe eine alte Spur, aber sie bleibt Beobachtung.",
        )
    return (
        "reflection_memory_unclear",
        "old_trace_seen_without_clear_consequence",
        "Ich sehe eine alte Spur, aber ihre Wirkung ist noch unklar.",
    )


def _build_rows(memory: SemanticMemory, debug_root: Path) -> list[dict]:
    episodes = _iter_episode_rows(debug_root)
    by_family: dict[str, list[dict]] = {}
    for row in episodes:
        family = str(row.get("symbol_family", "") or "")
        by_family.setdefault(family, []).append(row)

    rows = []
    for seed in _reflection_seeds(memory):
        family = seed["symbol_family"]
        episode = _episode_summary(by_family.get(family, []))
        map_state, map_reason, dio_sentence = _classify(seed, episode)
        rows.append(
            {
                "reflection_symbol": seed["reflection_symbol"],
                "symbol_family": family,
                "reflection_state": seed["reflection_state"],
                "reflection_map_state": map_state,
                "reflection_map_reason": map_reason,
                "dio_sentence": dio_sentence,
                "seen_count": episode["seen_count"],
                "executed_count": episode["executed_count"],
                "observed_count": episode["observed_count"],
                "reward_sum": round(float(episode["reward_sum"]), 6),
                "best_reward_sum": round(float(episode["best_reward_sum"]), 6),
                "actions": episode["actions"],
                "runs": episode["runs"],
                "prior_observation_count": seed["prior_observation_count"],
                "prior_execution_count": seed["prior_execution_count"],
                "prior_execution_reward_sum": round(float(seed["prior_execution_reward_sum"]), 6),
                "followup_seen_count": seed["followup_seen_count"],
                "followup_executed_aligned_count": seed["followup_executed_aligned_count"],
                "followup_executed_reward": round(float(seed["followup_executed_reward"]), 6),
                "passive_only": seed["passive_only"],
            }
        )
    rows.sort(
        key=lambda row: (
            row["reflection_map_state"] != "reflection_memory_reconfirmed",
            row["reflection_map_state"] != "reflection_memory_partly_reconfirmed",
            row["reflection_map_state"] != "reflection_memory_observed",
            row["reflection_map_state"],
            row["symbol_family"],
        )
    )
    return rows


def _summary(rows: list[dict]) -> list[dict]:
    groups: dict[str, dict] = {}
    for row in rows:
        state = row["reflection_map_state"]
        item = groups.setdefault(
            state,
            {
                "reflection_map_state": state,
                "count": 0,
                "reward_sum": 0.0,
                "families": set(),
            },
        )
        item["count"] += 1
        item["reward_sum"] += float(row["reward_sum"])
        item["families"].add(str(row["symbol_family"]))
    summary = []
    for item in groups.values():
        summary.append(
            {
                "reflection_map_state": item["reflection_map_state"],
                "count": int(item["count"]),
                "reward_sum": round(float(item["reward_sum"]), 6),
                "families": ",".join(sorted(name for name in item["families"] if name)),
            }
        )
    summary.sort(key=lambda item: (-float(item["reward_sum"]), item["reflection_map_state"]))
    return summary


def _write(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fields = [
        "reflection_symbol",
        "symbol_family",
        "reflection_state",
        "reflection_map_state",
        "reflection_map_reason",
        "dio_sentence",
        "seen_count",
        "executed_count",
        "observed_count",
        "reward_sum",
        "best_reward_sum",
        "actions",
        "runs",
        "prior_observation_count",
        "prior_execution_count",
        "prior_execution_reward_sum",
        "followup_seen_count",
        "followup_executed_aligned_count",
        "followup_executed_reward",
        "passive_only",
    ]
    detail_path = output_dir / "dio_mini_reflection_map.csv"
    summary_path = output_dir / "dio_mini_reflection_map_summary.csv"
    json_path = output_dir / "dio_mini_reflection_map.json"
    md_path = output_dir / "dio_mini_reflection_map.md"

    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    summary_rows = _summary(rows)
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["reflection_map_state", "count", "reward_sum", "families"])
        writer.writeheader()
        writer.writerows(summary_rows)

    json_path.write_text(json.dumps({"detail": rows, "summary": summary_rows}, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Reflection Map", ""]
    for item in summary_rows:
        lines.extend(
            [
                f"## {item['reflection_map_state']}",
                f"- count: {item['count']}",
                f"- reward_sum: {float(item['reward_sum']):.6f}",
                f"- families: {item['families'] or '-'}",
                "",
            ]
        )
    lines.append("# Detail")
    lines.append("")
    for row in rows:
        lines.extend(
            [
                f"## {row['reflection_symbol']}",
                f"- family: {row['symbol_family']}",
                f"- state: {row['reflection_map_state']}",
                f"- reason: {row['reflection_map_reason']}",
                f"- DIO: {row['dio_sentence']}",
                f"- seen/executed/observed: {row['seen_count']} / {row['executed_count']} / {row['observed_count']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- passive_only: {row['passive_only']}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory", required=True)
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    memory = SemanticMemory(args.memory)
    memory.load()
    rows = _build_rows(memory, Path(args.debug_root))
    _write(rows, Path(args.output_dir))
    print(f"reflection_map={len(rows)}")
    for row in rows:
        print(
            f"{row['reflection_symbol']} family={row['symbol_family']} "
            f"state={row['reflection_map_state']} reward={row['reward_sum']}"
        )


if __name__ == "__main__":
    main()
