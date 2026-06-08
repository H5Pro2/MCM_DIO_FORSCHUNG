"""Trace selected dio_* families across passive inner-map stages.

This report is diagnostic only. It follows selected families through existing
text-island inner maps and shows whether they stay stable, drift, disappear or
reappear through new text islands.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


PASSIVE_FLAGS = {
    "passive_only": True,
    "writes_runtime_memory": False,
    "read_by_mini_dio": False,
    "influences_action": False,
    "is_gate": False,
    "is_motoric": False,
    "is_entry_signal": False,
    "is_direction_signal": False,
}


def _safe_float(value: Any) -> float:
    try:
        return float(value or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def _parse_stage(raw: str) -> tuple[str, Path]:
    if "=" not in raw:
        raise ValueError(f"Stage must use LABEL=PATH, got {raw!r}")
    label, path = raw.split("=", 1)
    return label.strip(), Path(path.strip())


def _families(row: dict[str, str]) -> set[str]:
    return {item for item in str(row.get("families", "") or "").split("|") if item}


def _stage_motion_state(score_delta: float, state: str, found: bool) -> str:
    if not found:
        return "family_not_visible"
    if "drift" in state:
        return "family_drift_phase"
    if score_delta > 0.055:
        return "family_strengthening_phase"
    if score_delta < -0.055:
        return "family_softening_phase"
    return "family_carried_phase"


def build_rows(families: list[str], stages: list[tuple[str, Path]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    detail_rows: list[dict[str, Any]] = []
    previous_score: dict[str, float | None] = {family: None for family in families}
    previous_text: dict[str, str] = {family: "" for family in families}

    for order, (stage_label, path) in enumerate(stages, start=1):
        rows = _read_csv(path)
        for family in families:
            matches = [row for row in rows if family in _families(row)]
            if matches:
                score = round(mean(_safe_float(row.get("semantic_maturity_score")) for row in matches), 9)
                stability = round(mean(_safe_float(row.get("stability_pressure")) for row in matches), 9)
                variation = round(mean(_safe_float(row.get("variation_bearing")) for row in matches), 9)
                drift = round(mean(_safe_float(row.get("drift_pressure")) for row in matches), 9)
                text_islands = "|".join(sorted(str(row.get("text_island_symbol", "") or "") for row in matches))
                inner_states = "|".join(sorted({str(row.get("inner_map_state", "") or "") for row in matches}))
                maturity_states = "|".join(
                    sorted({str(row.get("text_island_maturity_state", "") or "") for row in matches})
                )
                prior_score = previous_score.get(family)
                score_delta = round(score - prior_score, 9) if prior_score is not None else 0.0
                text_changed = bool(previous_text.get(family) and previous_text[family] != text_islands)
                previous_score[family] = score
                previous_text[family] = text_islands
                found = True
            else:
                score = 0.0
                stability = 0.0
                variation = 0.0
                drift = 0.0
                text_islands = ""
                inner_states = ""
                maturity_states = ""
                score_delta = 0.0
                text_changed = False
                found = False
            detail_rows.append(
                {
                    "stage_order": order,
                    "stage_label": stage_label,
                    "family": family,
                    "found": found,
                    "match_count": len(matches),
                    "text_islands": text_islands,
                    "text_changed_from_previous": text_changed,
                    "inner_map_states": inner_states,
                    "maturity_states": maturity_states,
                    "semantic_maturity_score": score,
                    "score_delta_from_previous": score_delta,
                    "stability_pressure": stability,
                    "variation_bearing": variation,
                    "drift_pressure": drift,
                    "lineage_motion_state": _stage_motion_state(score_delta, inner_states, found),
                    **PASSIVE_FLAGS,
                }
            )

    summary_rows: list[dict[str, Any]] = []
    by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in detail_rows:
        by_family[str(row["family"])].append(row)
    for family, items in sorted(by_family.items()):
        found_items = [row for row in items if row["found"]]
        scores = [_safe_float(row["semantic_maturity_score"]) for row in found_items]
        visible_stages = [str(row["stage_label"]) for row in found_items]
        text_sequence = [str(row["text_islands"]) for row in found_items if row["text_islands"]]
        summary_rows.append(
            {
                "family": family,
                "visible_stage_count": len(found_items),
                "visible_stages": "|".join(visible_stages),
                "unique_text_island_count": len(set(text_sequence)),
                "text_island_sequence": " -> ".join(text_sequence),
                "first_score": round(scores[0], 9) if scores else 0.0,
                "last_score": round(scores[-1], 9) if scores else 0.0,
                "score_delta_first_to_last": round((scores[-1] - scores[0]), 9) if len(scores) >= 2 else 0.0,
                "max_score": round(max(scores), 9) if scores else 0.0,
                "min_score": round(min(scores), 9) if scores else 0.0,
                "has_drift_phase": any("drift" in str(row["inner_map_states"]) for row in found_items),
                "has_text_change": len(set(text_sequence)) > 1,
                **PASSIVE_FLAGS,
            }
        )
    return detail_rows, summary_rows


def _write_markdown(output_dir: Path, detail_rows: list[dict[str, Any]], summary_rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Passive Family Bridge Lineage",
        "",
        "Dieser Bericht verfolgt ausgewaehlte dio_* Familien ueber passive Inner-Maps.",
        "",
        "## Zusammenfassung",
    ]
    for row in summary_rows:
        lines.append(
            "- {family}: visible={visible}, texts={texts}, delta={delta}, drift={drift}, sequence={seq}".format(
                family=row["family"],
                visible=row["visible_stage_count"],
                texts=row["unique_text_island_count"],
                delta=row["score_delta_first_to_last"],
                drift=row["has_drift_phase"],
                seq=row["text_island_sequence"],
            )
        )
    lines.append("")
    lines.append("## Verlauf")
    for row in detail_rows:
        if not row["found"]:
            continue
        lines.append(
            "- {stage} / {family}: {text}; state={state}; score={score}; delta={delta}".format(
                stage=row["stage_label"],
                family=row["family"],
                text=row["text_islands"],
                state=row["inner_map_states"],
                score=row["semantic_maturity_score"],
                delta=row["score_delta_from_previous"],
            )
        )
    lines.append("")
    lines.append("## Wirkungsgrenze")
    lines.append("- keine Runtime-Lesung")
    lines.append("- keine Handlung")
    lines.append("- kein Gate")
    lines.append("- kein Entry-Signal")
    lines.append("- kein Richtungssignal")
    text = "\n".join(lines)
    (output_dir / "passive_family_bridge_lineage.md").write_text(text, encoding="utf-8")
    (output_dir / "passive_family_bridge_lineage.txt").write_text(text, encoding="utf-8")


def run(families: list[str], stages: list[tuple[str, Path]], output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_rows, summary_rows = build_rows(families, stages)
    detail_fields = [
        "stage_order",
        "stage_label",
        "family",
        "found",
        "match_count",
        "text_islands",
        "text_changed_from_previous",
        "inner_map_states",
        "maturity_states",
        "semantic_maturity_score",
        "score_delta_from_previous",
        "stability_pressure",
        "variation_bearing",
        "drift_pressure",
        "lineage_motion_state",
        *PASSIVE_FLAGS.keys(),
    ]
    summary_fields = [
        "family",
        "visible_stage_count",
        "visible_stages",
        "unique_text_island_count",
        "text_island_sequence",
        "first_score",
        "last_score",
        "score_delta_first_to_last",
        "max_score",
        "min_score",
        "has_drift_phase",
        "has_text_change",
        *PASSIVE_FLAGS.keys(),
    ]
    _write_csv(output_dir / "passive_family_bridge_lineage.csv", detail_rows, detail_fields)
    _write_csv(output_dir / "passive_family_bridge_lineage_summary.csv", summary_rows, summary_fields)
    payload = {
        "schema": "dio_mini_passive_family_bridge_lineage.v1",
        "families": families,
        "stages": [{"label": label, "path": str(path)} for label, path in stages],
        "rows": detail_rows,
        "summary": summary_rows,
        **PASSIVE_FLAGS,
    }
    (output_dir / "passive_family_bridge_lineage.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    _write_markdown(output_dir, detail_rows, summary_rows)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Trace passive Mini-DIO family bridge lineage")
    parser.add_argument("--family", action="append", required=True)
    parser.add_argument(
        "--stage",
        action="append",
        required=True,
        help="Stage mapping in the form LABEL=path/to/passive_text_island_inner_map.csv",
    )
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = run(list(args.family or []), [_parse_stage(item) for item in args.stage], Path(args.output_dir))
    print(
        f"family_bridge_lineage families={len(result['families'])} "
        f"stages={len(result['stages'])} output={args.output_dir}"
    )


if __name__ == "__main__":
    main()
