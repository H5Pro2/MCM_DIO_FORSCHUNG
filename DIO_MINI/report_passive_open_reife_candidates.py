"""Report Mini-DIO passive traces that carried but are not inner-mature yet.

This diagnostic reads the passive time+maturity join and extracts a small
watchlist. It does not write memory and is not read by Mini-DIO motorics.
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
        return 0.0
    return value


def _safe_int(value: object) -> int:
    try:
        return int(float(value or 0))
    except Exception:
        return 0


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _avg(value: object) -> float:
    text = str(value or "").strip()
    if not text:
        return 0.0
    return _safe_float(text)


def _candidate_state(row: dict) -> str:
    state = str(row.get("time_maturity_state", "") or "")
    if state == "fresh_carried_without_inner_memory":
        return "open_inner_reife_candidate"
    if state == "fresh_carried_from_inner_bridge":
        return "already_inner_bridged_reference"
    if state == "burden_without_inner_memory":
        return "burden_reife_watch"
    if state == "older_trace_without_inner_memory":
        return "older_open_trace_watch"
    if state == "fresh_waiting_without_inner_memory":
        return "fresh_waiting_context"
    return "other_passive_trace"


def _observation_weight(row: dict, candidate_state: str) -> float:
    reward = _safe_float(row.get("event_reward_sum"))
    source_count = _safe_int(row.get("episode_source_count"))
    episode_count = _safe_int(row.get("episode_count"))
    avg_reward = _safe_float(row.get("avg_event_reward"))
    bridge_bonus = 0.8 if str(row.get("bridge_passive_family_action", "") or "") else 0.0
    state_bonus = {
        "open_inner_reife_candidate": 2.0,
        "already_inner_bridged_reference": 1.5,
        "burden_reife_watch": 1.2,
        "older_open_trace_watch": 0.4,
        "fresh_waiting_context": 0.1,
    }.get(candidate_state, 0.0)
    return round((reward * 0.30) + (source_count * 0.55) + (episode_count * 0.06) + avg_reward + bridge_bonus + state_bonus, 6)


def _note(row: dict) -> str:
    candidate_state = str(row.get("open_reife_candidate_state", "") or "")
    family_action = str(row.get("family_action", "") or "-")
    sources = str(row.get("episode_source_labels", "") or "-")
    reward = _safe_float(row.get("event_reward_sum"))
    outcomes = str(row.get("outcome_events", "") or "-")
    bridge = str(row.get("bridge_passive_family_action", "") or "")
    if candidate_state == "open_inner_reife_candidate":
        return (
            f"{family_action}: reale frische Tragspur ohne innere Reife. "
            f"Weiter passiv beobachten; Quellen={sources}; outcomes={outcomes}; reward={reward:.6f}."
        )
    if candidate_state == "already_inner_bridged_reference":
        return (
            f"{family_action}: bereits ueber innere Reifebruecke lesbar"
            f" ({bridge or '-'}); Quellen={sources}; reward={reward:.6f}."
        )
    if candidate_state == "burden_reife_watch":
        return (
            f"{family_action}: belastete Spur ohne innere Reife. "
            f"Nicht verdraengen, aber passiv als Vorsichtsspur lesen; Quellen={sources}; reward={reward:.6f}."
        )
    if candidate_state == "older_open_trace_watch":
        return f"{family_action}: alte offene Zeitspur ohne aktuelle Konsequenz; Quellen={sources}."
    if candidate_state == "fresh_waiting_context":
        return f"{family_action}: frischer Wartungskontext; keine Handlung, aber Zeitumgebung bleibt sichtbar; Quellen={sources}."
    return f"{family_action}: passive Spur; Quellen={sources}; reward={reward:.6f}."


def build_rows(join_rows: list[dict]) -> list[dict]:
    rows: list[dict] = []
    seen: set[tuple] = set()
    for source_row in join_rows:
        key = (
            str(source_row.get("family_action", "") or ""),
            str(source_row.get("time_maturity_state", "") or ""),
            str(source_row.get("episode_source_labels", "") or ""),
            str(source_row.get("outcome_events", "") or ""),
            str(source_row.get("event_reward_sum", "") or ""),
        )
        if key in seen:
            continue
        seen.add(key)

        candidate_state = _candidate_state(source_row)
        if candidate_state == "other_passive_trace":
            continue
        row = {
            "family_action": str(source_row.get("family_action", "") or ""),
            "symbol_family": str(source_row.get("symbol_family", "") or ""),
            "action": str(source_row.get("action", "") or ""),
            "open_reife_candidate_state": candidate_state,
            "time_maturity_state": str(source_row.get("time_maturity_state", "") or ""),
            "episode_freshness_state": str(source_row.get("episode_freshness_state", "") or ""),
            "episode_source_labels": str(source_row.get("episode_source_labels", "") or ""),
            "episode_source_count": _safe_int(source_row.get("episode_source_count")),
            "episode_count": _safe_int(source_row.get("episode_count")),
            "phase_time_states": str(source_row.get("phase_time_states", "") or ""),
            "outcome_events": str(source_row.get("outcome_events", "") or ""),
            "event_reward_sum": round(_safe_float(source_row.get("event_reward_sum")), 6),
            "avg_event_reward": round(_safe_float(source_row.get("avg_event_reward")), 6),
            "avg_finite_phase_age": round(_avg(source_row.get("avg_finite_phase_age")), 6),
            "avg_bars_held": round(_avg(source_row.get("avg_bars_held")), 6),
            "has_inner_maturity": _safe_int(source_row.get("has_inner_maturity")),
            "inner_memory_state": str(source_row.get("inner_memory_state", "") or ""),
            "inner_map_count": _safe_int(source_row.get("inner_map_count")),
            "inner_seeds": str(source_row.get("inner_seeds", "") or ""),
            "bridge_passive_family_action": str(source_row.get("bridge_passive_family_action", "") or ""),
            "bridge_maturity_state": str(source_row.get("bridge_maturity_state", "") or ""),
            "bridge_similarity": round(_safe_float(source_row.get("bridge_similarity")), 6),
            "passive_only": 1,
            "influences_action": 0,
            "is_gate": 0,
            "is_motoric": 0,
        }
        row["observation_weight"] = _observation_weight(row, candidate_state)
        row["open_reife_note"] = _note(row)
        rows.append(row)

    priority = {
        "open_inner_reife_candidate": 0,
        "already_inner_bridged_reference": 1,
        "burden_reife_watch": 2,
        "older_open_trace_watch": 3,
        "fresh_waiting_context": 4,
    }
    rows.sort(
        key=lambda row: (
            priority.get(str(row.get("open_reife_candidate_state", "")), 9),
            -_safe_float(row.get("observation_weight")),
            str(row.get("family_action", "")),
        )
    )
    return rows


def build_summary(rows: list[dict]) -> list[dict]:
    grouped: dict[str, dict] = {}
    for row in rows:
        state = str(row.get("open_reife_candidate_state", "") or "unknown")
        bucket = grouped.setdefault(
            state,
            {
                "open_reife_candidate_state": state,
                "count": 0,
                "family_actions": set(),
                "event_reward_sum": 0.0,
                "with_inner_maturity": 0,
                "avg_observation_weight": 0.0,
            },
        )
        bucket["count"] += 1
        bucket["family_actions"].add(str(row.get("family_action", "") or ""))
        bucket["event_reward_sum"] += _safe_float(row.get("event_reward_sum"))
        bucket["with_inner_maturity"] += _safe_int(row.get("has_inner_maturity"))
        bucket["avg_observation_weight"] += _safe_float(row.get("observation_weight"))

    summary: list[dict] = []
    for bucket in grouped.values():
        count = max(1, _safe_int(bucket["count"]))
        summary.append(
            {
                "open_reife_candidate_state": str(bucket["open_reife_candidate_state"]),
                "count": _safe_int(bucket["count"]),
                "with_inner_maturity": _safe_int(bucket["with_inner_maturity"]),
                "event_reward_sum": round(_safe_float(bucket["event_reward_sum"]), 6),
                "avg_observation_weight": round(_safe_float(bucket["avg_observation_weight"]) / count, 6),
                "family_actions": ",".join(sorted(item for item in bucket["family_actions"] if item)),
            }
        )
    summary.sort(key=lambda row: (-_safe_float(row.get("event_reward_sum")), str(row.get("open_reife_candidate_state", ""))))
    return summary


def write_outputs(rows: list[dict], summary: list[dict], output_dir: Path, join_path: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows_path = output_dir / "dio_mini_passive_open_reife_candidates.csv"
    summary_path = output_dir / "dio_mini_passive_open_reife_candidates_summary.csv"
    json_path = output_dir / "dio_mini_passive_open_reife_candidates.json"
    md_path = output_dir / "dio_mini_passive_open_reife_candidates.md"
    txt_path = output_dir / "dio_mini_passive_open_reife_candidates.txt"

    row_fields = list(rows[0].keys()) if rows else [
        "family_action",
        "open_reife_candidate_state",
        "event_reward_sum",
        "passive_only",
        "influences_action",
    ]
    summary_fields = list(summary[0].keys()) if summary else [
        "open_reife_candidate_state",
        "count",
        "event_reward_sum",
        "family_actions",
    ]
    _write_csv(rows_path, rows, row_fields)
    _write_csv(summary_path, summary, summary_fields)
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_open_reife_candidates.v1",
                "source_join": str(join_path),
                "rows": rows,
                "summary": summary,
                "passive_only": True,
                "influences_action": False,
                "is_gate": False,
                "is_motoric": False,
            },
            indent=2,
            ensure_ascii=True,
        ),
        encoding="utf-8",
    )

    lines: list[str] = [
        "# Mini-DIO passive offene Reife-Kandidaten",
        "",
        "Quelle:",
        "",
        f"- `{join_path}`",
        "",
        "Grenze:",
        "",
        "- Diagnose nur passiv.",
        "- Kein Trainingsmemory.",
        "- Keine Handlung.",
        "- Kein Gate.",
        "- Keine Motorik.",
        "",
        "Zusammenfassung:",
        "",
    ]
    for item in summary:
        lines.append(
            f"- {item['open_reife_candidate_state']}: count={item['count']} "
            f"reward={item['event_reward_sum']} inner={item['with_inner_maturity']}"
        )
    lines.extend(["", "Offene Reife-Kandidaten:", ""])
    for row in rows:
        if row["open_reife_candidate_state"] != "open_inner_reife_candidate":
            continue
        lines.append(
            f"- `{row['family_action']}` reward={row['event_reward_sum']} "
            f"sources={row['episode_source_labels']} episodes={row['episode_count']}"
        )
        lines.append(f"  {row['open_reife_note']}")
    lines.extend(["", "Referenzen mit innerer Bruecke:", ""])
    for row in rows:
        if row["open_reife_candidate_state"] != "already_inner_bridged_reference":
            continue
        lines.append(
            f"- `{row['family_action']}` via `{row['bridge_passive_family_action'] or '-'}` "
            f"inner={row['inner_memory_state'] or '-'} reward={row['event_reward_sum']}"
        )
    lines.extend(["", "Belastete Beobachtungsspuren:", ""])
    for row in rows:
        if row["open_reife_candidate_state"] != "burden_reife_watch":
            continue
        lines.append(f"- `{row['family_action']}` reward={row['event_reward_sum']} sources={row['episode_source_labels']}")
    lines.extend(
        [
            "",
            "Fachliche Lesung:",
            "",
            "Die offenen Kandidaten sind reale, wiederkehrend getragene Spuren.",
            "Sie werden nicht automatisch zu Handlung oder Reife.",
            "Sie markieren nur, wo Mini-DIO in Folgelaeufen beobachten sollte, ob innere Reife entsteht.",
        ]
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    txt_path.write_text(
        "\n".join(
            [
                f"open_reife_candidate_rows={len(rows)}",
                f"summary={len(summary)}",
                "",
                *[
                    f"{item['open_reife_candidate_state']}: count={item['count']} reward={item['event_reward_sum']} inner={item['with_inner_maturity']}"
                    for item in summary
                ],
                "",
                "open candidates:",
                *[
                    f"{row['family_action']} reward={row['event_reward_sum']} sources={row['episode_source_labels']} episodes={row['episode_count']}"
                    for row in rows
                    if row["open_reife_candidate_state"] == "open_inner_reife_candidate"
                ],
                "",
                "passive_only=1",
                "influences_action=0",
                "is_gate=0",
                "is_motoric=0",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--time-maturity-join", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    join_rows = _read_csv(args.time_maturity_join)
    rows = build_rows(join_rows)
    summary = build_summary(rows)
    write_outputs(rows, summary, args.output_dir, args.time_maturity_join)
    print(f"open_reife_candidate_rows={len(rows)}")
    print(f"summary={len(summary)}")
    print(args.output_dir)


if __name__ == "__main__":
    main()
