"""Store passive Mini-DIO reflection context observations separately.

This memory is diagnostic only. It stores which world/form families repeatedly
produce carried or cautious inner context. Mini-DIO does not read this file for
action, gates, or motorics.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import time
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


def _clip(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, float(value)))


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


def _atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f"{path.name}.tmp.{os.getpid()}.{int(time.time() * 1000)}")
    temp_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temp_path, path)


def _hash_base36(text: str) -> str:
    value = 2166136261
    for char in text:
        value ^= ord(char)
        value = (value * 16777619) & 0xFFFFFFFF
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    if value == 0:
        return "0"
    chars = []
    while value:
        value, rest = divmod(value, 36)
        chars.append(alphabet[rest])
    return "".join(reversed(chars))


def make_reflection_context_symbol(world_label: str, family: str, state: str, carry: float, strain: float) -> str:
    """Create a compact DIO-owned symbol for a passive reflection context."""

    carry_band = int(_clip(carry) * 9)
    strain_band = int(_clip(strain) * 9)
    raw = f"{world_label}|{family}|{state}|c{carry_band}|s{strain_band}"
    return f"dio_rctx_{_hash_base36(raw)[:10]}"


def _empty_stats() -> dict:
    return {
        "episodes": 0,
        "trades": 0,
        "tp": 0,
        "sl": 0,
        "reward_sum": 0.0,
        "carried_count": 0,
        "cautious_count": 0,
        "unloaded_count": 0,
        "sum_reflection_carry": 0.0,
        "sum_reflection_strain": 0.0,
        "sum_reflection_alignment": 0.0,
        "sum_reflection_world_support": 0.0,
        "sum_reflection_current_support": 0.0,
        "sum_trade_readiness": 0.0,
        "sum_neuro_balance": 0.0,
        "sum_observation_learning_pressure": 0.0,
        "max_reflection_carry": 0.0,
        "max_reflection_strain": 0.0,
        "last_context_state": "-",
        "last_symbol": "-",
    }


def _add_row(stats: dict, row: dict) -> None:
    state = str(row.get("reflection_context_state", "") or "-")
    carry = _safe_float(row.get("reflection_context_carry"))
    strain = _safe_float(row.get("reflection_context_strain"))
    alignment = _safe_float(row.get("reflection_context_alignment"))
    reward = _safe_float(row.get("event_reward") or row.get("reward"))
    outcome = str(row.get("outcome_event", "") or "")
    action = str(row.get("action", "") or "")

    stats["episodes"] += 1
    stats["reward_sum"] += reward
    if action in ("LONG", "SHORT") or outcome in ("TP", "SL"):
        stats["trades"] += 1
    if outcome == "TP":
        stats["tp"] += 1
    elif outcome == "SL":
        stats["sl"] += 1

    if state == "reflection_context_carried":
        stats["carried_count"] += 1
    elif state == "reflection_context_cautious":
        stats["cautious_count"] += 1
    elif state == "reflection_context_unloaded":
        stats["unloaded_count"] += 1

    stats["sum_reflection_carry"] += carry
    stats["sum_reflection_strain"] += strain
    stats["sum_reflection_alignment"] += alignment
    stats["sum_reflection_world_support"] += _safe_float(row.get("reflection_world_support"))
    stats["sum_reflection_current_support"] += _safe_float(row.get("reflection_current_support"))
    stats["sum_trade_readiness"] += _safe_float(row.get("trade_readiness"))
    stats["sum_neuro_balance"] += _safe_float(row.get("mini_neuro_balance"))
    stats["sum_observation_learning_pressure"] += _safe_float(row.get("observation_learning_pressure"))
    stats["max_reflection_carry"] = max(float(stats["max_reflection_carry"]), carry)
    stats["max_reflection_strain"] = max(float(stats["max_reflection_strain"]), strain)
    stats["last_context_state"] = state
    stats["last_symbol"] = str(row.get("symbol", "") or "-")


def _finalize_stats(stats: dict, world_label: str, family: str = "") -> dict:
    episodes = max(1, int(stats.get("episodes", 0) or 0))
    avg_carry = float(stats["sum_reflection_carry"]) / episodes
    avg_strain = float(stats["sum_reflection_strain"]) / episodes
    state = str(stats.get("last_context_state", "-") or "-")
    symbol = make_reflection_context_symbol(world_label, family or "world", state, avg_carry, avg_strain)
    return {
        "reflection_context_symbol": symbol,
        "world_label": world_label,
        "symbol_family": family,
        "episodes": int(stats["episodes"]),
        "trades": int(stats["trades"]),
        "tp": int(stats["tp"]),
        "sl": int(stats["sl"]),
        "reward_sum": round(float(stats["reward_sum"]), 9),
        "carried_count": int(stats["carried_count"]),
        "cautious_count": int(stats["cautious_count"]),
        "unloaded_count": int(stats["unloaded_count"]),
        "avg_reflection_carry": round(avg_carry, 9),
        "avg_reflection_strain": round(avg_strain, 9),
        "avg_reflection_alignment": round(float(stats["sum_reflection_alignment"]) / episodes, 9),
        "avg_reflection_world_support": round(float(stats["sum_reflection_world_support"]) / episodes, 9),
        "avg_reflection_current_support": round(float(stats["sum_reflection_current_support"]) / episodes, 9),
        "avg_trade_readiness": round(float(stats["sum_trade_readiness"]) / episodes, 9),
        "avg_mini_neuro_balance": round(float(stats["sum_neuro_balance"]) / episodes, 9),
        "avg_observation_learning_pressure": round(float(stats["sum_observation_learning_pressure"]) / episodes, 9),
        "max_reflection_carry": round(float(stats["max_reflection_carry"]), 9),
        "max_reflection_strain": round(float(stats["max_reflection_strain"]), 9),
        "last_context_state": state,
        "last_symbol": str(stats.get("last_symbol", "-") or "-"),
        "passive_only": True,
        "read_by_mini_dio": False,
        "influences_action": False,
        "is_gate": False,
        "is_motoric": False,
    }


def parse_world_args(items: list[str]) -> list[tuple[str, Path]]:
    worlds: list[tuple[str, Path]] = []
    for item in items:
        if "=" not in item:
            raise ValueError(f"World argument must be label=path: {item}")
        label, raw_path = item.split("=", 1)
        label = label.strip()
        if not label:
            raise ValueError(f"World label is empty: {item}")
        worlds.append((label, Path(raw_path.strip())))
    return worlds


def find_episode_files(root: Path) -> list[Path]:
    if root.is_file() and root.name == "episodes.csv":
        return [root]
    return sorted(root.rglob("episodes.csv"))


def build_memory(worlds: list[tuple[str, Path]]) -> dict:
    memory = {
        "schema": "dio_mini_passive_reflection_context_memory.v1",
        "created_utc_ms": int(time.time() * 1000),
        "boundary": {
            "passive_only": True,
            "read_by_mini_dio": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
            "stores_inner_perception": True,
            "stores_real_outcome_context": True,
        },
        "source_runs": [],
        "summary": {},
        "worlds": {},
        "families": {},
    }

    global_stats = _empty_stats()
    for world_label, root in worlds:
        world_stats = _empty_stats()
        family_stats: dict[str, dict] = {}
        files = find_episode_files(root)
        memory["source_runs"].append(
            {
                "world_label": world_label,
                "root": str(root),
                "episode_files": len(files),
            }
        )
        for path in files:
            for row in _read_csv(path):
                family = str(row.get("symbol_family", "") or "-")
                _add_row(global_stats, row)
                _add_row(world_stats, row)
                current = family_stats.setdefault(family, _empty_stats())
                _add_row(current, row)

        finalized_families = {
            family: _finalize_stats(stats, world_label, family)
            for family, stats in sorted(family_stats.items())
        }
        memory["worlds"][world_label] = {
            "summary": _finalize_stats(world_stats, world_label, "world"),
            "families": finalized_families,
        }
        for family, item in finalized_families.items():
            memory["families"][f"{world_label}|{family}"] = item

    memory["summary"] = _finalize_stats(global_stats, "all_worlds", "summary")
    memory["summary"]["world_count"] = len(worlds)
    memory["summary"]["family_count"] = len(memory["families"])
    return memory


def write_outputs(memory: dict, memory_path: Path, output_dir: Path | None) -> None:
    _atomic_write_json(memory_path, memory)
    if output_dir is None:
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    family_rows = list(memory.get("families", {}).values())
    family_rows.sort(
        key=lambda row: (
            str(row.get("world_label", "")),
            -_safe_float(row.get("avg_reflection_carry")),
            _safe_float(row.get("avg_reflection_strain")),
            str(row.get("symbol_family", "")),
        )
    )
    _write_csv(
        output_dir / "dio_mini_passive_reflection_context_memory_families.csv",
        family_rows,
        [
            "world_label",
            "symbol_family",
            "reflection_context_symbol",
            "episodes",
            "trades",
            "tp",
            "sl",
            "reward_sum",
            "carried_count",
            "cautious_count",
            "avg_reflection_carry",
            "avg_reflection_strain",
            "avg_reflection_alignment",
        ],
    )

    lines = [
        "# Mini-DIO Passive Reflection Context Memory",
        "",
        f"- memory: `{memory_path}`",
        "- boundary: passive only; not read by Mini-DIO; no action; no gate",
        "",
        "## Summary",
    ]
    for key, value in memory.get("summary", {}).items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Worlds"])
    for world, payload in sorted(memory.get("worlds", {}).items()):
        summary = dict(payload.get("summary", {}) or {})
        lines.append(
            f"- {world}: episodes={summary.get('episodes', 0)} "
            f"trades={summary.get('trades', 0)} tp={summary.get('tp', 0)} sl={summary.get('sl', 0)} "
            f"avg_carry={summary.get('avg_reflection_carry', 0.0)} "
            f"avg_strain={summary.get('avg_reflection_strain', 0.0)}"
        )
    lines.extend(["", "## Grenze"])
    lines.append("- Reflexion merkt Innenkontext, sie entscheidet nicht.")
    lines.append("- Handlung bleibt an reale Kopplung und Konsequenz gebunden.")
    (output_dir / "dio_mini_passive_reflection_context_memory.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )
    (output_dir / "dio_mini_passive_reflection_context_memory.txt").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--world", action="append", default=[], help="World debug root as label=path")
    parser.add_argument(
        "--memory",
        type=Path,
        default=Path("bot_memory/dio_mini_passive_reflection_context_memory.json"),
    )
    parser.add_argument("--output-dir", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    worlds = parse_world_args(args.world)
    memory = build_memory(worlds)
    write_outputs(memory, args.memory, args.output_dir)
    summary = memory["summary"]
    print(
        "passive_reflection_context_memory "
        f"worlds={summary['world_count']} "
        f"families={summary['family_count']} "
        f"episodes={summary['episodes']} "
        f"trades={summary['trades']} "
        f"tp={summary['tp']} "
        f"sl={summary['sl']} "
        f"avg_carry={summary['avg_reflection_carry']} "
        f"avg_strain={summary['avg_reflection_strain']}"
    )


if __name__ == "__main__":
    main()
