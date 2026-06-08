"""Classify passive DIO_MINI reflection seeds as self-awareness traces."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.semantic_memory import SemanticMemory


def _safe_int(value: object) -> int:
    try:
        return int(float(value))
    except Exception:
        return 0


def _safe_float(value: object) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


def _classify(seed: dict) -> tuple[str, str]:
    state = str(seed.get("reflection_state", "") or "")
    prior_obs = _safe_int(seed.get("prior_observation_count"))
    prior_exec = _safe_int(seed.get("prior_execution_count"))
    prior_reward = _safe_float(seed.get("prior_execution_reward_sum"))
    follow_seen = _safe_int(seed.get("followup_seen_count"))
    follow_exec = _safe_int(seed.get("followup_executed_aligned_count"))
    follow_reward = _safe_float(seed.get("followup_executed_reward"))
    follow_observed = _safe_int(seed.get("followup_observed_count"))
    follow_overheld = _safe_int(seed.get("followup_overheld_count"))

    if state != "reflection_seed_reconfirmed":
        return "self_awareness_report_only", "not_reconfirmed"
    if follow_overheld > 0:
        return "self_awareness_conflicted", "followup_overheld"
    if follow_exec >= 2 and follow_reward > prior_reward and follow_observed == 0:
        return "self_awareness_stable", "reconfirmed_without_observation_residue"
    if follow_exec >= 1 and follow_reward > 0.0 and prior_obs > prior_exec:
        return "self_awareness_tentative", "partly_reconfirmed_after_observation"
    if follow_exec >= 1 and follow_reward > 0.0:
        return "self_awareness_tentative", "single_reconfirmation"
    if follow_seen > 0:
        return "self_awareness_report_only", "seen_without_reconfirmation"
    return "self_awareness_report_only", "not_seen_again"


def _rows(memory: SemanticMemory) -> list[dict]:
    seeds = memory.data.setdefault("reflection_seeds", {})
    if not isinstance(seeds, dict):
        return []
    rows = []
    for symbol, seed in seeds.items():
        seed = dict(seed or {})
        awareness_state, reason = _classify(seed)
        rows.append(
            {
                "reflection_symbol": str(seed.get("reflection_symbol", symbol) or symbol),
                "symbol_family": str(seed.get("symbol_family", "") or ""),
                "reflection_state": str(seed.get("reflection_state", "") or ""),
                "self_awareness_state": awareness_state,
                "self_awareness_reason": reason,
                "prior_observation_count": _safe_int(seed.get("prior_observation_count")),
                "prior_execution_count": _safe_int(seed.get("prior_execution_count")),
                "prior_execution_reward_sum": round(_safe_float(seed.get("prior_execution_reward_sum")), 6),
                "followup_seen_count": _safe_int(seed.get("followup_seen_count")),
                "followup_executed_aligned_count": _safe_int(seed.get("followup_executed_aligned_count")),
                "followup_executed_reward": round(_safe_float(seed.get("followup_executed_reward")), 6),
                "followup_observed_count": _safe_int(seed.get("followup_observed_count")),
                "followup_overheld_count": _safe_int(seed.get("followup_overheld_count")),
                "followup_actions": str(seed.get("followup_actions", "") or ""),
                "passive_only": _safe_int(seed.get("passive_only")),
            }
        )
    rows.sort(
        key=lambda item: (
            item["self_awareness_state"] != "self_awareness_stable",
            item["self_awareness_state"] != "self_awareness_tentative",
            -float(item["followup_executed_reward"]),
            item["symbol_family"],
        )
    )
    return rows


def _summary(rows: list[dict]) -> list[dict]:
    groups: dict[str, dict] = {}
    for row in rows:
        state = row["self_awareness_state"]
        item = groups.setdefault(
            state,
            {
                "self_awareness_state": state,
                "count": 0,
                "followup_reward_sum": 0.0,
                "families": set(),
            },
        )
        item["count"] += 1
        item["followup_reward_sum"] += float(row["followup_executed_reward"])
        item["families"].add(str(row["symbol_family"]))
    summary = []
    for item in groups.values():
        summary.append(
            {
                "self_awareness_state": item["self_awareness_state"],
                "count": int(item["count"]),
                "followup_reward_sum": round(float(item["followup_reward_sum"]), 6),
                "families": ",".join(sorted(name for name in item["families"] if name)),
            }
        )
    summary.sort(key=lambda item: (-int(item["count"]), item["self_awareness_state"]))
    return summary


def _write(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_reflection_self_awareness.csv"
    summary_path = output_dir / "dio_mini_reflection_self_awareness_summary.csv"
    json_path = output_dir / "dio_mini_reflection_self_awareness.json"
    md_path = output_dir / "dio_mini_reflection_self_awareness.md"
    fields = [
        "reflection_symbol",
        "symbol_family",
        "reflection_state",
        "self_awareness_state",
        "self_awareness_reason",
        "prior_observation_count",
        "prior_execution_count",
        "prior_execution_reward_sum",
        "followup_seen_count",
        "followup_executed_aligned_count",
        "followup_executed_reward",
        "followup_observed_count",
        "followup_overheld_count",
        "followup_actions",
        "passive_only",
    ]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    summary_rows = _summary(rows)
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["self_awareness_state", "count", "followup_reward_sum", "families"])
        writer.writeheader()
        writer.writerows(summary_rows)
    json_path.write_text(json.dumps({"detail": rows, "summary": summary_rows}, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Reflection Self-Awareness", ""]
    if not rows:
        lines.append("Keine Reflexionskeime gefunden.")
    for item in summary_rows:
        lines.extend(
            [
                f"## {item['self_awareness_state']}",
                f"- count: {item['count']}",
                f"- followup_reward_sum: {float(item['followup_reward_sum']):.6f}",
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
                f"- state: {row['self_awareness_state']}",
                f"- reason: {row['self_awareness_reason']}",
                f"- prior observation/execution: {row['prior_observation_count']} / {row['prior_execution_count']}",
                f"- followup executed: {row['followup_executed_aligned_count']} / {float(row['followup_executed_reward']):.6f}",
                f"- followup observed/overheld: {row['followup_observed_count']} / {row['followup_overheld_count']}",
                f"- passive_only: {row['passive_only']}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    memory = SemanticMemory(args.memory)
    memory.load()
    rows = _rows(memory)
    _write(rows, Path(args.output_dir))
    print(f"reflection_self_awareness={len(rows)}")
    for row in rows:
        print(
            f"{row['reflection_symbol']} family={row['symbol_family']} "
            f"state={row['self_awareness_state']} reason={row['self_awareness_reason']}"
        )


if __name__ == "__main__":
    main()
