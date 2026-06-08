"""Report passive inner-awareness states from Mini-DIO runtime traces.

This tool is diagnostic only. It reads episodes.csv files and writes reports.
It does not write memory and does not feed back into Mini-DIO runtime.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value or default)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _iter_episode_rows(debug_roots: list[Path]) -> list[dict]:
    rows: list[dict] = []
    for debug_root in debug_roots:
        for path in sorted(debug_root.glob("**/episodes.csv")):
            run_id = path.parent.name.replace("dio_mini_lauf_", "")
            with path.open(newline="", encoding="utf-8") as handle:
                for row in csv.DictReader(handle):
                    item = dict(row)
                    item["run"] = run_id
                    item["debug_root"] = str(debug_root)
                    item["source_file"] = str(path)
                    rows.append(item)
    return rows


def _state_name(row: dict) -> str:
    state = str(row.get("passive_inner_awareness_state", "") or "").strip()
    if not state or state == "-":
        loaded = str(row.get("passive_inner_awareness_loaded", "0") or "0")
        return "unloaded" if loaded in {"0", "0.0", "false", "False", ""} else "unknown"
    return state


def _action_name(value: object) -> str:
    action = str(value or "WAIT").upper()
    if action not in {"WAIT", "LONG", "SHORT"}:
        return "WAIT"
    return action


def _outcome_name(value: object) -> str:
    outcome = str(value or "NO_TRADE").upper()
    return outcome or "NO_TRADE"


def build_rows(debug_roots: list[Path]) -> tuple[list[dict], list[dict], list[dict]]:
    detail: list[dict] = []
    state_groups: dict[str, dict] = {}
    family_groups: dict[tuple[str, str], dict] = {}

    for row in _iter_episode_rows(debug_roots):
        state = _state_name(row)
        family = str(row.get("symbol_family", "") or "-")
        action = _action_name(row.get("action"))
        raw_action = _action_name(row.get("raw_action"))
        best_action = _action_name(row.get("best_action_training"))
        outcome = _outcome_name(row.get("outcome_event"))
        reward = _safe_float(row.get("reward"))
        event_reward = _safe_float(row.get("event_reward"))
        best_reward = _safe_float(row.get("best_reward_training"))
        loaded = str(row.get("passive_inner_awareness_loaded", "0") or "0") not in {"0", "0.0", "false", "False", ""}
        reflection_context = str(row.get("reflection_context_state", "-") or "-")

        trade_action = action in {"LONG", "SHORT"}
        best_trade = best_action in {"LONG", "SHORT"}
        withheld_best_trade = (action == "WAIT" and best_trade)
        acted_against_best = (trade_action and best_trade and action != best_action)
        acted_with_best = (trade_action and action == best_action)

        item = {
            "run": str(row.get("run", "") or ""),
            "tick": str(row.get("tick", "") or ""),
            "timestamp_ms": str(row.get("timestamp_ms", "") or ""),
            "debug_root": str(row.get("debug_root", "") or ""),
            "symbol_family": family,
            "passive_inner_awareness_loaded": 1 if loaded else 0,
            "passive_inner_awareness_state": state,
            "passive_inner_awareness_direction": str(row.get("passive_inner_awareness_direction", "NONE") or "NONE"),
            "passive_inner_awareness_observations": str(row.get("passive_inner_awareness_observations", "0") or "0"),
            "passive_inner_awareness_afterlook": round(_safe_float(row.get("passive_inner_awareness_afterlook")), 6),
            "passive_inner_awareness_carry": round(_safe_float(row.get("passive_inner_awareness_carry")), 6),
            "passive_inner_awareness_world_carry": round(_safe_float(row.get("passive_inner_awareness_world_carry")), 6),
            "action": action,
            "raw_action": raw_action,
            "best_action_training": best_action,
            "outcome_event": outcome,
            "reward": round(reward, 6),
            "event_reward": round(event_reward, 6),
            "best_reward_training": round(best_reward, 6),
            "withheld_best_trade": 1 if withheld_best_trade else 0,
            "acted_with_best": 1 if acted_with_best else 0,
            "acted_against_best": 1 if acted_against_best else 0,
            "reflection_context_state": str(row.get("reflection_context_state", "-") or "-"),
            "reflection_context_carry": round(_safe_float(row.get("reflection_context_carry")), 6),
            "reflection_context_strain": round(_safe_float(row.get("reflection_context_strain")), 6),
            "reflection_context_alignment": round(_safe_float(row.get("reflection_context_alignment")), 6),
            "sehen_form_stability": round(_safe_float(row.get("sehen_form_stability")), 6),
            "hoeren_energy_tone": round(_safe_float(row.get("hoeren_energy_tone")), 6),
            "fuehlen_mcm_coherence": round(_safe_float(row.get("fuehlen_mcm_coherence")), 6),
            "fuehlen_mcm_tension": round(_safe_float(row.get("fuehlen_mcm_tension")), 6),
            "source_file": str(row.get("source_file", "") or ""),
        }
        detail.append(item)

        state_group = state_groups.setdefault(
            state,
            {
                "passive_inner_awareness_state": state,
                "count": 0,
                "loaded_count": 0,
                "wait_count": 0,
                "long_count": 0,
                "short_count": 0,
                "tp_count": 0,
                "sl_count": 0,
                "no_trade_count": 0,
                "withheld_best_trade_count": 0,
                "acted_with_best_count": 0,
                "acted_against_best_count": 0,
                "reflection_context_carried_count": 0,
                "reflection_context_cautious_count": 0,
                "reflection_context_unloaded_count": 0,
                "reward_sum": 0.0,
                "best_reward_sum": 0.0,
                "afterlook_sum": 0.0,
                "carry_sum": 0.0,
                "world_carry_sum": 0.0,
                "families": set(),
                "runs": set(),
                "debug_roots": set(),
            },
        )
        state_group["count"] += 1
        state_group["loaded_count"] += 1 if loaded else 0
        state_group["wait_count"] += 1 if action == "WAIT" else 0
        state_group["long_count"] += 1 if action == "LONG" else 0
        state_group["short_count"] += 1 if action == "SHORT" else 0
        state_group["tp_count"] += 1 if outcome == "TP" else 0
        state_group["sl_count"] += 1 if outcome == "SL" else 0
        state_group["no_trade_count"] += 1 if outcome == "NO_TRADE" else 0
        state_group["withheld_best_trade_count"] += 1 if withheld_best_trade else 0
        state_group["acted_with_best_count"] += 1 if acted_with_best else 0
        state_group["acted_against_best_count"] += 1 if acted_against_best else 0
        state_group["reflection_context_carried_count"] += 1 if reflection_context == "reflection_context_carried" else 0
        state_group["reflection_context_cautious_count"] += 1 if reflection_context == "reflection_context_cautious" else 0
        state_group["reflection_context_unloaded_count"] += 1 if reflection_context == "reflection_context_unloaded" else 0
        state_group["reward_sum"] += reward
        state_group["best_reward_sum"] += best_reward
        state_group["afterlook_sum"] += _safe_float(row.get("passive_inner_awareness_afterlook"))
        state_group["carry_sum"] += _safe_float(row.get("passive_inner_awareness_carry"))
        state_group["world_carry_sum"] += _safe_float(row.get("passive_inner_awareness_world_carry"))
        state_group["families"].add(family)
        state_group["runs"].add(str(row.get("run", "") or ""))
        state_group["debug_roots"].add(str(row.get("debug_root", "") or ""))

        family_key = (family, state)
        family_group = family_groups.setdefault(
            family_key,
            {
                "symbol_family": family,
                "passive_inner_awareness_state": state,
                "count": 0,
                "wait_count": 0,
                "trade_count": 0,
                "withheld_best_trade_count": 0,
                "tp_count": 0,
                "sl_count": 0,
                "reward_sum": 0.0,
                "best_reward_sum": 0.0,
                "actions": set(),
                "best_actions": set(),
                "runs": set(),
                "debug_roots": set(),
            },
        )
        family_group["count"] += 1
        family_group["wait_count"] += 1 if action == "WAIT" else 0
        family_group["trade_count"] += 1 if trade_action else 0
        family_group["withheld_best_trade_count"] += 1 if withheld_best_trade else 0
        family_group["tp_count"] += 1 if outcome == "TP" else 0
        family_group["sl_count"] += 1 if outcome == "SL" else 0
        family_group["reward_sum"] += reward
        family_group["best_reward_sum"] += best_reward
        family_group["actions"].add(action)
        family_group["best_actions"].add(best_action)
        family_group["runs"].add(str(row.get("run", "") or ""))
        family_group["debug_roots"].add(str(row.get("debug_root", "") or ""))

    state_summary: list[dict] = []
    for group in state_groups.values():
        count = int(group["count"])
        state_summary.append(
            {
                "passive_inner_awareness_state": group["passive_inner_awareness_state"],
                "count": count,
                "loaded_count": int(group["loaded_count"]),
                "wait_count": int(group["wait_count"]),
                "long_count": int(group["long_count"]),
                "short_count": int(group["short_count"]),
                "tp_count": int(group["tp_count"]),
                "sl_count": int(group["sl_count"]),
                "no_trade_count": int(group["no_trade_count"]),
                "withheld_best_trade_count": int(group["withheld_best_trade_count"]),
                "acted_with_best_count": int(group["acted_with_best_count"]),
                "acted_against_best_count": int(group["acted_against_best_count"]),
                "reflection_context_carried_count": int(group["reflection_context_carried_count"]),
                "reflection_context_cautious_count": int(group["reflection_context_cautious_count"]),
                "reflection_context_unloaded_count": int(group["reflection_context_unloaded_count"]),
                "reward_sum": round(float(group["reward_sum"]), 6),
                "avg_reward": round(float(group["reward_sum"]) / count, 6) if count else 0.0,
                "avg_best_reward": round(float(group["best_reward_sum"]) / count, 6) if count else 0.0,
                "avg_afterlook": round(float(group["afterlook_sum"]) / count, 6) if count else 0.0,
                "avg_carry": round(float(group["carry_sum"]) / count, 6) if count else 0.0,
                "avg_world_carry": round(float(group["world_carry_sum"]) / count, 6) if count else 0.0,
                "family_count": len(group["families"]),
                "families": "|".join(sorted(group["families"])),
                "runs": "|".join(sorted(group["runs"])),
                "debug_roots": "|".join(sorted(group["debug_roots"])),
                "debug_root_count": len(group["debug_roots"]),
                "passive_only": True,
                "influences_action": False,
            }
        )

    family_summary: list[dict] = []
    for group in family_groups.values():
        count = int(group["count"])
        family_summary.append(
            {
                "symbol_family": group["symbol_family"],
                "passive_inner_awareness_state": group["passive_inner_awareness_state"],
                "count": count,
                "wait_count": int(group["wait_count"]),
                "trade_count": int(group["trade_count"]),
                "withheld_best_trade_count": int(group["withheld_best_trade_count"]),
                "tp_count": int(group["tp_count"]),
                "sl_count": int(group["sl_count"]),
                "reward_sum": round(float(group["reward_sum"]), 6),
                "avg_reward": round(float(group["reward_sum"]) / count, 6) if count else 0.0,
                "avg_best_reward": round(float(group["best_reward_sum"]) / count, 6) if count else 0.0,
                "actions": "|".join(sorted(group["actions"])),
                "best_actions": "|".join(sorted(group["best_actions"])),
                "runs": "|".join(sorted(group["runs"])),
                "debug_roots": "|".join(sorted(group["debug_roots"])),
                "debug_root_count": len(group["debug_roots"]),
                "passive_only": True,
                "influences_action": False,
            }
        )

    state_summary.sort(key=lambda row: (-int(row["count"]), str(row["passive_inner_awareness_state"])))
    family_summary.sort(key=lambda row: (-int(row["count"]), str(row["symbol_family"])))
    return detail, state_summary, family_summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(detail: list[dict], state_summary: list[dict], family_summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_passive_inner_awareness_runtime_trace.csv"
    state_path = output_dir / "dio_mini_passive_inner_awareness_runtime_state_summary.csv"
    family_path = output_dir / "dio_mini_passive_inner_awareness_runtime_family_summary.csv"
    json_path = output_dir / "dio_mini_passive_inner_awareness_runtime_trace.json"
    md_path = output_dir / "dio_mini_passive_inner_awareness_runtime_trace.md"

    _write_csv(detail_path, detail, ["run", "tick", "symbol_family", "passive_inner_awareness_state", "action"])
    _write_csv(state_path, state_summary, ["passive_inner_awareness_state", "count"])
    _write_csv(family_path, family_summary, ["symbol_family", "passive_inner_awareness_state", "count"])

    json_path.write_text(
        json.dumps(
            {
                "boundary": {
                    "passive_only": True,
                    "influences_action": False,
                    "writes_memory": False,
                    "is_gate": False,
                    "is_motoric": False,
                },
                "detail": detail,
                "state_summary": state_summary,
                "family_summary": family_summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# DIO Mini Passive Inner Awareness Runtime Trace",
        "",
        "## Grenze",
        "- liest nur episodes.csv",
        "- schreibt kein Memory",
        "- beeinflusst keine Handlung",
        "- ist kein Gate und keine Motorik",
        "",
        "## Zustandsuebersicht",
    ]
    if not state_summary:
        lines.append("- keine Zeilen")
    else:
        for row in state_summary:
            lines.append(
                f"- {row['passive_inner_awareness_state']}: count={row['count']} "
                f"wait={row['wait_count']} long={row['long_count']} short={row['short_count']} "
                f"tp={row['tp_count']} sl={row['sl_count']} "
                f"withheld_best_trade={row['withheld_best_trade_count']} "
                f"reflection_carried={row['reflection_context_carried_count']} "
                f"reflection_cautious={row['reflection_context_cautious_count']} "
                f"avg_best={row['avg_best_reward']}"
            )
    lines.extend(["", "## Staerkste Familien"])
    for row in family_summary[:20]:
        lines.append(
            f"- {row['symbol_family']} / {row['passive_inner_awareness_state']}: "
            f"count={row['count']} trade={row['trade_count']} wait={row['wait_count']} "
            f"withheld_best_trade={row['withheld_best_trade_count']} "
            f"best_actions={row['best_actions']}"
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive inner-awareness runtime trace")
    parser.add_argument("--debug-root", required=True, nargs="+")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    detail, state_summary, family_summary = build_rows([Path(item) for item in args.debug_root])
    write_outputs(detail, state_summary, family_summary, Path(args.output_dir))
    print(
        "detail_rows="
        f"{len(detail)} state_rows={len(state_summary)} family_rows={len(family_summary)}"
    )


if __name__ == "__main__":
    main()
