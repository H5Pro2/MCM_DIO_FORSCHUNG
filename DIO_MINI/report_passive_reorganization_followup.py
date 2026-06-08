"""Check passive follow-up state for previously reorganized conflict families.

The report reads passive inner-awareness families and one or more latest
variant maturity maps. It verifies whether a previously burdened action stays
out of action while the same family remains observable as WAIT.

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


def _awareness_csv(path: Path) -> Path:
    if path.is_dir():
        return path / "dio_mini_passive_conflict_stability_inner_awareness_family.csv"
    return path


def _variant_map_csv(path: Path) -> Path:
    if path.is_dir():
        return path / "dio_mini_passive_variant_reife_map.csv"
    return path


def _state_for(action_row: dict | None, wait_row: dict | None) -> str:
    action_state = str((action_row or {}).get("variant_reife_state", "") or "")
    wait_state = str((wait_row or {}).get("variant_reife_state", "") or "")
    action_reward = _safe_float((action_row or {}).get("event_reward_sum"))
    if action_row and action_state == "variant_self_burden_action_trace":
        if wait_row:
            return "reorganization_still_softening_with_wait"
        return "reorganization_still_burdened_without_wait"
    if action_row and action_reward > 0.0:
        return "reorganization_shifted_back_to_carried_action"
    if wait_row and wait_state in ("variant_related_observation_trace", "variant_local_wait_context"):
        return "reorganization_quiet_wait_continues"
    if wait_row:
        return "reorganization_wait_visible"
    return "reorganization_family_not_seen"


def build_rows(awareness: Path, latest_sources: list[tuple[str, Path]]) -> tuple[list[dict], list[dict]]:
    awareness_rows = _read_csv(_awareness_csv(awareness))
    known = [
        row
        for row in awareness_rows
        if str(row.get("inner_awareness_state", "") or "") == "family_burden_reorganized_to_observation"
    ]
    detail: list[dict] = []
    for label, source in latest_sources:
        rows = _read_csv(_variant_map_csv(source))
        by_family_action = {str(row.get("family_action", "") or ""): row for row in rows}
        for item in known:
            family = str(item.get("symbol_family", "") or "")
            action = str(item.get("burden_action", "") or "")
            action_key = f"{family}:{action}"
            wait_key = f"{family}:WAIT"
            action_row = by_family_action.get(action_key)
            wait_row = by_family_action.get(wait_key)
            followup_state = _state_for(action_row, wait_row)
            detail.append(
                {
                    "source": label,
                    "symbol_family": family,
                    "burden_action": action,
                    "followup_state": followup_state,
                    "action_present": 1 if action_row else 0,
                    "wait_present": 1 if wait_row else 0,
                    "action_variant_state": str((action_row or {}).get("variant_reife_state", "") or ""),
                    "wait_variant_state": str((wait_row or {}).get("variant_reife_state", "") or ""),
                    "action_reward": round(_safe_float((action_row or {}).get("event_reward_sum")), 9),
                    "wait_reward": round(_safe_float((wait_row or {}).get("event_reward_sum")), 9),
                    "action_episodes": _safe_int((action_row or {}).get("episode_count")),
                    "wait_episodes": _safe_int((wait_row or {}).get("episode_count")),
                    "dio_syntax_sentence": (
                        f"reorganization_followup|{family}|{action}|{followup_state}|"
                        f"source={label}|action={1 if action_row else 0}|wait={1 if wait_row else 0}"
                    ),
                    "passive_only": 1,
                    "writes_training_memory": 0,
                    "read_by_mini_dio": 0,
                    "influences_action": 0,
                    "is_gate": 0,
                    "is_motoric": 0,
                }
            )

    summary_buckets: dict[str, dict] = {}
    for row in detail:
        state = str(row.get("followup_state", "") or "")
        bucket = summary_buckets.setdefault(
            state,
            {
                "followup_state": state,
                "count": 0,
                "families": [],
                "sources": [],
                "wait_present_count": 0,
                "action_present_count": 0,
            },
        )
        bucket["count"] += 1
        bucket["families"].append(str(row.get("symbol_family", "") or ""))
        bucket["sources"].append(str(row.get("source", "") or ""))
        bucket["wait_present_count"] += _safe_int(row.get("wait_present"))
        bucket["action_present_count"] += _safe_int(row.get("action_present"))
    summary = [
        {
            "followup_state": row["followup_state"],
            "count": row["count"],
            "families": ",".join(sorted(set(row["families"]))),
            "sources": ",".join(sorted(set(row["sources"]))),
            "wait_present_count": row["wait_present_count"],
            "action_present_count": row["action_present_count"],
        }
        for row in summary_buckets.values()
    ]
    detail.sort(key=lambda row: (str(row["source"]), str(row["symbol_family"])))
    summary.sort(key=lambda row: str(row["followup_state"]))
    return detail, summary


def write_outputs(
    output_dir: Path,
    awareness: Path,
    latest_sources: list[tuple[str, Path]],
    detail: list[dict],
    summary: list[dict],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_reorganization_followup_detail.csv"
    summary_csv = output_dir / "dio_mini_passive_reorganization_followup_summary.csv"
    json_path = output_dir / "dio_mini_passive_reorganization_followup.json"
    md_path = output_dir / "dio_mini_passive_reorganization_followup.md"
    txt_path = output_dir / "dio_mini_passive_reorganization_followup.txt"

    _write_csv(detail_csv, detail, ["source", "symbol_family", "burden_action", "followup_state"])
    _write_csv(summary_csv, summary, ["followup_state", "count", "families", "sources"])
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_reorganization_followup.v1",
                "awareness": str(awareness),
                "latest_sources": [{"label": label, "path": str(path)} for label, path in latest_sources],
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

    lines = [
        "# Mini-DIO Passive Reorganization Follow-up",
        "",
        f"- awareness: `{awareness}`",
        "",
        "## Summary",
    ]
    if not summary:
        lines.append("- keine Reorganisationsfamilien")
    for row in summary:
        lines.append(
            f"- {row['followup_state']}: count={row['count']} "
            f"families={row['families'] or '-'} sources={row['sources'] or '-'} "
            f"wait={row['wait_present_count']} action={row['action_present_count']}"
        )
    lines.extend(["", "## Detail"])
    for row in detail:
        lines.append(
            f"- {row['source']} {row['symbol_family']}:{row['burden_action']} -> "
            f"{row['followup_state']} "
            f"(action={row['action_present']}, wait={row['wait_present']})"
        )
        lines.append(f"  DIO-Syntax: `{row['dio_syntax_sentence']}`")
    lines.extend(
        [
            "",
            "## Grenze",
            "- passiver Follow-up-Leser",
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
    parser.add_argument("--awareness", required=True, type=Path)
    parser.add_argument("--latest-map", action="append", required=True, help="label=dir_or_csv; can be repeated")
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    latest_sources = [_parse_source(item) for item in args.latest_map]
    detail, summary = build_rows(args.awareness, latest_sources)
    write_outputs(args.output_dir, args.awareness, latest_sources, detail, summary)
    print(f"passive_reorganization_followup detail={len(detail)} summary={len(summary)}")
    for row in summary:
        print(
            f"{row['followup_state']} count={row['count']} "
            f"families={row['families']} wait={row['wait_present_count']} action={row['action_present_count']}"
        )


if __name__ == "__main__":
    main()
