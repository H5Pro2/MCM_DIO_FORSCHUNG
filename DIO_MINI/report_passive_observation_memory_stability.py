"""Compare passive Mini-DIO observation-memory maps across variants.

The report stays diagnostic. It checks whether non-traded possibilities
repeat across controlled worlds without writing memory or changing action.
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


def _parse_source(spec: str) -> tuple[str, Path]:
    if "=" in spec:
        label, path = spec.split("=", 1)
        return label.strip() or Path(path).parent.name, Path(path)
    path = Path(spec)
    return path.parent.name, path


def _reading_for_pair(source_count: int, trace_count: int, potential_sum: float) -> str:
    if source_count >= 2 and potential_sum > 0.0:
        return "passive_possibility_repeats_across_variants"
    if trace_count > 1 and potential_sum > 0.0:
        return "passive_possibility_repeats_inside_variant"
    return "passive_possibility_local_trace"


def _reading_for_family(source_count: int, actions: set[str], potential_sum: float) -> str:
    if source_count >= 2 and len(actions) >= 2:
        return "family_repeats_with_action_variance"
    if source_count >= 2 and potential_sum > 0.0:
        return "family_repeats_same_action_tendency"
    if potential_sum > 0.0:
        return "family_local_potential"
    return "family_open_trace"


def build_report(sources: list[tuple[str, Path]]) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    detail: list[dict] = []
    by_family_action: dict[tuple[str, str], dict] = {}
    by_family: dict[str, dict] = {}
    by_action: dict[str, dict] = {}

    for label, path in sources:
        for row in _read_csv(path):
            family = str(row.get("symbol_family", "") or "-")
            action = str(row.get("observed_possible_action", "") or "-").upper()
            trace_count = _safe_int(row.get("trace_count"))
            potential_sum = _safe_float(row.get("potential_reward_sum"))
            pressure = _safe_float(row.get("avg_observation_learning_pressure"))
            item = {
                "source_label": label,
                "symbol_family": family,
                "observed_possible_action": action,
                "family_action": f"{family}:{action}",
                "passive_observation_state": str(row.get("passive_observation_state", "") or ""),
                "trace_count": trace_count,
                "run_count": _safe_int(row.get("run_count")),
                "potential_reward_sum": round(potential_sum, 9),
                "avg_potential_reward": round(_safe_float(row.get("avg_potential_reward")), 9),
                "avg_observation_learning_pressure": round(pressure, 9),
                "phase_active_count": _safe_int(row.get("phase_active_count")),
                "inner_observation_note": str(row.get("inner_observation_note", "") or ""),
                "passive_only": 1,
            }
            for field in AVG_SENSE_FIELDS:
                item[field] = round(_safe_float(row.get(field)), 9)
            detail.append(item)

            pair_key = (family, action)
            pair_bucket = by_family_action.setdefault(
                pair_key,
                {
                    "symbol_family": family,
                    "observed_possible_action": action,
                    "source_count": 0,
                    "sources": set(),
                    "trace_count": 0,
                    "potential_reward_sum": 0.0,
                    "pressure_sum": 0.0,
                    "row_count": 0,
                    "sense_sums": {field: 0.0 for field in AVG_SENSE_FIELDS},
                },
            )
            pair_bucket["sources"].add(label)
            pair_bucket["trace_count"] += trace_count
            pair_bucket["potential_reward_sum"] += potential_sum
            pair_bucket["pressure_sum"] += pressure
            pair_bucket["row_count"] += 1
            for field in AVG_SENSE_FIELDS:
                pair_bucket["sense_sums"][field] += float(item[field])

            family_bucket = by_family.setdefault(
                family,
                {
                    "symbol_family": family,
                    "source_count": 0,
                    "sources": set(),
                    "actions": set(),
                    "trace_count": 0,
                    "potential_reward_sum": 0.0,
                    "pressure_sum": 0.0,
                    "row_count": 0,
                    "sense_sums": {field: 0.0 for field in AVG_SENSE_FIELDS},
                },
            )
            family_bucket["sources"].add(label)
            family_bucket["actions"].add(action)
            family_bucket["trace_count"] += trace_count
            family_bucket["potential_reward_sum"] += potential_sum
            family_bucket["pressure_sum"] += pressure
            family_bucket["row_count"] += 1
            for field in AVG_SENSE_FIELDS:
                family_bucket["sense_sums"][field] += float(item[field])

            action_bucket = by_action.setdefault(
                action,
                {
                    "observed_possible_action": action,
                    "source_count": 0,
                    "sources": set(),
                    "family_count": 0,
                    "families": set(),
                    "trace_count": 0,
                    "potential_reward_sum": 0.0,
                    "pressure_sum": 0.0,
                    "row_count": 0,
                },
            )
            action_bucket["sources"].add(label)
            action_bucket["families"].add(family)
            action_bucket["trace_count"] += trace_count
            action_bucket["potential_reward_sum"] += potential_sum
            action_bucket["pressure_sum"] += pressure
            action_bucket["row_count"] += 1

    pair_summary: list[dict] = []
    for bucket in by_family_action.values():
        row_count = max(1, int(bucket["row_count"]))
        sources = set(bucket["sources"])
        trace_count = int(bucket["trace_count"])
        potential_sum = float(bucket["potential_reward_sum"])
        item = {
            "symbol_family": bucket["symbol_family"],
            "observed_possible_action": bucket["observed_possible_action"],
            "family_action": f"{bucket['symbol_family']}:{bucket['observed_possible_action']}",
            "source_count": len(sources),
            "sources": ",".join(sorted(sources)),
            "trace_count": trace_count,
            "potential_reward_sum": round(potential_sum, 9),
            "avg_observation_learning_pressure": round(float(bucket["pressure_sum"]) / row_count, 9),
            "stability_reading": _reading_for_pair(len(sources), trace_count, potential_sum),
            "passive_only": 1,
        }
        for field in AVG_SENSE_FIELDS:
            item[field] = round(float(bucket["sense_sums"][field]) / row_count, 9)
        pair_summary.append(item)

    family_summary: list[dict] = []
    for bucket in by_family.values():
        row_count = max(1, int(bucket["row_count"]))
        sources = set(bucket["sources"])
        actions = set(bucket["actions"])
        potential_sum = float(bucket["potential_reward_sum"])
        item = {
            "symbol_family": bucket["symbol_family"],
            "source_count": len(sources),
            "sources": ",".join(sorted(sources)),
            "actions": ",".join(sorted(actions)),
            "action_count": len(actions),
            "trace_count": int(bucket["trace_count"]),
            "potential_reward_sum": round(potential_sum, 9),
            "avg_observation_learning_pressure": round(float(bucket["pressure_sum"]) / row_count, 9),
            "stability_reading": _reading_for_family(len(sources), actions, potential_sum),
            "passive_only": 1,
        }
        for field in AVG_SENSE_FIELDS:
            item[field] = round(float(bucket["sense_sums"][field]) / row_count, 9)
        family_summary.append(item)

    action_summary: list[dict] = []
    for bucket in by_action.values():
        row_count = max(1, int(bucket["row_count"]))
        sources = set(bucket["sources"])
        families = set(bucket["families"])
        action_summary.append(
            {
                "observed_possible_action": bucket["observed_possible_action"],
                "source_count": len(sources),
                "sources": ",".join(sorted(sources)),
                "family_count": len(families),
                "families": ",".join(sorted(families)),
                "trace_count": int(bucket["trace_count"]),
                "potential_reward_sum": round(float(bucket["potential_reward_sum"]), 9),
                "avg_observation_learning_pressure": round(float(bucket["pressure_sum"]) / row_count, 9),
                "passive_only": 1,
            }
        )

    detail.sort(key=lambda item: (str(item["source_label"]), str(item["symbol_family"]), str(item["observed_possible_action"])))
    pair_summary.sort(key=lambda item: (-int(item["source_count"]), -int(item["trace_count"]), str(item["family_action"])))
    family_summary.sort(key=lambda item: (-int(item["source_count"]), -int(item["trace_count"]), str(item["symbol_family"])))
    action_summary.sort(key=lambda item: (-int(item["trace_count"]), str(item["observed_possible_action"])))
    return detail, pair_summary, family_summary, action_summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(
    detail: list[dict],
    pair_summary: list[dict],
    family_summary: list[dict],
    action_summary: list[dict],
    sources: list[tuple[str, Path]],
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_observation_memory_stability.csv"
    pair_csv = output_dir / "dio_mini_passive_observation_memory_stability_by_family_action.csv"
    family_csv = output_dir / "dio_mini_passive_observation_memory_stability_by_family.csv"
    action_csv = output_dir / "dio_mini_passive_observation_memory_stability_by_action.csv"
    json_path = output_dir / "dio_mini_passive_observation_memory_stability.json"
    md_path = output_dir / "dio_mini_passive_observation_memory_stability.md"
    txt_path = output_dir / "dio_mini_passive_observation_memory_stability.txt"

    _write_csv(detail_csv, detail, ["source_label", "symbol_family", "observed_possible_action"])
    _write_csv(pair_csv, pair_summary, ["symbol_family", "observed_possible_action", "source_count"])
    _write_csv(family_csv, family_summary, ["symbol_family", "source_count", "actions"])
    _write_csv(action_csv, action_summary, ["observed_possible_action", "source_count", "trace_count"])

    payload = {
        "sources": [{"label": label, "path": str(path)} for label, path in sources],
        "detail": detail,
        "pair_summary": pair_summary,
        "family_summary": family_summary,
        "action_summary": action_summary,
        "boundary": {
            "writes_training_memory": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
            "is_future_teacher": False,
        },
    }
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Passive Observation Memory Stability", ""]
    lines.append("## Quellen")
    for label, path in sources:
        lines.append(f"- {label}: {path}")
    lines.extend(["", "## Familien"])
    if not family_summary:
        lines.append("- keine passiven Beobachtungsfamilien")
    for row in family_summary[:20]:
        lines.append(
            f"- {row['symbol_family']}: sources={row['source_count']} actions={row['actions']} "
            f"traces={row['trace_count']} potential={row['potential_reward_sum']} "
            f"reading={row['stability_reading']}"
        )
    lines.extend(["", "## Familien/Aktion"])
    if not pair_summary:
        lines.append("- keine Familien/Aktion-Spuren")
    for row in pair_summary[:20]:
        lines.append(
            f"- {row['family_action']}: sources={row['source_count']} traces={row['trace_count']} "
            f"potential={row['potential_reward_sum']} reading={row['stability_reading']}"
        )
    lines.extend(["", "## Aktionsrichtung"])
    for row in action_summary:
        lines.append(
            f"- {row['observed_possible_action']}: sources={row['source_count']} "
            f"families={row['family_count']} traces={row['trace_count']} potential={row['potential_reward_sum']}"
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Beobachtungs-Stabilitaetsdiagnose",
            "- keine Handlung",
            "- kein Trainingsmemory",
            "- kein Gate",
            "- kein Zukunftslehrer",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")

    txt_lines = [
        f"{row['symbol_family']} | {row['actions']} | sources={row['source_count']} | "
        f"traces={row['trace_count']} | {row['stability_reading']}"
        for row in family_summary
    ]
    txt_path.write_text("\n".join(txt_lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare passive Mini-DIO observation-memory maps")
    parser.add_argument("--source", action="append", required=True, help="label=path or path; can be repeated")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    sources = [_parse_source(spec) for spec in args.source]
    detail, pair_summary, family_summary, action_summary = build_report(sources)
    write_outputs(detail, pair_summary, family_summary, action_summary, sources, Path(args.output_dir))
    print(
        f"passive_observation_memory_stability_rows={len(detail)} "
        f"families={len(family_summary)} family_actions={len(pair_summary)} actions={len(action_summary)}"
    )
    for row in family_summary[:12]:
        print(
            f"{row['symbol_family']} sources={row['source_count']} actions={row['actions']} "
            f"traces={row['trace_count']} reading={row['stability_reading']}"
        )


if __name__ == "__main__":
    main()
