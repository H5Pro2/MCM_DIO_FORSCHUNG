"""Compare passive inner-coherence maps across DIO_MINI worlds.

This report reads multiple ``dio_mini_passive_inner_coherence_map_detail.csv``
files and compares inner-state sensor coupling across worlds. It is passive
diagnosis only.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


SENSOR_AVG_FIELDS = [
    "avg_sehen_form_flow",
    "avg_sehen_form_stability",
    "avg_hoeren_energy_tone",
    "avg_fuehlen_mcm_coherence",
    "avg_fuehlen_mcm_tension",
]


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


def _parse_input(raw: str) -> tuple[str, Path]:
    if "=" not in raw:
        raise SystemExit(f"--coherence must be label=csv_path, got: {raw}")
    label, path = raw.split("=", 1)
    label = label.strip()
    if not label:
        raise SystemExit(f"Empty label in --coherence: {raw}")
    return label, Path(path.strip())


def _read_labeled(label: str, path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            item = dict(row)
            item["world"] = label
            item["source_file"] = str(path)
            rows.append(item)
    return rows


def _weighted_add(group: dict, row: dict) -> None:
    count = max(1, _safe_int(row.get("count")))
    group["count"] += count
    group["reward_sum"] += _safe_float(row.get("reward_sum"))
    group["best_reward_sum"] += _safe_float(row.get("best_reward_sum"))
    group["families"].add(str(row.get("symbol_family", "") or ""))
    group["contact_qualities"].add(str(row.get("contact_quality", "") or ""))
    group["worlds"].add(str(row.get("world", "") or ""))
    for field in SENSOR_AVG_FIELDS:
        group["sensor_weighted"][field] += _safe_float(row.get(field)) * count


def _finish_group(group: dict) -> dict:
    count = max(1, int(group["count"]))
    row = {
        "inner_state": group["inner_state"],
        "contact_quality": group.get("contact_quality", ""),
        "world_count": len(group["worlds"]),
        "worlds": ",".join(sorted(name for name in group["worlds"] if name)),
        "count": int(group["count"]),
        "reward_sum": round(float(group["reward_sum"]), 6),
        "best_reward_sum": round(float(group["best_reward_sum"]), 6),
        "avg_reward": round(float(group["reward_sum"]) / count, 6),
        "families": ",".join(sorted(name for name in group["families"] if name)),
        "contact_qualities": ",".join(sorted(name for name in group["contact_qualities"] if name)),
    }
    for field in SENSOR_AVG_FIELDS:
        row[field] = round(float(group["sensor_weighted"][field]) / count, 6)
    return row


def build_rows(inputs: list[tuple[str, Path]]) -> tuple[list[dict], list[dict], list[dict]]:
    detail: list[dict] = []
    by_world_inner: dict[tuple[str, str], dict] = {}
    by_inner_contact: dict[tuple[str, str], dict] = {}
    for label, path in inputs:
        for row in _read_labeled(label, path):
            detail.append(row)
            inner = str(row.get("inner_state", "inner_unknown") or "inner_unknown")
            contact = str(row.get("contact_quality", "") or "")
            world_key = (label, inner)
            world_group = by_world_inner.setdefault(
                world_key,
                {
                    "inner_state": inner,
                    "contact_quality": "",
                    "worlds": {label},
                    "count": 0,
                    "reward_sum": 0.0,
                    "best_reward_sum": 0.0,
                    "families": set(),
                    "contact_qualities": set(),
                    "sensor_weighted": {field: 0.0 for field in SENSOR_AVG_FIELDS},
                },
            )
            _weighted_add(world_group, row)

            contact_key = (inner, contact)
            contact_group = by_inner_contact.setdefault(
                contact_key,
                {
                    "inner_state": inner,
                    "contact_quality": contact,
                    "worlds": set(),
                    "count": 0,
                    "reward_sum": 0.0,
                    "best_reward_sum": 0.0,
                    "families": set(),
                    "contact_qualities": set(),
                    "sensor_weighted": {field: 0.0 for field in SENSOR_AVG_FIELDS},
                },
            )
            _weighted_add(contact_group, row)

    world_summary = []
    for (world, _inner), group in by_world_inner.items():
        row = _finish_group(group)
        row["world"] = world
        world_summary.append(row)
    world_summary.sort(
        key=lambda row: (
            str(row.get("inner_state", "")) != "inner_carried",
            str(row.get("world", "")),
            -_safe_float(row.get("reward_sum")),
        )
    )

    transfer_summary = [_finish_group(group) for group in by_inner_contact.values()]
    transfer_summary.sort(
        key=lambda row: (
            str(row.get("inner_state", "")) != "inner_carried",
            -int(row.get("world_count", 0) or 0),
            -_safe_float(row.get("reward_sum")),
            str(row.get("contact_quality", "")),
        )
    )
    return detail, world_summary, transfer_summary


def write_outputs(detail: list[dict], world_summary: list[dict], transfer_summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_passive_inner_coherence_transfer_detail.csv"
    world_path = output_dir / "dio_mini_passive_inner_coherence_transfer_by_world.csv"
    transfer_path = output_dir / "dio_mini_passive_inner_coherence_transfer_summary.csv"
    json_path = output_dir / "dio_mini_passive_inner_coherence_transfer.json"
    md_path = output_dir / "dio_mini_passive_inner_coherence_transfer.md"

    detail_fields = list(detail[0].keys()) if detail else ["world", "inner_state", "symbol_family"]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)

    world_fields = list(world_summary[0].keys()) if world_summary else ["world", "inner_state", "count"]
    with world_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=world_fields)
        writer.writeheader()
        writer.writerows(world_summary)

    transfer_fields = list(transfer_summary[0].keys()) if transfer_summary else ["inner_state", "contact_quality", "count"]
    with transfer_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=transfer_fields)
        writer.writeheader()
        writer.writerows(transfer_summary)

    json_path.write_text(
        json.dumps(
            {"detail": detail, "world_summary": world_summary, "transfer_summary": transfer_summary},
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = ["# DIO Mini Passive Inner Coherence Transfer", ""]
    lines.append("## Transfer")
    lines.append("")
    if not transfer_summary:
        lines.append("Keine Transferdaten gefunden.")
    for row in transfer_summary:
        lines.extend(
            [
                f"### {row['inner_state']} / {row['contact_quality'] or '-'}",
                f"- world_count: {row['world_count']}",
                f"- worlds: {row['worlds'] or '-'}",
                f"- count: {row['count']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- best_reward_sum: {float(row['best_reward_sum']):.6f}",
                f"- avg_sehen_form_stability: {float(row['avg_sehen_form_stability']):.6f}",
                f"- avg_hoeren_energy_tone: {float(row['avg_hoeren_energy_tone']):.6f}",
                f"- avg_fuehlen_mcm_coherence: {float(row['avg_fuehlen_mcm_coherence']):.6f}",
                f"- avg_fuehlen_mcm_tension: {float(row['avg_fuehlen_mcm_tension']):.6f}",
                f"- families: {row['families'] or '-'}",
                "",
            ]
        )
    lines.append("## Pro Welt")
    lines.append("")
    for row in world_summary:
        lines.extend(
            [
                f"### {row['world']} / {row['inner_state']}",
                f"- count: {row['count']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- contact_qualities: {row['contact_qualities'] or '-'}",
                f"- avg_fuehlen_mcm_coherence: {float(row['avg_fuehlen_mcm_coherence']):.6f}",
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
    parser = argparse.ArgumentParser(description="Compare passive inner coherence across worlds")
    parser.add_argument("--coherence", action="append", required=True, help="label=coherence_detail_csv")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    detail, world_summary, transfer_summary = build_rows([_parse_input(item) for item in args.coherence])
    write_outputs(detail, world_summary, transfer_summary, Path(args.output_dir))
    print(
        f"detail_rows={len(detail)} world_rows={len(world_summary)} "
        f"transfer_rows={len(transfer_summary)}"
    )
    for row in transfer_summary[:20]:
        print(
            f"{row['inner_state']} {row['contact_quality']} worlds={row['world_count']} "
            f"reward={row['reward_sum']} families={row['families']}"
        )


if __name__ == "__main__":
    main()
