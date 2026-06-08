"""Build passive development diagnosis from Mini-DIO maturation timelines.

This report condenses family timelines into readable development states:
carried, quiet, burdened, or shifting from observation to carried. It is
diagnostic only and must not influence action.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _safe_float(value: object) -> float:
    try:
        return float(value or 0.0)
    except Exception:
        return 0.0


def _safe_int(value: object) -> int:
    try:
        return int(float(value or 0))
    except Exception:
        return 0


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _split_path(path: str) -> list[str]:
    return [item.strip() for item in str(path or "").split("->") if item.strip()]


def _diagnosis(row: dict) -> str:
    maturation = str(row.get("maturation_state", "") or "")
    moments = _split_path(str(row.get("moment_path", "") or ""))
    reward = _safe_float(row.get("reward_sum", 0.0))
    first = str(row.get("first_moment_state", "") or "")
    last = str(row.get("last_moment_state", "") or "")

    if first in ("moment_quiet_held", "moment_quiet_observed") and last == "moment_carried" and reward > 0.0:
        return "development_observation_to_carried"
    if maturation == "maturation_stable_carried" and moments and all(item == "moment_carried" for item in moments):
        return "development_stable_carried"
    if maturation == "maturation_stable_conflicted_burden" and moments and all(
        item == "moment_conflicted_burden" for item in moments
    ):
        return "development_repeated_burden"
    if maturation == "maturation_quiet_observation" and moments and all(
        item in ("moment_quiet_held", "moment_quiet_observed") for item in moments
    ):
        return "development_quiet_observation"
    if "mixed" in maturation or len(set(moments)) > 1:
        return "development_mixed_shift"
    if reward > 0.0:
        return "development_positive_open"
    if reward < 0.0:
        return "development_negative_open"
    return "development_open"


def _sentence(row: dict, diagnosis: str) -> str:
    family = str(row.get("symbol_family", "") or "-")
    path = str(row.get("moment_path", "") or "-")
    reward = _safe_float(row.get("reward_sum", 0.0))
    action_path = str(row.get("action_path", "") or "-")
    if diagnosis == "development_observation_to_carried":
        return (
            f"{family}: Entwicklung von Beobachtung/Halten zu getragenem Kontakt; "
            f"Pfad={path}; Aktionen={action_path}; reward_sum={reward:.6f}."
        )
    if diagnosis == "development_stable_carried":
        return f"{family}: stabil getragen; Pfad={path}; Aktionen={action_path}; reward_sum={reward:.6f}."
    if diagnosis == "development_repeated_burden":
        return f"{family}: wiederholt belastend/widerspruechlich; Pfad={path}; Aktionen={action_path}; reward_sum={reward:.6f}."
    if diagnosis == "development_quiet_observation":
        return f"{family}: ruhig beobachtet/gehalten; Pfad={path}; Aktionen={action_path}."
    if diagnosis == "development_mixed_shift":
        return f"{family}: gemischter Entwicklungswechsel; Pfad={path}; Aktionen={action_path}; reward_sum={reward:.6f}."
    if diagnosis == "development_positive_open":
        return f"{family}: positive offene Entwicklung; Pfad={path}; reward_sum={reward:.6f}."
    if diagnosis == "development_negative_open":
        return f"{family}: negative offene Entwicklung; Pfad={path}; reward_sum={reward:.6f}."
    return f"{family}: offene Entwicklung; Pfad={path}; reward_sum={reward:.6f}."


def build_rows(timeline_summary_csv: Path) -> tuple[list[dict], list[dict]]:
    detail: list[dict] = []
    for row in _read_csv(timeline_summary_csv):
        diagnosis = _diagnosis(row)
        moments = _split_path(str(row.get("moment_path", "") or ""))
        item = {
            "symbol_family": str(row.get("symbol_family", "") or "-"),
            "development_state": diagnosis,
            "maturation_state": str(row.get("maturation_state", "") or ""),
            "count": _safe_int(row.get("count", 0)),
            "runs": str(row.get("runs", "") or ""),
            "first_moment_state": str(row.get("first_moment_state", "") or ""),
            "last_moment_state": str(row.get("last_moment_state", "") or ""),
            "moment_path": str(row.get("moment_path", "") or ""),
            "binding_path": str(row.get("binding_path", "") or ""),
            "action_path": str(row.get("action_path", "") or ""),
            "distinct_moment_count": len(set(moments)),
            "reward_sum": round(_safe_float(row.get("reward_sum", 0.0)), 6),
            "event_reward_sum": round(_safe_float(row.get("event_reward_sum", 0.0)), 6),
            "development_sentence": "",
            "passive_only": 1,
        }
        item["development_sentence"] = _sentence(row, diagnosis)
        detail.append(item)

    groups: dict[str, dict] = {}
    for row in detail:
        state = str(row.get("development_state", "") or "")
        group = groups.setdefault(
            state,
            {
                "development_state": state,
                "family_count": 0,
                "row_count": 0,
                "reward_sum": 0.0,
                "event_reward_sum": 0.0,
                "families": set(),
                "maturation_states": set(),
            },
        )
        group["family_count"] += 1
        group["row_count"] += _safe_int(row.get("count", 0))
        group["reward_sum"] += _safe_float(row.get("reward_sum", 0.0))
        group["event_reward_sum"] += _safe_float(row.get("event_reward_sum", 0.0))
        group["families"].add(str(row.get("symbol_family", "") or ""))
        group["maturation_states"].add(str(row.get("maturation_state", "") or ""))

    summary: list[dict] = []
    for group in groups.values():
        summary.append(
            {
                "development_state": group["development_state"],
                "family_count": int(group["family_count"]),
                "row_count": int(group["row_count"]),
                "reward_sum": round(float(group["reward_sum"]), 6),
                "event_reward_sum": round(float(group["event_reward_sum"]), 6),
                "families": ",".join(sorted(name for name in group["families"] if name)),
                "maturation_states": ",".join(sorted(name for name in group["maturation_states"] if name)),
            }
        )

    order = {
        "development_stable_carried": 0,
        "development_observation_to_carried": 1,
        "development_positive_open": 2,
        "development_mixed_shift": 3,
        "development_quiet_observation": 4,
        "development_repeated_burden": 5,
        "development_negative_open": 6,
        "development_open": 7,
    }
    detail.sort(key=lambda item: (order.get(str(item.get("development_state", "")), 99), str(item.get("symbol_family", ""))))
    summary.sort(key=lambda item: order.get(str(item.get("development_state", "")), 99))
    return detail, summary


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path, timeline_summary_csv: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_passive_development_diagnosis.csv"
    summary_path = output_dir / "dio_mini_passive_development_diagnosis_summary.csv"
    json_path = output_dir / "dio_mini_passive_development_diagnosis.json"
    md_path = output_dir / "dio_mini_passive_development_diagnosis.md"

    detail_fields = list(detail[0].keys()) if detail else [
        "symbol_family",
        "development_state",
        "maturation_state",
        "count",
        "moment_path",
        "reward_sum",
        "development_sentence",
        "passive_only",
    ]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)

    summary_fields = list(summary[0].keys()) if summary else [
        "development_state",
        "family_count",
        "row_count",
        "reward_sum",
        "event_reward_sum",
        "families",
        "maturation_states",
    ]
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)

    json_path.write_text(
        json.dumps(
            {
                "timeline_summary_csv": str(timeline_summary_csv),
                "detail": detail,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# DIO Mini Passive Development Diagnosis",
        "",
        "## Grenze",
        "- liest nur die passive Reife-Timeline",
        "- schreibt kein Memory",
        "- beeinflusst keine Handlung",
        "- kein Gate",
        "",
        "## Zusammenfassung",
    ]
    if not summary:
        lines.append("- keine Entwicklungsdaten")
    else:
        for row in summary:
            lines.append(
                f"- {row.get('development_state', '-')}: families={row.get('family_count', 0)} "
                f"rows={row.get('row_count', 0)} reward_sum={row.get('reward_sum', 0.0)} "
                f"families_list={row.get('families', '-') or '-'}"
            )
    lines.extend(["", "## Familien"])
    for row in detail:
        lines.append(f"- {row.get('development_sentence', '-')}")
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive Mini-DIO development diagnosis")
    parser.add_argument("--timeline-summary-csv", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    timeline_summary_csv = Path(args.timeline_summary_csv)
    detail, summary = build_rows(timeline_summary_csv)
    write_outputs(detail, summary, Path(args.output_dir), timeline_summary_csv)
    print(f"development_rows={len(detail)} summary_rows={len(summary)}")
    for row in summary:
        print(
            f"{row['development_state']} families={row['family_count']} "
            f"rows={row['row_count']} reward={row['reward_sum']}"
        )


if __name__ == "__main__":
    main()
