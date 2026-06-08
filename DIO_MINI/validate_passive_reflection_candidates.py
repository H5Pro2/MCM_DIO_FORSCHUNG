"""Validate passive reflection candidates against held-out Mini-DIO traces.

This is a diagnostic-only comparison. It does not write runtime memory and does
not feed any result back into Mini-DIO.
"""

from __future__ import annotations

import argparse
import csv
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


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value or default)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _truthy(value: object) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes"}


def build_validation(candidate_path: Path, validation_family_summary_path: Path) -> tuple[list[dict], list[dict]]:
    candidates = _read_csv(candidate_path)
    validation_rows = _read_csv(validation_family_summary_path)
    validation_by_family = {
        str(row.get("symbol_family", "") or "-"): dict(row)
        for row in validation_rows
    }

    detail: list[dict] = []
    groups: dict[str, dict] = {}

    for candidate in candidates:
        family = str(candidate.get("symbol_family", "") or "-")
        candidate_only = _truthy(candidate.get("candidate_only"))
        candidate_state = str(candidate.get("passive_reflection_candidate_state", "") or "")
        validation = validation_by_family.get(family, {})
        recurred = bool(validation)
        validation_state = str(validation.get("passive_inner_awareness_state", "not_seen") or "not_seen")
        validation_count = _safe_int(validation.get("count"))
        validation_withheld = _safe_int(validation.get("withheld_best_trade_count"))
        validation_best = _safe_float(validation.get("avg_best_reward"))

        if not candidate_only:
            result_state = "not_validated_not_candidate"
        elif not recurred:
            result_state = "candidate_not_seen_in_validation_world"
        elif validation_state in {"unloaded", "-", "not_seen"}:
            result_state = "candidate_seen_without_inner_awareness"
        elif validation_withheld > 0:
            result_state = "candidate_recurred_with_passive_withholding"
        else:
            result_state = "candidate_recurred_without_withholding"

        item = {
            "symbol_family": family,
            "validation_result_state": result_state,
            "candidate_only": candidate_only,
            "candidate_state": candidate_state,
            "candidate_pressure_state": str(candidate.get("source_pressure_state", "") or ""),
            "candidate_world_count": _safe_int(candidate.get("debug_root_count")),
            "candidate_observation_count": _safe_int(candidate.get("observation_count")),
            "candidate_withheld_best_trade_count": _safe_int(candidate.get("withheld_best_trade_count")),
            "candidate_best_actions": str(candidate.get("best_actions", "") or ""),
            "validation_seen": recurred,
            "validation_inner_state": validation_state,
            "validation_debug_root_count": _safe_int(validation.get("debug_root_count")),
            "validation_observation_count": validation_count,
            "validation_wait_count": _safe_int(validation.get("wait_count")),
            "validation_trade_count": _safe_int(validation.get("trade_count")),
            "validation_withheld_best_trade_count": validation_withheld,
            "validation_avg_best_reward": round(validation_best, 6),
            "validation_best_actions": str(validation.get("best_actions", "") or ""),
            "passive_only": True,
            "writes_runtime_memory": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
            "is_entry_signal": False,
        }
        detail.append(item)

        group = groups.setdefault(
            result_state,
            {
                "validation_result_state": result_state,
                "family_count": 0,
                "candidate_count": 0,
                "validation_seen_count": 0,
                "validation_withheld_best_trade_count": 0,
            },
        )
        group["family_count"] += 1
        group["candidate_count"] += 1 if candidate_only else 0
        group["validation_seen_count"] += 1 if recurred else 0
        group["validation_withheld_best_trade_count"] += validation_withheld

    summary = [
        {
            "validation_result_state": group["validation_result_state"],
            "family_count": int(group["family_count"]),
            "candidate_count": int(group["candidate_count"]),
            "validation_seen_count": int(group["validation_seen_count"]),
            "validation_withheld_best_trade_count": int(group["validation_withheld_best_trade_count"]),
            "passive_only": True,
            "influences_action": False,
        }
        for group in groups.values()
    ]
    detail.sort(key=lambda row: (0 if row["candidate_only"] else 1, str(row["validation_result_state"]), str(row["symbol_family"])))
    summary.sort(key=lambda row: (-int(row["candidate_count"]), str(row["validation_result_state"])))
    return detail, summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "dio_mini_passive_reflection_candidate_validation.csv"
    summary_path = output_dir / "dio_mini_passive_reflection_candidate_validation_summary.csv"
    json_path = output_dir / "dio_mini_passive_reflection_candidate_validation.json"
    md_path = output_dir / "dio_mini_passive_reflection_candidate_validation.md"

    _write_csv(detail_path, detail, ["symbol_family", "validation_result_state"])
    _write_csv(summary_path, summary, ["validation_result_state", "family_count"])
    json_path.write_text(
        json.dumps(
            {
                "boundary": {
                    "passive_only": True,
                    "writes_runtime_memory": False,
                    "influences_action": False,
                    "is_gate": False,
                    "is_motoric": False,
                    "is_entry_signal": False,
                },
                "detail": detail,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# DIO Mini Passive Reflection Candidate Validation",
        "",
        "## Grenze",
        "- Validierung, kein Runtime-Speicher",
        "- keine Entry-Wirkung",
        "- keine Gate-Wirkung",
        "- keine Motorik",
        "",
        "## Summary",
    ]
    if not summary:
        lines.append("- keine Zeilen")
    else:
        for row in summary:
            lines.append(
                f"- {row['validation_result_state']}: families={row['family_count']} "
                f"candidates={row['candidate_count']} seen={row['validation_seen_count']} "
                f"withheld_best_trade={row['validation_withheld_best_trade_count']}"
            )
    lines.extend(["", "## Gesehene Kandidaten"])
    for row in [item for item in detail if item["candidate_only"] and item["validation_seen"]][:20]:
        lines.append(
            f"- {row['symbol_family']}: {row['validation_result_state']} "
            f"candidate={row['candidate_state']} validation={row['validation_inner_state']} "
            f"obs={row['validation_observation_count']} withheld={row['validation_withheld_best_trade_count']} "
            f"best={row['validation_best_actions']}"
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate passive Mini-DIO reflection candidates")
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--validation-family-summary", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    detail, summary = build_validation(Path(args.candidates), Path(args.validation_family_summary))
    write_outputs(detail, summary, Path(args.output_dir))
    print(f"detail_rows={len(detail)} summary_rows={len(summary)}")


if __name__ == "__main__":
    main()
