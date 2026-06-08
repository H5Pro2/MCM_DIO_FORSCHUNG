"""Compare passive inner-universe lupes on family level.

The report checks which dio_* families recur across two lupe transitions and
whether they appear as stable core, drift, soft variation or raw extension.
It is diagnostic only and does not feed Mini-DIO runtime.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
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


def _families(row: dict[str, str]) -> list[str]:
    return [item for item in str(row.get("families", "") or "").split("|") if item]


def _index_lupe(rows: list[dict[str, str]], label: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        category = str(row.get("lupe_category", "") or "unknown")
        text_symbol = str(row.get("text_island_symbol", "") or "")
        for family in _families(row):
            item = indexed.setdefault(
                family,
                {
                    "family": family,
                    f"{label}_count": 0,
                    f"{label}_categories": Counter(),
                    f"{label}_text_islands": set(),
                    f"{label}_score_sum": 0.0,
                    f"{label}_drift_sum": 0.0,
                },
            )
            item[f"{label}_count"] += 1
            item[f"{label}_categories"][category] += 1
            item[f"{label}_text_islands"].add(text_symbol)
            item[f"{label}_score_sum"] += _safe_float(row.get("semantic_maturity_score"))
            item[f"{label}_drift_sum"] += _safe_float(row.get("drift_pressure"))
    return indexed


def _dominant(counter: Counter[str]) -> str:
    if not counter:
        return "-"
    return counter.most_common(1)[0][0]


def _state(left_categories: Counter[str], right_categories: Counter[str], in_left: bool, in_right: bool) -> str:
    if in_left and not in_right:
        return "left_specific_family"
    if in_right and not in_left:
        return "right_specific_family"
    left_dom = _dominant(left_categories)
    right_dom = _dominant(right_categories)
    if left_dom == "stable_core" and right_dom == "stable_core":
        return "recurrent_stable_core_family"
    if left_dom == "drift_watch" or right_dom == "drift_watch":
        return "recurrent_drift_family"
    if left_dom != right_dom:
        return "recurrent_category_shift_family"
    if left_dom == "soft_variation_space":
        return "recurrent_variation_family"
    if left_dom == "carried_raw_space":
        return "recurrent_carried_raw_family"
    if left_dom == "new_raw_extension" or right_dom == "new_raw_extension":
        return "recurrent_raw_extension_family"
    return "recurrent_open_family"


def build_rows(left_label: str, left_rows: list[dict[str, str]], right_label: str, right_rows: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    left = _index_lupe(left_rows, "left")
    right = _index_lupe(right_rows, "right")
    families = sorted(set(left) | set(right))
    rows: list[dict[str, Any]] = []
    for family in families:
        left_item = left.get(family, {})
        right_item = right.get(family, {})
        left_categories = left_item.get("left_categories", Counter())
        right_categories = right_item.get("right_categories", Counter())
        left_count = int(left_item.get("left_count", 0) or 0)
        right_count = int(right_item.get("right_count", 0) or 0)
        in_left = left_count > 0
        in_right = right_count > 0
        left_text = sorted(left_item.get("left_text_islands", set()) or set())
        right_text = sorted(right_item.get("right_text_islands", set()) or set())
        state = _state(left_categories, right_categories, in_left, in_right)
        row = {
            "family": family,
            "cross_lupe_state": state,
            "left_label": left_label,
            "right_label": right_label,
            "appears_left": in_left,
            "appears_right": in_right,
            "left_count": left_count,
            "right_count": right_count,
            "left_dominant_category": _dominant(left_categories),
            "right_dominant_category": _dominant(right_categories),
            "left_categories": json.dumps(dict(sorted(left_categories.items())), sort_keys=True),
            "right_categories": json.dumps(dict(sorted(right_categories.items())), sort_keys=True),
            "left_avg_score": round(_safe_float(left_item.get("left_score_sum")) / max(1, left_count), 9),
            "right_avg_score": round(_safe_float(right_item.get("right_score_sum")) / max(1, right_count), 9),
            "score_delta_right_minus_left": round(
                (_safe_float(right_item.get("right_score_sum")) / max(1, right_count))
                - (_safe_float(left_item.get("left_score_sum")) / max(1, left_count)),
                9,
            ),
            "left_avg_drift": round(_safe_float(left_item.get("left_drift_sum")) / max(1, left_count), 9),
            "right_avg_drift": round(_safe_float(right_item.get("right_drift_sum")) / max(1, right_count), 9),
            "left_text_islands": "|".join(left_text[:20]),
            "right_text_islands": "|".join(right_text[:20]),
            **PASSIVE_FLAGS,
        }
        rows.append(row)

    rows.sort(
        key=lambda item: (
            str(item["cross_lupe_state"]),
            -int(item["left_count"]) - int(item["right_count"]),
            str(item["family"]),
        )
    )
    summary_map: dict[str, dict[str, Any]] = {}
    for row in rows:
        state = str(row["cross_lupe_state"])
        bucket = summary_map.setdefault(
            state,
            {
                "cross_lupe_state": state,
                "family_count": 0,
                "avg_left_count": 0.0,
                "avg_right_count": 0.0,
                "avg_score_delta_right_minus_left": 0.0,
                "top_families": [],
                **PASSIVE_FLAGS,
            },
        )
        bucket["family_count"] += 1
        bucket["_sum_left_count"] = bucket.get("_sum_left_count", 0.0) + _safe_float(row["left_count"])
        bucket["_sum_right_count"] = bucket.get("_sum_right_count", 0.0) + _safe_float(row["right_count"])
        bucket["_sum_score_delta"] = bucket.get("_sum_score_delta", 0.0) + _safe_float(row["score_delta_right_minus_left"])
        bucket["top_families"].append(str(row["family"]))
    summary_rows = []
    for bucket in summary_map.values():
        count = max(1, int(bucket["family_count"]))
        bucket["avg_left_count"] = round(bucket.pop("_sum_left_count", 0.0) / count, 9)
        bucket["avg_right_count"] = round(bucket.pop("_sum_right_count", 0.0) / count, 9)
        bucket["avg_score_delta_right_minus_left"] = round(bucket.pop("_sum_score_delta", 0.0) / count, 9)
        bucket["top_families"] = "|".join(bucket["top_families"][:20])
        summary_rows.append(bucket)
    summary_rows.sort(key=lambda item: (-int(item["family_count"]), str(item["cross_lupe_state"])))
    return rows, summary_rows


def _write_markdown(output_dir: Path, rows: list[dict[str, Any]], summary_rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Passive Inner-Universe Cross-Lupe",
        "",
        "Dieser Bericht vergleicht konkrete dio_* Familien ueber zwei Lupe-Uebergaenge.",
        "Er bleibt passiv und steuert Mini-DIO nicht.",
        "",
        "## Zusammenfassung",
    ]
    for item in summary_rows:
        lines.append(
            "- {state}: families={count}, avg_score_delta={delta}".format(
                state=item["cross_lupe_state"],
                count=item["family_count"],
                delta=item["avg_score_delta_right_minus_left"],
            )
        )
    lines.append("")
    lines.append("## Top-Familien je Zustand")
    for item in summary_rows:
        state = str(item["cross_lupe_state"])
        lines.append("")
        lines.append(f"### {state}")
        selected = [row for row in rows if row["cross_lupe_state"] == state][:12]
        for row in selected:
            lines.append(
                "- {family}: {left}->{right}, delta={delta}, left_text={lt}, right_text={rt}".format(
                    family=row["family"],
                    left=row["left_dominant_category"],
                    right=row["right_dominant_category"],
                    delta=row["score_delta_right_minus_left"],
                    lt=row["left_text_islands"],
                    rt=row["right_text_islands"],
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
    (output_dir / "passive_inner_universe_cross_lupe.md").write_text(text, encoding="utf-8")
    (output_dir / "passive_inner_universe_cross_lupe.txt").write_text(text, encoding="utf-8")


def run(left_label: str, left_path: Path, right_label: str, right_path: Path, output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows, summary_rows = build_rows(left_label, _read_csv(left_path), right_label, _read_csv(right_path))
    row_fields = [
        "family",
        "cross_lupe_state",
        "left_label",
        "right_label",
        "appears_left",
        "appears_right",
        "left_count",
        "right_count",
        "left_dominant_category",
        "right_dominant_category",
        "left_categories",
        "right_categories",
        "left_avg_score",
        "right_avg_score",
        "score_delta_right_minus_left",
        "left_avg_drift",
        "right_avg_drift",
        "left_text_islands",
        "right_text_islands",
        *PASSIVE_FLAGS.keys(),
    ]
    summary_fields = [
        "cross_lupe_state",
        "family_count",
        "avg_left_count",
        "avg_right_count",
        "avg_score_delta_right_minus_left",
        "top_families",
        *PASSIVE_FLAGS.keys(),
    ]
    _write_csv(output_dir / "passive_inner_universe_cross_lupe.csv", rows, row_fields)
    _write_csv(output_dir / "passive_inner_universe_cross_lupe_summary.csv", summary_rows, summary_fields)
    payload = {
        "schema": "dio_mini_passive_inner_universe_cross_lupe.v1",
        "left_label": left_label,
        "right_label": right_label,
        "left_path": str(left_path),
        "right_path": str(right_path),
        "family_count": len(rows),
        "summary": summary_rows,
        "rows": rows,
        **PASSIVE_FLAGS,
    }
    (output_dir / "passive_inner_universe_cross_lupe.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    _write_markdown(output_dir, rows, summary_rows)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare passive Mini-DIO inner-universe lupes")
    parser.add_argument("--left-label", required=True)
    parser.add_argument("--left-lupe", required=True)
    parser.add_argument("--right-label", required=True)
    parser.add_argument("--right-lupe", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = run(
        args.left_label,
        Path(args.left_lupe),
        args.right_label,
        Path(args.right_lupe),
        Path(args.output_dir),
    )
    print(f"inner_universe_cross_lupe families={result['family_count']} output={args.output_dir}")


if __name__ == "__main__":
    main()
