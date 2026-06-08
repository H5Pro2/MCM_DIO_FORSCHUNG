"""Analyze passive direction support behind maturity shifts.

This diagnostic joins syntax/maturity shifts with episode-level direction
traces. It checks whether a surviving syntax family keeps the same sensory
field while its observed best direction, reward context, or episode support
changes between two controlled worlds.

Passive only: Mini-DIO does not read this report for runtime, action, gates,
entry, or direction.
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


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        result = float(value if value not in (None, "") else default)
    except (TypeError, ValueError):
        return default
    if result != result:
        return default
    return result


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value if value not in (None, "") else default))
    except (TypeError, ValueError):
        return default


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = list(fields)
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=ordered)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in ordered})


def _episode_files(root: Path) -> list[Path]:
    if root.is_file() and root.name == "episodes.csv":
        return [root]
    return sorted(root.rglob("episodes.csv"))


def _families_from_alignment(rows: list[dict[str, str]]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for row in rows:
        family = str(row.get("symbol_family", "") or "").strip()
        if family and family not in seen:
            result.append(family)
            seen.add(family)
    return result


def _dominant(counter: Counter[str]) -> str:
    if not counter:
        return "-"
    return counter.most_common(1)[0][0]


def _counter_text(counter: Counter[str]) -> str:
    return "|".join(f"{key}:{value}" for key, value in sorted(counter.items()))


def _avg(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def _aggregate_family(roots: list[Path], family: str) -> dict[str, Any]:
    rows: list[dict[str, str]] = []
    source_files: set[str] = set()
    for root in roots:
        for path in _episode_files(root):
            with path.open("r", newline="", encoding="utf-8") as handle:
                for row in csv.DictReader(handle):
                    if str(row.get("symbol_family", "") or "") == family:
                        rows.append(dict(row))
                        source_files.add(str(path.parent.name))
    action = Counter(str(row.get("action", "") or "-") for row in rows)
    best_action = Counter(str(row.get("best_action_training", "") or "-") for row in rows)
    observation_action = Counter(str(row.get("observation_learning_action", "") or "-") for row in rows)
    world_labels = Counter(str(row.get("passive_world_label", "") or "-") for row in rows)
    temporal = Counter(str(row.get("mini_temporal_state", "") or "-") for row in rows)
    neuro = Counter(str(row.get("mini_neuro_dominant_tone", "") or "-") for row in rows)
    count = len(rows)
    return {
        "family": family,
        "episode_count": count,
        "source_count": len(source_files),
        "source_files": "|".join(sorted(source_files)),
        "world_labels": _counter_text(world_labels),
        "dominant_action": _dominant(action),
        "action_counts": _counter_text(action),
        "dominant_best_action": _dominant(best_action),
        "best_action_counts": _counter_text(best_action),
        "dominant_observation_action": _dominant(observation_action),
        "observation_action_counts": _counter_text(observation_action),
        "dominant_temporal_state": _dominant(temporal),
        "temporal_state_counts": _counter_text(temporal),
        "dominant_neuro_tone": _dominant(neuro),
        "neuro_tone_counts": _counter_text(neuro),
        "avg_reward": round(_avg([_safe_float(row.get("reward")) for row in rows]), 9),
        "avg_close_reward": round(_avg([_safe_float(row.get("close_reward")) for row in rows]), 9),
        "avg_best_reward_training": round(_avg([_safe_float(row.get("best_reward_training")) for row in rows]), 9),
        "avg_score_long": round(_avg([_safe_float(row.get("score_long")) for row in rows]), 9),
        "avg_score_short": round(_avg([_safe_float(row.get("score_short")) for row in rows]), 9),
        "avg_readiness_long": round(_avg([_safe_float(row.get("readiness_long")) for row in rows]), 9),
        "avg_readiness_short": round(_avg([_safe_float(row.get("readiness_short")) for row in rows]), 9),
        "avg_observation_long": round(_avg([_safe_float(row.get("observation_long")) for row in rows]), 9),
        "avg_observation_short": round(_avg([_safe_float(row.get("observation_short")) for row in rows]), 9),
        "avg_trade_readiness": round(_avg([_safe_float(row.get("trade_readiness")) for row in rows]), 9),
        "avg_observation_learning_pressure": round(
            _avg([_safe_float(row.get("observation_learning_pressure")) for row in rows]), 9
        ),
        "avg_sehen_form_flow": round(_avg([_safe_float(row.get("sehen_form_flow")) for row in rows]), 9),
        "avg_hoeren_energy_tone": round(_avg([_safe_float(row.get("hoeren_energy_tone")) for row in rows]), 9),
        "avg_fuehlen_mcm_coherence": round(_avg([_safe_float(row.get("fuehlen_mcm_coherence")) for row in rows]), 9),
    }


def _direction_state(left: dict[str, Any], right: dict[str, Any], align: dict[str, str]) -> str:
    left_best = str(left.get("dominant_best_action", "-"))
    right_best = str(right.get("dominant_best_action", "-"))
    left_obs = str(left.get("dominant_observation_action", "-"))
    right_obs = str(right.get("dominant_observation_action", "-"))
    reward_delta = _safe_float(right.get("avg_best_reward_training")) - _safe_float(left.get("avg_best_reward_training"))
    episode_delta = _safe_int(right.get("episode_count")) - _safe_int(left.get("episode_count"))
    sensory_state = str(align.get("alignment_state", ""))

    if left_best in {"LONG", "SHORT"} and right_best in {"LONG", "SHORT"} and left_best != right_best:
        return "direction_support_flips"
    if left_obs in {"LONG", "SHORT"} and right_obs in {"LONG", "SHORT"} and left_obs != right_obs:
        return "observation_direction_flips"
    if reward_delta < -0.20 and sensory_state.startswith("same_sensory_field"):
        return "same_sensory_field_direction_reward_weakens"
    if episode_delta < 0 and sensory_state == "same_sensory_field_but_less_lived_support":
        return "same_sensory_field_less_lived_direction_support"
    if left_best == right_best and left_best in {"LONG", "SHORT"} and sensory_state.startswith("same_sensory_field"):
        return "same_sensory_field_same_direction_but_reife_kippt"
    if right_best in {"-", "WAIT", "NONE"}:
        return "direction_support_not_visible_right"
    return "direction_support_reorganized"


def build_rows(
    *,
    alignment_rows: list[dict[str, str]],
    left_roots: list[Path],
    right_roots: list[Path],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    alignment_by_family = {
        str(row.get("symbol_family", "") or ""): row
        for row in alignment_rows
        if str(row.get("symbol_family", "") or "")
    }
    rows: list[dict[str, Any]] = []
    for family in _families_from_alignment(alignment_rows):
        left = _aggregate_family(left_roots, family)
        right = _aggregate_family(right_roots, family)
        align = alignment_by_family.get(family, {})
        row = {
            "direction_support_state": _direction_state(left, right, align),
            "symbol_family": family,
            "alignment_state": align.get("alignment_state", ""),
            "shift_state": align.get("shift_state", ""),
            "left_text_island_symbol": align.get("left_text_island_symbol", ""),
            "right_text_island_symbol": align.get("right_text_island_symbol", ""),
            "score_delta": align.get("score_delta", ""),
            "sensory_field_distance": align.get("sensory_field_distance", ""),
            "left_episode_count": left["episode_count"],
            "right_episode_count": right["episode_count"],
            "episode_count_delta": right["episode_count"] - left["episode_count"],
            "left_dominant_best_action": left["dominant_best_action"],
            "right_dominant_best_action": right["dominant_best_action"],
            "left_best_action_counts": left["best_action_counts"],
            "right_best_action_counts": right["best_action_counts"],
            "left_dominant_observation_action": left["dominant_observation_action"],
            "right_dominant_observation_action": right["dominant_observation_action"],
            "left_observation_action_counts": left["observation_action_counts"],
            "right_observation_action_counts": right["observation_action_counts"],
            "left_avg_best_reward_training": left["avg_best_reward_training"],
            "right_avg_best_reward_training": right["avg_best_reward_training"],
            "best_reward_training_delta": round(
                _safe_float(right["avg_best_reward_training"]) - _safe_float(left["avg_best_reward_training"]), 9
            ),
            "left_avg_close_reward": left["avg_close_reward"],
            "right_avg_close_reward": right["avg_close_reward"],
            "close_reward_delta": round(_safe_float(right["avg_close_reward"]) - _safe_float(left["avg_close_reward"]), 9),
            "left_avg_trade_readiness": left["avg_trade_readiness"],
            "right_avg_trade_readiness": right["avg_trade_readiness"],
            "trade_readiness_delta": round(
                _safe_float(right["avg_trade_readiness"]) - _safe_float(left["avg_trade_readiness"]), 9
            ),
            "left_world_labels": left["world_labels"],
            "right_world_labels": right["world_labels"],
            "left_temporal_state_counts": left["temporal_state_counts"],
            "right_temporal_state_counts": right["temporal_state_counts"],
            "left_neuro_tone_counts": left["neuro_tone_counts"],
            "right_neuro_tone_counts": right["neuro_tone_counts"],
            **PASSIVE_FLAGS,
        }
        rows.append(row)

    summary_map: dict[str, dict[str, Any]] = {}
    for row in rows:
        state = str(row["direction_support_state"])
        bucket = summary_map.setdefault(
            state,
            {
                "direction_support_state": state,
                "family_count": 0,
                "avg_episode_count_delta": 0.0,
                "avg_best_reward_training_delta": 0.0,
                "avg_trade_readiness_delta": 0.0,
                "families": [],
                **PASSIVE_FLAGS,
            },
        )
        count = int(bucket["family_count"])
        bucket["family_count"] = count + 1
        bucket["families"].append(str(row["symbol_family"]))
        for source_key, avg_key in [
            ("episode_count_delta", "avg_episode_count_delta"),
            ("best_reward_training_delta", "avg_best_reward_training_delta"),
            ("trade_readiness_delta", "avg_trade_readiness_delta"),
        ]:
            bucket[avg_key] = (
                (float(bucket[avg_key]) * count) + _safe_float(row.get(source_key))
            ) / max(1, count + 1)

    summary_rows: list[dict[str, Any]] = []
    for row in summary_map.values():
        for key in ["avg_episode_count_delta", "avg_best_reward_training_delta", "avg_trade_readiness_delta"]:
            row[key] = round(float(row[key]), 9)
        row["families"] = "|".join(sorted(row["families"])[:30])
        summary_rows.append(row)
    rows.sort(key=lambda item: (str(item["direction_support_state"]), str(item["symbol_family"])))
    summary_rows.sort(key=lambda item: (-int(item["family_count"]), str(item["direction_support_state"])))
    return rows, summary_rows


def _write_markdown(output_dir: Path, rows: list[dict[str, Any]], summary_rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Passive Direction Support Shift",
        "",
        "Dieser Bericht prueft, ob eine gekippte Syntax mit veraenderter Richtungsstuetzung zusammenhaengt.",
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
            "- {state}: families={count}, episode_delta={episodes}, "
            "best_reward_delta={reward}, trade_readiness_delta={readiness}, examples={families}".format(
                state=row["direction_support_state"],
                count=row["family_count"],
                episodes=row["avg_episode_count_delta"],
                reward=row["avg_best_reward_training_delta"],
                readiness=row["avg_trade_readiness_delta"],
                families=row["families"] or "-",
            )
        )
    lines.extend(["", "## Anker", ""])
    for row in rows[:90]:
        lines.append(
            "- {family}: {state}; best={left_best}->{right_best}; obs={left_obs}->{right_obs}; "
            "episodes={left_ep}->{right_ep}; best_reward_delta={reward}; align={align}".format(
                family=row["symbol_family"],
                state=row["direction_support_state"],
                left_best=row["left_dominant_best_action"],
                right_best=row["right_dominant_best_action"],
                left_obs=row["left_dominant_observation_action"],
                right_obs=row["right_dominant_observation_action"],
                left_ep=row["left_episode_count"],
                right_ep=row["right_episode_count"],
                reward=row["best_reward_training_delta"],
                align=row["alignment_state"],
            )
        )
    (output_dir / "passive_direction_support_shift.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs(output_dir: Path, rows: list[dict[str, Any]], summary_rows: list[dict[str, Any]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(
        output_dir / "passive_direction_support_shift.csv",
        rows,
        [
            "direction_support_state",
            "symbol_family",
            "alignment_state",
            "shift_state",
            "left_text_island_symbol",
            "right_text_island_symbol",
            "score_delta",
            "sensory_field_distance",
            "left_episode_count",
            "right_episode_count",
            "episode_count_delta",
            "left_dominant_best_action",
            "right_dominant_best_action",
            "left_dominant_observation_action",
            "right_dominant_observation_action",
            "left_avg_best_reward_training",
            "right_avg_best_reward_training",
            "best_reward_training_delta",
            "left_avg_trade_readiness",
            "right_avg_trade_readiness",
            "trade_readiness_delta",
        ],
    )
    _write_csv(
        output_dir / "passive_direction_support_shift_summary.csv",
        summary_rows,
        [
            "direction_support_state",
            "family_count",
            "avg_episode_count_delta",
            "avg_best_reward_training_delta",
            "avg_trade_readiness_delta",
            "families",
        ],
    )
    payload = {"rows": rows, "summary": summary_rows, "boundary": PASSIVE_FLAGS}
    (output_dir / "passive_direction_support_shift.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    _write_markdown(output_dir, rows, summary_rows)
    (output_dir / "passive_direction_support_shift.txt").write_text(
        "\n".join(
            f"{row['symbol_family']}: {row['direction_support_state']} "
            f"{row['left_dominant_best_action']}->{row['right_dominant_best_action']}"
            for row in rows
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive direction support shift")
    parser.add_argument("--alignment", type=Path, required=True)
    parser.add_argument("--left-debug-root", type=Path, action="append", required=True)
    parser.add_argument("--right-debug-root", type=Path, action="append", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    rows, summary_rows = build_rows(
        alignment_rows=_read_csv(args.alignment),
        left_roots=args.left_debug_root,
        right_roots=args.right_debug_root,
    )
    write_outputs(args.output_dir, rows, summary_rows)
    print(
        json.dumps(
            {
                "families": len(rows),
                "summary": {row["direction_support_state"]: row["family_count"] for row in summary_rows},
                **PASSIVE_FLAGS,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
