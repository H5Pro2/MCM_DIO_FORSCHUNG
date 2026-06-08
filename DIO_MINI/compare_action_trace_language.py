"""Compare passive DIO mini action trace language snapshots.

This is a diagnostics-only tool. It compares two trace-language outputs and
reports which DIO families kept the same trace, changed trace, appeared, or
disappeared.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _load_rows(path: Path) -> list[dict]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return [dict(item) for item in data if isinstance(item, dict)]
        raise ValueError(f"Expected JSON list in {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _index_rows(rows: list[dict]) -> dict[str, dict]:
    indexed = {}
    for row in rows:
        family = str(row.get("family", "-") or "-")
        if family == "-":
            continue
        indexed[family] = row
    return indexed


def _classify_trace_change(before: dict, after: dict) -> str:
    before_trace = str(before.get("dio_trace_code", "-") or "-")
    after_trace = str(after.get("dio_trace_code", "-") or "-")
    before_strength = _safe_float(before.get("trace_strength", 0.0))
    after_strength = _safe_float(after.get("trace_strength", 0.0))
    if before_trace != after_trace:
        return "trace_shift"
    if after_strength > before_strength + 0.05:
        return "same_trace_stronger"
    if after_strength < before_strength - 0.05:
        return "same_trace_weaker"
    return "stable_trace"


def compare_traces(baseline_rows: list[dict], current_rows: list[dict]) -> tuple[list[dict], dict]:
    baseline = _index_rows(baseline_rows)
    current = _index_rows(current_rows)
    rows = []
    for family in sorted(set(baseline) | set(current)):
        before = baseline.get(family)
        after = current.get(family)
        if before is None and after is not None:
            state = "new_trace_family"
        elif before is not None and after is None:
            state = "missing_trace_family"
        else:
            state = _classify_trace_change(before or {}, after or {})
        rows.append(
            {
                "family": family,
                "stability_state": state,
                "baseline_trace": str((before or {}).get("dio_trace_code", "-") or "-"),
                "current_trace": str((after or {}).get("dio_trace_code", "-") or "-"),
                "baseline_strength": round(_safe_float((before or {}).get("trace_strength", 0.0)), 6),
                "current_strength": round(_safe_float((after or {}).get("trace_strength", 0.0)), 6),
                "baseline_reward": round(_safe_float((before or {}).get("reward_sum", 0.0)), 6),
                "current_reward": round(_safe_float((after or {}).get("reward_sum", 0.0)), 6),
                "baseline_phases": str((before or {}).get("phases", "-") or "-"),
                "current_phases": str((after or {}).get("phases", "-") or "-"),
            }
        )
    rows.sort(
        key=lambda item: (
            item["stability_state"] == "trace_shift",
            item["stability_state"] == "same_trace_stronger",
            item["stability_state"] == "same_trace_weaker",
            item["stability_state"] == "new_trace_family",
            item["current_strength"],
            item["current_reward"],
        ),
        reverse=True,
    )
    counts: dict[str, int] = {}
    for row in rows:
        key = str(row["stability_state"])
        counts[key] = counts.get(key, 0) + 1
    overview = {
        "stability_counts": counts,
        "stable_reif_handlung": [
            row["family"]
            for row in rows
            if row["stability_state"] == "stable_trace" and row["current_trace"] == "dio_trace_reif_handlung"
        ][:8],
        "trace_shift": [row["family"] for row in rows if row["stability_state"] == "trace_shift"][:8],
        "new_trace_family": [row["family"] for row in rows if row["stability_state"] == "new_trace_family"][:8],
    }
    return rows, overview


def _write_outputs(rows: list[dict], overview: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_action_trace_stability.json").write_text(
        json.dumps(rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "dio_mini_action_trace_stability_overview.json").write_text(
        json.dumps(overview, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    if rows:
        with (output_dir / "dio_mini_action_trace_stability.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    lines = ["# DIO Mini Action Trace Stability", ""]
    lines.append("## Stability Counts")
    for key, value in sorted(dict(overview.get("stability_counts", {}) or {}).items()):
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Trace Shifts")
    for family in overview.get("trace_shift", []) or []:
        lines.append(f"- {family}")
    lines.append("")
    lines.append("## Stable Reif Handlung")
    for family in overview.get("stable_reif_handlung", []) or []:
        lines.append(f"- {family}")
    lines.append("")
    (output_dir / "dio_mini_action_trace_stability.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare passive DIO mini action trace language snapshots")
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--current", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    baseline_rows = _load_rows(Path(args.baseline))
    current_rows = _load_rows(Path(args.current))
    rows, overview = compare_traces(baseline_rows, current_rows)
    _write_outputs(rows, overview, Path(args.output_dir))
    for key, value in sorted(dict(overview.get("stability_counts", {}) or {}).items()):
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
