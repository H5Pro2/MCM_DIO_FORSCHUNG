"""Report passive DIO_MINI contact-lage memory."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.semantic_memory import SemanticMemory


def _rows(memory: SemanticMemory) -> list[dict]:
    contact_lagen = memory.data.get("contact_lagen", {})
    rows = []
    for contact_id, item in sorted(contact_lagen.items()):
        data = dict(item or {})
        rows.append(
            {
                "contact_id": contact_id,
                "contact_symbol": data.get("contact_symbol", ""),
                "contact_lage_state": data.get("contact_lage_state", ""),
                "runs": int(data.get("runs", 0) or 0),
                "trades_total": int(data.get("trades_total", 0) or 0),
                "reward_total": float(data.get("reward_total", 0.0) or 0.0),
                "contact_reward_sum": float(data.get("contact_reward_sum", 0.0) or 0.0),
                "direct_positive_action": int(data.get("direct_positive_action", 0) or 0),
                "observation_to_positive_action": int(data.get("observation_to_positive_action", 0) or 0),
                "held_observation": int(data.get("held_observation", 0) or 0),
                "passive_only": int(data.get("passive_only", 0) or 0),
            }
        )
    rows.sort(
        key=lambda item: (
            item["contact_lage_state"],
            -item["contact_reward_sum"],
            item["contact_id"],
        )
    )
    return rows


def _write(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "dio_mini_contact_lagen_report.csv"
    json_path = output_dir / "dio_mini_contact_lagen_report.json"
    md_path = output_dir / "dio_mini_contact_lagen_report.md"
    fieldnames = [
        "contact_id",
        "contact_symbol",
        "contact_lage_state",
        "runs",
        "trades_total",
        "reward_total",
        "contact_reward_sum",
        "direct_positive_action",
        "observation_to_positive_action",
        "held_observation",
        "passive_only",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    lines = ["# DIO Mini Contact Lagen Report", ""]
    for row in rows:
        lines.extend(
            [
                f"## {row['contact_symbol'] or row['contact_id']}",
                f"- contact_id: {row['contact_id']}",
                f"- state: {row['contact_lage_state']}",
                f"- passive_only: {row['passive_only']}",
                f"- trades_total: {row['trades_total']}",
                f"- contact_reward_sum: {row['contact_reward_sum']:.6f}",
                f"- direct_positive_action: {row['direct_positive_action']}",
                f"- observation_to_positive_action: {row['observation_to_positive_action']}",
                f"- held_observation: {row['held_observation']}",
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
    for row in rows:
        print(
            f"{row['contact_symbol']} {row['contact_lage_state']} "
            f"reward={row['contact_reward_sum']:.6f} passive_only={row['passive_only']}"
        )


if __name__ == "__main__":
    main()
