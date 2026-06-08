"""Passive maturity consequence landscape for Mini-DIO.

This report separates real action from passive afterlook. It is diagnostic only.
It must not be used as an entry gate, motoric rule, or future teacher.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


PASSIVE_BOUNDARY = {
    "passive_only": True,
    "read_by_mini_dio": False,
    "influences_action": False,
    "is_gate": False,
    "is_motoric": False,
    "is_future_teacher": False,
}


def _f(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _i(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _collect_episode_afterlook(world_roots: dict[str, Path]) -> dict[tuple[str, str], dict[str, Any]]:
    agg: dict[tuple[str, str], dict[str, Any]] = {}
    for world_label, root in world_roots.items():
        for episode_file in root.rglob("episodes.csv"):
            for row in _read_csv(episode_file):
                family = str(row.get("symbol_family", "") or "").strip()
                if not family:
                    continue
                key = (world_label, family)
                item = agg.setdefault(
                    key,
                    {
                        "world_label": world_label,
                        "symbol_family": family,
                        "rows": 0,
                        "best_rewards": [],
                        "best_positive_count": 0,
                        "best_long": 0,
                        "best_short": 0,
                        "best_wait": 0,
                        "event_tp": 0,
                        "event_sl": 0,
                        "event_trades": 0,
                        "event_reward_sum": 0.0,
                    },
                )
                item["rows"] += 1
                best_action = str(row.get("best_action_training", "") or "").upper()
                best_reward = _f(row.get("best_reward_training"))
                item["best_rewards"].append(best_reward)
                if best_reward > 0.0 and best_action in {"LONG", "SHORT"}:
                    item["best_positive_count"] += 1
                if best_action == "LONG":
                    item["best_long"] += 1
                elif best_action == "SHORT":
                    item["best_short"] += 1
                elif best_action == "WAIT":
                    item["best_wait"] += 1

                event = str(row.get("outcome_event", "") or "").upper()
                if event in {"TP", "SL"}:
                    item["event_trades"] += 1
                    item["event_reward_sum"] += _f(row.get("event_reward"))
                    if event == "TP":
                        item["event_tp"] += 1
                    elif event == "SL":
                        item["event_sl"] += 1
    return agg


def _direction_hint(long_count: int, short_count: int) -> str:
    if long_count > short_count:
        return "LONG"
    if short_count > long_count:
        return "SHORT"
    if long_count or short_count:
        return "MIXED"
    return "NONE"


def _state_for(row: dict[str, str], episode: dict[str, Any] | None) -> str:
    trades = _i(row.get("reflection_trades"))
    tp = _i(row.get("reflection_tp"))
    sl = _i(row.get("reflection_sl"))
    reward_sum = _f(row.get("reflection_reward_sum"))
    alignment_state = str(row.get("alignment_state", "") or "").strip()
    best_positive = _i((episode or {}).get("best_positive_count"))
    avg_best_reward = mean((episode or {}).get("best_rewards") or [0.0])

    if trades > 0:
        if tp > sl or reward_sum > 0.0:
            return "action_carried"
        if sl > tp or reward_sum < 0.0:
            return "action_not_carried"
        return "action_unclear"
    if best_positive > 0 and avg_best_reward > 0.0:
        if alignment_state in {"alignment_carried_unconfirmed", "alignment_inner_carried_unconfirmed"}:
            return "withheld_carried_context_later_carried"
        if alignment_state == "alignment_cautious":
            return "withheld_cautious_context_later_carried"
        if alignment_state == "alignment_open":
            return "withheld_open_context_later_carried"
        return "withheld_later_carried"
    return "withheld_not_carried"


def build_report(alignment_csv: Path, world_roots: dict[str, Path]) -> dict[str, Any]:
    rows = _read_csv(alignment_csv)
    episodes = _collect_episode_afterlook(world_roots)
    entries: list[dict[str, Any]] = []
    state_counts: Counter[str] = Counter()

    for row in rows:
        world_label = str(row.get("world_label", "") or "").strip()
        family = str(row.get("symbol_family", "") or "").strip()
        if not world_label or not family:
            continue
        episode = episodes.get((world_label, family), {})
        state = _state_for(row, episode)
        state_counts[state] += 1
        best_rewards = episode.get("best_rewards") or []
        entry = {
            "world_label": world_label,
            "symbol_family": family,
            "maturity_consequence_state": state,
            "alignment_state": row.get("alignment_state", ""),
            "reflection_trades": _i(row.get("reflection_trades")),
            "reflection_tp": _i(row.get("reflection_tp")),
            "reflection_sl": _i(row.get("reflection_sl")),
            "reflection_reward_sum": _f(row.get("reflection_reward_sum")),
            "avg_reflection_carry": _f(row.get("avg_reflection_carry")),
            "avg_reflection_strain": _f(row.get("avg_reflection_strain")),
            "world_carry": _f(row.get("world_carry")),
            "world_carried_cos": _f(row.get("world_carried_cos")),
            "afterlook_rows": _i(episode.get("rows")),
            "afterlook_best_positive_count": _i(episode.get("best_positive_count")),
            "afterlook_avg_best_reward": mean(best_rewards or [0.0]),
            "afterlook_best_long": _i(episode.get("best_long")),
            "afterlook_best_short": _i(episode.get("best_short")),
            "afterlook_best_wait": _i(episode.get("best_wait")),
            "afterlook_direction_hint": _direction_hint(
                _i(episode.get("best_long")),
                _i(episode.get("best_short")),
            ),
            "event_trades_seen": _i(episode.get("event_trades")),
            "event_tp_seen": _i(episode.get("event_tp")),
            "event_sl_seen": _i(episode.get("event_sl")),
            "event_reward_sum_seen": _f(episode.get("event_reward_sum")),
            **PASSIVE_BOUNDARY,
        }
        entries.append(entry)

    return {
        "boundary": dict(PASSIVE_BOUNDARY),
        "alignment_csv": str(alignment_csv),
        "world_roots": {k: str(v) for k, v in world_roots.items()},
        "summary": {
            "families": len(entries),
            "state_counts": dict(state_counts),
            "avg_reflection_carry": mean([e["avg_reflection_carry"] for e in entries] or [0.0]),
            "avg_world_carry": mean([e["world_carry"] for e in entries] or [0.0]),
            "avg_afterlook_best_reward": mean([e["afterlook_avg_best_reward"] for e in entries] or [0.0]),
        },
        "entries": entries,
    }


def _write_outputs(report: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "passive_maturity_consequence_landscape.json"
    csv_path = output_dir / "passive_maturity_consequence_landscape.csv"
    md_path = output_dir / "passive_maturity_consequence_landscape.md"
    txt_path = output_dir / "passive_maturity_consequence_landscape.txt"

    json_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    entries = report.get("entries", [])
    if entries:
        with csv_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(entries[0].keys()))
            writer.writeheader()
            writer.writerows(entries)
    else:
        csv_path.write_text("world_label,symbol_family,maturity_consequence_state\n", encoding="utf-8")

    summary = report.get("summary", {})
    lines = [
        "# Mini-DIO Passive Maturity Consequence Landscape",
        "",
        "- boundary: passive only; not read by Mini-DIO; no action; no gate",
        "",
        "## Summary",
        f"- families: {summary.get('families', 0)}",
        f"- state_counts: {summary.get('state_counts', {})}",
        f"- avg_reflection_carry: {summary.get('avg_reflection_carry', 0.0):.9f}",
        f"- avg_world_carry: {summary.get('avg_world_carry', 0.0):.9f}",
        f"- avg_afterlook_best_reward: {summary.get('avg_afterlook_best_reward', 0.0):.9f}",
        "",
        "## Strongest Passive Entries",
    ]
    ranked = sorted(
        entries,
        key=lambda e: (
            str(e.get("maturity_consequence_state", "")).startswith("withheld_carried"),
            e.get("afterlook_avg_best_reward", 0.0),
            e.get("avg_reflection_carry", 0.0),
        ),
        reverse=True,
    )
    for entry in ranked[:20]:
        lines.append(
            "- "
            f"{entry['world_label']}/{entry['symbol_family']}: "
            f"{entry['maturity_consequence_state']}, "
            f"direction={entry['afterlook_direction_hint']}, "
            f"afterlook_reward={entry['afterlook_avg_best_reward']:.6f}, "
            f"r_carry={entry['avg_reflection_carry']:.6f}."
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- keine Entry-Regel",
            "- keine Future-Teacher-Mechanik",
            "- nur passive Unterscheidung von Handlung, Nicht-Handlung und spaeterer Konsequenz",
        ]
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    txt_lines = []
    for entry in ranked:
        txt_lines.append(
            f"{entry['world_label']} {entry['symbol_family']} | "
            f"{entry['maturity_consequence_state']} | "
            f"{entry['afterlook_direction_hint']} | "
            f"afterlook={entry['afterlook_avg_best_reward']:.6f}"
        )
    txt_path.write_text("\n".join(txt_lines) + ("\n" if txt_lines else ""), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--alignment-csv", required=True)
    parser.add_argument(
        "--world",
        action="append",
        default=[],
        help="World binding as label=debug_root.",
    )
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    world_roots: dict[str, Path] = {}
    for item in args.world:
        if "=" not in item:
            raise SystemExit(f"Invalid --world value: {item!r}; expected label=path")
        label, path = item.split("=", 1)
        world_roots[label] = Path(path)

    report = build_report(Path(args.alignment_csv), world_roots)
    _write_outputs(report, Path(args.output_dir))
    print(json.dumps(report["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
