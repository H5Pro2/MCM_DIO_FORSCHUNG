"""Report passive Mini-DIO syntax that survives while maturity shifts.

This diagnostic compares two passive text-island inner maps. It focuses on the
case where the same syntax or the same family remains visible, but the inner
map maturity falls from stable/bearing into raw, softened, drift, or foreign
space.

The report is passive only. It is not read by Mini-DIO and does not influence
action, gates, entries, direction, or runtime memory.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


PASSIVE_FLAGS = {
    "passive_only": True,
    "writes_runtime_memory": False,
    "read_by_mini_dio": False,
    "influences_action": False,
    "is_gate": False,
    "is_motoric": False,
    "is_entry_signal": False,
    "is_direction_signal": False,
}


STATE_RANK = {
    "inner_unconfirmed_raw_space": 0,
    "inner_drift_watch_space": 1,
    "inner_foreign_boundary_space": 1,
    "inner_soft_variation_space": 2,
    "inner_stable_recurrence_space": 3,
    "inner_variation_bearing_space": 4,
}


STRONG_STATES = {"inner_stable_recurrence_space", "inner_variation_bearing_space"}
WEAK_STATES = {
    "inner_unconfirmed_raw_space",
    "inner_drift_watch_space",
    "inner_foreign_boundary_space",
    "inner_soft_variation_space",
}


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        result = float(value if value not in (None, "") else default)
    except (TypeError, ValueError):
        return default
    if result != result:
        return default
    return result


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = list(fieldnames)
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=ordered)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in ordered})


def _families(row: dict[str, str]) -> set[str]:
    return {item.strip() for item in str(row.get("families", "") or "").split("|") if item.strip()}


def _index_by_text_island(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {str(row.get("text_island_symbol", "") or ""): row for row in rows if row.get("text_island_symbol")}


def _index_by_family(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    index: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        for family in _families(row):
            index[family].append(row)
    return dict(index)


def _best_family_row(rows: list[dict[str, str]]) -> dict[str, str]:
    return max(rows, key=lambda row: _safe_float(row.get("semantic_maturity_score")), default={})


def _shift_state(left_state: str, right_state: str, score_delta: float) -> str:
    left_rank = STATE_RANK.get(left_state, 0)
    right_rank = STATE_RANK.get(right_state, 0)
    if left_state in STRONG_STATES and right_state in WEAK_STATES:
        return "syntax_survives_reife_kippt"
    if right_state == "inner_unconfirmed_raw_space" and left_state:
        return "syntax_survives_raw"
    if right_rank < left_rank or score_delta < -0.08:
        return "syntax_survives_softened"
    if right_rank == left_rank and left_state == right_state:
        return "syntax_survives_same_reife"
    if right_rank > left_rank or score_delta > 0.08:
        return "syntax_survives_reife_steigt"
    return "syntax_survives_reorganized"


def _make_shift_row(
    *,
    anchor_type: str,
    anchor_symbol: str,
    left_label: str,
    right_label: str,
    left_row: dict[str, str],
    right_row: dict[str, str],
) -> dict[str, Any]:
    left_state = str(left_row.get("inner_map_state", "") or "")
    right_state = str(right_row.get("inner_map_state", "") or "")
    left_score = _safe_float(left_row.get("semantic_maturity_score"))
    right_score = _safe_float(right_row.get("semantic_maturity_score"))
    score_delta = right_score - left_score
    left_families = _families(left_row)
    right_families = _families(right_row)
    shared_families = sorted(left_families & right_families)
    return {
        "shift_state": _shift_state(left_state, right_state, score_delta),
        "anchor_type": anchor_type,
        "anchor_symbol": anchor_symbol,
        "left_label": left_label,
        "right_label": right_label,
        "left_text_island_symbol": str(left_row.get("text_island_symbol", "") or ""),
        "right_text_island_symbol": str(right_row.get("text_island_symbol", "") or ""),
        "same_text_island": str(left_row.get("text_island_symbol", "") or "")
        == str(right_row.get("text_island_symbol", "") or ""),
        "left_inner_map_state": left_state,
        "right_inner_map_state": right_state,
        "left_semantic_maturity_score": round(left_score, 9),
        "right_semantic_maturity_score": round(right_score, 9),
        "score_delta": round(score_delta, 9),
        "left_stability_pressure": round(_safe_float(left_row.get("stability_pressure")), 9),
        "right_stability_pressure": round(_safe_float(right_row.get("stability_pressure")), 9),
        "left_variation_bearing": round(_safe_float(left_row.get("variation_bearing")), 9),
        "right_variation_bearing": round(_safe_float(right_row.get("variation_bearing")), 9),
        "left_rawness": round(_safe_float(left_row.get("rawness")), 9),
        "right_rawness": round(_safe_float(right_row.get("rawness")), 9),
        "left_families": "|".join(sorted(left_families)),
        "right_families": "|".join(sorted(right_families)),
        "shared_families": "|".join(shared_families),
        "shared_family_count": len(shared_families),
        **PASSIVE_FLAGS,
    }


def build_shift_rows(
    *,
    left_label: str,
    left_rows: list[dict[str, str]],
    right_label: str,
    right_rows: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    left_by_text = _index_by_text_island(left_rows)
    right_by_text = _index_by_text_island(right_rows)
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    for symbol in sorted(set(left_by_text) & set(right_by_text)):
        row = _make_shift_row(
            anchor_type="text_island",
            anchor_symbol=symbol,
            left_label=left_label,
            right_label=right_label,
            left_row=left_by_text[symbol],
            right_row=right_by_text[symbol],
        )
        rows.append(row)
        seen.add((str(row["left_text_island_symbol"]), str(row["right_text_island_symbol"])))

    left_by_family = _index_by_family(left_rows)
    right_by_family = _index_by_family(right_rows)
    for family in sorted(set(left_by_family) & set(right_by_family)):
        left_row = _best_family_row(left_by_family[family])
        right_row = _best_family_row(right_by_family[family])
        key = (str(left_row.get("text_island_symbol", "")), str(right_row.get("text_island_symbol", "")))
        if key in seen:
            continue
        rows.append(
            _make_shift_row(
                anchor_type="family",
                anchor_symbol=family,
                left_label=left_label,
                right_label=right_label,
                left_row=left_row,
                right_row=right_row,
            )
        )
        seen.add(key)

    summary_map: dict[str, dict[str, Any]] = {}
    for row in rows:
        state = str(row["shift_state"])
        bucket = summary_map.setdefault(
            state,
            {
                "shift_state": state,
                "count": 0,
                "text_island_anchors": 0,
                "family_anchors": 0,
                "avg_score_delta": 0.0,
                "avg_rawness_delta": 0.0,
                **PASSIVE_FLAGS,
            },
        )
        count = int(bucket["count"])
        bucket["count"] = count + 1
        if row["anchor_type"] == "text_island":
            bucket["text_island_anchors"] += 1
        else:
            bucket["family_anchors"] += 1
        bucket["avg_score_delta"] = (
            (float(bucket["avg_score_delta"]) * count) + float(row["score_delta"])
        ) / max(1, count + 1)
        rawness_delta = float(row["right_rawness"]) - float(row["left_rawness"])
        bucket["avg_rawness_delta"] = (
            (float(bucket["avg_rawness_delta"]) * count) + rawness_delta
        ) / max(1, count + 1)

    summary_rows = []
    for row in summary_map.values():
        row["avg_score_delta"] = round(float(row["avg_score_delta"]), 9)
        row["avg_rawness_delta"] = round(float(row["avg_rawness_delta"]), 9)
        summary_rows.append(row)

    rows.sort(
        key=lambda row: (
            str(row["shift_state"]),
            str(row["anchor_type"]),
            str(row["anchor_symbol"]),
        )
    )
    summary_rows.sort(key=lambda row: (-int(row["count"]), str(row["shift_state"])))
    return rows, summary_rows


def _write_markdown(
    output_dir: Path,
    *,
    left: Path,
    right: Path,
    rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# Passive Syntax-Maturity Shift",
        "",
        "Dieser Bericht prüft, ob Syntax/Familien sichtbar bleiben, während die innere Reife kippt.",
        "",
        f"- left: `{left}`",
        f"- right: `{right}`",
        f"- compared_anchors: `{len(rows)}`",
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
            "- {state}: count={count}, text_island={text}, family={family}, "
            "avg_score_delta={score}, avg_rawness_delta={raw}".format(
                state=row["shift_state"],
                count=row["count"],
                text=row["text_island_anchors"],
                family=row["family_anchors"],
                score=row["avg_score_delta"],
                raw=row["avg_rawness_delta"],
            )
        )

    selected = [
        row
        for row in rows
        if row["shift_state"]
        in {"syntax_survives_reife_kippt", "syntax_survives_raw", "syntax_survives_softened"}
    ][:60]
    lines.extend(["", "## Reife kippt", ""])
    for row in selected:
        lines.append(
            "- {anchor_type}:{anchor_symbol} | {left_text} -> {right_text} | "
            "{left_state} -> {right_state} | score_delta={score_delta} | shared={shared}".format(
                anchor_type=row["anchor_type"],
                anchor_symbol=row["anchor_symbol"],
                left_text=row["left_text_island_symbol"],
                right_text=row["right_text_island_symbol"],
                left_state=row["left_inner_map_state"],
                right_state=row["right_inner_map_state"],
                score_delta=row["score_delta"],
                shared=row["shared_families"] or "-",
            )
        )
    (output_dir / "passive_syntax_maturity_shift.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs(
    *,
    output_dir: Path,
    left: Path,
    right: Path,
    rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(
        output_dir / "passive_syntax_maturity_shift.csv",
        rows,
        [
            "shift_state",
            "anchor_type",
            "anchor_symbol",
            "left_label",
            "right_label",
            "left_text_island_symbol",
            "right_text_island_symbol",
            "same_text_island",
            "left_inner_map_state",
            "right_inner_map_state",
            "left_semantic_maturity_score",
            "right_semantic_maturity_score",
            "score_delta",
            "left_rawness",
            "right_rawness",
            "shared_families",
            "shared_family_count",
        ],
    )
    _write_csv(
        output_dir / "passive_syntax_maturity_shift_summary.csv",
        summary_rows,
        [
            "shift_state",
            "count",
            "text_island_anchors",
            "family_anchors",
            "avg_score_delta",
            "avg_rawness_delta",
        ],
    )
    payload = {
        "left": str(left),
        "right": str(right),
        "rows": rows,
        "summary": summary_rows,
        "boundary": PASSIVE_FLAGS,
    }
    (output_dir / "passive_syntax_maturity_shift.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    _write_markdown(output_dir, left=left, right=right, rows=rows, summary_rows=summary_rows)
    (output_dir / "passive_syntax_maturity_shift.txt").write_text(
        "\n".join(
            f"{row['shift_state']}: {row['anchor_type']}:{row['anchor_symbol']} "
            f"{row['left_inner_map_state']}->{row['right_inner_map_state']}"
            for row in rows
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive syntax maturity shifts")
    parser.add_argument("--left", type=Path, required=True)
    parser.add_argument("--right", type=Path, required=True)
    parser.add_argument("--left-label", default="LEFT")
    parser.add_argument("--right-label", default="RIGHT")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    rows, summary_rows = build_shift_rows(
        left_label=args.left_label,
        left_rows=_read_csv(args.left),
        right_label=args.right_label,
        right_rows=_read_csv(args.right),
    )
    write_outputs(output_dir=args.output_dir, left=args.left, right=args.right, rows=rows, summary_rows=summary_rows)
    print(
        json.dumps(
            {
                "left": str(args.left),
                "right": str(args.right),
                "compared_anchors": len(rows),
                "summary": {row["shift_state"]: row["count"] for row in summary_rows},
                **PASSIVE_FLAGS,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
