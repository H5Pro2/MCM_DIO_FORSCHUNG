"""Join Mini-DIO episodes with passive consequence inner awareness.

This report shows, tick by tick, whether the currently seen family has a
stored consequence feeling: carried, burdened, conflicted, quiet, or open.
It is a passive protocol and must not write memory or influence action.
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


def _load_awareness(path: Path) -> dict[str, list[dict]]:
    awareness: dict[str, list[dict]] = {}
    if not path.exists():
        return awareness
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            family = str(row.get("symbol_family", "") or "")
            if family:
                awareness.setdefault(family, []).append(dict(row))
    return awareness


def _iter_episode_rows(debug_root: Path) -> list[dict]:
    rows: list[dict] = []
    for path in sorted(debug_root.glob("**/episodes.csv")):
        run_id = path.parent.name.replace("dio_mini_lauf_", "")
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                item = dict(row)
                item["run"] = run_id
                item["source_file"] = str(path)
                rows.append(item)
    return rows


def _choose_awareness(items: list[dict], action: str) -> dict:
    if not items:
        return {}
    action = str(action or "WAIT").upper()
    action_matches = [item for item in items if str(item.get("action", "") or "").upper() == action]
    if action_matches:
        return action_matches[0]
    active = [
        item
        for item in items
        if str(item.get("action", "") or "").upper() in ("LONG", "SHORT")
    ]
    if active:
        return active[0]
    return items[0]


def _episode_contact_state(row: dict) -> str:
    action = str(row.get("action", "WAIT") or "WAIT").upper()
    raw_action = str(row.get("raw_action", action) or action).upper()
    event = str(row.get("outcome_event", "NO_TRADE") or "NO_TRADE").upper()
    phase_active = str(row.get("phase_active", "0") or "0") in ("1", "true", "True")
    if action in ("LONG", "SHORT"):
        if event == "TP":
            return "real_contact_carried"
        if event == "SL":
            return "real_contact_burdened"
        if event in ("TIMEOUT", "BOTH_TOUCHED"):
            return "real_contact_unclear"
        return "real_contact_open"
    if raw_action in ("LONG", "SHORT") and phase_active:
        return "held_impulse_without_action"
    return "observed_without_action"


def _protocol_sentence(row: dict, awareness: dict, contact_state: str) -> str:
    family = str(row.get("symbol_family", "") or "-")
    action = str(row.get("action", "WAIT") or "WAIT").upper()
    event = str(row.get("outcome_event", "NO_TRADE") or "NO_TRADE").upper()
    inner_state = str(awareness.get("inner_state", "inner_consequence_unknown") or "inner_consequence_unknown")
    memory_trust = _safe_float(awareness.get("memory_trust", 0.0))
    memory_caution = _safe_float(awareness.get("memory_caution", 0.0))
    if inner_state == "inner_consequence_carried":
        return (
            f"{family}: DIO sieht eine innen getragene Konsequenzspur; "
            f"Kontakt={contact_state}, Aktion={action}, Event={event}, "
            f"trust={memory_trust:.6f}, caution={memory_caution:.6f}."
        )
    if inner_state == "inner_consequence_conflicted":
        return (
            f"{family}: DIO sieht eine widerspruechliche Konsequenzspur; "
            f"Kontakt={contact_state}, Aktion={action}, Event={event}, "
            f"trust={memory_trust:.6f}, caution={memory_caution:.6f}."
        )
    if inner_state == "inner_consequence_burdened":
        return (
            f"{family}: DIO sieht eine belastete Konsequenzspur; "
            f"Kontakt={contact_state}, Aktion={action}, Event={event}, "
            f"trust={memory_trust:.6f}, caution={memory_caution:.6f}."
        )
    if inner_state == "inner_consequence_quiet":
        return f"{family}: DIO sieht eine ruhige Beobachtungsspur; Kontakt={contact_state}."
    if inner_state == "inner_consequence_unknown":
        return f"{family}: keine gespeicherte Konsequenz-Innenlage; Kontakt={contact_state}."
    return f"{family}: {inner_state}; Kontakt={contact_state}, Aktion={action}, Event={event}."


def build_rows(debug_root: Path, awareness_csv: Path) -> tuple[list[dict], list[dict]]:
    awareness_by_family = _load_awareness(awareness_csv)
    detail: list[dict] = []
    for row in _iter_episode_rows(debug_root):
        family = str(row.get("symbol_family", "") or "")
        action = str(row.get("action", "WAIT") or "WAIT").upper()
        awareness = _choose_awareness(awareness_by_family.get(family, []), action)
        contact_state = _episode_contact_state(row)
        item = {
            "run": str(row.get("run", "") or ""),
            "tick": str(row.get("tick", "") or ""),
            "timestamp_ms": str(row.get("timestamp_ms", "") or ""),
            "symbol": str(row.get("symbol", "") or ""),
            "symbol_family": family,
            "action": action,
            "raw_action": str(row.get("raw_action", action) or action).upper(),
            "outcome_event": str(row.get("outcome_event", "NO_TRADE") or "NO_TRADE").upper(),
            "reward": round(_safe_float(row.get("reward", 0.0)), 6),
            "event_reward": round(_safe_float(row.get("event_reward", 0.0)), 6),
            "contact_state": contact_state,
            "inner_state": str(awareness.get("inner_state", "inner_consequence_unknown") or "inner_consequence_unknown"),
            "memory_trust": round(_safe_float(awareness.get("memory_trust", 0.0)), 6),
            "memory_caution": round(_safe_float(awareness.get("memory_caution", 0.0)), 6),
            "memory_trust_minus_caution": round(_safe_float(awareness.get("memory_trust_minus_caution", 0.0)), 6),
            "memory_action_count": _safe_int(awareness.get("memory_action_count", 0)),
            "consequence_effect": str(awareness.get("consequence_effect", "") or ""),
            "sehen_form_flow": round(_safe_float(row.get("sehen_form_flow", 0.0)), 6),
            "sehen_form_stability": round(_safe_float(row.get("sehen_form_stability", 0.0)), 6),
            "hoeren_energy_tone": round(_safe_float(row.get("hoeren_energy_tone", 0.0)), 6),
            "fuehlen_mcm_coherence": round(_safe_float(row.get("fuehlen_mcm_coherence", 0.0)), 6),
            "fuehlen_mcm_tension": round(_safe_float(row.get("fuehlen_mcm_tension", 0.0)), 6),
            "inner_sentence": _protocol_sentence(row, awareness, contact_state),
            "source_file": str(row.get("source_file", "") or ""),
            "passive_only": 1,
        }
        detail.append(item)

    groups: dict[tuple[str, str], dict] = {}
    for row in detail:
        key = (str(row.get("inner_state", "")), str(row.get("contact_state", "")))
        group = groups.setdefault(
            key,
            {
                "inner_state": key[0],
                "contact_state": key[1],
                "count": 0,
                "reward_sum": 0.0,
                "event_reward_sum": 0.0,
                "families": set(),
                "actions": set(),
                "outcome_events": set(),
            },
        )
        group["count"] += 1
        group["reward_sum"] += _safe_float(row.get("reward", 0.0))
        group["event_reward_sum"] += _safe_float(row.get("event_reward", 0.0))
        group["families"].add(str(row.get("symbol_family", "") or ""))
        group["actions"].add(str(row.get("action", "") or ""))
        group["outcome_events"].add(str(row.get("outcome_event", "") or ""))

    summary: list[dict] = []
    for group in groups.values():
        count = int(group["count"])
        summary.append(
            {
                "inner_state": group["inner_state"],
                "contact_state": group["contact_state"],
                "count": count,
                "reward_sum": round(float(group["reward_sum"]), 6),
                "event_reward_sum": round(float(group["event_reward_sum"]), 6),
                "avg_reward": round(float(group["reward_sum"]) / max(1, count), 6),
                "families": ",".join(sorted(name for name in group["families"] if name)),
                "actions": ",".join(sorted(name for name in group["actions"] if name)),
                "outcome_events": ",".join(sorted(name for name in group["outcome_events"] if name)),
            }
        )

    order = {
        "inner_consequence_carried": 0,
        "inner_consequence_conflicted": 1,
        "inner_consequence_burdened": 2,
        "inner_consequence_unclear": 3,
        "inner_consequence_quiet": 4,
        "inner_consequence_open": 5,
        "inner_consequence_unknown": 6,
    }
    summary.sort(
        key=lambda item: (
            order.get(str(item.get("inner_state", "")), 99),
            str(item.get("contact_state", "")),
        )
    )
    detail.sort(
        key=lambda item: (
            str(item.get("run", "")),
            _safe_int(item.get("tick", 0)),
            order.get(str(item.get("inner_state", "")), 99),
        )
    )
    return detail, summary


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path, awareness_csv: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_passive_consequence_inner_state_protocol.csv"
    summary_path = output_dir / "dio_mini_passive_consequence_inner_state_protocol_summary.csv"
    json_path = output_dir / "dio_mini_passive_consequence_inner_state_protocol.json"
    md_path = output_dir / "dio_mini_passive_consequence_inner_state_protocol.md"

    detail_fields = list(detail[0].keys()) if detail else [
        "run",
        "tick",
        "symbol_family",
        "action",
        "outcome_event",
        "contact_state",
        "inner_state",
        "inner_sentence",
        "passive_only",
    ]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)

    summary_fields = list(summary[0].keys()) if summary else [
        "inner_state",
        "contact_state",
        "count",
        "reward_sum",
        "event_reward_sum",
        "avg_reward",
        "families",
        "actions",
        "outcome_events",
    ]
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)

    json_path.write_text(
        json.dumps(
            {
                "awareness_csv": str(awareness_csv),
                "detail": detail,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# DIO Mini Passive Consequence Inner State Protocol",
        "",
        "## Grenze",
        "- liest nur episodes.csv und passive Konsequenz-Innenlage",
        "- schreibt kein Memory",
        "- beeinflusst keine Handlung",
        "- kein Gate",
        "",
        "## Zusammenfassung",
    ]
    if not summary:
        lines.append("- keine Episoden gefunden")
    else:
        for row in summary:
            lines.append(
                f"- {row.get('inner_state', '-')}/{row.get('contact_state', '-')}: "
                f"count={row.get('count', 0)} reward_sum={row.get('reward_sum', 0.0)} "
                f"families={row.get('families', '-') or '-'}"
            )
    lines.extend(["", "## Erste Tick-Lesung"])
    for row in detail[:80]:
        lines.append(f"- run {row.get('run', '-')} tick {row.get('tick', '-')}: {row.get('inner_sentence', '-')}")
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Join Mini-DIO episodes with passive consequence inner awareness")
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--inner-awareness-csv", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    awareness_csv = Path(args.inner_awareness_csv)
    detail, summary = build_rows(Path(args.debug_root), awareness_csv)
    write_outputs(detail, summary, Path(args.output_dir), awareness_csv)
    print(f"consequence_inner_state_rows={len(detail)} summary_rows={len(summary)}")
    for row in summary[:20]:
        print(
            f"{row['inner_state']} {row['contact_state']} "
            f"count={row['count']} reward={row['reward_sum']} families={row['families']}"
        )


if __name__ == "__main__":
    main()
