"""Combine reflection map with local syntax confirmation.

This is diagnostic only. It answers: does a family only remember related
experience, or is it already locally confirmed in the current world?
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.analyze_syntax import analyze as analyze_syntax


TRADE_ACTIONS = ("LONG", "SHORT")


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _dominant_local_action(row: dict) -> str:
    executed_long = _safe_int(row.get("executed_long", 0))
    executed_short = _safe_int(row.get("executed_short", 0))
    best_long = _safe_int(row.get("best_long", 0))
    best_short = _safe_int(row.get("best_short", 0))
    long_score = executed_long + (best_long * 0.35)
    short_score = executed_short + (best_short * 0.35)
    if long_score <= 0.0 and short_score <= 0.0:
        return "-"
    return "LONG" if long_score >= short_score else "SHORT"


def _local_confirmation(row: dict, action: str) -> float:
    if action not in TRADE_ACTIONS:
        return 0.0
    executed = _safe_int(row.get(f"executed_{action.lower()}", 0))
    best = _safe_int(row.get(f"best_{action.lower()}", 0))
    rows = max(1, _safe_int(row.get("rows", 0)))
    reward = max(0.0, _safe_float(row.get("reward_sum", 0.0)))
    observation_events = _safe_int(row.get("observation_learning_events", 0))
    observation_pressure = _safe_float(row.get("avg_observation_pressure", 0.0))
    executed_part = executed / rows
    best_part = best / rows
    observation_part = min(1.0, observation_events / rows) * observation_pressure
    reward_part = min(1.0, reward / max(1, rows))
    return (executed_part * 0.45) + (best_part * 0.22) + (observation_part * 0.18) + (reward_part * 0.15)


def _load_reflection_map(path: Path) -> dict[str, dict]:
    rows = {}
    if not path.exists():
        return rows
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows[str(row.get("family", "-") or "-")] = dict(row)
    return rows


def _confirmation_state(local_score: float, row: dict, reflection: dict) -> str:
    executed_total = _safe_int(row.get("executed_long", 0)) + _safe_int(row.get("executed_short", 0))
    observation_events = _safe_int(row.get("observation_learning_events", 0))
    conflict_score = _safe_float(reflection.get("best_conflict_score", 0.0)) if reflection else 0.0
    support_score = _safe_float(reflection.get("best_support_score", 0.0)) if reflection else 0.0
    if local_score > 0.0 and executed_total > 0:
        return "locally_confirmed"
    if observation_events > 0 and support_score > 0.0:
        return "observed_related"
    if conflict_score > support_score and conflict_score > 0.0:
        return "conflict_related"
    if support_score > 0.0:
        return "related_unconfirmed"
    return "local_only"


def _confirmation_label(row: dict, local_score: float, reflection: dict) -> str:
    executed_total = _safe_int(row.get("executed_long", 0)) + _safe_int(row.get("executed_short", 0))
    observation_events = _safe_int(row.get("observation_learning_events", 0))
    support_score = _safe_float(reflection.get("best_support_score", 0.0)) if reflection else 0.0
    if executed_total > 0:
        return "executed_local_confirmation"
    if observation_events > 0 and support_score > 0.0:
        return "observed_related_potential"
    if local_score > 0.0:
        return "unexecuted_local_potential"
    return "unconfirmed"


def build_confirmation(debug_root: Path, reflection_map_path: Path) -> list[dict]:
    syntax_rows = analyze_syntax(debug_root)
    reflection_rows = _load_reflection_map(reflection_map_path)
    output = []
    for row in syntax_rows:
        family = str(row.get("family", "-") or "-")
        reflection = reflection_rows.get(family, {})
        local_action = _dominant_local_action(row)
        local_score = _local_confirmation(row, local_action)
        support_action = str(reflection.get("best_support_action", "-") or "-")
        support_family = str(reflection.get("best_support_family", "-") or "-")
        conflict_family = str(reflection.get("best_conflict_family", "-") or "-")
        support_matches_local = int(local_action in TRADE_ACTIONS and support_action == local_action)
        output.append(
            {
                "family": family,
                "local_action": local_action,
                "local_confirmation": round(local_score, 6),
                "state": _confirmation_state(local_score, row, reflection),
                "confirmation_label": _confirmation_label(row, local_score, reflection),
                "runs": row.get("runs", ""),
                "rows": _safe_int(row.get("rows", 0)),
                "executed_long": _safe_int(row.get("executed_long", 0)),
                "executed_short": _safe_int(row.get("executed_short", 0)),
                "best_long": _safe_int(row.get("best_long", 0)),
                "best_short": _safe_int(row.get("best_short", 0)),
                "reward_sum": round(_safe_float(row.get("reward_sum", 0.0)), 6),
                "observation_learning_events": _safe_int(row.get("observation_learning_events", 0)),
                "avg_observation_pressure": round(_safe_float(row.get("avg_observation_pressure", 0.0)), 6),
                "best_support_family": support_family,
                "best_support_action": support_action,
                "best_support_score": round(_safe_float(reflection.get("best_support_score", 0.0)), 6),
                "support_matches_local": support_matches_local,
                "best_conflict_family": conflict_family,
                "best_conflict_actions": str(reflection.get("best_conflict_actions", "-") or "-"),
                "best_conflict_score": round(_safe_float(reflection.get("best_conflict_score", 0.0)), 6),
            }
        )
    output.sort(
        key=lambda item: (
            _safe_float(item.get("local_confirmation", 0.0)),
            _safe_float(item.get("best_support_score", 0.0)),
            _safe_float(item.get("reward_sum", 0.0)),
        ),
        reverse=True,
    )
    return output


def write_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_local_confirmation.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    if rows:
        with (output_dir / "dio_mini_local_confirmation.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build DIO mini local confirmation report")
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--reflection-map", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    rows = build_confirmation(Path(args.debug_root), Path(args.reflection_map))
    write_outputs(rows, Path(args.output_dir))
    for row in rows[:12]:
        print(
            f"family={row['family']} label={row['confirmation_label']} state={row['state']} local={row['local_action']} "
            f"confirm={row['local_confirmation']:.4f} support={row['best_support_family']}"
        )


if __name__ == "__main__":
    main()
