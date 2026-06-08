"""Build a passive core list from stable Mini-DIO inner-map transitions.

The list preserves stable variation-bearing, stable recurrence, and stable
foreign-boundary spaces. It is diagnostic only and must not influence action,
entries, gates, or direction.
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


CORE_STATES = {
    "stable_variation_bearing": "passive_variation_core",
    "stable_recurrence": "passive_recurrence_core",
    "stable_foreign_boundary": "passive_foreign_boundary_core",
}


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value if value not in (None, "") else default)
    except Exception:
        return default
    if result != result:
        return default
    return result


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


def _core_note(row: dict) -> str:
    return (
        f"{row['text_island_symbol']}: {row['inner_core_state']}; "
        f"right={row['right_inner_map_state']}; "
        f"score={row['right_semantic_maturity_score']:.3f}; "
        "passiv, keine Handlung."
    )


def build_rows(compare_rows: list[dict]) -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    for item in compare_rows:
        transition = str(item.get("inner_map_transition_state", "") or "")
        if transition not in CORE_STATES:
            continue
        right_score = _safe_float(item.get("right_semantic_maturity_score"))
        left_score = _safe_float(item.get("left_semantic_maturity_score"))
        row = {
            "text_island_symbol": item.get("text_island_symbol", ""),
            "inner_core_state": CORE_STATES[transition],
            "inner_map_transition_state": transition,
            "left_inner_map_state": item.get("left_inner_map_state", ""),
            "right_inner_map_state": item.get("right_inner_map_state", ""),
            "left_semantic_maturity_score": round(left_score, 9),
            "right_semantic_maturity_score": round(right_score, 9),
            "score_delta": round(_safe_float(item.get("score_delta")), 9),
            "stability_delta": round(_safe_float(item.get("stability_delta")), 9),
            "variation_delta": round(_safe_float(item.get("variation_delta")), 9),
            "drift_delta": round(_safe_float(item.get("drift_delta")), 9),
            "left_families": item.get("left_families", ""),
            "right_families": item.get("right_families", ""),
            **PASSIVE_BOUNDARY,
        }
        row["core_note"] = _core_note(row)
        rows.append(row)

    summary: dict[str, dict] = {}
    for row in rows:
        state = str(row["inner_core_state"])
        bucket = summary.setdefault(
            state,
            {
                "inner_core_state": state,
                "count": 0,
                "avg_right_semantic_maturity_score": 0.0,
                "avg_score_delta": 0.0,
                **PASSIVE_BOUNDARY,
            },
        )
        count = int(bucket["count"])
        bucket["count"] = count + 1
        bucket["avg_right_semantic_maturity_score"] = (
            (float(bucket["avg_right_semantic_maturity_score"]) * count)
            + float(row["right_semantic_maturity_score"])
        ) / max(1, count + 1)
        bucket["avg_score_delta"] = (
            (float(bucket["avg_score_delta"]) * count) + float(row["score_delta"])
        ) / max(1, count + 1)
    summary_rows = []
    for item in summary.values():
        item["avg_right_semantic_maturity_score"] = round(float(item["avg_right_semantic_maturity_score"]), 9)
        item["avg_score_delta"] = round(float(item["avg_score_delta"]), 9)
        summary_rows.append(item)
    return (
        sorted(rows, key=lambda row: (row["inner_core_state"], -float(row["right_semantic_maturity_score"]))),
        sorted(summary_rows, key=lambda row: (-int(row["count"]), row["inner_core_state"])),
    )


def write_outputs(rows: list[dict], summary_rows: list[dict], output_dir: Path, compare_path: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(
        output_dir / "passive_inner_core_list.csv",
        rows,
        [
            "text_island_symbol",
            "inner_core_state",
            "inner_map_transition_state",
            "right_inner_map_state",
            "right_semantic_maturity_score",
            "score_delta",
            "core_note",
        ],
    )
    _write_csv(
        output_dir / "passive_inner_core_list_summary.csv",
        summary_rows,
        ["inner_core_state", "count", "avg_right_semantic_maturity_score", "avg_score_delta"],
    )
    (output_dir / "passive_inner_core_list.json").write_text(
        json.dumps(
            {
                "source_compare": str(compare_path),
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
        "# Passive Inner Core List",
        "",
        f"- source_compare: `{compare_path}`",
        f"- core_items: `{len(rows)}`",
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
            f"- {row['inner_core_state']}: {row['count']} "
            f"(score={row['avg_right_semantic_maturity_score']:.3f}, "
            f"delta={row['avg_score_delta']:.3f})"
        )
    lines.extend(["", "## Core Items", ""])
    for row in rows[:80]:
        lines.append(f"- {row['core_note']}")
    (output_dir / "passive_inner_core_list.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (output_dir / "passive_inner_core_list.txt").write_text(
        "\n".join(row["core_note"] for row in rows) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive inner core list")
    parser.add_argument("--compare", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    rows, summary_rows = build_rows(_read_csv(args.compare))
    write_outputs(rows, summary_rows, args.output_dir, args.compare)
    print(
        json.dumps(
            {
                "source_compare": str(args.compare),
                "core_items": len(rows),
                "summary": {row["inner_core_state"]: row["count"] for row in summary_rows},
                **PASSIVE_BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
