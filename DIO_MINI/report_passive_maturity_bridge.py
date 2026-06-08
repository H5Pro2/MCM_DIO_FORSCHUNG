"""Build a passive maturity bridge between observation and real outcomes.

The report compares passive WAIT observations with real LONG/SHORT actions
that happened in the same controlled source and direction. It stays diagnostic:

- no memory write
- no action influence
- no gate
- no future teacher

It answers the question:
"Did something I only observed resemble something that was later carried or
burdened by real consequence?"
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


AVG_SENSE_FIELDS = (
    "avg_sehen_form_flow",
    "avg_sehen_form_stability",
    "avg_sehen_form_change",
    "avg_hoeren_energy_tone",
    "avg_hoeren_energy_shift",
    "avg_fuehlen_mcm_coherence",
    "avg_fuehlen_mcm_tension",
    "avg_fuehlen_mcm_asymmetry",
)


def _safe_float(value: object) -> float:
    try:
        value = float(value or 0.0)
    except Exception:
        value = 0.0
    if value != value:
        value = 0.0
    return value


def _safe_int(value: object) -> int:
    try:
        return int(float(value or 0))
    except Exception:
        return 0


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _sense_similarity(left: dict, right: dict) -> float:
    diffs = []
    for field in AVG_SENSE_FIELDS:
        # The Mini-DIO sense values are normalized around roughly -1..1.
        diffs.append(min(1.0, abs(_safe_float(left.get(field)) - _safe_float(right.get(field))) / 2.0))
    if not diffs:
        return 0.0
    return round(max(0.0, 1.0 - (sum(diffs) / len(diffs))), 9)


def _mcm_similarity(left: dict, right: dict) -> float:
    fields = (
        "avg_fuehlen_mcm_coherence",
        "avg_fuehlen_mcm_tension",
        "avg_fuehlen_mcm_asymmetry",
    )
    diffs = [min(1.0, abs(_safe_float(left.get(field)) - _safe_float(right.get(field))) / 2.0) for field in fields]
    return round(max(0.0, 1.0 - (sum(diffs) / max(1, len(diffs)))), 9)


def _sensory_similarity(left: dict, right: dict) -> float:
    fields = (
        "avg_sehen_form_flow",
        "avg_sehen_form_stability",
        "avg_sehen_form_change",
        "avg_hoeren_energy_tone",
        "avg_hoeren_energy_shift",
    )
    diffs = [min(1.0, abs(_safe_float(left.get(field)) - _safe_float(right.get(field))) / 2.0) for field in fields]
    return round(max(0.0, 1.0 - (sum(diffs) / max(1, len(diffs)))), 9)


def _bridge_reading(real_reward: float, tp_count: int, sl_count: int, similarity: float) -> str:
    if similarity <= 0.0:
        return "passive_maturity_unreadable"
    if real_reward > 0.0 and tp_count > sl_count:
        return "passive_near_carried_outcome"
    if sl_count >= tp_count and real_reward <= 0.0:
        return "passive_near_burdened_outcome"
    return "passive_near_mixed_outcome"


def build_report(summary_path: Path) -> tuple[list[dict], list[dict]]:
    rows = _read_csv(summary_path)
    passive_rows = [
        row
        for row in rows
        if _safe_int(row.get("passive_wait_traces")) > 0 and _safe_int(row.get("real_action_traces")) == 0
    ]
    action_rows = [
        row
        for row in rows
        if _safe_int(row.get("real_action_traces")) > 0
    ]

    detail: list[dict] = []
    by_passive_family: dict[str, dict] = {}

    for passive in passive_rows:
        source = str(passive.get("source_label", "") or "")
        action = str(passive.get("action", "") or "")
        candidates = [
            row
            for row in action_rows
            if str(row.get("source_label", "") or "") == source and str(row.get("action", "") or "") == action
        ]
        for real in candidates:
            similarity = _sense_similarity(passive, real)
            mcm_similarity = _mcm_similarity(passive, real)
            sensory_similarity = _sensory_similarity(passive, real)
            real_reward = _safe_float(real.get("real_reward_sum"))
            tp_count = _safe_int(real.get("tp_count"))
            sl_count = _safe_int(real.get("sl_count"))
            passive_key = f"{source}:{passive.get('family_action', '')}"
            item = {
                "source_label": source,
                "passive_family_action": str(passive.get("family_action", "") or ""),
                "real_family_action": str(real.get("family_action", "") or ""),
                "action": action,
                "sense_similarity": similarity,
                "sensory_similarity": sensory_similarity,
                "mcm_similarity": mcm_similarity,
                "passive_wait_traces": _safe_int(passive.get("passive_wait_traces")),
                "passive_potential_sum": round(_safe_float(passive.get("passive_potential_sum")), 9),
                "real_action_traces": _safe_int(real.get("real_action_traces")),
                "real_tp_count": tp_count,
                "real_sl_count": sl_count,
                "real_reward_sum": round(real_reward, 9),
                "maturity_reading": _bridge_reading(real_reward, tp_count, sl_count, similarity),
                "passive_only": 1,
            }
            detail.append(item)

            bucket = by_passive_family.setdefault(
                passive_key,
                {
                    "source_label": source,
                    "passive_family_action": str(passive.get("family_action", "") or ""),
                    "action": action,
                    "candidate_count": 0,
                    "best_similarity": 0.0,
                    "best_sensory_similarity": 0.0,
                    "best_mcm_similarity": 0.0,
                    "best_real_family_action": "",
                    "best_real_reward_sum": 0.0,
                    "best_real_tp_count": 0,
                    "best_real_sl_count": 0,
                    "carried_candidate_count": 0,
                    "burdened_candidate_count": 0,
                    "mixed_candidate_count": 0,
                    "best_reading": "",
                },
            )
            bucket["candidate_count"] += 1
            if item["maturity_reading"] == "passive_near_carried_outcome":
                bucket["carried_candidate_count"] += 1
            elif item["maturity_reading"] == "passive_near_burdened_outcome":
                bucket["burdened_candidate_count"] += 1
            else:
                bucket["mixed_candidate_count"] += 1
            if similarity > float(bucket["best_similarity"]):
                bucket["best_similarity"] = similarity
                bucket["best_sensory_similarity"] = sensory_similarity
                bucket["best_mcm_similarity"] = mcm_similarity
                bucket["best_real_family_action"] = item["real_family_action"]
                bucket["best_real_reward_sum"] = item["real_reward_sum"]
                bucket["best_real_tp_count"] = item["real_tp_count"]
                bucket["best_real_sl_count"] = item["real_sl_count"]
                bucket["best_reading"] = item["maturity_reading"]

    summary = []
    for bucket in by_passive_family.values():
        item = dict(bucket)
        if int(item["carried_candidate_count"]) and not int(item["burdened_candidate_count"]):
            item["passive_maturity_state"] = "passive_observation_has_carried_neighbor"
        elif int(item["burdened_candidate_count"]) and not int(item["carried_candidate_count"]):
            item["passive_maturity_state"] = "passive_observation_has_burdened_neighbor"
        elif int(item["carried_candidate_count"]) and int(item["burdened_candidate_count"]):
            item["passive_maturity_state"] = "passive_observation_has_mixed_neighbors"
        else:
            item["passive_maturity_state"] = "passive_observation_has_open_neighbor"
        item["passive_only"] = 1
        summary.append(item)

    detail.sort(key=lambda item: (str(item["source_label"]), -float(item["sense_similarity"]), str(item["passive_family_action"])))
    summary.sort(key=lambda item: (str(item["source_label"]), -float(item["best_similarity"]), str(item["passive_family_action"])))
    return detail, summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(detail: list[dict], summary: list[dict], source_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_maturity_bridge.csv"
    summary_csv = output_dir / "dio_mini_passive_maturity_bridge_summary.csv"
    json_path = output_dir / "dio_mini_passive_maturity_bridge.json"
    md_path = output_dir / "dio_mini_passive_maturity_bridge.md"

    _write_csv(detail_csv, detail, ["source_label", "passive_family_action", "real_family_action"])
    _write_csv(summary_csv, summary, ["source_label", "passive_family_action", "passive_maturity_state"])
    json_path.write_text(
        json.dumps(
            {
                "source": str(source_path),
                "detail": detail,
                "summary": summary,
                "boundary": {
                    "writes_training_memory": False,
                    "influences_action": False,
                    "is_gate": False,
                    "is_motoric": False,
                    "is_future_teacher": False,
                },
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = ["# DIO Mini Passive Maturity Bridge", "", f"- source: {source_path}", ""]
    lines.append("## Zusammenfassung")
    if not summary:
        lines.append("- keine passive Reifebruecke lesbar")
    for row in summary[:30]:
        lines.append(
            f"- {row['source_label']} {row['passive_family_action']} -> {row['best_real_family_action']}: "
            f"similarity={row['best_similarity']} sensory={row['best_sensory_similarity']} "
            f"mcm={row['best_mcm_similarity']} reward={row['best_real_reward_sum']} "
            f"state={row['passive_maturity_state']}"
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Reifebruecke",
            "- keine Handlung",
            "- kein Trainingsmemory",
            "- kein Gate",
            "- kein Zukunftslehrer",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive Mini-DIO maturity bridge")
    parser.add_argument("--bridge-summary", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    source_path = Path(args.bridge_summary)
    detail, summary = build_report(source_path)
    write_outputs(detail, summary, source_path, Path(args.output_dir))
    print(f"passive_maturity_bridge_rows={len(detail)} summary={len(summary)}")
    for row in summary[:12]:
        print(
            f"{row['source_label']} {row['passive_family_action']} -> {row['best_real_family_action']} "
            f"similarity={row['best_similarity']} state={row['passive_maturity_state']}"
        )


if __name__ == "__main__":
    main()
