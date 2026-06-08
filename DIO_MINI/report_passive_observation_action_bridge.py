"""Bridge passive Mini-DIO observations to later real action outcomes.

This is a diagnostic report only. It compares:

- WAIT moments where a later possible action was visible in hindsight
- real LONG/SHORT actions on the same symbol family and direction

It does not train memory, influence action, or create gates.
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


def _parse_source(spec: str) -> tuple[str, Path]:
    if "=" in spec:
        label, path = spec.split("=", 1)
        return label.strip() or Path(path).name, Path(path)
    path = Path(spec)
    return path.name, path


def _new_bucket(label: str, family: str, action: str) -> dict:
    return {
        "source_label": label,
        "symbol_family": family,
        "action": action,
        "family_action": f"{family}:{action}",
        "passive_wait_traces": 0,
        "passive_potential_sum": 0.0,
        "passive_pressure_sum": 0.0,
        "real_action_traces": 0,
        "tp_count": 0,
        "sl_count": 0,
        "no_trade_count": 0,
        "other_outcome_count": 0,
        "real_reward_sum": 0.0,
        "event_reward_sum": 0.0,
        "passive_runs": set(),
        "action_runs": set(),
        "sense_sums": {field: 0.0 for field in SENSE_FIELDS},
        "sense_count": 0,
    }


def _bridge_state(bucket: dict) -> str:
    passive = int(bucket["passive_wait_traces"])
    actions = int(bucket["real_action_traces"])
    tp_count = int(bucket["tp_count"])
    sl_count = int(bucket["sl_count"])
    reward = float(bucket["real_reward_sum"])
    if passive > 0 and actions == 0:
        return "passive_seen_not_yet_acted"
    if passive == 0 and actions > 0:
        return "acted_without_passive_trace"
    if passive > 0 and actions > 0 and tp_count > sl_count and reward > 0.0:
        return "passive_seen_and_real_action_carried"
    if passive > 0 and actions > 0 and sl_count >= tp_count:
        return "passive_seen_but_real_action_burdened"
    if passive > 0 and actions > 0:
        return "passive_seen_and_real_action_mixed"
    return "open_trace"


def build_report(sources: list[tuple[str, Path]]) -> tuple[list[dict], list[dict]]:
    detail: list[dict] = []
    buckets: dict[tuple[str, str, str], dict] = {}

    for label, debug_root in sources:
        for episode_path in _episode_paths(debug_root):
            run_name = episode_path.parent.name
            for row in _read_csv(episode_path):
                family = str(row.get("symbol_family", "") or row.get("symbol", "") or "-")
                action = str(row.get("action", "") or "").upper()
                best_action = str(row.get("best_action_training", "") or "").upper()
                best_reward = _safe_float(row.get("best_reward_training"))
                outcome = str(row.get("outcome_event", "") or "").upper()
                event_reward = _safe_float(row.get("event_reward"))
                reward = _safe_float(row.get("reward"))

                if action == "WAIT" and best_action in ("LONG", "SHORT") and best_reward > 0.0:
                    key = (label, family, best_action)
                    bucket = buckets.setdefault(key, _new_bucket(label, family, best_action))
                    bucket["passive_wait_traces"] += 1
                    bucket["passive_potential_sum"] += best_reward
                    bucket["passive_pressure_sum"] += _safe_float(row.get("observation_learning_pressure"))
                    bucket["passive_runs"].add(run_name)
                    for field in SENSE_FIELDS:
                        bucket["sense_sums"][field] += _safe_float(row.get(field))
                    bucket["sense_count"] += 1
                    detail.append(
                        {
                            "source_label": label,
                            "run": run_name,
                            "tick": str(row.get("tick", "") or ""),
                            "symbol_family": family,
                            "action": "WAIT",
                            "observed_possible_action": best_action,
                            "trace_kind": "passive_wait_possible_action",
                            "outcome_event": outcome,
                            "potential_reward": round(best_reward, 9),
                            "real_reward": round(reward, 9),
                            "passive_only": 1,
                        }
                    )
                    continue

                if action in ("LONG", "SHORT"):
                    key = (label, family, action)
                    bucket = buckets.setdefault(key, _new_bucket(label, family, action))
                    bucket["real_action_traces"] += 1
                    bucket["real_reward_sum"] += reward
                    bucket["event_reward_sum"] += event_reward
                    bucket["action_runs"].add(run_name)
                    if outcome == "TP":
                        bucket["tp_count"] += 1
                    elif outcome == "SL":
                        bucket["sl_count"] += 1
                    elif outcome == "NO_TRADE":
                        bucket["no_trade_count"] += 1
                    else:
                        bucket["other_outcome_count"] += 1
                    for field in SENSE_FIELDS:
                        bucket["sense_sums"][field] += _safe_float(row.get(field))
                    bucket["sense_count"] += 1
                    detail.append(
                        {
                            "source_label": label,
                            "run": run_name,
                            "tick": str(row.get("tick", "") or ""),
                            "symbol_family": family,
                            "action": action,
                            "observed_possible_action": "",
                            "trace_kind": "real_action_outcome",
                            "outcome_event": outcome,
                            "potential_reward": round(best_reward, 9),
                            "real_reward": round(reward, 9),
                            "passive_only": 1,
                        }
                    )

    summary: list[dict] = []
    for bucket in buckets.values():
        sense_count = max(1, int(bucket["sense_count"]))
        passive_count = int(bucket["passive_wait_traces"])
        item = {
            "source_label": bucket["source_label"],
            "symbol_family": bucket["symbol_family"],
            "action": bucket["action"],
            "family_action": bucket["family_action"],
            "passive_wait_traces": passive_count,
            "passive_potential_sum": round(float(bucket["passive_potential_sum"]), 9),
            "avg_passive_pressure": round(float(bucket["passive_pressure_sum"]) / max(1, passive_count), 9),
            "real_action_traces": int(bucket["real_action_traces"]),
            "tp_count": int(bucket["tp_count"]),
            "sl_count": int(bucket["sl_count"]),
            "no_trade_count": int(bucket["no_trade_count"]),
            "other_outcome_count": int(bucket["other_outcome_count"]),
            "real_reward_sum": round(float(bucket["real_reward_sum"]), 9),
            "event_reward_sum": round(float(bucket["event_reward_sum"]), 9),
            "passive_runs": ",".join(sorted(bucket["passive_runs"])),
            "action_runs": ",".join(sorted(bucket["action_runs"])),
            "bridge_state": _bridge_state(bucket),
            "passive_only": 1,
        }
        for field in SENSE_FIELDS:
            item[f"avg_{field}"] = round(float(bucket["sense_sums"][field]) / sense_count, 9)
        summary.append(item)

    detail.sort(key=lambda item: (str(item["source_label"]), str(item["run"]), int(item["tick"] or 0), str(item["symbol_family"])))
    summary.sort(
        key=lambda item: (
            str(item["source_label"]),
            -int(item["real_action_traces"]),
            -int(item["passive_wait_traces"]),
            str(item["family_action"]),
        )
    )
    return detail, summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(detail: list[dict], summary: list[dict], sources: list[tuple[str, Path]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_observation_action_bridge.csv"
    summary_csv = output_dir / "dio_mini_passive_observation_action_bridge_summary.csv"
    json_path = output_dir / "dio_mini_passive_observation_action_bridge.json"
    md_path = output_dir / "dio_mini_passive_observation_action_bridge.md"

    _write_csv(detail_csv, detail, ["source_label", "run", "tick", "symbol_family", "trace_kind"])
    _write_csv(summary_csv, summary, ["source_label", "symbol_family", "action", "bridge_state"])
    json_path.write_text(
        json.dumps(
            {
                "sources": [{"label": label, "path": str(path)} for label, path in sources],
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

    lines = ["# DIO Mini Passive Observation Action Bridge", ""]
    lines.append("## Quellen")
    for label, path in sources:
        lines.append(f"- {label}: {path}")
    lines.extend(["", "## Zusammenfassung"])
    if not summary:
        lines.append("- keine Brueckenspuren")
    for row in summary[:30]:
        lines.append(
            f"- {row['source_label']} {row['family_action']}: passive={row['passive_wait_traces']} "
            f"actions={row['real_action_traces']} TP={row['tp_count']} SL={row['sl_count']} "
            f"reward={row['real_reward_sum']} state={row['bridge_state']}"
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Brueckendiagnose",
            "- keine Handlung",
            "- kein Trainingsmemory",
            "- kein Gate",
            "- kein Zukunftslehrer",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bridge passive Mini-DIO observations to real actions")
    parser.add_argument("--source", action="append", required=True, help="label=debug_root or debug_root; can be repeated")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    sources = [_parse_source(spec) for spec in args.source]
    detail, summary = build_report(sources)
    write_outputs(detail, summary, sources, Path(args.output_dir))
    print(f"passive_observation_action_bridge_rows={len(detail)} summary={len(summary)}")
    for row in summary[:12]:
        print(
            f"{row['source_label']} {row['family_action']} passive={row['passive_wait_traces']} "
            f"actions={row['real_action_traces']} TP={row['tp_count']} SL={row['sl_count']} "
            f"state={row['bridge_state']}"
        )


if __name__ == "__main__":
    main()
