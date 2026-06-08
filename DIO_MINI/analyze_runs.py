"""Summarize DIO mini run reports.

This tool is diagnostic only. It does not alter memory or behavior.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _top_family(report: dict, action: str) -> tuple[str, float, int]:
    action = str(action or "").upper()
    best_family = "-"
    best_trust = 0.0
    best_count = 0
    for family in report.get("family_top", []) or []:
        if not isinstance(family, dict):
            continue
        state = dict(family.get("actions", {}) or {}).get(action, {}) or {}
        trust = _safe_float(state.get("trust", 0.0))
        count = _safe_int(state.get("count", 0))
        if trust > best_trust or (trust == best_trust and count > best_count):
            best_family = str(family.get("family", "-") or "-")
            best_trust = trust
            best_count = count
    return best_family, best_trust, best_count


def _family_stats(report: dict) -> dict:
    families = [family for family in report.get("family_top", []) or [] if isinstance(family, dict)]
    active_families = 0
    observation_families = 0
    for family in families:
        actions = dict(family.get("actions", {}) or {})
        observations = dict(family.get("observations", {}) or {})
        has_action = False
        has_observation = False
        for action in ("LONG", "SHORT"):
            action_state = dict(actions.get(action, {}) or {})
            observation_state = dict(observations.get(action, {}) or {})
            if _safe_int(action_state.get("count", 0)) > 0:
                has_action = True
            if _safe_int(observation_state.get("count", 0)) > 0:
                has_observation = True
        active_families += 1 if has_action else 0
        observation_families += 1 if has_observation else 0
    return {
        "tracked_families": len(families),
        "active_trade_families": active_families,
        "observation_families": observation_families,
    }


def _episode_stats(report_path: str | Path) -> dict:
    path = Path(str(report_path))
    episode_path = path.parent / "episodes.csv"
    stats = {
        "raw_trade_pressure": 0,
        "phase_suppressed": 0,
        "executed_trades": 0,
    }
    if not episode_path.exists():
        return stats
    try:
        with episode_path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                raw_action = str(row.get("raw_action", "") or "").upper()
                action = str(row.get("action", "") or "").upper()
                phase_active = _safe_int(row.get("phase_active", 0))
                if raw_action in ("LONG", "SHORT"):
                    stats["raw_trade_pressure"] += 1
                if action in ("LONG", "SHORT"):
                    stats["executed_trades"] += 1
                if phase_active and raw_action in ("LONG", "SHORT") and action == "WAIT":
                    stats["phase_suppressed"] += 1
    except Exception:
        return stats
    return stats


def collect_reports(debug_root: Path) -> list[dict]:
    reports = []
    for path in sorted(debug_root.glob("dio_mini_lauf_*/mini_report.json")):
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(report, dict):
            continue
        report["_path"] = str(path)
        reports.append(report)
    reports.sort(key=lambda item: _safe_int(item.get("run", 0)))
    return reports


def summarize(reports: list[dict]) -> list[dict]:
    rows = []
    for report in reports:
        long_family, long_trust, long_count = _top_family(report, "LONG")
        short_family, short_trust, short_count = _top_family(report, "SHORT")
        episode_stats = _episode_stats(report.get("_path", ""))
        family_stats = _family_stats(report)
        trades = _safe_int(report.get("trades", 0))
        episodes = _safe_int(report.get("episodes", 0))
        unique_symbols = _safe_int(report.get("unique_symbols", 0))
        rows.append(
            {
                "run": _safe_int(report.get("run", 0)),
                "candles": _safe_int(report.get("candles", 0)),
                "episodes": episodes,
                "trades": trades,
                "waits": _safe_int(report.get("waits", 0)),
                "long_trades": _safe_int(report.get("long_trades", 0)),
                "short_trades": _safe_int(report.get("short_trades", 0)),
                "total_reward": round(_safe_float(report.get("total_reward", 0.0)), 6),
                "avg_reward": round(_safe_float(report.get("avg_reward", 0.0)), 6),
                "unique_symbols": unique_symbols,
                "symbol_density": round(unique_symbols / max(1, episodes), 6),
                "tracked_families": family_stats["tracked_families"],
                "active_trade_families": family_stats["active_trade_families"],
                "observation_families": family_stats["observation_families"],
                "family_compression": round(family_stats["active_trade_families"] / max(1, unique_symbols), 6),
                "actionable_seen": _safe_int(report.get("actionable_seen", 0)),
                "correct_action_when_actionable": _safe_int(report.get("correct_action_when_actionable", 0)),
                "avg_trade_readiness": round(_safe_float(report.get("avg_trade_readiness", 0.0)), 6),
                "max_trade_readiness": round(_safe_float(report.get("max_trade_readiness", 0.0)), 6),
                "avg_associative_trade": round(_safe_float(report.get("avg_associative_trade", 0.0)), 6),
                "max_associative_trade": round(_safe_float(report.get("max_associative_trade", 0.0)), 6),
                "avg_maturity_gap": round(_safe_float(report.get("avg_maturity_gap", 0.0)), 6),
                "max_maturity_gap": round(_safe_float(report.get("max_maturity_gap", 0.0)), 6),
                "avg_mature_transfer": round(_safe_float(report.get("avg_mature_transfer", 0.0)), 6),
                "max_mature_transfer": round(_safe_float(report.get("max_mature_transfer", 0.0)), 6),
                "avg_observation_trade_signal": round(_safe_float(report.get("avg_observation_trade_signal", 0.0)), 6),
                "max_observation_trade_signal": round(_safe_float(report.get("max_observation_trade_signal", 0.0)), 6),
                "avg_observation_trade_readiness": round(_safe_float(report.get("avg_observation_trade_readiness", 0.0)), 6),
                "max_observation_trade_readiness": round(_safe_float(report.get("max_observation_trade_readiness", 0.0)), 6),
                "observation_learning_events": _safe_int(report.get("observation_learning_events", 0)),
                "avg_observation_learning_pressure": round(_safe_float(report.get("avg_observation_learning_pressure", 0.0)), 6),
                "max_observation_learning_pressure": round(_safe_float(report.get("max_observation_learning_pressure", 0.0)), 6),
                "trade_density": round(trades / max(1, episodes), 6),
                "raw_trade_pressure": episode_stats["raw_trade_pressure"],
                "phase_suppressed": episode_stats["phase_suppressed"],
                "compressed_contacts": max(0, episode_stats["raw_trade_pressure"] - episode_stats["executed_trades"]),
                "top_long_family": long_family,
                "top_long_trust": round(long_trust, 6),
                "top_long_count": long_count,
                "top_short_family": short_family,
                "top_short_trust": round(short_trust, 6),
                "top_short_count": short_count,
                "report_path": report.get("_path", "-"),
            }
        )
    return rows


def write_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "dio_mini_summary.json"
    csv_path = output_dir / "dio_mini_summary.csv"
    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    if rows:
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze DIO mini run reports")
    parser.add_argument("--debug-root", default="debug")
    parser.add_argument("--output-dir", default="debug")
    args = parser.parse_args()

    debug_root = Path(args.debug_root)
    rows = summarize(collect_reports(debug_root))
    write_outputs(rows, Path(args.output_dir))
    for row in rows:
        print(
            f"run={row['run']} trades={row['trades']} reward={row['total_reward']:.4f} "
            f"long={row['long_trades']} short={row['short_trades']} "
            f"families=({row['top_long_family']},{row['top_short_family']})"
        )


if __name__ == "__main__":
    main()
