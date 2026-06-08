"""Aggregate DIO mini local confirmations across controlled worlds.

Diagnostic only. This keeps reflection separate from motor action and answers:
which syntax families are repeatedly confirmed locally, and which remain
observed potential?
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

from DIO_MINI.local_confirmation import build_confirmation


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _phase_dirs(debug_root: Path) -> list[Path]:
    if (debug_root / "dio_mini_lauf_1").exists():
        return [debug_root]
    return sorted(path for path in debug_root.iterdir() if path.is_dir() and any(path.glob("dio_mini_lauf_*/episodes.csv")))


def _support_pair(family: str, support_family: str, support_matches_local: object) -> str:
    if not family or family == "-" or not support_family or support_family == "-":
        return "-"
    if _safe_int(support_matches_local, 0) <= 0:
        return "-"
    return "<->".join(sorted((family, support_family)))


def build_history(debug_root: Path, reflection_map_path: Path) -> tuple[list[dict], list[dict], list[dict]]:
    detail_rows = []
    summaries: dict[str, dict] = {}
    relation_summaries: dict[str, dict] = {}
    for phase_dir in _phase_dirs(debug_root):
        phase = phase_dir.name
        for row in build_confirmation(phase_dir, reflection_map_path):
            item = dict(row)
            item["phase"] = phase
            item["support_pair"] = _support_pair(
                str(item.get("family", "-") or "-"),
                str(item.get("best_support_family", "-") or "-"),
                item.get("support_matches_local", 0),
            )
            detail_rows.append(item)
            family = str(item.get("family", "-") or "-")
            summary = summaries.setdefault(
                family,
                {
                    "family": family,
                    "phases": set(),
                    "rows": 0,
                    "executed_local_confirmation": 0,
                    "observed_related_potential": 0,
                    "unexecuted_local_potential": 0,
                    "unconfirmed": 0,
                    "long_local": 0,
                    "short_local": 0,
                    "confirmation_sum": 0.0,
                    "confirmation_max": 0.0,
                    "reward_sum": 0.0,
                    "support_families": defaultdict(int),
                    "conflict_families": defaultdict(int),
                },
            )
            label = str(item.get("confirmation_label", "unconfirmed") or "unconfirmed")
            action = str(item.get("local_action", "-") or "-").upper()
            support_family = str(item.get("best_support_family", "-") or "-")
            conflict_family = str(item.get("best_conflict_family", "-") or "-")
            confirmation = _safe_float(item.get("local_confirmation", 0.0))
            summary["phases"].add(phase)
            summary["rows"] += 1
            summary[label] = _safe_int(summary.get(label, 0)) + 1
            if action == "LONG":
                summary["long_local"] += 1
            elif action == "SHORT":
                summary["short_local"] += 1
            summary["confirmation_sum"] += confirmation
            summary["confirmation_max"] = max(_safe_float(summary["confirmation_max"]), confirmation)
            summary["reward_sum"] += _safe_float(item.get("reward_sum", 0.0))
            if support_family and support_family != "-":
                summary["support_families"][support_family] += 1
            if conflict_family and conflict_family != "-":
                summary["conflict_families"][conflict_family] += 1
            support_pair = str(item.get("support_pair", "-") or "-")
            if support_pair != "-":
                relation_summary = relation_summaries.setdefault(
                    support_pair,
                    {
                        "support_pair": support_pair,
                        "families": set(),
                        "phases": set(),
                        "rows": 0,
                        "executed_local_confirmation": 0,
                        "observed_related_potential": 0,
                        "long_local": 0,
                        "short_local": 0,
                        "confirmation_sum": 0.0,
                        "confirmation_max": 0.0,
                        "reward_sum": 0.0,
                    },
                )
                label = str(item.get("confirmation_label", "unconfirmed") or "unconfirmed")
                action = str(item.get("local_action", "-") or "-").upper()
                relation_summary["families"].add(family)
                relation_summary["families"].add(support_family)
                relation_summary["phases"].add(phase)
                relation_summary["rows"] += 1
                relation_summary[label] = _safe_int(relation_summary.get(label, 0)) + 1
                if action == "LONG":
                    relation_summary["long_local"] += 1
                elif action == "SHORT":
                    relation_summary["short_local"] += 1
                relation_summary["confirmation_sum"] += confirmation
                relation_summary["confirmation_max"] = max(_safe_float(relation_summary["confirmation_max"]), confirmation)
                relation_summary["reward_sum"] += _safe_float(item.get("reward_sum", 0.0))

    summary_rows = []
    for summary in summaries.values():
        rows = max(1, _safe_int(summary["rows"]))
        support = sorted(summary["support_families"].items(), key=lambda item: item[1], reverse=True)
        conflict = sorted(summary["conflict_families"].items(), key=lambda item: item[1], reverse=True)
        summary_rows.append(
            {
                "family": summary["family"],
                "phases": ",".join(sorted(summary["phases"])),
                "phase_count": len(summary["phases"]),
                "rows": rows,
                "executed_local_confirmation": _safe_int(summary.get("executed_local_confirmation", 0)),
                "observed_related_potential": _safe_int(summary.get("observed_related_potential", 0)),
                "unexecuted_local_potential": _safe_int(summary.get("unexecuted_local_potential", 0)),
                "unconfirmed": _safe_int(summary.get("unconfirmed", 0)),
                "long_local": _safe_int(summary.get("long_local", 0)),
                "short_local": _safe_int(summary.get("short_local", 0)),
                "avg_local_confirmation": round(_safe_float(summary["confirmation_sum"]) / rows, 6),
                "max_local_confirmation": round(_safe_float(summary["confirmation_max"]), 6),
                "reward_sum": round(_safe_float(summary["reward_sum"]), 6),
                "top_support_family": support[0][0] if support else "-",
                "top_support_count": support[0][1] if support else 0,
                "top_conflict_family": conflict[0][0] if conflict else "-",
                "top_conflict_count": conflict[0][1] if conflict else 0,
            }
        )
    summary_rows.sort(
        key=lambda item: (
            item["executed_local_confirmation"],
            item["observed_related_potential"],
            item["phase_count"],
            item["max_local_confirmation"],
        ),
        reverse=True,
    )
    relation_rows = []
    for summary in relation_summaries.values():
        rows = max(1, _safe_int(summary["rows"]))
        relation_rows.append(
            {
                "support_pair": summary["support_pair"],
                "families": ",".join(sorted(summary["families"])),
                "phases": ",".join(sorted(summary["phases"])),
                "phase_count": len(summary["phases"]),
                "rows": rows,
                "executed_local_confirmation": _safe_int(summary.get("executed_local_confirmation", 0)),
                "observed_related_potential": _safe_int(summary.get("observed_related_potential", 0)),
                "long_local": _safe_int(summary.get("long_local", 0)),
                "short_local": _safe_int(summary.get("short_local", 0)),
                "avg_local_confirmation": round(_safe_float(summary["confirmation_sum"]) / rows, 6),
                "max_local_confirmation": round(_safe_float(summary["confirmation_max"]), 6),
                "reward_sum": round(_safe_float(summary["reward_sum"]), 6),
            }
        )
    relation_rows.sort(
        key=lambda item: (
            item["executed_local_confirmation"],
            item["observed_related_potential"],
            item["phase_count"],
            item["max_local_confirmation"],
        ),
        reverse=True,
    )
    detail_rows.sort(key=lambda item: (str(item.get("phase", "")), _safe_float(item.get("local_confirmation", 0.0))), reverse=True)
    return detail_rows, summary_rows, relation_rows


def write_outputs(detail_rows: list[dict], summary_rows: list[dict], relation_rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "dio_mini_confirmation_history_details.json").write_text(
        json.dumps(detail_rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "dio_mini_confirmation_history_summary.json").write_text(
        json.dumps(summary_rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "dio_mini_confirmation_relation_summary.json").write_text(
        json.dumps(relation_rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    if detail_rows:
        with (output_dir / "dio_mini_confirmation_history_details.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(detail_rows[0].keys()))
            writer.writeheader()
            writer.writerows(detail_rows)
    if summary_rows:
        with (output_dir / "dio_mini_confirmation_history_summary.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(summary_rows[0].keys()))
            writer.writeheader()
            writer.writerows(summary_rows)
    if relation_rows:
        with (output_dir / "dio_mini_confirmation_relation_summary.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(relation_rows[0].keys()))
            writer.writeheader()
            writer.writerows(relation_rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate DIO mini confirmation history")
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--reflection-map", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    detail_rows, summary_rows, relation_rows = build_history(Path(args.debug_root), Path(args.reflection_map))
    write_outputs(detail_rows, summary_rows, relation_rows, Path(args.output_dir))
    for row in summary_rows[:12]:
        print(
            f"family={row['family']} phases={row['phase_count']} executed={row['executed_local_confirmation']} "
            f"observed={row['observed_related_potential']} max_confirm={row['max_local_confirmation']:.4f}"
        )
    for row in relation_rows[:8]:
        print(
            f"relation={row['support_pair']} phases={row['phase_count']} executed={row['executed_local_confirmation']} "
            f"observed={row['observed_related_potential']} max_confirm={row['max_local_confirmation']:.4f}"
        )


if __name__ == "__main__":
    main()
