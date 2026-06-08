"""Build passive reorganization history for Mini-DIO text islands.

The report compares multiple passive text-island inner maps and describes how
each text-island symbol moves through inner states over time:
core, variation, drift, raw emergence, foreign boundary, or absence.

Diagnostic only. No runtime reading, no action, no entry, no gate.
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
    "inner_variation_bearing_space",
    "inner_stable_recurrence_space",
    "inner_foreign_boundary_space",
}

DRIFT_STATES = {
    "inner_drift_watch_space",
}

RAW_STATES = {
    "inner_unconfirmed_raw_space",
}

SOFT_STATES = {
    "inner_soft_variation_space",
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


def _parse_source(raw: str) -> tuple[str, Path]:
    if "=" in raw:
        label, path = raw.split("=", 1)
        return label.strip(), Path(path.strip())
    path = Path(raw.strip())
    return path.stem, path


def _source_csv(path: Path) -> Path:
    if path.is_dir():
        return path / "passive_text_island_inner_map.csv"
    return path


def _families(value: object) -> set[str]:
    text = str(value or "").strip()
    if not text or text == "-":
        return set()
    return {item.strip() for item in text.split("|") if item.strip() and item.strip() != "-"}


def _trajectory_state(states: list[str]) -> str:
    visible = [state for state in states if state != "absent"]
    if not visible:
        return "text_island_absent"
    unique = set(visible)
    if len(unique) == 1:
        only = visible[0]
        if only == "inner_foreign_boundary_space":
            return "stable_foreign_boundary_history"
        if only == "inner_stable_recurrence_space":
            return "stable_recurrence_history"
        if only == "inner_variation_bearing_space":
            return "stable_variation_history"
        if only == "inner_drift_watch_space":
            return "persistent_drift_history"
        if only == "inner_unconfirmed_raw_space":
            return "persistent_raw_history"
        return f"stable_{only}"
    if visible[-1] in DRIFT_STATES and any(state in CORE_STATES for state in visible[:-1]):
        return "core_to_drift_reorganization"
    if visible[-1] in CORE_STATES and any(state in DRIFT_STATES | RAW_STATES | SOFT_STATES for state in visible[:-1]):
        return "reorganized_into_core"
    if visible[-1] in SOFT_STATES and any(state in CORE_STATES for state in visible[:-1]):
        return "core_to_soft_variation"
    if visible[-1] in RAW_STATES and any(state in CORE_STATES for state in visible[:-1]):
        return "core_to_raw_softening"
    if "absent" in states[:-1] and visible[-1] in CORE_STATES:
        return "late_core_emergence"
    if "absent" in states[:-1]:
        return "late_text_island_emergence"
    return "mixed_reorganization_history"


def _family_change_state(family_sets: list[set[str]]) -> str:
    visible = [families for families in family_sets if families]
    if len(visible) < 2:
        return "family_basis_single_or_absent"
    first = visible[0]
    last = visible[-1]
    if first == last:
        return "family_basis_stable"
    if first and last and last < first:
        return "family_basis_thinned"
    if first and last and first < last:
        return "family_basis_expanded"
    overlap = len(first & last) / max(1, len(first | last))
    if overlap >= 0.50:
        return "family_basis_reorganized_near"
    if overlap > 0.0:
        return "family_basis_fragmented"
    return "family_basis_replaced"


def _note(row: dict) -> str:
    return (
        f"{row['text_island_symbol']}: {row['trajectory_state']}; "
        f"states={row['state_path']}; families={row['family_change_state']}; "
        "passiv, keine Handlung."
    )


def build_rows(sources: list[tuple[str, Path]]) -> tuple[list[dict], list[dict]]:
    maps: list[tuple[str, dict[str, dict]]] = []
    for label, source in sources:
        rows = _read_csv(_source_csv(source))
        maps.append((label, {str(row.get("text_island_symbol", "") or ""): row for row in rows}))

    symbols = sorted({symbol for _, mapping in maps for symbol in mapping if symbol})
    rows: list[dict] = []
    for symbol in symbols:
        states: list[str] = []
        maturities: list[str] = []
        scores: list[float] = []
        stability: list[float] = []
        variation: list[float] = []
        drift: list[float] = []
        family_sets: list[set[str]] = []
        family_counts: list[int] = []
        for _, mapping in maps:
            item = mapping.get(symbol)
            if item is None:
                states.append("absent")
                maturities.append("absent")
                scores.append(0.0)
                stability.append(0.0)
                variation.append(0.0)
                drift.append(0.0)
                family_sets.append(set())
                family_counts.append(0)
                continue
            states.append(str(item.get("inner_map_state", "") or "unknown"))
            maturities.append(str(item.get("text_island_maturity_state", "") or "unknown"))
            scores.append(_safe_float(item.get("semantic_maturity_score")))
            stability.append(_safe_float(item.get("stability_pressure")))
            variation.append(_safe_float(item.get("variation_bearing")))
            drift.append(_safe_float(item.get("drift_pressure")))
            families = _families(item.get("families"))
            family_sets.append(families)
            family_counts.append(_safe_int(item.get("family_count"), len(families)))

        row = {
            "text_island_symbol": symbol,
            "trajectory_state": _trajectory_state(states),
            "family_change_state": _family_change_state(family_sets),
            "labels": "|".join(label for label, _ in maps),
            "state_path": " -> ".join(states),
            "maturity_path": " -> ".join(maturities),
            "score_path": " -> ".join(f"{score:.6f}" for score in scores),
            "family_count_path": " -> ".join(str(count) for count in family_counts),
            "first_score": round(scores[0], 9) if scores else 0.0,
            "last_score": round(scores[-1], 9) if scores else 0.0,
            "score_delta": round((scores[-1] - scores[0]) if scores else 0.0, 9),
            "max_score": round(max(scores) if scores else 0.0, 9),
            "max_stability_pressure": round(max(stability) if stability else 0.0, 9),
            "max_variation_bearing": round(max(variation) if variation else 0.0, 9),
            "max_drift_pressure": round(max(drift) if drift else 0.0, 9),
            "first_families": "|".join(sorted(next((items for items in family_sets if items), set()))),
            "last_families": "|".join(sorted(next((items for items in reversed(family_sets) if items), set()))),
            **PASSIVE_BOUNDARY,
        }
        row["reorganization_history_note"] = _note(row)
        rows.append(row)

    summary: dict[str, dict] = {}
    for row in rows:
        state = str(row["trajectory_state"])
        bucket = summary.setdefault(
            state,
            {
                "trajectory_state": state,
                "count": 0,
                "avg_score_delta": 0.0,
                "avg_max_drift_pressure": 0.0,
                **PASSIVE_BOUNDARY,
            },
        )
        count = int(bucket["count"])
        bucket["count"] = count + 1
        bucket["avg_score_delta"] = ((float(bucket["avg_score_delta"]) * count) + float(row["score_delta"])) / max(
            1, count + 1
        )
        bucket["avg_max_drift_pressure"] = (
            (float(bucket["avg_max_drift_pressure"]) * count) + float(row["max_drift_pressure"])
        ) / max(1, count + 1)

    summary_rows = []
    for item in summary.values():
        item["avg_score_delta"] = round(float(item["avg_score_delta"]), 9)
        item["avg_max_drift_pressure"] = round(float(item["avg_max_drift_pressure"]), 9)
        summary_rows.append(item)
    return (
        sorted(rows, key=lambda row: (row["trajectory_state"], row["text_island_symbol"])),
        sorted(summary_rows, key=lambda row: (-int(row["count"]), row["trajectory_state"])),
    )


def write_outputs(rows: list[dict], summary_rows: list[dict], output_dir: Path, sources: list[tuple[str, Path]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(
        output_dir / "passive_text_island_reorganization_history.csv",
        rows,
        [
            "text_island_symbol",
            "trajectory_state",
            "family_change_state",
            "state_path",
            "maturity_path",
            "score_path",
            "family_count_path",
            "score_delta",
            "reorganization_history_note",
        ],
    )
    _write_csv(
        output_dir / "passive_text_island_reorganization_history_summary.csv",
        summary_rows,
        ["trajectory_state", "count", "avg_score_delta", "avg_max_drift_pressure"],
    )
    (output_dir / "passive_text_island_reorganization_history.json").write_text(
        json.dumps(
            {
                "sources": [{"label": label, "path": str(path)} for label, path in sources],
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
        "# Passive Text Island Reorganization History",
        "",
        "## Sources",
    ]
    for label, path in sources:
        lines.append(f"- {label}: `{path}`")
    lines.extend(
        [
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
    )
    for row in summary_rows:
        lines.append(
            f"- {row['trajectory_state']}: {row['count']} "
            f"delta={row['avg_score_delta']:.3f} drift={row['avg_max_drift_pressure']:.3f}"
        )
    lines.extend(["", "## History"])
    for row in rows[:160]:
        lines.append(f"- {row['reorganization_history_note']}")
    (output_dir / "passive_text_island_reorganization_history.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )
    (output_dir / "passive_text_island_reorganization_history.txt").write_text(
        "\n".join(row["reorganization_history_note"] for row in rows) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive text-island reorganization history")
    parser.add_argument("--map", action="append", required=True, help="label=path; can be repeated")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    sources = [_parse_source(item) for item in args.map]
    rows, summary_rows = build_rows(sources)
    write_outputs(rows, summary_rows, args.output_dir, sources)
    print(
        json.dumps(
            {
                "text_islands": len(rows),
                "summary": {row["trajectory_state"]: row["count"] for row in summary_rows},
                **PASSIVE_BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
