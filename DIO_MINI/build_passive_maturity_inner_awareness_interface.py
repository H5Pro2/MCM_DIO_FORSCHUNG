"""Build a passive maturity inner-awareness interface.

This file translates passive consequence-landscape comparison into a readable
inner-state interface. It is prepared for later Mini-DIO reading, but it is not
connected to runtime and must not influence action, gates, motorics, entries, or
future labels.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any


BOUNDARY = {
    "passive_only": True,
    "prepared_for_inner_awareness_reading": True,
    "read_by_mini_dio": False,
    "influences_action": False,
    "is_gate": False,
    "is_motoric": False,
    "is_entry_signal": False,
    "is_future_teacher": False,
}


def _f(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        number = float(value)
        if number != number:
            return default
        return number
    except (TypeError, ValueError):
        return default


def _i(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _inner_state(stability_state: str) -> str:
    mapping = {
        "family_stably_acted_carried": "inner_action_trust_seed",
        "family_stably_overcautious_carried": "inner_overcautious_carrying_pressure",
        "family_stably_cautious_potential": "inner_cautious_potential",
        "family_stably_open_potential": "inner_open_potential",
        "family_context_dependent_withholding": "inner_context_dependent_withholding",
        "family_context_switches_action_and_withholding": "inner_action_withholding_split",
    }
    return mapping.get(stability_state, "inner_maturity_unclassified")


def _dio_sentence(entry: dict[str, Any], inner_state: str) -> str:
    family = str(entry.get("symbol_family", "") or "-")
    direction = str(entry.get("dominant_direction", "") or "NONE")
    observations = _i(entry.get("observation_count"))
    reward = _f(entry.get("avg_afterlook_best_reward"))
    carry = _f(entry.get("avg_reflection_carry"))
    return f"{family}|{inner_state}|dir={direction}|obs={observations}|carry={carry:.6f}|after={reward:.6f}"


def _human_sentence(entry: dict[str, Any], inner_state: str) -> str:
    family = str(entry.get("symbol_family", "") or "-")
    direction = str(entry.get("dominant_direction", "") or "NONE")
    observations = _i(entry.get("observation_count"))
    reward = _f(entry.get("avg_afterlook_best_reward"))

    if inner_state == "inner_action_trust_seed":
        return (
            f"{family}: Diese Familie wurde bereits getragen gehandelt "
            f"({direction}, Beobachtungen={observations}, Nachblick={reward:.6f}). "
            "Das ist ein passiver Vertrauenskeim, keine Handlungsregel."
        )
    if inner_state == "inner_overcautious_carrying_pressure":
        return (
            f"{family}: Diese Familie wurde mehrfach getragen wahrgenommen, "
            f"aber zurueckgehalten ({direction}, Beobachtungen={observations}, Nachblick={reward:.6f}). "
            "Das ist passiver Reifungsdruck gegen Uebervorsicht."
        )
    if inner_state == "inner_cautious_potential":
        return (
            f"{family}: Diese Familie bleibt vorsichtig, zeigt aber spaeter tragendes Potential "
            f"({direction}, Beobachtungen={observations}, Nachblick={reward:.6f})."
        )
    if inner_state == "inner_open_potential":
        return (
            f"{family}: Diese Familie bleibt offen und zeigt spaeter tragendes Potential "
            f"({direction}, Beobachtungen={observations}, Nachblick={reward:.6f})."
        )
    if inner_state == "inner_action_withholding_split":
        return (
            f"{family}: Diese Familie wechselt zwischen getragener Handlung und Zurueckhaltung "
            f"({direction}, Beobachtungen={observations}, Nachblick={reward:.6f})."
        )
    if inner_state == "inner_context_dependent_withholding":
        return (
            f"{family}: Diese Familie wird kontextabhaengig zurueckgehalten "
            f"({direction}, Beobachtungen={observations}, Nachblick={reward:.6f})."
        )
    return (
        f"{family}: Diese Familie ist passiv noch nicht eindeutig eingeordnet "
        f"({direction}, Beobachtungen={observations}, Nachblick={reward:.6f})."
    )


def build_interface(compare_report: dict[str, Any]) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for source in compare_report.get("entries", []) or []:
        stability_state = str(source.get("family_stability_state", "") or "")
        state = _inner_state(stability_state)
        entry = {
            "symbol_family": str(source.get("symbol_family", "") or ""),
            "inner_awareness_state": state,
            "family_stability_state": stability_state,
            "dominant_direction": str(source.get("dominant_direction", "") or "NONE"),
            "observation_count": _i(source.get("observation_count")),
            "avg_afterlook_best_reward": _f(source.get("avg_afterlook_best_reward")),
            "avg_reflection_carry": _f(source.get("avg_reflection_carry")),
            "avg_world_carry": _f(source.get("avg_world_carry")),
            "class_counts": dict(source.get("class_counts", {}) or {}),
            "direction_counts": dict(source.get("direction_counts", {}) or {}),
            "dio_syntax": "",
            "human_sentence": "",
            **BOUNDARY,
        }
        entry["dio_syntax"] = _dio_sentence(entry, state)
        entry["human_sentence"] = _human_sentence(entry, state)
        entries.append(entry)

    entries.sort(
        key=lambda item: (
            item["inner_awareness_state"] == "inner_overcautious_carrying_pressure",
            item["inner_awareness_state"] == "inner_action_trust_seed",
            item["observation_count"],
            item["avg_afterlook_best_reward"],
            item["avg_reflection_carry"],
        ),
        reverse=True,
    )
    counts = Counter(entry["inner_awareness_state"] for entry in entries)
    return {
        "boundary": dict(BOUNDARY),
        "source_summary": dict(compare_report.get("summary", {}) or {}),
        "summary": {
            "families": len(entries),
            "inner_awareness_counts": dict(counts),
            "avg_afterlook_best_reward": mean([e["avg_afterlook_best_reward"] for e in entries] or [0.0]),
            "avg_reflection_carry": mean([e["avg_reflection_carry"] for e in entries] or [0.0]),
            "avg_world_carry": mean([e["avg_world_carry"] for e in entries] or [0.0]),
        },
        "entries": entries,
    }


def _write_outputs(interface: dict[str, Any], output_dir: Path, memory_path: Path | None) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_text = json.dumps(interface, indent=2, sort_keys=True)
    (output_dir / "passive_maturity_inner_awareness_interface.json").write_text(json_text, encoding="utf-8")
    if memory_path is not None:
        memory_path.parent.mkdir(parents=True, exist_ok=True)
        memory_path.write_text(json_text, encoding="utf-8")

    entries = list(interface.get("entries", []) or [])
    csv_path = output_dir / "passive_maturity_inner_awareness_interface.csv"
    if entries:
        flat_rows = []
        for entry in entries:
            row = dict(entry)
            row["class_counts"] = json.dumps(row.get("class_counts", {}), sort_keys=True)
            row["direction_counts"] = json.dumps(row.get("direction_counts", {}), sort_keys=True)
            flat_rows.append(row)
        with csv_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(flat_rows[0].keys()))
            writer.writeheader()
            writer.writerows(flat_rows)
    else:
        csv_path.write_text("symbol_family,inner_awareness_state\n", encoding="utf-8")

    summary = interface.get("summary", {})
    lines = [
        "# Mini-DIO Passive Maturity Inner Awareness Interface",
        "",
        "- boundary: prepared for inner awareness reading; not read by Mini-DIO; no action; no gate",
        "",
        "## Summary",
        f"- families: {summary.get('families', 0)}",
        f"- inner_awareness_counts: {summary.get('inner_awareness_counts', {})}",
        f"- avg_afterlook_best_reward: {summary.get('avg_afterlook_best_reward', 0.0):.9f}",
        f"- avg_reflection_carry: {summary.get('avg_reflection_carry', 0.0):.9f}",
        f"- avg_world_carry: {summary.get('avg_world_carry', 0.0):.9f}",
        "",
        "## Top Inner Sentences",
    ]
    for entry in entries[:30]:
        lines.append(f"- {entry['human_sentence']}")
    lines.extend(
        [
            "",
            "## Grenze",
            "- keine Runtime-Anbindung",
            "- keine Entry-Regel",
            "- keine Motorik",
            "- keine Future-Teacher-Mechanik",
            "- nur vorbereitete Innenwahrnehmung",
        ]
    )
    (output_dir / "passive_maturity_inner_awareness_interface.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )
    (output_dir / "passive_maturity_inner_awareness_interface.txt").write_text(
        "\n".join(entry["dio_syntax"] for entry in entries) + ("\n" if entries else ""),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare-report", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--memory", default="")
    args = parser.parse_args()

    interface = build_interface(_read_json(Path(args.compare_report)))
    memory_path = Path(args.memory) if args.memory else None
    _write_outputs(interface, Path(args.output_dir), memory_path)
    print(json.dumps(interface["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
