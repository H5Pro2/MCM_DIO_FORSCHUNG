"""Build a passive per-episode inner-state protocol for DIO_MINI.

The protocol joins episode rows with passive inner-awareness families. It shows
when a family was internally read as carried, cautious, open, or unfinished
during a debug world. It is diagnostic only.
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


def _load_inner_awareness(path: Path) -> dict[str, dict]:
    items: dict[str, dict] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            family = str(row.get("family", "") or "")
            if family:
                items[family] = dict(row)
    return items


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


def _contact_state(row: dict) -> str:
    action = str(row.get("action", "WAIT") or "WAIT").upper()
    raw_action = str(row.get("raw_action", action) or action).upper()
    best_action = str(row.get("best_action_training", "WAIT") or "WAIT").upper()
    reward = _safe_float(row.get("reward"))
    best_reward = _safe_float(row.get("best_reward_training"))
    phase_active = str(row.get("phase_active", "0") or "0") in ("1", "true", "True")
    if action in ("LONG", "SHORT"):
        if reward > 0.0:
            return "executed_positive_contact"
        if reward < 0.0:
            return "executed_negative_contact"
        return "executed_neutral_contact"
    if action == "WAIT" and raw_action in ("LONG", "SHORT") and phase_active:
        return "held_active_impulse"
    if action == "WAIT" and best_action in ("LONG", "SHORT") and best_reward > 0.0:
        return "observed_potential_contact"
    return "quiet_contact"


def _protocol_sentence(row: dict, awareness: dict, contact_state: str) -> str:
    family = str(row.get("symbol_family", "") or "-")
    inner_state = str(awareness.get("inner_state", "inner_unknown") or "inner_unknown")
    action = str(row.get("action", "WAIT") or "WAIT").upper()
    reward = _safe_float(row.get("reward"))
    if inner_state == "inner_carried" and action in ("LONG", "SHORT"):
        return f"{family}: innen getragen, realer Kontakt {action}, reward={reward:.6f}."
    if inner_state == "inner_carried":
        return f"{family}: innen getragen, aber in dieser Episode nicht gehandelt."
    if inner_state == "inner_cautious":
        return f"{family}: innen vorsichtig; Kontaktzustand {contact_state}."
    if inner_state == "inner_open_observation":
        return f"{family}: innen offen beobachtet; Kontaktzustand {contact_state}."
    if inner_state == "inner_unknown":
        return f"{family}: keine passive Innenlage zugeordnet; Kontaktzustand {contact_state}."
    return f"{family}: {inner_state}; Kontaktzustand {contact_state}."


def build_rows(debug_root: Path, inner_awareness_csv: Path) -> tuple[list[dict], list[dict]]:
    awareness_by_family = _load_inner_awareness(inner_awareness_csv)
    detail: list[dict] = []
    for row in _iter_episode_rows(debug_root):
        family = str(row.get("symbol_family", "") or "")
        awareness = awareness_by_family.get(family, {})
        contact_state = _contact_state(row)
        item = {
            "run": str(row.get("run", "") or ""),
            "tick": str(row.get("tick", "") or ""),
            "timestamp_ms": str(row.get("timestamp_ms", "") or ""),
            "symbol": str(row.get("symbol", "") or ""),
            "symbol_family": family,
            "inner_state": str(awareness.get("inner_state", "inner_unknown") or "inner_unknown"),
            "reflection_posture": str(awareness.get("reflection_posture", "") or ""),
            "contact_state": contact_state,
            "action": str(row.get("action", "WAIT") or "WAIT").upper(),
            "raw_action": str(row.get("raw_action", row.get("action", "WAIT")) or "WAIT").upper(),
            "best_action_training": str(row.get("best_action_training", "WAIT") or "WAIT").upper(),
            "reward": round(_safe_float(row.get("reward")), 6),
            "best_reward_training": round(_safe_float(row.get("best_reward_training")), 6),
            "phase_active": _safe_int(row.get("phase_active")),
            "episode_relation": str(row.get("episode_relation", "") or ""),
            "sehen_form_flow": round(_safe_float(row.get("sehen_form_flow")), 6),
            "sehen_form_stability": round(_safe_float(row.get("sehen_form_stability")), 6),
            "hoeren_energy_tone": round(_safe_float(row.get("hoeren_energy_tone")), 6),
            "fuehlen_mcm_coherence": round(_safe_float(row.get("fuehlen_mcm_coherence")), 6),
            "fuehlen_mcm_tension": round(_safe_float(row.get("fuehlen_mcm_tension")), 6),
            "inner_sentence": _protocol_sentence(row, awareness, contact_state),
            "passive_only": 1,
        }
        detail.append(item)

    groups: dict[tuple[str, str], dict] = {}
    for row in detail:
        key = (str(row["inner_state"]), str(row["contact_state"]))
        item = groups.setdefault(
            key,
            {
                "inner_state": key[0],
                "contact_state": key[1],
                "count": 0,
                "reward_sum": 0.0,
                "best_reward_sum": 0.0,
                "families": set(),
                "actions": set(),
            },
        )
        item["count"] += 1
        item["reward_sum"] += _safe_float(row.get("reward"))
        item["best_reward_sum"] += _safe_float(row.get("best_reward_training"))
        item["families"].add(str(row.get("symbol_family", "") or ""))
        item["actions"].add(str(row.get("action", "") or ""))

    summary: list[dict] = []
    for item in groups.values():
        count = int(item["count"])
        summary.append(
            {
                "inner_state": item["inner_state"],
                "contact_state": item["contact_state"],
                "count": count,
                "reward_sum": round(float(item["reward_sum"]), 6),
                "best_reward_sum": round(float(item["best_reward_sum"]), 6),
                "avg_reward": round(float(item["reward_sum"]) / max(1, count), 6),
                "families": ",".join(sorted(name for name in item["families"] if name)),
                "actions": ",".join(sorted(name for name in item["actions"] if name)),
            }
        )
    summary.sort(
        key=lambda item: (
            str(item.get("inner_state", "")) != "inner_carried",
            -_safe_float(item.get("reward_sum", 0.0)),
            str(item.get("inner_state", "")),
            str(item.get("contact_state", "")),
        )
    )
    return detail, summary


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_passive_inner_state_protocol.csv"
    summary_path = output_dir / "dio_mini_passive_inner_state_protocol_summary.csv"
    json_path = output_dir / "dio_mini_passive_inner_state_protocol.json"
    md_path = output_dir / "dio_mini_passive_inner_state_protocol.md"
    detail_fields = list(detail[0].keys()) if detail else [
        "run",
        "tick",
        "symbol_family",
        "inner_state",
        "contact_state",
        "action",
        "reward",
    ]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)

    summary_fields = [
        "inner_state",
        "contact_state",
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
    json_path.write_text(json.dumps({"detail": detail, "summary": summary}, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Passive Inner State Protocol", ""]
    if not summary:
        lines.append("Keine Innenlage-Episoden gefunden.")
    for row in summary:
        lines.extend(
            [
                f"## {row['inner_state']} / {row['contact_state']}",
                f"- count: {row['count']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- best_reward_sum: {float(row['best_reward_sum']):.6f}",
                f"- avg_reward: {float(row['avg_reward']):.6f}",
                f"- actions: {row['actions'] or '-'}",
                f"- families: {row['families'] or '-'}",
                "",
            ]
        )
    lines.extend(["# Detail", ""])
    for row in detail[:80]:
        lines.extend(
            [
                f"## run {row['run']} tick {row['tick']} {row['symbol_family']}",
                f"- inner_state: {row['inner_state']}",
                f"- contact_state: {row['contact_state']}",
                f"- action/raw/best: {row['action']} / {row['raw_action']} / {row['best_action_training']}",
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
    parser = argparse.ArgumentParser(description="Build passive per-episode inner-state protocol")
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--inner-awareness-csv", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    detail, summary = build_rows(Path(args.debug_root), Path(args.inner_awareness_csv))
    write_outputs(detail, summary, Path(args.output_dir))
    print(f"inner_state_protocol_rows={len(detail)} summary_rows={len(summary)}")
    for row in summary[:20]:
        print(
            f"{row['inner_state']} {row['contact_state']} "
            f"count={row['count']} reward={row['reward_sum']} actions={row['actions']}"
        )


if __name__ == "__main__":
    main()
