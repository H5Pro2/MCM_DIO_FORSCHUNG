"""Compare passive temporal/neuro traces across two Mini-DIO worlds.

The report is diagnostic only. It reads episode traces from a source world and
a target/conflict world and checks whether family maturity transfers as action,
observation, or non-transfer.
"""

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
        return int(float(value))
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
                item = dict(row)
                item["run"] = run
                rows.append(item)
    return rows


def aggregate_families(rows: list[dict]) -> dict[str, dict]:
    families: dict[str, dict] = {}
    for row in rows:
        family = str(row.get("symbol_family", "-") or "-")
        state = families.setdefault(
            family,
            {
                "family": family,
                "rows": 0,
                "trades": 0,
                "tp": 0,
                "sl": 0,
                "reward_sum": 0.0,
                "tone_counts": {},
                "temporal_states": {},
                "support_sum": 0.0,
                "load_sum": 0.0,
                "balance_sum": 0.0,
                "max_trust_tone": 0.0,
                "max_caution_tone": 0.0,
                "max_temporal_trust_support": 0.0,
                "max_temporal_caution_support": 0.0,
                "max_afterimage": 0.0,
                "max_trade_readiness": 0.0,
            },
        )
        state["rows"] += 1
        action = str(row.get("action", "") or "").upper()
        if action in ("LONG", "SHORT"):
            state["trades"] += 1
        outcome = str(row.get("outcome_event", "") or "")
        state["tp"] += 1 if outcome == "TP" else 0
        state["sl"] += 1 if outcome == "SL" else 0
        state["reward_sum"] += _float(row.get("reward"))

        tone = str(row.get("mini_neuro_dominant_tone", "-") or "-")
        temporal_state = str(row.get("mini_temporal_state", "-") or "-")
        state["tone_counts"][tone] = _int(state["tone_counts"].get(tone)) + 1
        state["temporal_states"][temporal_state] = _int(state["temporal_states"].get(temporal_state)) + 1

        state["support_sum"] += _float(row.get("mini_neuro_support"))
        state["load_sum"] += _float(row.get("mini_neuro_load"))
        state["balance_sum"] += _float(row.get("mini_neuro_balance"))
        state["max_trust_tone"] = max(float(state["max_trust_tone"]), _float(row.get("mini_trust_tone")))
        state["max_caution_tone"] = max(float(state["max_caution_tone"]), _float(row.get("mini_caution_tone")))
        state["max_temporal_trust_support"] = max(
            float(state["max_temporal_trust_support"]),
            _float(row.get("mini_temporal_trust_support")),
        )
        state["max_temporal_caution_support"] = max(
            float(state["max_temporal_caution_support"]),
            _float(row.get("mini_temporal_caution_support")),
        )
        state["max_afterimage"] = max(float(state["max_afterimage"]), _float(row.get("mini_afterimage")))
        state["max_trade_readiness"] = max(float(state["max_trade_readiness"]), _float(row.get("trade_readiness")))

    for state in families.values():
        rows_count = max(1, int(state["rows"]))
        state["avg_support"] = float(state["support_sum"]) / rows_count
        state["avg_load"] = float(state["load_sum"]) / rows_count
        state["avg_balance"] = float(state["balance_sum"]) / rows_count
    return families


def classify_transfer(source: dict, target: dict) -> str:
    if not source and target:
        return "new_target_family"
    if source and not target:
        return "source_only"
    if not source and not target:
        return "empty"
    if source.get("trades", 0) > 0 and target.get("trades", 0) > 0:
        if target.get("reward_sum", 0.0) > 0.0:
            return "transferred_with_positive_action"
        if target.get("reward_sum", 0.0) < 0.0:
            return "transferred_with_negative_action"
        return "transferred_with_neutral_action"
    if source.get("trades", 0) > 0 and target.get("trades", 0) == 0:
        if target.get("max_temporal_trust_support", 0.0) > 0.0 or target.get("max_afterimage", 0.0) > 0.0:
            return "recognized_without_action"
        return "not_reactivated"
    if source.get("trades", 0) == 0 and target.get("trades", 0) > 0:
        return "target_action_without_source_action"
    return "observed_in_both"


