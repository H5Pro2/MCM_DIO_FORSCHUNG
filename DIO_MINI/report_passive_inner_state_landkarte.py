"""Build a passive inner-state map from Mini-DIO reflection and timeline.

The map compares repeated controlled runs per symbol family. It answers:

- does a passive reflection state stay stable?
- does it shift?
- is the repeat structurally identical in the controlled world?

This is diagnostic only. It writes no memory, does not influence action, and is
not a gate.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


def _safe_float(value: object) -> float:
    try:
        return float(value or 0.0)
    except Exception:
        return 0.0


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _dominant(values: list[str]) -> str:
    counts: dict[str, int] = {}
    for value in values:
        key = str(value or "-")
        counts[key] = counts.get(key, 0) + 1
    if not counts:
        return "-"
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0]


def _run_signature(rows: list[dict]) -> str:
    parts = []
    for row in sorted(rows, key=lambda item: (str(item.get("tick", "")), str(item.get("timestamp_ms", "")))):
        parts.append(
            "|".join(
                [
                    str(row.get("tick", "") or ""),
                    str(row.get("moment_state", "") or ""),
                    str(row.get("binding_state", "") or ""),
                    str(row.get("action", "") or ""),
                    str(row.get("outcome_event", "") or ""),
                    str(row.get("sight_state", "") or ""),
                    str(row.get("hearing_state", "") or ""),
                    str(row.get("feeling_state", "") or ""),
                ]
            )
        )
    return " ; ".join(parts)


def _landkarte_state(reflection_state: str, run_count: int, unique_run_signatures: int, reward_sum: float) -> str:
    if run_count <= 1:
        return "inner_map_single_observation"
    stable_repeat = unique_run_signatures == 1
    if reflection_state == "reflection_trust_seed" and reward_sum > 0.0:
        if stable_repeat:
            return "inner_map_trust_stable_identical_repeat"
        return "inner_map_trust_stable_variant_repeat"
    if reflection_state == "reflection_quiet_observation":
        if stable_repeat:
            return "inner_map_quiet_stable_identical_repeat"
        return "inner_map_quiet_variant_repeat"
    if reflection_state == "reflection_caution_seed":
        if stable_repeat:
            return "inner_map_caution_stable_identical_repeat"
        return "inner_map_caution_variant_repeat"
    if stable_repeat:
        return "inner_map_open_identical_repeat"
    return "inner_map_shift_or_variant"


def _sentence(family: str, state: str, reflection_state: str, run_count: int) -> str:
    if state == "inner_map_trust_stable_identical_repeat":
        return (
            f"{family}: Reflexion bleibt getragen und wiederholt sich in der kontrollierten Welt identisch "
            f"ueber {run_count} Laeufe; das ist Stabilitaet, aber noch kein Generalisierungsnachweis."
        )
    if state == "inner_map_trust_stable_variant_repeat":
        return (
            f"{family}: Reflexion bleibt getragen, obwohl die Wiederholung variiert; das waere staerker "
            f"als reines Auswendigwiederholen."
        )
    if state == "inner_map_quiet_stable_identical_repeat":
        return f"{family}: Ruhige Beobachtung bleibt identisch; DIO haelt diesen Kontakt passiv stabil."
    if state == "inner_map_caution_stable_identical_repeat":
        return f"{family}: Vorsicht bleibt identisch; DIO erinnert Belastung passiv stabil."
    if state == "inner_map_shift_or_variant":
        return f"{family}: Innenzustand oder Verlauf variiert; hier muss geprueft werden, ob Reifung kippt."
    return f"{family}: Innenzustand bleibt passiv offen; reflection={reflection_state}."


def build_rows(timeline_csv: Path, reflection_csv: Path) -> tuple[list[dict], list[dict]]:
    reflection_by_family = {
        str(row.get("symbol_family", "") or ""): row
        for row in _read_csv(reflection_csv)
        if str(row.get("symbol_family", "") or "")
    }
    grouped: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for row in _read_csv(timeline_csv):
        family = str(row.get("symbol_family", "") or "")
        run = str(row.get("run", "") or "")
        if family and run:
            grouped[family][run].append(row)

    detail: list[dict] = []
    summary: dict[str, dict] = {}
    for family, by_run in grouped.items():
        reflection = reflection_by_family.get(family, {})
        reflection_state = str(reflection.get("passive_reflection_state", "reflection_missing") or "reflection_missing")
        run_signatures = [_run_signature(rows) for _, rows in sorted(by_run.items())]
        unique_run_signatures = len(set(run_signatures))
        all_rows = [row for rows in by_run.values() for row in rows]
        reward_sum = sum(_safe_float(row.get("reward")) for row in all_rows)
        event_reward_sum = sum(_safe_float(row.get("event_reward")) for row in all_rows)
        run_count = len(by_run)
        state = _landkarte_state(reflection_state, run_count, unique_run_signatures, reward_sum)
        item = {
            "symbol_family": family,
            "inner_landkarte_state": state,
            "passive_reflection_state": reflection_state,
            "run_count": run_count,
            "runs": ",".join(sorted(by_run)),
            "row_count": len(all_rows),
            "unique_run_signatures": unique_run_signatures,
            "identical_repeat": int(unique_run_signatures == 1 and run_count > 1),
            "reward_sum": round(reward_sum, 6),
            "event_reward_sum": round(event_reward_sum, 6),
            "dominant_moment_state": _dominant([str(row.get("moment_state", "") or "") for row in all_rows]),
            "dominant_binding_state": _dominant([str(row.get("binding_state", "") or "") for row in all_rows]),
            "dominant_action": _dominant([str(row.get("action", "") or "") for row in all_rows]),
            "dominant_outcome": _dominant([str(row.get("outcome_event", "") or "") for row in all_rows]),
            "dominant_sight": _dominant([str(row.get("sight_state", "") or "") for row in all_rows]),
            "dominant_hearing": _dominant([str(row.get("hearing_state", "") or "") for row in all_rows]),
            "dominant_feeling": _dominant([str(row.get("feeling_state", "") or "") for row in all_rows]),
            "landkarte_sentence": _sentence(family, state, reflection_state, run_count),
            "passive_only": 1,
        }
        detail.append(item)
        bucket = summary.setdefault(
            state,
            {
                "inner_landkarte_state": state,
                "family_count": 0,
                "row_count": 0,
                "reward_sum": 0.0,
                "identical_repeat_families": 0,
                "families": [],
            },
        )
        bucket["family_count"] += 1
        bucket["row_count"] += len(all_rows)
        bucket["reward_sum"] += reward_sum
        bucket["identical_repeat_families"] += int(item["identical_repeat"])
        bucket["families"].append(family)

    detail.sort(key=lambda item: (str(item["inner_landkarte_state"]), str(item["symbol_family"])))
    summary_rows = []
    for row in summary.values():
        row["reward_sum"] = round(float(row["reward_sum"]), 6)
        row["families"] = ",".join(sorted(row["families"]))
        summary_rows.append(row)
    summary_rows.sort(key=lambda item: (str(item["inner_landkarte_state"]), str(item["families"])))
    return detail, summary_rows


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path, timeline_csv: Path, reflection_csv: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_inner_state_landkarte.csv"
    summary_csv = output_dir / "dio_mini_passive_inner_state_landkarte_summary.csv"
    json_path = output_dir / "dio_mini_passive_inner_state_landkarte.json"
    md_path = output_dir / "dio_mini_passive_inner_state_landkarte.md"

    detail_fields = list(detail[0].keys()) if detail else ["symbol_family", "inner_landkarte_state"]
    with detail_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)

    summary_fields = list(summary[0].keys()) if summary else ["inner_landkarte_state", "family_count"]
    with summary_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)

    json_path.write_text(
        json.dumps(
            {
                "timeline_source": str(timeline_csv),
                "reflection_source": str(reflection_csv),
                "detail": detail,
                "summary": summary,
                "boundary": {
                    "writes_memory": False,
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
        "# DIO Mini Passive Inner State Landkarte",
        "",
        f"- timeline_source: {timeline_csv}",
        f"- reflection_source: {reflection_csv}",
        "",
        "## Zusammenfassung",
    ]
    if not summary:
        lines.append("- keine Innenzustandsdaten")
    for row in summary:
        lines.append(
            f"- {row['inner_landkarte_state']}: families={row['family_count']} "
            f"rows={row['row_count']} reward_sum={row['reward_sum']} "
            f"identical_repeat_families={row['identical_repeat_families']} "
            f"families_list={row['families'] or '-'}"
        )
    lines.extend(["", "## Familien"])
    for row in detail:
        lines.extend(
            [
                f"- {row['symbol_family']}: {row['inner_landkarte_state']}; "
                f"reflection={row['passive_reflection_state']}; runs={row['runs']}; "
                f"unique_run_signatures={row['unique_run_signatures']}; reward={float(row['reward_sum']):.6f}",
                f"  {row['landkarte_sentence']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Innenzustands-Landkarte",
            "- kein Memory-Schreiben",
            "- keine Motorik",
            "- kein Gate",
            "- keine harte Regel",
            "- identische Wiederholung ist Stabilitaet im kontrollierten Datensatz, kein Beweis fuer Generalisierung",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive Mini-DIO inner-state map")
    parser.add_argument("--timeline-csv", required=True)
    parser.add_argument("--reflection-csv", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    detail, summary = build_rows(Path(args.timeline_csv), Path(args.reflection_csv))
    write_outputs(detail, summary, Path(args.output_dir), Path(args.timeline_csv), Path(args.reflection_csv))
    print(f"passive_inner_state_landkarte_rows={len(detail)} summary={len(summary)}")
    for row in summary:
        print(
            f"{row['inner_landkarte_state']} families={row['family_count']} "
            f"identical={row['identical_repeat_families']} reward={row['reward_sum']}"
        )


if __name__ == "__main__":
    main()
