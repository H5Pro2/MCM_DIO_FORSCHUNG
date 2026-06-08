"""Mark passive temporal kipp points for situational emergent traces.

The report compares selected Mini-DIO families across matching controlled
probe worlds. It marks where a surviving syntax/family first loses carried
support: direction flips, lived episode support drops, hypothetical world
reward weakens, readiness softens, or neuro/temporal state reorganizes.

Passive only. The output is not read by Mini-DIO for runtime, action, gates,
entry, or direction.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
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


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        result = float(value if value not in (None, "") else default)
    except (TypeError, ValueError):
        return default
    if result != result:
        return default
    return result


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


def _probe_key(*values: Any) -> str:
    for value in values:
        match = re.search(r"probe(\d+)", str(value or ""))
        if match:
            return f"probe{match.group(1)}"
    return "probe_unknown"


def _dominant(counter: Counter[str]) -> str:
    if not counter:
        return "-"
    return counter.most_common(1)[0][0]


def _counter_text(counter: Counter[str]) -> str:
    return "|".join(f"{key}:{value}" for key, value in sorted(counter.items()))


def _avg(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def _families_from_direction(rows: list[dict[str, str]]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for row in rows:
        family = str(row.get("symbol_family", "") or "").strip()
        if family and family not in seen:
            result.append(family)
            seen.add(family)
    return result


def _collect_probe_rows(roots: list[Path], families: set[str]) -> dict[str, dict[str, list[dict[str, str]]]]:
    collected: dict[str, dict[str, list[dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for root in roots:
        for path in _episode_files(root):
            with path.open("r", newline="", encoding="utf-8") as handle:
                for row in csv.DictReader(handle):
                    family = str(row.get("symbol_family", "") or "")
                    if family not in families:
                        continue
                    probe = _probe_key(row.get("passive_world_label"), path)
                    collected[family][probe].append(dict(row))
    return collected


def _aggregate(rows: list[dict[str, str]]) -> dict[str, Any]:
    best = Counter(str(row.get("best_action_training", "") or "-") for row in rows)
    obs = Counter(str(row.get("observation_learning_action", "") or "-") for row in rows)
    action = Counter(str(row.get("action", "") or "-") for row in rows)
    neuro = Counter(str(row.get("mini_neuro_dominant_tone", "") or "-") for row in rows)
    temporal = Counter(str(row.get("mini_temporal_state", "") or "-") for row in rows)
    return {
        "episode_count": len(rows),
        "dominant_action": _dominant(action),
        "action_counts": _counter_text(action),
        "dominant_best_action": _dominant(best),
        "best_action_counts": _counter_text(best),
        "dominant_observation_action": _dominant(obs),
        "observation_action_counts": _counter_text(obs),
        "dominant_neuro_tone": _dominant(neuro),
        "neuro_tone_counts": _counter_text(neuro),
        "dominant_temporal_state": _dominant(temporal),
        "temporal_state_counts": _counter_text(temporal),
        "avg_best_reward_training": round(_avg([_safe_float(row.get("best_reward_training")) for row in rows]), 9),
        "avg_trade_readiness": round(_avg([_safe_float(row.get("trade_readiness")) for row in rows]), 9),
        "avg_observation_learning_pressure": round(
            _avg([_safe_float(row.get("observation_learning_pressure")) for row in rows]), 9
        ),
        "avg_fuehlen_mcm_coherence": round(_avg([_safe_float(row.get("fuehlen_mcm_coherence")) for row in rows]), 9),
        "avg_sehen_form_flow": round(_avg([_safe_float(row.get("sehen_form_flow")) for row in rows]), 9),
        "avg_hoeren_energy_tone": round(_avg([_safe_float(row.get("hoeren_energy_tone")) for row in rows]), 9),
    }


def _probe_kipp_state(left: dict[str, Any], right: dict[str, Any]) -> str:
    left_best = str(left.get("dominant_best_action", "-"))
    right_best = str(right.get("dominant_best_action", "-"))
    left_obs = str(left.get("dominant_observation_action", "-"))
    right_obs = str(right.get("dominant_observation_action", "-"))
    if left_best in {"LONG", "SHORT"} and right_best in {"LONG", "SHORT"} and left_best != right_best:
        return "probe_direction_flip"
    if left_obs in {"LONG", "SHORT"} and right_obs in {"LONG", "SHORT"} and left_obs != right_obs:
        return "probe_observation_direction_flip"
    if int(right.get("episode_count", 0)) < int(left.get("episode_count", 0)):
        return "probe_lived_support_drop"
    if _safe_float(right.get("avg_best_reward_training")) < _safe_float(left.get("avg_best_reward_training")):
        return "probe_best_reward_softens"
    if _safe_float(right.get("avg_trade_readiness")) < _safe_float(left.get("avg_trade_readiness")):
        return "probe_trade_readiness_softens"
    if str(right.get("dominant_neuro_tone", "-")) != str(left.get("dominant_neuro_tone", "-")):
        return "probe_neuro_tone_reorganizes"
    if str(right.get("dominant_temporal_state", "-")) != str(left.get("dominant_temporal_state", "-")):
        return "probe_temporal_state_reorganizes"
    return "probe_no_visible_kipp"


def _family_kipp_state(probe_states: list[str]) -> str:
    if not probe_states:
        return "family_not_visible_in_probe_trace"
    if any(state == "probe_direction_flip" for state in probe_states):
        return "family_has_direction_flip"
    if any(state == "probe_observation_direction_flip" for state in probe_states):
        return "family_has_observation_direction_flip"
    if any(state == "probe_lived_support_drop" for state in probe_states):
        return "family_loses_lived_support"
    if any(state == "probe_best_reward_softens" for state in probe_states):
        return "family_best_reward_softens"
    if any(state == "probe_trade_readiness_softens" for state in probe_states):
        return "family_trade_readiness_softens"
    if any(state in {"probe_neuro_tone_reorganizes", "probe_temporal_state_reorganizes"} for state in probe_states):
        return "family_neuro_temporal_reorganizes"
    return "family_no_visible_temporal_kipp"


def build_rows(
    *,
    direction_rows: list[dict[str, str]],
    left_roots: list[Path],
    right_roots: list[Path],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    direction_by_family = {str(row.get("symbol_family", "") or ""): row for row in direction_rows}
    families = set(_families_from_direction(direction_rows))
    left = _collect_probe_rows(left_roots, families)
    right = _collect_probe_rows(right_roots, families)
    detail_rows: list[dict[str, Any]] = []
    family_rows: list[dict[str, Any]] = []

    for family in sorted(families):
        probes = sorted(set(left.get(family, {})) | set(right.get(family, {})))
        states: list[str] = []
        first_kipp_probe = ""
        first_kipp_state = ""
        for probe in probes:
            left_agg = _aggregate(left.get(family, {}).get(probe, []))
            right_agg = _aggregate(right.get(family, {}).get(probe, []))
            state = _probe_kipp_state(left_agg, right_agg)
            states.append(state)
            if not first_kipp_probe and state != "probe_no_visible_kipp":
                first_kipp_probe = probe
                first_kipp_state = state
            detail_rows.append(
                {
                    "symbol_family": family,
                    "probe": probe,
                    "probe_kipp_state": state,
                    "left_episode_count": left_agg["episode_count"],
                    "right_episode_count": right_agg["episode_count"],
                    "episode_count_delta": right_agg["episode_count"] - left_agg["episode_count"],
                    "left_dominant_best_action": left_agg["dominant_best_action"],
                    "right_dominant_best_action": right_agg["dominant_best_action"],
                    "left_dominant_observation_action": left_agg["dominant_observation_action"],
                    "right_dominant_observation_action": right_agg["dominant_observation_action"],
                    "left_avg_best_reward_training": left_agg["avg_best_reward_training"],
                    "right_avg_best_reward_training": right_agg["avg_best_reward_training"],
                    "best_reward_training_delta": round(
                        _safe_float(right_agg["avg_best_reward_training"])
                        - _safe_float(left_agg["avg_best_reward_training"]),
                        9,
                    ),
                    "left_avg_trade_readiness": left_agg["avg_trade_readiness"],
                    "right_avg_trade_readiness": right_agg["avg_trade_readiness"],
                    "trade_readiness_delta": round(
                        _safe_float(right_agg["avg_trade_readiness"]) - _safe_float(left_agg["avg_trade_readiness"]),
                        9,
                    ),
                    "left_dominant_neuro_tone": left_agg["dominant_neuro_tone"],
                    "right_dominant_neuro_tone": right_agg["dominant_neuro_tone"],
                    "left_dominant_temporal_state": left_agg["dominant_temporal_state"],
                    "right_dominant_temporal_state": right_agg["dominant_temporal_state"],
                    "left_avg_fuehlen_mcm_coherence": left_agg["avg_fuehlen_mcm_coherence"],
                    "right_avg_fuehlen_mcm_coherence": right_agg["avg_fuehlen_mcm_coherence"],
                    **PASSIVE_FLAGS,
                }
            )
        direction = direction_by_family.get(family, {})
        family_rows.append(
            {
                "symbol_family": family,
                "family_temporal_kipp_state": _family_kipp_state(states),
                "first_kipp_probe": first_kipp_probe or "-",
                "first_kipp_state": first_kipp_state or "probe_no_visible_kipp",
                "probe_state_path": " -> ".join(states),
                "direction_support_state": direction.get("direction_support_state", ""),
                "alignment_state": direction.get("alignment_state", ""),
                "left_text_island_symbol": direction.get("left_text_island_symbol", ""),
                "right_text_island_symbol": direction.get("right_text_island_symbol", ""),
                "score_delta": direction.get("score_delta", ""),
                **PASSIVE_FLAGS,
            }
        )

    summary_map: dict[str, dict[str, Any]] = {}
    for row in family_rows:
        state = str(row["family_temporal_kipp_state"])
        bucket = summary_map.setdefault(
            state,
            {
                "family_temporal_kipp_state": state,
                "family_count": 0,
                "families": [],
                **PASSIVE_FLAGS,
            },
        )
        bucket["family_count"] += 1
        bucket["families"].append(str(row["symbol_family"]))
    summary_rows: list[dict[str, Any]] = []
    for row in summary_map.values():
        row["families"] = "|".join(sorted(row["families"])[:40])
        summary_rows.append(row)

    family_rows.sort(key=lambda row: (str(row["family_temporal_kipp_state"]), str(row["symbol_family"])))
    detail_rows.sort(key=lambda row: (str(row["symbol_family"]), str(row["probe"])))
    summary_rows.sort(key=lambda row: (-int(row["family_count"]), str(row["family_temporal_kipp_state"])))
    return detail_rows, family_rows, summary_rows


def _write_markdown(output_dir: Path, family_rows: list[dict[str, Any]], summary_rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Passive Temporal Kipp Points",
        "",
        "Dieser Bericht markiert zeitliche Kipp-Punkte situativer emergenter Spuren.",
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
            f"- {row['family_temporal_kipp_state']}: families={row['family_count']}; examples={row['families'] or '-'}"
        )
    lines.extend(["", "## Familien", ""])
    for row in family_rows[:100]:
        lines.append(
            "- {family}: {state}; first={probe}/{first}; direction={direction}; alignment={alignment}; "
            "text={left_text}->{right_text}".format(
                family=row["symbol_family"],
                state=row["family_temporal_kipp_state"],
                probe=row["first_kipp_probe"],
                first=row["first_kipp_state"],
                direction=row["direction_support_state"],
                alignment=row["alignment_state"],
                left_text=row["left_text_island_symbol"],
                right_text=row["right_text_island_symbol"],
            )
        )
    (output_dir / "passive_temporal_kipp_points.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs(
    output_dir: Path,
    detail_rows: list[dict[str, Any]],
    family_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(
        output_dir / "passive_temporal_kipp_points_detail.csv",
        detail_rows,
        [
            "symbol_family",
            "probe",
            "probe_kipp_state",
            "left_episode_count",
            "right_episode_count",
            "episode_count_delta",
            "left_dominant_best_action",
            "right_dominant_best_action",
            "left_dominant_observation_action",
            "right_dominant_observation_action",
            "best_reward_training_delta",
            "trade_readiness_delta",
            "left_dominant_neuro_tone",
            "right_dominant_neuro_tone",
            "left_dominant_temporal_state",
            "right_dominant_temporal_state",
        ],
    )
    _write_csv(
        output_dir / "passive_temporal_kipp_points_families.csv",
        family_rows,
        [
            "symbol_family",
            "family_temporal_kipp_state",
            "first_kipp_probe",
            "first_kipp_state",
            "probe_state_path",
            "direction_support_state",
            "alignment_state",
            "left_text_island_symbol",
            "right_text_island_symbol",
            "score_delta",
        ],
    )
    _write_csv(
        output_dir / "passive_temporal_kipp_points_summary.csv",
        summary_rows,
        ["family_temporal_kipp_state", "family_count", "families"],
    )
    payload = {"detail": detail_rows, "families": family_rows, "summary": summary_rows, "boundary": PASSIVE_FLAGS}
    (output_dir / "passive_temporal_kipp_points.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    _write_markdown(output_dir, family_rows, summary_rows)
    (output_dir / "passive_temporal_kipp_points.txt").write_text(
        "\n".join(
            f"{row['symbol_family']}: {row['family_temporal_kipp_state']} at {row['first_kipp_probe']}"
            for row in family_rows
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive temporal kipp points")
    parser.add_argument("--direction", type=Path, required=True)
    parser.add_argument("--left-debug-root", type=Path, action="append", required=True)
    parser.add_argument("--right-debug-root", type=Path, action="append", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    detail_rows, family_rows, summary_rows = build_rows(
        direction_rows=_read_csv(args.direction),
        left_roots=args.left_debug_root,
        right_roots=args.right_debug_root,
    )
    write_outputs(args.output_dir, detail_rows, family_rows, summary_rows)
    print(
        json.dumps(
            {
                "families": len(family_rows),
                "detail_rows": len(detail_rows),
                "summary": {row["family_temporal_kipp_state"]: row["family_count"] for row in summary_rows},
                **PASSIVE_FLAGS,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
