"""Create a short passive development diagnosis from a DIO mini maturity map."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


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


def _read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _has_note(row: dict, note: str) -> bool:
    return note in str(row.get("trace_notes", "") or "").split("|")


def _classify(row: dict) -> str:
    reward = _safe_float(row.get("reward_sum", 0.0))
    per_trade = _safe_float(row.get("reward_per_executed_run", 0.0))
    phase_count = _safe_int(row.get("phase_count", 0))
    executed = _safe_int(row.get("executed_runs", 0))
    observed = _safe_int(row.get("observed_runs", 0))
    has_neighbors = _safe_int(row.get("bearing_neighbor_count", 0)) > 0
    same_family = _safe_int(row.get("same_family_relation_count", 0)) > 0
    afterimage = _has_note(row, "nachhall_gehalten")
    if reward < 0.0:
        return "belastete_spur"
    if phase_count > 1 and reward > 3.0 and same_family and not afterimage:
        return "stabile_reifespur"
    if phase_count > 1 and reward > 0.0 and same_family:
        return "entwickelnde_reifespur"
    if phase_count > 1 and reward > 0.0 and afterimage:
        return "reifespur_mit_nachhall"
    if phase_count > 1 and executed > 0 and reward <= 0.5:
        return "schwache_wiederkehr"
    if phase_count == 1 and reward > 2.0 and has_neighbors:
        return "starke_lokale_sensorikspur"
    if executed == 0 and observed > 0 and afterimage:
        return "beobachteter_nachhall"
    if executed == 0 and observed > 0:
        return "stabile_beobachtung"
    if reward > 0.0 and per_trade > 0.0:
        return "positive_einzelspur"
    return "ruhige_spur"


def build_summary(rows: list[dict]) -> tuple[list[dict], dict]:
    output = []
    counts: dict[str, int] = {}
    reward_by_class: dict[str, float] = {}
    for row in rows:
        classification = _classify(row)
        counts[classification] = counts.get(classification, 0) + 1
        reward_by_class[classification] = reward_by_class.get(classification, 0.0) + _safe_float(row.get("reward_sum", 0.0))
        output.append(
            {
                "family": row.get("family", "-"),
                "classification": classification,
                "trace_notes": row.get("trace_notes", "-"),
                "phases": row.get("phases", "-"),
                "phase_count": _safe_int(row.get("phase_count", 0)),
                "executed_runs": _safe_int(row.get("executed_runs", 0)),
                "observed_runs": _safe_int(row.get("observed_runs", 0)),
                "reward_sum": round(_safe_float(row.get("reward_sum", 0.0)), 6),
                "reward_per_executed_run": round(_safe_float(row.get("reward_per_executed_run", 0.0)), 6),
                "visual_mcm": round(_safe_float(row.get("avg_visual_mcm_alignment_trace", 0.0)), 6),
                "tone_tension": round(_safe_float(row.get("avg_tone_tension_resonance_trace", 0.0)), 6),
                "bearing_neighbor_count": _safe_int(row.get("bearing_neighbor_count", 0)),
                "same_family_relation_count": _safe_int(row.get("same_family_relation_count", 0)),
            }
        )
    output.sort(
        key=lambda item: (
            item["classification"] == "stabile_reifespur",
            item["classification"] == "starke_lokale_sensorikspur",
            item["classification"] == "reifespur_mit_nachhall",
            item["reward_sum"],
            item["phase_count"],
        ),
        reverse=True,
    )
    overview = {
        "class_counts": counts,
        "class_reward_sum": {key: round(value, 6) for key, value in sorted(reward_by_class.items())},
        "top_stable_maturity": [row["family"] for row in output if row["classification"] == "stabile_reifespur"][:5],
        "developing_maturity": [row["family"] for row in output if row["classification"] == "entwickelnde_reifespur"][:5],
        "top_local_sensor": [row["family"] for row in output if row["classification"] == "starke_lokale_sensorikspur"][:5],
        "afterimage_traces": [row["family"] for row in output if row["classification"] == "reifespur_mit_nachhall"][:5],
        "weak_recurrence": [row["family"] for row in output if row["classification"] == "schwache_wiederkehr"][:5],
    }
    return output, overview


def write_outputs(rows: list[dict], overview: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_maturity_diagnosis.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "dio_mini_maturity_diagnosis_overview.json").write_text(
        json.dumps(overview, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    if rows:
        with (output_dir / "dio_mini_maturity_diagnosis.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    lines = ["# DIO Mini Maturity Diagnosis", ""]
    lines.append("## Klassen")
    for key, value in sorted(overview.get("class_counts", {}).items()):
        reward = dict(overview.get("class_reward_sum", {}) or {}).get(key, 0.0)
        lines.append(f"- {key}: {value} Spuren, Reward {reward}")
    lines.append("")
    lines.append("## Stabile Reifespuren")
    for family in overview.get("top_stable_maturity", []) or []:
        lines.append(f"- {family}")
    lines.append("")
    lines.append("## Entwickelnde Reifespuren")
    for family in overview.get("developing_maturity", []) or []:
        lines.append(f"- {family}")
    lines.append("")
    lines.append("## Lokale Sensorikspuren")
    for family in overview.get("top_local_sensor", []) or []:
        lines.append(f"- {family}")
    lines.append("")
    lines.append("## Nachhallspuren")
    for family in overview.get("afterimage_traces", []) or []:
        lines.append(f"- {family}")
    lines.append("")
    lines.append("## Schwache Wiederkehr")
    for family in overview.get("weak_recurrence", []) or []:
        lines.append(f"- {family}")
    lines.append("")
    (output_dir / "dio_mini_maturity_diagnosis.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize passive DIO mini maturity map")
    parser.add_argument("--maturity-map", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    rows = _read_rows(Path(args.maturity_map))
    diagnosis, overview = build_summary(rows)
    write_outputs(diagnosis, overview, Path(args.output_dir))
    for row in diagnosis[:16]:
        print(
            f"family={row['family']} class={row['classification']} reward={row['reward_sum']:.4f} "
            f"phases={row['phase_count']} neighbors={row['bearing_neighbor_count']}"
        )


if __name__ == "__main__":
    main()
