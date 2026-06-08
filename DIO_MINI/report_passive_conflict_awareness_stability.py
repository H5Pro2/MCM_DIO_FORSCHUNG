"""Track passive conflict inner-awareness across reports.

The report consolidates one or more passive conflict inner-awareness maps and
keeps them as an external reflection layer. It does not write Mini-DIO memory
and does not influence action.
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


def _family_csv(path: Path) -> Path:
    if path.is_dir():
        return path / "dio_mini_passive_conflict_stability_inner_awareness_family.csv"
    return path


def _global_csv(path: Path) -> Path:
    if path.is_dir():
        return path / "dio_mini_passive_conflict_stability_inner_awareness_global.csv"
    return path


def build_rows(sources: list[tuple[str, Path]]) -> tuple[list[dict], list[dict], list[dict]]:
    detail: list[dict] = []
    global_detail: list[dict] = []
    for label, source in sources:
        family_path = _family_csv(source)
        if family_path.exists():
            for row in _read_csv(family_path):
                detail.append(
                    {
                        "source": label,
                        "symbol_family": str(row.get("symbol_family", "") or ""),
                        "burden_action": str(row.get("burden_action", "") or ""),
                        "inner_awareness_state": str(row.get("inner_awareness_state", "") or ""),
                        "reward_delta": round(_safe_float(row.get("reward_delta")), 9),
                        "episode_delta": _safe_int(row.get("episode_delta")),
                        "wait_trace_count": _safe_int(row.get("wait_trace_count")),
                        "dio_syntax_sentence": str(row.get("dio_syntax_sentence", "") or ""),
                        "passive_only": 1,
                        "writes_training_memory": 0,
                        "read_by_mini_dio": 0,
                        "influences_action": 0,
                        "is_gate": 0,
                        "is_motoric": 0,
                    }
                )
        global_path = _global_csv(source)
        if global_path.exists():
            for row in _read_csv(global_path):
                global_detail.append(
                    {
                        "source": label,
                        "inner_awareness_key": str(row.get("inner_awareness_key", "") or ""),
                        "inner_awareness_state": str(row.get("inner_awareness_state", "") or ""),
                        "count": _safe_int(row.get("count")),
                        "families": str(row.get("families", "") or ""),
                        "reward_delta": round(_safe_float(row.get("reward_delta")), 9),
                        "episode_delta": _safe_int(row.get("episode_delta")),
                        "dio_syntax_sentence": str(row.get("dio_syntax_sentence", "") or ""),
                        "passive_only": 1,
                        "writes_training_memory": 0,
                        "read_by_mini_dio": 0,
                        "influences_action": 0,
                        "is_gate": 0,
                        "is_motoric": 0,
                    }
                )

    by_family: dict[str, dict] = {}
    for row in detail:
        family = str(row.get("symbol_family", "") or "")
        bucket = by_family.setdefault(
            family,
            {
                "symbol_family": family,
                "source_count": 0,
                "states": [],
                "actions": [],
                "sources": [],
                "reward_delta": 0.0,
                "episode_delta": 0,
                "wait_trace_count": 0,
            },
        )
        bucket["source_count"] += 1
        bucket["states"].append(str(row.get("inner_awareness_state", "") or ""))
        bucket["actions"].append(str(row.get("burden_action", "") or ""))
        bucket["sources"].append(str(row.get("source", "") or ""))
        bucket["reward_delta"] += _safe_float(row.get("reward_delta"))
        bucket["episode_delta"] += _safe_int(row.get("episode_delta"))
        bucket["wait_trace_count"] += _safe_int(row.get("wait_trace_count"))

    family_summary: list[dict] = []
    for row in by_family.values():
        states = sorted(set(state for state in row["states"] if state))
        reflection_state = (
            "stable_passive_reorganization_trace"
            if "family_burden_reorganized_to_observation" in states
            else "open_passive_conflict_trace"
        )
        family_summary.append(
            {
                "symbol_family": row["symbol_family"],
                "reflection_state": reflection_state,
                "source_count": row["source_count"],
                "states": ",".join(states),
                "actions": ",".join(sorted(set(action for action in row["actions"] if action))),
                "sources": ",".join(sorted(set(source for source in row["sources"] if source))),
                "reward_delta": round(float(row["reward_delta"]), 9),
                "episode_delta": row["episode_delta"],
                "wait_trace_count": row["wait_trace_count"],
                "dio_syntax_sentence": (
                    f"conflict_awareness_stability|{row['symbol_family']}|"
                    f"{reflection_state}|sources={row['source_count']}|"
                    f"wait={row['wait_trace_count']}"
                ),
                "passive_only": 1,
                "writes_training_memory": 0,
                "read_by_mini_dio": 0,
                "influences_action": 0,
                "is_gate": 0,
                "is_motoric": 0,
            }
        )

    family_summary.sort(key=lambda item: str(item["symbol_family"]))
    detail.sort(key=lambda item: (str(item["source"]), str(item["symbol_family"])))
    global_detail.sort(key=lambda item: (str(item["source"]), str(item["inner_awareness_key"])))
    return detail, global_detail, family_summary


def write_outputs(
    output_dir: Path,
    sources: list[tuple[str, Path]],
    detail: list[dict],
    global_detail: list[dict],
    family_summary: list[dict],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_conflict_awareness_stability_detail.csv"
    global_csv = output_dir / "dio_mini_passive_conflict_awareness_stability_global.csv"
    family_csv = output_dir / "dio_mini_passive_conflict_awareness_stability_family.csv"
    json_path = output_dir / "dio_mini_passive_conflict_awareness_stability.json"
    md_path = output_dir / "dio_mini_passive_conflict_awareness_stability.md"
    txt_path = output_dir / "dio_mini_passive_conflict_awareness_stability.txt"

    _write_csv(detail_csv, detail, ["source", "symbol_family", "inner_awareness_state"])
    _write_csv(global_csv, global_detail, ["source", "inner_awareness_key", "inner_awareness_state"])
    _write_csv(family_csv, family_summary, ["symbol_family", "reflection_state", "source_count"])
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_conflict_awareness_stability.v1",
                "sources": [{"label": label, "path": str(path)} for label, path in sources],
                "detail": detail,
                "global": global_detail,
                "family_summary": family_summary,
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

    lines = ["# Mini-DIO Passive Conflict Awareness Stability", "", "## Sources"]
    for label, path in sources:
        lines.append(f"- {label}: `{path}`")
    lines.extend(["", "## Family Summary"])
    if not family_summary:
        lines.append("- keine passiven Konflikt-Innenwahrnehmungen")
    for row in family_summary:
        lines.extend(
            [
                f"- {row['symbol_family']}: {row['reflection_state']}",
                f"  DIO-Syntax: `{row['dio_syntax_sentence']}`",
                f"  sources={row['sources']} actions={row['actions']} "
                f"reward_delta={float(row['reward_delta']):.6f} "
                f"episode_delta={row['episode_delta']} wait={row['wait_trace_count']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Reflexionsschicht",
            "- keine Handlung",
            "- kein Gate",
            "- keine Motorik",
            "- kein Trainingsmemory",
            "- Mini-DIO liest diesen Bericht nicht aktiv",
        ]
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    txt_path.write_text(
        "\n".join(str(row["dio_syntax_sentence"]) for row in family_summary) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--awareness", action="append", required=True, help="label=dir_or_csv; can be repeated")
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    sources = [_parse_source(item) for item in args.awareness]
    detail, global_detail, family_summary = build_rows(sources)
    write_outputs(args.output_dir, sources, detail, global_detail, family_summary)
    print(
        f"passive_conflict_awareness_stability detail={len(detail)} "
        f"global={len(global_detail)} families={len(family_summary)}"
    )
    for row in family_summary:
        print(f"{row['symbol_family']} {row['reflection_state']} sources={row['source_count']}")


if __name__ == "__main__":
    main()
