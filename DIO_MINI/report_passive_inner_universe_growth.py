"""Report passive Mini-DIO inner-universe growth across inner-map stages.

The report is diagnostic only. It reads existing passive text-island inner maps
and summarizes stable core, raw space, variation space, drift and recurrence.
It does not write runtime memory and is not read by Mini-DIO.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
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


def _parse_stage(raw: str) -> tuple[str, Path]:
    if "=" not in raw:
        raise ValueError(f"Stage must use LABEL=PATH, got: {raw}")
    label, path = raw.split("=", 1)
    label = label.strip()
    if not label:
        raise ValueError(f"Stage label is empty: {raw}")
    return label, Path(path.strip())


def _ratio(part: int | float, whole: int | float) -> float:
    return round(float(part) / max(1.0, float(whole)), 9)


def _avg(rows: list[dict[str, str]], key: str) -> float:
    if not rows:
        return 0.0
    return round(mean(_safe_float(row.get(key)) for row in rows), 9)


def _stage_summary(label: str, path: Path, rows: list[dict[str, str]], order: int) -> dict[str, Any]:
    inner_counts = Counter(str(row.get("inner_map_state", "") or "unknown") for row in rows)
    maturity_counts = Counter(str(row.get("text_island_maturity_state", "") or "unknown") for row in rows)
    total = len(rows)
    stable_core = inner_counts.get("inner_stable_recurrence_space", 0)
    variation = inner_counts.get("inner_soft_variation_space", 0)
    drift = inner_counts.get("inner_drift_watch_space", 0)
    raw = (
        inner_counts.get("inner_unconfirmed_raw_space", 0)
        + inner_counts.get("inner_unconfirmed_movement_space", 0)
    )
    dominant_inner_state = inner_counts.most_common(1)[0][0] if inner_counts else "unknown"
    dominant_maturity_state = maturity_counts.most_common(1)[0][0] if maturity_counts else "unknown"
    return {
        "stage_order": order,
        "stage_label": label,
        "source_path": str(path),
        "text_island_count": total,
        "stable_core_count": stable_core,
        "stable_core_ratio": _ratio(stable_core, total),
        "soft_variation_count": variation,
        "soft_variation_ratio": _ratio(variation, total),
        "drift_watch_count": drift,
        "drift_watch_ratio": _ratio(drift, total),
        "raw_space_count": raw,
        "raw_space_ratio": _ratio(raw, total),
        "avg_semantic_maturity_score": _avg(rows, "semantic_maturity_score"),
        "avg_stability_pressure": _avg(rows, "stability_pressure"),
        "avg_variation_bearing": _avg(rows, "variation_bearing"),
        "avg_drift_pressure": _avg(rows, "drift_pressure"),
        "dominant_inner_state": dominant_inner_state,
        "dominant_maturity_state": dominant_maturity_state,
        "inner_state_counts": dict(sorted(inner_counts.items())),
        "maturity_state_counts": dict(sorted(maturity_counts.items())),
        **PASSIVE_FLAGS,
    }


def _index_by_symbol(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    indexed: dict[str, dict[str, str]] = {}
    for row in rows:
        symbol = str(row.get("text_island_symbol", "") or "").strip()
        if symbol:
            indexed[symbol] = row
    return indexed


def _transition_summary(
    left_label: str,
    left_rows: list[dict[str, str]],
    right_label: str,
    right_rows: list[dict[str, str]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    left = _index_by_symbol(left_rows)
    right = _index_by_symbol(right_rows)
    left_symbols = set(left)
    right_symbols = set(right)
    shared = sorted(left_symbols & right_symbols)
    new = sorted(right_symbols - left_symbols)
    lost = sorted(left_symbols - right_symbols)
    transition_counts: Counter[str] = Counter()
    maturity_transition_counts: Counter[str] = Counter()
    details: list[dict[str, Any]] = []

    for symbol in shared:
        lrow = left[symbol]
        rrow = right[symbol]
        left_state = str(lrow.get("inner_map_state", "") or "unknown")
        right_state = str(rrow.get("inner_map_state", "") or "unknown")
        left_maturity = str(lrow.get("text_island_maturity_state", "") or "unknown")
        right_maturity = str(rrow.get("text_island_maturity_state", "") or "unknown")
        transition = f"{left_state}->{right_state}"
        maturity_transition = f"{left_maturity}->{right_maturity}"
        transition_counts[transition] += 1
        maturity_transition_counts[maturity_transition] += 1
        details.append(
            {
                "transition": f"{left_label}->{right_label}",
                "text_island_symbol": symbol,
                "left_inner_map_state": left_state,
                "right_inner_map_state": right_state,
                "left_maturity_state": left_maturity,
                "right_maturity_state": right_maturity,
                "semantic_maturity_delta": round(
                    _safe_float(rrow.get("semantic_maturity_score"))
                    - _safe_float(lrow.get("semantic_maturity_score")),
                    9,
                ),
                "stability_pressure_delta": round(
                    _safe_float(rrow.get("stability_pressure"))
                    - _safe_float(lrow.get("stability_pressure")),
                    9,
                ),
                "variation_bearing_delta": round(
                    _safe_float(rrow.get("variation_bearing"))
                    - _safe_float(lrow.get("variation_bearing")),
                    9,
                ),
                "drift_pressure_delta": round(
                    _safe_float(rrow.get("drift_pressure"))
                    - _safe_float(lrow.get("drift_pressure")),
                    9,
                ),
                "right_families": str(rrow.get("families", "") or ""),
                **PASSIVE_FLAGS,
            }
        )

    state_counts_right = Counter(str(right[s].get("inner_map_state", "") or "unknown") for s in new)
    maturity_counts_right = Counter(
        str(right[s].get("text_island_maturity_state", "") or "unknown") for s in new
    )
    shared_ratio_left = _ratio(len(shared), len(left_symbols))
    new_ratio_right = _ratio(len(new), len(right_symbols))
    lost_ratio_left = _ratio(len(lost), len(left_symbols))
    avg_score_delta = round(
        mean(_safe_float(row["semantic_maturity_delta"]) for row in details) if details else 0.0,
        9,
    )
    avg_drift_delta = round(
        mean(_safe_float(row["drift_pressure_delta"]) for row in details) if details else 0.0,
        9,
    )
    development_state = _development_state(
        shared_ratio_left=shared_ratio_left,
        new_ratio_right=new_ratio_right,
        lost_ratio_left=lost_ratio_left,
        avg_score_delta=avg_score_delta,
        avg_drift_delta=avg_drift_delta,
    )
    summary = {
        "transition": f"{left_label}->{right_label}",
        "left_stage": left_label,
        "right_stage": right_label,
        "left_text_island_count": len(left_symbols),
        "right_text_island_count": len(right_symbols),
        "shared_text_island_count": len(shared),
        "new_text_island_count": len(new),
        "lost_text_island_count": len(lost),
        "shared_ratio_left": shared_ratio_left,
        "shared_ratio_right": _ratio(len(shared), len(right_symbols)),
        "new_ratio_right": new_ratio_right,
        "lost_ratio_left": lost_ratio_left,
        "new_inner_state_counts": dict(sorted(state_counts_right.items())),
        "new_maturity_state_counts": dict(sorted(maturity_counts_right.items())),
        "inner_state_transition_counts": dict(sorted(transition_counts.items())),
        "maturity_transition_counts": dict(sorted(maturity_transition_counts.items())),
        "avg_shared_semantic_maturity_delta": avg_score_delta,
        "avg_shared_stability_pressure_delta": round(
            mean(_safe_float(row["stability_pressure_delta"]) for row in details) if details else 0.0,
            9,
        ),
        "avg_shared_variation_bearing_delta": round(
            mean(_safe_float(row["variation_bearing_delta"]) for row in details) if details else 0.0,
            9,
        ),
        "avg_shared_drift_pressure_delta": avg_drift_delta,
        "development_state": development_state,
        **PASSIVE_FLAGS,
    }
    return summary, details


def _development_state(
    *,
    shared_ratio_left: float,
    new_ratio_right: float,
    lost_ratio_left: float,
    avg_score_delta: float,
    avg_drift_delta: float,
) -> str:
    if lost_ratio_left > 0.12:
        return "evolutionary_regression"
    if lost_ratio_left > 0.0 or avg_drift_delta > 0.055:
        return "reorganization_pressure"
    if new_ratio_right >= 0.32 and shared_ratio_left >= 0.80:
        return "jump_expansion_with_binding"
    if new_ratio_right >= 0.14 and shared_ratio_left >= 0.80:
        return "organic_expansion"
    if new_ratio_right < 0.08 and abs(avg_score_delta) < 0.03 and shared_ratio_left >= 0.80:
        return "plateau_stabilization"
    if avg_score_delta > 0.06 and shared_ratio_left >= 0.80:
        return "consolidating_recurrence"
    return "open_evolutionary_motion"


def _build_reading(stage_rows: list[dict[str, Any]], transition_rows: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    lines.append("# Passive Inner-Universe Growth")
    lines.append("")
    lines.append("Dieser Bericht ist passiv. Er schreibt keine Runtime-Memory und beeinflusst keine Handlung.")
    lines.append("")
    lines.append("## Stufen")
    for row in stage_rows:
        lines.append(
            "- {stage}: text_islands={count}, stable_core={stable}, "
            "soft_variation={variation}, drift_watch={drift}, raw_space={raw}, "
            "avg_score={score}".format(
                stage=row["stage_label"],
                count=row["text_island_count"],
                stable=row["stable_core_count"],
                variation=row["soft_variation_count"],
                drift=row["drift_watch_count"],
                raw=row["raw_space_count"],
                score=row["avg_semantic_maturity_score"],
            )
        )
    if transition_rows:
        lines.append("")
        lines.append("## Uebergaenge")
        for row in transition_rows:
            lines.append(
                "- {transition}: shared={shared}, new={new}, lost={lost}, "
                "new_ratio={new_ratio}, shared_delta_score={delta}, state={state}".format(
                    transition=row["transition"],
                    shared=row["shared_text_island_count"],
                    new=row["new_text_island_count"],
                    lost=row["lost_text_island_count"],
                    new_ratio=row["new_ratio_right"],
                    delta=row["avg_shared_semantic_maturity_delta"],
                    state=row["development_state"],
                )
            )
    lines.append("")
    lines.append("## Lesart")
    lines.append(
        "Reproduzierbare Inseln zeigen Rueckbindung an gelebte Realitaet. "
        "Neue Inseln zeigen Erweiterung des inneren Universums. Drift zeigt "
        "noch ungebundene oder umorganisierte Bedeutung."
    )
    lines.append("")
    lines.append("## Wirkungsgrenze")
    lines.append("- keine Runtime-Lesung")
    lines.append("- keine Handlung")
    lines.append("- kein Gate")
    lines.append("- kein Entry-Signal")
    lines.append("- kein Richtungssignal")
    return lines


def run(stages: list[tuple[str, Path]], output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    loaded: list[tuple[str, Path, list[dict[str, str]]]] = [
        (label, path, _read_csv(path)) for label, path in stages
    ]
    stage_rows = [
        _stage_summary(label, path, rows, index + 1)
        for index, (label, path, rows) in enumerate(loaded)
    ]
    transition_rows: list[dict[str, Any]] = []
    detail_rows: list[dict[str, Any]] = []
    for left, right in zip(loaded, loaded[1:]):
        summary, details = _transition_summary(left[0], left[2], right[0], right[2])
        transition_rows.append(summary)
        detail_rows.extend(details)

    payload = {
        "schema": "dio_mini_passive_inner_universe_growth.v1",
        "stage_count": len(stage_rows),
        "transition_count": len(transition_rows),
        "stages": stage_rows,
        "transitions": transition_rows,
        "shared_details": detail_rows,
        **PASSIVE_FLAGS,
    }

    stage_fields = [
        "stage_order",
        "stage_label",
        "source_path",
        "text_island_count",
        "stable_core_count",
        "stable_core_ratio",
        "soft_variation_count",
        "soft_variation_ratio",
        "drift_watch_count",
        "drift_watch_ratio",
        "raw_space_count",
        "raw_space_ratio",
        "avg_semantic_maturity_score",
        "avg_stability_pressure",
        "avg_variation_bearing",
        "avg_drift_pressure",
        "dominant_inner_state",
        "dominant_maturity_state",
        *PASSIVE_FLAGS.keys(),
    ]
    transition_fields = [
        "transition",
        "left_text_island_count",
        "right_text_island_count",
        "shared_text_island_count",
        "new_text_island_count",
        "lost_text_island_count",
        "development_state",
        "shared_ratio_left",
        "shared_ratio_right",
        "new_ratio_right",
        "lost_ratio_left",
        "avg_shared_semantic_maturity_delta",
        "avg_shared_stability_pressure_delta",
        "avg_shared_variation_bearing_delta",
        "avg_shared_drift_pressure_delta",
        *PASSIVE_FLAGS.keys(),
    ]
    detail_fields = [
        "transition",
        "text_island_symbol",
        "left_inner_map_state",
        "right_inner_map_state",
        "left_maturity_state",
        "right_maturity_state",
        "semantic_maturity_delta",
        "stability_pressure_delta",
        "variation_bearing_delta",
        "drift_pressure_delta",
        "right_families",
        *PASSIVE_FLAGS.keys(),
    ]

    _write_csv(output_dir / "passive_inner_universe_growth_stages.csv", stage_rows, stage_fields)
    _write_csv(output_dir / "passive_inner_universe_growth_transitions.csv", transition_rows, transition_fields)
    _write_csv(output_dir / "passive_inner_universe_growth_shared_details.csv", detail_rows, detail_fields)
    (output_dir / "passive_inner_universe_growth.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    reading = "\n".join(_build_reading(stage_rows, transition_rows))
    (output_dir / "passive_inner_universe_growth.md").write_text(reading, encoding="utf-8")
    (output_dir / "passive_inner_universe_growth.txt").write_text(reading, encoding="utf-8")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive Mini-DIO inner-universe growth")
    parser.add_argument(
        "--stage",
        action="append",
        required=True,
        help="Stage mapping in the form LABEL=path/to/passive_text_island_inner_map.csv",
    )
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    stages = [_parse_stage(item) for item in args.stage]
    result = run(stages, Path(args.output_dir))
    print(
        f"inner_universe_growth stages={result['stage_count']} "
        f"transitions={result['transition_count']} output={args.output_dir}"
    )


if __name__ == "__main__":
    main()
