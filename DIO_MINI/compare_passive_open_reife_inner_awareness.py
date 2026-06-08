"""Compare two passive open maturity inner-awareness reports.

This checks whether the passive inner reading and DIO syntax sentence remain
stable across controlled follow-ups. It is diagnostic only.
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


def _load_by_family(path: Path) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for row in _read_csv(path):
        key = str(row.get("family_action", "") or "")
        if key:
            result[key] = row
    return result


def _compare_state(before: dict | None, after: dict | None) -> str:
    if before and after:
        before_state = str(before.get("inner_reife_awareness_state", "") or "")
        after_state = str(after.get("inner_reife_awareness_state", "") or "")
        before_family = str(before.get("symbol_family", "") or "")
        after_family = str(after.get("symbol_family", "") or "")
        before_action = str(before.get("action", "") or "")
        after_action = str(after.get("action", "") or "")
        if before_state == after_state and before_family == after_family and before_action == after_action:
            return "same_inner_reading"
        if before_state != after_state:
            return "inner_reading_shift"
        return "same_family_action_with_detail_shift"
    if after:
        return "new_inner_reading"
    if before:
        return "removed_inner_reading"
    return "missing"


def build_rows(before_csv: Path, after_csv: Path) -> tuple[list[dict], list[dict]]:
    before = _load_by_family(before_csv)
    after = _load_by_family(after_csv)
    keys = sorted(set(before) | set(after))
    detail: list[dict] = []
    summary: dict[str, dict] = {}
    for key in keys:
        before_row = before.get(key)
        after_row = after.get(key)
        state = _compare_state(before_row, after_row)
        before_score = _safe_float((before_row or {}).get("passive_reife_score"))
        after_score = _safe_float((after_row or {}).get("passive_reife_score"))
        before_reward = _safe_float((before_row or {}).get("event_reward_sum"))
        after_reward = _safe_float((after_row or {}).get("event_reward_sum"))
        row = {
            "family_action": key,
            "compare_state": state,
            "before_inner_state": str((before_row or {}).get("inner_reife_awareness_state", "-") or "-"),
            "after_inner_state": str((after_row or {}).get("inner_reife_awareness_state", "-") or "-"),
            "before_score": round(before_score, 9),
            "after_score": round(after_score, 9),
            "score_delta": round(after_score - before_score, 9),
            "before_reward": round(before_reward, 9),
            "after_reward": round(after_reward, 9),
            "reward_delta": round(after_reward - before_reward, 9),
            "before_episode_count": _safe_int((before_row or {}).get("episode_count")),
            "after_episode_count": _safe_int((after_row or {}).get("episode_count")),
            "episode_delta": _safe_int((after_row or {}).get("episode_count"))
            - _safe_int((before_row or {}).get("episode_count")),
            "before_dio_syntax_sentence": str((before_row or {}).get("dio_syntax_sentence", "-") or "-"),
            "after_dio_syntax_sentence": str((after_row or {}).get("dio_syntax_sentence", "-") or "-"),
            "same_state": int(str((before_row or {}).get("inner_reife_awareness_state", "")) == str((after_row or {}).get("inner_reife_awareness_state", ""))),
            "passive_only": 1,
            "influences_action": 0,
            "is_gate": 0,
            "is_motoric": 0,
        }
        detail.append(row)
        bucket = summary.setdefault(
            state,
            {
                "compare_state": state,
                "count": 0,
                "reward_delta": 0.0,
                "score_delta": 0.0,
                "families": [],
            },
        )
        bucket["count"] += 1
        bucket["reward_delta"] += row["reward_delta"]
        bucket["score_delta"] += row["score_delta"]
        bucket["families"].append(key)

    summary_rows: list[dict] = []
    for row in summary.values():
        count = max(1, int(row["count"]))
        summary_rows.append(
            {
                "compare_state": row["compare_state"],
                "count": row["count"],
                "reward_delta": round(float(row["reward_delta"]), 9),
                "avg_score_delta": round(float(row["score_delta"]) / count, 9),
                "families": ",".join(sorted(row["families"])),
            }
        )
    summary_rows.sort(key=lambda item: (str(item["compare_state"]), str(item["families"])))
    detail.sort(key=lambda item: (str(item["compare_state"]), str(item["family_action"])))
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


def write_outputs(output_dir: Path, before_csv: Path, after_csv: Path, detail: list[dict], summary: list[dict]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_open_reife_inner_awareness_compare.csv"
    summary_csv = output_dir / "dio_mini_passive_open_reife_inner_awareness_compare_summary.csv"
    json_path = output_dir / "dio_mini_passive_open_reife_inner_awareness_compare.json"
    md_path = output_dir / "dio_mini_passive_open_reife_inner_awareness_compare.md"

    _write_csv(detail_csv, detail, ["family_action", "compare_state", "score_delta", "reward_delta"])
    _write_csv(summary_csv, summary, ["compare_state", "count", "reward_delta", "avg_score_delta"])
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_open_reife_inner_awareness_compare.v1",
                "before": str(before_csv),
                "after": str(after_csv),
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
        "# Mini-DIO Passive Open Reife Inner Awareness Compare",
        "",
        f"- before: `{before_csv}`",
        f"- after: `{after_csv}`",
        "",
        "## Summary",
    ]
    if not summary:
        lines.append("- keine Vergleichsdaten")
    for row in summary:
        lines.append(
            f"- {row['compare_state']}: count={row['count']} "
            f"reward_delta={float(row['reward_delta']):.6f} "
            f"avg_score_delta={float(row['avg_score_delta']):.6f} "
            f"families={row['families'] or '-'}"
        )
    lines.extend(["", "## Detail"])
    for row in detail:
        lines.append(
            f"- {row['family_action']}: {row['compare_state']}; "
            f"state {row['before_inner_state']} -> {row['after_inner_state']}; "
            f"score {float(row['before_score']):.6f} -> {float(row['after_score']):.6f}; "
            f"reward {float(row['before_reward']):.6f} -> {float(row['after_reward']):.6f}; "
            f"episodes {row['before_episode_count']} -> {row['after_episode_count']}"
        )
        lines.append(f"  before: `{row['before_dio_syntax_sentence']}`")
        lines.append(f"  after: `{row['after_dio_syntax_sentence']}`")
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Innenwahrnehmungs-Diagnose",
            "- keine Handlung",
            "- kein Gate",
            "- keine Motorik",
            "- kein Trainingsmemory",
        ]
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", type=Path, required=True)
    parser.add_argument("--after", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    detail, summary = build_rows(args.before, args.after)
    write_outputs(args.output_dir, args.before, args.after, detail, summary)
    print(f"passive_open_reife_inner_awareness_compare rows={len(detail)} summary={len(summary)}")
    for row in summary:
        print(
            f"{row['compare_state']} count={row['count']} "
            f"reward_delta={row['reward_delta']} avg_score_delta={row['avg_score_delta']}"
        )


if __name__ == "__main__":
    main()
