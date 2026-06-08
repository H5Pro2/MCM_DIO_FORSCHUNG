"""Aggregate DIO mini family persistence across multiple controlled worlds."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.analyze_family_persistence import analyze as analyze_persistence
from DIO_MINI.analyze_family_persistence import summarize as summarize_persistence


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def parse_phase(text: str) -> tuple[str, Path]:
    parts = str(text or "").split(":", 1)
    if len(parts) != 2:
        raise ValueError(f"Phase must use name:path format, got {text!r}")
    return parts[0].strip() or "phase", Path(parts[1].strip())


def build_cross_world(phases: list[tuple[str, Path]]) -> tuple[list[dict], list[dict], list[dict]]:
    phase_rows = []
    phase_summaries = []
    family_world: dict[str, dict] = {}
    for phase_name, debug_root in phases:
        rows = analyze_persistence(debug_root, [])
        summaries = summarize_persistence(rows)
        for row in rows:
            phase_rows.append({"phase": phase_name, **row})
        for row in summaries:
            item = {"phase": phase_name, **row}
            phase_summaries.append(item)
            family = str(row.get("family", "-") or "-")
            record = family_world.setdefault(
                family,
                {
                    "family": family,
                    "phases": set(),
                    "transition_counts": {},
                    "executed_runs": 0,
                    "observed_runs": 0,
                    "held_runs": 0,
                    "raw_runs": 0,
                    "reward_sum": 0.0,
                    "max_trade_readiness": 0.0,
                    "max_mature_transfer": 0.0,
                },
            )
            transition = str(row.get("transition", "unknown") or "unknown")
            record["phases"].add(phase_name)
            record["transition_counts"][transition] = int(record["transition_counts"].get(transition, 0)) + 1
            record["executed_runs"] += _safe_int(row.get("executed_runs", 0))
            record["observed_runs"] += _safe_int(row.get("observed_runs", 0))
            record["held_runs"] += _safe_int(row.get("held_runs", 0))
            record["raw_runs"] += _safe_int(row.get("raw_runs", 0))
            record["reward_sum"] += _safe_float(row.get("reward_sum", 0.0))
            record["max_trade_readiness"] = max(record["max_trade_readiness"], _safe_float(row.get("max_trade_readiness", 0.0)))
            record["max_mature_transfer"] = max(record["max_mature_transfer"], _safe_float(row.get("max_mature_transfer", 0.0)))
    world_rows = []
    for record in family_world.values():
        transitions = dict(record["transition_counts"])
        dominant_transition = "-"
        if transitions:
            dominant_transition = sorted(transitions.items(), key=lambda item: item[1], reverse=True)[0][0]
        world_rows.append(
            {
                "family": record["family"],
                "phases": ",".join(sorted(record["phases"])),
                "phase_count": len(record["phases"]),
                "dominant_transition": dominant_transition,
                "transition_counts": json.dumps(transitions, sort_keys=True),
                "executed_runs": record["executed_runs"],
                "observed_runs": record["observed_runs"],
                "held_runs": record["held_runs"],
                "raw_runs": record["raw_runs"],
                "reward_sum": round(record["reward_sum"], 6),
                "max_trade_readiness": round(record["max_trade_readiness"], 6),
                "max_mature_transfer": round(record["max_mature_transfer"], 6),
            }
        )
    world_rows.sort(
        key=lambda item: (
            item["phase_count"],
            item["executed_runs"],
            item["observed_runs"],
            item["reward_sum"],
        ),
        reverse=True,
    )
    return phase_rows, phase_summaries, world_rows


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(phase_rows: list[dict], phase_summaries: list[dict], world_rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_cross_world_persistence_details.json").write_text(
        json.dumps(phase_rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "dio_mini_cross_world_persistence_phase_summary.json").write_text(
        json.dumps(phase_summaries, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "dio_mini_cross_world_persistence_world_summary.json").write_text(
        json.dumps(world_rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    write_csv(output_dir / "dio_mini_cross_world_persistence_details.csv", phase_rows)
    write_csv(output_dir / "dio_mini_cross_world_persistence_phase_summary.csv", phase_summaries)
    write_csv(output_dir / "dio_mini_cross_world_persistence_world_summary.csv", world_rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze DIO mini persistence across controlled worlds")
    parser.add_argument("--phase", action="append", required=True, help="name:path")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    phases = [parse_phase(item) for item in args.phase]
    phase_rows, phase_summaries, world_rows = build_cross_world(phases)
    write_outputs(phase_rows, phase_summaries, world_rows, Path(args.output_dir))
    for row in world_rows[:16]:
        print(
            f"family={row['family']} phases={row['phase_count']} transition={row['dominant_transition']} "
            f"executed={row['executed_runs']} observed={row['observed_runs']} reward={row['reward_sum']:.4f}"
        )


if __name__ == "__main__":
    main()
