"""Report passive self-awareness family transfer into a later DIO_MINI run."""

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


def _seed_rows(memory: SemanticMemory) -> list[dict]:
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
                "prior_execution_reward_sum": _safe_float(seed.get("prior_execution_reward_sum")),
                "followup_executed_reward": _safe_float(seed.get("followup_executed_reward")),
                "passive_only": _safe_int(seed.get("passive_only")),
            }
        )
    return rows


def _classify(matches: list[dict]) -> tuple[str, str]:
    if not matches:
        return "transfer_not_seen", "family_absent_in_probe"
    executed = [row for row in matches if str(row.get("action", "WAIT") or "WAIT").upper() in ("LONG", "SHORT")]
    observed = [row for row in matches if str(row.get("action", "WAIT") or "WAIT").upper() == "WAIT"]
    reward_sum = sum(_safe_float(row.get("reward")) for row in executed)
    negative_count = sum(1 for row in executed if _safe_float(row.get("reward")) < 0.0)
    positive_count = sum(1 for row in executed if _safe_float(row.get("reward")) > 0.0)
    if executed and negative_count and reward_sum <= 0.0:
        return "transfer_conflicted", "executed_but_not_carried"
    if positive_count and reward_sum > 0.0:
        if observed:
            return "transfer_reconfirmed_mixed", "executed_positive_with_observation_residue"
        return "transfer_reconfirmed_clean", "executed_positive_without_residue"
    if observed:
        return "transfer_seen_observed", "seen_but_not_executed"
    return "transfer_seen_unclear", "seen_without_clear_contact"


def _build_rows(seed_rows: list[dict], episode_rows: list[dict]) -> list[dict]:
    by_family: dict[str, list[dict]] = {}
    for row in episode_rows:
        family = str(row.get("symbol_family", "") or "")
        by_family.setdefault(family, []).append(row)

    rows = []
    for seed in seed_rows:
        family = seed["symbol_family"]
        matches = by_family.get(family, [])
        state, reason = _classify(matches)
        executed = [row for row in matches if str(row.get("action", "WAIT") or "WAIT").upper() in ("LONG", "SHORT")]
        observed = [row for row in matches if str(row.get("action", "WAIT") or "WAIT").upper() == "WAIT"]
        rows.append(
            {
                "reflection_symbol": seed["reflection_symbol"],
                "symbol_family": family,
                "reflection_state": seed["reflection_state"],
                "transfer_state": state,
                "transfer_reason": reason,
                "seen_count": len(matches),
                "executed_count": len(executed),
                "observed_count": len(observed),
                "reward_sum": round(sum(_safe_float(row.get("reward")) for row in executed), 6),
                "best_reward_sum": round(sum(_safe_float(row.get("best_reward_training")) for row in matches), 6),
                "actions": ",".join(sorted({str(row.get("action", "") or "") for row in matches if row.get("action")})),
                "runs": ",".join(sorted({str(row.get("run", "") or "") for row in matches if row.get("run")})),
                "prior_execution_reward_sum": round(seed["prior_execution_reward_sum"], 6),
                "followup_executed_reward": round(seed["followup_executed_reward"], 6),
                "passive_only": seed["passive_only"],
            }
        )
    rows.sort(key=lambda row: (row["transfer_state"], row["symbol_family"]))
    return rows


def _summary(rows: list[dict]) -> list[dict]:
    groups: dict[str, dict] = {}
    for row in rows:
        state = row["transfer_state"]
        item = groups.setdefault(
            state,
            {
                "transfer_state": state,
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
                "transfer_state": item["transfer_state"],
                "count": int(item["count"]),
                "reward_sum": round(float(item["reward_sum"]), 6),
                "families": ",".join(sorted(name for name in item["families"] if name)),
            }
        )
    summary.sort(key=lambda item: (-int(item["count"]), item["transfer_state"]))
    return summary


def _write(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_self_awareness_transfer.csv"
    summary_path = output_dir / "dio_mini_self_awareness_transfer_summary.csv"
    json_path = output_dir / "dio_mini_self_awareness_transfer.json"
    md_path = output_dir / "dio_mini_self_awareness_transfer.md"
    fields = [
        "reflection_symbol",
        "symbol_family",
        "reflection_state",
        "transfer_state",
        "transfer_reason",
        "seen_count",
        "executed_count",
        "observed_count",
        "reward_sum",
        "best_reward_sum",
        "actions",
        "runs",
        "prior_execution_reward_sum",
        "followup_executed_reward",
        "passive_only",
    ]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    summary_rows = _summary(rows)
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["transfer_state", "count", "reward_sum", "families"])
        writer.writeheader()
        writer.writerows(summary_rows)

    json_path.write_text(json.dumps({"detail": rows, "summary": summary_rows}, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Self-Awareness Transfer", ""]
    for item in summary_rows:
        lines.extend(
            [
                f"## {item['transfer_state']}",
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
                f"- transfer: {row['transfer_state']} ({row['transfer_reason']})",
                f"- seen/executed/observed: {row['seen_count']} / {row['executed_count']} / {row['observed_count']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- actions: {row['actions'] or '-'}",
                f"- runs: {row['runs'] or '-'}",
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
    rows = _build_rows(_seed_rows(memory), _iter_episode_rows(Path(args.debug_root)))
    _write(rows, Path(args.output_dir))
    print(f"self_awareness_transfer={len(rows)}")
    for row in rows:
        print(
            f"{row['reflection_symbol']} family={row['symbol_family']} "
            f"state={row['transfer_state']} reward={row['reward_sum']}"
        )


if __name__ == "__main__":
    main()
