"""Compare two passive Mini-DIO text-island inner maps.

The comparison is diagnostic only. It checks whether text islands keep their
inner map state, soften, strengthen, drift, or remain foreign-separated across
two passive map snapshots.
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


STATE_RANK = {
    "inner_unconfirmed_raw_space": 0,
    "inner_drift_watch_space": 1,
    "inner_foreign_boundary_space": 1,
    "inner_soft_variation_space": 2,
    "inner_stable_recurrence_space": 3,
    "inner_variation_bearing_space": 4,
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


def _transition_state(left_state: str, right_state: str, score_delta: float) -> str:
    if not left_state:
        return "new_in_right_inner_map"
    if not right_state:
        return "missing_in_right_inner_map"
    if left_state == right_state:
        if left_state == "inner_foreign_boundary_space":
            return "stable_foreign_boundary"
        if left_state == "inner_variation_bearing_space":
            return "stable_variation_bearing"
        if left_state == "inner_stable_recurrence_space":
            return "stable_recurrence"
        if left_state == "inner_drift_watch_space":
            return "persistent_drift_watch"
        return "stable_same_inner_state"
    left_rank = STATE_RANK.get(left_state, 0)
    right_rank = STATE_RANK.get(right_state, 0)
    if right_state == "inner_drift_watch_space":
        return "shifted_into_drift_watch"
    if right_state == "inner_foreign_boundary_space":
        return "shifted_into_foreign_boundary"
    if right_rank > left_rank or score_delta > 0.08:
        return "inner_state_strengthened"
    if right_rank < left_rank or score_delta < -0.08:
        return "inner_state_softened"
    return "inner_state_reorganized"


def build_rows(left_rows: list[dict], right_rows: list[dict]) -> tuple[list[dict], list[dict]]:
    left = _index(left_rows)
    right = _index(right_rows)
    symbols = sorted(set(left) | set(right))
    rows: list[dict] = []
    for symbol in symbols:
        lrow = dict(left.get(symbol, {}) or {})
        rrow = dict(right.get(symbol, {}) or {})
        left_state = str(lrow.get("inner_map_state", "") or "")
        right_state = str(rrow.get("inner_map_state", "") or "")
        left_score = _safe_float(lrow.get("semantic_maturity_score"))
        right_score = _safe_float(rrow.get("semantic_maturity_score"))
        left_stability = _safe_float(lrow.get("stability_pressure"))
        right_stability = _safe_float(rrow.get("stability_pressure"))
        left_variation = _safe_float(lrow.get("variation_bearing"))
        right_variation = _safe_float(rrow.get("variation_bearing"))
        left_drift = _safe_float(lrow.get("drift_pressure"))
        right_drift = _safe_float(rrow.get("drift_pressure"))
        score_delta = right_score - left_score
        state = _transition_state(left_state, right_state, score_delta)
        rows.append(
            {
                "text_island_symbol": symbol,
                "inner_map_transition_state": state,
                "left_inner_map_state": left_state,
                "right_inner_map_state": right_state,
                "left_semantic_maturity_score": round(left_score, 9),
                "right_semantic_maturity_score": round(right_score, 9),
                "score_delta": round(score_delta, 9),
                "stability_delta": round(right_stability - left_stability, 9),
                "variation_delta": round(right_variation - left_variation, 9),
                "drift_delta": round(right_drift - left_drift, 9),
                "left_families": lrow.get("families", ""),
                "right_families": rrow.get("families", ""),
                **PASSIVE_BOUNDARY,
            }
        )

    summary: dict[str, dict] = {}
    for row in rows:
        state = str(row["inner_map_transition_state"])
        bucket = summary.setdefault(
            state,
            {
                "inner_map_transition_state": state,
                "count": 0,
                "avg_score_delta": 0.0,
                "avg_stability_delta": 0.0,
                "avg_variation_delta": 0.0,
                "avg_drift_delta": 0.0,
                **PASSIVE_BOUNDARY,
            },
        )
        count = int(bucket["count"])
        bucket["count"] = count + 1
        for key in ["score_delta", "stability_delta", "variation_delta", "drift_delta"]:
            avg_key = f"avg_{key}"
            bucket[avg_key] = ((float(bucket[avg_key]) * count) + float(row[key])) / max(1, count + 1)
    summary_rows = []
    for item in summary.values():
        for key in ["avg_score_delta", "avg_stability_delta", "avg_variation_delta", "avg_drift_delta"]:
            item[key] = round(float(item[key]), 9)
        summary_rows.append(item)
    return rows, sorted(summary_rows, key=lambda row: (-int(row["count"]), row["inner_map_transition_state"]))


def write_outputs(rows: list[dict], summary_rows: list[dict], output_dir: Path, left_path: Path, right_path: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(
        output_dir / "passive_text_island_inner_map_compare.csv",
        rows,
        [
            "text_island_symbol",
            "inner_map_transition_state",
            "left_inner_map_state",
            "right_inner_map_state",
            "left_semantic_maturity_score",
            "right_semantic_maturity_score",
            "score_delta",
            "stability_delta",
            "variation_delta",
            "drift_delta",
        ],
    )
    _write_csv(
        output_dir / "passive_text_island_inner_map_compare_summary.csv",
        summary_rows,
        [
            "inner_map_transition_state",
            "count",
            "avg_score_delta",
            "avg_stability_delta",
            "avg_variation_delta",
            "avg_drift_delta",
        ],
    )
    payload = {
        "left": str(left_path),
        "right": str(right_path),
        "rows": rows,
        "summary": summary_rows,
        "boundary": PASSIVE_BOUNDARY,
    }
    (output_dir / "passive_text_island_inner_map_compare.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    lines = [
        "# Passive Text Island Inner Map Compare",
        "",
        f"- left: `{left_path}`",
        f"- right: `{right_path}`",
        f"- compared_text_islands: `{len(rows)}`",
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
            f"- {row['inner_map_transition_state']}: {row['count']} "
            f"(score_delta={row['avg_score_delta']:.3f}, "
            f"stability_delta={row['avg_stability_delta']:.3f}, "
            f"variation_delta={row['avg_variation_delta']:.3f})"
        )
    lines.extend(["", "## Wichtige stabile Raeume", ""])
    stable_states = {"stable_variation_bearing", "stable_recurrence", "stable_foreign_boundary"}
    for row in [item for item in rows if item["inner_map_transition_state"] in stable_states][:40]:
        lines.append(
            f"- {row['text_island_symbol']}: {row['inner_map_transition_state']} "
            f"{row['left_inner_map_state']} -> {row['right_inner_map_state']}; "
            f"score_delta={row['score_delta']:.3f}"
        )
    (output_dir / "passive_text_island_inner_map_compare.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (output_dir / "passive_text_island_inner_map_compare.txt").write_text(
        "\n".join(f"{row['text_island_symbol']}: {row['inner_map_transition_state']}" for row in rows) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare passive text-island inner maps")
    parser.add_argument("--left", type=Path, required=True)
    parser.add_argument("--right", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    rows, summary_rows = build_rows(_read_csv(args.left), _read_csv(args.right))
    write_outputs(rows, summary_rows, args.output_dir, args.left, args.right)
    print(
        json.dumps(
            {
                "left": str(args.left),
                "right": str(args.right),
                "compared_text_islands": len(rows),
                "summary": {row["inner_map_transition_state"]: row["count"] for row in summary_rows},
                **PASSIVE_BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
