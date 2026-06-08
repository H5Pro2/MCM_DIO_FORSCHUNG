"""Report passive freshness and age of Mini-DIO inner maturity memory.

This reader adds a time-perception layer to the separated passive inner
maturity memory. It does not write training memory and it is not read by the
Mini-DIO action core.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


DEFAULT_MAP_ORDER = ["basis", "followup1", "followup2"]


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


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _split_order(value: str | None) -> list[str]:
    items = [item.strip() for item in str(value or "").split(",") if item.strip()]
    return items or list(DEFAULT_MAP_ORDER)


def _ordered_labels(labels: list[str], order: list[str]) -> list[str]:
    rank = {label: index for index, label in enumerate(order)}
    return sorted(labels, key=lambda item: (rank.get(item, len(order)), item))


def _map_indices(labels: list[str], order: list[str]) -> list[int]:
    rank = {label: index for index, label in enumerate(order)}
    return sorted(rank[label] for label in labels if label in rank)


def _freshness_state(item: dict, labels: list[str], order: list[str]) -> str:
    latest = order[-1] if order else ""
    memory_state = str(item.get("inner_memory_state", "") or "")
    if latest and latest in labels:
        if memory_state == "passive_inner_memory_stable":
            return "fresh_stable_trace"
        if memory_state == "passive_inner_memory_reorganizing":
            return "fresh_reorganizing_trace"
        return "fresh_local_trace"
    if memory_state == "passive_inner_memory_local":
        return "local_trace_without_recent_return"
    return "stale_trace_without_recent_consequence"


def _time_note(item: dict, row: dict) -> str:
    family = str(item.get("passive_family_action", "") or "-")
    state = row["freshness_state"]
    first_seen = row["first_seen_map"] or "-"
    last_seen = row["last_seen_map"] or "-"
    seeds = row["seeds"] or "-"
    if state == "fresh_stable_trace":
        return f"{family}: Zeitspur bleibt frisch und stabil ({first_seen} -> {last_seen}); Samen={seeds}."
    if state == "fresh_reorganizing_trace":
        return f"{family}: Zeitspur ist frisch, aber reorganisierend ({first_seen} -> {last_seen}); Samen={seeds}."
    if state == "fresh_local_trace":
        return f"{family}: lokale Spur ist in der juengsten Karte sichtbar; noch keine stabile Zeit-Tiefe."
    if state == "local_trace_without_recent_return":
        return f"{family}: lokale Spur kehrt in der juengsten Karte nicht wieder; sie bleibt offene Erinnerung."
    return f"{family}: Spur war frueher sichtbar, aber ohne juengste Konsequenz; zeitlich vorsichtig lesen."


def build_rows(memory: dict, map_order: list[str]) -> list[dict]:
    rows: list[dict] = []
    for item in list(memory.get("entries", []) or []):
        labels = _ordered_labels(list(item.get("map_labels", []) or []), map_order)
        indices = _map_indices(labels, map_order)
        first_seen = map_order[min(indices)] if indices else ""
        last_seen = map_order[max(indices)] if indices else ""
        latest_index = len(map_order) - 1
        last_index = max(indices) if indices else -1
        missing_after_last = map_order[last_index + 1 :] if last_index >= 0 else list(map_order)
        seen_density = len(set(labels)) / max(1, len(map_order))
        time_span_maps = (max(indices) - min(indices) + 1) if indices else 0
        state = _freshness_state(item, labels, map_order)
        row = {
            "passive_family_action": str(item.get("passive_family_action", "") or ""),
            "freshness_state": state,
            "inner_memory_state": str(item.get("inner_memory_state", "") or ""),
            "first_seen_map": first_seen,
            "last_seen_map": last_seen,
            "latest_map": map_order[-1] if map_order else "",
            "map_labels": ",".join(labels),
            "missing_after_last_seen": ",".join(missing_after_last),
            "map_count": _safe_int(item.get("map_count")),
            "time_span_maps": time_span_maps,
            "seen_density": f"{seen_density:.6f}",
            "trace_count": _safe_int(item.get("trace_count")),
            "seeds": ",".join(list(item.get("seeds", []) or [])),
            "actions": ",".join(list(item.get("actions", []) or [])),
            "real_reward_sum": f"{_safe_float(item.get('real_reward_sum')):.6f}",
            "avg_similarity": f"{_safe_float(item.get('avg_similarity')):.6f}",
            "avg_mcm_similarity": f"{_safe_float(item.get('avg_mcm_similarity')):.6f}",
            "passive_only": "1",
            "influences_action": "0",
            "is_gate": "0",
            "is_motoric": "0",
        }
        row["time_note"] = _time_note(item, row)
        rows.append(row)
    rows.sort(
        key=lambda item: (
            str(item.get("freshness_state", "")) not in ("fresh_stable_trace", "fresh_reorganizing_trace"),
            -_safe_int(item.get("map_count")),
            str(item.get("passive_family_action", "")),
        )
    )
    return rows


def build_summary(rows: list[dict]) -> dict:
    states: dict[str, int] = {}
    for row in rows:
        key = str(row.get("freshness_state", "") or "unknown")
        states[key] = states.get(key, 0) + 1
    return {
        "row_count": len(rows),
        "fresh_stable_trace": states.get("fresh_stable_trace", 0),
        "fresh_reorganizing_trace": states.get("fresh_reorganizing_trace", 0),
        "fresh_local_trace": states.get("fresh_local_trace", 0),
        "stale_trace_without_recent_consequence": states.get("stale_trace_without_recent_consequence", 0),
        "local_trace_without_recent_return": states.get("local_trace_without_recent_return", 0),
        "states": states,
    }


def _write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(rows: list[dict], summary: dict, output_dir: Path, memory_path: Path, map_order: list[str]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "dio_mini_passive_inner_maturity_freshness.csv"
    json_path = output_dir / "dio_mini_passive_inner_maturity_freshness.json"
    md_path = output_dir / "dio_mini_passive_inner_maturity_freshness.md"
    txt_path = output_dir / "dio_mini_passive_inner_maturity_freshness.txt"

    fields = [
        "passive_family_action",
        "freshness_state",
        "inner_memory_state",
        "first_seen_map",
        "last_seen_map",
        "latest_map",
        "map_labels",
        "missing_after_last_seen",
        "map_count",
        "time_span_maps",
        "seen_density",
        "trace_count",
        "seeds",
        "actions",
        "real_reward_sum",
        "avg_similarity",
        "avg_mcm_similarity",
        "passive_only",
        "influences_action",
        "is_gate",
        "is_motoric",
        "time_note",
    ]
    _write_csv(csv_path, rows, fields)
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_inner_maturity_freshness.v1",
                "memory_path": str(memory_path),
                "map_order": map_order,
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

    lines = ["# DIO Mini Passive Inner Maturity Freshness", ""]
    lines.append(f"- memory: {memory_path}")
    lines.append(f"- map_order: {', '.join(map_order)}")
    lines.extend(["", "## Summary"])
    for key, value in summary.items():
        if key == "states":
            continue
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Time Notes"])
    if not rows:
        lines.append("- keine Eintraege")
    for row in rows:
        lines.append(f"- {row['time_note']}")
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Zeit-Leseschicht",
            "- keine Motorik",
            "- kein Gate",
            "- keine Trainingsmemory-Schreibung",
            "- nicht vom aktiven Mini-DIO gelesen",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    txt_path.write_text("\n".join(row["time_note"] for row in rows), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive Mini-DIO inner maturity freshness")
    parser.add_argument("--memory", default="bot_memory/dio_mini_passive_inner_maturity_memory.json")
    parser.add_argument("--map-order", default=",".join(DEFAULT_MAP_ORDER))
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    memory_path = Path(args.memory)
    map_order = _split_order(args.map_order)
    memory = _read_json(memory_path)
    rows = build_rows(memory, map_order)
    summary = build_summary(rows)
    write_outputs(rows, summary, Path(args.output_dir), memory_path, map_order)
    print(
        "passive_inner_maturity_freshness "
        f"rows={summary['row_count']} fresh_stable={summary['fresh_stable_trace']} "
        f"fresh_reorganizing={summary['fresh_reorganizing_trace']} "
        f"stale={summary['stale_trace_without_recent_consequence']}"
    )
    for row in rows[:12]:
        print(f"{row['freshness_state']} {row['passive_family_action']} maps={row['map_labels']}")


if __name__ == "__main__":
    main()
