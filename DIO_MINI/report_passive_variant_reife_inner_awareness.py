"""Build passive inner-awareness sentences from a variant maturity map.

This makes variant maturity readable without feeding it back into Mini-DIO.
It is diagnostic only: no memory writes, no action influence, no gate.
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


def _awareness_state(row: dict) -> str:
    state = str(row.get("variant_reife_state", "") or "")
    if state == "variant_self_carried_action_trace":
        return "inner_variant_self_carried"
    if state == "variant_self_burden_action_trace":
        return "inner_variant_self_burden"
    if state == "variant_related_observation_trace":
        return "inner_variant_related_observation"
    if state == "variant_local_wait_context":
        return "inner_variant_wait_context"
    return "inner_variant_open"


def _dio_syntax_sentence(row: dict, awareness_state: str) -> str:
    family_action = str(row.get("family_action", "") or "-")
    reward = _safe_float(row.get("event_reward_sum"))
    episodes = _safe_int(row.get("episode_count"))
    related = str(row.get("related_reference_family", "") or "-")
    similarity = _safe_float(row.get("transfer_similarity"))
    return (
        f"{family_action}|{awareness_state}|episodes={episodes}|"
        f"reward={reward:.6f}|related={related}|similarity={similarity:.6f}"
    )


def _human_sentence(row: dict, awareness_state: str) -> str:
    family_action = str(row.get("family_action", "") or "-")
    reward = _safe_float(row.get("event_reward_sum"))
    episodes = _safe_int(row.get("episode_count"))
    related = str(row.get("related_reference_family", "") or "")
    similarity = _safe_float(row.get("transfer_similarity"))
    if awareness_state == "inner_variant_self_carried":
        return (
            f"{family_action}: Diese Variante traegt sich lokal aus eigener Konsequenz; "
            f"Episoden={episodes}, Konsequenz={reward:.6f}. Sie bleibt passive Innenwahrnehmung."
        )
    if awareness_state == "inner_variant_self_burden":
        return (
            f"{family_action}: Diese Variante war lokal belastend; Episoden={episodes}, "
            f"Konsequenz={reward:.6f}. Sie bleibt Warnspur, nicht Sperre."
        )
    if awareness_state == "inner_variant_related_observation":
        return (
            f"{family_action}: Diese Variante erinnert passiv an {related or '-'} "
            f"(similarity={similarity:.6f}), bleibt aber Beobachtung."
        )
    if awareness_state == "inner_variant_wait_context":
        return f"{family_action}: Diese Variante bleibt lokaler Wartungs- und Beobachtungskontext."
    return f"{family_action}: Diese Variante bleibt passiv offen; Konsequenz={reward:.6f}."


def build_rows(variant_map_csv: Path) -> tuple[list[dict], list[dict]]:
    detail: list[dict] = []
    for source in _read_csv(variant_map_csv):
        awareness_state = _awareness_state(source)
        row = {
            "family_action": str(source.get("family_action", "") or ""),
            "symbol_family": str(source.get("symbol_family", "") or ""),
            "action": str(source.get("action", "") or ""),
            "inner_variant_awareness_state": awareness_state,
            "variant_reife_state": str(source.get("variant_reife_state", "") or ""),
            "event_reward_sum": round(_safe_float(source.get("event_reward_sum")), 9),
            "episode_count": _safe_int(source.get("episode_count")),
            "outcome_events": str(source.get("outcome_events", "") or ""),
            "related_reference_family": str(source.get("related_reference_family", "") or ""),
            "related_reference_action": str(source.get("related_reference_action", "") or ""),
            "related_reference_outcome": str(source.get("related_reference_outcome", "") or ""),
            "transfer_reife_state": str(source.get("transfer_reife_state", "") or ""),
            "transfer_reife": round(_safe_float(source.get("transfer_reife")), 9),
            "transfer_similarity": round(_safe_float(source.get("transfer_similarity")), 9),
            "dio_syntax_sentence": _dio_syntax_sentence(source, awareness_state),
            "inner_awareness_sentence": _human_sentence(source, awareness_state),
            "passive_only": 1,
            "writes_training_memory": 0,
            "read_by_mini_dio": 0,
            "influences_action": 0,
            "is_gate": 0,
            "is_motoric": 0,
        }
        detail.append(row)

    groups: dict[str, dict] = {}
    for row in detail:
        state = str(row["inner_variant_awareness_state"])
        bucket = groups.setdefault(
            state,
            {
                "inner_variant_awareness_state": state,
                "count": 0,
                "event_reward_sum": 0.0,
                "episode_count": 0,
                "families": [],
            },
        )
        bucket["count"] += 1
        bucket["event_reward_sum"] += _safe_float(row.get("event_reward_sum"))
        bucket["episode_count"] += _safe_int(row.get("episode_count"))
        bucket["families"].append(str(row.get("family_action", "") or ""))

    summary: list[dict] = []
    for row in groups.values():
        summary.append(
            {
                "inner_variant_awareness_state": row["inner_variant_awareness_state"],
                "count": row["count"],
                "event_reward_sum": round(float(row["event_reward_sum"]), 9),
                "episode_count": row["episode_count"],
                "family_actions": ",".join(sorted(name for name in row["families"] if name)),
            }
        )
    detail.sort(
        key=lambda item: (
            str(item["inner_variant_awareness_state"]),
            -_safe_float(item.get("event_reward_sum")),
            str(item.get("family_action", "")),
        )
    )
    summary.sort(key=lambda item: (str(item["inner_variant_awareness_state"]), str(item["family_actions"])))
    return detail, summary


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


def write_outputs(variant_map_csv: Path, output_dir: Path, detail: list[dict], summary: list[dict]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_variant_reife_inner_awareness.csv"
    summary_csv = output_dir / "dio_mini_passive_variant_reife_inner_awareness_summary.csv"
    json_path = output_dir / "dio_mini_passive_variant_reife_inner_awareness.json"
    md_path = output_dir / "dio_mini_passive_variant_reife_inner_awareness.md"
    txt_path = output_dir / "dio_mini_passive_variant_reife_inner_awareness.txt"

    _write_csv(detail_csv, detail, ["family_action", "inner_variant_awareness_state", "event_reward_sum"])
    _write_csv(summary_csv, summary, ["inner_variant_awareness_state", "count", "event_reward_sum"])
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_variant_reife_inner_awareness.v1",
                "source_variant_map": str(variant_map_csv),
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
        "# Mini-DIO Passive Variant Reife Inner Awareness",
        "",
        f"- source_variant_map: `{variant_map_csv}`",
        "",
        "## Summary",
    ]
    if not summary:
        lines.append("- keine passive Varianten-Innenwahrnehmung")
    for row in summary:
        lines.append(
            f"- {row['inner_variant_awareness_state']}: count={row['count']} "
            f"reward={float(row['event_reward_sum']):.6f} "
            f"episodes={row['episode_count']} "
            f"families={row['family_actions'] or '-'}"
        )
    lines.extend(["", "## Detail"])
    for row in detail:
        lines.extend(
            [
                f"- {row['family_action']}: {row['inner_variant_awareness_state']}",
                f"  DIO-Syntax: `{row['dio_syntax_sentence']}`",
                f"  Lesung: {row['inner_awareness_sentence']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Innenwahrnehmung",
            "- keine Handlung",
            "- kein Gate",
            "- keine Motorik",
            "- kein Trainingsmemory",
            "- Mini-DIO liest diesen Bericht nicht aktiv",
        ]
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    txt_path.write_text("\n".join(str(row["dio_syntax_sentence"]) for row in detail) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant-map", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    detail, summary = build_rows(args.variant_map)
    write_outputs(args.variant_map, args.output_dir, detail, summary)
    print(f"passive_variant_reife_inner_awareness rows={len(detail)} summary={len(summary)}")
    for row in summary:
        print(
            f"{row['inner_variant_awareness_state']} count={row['count']} "
            f"reward={row['event_reward_sum']} episodes={row['episode_count']}"
        )


if __name__ == "__main__":
    main()
