"""Report passive Mini-DIO neuro-state traces."""

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


def build_report(rows: list[dict]) -> dict:
    tone_counts: dict[str, int] = {}
    by_family: dict[str, dict] = {}
    for row in rows:
        tone = str(row.get("mini_neuro_dominant_tone", "-") or "-")
        tone_counts[tone] = int(tone_counts.get(tone, 0) or 0) + 1
        family = str(row.get("symbol_family", "-") or "-")
        state = by_family.setdefault(
            family,
            {
                "family": family,
                "rows": 0,
                "trades": 0,
                "tp": 0,
                "sl": 0,
                "reward_sum": 0.0,
                "tone_counts": {},
                "support_sum": 0.0,
                "load_sum": 0.0,
                "balance_sum": 0.0,
                "max_trust_tone": 0.0,
                "max_caution_tone": 0.0,
                "max_strain_tone": 0.0,
                "max_relief_tone": 0.0,
            },
        )
        state["rows"] += 1
        state["tone_counts"][tone] = int(state["tone_counts"].get(tone, 0) or 0) + 1
        action = str(row.get("action", "") or "").upper()
        if action in ("LONG", "SHORT"):
            state["trades"] += 1
        outcome = str(row.get("outcome_event", "") or "")
        state["tp"] += 1 if outcome == "TP" else 0
        state["sl"] += 1 if outcome == "SL" else 0
        state["reward_sum"] += _float(row.get("reward"))
        state["support_sum"] += _float(row.get("mini_neuro_support"))
        state["load_sum"] += _float(row.get("mini_neuro_load"))
        state["balance_sum"] += _float(row.get("mini_neuro_balance"))
        state["max_trust_tone"] = max(float(state["max_trust_tone"]), _float(row.get("mini_trust_tone")))
        state["max_caution_tone"] = max(float(state["max_caution_tone"]), _float(row.get("mini_caution_tone")))
        state["max_strain_tone"] = max(float(state["max_strain_tone"]), _float(row.get("mini_strain_tone")))
        state["max_relief_tone"] = max(float(state["max_relief_tone"]), _float(row.get("mini_relief_tone")))

    families = []
    for state in by_family.values():
        rows_count = max(1, int(state["rows"]))
        families.append(
            {
                "family": state["family"],
                "rows": int(state["rows"]),
                "trades": int(state["trades"]),
                "tp": int(state["tp"]),
                "sl": int(state["sl"]),
                "reward_sum": float(state["reward_sum"]),
                "tone_counts": dict(state["tone_counts"]),
                "avg_support": float(state["support_sum"]) / rows_count,
                "avg_load": float(state["load_sum"]) / rows_count,
                "avg_balance": float(state["balance_sum"]) / rows_count,
                "max_trust_tone": float(state["max_trust_tone"]),
                "max_caution_tone": float(state["max_caution_tone"]),
                "max_strain_tone": float(state["max_strain_tone"]),
                "max_relief_tone": float(state["max_relief_tone"]),
            }
        )
    families.sort(key=lambda item: (item["reward_sum"], item["avg_balance"], item["rows"]), reverse=True)
    return {
        "rows_scanned": len(rows),
        "tone_counts": dict(sorted(tone_counts.items())),
        "trades": sum(1 for row in rows if str(row.get("action", "") or "").upper() in ("LONG", "SHORT")),
        "tp": sum(1 for row in rows if str(row.get("outcome_event", "") or "") == "TP"),
        "sl": sum(1 for row in rows if str(row.get("outcome_event", "") or "") == "SL"),
        "families": families,
        "top_families": families[:16],
    }


def write_outputs(report: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "neuro_state_trace_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    rows = list(report.get("families", []) or [])
    if rows:
        with (output_dir / "neuro_state_trace.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    lines = [
        "MINI DIO NEURO STATE TRACE",
        f"rows_scanned={report.get('rows_scanned', 0)} trades={report.get('trades', 0)} tp={report.get('tp', 0)} sl={report.get('sl', 0)}",
        f"tone_counts={report.get('tone_counts', {})}",
        "",
        "TOP FAMILIES",
    ]
    for family in report.get("top_families", []) or []:
        lines.append(
            f"{family['family']}: rows={family['rows']} trades={family['trades']} "
            f"tp={family['tp']} sl={family['sl']} reward={family['reward_sum']:.6f} "
            f"balance={family['avg_balance']:.6f} support={family['avg_support']:.6f} "
            f"load={family['avg_load']:.6f} max_trust={family['max_trust_tone']:.6f} "
            f"max_caution={family['max_caution_tone']:.6f} tones={family['tone_counts']}"
        )
    (output_dir / "neuro_state_trace_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Mini-DIO passive neuro-state trace report")
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    rows = load_episode_rows(Path(args.debug_root))
    report = build_report(rows)
    write_outputs(report, Path(args.output))
    print(json.dumps({k: report[k] for k in ("rows_scanned", "trades", "tp", "sl", "tone_counts")}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
