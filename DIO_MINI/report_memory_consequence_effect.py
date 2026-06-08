"""Compare Mini-DIO trade events with semantic memory action state.

This is a passive diagnostic. It reads an event summary and a memory file,
then shows whether TP/SL consequences are visible as trust or caution in the
stored family/action state.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ACTION_FIELDS = [
    "memory_action_count",
    "memory_reward_sum",
    "memory_trust",
    "memory_caution",
    "memory_last_reward",
    "memory_timing_improvement_sum",
]


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


def _read_memory(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _classify_effect(event: str, event_reward: float, trust: float, caution: float, reward_sum: float) -> str:
    event = str(event or "").upper()
    if event == "TP":
        if trust > caution and reward_sum > 0.0:
            return "tp_trust_visible"
        return "tp_not_yet_stable"
    if event == "SL":
        if caution >= trust:
            return "sl_caution_dominant"
        if caution > 0.0 and event_reward < 0.0:
            return "sl_caution_visible_but_not_dominant"
        return "sl_not_yet_visible"
    if event == "TIMEOUT":
        return "timeout_neutral_trace"
    if event == "BOTH_TOUCHED":
        return "ambiguous_contact_trace"
    return "no_trade_or_observation"


def build_rows(memory_path: Path, events_path: Path) -> list[dict]:
    memory = _read_memory(memory_path)
    families = dict(memory.get("families", {}) or {})
    rows: list[dict] = []

    for event_row in _read_csv(events_path):
        family = str(event_row.get("symbol_family", "") or "-")
        action = str(event_row.get("action", "WAIT") or "WAIT").upper()
        event = str(event_row.get("outcome_event", "NO_TRADE") or "NO_TRADE").upper()
        family_record = dict(families.get(family, {}) or {})
        action_state = dict(dict(family_record.get("actions", {}) or {}).get(action, {}) or {})

        memory_count = _safe_int(action_state.get("count", 0))
        memory_reward_sum = _safe_float(action_state.get("reward_sum", 0.0))
        trust = _safe_float(action_state.get("trust", 0.0))
        caution = _safe_float(action_state.get("caution", 0.0))
        event_count = _safe_int(event_row.get("count", 0))
        event_reward_sum = _safe_float(event_row.get("reward_sum", 0.0))

        rows.append(
            {
                "symbol_family": family,
                "action": action,
                "outcome_event": event,
                "event_count": event_count,
                "event_reward_sum": round(event_reward_sum, 6),
                "event_avg_reward": round(_safe_float(event_row.get("avg_reward", 0.0)), 6),
                "memory_family_count": _safe_int(family_record.get("count", 0)),
                "memory_action_count": memory_count,
                "memory_reward_sum": round(memory_reward_sum, 6),
                "memory_avg_reward": round(memory_reward_sum / max(1, memory_count), 6),
                "memory_trust": round(trust, 6),
                "memory_caution": round(caution, 6),
                "memory_trust_minus_caution": round(trust - caution, 6),
                "memory_last_reward": round(_safe_float(action_state.get("last_reward", 0.0)), 6),
                "memory_timing_improvement_sum": round(
                    _safe_float(action_state.get("timing_improvement_sum", 0.0)),
                    6,
                ),
                "consequence_effect": _classify_effect(
                    event,
                    event_reward_sum / max(1, event_count),
                    trust,
                    caution,
                    memory_reward_sum,
                ),
                "passive_only": 1,
            }
        )

    rows.sort(
        key=lambda item: (
            str(item.get("consequence_effect", "")),
            str(item.get("outcome_event", "")),
            str(item.get("symbol_family", "")),
            str(item.get("action", "")),
        )
    )
    return rows


def write_outputs(rows: list[dict], output_dir: Path, memory_path: Path, events_path: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "dio_mini_memory_consequence_effect.csv"
    json_path = output_dir / "dio_mini_memory_consequence_effect.json"
    md_path = output_dir / "dio_mini_memory_consequence_effect.md"

    fields = list(rows[0].keys()) if rows else [
        "symbol_family",
        "action",
        "outcome_event",
        "event_count",
        "event_reward_sum",
        "event_avg_reward",
        "memory_family_count",
        *ACTION_FIELDS,
        "memory_avg_reward",
        "memory_trust_minus_caution",
        "consequence_effect",
        "passive_only",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    json_path.write_text(
        json.dumps(
            {
                "memory_path": str(memory_path),
                "events_path": str(events_path),
                "rows": rows,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    effect_counts: dict[str, int] = {}
    for row in rows:
        key = str(row.get("consequence_effect", "-") or "-")
        effect_counts[key] = effect_counts.get(key, 0) + 1

    lines = [
        "# DIO Mini Memory Consequence Effect",
        "",
        "## Grenze",
        "- liest Trade-Event-Report und Memory",
        "- schreibt kein Memory",
        "- beeinflusst keine Handlung",
        "",
        "## Effektklassen",
    ]
    if not effect_counts:
        lines.append("- keine Daten")
    else:
        for key, count in sorted(effect_counts.items()):
            lines.append(f"- {key}: {count}")
    lines.extend(["", "## Familien"])
    for row in rows:
        lines.append(
            f"- {row.get('symbol_family', '-')}: {row.get('action', '-')} "
            f"{row.get('outcome_event', '-')} events={row.get('event_count', 0)} "
            f"memory_count={row.get('memory_action_count', 0)} "
            f"trust={row.get('memory_trust', 0.0)} "
            f"caution={row.get('memory_caution', 0.0)} "
            f"effect={row.get('consequence_effect', '-')}"
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare Mini-DIO TP/SL events with memory action state")
    parser.add_argument("--memory", required=True)
    parser.add_argument("--events", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    memory_path = Path(args.memory)
    events_path = Path(args.events)
    rows = build_rows(memory_path, events_path)
    write_outputs(rows, Path(args.output_dir), memory_path, events_path)
    print(f"rows={len(rows)}")


if __name__ == "__main__":
    main()
