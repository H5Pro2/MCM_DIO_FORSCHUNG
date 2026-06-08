"""Read passive stable direction traces from DIO_MINI sentence memory."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.read_sentence_conflicts import BURDEN_STATES, POSITIVE_STATES, _action_counts, _load_grouped
from DIO_MINI.semantic_memory import SemanticMemory


TRADE_ACTIONS = {"LONG", "SHORT"}


def _summaries(grouped: dict[str, list[dict]]) -> list[dict]:
    rows = []
    for family, traces in grouped.items():
        positive_actions: dict[str, int] = {}
        all_actions: dict[str, int] = {}
        positive_reward = 0.0
        burden_reward = 0.0
        positive_count = 0
        burden_count = 0
        positive_contacts = set()
        burden_contacts = set()
        positive_states = set()
        burden_states = set()
        for trace in traces:
            state = str(trace.get("episode_contact_state", "") or "")
            contact_state = str(trace.get("contact_lage_state", "") or "")
            reward = float(trace.get("reward_sum", 0.0) or 0.0)
            count = int(trace.get("count", 0) or 0)
            actions = _action_counts(str(trace.get("actions", "") or ""))
            for action, action_count in actions.items():
                all_actions[action] = all_actions.get(action, 0) + action_count
            if state in POSITIVE_STATES:
                positive_reward += reward
                positive_count += count
                positive_contacts.add(contact_state)
                positive_states.add(state)
                for action, action_count in actions.items():
                    if action in TRADE_ACTIONS:
                        positive_actions[action] = positive_actions.get(action, 0) + action_count
            if state in BURDEN_STATES:
                burden_reward += reward
                burden_count += count
                burden_contacts.add(contact_state)
                burden_states.add(state)
        trade_actions = {action: count for action, count in positive_actions.items() if count > 0}
        if len(trade_actions) == 1 and len(positive_contacts) > 1 and not burden_count:
            stable_action = next(iter(trade_actions))
            stability_state = "kontaktlagenuebergreifend_bestaetigt"
        elif len(trade_actions) == 1 and positive_contacts and not burden_count:
            stable_action = next(iter(trade_actions))
            stability_state = "lokal_bestaetigt"
        elif len(trade_actions) == 1 and len(positive_contacts) > 1 and burden_count:
            stable_action = next(iter(trade_actions))
            stability_state = "kontaktlagenuebergreifend_mit_belastung"
        elif len(trade_actions) == 1 and positive_contacts and burden_count:
            stable_action = next(iter(trade_actions))
            stability_state = "lokal_bestaetigt_mit_belastung"
        elif len(trade_actions) > 1:
            stable_action = "mixed"
            stability_state = "richtungs_konflikt"
        elif positive_count > 0:
            stable_action = "-"
            stability_state = "bestaetigt_ohne_tradewort"
        elif burden_count > 0:
            stable_action = "-"
            stability_state = "belastet"
        else:
            stable_action = "-"
            stability_state = "beobachtung"
        rows.append(
            {
                "symbol_family": family,
                "stability_state": stability_state,
                "stable_action": stable_action,
                "positive_contact_count": len(positive_contacts),
                "positive_contact_lage_states": ",".join(sorted(positive_contacts)),
                "burden_contact_count": len(burden_contacts),
                "burden_contact_lage_states": ",".join(sorted(burden_contacts)),
                "positive_count": positive_count,
                "burden_count": burden_count,
                "positive_reward_sum": round(positive_reward, 6),
                "burden_reward_sum": round(burden_reward, 6),
                "positive_actions": ",".join(f"{key}:{value}" for key, value in sorted(positive_actions.items())),
                "all_actions": ",".join(f"{key}:{value}" for key, value in sorted(all_actions.items())),
                "passive_only": 1,
            }
        )
    rows.sort(
        key=lambda item: (
            item["stability_state"] != "kontaktlagenuebergreifend_bestaetigt",
            item["stability_state"] != "lokal_bestaetigt",
            -int(item["positive_contact_count"]),
            -float(item["positive_reward_sum"]),
            str(item["symbol_family"]),
        )
    )
    return rows


def _write(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "dio_mini_stable_direction_traces.csv"
    json_path = output_dir / "dio_mini_stable_direction_traces.json"
    md_path = output_dir / "dio_mini_stable_direction_traces.md"
    fieldnames = [
        "symbol_family",
        "stability_state",
        "stable_action",
        "positive_contact_count",
        "positive_contact_lage_states",
        "burden_contact_count",
        "burden_contact_lage_states",
        "positive_count",
        "burden_count",
        "positive_reward_sum",
        "burden_reward_sum",
        "positive_actions",
        "all_actions",
        "passive_only",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Stable Direction Traces", ""]
    lines.extend(
        [
            "Diese Auswertung ist passiv.",
            "Sie zeigt, ob eine Formfamilie ueber mehrere Kontaktlagen dieselbe Richtung traegt.",
            "",
        ]
    )
    for row in rows[:24]:
        lines.extend(
            [
                f"## {row['symbol_family']}",
                f"- state: {row['stability_state']}",
                f"- stable_action: {row['stable_action']}",
                f"- positive_contact_count: {row['positive_contact_count']}",
                f"- positive_contact_lage_states: {row['positive_contact_lage_states'] or '-'}",
                f"- burden_contact_count: {row['burden_contact_count']}",
                f"- positive_reward_sum: {float(row['positive_reward_sum']):.6f}",
                f"- burden_reward_sum: {float(row['burden_reward_sum']):.6f}",
                f"- positive_actions: {row['positive_actions'] or '-'}",
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
    rows = _summaries(_load_grouped(memory))
    _write(rows, Path(args.output_dir))
    multi = [row for row in rows if row["stability_state"] == "kontaktlagenuebergreifend_bestaetigt"]
    local = [row for row in rows if row["stability_state"] == "lokal_bestaetigt"]
    conflict = [
        row
        for row in rows
        if row["stability_state"]
        in ("richtungs_konflikt", "kontaktlagenuebergreifend_mit_belastung", "lokal_bestaetigt_mit_belastung")
    ]
    print(
        f"families={len(rows)} "
        f"kontaktlagenuebergreifend={len(multi)} "
        f"lokal={len(local)} "
        f"conflict_or_burden={len(conflict)}"
    )
    for row in (multi + local)[:12]:
        print(
            f"{row['symbol_family']} {row['stable_action']} "
            f"contacts={row['positive_contact_count']} reward={row['positive_reward_sum']}"
        )


if __name__ == "__main__":
    main()
