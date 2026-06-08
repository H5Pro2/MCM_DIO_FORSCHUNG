"""Inspect lost passive inner cores against a newer inner map.

The report checks whether lost core text-islands disappeared, softened, drifted,
or reappeared through family overlap in a newer passive inner map. Diagnostic
only; no runtime coupling.
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


def _split(value: object) -> set[str]:
    text = str(value or "").strip()
    if not text or text == "-":
        return set()
    return {item.strip() for item in text.split("|") if item.strip() and item.strip() != "-"}


def _jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 1.0
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def _classify(symbol_match: dict | None, best_overlap: float) -> str:
    if symbol_match:
        state = str(symbol_match.get("inner_map_state", "") or "")
        if state == "inner_variation_bearing_space":
            return "still_variation_bearing_but_not_core"
        if state == "inner_soft_variation_space":
            return "softened_into_inner_variation"
        if state == "inner_drift_watch_space":
            return "shifted_into_drift_watch"
        if state == "inner_unconfirmed_raw_space":
            return "softened_into_raw_unconfirmed"
        return f"present_as_{state or 'unknown'}"
    if best_overlap >= 0.50:
        return "reorganized_into_related_text_island"
    if best_overlap > 0.0:
        return "fragmented_into_weak_overlap"
    return "not_visible_in_right_inner_map"


def _note(row: dict) -> str:
    return (
        f"{row['lost_text_island_symbol']}: {row['lost_core_reorganization_state']}; "
        f"best_overlap={row['best_family_overlap']:.3f}; "
        f"best_target={row['best_target_text_island_symbol'] or '-'}; "
        "passiv, keine Handlung."
    )


def build_rows(lost_rows: list[dict], right_inner_map_rows: list[dict], targets: set[str]) -> tuple[list[dict], list[dict]]:
    right_by_symbol = {str(row.get("text_island_symbol", "") or ""): row for row in right_inner_map_rows}
    output: list[dict] = []
    selected = [
        row
        for row in lost_rows
        if str(row.get("core_stability_state", "") or "").startswith("lost_")
        and (not targets or str(row.get("text_island_symbol", "") or "") in targets)
    ]
    for lost in selected:
        symbol = str(lost.get("text_island_symbol", "") or "")
        lost_families = _split(lost.get("left_families"))
        symbol_match = right_by_symbol.get(symbol)
        best_symbol = ""
        best_state = ""
        best_families = ""
        best_overlap = 0.0
        for candidate in right_inner_map_rows:
            candidate_symbol = str(candidate.get("text_island_symbol", "") or "")
            candidate_families = _split(candidate.get("families"))
            overlap = _jaccard(lost_families, candidate_families)
            if overlap > best_overlap:
                best_overlap = overlap
                best_symbol = candidate_symbol
                best_state = str(candidate.get("inner_map_state", "") or "")
                best_families = str(candidate.get("families", "") or "")
        row = {
            "lost_text_island_symbol": symbol,
            "lost_core_state": lost.get("left_inner_core_state", ""),
            "lost_score": round(_safe_float(lost.get("left_score")), 9),
            "right_symbol_present": bool(symbol_match),
            "right_symbol_inner_map_state": (symbol_match or {}).get("inner_map_state", ""),
            "right_symbol_score": round(_safe_float((symbol_match or {}).get("semantic_maturity_score")), 9),
            "best_target_text_island_symbol": best_symbol,
            "best_target_inner_map_state": best_state,
            "best_family_overlap": round(best_overlap, 9),
            "lost_families": "|".join(sorted(lost_families)),
            "best_target_families": best_families,
            **PASSIVE_BOUNDARY,
        }
        row["lost_core_reorganization_state"] = _classify(symbol_match, best_overlap)
        row["reorganization_note"] = _note(row)
        output.append(row)

    summary: dict[str, dict] = {}
    for row in output:
        state = str(row["lost_core_reorganization_state"])
        bucket = summary.setdefault(
            state,
            {
                "lost_core_reorganization_state": state,
                "count": 0,
                "avg_best_family_overlap": 0.0,
                **PASSIVE_BOUNDARY,
            },
        )
        count = int(bucket["count"])
        bucket["count"] = count + 1
        bucket["avg_best_family_overlap"] = (
            (float(bucket["avg_best_family_overlap"]) * count) + float(row["best_family_overlap"])
        ) / max(1, count + 1)
    summary_rows = []
    for item in summary.values():
        item["avg_best_family_overlap"] = round(float(item["avg_best_family_overlap"]), 9)
        summary_rows.append(item)
    return output, sorted(summary_rows, key=lambda row: (-int(row["count"]), row["lost_core_reorganization_state"]))


def write_outputs(rows: list[dict], summary: list[dict], output_dir: Path, lost_path: Path, right_map_path: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(
        output_dir / "passive_lost_core_reorganization_lupe.csv",
        rows,
        [
            "lost_text_island_symbol",
            "lost_core_reorganization_state",
            "lost_score",
            "right_symbol_present",
            "right_symbol_inner_map_state",
            "best_target_text_island_symbol",
            "best_target_inner_map_state",
            "best_family_overlap",
            "reorganization_note",
        ],
    )
    _write_csv(
        output_dir / "passive_lost_core_reorganization_lupe_summary.csv",
        summary,
        ["lost_core_reorganization_state", "count", "avg_best_family_overlap"],
    )
    (output_dir / "passive_lost_core_reorganization_lupe.json").write_text(
        json.dumps(
            {
                "lost_core_stability_lupe": str(lost_path),
                "right_inner_map": str(right_map_path),
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
        "# Passive Lost Core Reorganization Lupe",
        "",
        f"- lost_core_stability_lupe: `{lost_path}`",
        f"- right_inner_map: `{right_map_path}`",
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
        lines.append(
            f"- {row['lost_core_reorganization_state']}: {row['count']} "
            f"overlap={row['avg_best_family_overlap']:.3f}"
        )
    lines.extend(["", "## Lupe"])
    for row in rows:
        lines.append(f"- {row['reorganization_note']}")
    (output_dir / "passive_lost_core_reorganization_lupe.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect lost passive inner cores")
    parser.add_argument("--core-stability-lupe", type=Path, required=True)
    parser.add_argument("--right-inner-map", type=Path, required=True)
    parser.add_argument("--target", nargs="*", default=[])
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    rows, summary = build_rows(_read_csv(args.core_stability_lupe), _read_csv(args.right_inner_map), set(args.target))
    write_outputs(rows, summary, args.output_dir, args.core_stability_lupe, args.right_inner_map)
    print(
        json.dumps(
            {
                "lost_cores": len(rows),
                "summary": {row["lost_core_reorganization_state"]: row["count"] for row in summary},
                **PASSIVE_BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
