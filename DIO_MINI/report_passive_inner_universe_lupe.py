"""Inspect concrete passive Mini-DIO inner-universe text islands.

This diagnostic report compares two text-island inner maps and lists the
specific islands that form stable core, variation space, drift watch, raw
extension and carried raw space.
"""

from __future__ import annotations

import argparse
import csv
import json
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


def _safe_float(value: Any) -> float:
    try:
        return float(value or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def _index(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        symbol = str(row.get("text_island_symbol", "") or "").strip()
        if symbol:
            result[symbol] = row
    return result


def _family_count(row: dict[str, str]) -> int:
    families = [item for item in str(row.get("families", "") or "").split("|") if item]
    return len(families)


def _category(symbol: str, left: dict[str, dict[str, str]], right_row: dict[str, str]) -> str:
    right_state = str(right_row.get("inner_map_state", "") or "unknown")
    right_maturity = str(right_row.get("text_island_maturity_state", "") or "unknown")
    if symbol not in left:
        if right_state == "inner_stable_recurrence_space":
            return "new_but_stable_core_candidate"
        if right_state == "inner_soft_variation_space":
            return "new_soft_variation_space"
        if right_state == "inner_drift_watch_space":
            return "new_drift_watch_space"
        return "new_raw_extension"
    if right_state == "inner_stable_recurrence_space":
        return "stable_core"
    if right_state == "inner_soft_variation_space":
        return "soft_variation_space"
    if right_state == "inner_drift_watch_space":
        return "drift_watch"
    if right_maturity == "stable_recurrent_text_island":
        return "matured_recurrence_without_core_state"
    return "carried_raw_space"


def _make_row(
    transition: str,
    symbol: str,
    category: str,
    left_row: dict[str, str] | None,
    right_row: dict[str, str],
) -> dict[str, Any]:
    left_score = _safe_float((left_row or {}).get("semantic_maturity_score"))
    right_score = _safe_float(right_row.get("semantic_maturity_score"))
    return {
        "transition": transition,
        "text_island_symbol": symbol,
        "lupe_category": category,
        "was_present_before": bool(left_row),
        "left_inner_map_state": str((left_row or {}).get("inner_map_state", "") or "-"),
        "right_inner_map_state": str(right_row.get("inner_map_state", "") or "-"),
        "left_maturity_state": str((left_row or {}).get("text_island_maturity_state", "") or "-"),
        "right_maturity_state": str(right_row.get("text_island_maturity_state", "") or "-"),
        "semantic_maturity_score": round(right_score, 9),
        "semantic_maturity_delta": round(right_score - left_score, 9),
        "stability_pressure": round(_safe_float(right_row.get("stability_pressure")), 9),
        "variation_bearing": round(_safe_float(right_row.get("variation_bearing")), 9),
        "drift_pressure": round(_safe_float(right_row.get("drift_pressure")), 9),
        "family_count": _family_count(right_row),
        "families": str(right_row.get("families", "") or ""),
        "inner_map_note": str(right_row.get("inner_map_note", "") or ""),
        **PASSIVE_FLAGS,
    }


def build_rows(
    *,
    left_label: str,
    left_rows: list[dict[str, str]],
    right_label: str,
    right_rows: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    left = _index(left_rows)
    right = _index(right_rows)
    transition = f"{left_label}->{right_label}"
    rows: list[dict[str, Any]] = []
    for symbol in sorted(right):
        right_row = right[symbol]
        category = _category(symbol, left, right_row)
        rows.append(_make_row(transition, symbol, category, left.get(symbol), right_row))

    summary_map: dict[str, dict[str, Any]] = {}
    for row in rows:
        category = str(row["lupe_category"])
        bucket = summary_map.setdefault(
            category,
            {
                "transition": transition,
                "lupe_category": category,
                "count": 0,
                "avg_semantic_maturity_score": 0.0,
                "avg_semantic_maturity_delta": 0.0,
                "avg_stability_pressure": 0.0,
                "avg_variation_bearing": 0.0,
                "avg_drift_pressure": 0.0,
                "avg_family_count": 0.0,
                "top_symbols": [],
                **PASSIVE_FLAGS,
            },
        )
        bucket["count"] += 1
        for key in (
            "semantic_maturity_score",
            "semantic_maturity_delta",
            "stability_pressure",
            "variation_bearing",
            "drift_pressure",
            "family_count",
        ):
            bucket[f"_sum_{key}"] = bucket.get(f"_sum_{key}", 0.0) + _safe_float(row.get(key))
        bucket["top_symbols"].append(str(row.get("text_island_symbol", "")))

    summary_rows: list[dict[str, Any]] = []
    for bucket in summary_map.values():
        count = max(1, int(bucket["count"]))
        bucket["avg_semantic_maturity_score"] = round(bucket.pop("_sum_semantic_maturity_score", 0.0) / count, 9)
        bucket["avg_semantic_maturity_delta"] = round(bucket.pop("_sum_semantic_maturity_delta", 0.0) / count, 9)
        bucket["avg_stability_pressure"] = round(bucket.pop("_sum_stability_pressure", 0.0) / count, 9)
        bucket["avg_variation_bearing"] = round(bucket.pop("_sum_variation_bearing", 0.0) / count, 9)
        bucket["avg_drift_pressure"] = round(bucket.pop("_sum_drift_pressure", 0.0) / count, 9)
        bucket["avg_family_count"] = round(bucket.pop("_sum_family_count", 0.0) / count, 9)
        bucket["top_symbols"] = "|".join(bucket["top_symbols"][:12])
        summary_rows.append(bucket)

    summary_rows.sort(key=lambda item: (-int(item["count"]), str(item["lupe_category"])))
    rows.sort(
        key=lambda item: (
            str(item["lupe_category"]),
            -_safe_float(item["semantic_maturity_score"]),
            str(item["text_island_symbol"]),
        )
    )
    return rows, summary_rows


def _write_markdown(output_dir: Path, rows: list[dict[str, Any]], summary_rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Passive Inner-Universe Lupe",
        "",
        "Dieser Bericht ist passiv. Er benennt konkrete Textinseln, ohne Mini-DIO zu steuern.",
        "",
        "## Kategorien",
    ]
    for item in summary_rows:
        lines.append(
            "- {category}: count={count}, avg_score={score}, avg_delta={delta}, "
            "avg_drift={drift}".format(
                category=item["lupe_category"],
                count=item["count"],
                score=item["avg_semantic_maturity_score"],
                delta=item["avg_semantic_maturity_delta"],
                drift=item["avg_drift_pressure"],
            )
        )
    lines.append("")
    lines.append("## Top-Inseln je Kategorie")
    for item in summary_rows:
        category = str(item["lupe_category"])
        lines.append("")
        lines.append(f"### {category}")
        selected = [row for row in rows if row["lupe_category"] == category][:8]
        for row in selected:
            lines.append(
                "- {symbol}: score={score}, delta={delta}, families={families}".format(
                    symbol=row["text_island_symbol"],
                    score=row["semantic_maturity_score"],
                    delta=row["semantic_maturity_delta"],
                    families=row["families"],
                )
            )
    lines.append("")
    lines.append("## Wirkungsgrenze")
    lines.append("- keine Runtime-Lesung")
    lines.append("- keine Handlung")
    lines.append("- kein Gate")
    lines.append("- kein Entry-Signal")
    lines.append("- kein Richtungssignal")
    text = "\n".join(lines)
    (output_dir / "passive_inner_universe_lupe.md").write_text(text, encoding="utf-8")
    (output_dir / "passive_inner_universe_lupe.txt").write_text(text, encoding="utf-8")


def run(left_label: str, left_path: Path, right_label: str, right_path: Path, output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows, summary_rows = build_rows(
        left_label=left_label,
        left_rows=_read_csv(left_path),
        right_label=right_label,
        right_rows=_read_csv(right_path),
    )
    row_fields = [
        "transition",
        "text_island_symbol",
        "lupe_category",
        "was_present_before",
        "left_inner_map_state",
        "right_inner_map_state",
        "left_maturity_state",
        "right_maturity_state",
        "semantic_maturity_score",
        "semantic_maturity_delta",
        "stability_pressure",
        "variation_bearing",
        "drift_pressure",
        "family_count",
        "families",
        "inner_map_note",
        *PASSIVE_FLAGS.keys(),
    ]
    summary_fields = [
        "transition",
        "lupe_category",
        "count",
        "avg_semantic_maturity_score",
        "avg_semantic_maturity_delta",
        "avg_stability_pressure",
        "avg_variation_bearing",
        "avg_drift_pressure",
        "avg_family_count",
        "top_symbols",
        *PASSIVE_FLAGS.keys(),
    ]
    _write_csv(output_dir / "passive_inner_universe_lupe.csv", rows, row_fields)
    _write_csv(output_dir / "passive_inner_universe_lupe_summary.csv", summary_rows, summary_fields)
    payload = {
        "schema": "dio_mini_passive_inner_universe_lupe.v1",
        "left_label": left_label,
        "right_label": right_label,
        "left_path": str(left_path),
        "right_path": str(right_path),
        "row_count": len(rows),
        "summary": summary_rows,
        "rows": rows,
        **PASSIVE_FLAGS,
    }
    (output_dir / "passive_inner_universe_lupe.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    _write_markdown(output_dir, rows, summary_rows)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect passive Mini-DIO inner-universe text islands")
    parser.add_argument("--left-label", required=True)
    parser.add_argument("--left-map", required=True)
    parser.add_argument("--right-label", required=True)
    parser.add_argument("--right-map", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = run(
        args.left_label,
        Path(args.left_map),
        args.right_label,
        Path(args.right_map),
        Path(args.output_dir),
    )
    print(f"inner_universe_lupe rows={result['row_count']} output={args.output_dir}")


if __name__ == "__main__":
    main()
