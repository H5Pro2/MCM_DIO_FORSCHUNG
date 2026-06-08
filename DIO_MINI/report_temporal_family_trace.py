"""Report passive temporal family traces for Mini-DIO."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _int(value: object, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _run_number(path: Path) -> int:
    try:
        return int(path.name.rsplit("_", 1)[-1])
    except Exception:
        return 0


def load_episode_rows(debug_root: Path) -> list[dict]:
    rows: list[dict] = []
    for path in sorted(debug_root.glob("dio_mini_lauf_*/episodes.csv"), key=lambda p: _run_number(p.parent)):
        run = _run_number(path.parent)
        with path.open("r", newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                row["run"] = run
                rows.append(row)
    return rows


def load_memory(memory_path: Path | None) -> dict:
    if memory_path is None or not memory_path.exists():
        return {}
    return json.loads(memory_path.read_text(encoding="utf-8"))


def build_report(rows: list[dict], memory: dict) -> dict:
    families: dict[str, dict] = {}
    state_counts: dict[str, int] = {}
    for row in rows:
        family = str(row.get("symbol_family", "-") or "-")
        temporal_state = str(row.get("mini_temporal_state", "-") or "-")
        state_counts[temporal_state] = int(state_counts.get(temporal_state, 0) or 0) + 1
        state = families.setdefault(
            family,
            {
                "family": family,
                "rows": 0,
                "runs": set(),
                "states": {},
                "trades": 0,
                "tp": 0,
                "sl": 0,
                "reward_sum": 0.0,
                "max_afterimage": 0.0,
                "max_recurrence_strength": 0.0,
                "max_temporal_trust_support": 0.0,
                "max_temporal_caution_support": 0.0,
                "avg_time_distance_sum": 0.0,
            },
        )
        state["rows"] += 1
        state["runs"].add(_int(row.get("run")))
        state["states"][temporal_state] = int(state["states"].get(temporal_state, 0) or 0) + 1
        action = str(row.get("action", "") or "").upper()
        if action in ("LONG", "SHORT"):
            state["trades"] += 1
        outcome_event = str(row.get("outcome_event", "") or "")
        state["tp"] += 1 if outcome_event == "TP" else 0
        state["sl"] += 1 if outcome_event == "SL" else 0
        state["reward_sum"] += _float(row.get("reward"))
        state["max_afterimage"] = max(float(state["max_afterimage"]), _float(row.get("mini_afterimage")))
        state["max_recurrence_strength"] = max(
            float(state["max_recurrence_strength"]),
            _float(row.get("mini_recurrence_strength")),
        )
        state["max_temporal_trust_support"] = max(
            float(state["max_temporal_trust_support"]),
            _float(row.get("mini_temporal_trust_support")),
        )
        state["max_temporal_caution_support"] = max(
            float(state["max_temporal_caution_support"]),
            _float(row.get("mini_temporal_caution_support")),
        )
        state["avg_time_distance_sum"] += _float(row.get("mini_time_distance"))

    memory_temporal = dict(memory.get("temporal_families", {}) or {})
    compact_families = []
    for state in families.values():
        rows_count = max(1, int(state["rows"]))
        memory_state = dict(memory_temporal.get(state["family"], {}) or {})
        compact_families.append(
            {
                "family": state["family"],
                "rows": int(state["rows"]),
                "runs": sorted(int(item) for item in state["runs"] if item),
                "states": dict(state["states"]),
                "trades": int(state["trades"]),
                "tp": int(state["tp"]),
                "sl": int(state["sl"]),
                "reward_sum": float(state["reward_sum"]),
                "max_afterimage": float(state["max_afterimage"]),
                "max_recurrence_strength": float(state["max_recurrence_strength"]),
                "max_temporal_trust_support": float(state["max_temporal_trust_support"]),
                "max_temporal_caution_support": float(state["max_temporal_caution_support"]),
                "avg_time_distance": float(state["avg_time_distance_sum"]) / rows_count,
                "memory_seen_count": _int(memory_state.get("seen_count")),
                "memory_last_state": str(memory_state.get("last_temporal_state", "") or ""),
                "memory_max_afterimage": _float(memory_state.get("max_afterimage")),
                "memory_max_trust_support": _float(memory_state.get("max_temporal_trust_support")),
                "memory_max_caution_support": _float(memory_state.get("max_temporal_caution_support")),
            }
        )

    compact_families.sort(
        key=lambda item: (
            item["max_temporal_trust_support"],
            item["max_afterimage"],
            item["rows"],
            -item["max_temporal_caution_support"],
        ),
        reverse=True,
    )
    return {
        "rows_scanned": len(rows),
        "families": compact_families,
        "temporal_state_counts": dict(sorted(state_counts.items())),
        "top_families": compact_families[:16],
    }


def write_outputs(report: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "temporal_family_trace_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    rows = list(report.get("families", []) or [])
    if rows:
        with (output_dir / "temporal_family_trace.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    lines = [
        "MINI DIO TEMPORAL FAMILY TRACE",
        f"rows_scanned={report.get('rows_scanned', 0)}",
        f"temporal_state_counts={report.get('temporal_state_counts', {})}",
        "",
        "TOP FAMILIES",
    ]
    for family in report.get("top_families", []) or []:
        lines.append(
            f"{family['family']}: rows={family['rows']} trades={family['trades']} "
            f"tp={family['tp']} sl={family['sl']} reward={family['reward_sum']:.6f} "
            f"afterimage={family['max_afterimage']:.6f} recurrence={family['max_recurrence_strength']:.6f} "
            f"trust_support={family['max_temporal_trust_support']:.6f} "
            f"caution_support={family['max_temporal_caution_support']:.6f} "
            f"memory_seen={family['memory_seen_count']} states={family['states']}"
        )
    (output_dir / "temporal_family_trace_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Mini-DIO passive temporal family trace report")
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--memory")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    rows = load_episode_rows(Path(args.debug_root))
    memory = load_memory(Path(args.memory) if args.memory else None)
    report = build_report(rows, memory)
    write_outputs(report, Path(args.output))
    print(json.dumps({k: report[k] for k in ("rows_scanned", "temporal_state_counts")}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
