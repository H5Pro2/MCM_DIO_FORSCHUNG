"""Detect passive anchor/exchange patterns between two text-island maps.

An anchor/exchange pattern means a text island keeps at least one family while
other families are replaced in a related world. Diagnostic only.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


PASSIVE_BOUNDARY = {
    "passive_only": True,
    "writes_runtime_memory": False,
    "read_by_mini_dio": False,
    "influences_action": False,
    "is_gate": False,
    "is_motoric": False,
    "is_entry_signal": False,
    "is_direction_signal": False,
}


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value if value not in (None, "") else default)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(fallback_fields)
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _families(raw: object) -> set[str]:
    return {item for item in str(raw or "").split("|") if item}


def _state(left: set[str], right: set[str]) -> str:
    if not left and right:
        return "new_text_island"
    if left and not right:
        return "lost_text_island"
    if left == right:
        return "same_family_basis"
    anchor = left & right
    added = right - left
    removed = left - right
    if anchor and added and removed:
        return "anchor_exchange"
    if anchor and added:
        return "anchor_expansion"
    if anchor and removed:
        return "anchor_thinning"
    if not anchor and left and right:
        return "family_basis_replaced"
    return "unknown"


def build_report(left_rows: list[dict], right_rows: list[dict]) -> tuple[list[dict], list[dict]]:
    by_left = {str(row.get("text_island_symbol", "") or ""): row for row in left_rows}
    by_right = {str(row.get("text_island_symbol", "") or ""): row for row in right_rows}
    symbols = sorted(set(by_left) | set(by_right))
    detail: list[dict] = []
    for symbol in symbols:
        left = by_left.get(symbol, {})
        right = by_right.get(symbol, {})
        left_families = _families(left.get("families", ""))
        right_families = _families(right.get("families", ""))
        anchor = left_families & right_families
        added = right_families - left_families
        removed = left_families - right_families
        union = left_families | right_families
        family_stability = len(anchor) / max(1, len(union))
        state = _state(left_families, right_families)
        left_score = _safe_float(left.get("semantic_maturity_score"))
        right_score = _safe_float(right.get("semantic_maturity_score"))
        detail.append(
            {
                "text_island_symbol": symbol,
                "anchor_exchange_state": state,
                "left_inner_state": str(left.get("inner_map_state", "") or "absent"),
                "right_inner_state": str(right.get("inner_map_state", "") or "absent"),
                "left_maturity_state": str(left.get("text_island_maturity_state", "") or "absent"),
                "right_maturity_state": str(right.get("text_island_maturity_state", "") or "absent"),
                "left_score": round(left_score, 9),
                "right_score": round(right_score, 9),
                "score_delta": round(right_score - left_score, 9),
                "family_stability": round(family_stability, 9),
                "anchor_families": "|".join(sorted(anchor)),
                "added_families": "|".join(sorted(added)),
                "removed_families": "|".join(sorted(removed)),
                "left_families": "|".join(sorted(left_families)),
                "right_families": "|".join(sorted(right_families)),
                "dio_anchor_exchange_sentence": (
                    f"{symbol}: {state}; anchor={'|'.join(sorted(anchor)) or '-'}; "
                    f"added={'|'.join(sorted(added)) or '-'}; removed={'|'.join(sorted(removed)) or '-'}; "
                    "passiv, keine Handlung."
                ),
                **PASSIVE_BOUNDARY,
            }
        )

    counts: dict[str, int] = {}
    for row in detail:
        state = str(row.get("anchor_exchange_state", "") or "unknown")
        counts[state] = counts.get(state, 0) + 1
    summary = [
        {
            "summary_group": "anchor_exchange_state",
            "state": state,
            "count": count,
            **PASSIVE_BOUNDARY,
        }
        for state, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]
    exchange = [row for row in detail if row.get("anchor_exchange_state") == "anchor_exchange"]
    summary.append(
        {
            "summary_group": "totals",
            "state": "anchor_exchange",
            "count": len(exchange),
            "avg_family_stability": round(
                sum(_safe_float(row.get("family_stability")) for row in exchange) / max(1, len(exchange)),
                9,
            ),
            "avg_score_delta": round(
                sum(_safe_float(row.get("score_delta")) for row in exchange) / max(1, len(exchange)),
                9,
            ),
            **PASSIVE_BOUNDARY,
        }
    )
    return detail, summary


def write_outputs(detail: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(
        output_dir / "passive_anchor_exchange_lupe.csv",
        detail,
        [
            "text_island_symbol",
            "anchor_exchange_state",
            "left_inner_state",
            "right_inner_state",
            "score_delta",
            "family_stability",
            "anchor_families",
            "added_families",
            "removed_families",
        ],
    )
    _write_csv(
        output_dir / "passive_anchor_exchange_lupe_summary.csv",
        summary,
        ["summary_group", "state", "count", "avg_family_stability", "avg_score_delta"],
    )
    payload = {
        "schema": "dio_mini_passive_anchor_exchange_lupe.v1",
        "boundary": dict(PASSIVE_BOUNDARY),
        "summary": summary,
        "detail": detail,
    }
    (output_dir / "passive_anchor_exchange_lupe.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    lines = [
        "# Mini-DIO Passive Anchor/Exchange Lupe",
        "",
        "## Grenze",
        "- Nur Diagnose.",
        "- Keine Runtime-Lesung.",
        "- Keine Handlung.",
        "- Kein Gate.",
        "- Kein Entry.",
        "- Keine Richtung.",
        "",
        "## Summary",
    ]
    for row in summary:
        extra = ""
        if "avg_family_stability" in row:
            extra = f"; avg_family_stability={row.get('avg_family_stability')}; avg_score_delta={row.get('avg_score_delta')}"
        lines.append(f"- {row.get('summary_group')}:{row.get('state')} = {row.get('count')}{extra}")
    lines.extend(["", "## Anchor Exchange"])
    for row in [item for item in detail if item.get("anchor_exchange_state") == "anchor_exchange"][:40]:
        lines.append(
            f"- {row.get('text_island_symbol')}: anchor={row.get('anchor_families') or '-'}; "
            f"added={row.get('added_families') or '-'}; removed={row.get('removed_families') or '-'}; "
            f"score_delta={row.get('score_delta')}"
        )
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect passive anchor/exchange patterns between text-island maps.")
    parser.add_argument("--left", required=True, type=Path)
    parser.add_argument("--right", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    detail, summary = build_report(_read_csv(args.left), _read_csv(args.right))
    write_outputs(detail, summary, args.output_dir)
    print(
        json.dumps(
            {
                "output_dir": str(args.output_dir),
                "summary": summary,
                **PASSIVE_BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
