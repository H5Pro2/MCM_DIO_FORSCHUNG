"""Compare passive Mini-DIO transfer learning notes across variants.

This report stays diagnostic. It checks whether passive transfer note kinds
repeat across several controlled worlds without writing training memory or
changing action.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


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


def _parse_source(spec: str) -> tuple[str, Path]:
    if "=" in spec:
        label, path = spec.split("=", 1)
        return label.strip() or Path(path).parent.name, Path(path)
    path = Path(spec)
    return path.parent.name, path


def build_report(sources: list[tuple[str, Path]]) -> tuple[list[dict], list[dict], list[dict]]:
    detail: list[dict] = []
    by_kind: dict[str, dict] = {}
    by_pair: dict[str, dict] = {}

    for label, path in sources:
        rows = _read_csv(path)
        for row in rows:
            kind = str(row.get("learning_note_kind", "") or "note_unknown")
            pair = f"{row.get('left_family', '')}->{row.get('right_family', '')}"
            item = {
                "source_label": label,
                "learning_note_kind": kind,
                "left_family": str(row.get("left_family", "") or ""),
                "right_family": str(row.get("right_family", "") or ""),
                "pair": pair,
                "transfer_reife": round(_safe_float(row.get("transfer_reife")), 9),
                "sensory_mcm_similarity": round(_safe_float(row.get("sensory_mcm_similarity")), 9),
                "left_action": str(row.get("left_action", "") or ""),
                "right_action": str(row.get("right_action", "") or ""),
                "left_outcome": str(row.get("left_outcome", "") or ""),
                "right_outcome": str(row.get("right_outcome", "") or ""),
                "inner_learning_note": str(row.get("inner_learning_note", "") or ""),
                "passive_only": 1,
            }
            detail.append(item)

            kind_bucket = by_kind.setdefault(
                kind,
                {
                    "learning_note_kind": kind,
                    "source_count": 0,
                    "note_count": 0,
                    "avg_transfer_reife": 0.0,
                    "avg_similarity": 0.0,
                    "sources": set(),
                    "pairs": [],
                    "stability_reading": "",
                },
            )
            kind_bucket["source_count"] = 0
            kind_bucket["note_count"] += 1
            kind_bucket["avg_transfer_reife"] += item["transfer_reife"]
            kind_bucket["avg_similarity"] += item["sensory_mcm_similarity"]
            kind_bucket["sources"].add(label)
            kind_bucket["pairs"].append(pair)

            pair_bucket = by_pair.setdefault(
                pair,
                {
                    "pair": pair,
                    "source_count": 0,
                    "note_count": 0,
                    "learning_note_kinds": set(),
                    "sources": set(),
                    "avg_transfer_reife": 0.0,
                    "avg_similarity": 0.0,
                },
            )
            pair_bucket["note_count"] += 1
            pair_bucket["avg_transfer_reife"] += item["transfer_reife"]
            pair_bucket["avg_similarity"] += item["sensory_mcm_similarity"]
            pair_bucket["learning_note_kinds"].add(kind)
            pair_bucket["sources"].add(label)

    kind_summary: list[dict] = []
    for bucket in by_kind.values():
        count = max(1, int(bucket["note_count"]))
        sources_set = set(bucket["sources"])
        source_count = len(sources_set)
        if source_count >= 2:
            reading = "note_kind_repeats_across_variants"
        elif count > 1:
            reading = "note_kind_repeats_inside_one_variant"
        else:
            reading = "note_kind_single_variant"
        kind_summary.append(
            {
                "learning_note_kind": bucket["learning_note_kind"],
                "source_count": source_count,
                "note_count": count,
                "avg_transfer_reife": round(float(bucket["avg_transfer_reife"]) / count, 9),
                "avg_similarity": round(float(bucket["avg_similarity"]) / count, 9),
                "sources": ",".join(sorted(sources_set)),
                "pairs": ",".join(sorted(set(bucket["pairs"]))),
                "stability_reading": reading,
                "passive_only": 1,
            }
        )

    pair_summary: list[dict] = []
    for bucket in by_pair.values():
        count = max(1, int(bucket["note_count"]))
        sources_set = set(bucket["sources"])
        pair_summary.append(
            {
                "pair": bucket["pair"],
                "source_count": len(sources_set),
                "note_count": count,
                "learning_note_kinds": ",".join(sorted(bucket["learning_note_kinds"])),
                "sources": ",".join(sorted(sources_set)),
                "avg_transfer_reife": round(float(bucket["avg_transfer_reife"]) / count, 9),
                "avg_similarity": round(float(bucket["avg_similarity"]) / count, 9),
                "passive_only": 1,
            }
        )

    detail.sort(key=lambda item: (str(item["source_label"]), str(item["learning_note_kind"]), str(item["pair"])))
    kind_summary.sort(key=lambda item: (-int(item["source_count"]), -int(item["note_count"]), str(item["learning_note_kind"])))
    pair_summary.sort(key=lambda item: (-int(item["source_count"]), -int(item["note_count"]), str(item["pair"])))
    return detail, kind_summary, pair_summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(
    detail: list[dict],
    kind_summary: list[dict],
    pair_summary: list[dict],
    sources: list[tuple[str, Path]],
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = output_dir / "dio_mini_passive_transfer_note_stability.csv"
    kind_csv = output_dir / "dio_mini_passive_transfer_note_stability_by_kind.csv"
    pair_csv = output_dir / "dio_mini_passive_transfer_note_stability_by_pair.csv"
    json_path = output_dir / "dio_mini_passive_transfer_note_stability.json"
    md_path = output_dir / "dio_mini_passive_transfer_note_stability.md"

    _write_csv(detail_csv, detail, ["source_label", "learning_note_kind", "pair"])
    _write_csv(kind_csv, kind_summary, ["learning_note_kind", "source_count", "note_count"])
    _write_csv(pair_csv, pair_summary, ["pair", "source_count", "note_count"])

    json_path.write_text(
        json.dumps(
            {
                "sources": [{"label": label, "path": str(path)} for label, path in sources],
                "detail": detail,
                "kind_summary": kind_summary,
                "pair_summary": pair_summary,
                "boundary": {
                    "writes_training_memory": False,
                    "influences_action": False,
                    "is_gate": False,
                    "is_motoric": False,
                    "is_hard_rule": False,
                },
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = ["# DIO Mini Passive Transfer Note Stability", ""]
    lines.append("## Quellen")
    for label, path in sources:
        lines.append(f"- {label}: {path}")
    lines.extend(["", "## Notiztypen"])
    if not kind_summary:
        lines.append("- keine Notiztypen")
    for row in kind_summary:
        lines.append(
            f"- {row['learning_note_kind']}: sources={row['source_count']} notes={row['note_count']} "
            f"avg_transfer_reife={row['avg_transfer_reife']} avg_similarity={row['avg_similarity']} "
            f"reading={row['stability_reading']}"
        )
    lines.extend(["", "## Wiederkehrende Paare"])
    repeated_pairs = [row for row in pair_summary if int(row["source_count"]) >= 2]
    if not repeated_pairs:
        lines.append("- keine identischen Familienpaare ueber mehrere Varianten; Vergleich bleibt ueber Notiztyp und Vektornaehe.")
    for row in repeated_pairs:
        lines.append(
            f"- {row['pair']}: sources={row['source_count']} notes={row['note_count']} "
            f"kinds={row['learning_note_kinds']} avg_transfer_reife={row['avg_transfer_reife']}"
        )
    lines.extend(
        [
            "",
            "## Grenze",
            "- passive Stabilitaetsdiagnose",
            "- keine Handlung",
            "- kein Trainingsmemory",
            "- kein Gate",
            "- keine harte Regel",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare passive Mini-DIO transfer learning notes")
    parser.add_argument("--source", action="append", required=True, help="label=path or path; can be repeated")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    sources = [_parse_source(spec) for spec in args.source]
    detail, kind_summary, pair_summary = build_report(sources)
    write_outputs(detail, kind_summary, pair_summary, sources, Path(args.output_dir))
    print(
        f"passive_transfer_note_stability_rows={len(detail)} "
        f"kinds={len(kind_summary)} pairs={len(pair_summary)}"
    )
    for row in kind_summary:
        print(
            f"{row['learning_note_kind']} sources={row['source_count']} "
            f"notes={row['note_count']} reading={row['stability_reading']}"
        )


if __name__ == "__main__":
    main()
