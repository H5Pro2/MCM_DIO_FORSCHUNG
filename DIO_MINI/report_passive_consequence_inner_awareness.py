"""Build passive inner awareness from Mini-DIO consequence memory effects.

This report translates TP/SL memory effects into an internal state view:
carried, cautious, conflicted, quiet, or unclear. It is diagnostic only.
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


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _inner_state(row: dict) -> str:
    event = str(row.get("outcome_event", "") or "").upper()
    effect = str(row.get("consequence_effect", "") or "")
    trust = _safe_float(row.get("memory_trust", 0.0))
    caution = _safe_float(row.get("memory_caution", 0.0))
    reward_sum = _safe_float(row.get("memory_reward_sum", 0.0))
    if event == "TP" and trust > caution and reward_sum > 0.0:
        return "inner_consequence_carried"
    if event == "SL" and caution >= trust:
        return "inner_consequence_burdened"
    if event == "SL" and caution > 0.0 and trust > caution:
        return "inner_consequence_conflicted"
    if effect in ("timeout_neutral_trace", "ambiguous_contact_trace"):
        return "inner_consequence_unclear"
    if event in ("NO_TRADE", ""):
        return "inner_consequence_quiet"
    return "inner_consequence_open"


def _sentence(row: dict, state: str) -> str:
    family = str(row.get("symbol_family", "") or "-")
    action = str(row.get("action", "") or "-")
    event = str(row.get("outcome_event", "") or "-")
    trust = _safe_float(row.get("memory_trust", 0.0))
    caution = _safe_float(row.get("memory_caution", 0.0))
    count = _safe_int(row.get("event_count", 0))
    if state == "inner_consequence_carried":
        return (
            f"{family}: {action} wurde durch {event} getragen; "
            f"innen entsteht Vertrauen ({trust:.6f}) bei Vorsicht {caution:.6f}."
        )
    if state == "inner_consequence_burdened":
        return (
            f"{family}: {action} wurde durch {event} belastet; "
            f"innen dominiert Vorsicht ({caution:.6f}) gegen Vertrauen {trust:.6f}."
        )
    if state == "inner_consequence_conflicted":
        return (
            f"{family}: {action} wurde durch {event} belastet, aber alte Erfahrung traegt noch; "
            f"innen bleibt Widerspruch trust={trust:.6f}, caution={caution:.6f}."
        )
    if state == "inner_consequence_unclear":
        return f"{family}: {action} blieb in {event} unklar; innen bleibt die Folge offen."
    if state == "inner_consequence_quiet":
        return f"{family}: keine reale Handlung; innen bleibt die Familie ruhig beobachtet ({count} Ereignisse)."
    return f"{family}: {action} {event}; innere Konsequenz noch offen."


def build_rows(effect_csv: Path) -> tuple[list[dict], list[dict]]:
    detail: list[dict] = []
    for row in _read_csv(effect_csv):
        state = _inner_state(row)
        item = {
            "symbol_family": str(row.get("symbol_family", "") or "-"),
            "action": str(row.get("action", "WAIT") or "WAIT").upper(),
            "outcome_event": str(row.get("outcome_event", "NO_TRADE") or "NO_TRADE").upper(),
            "inner_state": state,
            "event_count": _safe_int(row.get("event_count", 0)),
            "event_reward_sum": round(_safe_float(row.get("event_reward_sum", 0.0)), 6),
            "memory_action_count": _safe_int(row.get("memory_action_count", 0)),
            "memory_reward_sum": round(_safe_float(row.get("memory_reward_sum", 0.0)), 6),
            "memory_trust": round(_safe_float(row.get("memory_trust", 0.0)), 6),
            "memory_caution": round(_safe_float(row.get("memory_caution", 0.0)), 6),
            "memory_trust_minus_caution": round(_safe_float(row.get("memory_trust_minus_caution", 0.0)), 6),
            "consequence_effect": str(row.get("consequence_effect", "") or ""),
            "inner_sentence": _sentence(row, state),
            "passive_only": 1,
        }
        detail.append(item)

    groups: dict[str, dict] = {}
    for row in detail:
        state = str(row.get("inner_state", "") or "")
        item = groups.setdefault(
            state,
            {
                "inner_state": state,
                "count": 0,
                "event_reward_sum": 0.0,
                "memory_reward_sum": 0.0,
                "families": set(),
                "actions": set(),
            },
        )
        item["count"] += 1
        item["event_reward_sum"] += _safe_float(row.get("event_reward_sum", 0.0))
        item["memory_reward_sum"] += _safe_float(row.get("memory_reward_sum", 0.0))
        item["families"].add(str(row.get("symbol_family", "") or ""))
        item["actions"].add(str(row.get("action", "") or ""))

    summary: list[dict] = []
    for item in groups.values():
        summary.append(
            {
                "inner_state": item["inner_state"],
                "count": int(item["count"]),
                "event_reward_sum": round(float(item["event_reward_sum"]), 6),
                "memory_reward_sum": round(float(item["memory_reward_sum"]), 6),
                "families": ",".join(sorted(name for name in item["families"] if name)),
                "actions": ",".join(sorted(name for name in item["actions"] if name)),
            }
        )

    order = {
        "inner_consequence_carried": 0,
        "inner_consequence_burdened": 1,
        "inner_consequence_conflicted": 2,
        "inner_consequence_unclear": 3,
        "inner_consequence_quiet": 4,
        "inner_consequence_open": 5,
    }
    detail.sort(key=lambda item: (order.get(str(item.get("inner_state", "")), 99), str(item.get("symbol_family", ""))))
    summary.sort(key=lambda item: (order.get(str(item.get("inner_state", "")), 99), str(item.get("inner_state", ""))))
    return detail, summary


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path, effect_csv: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_passive_consequence_inner_awareness.csv"
    summary_path = output_dir / "dio_mini_passive_consequence_inner_awareness_summary.csv"
    json_path = output_dir / "dio_mini_passive_consequence_inner_awareness.json"
    md_path = output_dir / "dio_mini_passive_consequence_inner_awareness.md"

    detail_fields = list(detail[0].keys()) if detail else [
        "symbol_family",
        "action",
        "outcome_event",
        "inner_state",
        "event_count",
        "event_reward_sum",
        "memory_action_count",
        "memory_reward_sum",
        "memory_trust",
        "memory_caution",
        "memory_trust_minus_caution",
        "consequence_effect",
        "inner_sentence",
        "passive_only",
    ]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)

    summary_fields = list(summary[0].keys()) if summary else [
        "inner_state",
        "count",
        "event_reward_sum",
        "memory_reward_sum",
        "families",
        "actions",
    ]
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)

    json_path.write_text(
        json.dumps(
            {
                "effect_csv": str(effect_csv),
                "detail": detail,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# DIO Mini Passive Consequence Inner Awareness",
        "",
        "## Grenze",
        "- liest nur den passiven Konsequenzwirkungs-Report",
        "- schreibt kein Memory",
        "- beeinflusst keine Handlung",
        "- kein Gate",
        "",
        "## Zusammenfassung",
    ]
    if not summary:
        lines.append("- keine Innenlage gefunden")
    else:
        for row in summary:
            lines.append(
                f"- {row.get('inner_state', '-')}: count={row.get('count', 0)} "
                f"event_reward_sum={row.get('event_reward_sum', 0.0)} "
                f"memory_reward_sum={row.get('memory_reward_sum', 0.0)} "
                f"families={row.get('families', '-') or '-'}"
            )
    lines.extend(["", "## Familien"])
    for row in detail:
        lines.append(f"- {row.get('inner_sentence', '-')}")
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive consequence inner awareness for Mini-DIO")
    parser.add_argument("--effect-csv", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    effect_csv = Path(args.effect_csv)
    detail, summary = build_rows(effect_csv)
    write_outputs(detail, summary, Path(args.output_dir), effect_csv)
    print(f"inner_consequence_rows={len(detail)} summary_rows={len(summary)}")
    for row in summary:
        print(
            f"{row['inner_state']} count={row['count']} "
            f"families={row['families']} actions={row['actions']}"
        )


if __name__ == "__main__":
    main()
