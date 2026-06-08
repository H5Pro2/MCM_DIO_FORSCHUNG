"""Build a passive temporal-semantic sign memory for Mini-DIO.

This layer stores recurring internal signs from passive evidence reports. It is
not runtime memory and is not read by the Mini-DIO action loop.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _base36(number: int) -> str:
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    number = abs(int(number))
    if number == 0:
        return "0"
    chars = []
    while number:
        number, rem = divmod(number, 36)
        chars.append(alphabet[rem])
    return "".join(reversed(chars))


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(float(value or default))
    except Exception:
        return default


def _truthy(value: object) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes"}


def make_passive_sign_symbol(payload: dict) -> str:
    """Create DIO-owned syntax for a passive recurring sign."""

    family = str(payload.get("symbol_family", "") or "")
    state = str(payload.get("sign_state", "") or "")
    kind = str(payload.get("sign_kind", "") or "")
    fields = str(payload.get("stable_fields", "") or "")
    direction_state = str(payload.get("direction_state", "") or "")
    readings = str(payload.get("emergence_readings", "") or "")
    values = [
        len(family),
        len(state),
        len(kind),
        len(fields),
        len(direction_state),
        len(readings),
    ]
    hash_value = 2166136261
    for char in f"{family}|{state}|{kind}|{fields}|{direction_state}|{readings}":
        hash_value ^= ord(char) + 59
        hash_value = (hash_value * 16777619) & 0xFFFFFFFF
    for value in values:
        hash_value ^= abs(int(value)) + 59
        hash_value = (hash_value * 16777619) & 0xFFFFFFFF
    return f"dio_sign_{_base36(hash_value).rjust(7, '0')}"


def _sign_kind(row: dict) -> str:
    state = str(row.get("evidence_state", "") or "")
    readings = str(row.get("emergence_readings", "") or "")
    best_actions = {item.strip() for item in str(row.get("validation_best_actions", "") or "").split("|") if item.strip()}
    if state == "repeated_passive_emergence_candidate":
        return "recurrent_form_field_sign"
    if "emergence_candidate_form_field_without_direction" in readings:
        return "open_form_field_sign"
    if len(best_actions) == 1 and state == "passive_stable_direction_candidate":
        return "stable_form_field_direction_sign"
    return "passive_seen_sign"


def _sign_state(row: dict) -> str:
    kind = _sign_kind(row)
    best_actions = {item.strip() for item in str(row.get("validation_best_actions", "") or "").split("|") if item.strip()}
    if kind == "recurrent_form_field_sign" and len(best_actions) > 1:
        return "known_lage_direction_unripe"
    if kind == "open_form_field_sign":
        return "known_lage_open_direction"
    if kind == "stable_form_field_direction_sign":
        return "known_lage_direction_candidate"
    return "known_lage_observed"


def _dio_sentence(payload: dict) -> str:
    family = str(payload.get("symbol_family", "") or "")
    state = str(payload.get("sign_state", "") or "")
    if state == "known_lage_direction_unripe":
        return (
            f"{family}: Ich kenne diese Lage als wiederkehrende Form-/Feldnaehe, "
            "aber Richtung ist nicht gereift."
        )
    if state == "known_lage_open_direction":
        return f"{family}: Diese Lage kommt wieder, aber sie bleibt offen."
    if state == "known_lage_direction_candidate":
        return f"{family}: Diese Lage zeigt passive Richtungshoehe, aber bleibt ohne Handlung."
    return f"{family}: Diese Lage wurde passiv gesehen."


def build_passive_sign_memory(evidence_rows: list[dict], min_sources: int = 1) -> tuple[list[dict], list[dict]]:
    signs: list[dict] = []
    summary_groups: dict[str, dict] = {}

    for row in evidence_rows:
        if not _truthy(row.get("candidate_only")) and str(row.get("evidence_state", "")) == "not_seen_in_validation":
            continue
        source_count = _safe_int(row.get("validation_source_count"))
        if source_count < int(min_sources):
            continue
        payload = {
            "symbol_family": str(row.get("symbol_family", "") or ""),
            "evidence_state": str(row.get("evidence_state", "") or ""),
            "sign_kind": _sign_kind(row),
            "sign_state": _sign_state(row),
            "validation_source_count": source_count,
            "validation_sources_seen": str(row.get("validation_sources_seen", "") or ""),
            "validation_sources_withheld": str(row.get("validation_sources_withheld", "") or ""),
            "validation_observation_count": _safe_int(row.get("validation_observation_count")),
            "validation_withheld_best_trade_count": _safe_int(row.get("validation_withheld_best_trade_count")),
            "validation_best_actions": str(row.get("validation_best_actions", "") or ""),
            "emergence_readings": str(row.get("emergence_readings", "") or ""),
            "stable_fields": str(row.get("stable_fields", "") or ""),
            "direction_state": "direction_unripe"
            if "|" in str(row.get("validation_best_actions", "") or "")
            else "direction_candidate",
            "temporal_semantic_layer": True,
            "subconscious_like_layer": True,
            "passive_only": True,
            "writes_runtime_memory": False,
            "read_by_mini_dio": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
            "is_entry_signal": False,
            "is_direction_signal": False,
        }
        payload["passive_sign_symbol"] = make_passive_sign_symbol(payload)
        payload["dio_sentence"] = _dio_sentence(payload)
        signs.append(payload)

        group = summary_groups.setdefault(
            payload["sign_state"],
            {
                "sign_state": payload["sign_state"],
                "sign_count": 0,
                "families": [],
                "source_count_sum": 0,
                "withheld_count_sum": 0,
            },
        )
        group["sign_count"] += 1
        group["families"].append(payload["symbol_family"])
        group["source_count_sum"] += int(payload["validation_source_count"])
        group["withheld_count_sum"] += int(payload["validation_withheld_best_trade_count"])

    signs.sort(
        key=lambda item: (
            0 if item["sign_state"] == "known_lage_direction_unripe" else 1,
            -int(item["validation_source_count"]),
            str(item["symbol_family"]),
        )
    )
    summary = [
        {
            "sign_state": group["sign_state"],
            "sign_count": int(group["sign_count"]),
            "families": "|".join(sorted(group["families"])),
            "source_count_sum": int(group["source_count_sum"]),
            "withheld_count_sum": int(group["withheld_count_sum"]),
            "passive_only": True,
            "influences_action": False,
        }
        for group in summary_groups.values()
    ]
    summary.sort(key=lambda item: (-int(item["sign_count"]), str(item["sign_state"])))
    return signs, summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(signs: list[dict], summary: list[dict], output_dir: Path, memory_path: Path | None = None) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "passive_sign_memory.csv"
    summary_path = output_dir / "passive_sign_memory_summary.csv"
    json_path = output_dir / "passive_sign_memory.json"
    md_path = output_dir / "passive_sign_memory.md"

    payload = {
        "boundary": {
            "passive_only": True,
            "writes_runtime_memory": False,
            "read_by_mini_dio": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
            "is_entry_signal": False,
            "is_direction_signal": False,
        },
        "layer": {
            "name": "passive_sign_memory",
            "type": "temporal_semantic_layer",
            "subconscious_like_layer": True,
            "purpose": "store recurring internal signs without action coupling",
        },
        "signs": signs,
        "summary": summary,
    }

    _write_csv(detail_path, signs, ["passive_sign_symbol", "symbol_family", "sign_state"])
    _write_csv(summary_path, summary, ["sign_state", "sign_count"])
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    if memory_path is not None:
        memory_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = memory_path.with_suffix(memory_path.suffix + ".tmp")
        temp_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        temp_path.replace(memory_path)

    lines = [
        "# Passive Sign Memory",
        "",
        "## Grenze",
        "- passiv",
        "- keine Runtime-Lesung",
        "- keine Handlung",
        "- kein Gate",
        "- keine Richtung",
        "",
        "## Summary",
    ]
    for row in summary:
        lines.append(
            f"- {row['sign_state']}: signs={row['sign_count']} "
            f"sources={row['source_count_sum']} withheld={row['withheld_count_sum']} "
            f"{row['families']}"
        )
    lines.extend(["", "## Zeichen"])
    for item in signs[:20]:
        lines.append(
            f"- {item['passive_sign_symbol']} / {item['symbol_family']}: "
            f"{item['sign_state']} sources={item['validation_source_count']} "
            f"best={item['validation_best_actions']}"
        )
        lines.append(f"  {item['dio_sentence']}")
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive Mini-DIO sign memory")
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--memory-output", default="")
    parser.add_argument("--min-sources", type=int, default=1)
    args = parser.parse_args()

    signs, summary = build_passive_sign_memory(_read_csv(Path(args.evidence)), min_sources=args.min_sources)
    memory_path = Path(args.memory_output) if args.memory_output else None
    write_outputs(signs, summary, Path(args.output_dir), memory_path=memory_path)
    print(f"signs={len(signs)} summary_rows={len(summary)}")


if __name__ == "__main__":
    main()
