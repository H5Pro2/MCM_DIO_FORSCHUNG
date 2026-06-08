"""Build a passive DIO_MINI family file from semantic memory.

The family file joins action memory, observation memory and passive reflection
layers. It is a reader only; it does not write memory and it is not imported by
the mini motor path.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from DIO_MINI.semantic_memory import ACTION_NAMES, SemanticMemory


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


def _action_summary(record: dict, action: str) -> dict:
    state = dict(dict(record.get("actions", {}) or {}).get(action, {}) or {})
    return {
        f"{action.lower()}_count": _safe_int(state.get("count", 0)),
        f"{action.lower()}_reward_sum": round(_safe_float(state.get("reward_sum", 0.0)), 6),
        f"{action.lower()}_trust": round(_safe_float(state.get("trust", 0.0)), 6),
        f"{action.lower()}_caution": round(_safe_float(state.get("caution", 0.0)), 6),
    }


def _observation_summary(record: dict, action: str) -> dict:
    state = dict(dict(record.get("observations", {}) or {}).get(action, {}) or {})
    count = _safe_int(state.get("count", 0))
    recognition_sum = _safe_float(state.get("recognition_sum", 0.0))
    reward_sum = _safe_float(state.get("reward_sum", 0.0))
    return {
        f"observed_{action.lower()}_count": count,
        f"observed_{action.lower()}_recognition_avg": round(recognition_sum / max(1, count), 6),
        f"observed_{action.lower()}_reward_sum": round(reward_sum, 6),
    }


def _group_by_family(items: dict, family_key: str = "symbol_family") -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    if not isinstance(items, dict):
        return grouped
    for key, payload in items.items():
        item = dict(payload or {})
        item.setdefault("memory_key", key)
        family = str(item.get(family_key, "") or "")
        if not family:
            continue
        grouped.setdefault(family, []).append(item)
    return grouped


def _contact_lagen_by_family(items: dict) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    if not isinstance(items, dict):
        return grouped
    for key, payload in items.items():
        item = dict(payload or {})
        item.setdefault("memory_key", key)
        families = set()
        for list_key in ("top_direct_action", "top_observation_to_action"):
            for family in list(item.get(list_key, []) or []):
                text = str(family or "")
                if text:
                    families.add(text)
        for family in families:
            grouped.setdefault(family, []).append(item)
    return grouped


def _strongest_action_trace(row: dict) -> str:
    candidates = []
    for action in ACTION_NAMES:
        key = action.lower()
        count = _safe_int(row.get(f"{key}_count", 0))
        reward = _safe_float(row.get(f"{key}_reward_sum", 0.0))
        trust = _safe_float(row.get(f"{key}_trust", 0.0))
        caution = _safe_float(row.get(f"{key}_caution", 0.0))
        score = (reward * 0.55) + (trust * 1.0) - (caution * 0.75) + (min(8, count) * 0.02)
        candidates.append((score, reward, count, action))
    candidates.sort(reverse=True)
    return candidates[0][3] if candidates else "WAIT"


def _state_counts(items: list[dict], key: str) -> str:
    counts: dict[str, int] = {}
    for item in items:
        state = str(item.get(key, "") or "-")
        counts[state] = counts.get(state, 0) + 1
    return "|".join(f"{name}:{count}" for name, count in sorted(counts.items())) if counts else "-"


def _passive_sentence(row: dict) -> str:
    family = str(row.get("family", "") or "-")
    best = str(row.get("strongest_action_trace", "") or "WAIT")
    maps = str(row.get("reflection_map_states", "") or "")
    seeds = str(row.get("reflection_seed_states", "") or "")
    sentence = f"{family}: "
    if "reflection_memory_conflict" in maps:
        sentence += "wurde getragen und im Konflikt wiedergefunden; "
    elif "reflection_memory_reconfirmed" in maps:
        sentence += "wurde passiv wiedererkannt und getragen; "
    elif "reflection_memory_quiet" in maps:
        sentence += "wurde still wiedergefunden; "
    elif "reflection_seed_reconfirmed" in seeds:
        sentence += "hat einen getragenen Reflexionskeim; "
    else:
        sentence += "hat aktive oder beobachtete Erfahrung ohne passive Reflexionskarte; "

    if best in ("LONG", "SHORT"):
        sentence += f"die bisher staerkste Handlungsspur liegt bei {best}."
    else:
        sentence += "die bisher staerkste Spur bleibt Beobachtung/Warten."
    return sentence


def build_rows(memory: SemanticMemory, selected_families: set[str] | None = None) -> list[dict]:
    families = dict(memory.data.get("families", {}) or {})
    symbols = dict(memory.data.get("symbols", {}) or {})
    sentence_traces = _group_by_family(dict(memory.data.get("sentence_traces", {}) or {}))
    reflection_seeds = _group_by_family(dict(memory.data.get("reflection_seeds", {}) or {}))
    reflection_maps = _group_by_family(dict(memory.data.get("reflection_maps", {}) or {}))
    contact_lagen = _contact_lagen_by_family(dict(memory.data.get("contact_lagen", {}) or {}))

    family_names = set(families.keys())
    family_names.update(sentence_traces.keys())
    family_names.update(reflection_seeds.keys())
    family_names.update(reflection_maps.keys())
    family_names.update(contact_lagen.keys())
    if selected_families:
        family_names &= selected_families

    symbol_counts: dict[str, int] = {}
    for symbol_record in symbols.values():
        family = str(dict(symbol_record or {}).get("syntax_family", "") or "")
        if family:
            symbol_counts[family] = symbol_counts.get(family, 0) + 1

    rows = []
    for family in sorted(family_names):
        record = dict(families.get(family, {}) or {})
        row = {
            "family": family,
            "family_count": _safe_int(record.get("count", 0)),
            "symbol_count": symbol_counts.get(family, 0),
        }
        for action in ACTION_NAMES:
            row.update(_action_summary(record, action))
            row.update(_observation_summary(record, action))

        seeds = reflection_seeds.get(family, [])
        maps = reflection_maps.get(family, [])
        sentences = sentence_traces.get(family, [])
        contacts = contact_lagen.get(family, [])
        row.update(
            {
                "sentence_trace_count": len(sentences),
                "sentence_trace_reward_sum": round(
                    sum(_safe_float(item.get("reward_sum", 0.0)) for item in sentences),
                    6,
                ),
                "sentence_contact_states": _state_counts(sentences, "episode_contact_state"),
                "contact_lage_count": len(contacts),
                "contact_lage_states": _state_counts(contacts, "contact_lage_state"),
                "reflection_seed_count": len(seeds),
                "reflection_seed_states": _state_counts(seeds, "reflection_state"),
                "reflection_seed_followup_reward": round(
                    sum(_safe_float(item.get("followup_executed_reward", 0.0)) for item in seeds),
                    6,
                ),
                "reflection_map_count": len(maps),
                "reflection_map_states": _state_counts(maps, "reflection_map_state"),
                "reflection_map_reward_sum": round(
                    sum(_safe_float(item.get("reward_sum", 0.0)) for item in maps),
                    6,
                ),
                "reflection_map_sources": "|".join(
                    sorted({str(item.get("source_probe", "") or "-") for item in maps})
                )
                if maps
                else "-",
            }
        )
        row["strongest_action_trace"] = _strongest_action_trace(row)
        row["passive_sentence"] = _passive_sentence(row)
        rows.append(row)

    rows.sort(
        key=lambda item: (
            -_safe_int(item.get("reflection_map_count", 0)),
            -_safe_int(item.get("reflection_seed_count", 0)),
            -_safe_int(item.get("family_count", 0)),
            str(item.get("family", "")),
        )
    )
    return rows


def write_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "dio_mini_family_file.csv"
    json_path = output_dir / "dio_mini_family_file.json"
    md_path = output_dir / "dio_mini_family_file.md"

    fields = [
        "family",
        "family_count",
        "symbol_count",
        "strongest_action_trace",
        "wait_count",
        "wait_reward_sum",
        "wait_trust",
        "wait_caution",
        "long_count",
        "long_reward_sum",
        "long_trust",
        "long_caution",
        "short_count",
        "short_reward_sum",
        "short_trust",
        "short_caution",
        "observed_wait_count",
        "observed_wait_recognition_avg",
        "observed_wait_reward_sum",
        "observed_long_count",
        "observed_long_recognition_avg",
        "observed_long_reward_sum",
        "observed_short_count",
        "observed_short_recognition_avg",
        "observed_short_reward_sum",
        "sentence_trace_count",
        "sentence_trace_reward_sum",
        "sentence_contact_states",
        "contact_lage_count",
        "contact_lage_states",
        "reflection_seed_count",
        "reflection_seed_states",
        "reflection_seed_followup_reward",
        "reflection_map_count",
        "reflection_map_states",
        "reflection_map_reward_sum",
        "reflection_map_sources",
        "passive_sentence",
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Familienakte", ""]
    if not rows:
        lines.append("Keine Familien gefunden.")
    for row in rows:
        lines.extend(
            [
                f"## {row['family']}",
                f"- passive_sentence: {row['passive_sentence']}",
                f"- family_count / symbol_count: {row['family_count']} / {row['symbol_count']}",
                f"- strongest_action_trace: {row['strongest_action_trace']}",
                (
                    "- action_memory: "
                    f"WAIT {row['wait_count']} ({float(row['wait_reward_sum']):.6f}), "
                    f"LONG {row['long_count']} ({float(row['long_reward_sum']):.6f}), "
                    f"SHORT {row['short_count']} ({float(row['short_reward_sum']):.6f})"
                ),
                (
                    "- observation_memory: "
                    f"WAIT {row['observed_wait_count']} ({float(row['observed_wait_reward_sum']):.6f}), "
                    f"LONG {row['observed_long_count']} ({float(row['observed_long_reward_sum']):.6f}), "
                    f"SHORT {row['observed_short_count']} ({float(row['observed_short_reward_sum']):.6f})"
                ),
                f"- sentence_traces: {row['sentence_trace_count']} / {row['sentence_contact_states']}",
                f"- contact_lagen: {row['contact_lage_count']} / {row['contact_lage_states']}",
                f"- reflection_seeds: {row['reflection_seed_count']} / {row['reflection_seed_states']}",
                (
                    f"- reflection_maps: {row['reflection_map_count']} / "
                    f"{row['reflection_map_states']} / sources={row['reflection_map_sources']}"
                ),
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a passive DIO_MINI family file")
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
    for row in rows[:12]:
        print(
            f"{row['family']} strongest_trace={row['strongest_action_trace']} "
            f"maps={row['reflection_map_states']} seeds={row['reflection_seed_states']}"
        )


if __name__ == "__main__":
    main()
