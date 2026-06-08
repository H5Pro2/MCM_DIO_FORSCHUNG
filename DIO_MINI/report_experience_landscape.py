"""Report the passive DIO_MINI experience landscape."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.read_sentence_conflicts import _load_grouped, _summaries
from DIO_MINI.semantic_memory import SemanticMemory


SECTION_ORDER = [
    "form_erleben_konflikt",
    "form_bestaetigungsspur",
    "form_belastungsspur",
    "form_beobachtungsspur",
]

SECTION_TITLES = {
    "form_erleben_konflikt": "Konfliktfamilien",
    "form_bestaetigungsspur": "Bestaetigte Familien",
    "form_belastungsspur": "Belastete Familien",
    "form_beobachtungsspur": "Beobachtende Familien",
}


def _bucket(rows: list[dict]) -> dict[str, list[dict]]:
    buckets = {key: [] for key in SECTION_ORDER}
    for row in rows:
        state = str(row.get("conflict_state", "") or "form_beobachtungsspur")
        buckets.setdefault(state, []).append(row)
    for state, items in buckets.items():
        items.sort(
            key=lambda item: (
                -abs(float(item.get("burden_reward_sum", 0.0) or 0.0)),
                -float(item.get("positive_reward_sum", 0.0) or 0.0),
                -float(item.get("total_reward_sum", 0.0) or 0.0),
                str(item.get("symbol_family", "")),
            )
        )
    return buckets


def _write(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    buckets = _bucket(rows)
    csv_path = output_dir / "dio_mini_experience_landscape.csv"
    json_path = output_dir / "dio_mini_experience_landscape.json"
    md_path = output_dir / "dio_mini_experience_landscape.md"

    fieldnames = [
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
    ordered_rows = []
    for state in SECTION_ORDER:
        ordered_rows.extend(buckets.get(state, []))
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ordered_rows)
    json_path.write_text(json.dumps(ordered_rows, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Experience Landscape", ""]
    lines.extend(
        [
            "Diese Auswertung ist passiv.",
            "Sie beschreibt gespeicherte Satzspuren, ohne Handlung abzuleiten.",
            "",
            "## Uebersicht",
            "",
        ]
    )
    for state in SECTION_ORDER:
        lines.append(f"- {SECTION_TITLES[state]}: {len(buckets.get(state, []))}")
    lines.append("")
    for state in SECTION_ORDER:
        items = buckets.get(state, [])
        lines.extend([f"## {SECTION_TITLES[state]}", ""])
        if not items:
            lines.extend(["Keine Familien.", ""])
            continue
        for row in items[:12]:
            lines.extend(
                [
                    f"### {row['symbol_family']}",
                    f"- trace_count: {row['trace_count']}",
                    f"- contact_lage_states: {row['contact_lage_states'] or '-'}",
                    f"- episode_contact_states: {row['episode_contact_states'] or '-'}",
                    f"- positive_count: {row['positive_count']}",
                    f"- burden_count: {row['burden_count']}",
                    f"- positive_reward_sum: {float(row['positive_reward_sum']):.6f}",
                    f"- burden_reward_sum: {float(row['burden_reward_sum']):.6f}",
                    f"- total_reward_sum: {float(row['total_reward_sum']):.6f}",
                    f"- actions: {row['actions'] or '-'}",
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
    buckets = _bucket(rows)
    print(
        " ".join(
            f"{state}={len(buckets.get(state, []))}"
            for state in SECTION_ORDER
        )
    )


if __name__ == "__main__":
    main()
