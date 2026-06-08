"""Passive schema check for a future DIO_MINI reflection memory.

This tool does not write reflection memory. It only checks whether passive
reflection maturity rows contain the minimal information that a later
reflection-memory writer would need.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REQUIRED_FIELDS = [
    "symbol_family",
    "reflection_maturity",
    "worlds",
    "hits",
    "reward_sum",
    "best_reward_sum",
    "positive_contacts",
    "negative_contacts",
    "observed_contacts",
    "carried_hits",
    "cautious_hits",
    "open_hits",
    "reflection_question",
]


ALLOWED_MATURITY = {
    "reflection_reorganized_readable",
    "reflection_cautious_unresolved",
    "reflection_mixed_inner_state",
    "reflection_observed_only",
    "reflection_open_unreadable",
}


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


def _missing_fields(row: dict) -> list[str]:
    missing: list[str] = []
    for field in REQUIRED_FIELDS:
        value = row.get(field)
        if value is None:
            missing.append(field)
            continue
        if isinstance(value, str) and value.strip() == "":
            missing.append(field)
    return missing


def _contact_path(row: dict) -> str:
    parts: list[str] = []
    negative = _safe_int(row.get("negative_contacts"))
    observed = _safe_int(row.get("observed_contacts"))
    positive = _safe_int(row.get("positive_contacts"))
    if negative:
        parts.append(f"negative:{negative}")
    if observed:
        parts.append(f"observed:{observed}")
    if positive:
        parts.append(f"positive:{positive}")
    return " -> ".join(parts) or "empty"


def _inner_path(row: dict) -> str:
    parts: list[str] = []
    carried = _safe_int(row.get("carried_hits"))
    cautious = _safe_int(row.get("cautious_hits"))
    open_hits = _safe_int(row.get("open_hits"))
    if carried:
        parts.append(f"carried:{carried}")
    if cautious:
        parts.append(f"cautious:{cautious}")
    if open_hits:
        parts.append(f"open:{open_hits}")
    return " -> ".join(parts) or "unknown"


def _schema_state(row: dict) -> tuple[str, list[str]]:
    reasons: list[str] = []
    missing = _missing_fields(row)
    if missing:
        reasons.append("missing:" + ",".join(missing))
    maturity = str(row.get("reflection_maturity", "") or "")
    if maturity not in ALLOWED_MATURITY:
        reasons.append("unknown_maturity")
    if _safe_int(row.get("hits")) <= 0:
        reasons.append("no_hits")
    if _safe_int(row.get("positive_contacts")) + _safe_int(row.get("negative_contacts")) + _safe_int(row.get("observed_contacts")) <= 0:
        reasons.append("no_contact_path")
    if not str(row.get("worlds", "") or "").strip():
        reasons.append("no_world_context")
    if not str(row.get("reflection_question", "") or "").strip():
        reasons.append("no_reflection_question")
    if reasons:
        return "not_eligible_passive_schema", reasons
    return "eligible_passive_schema", ["minimal_schema_present"]


def _candidate_payload(row: dict) -> dict:
    """Return a non-persistent candidate payload for inspection only."""
    return {
        "family_id": str(row.get("symbol_family", "") or ""),
        "source": "passive_reflection_maturity",
        "real_contact_path": _contact_path(row),
        "inner_state_path": _inner_path(row),
        "reflection_maturity": str(row.get("reflection_maturity", "") or ""),
        "reflection_question": str(row.get("reflection_question", "") or ""),
        "worlds": str(row.get("worlds", "") or ""),
        "reward_sum": round(_safe_float(row.get("reward_sum")), 6),
        "best_reward_sum": round(_safe_float(row.get("best_reward_sum")), 6),
        "passive_origin": True,
    }


def build_rows(maturity_rows: list[dict]) -> tuple[list[dict], list[dict]]:
    detail: list[dict] = []
    for row in maturity_rows:
        schema_state, reasons = _schema_state(row)
        payload = _candidate_payload(row)
        detail.append(
            {
                "symbol_family": payload["family_id"],
                "schema_state": schema_state,
                "schema_reasons": ",".join(reasons),
                "reflection_maturity": payload["reflection_maturity"],
                "real_contact_path": payload["real_contact_path"],
                "inner_state_path": payload["inner_state_path"],
                "worlds": payload["worlds"],
                "reward_sum": payload["reward_sum"],
                "best_reward_sum": payload["best_reward_sum"],
                "reflection_question": payload["reflection_question"],
                "candidate_payload_json": json.dumps(payload, sort_keys=True),
                "writes_memory": 0,
                "passive_only": 1,
            }
        )

    groups: dict[str, dict] = {}
    for row in detail:
        state = str(row.get("schema_state", "") or "")
        item = groups.setdefault(
            state,
            {
                "schema_state": state,
                "count": 0,
                "families": set(),
            },
        )
        item["count"] += 1
        item["families"].add(str(row.get("symbol_family", "") or ""))

    summary: list[dict] = []
    for item in groups.values():
        summary.append(
            {
                "schema_state": item["schema_state"],
                "count": int(item["count"]),
                "families": ",".join(sorted(name for name in item["families"] if name)),
            }
        )
    summary.sort(key=lambda row: (str(row.get("schema_state", "")) != "eligible_passive_schema", str(row.get("schema_state", ""))))
    detail.sort(key=lambda row: (str(row.get("schema_state", "")) != "eligible_passive_schema", str(row.get("symbol_family", ""))))
    return detail, summary


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_passive_reflection_memory_schema_check.csv"
    summary_path = output_dir / "dio_mini_passive_reflection_memory_schema_check_summary.csv"
    json_path = output_dir / "dio_mini_passive_reflection_memory_schema_check.json"
    md_path = output_dir / "dio_mini_passive_reflection_memory_schema_check.md"

    detail_fields = list(detail[0].keys()) if detail else ["symbol_family", "schema_state"]
    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)

    summary_fields = list(summary[0].keys()) if summary else ["schema_state", "count", "families"]
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)

    json_path.write_text(json.dumps({"detail": detail, "summary": summary}, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["# DIO Mini Passive Reflection Memory Schema Check", ""]
    if not summary:
        lines.append("Keine Reflexionsschema-Daten gefunden.")
    for row in summary:
        lines.extend(
            [
                f"## {row['schema_state']}",
                f"- count: {row['count']}",
                f"- families: {row['families'] or '-'}",
                "",
            ]
        )
    lines.extend(["# Detail", ""])
    for row in detail:
        lines.extend(
            [
                f"## {row['symbol_family']}",
                f"- schema_state: {row['schema_state']}",
                f"- schema_reasons: {row['schema_reasons']}",
                f"- reflection_maturity: {row['reflection_maturity']}",
                f"- real_contact_path: {row['real_contact_path']}",
                f"- inner_state_path: {row['inner_state_path']}",
                f"- worlds: {row['worlds']}",
                f"- writes_memory: {row['writes_memory']}",
                f"- question: {row['reflection_question']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Grenze",
            "- passive Schema-Pruefung",
            "- kein Reflexionsspeicher-Schreiben",
            "- keine Motorik",
            "- kein Gate",
            "- keine harte Regel",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check passive reflection-memory schema eligibility")
    parser.add_argument("--reflection-maturity", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    detail, summary = build_rows(_read_csv(Path(args.reflection_maturity)))
    write_outputs(detail, summary, Path(args.output_dir))
    print(f"schema_detail_rows={len(detail)} schema_summary_rows={len(summary)}")
    for row in summary:
        print(f"{row['schema_state']} count={row['count']} families={row['families']}")


if __name__ == "__main__":
    main()
