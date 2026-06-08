"""Report passive sensor coherence by inner state and family.

This map reads the passive inner-state timeline and aggregates seeing, hearing,
and feeling signals by inner state/family/contact. It is diagnostic only.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


SENSOR_FIELDS = [
    "sehen_form_flow",
    "sehen_form_stability",
    "hoeren_energy_tone",
    "fuehlen_mcm_coherence",
    "fuehlen_mcm_tension",
]


def _safe_float(value: object) -> float:
    try:
        return float(value or 0.0)
    except Exception:
        return 0.0


def _read_timeline(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _avg(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def _spread(values: list[float]) -> float:
    if not values:
        return 0.0
    return max(values) - min(values)


def _contact_quality(row: dict) -> str:
    action = str(row.get("action", "WAIT") or "WAIT").upper()
    reward = _safe_float(row.get("reward"))
    best = _safe_float(row.get("best_reward_training"))
    if action in ("LONG", "SHORT") and reward > 0.0:
        return "positive_real_contact"
    if action in ("LONG", "SHORT") and reward < 0.0:
        return "negative_real_contact"
    if action == "WAIT" and best > 0.0:
        return "observed_potential"
    return str(row.get("contact_state", "") or "quiet")


def _coherence_note(row: dict) -> str:
    inner = str(row.get("inner_state", "") or "")
    contact = str(row.get("contact_quality", "") or "")
    reward = _safe_float(row.get("reward_sum"))
    avg_mcm = _safe_float(row.get("avg_fuehlen_mcm_coherence"))
    avg_stability = _safe_float(row.get("avg_sehen_form_stability"))
    if inner == "inner_carried" and contact == "positive_real_contact" and reward > 0.0:
        return "getragen_sensorisch_bestaetigt"
    if inner == "inner_cautious" and contact == "observed_potential":
        return "vorsicht_beobachtet_potenzial"
    if inner == "inner_open_observation" and contact == "observed_potential":
        return "offen_beobachtet_potenzial"
    if avg_mcm > 0.85 and avg_stability > 0.85 and contact != "positive_real_contact":
        return "hohe_sicht_feld_kohärenz_ohne_handlung"
    return "offen_lesen"


def build_rows(timeline_csv: Path) -> tuple[list[dict], list[dict]]:
    rows = _read_timeline(timeline_csv)
    groups: dict[tuple[str, str, str], dict] = {}
    inner_groups: dict[str, dict] = {}
    for row in rows:
        inner = str(row.get("inner_state", "inner_unknown") or "inner_unknown")
        family = str(row.get("symbol_family", "") or "")
        contact = _contact_quality(row)
        key = (inner, family, contact)
        item = groups.setdefault(
            key,
            {
                "inner_state": inner,
                "symbol_family": family,
                "contact_quality": contact,
                "count": 0,
                "reward_sum": 0.0,
                "best_reward_sum": 0.0,
                "actions": set(),
                "transitions": set(),
                "sensor_values": {field: [] for field in SENSOR_FIELDS},
            },
        )
        item["count"] += 1
        item["reward_sum"] += _safe_float(row.get("reward"))
        item["best_reward_sum"] += _safe_float(row.get("best_reward_training"))
        item["actions"].add(str(row.get("action", "") or ""))
        item["transitions"].add(str(row.get("inner_transition", "") or ""))
        for field in SENSOR_FIELDS:
            item["sensor_values"][field].append(_safe_float(row.get(field)))

        inner_item = inner_groups.setdefault(
            inner,
            {
                "inner_state": inner,
                "count": 0,
                "reward_sum": 0.0,
                "best_reward_sum": 0.0,
                "families": set(),
                "contact_qualities": set(),
                "sensor_values": {field: [] for field in SENSOR_FIELDS},
            },
        )
        inner_item["count"] += 1
        inner_item["reward_sum"] += _safe_float(row.get("reward"))
        inner_item["best_reward_sum"] += _safe_float(row.get("best_reward_training"))
        inner_item["families"].add(family)
        inner_item["contact_qualities"].add(contact)
        for field in SENSOR_FIELDS:
            inner_item["sensor_values"][field].append(_safe_float(row.get(field)))

    detail: list[dict] = []
    for item in groups.values():
        count = int(item["count"])
        row = {
            "inner_state": item["inner_state"],
            "symbol_family": item["symbol_family"],
            "contact_quality": item["contact_quality"],
            "count": count,
            "reward_sum": round(float(item["reward_sum"]), 6),
            "best_reward_sum": round(float(item["best_reward_sum"]), 6),
            "avg_reward": round(float(item["reward_sum"]) / max(1, count), 6),
            "actions": ",".join(sorted(name for name in item["actions"] if name)),
            "transitions": ",".join(sorted(name for name in item["transitions"] if name)),
        }
        for field in SENSOR_FIELDS:
            values = item["sensor_values"][field]
            row[f"avg_{field}"] = round(_avg(values), 6)
            row[f"spread_{field}"] = round(_spread(values), 6)
        row["coherence_note"] = _coherence_note(row)
        row["passive_only"] = 1
        detail.append(row)

    summary: list[dict] = []
    for item in inner_groups.values():
        count = int(item["count"])
        row = {
            "inner_state": item["inner_state"],
            "count": count,
            "reward_sum": round(float(item["reward_sum"]), 6),
            "best_reward_sum": round(float(item["best_reward_sum"]), 6),
            "avg_reward": round(float(item["reward_sum"]) / max(1, count), 6),
            "families": ",".join(sorted(name for name in item["families"] if name)),
            "contact_qualities": ",".join(sorted(name for name in item["contact_qualities"] if name)),
        }
        for field in SENSOR_FIELDS:
            values = item["sensor_values"][field]
            row[f"avg_{field}"] = round(_avg(values), 6)
            row[f"spread_{field}"] = round(_spread(values), 6)
        row["passive_only"] = 1
        summary.append(row)

    detail.sort(
        key=lambda row: (
            str(row.get("inner_state", "")) != "inner_carried",
            -_safe_float(row.get("reward_sum")),
            str(row.get("symbol_family", "")),
        )
    )
    summary.sort(
        key=lambda row: (
            str(row.get("inner_state", "")) != "inner_carried",
            -_safe_float(row.get("reward_sum")),
            str(row.get("inner_state", "")),
        )
    )
    return detail, summary


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_passive_inner_coherence_map_detail.csv"
    summary_path = output_dir / "dio_mini_passive_inner_coherence_map_summary.csv"
    json_path = output_dir / "dio_mini_passive_inner_coherence_map.json"
    md_path = output_dir / "dio_mini_passive_inner_coherence_map.md"
    detail_fields = list(detail[0].keys()) if detail else [
        "inner_state",
        "symbol_family",
        "contact_quality",
        "count",
        "reward_sum",
    ]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)
    summary_fields = list(summary[0].keys()) if summary else [
        "inner_state",
        "count",
        "reward_sum",
    ]
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)
    json_path.write_text(json.dumps({"detail": detail, "summary": summary}, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Passive Inner Coherence Map", ""]
    lines.append("## Innenzustand")
    lines.append("")
    if not summary:
        lines.append("Keine Kohärenzdaten gefunden.")
    for row in summary:
        lines.extend(
            [
                f"### {row['inner_state']}",
                f"- count: {row['count']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- best_reward_sum: {float(row['best_reward_sum']):.6f}",
                f"- contact_qualities: {row['contact_qualities'] or '-'}",
                f"- families: {row['families'] or '-'}",
                f"- avg_sehen_form_stability: {float(row['avg_sehen_form_stability']):.6f}",
                f"- avg_hoeren_energy_tone: {float(row['avg_hoeren_energy_tone']):.6f}",
                f"- avg_fuehlen_mcm_coherence: {float(row['avg_fuehlen_mcm_coherence']):.6f}",
                f"- avg_fuehlen_mcm_tension: {float(row['avg_fuehlen_mcm_tension']):.6f}",
                "",
            ]
        )
    lines.append("## Familien")
    lines.append("")
    for row in detail:
        lines.extend(
            [
                f"### {row['symbol_family']} / {row['inner_state']} / {row['contact_quality']}",
                f"- count: {row['count']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- avg_reward: {float(row['avg_reward']):.6f}",
                f"- actions: {row['actions'] or '-'}",
                f"- transitions: {row['transitions'] or '-'}",
                f"- avg_sehen_form_flow: {float(row['avg_sehen_form_flow']):.6f}",
                f"- avg_sehen_form_stability: {float(row['avg_sehen_form_stability']):.6f}",
                f"- avg_hoeren_energy_tone: {float(row['avg_hoeren_energy_tone']):.6f}",
                f"- avg_fuehlen_mcm_coherence: {float(row['avg_fuehlen_mcm_coherence']):.6f}",
                f"- avg_fuehlen_mcm_tension: {float(row['avg_fuehlen_mcm_tension']):.6f}",
                f"- note: {row['coherence_note']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Grenze",
            "- kein Memory-Schreiben",
            "- keine Motorik",
            "- kein Gate",
            "- keine harte Regel",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive inner coherence map from timeline CSV")
    parser.add_argument("--timeline-csv", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    detail, summary = build_rows(Path(args.timeline_csv))
    write_outputs(detail, summary, Path(args.output_dir))
    print(f"coherence_rows={len(detail)} summary_rows={len(summary)}")
    for row in summary:
        print(
            f"{row['inner_state']} count={row['count']} reward={row['reward_sum']} "
            f"mcm={row['avg_fuehlen_mcm_coherence']} stability={row['avg_sehen_form_stability']}"
        )


if __name__ == "__main__":
    main()
