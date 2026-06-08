"""Compare carried and immediately kipping situational traces.

This passive report contrasts trace families that remain carried with families
that kip immediately or continuously. It joins carry curve, sensory/field
alignment, direction support, and temporal detail diagnostics.

Passive only. No runtime memory writes, no action, no gate, no entry, no
direction signal.
"""

from __future__ import annotations

import argparse
import csv
import json
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


def _index(rows: list[dict[str, str]], key: str = "symbol_family") -> dict[str, dict[str, str]]:
    return {str(row.get(key, "") or ""): row for row in rows if str(row.get(key, "") or "")}


def _contrast_group(carry_row: dict[str, str]) -> str:
    state = str(carry_row.get("trace_carry_state", "") or "")
    visible = _safe_float(carry_row.get("visible_probe_count"))
    if state == "trace_fully_carried" and visible >= 2:
        return "multi_probe_carried_trace"
    if state == "trace_fully_carried":
        return "single_probe_carried_trace"
    if state == "trace_immediate_or_continuous_kipp":
        return "immediate_or_continuous_kipp_trace"
    if state == "trace_carries_then_kipps":
        return "carries_then_kipps_trace"
    if state == "trace_kipps_then_recarries":
        return "kipps_then_recarries_trace"
    return "mixed_or_unclear_trace"


def _temporal_aggregate(rows: list[dict[str, str]]) -> dict[str, Any]:
    states = Counter(str(row.get("probe_kipp_state", "") or "") for row in rows)
    count = len(rows)
    return {
        "temporal_detail_count": count,
        "avg_episode_count_delta": round(
            sum(_safe_float(row.get("episode_count_delta")) for row in rows) / max(1, count), 9
        ),
        "avg_trade_readiness_delta": round(
            sum(_safe_float(row.get("trade_readiness_delta")) for row in rows) / max(1, count), 9
        ),
        "avg_best_reward_training_delta": round(
            sum(_safe_float(row.get("best_reward_training_delta")) for row in rows) / max(1, count), 9
        ),
        "lived_support_drop_count": states.get("probe_lived_support_drop", 0),
        "direction_flip_count": states.get("probe_direction_flip", 0),
        "best_reward_softens_count": states.get("probe_best_reward_softens", 0),
        "trade_readiness_softens_count": states.get("probe_trade_readiness_softens", 0),
        "neuro_tone_reorganizes_count": states.get("probe_neuro_tone_reorganizes", 0),
        "no_visible_kipp_count": states.get("probe_no_visible_kipp", 0),
        "temporal_state_counts": "|".join(f"{key}:{value}" for key, value in sorted(states.items())),
    }


