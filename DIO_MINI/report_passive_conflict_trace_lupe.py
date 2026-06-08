"""Passive conflict trace magnifier for DIO_MINI.

This report reads the passive inner-coherence transfer detail and follows
families that had negative real contact across all available worlds. It is
diagnosis only: no memory write, no motor output, no gate.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


SENSOR_FIELDS = [
    "avg_sehen_form_flow",
    "avg_sehen_form_stability",
    "avg_hoeren_energy_tone",
    "avg_fuehlen_mcm_coherence",
    "avg_fuehlen_mcm_tension",
]


WORLD_ORDER = {
    "probe17_first": 10,
    "probe17_repeat": 20,
    "probe18_first": 30,
    "probe18_repeat1": 40,
    "probe18_repeat2": 50,
}


def _safe_float(value: object) -> float:
    try:
        return float(value or 0.0)
    except Exception:
        return 0.0


def _safe_int(value: object) -> int:
    try:
        return int(float(value or 0))
    except Exception:
        return 0


def _world_sort_key(row: dict) -> tuple[int, str, str]:
    world = str(row.get("world", "") or "")
    return (WORLD_ORDER.get(world, 999), world, str(row.get("symbol_family", "") or ""))


def _read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _role_for(row: dict) -> str:
    contact = str(row.get("contact_quality", "") or "")
    reward = _safe_float(row.get("reward_sum"))
    if contact == "negative_real_contact" or reward < 0.0:
        return "conflict"
    if contact == "positive_real_contact" and reward > 0.0:
        return "carried_positive"
    if contact == "observed_potential":
        return "observed_potential"
    return "other"


def _weighted_average(rows: list[dict], field: str) -> float:
    total_count = 0
    total_value = 0.0
    for row in rows:
        count = max(1, _safe_int(row.get("count")))
        total_count += count
        total_value += _safe_float(row.get(field)) * count
    if total_count <= 0:
        return 0.0
    return total_value / total_count


def _sum_count(rows: list[dict]) -> int:
    return sum(max(1, _safe_int(row.get("count"))) for row in rows)


def _sum_reward(rows: list[dict], field: str = "reward_sum") -> float:
    return sum(_safe_float(row.get(field)) for row in rows)


def _classify_family(conflict_rows: list[dict], positive_rows: list[dict], observed_rows: list[dict]) -> str:
    conflict_reward = _sum_reward(conflict_rows)
    positive_reward = _sum_reward(positive_rows)
    if positive_rows and positive_reward > abs(conflict_reward):
        return "conflict_reorganized_to_carried"
    if positive_rows:
        return "mixed_conflict_with_carried_trace"
    if observed_rows:
        return "conflict_to_observation"
    return "open_conflict_trace"


def build_rows(input_rows: list[dict]) -> tuple[list[dict], list[dict]]:
    conflict_families = {
        str(row.get("symbol_family", "") or "")
        for row in input_rows
        if _role_for(row) == "conflict" and str(row.get("symbol_family", "") or "")
    }

    family_rows: dict[str, list[dict]] = defaultdict(list)
    for row in input_rows:
        family = str(row.get("symbol_family", "") or "")
        if family in conflict_families:
            family_rows[family].append(row)

    detail: list[dict] = []
    summary: list[dict] = []

    for family in sorted(family_rows):
        rows = sorted(family_rows[family], key=_world_sort_key)
        conflict_rows = [row for row in rows if _role_for(row) == "conflict"]
        positive_rows = [row for row in rows if _role_for(row) == "carried_positive"]
        observed_rows = [row for row in rows if _role_for(row) == "observed_potential"]
        passive_conflict_state = _classify_family(conflict_rows, positive_rows, observed_rows)

        for row in rows:
            item = {
                "symbol_family": family,
                "world": str(row.get("world", "") or ""),
                "inner_state": str(row.get("inner_state", "") or ""),
                "contact_quality": str(row.get("contact_quality", "") or ""),
                "trace_role": _role_for(row),
                "count": _safe_int(row.get("count")),
                "reward_sum": round(_safe_float(row.get("reward_sum")), 6),
                "best_reward_sum": round(_safe_float(row.get("best_reward_sum")), 6),
                "avg_reward": round(_safe_float(row.get("avg_reward")), 6),
                "actions": str(row.get("actions", "") or ""),
                "transitions": str(row.get("transitions", "") or ""),
                "coherence_note": str(row.get("coherence_note", "") or ""),
                "passive_conflict_state": passive_conflict_state,
            }
            for field in SENSOR_FIELDS:
                item[field] = round(_safe_float(row.get(field)), 6)
            detail.append(item)

        world_path = " -> ".join(
            f"{row.get('world', '')}:{row.get('inner_state', '')}/{row.get('contact_quality', '')}"
            for row in rows
        )
        reward_path = " -> ".join(
            f"{row.get('world', '')}:{_safe_float(row.get('reward_sum')):.6f}"
            for row in rows
        )

        summary_row = {
            "symbol_family": family,
            "passive_conflict_state": passive_conflict_state,
            "world_path": world_path,
            "reward_path": reward_path,
            "conflict_worlds": ",".join(str(row.get("world", "") or "") for row in conflict_rows),
            "positive_worlds": ",".join(str(row.get("world", "") or "") for row in positive_rows),
            "observed_worlds": ",".join(str(row.get("world", "") or "") for row in observed_rows),
            "conflict_count": _sum_count(conflict_rows),
            "positive_count": _sum_count(positive_rows),
            "observed_count": _sum_count(observed_rows),
            "conflict_reward_sum": round(_sum_reward(conflict_rows), 6),
            "positive_reward_sum": round(_sum_reward(positive_rows), 6),
            "observed_best_reward_sum": round(_sum_reward(observed_rows, "best_reward_sum"), 6),
        }
        for field in SENSOR_FIELDS:
            summary_row[f"conflict_{field}"] = round(_weighted_average(conflict_rows, field), 6)
            summary_row[f"positive_{field}"] = round(_weighted_average(positive_rows, field), 6)
            summary_row[f"observed_{field}"] = round(_weighted_average(observed_rows, field), 6)
        summary.append(summary_row)

    summary.sort(
        key=lambda row: (
            str(row.get("passive_conflict_state", "")),
            str(row.get("symbol_family", "")),
        )
    )
    return detail, summary


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_passive_conflict_trace_lupe_detail.csv"
    summary_path = output_dir / "dio_mini_passive_conflict_trace_lupe_family_summary.csv"
    json_path = output_dir / "dio_mini_passive_conflict_trace_lupe.json"
    md_path = output_dir / "dio_mini_passive_conflict_trace_lupe.md"

    detail_fields = list(detail[0].keys()) if detail else ["symbol_family", "world", "trace_role"]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)

    summary_fields = list(summary[0].keys()) if summary else ["symbol_family", "passive_conflict_state"]
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)

    json_path.write_text(
        json.dumps({"detail": detail, "summary": summary}, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    lines = ["# DIO Mini Passive Conflict Trace Lupe", ""]
    if not summary:
        lines.append("Keine Konfliktfamilien gefunden.")
    for row in summary:
        lines.extend(
            [
                f"## {row['symbol_family']}",
                f"- passive_conflict_state: {row['passive_conflict_state']}",
                f"- conflict_worlds: {row['conflict_worlds'] or '-'}",
                f"- positive_worlds: {row['positive_worlds'] or '-'}",
                f"- observed_worlds: {row['observed_worlds'] or '-'}",
                f"- conflict_reward_sum: {float(row['conflict_reward_sum']):.6f}",
                f"- positive_reward_sum: {float(row['positive_reward_sum']):.6f}",
                f"- observed_best_reward_sum: {float(row['observed_best_reward_sum']):.6f}",
                f"- world_path: {row['world_path']}",
                "",
                "Sensorvergleich:",
                f"- conflict avg sehen_stability: {float(row['conflict_avg_sehen_form_stability']):.6f}",
                f"- positive avg sehen_stability: {float(row['positive_avg_sehen_form_stability']):.6f}",
                f"- observed avg sehen_stability: {float(row['observed_avg_sehen_form_stability']):.6f}",
                f"- conflict avg mcm_coherence: {float(row['conflict_avg_fuehlen_mcm_coherence']):.6f}",
                f"- positive avg mcm_coherence: {float(row['positive_avg_fuehlen_mcm_coherence']):.6f}",
                f"- observed avg mcm_coherence: {float(row['observed_avg_fuehlen_mcm_coherence']):.6f}",
                "",
            ]
        )
    lines.extend(
        [
            "## Grenze",
            "- passiver Leser",
            "- kein Memory-Schreiben",
            "- keine Motorik",
            "- kein Gate",
            "- keine harte Regel",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive conflict trace magnifier")
    parser.add_argument("--transfer-detail", required=True, help="dio_mini_passive_inner_coherence_transfer_detail.csv")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    detail, summary = build_rows(_read_rows(Path(args.transfer_detail)))
    write_outputs(detail, summary, Path(args.output_dir))
    print(f"detail_rows={len(detail)} summary_rows={len(summary)}")
    for row in summary:
        print(
            f"{row['symbol_family']} {row['passive_conflict_state']} "
            f"conflict={row['conflict_reward_sum']} positive={row['positive_reward_sum']} "
            f"observed_best={row['observed_best_reward_sum']}"
        )


if __name__ == "__main__":
    main()
