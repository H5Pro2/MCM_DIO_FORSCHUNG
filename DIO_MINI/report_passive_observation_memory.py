"""Build a passive observation-memory map for Mini-DIO.

The report records moments where DIO did not act, but later evaluation shows
that a possible action existed. This is not a future teacher:

- no training memory is written
- no neuron field is changed
- no action is influenced

It only preserves the diagnostic statement:
"I did not act here; later this looked like a possible contact."
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


def _safe_float(value: object) -> float:
    try:
        value = float(value or 0.0)
    except Exception:
        value = 0.0
    if value != value:
        value = 0.0
    return value


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _episode_paths(debug_root: Path) -> list[Path]:
    return sorted(debug_root.glob("**/episodes.csv"))


def _state_for(count: int, potential_reward_sum: float, avg_pressure: float) -> str:
    if count <= 1:
        return "passive_observation_single_trace"
    if potential_reward_sum > 0.0 and avg_pressure > 0.0:
        return "passive_observation_repeated_potential_trace"
    if potential_reward_sum > 0.0:
        return "passive_observation_repeated_low_pressure_trace"
    return "passive_observation_repeated_open_trace"


def build_rows(debug_root: Path) -> tuple[list[dict], list[dict]]:
    detail: list[dict] = []
    groups: dict[tuple[str, str], dict] = {}
    for episode_path in _episode_paths(debug_root):
        run_name = episode_path.parent.name
        for row in _read_csv(episode_path):
            action = str(row.get("action", "") or "").upper()
            best_action = str(row.get("best_action_training", "") or "").upper()
            best_reward = _safe_float(row.get("best_reward_training"))
            if action != "WAIT" or best_action not in ("LONG", "SHORT") or best_reward <= 0.0:
                continue
            family = str(row.get("symbol_family", "") or row.get("symbol", "") or "-")
            key = (family, best_action)
            item = {
                "run": run_name,
                "tick": str(row.get("tick", "") or ""),
                "timestamp_ms": str(row.get("timestamp_ms", "") or ""),
                "symbol": str(row.get("symbol", "") or ""),
                "symbol_family": family,
                "observed_possible_action": best_action,
                "actual_action": action,
                "outcome_event": str(row.get("outcome_event", "") or ""),
                "potential_reward": round(best_reward, 9),
                "observation_learning_pressure": round(_safe_float(row.get("observation_learning_pressure")), 9),
                "phase_active": int(_safe_float(row.get("phase_active"))),
                "phase_relation": str(row.get("episode_relation", "") or ""),
                "passive_only": 1,
            }
            for field in SENSE_FIELDS:
                item[field] = round(_safe_float(row.get(field)), 9)
            detail.append(item)

            group = groups.setdefault(
                key,
                {
                    "symbol_family": family,
                    "observed_possible_action": best_action,
                    "trace_count": 0,
                    "potential_reward_sum": 0.0,
                    "observation_pressure_sum": 0.0,
                    "phase_active_count": 0,
                    "runs": set(),
                    "sense_sums": {field: 0.0 for field in SENSE_FIELDS},
                    "symbols": set(),
                },
            )
            group["trace_count"] += 1
            group["potential_reward_sum"] += best_reward
            group["observation_pressure_sum"] += item["observation_learning_pressure"]
            group["phase_active_count"] += int(item["phase_active"])
            group["runs"].add(run_name)
            group["symbols"].add(item["symbol"])
            for field in SENSE_FIELDS:
                group["sense_sums"][field] += float(item[field])

    summary: list[dict] = []
    for group in groups.values():
        count = max(1, int(group["trace_count"]))
        avg_pressure = float(group["observation_pressure_sum"]) / count
        potential_reward_sum = float(group["potential_reward_sum"])
        state = _state_for(count, potential_reward_sum, avg_pressure)
        item = {
            "symbol_family": group["symbol_family"],
            "observed_possible_action": group["observed_possible_action"],
            "passive_observation_state": state,
            "trace_count": count,
            "run_count": len(group["runs"]),
            "potential_reward_sum": round(potential_reward_sum, 9),
            "avg_potential_reward": round(potential_reward_sum / count, 9),
            "avg_observation_learning_pressure": round(avg_pressure, 9),
            "phase_active_count": int(group["phase_active_count"]),
            "symbols": ",".join(sorted(group["symbols"])),
            "runs": ",".join(sorted(group["runs"])),
            "inner_observation_note": "",
            "passive_only": 1,
        }
        for field in SENSE_FIELDS:
            item[f"avg_{field}"] = round(float(group["sense_sums"][field]) / count, 9)
        item["inner_observation_note"] = (
            f"{item['symbol_family']} wurde {count}x nicht gehandelt; "
            f"spaeter lag {item['observed_possible_action']} als Moeglichkeit im Raum "
            f"(Potenzial={item['potential_reward_sum']:.6f}, Druck={item['avg_observation_learning_pressure']:.6f})."
        )
        summary.append(item)

    detail.sort(key=lambda item: (str(item["run"]), int(item["tick"] or 0), str(item["symbol_family"])))
    summary.sort(
        key=lambda item: (
            -int(item["trace_count"]),
            -float(item["potential_reward_sum"]),
            str(item["symbol_family"]),
            str(item["observed_possible_action"]),
        )
    )
    return detail, summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path, debug_root: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_observation_memory.csv"
    summary_csv = output_dir / "dio_mini_passive_observation_memory_summary.csv"
    json_path = output_dir / "dio_mini_passive_observation_memory.json"
    md_path = output_dir / "dio_mini_passive_observation_memory.md"
    txt_path = output_dir / "dio_mini_passive_observation_memory.txt"

    _write_csv(detail_csv, detail, ["run", "tick", "symbol_family", "observed_possible_action"])
    _write_csv(summary_csv, summary, ["symbol_family", "observed_possible_action", "trace_count"])
    json_path.write_text(
        json.dumps(
            {
                "debug_root": str(debug_root),
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

    lines = ["# DIO Mini Passive Observation Memory", "", f"- debug_root: {debug_root}", ""]
    lines.append("## Zusammenfassung")
    if not summary:
        lines.append("- keine passive Beobachtungsmoeglichkeit")
    for row in summary:
        lines.append(
            f"- {row['symbol_family']} / {row['observed_possible_action']}: "
            f"state={row['passive_observation_state']} traces={row['trace_count']} "
            f"runs={row['run_count']} potential={row['potential_reward_sum']} "
            f"pressure={row['avg_observation_learning_pressure']}"
        )
    lines.extend(["", "## Innere Notizen"])
    txt_lines = []
    for row in summary:
        note = str(row["inner_observation_note"])
        lines.append(f"- {note}")
        txt_lines.append(note)
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Beobachtungs-Erinnerung",
            "- kein Trainingsmemory",
            "- keine Motorik",
            "- kein Gate",
            "- kein Zukunftslehrer",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    txt_path.write_text("\n".join(txt_lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive Mini-DIO observation memory map")
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    detail, summary = build_rows(Path(args.debug_root))
    write_outputs(detail, summary, Path(args.output_dir), Path(args.debug_root))
    print(f"passive_observation_memory_rows={len(detail)} summary={len(summary)}")
    for row in summary[:12]:
        print(
            f"{row['symbol_family']} {row['observed_possible_action']} "
            f"traces={row['trace_count']} potential={row['potential_reward_sum']} "
            f"state={row['passive_observation_state']}"
        )


if __name__ == "__main__":
    main()
