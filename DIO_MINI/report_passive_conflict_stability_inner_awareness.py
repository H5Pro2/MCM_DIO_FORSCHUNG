"""Translate passive conflict stability into Mini-DIO inner-awareness text.

This report reads the consolidated passive conflict stability output and turns
it into compact DIO syntax plus human-readable sentences.

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


def _resolve(path: Path, filename: str) -> Path:
    if path.is_dir():
        return path / filename
    return path


def _detail_sentence(row: dict) -> str:
    family = str(row.get("symbol_family", "") or "-")
    action = str(row.get("burden_action", "") or "-")
    before_reward = _safe_float(row.get("before_reward"))
    after_reward = _safe_float(row.get("after_reward"))
    before_episodes = _safe_int(row.get("before_episode_count"))
    after_episodes = _safe_int(row.get("after_episode_count"))
    wait = _safe_int(row.get("wait_trace_count"))
    return (
        f"{family}: {action} hat belastet. "
        f"Die Wiederholung wurde schwacher ({before_reward:.6f}->{after_reward:.6f}, "
        f"Episoden {before_episodes}->{after_episodes}). "
        f"Die Familie bleibt als Beobachtung sichtbar (WAIT-Spuren={wait})."
    )


def build_rows(stability_dir_or_detail: Path, reflection_dir_or_csv: Path) -> tuple[list[dict], list[dict]]:
    detail_csv = _resolve(stability_dir_or_detail, "dio_mini_passive_conflict_stability_detail.csv")
    reflection_csv = _resolve(reflection_dir_or_csv, "dio_mini_passive_conflict_stability_reflection.csv")
    detail_rows = _read_csv(detail_csv) if detail_csv.exists() else []
    reflection_rows = _read_csv(reflection_csv) if reflection_csv.exists() else []

    family_rows: list[dict] = []
    for row in detail_rows:
        state = str(row.get("reflection_state", "") or "")
        family = str(row.get("symbol_family", "") or "")
        action = str(row.get("burden_action", "") or "")
        family_rows.append(
            {
                "symbol_family": family,
                "source": str(row.get("source", "") or ""),
                "burden_action": action,
                "inner_awareness_state": "family_burden_reorganized_to_observation"
                if state == "burden_reorganized_into_observation"
                else "family_conflict_open",
                "reward_delta": round(_safe_float(row.get("reward_delta")), 9),
                "episode_delta": _safe_int(row.get("episode_delta")),
                "wait_trace_count": _safe_int(row.get("wait_trace_count")),
                "dio_syntax_sentence": (
                    f"inner_conflict_awareness|{family}|{action}|"
                    f"burden_to_observation|reward_delta={_safe_float(row.get('reward_delta')):.6f}|"
                    f"wait={_safe_int(row.get('wait_trace_count'))}"
                ),
                "inner_sentence": _detail_sentence(row),
                "passive_only": 1,
                "writes_training_memory": 0,
                "read_by_mini_dio": 0,
                "influences_action": 0,
                "is_gate": 0,
                "is_motoric": 0,
            }
        )

    global_rows: list[dict] = []
    for row in reflection_rows:
        families = str(row.get("families", "") or "")
        count = _safe_int(row.get("count"))
        reward_delta = _safe_float(row.get("reward_delta"))
        episode_delta = _safe_int(row.get("episode_delta"))
        global_rows.append(
            {
                "inner_awareness_key": "repeated_burden_to_observation",
                "inner_awareness_state": str(row.get("reflection_state", "") or ""),
                "count": count,
                "families": families,
                "reward_delta": round(reward_delta, 9),
                "episode_delta": episode_delta,
                "dio_syntax_sentence": (
                    f"inner_conflict_awareness|global|burden_to_observation|"
                    f"families={families}|count={count}|reward_delta={reward_delta:.6f}|"
                    f"episode_delta={episode_delta}"
                ),
                "inner_sentence": (
                    "Mehrere Familien zeigen: belastete Handlung wird weniger wiederholt, "
                    "aber die Familie bleibt beobachtbar. Das ist Reorganisation, keine Angstsperre."
                ),
                "passive_only": 1,
                "writes_training_memory": 0,
                "read_by_mini_dio": 0,
                "influences_action": 0,
                "is_gate": 0,
                "is_motoric": 0,
            }
        )

    family_rows.sort(key=lambda item: str(item["symbol_family"]))
    global_rows.sort(key=lambda item: str(item["inner_awareness_key"]))
    return family_rows, global_rows


def write_outputs(output_dir: Path, family_rows: list[dict], global_rows: list[dict]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    family_csv = output_dir / "dio_mini_passive_conflict_stability_inner_awareness_family.csv"
    global_csv = output_dir / "dio_mini_passive_conflict_stability_inner_awareness_global.csv"
    json_path = output_dir / "dio_mini_passive_conflict_stability_inner_awareness.json"
    md_path = output_dir / "dio_mini_passive_conflict_stability_inner_awareness.md"
    txt_path = output_dir / "dio_mini_passive_conflict_stability_inner_awareness.txt"

    _write_csv(family_csv, family_rows, ["symbol_family", "inner_awareness_state", "dio_syntax_sentence"])
    _write_csv(global_csv, global_rows, ["inner_awareness_key", "inner_awareness_state", "dio_syntax_sentence"])
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_conflict_stability_inner_awareness.v1",
                "family": family_rows,
                "global": global_rows,
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

    lines = ["# Mini-DIO Passive Conflict Stability Inner Awareness", ""]
    lines.append("## Global")
    if not global_rows:
        lines.append("- keine globale Konflikt-Innenwahrnehmung")
    for row in global_rows:
        lines.extend(
            [
                f"- {row['inner_awareness_state']}",
                f"  DIO-Syntax: `{row['dio_syntax_sentence']}`",
                f"  Satz: {row['inner_sentence']}",
            ]
        )
    lines.extend(["", "## Families"])
    if not family_rows:
        lines.append("- keine Familien-Innenwahrnehmung")
    for row in family_rows:
        lines.extend(
            [
                f"- {row['symbol_family']}:{row['burden_action']} ({row['source']})",
                f"  DIO-Syntax: `{row['dio_syntax_sentence']}`",
                f"  Satz: {row['inner_sentence']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Innenzustands-Landkarte",
            "- keine Handlung",
            "- kein Gate",
            "- keine Motorik",
            "- kein Trainingsmemory",
            "- Mini-DIO liest diesen Bericht nicht aktiv",
        ]
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    txt_path.write_text(
        "\n".join(str(row["dio_syntax_sentence"]) for row in global_rows + family_rows) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stability", required=True, type=Path)
    parser.add_argument("--reflection", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    family_rows, global_rows = build_rows(args.stability, args.reflection)
    write_outputs(args.output_dir, family_rows, global_rows)
    print(f"conflict_stability_inner_awareness family={len(family_rows)} global={len(global_rows)}")
    for row in global_rows:
        print(row["dio_syntax_sentence"])


if __name__ == "__main__":
    main()
