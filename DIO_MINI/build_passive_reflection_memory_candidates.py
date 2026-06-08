"""Build passive reflection-memory candidates from maturity-pressure maps.

Candidates are not runtime memory and not action permissions. They only mark
families whose passive inner pressure repeats across more than one debug world.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(float(value or default))
    except Exception:
        return default


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value or default)
    except Exception:
        return default
    if result != result:
        return default
    return result


def read_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def candidate_state(pressure: str, debug_root_count: int) -> str:
    if pressure == "passive_unloaded_no_inner_awareness":
        return "not_candidate_unloaded_no_inner_awareness"
    if debug_root_count <= 1:
        return "not_candidate_single_world_only"
    if pressure == "passive_overcautious_carried_pressure":
        return "candidate_stable_overcautious_reflection"
    if pressure == "passive_cautious_potential_pressure":
        return "candidate_stable_cautious_reflection"
    if pressure == "passive_action_trust_seed_pressure":
        return "candidate_stable_trust_seed_reflection"
    if pressure == "passive_open_potential_pressure":
        return "candidate_stable_open_potential_reflection"
    if pressure == "passive_context_dependent_withholding_pressure":
        return "candidate_context_dependent_reflection"
    if pressure == "passive_action_withholding_split_pressure":
        return "candidate_action_withholding_split_reflection"
    return "not_candidate_unclassified"


def build_candidates(pressure_map_path: Path) -> tuple[list[dict], list[dict]]:
    entries: list[dict] = []
    groups: dict[str, dict] = {}

    for row in read_rows(pressure_map_path):
        pressure = str(row.get("passive_maturity_pressure_state", "") or "")
        debug_root_count = _safe_int(row.get("debug_root_count"))
        state = candidate_state(pressure, debug_root_count)
        family = str(row.get("symbol_family", "") or "-")
        item = {
            "symbol_family": family,
            "passive_reflection_candidate_state": state,
            "source_pressure_state": pressure,
            "debug_root_count": debug_root_count,
            "debug_roots": str(row.get("debug_roots", "") or ""),
            "observation_count": _safe_int(row.get("observation_count")),
            "wait_count": _safe_int(row.get("wait_count")),
            "withheld_best_trade_count": _safe_int(row.get("withheld_best_trade_count")),
            "avg_best_reward": round(_safe_float(row.get("avg_best_reward")), 6),
            "avg_reward": round(_safe_float(row.get("avg_reward")), 6),
            "best_actions": str(row.get("best_actions", "") or ""),
            "actions": str(row.get("actions", "") or ""),
            "passive_only": True,
            "writes_runtime_memory": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
            "is_entry_signal": False,
            "candidate_only": state.startswith("candidate_"),
            "human_reading": _human_reading(state),
        }
        entries.append(item)

        group = groups.setdefault(
            state,
            {
                "passive_reflection_candidate_state": state,
                "family_count": 0,
                "observation_count": 0,
                "wait_count": 0,
                "withheld_best_trade_count": 0,
                "avg_best_reward_sum": 0.0,
                "candidate_only": state.startswith("candidate_"),
            },
        )
        group["family_count"] += 1
        group["observation_count"] += item["observation_count"]
        group["wait_count"] += item["wait_count"]
        group["withheld_best_trade_count"] += item["withheld_best_trade_count"]
        group["avg_best_reward_sum"] += item["avg_best_reward"]

    summary: list[dict] = []
    for group in groups.values():
        family_count = int(group["family_count"])
        summary.append(
            {
                "passive_reflection_candidate_state": group["passive_reflection_candidate_state"],
                "family_count": family_count,
                "observation_count": int(group["observation_count"]),
                "wait_count": int(group["wait_count"]),
                "withheld_best_trade_count": int(group["withheld_best_trade_count"]),
                "avg_family_best_reward": round(float(group["avg_best_reward_sum"]) / family_count, 6)
                if family_count
                else 0.0,
                "candidate_only": bool(group["candidate_only"]),
                "passive_only": True,
                "influences_action": False,
            }
        )

    entries.sort(
        key=lambda item: (
            0 if item["candidate_only"] else 1,
            -int(item["debug_root_count"]),
            -int(item["withheld_best_trade_count"]),
            str(item["symbol_family"]),
        )
    )
    summary.sort(key=lambda item: (0 if item["candidate_only"] else 1, -int(item["family_count"])))
    return entries, summary


def _human_reading(state: str) -> str:
    if state == "candidate_stable_overcautious_reflection":
        return "Mehrweltliche Spur: getragen wirkende Zurueckhaltung als Reflexionskandidat."
    if state == "candidate_stable_cautious_reflection":
        return "Mehrweltliche Spur: vorsichtige Schutzlage als Reflexionskandidat."
    if state == "candidate_stable_trust_seed_reflection":
        return "Mehrweltliche Spur: passive Vertrauenssaat als Reflexionskandidat."
    if state == "candidate_stable_open_potential_reflection":
        return "Mehrweltliche Spur: offene potenzielle Tragfaehigkeit als Reflexionskandidat."
    if state == "candidate_context_dependent_reflection":
        return "Mehrweltliche Spur: kontextabhaengige Zurueckhaltung als Reflexionskandidat."
    if state == "candidate_action_withholding_split_reflection":
        return "Mehrweltliche Spur: Handlung/Zurueckhaltung gespalten als Reflexionskandidat."
    if state == "not_candidate_unloaded_no_inner_awareness":
        return "Keine geladene Innenlage; keine Kandidatur."
    if state == "not_candidate_single_world_only":
        return "Nur eine Welt gelesen; noch keine mehrweltliche Kandidatur."
    return "Nicht als Reflexionskandidat verwendbar."


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(entries: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    entries_path = output_dir / "dio_mini_passive_reflection_memory_candidates.csv"
    summary_path = output_dir / "dio_mini_passive_reflection_memory_candidates_summary.csv"
    json_path = output_dir / "dio_mini_passive_reflection_memory_candidates.json"
    md_path = output_dir / "dio_mini_passive_reflection_memory_candidates.md"

    _write_csv(entries_path, entries, ["symbol_family", "passive_reflection_candidate_state"])
    _write_csv(summary_path, summary, ["passive_reflection_candidate_state", "family_count"])
    json_path.write_text(
        json.dumps(
            {
                "boundary": {
                    "passive_only": True,
                    "writes_runtime_memory": False,
                    "influences_action": False,
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
        "# DIO Mini Passive Reflection Memory Candidates",
        "",
        "## Grenze",
        "- Kandidat, kein Runtime-Speicher",
        "- keine Entry-Wirkung",
        "- keine Gate-Wirkung",
        "- keine Motorik",
        "",
        "## Summary",
    ]
    if not summary:
        lines.append("- keine Kandidaten")
    else:
        for row in summary:
            lines.append(
                f"- {row['passive_reflection_candidate_state']}: "
                f"families={row['family_count']} observations={row['observation_count']} "
                f"wait={row['wait_count']} withheld_best_trade={row['withheld_best_trade_count']} "
                f"candidate={row['candidate_only']}"
            )
    lines.extend(["", "## Staerkste Kandidaten"])
    for row in [item for item in entries if item["candidate_only"]][:20]:
        lines.append(
            f"- {row['symbol_family']}: {row['passive_reflection_candidate_state']} "
            f"worlds={row['debug_root_count']} obs={row['observation_count']} "
            f"withheld_best_trade={row['withheld_best_trade_count']} best_actions={row['best_actions']}"
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive reflection-memory candidates")
    parser.add_argument("--pressure-map", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    entries, summary = build_candidates(Path(args.pressure_map))
    write_outputs(entries, summary, Path(args.output_dir))
    print(f"entries={len(entries)} summary_rows={len(summary)}")


if __name__ == "__main__":
    main()
