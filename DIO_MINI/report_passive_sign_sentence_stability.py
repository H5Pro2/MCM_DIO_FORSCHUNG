"""Report stability of passive sign reflection sentences.

This diagnostic compares passive_sign_reflection_sentences.csv outputs across
multiple evidence states. It is passive only and does not feed Mini-DIO runtime.
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


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value or default)
    except Exception:
        return default
    if result != result:
        return default
    return result


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
    name = name.replace("dio_mini_passive_sign_reflection_sentences_", "")
    name = name.replace("dio_0x52_", "")
    return name or path.stem


def _recent_same(values: list[str], count: int = 2) -> bool:
    if len(values) < count:
        return False
    recent = values[-count:]
    return len(set(recent)) == 1


def _sentence_stability_state(symbols: list[str], kinds: list[str], source_count: int, available: int) -> str:
    if source_count <= 0:
        return "not_seen"
    if source_count == 1:
        return "single_passive_sentence"
    if len(set(symbols)) == 1 and len(set(kinds)) == 1 and source_count == available:
        return "stable_passive_sentence"
    if _recent_same(symbols) and _recent_same(kinds):
        return "recently_stable_passive_sentence"
    return "changing_passive_sentence"


def build_stability(sentence_paths: list[Path]) -> tuple[list[dict], list[dict]]:
    available_sources = len(sentence_paths)
    grouped: dict[tuple[str, str], dict] = {}

    for path in sentence_paths:
        source = _source_label(path)
        for row in _read_csv(path):
            target = str(row.get("target_family", "") or "")
            related = str(row.get("related_family", "") or "")
            if not target or not related:
                continue
            key = (target, related)
            item = grouped.setdefault(
                key,
                {
                    "target_family": target,
                    "related_family": related,
                    "sources": [],
                    "symbols": [],
                    "kinds": [],
                    "sentences": [],
                    "scores": [],
                    "field_overlaps": [],
                    "afterlook_overlaps": [],
                },
            )
            item["sources"].append(source)
            item["symbols"].append(str(row.get("reflection_sentence_symbol", "") or ""))
            item["kinds"].append(str(row.get("reflection_sentence_kind", "") or ""))
            item["sentences"].append(str(row.get("dio_sentence", "") or ""))
            item["scores"].append(_safe_float(row.get("avg_relation_score")))
            item["field_overlaps"].append(_safe_float(row.get("avg_field_overlap")))
            item["afterlook_overlaps"].append(_safe_float(row.get("avg_action_overlap")))

    rows: list[dict] = []
    groups: dict[str, dict] = {}
    for item in grouped.values():
        source_count = len(set(item["sources"]))
        state = _sentence_stability_state(item["symbols"], item["kinds"], source_count, available_sources)
        latest_symbol = item["symbols"][-1] if item["symbols"] else ""
        latest_kind = item["kinds"][-1] if item["kinds"] else ""
        latest_sentence = item["sentences"][-1] if item["sentences"] else ""
        row = {
            "target_family": item["target_family"],
            "related_family": item["related_family"],
            "sentence_stability_state": state,
            "sentence_source_count": source_count,
            "available_sentence_sources": available_sources,
            "sentence_sources": "|".join(item["sources"]),
            "latest_sentence_symbol": latest_symbol,
            "symbol_history": "|".join(item["symbols"]),
            "latest_sentence_kind": latest_kind,
            "kind_history": "|".join(item["kinds"]),
            "avg_relation_score": round(sum(item["scores"]) / max(1, len(item["scores"])), 6),
            "latest_relation_score": round(item["scores"][-1] if item["scores"] else 0.0, 6),
            "avg_field_overlap": round(sum(item["field_overlaps"]) / max(1, len(item["field_overlaps"])), 6),
            "latest_field_overlap": round(item["field_overlaps"][-1] if item["field_overlaps"] else 0.0, 6),
            "avg_afterlook_overlap": round(sum(item["afterlook_overlaps"]) / max(1, len(item["afterlook_overlaps"])), 6),
            "latest_sentence": latest_sentence,
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
                "sentence_stability_state": state,
                "sentence_count": 0,
                "families": [],
            },
        )
        group["sentence_count"] += 1
        group["families"].append(f"{item['target_family']}->{item['related_family']}")

    rows.sort(
        key=lambda row: (
            row["sentence_stability_state"] != "stable_passive_sentence",
            row["sentence_stability_state"] != "recently_stable_passive_sentence",
            -int(row["sentence_source_count"]),
            -float(row["latest_relation_score"]),
            str(row["target_family"]),
            str(row["related_family"]),
        )
    )
    summary = [
        {
            "sentence_stability_state": group["sentence_stability_state"],
            "sentence_count": int(group["sentence_count"]),
            "families": "|".join(sorted(group["families"])),
            "passive_only": True,
            "influences_action": False,
        }
        for group in groups.values()
    ]
    summary.sort(key=lambda row: (-int(row["sentence_count"]), str(row["sentence_stability_state"])))
    return rows, summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(rows: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "passive_sign_sentence_stability.csv"
    summary_path = output_dir / "passive_sign_sentence_stability_summary.csv"
    json_path = output_dir / "passive_sign_sentence_stability.json"
    md_path = output_dir / "passive_sign_sentence_stability.md"
    _write_csv(detail_path, rows, ["target_family", "related_family", "sentence_stability_state"])
    _write_csv(summary_path, summary, ["sentence_stability_state", "sentence_count"])
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
                "sentences": rows,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Passive Sign Sentence Stability",
        "",
        "## Grenze",
        "- passiv",
        "- keine Runtime-Lesung",
        "- keine Handlung",
        "- keine Richtung",
        "",
        "## Summary",
    ]
    for row in summary:
        lines.append(f"- {row['sentence_stability_state']}: {row['sentence_count']} {row['families']}")
    lines.extend(["", "## Sentences"])
    for row in rows[:20]:
        lines.append(
            f"- {row['target_family']}->{row['related_family']}: {row['sentence_stability_state']} "
            f"{row['latest_sentence_symbol']} | {row['latest_sentence']}"
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Report passive sign sentence stability")
    parser.add_argument("--sentences", nargs="+", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    rows, summary = build_stability(_expand_patterns(args.sentences))
    write_outputs(rows, summary, Path(args.output_dir))
    print(f"sentence_sources={len(args.sentences)} sentences={len(rows)} summary_rows={len(summary)}")
    for row in rows[:8]:
        print(
            f"{row['target_family']}->{row['related_family']} "
            f"{row['sentence_stability_state']} {row['latest_sentence_symbol']}"
        )


if __name__ == "__main__":
    main()
