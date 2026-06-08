"""Run DIO mini transfer phases with one shared memory.

This is diagnostic. It checks whether DIO-owned syntax carries experience
between controlled worlds instead of learning every world from zero.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from config import Config
from DIO_MINI.run_mini import run_once
from DIO_MINI.semantic_memory import SemanticMemory


DEFAULT_PHASES = (
    ("referenz", "data/kontrolliert_2episoden_5m_SOLUSDT.csv", 6),
    ("varianz", "data/kontrolliert_varianz_2episoden_5m_SOLUSDT.csv", 4),
    ("rauschen", "data/kontrolliert_rauschen_2episoden_5m_SOLUSDT.csv", 4),
    ("sensorische_varianz", "data/kontrolliert_sensorische_varianz_2episoden_5m_SOLUSDT.csv", 4),
    ("sensorischer_drift", "data/kontrolliert_sensorischer_drift_2episoden_5m_SOLUSDT.csv", 4),
)


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value)
    except Exception:
        return default
    if result != result:
        return default
    return result


def parse_phase(text: str) -> tuple[str, str, int]:
    parts = [part.strip() for part in str(text or "").split(":", 2)]
    if len(parts) != 3:
        raise ValueError(f"Phase must use name:path:runs format, got {text!r}")
    name, path, runs = parts
    return name or "phase", path, max(1, int(runs))


def compact_family_focus(report: dict) -> dict:
    focus = {
        "top_long_family": "-",
        "top_long_trust": 0.0,
        "top_short_family": "-",
        "top_short_trust": 0.0,
    }
    for family in report.get("family_top", []) or []:
        if not isinstance(family, dict):
            continue
        family_name = str(family.get("family", "-") or "-")
        actions = dict(family.get("actions", {}) or {})
        long_trust = _safe_float(dict(actions.get("LONG", {}) or {}).get("trust", 0.0))
        short_trust = _safe_float(dict(actions.get("SHORT", {}) or {}).get("trust", 0.0))
        if long_trust > focus["top_long_trust"]:
            focus["top_long_family"] = family_name
            focus["top_long_trust"] = long_trust
        if short_trust > focus["top_short_trust"]:
            focus["top_short_family"] = family_name
            focus["top_short_trust"] = short_trust
    return focus


def run_transfer(phases: list[tuple[str, str, int]], memory_path: Path, debug_root: Path, reset_memory: bool) -> list[dict]:
    if reset_memory and memory_path.exists():
        memory_path.unlink()
    memory = SemanticMemory(memory_path, max_symbols=getattr(Config, "DIO_MINI_MAX_EPISODES", 2048))
    memory.load()
    rows = []
    for phase_name, data_path_text, runs in phases:
        data_path = Path(data_path_text)
        phase_debug_root = debug_root / phase_name
        for phase_run in range(1, runs + 1):
            memory.mark_run()
            global_run = _safe_int(memory.data.get("runs", 1), 1)
            report = run_once(data_path, memory, global_run, phase_debug_root)
            memory.save()
            focus = compact_family_focus(report)
            rows.append(
                {
                    "phase": phase_name,
                    "phase_run": phase_run,
                    "global_run": global_run,
                    "data_path": str(data_path),
                    "candles": _safe_int(report.get("candles", 0)),
                    "episodes": _safe_int(report.get("episodes", 0)),
                    "trades": _safe_int(report.get("trades", 0)),
                    "long_trades": _safe_int(report.get("long_trades", 0)),
                    "short_trades": _safe_int(report.get("short_trades", 0)),
                    "waits": _safe_int(report.get("waits", 0)),
                    "total_reward": round(_safe_float(report.get("total_reward", 0.0)), 6),
                    "avg_reward": round(_safe_float(report.get("avg_reward", 0.0)), 6),
                    "unique_symbols": _safe_int(report.get("unique_symbols", 0)),
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
                    **focus,
                }
            )
            print(
                f"TRANSFER {phase_name} run={phase_run}/{runs} global={global_run} "
                f"trades={report['trades']} reward={report['total_reward']:.4f} "
                f"symbols={report['unique_symbols']}"
            )
    return rows


def write_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "transfer_summary.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    if rows:
        with (output_dir / "transfer_summary.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="DIO mini transfer diagnostic")
    parser.add_argument("--phase", action="append", help="name:path:runs. Can be passed multiple times.")
    parser.add_argument("--memory", default="bot_memory/dio_mini_transfer_memory.json")
    parser.add_argument("--debug-root", default="debug/dio_mini_transfer_test")
    parser.add_argument("--reset-memory", action="store_true")
    args = parser.parse_args()

    phases = [parse_phase(item) for item in args.phase] if args.phase else list(DEFAULT_PHASES)
    rows = run_transfer(phases, Path(args.memory), Path(args.debug_root), bool(args.reset_memory))
    write_outputs(rows, Path(args.debug_root))
    print(json.dumps(rows[-1] if rows else {}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
