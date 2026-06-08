"""Classify stable passive inner-universe core families.

This report reads a passive inner-universe cross-lupe and separates exact
single-family anchors from deeper recurring anchors and variant bridges.
It remains diagnostic only.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
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


def _safe_int(value: Any) -> int:
    try:
        return int(float(value or 0))
    except (TypeError, ValueError):
        return 0


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


def _split_symbols(value: str) -> list[str]:
    return [item for item in str(value or "").split("|") if item]


def _anchor_state(row: dict[str, str]) -> str:
    state = str(row.get("cross_lupe_state", "") or "")
    left_text = _split_symbols(str(row.get("left_text_islands", "") or ""))
    right_text = _split_symbols(str(row.get("right_text_islands", "") or ""))
    left_count = _safe_int(row.get("left_count"))
    right_count = _safe_int(row.get("right_count"))
    delta = abs(_safe_float(row.get("score_delta_right_minus_left")))
    same_text = bool(left_text and right_text and set(left_text) == set(right_text))

    if state == "recurrent_stable_core_family":
        if same_text and left_count == 1 and right_count == 1 and delta < 0.01:
            return "exact_single_form_anchor"
        if same_text and delta < 0.03:
            return "exact_multi_form_anchor"
        return "stable_core_reorganized_anchor"
    if state == "recurrent_variation_family":
        if set(left_text) != set(right_text):
            return "variant_bridge_anchor"
        return "same_text_variation_anchor"
    if state == "recurrent_drift_family":
        return "drift_sensitive_anchor"
    if state == "recurrent_category_shift_family":
        return "category_shift_anchor"
    return "outside_anchor_scope"


def build_rows(rows: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    selected_states = {
        "recurrent_stable_core_family",
        "recurrent_variation_family",
        "recurrent_drift_family",
        "recurrent_category_shift_family",
    }
    output: list[dict[str, Any]] = []
    for row in rows:
        if str(row.get("cross_lupe_state", "") or "") not in selected_states:
            continue
        anchor_state = _anchor_state(row)
        left_text = _split_symbols(str(row.get("left_text_islands", "") or ""))
        right_text = _split_symbols(str(row.get("right_text_islands", "") or ""))
        output.append(
            {
                "family": str(row.get("family", "") or ""),
                "anchor_lupe_state": anchor_state,
                "cross_lupe_state": str(row.get("cross_lupe_state", "") or ""),
                "left_dominant_category": str(row.get("left_dominant_category", "") or ""),
                "right_dominant_category": str(row.get("right_dominant_category", "") or ""),
                "left_count": _safe_int(row.get("left_count")),
                "right_count": _safe_int(row.get("right_count")),
                "left_avg_score": round(_safe_float(row.get("left_avg_score")), 9),
                "right_avg_score": round(_safe_float(row.get("right_avg_score")), 9),
                "score_delta_right_minus_left": round(_safe_float(row.get("score_delta_right_minus_left")), 9),
                "same_text_island": bool(left_text and right_text and set(left_text) == set(right_text)),
                "left_text_islands": "|".join(left_text),
                "right_text_islands": "|".join(right_text),
                **PASSIVE_FLAGS,
            }
        )

    counts = Counter(str(row["anchor_lupe_state"]) for row in output)
    summary: list[dict[str, Any]] = []
    for state, count in sorted(counts.items()):
        state_rows = [row for row in output if row["anchor_lupe_state"] == state]
        summary.append(
            {
                "anchor_lupe_state": state,
                "count": count,
                "avg_left_score": round(
                    sum(_safe_float(row["left_avg_score"]) for row in state_rows) / max(1, count),
                    9,
                ),
                "avg_right_score": round(
                    sum(_safe_float(row["right_avg_score"]) for row in state_rows) / max(1, count),
                    9,
                ),
                "avg_score_delta_right_minus_left": round(
                    sum(_safe_float(row["score_delta_right_minus_left"]) for row in state_rows)
                    / max(1, count),
                    9,
                ),
                "same_text_count": sum(1 for row in state_rows if row["same_text_island"]),
                "top_families": "|".join(str(row["family"]) for row in state_rows[:20]),
                **PASSIVE_FLAGS,
            }
        )

    output.sort(
        key=lambda item: (
            str(item["anchor_lupe_state"]),
            -_safe_float(item["right_avg_score"]),
            str(item["family"]),
        )
    )
    summary.sort(key=lambda item: (-int(item["count"]), str(item["anchor_lupe_state"])))
    return output, summary


def _write_markdown(output_dir: Path, rows: list[dict[str, Any]], summary: list[dict[str, Any]]) -> None:
    lines = [
        "# Passive Inner-Core Anchor Lupe",
        "",
        "Dieser Bericht prueft, ob stabile Familien tiefe Anker oder nur stabile Einzelformen sind.",
        "",
        "## Zusammenfassung",
    ]
    for item in summary:
        lines.append(
            "- {state}: count={count}, same_text={same}, avg_delta={delta}".format(
                state=item["anchor_lupe_state"],
                count=item["count"],
                same=item["same_text_count"],
                delta=item["avg_score_delta_right_minus_left"],
            )
        )
    lines.append("")
    lines.append("## Familien")
    for item in summary:
        state = str(item["anchor_lupe_state"])
        lines.append("")
        lines.append(f"### {state}")
        for row in [row for row in rows if row["anchor_lupe_state"] == state][:20]:
            lines.append(
                "- {family}: {left}->{right}, same_text={same}, delta={delta}, text={text}".format(
                    family=row["family"],
                    left=row["left_dominant_category"],
                    right=row["right_dominant_category"],
                    same=row["same_text_island"],
                    delta=row["score_delta_right_minus_left"],
                    text=row["right_text_islands"],
                )
            )
    lines.append("")
    lines.append("## Lesart")
    lines.append(
        "Exact single-form anchors sind stabil und realitaetsgebunden, aber noch flach. "
        "Tiefe Anker wuerden mehrere Textinseln, Varianten oder Reorganisationsfaehigkeit tragen."
    )
    lines.append("")
    lines.append("## Wirkungsgrenze")
    lines.append("- keine Runtime-Lesung")
    lines.append("- keine Handlung")
    lines.append("- kein Gate")
    lines.append("- kein Entry-Signal")
    lines.append("- kein Richtungssignal")
    text = "\n".join(lines)
    (output_dir / "passive_inner_core_anchor_lupe.md").write_text(text, encoding="utf-8")
    (output_dir / "passive_inner_core_anchor_lupe.txt").write_text(text, encoding="utf-8")


def run(cross_lupe_path: Path, output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows, summary = build_rows(_read_csv(cross_lupe_path))
    row_fields = [
        "family",
        "anchor_lupe_state",
        "cross_lupe_state",
        "left_dominant_category",
        "right_dominant_category",
        "left_count",
        "right_count",
        "left_avg_score",
        "right_avg_score",
        "score_delta_right_minus_left",
        "same_text_island",
        "left_text_islands",
        "right_text_islands",
        *PASSIVE_FLAGS.keys(),
    ]
    summary_fields = [
        "anchor_lupe_state",
        "count",
        "avg_left_score",
        "avg_right_score",
        "avg_score_delta_right_minus_left",
        "same_text_count",
        "top_families",
        *PASSIVE_FLAGS.keys(),
    ]
    _write_csv(output_dir / "passive_inner_core_anchor_lupe.csv", rows, row_fields)
    _write_csv(output_dir / "passive_inner_core_anchor_lupe_summary.csv", summary, summary_fields)
    payload = {
        "schema": "dio_mini_passive_inner_core_anchor_lupe.v1",
        "cross_lupe_path": str(cross_lupe_path),
        "row_count": len(rows),
        "summary": summary,
        "rows": rows,
        **PASSIVE_FLAGS,
    }
    (output_dir / "passive_inner_core_anchor_lupe.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    _write_markdown(output_dir, rows, summary)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify passive Mini-DIO inner-core anchors")
    parser.add_argument("--cross-lupe", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = run(Path(args.cross_lupe), Path(args.output_dir))
    print(f"inner_core_anchor_lupe rows={result['row_count']} output={args.output_dir}")


if __name__ == "__main__":
    main()
