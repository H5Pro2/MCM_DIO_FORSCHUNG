"""Build a passive conflict reflection from a variant-map comparison.

The report detects cases where a burdened action remains visible while the
same symbol family also appears as WAIT/observation in the follow-up map.

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


def _family_name(family_action: str) -> str:
    return str(family_action or "").split(":", 1)[0]


def _action_name(family_action: str) -> str:
    parts = str(family_action or "").split(":", 1)
    return parts[1] if len(parts) == 2 else ""


def build_rows(compare_csv: Path, after_map_csv: Path) -> tuple[list[dict], list[dict]]:
    compare_rows = _read_csv(compare_csv)
    after_rows = _read_csv(after_map_csv)
    after_by_family: dict[str, list[dict]] = {}
    for row in after_rows:
        after_by_family.setdefault(str(row.get("symbol_family", "") or _family_name(row.get("family_action", ""))), []).append(row)

    detail: list[dict] = []
    for compare in compare_rows:
        family_action = str(compare.get("family_action", "") or "")
        family = _family_name(family_action)
        action = _action_name(family_action)
        before_state = str(compare.get("before_variant_reife_state", "") or "")
        after_state = str(compare.get("after_variant_reife_state", "") or "")
        if after_state != "variant_self_burden_action_trace" and before_state != "variant_self_burden_action_trace":
            continue
        wait_rows = [
            row
            for row in after_by_family.get(family, [])
            if str(row.get("action", "") or "") == "WAIT"
        ]
        wait_related = [
            row
            for row in wait_rows
            if str(row.get("variant_reife_state", "") or "") == "variant_related_observation_trace"
        ]
        before_reward = _safe_float(compare.get("before_reward"))
        after_reward = _safe_float(compare.get("after_reward"))
        before_episodes = _safe_int(compare.get("before_episode_count"))
        after_episodes = _safe_int(compare.get("after_episode_count"))
        burden_reduced = after_reward > before_reward or after_episodes < before_episodes
        wait_observation_emerged = bool(wait_related or wait_rows)
        if burden_reduced and wait_observation_emerged:
            reflection_state = "burden_reorganized_into_observation"
        elif burden_reduced:
            reflection_state = "burden_reduced_without_wait_trace"
        elif wait_observation_emerged:
            reflection_state = "burden_with_parallel_wait_trace"
        else:
            reflection_state = "burden_remains_action_trace"
        wait_family_actions = ",".join(str(row.get("family_action", "") or "") for row in wait_rows)
        wait_states = ",".join(str(row.get("variant_reife_state", "") or "") for row in wait_rows)
        row = {
            "symbol_family": family,
            "burden_family_action": family_action,
            "burden_action": action,
            "reflection_state": reflection_state,
            "before_reward": round(before_reward, 9),
            "after_reward": round(after_reward, 9),
            "reward_delta": round(after_reward - before_reward, 9),
            "before_episode_count": before_episodes,
            "after_episode_count": after_episodes,
            "episode_delta": after_episodes - before_episodes,
            "wait_trace_count": len(wait_rows),
            "wait_related_observation_count": len(wait_related),
            "wait_family_actions": wait_family_actions,
            "wait_states": wait_states,
            "dio_syntax_sentence": (
                f"conflict_reflection|{family}|{action}|{reflection_state}|"
                f"reward_delta={after_reward - before_reward:.6f}|wait_traces={len(wait_rows)}"
            ),
            "reflection_sentence": _sentence(
                family,
                action,
                reflection_state,
                before_reward,
                after_reward,
                before_episodes,
                after_episodes,
            ),
            "passive_only": 1,
            "writes_training_memory": 0,
            "read_by_mini_dio": 0,
            "influences_action": 0,
            "is_gate": 0,
            "is_motoric": 0,
        }
        detail.append(row)

    summary: dict[str, dict] = {}
    for row in detail:
        state = str(row["reflection_state"])
        bucket = summary.setdefault(
            state,
            {
                "reflection_state": state,
                "count": 0,
                "reward_delta": 0.0,
                "episode_delta": 0,
                "families": [],
            },
        )
        bucket["count"] += 1
        bucket["reward_delta"] += _safe_float(row.get("reward_delta"))
        bucket["episode_delta"] += _safe_int(row.get("episode_delta"))
        bucket["families"].append(str(row.get("symbol_family", "") or ""))

    summary_rows = [
        {
            "reflection_state": row["reflection_state"],
            "count": row["count"],
            "reward_delta": round(float(row["reward_delta"]), 9),
            "episode_delta": row["episode_delta"],
            "families": ",".join(sorted(set(row["families"]))),
        }
        for row in summary.values()
    ]
    detail.sort(key=lambda item: (str(item["reflection_state"]), str(item["symbol_family"])))
    summary_rows.sort(key=lambda item: (str(item["reflection_state"]), str(item["families"])))
    return detail, summary_rows


def _sentence(
    family: str,
    action: str,
    reflection_state: str,
    before_reward: float,
    after_reward: float,
    before_episodes: int,
    after_episodes: int,
) -> str:
    if reflection_state == "burden_reorganized_into_observation":
        return (
            f"{family}:{action} war belastet und wird im Folgelauf schwaecher "
            f"({before_reward:.6f}->{after_reward:.6f}, Episoden {before_episodes}->{after_episodes}). "
            "Dieselbe Familie taucht zusaetzlich als Beobachtung auf. Das ist Reorganisation, keine Sperre."
        )
    if reflection_state == "burden_reduced_without_wait_trace":
        return (
            f"{family}:{action} bleibt belastet, aber die Belastung nimmt ab "
            f"({before_reward:.6f}->{after_reward:.6f})."
        )
    if reflection_state == "burden_with_parallel_wait_trace":
        return (
            f"{family}:{action} bleibt belastet, waehrend dieselbe Familie auch als WAIT-Kontext auftaucht."
        )
    return f"{family}:{action} bleibt passive Warnspur."


def write_outputs(output_dir: Path, compare_csv: Path, after_map_csv: Path, detail: list[dict], summary: list[dict]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_conflict_reflection.csv"
    summary_csv = output_dir / "dio_mini_passive_conflict_reflection_summary.csv"
    json_path = output_dir / "dio_mini_passive_conflict_reflection.json"
    md_path = output_dir / "dio_mini_passive_conflict_reflection.md"
    txt_path = output_dir / "dio_mini_passive_conflict_reflection.txt"

    _write_csv(detail_csv, detail, ["symbol_family", "burden_family_action", "reflection_state", "reward_delta"])
    _write_csv(summary_csv, summary, ["reflection_state", "count", "reward_delta", "episode_delta"])
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_conflict_reflection.v1",
                "compare_source": str(compare_csv),
                "after_map_source": str(after_map_csv),
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
        "# Mini-DIO Passive Conflict Reflection",
        "",
        f"- compare_source: `{compare_csv}`",
        f"- after_map_source: `{after_map_csv}`",
        "",
        "## Summary",
    ]
    if not summary:
        lines.append("- keine Konflikt-Reorganisation gefunden")
    for row in summary:
        lines.append(
            f"- {row['reflection_state']}: count={row['count']} "
            f"reward_delta={float(row['reward_delta']):.6f} "
            f"episode_delta={row['episode_delta']} families={row['families'] or '-'}"
        )
    lines.extend(["", "## Detail"])
    for row in detail:
        lines.extend(
            [
                f"- {row['burden_family_action']}: {row['reflection_state']}",
                f"  DIO-Syntax: `{row['dio_syntax_sentence']}`",
                f"  Lesung: {row['reflection_sentence']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Konfliktreflexion",
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
    parser.add_argument("--compare", required=True, type=Path)
    parser.add_argument("--after-map", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    detail, summary = build_rows(args.compare, args.after_map)
    write_outputs(args.output_dir, args.compare, args.after_map, detail, summary)
    print(f"passive_conflict_reflection rows={len(detail)} summary={len(summary)}")
    for row in summary:
        print(
            f"{row['reflection_state']} count={row['count']} "
            f"reward_delta={row['reward_delta']} episode_delta={row['episode_delta']}"
        )


if __name__ == "__main__":
    main()
