"""Build a passive reflection map from consolidated variant stability.

This report turns passive stability evidence into readable inner reflection.
It remains diagnostic only:

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


def _split_csv(value: object) -> list[str]:
    return [part.strip() for part in str(value or "").split(",") if part.strip()]


def _build_reflection_rows(stability: dict) -> tuple[list[dict], list[dict]]:
    carried = list(stability.get("carried_action_summary", []) or [])
    states = list(stability.get("state_summary", []) or [])
    compares = list(stability.get("compare_summary", []) or [])

    rows: list[dict] = []
    carried_actions = sorted(str(item.get("action", "") or "") for item in carried if str(item.get("action", "") or ""))
    carried_variants = sorted({variant for item in carried for variant in _split_csv(item.get("variants"))})
    all_variants = sorted({variant for item in states for variant in _split_csv(item.get("variants"))})
    stable_compare_count = sum(
        _safe_int(item.get("count"))
        for item in compares
        if str(item.get("compare_state", "") or "") == "same_variant_state"
    )
    compare_count = sum(_safe_int(item.get("count")) for item in compares)
    burden_count = sum(
        _safe_int(item.get("count"))
        for item in states
        if str(item.get("variant_reife_state", "") or "") == "variant_self_burden_action_trace"
    )
    burden_reward = sum(
        _safe_float(item.get("event_reward_sum"))
        for item in states
        if str(item.get("variant_reife_state", "") or "") == "variant_self_burden_action_trace"
    )
    burden_episodes = sum(
        _safe_int(item.get("episode_count"))
        for item in states
        if str(item.get("variant_reife_state", "") or "") == "variant_self_burden_action_trace"
    )
    observation_count = sum(
        _safe_int(item.get("count"))
        for item in states
        if str(item.get("variant_reife_state", "") or "") == "variant_related_observation_trace"
    )
    carried_count = sum(
        _safe_int(item.get("count"))
        for item in states
        if str(item.get("variant_reife_state", "") or "") == "variant_self_carried_action_trace"
    )

    for item in carried:
        action = str(item.get("action", "") or "")
        families = str(item.get("family_actions", "") or "")
        variants = str(item.get("variants", "") or "")
        reward = _safe_float(item.get("event_reward_sum"))
        episodes = _safe_int(item.get("episode_count"))
        rows.append(
            {
                "reflection_key": f"direction_{action.lower()}_locally_carried",
                "reflection_state": "direction_can_be_locally_carried",
                "action": action,
                "variants": variants,
                "family_actions": families,
                "event_reward_sum": round(reward, 9),
                "episode_count": episodes,
                "dio_syntax_sentence": (
                    f"variant_reflection|{action}|locally_carried|"
                    f"variants={variants}|episodes={episodes}|reward={reward:.6f}"
                ),
                "reflection_sentence": (
                    f"{action} kann in einer passenden Variante lokal getragen sein. "
                    "Das ist Variantenreife, keine allgemeine Regel."
                ),
                "passive_only": 1,
                "writes_training_memory": 0,
                "read_by_mini_dio": 0,
                "influences_action": 0,
                "is_gate": 0,
                "is_motoric": 0,
            }
        )

    rows.append(
        {
            "reflection_key": "kinship_remains_observation",
            "reflection_state": "transfer_is_not_action",
            "action": "-",
            "variants": ",".join(carried_variants),
            "family_actions": "-",
            "event_reward_sum": 0.0,
            "episode_count": observation_count,
            "dio_syntax_sentence": (
                f"variant_reflection|transfer|observation_only|related_traces={observation_count}"
            ),
            "reflection_sentence": (
                "Verwandtschaft zu einer alten Reifespur bleibt Wahrnehmung. "
                "Sie wird nicht automatisch Handlung."
            ),
            "passive_only": 1,
            "writes_training_memory": 0,
            "read_by_mini_dio": 0,
            "influences_action": 0,
            "is_gate": 0,
            "is_motoric": 0,
        }
    )

    stability_state = "stable_variant_map_with_burden_trace" if burden_count else "stable_variant_map_without_burden"
    stability_sentence = (
        "Die geprueften Varianten blieben in den Folgelaeufen gleich eingeordnet. "
        "Eine Belastungsspur ist sichtbar und bleibt Warnspur, nicht Sperre."
        if burden_count
        else "Die geprueften Varianten blieben in den Folgelaeufen gleich eingeordnet. "
        "Belastete stabile Handlungen wurden nicht sichtbar."
    )
    rows.append(
        {
            "reflection_key": "stable_variant_map",
            "reflection_state": stability_state,
            "action": ",".join(carried_actions) or "-",
            "variants": ",".join(all_variants),
            "family_actions": "-",
            "event_reward_sum": sum(_safe_float(item.get("event_reward_sum")) for item in carried),
            "episode_count": stable_compare_count,
            "dio_syntax_sentence": (
                f"variant_reflection|stability|same_state={stable_compare_count}|burden={burden_count}"
            ),
            "reflection_sentence": stability_sentence,
            "passive_only": 1,
            "writes_training_memory": 0,
            "read_by_mini_dio": 0,
            "influences_action": 0,
            "is_gate": 0,
            "is_motoric": 0,
        }
    )
    if burden_count:
        rows.append(
            {
                "reflection_key": "burden_remains_warning_trace",
                "reflection_state": "burden_is_warning_not_gate",
                "action": "-",
                "variants": ",".join(all_variants),
                "family_actions": "-",
                "event_reward_sum": round(burden_reward, 9),
                "episode_count": burden_episodes,
                "dio_syntax_sentence": (
                    f"variant_reflection|burden|warning_trace|count={burden_count}|reward={burden_reward:.6f}"
                ),
                "reflection_sentence": (
                    "Belastung wird als passive Warnspur lesbar. "
                    "Sie beschreibt Konsequenz und Reorganisation, keine harte Sperre."
                ),
                "passive_only": 1,
                "writes_training_memory": 0,
                "read_by_mini_dio": 0,
                "influences_action": 0,
                "is_gate": 0,
                "is_motoric": 0,
            }
        )

    summary = [
        {
            "reflection_state": "direction_can_be_locally_carried",
            "count": len(carried),
            "event_reward_sum": round(sum(_safe_float(item.get("event_reward_sum")) for item in carried), 9),
            "episode_count": sum(_safe_int(item.get("episode_count")) for item in carried),
            "actions": ",".join(carried_actions),
            "variants": ",".join(carried_variants),
        },
        {
                "reflection_state": "transfer_is_not_action",
                "count": 1 if observation_count else 0,
                "event_reward_sum": 0.0,
                "episode_count": observation_count,
                "actions": "-",
                "variants": ",".join(all_variants),
            },
        {
            "reflection_state": stability_state,
            "count": 1 if compare_count else 0,
            "event_reward_sum": round(sum(_safe_float(item.get("event_reward_sum")) for item in carried), 9),
            "episode_count": stable_compare_count,
            "actions": ",".join(carried_actions),
            "variants": ",".join(all_variants),
        },
    ]
    if burden_count:
        summary.append(
            {
                "reflection_state": "burden_is_warning_not_gate",
                "count": burden_count,
                "event_reward_sum": round(burden_reward, 9),
                "episode_count": burden_episodes,
                "actions": "-",
                "variants": ",".join(all_variants),
            }
        )
    rows.sort(key=lambda item: (str(item["reflection_state"]), str(item["reflection_key"])))
    summary.sort(key=lambda item: str(item["reflection_state"]))
    return rows, summary


def write_outputs(stability_path: Path, output_dir: Path, detail: list[dict], summary: list[dict]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_variant_reflection.csv"
    summary_csv = output_dir / "dio_mini_passive_variant_reflection_summary.csv"
    json_path = output_dir / "dio_mini_passive_variant_reflection.json"
    md_path = output_dir / "dio_mini_passive_variant_reflection.md"
    txt_path = output_dir / "dio_mini_passive_variant_reflection.txt"

    _write_csv(detail_csv, detail, ["reflection_key", "reflection_state", "action", "event_reward_sum"])
    _write_csv(summary_csv, summary, ["reflection_state", "count", "event_reward_sum", "episode_count"])
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_variant_reflection.v1",
                "source_stability": str(stability_path),
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
        "# Mini-DIO Passive Variant Reflection",
        "",
        f"- source_stability: `{stability_path}`",
        "",
        "## Summary",
    ]
    for row in summary:
        lines.append(
            f"- {row['reflection_state']}: count={row['count']} "
            f"reward={float(row['event_reward_sum']):.6f} "
            f"episodes={row['episode_count']} actions={row['actions']} variants={row['variants']}"
        )
    lines.extend(["", "## Detail"])
    for row in detail:
        lines.extend(
            [
                f"- {row['reflection_key']}: {row['reflection_state']}",
                f"  DIO-Syntax: `{row['dio_syntax_sentence']}`",
                f"  Lesung: {row['reflection_sentence']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Reflexion",
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
    parser.add_argument("--stability", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    stability = json.loads(args.stability.read_text(encoding="utf-8"))
    detail, summary = _build_reflection_rows(stability)
    write_outputs(args.stability, args.output_dir, detail, summary)
    print(f"passive_variant_reflection rows={len(detail)} summary={len(summary)}")
    for row in summary:
        print(
            f"{row['reflection_state']} count={row['count']} "
            f"reward={row['event_reward_sum']} episodes={row['episode_count']}"
        )


if __name__ == "__main__":
    main()
