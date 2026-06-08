"""Inspect passive text islands that reorganized into core-near states.

Diagnostic only. The report reads a passive text-island reorganization history
and filters `reorganized_into_core` trajectories. It does not write runtime
memory and does not influence Mini-DIO action.
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


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(fallback_fields)
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _count(values: list[str]) -> dict[str, int]:
    result: dict[str, int] = {}
    for value in values:
        key = value or "unknown"
        result[key] = result.get(key, 0) + 1
    return dict(sorted(result.items(), key=lambda item: (-item[1], item[0])))


def _core_entry_mode(row: dict) -> str:
    state_path = str(row.get("state_path", "") or "")
    parts = [part.strip() for part in state_path.split("->") if part.strip()]
    first = parts[0] if parts else ""
    last = parts[-1] if parts else ""
    if first == "absent" and last == "inner_stable_recurrence_space":
        return "new_raw_to_stable_recurrence"
    if first == "inner_drift_watch_space" and last == "inner_stable_recurrence_space":
        return "drift_to_stable_recurrence"
    if first == "inner_soft_variation_space" and last == "inner_variation_bearing_space":
        return "soft_variation_to_variation_core"
    if last == "inner_variation_bearing_space":
        return "to_variation_core"
    if last == "inner_stable_recurrence_space":
        return "to_stable_recurrence_core"
    return "other_core_reorganization"


def build_report(history_rows: list[dict]) -> tuple[list[dict], list[dict]]:
    rows = [
        row
        for row in history_rows
        if str(row.get("trajectory_state", "") or "") == "reorganized_into_core"
    ]
    detail: list[dict] = []
    for row in rows:
        first_families = [
            item for item in str(row.get("first_families", "") or "").split("|") if item
        ]
        last_families = [
            item for item in str(row.get("last_families", "") or "").split("|") if item
        ]
        first_set = set(first_families)
        last_set = set(last_families)
        overlap = len(first_set & last_set) / max(1, len(first_set | last_set))
        detail.append(
            {
                "text_island_symbol": str(row.get("text_island_symbol", "") or ""),
                "core_entry_mode": _core_entry_mode(row),
                "family_change_state": str(row.get("family_change_state", "") or ""),
                "state_path": str(row.get("state_path", "") or ""),
                "maturity_path": str(row.get("maturity_path", "") or ""),
                "score_path": str(row.get("score_path", "") or ""),
                "family_count_path": str(row.get("family_count_path", "") or ""),
                "score_delta": round(_safe_float(row.get("score_delta")), 9),
                "last_score": round(_safe_float(row.get("last_score")), 9),
                "max_stability_pressure": round(_safe_float(row.get("max_stability_pressure")), 9),
                "max_variation_bearing": round(_safe_float(row.get("max_variation_bearing")), 9),
                "max_drift_pressure": round(_safe_float(row.get("max_drift_pressure")), 9),
                "first_family_count": len(first_families),
                "last_family_count": len(last_families),
                "family_overlap": round(overlap, 9),
                "last_families": "|".join(last_families),
                "dio_reorganization_sentence": (
                    f"{row.get('text_island_symbol', '')}: {_core_entry_mode(row)}; "
                    f"{row.get('state_path', '')}; families={row.get('family_change_state', '')}; "
                    "passiv, keine Handlung."
                ),
                **PASSIVE_BOUNDARY,
            }
        )

    summary: list[dict] = []
    mode_counts = _count([str(row.get("core_entry_mode", "") or "") for row in detail])
    family_counts = _count([str(row.get("family_change_state", "") or "") for row in detail])
    for key, value in mode_counts.items():
        summary.append({"summary_group": "core_entry_mode", "state": key, "count": value, **PASSIVE_BOUNDARY})
    for key, value in family_counts.items():
        summary.append({"summary_group": "family_change_state", "state": key, "count": value, **PASSIVE_BOUNDARY})
    summary.append(
        {
            "summary_group": "totals",
            "state": "reorganized_into_core",
            "count": len(detail),
            "avg_score_delta": round(sum(_safe_float(row.get("score_delta")) for row in detail) / max(1, len(detail)), 9),
            "avg_family_overlap": round(sum(_safe_float(row.get("family_overlap")) for row in detail) / max(1, len(detail)), 9),
            **PASSIVE_BOUNDARY,
        }
    )
    return detail, summary


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(
        output_dir / "passive_reorganized_core_lupe.csv",
        detail,
        [
            "text_island_symbol",
            "core_entry_mode",
            "family_change_state",
            "state_path",
            "score_delta",
            "last_score",
            "family_overlap",
        ],
    )
    _write_csv(
        output_dir / "passive_reorganized_core_lupe_summary.csv",
        summary,
        ["summary_group", "state", "count", "avg_score_delta", "avg_family_overlap"],
    )
    payload = {
        "schema": "dio_mini_passive_reorganized_core_lupe.v1",
        "boundary": dict(PASSIVE_BOUNDARY),
        "detail": detail,
        "summary": summary,
    }
    (output_dir / "passive_reorganized_core_lupe.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    lines = [
        "# Mini-DIO Passive Reorganized-Core Lupe",
        "",
        "## Grenze",
        "- Nur Diagnose.",
        "- Keine Runtime-Lesung.",
        "- Keine Handlung.",
        "- Kein Gate.",
        "- Kein Entry.",
        "- Keine Richtung.",
        "",
        "## Summary",
    ]
    for row in summary:
        extra = ""
        if "avg_score_delta" in row:
            extra = f"; avg_score_delta={row.get('avg_score_delta')}; avg_family_overlap={row.get('avg_family_overlap')}"
        lines.append(f"- {row.get('summary_group')}:{row.get('state')} = {row.get('count')}{extra}")
    lines.extend(["", "## Top Score-Zuwachs"])
    for row in sorted(detail, key=lambda item: _safe_float(item.get("score_delta")), reverse=True)[:12]:
        lines.append(
            f"- {row.get('text_island_symbol')}: {row.get('core_entry_mode')}; "
            f"score_delta={row.get('score_delta')}; families={row.get('family_change_state')}"
        )
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect passive reorganized_into_core text islands.")
    parser.add_argument("--history", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    detail, summary = build_report(_read_csv(args.history))
    write_outputs(detail, summary, args.output_dir)
    print(
        json.dumps(
            {
                "output_dir": str(args.output_dir),
                "reorganized_core_items": len(detail),
                **PASSIVE_BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
