"""Report passive sign identity drift across sign-memory snapshots.

This diagnostic compares passive_sign_memory.csv outputs. It is passive only:
it does not write runtime memory and is not read by Mini-DIO action logic.
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
from pathlib import Path


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


def _expand_patterns(patterns: list[str]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        matches = glob.glob(pattern)
        if matches:
            paths.extend(Path(match) for match in matches)
        else:
            paths.append(Path(pattern))
    unique = {str(path.resolve()): path for path in paths}
    return [unique[key] for key in sorted(unique)]


def _source_label(path: Path) -> str:
    name = path.parent.name or path.stem
    name = name.replace("dio_mini_passive_sign_memory_", "")
    return name or path.stem


def _identity_payload(row: dict) -> str:
    """Return the passive identity-bearing payload without evidence counters."""

    return "|".join(
        [
            str(row.get("symbol_family", "") or ""),
            str(row.get("sign_kind", "") or ""),
            str(row.get("sign_state", "") or ""),
            str(row.get("stable_fields", "") or ""),
            str(row.get("direction_state", "") or ""),
            str(row.get("emergence_readings", "") or ""),
        ]
    )


def _drift_state(symbols: list[str], identities: list[str], source_count: int) -> str:
    if source_count <= 0:
        return "not_seen"
    if source_count == 1:
        return "single_passive_sign_identity"
    if len(set(symbols)) == 1 and len(set(identities)) == 1:
        return "stable_passive_sign_identity"
    if len(set(identities)) == 1:
        return "symbol_changed_without_identity_drift"
    return "passive_sign_identity_drift"


def build_identity_drift(sign_memory_paths: list[Path], target_family: str | None = None) -> tuple[list[dict], list[dict]]:
    available_sources = len(sign_memory_paths)
    grouped: dict[str, dict] = {}

    for path in sign_memory_paths:
        source = _source_label(path)
        for row in _read_csv(path):
            family = str(row.get("symbol_family", "") or "")
            if not family:
                continue
            if target_family and family != target_family:
                continue
            item = grouped.setdefault(
                family,
                {
                    "symbol_family": family,
                    "sources": [],
                    "passive_sign_symbols": [],
                    "sign_states": [],
                    "sign_kinds": [],
                    "stable_fields": [],
                    "direction_states": [],
                    "emergence_readings": [],
                    "source_counts": [],
                    "observation_counts": [],
                    "identity_payloads": [],
                    "sentences": [],
                },
            )
            item["sources"].append(source)
            item["passive_sign_symbols"].append(str(row.get("passive_sign_symbol", "") or ""))
            item["sign_states"].append(str(row.get("sign_state", "") or ""))
            item["sign_kinds"].append(str(row.get("sign_kind", "") or ""))
            item["stable_fields"].append(str(row.get("stable_fields", "") or ""))
            item["direction_states"].append(str(row.get("direction_state", "") or ""))
            item["emergence_readings"].append(str(row.get("emergence_readings", "") or ""))
            item["source_counts"].append(_safe_int(row.get("validation_source_count")))
            item["observation_counts"].append(_safe_int(row.get("validation_observation_count")))
            item["identity_payloads"].append(_identity_payload(row))
            item["sentences"].append(str(row.get("dio_sentence", "") or ""))

    rows: list[dict] = []
    groups: dict[str, dict] = {}
    for item in grouped.values():
        source_count = len(set(item["sources"]))
        state = _drift_state(item["passive_sign_symbols"], item["identity_payloads"], source_count)
        latest_index = len(item["sources"]) - 1
        latest_symbol = item["passive_sign_symbols"][latest_index] if latest_index >= 0 else ""
        latest_fields = item["stable_fields"][latest_index] if latest_index >= 0 else ""
        latest_sentence = item["sentences"][latest_index] if latest_index >= 0 else ""
        unique_symbols = sorted(set(item["passive_sign_symbols"]))
        row = {
            "symbol_family": item["symbol_family"],
            "identity_drift_state": state,
            "sign_source_count": source_count,
            "available_sign_sources": available_sources,
            "sources": "|".join(item["sources"]),
            "latest_passive_sign_symbol": latest_symbol,
            "passive_sign_symbol_history": "|".join(item["passive_sign_symbols"]),
            "unique_passive_sign_symbols": "|".join(unique_symbols),
            "unique_passive_sign_symbol_count": len(unique_symbols),
            "latest_sign_state": item["sign_states"][latest_index] if latest_index >= 0 else "",
            "sign_state_history": "|".join(item["sign_states"]),
            "latest_sign_kind": item["sign_kinds"][latest_index] if latest_index >= 0 else "",
            "sign_kind_history": "|".join(item["sign_kinds"]),
            "latest_stable_fields": latest_fields,
            "stable_fields_history": " || ".join(item["stable_fields"]),
            "latest_direction_state": item["direction_states"][latest_index] if latest_index >= 0 else "",
            "direction_state_history": "|".join(item["direction_states"]),
            "latest_emergence_readings": item["emergence_readings"][latest_index] if latest_index >= 0 else "",
            "emergence_readings_history": " || ".join(item["emergence_readings"]),
            "validation_source_count_history": "|".join(str(value) for value in item["source_counts"]),
            "validation_observation_count_history": "|".join(str(value) for value in item["observation_counts"]),
            "latest_dio_sentence": latest_sentence,
            "passive_only": True,
            "writes_runtime_memory": False,
            "read_by_mini_dio": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
            "is_entry_signal": False,
            "is_direction_signal": False,
        }
        rows.append(row)
        group = groups.setdefault(
            state,
            {
                "identity_drift_state": state,
                "family_count": 0,
                "families": [],
            },
        )
        group["family_count"] += 1
        group["families"].append(item["symbol_family"])

    rows.sort(
        key=lambda row: (
            row["identity_drift_state"] != "passive_sign_identity_drift",
            row["identity_drift_state"] != "stable_passive_sign_identity",
            -int(row["sign_source_count"]),
            str(row["symbol_family"]),
        )
    )
    summary = [
        {
            "identity_drift_state": group["identity_drift_state"],
            "family_count": int(group["family_count"]),
            "families": "|".join(sorted(group["families"])),
            "passive_only": True,
            "influences_action": False,
        }
        for group in groups.values()
    ]
    summary.sort(key=lambda row: (-int(row["family_count"]), str(row["identity_drift_state"])))
    return rows, summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(rows: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "passive_sign_identity_drift.csv"
    summary_path = output_dir / "passive_sign_identity_drift_summary.csv"
    json_path = output_dir / "passive_sign_identity_drift.json"
    md_path = output_dir / "passive_sign_identity_drift.md"
    _write_csv(detail_path, rows, ["symbol_family", "identity_drift_state"])
    _write_csv(summary_path, summary, ["identity_drift_state", "family_count"])
    json_path.write_text(
        json.dumps(
            {
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
                "families": rows,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Passive Sign Identity Drift",
        "",
        "## Grenze",
        "- passiv",
        "- keine Runtime-Lesung",
        "- keine Handlung",
        "- keine Richtung",
        "- kein Entry",
        "",
        "## Zusammenfassung",
    ]
    for row in summary:
        lines.append(
            f"- {row['identity_drift_state']}: {row['family_count']} "
            f"({row.get('families', '')})"
        )
    lines.extend(["", "## Details"])
    for row in rows[:20]:
        lines.append(
            f"- {row['symbol_family']}: {row['identity_drift_state']} "
            f"symbols={row['unique_passive_sign_symbols']} latest={row['latest_passive_sign_symbol']}"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sign-memory", nargs="+", required=True, help="passive_sign_memory.csv files or glob patterns")
    parser.add_argument("--target-family", default="", help="Optional family to inspect, e.g. dio_0x52")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    paths = _expand_patterns(args.sign_memory)
    rows, summary = build_identity_drift(paths, target_family=args.target_family or None)
    write_outputs(rows, summary, Path(args.output_dir))
    print(f"sign_sources={len(paths)} families={len(rows)} summary_rows={len(summary)}")
    for row in rows[:8]:
        print(
            f"{row['symbol_family']} {row['identity_drift_state']} "
            f"{row['unique_passive_sign_symbols']}"
        )


if __name__ == "__main__":
    main()
