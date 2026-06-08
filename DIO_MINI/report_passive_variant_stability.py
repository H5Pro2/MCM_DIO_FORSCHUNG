"""Build a consolidated passive stability report for Mini-DIO variants.

The report joins multiple passive variant maturity maps and optional
map-compare reports. It is diagnostic only:

- no memory writes
- no action influence
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


def _parse_labeled_path(value: str) -> tuple[str, Path]:
    if "=" not in value:
        path = Path(value)
        return path.stem, path
    label, raw_path = value.split("=", 1)
    return label.strip(), Path(raw_path.strip())


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


def _load_variant_rows(variant_specs: list[str]) -> list[dict]:
    detail: list[dict] = []
    for spec in variant_specs:
        label, path = _parse_labeled_path(spec)
        for row in _read_csv(path):
            item = dict(row)
            item["variant_label"] = label
            item["source_variant_map"] = str(path)
            item["event_reward_sum"] = round(_safe_float(item.get("event_reward_sum")), 9)
            item["episode_count"] = _safe_int(item.get("episode_count"))
            item["transfer_similarity"] = round(_safe_float(item.get("transfer_similarity")), 9)
            item["passive_only"] = 1
            item["writes_training_memory"] = 0
            item["read_by_mini_dio"] = 0
            item["influences_action"] = 0
            item["is_gate"] = 0
            item["is_motoric"] = 0
            detail.append(item)
    detail.sort(key=lambda row: (str(row.get("variant_label", "")), str(row.get("variant_reife_state", "")), str(row.get("family_action", ""))))
    return detail


def _state_summary(rows: list[dict]) -> list[dict]:
    buckets: dict[str, dict] = {}
    for row in rows:
        state = str(row.get("variant_reife_state", "") or "variant_unknown")
        bucket = buckets.setdefault(
            state,
            {
                "variant_reife_state": state,
                "count": 0,
                "event_reward_sum": 0.0,
                "episode_count": 0,
                "variants": set(),
                "family_actions": [],
            },
        )
        bucket["count"] += 1
        bucket["event_reward_sum"] += _safe_float(row.get("event_reward_sum"))
        bucket["episode_count"] += _safe_int(row.get("episode_count"))
        bucket["variants"].add(str(row.get("variant_label", "") or ""))
        bucket["family_actions"].append(f"{row.get('variant_label')}:{row.get('family_action')}")
    summary: list[dict] = []
    for row in buckets.values():
        summary.append(
            {
                "variant_reife_state": row["variant_reife_state"],
                "count": row["count"],
                "event_reward_sum": round(float(row["event_reward_sum"]), 9),
                "episode_count": row["episode_count"],
                "variant_count": len(row["variants"]),
                "variants": ",".join(sorted(row["variants"])),
                "family_actions": ",".join(sorted(name for name in row["family_actions"] if name)),
            }
        )
    summary.sort(key=lambda item: (str(item["variant_reife_state"]), str(item["variants"])))
    return summary


def _carried_action_summary(rows: list[dict]) -> list[dict]:
    buckets: dict[str, dict] = {}
    for row in rows:
        if str(row.get("variant_reife_state", "") or "") != "variant_self_carried_action_trace":
            continue
        action = str(row.get("action", "") or "")
        bucket = buckets.setdefault(
            action,
            {
                "action": action,
                "count": 0,
                "event_reward_sum": 0.0,
                "episode_count": 0,
                "variants": set(),
                "family_actions": [],
            },
        )
        bucket["count"] += 1
        bucket["event_reward_sum"] += _safe_float(row.get("event_reward_sum"))
        bucket["episode_count"] += _safe_int(row.get("episode_count"))
        bucket["variants"].add(str(row.get("variant_label", "") or ""))
        bucket["family_actions"].append(f"{row.get('variant_label')}:{row.get('family_action')}")
    summary: list[dict] = []
    for row in buckets.values():
        summary.append(
            {
                "action": row["action"],
                "count": row["count"],
                "event_reward_sum": round(float(row["event_reward_sum"]), 9),
                "episode_count": row["episode_count"],
                "variant_count": len(row["variants"]),
                "variants": ",".join(sorted(row["variants"])),
                "family_actions": ",".join(sorted(name for name in row["family_actions"] if name)),
            }
        )
    summary.sort(key=lambda item: (str(item["action"]), str(item["variants"])))
    return summary


def _load_compare_rows(compare_specs: list[str]) -> list[dict]:
    detail: list[dict] = []
    for spec in compare_specs:
        label, path = _parse_labeled_path(spec)
        for row in _read_csv(path):
            item = dict(row)
            item["compare_label"] = label
            item["source_compare"] = str(path)
            item["reward_delta"] = round(_safe_float(item.get("reward_delta")), 9)
            item["episode_delta"] = _safe_int(item.get("episode_delta"))
            detail.append(item)
    detail.sort(key=lambda row: (str(row.get("compare_label", "")), str(row.get("compare_state", "")), str(row.get("family_action", ""))))
    return detail


def _compare_summary(rows: list[dict]) -> list[dict]:
    buckets: dict[str, dict] = {}
    for row in rows:
        key = f"{row.get('compare_label')}|{row.get('compare_state')}"
        bucket = buckets.setdefault(
            key,
            {
                "compare_label": str(row.get("compare_label", "") or ""),
                "compare_state": str(row.get("compare_state", "") or ""),
                "count": 0,
                "reward_delta": 0.0,
                "episode_delta": 0,
                "families": [],
            },
        )
        bucket["count"] += 1
        bucket["reward_delta"] += _safe_float(row.get("reward_delta"))
        bucket["episode_delta"] += _safe_int(row.get("episode_delta"))
        bucket["families"].append(str(row.get("family_action", "") or ""))
    summary: list[dict] = []
    for row in buckets.values():
        summary.append(
            {
                "compare_label": row["compare_label"],
                "compare_state": row["compare_state"],
                "count": row["count"],
                "reward_delta": round(float(row["reward_delta"]), 9),
                "episode_delta": row["episode_delta"],
                "families": ",".join(sorted(name for name in row["families"] if name)),
            }
        )
    summary.sort(key=lambda item: (str(item["compare_label"]), str(item["compare_state"])))
    return summary


def write_outputs(
    output_dir: Path,
    variant_rows: list[dict],
    state_summary: list[dict],
    carried_action_summary: list[dict],
    compare_rows: list[dict],
    compare_summary: list[dict],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    variant_csv = output_dir / "dio_mini_passive_variant_stability_detail.csv"
    state_csv = output_dir / "dio_mini_passive_variant_stability_state_summary.csv"
    carried_csv = output_dir / "dio_mini_passive_variant_stability_carried_action_summary.csv"
    compare_csv = output_dir / "dio_mini_passive_variant_stability_compare_detail.csv"
    compare_summary_csv = output_dir / "dio_mini_passive_variant_stability_compare_summary.csv"
    json_path = output_dir / "dio_mini_passive_variant_stability.json"
    md_path = output_dir / "dio_mini_passive_variant_stability.md"

    _write_csv(variant_csv, variant_rows, ["variant_label", "family_action", "variant_reife_state", "event_reward_sum"])
    _write_csv(state_csv, state_summary, ["variant_reife_state", "count", "event_reward_sum", "variant_count"])
    _write_csv(carried_csv, carried_action_summary, ["action", "count", "event_reward_sum", "variant_count"])
    _write_csv(compare_csv, compare_rows, ["compare_label", "family_action", "compare_state", "reward_delta", "episode_delta"])
    _write_csv(compare_summary_csv, compare_summary, ["compare_label", "compare_state", "count", "reward_delta", "episode_delta"])
    json_path.write_text(
        json.dumps(
            {
                "schema": "dio_mini_passive_variant_stability.v1",
                "state_summary": state_summary,
                "carried_action_summary": carried_action_summary,
                "compare_summary": compare_summary,
                "variant_detail": variant_rows,
                "compare_detail": compare_rows,
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
        "# Mini-DIO Passive Variant Stability",
        "",
        "## State Summary",
    ]
    for row in state_summary:
        lines.append(
            f"- {row['variant_reife_state']}: count={row['count']} "
            f"reward={float(row['event_reward_sum']):.6f} "
            f"episodes={row['episode_count']} variants={row['variants'] or '-'}"
        )
    lines.extend(["", "## Carried Actions"])
    if not carried_action_summary:
        lines.append("- keine getragenen Variantenhandlungen")
    for row in carried_action_summary:
        lines.append(
            f"- {row['action']}: count={row['count']} "
            f"reward={float(row['event_reward_sum']):.6f} "
            f"episodes={row['episode_count']} variants={row['variants'] or '-'} "
            f"families={row['family_actions'] or '-'}"
        )
    lines.extend(["", "## Stability Compare"])
    if not compare_summary:
        lines.append("- keine Vergleichsdaten")
    for row in compare_summary:
        lines.append(
            f"- {row['compare_label']} / {row['compare_state']}: count={row['count']} "
            f"reward_delta={float(row['reward_delta']):.6f} episode_delta={row['episode_delta']}"
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive_only=true",
            "- writes_training_memory=false",
            "- read_by_mini_dio=false",
            "- influences_action=false",
            "- is_gate=false",
            "- is_motoric=false",
        ]
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", action="append", required=True, help="label=path to variant reife map CSV")
    parser.add_argument("--compare", action="append", default=[], help="label=path to variant map compare CSV")
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    variant_rows = _load_variant_rows(args.variant)
    states = _state_summary(variant_rows)
    carried = _carried_action_summary(variant_rows)
    compare_rows = _load_compare_rows(args.compare)
    compares = _compare_summary(compare_rows)
    write_outputs(args.output_dir, variant_rows, states, carried, compare_rows, compares)
    print(f"passive_variant_stability variants={len(args.variant)} rows={len(variant_rows)} compares={len(compare_rows)}")
    for row in carried:
        print(
            f"carried {row['action']} count={row['count']} "
            f"reward={row['event_reward_sum']} variants={row['variants']}"
        )
    for row in compares:
        print(
            f"compare {row['compare_label']} {row['compare_state']} "
            f"count={row['count']} reward_delta={row['reward_delta']} episode_delta={row['episode_delta']}"
        )


if __name__ == "__main__":
    main()
