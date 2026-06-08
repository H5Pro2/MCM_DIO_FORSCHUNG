"""Store passive Mini-DIO inner-core memory.

This memory preserves stable inner spaces from passive text-island maps. It is
diagnostic only. Mini-DIO must not read it for action, gates, entries, or
direction.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import time
from pathlib import Path


PASSIVE_BOUNDARY = {
    "passive_only": True,
    "writes_runtime_memory": False,
    "read_by_mini_dio": False,
    "influences_action": False,
    "is_gate": False,
    "is_motoric": False,
    "is_entry_signal": False,
    "is_direction_signal": False,
}


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
    if not path.exists():
        return []
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


def _empty_memory() -> dict:
    return {
        "schema": "dio_mini_passive_inner_core_memory.v1",
        "version": 1,
        "created_at": int(time.time()),
        "updated_at": int(time.time()),
        "boundary": dict(PASSIVE_BOUNDARY),
        "sources": [],
        "cores": {},
        "summary": {},
    }


def _load_memory(path: Path) -> dict:
    if not path.exists():
        return _empty_memory()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return _empty_memory()
    if not isinstance(payload, dict):
        return _empty_memory()
    memory = _empty_memory()
    memory.update(payload)
    memory["sources"] = list(memory.get("sources", []) or [])
    memory["cores"] = dict(memory.get("cores", {}) or {})
    memory["summary"] = dict(memory.get("summary", {}) or {})
    memory["boundary"] = dict(PASSIVE_BOUNDARY)
    return memory


def _state_affordance(state: str) -> str:
    if state == "passive_variation_core":
        return "can_preserve_bearing_variation_as_inner_space"
    if state == "passive_recurrence_core":
        return "can_preserve_recurrent_inner_space"
    if state == "passive_foreign_boundary_core":
        return "can_preserve_foreign_boundary_without_mixing"
    return "can_hold_passive_inner_core"


def _memory_note(item: dict) -> str:
    return (
        f"{item['text_island_symbol']}: {item['inner_core_state']}; "
        f"observations={item['observations']}; "
        f"score={item['avg_semantic_maturity_score']:.3f}; "
        "passiv, keine Handlung."
    )


def update_memory(memory: dict, rows: list[dict], source_path: Path, source_label: str) -> tuple[dict, list[dict]]:
    now = int(time.time())
    memory["updated_at"] = now
    memory.setdefault("sources", []).append(
        {
            "source_label": source_label,
            "source_path": str(source_path),
            "timestamp": now,
            "core_count": len(rows),
            **PASSIVE_BOUNDARY,
        }
    )

    updates: list[dict] = []
    cores = memory.setdefault("cores", {})
    for row in rows:
        symbol = str(row.get("text_island_symbol", "") or "").strip()
        if not symbol:
            continue
        state = str(row.get("inner_core_state", "") or "passive_inner_core")
        score = _safe_float(row.get("right_semantic_maturity_score"))
        previous = dict(cores.get(symbol, {}) or {})
        observations = _safe_int(previous.get("observations"))
        old_avg = _safe_float(previous.get("avg_semantic_maturity_score"))
        avg_score = ((old_avg * observations) + score) / max(1, observations + 1)
        state_counts = dict(previous.get("state_counts", {}) or {})
        state_counts[state] = _safe_int(state_counts.get(state)) + 1
        record = {
            "text_island_symbol": symbol,
            "inner_core_state": state,
            "dominant_inner_core_state": max(state_counts.items(), key=lambda item: item[1])[0],
            "observations": observations + 1,
            "first_seen_source": previous.get("first_seen_source") or source_label,
            "last_seen_source": source_label,
            "avg_semantic_maturity_score": round(avg_score, 9),
            "last_semantic_maturity_score": round(score, 9),
            "last_score_delta": round(_safe_float(row.get("score_delta")), 9),
            "last_stability_delta": round(_safe_float(row.get("stability_delta")), 9),
            "last_variation_delta": round(_safe_float(row.get("variation_delta")), 9),
            "last_drift_delta": round(_safe_float(row.get("drift_delta")), 9),
            "last_left_inner_map_state": row.get("left_inner_map_state", ""),
            "last_right_inner_map_state": row.get("right_inner_map_state", ""),
            "left_families": row.get("left_families", ""),
            "right_families": row.get("right_families", ""),
            "state_counts": state_counts,
            "passive_affordance": _state_affordance(state),
            **PASSIVE_BOUNDARY,
        }
        record["memory_note"] = _memory_note(record)
        cores[symbol] = record
        updates.append(record)

    memory["summary"] = _summary(cores)
    return memory, updates


def _summary(cores: dict) -> dict:
    rows = list(cores.values())
    states: dict[str, int] = {}
    for row in rows:
        state = str(row.get("dominant_inner_core_state", "") or "-")
        states[state] = states.get(state, 0) + 1
    return {
        "core_count": len(rows),
        "dominant_states": dict(sorted(states.items())),
        "avg_semantic_maturity_score": round(
            sum(_safe_float(row.get("avg_semantic_maturity_score")) for row in rows) / max(1, len(rows)),
            9,
        ),
        **PASSIVE_BOUNDARY,
    }


def write_outputs(memory: dict, memory_path: Path, output_dir: Path | None, updates: list[dict]) -> None:
    _atomic_write_json(memory_path, memory)
    if output_dir is None:
        return
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = sorted(
        list(memory.get("cores", {}).values()),
        key=lambda item: (
            str(item.get("dominant_inner_core_state", "")),
            -_safe_float(item.get("avg_semantic_maturity_score")),
            str(item.get("text_island_symbol", "")),
        ),
    )
    _write_csv(
        output_dir / "dio_mini_passive_inner_core_memory.csv",
        rows,
        [
            "text_island_symbol",
            "dominant_inner_core_state",
            "observations",
            "avg_semantic_maturity_score",
            "last_semantic_maturity_score",
            "passive_affordance",
            "memory_note",
        ],
    )
    _write_csv(
        output_dir / "dio_mini_passive_inner_core_memory_updates.csv",
        updates,
        [
            "text_island_symbol",
            "inner_core_state",
            "observations",
            "avg_semantic_maturity_score",
            "last_semantic_maturity_score",
            "passive_affordance",
            "memory_note",
        ],
    )
    lines = [
        "# Mini-DIO Passive Inner Core Memory",
        "",
        f"- memory: `{memory_path}`",
        "",
        "## Summary",
    ]
    for key, value in dict(memory.get("summary", {}) or {}).items():
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## Grenze",
            "- passiver Kernspeicher",
            "- keine Runtime-Lesung",
            "- keine Handlung",
            "- kein Gate",
            "- kein Entry",
            "- keine Richtung",
            "",
            "## Cores",
        ]
    )
    for row in rows[:120]:
        lines.append(f"- {row['memory_note']}")
    text = "\n".join(lines) + "\n"
    (output_dir / "dio_mini_passive_inner_core_memory.md").write_text(text, encoding="utf-8")
    (output_dir / "dio_mini_passive_inner_core_memory.txt").write_text(
        "\n".join(row["memory_note"] for row in rows) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Store passive Mini-DIO inner core memory")
    parser.add_argument("--core-list", required=True, type=Path, help="passive_inner_core_list.csv")
    parser.add_argument(
        "--memory",
        default=Path("bot_memory/dio_mini_passive_inner_core_memory.json"),
        type=Path,
    )
    parser.add_argument("--source-label", default="passive_inner_core_list")
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()

    memory, updates = update_memory(
        _load_memory(args.memory),
        _read_csv(args.core_list),
        args.core_list,
        args.source_label,
    )
    write_outputs(memory, args.memory, args.output_dir, updates)
    print(
        json.dumps(
            {
                "memory": str(args.memory),
                "output_dir": str(args.output_dir) if args.output_dir else "",
                "core_count": memory.get("summary", {}).get("core_count", 0),
                "updates": len(updates),
                **PASSIVE_BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
