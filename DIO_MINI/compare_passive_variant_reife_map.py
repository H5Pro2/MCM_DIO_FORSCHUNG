"""Compare two passive Mini-DIO variant maturity maps.

This report is diagnostic only. It does not write memory, does not influence
Mini-DIO action, and is not a gate.
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


def _row_map(path: Path) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    if not path.exists():
        return rows
    for row in _read_csv(path):
        family_action = str(row.get("family_action", "") or "")
        if family_action:
            rows[family_action] = row
    return rows


def _compare_state(before: dict | None, after: dict | None) -> str:
    if before and after:
        before_state = str(before.get("variant_reife_state", "") or "")
        after_state = str(after.get("variant_reife_state", "") or "")
        if before_state == after_state:
            return "same_variant_state"
        return "variant_state_shift"
    if after:
        return "new_variant_trace"
    if before:
        return "removed_variant_trace"
    return "missing"


def build_compare_rows(before_csv: Path, after_csv: Path) -> tuple[list[dict], list[dict]]:
    before = _row_map(before_csv)
    after = _row_map(after_csv)
    family_actions = sorted(set(before) | set(after))
    detail: list[dict] = []
    summary: dict[str, dict] = {}

    for family_action in family_actions:
        before_row = before.get(family_action)
        after_row = after.get(family_action)
        compare_state = _compare_state(before_row, after_row)
        before_reward = _safe_float((before_row or {}).get("event_reward_sum"))
        after_reward = _safe_float((after_row or {}).get("event_reward_sum"))
        before_episodes = _safe_int((before_row or {}).get("episode_count"))
        after_episodes = _safe_int((after_row or {}).get("episode_count"))
        row = {
            "family_action": family_action,
            "compare_state": compare_state,
            "before_variant_reife_state": str((before_row or {}).get("variant_reife_state", "") or ""),
            "after_variant_reife_state": str((after_row or {}).get("variant_reife_state", "") or ""),
            "before_reward": round(before_reward, 9),
            "after_reward": round(after_reward, 9),
            "reward_delta": round(after_reward - before_reward, 9),
            "before_episode_count": before_episodes,
            "after_episode_count": after_episodes,
            "episode_delta": after_episodes - before_episodes,
            "before_related_reference_family": str((before_row or {}).get("related_reference_family", "") or ""),
            "after_related_reference_family": str((after_row or {}).get("related_reference_family", "") or ""),
            "before_transfer_similarity": round(_safe_float((before_row or {}).get("transfer_similarity")), 9),
            "after_transfer_similarity": round(_safe_float((after_row or {}).get("transfer_similarity")), 9),
            "passive_only": 1,
            "writes_training_memory": 0,
            "read_by_mini_dio": 0,
            "influences_action": 0,
            "is_gate": 0,
            "is_motoric": 0,
        }
        detail.append(row)
        bucket = summary.setdefault(
            compare_state,
            {
                "compare_state": compare_state,
                "count": 0,
                "before_reward": 0.0,
                "after_reward": 0.0,
                "before_episodes": 0,
                "after_episodes": 0,
                "families": [],
            },
        )
        bucket["count"] += 1
        bucket["before_reward"] += before_reward
        bucket["after_reward"] += after_reward
        bucket["before_episodes"] += before_episodes
        bucket["after_episodes"] += after_episodes
        bucket["families"].append(family_action)

    summary_rows: list[dict] = []
    for row in summary.values():
        summary_rows.append(
            {
                "compare_state": row["compare_state"],
                "count": row["count"],
                "before_reward": round(float(row["before_reward"]), 9),
                "after_reward": round(float(row["after_reward"]), 9),
                "reward_delta": round(float(row["after_reward"]) - float(row["before_reward"]), 9),
                "before_episode_count": row["before_episodes"],
                "after_episode_count": row["after_episodes"],
                "episode_delta": int(row["after_episodes"]) - int(row["before_episodes"]),
                "families": ",".join(sorted(name for name in row["families"] if name)),
            }
        )
    detail.sort(key=lambda item: (str(item["compare_state"]), str(item["family_action"])))
    summary_rows.sort(key=lambda item: (str(item["compare_state"]), str(item["families"])))
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
    detail_csv = output_dir / "dio_mini_passive_variant_reife_map_compare.csv"
    summary_csv = output_dir / "dio_mini_passive_variant_reife_map_compare_summary.csv"
    json_path = output_dir / "dio_mini_passive_variant_reife_map_compare.json"
    md_path = output_dir / "dio_mini_passive_variant_reife_map_compare.md"

    _write_csv(detail_csv, detail, ["family_action", "compare_state", "before_variant_reife_state", "after_variant_reife_state"])
    _write_csv(summary_csv, summary, ["compare_state", "count", "reward_delta", "episode_delta"])
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_variant_reife_map_compare.v1",
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
        "# Mini-DIO Passive Variant Reife Map Compare",
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
            f"episode_delta={row['episode_delta']} "
            f"families={row['families'] or '-'}"
        )
    lines.extend(["", "## Grenze"])
    lines.extend(
        [
            "- passive_only=true",
            "- writes_training_memory=false",
            "- read_by_mini_dio=false",
            "- influences_action=false",
            "- is_gate=false",
            "- is_motoric=false",
        ]
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", required=True, type=Path)
    parser.add_argument("--after", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    detail, summary = build_compare_rows(args.before, args.after)
    write_outputs(args.output_dir, args.before, args.after, detail, summary)
    print(f"passive_variant_reife_map_compare rows={len(detail)} summary={len(summary)}")
    for row in summary:
        print(
            f"{row['compare_state']} count={row['count']} "
            f"reward_delta={row['reward_delta']} episode_delta={row['episode_delta']}"
        )


if __name__ == "__main__":
    main()
