"""Build a passive inner-awareness map from mature Mini-DIO text islands.

This report turns text-island maturity into a diagnostic inner map. It is not
read by Mini-DIO for action and must not influence gates, entries, or direction.
"""

from __future__ import annotations

import argparse
import csv
import json
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


def _inner_map_state(maturity_state: str, score: float, drift: float, variation: float, foreign: float) -> str:
    if maturity_state == "variant_resilient_text_island" and score >= 0.62:
        return "inner_variation_bearing_space"
    if maturity_state == "stable_recurrent_text_island":
        return "inner_stable_recurrence_space"
    if maturity_state == "drifting_unstable_text_island" or drift > 0.35:
        return "inner_drift_watch_space"
    if maturity_state == "foreign_separated_text_island" or foreign > 0.45:
        return "inner_foreign_boundary_space"
    if maturity_state == "variant_resilient_text_island":
        return "inner_soft_variation_space"
    if maturity_state == "new_unconfirmed_text_island" and variation > 0.0:
        return "inner_unconfirmed_movement_space"
    return "inner_unconfirmed_raw_space"


def _inner_note(row: dict) -> str:
    return (
        f"{row['text_island_symbol']}: {row['inner_map_state']}; "
        f"score={row['semantic_maturity_score']:.3f}; "
        f"stable={row['stability_pressure']:.3f}; "
        f"var={row['variation_bearing']:.3f}; "
        "passiv, keine Handlung."
    )


def build_rows(maturity_rows: list[dict]) -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    for item in maturity_rows:
        symbol = str(item.get("text_island_symbol", "") or "")
        if not symbol:
            continue
        maturity_state = str(item.get("text_island_maturity_state", "") or "")
        score = _safe_float(item.get("semantic_maturity_score"))
        density_stability = _safe_float(item.get("density_stability"))
        variation = _safe_float(item.get("variation_tolerance"))
        foreign = _safe_float(item.get("foreign_separation"))
        drift = _safe_float(item.get("drift_pressure"))
        recurrence = _safe_int(item.get("recurrence_count"))
        family_count = _safe_int(item.get("family_count"))
        state = _inner_map_state(maturity_state, score, drift, variation, foreign)
        stability_pressure = max(0.0, min(1.0, (density_stability * 0.55) + (min(1.0, recurrence / 4.0) * 0.45)))
        variation_bearing = max(0.0, min(1.0, (variation * 0.60) + (score * 0.40)))
        boundary_clarity = max(0.0, min(1.0, foreign + (1.0 if state == "inner_foreign_boundary_space" else 0.0) * 0.25))
        rawness = max(0.0, min(1.0, 1.0 - score))
        row = {
            "text_island_symbol": symbol,
            "inner_map_state": state,
            "text_island_maturity_state": maturity_state,
            "semantic_maturity_score": round(score, 9),
            "stability_pressure": round(stability_pressure, 9),
            "variation_bearing": round(variation_bearing, 9),
            "boundary_clarity": round(boundary_clarity, 9),
            "drift_pressure": round(drift, 9),
            "rawness": round(rawness, 9),
            "recurrence_count": recurrence,
            "family_count": family_count,
            "families": item.get("families", ""),
            **PASSIVE_BOUNDARY,
        }
        row["inner_map_note"] = _inner_note(row)
        rows.append(row)

    summary: dict[str, dict] = {}
    for row in rows:
        state = row["inner_map_state"]
        bucket = summary.setdefault(
            state,
            {
                "inner_map_state": state,
                "count": 0,
                "avg_semantic_maturity_score": 0.0,
                "avg_stability_pressure": 0.0,
                "avg_variation_bearing": 0.0,
                "avg_drift_pressure": 0.0,
                **PASSIVE_BOUNDARY,
            },
        )
        count = int(bucket["count"])
        bucket["count"] = count + 1
        for key in [
            "avg_semantic_maturity_score",
            "avg_stability_pressure",
            "avg_variation_bearing",
            "avg_drift_pressure",
        ]:
            row_key = key.replace("avg_", "")
            bucket[key] = ((float(bucket[key]) * count) + float(row.get(row_key, 0.0))) / max(1, count + 1)
    summary_rows = []
    for item in summary.values():
        for key in [
            "avg_semantic_maturity_score",
            "avg_stability_pressure",
            "avg_variation_bearing",
            "avg_drift_pressure",
        ]:
            item[key] = round(float(item[key]), 9)
        summary_rows.append(item)
    return rows, sorted(summary_rows, key=lambda row: (-int(row["count"]), row["inner_map_state"]))


def write_outputs(rows: list[dict], summary_rows: list[dict], output_dir: Path, maturity_path: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(
        output_dir / "passive_text_island_inner_map.csv",
        rows,
        [
            "text_island_symbol",
            "inner_map_state",
            "text_island_maturity_state",
            "semantic_maturity_score",
            "stability_pressure",
            "variation_bearing",
            "boundary_clarity",
            "drift_pressure",
            "rawness",
            "inner_map_note",
        ],
    )
    _write_csv(
        output_dir / "passive_text_island_inner_map_summary.csv",
        summary_rows,
        [
            "inner_map_state",
            "count",
            "avg_semantic_maturity_score",
            "avg_stability_pressure",
            "avg_variation_bearing",
            "avg_drift_pressure",
        ],
    )
    (output_dir / "passive_text_island_inner_map.json").write_text(
        json.dumps(
            {
                "source_maturity": str(maturity_path),
                "rows": rows,
                "summary": summary_rows,
                "boundary": PASSIVE_BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Passive Text Island Inner Map",
        "",
        f"- source_maturity: `{maturity_path}`",
        f"- text_islands: `{len(rows)}`",
        "",
        "## Grenze",
        "",
        "- passiv",
        "- keine Runtime-Lesung",
        "- keine Handlung",
        "- kein Gate",
        "- kein Entry",
        "- keine Richtung",
        "",
        "## Summary",
        "",
    ]
    for row in summary_rows:
        lines.append(
            f"- {row['inner_map_state']}: {row['count']} "
            f"(score={row['avg_semantic_maturity_score']:.3f}, "
            f"stabil={row['avg_stability_pressure']:.3f}, "
            f"var={row['avg_variation_bearing']:.3f})"
        )
    lines.extend(["", "## Tragende Innenraeume", ""])
    for row in sorted(rows, key=lambda item: float(item["semantic_maturity_score"]), reverse=True)[:30]:
        lines.append(f"- {row['inner_map_note']}")
    (output_dir / "passive_text_island_inner_map.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (output_dir / "passive_text_island_inner_map.txt").write_text(
        "\n".join(row["inner_map_note"] for row in rows) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive text-island inner map")
    parser.add_argument("--maturity", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    maturity_rows = _read_csv(args.maturity)
    rows, summary_rows = build_rows(maturity_rows)
    write_outputs(rows, summary_rows, args.output_dir, args.maturity)
    print(
        json.dumps(
            {
                "source_maturity": str(args.maturity),
                "text_islands": len(rows),
                "summary": {row["inner_map_state"]: row["count"] for row in summary_rows},
                **PASSIVE_BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
