"""Store passive Mini-DIO recurrence maturity candidates separately.

This memory is diagnostic only. It stores which Mini-DIO syntax families stay
stable, remain meaning-near under variation, or fragment under temporal drift.
Mini-DIO must not read this file for action, gates, or motorics.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import time
from pathlib import Path


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value if value not in (None, "") else default)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(float(value if value not in (None, "") else default))
    except Exception:
        return default


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = list(fields)
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=ordered)
        writer.writeheader()
        writer.writerows(rows)


def _atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f"{path.name}.tmp.{os.getpid()}.{int(time.time() * 1000)}")
    temp_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temp_path, path)


def _hash_base36(text: str) -> str:
    value = 2166136261
    for char in text:
        value ^= ord(char)
        value = (value * 16777619) & 0xFFFFFFFF
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    if value == 0:
        return "0"
    chars: list[str] = []
    while value:
        value, rest = divmod(value, 36)
        chars.append(alphabet[rest])
    return "".join(reversed(chars))


def make_candidate_symbol(family: str, state: str, meaning_rate: float, temporal_fragility: float) -> str:
    meaning_band = int(max(0.0, min(1.0, meaning_rate)) * 9)
    temporal_band = int(max(0.0, min(1.0, temporal_fragility)) * 9)
    raw = f"{family}|{state}|m{meaning_band}|t{temporal_band}"
    return f"dio_recur_{_hash_base36(raw)[:10]}"


def _candidate_note(item: dict) -> str:
    return (
        f"{item['reference_family']}: passive Wiederkehrspur; "
        f"state={item['passive_reife_state']}; "
        f"Sinn-Erhalt={item['meaning_preservation_rate']:.6f}; "
        f"Zeitfragilitaet={item['temporal_fragility']:.6f}; "
        "keine Handlung, keine Motorik."
    )


def build_memory(rows: list[dict], source_path: Path) -> dict:
    entries: list[dict] = []
    for row in rows:
        family = str(row.get("reference_family", "") or "")
        state = str(row.get("passive_reife_state", "") or "offen_reifend")
        meaning_rate = _safe_float(row.get("meaning_preservation_rate"))
        temporal_fragility = _safe_float(row.get("temporal_fragility"))
        item = {
            "recurrence_maturity_symbol": make_candidate_symbol(family, state, meaning_rate, temporal_fragility),
            "reference_family": family,
            "passive_reife_state": state,
            "episodes": _safe_int(row.get("episodes")),
            "stable_recurrence_count": _safe_int(row.get("stable_recurrence_count")),
            "fine_signature_shift_count": _safe_int(row.get("fine_signature_shift_count")),
            "same_meaning_variant_count": _safe_int(row.get("same_meaning_variant_count")),
            "far_kinship_same_direction_count": _safe_int(row.get("far_kinship_same_direction_count")),
            "new_preconscious_pattern_count": _safe_int(row.get("new_preconscious_pattern_count")),
            "same_family_count": _safe_int(row.get("same_family_count")),
            "same_action_count": _safe_int(row.get("same_action_count")),
            "stable_recurrence_rate": round(_safe_float(row.get("stable_recurrence_rate")), 9),
            "meaning_preservation_rate": round(meaning_rate, 9),
            "variant_capacity_rate": round(_safe_float(row.get("variant_capacity_rate")), 9),
            "conflict_or_new_rate": round(_safe_float(row.get("conflict_or_new_rate")), 9),
            "avg_sense_abs_delta_sum": round(_safe_float(row.get("avg_sense_abs_delta_sum")), 9),
            "max_sense_abs_delta_sum": round(_safe_float(row.get("max_sense_abs_delta_sum")), 9),
            "temporal_probe23_same_family": _safe_int(row.get("temporal_probe23_same_family")),
            "temporal_probe23_same_action": _safe_int(row.get("temporal_probe23_same_action")),
            "temporal_probe23_avg_delta": round(_safe_float(row.get("temporal_probe23_avg_delta")), 9),
            "temporal_fragility": round(temporal_fragility, 9),
            "probe_trace": str(row.get("probe_trace", "") or ""),
            "passive_only": True,
            "writes_training_memory": False,
            "read_by_mini_dio": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
            "is_future_teacher": False,
        }
        item["memory_note"] = _candidate_note(item)
        entries.append(item)

    entries.sort(
        key=lambda item: (
            -_safe_float(item.get("meaning_preservation_rate")),
            -_safe_float(item.get("stable_recurrence_rate")),
            str(item.get("reference_family", "")),
        )
    )
    return {
        "schema": "dio_mini_passive_recurrence_maturity_candidates.v1",
        "source_reifezaehlung": str(source_path),
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
            "states": _state_counts(entries),
            "avg_meaning_preservation_rate": round(
                sum(_safe_float(item.get("meaning_preservation_rate")) for item in entries) / max(1, len(entries)),
                9,
            ),
            "avg_stable_recurrence_rate": round(
                sum(_safe_float(item.get("stable_recurrence_rate")) for item in entries) / max(1, len(entries)),
                9,
            ),
            "avg_temporal_fragility": round(
                sum(_safe_float(item.get("temporal_fragility")) for item in entries) / max(1, len(entries)),
                9,
            ),
        },
        "entries": entries,
    }


def _state_counts(entries: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in entries:
        state = str(item.get("passive_reife_state", "") or "-")
        counts[state] = counts.get(state, 0) + 1
    return dict(sorted(counts.items()))


def write_outputs(memory: dict, output_json: Path, output_dir: Path | None) -> None:
    _atomic_write_json(output_json, memory)
    if output_dir is None:
        return
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = list(memory.get("entries", []) or [])
    entries_csv = output_dir / "dio_mini_passive_recurrence_maturity_candidates.csv"
    md_path = output_dir / "dio_mini_passive_recurrence_maturity_candidates.md"
    txt_path = output_dir / "dio_mini_passive_recurrence_maturity_candidates.txt"

    _write_csv(
        entries_csv,
        rows,
        [
            "recurrence_maturity_symbol",
            "reference_family",
            "passive_reife_state",
            "meaning_preservation_rate",
            "stable_recurrence_rate",
            "temporal_fragility",
        ],
    )

    lines = [
        "# Mini-DIO Passive Recurrence Maturity Candidates",
        "",
        f"- json: `{output_json}`",
        f"- source_reifezaehlung: `{memory['source_reifezaehlung']}`",
        "",
        "## Summary",
    ]
    for key, value in memory["summary"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Entries"])
    if not rows:
        lines.append("- keine Eintraege")
    for item in rows:
        lines.append(f"- {item['memory_note']}")
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Kandidaten-Ablage",
            "- Mini-DIO liest diese Datei nicht",
            "- keine Handlung",
            "- kein Trainingsmemory",
            "- kein Gate",
        ]
    )
    text = "\n".join(lines) + "\n"
    md_path.write_text(text, encoding="utf-8")
    txt_path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Store passive Mini-DIO recurrence maturity candidates")
    parser.add_argument("--source", required=True, type=Path, help="dio_mini_passive_wiederkehr_reifezaehlung.csv")
    parser.add_argument(
        "--output-json",
        default=Path("bot_memory/dio_mini_passive_recurrence_maturity_candidates.json"),
        type=Path,
    )
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()

    memory = build_memory(_read_csv(args.source), args.source)
    write_outputs(memory, args.output_json, args.output_dir)
    print(
        json.dumps(
            {
                "passive_recurrence_maturity_candidates": len(memory.get("entries", []) or []),
                "output_json": str(args.output_json),
                "output_dir": str(args.output_dir) if args.output_dir else "",
                "read_by_mini_dio": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
