"""Build passive inner-awareness sentences from open maturity memory.

The report makes passive open maturity readable as an inner perception:
"I know this trace passively as carried." It is diagnostic only and must not
be used by Mini-DIO for action, gates, motorics, or training.
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


def _read_memory(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _inner_awareness_state(entry: dict) -> str:
    state = str(entry.get("passive_open_reife_state", "") or "")
    if state == "passive_reife_carried_candidate":
        return "inner_reife_passively_carried"
    if state:
        return f"inner_reife_{state}"
    return "inner_reife_open"


def _dio_syntax_sentence(entry: dict, awareness_state: str) -> str:
    family_action = str(entry.get("family_action", "") or "-")
    score = _safe_float(entry.get("passive_reife_score"))
    reward = _safe_float(entry.get("event_reward_sum"))
    episodes = _safe_int(entry.get("episode_count"))
    return (
        f"{family_action}|{awareness_state}|score={score:.6f}|"
        f"episodes={episodes}|reward={reward:.6f}"
    )


def _human_sentence(entry: dict, awareness_state: str) -> str:
    family_action = str(entry.get("family_action", "") or "-")
    score = _safe_float(entry.get("passive_reife_score"))
    reward = _safe_float(entry.get("event_reward_sum"))
    episodes = _safe_int(entry.get("episode_count"))
    if awareness_state == "inner_reife_passively_carried":
        return (
            f"{family_action}: Diese Spur ist passiv als getragen lesbar; "
            f"Score={score:.6f}, Episoden={episodes}, Konsequenz={reward:.6f}. "
            "Sie bleibt Innenwahrnehmung, nicht Handlung."
        )
    return (
        f"{family_action}: Diese Spur bleibt passiv offen; "
        f"Score={score:.6f}, Episoden={episodes}, Konsequenz={reward:.6f}. "
        "Sie bleibt Innenwahrnehmung, nicht Handlung."
    )


def build_rows(memory: dict) -> tuple[list[dict], list[dict]]:
    detail: list[dict] = []
    for entry in memory.get("entries", []) or []:
        awareness_state = _inner_awareness_state(entry)
        detail.append(
            {
                "family_action": str(entry.get("family_action", "") or ""),
                "symbol_family": str(entry.get("symbol_family", "") or ""),
                "action": str(entry.get("action", "") or ""),
                "inner_reife_awareness_state": awareness_state,
                "passive_open_reife_state": str(entry.get("passive_open_reife_state", "") or ""),
                "passive_reife_score": round(_safe_float(entry.get("passive_reife_score")), 9),
                "event_reward_sum": round(_safe_float(entry.get("event_reward_sum")), 9),
                "episode_count": _safe_int(entry.get("episode_count")),
                "trade_count": _safe_int(entry.get("trade_count")),
                "tp_count": _safe_int(entry.get("tp_count")),
                "sl_count": _safe_int(entry.get("sl_count")),
                "multisensory_stability": round(_safe_float(entry.get("multisensory_stability")), 9),
                "visual_stability": round(_safe_float(entry.get("visual_stability")), 9),
                "auditory_stability": round(_safe_float(entry.get("auditory_stability")), 9),
                "mcm_stability": round(_safe_float(entry.get("mcm_stability")), 9),
                "dio_syntax_sentence": _dio_syntax_sentence(entry, awareness_state),
                "inner_awareness_sentence": _human_sentence(entry, awareness_state),
                "passive_only": 1,
                "writes_training_memory": 0,
                "read_by_mini_dio": 0,
                "influences_action": 0,
                "is_gate": 0,
                "is_motoric": 0,
            }
        )

    groups: dict[str, dict] = {}
    for row in detail:
        state = str(row["inner_reife_awareness_state"])
        item = groups.setdefault(
            state,
            {
                "inner_reife_awareness_state": state,
                "count": 0,
                "event_reward_sum": 0.0,
                "score_sum": 0.0,
                "episode_count": 0,
                "family_actions": [],
            },
        )
        item["count"] += 1
        item["event_reward_sum"] += _safe_float(row.get("event_reward_sum"))
        item["score_sum"] += _safe_float(row.get("passive_reife_score"))
        item["episode_count"] += _safe_int(row.get("episode_count"))
        item["family_actions"].append(str(row.get("family_action", "") or ""))

    summary: list[dict] = []
    for row in groups.values():
        count = max(1, int(row["count"]))
        summary.append(
            {
                "inner_reife_awareness_state": row["inner_reife_awareness_state"],
                "count": row["count"],
                "event_reward_sum": round(float(row["event_reward_sum"]), 9),
                "avg_passive_reife_score": round(float(row["score_sum"]) / count, 9),
                "episode_count": row["episode_count"],
                "family_actions": ",".join(sorted(name for name in row["family_actions"] if name)),
            }
        )
    detail.sort(key=lambda item: (-_safe_float(item.get("passive_reife_score")), str(item.get("family_action", ""))))
    summary.sort(key=lambda item: (str(item["inner_reife_awareness_state"]), str(item["family_actions"])))
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


def write_outputs(memory_path: Path, memory: dict, detail: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_open_reife_inner_awareness.csv"
    summary_csv = output_dir / "dio_mini_passive_open_reife_inner_awareness_summary.csv"
    json_path = output_dir / "dio_mini_passive_open_reife_inner_awareness.json"
    md_path = output_dir / "dio_mini_passive_open_reife_inner_awareness.md"
    txt_path = output_dir / "dio_mini_passive_open_reife_inner_awareness.txt"

    _write_csv(
        detail_csv,
        detail,
        ["family_action", "inner_reife_awareness_state", "passive_reife_score", "event_reward_sum"],
    )
    _write_csv(summary_csv, summary, ["inner_reife_awareness_state", "count", "event_reward_sum"])
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_open_reife_inner_awareness.v1",
                "source_memory": str(memory_path),
                "source_memory_summary": memory.get("summary", {}),
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
        "# Mini-DIO Passive Open Reife Inner Awareness",
        "",
        f"- source_memory: `{memory_path}`",
        "",
        "## Summary",
    ]
    if not summary:
        lines.append("- keine passive Reife-Innenwahrnehmung")
    for row in summary:
        lines.append(
            f"- {row['inner_reife_awareness_state']}: count={row['count']} "
            f"reward={float(row['event_reward_sum']):.6f} "
            f"avg_score={float(row['avg_passive_reife_score']):.6f} "
            f"episodes={row['episode_count']} "
            f"families={row['family_actions'] or '-'}"
        )
    lines.extend(["", "## Detail"])
    for row in detail:
        lines.extend(
            [
                f"- {row['family_action']}: {row['inner_reife_awareness_state']}",
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
    text = "\n".join(lines) + "\n"
    md_path.write_text(text, encoding="utf-8")
    txt_path.write_text("\n".join(str(row["dio_syntax_sentence"]) for row in detail) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--memory", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    memory = _read_memory(args.memory)
    detail, summary = build_rows(memory)
    write_outputs(args.memory, memory, detail, summary, args.output_dir)
    print(f"passive_open_reife_inner_awareness rows={len(detail)} summary={len(summary)}")
    for row in summary:
        print(
            f"{row['inner_reife_awareness_state']} count={row['count']} "
            f"reward={row['event_reward_sum']} avg_score={row['avg_passive_reife_score']}"
        )


if __name__ == "__main__":
    main()
