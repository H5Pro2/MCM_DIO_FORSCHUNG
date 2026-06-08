"""Inspect seeing, hearing, and feeling traces for selected DIO mini families.

Diagnostics only. This reads cross-world action phase rows and summarizes the
sensor basis of selected families without changing memory or motorics.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


SENSE_FIELDS = (
    "sehen_form_flow",
    "sehen_form_stability",
    "sehen_form_change",
    "hoeren_energy_tone",
    "hoeren_energy_shift",
    "fuehlen_mcm_coherence",
    "fuehlen_mcm_tension",
    "fuehlen_mcm_asymmetry",
)


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _sense_summary(row: dict, prefix: str) -> dict:
    return {field: round(_safe_float(row.get(f"{prefix}_{field}", 0.0)), 6) for field in SENSE_FIELDS}


def inspect(rows: list[dict], families: set[str]) -> tuple[list[dict], dict]:
    selected = [row for row in rows if str(row.get("family", "") or "") in families]
    output = []
    for row in selected:
        observed = _sense_summary(row, "observed")
        executed = _sense_summary(row, "executed")
        delta = {field: round(executed[field] - observed[field], 6) for field in SENSE_FIELDS}
        output.append(
            {
                "phase": row.get("phase", "-"),
                "family": row.get("family", "-"),
                "classification": row.get("classification", "-"),
                "executed_rows": int(float(row.get("executed_rows", 0) or 0)),
                "observed_rows": int(float(row.get("observed_rows", 0) or 0)),
                "reward_sum": round(_safe_float(row.get("reward_sum", 0.0)), 6),
                "observed": observed,
                "executed": executed,
                "executed_minus_observed": delta,
            }
        )
    output.sort(key=lambda item: (item["family"], item["phase"]))

    family_summary = {}
    for family in sorted(families):
        family_rows = [row for row in output if row["family"] == family]
        if not family_rows:
            continue
        reward = sum(_safe_float(row.get("reward_sum", 0.0)) for row in family_rows)
        executed_rows = sum(int(row.get("executed_rows", 0) or 0) for row in family_rows)
        observed_rows = sum(int(row.get("observed_rows", 0) or 0) for row in family_rows)
        max_delta = 0.0
        transition_delta = 0.0
        for row in family_rows:
            row_delta = max(abs(float(value)) for value in row["executed_minus_observed"].values())
            max_delta = max(max_delta, row_delta)
            if int(row.get("executed_rows", 0) or 0) > 0 and int(row.get("observed_rows", 0) or 0) > 0:
                transition_delta = max(transition_delta, row_delta)
        family_summary[family] = {
            "phases": [row["phase"] for row in family_rows],
            "reward_sum": round(reward, 6),
            "executed_rows": executed_rows,
            "observed_rows": observed_rows,
            "max_sensor_delta_all_phases": round(max_delta, 6),
            "max_sensor_delta_in_observation_to_action": round(transition_delta, 6),
        }
    overview = {"families": family_summary}
    return output, overview


def write_outputs(rows: list[dict], overview: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_family_senses.json").write_text(
        json.dumps(rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "dio_mini_family_senses_overview.json").write_text(
        json.dumps(overview, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    lines = ["# DIO Mini Family Senses", ""]
    for family, summary in sorted(dict(overview.get("families", {}) or {}).items()):
        lines.append(f"## {family}")
        lines.append(f"- phases: {', '.join(summary['phases'])}")
        lines.append(f"- reward_sum: {summary['reward_sum']}")
        lines.append(f"- executed_rows: {summary['executed_rows']}")
        lines.append(f"- observed_rows: {summary['observed_rows']}")
        lines.append(f"- max_sensor_delta_all_phases: {summary['max_sensor_delta_all_phases']}")
        lines.append(
            f"- max_sensor_delta_in_observation_to_action: {summary['max_sensor_delta_in_observation_to_action']}"
        )
        lines.append("")
        for row in [item for item in rows if item["family"] == family]:
            executed = row["executed"]
            observed = row["observed"]
            lines.append(f"### {row['phase']} / {row['classification']}")
            lines.append(f"- reward_sum: {row['reward_sum']}")
            lines.append(
                "- observed: "
                f"sehen_flow={observed['sehen_form_flow']}, "
                f"sehen_stability={observed['sehen_form_stability']}, "
                f"hoeren_tone={observed['hoeren_energy_tone']}, "
                f"hoeren_shift={observed['hoeren_energy_shift']}, "
                f"mcm_coherence={observed['fuehlen_mcm_coherence']}, "
                f"mcm_tension={observed['fuehlen_mcm_tension']}, "
                f"mcm_asymmetry={observed['fuehlen_mcm_asymmetry']}"
            )
            lines.append(
                "- executed: "
                f"sehen_flow={executed['sehen_form_flow']}, "
                f"sehen_stability={executed['sehen_form_stability']}, "
                f"hoeren_tone={executed['hoeren_energy_tone']}, "
                f"hoeren_shift={executed['hoeren_energy_shift']}, "
                f"mcm_coherence={executed['fuehlen_mcm_coherence']}, "
                f"mcm_tension={executed['fuehlen_mcm_tension']}, "
                f"mcm_asymmetry={executed['fuehlen_mcm_asymmetry']}"
            )
            lines.append("")
    (output_dir / "dio_mini_family_senses.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect selected DIO mini family senses")
    parser.add_argument("--phase-rows", required=True)
    parser.add_argument("--family", action="append", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    rows = _read_rows(Path(args.phase_rows))
    inspected, overview = inspect(rows, set(args.family))
    write_outputs(inspected, overview, Path(args.output_dir))
    print(json.dumps(overview, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
