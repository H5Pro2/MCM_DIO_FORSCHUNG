"""Create a passive Mini-DIO inner maturity memory file.

This turns repeated inner maturity diagnostics into a separated memory artifact.
The artifact is not consumed by Mini-DIO action code. It is a readable passive
record of inner trust, carefulness, and reorganization traces.
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
        value = 0.0
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


def _memory_state(row: dict) -> str:
    transition = str(row.get("transition_state", "") or "")
    if transition == "inner_seed_repeats_stably":
        return "passive_inner_memory_stable"
    if transition == "inner_seed_reorganizes":
        return "passive_inner_memory_reorganizing"
    return "passive_inner_memory_local"


def _memory_note(row: dict, state: str) -> str:
    family = str(row.get("passive_family_action", "") or "-")
    seeds = str(row.get("seeds", "") or "-")
    reward = _safe_float(row.get("real_reward_sum"))
    if state == "passive_inner_memory_stable":
        return f"{family}: innere Lesung wiederholt sich stabil als {seeds}; Konsequenzsumme={reward:.6f}."
    if state == "passive_inner_memory_reorganizing":
        return f"{family}: innere Lesung reorganisiert sich ({seeds}); diese Spur bleibt entwickelnd."
    return f"{family}: innere Lesung ist lokal ({seeds}); noch keine stabile Wiederkehr."


def build_memory(family_rows: list[dict], seed_rows: list[dict]) -> dict:
    entries: list[dict] = []
    stable_entries: list[dict] = []
    reorganizing_entries: list[dict] = []
    local_entries: list[dict] = []

    for row in family_rows:
        state = _memory_state(row)
        item = {
            "passive_family_action": str(row.get("passive_family_action", "") or ""),
            "inner_memory_state": state,
            "map_count": _safe_int(row.get("map_count")),
            "map_labels": _split_csv(row.get("map_labels")),
            "source_labels": _split_csv(row.get("source_labels")),
            "seeds": _split_csv(row.get("seeds")),
            "actions": _split_csv(row.get("actions")),
            "trace_count": _safe_int(row.get("trace_count")),
            "avg_similarity": round(_safe_float(row.get("avg_similarity")), 9),
            "avg_mcm_similarity": round(_safe_float(row.get("avg_mcm_similarity")), 9),
            "real_reward_sum": round(_safe_float(row.get("real_reward_sum")), 9),
            "transition_state": str(row.get("transition_state", "") or ""),
            "memory_note": "",
            "passive_only": True,
        }
        item["memory_note"] = _memory_note(row, state)
        entries.append(item)
        if state == "passive_inner_memory_stable":
            stable_entries.append(item)
        elif state == "passive_inner_memory_reorganizing":
            reorganizing_entries.append(item)
        else:
            local_entries.append(item)

    seed_summary = []
    for row in seed_rows:
        seed_summary.append(
            {
                "inner_maturity_seed": str(row.get("inner_maturity_seed", "") or ""),
                "map_count": _safe_int(row.get("map_count")),
                "map_labels": _split_csv(row.get("map_labels")),
                "source_labels": _split_csv(row.get("source_labels")),
                "family_count": _safe_int(row.get("family_count")),
                "families": _split_csv(row.get("families")),
                "actions": _split_csv(row.get("actions")),
                "trace_count": _safe_int(row.get("trace_count")),
                "avg_similarity": round(_safe_float(row.get("avg_similarity")), 9),
                "avg_mcm_similarity": round(_safe_float(row.get("avg_mcm_similarity")), 9),
                "real_reward_sum": round(_safe_float(row.get("real_reward_sum")), 9),
                "seed_stability": str(row.get("seed_stability", "") or ""),
                "passive_only": True,
            }
        )

    return {
        "schema": "dio_mini_passive_inner_maturity_memory.v1",
        "boundary": {
            "writes_training_memory": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
            "is_future_teacher": False,
            "read_by_mini_dio": False,
        },
        "summary": {
            "entry_count": len(entries),
            "stable_entry_count": len(stable_entries),
            "reorganizing_entry_count": len(reorganizing_entries),
            "local_entry_count": len(local_entries),
            "seed_count": len(seed_summary),
        },
        "seed_summary": seed_summary,
        "entries": entries,
        "stable_entries": stable_entries,
        "reorganizing_entries": reorganizing_entries,
        "local_entries": local_entries,
    }


def _atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f"{path.name}.tmp")
    temp_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temp_path, path)


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(memory: dict, output_json: Path, output_dir: Path | None) -> None:
    _atomic_write_json(output_json, memory)
    if output_dir is None:
        return
    output_dir.mkdir(parents=True, exist_ok=True)

    entries_csv = output_dir / "dio_mini_passive_inner_maturity_memory_entries.csv"
    seeds_csv = output_dir / "dio_mini_passive_inner_maturity_memory_seeds.csv"
    md_path = output_dir / "dio_mini_passive_inner_maturity_memory.md"
    txt_path = output_dir / "dio_mini_passive_inner_maturity_memory.txt"

    entry_rows = []
    for item in memory["entries"]:
        row = dict(item)
        row["map_labels"] = ",".join(row["map_labels"])
        row["source_labels"] = ",".join(row["source_labels"])
        row["seeds"] = ",".join(row["seeds"])
        row["actions"] = ",".join(row["actions"])
        entry_rows.append(row)
    seed_rows = []
    for item in memory["seed_summary"]:
        row = dict(item)
        row["map_labels"] = ",".join(row["map_labels"])
        row["source_labels"] = ",".join(row["source_labels"])
        row["families"] = ",".join(row["families"])
        row["actions"] = ",".join(row["actions"])
        seed_rows.append(row)

    _write_csv(entries_csv, entry_rows, ["passive_family_action", "inner_memory_state"])
    _write_csv(seeds_csv, seed_rows, ["inner_maturity_seed", "map_count"])

    lines = ["# DIO Mini Passive Inner Maturity Memory", ""]
    lines.append(f"- json: {output_json}")
    lines.extend(["", "## Summary"])
    for key, value in memory["summary"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Stable Entries"])
    if not memory["stable_entries"]:
        lines.append("- keine stabilen Eintraege")
    for item in memory["stable_entries"]:
        lines.append(f"- {item['memory_note']}")
    lines.extend(["", "## Reorganizing Entries"])
    if not memory["reorganizing_entries"]:
        lines.append("- keine reorganisierenden Eintraege")
    for item in memory["reorganizing_entries"]:
        lines.append(f"- {item['memory_note']}")
    lines.extend(["", "## Local Entries"])
    if not memory["local_entries"]:
        lines.append("- keine lokalen Eintraege")
    for item in memory["local_entries"]:
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
    md_path.write_text("\n".join(lines), encoding="utf-8")
    txt_path.write_text("\n".join(item["memory_note"] for item in memory["entries"]), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create passive Mini-DIO inner maturity memory")
    parser.add_argument("--family-stability", required=True)
    parser.add_argument("--seed-stability", required=True)
    parser.add_argument("--output-json", default="bot_memory/dio_mini_passive_inner_maturity_memory.json")
    parser.add_argument("--output-dir")
    args = parser.parse_args()

    family_rows = _read_csv(Path(args.family_stability))
    seed_rows = _read_csv(Path(args.seed_stability))
    memory = build_memory(family_rows, seed_rows)
    write_outputs(memory, Path(args.output_json), Path(args.output_dir) if args.output_dir else None)
    summary = memory["summary"]
    print(
        "passive_inner_maturity_memory "
        f"entries={summary['entry_count']} stable={summary['stable_entry_count']} "
        f"reorganizing={summary['reorganizing_entry_count']} local={summary['local_entry_count']}"
    )
    for item in memory["stable_entries"][:12]:
        print(f"stable {item['passive_family_action']} seeds={','.join(item['seeds'])}")
    for item in memory["reorganizing_entries"][:12]:
        print(f"reorganizing {item['passive_family_action']} seeds={','.join(item['seeds'])}")


if __name__ == "__main__":
    main()
