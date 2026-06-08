"""Build a passive contact-lage reference protocol for DIO_MINI."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _iter_reports(debug_root: Path) -> list[dict]:
    reports = []
    for path in sorted(debug_root.glob("dio_mini_lauf_*/mini_report.json")):
        data = _read_json(path)
        if isinstance(data, dict):
            reports.append(data)
    return reports


def _class_count(overview: dict, name: str) -> int:
    return int(dict(overview.get("class_counts", {}) or {}).get(name, 0) or 0)


def _class_reward(overview: dict, name: str) -> float:
    return float(dict(overview.get("class_reward_sum", {}) or {}).get(name, 0.0) or 0.0)


def _contact_state(state: str, overview: dict, reports: list[dict]) -> str:
    state = str(state or "").strip()
    if state:
        return state
    direct = _class_count(overview, "direct_positive_action")
    obs_action = _class_count(overview, "observation_to_positive_action")
    held = _class_count(overview, "held_observation")
    first_trades = int(reports[0].get("trades", 0) or 0) if reports else 0
    if direct > 0 and first_trades > 0:
        return "exakte_wiederbegegnung"
    if direct > 0 or obs_action >= held:
        return "nahe_aehnlichkeit"
    return "ferne_aehnlichkeit"


def _summarize_contact(spec: str) -> dict:
    parts = spec.split(":", 3)
    if len(parts) not in (3, 4):
        raise ValueError(
            "--contact must be state:contact_id:sensor_debug_root "
            "or state:contact_id:sensor_debug_root:transition_debug_root"
        )
    state_hint, contact_id, debug_root_text = parts[:3]
    debug_root = Path(debug_root_text)
    transition_root = Path(parts[3]) if len(parts) == 4 else debug_root
    overview = _read_json(transition_root / "dio_mini_action_transition_overview.json")
    reports = _iter_reports(debug_root)
    runs = len(reports)
    trades_total = sum(int(item.get("trades", 0) or 0) for item in reports)
    reward_total = sum(float(item.get("total_reward", 0.0) or 0.0) for item in reports)
    direct = _class_count(overview, "direct_positive_action")
    obs_action = _class_count(overview, "observation_to_positive_action")
    held = _class_count(overview, "held_observation")
    quiet = _class_count(overview, "quiet_family")
    contact_reward_sum = (
        _class_reward(overview, "direct_positive_action")
        + _class_reward(overview, "observation_to_positive_action")
    )
    return {
        "contact_id": contact_id,
        "contact_lage_state": _contact_state("" if state_hint == "auto" else state_hint, overview, reports),
        "debug_root": str(debug_root),
        "runs": runs,
        "trades_total": trades_total,
        "reward_total": round(reward_total, 6),
        "contact_reward_sum": round(contact_reward_sum, 6),
        "direct_positive_action": direct,
        "observation_to_positive_action": obs_action,
        "held_observation": held,
        "quiet_family": quiet,
        "top_direct_action": ",".join(str(item) for item in overview.get("top_direct_action", []) or []),
        "top_observation_to_action": ",".join(str(item) for item in overview.get("top_observation_to_action", []) or []),
    }


def _write_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "dio_mini_contact_reference_protocol.csv"
    json_path = output_dir / "dio_mini_contact_reference_protocol.json"
    md_path = output_dir / "dio_mini_contact_reference_protocol.md"
    fieldnames = [
        "contact_id",
        "contact_lage_state",
        "debug_root",
        "runs",
        "trades_total",
        "reward_total",
        "contact_reward_sum",
        "direct_positive_action",
        "observation_to_positive_action",
        "held_observation",
        "quiet_family",
        "top_direct_action",
        "top_observation_to_action",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    lines = ["# DIO Mini Contact Reference Protocol", ""]
    for row in rows:
        lines.extend(
            [
                f"## {row['contact_id']}",
                f"- state: {row['contact_lage_state']}",
                f"- runs: {row['runs']}",
                f"- trades_total: {row['trades_total']}",
                f"- reward_total: {row['reward_total']}",
                f"- contact_reward_sum: {row['contact_reward_sum']}",
                f"- direct_positive_action: {row['direct_positive_action']}",
                f"- observation_to_positive_action: {row['observation_to_positive_action']}",
                f"- held_observation: {row['held_observation']}",
                f"- top_direct_action: {row['top_direct_action'] or '-'}",
                f"- top_observation_to_action: {row['top_observation_to_action'] or '-'}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contact", action="append", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    rows = [_summarize_contact(item) for item in args.contact]
    _write_outputs(rows, Path(args.output_dir))
    for row in rows:
        print(
            f"{row['contact_id']}: {row['contact_lage_state']} "
            f"trades={row['trades_total']} reward={row['reward_total']}"
        )


if __name__ == "__main__":
    main()
