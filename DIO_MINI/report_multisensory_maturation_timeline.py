"""Build a passive maturation timeline for Mini-DIO families.

This joins the multisensory inner map with the passive maturation map. It shows
when families appear, whether they are quiet, carried, conflicted, or mixed,
and how their observed path unfolds over run/tick time. It is diagnostic only.
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


def _load_maturation(path: Path) -> dict[str, dict]:
    items: dict[str, dict] = {}
    for row in _read_csv(path):
        family = str(row.get("symbol_family", "") or "")
        if family:
            items[family] = dict(row)
    return items


def _moment_state(row: dict) -> str:
    binding = str(row.get("binding_state", "") or "")
    inner = str(row.get("inner_state", "") or "")
    contact = str(row.get("contact_state", "") or "")
    if binding == "multisensory_carried_contact" and contact == "real_contact_carried":
        return "moment_carried"
    if binding == "multisensory_conflicted_burden" and contact == "real_contact_burdened":
        return "moment_conflicted_burden"
    if inner == "inner_consequence_quiet" and contact.startswith("held_"):
        return "moment_quiet_held"
    if inner == "inner_consequence_quiet":
        return "moment_quiet_observed"
    if "conflicted" in inner:
        return "moment_conflicted_open"
    return "moment_open"


def _sentence(row: dict, maturation: dict, moment: str) -> str:
    family = str(row.get("symbol_family", "") or "-")
    run = str(row.get("run", "") or "-")
    tick = str(row.get("tick", "") or "-")
    maturation_state = str(maturation.get("maturation_state", "maturation_unknown") or "maturation_unknown")
    binding = str(row.get("binding_state", "") or "-")
    action = str(row.get("action", "WAIT") or "WAIT")
    reward = _safe_float(row.get("reward", 0.0))
    return (
        f"{family}: run={run} tick={tick}; {moment}; Reife={maturation_state}; "
        f"Bindung={binding}; Aktion={action}; reward={reward:.6f}."
    )


def build_rows(map_csv: Path, maturation_csv: Path) -> tuple[list[dict], list[dict]]:
    maturation_by_family = _load_maturation(maturation_csv)
    detail: list[dict] = []
    for row in _read_csv(map_csv):
        family = str(row.get("symbol_family", "") or "")
        maturation = maturation_by_family.get(family, {})
        moment = _moment_state(row)
        item = {
            "run": str(row.get("run", "") or ""),
            "tick": str(row.get("tick", "") or ""),
            "timestamp_ms": str(row.get("timestamp_ms", "") or ""),
            "symbol_family": family,
            "maturation_state": str(maturation.get("maturation_state", "maturation_unknown") or "maturation_unknown"),
            "moment_state": moment,
            "binding_state": str(row.get("binding_state", "") or ""),
            "inner_state": str(row.get("inner_state", "") or ""),
            "contact_state": str(row.get("contact_state", "") or ""),
            "action": str(row.get("action", "WAIT") or "WAIT").upper(),
            "outcome_event": str(row.get("outcome_event", "NO_TRADE") or "NO_TRADE").upper(),
            "sight_state": str(row.get("sight_state", "") or ""),
            "hearing_state": str(row.get("hearing_state", "") or ""),
            "feeling_state": str(row.get("feeling_state", "") or ""),
            "reward": round(_safe_float(row.get("reward", 0.0)), 6),
            "event_reward": round(_safe_float(row.get("event_reward", 0.0)), 6),
            "maturation_reward_sum": round(_safe_float(maturation.get("reward_sum", 0.0)), 6),
            "timeline_sentence": _sentence(row, maturation, moment),
            "passive_only": 1,
        }
        detail.append(item)

    detail.sort(key=lambda item: (str(item.get("run", "")), _safe_int(item.get("tick", 0)), str(item.get("symbol_family", ""))))

    grouped: dict[str, list[dict]] = {}
    for row in detail:
        grouped.setdefault(str(row.get("symbol_family", "") or ""), []).append(row)

    summary: list[dict] = []
    for family, rows in grouped.items():
        moment_path = " -> ".join(str(row.get("moment_state", "") or "-") for row in rows)
        binding_path = " -> ".join(str(row.get("binding_state", "") or "-") for row in rows)
        action_path = " -> ".join(str(row.get("action", "") or "-") for row in rows)
        reward_sum = sum(_safe_float(row.get("reward", 0.0)) for row in rows)
        event_reward_sum = sum(_safe_float(row.get("event_reward", 0.0)) for row in rows)
        maturation_state = str(rows[-1].get("maturation_state", "maturation_unknown") or "maturation_unknown")
        first_moment = str(rows[0].get("moment_state", "") or "-")
        last_moment = str(rows[-1].get("moment_state", "") or "-")
        summary.append(
            {
                "symbol_family": family,
                "maturation_state": maturation_state,
                "count": len(rows),
                "runs": ",".join(sorted({str(row.get("run", "") or "") for row in rows if str(row.get("run", "") or "")})),
                "first_moment_state": first_moment,
                "last_moment_state": last_moment,
                "moment_path": moment_path,
                "binding_path": binding_path,
                "action_path": action_path,
                "reward_sum": round(float(reward_sum), 6),
                "event_reward_sum": round(float(event_reward_sum), 6),
                "maturation_reward_sum": round(_safe_float(rows[-1].get("maturation_reward_sum", 0.0)), 6),
                "timeline_sentence": (
                    f"{family}: Reife={maturation_state}; Verlauf={moment_path}; "
                    f"reward_sum={reward_sum:.6f}."
                ),
                "passive_only": 1,
            }
        )

    order = {
        "maturation_stable_carried": 0,
        "maturation_mixed_recurrence": 1,
        "maturation_quiet_observation": 2,
        "maturation_stable_conflicted_burden": 3,
        "maturation_unknown": 4,
    }
    summary.sort(key=lambda item: (order.get(str(item.get("maturation_state", "")), 99), str(item.get("symbol_family", ""))))
    return detail, summary


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path, map_csv: Path, maturation_csv: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_multisensory_maturation_timeline.csv"
    summary_path = output_dir / "dio_mini_multisensory_maturation_timeline_summary.csv"
    json_path = output_dir / "dio_mini_multisensory_maturation_timeline.json"
    md_path = output_dir / "dio_mini_multisensory_maturation_timeline.md"

    detail_fields = list(detail[0].keys()) if detail else [
        "run",
        "tick",
        "symbol_family",
        "maturation_state",
        "moment_state",
        "binding_state",
        "action",
        "reward",
        "timeline_sentence",
        "passive_only",
    ]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)

    summary_fields = list(summary[0].keys()) if summary else [
        "symbol_family",
        "maturation_state",
        "count",
        "runs",
        "first_moment_state",
        "last_moment_state",
        "moment_path",
        "reward_sum",
        "timeline_sentence",
        "passive_only",
    ]
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)

    json_path.write_text(
        json.dumps(
            {
                "map_csv": str(map_csv),
                "maturation_csv": str(maturation_csv),
                "detail": detail,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# DIO Mini Multisensory Maturation Timeline",
        "",
        "## Grenze",
        "- liest nur passive multisensorische Innenkarte und passive Reifungskarte",
        "- schreibt kein Memory",
        "- beeinflusst keine Handlung",
        "- kein Gate",
        "",
        "## Zusammenfassung",
    ]
    if not summary:
        lines.append("- keine Timeline-Daten")
    else:
        for row in summary:
            lines.append(
                f"- {row.get('symbol_family', '-')}: {row.get('maturation_state', '-')} "
                f"count={row.get('count', 0)} reward_sum={row.get('reward_sum', 0.0)} "
                f"path={row.get('moment_path', '-')}"
            )
    lines.extend(["", "## Erste Tick-Lesung"])
    for row in detail[:100]:
        lines.append(f"- {row.get('timeline_sentence', '-')}")
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive Mini-DIO maturation timeline")
    parser.add_argument("--map-csv", required=True)
    parser.add_argument("--maturation-csv", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    map_csv = Path(args.map_csv)
    maturation_csv = Path(args.maturation_csv)
    detail, summary = build_rows(map_csv, maturation_csv)
    write_outputs(detail, summary, Path(args.output_dir), map_csv, maturation_csv)
    print(f"maturation_timeline_rows={len(detail)} summary_rows={len(summary)}")
    for row in summary[:20]:
        print(
            f"{row['symbol_family']} {row['maturation_state']} "
            f"count={row['count']} reward={row['reward_sum']}"
        )


if __name__ == "__main__":
    main()
