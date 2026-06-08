"""Compare passive Mini-DIO inner-core lists.

This lupe checks whether concrete text-island core symbols stay stable between
two passive core-list reports. It is diagnostic only and must not influence
action, entries, gates, or direction.
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


def _index(rows: list[dict]) -> dict[str, dict]:
    return {str(row.get("text_island_symbol", "") or ""): row for row in rows if row.get("text_island_symbol")}


def _state(left: dict | None, right: dict | None) -> str:
    if left and right:
        left_state = str(left.get("inner_core_state", "") or "")
        right_state = str(right.get("inner_core_state", "") or "")
        if left_state == right_state:
            if right_state == "passive_variation_core":
                return "stable_passive_variation_core"
            if right_state == "passive_recurrence_core":
                return "stable_passive_recurrence_core"
            if right_state == "passive_foreign_boundary_core":
                return "stable_passive_foreign_boundary_core"
            return "stable_passive_core"
        return "passive_core_state_shift"
    if left and not right:
        return f"lost_{str(left.get('inner_core_state', 'passive_core') or 'passive_core')}"
    if right and not left:
        return f"new_{str(right.get('inner_core_state', 'passive_core') or 'passive_core')}"
    return "empty"


def _note(row: dict) -> str:
    symbol = row["text_island_symbol"]
    state = row["core_stability_state"]
    if state.startswith("stable_"):
        return f"{symbol}: stabiler passiver Kern; {state}; keine Handlung."
    if state.startswith("lost_"):
        return f"{symbol}: Kern in rechter Variante nicht mehr als Kern sichtbar; {state}; nur Diagnose."
    if state.startswith("new_"):
        return f"{symbol}: neuer passiver Kern in rechter Variante; {state}; nur Diagnose."
    return f"{symbol}: Kernzustand verschoben; {state}; nur Diagnose."


def build_rows(left_rows: list[dict], right_rows: list[dict]) -> tuple[list[dict], list[dict]]:
    left = _index(left_rows)
    right = _index(right_rows)
    symbols = sorted(set(left) | set(right))
    rows: list[dict] = []
    for symbol in symbols:
        left_item = left.get(symbol)
        right_item = right.get(symbol)
        left_score = _safe_float((left_item or {}).get("right_semantic_maturity_score"))
        right_score = _safe_float((right_item or {}).get("right_semantic_maturity_score"))
        row = {
            "text_island_symbol": symbol,
            "core_stability_state": _state(left_item, right_item),
            "left_inner_core_state": (left_item or {}).get("inner_core_state", ""),
            "right_inner_core_state": (right_item or {}).get("inner_core_state", ""),
            "left_score": round(left_score, 9),
            "right_score": round(right_score, 9),
            "score_delta": round(right_score - left_score, 9),
            "left_right_inner_map_state": (left_item or {}).get("right_inner_map_state", ""),
            "right_right_inner_map_state": (right_item or {}).get("right_inner_map_state", ""),
            "left_families": (left_item or {}).get("right_families", ""),
            "right_families": (right_item or {}).get("right_families", ""),
            **PASSIVE_BOUNDARY,
        }
        row["stability_note"] = _note(row)
        rows.append(row)

    summary: dict[str, dict] = {}
    for row in rows:
        state = row["core_stability_state"]
        bucket = summary.setdefault(
            state,
            {
                "core_stability_state": state,
                "count": 0,
                "avg_score_delta": 0.0,
                **PASSIVE_BOUNDARY,
            },
        )
        count = int(bucket["count"])
        bucket["count"] = count + 1
        bucket["avg_score_delta"] = ((float(bucket["avg_score_delta"]) * count) + float(row["score_delta"])) / max(
            1, count + 1
        )
    summary_rows = []
    for item in summary.values():
        item["avg_score_delta"] = round(float(item["avg_score_delta"]), 9)
        summary_rows.append(item)
    return (
        sorted(rows, key=lambda row: (row["core_stability_state"], row["text_island_symbol"])),
        sorted(summary_rows, key=lambda row: (-int(row["count"]), row["core_stability_state"])),
    )


def write_outputs(rows: list[dict], summary: list[dict], output_dir: Path, left_path: Path, right_path: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(
        output_dir / "passive_inner_core_stability_lupe.csv",
        rows,
        [
            "text_island_symbol",
            "core_stability_state",
            "left_inner_core_state",
            "right_inner_core_state",
            "left_score",
            "right_score",
            "score_delta",
            "stability_note",
        ],
    )
    _write_csv(
        output_dir / "passive_inner_core_stability_lupe_summary.csv",
        summary,
        ["core_stability_state", "count", "avg_score_delta"],
    )
    (output_dir / "passive_inner_core_stability_lupe.json").write_text(
        json.dumps(
            {
                "left": str(left_path),
                "right": str(right_path),
                "rows": rows,
                "summary": summary,
                "boundary": PASSIVE_BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Passive Inner Core Stability Lupe",
        "",
        f"- left: `{left_path}`",
        f"- right: `{right_path}`",
        f"- compared_symbols: `{len(rows)}`",
        "",
        "## Grenze",
        "- passiv",
        "- keine Runtime-Lesung",
        "- keine Handlung",
        "- kein Gate",
        "- kein Entry",
        "- keine Richtung",
        "",
        "## Summary",
    ]
    for row in summary:
        lines.append(f"- {row['core_stability_state']}: {row['count']} delta={row['avg_score_delta']:.3f}")
    lines.extend(["", "## Lupe"])
    for row in rows[:120]:
        lines.append(f"- {row['stability_note']}")
    (output_dir / "passive_inner_core_stability_lupe.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (output_dir / "passive_inner_core_stability_lupe.txt").write_text(
        "\n".join(row["stability_note"] for row in rows) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare passive inner core lists")
    parser.add_argument("--left-core-list", type=Path, required=True)
    parser.add_argument("--right-core-list", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    rows, summary = build_rows(_read_csv(args.left_core_list), _read_csv(args.right_core_list))
    write_outputs(rows, summary, args.output_dir, args.left_core_list, args.right_core_list)
    print(
        json.dumps(
            {
                "compared_symbols": len(rows),
                "summary": {row["core_stability_state"]: row["count"] for row in summary},
                **PASSIVE_BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
