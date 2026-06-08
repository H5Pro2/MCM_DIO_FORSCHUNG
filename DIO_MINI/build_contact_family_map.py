"""Join passive contact-lage syntax with episode form families."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _read_contact_report(path: Path, contact_id: str) -> dict:
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if str(row.get("contact_id", "") or "") == contact_id:
                return dict(row)
    return {}


def _read_episode_rows(debug_root: Path) -> list[dict]:
    rows = []
    for path in sorted(debug_root.glob("dio_mini_lauf_*/episodes.csv")):
        run_id = path.parent.name.replace("dio_mini_lauf_", "")
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                item = dict(row)
                item["run"] = run_id
                rows.append(item)
    return rows


def _classify_episode(row: dict) -> str:
    action = str(row.get("action", "") or "")
    best = str(row.get("best_action_training", "") or "")
    reward = float(row.get("reward", 0.0) or 0.0)
    obs_action = str(row.get("observation_learning_action", "") or "")
    if action in ("LONG", "SHORT") and reward > 0.0:
        return "kontakt_handlung_bestaetigt"
    if action in ("LONG", "SHORT") and reward < 0.0:
        return "kontakt_handlung_belastet"
    if obs_action in ("LONG", "SHORT"):
        return "kontakt_beobachtet_reift"
    if best in ("LONG", "SHORT"):
        return "kontakt_gehalten"
    return "kontakt_ruhend"


def _build_rows(contact: dict, episode_rows: list[dict]) -> list[dict]:
    contact_id = str(contact.get("contact_id", "") or "")
    contact_symbol = str(contact.get("contact_symbol", "") or "")
    contact_state = str(contact.get("contact_lage_state", "") or "")
    rows = []
    for row in episode_rows:
        rows.append(
            {
                "contact_id": contact_id,
                "contact_symbol": contact_symbol,
                "contact_lage_state": contact_state,
                "run": row.get("run", ""),
                "tick": row.get("tick", ""),
                "timestamp_ms": row.get("timestamp_ms", ""),
                "symbol": row.get("symbol", ""),
                "symbol_family": row.get("symbol_family", ""),
                "episode_contact_state": _classify_episode(row),
                "action": row.get("action", ""),
                "best_action_training": row.get("best_action_training", ""),
                "observation_learning_action": row.get("observation_learning_action", ""),
                "reward": row.get("reward", ""),
                "trade_readiness": row.get("trade_readiness", ""),
                "associative_trade": row.get("associative_trade", ""),
                "observation_learning_pressure": row.get("observation_learning_pressure", ""),
            }
        )
    return rows


def _write(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "dio_mini_contact_family_map.csv"
    json_path = output_dir / "dio_mini_contact_family_map.json"
    md_path = output_dir / "dio_mini_contact_family_map.md"
    fieldnames = [
        "contact_id",
        "contact_symbol",
        "contact_lage_state",
        "run",
        "tick",
        "timestamp_ms",
        "symbol",
        "symbol_family",
        "episode_contact_state",
        "action",
        "best_action_training",
        "observation_learning_action",
        "reward",
        "trade_readiness",
        "associative_trade",
        "observation_learning_pressure",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    by_state: dict[str, int] = {}
    by_family: dict[str, int] = {}
    for row in rows:
        by_state[row["episode_contact_state"]] = by_state.get(row["episode_contact_state"], 0) + 1
        by_family[row["symbol_family"]] = by_family.get(row["symbol_family"], 0) + 1
    lines = ["# DIO Mini Contact Family Map", ""]
    if rows:
        lines.extend(
            [
                f"- contact_symbol: {rows[0]['contact_symbol']}",
                f"- contact_lage_state: {rows[0]['contact_lage_state']}",
                f"- rows: {len(rows)}",
                "",
                "## Episode States",
            ]
        )
        for key, value in sorted(by_state.items()):
            lines.append(f"- {key}: {value}")
        lines.extend(["", "## Top Families"])
        for key, value in sorted(by_family.items(), key=lambda item: item[1], reverse=True)[:12]:
            lines.append(f"- {key}: {value}")
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contact-report", required=True)
    parser.add_argument("--contact-id", required=True)
    parser.add_argument("--debug-root", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    contact = _read_contact_report(Path(args.contact_report), args.contact_id)
    if not contact:
        raise SystemExit(f"contact_id not found: {args.contact_id}")
    rows = _build_rows(contact, _read_episode_rows(Path(args.debug_root)))
    _write(rows, Path(args.output_dir))
    print(
        f"{contact.get('contact_symbol')} {contact.get('contact_lage_state')} "
        f"rows={len(rows)}"
    )


if __name__ == "__main__":
    main()
