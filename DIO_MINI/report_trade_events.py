"""Summarize Mini-DIO trade consequence events from episodes.csv files."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _safe_float(value: object) -> float:
    try:
        return float(value or 0.0)
    except Exception:
        return 0.0


def _iter_episode_rows(debug_root: Path) -> list[dict]:
    rows: list[dict] = []
    for path in sorted(debug_root.glob("**/episodes.csv")):
        run_id = path.parent.name.replace("dio_mini_lauf_", "")
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                item = dict(row)
                item["run"] = run_id
                item["source_file"] = str(path)
                rows.append(item)
    return rows


def build_rows(debug_root: Path) -> tuple[list[dict], list[dict]]:
    detail: list[dict] = []
    groups: dict[tuple[str, str, str], dict] = {}
    for row in _iter_episode_rows(debug_root):
        action = str(row.get("action", "WAIT") or "WAIT").upper()
        event = str(row.get("outcome_event", "NO_TRADE") or "NO_TRADE").upper()
        family = str(row.get("symbol_family", "") or "-")
        reward = _safe_float(row.get("reward", row.get("event_reward", 0.0)))
        item = {
            "run": str(row.get("run", "") or ""),
            "tick": str(row.get("tick", "") or ""),
            "symbol_family": family,
            "action": action,
            "outcome_event": event,
            "reward": round(reward, 6),
            "event_reward": round(_safe_float(row.get("event_reward", reward)), 6),
            "close_reward": round(_safe_float(row.get("close_reward", 0.0)), 6),
            "entry_price": str(row.get("entry_price", "") or ""),
            "tp_price": str(row.get("tp_price", "") or ""),
            "sl_price": str(row.get("sl_price", "") or ""),
            "exit_price": str(row.get("exit_price", "") or ""),
            "bars_held": str(row.get("bars_held", "") or ""),
            "source_file": str(row.get("source_file", "") or ""),
        }
        detail.append(item)

        key = (family, action, event)
        group = groups.setdefault(
            key,
            {
                "symbol_family": family,
                "action": action,
                "outcome_event": event,
                "count": 0,
                "reward_sum": 0.0,
                "runs": set(),
                "ticks": [],
            },
        )
        group["count"] += 1
        group["reward_sum"] += reward
        group["runs"].add(str(row.get("run", "") or ""))
        group["ticks"].append(str(row.get("tick", "") or ""))

    summary: list[dict] = []
    for group in groups.values():
        count = int(group["count"])
        summary.append(
            {
                "symbol_family": group["symbol_family"],
                "action": group["action"],
                "outcome_event": group["outcome_event"],
                "count": count,
                "reward_sum": round(float(group["reward_sum"]), 6),
                "avg_reward": round(float(group["reward_sum"]) / max(1, count), 6),
                "runs": ",".join(sorted(run for run in group["runs"] if run)),
                "ticks": ",".join(group["ticks"]),
                "passive_only": 1,
            }
        )
    summary.sort(
        key=lambda item: (
            str(item.get("outcome_event", "")) not in ("SL", "TP"),
            str(item.get("outcome_event", "")),
            str(item.get("symbol_family", "")),
            str(item.get("action", "")),
        )
    )
    return detail, summary


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_trade_events.csv"
    summary_path = output_dir / "dio_mini_trade_events_summary.csv"
    json_path = output_dir / "dio_mini_trade_events.json"
    md_path = output_dir / "dio_mini_trade_events.md"

    detail_fields = list(detail[0].keys()) if detail else [
        "run",
        "tick",
        "symbol_family",
        "action",
        "outcome_event",
        "reward",
        "event_reward",
        "close_reward",
        "entry_price",
        "tp_price",
        "sl_price",
        "exit_price",
        "bars_held",
        "source_file",
    ]
    summary_fields = list(summary[0].keys()) if summary else [
        "symbol_family",
        "action",
        "outcome_event",
        "count",
        "reward_sum",
        "avg_reward",
        "runs",
        "ticks",
        "passive_only",
    ]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)
    json_path.write_text(
        json.dumps({"detail": detail, "summary": summary}, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    lines = [
        "# DIO Mini Trade Events",
        "",
        "## Grenze",
        "- liest nur episodes.csv",
        "- schreibt kein Memory",
        "- beeinflusst keine Handlung",
        "",
        "## Zusammenfassung",
    ]
    if not summary:
        lines.append("- keine Ereignisse")
    else:
        for row in summary:
            lines.append(
                f"- {row.get('symbol_family', '-')}: {row.get('action', '-')} "
                f"{row.get('outcome_event', '-')} count={row.get('count', 0)} "
                f"reward_sum={row.get('reward_sum', 0.0)}"
            )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize Mini-DIO TP/SL trade events")
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    detail, summary = build_rows(Path(args.debug_root))
    write_outputs(detail, summary, Path(args.output_dir))
    print(f"detail_rows={len(detail)} summary_rows={len(summary)}")


if __name__ == "__main__":
    main()
