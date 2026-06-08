"""Analyze passive sight/hearing/feeling traces for DIO mini families."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


TRADE_ACTIONS = ("LONG", "SHORT")
SENSOR_FIELDS = (
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


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _clip01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def collect_episode_paths(debug_root: Path) -> list[Path]:
    if debug_root.name == "episodes.csv":
        return [debug_root]
    return sorted(debug_root.glob("dio_mini_lauf_*/episodes.csv"))


def _new_record(family: str) -> dict:
    record = {
        "family": family,
        "rows": 0,
        "executed": 0,
        "positive_executed": 0,
        "burdened_executed": 0,
        "observed_potential": 0,
        "held_same_episode": 0,
        "reward_sum": 0.0,
        "best_reward_sum": 0.0,
        "max_trade_readiness": 0.0,
        "max_mature_transfer": 0.0,
    }
    for field in SENSOR_FIELDS:
        record[f"{field}_sum"] = 0.0
        record[f"{field}_executed_sum"] = 0.0
        record[f"{field}_observed_sum"] = 0.0
    record["visual_mcm_distance_sum"] = 0.0
    record["tone_tension_distance_sum"] = 0.0
    record["visual_mcm_distance_executed_sum"] = 0.0
    record["tone_tension_distance_executed_sum"] = 0.0
    record["visual_mcm_distance_observed_sum"] = 0.0
    record["tone_tension_distance_observed_sum"] = 0.0
    return record


def _sensor_distances(row: dict) -> tuple[float, float]:
    form_flow = _safe_float(row.get("sehen_form_flow", 0.0))
    form_change = _safe_float(row.get("sehen_form_change", 0.0))
    energy_tone = _safe_float(row.get("hoeren_energy_tone", 0.0))
    mcm_tension = _safe_float(row.get("fuehlen_mcm_tension", 0.0))
    mcm_asymmetry = _safe_float(row.get("fuehlen_mcm_asymmetry", 0.0))
    visual_mcm_distance = abs(((form_flow * 0.65) + (form_change * 0.35)) - mcm_asymmetry)
    tone_tension_distance = abs(abs(energy_tone) - mcm_tension)
    return visual_mcm_distance, tone_tension_distance


def _observed_potential(row: dict, action: str, raw_action: str) -> bool:
    best_action = str(row.get("best_action_training", "WAIT") or "WAIT").upper()
    best_reward = _safe_float(row.get("best_reward_training", 0.0))
    return action == "WAIT" and raw_action not in TRADE_ACTIONS and best_action in TRADE_ACTIONS and best_reward > 0.0


def analyze(debug_root: Path) -> list[dict]:
    records: dict[str, dict] = {}
    for path in collect_episode_paths(debug_root):
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                family = str(row.get("symbol_family", "-") or "-")
                action = str(row.get("action", "WAIT") or "WAIT").upper()
                raw_action = str(row.get("raw_action", "WAIT") or "WAIT").upper()
                reward = _safe_float(row.get("reward", 0.0))
                observed = _observed_potential(row, action, raw_action)
                executed = action in TRADE_ACTIONS
                record = records.setdefault(family, _new_record(family))
                record["rows"] += 1
                record["reward_sum"] += reward
                record["best_reward_sum"] += _safe_float(row.get("best_reward_training", 0.0))
                record["max_trade_readiness"] = max(record["max_trade_readiness"], _safe_float(row.get("trade_readiness", 0.0)))
                record["max_mature_transfer"] = max(record["max_mature_transfer"], _safe_float(row.get("mature_transfer", 0.0)))
                if executed:
                    record["executed"] += 1
                    if reward > 0.0:
                        record["positive_executed"] += 1
                    else:
                        record["burdened_executed"] += 1
                if observed:
                    record["observed_potential"] += 1
                if _safe_int(row.get("phase_active", 0)) > 0:
                    record["held_same_episode"] += 1

                visual_mcm_distance, tone_tension_distance = _sensor_distances(row)
                record["visual_mcm_distance_sum"] += visual_mcm_distance
                record["tone_tension_distance_sum"] += tone_tension_distance
                if executed:
                    record["visual_mcm_distance_executed_sum"] += visual_mcm_distance
                    record["tone_tension_distance_executed_sum"] += tone_tension_distance
                if observed:
                    record["visual_mcm_distance_observed_sum"] += visual_mcm_distance
                    record["tone_tension_distance_observed_sum"] += tone_tension_distance

                for field in SENSOR_FIELDS:
                    value = _safe_float(row.get(field, 0.0))
                    record[f"{field}_sum"] += value
                    if executed:
                        record[f"{field}_executed_sum"] += value
                    if observed:
                        record[f"{field}_observed_sum"] += value

    rows = []
    for record in records.values():
        total = max(1, _safe_int(record.get("rows", 0)))
        executed = max(1, _safe_int(record.get("executed", 0)))
        observed = max(1, _safe_int(record.get("observed_potential", 0)))
        item = {
            "family": record["family"],
            "rows": record["rows"],
            "executed": record["executed"],
            "positive_executed": record["positive_executed"],
            "burdened_executed": record["burdened_executed"],
            "observed_potential": record["observed_potential"],
            "held_same_episode": record["held_same_episode"],
            "reward_sum": round(record["reward_sum"], 6),
            "best_reward_sum": round(record["best_reward_sum"], 6),
            "max_trade_readiness": round(record["max_trade_readiness"], 6),
            "max_mature_transfer": round(record["max_mature_transfer"], 6),
            "visual_mcm_alignment_trace": round(_clip01(1.0 - (record["visual_mcm_distance_sum"] / total)), 6),
            "tone_tension_resonance_trace": round(_clip01(1.0 - (record["tone_tension_distance_sum"] / total)), 6),
            "executed_visual_mcm_alignment_trace": round(
                _clip01(1.0 - (record["visual_mcm_distance_executed_sum"] / executed)),
                6,
            ),
            "executed_tone_tension_resonance_trace": round(
                _clip01(1.0 - (record["tone_tension_distance_executed_sum"] / executed)),
                6,
            ),
            "observed_visual_mcm_alignment_trace": round(
                _clip01(1.0 - (record["visual_mcm_distance_observed_sum"] / observed)),
                6,
            ),
            "observed_tone_tension_resonance_trace": round(
                _clip01(1.0 - (record["tone_tension_distance_observed_sum"] / observed)),
                6,
            ),
        }
        for field in SENSOR_FIELDS:
            item[f"avg_{field}"] = round(record[f"{field}_sum"] / total, 6)
            item[f"executed_avg_{field}"] = round(record[f"{field}_executed_sum"] / executed, 6)
            item[f"observed_avg_{field}"] = round(record[f"{field}_observed_sum"] / observed, 6)
        rows.append(item)
    rows.sort(
        key=lambda item: (
            item["positive_executed"],
            item["reward_sum"],
            item["observed_potential"],
            item["visual_mcm_alignment_trace"],
            item["tone_tension_resonance_trace"],
        ),
        reverse=True,
    )
    return rows


def write_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_sensor_maturity.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    if rows:
        with (output_dir / "dio_mini_sensor_maturity.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze passive DIO mini sensor maturity")
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    rows = analyze(Path(args.debug_root))
    write_outputs(rows, Path(args.output_dir))
    for row in rows[:16]:
        print(
            f"family={row['family']} executed={row['executed']} observed={row['observed_potential']} "
            f"reward={row['reward_sum']:.4f} visual_mcm={row['visual_mcm_alignment_trace']:.4f} "
            f"tone_tension={row['tone_tension_resonance_trace']:.4f}"
        )


if __name__ == "__main__":
    main()
