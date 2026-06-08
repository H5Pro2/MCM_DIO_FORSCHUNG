"""Passive report for mini-DIO negative consequence traces."""

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


def _classify(row: dict) -> str:
    event = str(row.get("outcome_event", "") or "").upper()
    reward = _float(row.get("reward"))
    if event == "SL" or reward < 0.0:
        tension = _float(row.get("fuehlen_mcm_tension"))
        readiness = max(_float(row.get("readiness_long")), _float(row.get("readiness_short")))
        observation = max(_float(row.get("observation_long")), _float(row.get("observation_short")))
        if tension > 0.70 and readiness < 0.10:
            return "negative_overloaded_low_readiness"
        if observation > readiness:
            return "negative_observation_over_action"
        return "negative_action_consequence"
    return "neutral_or_positive"


def load_negative_rows(debug_roots: list[Path]) -> list[dict]:
    rows: list[dict] = []
    for debug_root in debug_roots:
        for path in sorted(debug_root.glob("**/episodes.csv"), key=lambda p: (_run_number(p.parent), str(p))):
            run = _run_number(path.parent)
            with path.open("r", newline="", encoding="utf-8") as handle:
                for row in csv.DictReader(handle):
                    action = str(row.get("action", "") or "").upper()
                    if action not in ("LONG", "SHORT"):
                        continue
                    event = str(row.get("outcome_event", "") or "").upper()
                    reward = _float(row.get("reward"))
                    if event != "SL" and reward >= 0.0:
                        continue
                    item = {
                        "source": str(path.parent),
                        "run": run,
                        "tick": _int(row.get("tick")),
                        "timestamp_ms": str(row.get("timestamp_ms", "") or ""),
                        "symbol": str(row.get("symbol", "") or ""),
                        "family": str(row.get("symbol_family", "") or ""),
                        "action": action,
                        "outcome_event": event,
                        "reward": reward,
                        "readiness_long": _float(row.get("readiness_long")),
                        "readiness_short": _float(row.get("readiness_short")),
                        "observation_long": _float(row.get("observation_long")),
                        "observation_short": _float(row.get("observation_short")),
                        "sehen_form_flow": _float(row.get("sehen_form_flow")),
                        "sehen_form_stability": _float(row.get("sehen_form_stability")),
                        "hoeren_energy_tone": _float(row.get("hoeren_energy_tone")),
                        "fuehlen_mcm_coherence": _float(row.get("fuehlen_mcm_coherence")),
                        "fuehlen_mcm_tension": _float(row.get("fuehlen_mcm_tension")),
                    }
                    item["negative_trace_state"] = _classify({**row, **item})
                    rows.append(item)
    return rows


def build_report(rows: list[dict]) -> dict:
    family_map: dict[str, dict] = {}
    state_map: dict[str, int] = {}
    for row in rows:
        state = str(row["negative_trace_state"])
        state_map[state] = int(state_map.get(state, 0) or 0) + 1
        family = row["family"] or row["symbol"][:8]
        item = family_map.setdefault(
            family,
            {
                "family": family,
                "negative_count": 0,
                "sl_count": 0,
                "reward_sum": 0.0,
                "actions": {},
                "states": {},
                "max_tension": 0.0,
                "max_observation_minus_readiness": 0.0,
            },
        )
        action = row["action"]
        readiness = max(float(row["readiness_long"]), float(row["readiness_short"]))
        observation = max(float(row["observation_long"]), float(row["observation_short"]))
        item["negative_count"] += 1
        item["sl_count"] += 1 if row["outcome_event"] == "SL" else 0
        item["reward_sum"] += float(row["reward"])
        item["actions"][action] = int(item["actions"].get(action, 0) or 0) + 1
        item["states"][state] = int(item["states"].get(state, 0) or 0) + 1
        item["max_tension"] = max(float(item["max_tension"]), float(row["fuehlen_mcm_tension"]))
        item["max_observation_minus_readiness"] = max(
            float(item["max_observation_minus_readiness"]),
            observation - readiness,
        )
    return {
        "negative_rows": len(rows),
        "sl_rows": sum(1 for row in rows if row["outcome_event"] == "SL"),
        "states": dict(sorted(state_map.items())),
        "families": sorted(
            family_map.values(),
            key=lambda item: (item["negative_count"], -item["reward_sum"]),
            reverse=True,
        ),
        "rows": rows,
    }


def write_outputs(report: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "negative_consequence_trace_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    rows = list(report.get("rows", []) or [])
    if rows:
        with (output_dir / "negative_consequence_trace_rows.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    lines = [
        "NEGATIVE CONSEQUENCE TRACE",
        f"negative_rows={report.get('negative_rows', 0)} sl_rows={report.get('sl_rows', 0)}",
        f"states={report.get('states', {})}",
        "",
        "FAMILIES",
    ]
    for family in report.get("families", []) or []:
        lines.append(
            f"{family['family']}: negative={family['negative_count']} sl={family['sl_count']} "
            f"reward={family['reward_sum']:.6f} actions={family['actions']} states={family['states']} "
            f"max_tension={family['max_tension']:.6f} "
            f"max_obs_minus_ready={family['max_observation_minus_readiness']:.6f}"
        )
    (output_dir / "negative_consequence_trace_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Passive mini-DIO negative consequence trace report")
    parser.add_argument("--debug-root", action="append", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    rows = load_negative_rows([Path(item) for item in args.debug_root])
    report = build_report(rows)
    write_outputs(report, Path(args.output))
    print(json.dumps({k: report[k] for k in ("negative_rows", "sl_rows", "states")}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