def build_rows(
    *,
    carry_rows: list[dict[str, str]],
    alignment_rows: list[dict[str, str]],
    direction_rows: list[dict[str, str]],
    temporal_detail_rows: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    alignment = _index(alignment_rows)
    direction = _index(direction_rows)
    temporal_by_family: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in temporal_detail_rows:
        temporal_by_family[str(row.get("symbol_family", "") or "")].append(row)

    family_rows: list[dict[str, Any]] = []
    for carry in carry_rows:
        family = str(carry.get("symbol_family", "") or "")
        if not family:
            continue
        align = alignment.get(family, {})
        direct = direction.get(family, {})
        temporal = _temporal_aggregate(temporal_by_family.get(family, []))
        family_rows.append(
            {
                "contrast_group": _contrast_group(carry),
                "symbol_family": family,
                "trace_carry_state": carry.get("trace_carry_state", ""),
                "visible_probe_count": carry.get("visible_probe_count", ""),
                "carried_probe_count": carry.get("carried_probe_count", ""),
                "kipp_probe_count": carry.get("kipp_probe_count", ""),
                "carry_ratio": carry.get("carry_ratio", ""),
                "first_kipp_probe": carry.get("first_kipp_probe", ""),
                "first_kipp_state": carry.get("first_kipp_state", ""),
                "longest_carried_run": carry.get("longest_carried_run", ""),
                "longest_kipp_run": carry.get("longest_kipp_run", ""),
                "dominant_kipp_state": carry.get("dominant_kipp_state", ""),
                "alignment_state": align.get("alignment_state", carry.get("alignment_state", "")),
                "sensory_field_distance": align.get("sensory_field_distance", ""),
                "sehen_flow_delta": align.get("sehen_flow_delta", ""),
                "hoeren_energy_delta": align.get("hoeren_energy_delta", ""),
                "mcm_coherence_delta": align.get("mcm_coherence_delta", ""),
                "mcm_tension_delta": align.get("mcm_tension_delta", ""),
                "mcm_asymmetry_delta": align.get("mcm_asymmetry_delta", ""),
                "direction_support_state": direct.get("direction_support_state", carry.get("direction_support_state", "")),
                "left_dominant_best_action": direct.get("left_dominant_best_action", ""),
                "right_dominant_best_action": direct.get("right_dominant_best_action", ""),
                "best_reward_training_delta": direct.get("best_reward_training_delta", ""),
                "trade_readiness_delta": direct.get("trade_readiness_delta", ""),
                "left_text_island_symbol": carry.get("left_text_island_symbol", ""),
                "right_text_island_symbol": carry.get("right_text_island_symbol", ""),
                "score_delta": carry.get("score_delta", ""),
                **temporal,
                **PASSIVE_FLAGS,
            }
        )

    summary_map: dict[str, dict[str, Any]] = {}
    numeric_fields = [
        "visible_probe_count",
        "carried_probe_count",
        "carry_ratio",
        "sensory_field_distance",
        "sehen_flow_delta",
        "hoeren_energy_delta",
        "mcm_coherence_delta",
        "mcm_tension_delta",
        "mcm_asymmetry_delta",
        "best_reward_training_delta",
        "trade_readiness_delta",
        "avg_episode_count_delta",
        "avg_trade_readiness_delta",
        "avg_best_reward_training_delta",
        "lived_support_drop_count",
        "direction_flip_count",
        "neuro_tone_reorganizes_count",
        "no_visible_kipp_count",
    ]
    for row in family_rows:
        group = str(row["contrast_group"])
        bucket = summary_map.setdefault(
            group,
            {
                "contrast_group": group,
                "family_count": 0,
                "families": [],
                **{f"avg_{field}": 0.0 for field in numeric_fields},
                **PASSIVE_FLAGS,
            },
        )
        count = int(bucket["family_count"])
        bucket["family_count"] = count + 1
        bucket["families"].append(str(row["symbol_family"]))
        for field in numeric_fields:
            avg_key = f"avg_{field}"
            bucket[avg_key] = ((float(bucket[avg_key]) * count) + _safe_float(row.get(field))) / max(1, count + 1)

    summary_rows: list[dict[str, Any]] = []
    for row in summary_map.values():
        for key in list(row):
            if key.startswith("avg_"):
                row[key] = round(float(row[key]), 9)
        row["families"] = "|".join(sorted(row["families"])[:40])
        summary_rows.append(row)

    family_rows.sort(key=lambda row: (str(row["contrast_group"]), str(row["symbol_family"])))
    summary_rows.sort(key=lambda row: (-int(row["family_count"]), str(row["contrast_group"])))
    return family_rows, summary_rows


def _write_markdown(output_dir: Path, family_rows: list[dict[str, Any]], summary_rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Passive Carry Contrast",
        "",
        "Dieser Bericht vergleicht getragene und sofort kippende situative Spuren.",
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
        "## Gruppen",
        "",
    ]
    for row in summary_rows:
        lines.append(
            "- {group}: families={count}, avg_carry={carry}, avg_visible={visible}, "
            "avg_distance={distance}, avg_mcm_delta={mcm}, avg_support_drop={support}, examples={families}".format(
                group=row["contrast_group"],
                count=row["family_count"],
                carry=row["avg_carry_ratio"],
                visible=row["avg_visible_probe_count"],
                distance=row["avg_sensory_field_distance"],
                mcm=row["avg_mcm_coherence_delta"],
                support=row["avg_lived_support_drop_count"],
                families=row["families"] or "-",
            )
        )
    lines.extend(["", "## Familien", ""])
    for row in family_rows[:100]:
        lines.append(
            "- {family}: {group}; carry={carry}; visible={visible}; dist={dist}; "
            "mcm_delta={mcm}; support_drop={support}; text={left}->{right}".format(
                family=row["symbol_family"],
                group=row["contrast_group"],
                carry=row["carry_ratio"],
                visible=row["visible_probe_count"],
                dist=row["sensory_field_distance"],
                mcm=row["mcm_coherence_delta"],
                support=row["lived_support_drop_count"],
                left=row["left_text_island_symbol"],
                right=row["right_text_island_symbol"],
            )
        )
    (output_dir / "passive_carry_contrast.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs(output_dir: Path, family_rows: list[dict[str, Any]], summary_rows: list[dict[str, Any]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(
        output_dir / "passive_carry_contrast_families.csv",
        family_rows,
        [
            "contrast_group",
            "symbol_family",
            "trace_carry_state",
            "visible_probe_count",
            "carried_probe_count",
            "kipp_probe_count",
            "carry_ratio",
            "sensory_field_distance",
            "sehen_flow_delta",
            "hoeren_energy_delta",
            "mcm_coherence_delta",
            "mcm_tension_delta",
            "mcm_asymmetry_delta",
            "direction_support_state",
            "left_dominant_best_action",
            "right_dominant_best_action",
            "best_reward_training_delta",
            "trade_readiness_delta",
            "avg_episode_count_delta",
            "avg_trade_readiness_delta",
            "lived_support_drop_count",
            "direction_flip_count",
            "neuro_tone_reorganizes_count",
            "no_visible_kipp_count",
            "left_text_island_symbol",
            "right_text_island_symbol",
        ],
    )
    _write_csv(
        output_dir / "passive_carry_contrast_summary.csv",
        summary_rows,
        [
            "contrast_group",
            "family_count",
            "avg_visible_probe_count",
            "avg_carried_probe_count",
            "avg_carry_ratio",
            "avg_sensory_field_distance",
            "avg_mcm_coherence_delta",
            "avg_mcm_tension_delta",
            "avg_mcm_asymmetry_delta",
            "avg_best_reward_training_delta",
            "avg_trade_readiness_delta",
            "avg_lived_support_drop_count",
            "avg_direction_flip_count",
            "avg_neuro_tone_reorganizes_count",
            "avg_no_visible_kipp_count",
            "families",
        ],
    )
    payload = {"families": family_rows, "summary": summary_rows, "boundary": PASSIVE_FLAGS}
    (output_dir / "passive_carry_contrast.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    _write_markdown(output_dir, family_rows, summary_rows)
    (output_dir / "passive_carry_contrast.txt").write_text(
        "\n".join(f"{row['symbol_family']}: {row['contrast_group']}" for row in family_rows) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive carry contrast")
    parser.add_argument("--carry-families", type=Path, required=True)
    parser.add_argument("--alignment", type=Path, required=True)
    parser.add_argument("--direction", type=Path, required=True)
    parser.add_argument("--temporal-detail", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    family_rows, summary_rows = build_rows(
        carry_rows=_read_csv(args.carry_families),
        alignment_rows=_read_csv(args.alignment),
        direction_rows=_read_csv(args.direction),
        temporal_detail_rows=_read_csv(args.temporal_detail),
    )
    write_outputs(args.output_dir, family_rows, summary_rows)
    print(
        json.dumps(
            {
                "families": len(family_rows),
                "summary": {row["contrast_group"]: row["family_count"] for row in summary_rows},
                **PASSIVE_FLAGS,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
