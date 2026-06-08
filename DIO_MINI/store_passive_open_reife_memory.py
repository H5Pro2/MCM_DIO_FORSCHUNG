"""Store passive open maturity ratings in a separated Mini-DIO memory file.

This memory is a passive artifact. Mini-DIO does not read it for action,
gates, or motorics.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path


def _safe_float(value: object) -> float:
    try:
        value = float(value or 0.0)
    except Exception:
        value = 0.0
    if value != value:
        return 0.0
    return value


def _safe_int(value: object) -> int:
    try:
        return int(float(value or 0))
    except Exception:
        return 0


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _split_csv(value: object) -> list[str]:
    return [item.strip() for item in str(value or "").split(",") if item.strip()]


def _atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f"{path.name}.tmp")
    temp_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temp_path, path)


def _write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    if rows:
        ordered = list(fields)
        for row in rows:
            for key in row.keys():
                if key not in ordered:
                    ordered.append(key)
        fields = ordered
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _memory_note(item: dict) -> str:
    family_action = str(item.get("family_action", "") or "-")
    score = _safe_float(item.get("passive_reife_score"))
    reward = _safe_float(item.get("event_reward_sum"))
    return (
        f"{family_action}: passive offene Reifespur; "
        f"Score={score:.6f}; Konsequenz={reward:.6f}; "
        "keine Handlung, keine Motorik."
    )


def build_memory(rating_rows: list[dict], source_path: Path) -> dict:
    entries: list[dict] = []
    for row in rating_rows:
        state = str(row.get("passive_reife_rating_state", "") or "")
        if state != "passive_reife_carried_candidate":
            continue
        item = {
            "family_action": str(row.get("family_action", "") or ""),
            "symbol_family": str(row.get("symbol_family", "") or ""),
            "action": str(row.get("action", "") or ""),
            "passive_open_reife_state": state,
            "passive_reife_score": round(_safe_float(row.get("passive_reife_score")), 9),
            "consequence_support": round(_safe_float(row.get("consequence_support")), 9),
            "multisensory_stability": round(_safe_float(row.get("multisensory_stability")), 9),
            "visual_stability": round(_safe_float(row.get("visual_stability")), 9),
            "auditory_stability": round(_safe_float(row.get("auditory_stability")), 9),
            "mcm_stability": round(_safe_float(row.get("mcm_stability")), 9),
            "recurrence_support": round(_safe_float(row.get("recurrence_support")), 9),
            "source_support": round(_safe_float(row.get("source_support")), 9),
            "temporal_contact": round(_safe_float(row.get("temporal_contact")), 9),
            "episode_count": _safe_int(row.get("episode_count")),
            "trade_count": _safe_int(row.get("trade_count")),
            "tp_count": _safe_int(row.get("tp_count")),
            "sl_count": _safe_int(row.get("sl_count")),
            "event_reward_sum": round(_safe_float(row.get("event_reward_sum")), 9),
            "run_labels": _split_csv(row.get("run_labels")),
            "source_roots": _split_csv(row.get("source_roots")),
            "passive_only": True,
            "writes_training_memory": False,
            "read_by_mini_dio": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
        }
        item["memory_note"] = _memory_note(item)
        entries.append(item)

    entries.sort(key=lambda item: (-_safe_float(item.get("passive_reife_score")), str(item.get("family_action", ""))))
    return {
        "schema": "dio_mini_passive_open_reife_memory.v1",
        "source_rating": str(source_path),
        "boundary": {
            "passive_only": True,
            "writes_training_memory": False,
            "read_by_mini_dio": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
            "is_future_teacher": False,
        },
        "summary": {
            "entry_count": len(entries),
            "family_actions": [item["family_action"] for item in entries],
            "event_reward_sum": round(sum(_safe_float(item.get("event_reward_sum")) for item in entries), 9),
            "avg_passive_reife_score": round(
                sum(_safe_float(item.get("passive_reife_score")) for item in entries) / max(1, len(entries)),
                9,
            ),
            "avg_multisensory_stability": round(
                sum(_safe_float(item.get("multisensory_stability")) for item in entries) / max(1, len(entries)),
                9,
            ),
        },
        "entries": entries,
    }


def write_outputs(memory: dict, output_json: Path, output_dir: Path | None) -> None:
    _atomic_write_json(output_json, memory)
    if output_dir is None:
        return
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "dio_mini_passive_open_reife_memory_entries.csv"
    md_path = output_dir / "dio_mini_passive_open_reife_memory.md"
    txt_path = output_dir / "dio_mini_passive_open_reife_memory.txt"

    csv_rows = []
    for item in memory["entries"]:
        row = dict(item)
        row["run_labels"] = ",".join(row["run_labels"])
        row["source_roots"] = ",".join(row["source_roots"])
        csv_rows.append(row)
    _write_csv(csv_path, csv_rows, ["family_action", "passive_reife_score", "event_reward_sum"])

    lines = [
        "# Mini-DIO Passive Open Reife Memory",
        "",
        f"- json: `{output_json}`",
        f"- source_rating: `{memory['source_rating']}`",
        "",
        "## Summary",
    ]
    for key, value in memory["summary"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Entries"])
    if not memory["entries"]:
        lines.append("- keine Eintraege")
    for item in memory["entries"]:
        lines.append(f"- {item['memory_note']}")
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Memory-Ablage",
            "- Mini-DIO liest diese Datei nicht",
            "- keine Handlung",
            "- kein Trainingsmemory",
            "- kein Gate",
            "- kein Zukunftslehrer",
        ]
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    txt_path.write_text("\n".join(item["memory_note"] for item in memory["entries"]) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rating", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, default=Path("bot_memory/dio_mini_passive_open_reife_memory.json"))
    parser.add_argument("--output-dir", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rating_rows = _read_csv(args.rating)
    memory = build_memory(rating_rows, args.rating)
    write_outputs(memory, args.output_json, args.output_dir)
    summary = memory["summary"]
    print(
        "passive_open_reife_memory "
        f"entries={summary['entry_count']} "
        f"reward={summary['event_reward_sum']} "
        f"avg_score={summary['avg_passive_reife_score']}"
    )
    for item in memory["entries"]:
        print(f"entry {item['family_action']} score={item['passive_reife_score']} reward={item['event_reward_sum']}")


if __name__ == "__main__":
    main()
