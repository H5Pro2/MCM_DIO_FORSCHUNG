"""Build a passive timeline from DIO_MINI inner-state protocol rows.

The timeline keeps the chronological inner-state movement readable per run. It
does not write memory and does not influence actions.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _safe_float(value: object) -> float:
    try:
        return float(value or 0.0)
    except Exception:
        return 0.0


def _safe_int(value: object) -> int:
    try:
        return int(float(value or 0))
    except Exception:
        return 0


def _read_protocol(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append(dict(row))
    rows.sort(key=lambda row: (_safe_int(row.get("run")), _safe_int(row.get("tick"))))
    return rows


def _transition(from_state: str, to_state: str) -> str:
    if not from_state:
        return "timeline_start"
    if from_state == to_state:
        return "same_inner_state"
    return f"{from_state}_to_{to_state}"


def build_rows(protocol_csv: Path) -> tuple[list[dict], list[dict]]:
    rows = _read_protocol(protocol_csv)
    timeline: list[dict] = []
    previous_by_run: dict[str, str] = {}
    transition_groups: dict[str, dict] = {}
    for row in rows:
        run = str(row.get("run", "") or "")
        inner_state = str(row.get("inner_state", "inner_unknown") or "inner_unknown")
        previous = previous_by_run.get(run, "")
        transition = _transition(previous, inner_state)
        previous_by_run[run] = inner_state
        reward = _safe_float(row.get("reward"))
        best_reward = _safe_float(row.get("best_reward_training"))
        item = {
            "run": run,
            "tick": str(row.get("tick", "") or ""),
            "timestamp_ms": str(row.get("timestamp_ms", "") or ""),
            "symbol_family": str(row.get("symbol_family", "") or ""),
            "inner_state": inner_state,
            "previous_inner_state": previous or "-",
            "inner_transition": transition,
            "contact_state": str(row.get("contact_state", "") or ""),
            "action": str(row.get("action", "WAIT") or "WAIT").upper(),
            "raw_action": str(row.get("raw_action", "WAIT") or "WAIT").upper(),
            "best_action_training": str(row.get("best_action_training", "WAIT") or "WAIT").upper(),
            "reward": round(reward, 6),
            "best_reward_training": round(best_reward, 6),
            "sehen_form_flow": round(_safe_float(row.get("sehen_form_flow")), 6),
            "sehen_form_stability": round(_safe_float(row.get("sehen_form_stability")), 6),
            "hoeren_energy_tone": round(_safe_float(row.get("hoeren_energy_tone")), 6),
            "fuehlen_mcm_coherence": round(_safe_float(row.get("fuehlen_mcm_coherence")), 6),
            "fuehlen_mcm_tension": round(_safe_float(row.get("fuehlen_mcm_tension")), 6),
            "inner_sentence": str(row.get("inner_sentence", "") or ""),
            "passive_only": 1,
        }
        timeline.append(item)
        group = transition_groups.setdefault(
            transition,
            {
                "inner_transition": transition,
                "count": 0,
                "reward_sum": 0.0,
                "best_reward_sum": 0.0,
                "families": set(),
                "actions": set(),
            },
        )
        group["count"] += 1
        group["reward_sum"] += reward
        group["best_reward_sum"] += best_reward
        group["families"].add(str(item["symbol_family"]))
        group["actions"].add(str(item["action"]))

    summary: list[dict] = []
    for item in transition_groups.values():
        count = int(item["count"])
        summary.append(
            {
                "inner_transition": item["inner_transition"],
                "count": count,
                "reward_sum": round(float(item["reward_sum"]), 6),
                "best_reward_sum": round(float(item["best_reward_sum"]), 6),
                "avg_reward": round(float(item["reward_sum"]) / max(1, count), 6),
                "families": ",".join(sorted(name for name in item["families"] if name)),
                "actions": ",".join(sorted(name for name in item["actions"] if name)),
            }
        )
    summary.sort(key=lambda item: (-_safe_float(item.get("reward_sum")), str(item.get("inner_transition", ""))))
    return timeline, summary


def write_outputs(timeline: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    timeline_path = output_dir / "dio_mini_passive_inner_state_timeline.csv"
    summary_path = output_dir / "dio_mini_passive_inner_state_timeline_summary.csv"
    json_path = output_dir / "dio_mini_passive_inner_state_timeline.json"
    md_path = output_dir / "dio_mini_passive_inner_state_timeline.md"
    fields = list(timeline[0].keys()) if timeline else [
        "run",
        "tick",
        "symbol_family",
        "inner_state",
        "inner_transition",
        "contact_state",
        "action",
        "reward",
    ]
    with timeline_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(timeline)

    summary_fields = [
        "inner_transition",
        "count",
        "reward_sum",
        "best_reward_sum",
        "avg_reward",
        "families",
        "actions",
    ]
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)
    json_path.write_text(json.dumps({"timeline": timeline, "summary": summary}, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Passive Inner State Timeline", ""]
    if not summary:
        lines.append("Keine Innenlage-Zeitlinie gefunden.")
    for row in summary:
        lines.extend(
            [
                f"## {row['inner_transition']}",
                f"- count: {row['count']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- best_reward_sum: {float(row['best_reward_sum']):.6f}",
                f"- avg_reward: {float(row['avg_reward']):.6f}",
                f"- actions: {row['actions'] or '-'}",
                f"- families: {row['families'] or '-'}",
                "",
            ]
        )
    lines.extend(["# Timeline", ""])
    for row in timeline[:100]:
        lines.extend(
            [
                f"## run {row['run']} tick {row['tick']} {row['symbol_family']}",
                f"- transition: {row['inner_transition']}",
                f"- inner_state: {row['inner_state']}",
                f"- contact/action: {row['contact_state']} / {row['action']}",
                f"- reward/best: {float(row['reward']):.6f} / {float(row['best_reward_training']):.6f}",
                f"- sentence: {row['inner_sentence']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Grenze",
            "- kein Memory-Schreiben",
            "- keine Motorik",
            "- kein Gate",
            "- keine harte Regel",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive inner-state timeline from protocol CSV")
    parser.add_argument("--protocol-csv", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    timeline, summary = build_rows(Path(args.protocol_csv))
    write_outputs(timeline, summary, Path(args.output_dir))
    print(f"timeline_rows={len(timeline)} transition_rows={len(summary)}")
    for row in summary[:20]:
        print(
            f"{row['inner_transition']} count={row['count']} "
            f"reward={row['reward_sum']} actions={row['actions']}"
        )


if __name__ == "__main__":
    main()
