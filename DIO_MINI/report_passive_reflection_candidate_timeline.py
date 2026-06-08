"""Passive timeline for DIO_MINI reflection candidates.

This report joins passive reflection candidates with passive inner-state
protocol rows across worlds. It shows whether a candidate family is read as
carried, cautious, open, or unstable over time. It does not write memory and it
does not influence action.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


WORLD_ORDER = {
    "probe17_first": 10,
    "probe17_repeat": 20,
    "probe18_first": 30,
    "probe18_repeat1": 40,
    "probe18_repeat2": 50,
}


def _safe_float(value: object) -> float:
    try:
        return float(value or 0.0)
    except Exception:
        return 0.0


def _safe_int(value: object) -> int:
    try:
        return int(float(value or 0))
    except Exception:
        return 0


def _parse_input(raw: str) -> tuple[str, Path]:
    if "=" not in raw:
        raise SystemExit(f"--protocol must be label=csv_path, got: {raw}")
    label, path = raw.split("=", 1)
    label = label.strip()
    if not label:
        raise SystemExit(f"Empty label in --protocol: {raw}")
    return label, Path(path.strip())


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _load_candidates(path: Path) -> dict[str, dict]:
    items: dict[str, dict] = {}
    for row in _read_csv(path):
        family = str(row.get("symbol_family", "") or "")
        if family:
            items[family] = dict(row)
    return items


def _candidate_timeline_note(row: dict) -> str:
    family = str(row.get("symbol_family", "") or "-")
    kind = str(row.get("reflection_candidate_kind", "") or "")
    inner_path = str(row.get("inner_state_path", "") or "-")
    contact_path = str(row.get("contact_state_path", "") or "-")
    reward = _safe_float(row.get("reward_sum"))
    best = _safe_float(row.get("best_reward_sum"))
    if kind == "reflection_candidate_reorganized_trace":
        return (
            f"{family}: Reorganisierte Kandidatenspur im Innenverlauf; "
            f"inner={inner_path}; contact={contact_path}; reward={reward:.6f}; best={best:.6f}."
        )
    if kind == "reflection_candidate_cautious_trace":
        return (
            f"{family}: Vorsichtige Kandidatenspur im Innenverlauf; "
            f"inner={inner_path}; contact={contact_path}; reward={reward:.6f}; best={best:.6f}."
        )
    return f"{family}: Offene Kandidatenspur im Innenverlauf; inner={inner_path}."


def build_rows(candidates: dict[str, dict], protocols: list[tuple[str, Path]]) -> tuple[list[dict], list[dict]]:
    detail: list[dict] = []
    for world, path in protocols:
        for row in _read_csv(path):
            family = str(row.get("symbol_family", "") or "")
            if family not in candidates:
                continue
            candidate = candidates[family]
            detail.append(
                {
                    "world": world,
                    "world_order": WORLD_ORDER.get(world, 999),
                    "run": str(row.get("run", "") or ""),
                    "tick": _safe_int(row.get("tick")),
                    "timestamp_ms": str(row.get("timestamp_ms", "") or ""),
                    "symbol_family": family,
                    "reflection_candidate_kind": str(candidate.get("reflection_candidate_kind", "") or ""),
                    "passive_conflict_state": str(candidate.get("passive_conflict_state", "") or ""),
                    "inner_state": str(row.get("inner_state", "") or ""),
                    "reflection_posture": str(row.get("reflection_posture", "") or ""),
                    "contact_state": str(row.get("contact_state", "") or ""),
                    "action": str(row.get("action", "WAIT") or "WAIT").upper(),
                    "raw_action": str(row.get("raw_action", "WAIT") or "WAIT").upper(),
                    "best_action_training": str(row.get("best_action_training", "WAIT") or "WAIT").upper(),
                    "reward": round(_safe_float(row.get("reward")), 6),
                    "best_reward_training": round(_safe_float(row.get("best_reward_training")), 6),
                    "sehen_form_flow": round(_safe_float(row.get("sehen_form_flow")), 6),
                    "sehen_form_stability": round(_safe_float(row.get("sehen_form_stability")), 6),
                    "hoeren_energy_tone": round(_safe_float(row.get("hoeren_energy_tone")), 6),
                    "fuehlen_mcm_coherence": round(_safe_float(row.get("fuehlen_mcm_coherence")), 6),
                    "fuehlen_mcm_tension": round(_safe_float(row.get("fuehlen_mcm_tension")), 6),
                    "inner_sentence": str(row.get("inner_sentence", "") or ""),
                    "reflection_question": str(candidate.get("reflection_question", "") or ""),
                    "passive_only": 1,
                }
            )

    detail.sort(
        key=lambda row: (
            _safe_int(row.get("world_order")),
            str(row.get("world", "")),
            str(row.get("symbol_family", "")),
            _safe_int(row.get("run")),
            _safe_int(row.get("tick")),
        )
    )

    groups: dict[str, dict] = {}
    by_family_rows: dict[str, list[dict]] = defaultdict(list)
    for row in detail:
        by_family_rows[str(row.get("symbol_family", "") or "")].append(row)

    for family, rows in by_family_rows.items():
        candidate = candidates.get(family, {})
        worlds = []
        inner_states = []
        contact_states = []
        actions = set()
        reward_sum = 0.0
        best_reward_sum = 0.0
        for row in rows:
            world = str(row.get("world", "") or "")
            if world not in worlds:
                worlds.append(world)
            inner_states.append(str(row.get("inner_state", "") or ""))
            contact_states.append(str(row.get("contact_state", "") or ""))
            actions.add(str(row.get("action", "") or ""))
            reward_sum += _safe_float(row.get("reward"))
            best_reward_sum += _safe_float(row.get("best_reward_training"))
        inner_path = " -> ".join(inner_states)
        contact_path = " -> ".join(contact_states)
        item = {
            "symbol_family": family,
            "reflection_candidate_kind": str(candidate.get("reflection_candidate_kind", "") or ""),
            "passive_conflict_state": str(candidate.get("passive_conflict_state", "") or ""),
            "worlds": ",".join(worlds),
            "hits": len(rows),
            "reward_sum": round(reward_sum, 6),
            "best_reward_sum": round(best_reward_sum, 6),
            "inner_state_path": inner_path,
            "contact_state_path": contact_path,
            "actions": ",".join(sorted(action for action in actions if action)),
            "reflection_question": str(candidate.get("reflection_question", "") or ""),
        }
        item["candidate_timeline_note"] = _candidate_timeline_note(item)
        item["passive_only"] = 1
        groups[family] = item

    summary = sorted(
        groups.values(),
        key=lambda row: (
            str(row.get("reflection_candidate_kind", "")),
            str(row.get("symbol_family", "")),
        ),
    )
    return detail, summary


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_passive_reflection_candidate_timeline_detail.csv"
    summary_path = output_dir / "dio_mini_passive_reflection_candidate_timeline.csv"
    json_path = output_dir / "dio_mini_passive_reflection_candidate_timeline.json"
    md_path = output_dir / "dio_mini_passive_reflection_candidate_timeline.md"

    detail_fields = list(detail[0].keys()) if detail else ["world", "symbol_family", "inner_state"]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)

    summary_fields = list(summary[0].keys()) if summary else ["symbol_family", "reflection_candidate_kind"]
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)

    json_path.write_text(
        json.dumps({"detail": detail, "summary": summary}, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    lines = ["# DIO Mini Passive Reflection Candidate Timeline", ""]
    if not summary:
        lines.append("Keine Kandidaten-Zeitlinie gefunden.")
    for row in summary:
        lines.extend(
            [
                f"## {row['symbol_family']}",
                f"- kind: {row['reflection_candidate_kind']}",
                f"- worlds: {row['worlds'] or '-'}",
                f"- hits: {row['hits']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- best_reward_sum: {float(row['best_reward_sum']):.6f}",
                f"- inner_state_path: {row['inner_state_path']}",
                f"- contact_state_path: {row['contact_state_path']}",
                f"- question: {row['reflection_question']}",
                f"- note: {row['candidate_timeline_note']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Grenze",
            "- passiver Kandidaten-Zeitverlauf",
            "- kein Memory-Schreiben",
            "- keine Motorik",
            "- kein Gate",
            "- keine harte Regel",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive timeline for reflection candidates")
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--protocol", action="append", required=True, help="label=inner_state_protocol_csv")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    detail, summary = build_rows(_load_candidates(Path(args.candidates)), [_parse_input(item) for item in args.protocol])
    write_outputs(detail, summary, Path(args.output_dir))
    print(f"candidate_timeline_rows={len(summary)} detail_rows={len(detail)}")
    for row in summary:
        print(f"{row['symbol_family']} hits={row['hits']} worlds={row['worlds']} reward={row['reward_sum']}")


if __name__ == "__main__":
    main()
