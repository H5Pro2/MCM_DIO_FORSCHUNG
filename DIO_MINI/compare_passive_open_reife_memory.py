"""Compare two passive Mini-DIO open maturity memory snapshots.

This is a diagnostic report only. It does not write active memory, does not
influence Mini-DIO action, and is not a gate.
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
    if not path.exists():
        return {"entries": [], "summary": {}, "source": str(path)}
    return json.loads(path.read_text(encoding="utf-8"))


def _entry_map(memory: dict) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for item in memory.get("entries", []) or []:
        key = str(item.get("family_action", "") or "")
        if key:
            result[key] = dict(item)
    return result


def _compare_state(before: dict | None, after: dict | None) -> str:
    if before and after:
        return "stable_existing"
    if after:
        return "new_passive_entry"
    if before:
        return "removed_passive_entry"
    return "missing"


def build_compare_rows(before_memory: dict, after_memory: dict) -> tuple[list[dict], list[dict]]:
    before = _entry_map(before_memory)
    after = _entry_map(after_memory)
    family_actions = sorted(set(before) | set(after))
    detail: list[dict] = []
    summary: dict[str, dict] = {}
    for family_action in family_actions:
        before_item = before.get(family_action)
        after_item = after.get(family_action)
        state = _compare_state(before_item, after_item)
        before_score = _safe_float((before_item or {}).get("passive_reife_score"))
        after_score = _safe_float((after_item or {}).get("passive_reife_score"))
        before_reward = _safe_float((before_item or {}).get("event_reward_sum"))
        after_reward = _safe_float((after_item or {}).get("event_reward_sum"))
        before_episodes = _safe_int((before_item or {}).get("episode_count"))
        after_episodes = _safe_int((after_item or {}).get("episode_count"))
        row = {
            "family_action": family_action,
            "compare_state": state,
            "before_score": round(before_score, 9),
            "after_score": round(after_score, 9),
            "score_delta": round(after_score - before_score, 9),
            "before_reward": round(before_reward, 9),
            "after_reward": round(after_reward, 9),
            "reward_delta": round(after_reward - before_reward, 9),
            "before_episode_count": before_episodes,
            "after_episode_count": after_episodes,
            "episode_delta": after_episodes - before_episodes,
            "before_trade_count": _safe_int((before_item or {}).get("trade_count")),
            "after_trade_count": _safe_int((after_item or {}).get("trade_count")),
            "before_tp_count": _safe_int((before_item or {}).get("tp_count")),
            "after_tp_count": _safe_int((after_item or {}).get("tp_count")),
            "before_sl_count": _safe_int((before_item or {}).get("sl_count")),
            "after_sl_count": _safe_int((after_item or {}).get("sl_count")),
            "before_multisensory_stability": round(
                _safe_float((before_item or {}).get("multisensory_stability")),
                9,
            ),
            "after_multisensory_stability": round(
                _safe_float((after_item or {}).get("multisensory_stability")),
                9,
            ),
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
                "entry_count": 0,
                "before_reward": 0.0,
                "after_reward": 0.0,
                "before_score_sum": 0.0,
                "after_score_sum": 0.0,
                "families": [],
            },
        )
        bucket["entry_count"] += 1
        bucket["before_reward"] += before_reward
        bucket["after_reward"] += after_reward
        bucket["before_score_sum"] += before_score
        bucket["after_score_sum"] += after_score
        bucket["families"].append(family_action)

    summary_rows: list[dict] = []
    for row in summary.values():
        count = max(1, int(row["entry_count"]))
        summary_rows.append(
            {
                "compare_state": row["compare_state"],
                "entry_count": row["entry_count"],
                "before_reward": round(float(row["before_reward"]), 9),
                "after_reward": round(float(row["after_reward"]), 9),
                "reward_delta": round(float(row["after_reward"]) - float(row["before_reward"]), 9),
                "before_avg_score": round(float(row["before_score_sum"]) / count, 9),
                "after_avg_score": round(float(row["after_score_sum"]) / count, 9),
                "avg_score_delta": round(
                    (float(row["after_score_sum"]) - float(row["before_score_sum"])) / count,
                    9,
                ),
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


def write_outputs(
    output_dir: Path,
    before_path: Path,
    after_path: Path,
    before_memory: dict,
    after_memory: dict,
    detail: list[dict],
    summary: list[dict],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_open_reife_memory_compare.csv"
    summary_csv = output_dir / "dio_mini_passive_open_reife_memory_compare_summary.csv"
    json_path = output_dir / "dio_mini_passive_open_reife_memory_compare.json"
    md_path = output_dir / "dio_mini_passive_open_reife_memory_compare.md"
    txt_path = output_dir / "dio_mini_passive_open_reife_memory_compare.txt"

    _write_csv(
        detail_csv,
        detail,
        ["family_action", "compare_state", "before_score", "after_score", "score_delta"],
    )
    _write_csv(summary_csv, summary, ["compare_state", "entry_count", "reward_delta", "avg_score_delta"])
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_open_reife_memory_compare.v1",
                "before": str(before_path),
                "after": str(after_path),
                "before_summary": before_memory.get("summary", {}),
                "after_summary": after_memory.get("summary", {}),
                "summary": summary,
                "detail": detail,
                "boundary": {
                    "passive_only": True,
                    "writes_training_memory": False,
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
        "# Mini-DIO Passive Open Reife Memory Compare",
        "",
        f"- before: `{before_path}`",
        f"- after: `{after_path}`",
        "",
        "## Summary",
    ]
    if not summary:
        lines.append("- keine Vergleichsdaten")
    for row in summary:
        lines.append(
            f"- {row['compare_state']}: entries={row['entry_count']} "
            f"reward_delta={float(row['reward_delta']):.6f} "
            f"avg_score_delta={float(row['avg_score_delta']):.6f} "
            f"families={row['families'] or '-'}"
        )
    lines.extend(["", "## Detail"])
    for row in detail:
        lines.append(
            f"- {row['family_action']}: {row['compare_state']}; "
            f"score {float(row['before_score']):.6f} -> {float(row['after_score']):.6f}; "
            f"reward {float(row['before_reward']):.6f} -> {float(row['after_reward']):.6f}; "
            f"episodes {row['before_episode_count']} -> {row['after_episode_count']}"
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Diagnose",
            "- keine Handlung",
            "- kein Gate",
            "- keine Motorik",
            "- kein Trainingsmemory",
        ]
    )
    text = "\n".join(lines) + "\n"
    md_path.write_text(text, encoding="utf-8")
    txt_path.write_text(text, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", type=Path, required=True)
    parser.add_argument("--after", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    before_memory = _read_memory(args.before)
    after_memory = _read_memory(args.after)
    detail, summary = build_compare_rows(before_memory, after_memory)
    write_outputs(args.output_dir, args.before, args.after, before_memory, after_memory, detail, summary)
    print(f"passive_open_reife_memory_compare rows={len(detail)} summary={len(summary)}")
    for row in summary:
        print(
            f"{row['compare_state']} entries={row['entry_count']} "
            f"reward_delta={row['reward_delta']} avg_score_delta={row['avg_score_delta']}"
        )


if __name__ == "__main__":
    main()
