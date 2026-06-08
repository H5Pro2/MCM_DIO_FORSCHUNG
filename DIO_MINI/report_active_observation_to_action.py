"""Report active transition from observation memory into real mini-DIO action."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _int(value: object, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _run_number(path: Path) -> int:
    try:
        return int(path.name.rsplit("_", 1)[-1])
    except Exception:
        return 0


def load_episode_rows(debug_root: Path) -> list[dict]:
    rows: list[dict] = []
    for path in sorted(debug_root.glob("dio_mini_lauf_*/episodes.csv"), key=lambda p: _run_number(p.parent)):
        run = _run_number(path.parent)
        with path.open("r", newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                row["run"] = run
                rows.append(row)
    return rows


def load_memory(memory_path: Path) -> dict:
    if not memory_path.exists():
        return {}
    return json.loads(memory_path.read_text(encoding="utf-8"))


def build_report(rows: list[dict], memory: dict) -> dict:
    action_rows = [row for row in rows if str(row.get("action", "")).upper() in ("LONG", "SHORT")]
    family_rows: dict[str, list[dict]] = {}
    for row in rows:
        family = str(row.get("symbol_family", "-") or "-")
        family_rows.setdefault(family, []).append(row)

    symbols = dict(memory.get("symbols", {}) or {})
    transition_rows = []
    for row in action_rows:
        symbol = str(row.get("symbol", "") or "")
        family = str(row.get("symbol_family", "-") or "-")
        action = str(row.get("action", "") or "").upper()
        record = dict(symbols.get(symbol, {}) or {})
        actions = dict(record.get("actions", {}) or {})
        observations = dict(record.get("observations", {}) or {})
        action_state = dict(actions.get(action, {}) or {})
        observation_state = dict(observations.get(action, {}) or {})
        prior_seen = [
            item
            for item in family_rows.get(family, [])
            if _int(item.get("run")) <= _int(row.get("run"))
            and str(item.get("action", "")).upper() == "WAIT"
            and str(item.get("observation_learning_action", "")).upper() == action
        ]
        transition_rows.append(
            {
                "run": _int(row.get("run")),
                "tick": _int(row.get("tick")),
                "symbol": symbol,
                "family": family,
                "action": action,
                "outcome_event": str(row.get("outcome_event", "-") or "-"),
                "reward": _float(row.get("reward")),
                "readiness": _float(row.get(f"readiness_{action.lower()}")),
                "observation_signal": _float(row.get(f"observation_{action.lower()}")),
                "prior_family_observation_waits": len(prior_seen),
                "memory_action_count": _int(action_state.get("count")),
                "memory_action_trust": _float(action_state.get("trust")),
                "memory_observation_count": _int(observation_state.get("count")),
                "memory_observation_reward_sum": _float(observation_state.get("reward_sum")),
                "sehen_form_flow": _float(row.get("sehen_form_flow")),
                "sehen_form_stability": _float(row.get("sehen_form_stability")),
                "hoeren_energy_tone": _float(row.get("hoeren_energy_tone")),
                "fuehlen_mcm_coherence": _float(row.get("fuehlen_mcm_coherence")),
                "fuehlen_mcm_tension": _float(row.get("fuehlen_mcm_tension")),
            }
        )

    by_family: dict[str, dict] = {}
    for item in transition_rows:
        family = item["family"]
        state = by_family.setdefault(
            family,
            {
                "family": family,
                "actions": {},
                "trade_count": 0,
                "tp_count": 0,
                "sl_count": 0,
                "reward_sum": 0.0,
                "max_prior_family_observation_waits": 0,
                "max_memory_observation_count": 0,
                "max_memory_action_count": 0,
                "max_memory_action_trust": 0.0,
            },
        )
        action = item["action"]
        state["actions"][action] = int(state["actions"].get(action, 0) or 0) + 1
        state["trade_count"] += 1
        state["tp_count"] += 1 if item["outcome_event"] == "TP" else 0
        state["sl_count"] += 1 if item["outcome_event"] == "SL" else 0
        state["reward_sum"] += item["reward"]
        state["max_prior_family_observation_waits"] = max(
            int(state["max_prior_family_observation_waits"]),
            int(item["prior_family_observation_waits"]),
        )
        state["max_memory_observation_count"] = max(
            int(state["max_memory_observation_count"]),
            int(item["memory_observation_count"]),
        )
        state["max_memory_action_count"] = max(
            int(state["max_memory_action_count"]),
            int(item["memory_action_count"]),
        )
        state["max_memory_action_trust"] = max(
            float(state["max_memory_action_trust"]),
            float(item["memory_action_trust"]),
        )

    return {
        "rows_scanned": len(rows),
        "trades": len(action_rows),
        "tp": sum(1 for row in action_rows if str(row.get("outcome_event", "")) == "TP"),
        "sl": sum(1 for row in action_rows if str(row.get("outcome_event", "")) == "SL"),
        "transitions": transition_rows,
        "families": sorted(by_family.values(), key=lambda item: (item["reward_sum"], item["trade_count"]), reverse=True),
    }


def write_outputs(report: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "active_observation_to_action_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    rows = list(report.get("transitions", []) or [])
    if rows:
        with (output_dir / "active_observation_to_action_transitions.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    lines = [
        "ACTIVE OBSERVATION TO ACTION",
        f"rows_scanned={report.get('rows_scanned', 0)}",
        f"trades={report.get('trades', 0)} tp={report.get('tp', 0)} sl={report.get('sl', 0)}",
        "",
        "FAMILIES",
    ]
    for family in report.get("families", []) or []:
        lines.append(
            f"{family['family']}: trades={family['trade_count']} tp={family['tp_count']} "
            f"sl={family['sl_count']} reward={family['reward_sum']:.6f} "
            f"prior_obs_wait_max={family['max_prior_family_observation_waits']} "
            f"memory_obs_max={family['max_memory_observation_count']} "
            f"memory_action_max={family['max_memory_action_count']} "
            f"memory_trust_max={family['max_memory_action_trust']:.6f} "
            f"actions={family['actions']}"
        )
    (output_dir / "active_observation_to_action_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Mini-DIO active observation-to-action report")
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--memory", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    rows = load_episode_rows(Path(args.debug_root))
    memory = load_memory(Path(args.memory))
    report = build_report(rows, memory)
    write_outputs(report, Path(args.output))
    print(json.dumps({k: report[k] for k in ("rows_scanned", "trades", "tp", "sl")}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
