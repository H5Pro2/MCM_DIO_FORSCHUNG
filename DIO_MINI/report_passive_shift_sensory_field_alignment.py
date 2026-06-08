"""Join passive syntax-maturity shifts with sensory and MCM field context.

The report answers a narrow diagnostic question:

Does a surviving syntax/family keep a similar seen/heard/felt context, or does
it remain only as a raw name without a carried sensory-field relation?

This module is passive only. It reads diagnostic CSV files and writes reports.
Mini-DIO does not read the output for runtime, action, gates, entry, or
direction.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
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


SENSE_FIELDS = [
    "avg_sehen_form_flow",
    "avg_sehen_form_stability",
    "avg_sehen_form_change",
    "avg_hoeren_energy_tone",
    "avg_hoeren_energy_shift",
    "avg_fuehlen_mcm_coherence",
    "avg_fuehlen_mcm_tension",
    "avg_fuehlen_mcm_asymmetry",
    "avg_mini_recurrence_strength",
    "avg_mini_afterimage",
    "avg_mini_time_distance",
    "avg_mini_temporal_form_distance",
    "avg_mini_neuro_balance",
    "avg_reflection_context_alignment",
]


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


def _families(raw: Any) -> list[str]:
    return [item.strip() for item in str(raw or "").split("|") if item.strip()]


def _meaning_index(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {str(row.get("symbol_family", "") or ""): row for row in rows if row.get("symbol_family")}


def _vector(row: dict[str, str]) -> list[float]:
    return [_safe_float(row.get(field)) for field in SENSE_FIELDS]


def _distance(left: dict[str, str], right: dict[str, str]) -> float:
    if not left or not right:
        return 1.0
    lv = _vector(left)
    rv = _vector(right)
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(lv, rv)) / max(1, len(SENSE_FIELDS)))


def _mean(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def _alignment_state(row: dict[str, Any]) -> str:
    distance = _safe_float(row.get("sensory_field_distance"))
    right_episodes = _safe_int(row.get("right_episode_count"))
    left_episodes = _safe_int(row.get("left_episode_count"))
    right_mcm = _safe_float(row.get("right_avg_fuehlen_mcm_coherence"))
    mcm_delta = _safe_float(row.get("mcm_coherence_delta"))
    score_delta = _safe_float(row.get("score_delta"))

    if distance <= 0.08 and right_mcm >= 0.90 and score_delta < -0.08:
        if right_episodes < left_episodes:
            return "same_sensory_field_but_less_lived_support"
        return "same_sensory_field_but_reife_kippt"
    if distance <= 0.08:
        return "same_sensory_field_visible"
    if distance <= 0.18 and abs(mcm_delta) <= 0.08:
        return "near_mcm_field_with_sensory_variation"
    if distance > 0.18 and score_delta < -0.08:
        return "syntax_survives_but_context_changed"
    return "unclear_passive_alignment"


def _join_family(
    family: str,
    *,
    shift_row: dict[str, str],
    left_meaning: dict[str, dict[str, str]],
    right_meaning: dict[str, dict[str, str]],
) -> dict[str, Any]:
    left = left_meaning.get(family, {})
    right = right_meaning.get(family, {})
    row: dict[str, Any] = {
        "anchor_type": shift_row.get("anchor_type", ""),
        "anchor_symbol": shift_row.get("anchor_symbol", ""),
        "symbol_family": family,
        "shift_state": shift_row.get("shift_state", ""),
        "left_text_island_symbol": shift_row.get("left_text_island_symbol", ""),
        "right_text_island_symbol": shift_row.get("right_text_island_symbol", ""),
        "left_inner_map_state": shift_row.get("left_inner_map_state", ""),
        "right_inner_map_state": shift_row.get("right_inner_map_state", ""),
        "score_delta": round(_safe_float(shift_row.get("score_delta")), 9),
        "left_family_seen": 1 if left else 0,
        "right_family_seen": 1 if right else 0,
        "left_episode_count": _safe_int(left.get("episode_count")),
        "right_episode_count": _safe_int(right.get("episode_count")),
        "episode_count_delta": _safe_int(right.get("episode_count")) - _safe_int(left.get("episode_count")),
        "left_dominant_neuro_tone": left.get("dominant_neuro_tone", ""),
        "right_dominant_neuro_tone": right.get("dominant_neuro_tone", ""),
        "left_dominant_temporal_state": left.get("dominant_temporal_state", ""),
        "right_dominant_temporal_state": right.get("dominant_temporal_state", ""),
        "sensory_field_distance": round(_distance(left, right), 9),
        "left_avg_sehen_form_flow": round(_safe_float(left.get("avg_sehen_form_flow")), 9),
        "right_avg_sehen_form_flow": round(_safe_float(right.get("avg_sehen_form_flow")), 9),
        "sehen_flow_delta": round(
            _safe_float(right.get("avg_sehen_form_flow")) - _safe_float(left.get("avg_sehen_form_flow")),
            9,
        ),
        "left_avg_hoeren_energy_tone": round(_safe_float(left.get("avg_hoeren_energy_tone")), 9),
        "right_avg_hoeren_energy_tone": round(_safe_float(right.get("avg_hoeren_energy_tone")), 9),
        "hoeren_energy_delta": round(
            _safe_float(right.get("avg_hoeren_energy_tone")) - _safe_float(left.get("avg_hoeren_energy_tone")),
            9,
        ),
        "left_avg_fuehlen_mcm_coherence": round(_safe_float(left.get("avg_fuehlen_mcm_coherence")), 9),
        "right_avg_fuehlen_mcm_coherence": round(_safe_float(right.get("avg_fuehlen_mcm_coherence")), 9),
        "mcm_coherence_delta": round(
            _safe_float(right.get("avg_fuehlen_mcm_coherence"))
            - _safe_float(left.get("avg_fuehlen_mcm_coherence")),
            9,
        ),
        "left_avg_fuehlen_mcm_tension": round(_safe_float(left.get("avg_fuehlen_mcm_tension")), 9),
        "right_avg_fuehlen_mcm_tension": round(_safe_float(right.get("avg_fuehlen_mcm_tension")), 9),
        "mcm_tension_delta": round(
            _safe_float(right.get("avg_fuehlen_mcm_tension")) - _safe_float(left.get("avg_fuehlen_mcm_tension")),
            9,
        ),
        "left_avg_fuehlen_mcm_asymmetry": round(_safe_float(left.get("avg_fuehlen_mcm_asymmetry")), 9),
        "right_avg_fuehlen_mcm_asymmetry": round(_safe_float(right.get("avg_fuehlen_mcm_asymmetry")), 9),
        "mcm_asymmetry_delta": round(
            _safe_float(right.get("avg_fuehlen_mcm_asymmetry"))
            - _safe_float(left.get("avg_fuehlen_mcm_asymmetry")),
            9,
        ),
        **PASSIVE_FLAGS,
    }
    row["alignment_state"] = _alignment_state(row)
    return row


def build_rows(
    *,
    shift_rows: list[dict[str, str]],
    left_meaning_rows: list[dict[str, str]],
    right_meaning_rows: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    left_meaning = _meaning_index(left_meaning_rows)
    right_meaning = _meaning_index(right_meaning_rows)
    rows: list[dict[str, Any]] = []
    seen_keys: set[tuple[str, str, str]] = set()
    for shift_row in shift_rows:
        families = _families(shift_row.get("shared_families"))
        if not families:
            families = _families(shift_row.get("left_families"))
        for family in families:
            key = (str(shift_row.get("anchor_type")), str(shift_row.get("anchor_symbol")), family)
            if key in seen_keys:
                continue
            rows.append(
                _join_family(
                    family,
                    shift_row=shift_row,
                    left_meaning=left_meaning,
                    right_meaning=right_meaning,
                )
            )
            seen_keys.add(key)

    summary_map: dict[str, dict[str, Any]] = {}
    for row in rows:
        state = str(row["alignment_state"])
        bucket = summary_map.setdefault(
            state,
            {
                "alignment_state": state,
                "family_count": 0,
                "avg_sensory_field_distance": 0.0,
                "avg_score_delta": 0.0,
                "avg_episode_count_delta": 0.0,
                "avg_mcm_coherence_delta": 0.0,
                **PASSIVE_FLAGS,
            },
        )
        count = int(bucket["family_count"])
        bucket["family_count"] = count + 1
        for source_key, avg_key in [
            ("sensory_field_distance", "avg_sensory_field_distance"),
            ("score_delta", "avg_score_delta"),
            ("episode_count_delta", "avg_episode_count_delta"),
            ("mcm_coherence_delta", "avg_mcm_coherence_delta"),
        ]:
            bucket[avg_key] = (
                (float(bucket[avg_key]) * count) + _safe_float(row.get(source_key))
            ) / max(1, count + 1)

    summary_rows = []
    for row in summary_map.values():
        for key in [
            "avg_sensory_field_distance",
            "avg_score_delta",
            "avg_episode_count_delta",
            "avg_mcm_coherence_delta",
        ]:
            row[key] = round(float(row[key]), 9)
        summary_rows.append(row)

    rows.sort(key=lambda item: (str(item["alignment_state"]), str(item["symbol_family"])))
    summary_rows.sort(key=lambda item: (-int(item["family_count"]), str(item["alignment_state"])))
    return rows, summary_rows


def _write_markdown(output_dir: Path, rows: list[dict[str, Any]], summary_rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Passive Shift Sensory-Field Alignment",
        "",
        "Dieser Bericht koppelt Reife-Kippungen an Sehen, Hoeren und Fuehlen.",
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
            "- {state}: families={count}, dist={dist}, score_delta={score}, "
            "episode_delta={episodes}, mcm_delta={mcm}".format(
                state=row["alignment_state"],
                count=row["family_count"],
                dist=row["avg_sensory_field_distance"],
                score=row["avg_score_delta"],
                episodes=row["avg_episode_count_delta"],
                mcm=row["avg_mcm_coherence_delta"],
            )
        )
    lines.extend(["", "## Anker", ""])
    for row in rows[:80]:
        lines.append(
            "- {family}: {state}; text={left_text}->{right_text}; "
            "episodes={left_ep}->{right_ep}; dist={dist}; mcm={left_mcm}->{right_mcm}; "
            "score_delta={score}".format(
                family=row["symbol_family"],
                state=row["alignment_state"],
                left_text=row["left_text_island_symbol"],
                right_text=row["right_text_island_symbol"],
                left_ep=row["left_episode_count"],
                right_ep=row["right_episode_count"],
                dist=row["sensory_field_distance"],
                left_mcm=row["left_avg_fuehlen_mcm_coherence"],
                right_mcm=row["right_avg_fuehlen_mcm_coherence"],
                score=row["score_delta"],
            )
        )
    (output_dir / "passive_shift_sensory_field_alignment.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def write_outputs(
    *,
    output_dir: Path,
    rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    metadata: dict[str, str],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(
        output_dir / "passive_shift_sensory_field_alignment.csv",
        rows,
        [
            "alignment_state",
            "anchor_type",
            "anchor_symbol",
            "symbol_family",
            "shift_state",
            "left_text_island_symbol",
            "right_text_island_symbol",
            "left_inner_map_state",
            "right_inner_map_state",
            "score_delta",
            "left_episode_count",
            "right_episode_count",
            "episode_count_delta",
            "sensory_field_distance",
            "left_avg_sehen_form_flow",
            "right_avg_sehen_form_flow",
            "sehen_flow_delta",
            "left_avg_hoeren_energy_tone",
            "right_avg_hoeren_energy_tone",
            "hoeren_energy_delta",
            "left_avg_fuehlen_mcm_coherence",
            "right_avg_fuehlen_mcm_coherence",
            "mcm_coherence_delta",
        ],
    )
    _write_csv(
        output_dir / "passive_shift_sensory_field_alignment_summary.csv",
        summary_rows,
        [
            "alignment_state",
            "family_count",
            "avg_sensory_field_distance",
            "avg_score_delta",
            "avg_episode_count_delta",
            "avg_mcm_coherence_delta",
        ],
    )
    payload = {"metadata": metadata, "rows": rows, "summary": summary_rows, "boundary": PASSIVE_FLAGS}
    (output_dir / "passive_shift_sensory_field_alignment.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    _write_markdown(output_dir, rows, summary_rows)
    (output_dir / "passive_shift_sensory_field_alignment.txt").write_text(
        "\n".join(
            f"{row['symbol_family']}: {row['alignment_state']} "
            f"dist={row['sensory_field_distance']} score_delta={row['score_delta']}"
            for row in rows
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive shift sensory-field alignment")
    parser.add_argument("--shift", type=Path, required=True)
    parser.add_argument("--left-meaning-space", type=Path, required=True)
    parser.add_argument("--right-meaning-space", type=Path, required=True)
    parser.add_argument("--left-label", default="LEFT")
    parser.add_argument("--right-label", default="RIGHT")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    rows, summary_rows = build_rows(
        shift_rows=_read_csv(args.shift),
        left_meaning_rows=_read_csv(args.left_meaning_space),
        right_meaning_rows=_read_csv(args.right_meaning_space),
    )
    metadata = {
        "shift": str(args.shift),
        "left_meaning_space": str(args.left_meaning_space),
        "right_meaning_space": str(args.right_meaning_space),
        "left_label": args.left_label,
        "right_label": args.right_label,
    }
    write_outputs(output_dir=args.output_dir, rows=rows, summary_rows=summary_rows, metadata=metadata)
    print(
        json.dumps(
            {
                "families": len(rows),
                "summary": {row["alignment_state"]: row["family_count"] for row in summary_rows},
                **PASSIVE_FLAGS,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
