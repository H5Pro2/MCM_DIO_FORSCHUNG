"""Report passive reflection timeline per DIO_MINI family.

This joins stored reflection_maps into a family-level timeline. It is a reader
only and must stay outside the mini motor path.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.semantic_memory import SemanticMemory


def _safe_float(value: object) -> float:
    try:
        return float(value or 0.0)
    except Exception:
        return 0.0


def _safe_int(value: object) -> int:
    try:
        return int(value or 0)
    except Exception:
        return 0


def _probe_order(probe: str) -> tuple:
    text = str(probe or "")
    digits = "".join(char for char in text if char.isdigit())
    return (_safe_int(digits), text)


def _timeline_state(states: list[str]) -> str:
    state_set = {str(state or "") for state in states}
    has_reconfirmed = "reflection_memory_reconfirmed" in state_set
    has_conflict = "reflection_memory_conflict" in state_set
    has_quiet = "reflection_memory_quiet" in state_set
    if has_conflict and has_reconfirmed:
        return "mixed_reconfirmed_and_conflict"
    if has_conflict:
        return "conflict_seen"
    if has_reconfirmed and has_quiet:
        return "reconfirmed_with_quiet_return"
    if has_reconfirmed:
        return "reconfirmed_stable"
    if has_quiet:
        return "quiet_only"
    return "unclassified"


def _family_sentence(family: str, state: str, timeline: str, reward_sum: float) -> str:
    prefix = f"{family}: "
    if state == "mixed_reconfirmed_and_conflict":
        return prefix + "wurde getragen, aber nicht identisch in jeder Welt; Konflikt gehoert zur Akte."
    if state == "conflict_seen":
        return prefix + "wurde vor allem als Konfliktspur wiedergefunden."
    if state == "reconfirmed_with_quiet_return":
        return prefix + "wurde getragen und spaeter auch still wiedergefunden."
    if state == "reconfirmed_stable":
        return prefix + "wurde ueber die gelesenen Welten getragen wiedergefunden."
    if state == "quiet_only":
        return prefix + "ist bekannt, blieb in der gelesenen Welt aber still."
    return prefix + f"bleibt unklar; timeline={timeline or '-'} reward_sum={reward_sum:.6f}."


def build_rows(memory: SemanticMemory, selected_families: set[str] | None = None) -> list[dict]:
    maps = dict(memory.data.get("reflection_maps", {}) or {})
    grouped: dict[str, list[dict]] = {}
    for key, payload in maps.items():
        item = dict(payload or {})
        item.setdefault("reflection_map_symbol", key)
        family = str(item.get("symbol_family", "") or "")
        if not family:
            continue
        if selected_families and family not in selected_families:
            continue
        grouped.setdefault(family, []).append(item)

    rows = []
    for family, items in sorted(grouped.items()):
        ordered = sorted(items, key=lambda item: _probe_order(str(item.get("source_probe", "") or "")))
        states = [str(item.get("reflection_map_state", "") or "-") for item in ordered]
        probes = [str(item.get("source_probe", "") or "-") for item in ordered]
        timeline = " -> ".join(f"{probe}:{state}" for probe, state in zip(probes, states))
        reward_sum = sum(_safe_float(item.get("reward_sum", 0.0)) for item in ordered)
        best_reward_sum = sum(_safe_float(item.get("best_reward_sum", 0.0)) for item in ordered)
        seen_count = sum(_safe_int(item.get("seen_count", 0)) for item in ordered)
        executed_count = sum(_safe_int(item.get("executed_count", 0)) for item in ordered)
        observed_count = sum(_safe_int(item.get("observed_count", 0)) for item in ordered)
        state = _timeline_state(states)
        rows.append(
            {
                "family": family,
                "timeline_state": state,
                "timeline": timeline,
                "probe_count": len(ordered),
                "seen_count": seen_count,
                "executed_count": executed_count,
                "observed_count": observed_count,
                "reward_sum": round(reward_sum, 6),
                "best_reward_sum": round(best_reward_sum, 6),
                "map_symbols": "|".join(str(item.get("reflection_map_symbol", "") or "") for item in ordered),
                "passive_sentence": _family_sentence(family, state, timeline, reward_sum),
            }
        )

    rows.sort(
        key=lambda item: (
            str(item.get("timeline_state", "")) not in ("mixed_reconfirmed_and_conflict", "reconfirmed_stable"),
            -_safe_float(item.get("reward_sum", 0.0)),
            str(item.get("family", "")),
        )
    )
    return rows


def write_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "dio_mini_family_reflection_timeline.csv"
    json_path = output_dir / "dio_mini_family_reflection_timeline.json"
    md_path = output_dir / "dio_mini_family_reflection_timeline.md"
    fields = [
        "family",
        "timeline_state",
        "probe_count",
        "seen_count",
        "executed_count",
        "observed_count",
        "reward_sum",
        "best_reward_sum",
        "timeline",
        "map_symbols",
        "passive_sentence",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Family Reflection Timeline", ""]
    if not rows:
        lines.append("Keine reflection_maps gefunden.")
    for row in rows:
        lines.extend(
            [
                f"## {row['family']}",
                f"- state: {row['timeline_state']}",
                f"- passive_sentence: {row['passive_sentence']}",
                f"- timeline: {row['timeline']}",
                f"- seen / executed / observed: {row['seen_count']} / {row['executed_count']} / {row['observed_count']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive DIO_MINI family reflection timeline")
    parser.add_argument("--memory", required=True)
    parser.add_argument("--family", action="append", default=[])
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    memory = SemanticMemory(args.memory)
    memory.load()
    selected = {str(item).strip() for item in args.family if str(item).strip()}
    rows = build_rows(memory, selected_families=selected or None)
    write_outputs(rows, Path(args.output_dir))
    print(f"families={len(rows)}")
    for row in rows:
        print(f"{row['family']} state={row['timeline_state']} reward={row['reward_sum']}")


if __name__ == "__main__":
    main()
