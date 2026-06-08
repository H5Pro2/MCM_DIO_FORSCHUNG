"""Compare two passive Mini-DIO inner-state maps.

This report checks whether a controlled follow-up world repeats the same
families, shifts to new families, or keeps similar inner-state classes. It is
diagnostic only: no memory writes, no action influence, no gate.
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


def _state_class(state: str) -> str:
    state = str(state or "")
    if "trust" in state:
        return "trust"
    if "quiet" in state:
        return "quiet"
    if "caution" in state or "negative" in state:
        return "caution"
    if "shift" in state or "variant" in state:
        return "variant"
    if "single" in state:
        return "single"
    return "open"


def _load_map(path: Path) -> dict[str, dict]:
    return {
        str(row.get("symbol_family", "") or ""): row
        for row in _read_csv(path)
        if str(row.get("symbol_family", "") or "")
    }


def _classify(left: dict | None, right: dict | None) -> str:
    if left and right:
        left_class = _state_class(str(left.get("inner_landkarte_state", "") or ""))
        right_class = _state_class(str(right.get("inner_landkarte_state", "") or ""))
        if left_class == right_class:
            return f"same_family_same_{left_class}"
        return f"same_family_shift_{left_class}_to_{right_class}"
    if left:
        return f"left_only_{_state_class(str(left.get('inner_landkarte_state', '') or ''))}"
    if right:
        return f"right_only_{_state_class(str(right.get('inner_landkarte_state', '') or ''))}"
    return "missing"


def _sentence(family: str, compare_state: str) -> str:
    if compare_state.startswith("same_family_same_trust"):
        return f"{family}: gleiche Familie bleibt in beiden Welten getragen."
    if compare_state.startswith("same_family_same_quiet"):
        return f"{family}: gleiche Familie bleibt in beiden Welten ruhig beobachtend."
    if compare_state.startswith("same_family_shift"):
        return f"{family}: gleiche Familie bleibt erkennbar, aber der Innenzustand wechselt."
    if compare_state.startswith("left_only_trust"):
        return f"{family}: war links getragen, taucht rechts aber nicht als gleiche Syntaxfamilie auf."
    if compare_state.startswith("right_only_trust"):
        return f"{family}: entsteht rechts als getragene Familie neu."
    if compare_state.startswith("right_only_variant"):
        return f"{family}: entsteht rechts als Variante/Uebergang neu."
    if compare_state.startswith("left_only_quiet"):
        return f"{family}: war links ruhige Beobachtung, taucht rechts nicht als gleiche Syntaxfamilie auf."
    if compare_state.startswith("right_only_quiet"):
        return f"{family}: entsteht rechts als ruhige Beobachtung neu."
    return f"{family}: Vergleichszustand={compare_state}."


def build_rows(left_csv: Path, right_csv: Path, left_label: str, right_label: str) -> tuple[list[dict], list[dict]]:
    left = _load_map(left_csv)
    right = _load_map(right_csv)
    families = sorted(set(left) | set(right))
    detail: list[dict] = []
    summary: dict[str, dict] = {}
    for family in families:
        left_row = left.get(family)
        right_row = right.get(family)
        compare_state = _classify(left_row, right_row)
        item = {
            "symbol_family": family,
            "compare_state": compare_state,
            "left_label": left_label,
            "right_label": right_label,
            "left_landkarte_state": str((left_row or {}).get("inner_landkarte_state", "-") or "-"),
            "right_landkarte_state": str((right_row or {}).get("inner_landkarte_state", "-") or "-"),
            "left_reflection_state": str((left_row or {}).get("passive_reflection_state", "-") or "-"),
            "right_reflection_state": str((right_row or {}).get("passive_reflection_state", "-") or "-"),
            "left_runs": str((left_row or {}).get("runs", "-") or "-"),
            "right_runs": str((right_row or {}).get("runs", "-") or "-"),
            "left_reward_sum": round(_safe_float((left_row or {}).get("reward_sum")), 6),
            "right_reward_sum": round(_safe_float((right_row or {}).get("reward_sum")), 6),
            "left_identical_repeat": _safe_int((left_row or {}).get("identical_repeat")),
            "right_identical_repeat": _safe_int((right_row or {}).get("identical_repeat")),
            "compare_sentence": _sentence(family, compare_state),
            "passive_only": 1,
        }
        detail.append(item)
        bucket = summary.setdefault(
            compare_state,
            {
                "compare_state": compare_state,
                "family_count": 0,
                "left_reward_sum": 0.0,
                "right_reward_sum": 0.0,
                "families": [],
            },
        )
        bucket["family_count"] += 1
        bucket["left_reward_sum"] += item["left_reward_sum"]
        bucket["right_reward_sum"] += item["right_reward_sum"]
        bucket["families"].append(family)

    detail.sort(key=lambda item: (str(item["compare_state"]), str(item["symbol_family"])))
    summary_rows = []
    for row in summary.values():
        row["left_reward_sum"] = round(float(row["left_reward_sum"]), 6)
        row["right_reward_sum"] = round(float(row["right_reward_sum"]), 6)
        row["families"] = ",".join(sorted(row["families"]))
        summary_rows.append(row)
    summary_rows.sort(key=lambda item: (str(item["compare_state"]), str(item["families"])))
    return detail, summary_rows


def write_outputs(
    detail: list[dict],
    summary: list[dict],
    output_dir: Path,
    left_csv: Path,
    right_csv: Path,
    left_label: str,
    right_label: str,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_inner_state_landkarte_compare.csv"
    summary_csv = output_dir / "dio_mini_passive_inner_state_landkarte_compare_summary.csv"
    json_path = output_dir / "dio_mini_passive_inner_state_landkarte_compare.json"
    md_path = output_dir / "dio_mini_passive_inner_state_landkarte_compare.md"

    detail_fields = list(detail[0].keys()) if detail else ["symbol_family", "compare_state"]
    with detail_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail)

    summary_fields = list(summary[0].keys()) if summary else ["compare_state", "family_count"]
    with summary_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)

    json_path.write_text(
        json.dumps(
            {
                "left_label": left_label,
                "right_label": right_label,
                "left_source": str(left_csv),
                "right_source": str(right_csv),
                "detail": detail,
                "summary": summary,
                "boundary": {
                    "writes_memory": False,
                    "influences_action": False,
                    "is_gate": False,
                    "is_motoric": False,
                },
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# DIO Mini Passive Inner State Landkarte Compare",
        "",
        f"- left: {left_label} ({left_csv})",
        f"- right: {right_label} ({right_csv})",
        "",
        "## Zusammenfassung",
    ]
    if not summary:
        lines.append("- keine Vergleichsdaten")
    for row in summary:
        lines.append(
            f"- {row['compare_state']}: families={row['family_count']} "
            f"left_reward={row['left_reward_sum']} right_reward={row['right_reward_sum']} "
            f"families_list={row['families'] or '-'}"
        )
    lines.extend(["", "## Familien"])
    for row in detail:
        lines.append(
            f"- {row['symbol_family']}: {row['compare_state']}; "
            f"left={row['left_landkarte_state']} right={row['right_landkarte_state']}; "
            f"left_reward={float(row['left_reward_sum']):.6f} right_reward={float(row['right_reward_sum']):.6f}"
        )
        lines.append(f"  {row['compare_sentence']}")
    lines.extend(
        [
            "",
            "## Grenze",
            "- passiver Vergleich",
            "- kein Memory-Schreiben",
            "- keine Motorik",
            "- kein Gate",
            "- keine harte Regel",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare two passive Mini-DIO inner-state maps")
    parser.add_argument("--left-csv", required=True)
    parser.add_argument("--right-csv", required=True)
    parser.add_argument("--left-label", default="left")
    parser.add_argument("--right-label", default="right")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    detail, summary = build_rows(
        Path(args.left_csv),
        Path(args.right_csv),
        str(args.left_label or "left"),
        str(args.right_label or "right"),
    )
    write_outputs(
        detail,
        summary,
        Path(args.output_dir),
        Path(args.left_csv),
        Path(args.right_csv),
        str(args.left_label or "left"),
        str(args.right_label or "right"),
    )
    print(f"passive_landkarte_compare_rows={len(detail)} summary={len(summary)}")
    for row in summary:
        print(
            f"{row['compare_state']} families={row['family_count']} "
            f"left_reward={row['left_reward_sum']} right_reward={row['right_reward_sum']}"
        )


if __name__ == "__main__":
    main()
