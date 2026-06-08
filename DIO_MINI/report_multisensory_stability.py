"""Report passive multisensory stability across Mini-DIO runs.

This diagnostic reads a multisensory inner map and checks whether families are
seen with stable or drifting sensory/inner states across repeated runs.
It writes no memory and must not influence action.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


STATE_FIELDS = [
    "sight_state",
    "hearing_state",
    "feeling_state",
    "inner_state",
    "contact_state",
    "binding_state",
    "action",
    "outcome_event",
]


def _safe_float(value: object) -> float:
    try:
        return float(value or 0.0)
    except Exception:
        return 0.0


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _dominant(counter: Counter[str]) -> tuple[str, int, float]:
    total = sum(counter.values())
    if total <= 0:
        return "-", 0, 0.0
    value, count = counter.most_common(1)[0]
    return value, count, count / total


def _stability_label(shares: list[float], distinct_total: int) -> str:
    if not shares:
        return "multisensory_unseen"
    avg_share = sum(shares) / len(shares)
    if distinct_total <= len(shares) and avg_share >= 0.95:
        return "multisensory_stable_repeat"
    if avg_share >= 0.80:
        return "multisensory_mostly_stable"
    if avg_share >= 0.60:
        return "multisensory_mixed_repeat"
    return "multisensory_drifting_repeat"


def _sentence(row: dict) -> str:
    family = str(row.get("symbol_family", "-") or "-")
    label = str(row.get("stability_label", "-") or "-")
    binding = str(row.get("dominant_binding_state", "-") or "-")
    sight = str(row.get("dominant_sight_state", "-") or "-")
    hearing = str(row.get("dominant_hearing_state", "-") or "-")
    feeling = str(row.get("dominant_feeling_state", "-") or "-")
    runs = str(row.get("runs", "-") or "-")
    return (
        f"{family}: {label}; Bindung={binding}; "
        f"Sehen={sight}, Hoeren={hearing}, Fuehlen={feeling}; Runs={runs}."
    )


def build_rows(map_csv: Path) -> tuple[list[dict], list[dict]]:
    groups: dict[str, dict] = {}
    for row in _read_csv(map_csv):
        family = str(row.get("symbol_family", "") or "-")
        group = groups.setdefault(
            family,
            {
                "symbol_family": family,
                "count": 0,
                "reward_sum": 0.0,
                "event_reward_sum": 0.0,
                "runs": set(),
                "ticks": [],
                "states": {field: Counter() for field in STATE_FIELDS},
            },
        )
        group["count"] += 1
        group["reward_sum"] += _safe_float(row.get("reward", 0.0))
        group["event_reward_sum"] += _safe_float(row.get("event_reward", 0.0))
        run = str(row.get("run", "") or "")
        tick = str(row.get("tick", "") or "")
        if run:
            group["runs"].add(run)
        if tick:
            group["ticks"].append(tick)
        for field in STATE_FIELDS:
            value = str(row.get(field, "") or "-")
            group["states"][field][value] += 1

    detail: list[dict] = []
    for group in groups.values():
        shares: list[float] = []
        distinct_total = 0
        item = {
            "symbol_family": group["symbol_family"],
            "count": int(group["count"]),
            "run_count": len(group["runs"]),
            "runs": ",".join(sorted(group["runs"])),
            "ticks": ",".join(group["ticks"]),
            "reward_sum": round(float(group["reward_sum"]), 6),
            "event_reward_sum": round(float(group["event_reward_sum"]), 6),
            "avg_reward": round(float(group["reward_sum"]) / max(1, int(group["count"])), 6),
        }
        for field in STATE_FIELDS:
            dominant, dominant_count, share = _dominant(group["states"][field])
            distinct = len(group["states"][field])
            distinct_total += distinct
            shares.append(share)
            item[f"dominant_{field}"] = dominant
            item[f"{field}_dominant_count"] = dominant_count
            item[f"{field}_dominant_share"] = round(share, 6)
            item[f"{field}_distinct"] = distinct
        item["avg_dominant_share"] = round(sum(shares) / max(1, len(shares)), 6)
        item["state_distinct_total"] = distinct_total
        item["stability_label"] = _stability_label(shares, distinct_total)
        item["stability_sentence"] = _sentence(item)
        item["passive_only"] = 1
        detail.append(item)

    label_groups: dict[str, dict] = {}
    for row in detail:
        label = str(row.get("stability_label", "") or "-")
        group = label_groups.setdefault(
            label,
            {
                "stability_label": label,
                "count": 0,
                "family_count": 0,
                "reward_sum": 0.0,
                "event_reward_sum": 0.0,
                "families": set(),
                "binding_states": set(),
            },
        )
        group["family_count"] += 1
        group["count"] += int(row.get("count", 0) or 0)
        group["reward_sum"] += _safe_float(row.get("reward_sum", 0.0))
        group["event_reward_sum"] += _safe_float(row.get("event_reward_sum", 0.0))
        group["families"].add(str(row.get("symbol_family", "") or ""))
        group["binding_states"].add(str(row.get("dominant_binding_state", "") or ""))

    summary: list[dict] = []
    for group in label_groups.values():
        summary.append(
            {
                "stability_label": group["stability_label"],
                "family_count": int(group["family_count"]),
                "row_count": int(group["count"]),
                "reward_sum": round(float(group["reward_sum"]), 6),
                "event_reward_sum": round(float(group["event_reward_sum"]), 6),
                "families": ",".join(sorted(name for name in group["families"] if name)),
                "binding_states": ",".join(sorted(name for name in group["binding_states"] if name)),
            }
        )

    order = {
        "multisensory_stable_repeat": 0,
        "multisensory_mostly_stable": 1,
        "multisensory_mixed_repeat": 2,
        "multisensory_drifting_repeat": 3,
        "multisensory_unseen": 4,
    }
    detail.sort(
        key=lambda item: (
            order.get(str(item.get("stability_label", "")), 99),
            str(item.get("symbol_family", "")),
        )
    )
    summary.sort(key=lambda item: order.get(str(item.get("stability_label", "")), 99))
    return detail, summary


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path, map_csv: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_multisensory_stability.csv"
    summary_path = output_dir / "dio_mini_multisensory_stability_summary.csv"
    json_path = output_dir / "dio_mini_multisensory_stability.json"
    md_path = output_dir / "dio_mini_multisensory_stability.md"

    detail_fields = list(detail[0].keys()) if detail else [
        "symbol_family",
        "count",
        "run_count",
        "runs",
        "reward_sum",
        "dominant_binding_state",
        "avg_dominant_share",
        "stability_label",
        "stability_sentence",
        "passive_only",
    ]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)

    summary_fields = list(summary[0].keys()) if summary else [
        "stability_label",
        "family_count",
        "row_count",
        "reward_sum",
        "event_reward_sum",
        "families",
        "binding_states",
    ]
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)

    json_path.write_text(
        json.dumps(
            {
                "map_csv": str(map_csv),
                "detail": detail,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# DIO Mini Multisensory Stability",
        "",
        "## Grenze",
        "- liest nur die passive multisensorische Innenkarte",
        "- schreibt kein Memory",
        "- beeinflusst keine Handlung",
        "- kein Gate",
        "",
        "## Zusammenfassung",
    ]
    if not summary:
        lines.append("- keine Stabilitaetsdaten")
    else:
        for row in summary:
            lines.append(
                f"- {row.get('stability_label', '-')}: families={row.get('family_count', 0)} "
                f"rows={row.get('row_count', 0)} reward_sum={row.get('reward_sum', 0.0)} "
                f"binding={row.get('binding_states', '-') or '-'}"
            )
    lines.extend(["", "## Familien"])
    for row in detail:
        lines.append(f"- {row.get('stability_sentence', '-')}")
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive Mini-DIO multisensory stability")
    parser.add_argument("--map-csv", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    map_csv = Path(args.map_csv)
    detail, summary = build_rows(map_csv)
    write_outputs(detail, summary, Path(args.output_dir), map_csv)
    print(f"multisensory_stability_rows={len(detail)} summary_rows={len(summary)}")
    for row in summary:
        print(
            f"{row['stability_label']} families={row['family_count']} "
            f"rows={row['row_count']} reward={row['reward_sum']}"
        )


if __name__ == "__main__":
    main()
