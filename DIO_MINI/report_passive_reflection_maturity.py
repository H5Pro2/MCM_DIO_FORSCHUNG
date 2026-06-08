"""Passive reflection maturity report for DIO_MINI.

This report classifies passive reflection candidate timelines into readable
states such as reorganized, cautious, mixed, or open. It is diagnostic only.
"""

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


def _safe_int(value: object) -> int:
    try:
        return int(float(value or 0))
    except Exception:
        return 0


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _count_path(path: str, token: str) -> int:
    return sum(1 for item in str(path or "").split(" -> ") if item == token)


def _classify(row: dict) -> str:
    kind = str(row.get("reflection_candidate_kind", "") or "")
    reward = _safe_float(row.get("reward_sum"))
    positive_contacts = _count_path(str(row.get("contact_state_path", "") or ""), "executed_positive_contact")
    negative_contacts = _count_path(str(row.get("contact_state_path", "") or ""), "executed_negative_contact")
    observed_contacts = _count_path(str(row.get("contact_state_path", "") or ""), "observed_potential_contact")
    carried_hits = _count_path(str(row.get("inner_state_path", "") or ""), "inner_carried")
    cautious_hits = _count_path(str(row.get("inner_state_path", "") or ""), "inner_cautious")
    hits = max(1, _safe_int(row.get("hits")))

    if kind == "reflection_candidate_reorganized_trace" and reward > 0.0 and positive_contacts > negative_contacts:
        return "reflection_reorganized_readable"
    if kind == "reflection_candidate_cautious_trace" and negative_contacts > 0 and positive_contacts == 0:
        return "reflection_cautious_unresolved"
    if carried_hits > 0 and cautious_hits > 0:
        return "reflection_mixed_inner_state"
    if observed_contacts >= hits:
        return "reflection_observed_only"
    return "reflection_open_unreadable"


def _maturity_sentence(row: dict, maturity: str) -> str:
    family = str(row.get("symbol_family", "") or "-")
    reward = _safe_float(row.get("reward_sum"))
    best = _safe_float(row.get("best_reward_sum"))
    if maturity == "reflection_reorganized_readable":
        return (
            f"{family}: Die Spur ist passiv reorganisiert lesbar; Konflikt wurde spaeter getragen "
            f"(reward={reward:.6f}, best={best:.6f})."
        )
    if maturity == "reflection_cautious_unresolved":
        return (
            f"{family}: Die Spur ist passiv vorsichtig und noch ungeloest; Konflikt wurde beobachtet, "
            f"aber nicht getragen (reward={reward:.6f}, best={best:.6f})."
        )
    if maturity == "reflection_mixed_inner_state":
        return f"{family}: Die Spur ist passiv gemischt; Innenlage wechselt zwischen Tragen und Vorsicht."
    if maturity == "reflection_observed_only":
        return f"{family}: Die Spur ist passiv nur beobachtet; keine reale Kontaktreife sichtbar."
    return f"{family}: Die Spur ist passiv noch nicht sauber lesbar."


def build_rows(timeline_rows: list[dict]) -> list[dict]:
    output: list[dict] = []
    for row in timeline_rows:
        maturity = _classify(row)
        contact_path = str(row.get("contact_state_path", "") or "")
        inner_path = str(row.get("inner_state_path", "") or "")
        item = {
            "symbol_family": str(row.get("symbol_family", "") or ""),
            "reflection_maturity": maturity,
            "reflection_candidate_kind": str(row.get("reflection_candidate_kind", "") or ""),
            "passive_conflict_state": str(row.get("passive_conflict_state", "") or ""),
            "worlds": str(row.get("worlds", "") or ""),
            "hits": _safe_int(row.get("hits")),
            "reward_sum": round(_safe_float(row.get("reward_sum")), 6),
            "best_reward_sum": round(_safe_float(row.get("best_reward_sum")), 6),
            "positive_contacts": _count_path(contact_path, "executed_positive_contact"),
            "negative_contacts": _count_path(contact_path, "executed_negative_contact"),
            "observed_contacts": _count_path(contact_path, "observed_potential_contact"),
            "carried_hits": _count_path(inner_path, "inner_carried"),
            "cautious_hits": _count_path(inner_path, "inner_cautious"),
            "open_hits": _count_path(inner_path, "inner_open_observation"),
            "actions": str(row.get("actions", "") or ""),
            "reflection_question": str(row.get("reflection_question", "") or ""),
            "maturity_sentence": _maturity_sentence(row, maturity),
            "passive_only": 1,
        }
        output.append(item)
    output.sort(
        key=lambda row: (
            str(row.get("reflection_maturity", "")),
            str(row.get("symbol_family", "")),
        )
    )
    return output


def write_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "dio_mini_passive_reflection_maturity.csv"
    json_path = output_dir / "dio_mini_passive_reflection_maturity.json"
    md_path = output_dir / "dio_mini_passive_reflection_maturity.md"

    fields = list(rows[0].keys()) if rows else ["symbol_family", "reflection_maturity"]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    json_path.write_text(json.dumps({"maturity": rows}, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Passive Reflection Maturity", ""]
    if not rows:
        lines.append("Keine passive Reflexionsreife gefunden.")
    for row in rows:
        lines.extend(
            [
                f"## {row['symbol_family']}",
                f"- maturity: {row['reflection_maturity']}",
                f"- kind: {row['reflection_candidate_kind']}",
                f"- hits: {row['hits']}",
                f"- contacts: positive={row['positive_contacts']} negative={row['negative_contacts']} observed={row['observed_contacts']}",
                f"- inner: carried={row['carried_hits']} cautious={row['cautious_hits']} open={row['open_hits']}",
                f"- reward_sum: {float(row['reward_sum']):.6f}",
                f"- best_reward_sum: {float(row['best_reward_sum']):.6f}",
                f"- question: {row['reflection_question']}",
                f"- sentence: {row['maturity_sentence']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Grenze",
            "- passive Reifelesung",
            "- kein Memory-Schreiben",
            "- keine Motorik",
            "- kein Gate",
            "- keine harte Regel",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive reflection maturity report")
    parser.add_argument("--candidate-timeline", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    rows = build_rows(_read_csv(Path(args.candidate_timeline)))
    write_outputs(rows, Path(args.output_dir))
    print(f"reflection_maturity_rows={len(rows)}")
    for row in rows:
        print(f"{row['symbol_family']} {row['reflection_maturity']} reward={row['reward_sum']}")


if __name__ == "__main__":
    main()
