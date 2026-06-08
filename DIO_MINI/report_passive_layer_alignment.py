"""Compare Mini-DIO trading memory, passive world carrying, and reflection memory.

The report is passive. It checks whether the same DIO form families are carried
by real outcome memory, passive world carrying, and passive inner reflection.
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


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


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


def _best_action_from_family(family_payload: dict) -> dict:
    best = {
        "best_action": "-",
        "best_action_count": 0,
        "best_action_reward_sum": 0.0,
        "best_action_trust": 0.0,
        "best_action_caution": 0.0,
    }
    actions = dict(family_payload.get("actions", {}) or {})
    for action in ("LONG", "SHORT", "WAIT"):
        payload = dict(actions.get(action, {}) or {})
        candidate = {
            "best_action": action,
            "best_action_count": _safe_int(payload.get("count")),
            "best_action_reward_sum": _safe_float(payload.get("reward_sum")),
            "best_action_trust": _safe_float(payload.get("trust")),
            "best_action_caution": _safe_float(payload.get("caution")),
        }
        if (
            candidate["best_action_reward_sum"],
            candidate["best_action_trust"],
            candidate["best_action_count"],
        ) > (
            best["best_action_reward_sum"],
            best["best_action_trust"],
            best["best_action_count"],
        ):
            best = candidate
    return best


def _observation_direction_from_family(family_payload: dict) -> dict:
    best = {
        "best_observation_action": "-",
        "best_observation_count": 0,
        "best_observation_reward_sum": 0.0,
        "best_observation_recognition_avg": 0.0,
    }
    observations = dict(family_payload.get("observations", {}) or {})
    for action in ("LONG", "SHORT", "WAIT"):
        payload = dict(observations.get(action, {}) or {})
        count = _safe_int(payload.get("count"))
        reward_sum = _safe_float(payload.get("reward_sum"))
        recognition_avg = _safe_float(payload.get("recognition_sum")) / max(1, count)
        candidate = {
            "best_observation_action": action,
            "best_observation_count": count,
            "best_observation_reward_sum": reward_sum,
            "best_observation_recognition_avg": recognition_avg,
        }
        if (
            candidate["best_observation_reward_sum"],
            candidate["best_observation_recognition_avg"],
            candidate["best_observation_count"],
        ) > (
            best["best_observation_reward_sum"],
            best["best_observation_recognition_avg"],
            best["best_observation_count"],
        ):
            best = candidate
    return best


def _world_family_map(world_memory: dict) -> dict[tuple[str, str], dict]:
    mapped: dict[tuple[str, str], dict] = {}
    for world, payload in dict(world_memory.get("worlds", {}) or {}).items():
        last = dict(payload.get("last", {}) or {})
        for item in list(last.get("strongest_families", []) or []):
            row = dict(item)
            family = str(row.get("target_family", "") or "")
            if family:
                mapped[(str(world), family)] = row
    return mapped


def _alignment_state(row: dict) -> str:
    trade_reward = _safe_float(row.get("best_action_reward_sum"))
    obs_reward = _safe_float(row.get("best_observation_reward_sum"))
    reflection_tp = _safe_int(row.get("reflection_tp"))
    reflection_sl = _safe_int(row.get("reflection_sl"))
    reflection_carry = _safe_float(row.get("avg_reflection_carry"))
    reflection_strain = _safe_float(row.get("avg_reflection_strain"))
    world_carry = _safe_float(row.get("world_carry"))
    world_cos = _safe_float(row.get("world_carried_cos"))

    if reflection_sl > 0:
        return "alignment_conflict_outcome"
    if reflection_tp > 0 and trade_reward > 0.0 and world_carry > 0.0 and reflection_carry > reflection_strain:
        return "alignment_carried_three_layer"
    if reflection_tp > 0 and obs_reward > 0.0 and reflection_carry > reflection_strain:
        return "alignment_inner_outcome_carried"
    if reflection_tp <= 0 and reflection_carry > reflection_strain and world_carry > 0.0:
        return "alignment_carried_unconfirmed"
    if reflection_tp <= 0 and reflection_carry > reflection_strain:
        return "alignment_inner_carried_unconfirmed"
    if reflection_carry <= reflection_strain and world_cos <= 0.0:
        return "alignment_cautious"
    return "alignment_open"


def build_alignment_report(trading_memory: dict, world_memory: dict, reflection_memory: dict) -> dict:
    trading_families = dict(trading_memory.get("families", {}) or {})
    world_families = _world_family_map(world_memory)
    rows: list[dict] = []
    counts: dict[str, int] = {}

    for key, reflection in sorted(dict(reflection_memory.get("families", {}) or {}).items()):
        reflection = dict(reflection or {})
        world = str(reflection.get("world_label", "") or "-")
        family = str(reflection.get("symbol_family", "") or "-")
        trading = dict(trading_families.get(family, {}) or {})
        world_row = dict(world_families.get((world, family), {}) or {})
        row = {
            "world_label": world,
            "symbol_family": family,
            "reflection_context_symbol": str(reflection.get("reflection_context_symbol", "") or ""),
            "reflection_episodes": _safe_int(reflection.get("episodes")),
            "reflection_trades": _safe_int(reflection.get("trades")),
            "reflection_tp": _safe_int(reflection.get("tp")),
            "reflection_sl": _safe_int(reflection.get("sl")),
            "reflection_reward_sum": round(_safe_float(reflection.get("reward_sum")), 9),
            "reflection_carried_count": _safe_int(reflection.get("carried_count")),
            "reflection_cautious_count": _safe_int(reflection.get("cautious_count")),
            "avg_reflection_carry": round(_safe_float(reflection.get("avg_reflection_carry")), 9),
            "avg_reflection_strain": round(_safe_float(reflection.get("avg_reflection_strain")), 9),
            "avg_reflection_alignment": round(_safe_float(reflection.get("avg_reflection_alignment")), 9),
            "world_carry": round(_safe_float(world_row.get("carry")), 9),
            "world_carried_cos": round(_safe_float(world_row.get("carried_cos")), 9),
            "world_readiness": round(_safe_float(world_row.get("readiness")), 9),
            "world_carried_source": str(world_row.get("carried_source", "") or ""),
            "trading_family_count": _safe_int(trading.get("count")),
        }
        row.update(_best_action_from_family(trading))
        row.update(_observation_direction_from_family(trading))
        row["alignment_state"] = _alignment_state(row)
        counts[row["alignment_state"]] = counts.get(row["alignment_state"], 0) + 1
        rows.append(row)

    rows.sort(
        key=lambda row: (
            str(row.get("world_label", "")),
            str(row.get("alignment_state", "")),
            -_safe_float(row.get("reflection_reward_sum")),
            -_safe_float(row.get("avg_reflection_carry")),
            str(row.get("symbol_family", "")),
        )
    )
    return {
        "schema": "dio_mini_passive_layer_alignment_report.v1",
        "summary": {
            "families": len(rows),
            "alignment_counts": dict(sorted(counts.items())),
            "reflection_tp": sum(_safe_int(row.get("reflection_tp")) for row in rows),
            "reflection_sl": sum(_safe_int(row.get("reflection_sl")) for row in rows),
            "reflection_trades": sum(_safe_int(row.get("reflection_trades")) for row in rows),
        },
        "rows": rows,
    }


def write_report(report: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "passive_layer_alignment_report.json"
    csv_path = output_dir / "passive_layer_alignment_report.csv"
    md_path = output_dir / "passive_layer_alignment_report.md"
    inner_map_path = output_dir / "passive_inner_state_map.txt"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    _write_csv(
        csv_path,
        list(report.get("rows", []) or []),
        [
            "world_label",
            "symbol_family",
            "alignment_state",
            "reflection_trades",
            "reflection_tp",
            "reflection_sl",
            "reflection_reward_sum",
            "avg_reflection_carry",
            "avg_reflection_strain",
            "world_carry",
            "world_carried_cos",
            "best_action",
            "best_action_reward_sum",
            "best_action_trust",
            "best_observation_action",
            "best_observation_reward_sum",
        ],
    )

    lines = [
        "# Mini-DIO Passive Layer Alignment",
        "",
        "Grenze: passiver Vergleich, keine Handlung, kein Gate.",
        "",
        "## Summary",
    ]
    summary = dict(report.get("summary", {}) or {})
    for key, value in summary.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Top Rows"])
    for row in list(report.get("rows", []) or [])[:24]:
        lines.append(
            f"- {row['world_label']} {row['symbol_family']} "
            f"{row['alignment_state']} "
            f"tp={row['reflection_tp']} sl={row['reflection_sl']} "
            f"r_carry={row['avg_reflection_carry']} r_strain={row['avg_reflection_strain']} "
            f"world_carry={row['world_carry']} action={row['best_action']} "
            f"obs={row['best_observation_action']}"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    inner_lines = [
        "Mini-DIO passive Innenzustands-Landkarte",
        "",
        "Grenze: Beschreibung, keine Handlung, kein Gate.",
        "",
    ]
    for row in list(report.get("rows", []) or []):
        state = str(row.get("alignment_state", "") or "")
        world = str(row.get("world_label", "") or "")
        family = str(row.get("symbol_family", "") or "")
        if state == "alignment_carried_three_layer":
            meaning = "reale Erfahrung, Weltnaehe und Innenlage tragen gemeinsam"
        elif state == "alignment_inner_outcome_carried":
            meaning = "Innenlage und reales Ergebnis tragen, Weltnaehe bleibt noch zu pruefen"
        elif state == "alignment_carried_unconfirmed":
            meaning = "Weltnaehe und Innenlage tragen, aber reale Konsequenz fehlt noch"
        elif state == "alignment_inner_carried_unconfirmed":
            meaning = "Innenlage traegt, aber Weltnaehe oder reale Konsequenz fehlen noch"
        elif state == "alignment_cautious":
            meaning = "Innenlage bleibt vorsichtig oder belastet; keine tragende Kopplung"
        elif state == "alignment_conflict_outcome":
            meaning = "Konsequenz widerspricht der getragenen Deutung"
        else:
            meaning = "offene Lage; noch keine saubere dreischichtige Uebereinstimmung"
        inner_lines.append(
            f"{world}/{family}: {state}; {meaning}; "
            f"tp={row.get('reflection_tp', 0)} sl={row.get('reflection_sl', 0)} "
            f"carry={row.get('avg_reflection_carry', 0.0)} "
            f"strain={row.get('avg_reflection_strain', 0.0)}"
        )
    inner_map_path.write_text("\n".join(inner_lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trading-memory", type=Path, required=True)
    parser.add_argument("--world-memory", type=Path, required=True)
    parser.add_argument("--reflection-memory", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = build_alignment_report(
        _load_json(args.trading_memory),
        _load_json(args.world_memory),
        _load_json(args.reflection_memory),
    )
    write_report(report, args.output_dir)
    print(json.dumps(report["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
