"""Report passive DIO_MINI sentence trace memory."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.semantic_memory import SemanticMemory


def _rows(memory: SemanticMemory) -> list[dict]:
    traces = memory.data.get("sentence_traces", {})
    rows = []
    for sentence_symbol, item in sorted(traces.items()):
        data = dict(item or {})
        rows.append(
            {
                "sentence_symbol": sentence_symbol,
                "contact_symbol": data.get("contact_symbol", ""),
                "contact_lage_state": data.get("contact_lage_state", ""),
                "symbol_family": data.get("symbol_family", ""),
                "episode_contact_state": data.get("episode_contact_state", ""),
                "count": int(data.get("count", 0) or 0),
                "reward_sum": float(data.get("reward_sum", 0.0) or 0.0),
                "actions": data.get("actions", ""),
                "passive_only": int(data.get("passive_only", 0) or 0),
            }
        )
    rows.sort(
        key=lambda item: (
            item["episode_contact_state"] != "kontakt_handlung_bestaetigt",
            -item["reward_sum"],
            -item["count"],
            item["sentence_symbol"],
        )
    )
    return rows


def _write(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "dio_mini_sentence_trace_report.csv"
    json_path = output_dir / "dio_mini_sentence_trace_report.json"
    md_path = output_dir / "dio_mini_sentence_trace_report.md"
    fieldnames = [
        "sentence_symbol",
        "contact_symbol",
        "contact_lage_state",
        "symbol_family",
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
    lines = ["# DIO Mini Sentence Trace Report", ""]
    for row in rows[:40]:
        lines.extend(
            [
                f"## {row['sentence_symbol']}",
                f"- contact: {row['contact_symbol']} ({row['contact_lage_state']})",
                f"- form: {row['symbol_family']}",
                f"- erleben: {row['episode_contact_state']}",
                f"- count: {row['count']}",
                f"- reward_sum: {row['reward_sum']:.6f}",
                f"- actions: {row['actions'] or '-'}",
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
    rows = _rows(memory)
    _write(rows, Path(args.output_dir))
    print(f"sentence_traces={len(rows)}")
    for row in rows[:12]:
        print(
            f"{row['sentence_symbol']} {row['contact_symbol']} "
            f"{row['symbol_family']} {row['episode_contact_state']} "
            f"reward={row['reward_sum']:.6f}"
        )


if __name__ == "__main__":
    main()
