"""Build a passive readable trace from DIO mini action-transition summaries.

The DIO trace codes are debug language, not motor input. They compress the
development state of a family into a short readable line.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


TRACE_BY_CLASS = {
    "matured_action_pattern": ("dio_trace_reif_handlung", "gesehen -> beobachtet -> gehandelt -> bestaetigt"),
    "direct_mature_pattern": ("dio_trace_direkt_reif", "wiederkehrend gehandelt, ohne lokale Uebergangsphase"),
    "observation_maturing_pattern": ("dio_trace_reif_beobachtung", "wiederkehrend beobachtet und handlungsnah"),
    "local_observation_to_action": ("dio_trace_lokal_reift", "lokal beobachtet und spaeter gehandelt"),
    "local_direct_action": ("dio_trace_lokal_direkt", "lokal direkt gehandelt"),
    "held_observation_pattern": ("dio_trace_gehaltene_beobachtung", "gesehen, aber nicht gehandelt"),
    "burdened_action_pattern": ("dio_trace_belastet", "Handlung erzeugte Belastung"),
    "quiet_pattern": ("dio_trace_ruhig", "keine tragende Handlungsnaehe"),
}


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


def _read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _strength(row: dict) -> float:
    reward = max(0.0, _safe_float(row.get("reward_sum", 0.0)))
    phases = _safe_int(row.get("phase_count", 0))
    executed = _safe_int(row.get("executed_rows", 0))
    observed = _safe_int(row.get("observed_rows", 0))
    readiness = max(
        _safe_float(row.get("max_executed_trade_readiness", 0.0)),
        _safe_float(row.get("max_observed_trade_readiness", 0.0)),
    )
    transfer = max(
        _safe_float(row.get("max_executed_mature_transfer", 0.0)),
        _safe_float(row.get("max_observed_mature_transfer", 0.0)),
    )
    return round(
        min(1.0, (reward / 8.0) + (phases * 0.08) + (executed * 0.025) + (observed * 0.01) + readiness + transfer),
        6,
    )


def _state_line(row: dict, trace_code: str, human_hint: str) -> str:
    family = str(row.get("family", "-") or "-")
    phases = str(row.get("phases", "-") or "-")
    return (
        f"{family} | {trace_code} | strength={_strength(row):.6f} | "
        f"phases={phases} | reward={_safe_float(row.get('reward_sum', 0.0)):.6f} | {human_hint}"
    )


def build_trace(rows: list[dict]) -> tuple[list[dict], dict]:
    output = []
    class_counts: dict[str, int] = {}
    for row in rows:
        cls = str(row.get("action_transition_class", "quiet_pattern") or "quiet_pattern")
        trace_code, human_hint = TRACE_BY_CLASS.get(cls, TRACE_BY_CLASS["quiet_pattern"])
        item = {
            "family": row.get("family", "-"),
            "action_transition_class": cls,
            "dio_trace_code": trace_code,
            "trace_strength": _strength(row),
            "phases": row.get("phases", "-"),
            "phase_count": _safe_int(row.get("phase_count", 0)),
            "reward_sum": round(_safe_float(row.get("reward_sum", 0.0)), 6),
            "executed_rows": _safe_int(row.get("executed_rows", 0)),
            "observed_rows": _safe_int(row.get("observed_rows", 0)),
            "direct_positive_action": _safe_int(row.get("direct_positive_action", 0)),
            "observation_to_positive_action": _safe_int(row.get("observation_to_positive_action", 0)),
            "held_observation": _safe_int(row.get("held_observation", 0)),
            "human_hint": human_hint,
            "trace_line": _state_line(row, trace_code, human_hint),
        }
        class_counts[trace_code] = class_counts.get(trace_code, 0) + 1
        output.append(item)
    output.sort(
        key=lambda item: (
            item["dio_trace_code"] == "dio_trace_reif_handlung",
            item["dio_trace_code"] == "dio_trace_lokal_reift",
            item["dio_trace_code"] == "dio_trace_direkt_reif",
            item["trace_strength"],
            item["reward_sum"],
        ),
        reverse=True,
    )
    overview = {
        "trace_counts": class_counts,
        "top_reif_handlung": [row["family"] for row in output if row["dio_trace_code"] == "dio_trace_reif_handlung"][:8],
        "top_lokal_reift": [row["family"] for row in output if row["dio_trace_code"] == "dio_trace_lokal_reift"][:8],
        "top_gehaltene_beobachtung": [
            row["family"] for row in output if row["dio_trace_code"] == "dio_trace_gehaltene_beobachtung"
        ][:8],
    }
    return output, overview


def write_outputs(rows: list[dict], overview: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_action_trace_language.json").write_text(
        json.dumps(rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "dio_mini_action_trace_language_overview.json").write_text(
        json.dumps(overview, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    if rows:
        with (output_dir / "dio_mini_action_trace_language.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    lines = ["# DIO Mini Action Trace Language", ""]
    lines.append("## Trace Counts")
    for key, value in sorted(dict(overview.get("trace_counts", {}) or {}).items()):
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Trace Lines")
    for row in rows[:24]:
        lines.append(f"- {row['trace_line']}")
    lines.append("")
    (output_dir / "dio_mini_action_trace_language.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive DIO mini action trace language")
    parser.add_argument("--world-summary", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    rows = _read_rows(Path(args.world_summary))
    trace_rows, overview = build_trace(rows)
    write_outputs(trace_rows, overview, Path(args.output_dir))
    for row in trace_rows[:16]:
        print(row["trace_line"])


if __name__ == "__main__":
    main()
