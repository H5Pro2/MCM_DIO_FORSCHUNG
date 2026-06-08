"""Report passive Mini-DIO text-island maturity.

The report reads the separated semantic matrix memory and classifies how text
islands behave across repeated, varied, and foreign worlds. It is diagnostic
only and must not feed action, gates, entries, or direction.
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


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(float(value if value not in (None, "") else default))
    except Exception:
        return default


def _load_memory(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = list(fields)
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=ordered)
        writer.writeheader()
        writer.writerows(rows)


def _state_counts(history: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in history:
        state = str(item.get("development_state", "") or "unknown")
        counts[state] = counts.get(state, 0) + 1
    return counts


def _source_counts(history: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in history:
        source = str(item.get("source_label", "") or "unknown")
        counts[source] = counts.get(source, 0) + 1
    return counts


def _density_values(history: list[dict], fallback: float) -> list[float]:
    values = [_safe_float(item.get("semantic_density"), fallback) for item in history]
    return values or [fallback]


def _maturity_state(
    observations: int,
    state_counts: dict[str, int],
    source_counts: dict[str, int],
    density_stability: float,
    variation_tolerance: float,
    foreign_separation: float,
    drift_pressure: float,
) -> str:
    if observations <= 1:
        return "new_unconfirmed_text_island"
    if foreign_separation > 0.0 and observations <= 1:
        return "foreign_separated_text_island"
    if state_counts.get("drifting_text_island", 0) > 0 and density_stability < 0.55:
        return "drifting_unstable_text_island"
    if variation_tolerance > 0.0 and drift_pressure < 0.35 and density_stability >= 0.45:
        return "variant_resilient_text_island"
    if state_counts.get("reorganizing_text_island", 0) > 0 and density_stability >= 0.35:
        return "reorganizing_but_bearing_text_island"
    if state_counts.get("densifying_text_island", 0) > 0 and observations >= 2:
        return "stable_recurrent_text_island"
    if any("varianteB" in source for source in source_counts):
        return "foreign_separated_text_island"
    return "new_unconfirmed_text_island"


def _maturity_note(row: dict) -> str:
    return (
        f"{row['text_island_symbol']}: {row['text_island_maturity_state']}; "
        f"recur={row['recurrence_count']}; "
        f"var={row['variation_tolerance']:.3f}; "
        f"foreign={row['foreign_separation']:.3f}; "
        f"score={row['semantic_maturity_score']:.3f}; "
        "passiv, keine Handlung."
    )


def build_rows(memory: dict) -> tuple[list[dict], list[dict]]:
    text_islands = dict(memory.get("text_islands", {}) or {})
    rows: list[dict] = []
    for symbol, item in sorted(text_islands.items()):
        history = list(item.get("history", []) or [])
        observations = _safe_int(item.get("observations"), len(history))
        states = _state_counts(history)
        sources = _source_counts(history)
        density = _safe_float(item.get("semantic_density"))
        values = _density_values(history, density)
        density_min = min(values)
        density_max = max(values)
        density_range = max(0.0, density_max - density_min)
        density_stability = max(0.0, min(1.0, 1.0 - density_range))
        recurrence_count = states.get("densifying_text_island", 0) + max(0, observations - 1)
        variation_count = (
            states.get("reorganizing_text_island", 0)
            + states.get("expanding_text_island", 0)
            + states.get("drifting_text_island", 0)
        )
        variation_tolerance = min(1.0, variation_count / max(1, observations))
        foreign_count = sum(count for source, count in sources.items() if "varianteB" in source)
        foreign_separation = min(1.0, foreign_count / max(1, observations))
        reorganization_quality = min(
            1.0,
            (
                states.get("reorganizing_text_island", 0)
                + states.get("expanding_text_island", 0)
                + states.get("densifying_text_island", 0)
            )
            / max(1, observations),
        )
        drift_pressure = min(1.0, states.get("drifting_text_island", 0) / max(1, observations))
        maturity_state = _maturity_state(
            observations,
            states,
            sources,
            density_stability,
            variation_tolerance,
            foreign_separation,
            drift_pressure,
        )
        semantic_maturity_score = max(
            0.0,
            min(
                1.0,
                (
                    (min(1.0, recurrence_count / 3.0) * 0.28)
                    + (density_stability * 0.20)
                    + (variation_tolerance * 0.16)
                    + (reorganization_quality * 0.18)
                    + (foreign_separation * 0.12)
                    - (drift_pressure * 0.14)
                    + (min(1.0, _safe_int(item.get("family_count")) / 12.0) * 0.08)
                ),
            ),
        )
        row = {
            "text_island_symbol": symbol,
            "text_island_maturity_state": maturity_state,
            "observations": observations,
            "family_count": _safe_int(item.get("family_count")),
            "recurrence_count": recurrence_count,
            "density_stability": round(density_stability, 9),
            "variation_tolerance": round(variation_tolerance, 9),
            "foreign_separation": round(foreign_separation, 9),
            "reorganization_quality": round(reorganization_quality, 9),
            "drift_pressure": round(drift_pressure, 9),
            "semantic_density": round(density, 9),
            "semantic_vorticity": round(_safe_float(item.get("semantic_vorticity")), 9),
            "semantic_maturity_score": round(semantic_maturity_score, 9),
            "first_seen_source": item.get("first_seen_source", ""),
            "last_seen_source": item.get("last_seen_source", ""),
            "state_counts": json.dumps(states, sort_keys=True),
            "source_counts": json.dumps(sources, sort_keys=True),
            "families": "|".join(list(item.get("families", []) or [])),
            **PASSIVE_BOUNDARY,
        }
        row["maturity_note"] = _maturity_note(row)
        rows.append(row)

    summary_counts: dict[str, int] = {}
    for row in rows:
        state = str(row["text_island_maturity_state"])
        summary_counts[state] = summary_counts.get(state, 0) + 1
    summary_rows = [
        {
            "text_island_maturity_state": state,
            "count": count,
            **PASSIVE_BOUNDARY,
        }
        for state, count in sorted(summary_counts.items())
    ]
    return rows, summary_rows


def write_outputs(rows: list[dict], summary_rows: list[dict], output_dir: Path, memory_path: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_fields = [
        "text_island_symbol",
        "text_island_maturity_state",
        "observations",
        "family_count",
        "recurrence_count",
        "density_stability",
        "variation_tolerance",
        "foreign_separation",
        "reorganization_quality",
        "drift_pressure",
        "semantic_density",
        "semantic_maturity_score",
        "maturity_note",
    ]
    _write_csv(output_dir / "passive_text_island_maturity.csv", rows, detail_fields)
    _write_csv(
        output_dir / "passive_text_island_maturity_summary.csv",
        summary_rows,
        ["text_island_maturity_state", "count"],
    )
    (output_dir / "passive_text_island_maturity.json").write_text(
        json.dumps(
            {
                "memory": str(memory_path),
                "rows": rows,
                "summary": summary_rows,
                "boundary": PASSIVE_BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Passive Text Island Maturity",
        "",
        f"- memory: `{memory_path}`",
        f"- text_islands: `{len(rows)}`",
        "",
        "## Grenze",
        "",
        "- passiv",
        "- keine Runtime-Lesung",
        "- keine Handlung",
        "- kein Gate",
        "- kein Entry",
        "- keine Richtung",
        "",
        "## Summary",
        "",
    ]
    for row in summary_rows:
        lines.append(f"- {row['text_island_maturity_state']}: {row['count']}")
    lines.extend(["", "## Top-Reife", ""])
    for row in sorted(rows, key=lambda item: float(item["semantic_maturity_score"]), reverse=True)[:30]:
        lines.append(f"- {row['maturity_note']}")
    (output_dir / "passive_text_island_maturity.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (output_dir / "passive_text_island_maturity.txt").write_text(
        "\n".join(row["maturity_note"] for row in rows) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive text-island maturity")
    parser.add_argument("--memory", type=Path, default=Path("bot_memory/dio_mini_semantic_matrix_memory.json"))
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    memory = _load_memory(args.memory)
    rows, summary_rows = build_rows(memory)
    write_outputs(rows, summary_rows, args.output_dir, args.memory)
    print(
        json.dumps(
            {
                "memory": str(args.memory),
                "text_islands": len(rows),
                "summary": {row["text_island_maturity_state"]: row["count"] for row in summary_rows},
                **PASSIVE_BOUNDARY,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
