"""Build passive history for reorganized Mini-DIO families.

The report consolidates passive reorganization follow-up rows across one or
more runs. It classifies whether a family remains a quiet WAIT observation,
disappears from the checked world, or becomes action-present again.

Diagnostic only:
- no memory writes
- no Mini-DIO action influence
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


def _parse_source(raw: str) -> tuple[str, Path]:
    if "=" in raw:
        label, path = raw.split("=", 1)
        return label.strip(), Path(path.strip())
    path = Path(raw.strip())
    return path.name, path


def _followup_csv(path: Path) -> Path:
    if path.is_dir():
        return path / "dio_mini_passive_reorganization_followup_detail.csv"
    return path


def _history_state(quiet_wait: int, not_seen: int, action_present: int, burden_action: int, carried_action: int) -> str:
    if action_present and burden_action:
        return "reorganization_history_action_burden_reappeared"
    if action_present and carried_action:
        return "reorganization_history_action_reappeared_carried"
    if quiet_wait and not action_present:
        if not_seen:
            return "reorganization_history_quiet_wait_with_world_absence"
        return "reorganization_history_quiet_wait_stable"
    if not_seen and not action_present:
        return "reorganization_history_not_seen"
    return "reorganization_history_open"


def build_rows(sources: list[tuple[str, Path]]) -> tuple[list[dict], list[dict]]:
    detail: list[dict] = []
    for label, source in sources:
        csv_path = _followup_csv(source)
        if not csv_path.exists():
            continue
        for row in _read_csv(csv_path):
            action_present = _safe_int(row.get("action_present"))
            action_state = str(row.get("action_variant_state", "") or "")
            detail.append(
                {
                    "history_source": label,
                    "source": str(row.get("source", "") or ""),
                    "symbol_family": str(row.get("symbol_family", "") or ""),
                    "burden_action": str(row.get("burden_action", "") or ""),
                    "followup_state": str(row.get("followup_state", "") or ""),
                    "action_present": action_present,
                    "wait_present": _safe_int(row.get("wait_present")),
                    "action_variant_state": action_state,
                    "wait_variant_state": str(row.get("wait_variant_state", "") or ""),
                    "action_reward": round(_safe_float(row.get("action_reward")), 9),
                    "wait_reward": round(_safe_float(row.get("wait_reward")), 9),
                    "action_episodes": _safe_int(row.get("action_episodes")),
                    "wait_episodes": _safe_int(row.get("wait_episodes")),
                    "passive_only": 1,
                    "writes_training_memory": 0,
                    "read_by_mini_dio": 0,
                    "influences_action": 0,
                    "is_gate": 0,
                    "is_motoric": 0,
                }
            )

    buckets: dict[str, dict] = {}
    for row in detail:
        family = str(row.get("symbol_family", "") or "")
        action = str(row.get("burden_action", "") or "")
        key = f"{family}:{action}"
        bucket = buckets.setdefault(
            key,
            {
                "family_action": key,
                "symbol_family": family,
                "burden_action": action,
                "observations": 0,
                "quiet_wait_count": 0,
                "not_seen_count": 0,
                "action_present_count": 0,
                "burden_action_count": 0,
                "carried_action_count": 0,
                "wait_episode_sum": 0,
                "action_episode_sum": 0,
                "action_reward_sum": 0.0,
                "sources": [],
                "history_sources": [],
                "followup_states": [],
            },
        )
        followup_state = str(row.get("followup_state", "") or "")
        action_state = str(row.get("action_variant_state", "") or "")
        action_present = _safe_int(row.get("action_present"))
        bucket["observations"] += 1
        bucket["quiet_wait_count"] += 1 if followup_state == "reorganization_quiet_wait_continues" else 0
        bucket["not_seen_count"] += 1 if followup_state == "reorganization_family_not_seen" else 0
        bucket["action_present_count"] += action_present
        bucket["burden_action_count"] += 1 if action_present and action_state == "variant_self_burden_action_trace" else 0
        bucket["carried_action_count"] += 1 if action_present and action_state == "variant_self_carried_action_trace" else 0
        bucket["wait_episode_sum"] += _safe_int(row.get("wait_episodes"))
        bucket["action_episode_sum"] += _safe_int(row.get("action_episodes"))
        bucket["action_reward_sum"] += _safe_float(row.get("action_reward"))
        bucket["sources"].append(str(row.get("source", "") or ""))
        bucket["history_sources"].append(str(row.get("history_source", "") or ""))
        bucket["followup_states"].append(followup_state)

    summary: list[dict] = []
    for row in buckets.values():
        history_state = _history_state(
            int(row["quiet_wait_count"]),
            int(row["not_seen_count"]),
            int(row["action_present_count"]),
            int(row["burden_action_count"]),
            int(row["carried_action_count"]),
        )
        summary.append(
            {
                "family_action": row["family_action"],
                "symbol_family": row["symbol_family"],
                "burden_action": row["burden_action"],
                "history_state": history_state,
                "observations": row["observations"],
                "quiet_wait_count": row["quiet_wait_count"],
                "not_seen_count": row["not_seen_count"],
                "action_present_count": row["action_present_count"],
                "burden_action_count": row["burden_action_count"],
                "carried_action_count": row["carried_action_count"],
                "wait_episode_sum": row["wait_episode_sum"],
                "action_episode_sum": row["action_episode_sum"],
                "action_reward_sum": round(float(row["action_reward_sum"]), 9),
                "sources": ",".join(sorted(set(source for source in row["sources"] if source))),
                "history_sources": ",".join(sorted(set(source for source in row["history_sources"] if source))),
                "followup_states": ",".join(sorted(set(state for state in row["followup_states"] if state))),
                "dio_syntax_sentence": (
                    f"reorganization_history|{row['symbol_family']}|{row['burden_action']}|"
                    f"{history_state}|quiet={row['quiet_wait_count']}|"
                    f"not_seen={row['not_seen_count']}|action={row['action_present_count']}"
                ),
                "passive_only": 1,
                "writes_training_memory": 0,
                "read_by_mini_dio": 0,
                "influences_action": 0,
                "is_gate": 0,
                "is_motoric": 0,
            }
        )
    detail.sort(key=lambda item: (str(item["history_source"]), str(item["source"]), str(item["symbol_family"])))
    summary.sort(key=lambda item: str(item["family_action"]))
    return detail, summary


def write_outputs(output_dir: Path, sources: list[tuple[str, Path]], detail: list[dict], summary: list[dict]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_reorganization_history_detail.csv"
    summary_csv = output_dir / "dio_mini_passive_reorganization_history_summary.csv"
    json_path = output_dir / "dio_mini_passive_reorganization_history.json"
    md_path = output_dir / "dio_mini_passive_reorganization_history.md"
    txt_path = output_dir / "dio_mini_passive_reorganization_history.txt"

    _write_csv(detail_csv, detail, ["history_source", "source", "symbol_family", "followup_state"])
    _write_csv(summary_csv, summary, ["family_action", "history_state", "observations"])
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_reorganization_history.v1",
                "sources": [{"label": label, "path": str(path)} for label, path in sources],
                "detail": detail,
                "summary": summary,
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

    lines = ["# Mini-DIO Passive Reorganization History", "", "## Sources"]
    for label, path in sources:
        lines.append(f"- {label}: `{path}`")
    lines.extend(["", "## Summary"])
    if not summary:
        lines.append("- keine Reorganisationshistorie")
    for row in summary:
        lines.extend(
            [
                f"- {row['family_action']}: {row['history_state']}",
                f"  DIO-Syntax: `{row['dio_syntax_sentence']}`",
                f"  quiet={row['quiet_wait_count']} not_seen={row['not_seen_count']} "
                f"action={row['action_present_count']} wait_episodes={row['wait_episode_sum']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Reflexionshistorie",
            "- keine Handlung",
            "- kein Gate",
            "- keine Motorik",
            "- kein Trainingsmemory",
            "- Mini-DIO liest diesen Bericht nicht aktiv",
        ]
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    txt_path.write_text("\n".join(str(row["dio_syntax_sentence"]) for row in summary) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--followup", action="append", required=True, help="label=dir_or_csv; can be repeated")
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    sources = [_parse_source(item) for item in args.followup]
    detail, summary = build_rows(sources)
    write_outputs(args.output_dir, sources, detail, summary)
    print(f"passive_reorganization_history detail={len(detail)} summary={len(summary)}")
    for row in summary:
        print(
            f"{row['family_action']} {row['history_state']} "
            f"quiet={row['quiet_wait_count']} action={row['action_present_count']}"
        )


if __name__ == "__main__":
    main()
