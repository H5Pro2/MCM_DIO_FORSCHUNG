"""Aggregate passive sensor maturity across DIO mini controlled worlds."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.analyze_sensor_maturity import analyze as analyze_sensor_maturity


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


def build_cross_world(phases: list[tuple[str, Path]]) -> tuple[list[dict], list[dict]]:
    phase_rows = []
    families: dict[str, dict] = {}
    for phase_name, debug_root in phases:
        rows = analyze_sensor_maturity(debug_root)
        for row in rows:
            phase_row = {"phase": phase_name, **row}
            phase_rows.append(phase_row)
            family = str(row.get("family", "-") or "-")
            record = families.setdefault(
                family,
                {
                    "family": family,
                    "phases": set(),
                    "rows": 0,
                    "executed": 0,
                    "positive_executed": 0,
                    "burdened_executed": 0,
                    "observed_potential": 0,
                    "held_same_episode": 0,
                    "reward_sum": 0.0,
                    "visual_mcm_weighted_sum": 0.0,
                    "tone_tension_weighted_sum": 0.0,
                    "max_trade_readiness": 0.0,
                    "max_mature_transfer": 0.0,
                },
            )
            count = max(1, _safe_int(row.get("rows", 0)))
            record["phases"].add(phase_name)
            record["rows"] += _safe_int(row.get("rows", 0))
            record["executed"] += _safe_int(row.get("executed", 0))
            record["positive_executed"] += _safe_int(row.get("positive_executed", 0))
            record["burdened_executed"] += _safe_int(row.get("burdened_executed", 0))
            record["observed_potential"] += _safe_int(row.get("observed_potential", 0))
            record["held_same_episode"] += _safe_int(row.get("held_same_episode", 0))
            record["reward_sum"] += _safe_float(row.get("reward_sum", 0.0))
            record["visual_mcm_weighted_sum"] += _safe_float(row.get("visual_mcm_alignment_trace", 0.0)) * count
            record["tone_tension_weighted_sum"] += _safe_float(row.get("tone_tension_resonance_trace", 0.0)) * count
            record["max_trade_readiness"] = max(record["max_trade_readiness"], _safe_float(row.get("max_trade_readiness", 0.0)))
            record["max_mature_transfer"] = max(record["max_mature_transfer"], _safe_float(row.get("max_mature_transfer", 0.0)))

    world_rows = []
    for record in families.values():
        rows_count = max(1, _safe_int(record.get("rows", 0)))
        world_rows.append(
            {
                "family": record["family"],
                "phases": ",".join(sorted(record["phases"])),
                "phase_count": len(record["phases"]),
                "rows": record["rows"],
                "executed": record["executed"],
                "positive_executed": record["positive_executed"],
                "burdened_executed": record["burdened_executed"],
                "observed_potential": record["observed_potential"],
                "held_same_episode": record["held_same_episode"],
                "reward_sum": round(record["reward_sum"], 6),
                "avg_visual_mcm_alignment_trace": round(record["visual_mcm_weighted_sum"] / rows_count, 6),
                "avg_tone_tension_resonance_trace": round(record["tone_tension_weighted_sum"] / rows_count, 6),
                "max_trade_readiness": round(record["max_trade_readiness"], 6),
                "max_mature_transfer": round(record["max_mature_transfer"], 6),
            }
        )
    world_rows.sort(
        key=lambda item: (
            item["phase_count"],
            item["positive_executed"],
            item["reward_sum"],
            item["observed_potential"],
            item["avg_visual_mcm_alignment_trace"],
            item["avg_tone_tension_resonance_trace"],
        ),
        reverse=True,
    )
    return phase_rows, world_rows


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(phase_rows: list[dict], world_rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_cross_world_sensor_maturity_phase_rows.json").write_text(
        json.dumps(phase_rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "dio_mini_cross_world_sensor_maturity_world_summary.json").write_text(
        json.dumps(world_rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    write_csv(output_dir / "dio_mini_cross_world_sensor_maturity_phase_rows.csv", phase_rows)
    write_csv(output_dir / "dio_mini_cross_world_sensor_maturity_world_summary.csv", world_rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze DIO mini sensor maturity across controlled worlds")
    parser.add_argument("--phase", action="append", required=True, help="name:path")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    phases = [parse_phase(item) for item in args.phase]
    phase_rows, world_rows = build_cross_world(phases)
    write_outputs(phase_rows, world_rows, Path(args.output_dir))
    for row in world_rows[:16]:
        print(
            f"family={row['family']} phases={row['phase_count']} executed={row['executed']} "
            f"observed={row['observed_potential']} reward={row['reward_sum']:.4f} "
            f"visual_mcm={row['avg_visual_mcm_alignment_trace']:.4f} "
            f"tone_tension={row['avg_tone_tension_resonance_trace']:.4f}"
        )


if __name__ == "__main__":
    main()
