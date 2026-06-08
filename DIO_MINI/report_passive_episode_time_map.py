"""Build a passive episode time map for Mini-DIO.

The report reads Mini-DIO episodes.csv files and summarizes how symbol
families appear over run/tick time. It is diagnostic only: no memory writes, no
action influence, no gates.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


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


def _parse_source(value: str) -> tuple[str, Path]:
    if "=" in value:
        label, path = value.split("=", 1)
        return label.strip(), Path(path.strip())
    path = Path(value)
    return path.name, path


def _episode_files(debug_root: Path) -> list[Path]:
    if debug_root.is_file() and debug_root.name == "episodes.csv":
        return [debug_root]
    return sorted(debug_root.glob("dio_mini_lauf_*/episodes.csv"))


def _read_episode_rows(label: str, debug_root: Path) -> list[dict]:
    rows: list[dict] = []
    for path in _episode_files(debug_root):
        run_name = path.parent.name.replace("dio_mini_lauf_", "")
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                item = dict(row)
                item["source_label"] = label
                item["debug_root"] = str(debug_root)
                item["run"] = str(item.get("run", "") or run_name)
                rows.append(item)
    rows.sort(key=lambda item: (str(item.get("source_label", "")), _safe_int(item.get("run")), _safe_int(item.get("tick"))))
    return rows


def _phase_time_state(row: dict) -> str:
    phase_age = _safe_int(row.get("phase_age"))
    phase_active = _safe_int(row.get("phase_active"))
    relation = str(row.get("episode_relation", "") or "")
    action = str(row.get("action", "WAIT") or "WAIT").upper()
    outcome = str(row.get("outcome_event", "NO_TRADE") or "NO_TRADE").upper()
    if phase_active:
        return "active_afterimage_contact"
    if phase_age >= 9999:
        return "no_prior_phase"
    if action in ("LONG", "SHORT") and outcome != "NO_TRADE":
        return "executed_temporal_contact"
    if relation == "different_contact":
        return "different_contact_afterimage"
    if relation == "new_contact":
        return "released_prior_phase"
    return "separated_observation_contact"


def _time_sentence(row: dict) -> str:
    family = str(row.get("symbol_family", "") or "-")
    source = str(row.get("source_label", "") or "-")
    run = str(row.get("run", "") or "-")
    tick = str(row.get("tick", "") or "-")
    action = str(row.get("action", "WAIT") or "WAIT").upper()
    outcome = str(row.get("outcome_event", "NO_TRADE") or "NO_TRADE").upper()
    state = str(row.get("phase_time_state", "") or "-")
    reward = _safe_float(row.get("event_reward") or row.get("reward"))
    return f"{source} run={run} tick={tick}: {family} {action}/{outcome}; Zeitspur={state}; reward={reward:.6f}."


def build_detail(sources: list[tuple[str, Path]]) -> list[dict]:
    detail: list[dict] = []
    for label, debug_root in sources:
        for row in _read_episode_rows(label, debug_root):
            phase_age = _safe_int(row.get("phase_age"))
            finite_phase_age = phase_age if phase_age < 9999 else ""
            item = {
                "source_label": str(row.get("source_label", "") or ""),
                "run": str(row.get("run", "") or ""),
                "tick": str(row.get("tick", "") or ""),
                "timestamp_ms": str(row.get("timestamp_ms", "") or ""),
                "symbol": str(row.get("symbol", "") or ""),
                "symbol_family": str(row.get("symbol_family", "") or ""),
                "family_action": f"{str(row.get('symbol_family', '') or '')}:{str(row.get('action', 'WAIT') or 'WAIT').upper()}",
                "action": str(row.get("action", "WAIT") or "WAIT").upper(),
                "raw_action": str(row.get("raw_action", "WAIT") or "WAIT").upper(),
                "outcome_event": str(row.get("outcome_event", "NO_TRADE") or "NO_TRADE").upper(),
                "phase_time_state": _phase_time_state(row),
                "episode_relation": str(row.get("episode_relation", "") or ""),
                "phase_active": _safe_int(row.get("phase_active")),
                "phase_age": phase_age,
                "finite_phase_age": finite_phase_age,
                "phase_distance": round(_safe_float(row.get("phase_distance")), 6),
                "episode_binding_pressure": round(_safe_float(row.get("episode_binding_pressure")), 6),
                "episode_release_pressure": round(_safe_float(row.get("episode_release_pressure")), 6),
                "bars_held": _safe_int(row.get("bars_held")),
                "event_reward": round(_safe_float(row.get("event_reward") or row.get("reward")), 6),
                "reward": round(_safe_float(row.get("reward")), 6),
                "best_action_training": str(row.get("best_action_training", "WAIT") or "WAIT").upper(),
                "sehen_form_flow": round(_safe_float(row.get("sehen_form_flow")), 6),
                "hoeren_energy_tone": round(_safe_float(row.get("hoeren_energy_tone")), 6),
                "fuehlen_mcm_coherence": round(_safe_float(row.get("fuehlen_mcm_coherence")), 6),
                "passive_only": 1,
                "influences_action": 0,
                "is_gate": 0,
                "is_motoric": 0,
            }
            item["time_sentence"] = _time_sentence(item)
            detail.append(item)
    detail.sort(key=lambda item: (str(item.get("source_label", "")), _safe_int(item.get("run")), _safe_int(item.get("tick"))))
    return detail


def _avg(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def _count_values(rows: list[dict], key: str) -> str:
    counts: dict[str, int] = {}
    for row in rows:
        value = str(row.get(key, "") or "-")
        counts[value] = counts.get(value, 0) + 1
    return "|".join(f"{key}:{value}" for key, value in sorted(counts.items()))


def _source_order_index(label: str, source_order: list[str]) -> int:
    try:
        return source_order.index(label)
    except ValueError:
        return len(source_order)


def _freshness_state(source_labels: list[str], source_order: list[str]) -> str:
    if not source_labels:
        return "time_unseen"
    latest = source_order[-1] if source_order else source_labels[-1]
    if latest in source_labels and len(set(source_labels)) > 1:
        return "fresh_recurrent_episode_trace"
    if latest in source_labels:
        return "fresh_local_episode_trace"
    if len(set(source_labels)) > 1:
        return "older_recurrent_episode_trace"
    return "older_local_episode_trace"


def build_summary(detail: list[dict], source_order: list[str]) -> list[dict]:
    grouped: dict[str, list[dict]] = {}
    for row in detail:
        family_action = str(row.get("family_action", "") or "")
        grouped.setdefault(family_action, []).append(row)

    summary: list[dict] = []
    for family_action, rows in grouped.items():
        rows = sorted(rows, key=lambda item: (_source_order_index(str(item.get("source_label", "")), source_order), _safe_int(item.get("run")), _safe_int(item.get("tick"))))
        source_labels = sorted({str(row.get("source_label", "") or "") for row in rows}, key=lambda item: _source_order_index(item, source_order))
        finite_phase_ages = [_safe_float(row.get("finite_phase_age")) for row in rows if str(row.get("finite_phase_age", "")) != ""]
        bars = [_safe_float(row.get("bars_held")) for row in rows if _safe_float(row.get("bars_held")) > 0.0]
        event_rewards = [_safe_float(row.get("event_reward")) for row in rows]
        ticks = [_safe_int(row.get("tick")) for row in rows]
        item = {
            "family_action": family_action,
            "symbol_family": str(rows[0].get("symbol_family", "") or ""),
            "action": str(rows[0].get("action", "") or ""),
            "freshness_state": _freshness_state(source_labels, source_order),
            "source_count": len(source_labels),
            "source_labels": ",".join(source_labels),
            "run_count": len({str(row.get("run", "") or "") for row in rows}),
            "episode_count": len(rows),
            "first_source": source_labels[0] if source_labels else "",
            "last_source": source_labels[-1] if source_labels else "",
            "first_tick": min(ticks) if ticks else 0,
            "last_tick": max(ticks) if ticks else 0,
            "tick_span": (max(ticks) - min(ticks)) if ticks else 0,
            "phase_time_states": _count_values(rows, "phase_time_state"),
            "outcome_events": _count_values(rows, "outcome_event"),
            "phase_active_count": sum(_safe_int(row.get("phase_active")) for row in rows),
            "avg_finite_phase_age": round(_avg(finite_phase_ages), 6) if finite_phase_ages else "",
            "avg_bars_held": round(_avg(bars), 6) if bars else "",
            "event_reward_sum": round(sum(event_rewards), 6),
            "avg_event_reward": round(_avg(event_rewards), 6),
            "avg_phase_distance": round(_avg([_safe_float(row.get("phase_distance")) for row in rows]), 6),
            "avg_binding_pressure": round(_avg([_safe_float(row.get("episode_binding_pressure")) for row in rows]), 6),
            "avg_release_pressure": round(_avg([_safe_float(row.get("episode_release_pressure")) for row in rows]), 6),
            "passive_only": 1,
            "influences_action": 0,
            "is_gate": 0,
            "is_motoric": 0,
        }
        item["time_summary_sentence"] = (
            f"{family_action}: {item['freshness_state']}; Quellen={item['source_labels'] or '-'}; "
            f"Episoden={item['episode_count']}; Outcome={item['outcome_events']}; "
            f"RewardSumme={float(item['event_reward_sum']):.6f}."
        )
        summary.append(item)
    summary.sort(
        key=lambda item: (
            str(item.get("freshness_state", "")) not in ("fresh_recurrent_episode_trace", "fresh_local_episode_trace"),
            -_safe_int(item.get("source_count")),
            -_safe_float(item.get("event_reward_sum")),
            str(item.get("family_action", "")),
        )
    )
    return summary


def _write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path, sources: list[tuple[str, Path]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_passive_episode_time_map_detail.csv"
    summary_path = output_dir / "dio_mini_passive_episode_time_map_summary.csv"
    json_path = output_dir / "dio_mini_passive_episode_time_map.json"
    md_path = output_dir / "dio_mini_passive_episode_time_map.md"
    txt_path = output_dir / "dio_mini_passive_episode_time_map.txt"

    detail_fields = list(detail[0].keys()) if detail else [
        "source_label",
        "run",
        "tick",
        "symbol_family",
        "action",
        "outcome_event",
        "phase_time_state",
        "passive_only",
    ]
    summary_fields = list(summary[0].keys()) if summary else [
        "family_action",
        "freshness_state",
        "source_labels",
        "episode_count",
        "outcome_events",
        "event_reward_sum",
        "passive_only",
    ]
    _write_csv(detail_path, detail, detail_fields)
    _write_csv(summary_path, summary, summary_fields)
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_episode_time_map.v1",
                "sources": [{"label": label, "path": str(path)} for label, path in sources],
                "boundary": {
                    "passive_only": True,
                    "writes_training_memory": False,
                    "influences_action": False,
                    "is_gate": False,
                    "is_motoric": False,
                    "read_by_mini_dio": False,
                },
                "detail_count": len(detail),
                "summary_count": len(summary),
                "summary": summary,
                "detail": detail,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = ["# DIO Mini Passive Episode Time Map", ""]
    lines.extend(["## Grenze", "- passiv", "- kein Memory-Schreiben", "- keine Motorik", "- kein Gate", ""])
    lines.extend(["## Quellen"])
    for label, path in sources:
        lines.append(f"- {label}: {path}")
    lines.extend(["", "## Zusammenfassung"])
    if not summary:
        lines.append("- keine Zeitspuren")
    for row in summary[:80]:
        lines.append(f"- {row['time_summary_sentence']}")
    lines.extend(["", "## Detailauszug"])
    for row in detail[:80]:
        lines.append(f"- {row['time_sentence']}")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    txt_path.write_text("\n".join(row["time_summary_sentence"] for row in summary), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive Mini-DIO episode time map")
    parser.add_argument("--source", action="append", required=True, help="label=debug_root or debug_root; can be repeated")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    sources = [_parse_source(value) for value in args.source]
    detail = build_detail(sources)
    source_order = [label for label, _ in sources]
    summary = build_summary(detail, source_order)
    write_outputs(detail, summary, Path(args.output_dir), sources)
    print(f"episode_time_detail={len(detail)} summary={len(summary)}")
    for row in summary[:20]:
        print(
            f"{row['freshness_state']} {row['family_action']} "
            f"sources={row['source_labels']} episodes={row['episode_count']} reward={row['event_reward_sum']}"
        )


if __name__ == "__main__":
    main()
