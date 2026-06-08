"""Compare Mini-DIO families by sensory/MCM vectors across two worlds.

This is a passive kinship report. It compares the averaged seeing/hearing/
feeling vector of each family from one debug root with families from another
debug root. It does not use the family name as proof of identity.

Boundary:
- no memory writes
- no action influence
- no gate
- no hard rule
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path


VECTOR_FIELDS = (
    "sehen_form_flow",
    "sehen_form_stability",
    "sehen_form_change",
    "hoeren_energy_tone",
    "hoeren_energy_shift",
    "fuehlen_mcm_coherence",
    "fuehlen_mcm_tension",
    "fuehlen_mcm_asymmetry",
)


def _safe_float(value: object) -> float:
    try:
        value = float(value or 0.0)
    except Exception:
        value = 0.0
    if value != value:
        value = 0.0
    return value


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _dominant(values: list[str]) -> str:
    counts: dict[str, int] = {}
    for value in values:
        key = str(value or "-")
        counts[key] = counts.get(key, 0) + 1
    if not counts:
        return "-"
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0]


def _load_landkarte(path: Path | None) -> dict[str, dict]:
    if not path or not path.exists():
        return {}
    return {
        str(row.get("symbol_family", "") or ""): row
        for row in _read_csv(path)
        if str(row.get("symbol_family", "") or "")
    }


def _iter_episode_rows(debug_root: Path) -> list[dict]:
    rows: list[dict] = []
    for path in sorted(debug_root.rglob("episodes.csv")):
        rows.extend(_read_csv(path))
    return rows


def _family_vectors(debug_root: Path, landkarte_csv: Path | None = None) -> dict[str, dict]:
    landkarte = _load_landkarte(landkarte_csv)
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in _iter_episode_rows(debug_root):
        family = str(row.get("symbol_family", "") or "")
        if family:
            grouped[family].append(row)

    output: dict[str, dict] = {}
    for family, rows in grouped.items():
        averages = {
            field: sum(_safe_float(row.get(field)) for row in rows) / max(1, len(rows))
            for field in VECTOR_FIELDS
        }
        reward_sum = sum(_safe_float(row.get("reward")) for row in rows)
        event_reward_sum = sum(_safe_float(row.get("event_reward")) for row in rows)
        item = {
            "symbol_family": family,
            "count": len(rows),
            "reward_sum": round(reward_sum, 6),
            "event_reward_sum": round(event_reward_sum, 6),
            "dominant_action": _dominant([str(row.get("action", "") or "") for row in rows]),
            "dominant_outcome": _dominant([str(row.get("outcome_event", "") or "") for row in rows]),
            "vector": averages,
            "inner_landkarte_state": str(landkarte.get(family, {}).get("inner_landkarte_state", "-") or "-"),
            "passive_reflection_state": str(landkarte.get(family, {}).get("passive_reflection_state", "-") or "-"),
        }
        output[family] = item
    return output


def _distance(left: dict, right: dict) -> float:
    return math.sqrt(
        sum(
            (_safe_float(left.get(field)) - _safe_float(right.get(field))) ** 2
            for field in VECTOR_FIELDS
        )
        / max(1, len(VECTOR_FIELDS))
    )


def _similarity(distance: float) -> float:
    return 1.0 / (1.0 + max(0.0, distance))


def _state_class(state: str) -> str:
    state = str(state or "")
    if "trust" in state:
        return "trust"
    if "quiet" in state:
        return "quiet"
    if "shift" in state or "variant" in state:
        return "variant"
    if "single" in state:
        return "single"
    if "caution" in state or "negative" in state:
        return "caution"
    return "open"


def _sentence(row: dict) -> str:
    return (
        f"{row['left_family']} -> {row['right_family']}: sensorische/MCM-Naehe={float(row['similarity']):.6f}; "
        f"links={row['left_landkarte_state']} rechts={row['right_landkarte_state']}; "
        f"Aktion={row['left_action']}->{row['right_action']}."
    )


def build_rows(
    left_debug_root: Path,
    right_debug_root: Path,
    left_landkarte_csv: Path | None,
    right_landkarte_csv: Path | None,
    top_n: int,
) -> tuple[list[dict], list[dict], list[dict]]:
    left_families = _family_vectors(left_debug_root, left_landkarte_csv)
    right_families = _family_vectors(right_debug_root, right_landkarte_csv)

    detail: list[dict] = []
    best: list[dict] = []
    for left_family, left in sorted(left_families.items()):
        candidates = []
        for right_family, right in sorted(right_families.items()):
            distance = _distance(left["vector"], right["vector"])
            row = {
                "left_family": left_family,
                "right_family": right_family,
                "rank": 0,
                "distance": round(distance, 9),
                "similarity": round(_similarity(distance), 9),
                "left_count": int(left["count"]),
                "right_count": int(right["count"]),
                "left_reward_sum": left["reward_sum"],
                "right_reward_sum": right["reward_sum"],
                "left_event_reward_sum": left["event_reward_sum"],
                "right_event_reward_sum": right["event_reward_sum"],
                "left_action": left["dominant_action"],
                "right_action": right["dominant_action"],
                "left_outcome": left["dominant_outcome"],
                "right_outcome": right["dominant_outcome"],
                "left_landkarte_state": left["inner_landkarte_state"],
                "right_landkarte_state": right["inner_landkarte_state"],
                "left_reflection_state": left["passive_reflection_state"],
                "right_reflection_state": right["passive_reflection_state"],
                "left_state_class": _state_class(left["inner_landkarte_state"]),
                "right_state_class": _state_class(right["inner_landkarte_state"]),
                "same_state_class": int(_state_class(left["inner_landkarte_state"]) == _state_class(right["inner_landkarte_state"])),
                "same_action": int(str(left["dominant_action"]) == str(right["dominant_action"])),
                "same_outcome": int(str(left["dominant_outcome"]) == str(right["dominant_outcome"])),
                "passive_only": 1,
            }
            for field in VECTOR_FIELDS:
                row[f"left_{field}"] = round(_safe_float(left["vector"].get(field)), 9)
                row[f"right_{field}"] = round(_safe_float(right["vector"].get(field)), 9)
            candidates.append(row)
        candidates.sort(key=lambda item: (float(item["distance"]), str(item["right_family"])))
        for rank, row in enumerate(candidates[: max(1, int(top_n))], start=1):
            row["rank"] = rank
            row["kinship_sentence"] = _sentence(row)
            detail.append(row)
            if rank == 1:
                best.append(dict(row))

    summary_bucket: dict[str, dict] = {}
    for row in best:
        key = f"{row['left_state_class']}_to_{row['right_state_class']}"
        bucket = summary_bucket.setdefault(
            key,
            {
                "kinship_class": key,
                "family_count": 0,
                "avg_similarity": 0.0,
                "same_action_count": 0,
                "same_outcome_count": 0,
                "families": [],
            },
        )
        bucket["family_count"] += 1
        bucket["avg_similarity"] += float(row["similarity"])
        bucket["same_action_count"] += int(row["same_action"])
        bucket["same_outcome_count"] += int(row["same_outcome"])
        bucket["families"].append(f"{row['left_family']}->{row['right_family']}")

    summary = []
    for row in summary_bucket.values():
        count = max(1, int(row["family_count"]))
        row["avg_similarity"] = round(float(row["avg_similarity"]) / count, 9)
        row["families"] = ",".join(sorted(row["families"]))
        summary.append(row)
    summary.sort(key=lambda item: (str(item["kinship_class"]), str(item["families"])))
    return detail, best, summary


def write_outputs(
    detail: list[dict],
    best: list[dict],
    summary: list[dict],
    output_dir: Path,
    left_debug_root: Path,
    right_debug_root: Path,
    left_label: str,
    right_label: str,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_family_vector_kinship.csv"
    best_csv = output_dir / "dio_mini_passive_family_vector_kinship_best.csv"
    summary_csv = output_dir / "dio_mini_passive_family_vector_kinship_summary.csv"
    json_path = output_dir / "dio_mini_passive_family_vector_kinship.json"
    md_path = output_dir / "dio_mini_passive_family_vector_kinship.md"

    for path, rows, fallback in (
        (detail_csv, detail, ["left_family", "right_family", "rank", "similarity"]),
        (best_csv, best, ["left_family", "right_family", "similarity"]),
        (summary_csv, summary, ["kinship_class", "family_count", "avg_similarity"]),
    ):
        fields = list(rows[0].keys()) if rows else fallback
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    json_path.write_text(
        json.dumps(
            {
                "left_label": left_label,
                "right_label": right_label,
                "left_debug_root": str(left_debug_root),
                "right_debug_root": str(right_debug_root),
                "detail": detail,
                "best": best,
                "summary": summary,
                "boundary": {
                    "writes_memory": False,
                    "influences_action": False,
                    "is_gate": False,
                    "is_motoric": False,
                    "uses_hard_threshold": False,
                },
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# DIO Mini Passive Family Vector Kinship",
        "",
        f"- left: {left_label} ({left_debug_root})",
        f"- right: {right_label} ({right_debug_root})",
        "",
        "## Zusammenfassung",
    ]
    if not summary:
        lines.append("- keine Verwandtschaftsdaten")
    for row in summary:
        lines.append(
            f"- {row['kinship_class']}: families={row['family_count']} "
            f"avg_similarity={row['avg_similarity']} "
            f"same_action={row['same_action_count']} same_outcome={row['same_outcome_count']} "
            f"pairs={row['families'] or '-'}"
        )
    lines.extend(["", "## Beste Naehe je linker Familie"])
    for row in best:
        lines.append(
            f"- {row['left_family']} -> {row['right_family']}: "
            f"similarity={float(row['similarity']):.6f} distance={float(row['distance']):.6f} "
            f"state={row['left_state_class']}->{row['right_state_class']} "
            f"action={row['left_action']}->{row['right_action']} "
            f"outcome={row['left_outcome']}->{row['right_outcome']}"
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Sinnes-/MCM-Verwandtschaft",
            "- kein Memory-Schreiben",
            "- keine Motorik",
            "- kein Gate",
            "- keine harte Regel",
            "- Familiennamen werden nicht als Identitaetsbeweis benutzt",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare passive Mini-DIO family vectors across worlds")
    parser.add_argument("--left-debug-root", required=True)
    parser.add_argument("--right-debug-root", required=True)
    parser.add_argument("--left-landkarte-csv", default="")
    parser.add_argument("--right-landkarte-csv", default="")
    parser.add_argument("--left-label", default="left")
    parser.add_argument("--right-label", default="right")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--top-n", type=int, default=3)
    args = parser.parse_args()
    detail, best, summary = build_rows(
        Path(args.left_debug_root),
        Path(args.right_debug_root),
        Path(args.left_landkarte_csv) if args.left_landkarte_csv else None,
        Path(args.right_landkarte_csv) if args.right_landkarte_csv else None,
        int(args.top_n),
    )
    write_outputs(
        detail,
        best,
        summary,
        Path(args.output_dir),
        Path(args.left_debug_root),
        Path(args.right_debug_root),
        str(args.left_label or "left"),
        str(args.right_label or "right"),
    )
    print(f"passive_family_vector_kinship_rows={len(detail)} best={len(best)} summary={len(summary)}")
    for row in summary:
        print(
            f"{row['kinship_class']} families={row['family_count']} "
            f"avg_similarity={row['avg_similarity']}"
        )


if __name__ == "__main__":
    main()
