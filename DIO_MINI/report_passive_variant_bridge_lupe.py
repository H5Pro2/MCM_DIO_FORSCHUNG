"""Inspect passive variant bridge anchors.

Variant bridge anchors are families that remain in soft variation space across
two worlds while the text island changes. This report groups those bridges by
their text-island transition.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
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


def _bridge_state(delta: float, family_count: int) -> str:
    if family_count >= 3 and abs(delta) <= 0.07:
        return "shared_variant_bridge"
    if family_count >= 2 and delta > 0.04:
        return "strengthening_variant_bridge"
    if family_count >= 2 and delta < -0.04:
        return "softening_variant_bridge"
    if family_count >= 2:
        return "thin_variant_bridge"
    if delta > 0.04:
        return "single_strengthening_bridge"
    if delta < -0.04:
        return "single_softening_bridge"
    return "single_open_bridge"


def build_rows(rows: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    bridge_rows = [
        row for row in rows if str(row.get("anchor_lupe_state", "") or "") == "variant_bridge_anchor"
    ]
    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in bridge_rows:
        left_text = str(row.get("left_text_islands", "") or "")
        right_text = str(row.get("right_text_islands", "") or "")
        groups[(left_text, right_text)].append(row)

    detail_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    for (left_text, right_text), items in sorted(groups.items()):
        deltas = [_safe_float(item.get("score_delta_right_minus_left")) for item in items]
        avg_delta = round(mean(deltas) if deltas else 0.0, 9)
        state = _bridge_state(avg_delta, len(items))
        families = [str(item.get("family", "") or "") for item in items]
        summary_rows.append(
            {
                "variant_bridge_state": state,
                "left_text_island": left_text,
                "right_text_island": right_text,
                "family_count": len(items),
                "families": "|".join(families),
                "avg_left_score": round(
                    mean(_safe_float(item.get("left_avg_score")) for item in items), 9
                ),
                "avg_right_score": round(
                    mean(_safe_float(item.get("right_avg_score")) for item in items), 9
                ),
                "avg_score_delta_right_minus_left": avg_delta,
                **PASSIVE_FLAGS,
            }
        )
        for item in items:
            detail_rows.append(
                {
                    "variant_bridge_state": state,
                    "family": str(item.get("family", "") or ""),
                    "left_text_island": left_text,
                    "right_text_island": right_text,
                    "left_avg_score": round(_safe_float(item.get("left_avg_score")), 9),
                    "right_avg_score": round(_safe_float(item.get("right_avg_score")), 9),
                    "score_delta_right_minus_left": round(
                        _safe_float(item.get("score_delta_right_minus_left")), 9
                    ),
                    **PASSIVE_FLAGS,
                }
            )

    summary_rows.sort(key=lambda item: (-int(item["family_count"]), str(item["variant_bridge_state"])))
    detail_rows.sort(key=lambda item: (str(item["variant_bridge_state"]), str(item["family"])))
    return detail_rows, summary_rows


def _write_markdown(output_dir: Path, detail_rows: list[dict[str, Any]], summary_rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Passive Variant Bridge Lupe",
        "",
        "Dieser Bericht gruppiert variant_bridge_anchor nach Textinsel-Uebergang.",
        "",
        "## Bruecken",
    ]
    for row in summary_rows:
        lines.append(
            "- {state}: {left} -> {right}; families={count}; delta={delta}; {families}".format(
                state=row["variant_bridge_state"],
                left=row["left_text_island"],
                right=row["right_text_island"],
                count=row["family_count"],
                delta=row["avg_score_delta_right_minus_left"],
                families=row["families"],
            )
        )
    lines.append("")
    lines.append("## Lesart")
    lines.append(
        "Eine Variantenbruecke ist interessanter als ein stabiler Einzelform-Anker, "
        "weil die Familie erhalten bleibt, waehrend die Textinsel wechseln darf."
    )
    lines.append("")
    lines.append("## Wirkungsgrenze")
    lines.append("- keine Runtime-Lesung")
    lines.append("- keine Handlung")
    lines.append("- kein Gate")
    lines.append("- kein Entry-Signal")
    lines.append("- kein Richtungssignal")
    text = "\n".join(lines)
    (output_dir / "passive_variant_bridge_lupe.md").write_text(text, encoding="utf-8")
    (output_dir / "passive_variant_bridge_lupe.txt").write_text(text, encoding="utf-8")


def run(anchor_lupe_path: Path, output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_rows, summary_rows = build_rows(_read_csv(anchor_lupe_path))
    detail_fields = [
        "variant_bridge_state",
        "family",
        "left_text_island",
        "right_text_island",
        "left_avg_score",
        "right_avg_score",
        "score_delta_right_minus_left",
        *PASSIVE_FLAGS.keys(),
    ]
    summary_fields = [
        "variant_bridge_state",
        "left_text_island",
        "right_text_island",
        "family_count",
        "families",
        "avg_left_score",
        "avg_right_score",
        "avg_score_delta_right_minus_left",
        *PASSIVE_FLAGS.keys(),
    ]
    _write_csv(output_dir / "passive_variant_bridge_lupe.csv", detail_rows, detail_fields)
    _write_csv(output_dir / "passive_variant_bridge_lupe_summary.csv", summary_rows, summary_fields)
    payload = {
        "schema": "dio_mini_passive_variant_bridge_lupe.v1",
        "anchor_lupe_path": str(anchor_lupe_path),
        "bridge_group_count": len(summary_rows),
        "family_count": len(detail_rows),
        "summary": summary_rows,
        "rows": detail_rows,
        **PASSIVE_FLAGS,
    }
    (output_dir / "passive_variant_bridge_lupe.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    _write_markdown(output_dir, detail_rows, summary_rows)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect passive Mini-DIO variant bridges")
    parser.add_argument("--anchor-lupe", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = run(Path(args.anchor_lupe), Path(args.output_dir))
    print(
        f"variant_bridge_lupe groups={result['bridge_group_count']} "
        f"families={result['family_count']} output={args.output_dir}"
    )


if __name__ == "__main__":
    main()
