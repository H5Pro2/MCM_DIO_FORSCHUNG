"""Consolidate passive Mini-DIO conflict reflection reports.

This report reads passive conflict reflection outputs and summarizes whether
burdened action traces reorganize into WAIT/observation across controlled
variants.

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


def _resolve_conflict_csv(path: Path) -> Path:
    if path.is_dir():
        return path / "dio_mini_passive_conflict_reflection.csv"
    return path


def build_rows(sources: list[tuple[str, Path]]) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    detail: list[dict] = []
    for label, source in sources:
        csv_path = _resolve_conflict_csv(source)
        if not csv_path.exists():
            continue
        for row in _read_csv(csv_path):
            detail.append(
                {
                    "source": label,
                    "symbol_family": str(row.get("symbol_family", "") or ""),
                    "burden_family_action": str(row.get("burden_family_action", "") or ""),
                    "burden_action": str(row.get("burden_action", "") or ""),
                    "reflection_state": str(row.get("reflection_state", "") or ""),
                    "reward_delta": round(_safe_float(row.get("reward_delta")), 9),
                    "episode_delta": _safe_int(row.get("episode_delta")),
                    "before_reward": round(_safe_float(row.get("before_reward")), 9),
                    "after_reward": round(_safe_float(row.get("after_reward")), 9),
                    "before_episode_count": _safe_int(row.get("before_episode_count")),
                    "after_episode_count": _safe_int(row.get("after_episode_count")),
                    "wait_trace_count": _safe_int(row.get("wait_trace_count")),
                    "wait_related_observation_count": _safe_int(row.get("wait_related_observation_count")),
                    "wait_family_actions": str(row.get("wait_family_actions", "") or ""),
                    "dio_syntax_sentence": str(row.get("dio_syntax_sentence", "") or ""),
                    "passive_only": 1,
                    "writes_training_memory": 0,
                    "read_by_mini_dio": 0,
                    "influences_action": 0,
                    "is_gate": 0,
                    "is_motoric": 0,
                }
            )

    by_state: dict[str, dict] = {}
    by_family: dict[str, dict] = {}
    for row in detail:
        state = str(row.get("reflection_state", "") or "")
        family = str(row.get("symbol_family", "") or "")
        state_bucket = by_state.setdefault(
            state,
            {
                "reflection_state": state,
                "count": 0,
                "reward_delta": 0.0,
                "episode_delta": 0,
                "families": [],
                "actions": [],
                "sources": [],
            },
        )
        family_bucket = by_family.setdefault(
            family,
            {
                "symbol_family": family,
                "count": 0,
                "reflection_states": [],
                "reward_delta": 0.0,
                "episode_delta": 0,
                "actions": [],
                "sources": [],
                "wait_trace_count": 0,
            },
        )
        for bucket in (state_bucket, family_bucket):
            bucket["count"] += 1
            bucket["reward_delta"] += _safe_float(row.get("reward_delta"))
            bucket["episode_delta"] += _safe_int(row.get("episode_delta"))
            bucket["actions"].append(str(row.get("burden_action", "") or ""))
            bucket["sources"].append(str(row.get("source", "") or ""))
        state_bucket["families"].append(family)
        family_bucket["reflection_states"].append(state)
        family_bucket["wait_trace_count"] += _safe_int(row.get("wait_trace_count"))

    state_summary = [
        {
            "reflection_state": row["reflection_state"],
            "count": row["count"],
            "reward_delta": round(float(row["reward_delta"]), 9),
            "episode_delta": row["episode_delta"],
            "families": ",".join(sorted(set(row["families"]))),
            "actions": ",".join(sorted(set(action for action in row["actions"] if action))),
            "sources": ",".join(sorted(set(source for source in row["sources"] if source))),
        }
        for row in by_state.values()
    ]
    family_summary = [
        {
            "symbol_family": row["symbol_family"],
            "count": row["count"],
            "reflection_states": ",".join(sorted(set(row["reflection_states"]))),
            "reward_delta": round(float(row["reward_delta"]), 9),
            "episode_delta": row["episode_delta"],
            "actions": ",".join(sorted(set(action for action in row["actions"] if action))),
            "sources": ",".join(sorted(set(source for source in row["sources"] if source))),
            "wait_trace_count": row["wait_trace_count"],
        }
        for row in by_family.values()
    ]

    reflection_rows: list[dict] = []
    reorganized = [
        row
        for row in detail
        if str(row.get("reflection_state", "") or "") == "burden_reorganized_into_observation"
    ]
    if reorganized:
        families = sorted(set(str(row.get("symbol_family", "") or "") for row in reorganized))
        actions = sorted(set(str(row.get("burden_action", "") or "") for row in reorganized))
        reward_delta = sum(_safe_float(row.get("reward_delta")) for row in reorganized)
        episode_delta = sum(_safe_int(row.get("episode_delta")) for row in reorganized)
        reflection_rows.append(
            {
                "reflection_key": "burden_reorganizes_into_observation_across_variants",
                "reflection_state": "repeated_burden_to_observation",
                "count": len(reorganized),
                "reward_delta": round(reward_delta, 9),
                "episode_delta": episode_delta,
                "families": ",".join(families),
                "actions": ",".join(actions),
                "dio_syntax_sentence": (
                    "conflict_stability|burden_to_observation|"
                    f"families={','.join(families)}|count={len(reorganized)}|"
                    f"reward_delta={reward_delta:.6f}|episode_delta={episode_delta}"
                ),
                "reflection_sentence": (
                    "Mehrere kontrollierte Varianten zeigen dieselbe passive Richtung: "
                    "Belastete Handlung wird weniger wiederholt und bleibt als Beobachtung lesbar."
                ),
                "passive_only": 1,
                "writes_training_memory": 0,
                "read_by_mini_dio": 0,
                "influences_action": 0,
                "is_gate": 0,
                "is_motoric": 0,
            }
        )

    detail.sort(key=lambda item: (str(item["source"]), str(item["symbol_family"])))
    state_summary.sort(key=lambda item: str(item["reflection_state"]))
    family_summary.sort(key=lambda item: str(item["symbol_family"]))
    reflection_rows.sort(key=lambda item: str(item["reflection_key"]))
    return detail, state_summary, family_summary, reflection_rows


def write_outputs(
    output_dir: Path,
    sources: list[tuple[str, Path]],
    detail: list[dict],
    state_summary: list[dict],
    family_summary: list[dict],
    reflection_rows: list[dict],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_conflict_stability_detail.csv"
    state_csv = output_dir / "dio_mini_passive_conflict_stability_state_summary.csv"
    family_csv = output_dir / "dio_mini_passive_conflict_stability_family_summary.csv"
    reflection_csv = output_dir / "dio_mini_passive_conflict_stability_reflection.csv"
    json_path = output_dir / "dio_mini_passive_conflict_stability.json"
    md_path = output_dir / "dio_mini_passive_conflict_stability.md"
    txt_path = output_dir / "dio_mini_passive_conflict_stability.txt"

    _write_csv(detail_csv, detail, ["source", "symbol_family", "burden_family_action", "reflection_state"])
    _write_csv(state_csv, state_summary, ["reflection_state", "count", "reward_delta", "episode_delta"])
    _write_csv(family_csv, family_summary, ["symbol_family", "count", "reflection_states", "reward_delta"])
    _write_csv(reflection_csv, reflection_rows, ["reflection_key", "reflection_state", "count", "families"])
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_conflict_stability.v1",
                "sources": [{"label": label, "path": str(path)} for label, path in sources],
                "detail": detail,
                "state_summary": state_summary,
                "family_summary": family_summary,
                "reflection": reflection_rows,
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
        "# Mini-DIO Passive Conflict Stability",
        "",
        "## Sources",
    ]
    for label, path in sources:
        lines.append(f"- {label}: `{path}`")
    lines.extend(["", "## State Summary"])
    if not state_summary:
        lines.append("- keine Konfliktspuren")
    for row in state_summary:
        lines.append(
            f"- {row['reflection_state']}: count={row['count']} "
            f"reward_delta={float(row['reward_delta']):.6f} "
            f"episode_delta={row['episode_delta']} "
            f"families={row['families'] or '-'}"
        )
    lines.extend(["", "## Passive Reflection"])
    if not reflection_rows:
        lines.append("- keine wiederholte Konflikt-Reorganisation sichtbar")
    for row in reflection_rows:
        lines.extend(
            [
                f"- {row['reflection_state']}: count={row['count']} families={row['families']}",
                f"  DIO-Syntax: `{row['dio_syntax_sentence']}`",
                f"  Lesung: {row['reflection_sentence']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Konflikt-Stabilitaetskarte",
            "- keine Handlung",
            "- kein Gate",
            "- keine Motorik",
            "- kein Trainingsmemory",
            "- Mini-DIO liest diesen Bericht nicht aktiv",
        ]
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    txt_path.write_text("\n".join(str(row["dio_syntax_sentence"]) for row in reflection_rows) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--conflict", action="append", required=True, help="label=dir_or_csv; can be repeated")
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    sources = [_parse_source(item) for item in args.conflict]
    detail, state_summary, family_summary, reflection_rows = build_rows(sources)
    write_outputs(args.output_dir, sources, detail, state_summary, family_summary, reflection_rows)
    print(
        f"passive_conflict_stability detail={len(detail)} "
        f"states={len(state_summary)} families={len(family_summary)} reflections={len(reflection_rows)}"
    )
    for row in state_summary:
        print(
            f"{row['reflection_state']} count={row['count']} "
            f"reward_delta={row['reward_delta']} episode_delta={row['episode_delta']}"
        )


if __name__ == "__main__":
    main()
