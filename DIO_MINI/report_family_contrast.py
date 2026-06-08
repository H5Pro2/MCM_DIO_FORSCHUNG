"""Build a passive contrast report for selected DIO_MINI families.

The report compares carried, observed, and conflicted families from debug
episode files. It is diagnostic only: no memory writes, no motor influence.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


SENSOR_FIELDS = [
    "sehen_form_flow",
    "sehen_form_stability",
    "sehen_form_change",
    "hoeren_energy_tone",
    "hoeren_energy_shift",
    "fuehlen_mcm_coherence",
    "fuehlen_mcm_tension",
    "fuehlen_mcm_asymmetry",
]

COGNITIVE_FIELDS = [
    "trade_readiness",
    "associative_trade",
    "observation_trade_signal",
    "observation_trade_readiness",
    "maturity_gap",
    "mature_transfer",
    "observation_learning_pressure",
    "episode_binding_pressure",
    "episode_release_pressure",
]

SCORE_FIELDS = [
    "score_wait",
    "score_long",
    "score_short",
    "memory_bias_wait",
    "memory_bias_long",
    "memory_bias_short",
    "readiness_wait",
    "readiness_long",
    "readiness_short",
]

NUMERIC_FIELDS = SENSOR_FIELDS + COGNITIVE_FIELDS + SCORE_FIELDS + ["reward", "best_reward_training"]


def _safe_float(value: object) -> float:
    try:
        return float(value or 0.0)
    except Exception:
        return 0.0


def _safe_int(value: object) -> int:
    try:
        return int(value or 0)
    except Exception:
        return 0


def _iter_episode_rows(debug_root: Path) -> list[dict]:
    rows = []
    for path in sorted(debug_root.glob("**/episodes.csv")):
        run_id = path.parent.name.replace("dio_mini_lauf_", "")
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                item = dict(row)
                item["run"] = run_id
                rows.append(item)
    return rows


def _episode_state(row: dict) -> str:
    action = str(row.get("action", "WAIT") or "WAIT").upper()
    raw_action = str(row.get("raw_action", action) or action).upper()
    best_action = str(row.get("best_action_training", "WAIT") or "WAIT").upper()
    best_reward = _safe_float(row.get("best_reward_training", 0.0))
    phase_active = str(row.get("phase_active", "0") or "0") in ("1", "true", "True")
    if action in ("LONG", "SHORT"):
        return "executed_aligned" if action == best_action else "executed_misaligned"
    if action == "WAIT" and raw_action in ("LONG", "SHORT") and phase_active:
        return "held_trade_pressure"
    if best_action in ("LONG", "SHORT") and best_reward > 0.0:
        return "observed_trade_potential"
    return "quiet"


def _format_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "-"
    return "|".join(f"{key}:{value}" for key, value in sorted(counts.items()))


def _avg(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def _dominant_action(counts: dict[str, int]) -> str:
    if not counts:
        return "WAIT"
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0]


def _family_state(reward_sum: float, states: str, executed_count: int) -> str:
    if executed_count > 0 and reward_sum > 0.0 and "executed_misaligned" not in states:
        return "carried"
    if executed_count > 0 and reward_sum <= 0.0:
        return "conflict"
    if "executed_misaligned" in states and reward_sum <= 0.0:
        return "conflict"
    if "held_trade_pressure" in states:
        return "held"
    if "observed_trade_potential" in states:
        return "observed"
    return "quiet"


def _sentence(row: dict) -> str:
    family = str(row.get("family", "") or "-")
    state = str(row.get("family_state", "") or "-")
    action = str(row.get("dominant_action", "") or "-")
    if state == "carried":
        return f"{family}: wird mit {action} getragen; Sensorik und Konsequenz liegen zusammen."
    if state == "conflict":
        return f"{family}: erzeugt Handlung, aber die Konsequenz traegt noch nicht."
    if state == "held":
        return f"{family}: erzeugt Handelsspannung, bleibt aber gehalten."
    if state == "observed":
        return f"{family}: wird gesehen, bleibt als Potenzial ohne Handlung."
    return f"{family}: bleibt in dieser Lesung still oder unscharf."


def build_family_rows(debug_root: Path, selected_families: set[str] | None = None) -> list[dict]:
    grouped: dict[str, dict] = {}
    for row in _iter_episode_rows(debug_root):
        family = str(row.get("symbol_family", "") or "")
        if not family:
            continue
        if selected_families and family not in selected_families:
            continue
        action = str(row.get("action", "WAIT") or "WAIT").upper()
        state = _episode_state(row)
        item = grouped.setdefault(
            family,
            {
                "family": family,
                "runs": set(),
                "count": 0,
                "executed_count": 0,
                "actions": {},
                "states": {},
                "values": {field: [] for field in NUMERIC_FIELDS},
            },
        )
        item["runs"].add(str(row.get("run", "") or ""))
        item["count"] += 1
        item["actions"][action] = int(item["actions"].get(action, 0) or 0) + 1
        item["states"][state] = int(item["states"].get(state, 0) or 0) + 1
        if action in ("LONG", "SHORT"):
            item["executed_count"] += 1
        for field in NUMERIC_FIELDS:
            item["values"][field].append(_safe_float(row.get(field, 0.0)))

    rows = []
    for family, item in grouped.items():
        values = item["values"]
        actions = dict(item["actions"])
        states = _format_counts(dict(item["states"]))
        row = {
            "family": family,
            "run_count": len(item["runs"]),
            "episode_count": item["count"],
            "executed_count": item["executed_count"],
            "dominant_action": _dominant_action(actions),
            "actions": _format_counts(actions),
            "states": states,
            "reward_sum": round(sum(values["reward"]), 6),
            "best_reward_sum": round(sum(values["best_reward_training"]), 6),
        }
        for field in SENSOR_FIELDS + COGNITIVE_FIELDS + SCORE_FIELDS:
            row[f"{field}_avg"] = round(_avg(values[field]), 6)
        row["family_state"] = _family_state(float(row["reward_sum"]), states, _safe_int(row["executed_count"]))
        row["passive_sentence"] = _sentence(row)
        rows.append(row)

    rows.sort(
        key=lambda item: (
            str(item.get("family_state", "")) != "carried",
            str(item.get("family_state", "")) == "quiet",
            -_safe_float(item.get("reward_sum", 0.0)),
            str(item.get("family", "")),
        )
    )
    return rows


def _group_summary(rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = {}
    for row in rows:
        grouped.setdefault(str(row.get("family_state", "") or "unknown"), []).append(row)
    summaries = []
    for state, items in sorted(grouped.items()):
        summary = {
            "family_state": state,
            "family_count": len(items),
            "episode_count": sum(_safe_int(item.get("episode_count", 0)) for item in items),
            "executed_count": sum(_safe_int(item.get("executed_count", 0)) for item in items),
            "reward_sum": round(sum(_safe_float(item.get("reward_sum", 0.0)) for item in items), 6),
            "families": "|".join(str(item.get("family", "")) for item in items),
        }
        for field in SENSOR_FIELDS + COGNITIVE_FIELDS:
            key = f"{field}_avg"
            summary[key] = round(_avg([_safe_float(item.get(key, 0.0)) for item in items]), 6)
        summaries.append(summary)
    summaries.sort(key=lambda item: (-_safe_float(item.get("reward_sum", 0.0)), str(item.get("family_state", ""))))
    return summaries


def _write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = _group_summary(rows)
    family_csv = output_dir / "dio_mini_family_contrast.csv"
    summary_csv = output_dir / "dio_mini_family_contrast_summary.csv"
    json_path = output_dir / "dio_mini_family_contrast.json"
    md_path = output_dir / "dio_mini_family_contrast.md"

    family_fields = [
        "family",
        "family_state",
        "run_count",
        "episode_count",
        "executed_count",
        "dominant_action",
        "actions",
        "states",
        "reward_sum",
        "best_reward_sum",
    ]
    family_fields += [f"{field}_avg" for field in SENSOR_FIELDS + COGNITIVE_FIELDS + SCORE_FIELDS]
    family_fields.append("passive_sentence")
    _write_csv(family_csv, rows, family_fields)

    summary_fields = ["family_state", "family_count", "episode_count", "executed_count", "reward_sum", "families"]
    summary_fields += [f"{field}_avg" for field in SENSOR_FIELDS + COGNITIVE_FIELDS]
    _write_csv(summary_csv, summary, summary_fields)
    json_path.write_text(json.dumps({"families": rows, "summary": summary}, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Family Contrast", ""]
    lines.append("## Gruppen")
    lines.append("")
    for row in summary:
        lines.extend(
            [
                f"### {row['family_state']}",
                f"- families: {row['families']}",
                f"- episodes / executed: {row['episode_count']} / {row['executed_count']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- sehen_stability_avg: {float(row['sehen_form_stability_avg']):.6f}",
                f"- hoeren_tone_avg: {float(row['hoeren_energy_tone_avg']):.6f}",
                f"- mcm_coherence_avg: {float(row['fuehlen_mcm_coherence_avg']):.6f}",
                f"- mcm_tension_avg: {float(row['fuehlen_mcm_tension_avg']):.6f}",
                "",
            ]
        )
    lines.append("## Familien")
    lines.append("")
    for row in rows:
        lines.extend(
            [
                f"### {row['family']}",
                f"- state: {row['family_state']}",
                f"- action: {row['dominant_action']} ({row['actions']})",
                f"- states: {row['states']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- sehen: flow={float(row['sehen_form_flow_avg']):.6f}, stability={float(row['sehen_form_stability_avg']):.6f}, change={float(row['sehen_form_change_avg']):.6f}",
                f"- hoeren: tone={float(row['hoeren_energy_tone_avg']):.6f}, shift={float(row['hoeren_energy_shift_avg']):.6f}",
                f"- fuehlen: coherence={float(row['fuehlen_mcm_coherence_avg']):.6f}, tension={float(row['fuehlen_mcm_tension_avg']):.6f}, asymmetry={float(row['fuehlen_mcm_asymmetry_avg']):.6f}",
                f"- passive_sentence: {row['passive_sentence']}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive DIO_MINI family contrast report")
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--family", action="append", default=[])
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    selected = {str(item).strip() for item in args.family if str(item).strip()} or None
    rows = build_family_rows(Path(args.debug_root), selected_families=selected)
    write_outputs(rows, Path(args.output_dir))
    print(f"families={len(rows)}")
    for row in rows[:25]:
        print(
            f"{row['family']} state={row['family_state']} "
            f"action={row['dominant_action']} reward={row['reward_sum']} "
            f"seen_stability={row['sehen_form_stability_avg']} "
            f"mcm_tension={row['fuehlen_mcm_tension_avg']}"
        )


if __name__ == "__main__":
    main()