def build_report(source_rows: list[dict], target_rows: list[dict]) -> dict:
    source = aggregate_families(source_rows)
    target = aggregate_families(target_rows)
    family_names = sorted(set(source) | set(target))
    rows = []
    transfer_counts: dict[str, int] = {}
    for family in family_names:
        left = source.get(family, {})
        right = target.get(family, {})
        status = classify_transfer(left, right)
        transfer_counts[status] = _int(transfer_counts.get(status)) + 1
        rows.append(
            {
                "family": family,
                "transfer_status": status,
                "source_rows": _int(left.get("rows")),
                "source_trades": _int(left.get("trades")),
                "source_tp": _int(left.get("tp")),
                "source_sl": _int(left.get("sl")),
                "source_reward_sum": round(_float(left.get("reward_sum")), 6),
                "source_avg_balance": round(_float(left.get("avg_balance")), 6),
                "source_max_temporal_trust_support": round(_float(left.get("max_temporal_trust_support")), 6),
                "target_rows": _int(right.get("rows")),
                "target_trades": _int(right.get("trades")),
                "target_tp": _int(right.get("tp")),
                "target_sl": _int(right.get("sl")),
                "target_reward_sum": round(_float(right.get("reward_sum")), 6),
                "target_avg_balance": round(_float(right.get("avg_balance")), 6),
                "target_max_temporal_trust_support": round(_float(right.get("max_temporal_trust_support")), 6),
                "target_max_temporal_caution_support": round(_float(right.get("max_temporal_caution_support")), 6),
                "target_max_afterimage": round(_float(right.get("max_afterimage")), 6),
                "target_max_trade_readiness": round(_float(right.get("max_trade_readiness")), 6),
                "source_tones": dict(left.get("tone_counts", {}) or {}),
                "target_tones": dict(right.get("tone_counts", {}) or {}),
                "source_temporal_states": dict(left.get("temporal_states", {}) or {}),
                "target_temporal_states": dict(right.get("temporal_states", {}) or {}),
            }
        )
    rows.sort(
        key=lambda item: (
            item["source_reward_sum"],
            item["target_max_temporal_trust_support"],
            item["target_rows"],
        ),
        reverse=True,
    )
    return {
        "source_rows_scanned": len(source_rows),
        "target_rows_scanned": len(target_rows),
        "source_families": len(source),
        "target_families": len(target),
        "transfer_counts": dict(sorted(transfer_counts.items())),
        "families": rows,
        "top_families": rows[:20],
    }


def write_outputs(report: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "temporal_neuro_transfer_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    rows = list(report.get("families", []) or [])
    if rows:
        with (output_dir / "temporal_neuro_transfer.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    lines = [
        "MINI DIO TEMPORAL/NEURO TRANSFER",
        f"source_rows={report.get('source_rows_scanned', 0)} target_rows={report.get('target_rows_scanned', 0)}",
        f"source_families={report.get('source_families', 0)} target_families={report.get('target_families', 0)}",
        f"transfer_counts={report.get('transfer_counts', {})}",
        "",
        "TOP FAMILIES",
    ]
    for family in report.get("top_families", []) or []:
        lines.append(
            f"{family['family']}: status={family['transfer_status']} "
            f"source_trades={family['source_trades']} source_tp={family['source_tp']} "
            f"source_reward={family['source_reward_sum']:.6f} "
            f"target_trades={family['target_trades']} target_reward={family['target_reward_sum']:.6f} "
            f"target_trust={family['target_max_temporal_trust_support']:.6f} "
            f"target_caution={family['target_max_temporal_caution_support']:.6f} "
            f"target_afterimage={family['target_max_afterimage']:.6f} "
            f"target_readiness={family['target_max_trade_readiness']:.6f}"
        )
    (output_dir / "temporal_neuro_transfer_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Mini-DIO passive temporal/neuro transfer report")
    parser.add_argument("--source-debug-root", required=True)
    parser.add_argument("--target-debug-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    report = build_report(
        load_episode_rows(Path(args.source_debug_root)),
        load_episode_rows(Path(args.target_debug_root)),
    )
    write_outputs(report, Path(args.output))
    print(
        json.dumps(
            {
                "source_rows_scanned": report["source_rows_scanned"],
                "target_rows_scanned": report["target_rows_scanned"],
                "source_families": report["source_families"],
                "target_families": report["target_families"],
                "transfer_counts": report["transfer_counts"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
