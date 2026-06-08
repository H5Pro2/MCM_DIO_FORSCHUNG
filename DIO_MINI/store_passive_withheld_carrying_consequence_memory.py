"""Store passive Mini-DIO withheld carrying consequence memory.

This memory records carried-but-withheld situations where a passive afterlook
found positive consequence potential. It is diagnostic only and must not be
read by Mini-DIO runtime, action selection, or gates.
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
    ordered_fields = list(fields)
    for row in rows:
        for key in row.keys():
            if key not in ordered_fields:
                ordered_fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=ordered_fields)
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
    chars = []
    while value:
        value, rest = divmod(value, 36)
        chars.append(alphabet[rest])
    return "".join(reversed(chars))


def make_withheld_symbol(world_label: str, family: str, direction_hint: str) -> str:
    raw = f"{world_label}|{family}|{direction_hint}|withheld_carrying_consequence"
    return f"dio_wcc_{_hash_base36(raw)[:10]}"


def direction_hint(row: dict) -> str:
    long_count = _safe_int(row.get("best_long"))
    short_count = _safe_int(row.get("best_short"))
    if long_count > short_count:
        return "LONG"
    if short_count > long_count:
        return "SHORT"
    return "MIXED"


def build_memory(rows: list[dict], source_path: Path) -> dict:
    entries: list[dict] = []
    for row in rows:
        state = str(row.get("consequence_state", "") or "")
        if state != "unconfirmed_consequence_would_have_carried":
            continue
        world = str(row.get("world_label", "") or "")
        family = str(row.get("symbol_family", "") or "")
        hint = direction_hint(row)
        item = {
            "withheld_consequence_symbol": make_withheld_symbol(world, family, hint),
            "world_label": world,
            "symbol_family": family,
            "direction_hint": hint,
            "source_alignment_state": str(row.get("alignment_state", "") or ""),
            "source_consequence_state": state,
            "best_long": _safe_int(row.get("best_long")),
            "best_short": _safe_int(row.get("best_short")),
            "best_wait": _safe_int(row.get("best_wait")),
            "best_positive_count": _safe_int(row.get("best_positive_count")),
            "avg_best_reward": round(_safe_float(row.get("avg_best_reward")), 9),
            "max_best_reward": round(_safe_float(row.get("max_best_reward")), 9),
            "reflection_carry": round(_safe_float(row.get("reflection_carry")), 9),
            "reflection_strain": round(_safe_float(row.get("reflection_strain")), 9),
            "world_carry": round(_safe_float(row.get("world_carry")), 9),
            "avg_observation_pressure": round(_safe_float(row.get("avg_observation_pressure")), 9),
            "avg_trade_readiness": round(_safe_float(row.get("avg_trade_readiness")), 9),
            "passive_only": True,
            "read_by_mini_dio": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
        }
        item["memory_note"] = (
            f"{world}/{family}: getragen wahrgenommen, nicht gehandelt, "
            f"Nachblick haette {hint} getragen; avg_best_reward={item['avg_best_reward']:.6f}."
        )
        entries.append(item)

    entries.sort(
        key=lambda item: (
            -_safe_float(item.get("avg_best_reward")),
            -_safe_float(item.get("reflection_carry")),
            -_safe_float(item.get("world_carry")),
            str(item.get("world_label", "")),
            str(item.get("symbol_family", "")),
        )
    )
    direction_counts: dict[str, int] = {}
    for item in entries:
        direction = str(item.get("direction_hint", "MIXED") or "MIXED")
        direction_counts[direction] = direction_counts.get(direction, 0) + 1

    return {
        "schema": "dio_mini_passive_withheld_carrying_consequence_memory.v1",
        "source_report": str(source_path),
        "created_utc_ms": int(time.time() * 1000),
        "boundary": {
            "passive_only": True,
            "read_by_mini_dio": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
            "is_future_teacher": False,
        },
        "summary": {
            "entry_count": len(entries),
            "direction_counts": dict(sorted(direction_counts.items())),
            "avg_best_reward": round(
                sum(_safe_float(item.get("avg_best_reward")) for item in entries) / max(1, len(entries)),
                9,
            ),
            "avg_reflection_carry": round(
                sum(_safe_float(item.get("reflection_carry")) for item in entries) / max(1, len(entries)),
                9,
            ),
            "avg_world_carry": round(
                sum(_safe_float(item.get("world_carry")) for item in entries) / max(1, len(entries)),
                9,
            ),
        },
        "entries": entries,
    }


def write_outputs(memory: dict, memory_path: Path, output_dir: Path | None) -> None:
    _atomic_write_json(memory_path, memory)
    if output_dir is None:
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    entries = list(memory.get("entries", []) or [])
    _write_csv(
        output_dir / "passive_withheld_carrying_consequence_memory.csv",
        entries,
        [
            "world_label",
            "symbol_family",
            "direction_hint",
            "avg_best_reward",
            "reflection_carry",
            "reflection_strain",
            "world_carry",
            "best_long",
            "best_short",
            "best_positive_count",
            "withheld_consequence_symbol",
        ],
    )

    lines = [
        "# Mini-DIO Passive Withheld Carrying Consequence Memory",
        "",
        f"- memory: `{memory_path}`",
        "- boundary: passive only; not read by Mini-DIO; no action; no gate",
        "",
        "## Summary",
    ]
    for key, value in dict(memory.get("summary", {}) or {}).items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Entries"])
    for item in entries[:48]:
        lines.append(f"- {item['memory_note']}")
    lines.extend(
        [
            "",
            "## Grenze",
            "- Reifungsdruck, keine Entscheidung",
            "- nicht als Entry-Regel verwenden",
            "- keine harte Schwelle daraus ableiten",
        ]
    )
    text = "\n".join(lines) + "\n"
    (output_dir / "passive_withheld_carrying_consequence_memory.md").write_text(text, encoding="utf-8")
    (output_dir / "passive_withheld_carrying_consequence_memory.txt").write_text(text, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="passive_unconfirmed_consequence.csv")
    parser.add_argument(
        "--memory",
        type=Path,
        default=Path("bot_memory/dio_mini_passive_withheld_carrying_consequence_memory.json"),
    )
    parser.add_argument("--output-dir", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    memory = build_memory(_read_csv(args.source), args.source)
    write_outputs(memory, args.memory, args.output_dir)
    print(json.dumps(memory["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
