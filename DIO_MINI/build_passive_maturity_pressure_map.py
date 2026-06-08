"""Build a passive maturity-pressure map from Mini-DIO inner-awareness traces.

The map is diagnostic only. It names repeated inner pressure states but does
not create entries, gates, motoric rules, or runtime memory effects.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


STATE_TO_PRESSURE = {
    "inner_overcautious_carrying_pressure": "passive_overcautious_carried_pressure",
    "inner_action_withholding_split": "passive_action_withholding_split_pressure",
    "inner_context_dependent_withholding": "passive_context_dependent_withholding_pressure",
    "inner_cautious_potential": "passive_cautious_potential_pressure",
    "inner_open_potential": "passive_open_potential_pressure",
    "inner_action_trust_seed": "passive_action_trust_seed_pressure",
    "unloaded": "passive_unloaded_no_inner_awareness",
}


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value or default)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(float(value or default))
    except Exception:
        return default


def read_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def build_map(family_summary_path: Path) -> tuple[list[dict], list[dict]]:
    entries: list[dict] = []
    state_counts: dict[str, dict] = {}

    for row in read_rows(family_summary_path):
        state = str(row.get("passive_inner_awareness_state", "") or "unloaded")
        pressure = STATE_TO_PRESSURE.get(state, "passive_unclassified_pressure")
        family = str(row.get("symbol_family", "") or "-")
        count = _safe_int(row.get("count"))
        wait_count = _safe_int(row.get("wait_count"))
        trade_count = _safe_int(row.get("trade_count"))
        withheld_best_trade_count = _safe_int(row.get("withheld_best_trade_count"))
        avg_best_reward = _safe_float(row.get("avg_best_reward"))
        avg_reward = _safe_float(row.get("avg_reward"))
        debug_roots = str(row.get("debug_roots", "") or "")
        debug_root_count = _safe_int(row.get("debug_root_count"))

        entry = {
            "symbol_family": family,
            "passive_maturity_pressure_state": pressure,
            "source_inner_awareness_state": state,
            "observation_count": count,
            "wait_count": wait_count,
            "trade_count": trade_count,
            "withheld_best_trade_count": withheld_best_trade_count,
            "avg_best_reward": round(avg_best_reward, 6),
            "avg_reward": round(avg_reward, 6),
            "best_actions": str(row.get("best_actions", "") or ""),
            "actions": str(row.get("actions", "") or ""),
            "runs": str(row.get("runs", "") or ""),
            "debug_roots": debug_roots,
            "debug_root_count": debug_root_count,
            "passive_only": True,
            "influences_action": False,
            "writes_runtime_memory": False,
            "is_gate": False,
            "is_motoric": False,
            "is_entry_signal": False,
            "human_reading": _human_reading(pressure),
        }
        entries.append(entry)

        group = state_counts.setdefault(
            pressure,
            {
                "passive_maturity_pressure_state": pressure,
                "source_inner_awareness_states": set(),
                "family_count": 0,
                "observation_count": 0,
                "wait_count": 0,
                "trade_count": 0,
                "withheld_best_trade_count": 0,
                "avg_best_reward_sum": 0.0,
                "debug_roots": set(),
            },
        )
        group["source_inner_awareness_states"].add(state)
        group["family_count"] += 1
        group["observation_count"] += count
        group["wait_count"] += wait_count
        group["trade_count"] += trade_count
        group["withheld_best_trade_count"] += withheld_best_trade_count
        group["avg_best_reward_sum"] += avg_best_reward
        for debug_root in debug_roots.split("|"):
            if debug_root:
                group["debug_roots"].add(debug_root)

    summary: list[dict] = []
    for group in state_counts.values():
        family_count = int(group["family_count"])
        summary.append(
            {
                "passive_maturity_pressure_state": group["passive_maturity_pressure_state"],
                "source_inner_awareness_states": "|".join(sorted(group["source_inner_awareness_states"])),
                "family_count": family_count,
                "observation_count": int(group["observation_count"]),
                "wait_count": int(group["wait_count"]),
                "trade_count": int(group["trade_count"]),
                "withheld_best_trade_count": int(group["withheld_best_trade_count"]),
                "avg_family_best_reward": round(float(group["avg_best_reward_sum"]) / family_count, 6)
                if family_count
                else 0.0,
                "debug_root_count": len(group["debug_roots"]),
                "debug_roots": "|".join(sorted(group["debug_roots"])),
                "passive_only": True,
                "influences_action": False,
            }
        )

    entries.sort(key=lambda item: (-int(item["withheld_best_trade_count"]), str(item["symbol_family"])))
    summary.sort(key=lambda item: (-int(item["family_count"]), str(item["passive_maturity_pressure_state"])))
    return entries, summary


def _human_reading(pressure: str) -> str:
    if pressure == "passive_overcautious_carried_pressure":
        return "Wiederholt getragene Folge, aber passive Zurueckhaltung bleibt hoch."
    if pressure == "passive_action_withholding_split_pressure":
        return "Familie zeigt gespaltene Innenlage zwischen Handlungsspur und Zurueckhaltung."
    if pressure == "passive_context_dependent_withholding_pressure":
        return "Zurueckhaltung wirkt kontextabhaengig, nicht eindeutig unreif oder reif."
    if pressure == "passive_cautious_potential_pressure":
        return "Vorsicht wirkt noch als potenziell reife Schutzlage."
    if pressure == "passive_open_potential_pressure":
        return "Offene Innenlage mit potenzieller Tragfaehigkeit, noch ohne klare Reifung."
    if pressure == "passive_action_trust_seed_pressure":
        return "Passive Vertrauensspur aus frueherer Handlung, noch ohne Motorik."
    if pressure == "passive_unloaded_no_inner_awareness":
        return "Keine passive Innenwahrnehmung fuer diese Familie geladen."
    return "Nicht klassifizierte passive Innenlage."


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(entries: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    entries_path = output_dir / "dio_mini_passive_maturity_pressure_map.csv"
    summary_path = output_dir / "dio_mini_passive_maturity_pressure_summary.csv"
    json_path = output_dir / "dio_mini_passive_maturity_pressure_map.json"
    md_path = output_dir / "dio_mini_passive_maturity_pressure_map.md"

    _write_csv(entries_path, entries, ["symbol_family", "passive_maturity_pressure_state"])
    _write_csv(summary_path, summary, ["passive_maturity_pressure_state", "family_count"])
    json_path.write_text(
        json.dumps(
            {
                "boundary": {
                    "passive_only": True,
                    "influences_action": False,
                    "writes_runtime_memory": False,
                    "is_gate": False,
                    "is_motoric": False,
                    "is_entry_signal": False,
                },
                "entries": entries,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# DIO Mini Passive Maturity Pressure Map",
        "",
        "## Grenze",
        "- passiv",
        "- keine Entry-Wirkung",
        "- keine Gate-Wirkung",
        "- keine Motorik",
        "- keine Runtime-Memory-Wirkung",
        "",
        "## Summary",
    ]
    if not summary:
        lines.append("- keine Eintraege")
    else:
        for row in summary:
            lines.append(
                f"- {row['passive_maturity_pressure_state']}: "
                f"families={row['family_count']} observations={row['observation_count']} "
                f"wait={row['wait_count']} withheld_best_trade={row['withheld_best_trade_count']} "
                f"avg_family_best={row['avg_family_best_reward']}"
            )
    lines.extend(["", "## Staerkste Spuren"])
    for row in entries[:20]:
        lines.append(
            f"- {row['symbol_family']}: {row['passive_maturity_pressure_state']} "
            f"obs={row['observation_count']} wait={row['wait_count']} "
            f"withheld_best_trade={row['withheld_best_trade_count']} "
            f"best_actions={row['best_actions']}"
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive Mini-DIO maturity pressure map")
    parser.add_argument("--family-summary", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    entries, summary = build_map(Path(args.family_summary))
    write_outputs(entries, summary, Path(args.output_dir))
    print(f"entries={len(entries)} summary_rows={len(summary)}")


if __name__ == "__main__":
    main()
