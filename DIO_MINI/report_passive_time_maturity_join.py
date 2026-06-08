"""Join passive episode time maps with passive inner maturity memory.

The report keeps time, action consequence, and inner maturity readable in one
place. It is diagnostic only and is not read by the Mini-DIO action core.
"""

from __future__ import annotations

import argparse
import csv
import json
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


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_maturity(memory: dict) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for item in list(memory.get("entries", []) or []):
        key = str(item.get("passive_family_action", "") or "")
        if key:
            result[key] = dict(item)
    return result


def _split(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    return [item.strip() for item in str(value or "").split(",") if item.strip()]


def _time_maturity_state(time_row: dict, maturity: dict | None, bridge: dict | None = None) -> str:
    time_state = str(time_row.get("freshness_state", "") or "")
    outcome_events = str(time_row.get("outcome_events", "") or "")
    reward = _safe_float(time_row.get("event_reward_sum"))
    if bridge and maturity:
        bridge_state = str(bridge.get("passive_maturity_state", "") or "")
        if time_state.startswith("fresh") and bridge_state == "passive_observation_has_carried_neighbor" and reward > 0:
            return "fresh_carried_from_inner_bridge"
    if maturity:
        inner_state = str(maturity.get("inner_memory_state", "") or "")
        if time_state.startswith("fresh") and inner_state == "passive_inner_memory_stable" and reward > 0:
            return "fresh_carried_inner_trace"
        if time_state.startswith("fresh") and inner_state == "passive_inner_memory_reorganizing":
            return "fresh_reorganizing_inner_trace"
        if time_state.startswith("older") and reward < 0:
            return "older_burdened_inner_trace"
        if "WAIT" in str(time_row.get("family_action", "")) and time_state.startswith("fresh"):
            return "fresh_waiting_inner_context"
        return "time_trace_with_inner_memory"
    if "TP:" in outcome_events and reward > 0 and time_state.startswith("fresh"):
        return "fresh_carried_without_inner_memory"
    if "SL:" in outcome_events or reward < 0:
        return "burden_without_inner_memory"
    if "WAIT" in str(time_row.get("family_action", "")) and time_state.startswith("fresh"):
        return "fresh_waiting_without_inner_memory"
    if time_state.startswith("older"):
        return "older_trace_without_inner_memory"
    return "open_time_trace_without_inner_memory"


def _note(row: dict) -> str:
    family_action = str(row.get("family_action", "") or "-")
    state = str(row.get("time_maturity_state", "") or "-")
    time_state = str(row.get("episode_freshness_state", "") or "-")
    inner_state = str(row.get("inner_memory_state", "") or "-")
    reward = _safe_float(row.get("event_reward_sum"))
    sources = str(row.get("episode_source_labels", "") or "-")
    bridge_source = str(row.get("bridge_passive_family_action", "") or "")
    if state == "fresh_carried_from_inner_bridge":
        return (
            f"{family_action}: frisch getragen ueber passive Reifebruecke von {bridge_source}; "
            f"Zeit={time_state}; Innen={inner_state}; Quellen={sources}; reward={reward:.6f}."
        )
    if state == "fresh_carried_inner_trace":
        return f"{family_action}: frisch getragen; Zeit={time_state}; Innen={inner_state}; Quellen={sources}; reward={reward:.6f}."
    if state == "fresh_reorganizing_inner_trace":
        return f"{family_action}: frisch reorganisierend; Zeit={time_state}; Innen={inner_state}; Quellen={sources}; reward={reward:.6f}."
    if state == "older_burdened_inner_trace":
        return f"{family_action}: alte belastete Spur; Zeit={time_state}; Innen={inner_state}; Quellen={sources}; reward={reward:.6f}."
    if state == "fresh_waiting_inner_context":
        return f"{family_action}: frisch wartender Kontext mit Innenbezug; Quellen={sources}."
    if state == "fresh_carried_without_inner_memory":
        return f"{family_action}: frisch getragen, aber noch ohne innere Reife-Memory; Quellen={sources}; reward={reward:.6f}."
    if state == "fresh_waiting_without_inner_memory":
        return f"{family_action}: frisch wartend, ohne innere Reife-Memory; Quellen={sources}."
    if state == "burden_without_inner_memory":
        return f"{family_action}: belastete Zeitspur ohne innere Reife-Memory; Quellen={sources}; reward={reward:.6f}."
    return f"{family_action}: {state}; Zeit={time_state}; Innen={inner_state}; Quellen={sources}; reward={reward:.6f}."


def _load_bridge_rows(paths: list[Path]) -> dict[str, dict]:
    by_real: dict[str, dict] = {}
    for path in paths:
        for row in _read_csv(path):
            real_key = str(row.get("best_real_family_action", "") or row.get("real_family_action", "") or "")
            if not real_key:
                continue
            current = by_real.get(real_key)
            if current is None or _safe_float(row.get("best_similarity") or row.get("sense_similarity")) > _safe_float(
                current.get("best_similarity") or current.get("sense_similarity")
            ):
                by_real[real_key] = dict(row)
    return by_real


def build_rows(time_summaries: list[Path], maturity_memory: dict, maturity_bridge_summaries: list[Path] | None = None) -> list[dict]:
    maturity_by_key = _load_maturity(maturity_memory)
    bridge_by_real = _load_bridge_rows(list(maturity_bridge_summaries or []))
    rows: list[dict] = []
    for path in time_summaries:
        for time_row in _read_csv(path):
            family_action = str(time_row.get("family_action", "") or "")
            bridge = bridge_by_real.get(family_action)
            bridge_passive_key = str(bridge.get("passive_family_action", "") or "") if bridge else ""
            maturity = maturity_by_key.get(family_action)
            if maturity is None and bridge_passive_key:
                maturity = maturity_by_key.get(bridge_passive_key)
            row = {
                "family_action": family_action,
                "symbol_family": str(time_row.get("symbol_family", "") or ""),
                "action": str(time_row.get("action", "") or ""),
                "time_maturity_state": _time_maturity_state(time_row, maturity, bridge),
                "episode_freshness_state": str(time_row.get("freshness_state", "") or ""),
                "episode_source_labels": str(time_row.get("source_labels", "") or ""),
                "episode_source_count": _safe_int(time_row.get("source_count")),
                "episode_count": _safe_int(time_row.get("episode_count")),
                "phase_time_states": str(time_row.get("phase_time_states", "") or ""),
                "outcome_events": str(time_row.get("outcome_events", "") or ""),
                "event_reward_sum": round(_safe_float(time_row.get("event_reward_sum")), 6),
                "avg_event_reward": round(_safe_float(time_row.get("avg_event_reward")), 6),
                "avg_finite_phase_age": str(time_row.get("avg_finite_phase_age", "") or ""),
                "avg_bars_held": str(time_row.get("avg_bars_held", "") or ""),
                "inner_memory_state": str(maturity.get("inner_memory_state", "") if maturity else ""),
                "inner_map_count": _safe_int(maturity.get("map_count") if maturity else 0),
                "inner_map_labels": ",".join(_split(maturity.get("map_labels") if maturity else "")),
                "inner_seeds": ",".join(_split(maturity.get("seeds") if maturity else "")),
                "inner_real_reward_sum": round(_safe_float(maturity.get("real_reward_sum") if maturity else 0.0), 6),
                "has_inner_maturity": 1 if maturity else 0,
                "bridge_passive_family_action": bridge_passive_key,
                "bridge_maturity_state": str(bridge.get("passive_maturity_state", "") or "") if bridge else "",
                "bridge_similarity": round(_safe_float(bridge.get("best_similarity") or bridge.get("sense_similarity") if bridge else 0.0), 6),
                "passive_only": 1,
                "influences_action": 0,
                "is_gate": 0,
                "is_motoric": 0,
            }
            row["time_maturity_note"] = _note(row)
            rows.append(row)
    rows.sort(
        key=lambda item: (
            str(item.get("time_maturity_state", "")) not in (
                "fresh_carried_from_inner_bridge",
                "fresh_carried_inner_trace",
                "fresh_reorganizing_inner_trace",
                "fresh_carried_without_inner_memory",
            ),
            -_safe_float(item.get("event_reward_sum")),
            str(item.get("family_action", "")),
        )
    )
    return rows


def build_summary(rows: list[dict]) -> list[dict]:
    grouped: dict[str, dict] = {}
    for row in rows:
        state = str(row.get("time_maturity_state", "") or "unknown")
        bucket = grouped.setdefault(
            state,
            {
                "time_maturity_state": state,
                "count": 0,
                "family_actions": set(),
                "event_reward_sum": 0.0,
                "inner_count": 0,
            },
        )
        bucket["count"] += 1
        bucket["family_actions"].add(str(row.get("family_action", "") or ""))
        bucket["event_reward_sum"] += _safe_float(row.get("event_reward_sum"))
        bucket["inner_count"] += _safe_int(row.get("has_inner_maturity"))

    summary: list[dict] = []
    for bucket in grouped.values():
        count = _safe_int(bucket["count"])
        summary.append(
            {
                "time_maturity_state": str(bucket["time_maturity_state"]),
                "count": count,
                "inner_count": _safe_int(bucket["inner_count"]),
                "event_reward_sum": round(_safe_float(bucket["event_reward_sum"]), 6),
                "avg_event_reward": round(_safe_float(bucket["event_reward_sum"]) / max(1, count), 6),
                "family_actions": ",".join(sorted(item for item in bucket["family_actions"] if item)),
            }
        )
    summary.sort(key=lambda item: (-_safe_float(item.get("event_reward_sum")), str(item.get("time_maturity_state", ""))))
    return summary


def _write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(rows: list[dict], summary: list[dict], output_dir: Path, time_summaries: list[Path], memory_path: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows_path = output_dir / "dio_mini_passive_time_maturity_join.csv"
    summary_path = output_dir / "dio_mini_passive_time_maturity_join_summary.csv"
    json_path = output_dir / "dio_mini_passive_time_maturity_join.json"
    md_path = output_dir / "dio_mini_passive_time_maturity_join.md"
    txt_path = output_dir / "dio_mini_passive_time_maturity_join.txt"

    fields = list(rows[0].keys()) if rows else [
        "family_action",
        "time_maturity_state",
        "episode_freshness_state",
        "inner_memory_state",
        "event_reward_sum",
        "passive_only",
    ]
    summary_fields = list(summary[0].keys()) if summary else [
        "time_maturity_state",
        "count",
        "event_reward_sum",
        "family_actions",
    ]
    _write_csv(rows_path, rows, fields)
    _write_csv(summary_path, summary, summary_fields)
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_time_maturity_join.v1",
                "time_summaries": [str(path) for path in time_summaries],
                "maturity_memory": str(memory_path),
                "boundary": {
                    "passive_only": True,
                    "writes_training_memory": False,
                    "influences_action": False,
                    "is_gate": False,
                    "is_motoric": False,
                    "read_by_mini_dio": False,
                },
                "summary": summary,
                "rows": rows,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = ["# DIO Mini Passive Time Maturity Join", ""]
    lines.extend(["## Grenze", "- passiv", "- kein Memory-Schreiben", "- keine Motorik", "- kein Gate", ""])
    lines.extend(["## Quellen"])
    lines.append(f"- maturity_memory: {memory_path}")
    for path in time_summaries:
        lines.append(f"- time_summary: {path}")
    lines.extend(["", "## Summary"])
    for item in summary:
        lines.append(
            f"- {item['time_maturity_state']}: count={item['count']} "
            f"reward={float(item['event_reward_sum']):.6f} inner={item['inner_count']}"
        )
    lines.extend(["", "## Lesung"])
    for row in rows[:100]:
        lines.append(f"- {row['time_maturity_note']}")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    txt_path.write_text("\n".join(row["time_maturity_note"] for row in rows), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Join passive Mini-DIO time map with inner maturity memory")
    parser.add_argument("--time-summary", action="append", required=True)
    parser.add_argument("--maturity-bridge-summary", action="append", default=[])
    parser.add_argument("--maturity-memory", default="bot_memory/dio_mini_passive_inner_maturity_memory.json")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    time_summaries = [Path(path) for path in args.time_summary]
    memory_path = Path(args.maturity_memory)
    maturity_bridge_summaries = [Path(path) for path in list(args.maturity_bridge_summary or [])]
    rows = build_rows(time_summaries, _read_json(memory_path), maturity_bridge_summaries)
    summary = build_summary(rows)
    write_outputs(rows, summary, Path(args.output_dir), time_summaries, memory_path)
    print(f"time_maturity_join_rows={len(rows)} summary={len(summary)}")
    for row in summary[:20]:
        print(
            f"{row['time_maturity_state']} count={row['count']} "
            f"reward={row['event_reward_sum']} inner={row['inner_count']}"
        )


if __name__ == "__main__":
    main()
