"""Read passive sentence-trace conflicts from DIO_MINI memory."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.semantic_memory import SemanticMemory


POSITIVE_STATES = {"kontakt_handlung_bestaetigt"}
BURDEN_STATES = {"kontakt_handlung_belastet"}


def _action_counts(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for chunk in str(text or "").split(","):
        if ":" not in chunk:
            continue
        key, value = chunk.split(":", 1)
        key = key.strip() or "-"
        try:
            counts[key] = counts.get(key, 0) + int(float(value.strip() or 0))
        except Exception:
            continue
    return counts


def _load_grouped(memory: SemanticMemory) -> dict[str, list[dict]]:
    traces = memory.data.get("sentence_traces", {})
    grouped: dict[str, list[dict]] = {}
    for sentence_symbol, item in sorted(dict(traces or {}).items()):
        data = dict(item or {})
        family = str(data.get("symbol_family", "") or "").strip()
        if not family:
            continue
        row = {
            "sentence_symbol": str(sentence_symbol),
            "symbol_family": family,
            "contact_symbol": str(data.get("contact_symbol", "") or ""),
            "contact_lage_state": str(data.get("contact_lage_state", "") or ""),
            "episode_contact_state": str(data.get("episode_contact_state", "") or ""),
            "count": int(data.get("count", 0) or 0),
            "reward_sum": float(data.get("reward_sum", 0.0) or 0.0),
            "actions": str(data.get("actions", "") or ""),
            "passive_only": int(data.get("passive_only", 0) or 0),
        }
        grouped.setdefault(family, []).append(row)
    return grouped


def _classify(rows: list[dict]) -> str:
    states = {str(row.get("episode_contact_state", "") or "") for row in rows}
    has_positive = bool(states & POSITIVE_STATES)
    has_burden = bool(states & BURDEN_STATES)
    if has_positive and has_burden:
        return "form_erleben_konflikt"
    if has_burden:
        return "form_belastungsspur"
    if has_positive:
        return "form_bestaetigungsspur"
    return "form_beobachtungsspur"


def _summaries(grouped: dict[str, list[dict]]) -> list[dict]:
    out = []
    for family, rows in grouped.items():
        contact_states = sorted({str(row["contact_lage_state"]) for row in rows if row.get("contact_lage_state")})
        episode_states = sorted({str(row["episode_contact_state"]) for row in rows if row.get("episode_contact_state")})
        action_counts: dict[str, int] = {}
        positive_reward = 0.0
        burden_reward = 0.0
        total_reward = 0.0
        positive_count = 0
        burden_count = 0
        for row in rows:
            reward = float(row.get("reward_sum", 0.0) or 0.0)
            total_reward += reward
            state = str(row.get("episode_contact_state", "") or "")
            if state in POSITIVE_STATES:
                positive_reward += reward
                positive_count += int(row.get("count", 0) or 0)
            if state in BURDEN_STATES:
                burden_reward += reward
                burden_count += int(row.get("count", 0) or 0)
            for action, count in _action_counts(str(row.get("actions", "") or "")).items():
                action_counts[action] = action_counts.get(action, 0) + count
        out.append(
            {
                "symbol_family": family,
                "conflict_state": _classify(rows),
                "trace_count": len(rows),
                "contact_lage_states": ",".join(contact_states),
                "episode_contact_states": ",".join(episode_states),
                "positive_count": positive_count,
                "burden_count": burden_count,
                "positive_reward_sum": round(positive_reward, 6),
                "burden_reward_sum": round(burden_reward, 6),
                "total_reward_sum": round(total_reward, 6),
                "actions": ",".join(f"{key}:{value}" for key, value in sorted(action_counts.items())),
                "passive_only": 1,
            }
        )
    out.sort(
        key=lambda item: (
            item["conflict_state"] != "form_erleben_konflikt",
            -abs(float(item["burden_reward_sum"] or 0.0)),
            -float(item["positive_reward_sum"] or 0.0),
            item["symbol_family"],
        )
    )
    return out


def _write(summary_rows: list[dict], detail_rows: dict[str, list[dict]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_csv = output_dir / "dio_mini_sentence_conflict_read.csv"
    summary_json = output_dir / "dio_mini_sentence_conflict_read.json"
    detail_csv = output_dir / "dio_mini_sentence_conflict_detail.csv"
    md_path = output_dir / "dio_mini_sentence_conflict_read.md"

    summary_fields = [
        "symbol_family",
        "conflict_state",
        "trace_count",
        "contact_lage_states",
        "episode_contact_states",
        "positive_count",
        "burden_count",
        "positive_reward_sum",
        "burden_reward_sum",
        "total_reward_sum",
        "actions",
        "passive_only",
    ]
    detail_fields = [
        "symbol_family",
        "sentence_symbol",
        "contact_symbol",
        "contact_lage_state",
        "episode_contact_state",
        "count",
        "reward_sum",
        "actions",
        "passive_only",
    ]
    with summary_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary_rows)
    with detail_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        for summary in summary_rows:
            if summary["conflict_state"] != "form_erleben_konflikt":
                continue
            for row in detail_rows.get(str(summary["symbol_family"]), []):
                writer.writerow(row)
    summary_json.write_text(json.dumps(summary_rows, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Sentence Conflict Read", ""]
    if not summary_rows:
        lines.append("Keine Satzspuren gefunden.")
    for row in summary_rows[:24]:
        lines.extend(
            [
                f"## {row['symbol_family']}",
                f"- state: {row['conflict_state']}",
                f"- contact_lage_states: {row['contact_lage_states'] or '-'}",
                f"- episode_contact_states: {row['episode_contact_states'] or '-'}",
                f"- positive_count: {row['positive_count']}",
                f"- burden_count: {row['burden_count']}",
                f"- positive_reward_sum: {float(row['positive_reward_sum']):.6f}",
                f"- burden_reward_sum: {float(row['burden_reward_sum']):.6f}",
                f"- actions: {row['actions'] or '-'}",
                "- passive_only: 1",
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
    grouped = _load_grouped(memory)
    summary_rows = _summaries(grouped)
    _write(summary_rows, grouped, Path(args.output_dir))
    conflicts = [row for row in summary_rows if row["conflict_state"] == "form_erleben_konflikt"]
    print(f"families={len(summary_rows)} conflicts={len(conflicts)}")
    for row in conflicts[:12]:
        print(
            f"{row['symbol_family']} {row['conflict_state']} "
            f"positive={row['positive_reward_sum']} burden={row['burden_reward_sum']} "
            f"actions={row['actions'] or '-'}"
        )


if __name__ == "__main__":
    main()
