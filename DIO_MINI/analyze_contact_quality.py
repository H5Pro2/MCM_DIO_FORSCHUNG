"""Build a passive contact quality view from DIO mini semantic memory."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.analyze_timing_memory import analyze as analyze_timing_memory


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value)
    except Exception:
        return default
    if result != result:
        return default
    return result


def build_quality(memory_path: Path) -> list[dict]:
    result = analyze_timing_memory(memory_path)
    rows = []
    for row in result.get("family_rows", []) or []:
        avg_reward = _safe_float(row.get("avg_reward", 0.0))
        avg_timing = _safe_float(row.get("avg_timing_improvement", 0.0))
        trust = _safe_float(row.get("trust", 0.0))
        caution = _safe_float(row.get("caution", 0.0))
        consequence_balance = trust - caution
        carrying = max(0.0, avg_reward) * max(0.0, trust - caution)
        timing_residue = max(0.0, avg_timing)
        timing_to_carrying = timing_residue / max(1e-9, carrying)
        rows.append(
            {
                "family": row.get("name", "-"),
                "action": row.get("action", "-"),
                "count": row.get("count", 0),
                "avg_reward": row.get("avg_reward", 0.0),
                "trust": row.get("trust", 0.0),
                "caution": row.get("caution", 0.0),
                "consequence_balance": round(consequence_balance, 6),
                "avg_timing_improvement": row.get("avg_timing_improvement", 0.0),
                "carrying_trace": round(carrying, 6),
                "timing_residue": round(timing_residue, 6),
                "timing_to_carrying": round(timing_to_carrying, 6),
            }
        )
    rows.sort(
        key=lambda item: (
            item["carrying_trace"],
            -item["timing_residue"],
            item["count"],
        ),
        reverse=True,
    )
    return rows


def write_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_contact_quality.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    if rows:
        with (output_dir / "dio_mini_contact_quality.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze passive DIO mini contact quality")
    parser.add_argument("--memory", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    rows = build_quality(Path(args.memory))
    write_outputs(rows, Path(args.output_dir))
    for row in rows[:12]:
        print(
            f"family={row['family']} action={row['action']} count={row['count']} "
            f"balance={row['consequence_balance']:.4f} carrying={row['carrying_trace']:.4f} timing={row['timing_residue']:.6f} "
            f"timing_to_carrying={row['timing_to_carrying']:.6f}"
        )


if __name__ == "__main__":
    main()
