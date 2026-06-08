"""Compact transition matrix for passive anchor/exchange sensor reports.

Diagnostic only. It reads existing passive report outputs and summarizes how
text-island anchor exchange behaves across variant transitions.
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
    output_fields = list(fields)
    for row in rows:
        for key in row:
            if key not in output_fields:
                output_fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=output_fields)
        writer.writeheader()
        writer.writerows(rows)


def _summary_value(rows: list[dict], group: str, state: str, field: str = "count") -> float:
    for row in rows:
        if str(row.get("summary_group", "") or "") == group and str(row.get("state", "") or "") == state:
            return _safe_float(row.get(field))
    return 0.0


def _dominant_sensor(sensor_summary: list[dict]) -> str:
    states = [
        row
        for row in sensor_summary
        if str(row.get("summary_group", "") or "") == "sensor_exchange_state"
    ]
    if not states:
        return "unknown"
    ordered = sorted(states, key=lambda row: (-_safe_int(row.get("count")), str(row.get("state", ""))))
    return str(ordered[0].get("state", "") or "unknown")


def _build_row(label: str, anchor_dir: Path, sensor_dir: Path) -> dict:
    anchor_summary = _read_csv(anchor_dir / "passive_anchor_exchange_lupe_summary.csv")
    sensor_summary = _read_csv(sensor_dir / "passive_anchor_exchange_sensor_lupe_summary.csv")
    return {
        "transition": label,
        "same_family_basis": int(_summary_value(anchor_summary, "anchor_exchange_state", "same_family_basis")),
        "new_text_island": int(_summary_value(anchor_summary, "anchor_exchange_state", "new_text_island")),
        "anchor_exchange_count": int(_summary_value(anchor_summary, "anchor_exchange_state", "anchor_exchange")),
        "anchor_expansion": int(_summary_value(anchor_summary, "anchor_exchange_state", "anchor_expansion")),
        "anchor_thinning": int(_summary_value(anchor_summary, "anchor_exchange_state", "anchor_thinning")),
        "avg_family_stability": round(_summary_value(anchor_summary, "totals", "anchor_exchange", "avg_family_stability"), 9),
        "avg_score_delta": round(_summary_value(anchor_summary, "totals", "anchor_exchange", "avg_score_delta"), 9),
        "dominant_sensor_axis": _dominant_sensor(sensor_summary),
        "visual_dominant_count": int(_summary_value(sensor_summary, "sensor_exchange_state", "visual_dominant_delta")),
        "hearing_dominant_count": int(_summary_value(sensor_summary, "sensor_exchange_state", "hearing_dominant_delta")),
        "feeling_dominant_count": int(_summary_value(sensor_summary, "sensor_exchange_state", "feeling_dominant_delta")),
        "neuro_dominant_count": int(_summary_value(sensor_summary, "sensor_exchange_state", "neuro_dominant_delta")),
        "mixed_sensor_count": int(_summary_value(sensor_summary, "sensor_exchange_state", "mixed_sensor_delta")),
        "avg_visual_exchange_distance": round(_summary_value(sensor_summary, "avg_exchange_distance", "visual", "value"), 9),
        "avg_hearing_exchange_distance": round(_summary_value(sensor_summary, "avg_exchange_distance", "hearing", "value"), 9),
        "avg_feeling_exchange_distance": round(_summary_value(sensor_summary, "avg_exchange_distance", "feeling", "value"), 9),
        "avg_neuro_exchange_distance": round(_summary_value(sensor_summary, "avg_exchange_distance", "neuro", "value"), 9),
        **PASSIVE_BOUNDARY,
    }


def write_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fields = [
        "transition",
        "same_family_basis",
        "new_text_island",
        "anchor_exchange_count",
        "anchor_expansion",
        "anchor_thinning",
        "avg_family_stability",
        "avg_score_delta",
        "dominant_sensor_axis",
        "visual_dominant_count",
        "hearing_dominant_count",
        "feeling_dominant_count",
        "neuro_dominant_count",
        "mixed_sensor_count",
        "avg_visual_exchange_distance",
        "avg_hearing_exchange_distance",
        "avg_feeling_exchange_distance",
        "avg_neuro_exchange_distance",
    ]
    _write_csv(output_dir / "passive_anchor_exchange_transition_matrix.csv", rows, fields)
    payload = {
        "schema": "dio_mini_passive_anchor_exchange_transition_matrix.v1",
        "boundary": dict(PASSIVE_BOUNDARY),
        "transitions": rows,
    }
    (output_dir / "passive_anchor_exchange_transition_matrix.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    lines = [
        "# Mini-DIO Passive Anchor/Exchange Transition Matrix",
        "",
        "## Grenze",
        "- Nur Diagnose.",
        "- Keine Runtime-Lesung.",
        "- Keine Handlung.",
        "- Kein Gate.",
        "- Kein Entry.",
        "- Keine Richtung.",
        "",
        "## Matrix",
    ]
    for row in rows:
        lines.append(
            f"- {row['transition']}: anchor_exchange={row['anchor_exchange_count']}; "
            f"dominant={row['dominant_sensor_axis']}; "
            f"family_stability={row['avg_family_stability']}; "
            f"score_delta={row['avg_score_delta']}; "
            f"dist(visual/hearing/feeling/neuro)="
            f"{row['avg_visual_exchange_distance']}/"
            f"{row['avg_hearing_exchange_distance']}/"
            f"{row['avg_feeling_exchange_distance']}/"
            f"{row['avg_neuro_exchange_distance']}"
        )
    lines.extend(
        [
            "",
            "## Lesart",
            "Hoeren/Energie ist in den geprueften Uebergaengen bisher die haeufigste dominante Austauschachse.",
            "Das ist eine passive Diagnose und keine Handlungslogik.",
        ]
    )
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive anchor/exchange transition matrix.")
    parser.add_argument("--transition", action="append", nargs=3, metavar=("LABEL", "ANCHOR_DIR", "SENSOR_DIR"), required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    rows = [_build_row(label, Path(anchor_dir), Path(sensor_dir)) for label, anchor_dir, sensor_dir in args.transition]
    write_outputs(rows, args.output_dir)
    print(
        json.dumps(
            {
                "output_dir": str(args.output_dir),
                "transition_count": len(rows),
                "transitions": rows,
                **PASSIVE_BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
