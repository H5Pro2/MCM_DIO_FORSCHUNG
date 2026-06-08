"""Read passive sentence traces for one or more DIO form families."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.semantic_memory import SemanticMemory


def _load_rows(memory: SemanticMemory, families: set[str]) -> list[dict]:
    traces = memory.data.get("sentence_traces", {})
    rows = []
    for sentence_symbol, item in sorted(traces.items()):
        data = dict(item or {})
        family = str(data.get("symbol_family", "") or "")
        if families and family not in families:
            continue
        rows.append(
            {
                "sentence_symbol": sentence_symbol,
                "symbol_family": family,
                "contact_symbol": str(data.get("contact_symbol", "") or ""),
                "contact_lage_state": str(data.get("contact_lage_state", "") or ""),
                "episode_contact_state": str(data.get("episode_contact_state", "") or ""),
                "count": int(data.get("count", 0) or 0),
                "reward_sum": float(data.get("reward_sum", 0.0) or 0.0),
                "actions": str(data.get("actions", "") or ""),
                "passive_only": int(data.get("passive_only", 0) or 0),
            }
        )
    rows.sort(
        key=lambda item: (
            item["symbol_family"],
            item["episode_contact_state"] != "kontakt_handlung_bestaetigt",
            -item["reward_sum"],
            -item["count"],
            item["contact_lage_state"],
        )
    )
    return rows


def _write(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "dio_mini_form_sentence_read.csv"
    json_path = output_dir / "dio_mini_form_sentence_read.json"
    md_path = output_dir / "dio_mini_form_sentence_read.md"
    fieldnames = [
        "sentence_symbol",
        "symbol_family",
        "contact_symbol",
        "contact_lage_state",
        "episode_contact_state",
        "count",
        "reward_sum",
        "actions",
        "passive_only",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    lines = ["# DIO Mini Form Sentence Read", ""]
    current_family = None
    for row in rows:
        if row["symbol_family"] != current_family:
            current_family = row["symbol_family"]
            lines.extend([f"## {current_family}", ""])
        lines.extend(
            [
                f"- {row['sentence_symbol']}",
                f"  - contact: {row['contact_symbol']} ({row['contact_lage_state']})",
                f"  - erleben: {row['episode_contact_state']}",
                f"  - count: {row['count']}",
                f"  - reward_sum: {row['reward_sum']:.6f}",
                f"  - actions: {row['actions'] or '-'}",
                f"  - passive_only: {row['passive_only']}",
                "",
            ]
        )
    if not rows:
        lines.append("Keine Satzspuren gefunden.")
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory", required=True)
    parser.add_argument("--family", action="append", default=[])
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    families = {str(item).strip() for item in args.family if str(item).strip()}
    memory = SemanticMemory(args.memory)
    memory.load()
    rows = _load_rows(memory, families)
    _write(rows, Path(args.output_dir))
    print(f"sentence_trace_matches={len(rows)}")
    for row in rows[:20]:
        print(
            f"{row['symbol_family']} {row['sentence_symbol']} "
            f"{row['contact_lage_state']} {row['episode_contact_state']} "
            f"reward={row['reward_sum']:.6f}"
        )


if __name__ == "__main__":
    main()
