"""Report passive inner-state stability from a DIO_MINI inner timeline.

The report answers whether rewards emerge from stable inner state or from
transitions. It is read-only diagnosis.
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


def _read_timeline(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _stability_kind(row: dict) -> str:
    transition = str(row.get("inner_transition", "") or "")
    previous = str(row.get("previous_inner_state", "") or "")
    current = str(row.get("inner_state", "") or "")
    if transition == "timeline_start":
        return "start_state"
    if transition == "same_inner_state" or (previous and previous == current):
        return "stable_state"
    return "transition_state"


def _contact_quality(row: dict) -> str:
    contact = str(row.get("contact_state", "") or "")
    action = str(row.get("action", "WAIT") or "WAIT").upper()
    reward = _safe_float(row.get("reward"))
    best = _safe_float(row.get("best_reward_training"))
    if action in ("LONG", "SHORT") and reward > 0.0:
        return "positive_real_contact"
    if action in ("LONG", "SHORT") and reward < 0.0:
        return "negative_real_contact"
    if action == "WAIT" and best > 0.0:
        return "observed_potential"
    if contact:
        return contact
    return "quiet"


def build_rows(timeline_csv: Path) -> tuple[list[dict], list[dict], list[dict]]:
    timeline = _read_timeline(timeline_csv)
    detail: list[dict] = []
    groups: dict[tuple[str, str, str], dict] = {}
    transition_groups: dict[str, dict] = {}
    for row in timeline:
        stability = _stability_kind(row)
        quality = _contact_quality(row)
        inner_state = str(row.get("inner_state", "") or "inner_unknown")
        reward = _safe_float(row.get("reward"))
        best = _safe_float(row.get("best_reward_training"))
        item = {
            "run": str(row.get("run", "") or ""),
            "tick": str(row.get("tick", "") or ""),
            "symbol_family": str(row.get("symbol_family", "") or ""),
            "inner_state": inner_state,
            "previous_inner_state": str(row.get("previous_inner_state", "") or ""),
            "inner_transition": str(row.get("inner_transition", "") or ""),
            "stability_kind": stability,
            "contact_quality": quality,
            "contact_state": str(row.get("contact_state", "") or ""),
            "action": str(row.get("action", "WAIT") or "WAIT").upper(),
            "reward": round(reward, 6),
            "best_reward_training": round(best, 6),
            "passive_only": 1,
        }
        detail.append(item)

        key = (stability, inner_state, quality)
        group = groups.setdefault(
            key,
            {
                "stability_kind": stability,
                "inner_state": inner_state,
                "contact_quality": quality,
                "count": 0,
                "reward_sum": 0.0,
                "best_reward_sum": 0.0,
                "families": set(),
                "actions": set(),
            },
        )
        group["count"] += 1
        group["reward_sum"] += reward
        group["best_reward_sum"] += best
        group["families"].add(str(item["symbol_family"]))
        group["actions"].add(str(item["action"]))

        transition = str(item["inner_transition"])
        transition_group = transition_groups.setdefault(
            transition,
            {
                "inner_transition": transition,
                "stability_kind": stability,
                "count": 0,
                "reward_sum": 0.0,
                "best_reward_sum": 0.0,
                "positive_contacts": 0,
                "observed_potentials": 0,
                "families": set(),
                "actions": set(),
            },
        )
        transition_group["count"] += 1
        transition_group["reward_sum"] += reward
        transition_group["best_reward_sum"] += best
        if quality == "positive_real_contact":
            transition_group["positive_contacts"] += 1
        if quality == "observed_potential":
            transition_group["observed_potentials"] += 1
        transition_group["families"].add(str(item["symbol_family"]))
        transition_group["actions"].add(str(item["action"]))

    overview: list[dict] = []
    for group in groups.values():
        count = int(group["count"])
        overview.append(
            {
                "stability_kind": group["stability_kind"],
                "inner_state": group["inner_state"],
                "contact_quality": group["contact_quality"],
                "count": count,
                "reward_sum": round(float(group["reward_sum"]), 6),
                "best_reward_sum": round(float(group["best_reward_sum"]), 6),
                "avg_reward": round(float(group["reward_sum"]) / max(1, count), 6),
                "families": ",".join(sorted(name for name in group["families"] if name)),
                "actions": ",".join(sorted(name for name in group["actions"] if name)),
            }
        )
    overview.sort(
        key=lambda item: (
            str(item.get("stability_kind", "")) != "stable_state",
            -_safe_float(item.get("reward_sum")),
            str(item.get("inner_state", "")),
        )
    )

    transition_summary: list[dict] = []
    for group in transition_groups.values():
        count = int(group["count"])
        transition_summary.append(
            {
                "inner_transition": group["inner_transition"],
                "stability_kind": group["stability_kind"],
                "count": count,
                "reward_sum": round(float(group["reward_sum"]), 6),
                "best_reward_sum": round(float(group["best_reward_sum"]), 6),
                "avg_reward": round(float(group["reward_sum"]) / max(1, count), 6),
                "positive_contacts": int(group["positive_contacts"]),
                "observed_potentials": int(group["observed_potentials"]),
                "families": ",".join(sorted(name for name in group["families"] if name)),
                "actions": ",".join(sorted(name for name in group["actions"] if name)),
            }
        )
    transition_summary.sort(key=lambda item: (-_safe_float(item.get("reward_sum")), str(item.get("inner_transition", ""))))
    return detail, overview, transition_summary


def write_outputs(detail: list[dict], overview: list[dict], transition_summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_passive_inner_stability_detail.csv"
    overview_path = output_dir / "dio_mini_passive_inner_stability_overview.csv"
    transition_path = output_dir / "dio_mini_passive_inner_stability_transitions.csv"
    json_path = output_dir / "dio_mini_passive_inner_stability.json"
    md_path = output_dir / "dio_mini_passive_inner_stability.md"
    detail_fields = list(detail[0].keys()) if detail else [
        "run",
        "tick",
        "symbol_family",
        "inner_state",
        "stability_kind",
        "contact_quality",
        "reward",
    ]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)
    overview_fields = [
        "stability_kind",
        "inner_state",
        "contact_quality",
        "count",
        "reward_sum",
        "best_reward_sum",
        "avg_reward",
        "families",
        "actions",
    ]
    with overview_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=overview_fields)
        writer.writeheader()
        writer.writerows(overview)
    transition_fields = [
        "inner_transition",
        "stability_kind",
        "count",
        "reward_sum",
        "best_reward_sum",
        "avg_reward",
        "positive_contacts",
        "observed_potentials",
        "families",
        "actions",
    ]
    with transition_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=transition_fields)
        writer.writeheader()
        writer.writerows(transition_summary)
    json_path.write_text(
        json.dumps({"detail": detail, "overview": overview, "transitions": transition_summary}, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    lines = ["# DIO Mini Passive Inner Stability", ""]
    if not overview:
        lines.append("Keine Innenlage-Stabilitaet gefunden.")
    lines.append("## Stabilitaet")
    lines.append("")
    for row in overview:
        lines.extend(
            [
                f"### {row['stability_kind']} / {row['inner_state']} / {row['contact_quality']}",
                f"- count: {row['count']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- best_reward_sum: {float(row['best_reward_sum']):.6f}",
                f"- avg_reward: {float(row['avg_reward']):.6f}",
                f"- actions: {row['actions'] or '-'}",
                f"- families: {row['families'] or '-'}",
                "",
            ]
        )
    lines.append("## Uebergaenge")
    lines.append("")
    for row in transition_summary:
        lines.extend(
            [
                f"### {row['inner_transition']}",
                f"- stability_kind: {row['stability_kind']}",
                f"- count: {row['count']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- positive_contacts: {row['positive_contacts']}",
                f"- observed_potentials: {row['observed_potentials']}",
                f"- actions: {row['actions'] or '-'}",
                f"- families: {row['families'] or '-'}",
                "",
            ]
        )
    lines.extend(
        [
            "## Grenze",
            "- kein Memory-Schreiben",
            "- keine Motorik",
            "- kein Gate",
            "- keine harte Regel",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive inner-state stability report")
    parser.add_argument("--timeline-csv", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    detail, overview, transition_summary = build_rows(Path(args.timeline_csv))
    write_outputs(detail, overview, transition_summary, Path(args.output_dir))
    print(
        f"stability_rows={len(detail)} "
        f"overview_rows={len(overview)} transition_rows={len(transition_summary)}"
    )
    for row in overview[:20]:
        print(
            f"{row['stability_kind']} {row['inner_state']} {row['contact_quality']} "
            f"count={row['count']} reward={row['reward_sum']}"
        )


if __name__ == "__main__":
    main()
