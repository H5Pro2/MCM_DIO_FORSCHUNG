"""Inspect passive consequence potential for unconfirmed carried alignments.

This report reads alignment rows and episode traces. It checks whether families
that were carried but unconfirmed had a positive observed future action in the
episode trace. It is passive and does not feed Mini-DIO runtime.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value if value not in (None, "") else default)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(float(value if value not in (None, "") else default))
    except Exception:
        return default


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered_fields = list(fields)
    for row in rows:
        for key in row.keys():
            if key not in ordered_fields:
                ordered_fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=ordered_fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_world_args(items: list[str]) -> dict[str, Path]:
    worlds: dict[str, Path] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"World argument must be label=path: {item}")
        label, raw_path = item.split("=", 1)
        worlds[label.strip()] = Path(raw_path.strip())
    return worlds


def _episode_files(root: Path) -> list[Path]:
    if root.is_file() and root.name == "episodes.csv":
        return [root]
    return sorted(root.rglob("episodes.csv"))


def aggregate_episode_potential(root: Path) -> dict[str, dict]:
    families: dict[str, dict] = {}
    for path in _episode_files(root):
        for row in _read_csv(path):
            family = str(row.get("symbol_family", "") or "-")
            item = families.setdefault(
                family,
                {
                    "episodes": 0,
                    "best_long": 0,
                    "best_short": 0,
                    "best_wait": 0,
                    "best_reward_sum": 0.0,
                    "best_positive_count": 0,
                    "observation_pressure_sum": 0.0,
                    "trade_readiness_sum": 0.0,
                    "max_best_reward": 0.0,
                    "last_best_action": "-",
                },
            )
            best_action = str(row.get("best_action_training", "") or "-").upper()
            best_reward = _safe_float(row.get("best_reward_training"))
            item["episodes"] += 1
            item["best_reward_sum"] += best_reward
            item["observation_pressure_sum"] += _safe_float(row.get("observation_learning_pressure"))
            item["trade_readiness_sum"] += _safe_float(row.get("trade_readiness"))
            item["max_best_reward"] = max(float(item["max_best_reward"]), best_reward)
            item["last_best_action"] = best_action
            if best_reward > 0.0:
                item["best_positive_count"] += 1
            if best_action == "LONG":
                item["best_long"] += 1
            elif best_action == "SHORT":
                item["best_short"] += 1
            else:
                item["best_wait"] += 1
    return families


def consequence_state(row: dict) -> str:
    positive_count = _safe_int(row.get("best_positive_count"))
    avg_best_reward = _safe_float(row.get("avg_best_reward"))
    best_long = _safe_int(row.get("best_long"))
    best_short = _safe_int(row.get("best_short"))
    if positive_count > 0 and avg_best_reward > 0.0 and (best_long + best_short) > 0:
        return "unconfirmed_consequence_would_have_carried"
    if positive_count > 0:
        return "unconfirmed_consequence_partly_visible"
    return "unconfirmed_consequence_not_visible"


def build_report(alignment_rows: list[dict], worlds: dict[str, Path]) -> dict:
    episode_by_world = {label: aggregate_episode_potential(root) for label, root in worlds.items()}
    rows: list[dict] = []
    counts: dict[str, int] = {}
    for alignment in alignment_rows:
        state = str(alignment.get("alignment_state", "") or "")
        if state not in ("alignment_carried_unconfirmed", "alignment_inner_carried_unconfirmed"):
            continue
        world = str(alignment.get("world_label", "") or "")
        family = str(alignment.get("symbol_family", "") or "")
        potential = dict(episode_by_world.get(world, {}).get(family, {}) or {})
        episodes = max(1, _safe_int(potential.get("episodes")))
        row = {
            "world_label": world,
            "symbol_family": family,
            "alignment_state": state,
            "reflection_carry": _safe_float(alignment.get("avg_reflection_carry")),
            "reflection_strain": _safe_float(alignment.get("avg_reflection_strain")),
            "world_carry": _safe_float(alignment.get("world_carry")),
            "best_long": _safe_int(potential.get("best_long")),
            "best_short": _safe_int(potential.get("best_short")),
            "best_wait": _safe_int(potential.get("best_wait")),
            "best_positive_count": _safe_int(potential.get("best_positive_count")),
            "avg_best_reward": round(_safe_float(potential.get("best_reward_sum")) / episodes, 9),
            "max_best_reward": round(_safe_float(potential.get("max_best_reward")), 9),
            "avg_observation_pressure": round(_safe_float(potential.get("observation_pressure_sum")) / episodes, 9),
            "avg_trade_readiness": round(_safe_float(potential.get("trade_readiness_sum")) / episodes, 9),
            "passive_only": True,
            "influences_action": False,
            "is_gate": False,
        }
        row["consequence_state"] = consequence_state(row)
        counts[row["consequence_state"]] = counts.get(row["consequence_state"], 0) + 1
        rows.append(row)
    rows.sort(
        key=lambda row: (
            str(row.get("consequence_state", "")),
            -_safe_float(row.get("avg_best_reward")),
            -_safe_float(row.get("reflection_carry")),
            str(row.get("world_label", "")),
            str(row.get("symbol_family", "")),
        )
    )
    return {
        "schema": "dio_mini_passive_unconfirmed_consequence.v1",
        "summary": {
            "families": len(rows),
            "consequence_counts": dict(sorted(counts.items())),
            "passive_only": True,
            "influences_action": False,
        },
        "rows": rows,
    }


def write_report(report: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "passive_unconfirmed_consequence.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    rows = list(report.get("rows", []) or [])
    _write_csv(
        output_dir / "passive_unconfirmed_consequence.csv",
        rows,
        [
            "world_label",
            "symbol_family",
            "alignment_state",
            "consequence_state",
            "best_long",
            "best_short",
            "best_wait",
            "best_positive_count",
            "avg_best_reward",
            "max_best_reward",
            "reflection_carry",
            "reflection_strain",
            "world_carry",
        ],
    )
    lines = [
        "# Mini-DIO Passive Unconfirmed Consequence",
        "",
        "Grenze: passiver Nachblick, keine Handlung, kein Gate.",
        "",
        "## Summary",
    ]
    for key, value in dict(report.get("summary", {}) or {}).items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Rows"])
    for row in rows[:32]:
        lines.append(
            f"- {row['world_label']} {row['symbol_family']} {row['consequence_state']} "
            f"best_long={row['best_long']} best_short={row['best_short']} "
            f"avg_best_reward={row['avg_best_reward']} "
            f"r_carry={row['reflection_carry']} world_carry={row['world_carry']}"
        )
    (output_dir / "passive_unconfirmed_consequence.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--alignment-csv", type=Path, required=True)
    parser.add_argument("--world", action="append", default=[], help="label=debug_root")
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = build_report(_read_csv(args.alignment_csv), parse_world_args(args.world))
    write_report(report, args.output_dir)
    print(json.dumps(report["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
