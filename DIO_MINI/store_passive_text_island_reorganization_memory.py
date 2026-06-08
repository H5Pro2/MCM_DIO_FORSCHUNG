"""Store passive Mini-DIO text-island reorganization memory.

This memory persists text-island trajectories such as stable core, core to
drift, raw to core, or late emergence. It is diagnostic memory only.
Mini-DIO must not read it for action, entries, gates, or direction.
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
        "schema": "dio_mini_passive_text_island_reorganization_memory.v1",
        "version": 1,
        "created_at": int(time.time()),
        "updated_at": int(time.time()),
        "boundary": dict(PASSIVE_BOUNDARY),
        "sources": [],
        "text_islands": {},
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
    memory["boundary"] = dict(PASSIVE_BOUNDARY)
    memory["sources"] = list(memory.get("sources", []) or [])
    memory["text_islands"] = dict(memory.get("text_islands", {}) or {})
    memory["summary"] = dict(memory.get("summary", {}) or {})
    return memory


def _affordance(trajectory_state: str) -> str:
    if trajectory_state.startswith("stable_"):
        return "can_preserve_stable_passive_trajectory"
    if trajectory_state == "core_to_drift_reorganization":
        return "can_preserve_core_drift_warning"
    if trajectory_state == "reorganized_into_core":
        return "can_preserve_raw_to_core_reorganization"
    if trajectory_state == "late_text_island_emergence":
        return "can_preserve_late_emergence"
    if "raw" in trajectory_state:
        return "can_preserve_raw_semantic_trace"
    if "drift" in trajectory_state:
        return "can_preserve_drift_trace"
    return "can_preserve_passive_reorganization_trace"


def _memory_note(item: dict) -> str:
    return (
        f"{item['text_island_symbol']}: {item['dominant_trajectory_state']}; "
        f"observations={item['observations']}; "
        f"last_path={item['last_state_path']}; "
        "passiv, keine Handlung."
    )


def update_memory(memory: dict, history_rows: list[dict], source_path: Path, source_label: str) -> tuple[dict, list[dict]]:
    now = int(time.time())
    memory["updated_at"] = now
    memory.setdefault("sources", []).append(
        {
            "source_label": source_label,
            "source_path": str(source_path),
            "timestamp": now,
            "history_count": len(history_rows),
            **PASSIVE_BOUNDARY,
        }
    )
    updates: list[dict] = []
    store = memory.setdefault("text_islands", {})
    for row in history_rows:
        symbol = str(row.get("text_island_symbol", "") or "").strip()
        if not symbol:
            continue
        trajectory = str(row.get("trajectory_state", "") or "unknown")
        previous = dict(store.get(symbol, {}) or {})
        observations = _safe_int(previous.get("observations"))
        state_counts = dict(previous.get("trajectory_counts", {}) or {})
        state_counts[trajectory] = _safe_int(state_counts.get(trajectory)) + 1
        dominant = max(state_counts.items(), key=lambda item: item[1])[0]
        history = list(previous.get("history", []) or [])
        history.append(
            {
                "source_label": source_label,
                "trajectory_state": trajectory,
                "family_change_state": str(row.get("family_change_state", "") or ""),
                "state_path": str(row.get("state_path", "") or ""),
                "maturity_path": str(row.get("maturity_path", "") or ""),
                "score_path": str(row.get("score_path", "") or ""),
                "family_count_path": str(row.get("family_count_path", "") or ""),
                "score_delta": round(_safe_float(row.get("score_delta")), 9),
                "max_drift_pressure": round(_safe_float(row.get("max_drift_pressure")), 9),
                "timestamp": now,
            }
        )
        history = history[-24:]
        record = {
            "text_island_symbol": symbol,
            "observations": observations + 1,
            "first_seen_source": previous.get("first_seen_source") or source_label,
            "last_seen_source": source_label,
            "last_trajectory_state": trajectory,
            "dominant_trajectory_state": dominant,
            "last_family_change_state": str(row.get("family_change_state", "") or ""),
            "last_state_path": str(row.get("state_path", "") or ""),
            "last_maturity_path": str(row.get("maturity_path", "") or ""),
            "last_score_path": str(row.get("score_path", "") or ""),
            "last_score_delta": round(_safe_float(row.get("score_delta")), 9),
            "last_max_drift_pressure": round(_safe_float(row.get("max_drift_pressure")), 9),
            "trajectory_counts": state_counts,
            "passive_affordance": _affordance(trajectory),
            "history": history,
            **PASSIVE_BOUNDARY,
        }
        record["memory_note"] = _memory_note(record)
        store[symbol] = record
        updates.append(record)
    memory["summary"] = _summary(store)
    return memory, updates


def _summary(store: dict) -> dict:
    rows = list(store.values())
    states: dict[str, int] = {}
    for row in rows:
        state = str(row.get("dominant_trajectory_state", "") or "-")
        states[state] = states.get(state, 0) + 1
    return {
        "text_island_count": len(rows),
        "dominant_trajectory_states": dict(sorted(states.items())),
        "avg_last_drift_pressure": round(
            sum(_safe_float(row.get("last_max_drift_pressure")) for row in rows) / max(1, len(rows)),
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
        list(memory.get("text_islands", {}).values()),
        key=lambda item: (
            str(item.get("dominant_trajectory_state", "")),
            str(item.get("text_island_symbol", "")),
        ),
    )
    _write_csv(
        output_dir / "dio_mini_passive_text_island_reorganization_memory.csv",
        rows,
        [
            "text_island_symbol",
            "dominant_trajectory_state",
            "last_trajectory_state",
            "observations",
            "last_family_change_state",
            "last_score_delta",
            "last_max_drift_pressure",
            "passive_affordance",
            "memory_note",
        ],
    )
    _write_csv(
        output_dir / "dio_mini_passive_text_island_reorganization_memory_updates.csv",
        updates,
        [
            "text_island_symbol",
            "dominant_trajectory_state",
            "last_trajectory_state",
            "observations",
            "last_family_change_state",
            "last_score_delta",
            "last_max_drift_pressure",
            "passive_affordance",
            "memory_note",
        ],
    )
    lines = [
        "# Mini-DIO Passive Text-Island Reorganization Memory",
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
            "- passiver Reorganisationsspeicher",
            "- keine Runtime-Lesung",
            "- keine Handlung",
            "- kein Gate",
            "- kein Entry",
            "- keine Richtung",
            "",
            "## Textinseln",
        ]
    )
    for row in rows[:160]:
        lines.append(f"- {row['memory_note']}")
    text = "\n".join(lines) + "\n"
    (output_dir / "dio_mini_passive_text_island_reorganization_memory.md").write_text(text, encoding="utf-8")
    (output_dir / "dio_mini_passive_text_island_reorganization_memory.txt").write_text(
        "\n".join(row["memory_note"] for row in rows) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Store passive text-island reorganization memory")
    parser.add_argument("--history", type=Path, required=True)
    parser.add_argument(
        "--memory",
        type=Path,
        default=Path("bot_memory/dio_mini_passive_text_island_reorganization_memory.json"),
    )
    parser.add_argument("--source-label", default="text_island_reorganization_history")
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()

    memory, updates = update_memory(_load_memory(args.memory), _read_csv(args.history), args.history, args.source_label)
    write_outputs(memory, args.memory, args.output_dir, updates)
    print(
        json.dumps(
            {
                "memory": str(args.memory),
                "output_dir": str(args.output_dir) if args.output_dir else "",
                "text_island_count": memory.get("summary", {}).get("text_island_count", 0),
                "updates": len(updates),
                **PASSIVE_BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
