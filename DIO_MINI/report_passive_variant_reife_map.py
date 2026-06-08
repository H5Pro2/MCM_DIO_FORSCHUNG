"""Build a passive maturity map for a variant world.

This report joins local variant time traces with passive transfer maturity.
It keeps three things separated:

- local consequence in the variant world
- sensory/MCM kinship to a known reference world
- whether the variant is carried, observed, or burdened by its own outcome

Diagnostic only:
- no memory writes
- no action influence
- no gate
- no motorics
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


def _load_transfer_by_right_family(path: Path) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for row in _read_csv(path):
        right_family = str(row.get("right_family", "") or "")
        if right_family:
            grouped.setdefault(right_family, []).append(row)
    return grouped


def _best_transfer(rows: list[dict]) -> dict:
    if not rows:
        return {}
    return sorted(
        rows,
        key=lambda row: (
            -_safe_float(row.get("sensory_mcm_similarity") or row.get("similarity")),
            str(row.get("left_family", "")),
        ),
    )[0]


def _variant_state(row: dict, transfer: dict) -> str:
    action = str(row.get("action", "") or "")
    reward = _safe_float(row.get("event_reward_sum"))
    outcome = str(row.get("outcome_events", "") or "")
    has_transfer = bool(transfer)
    if action != "WAIT" and reward > 0.0:
        return "variant_self_carried_action_trace"
    if action != "WAIT" and reward < 0.0:
        return "variant_self_burden_action_trace"
    if action == "WAIT" and has_transfer:
        return "variant_related_observation_trace"
    if action == "WAIT" and "NO_TRADE" in outcome:
        return "variant_local_wait_context"
    return "variant_open_trace"


def _sentence(row: dict) -> str:
    state = str(row.get("variant_reife_state", "") or "")
    family_action = str(row.get("family_action", "") or "-")
    related = str(row.get("related_reference_family", "") or "")
    similarity = _safe_float(row.get("transfer_similarity"))
    reward = _safe_float(row.get("event_reward_sum"))
    if state == "variant_self_carried_action_trace":
        return f"{family_action}: Die Variante traegt diese Handlung aus eigener Konsequenz; reward={reward:.6f}."
    if state == "variant_self_burden_action_trace":
        return f"{family_action}: Die Variante belastet diese Handlung aus eigener Konsequenz; reward={reward:.6f}."
    if state == "variant_related_observation_trace":
        return (
            f"{family_action}: Die Variante ist verwandt mit {related or '-'} "
            f"(similarity={similarity:.6f}), bleibt aber Beobachtung."
        )
    if state == "variant_local_wait_context":
        return f"{family_action}: Die Variante bleibt lokaler Wartungs-/Beobachtungskontext."
    return f"{family_action}: Die Variante bleibt offen; reward={reward:.6f}."


def build_rows(time_summary_csv: Path, transfer_csv: Path) -> tuple[list[dict], list[dict]]:
    transfer_by_right = _load_transfer_by_right_family(transfer_csv)
    detail: list[dict] = []
    summary: dict[str, dict] = {}

    for source in _read_csv(time_summary_csv):
        symbol_family = str(source.get("symbol_family", "") or "")
        transfer = _best_transfer(transfer_by_right.get(symbol_family, []))
        state = _variant_state(source, transfer)
        row = {
            "family_action": str(source.get("family_action", "") or ""),
            "symbol_family": symbol_family,
            "action": str(source.get("action", "") or ""),
            "variant_reife_state": state,
            "freshness_state": str(source.get("freshness_state", "") or ""),
            "source_count": _safe_int(source.get("source_count")),
            "episode_count": _safe_int(source.get("episode_count")),
            "run_count": _safe_int(source.get("run_count")),
            "outcome_events": str(source.get("outcome_events", "") or ""),
            "event_reward_sum": round(_safe_float(source.get("event_reward_sum")), 9),
            "avg_event_reward": round(_safe_float(source.get("avg_event_reward")), 9),
            "phase_time_states": str(source.get("phase_time_states", "") or ""),
            "avg_phase_distance": round(_safe_float(source.get("avg_phase_distance")), 9),
            "avg_binding_pressure": round(_safe_float(source.get("avg_binding_pressure")), 9),
            "avg_release_pressure": round(_safe_float(source.get("avg_release_pressure")), 9),
            "related_reference_family": str(transfer.get("left_family", "") or ""),
            "related_reference_action": str(transfer.get("left_action", "") or ""),
            "related_reference_outcome": str(transfer.get("left_outcome", "") or ""),
            "transfer_reife_state": str(transfer.get("transfer_reife_state", "") or ""),
            "transfer_reife": round(_safe_float(transfer.get("transfer_reife")), 9),
            "transfer_similarity": round(_safe_float(transfer.get("sensory_mcm_similarity") or transfer.get("similarity")), 9),
            "transfer_event_relation": str(transfer.get("event_reward_relation", "") or ""),
            "passive_only": 1,
            "writes_training_memory": 0,
            "read_by_mini_dio": 0,
            "influences_action": 0,
            "is_gate": 0,
            "is_motoric": 0,
        }
        row["variant_reife_sentence"] = _sentence(row)
        detail.append(row)
        bucket = summary.setdefault(
            state,
            {
                "variant_reife_state": state,
                "count": 0,
                "event_reward_sum": 0.0,
                "episode_count": 0,
                "avg_transfer_similarity_sum": 0.0,
                "transfer_count": 0,
                "family_actions": [],
            },
        )
        bucket["count"] += 1
        bucket["event_reward_sum"] += _safe_float(row.get("event_reward_sum"))
        bucket["episode_count"] += _safe_int(row.get("episode_count"))
        if row.get("related_reference_family"):
            bucket["avg_transfer_similarity_sum"] += _safe_float(row.get("transfer_similarity"))
            bucket["transfer_count"] += 1
        bucket["family_actions"].append(str(row.get("family_action", "") or ""))

    summary_rows: list[dict] = []
    for row in summary.values():
        transfer_count = max(1, int(row["transfer_count"]))
        summary_rows.append(
            {
                "variant_reife_state": row["variant_reife_state"],
                "count": row["count"],
                "event_reward_sum": round(float(row["event_reward_sum"]), 9),
                "episode_count": row["episode_count"],
                "avg_transfer_similarity": round(float(row["avg_transfer_similarity_sum"]) / transfer_count, 9)
                if row["transfer_count"]
                else 0.0,
                "family_actions": ",".join(sorted(name for name in row["family_actions"] if name)),
            }
        )
    summary_rows.sort(key=lambda item: (str(item["variant_reife_state"]), str(item["family_actions"])))
    detail.sort(key=lambda item: (str(item["variant_reife_state"]), str(item["family_action"])))
    return detail, summary_rows


def _write_csv(path: Path, rows: list[dict], default_fields: list[str]) -> None:
    fields = list(default_fields)
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(output_dir: Path, time_summary_csv: Path, transfer_csv: Path, detail: list[dict], summary: list[dict]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_variant_reife_map.csv"
    summary_csv = output_dir / "dio_mini_passive_variant_reife_map_summary.csv"
    json_path = output_dir / "dio_mini_passive_variant_reife_map.json"
    md_path = output_dir / "dio_mini_passive_variant_reife_map.md"

    _write_csv(detail_csv, detail, ["family_action", "variant_reife_state", "event_reward_sum"])
    _write_csv(summary_csv, summary, ["variant_reife_state", "count", "event_reward_sum"])
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_variant_reife_map.v1",
                "time_summary_source": str(time_summary_csv),
                "transfer_source": str(transfer_csv),
                "summary": summary,
                "detail": detail,
                "boundary": {
                    "passive_only": True,
                    "writes_training_memory": False,
                    "read_by_mini_dio": False,
                    "influences_action": False,
                    "is_gate": False,
                    "is_motoric": False,
                },
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# Mini-DIO Passive Variant Reife Map",
        "",
        f"- time_summary_source: `{time_summary_csv}`",
        f"- transfer_source: `{transfer_csv}`",
        "",
        "## Summary",
    ]
    if not summary:
        lines.append("- keine Variantenreife-Daten")
    for row in summary:
        lines.append(
            f"- {row['variant_reife_state']}: count={row['count']} "
            f"reward={float(row['event_reward_sum']):.6f} "
            f"episodes={row['episode_count']} "
            f"avg_transfer_similarity={float(row['avg_transfer_similarity']):.6f} "
            f"families={row['family_actions'] or '-'}"
        )
    lines.extend(["", "## Detail"])
    for row in detail:
        lines.extend(
            [
                f"- {row['family_action']}: {row['variant_reife_state']}",
                f"  reward={float(row['event_reward_sum']):.6f}; outcomes={row['outcome_events']}; related={row['related_reference_family'] or '-'}; similarity={float(row['transfer_similarity']):.6f}",
                f"  {row['variant_reife_sentence']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Variantenreife",
            "- lokale Konsequenz und Transfernaehe bleiben getrennt",
            "- keine Handlung",
            "- kein Gate",
            "- keine Motorik",
            "- kein Trainingsmemory",
        ]
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--time-summary", type=Path, required=True)
    parser.add_argument("--transfer", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    detail, summary = build_rows(args.time_summary, args.transfer)
    write_outputs(args.output_dir, args.time_summary, args.transfer, detail, summary)
    print(f"passive_variant_reife_map rows={len(detail)} summary={len(summary)}")
    for row in summary:
        print(
            f"{row['variant_reife_state']} count={row['count']} "
            f"reward={row['event_reward_sum']} episodes={row['episode_count']}"
        )


if __name__ == "__main__":
    main()
