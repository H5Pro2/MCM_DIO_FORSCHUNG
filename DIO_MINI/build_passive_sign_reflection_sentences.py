"""Build passive reflection sentences from stable Mini-DIO sign relations.

The output is a readable diagnostic map. It does not write runtime memory and
does not influence action, direction, entries, or gates.
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


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value or default)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(float(value or default))
    except Exception:
        return default


def _base36(number: int) -> str:
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    number = abs(int(number))
    if number == 0:
        return "0"
    chars: list[str] = []
    while number:
        number, rem = divmod(number, 36)
        chars.append(alphabet[rem])
    return "".join(reversed(chars))


def _sentence_symbol(target_family: str, related_family: str, relation_state: str) -> str:
    hash_value = 2166136261
    for text in (target_family, related_family, relation_state):
        for char in str(text or ""):
            hash_value ^= ord(char)
            hash_value = (hash_value * 16777619) & 0xFFFFFFFF
    return f"dio_reflect_{_base36(hash_value).rjust(7, '0')}"


def _index_signs(rows: list[dict]) -> dict[str, dict]:
    return {str(row.get("symbol_family", "") or ""): dict(row) for row in rows}


def _reflection_kind(row: dict) -> str:
    state = str(row.get("relation_stability_state", "") or "")
    related_state = str(row.get("related_sign_states", "") or "")
    field_overlap = _safe_float(row.get("avg_field_overlap"))
    if state == "recurring_strong_passive_relation" and "known_lage_direction_candidate" in related_state:
        return "open_lage_near_direction_candidate"
    if state.startswith("recurring_") and field_overlap > 0.0:
        return "recurring_field_neighbor"
    if state.startswith("recurring_"):
        return "recurring_loose_neighbor"
    return "single_passive_neighbor"


def _dio_sentence(kind: str, target: dict, related: dict, row: dict) -> str:
    target_family = str(row.get("target_family", "") or "-")
    related_family = str(row.get("related_family", "") or "-")
    source_count = _safe_int(row.get("relation_source_count"))
    available = _safe_int(row.get("available_relation_sources"))
    field_overlap = _safe_float(row.get("avg_field_overlap"))
    afterlook_overlap = _safe_float(row.get("avg_action_overlap"))

    target_state = str(target.get("sign_state", row.get("target_sign_state", "")) or "")
    related_state = str(related.get("sign_state", row.get("related_sign_states", "")) or "")

    if kind == "open_lage_near_direction_candidate":
        return (
            f"{target_family}: Ich erkenne diese Lage als offen. "
            f"Sie liegt stabil nahe bei {related_family}, einem Richtungskandidaten. "
            f"Ich pruefe weiter und handle daraus nicht automatisch."
        )
    if kind == "recurring_field_neighbor":
        return (
            f"{target_family}: Ich kenne eine wiederkehrende Naehe zu {related_family}. "
            f"Die Beziehung ist passiv ({source_count}/{available}), Feldnaehe={field_overlap:.3f}, "
            f"Nachblickueberlappung={afterlook_overlap:.3f}. Ich halte sie als Orientierung, nicht als Handlung."
        )
    if kind == "recurring_loose_neighbor":
        return (
            f"{target_family}: Ich sehe eine wiederkehrende Randnaehe zu {related_family}. "
            f"Die Feldnaehe traegt hier nicht ({field_overlap:.3f}); "
            f"ich notiere sie nur als schwache Randspur."
        )
    return (
        f"{target_family}: Ich sehe eine einzelne Naehe zu {related_family}. "
        f"Das ist noch keine Reife und bleibt Beobachtung. "
        f"Zielzustand={target_state or '-'}, Nachbarzustand={related_state or '-'}."
    )


def build_sentences(relation_rows: list[dict], sign_rows: list[dict]) -> tuple[list[dict], list[dict]]:
    signs = _index_signs(sign_rows)
    output: list[dict] = []
    groups: dict[str, dict] = {}

    for row in relation_rows:
        target_family = str(row.get("target_family", "") or "")
        related_family = str(row.get("related_family", "") or "")
        if not target_family or not related_family:
            continue
        kind = _reflection_kind(row)
        target = signs.get(target_family, {})
        related = signs.get(related_family, {})
        symbol = _sentence_symbol(target_family, related_family, kind)
        item = {
            "reflection_sentence_symbol": symbol,
            "target_family": target_family,
            "target_sign_symbol": str(target.get("passive_sign_symbol", "") or ""),
            "target_sign_state": str(target.get("sign_state", "") or ""),
            "related_family": related_family,
            "related_sign_symbol": str(related.get("passive_sign_symbol", "") or ""),
            "related_sign_state": str(related.get("sign_state", row.get("related_sign_states", "")) or ""),
            "reflection_sentence_kind": kind,
            "relation_stability_state": str(row.get("relation_stability_state", "") or ""),
            "relation_source_count": _safe_int(row.get("relation_source_count")),
            "available_relation_sources": _safe_int(row.get("available_relation_sources")),
            "avg_relation_score": round(_safe_float(row.get("avg_relation_score")), 6),
            "avg_field_overlap": round(_safe_float(row.get("avg_field_overlap")), 6),
            "avg_action_overlap": round(_safe_float(row.get("avg_action_overlap")), 6),
            "dio_sentence": _dio_sentence(kind, target, related, row),
            "passive_only": True,
            "writes_runtime_memory": False,
            "read_by_mini_dio": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
            "is_entry_signal": False,
            "is_direction_signal": False,
        }
        output.append(item)
        group = groups.setdefault(
            kind,
            {
                "reflection_sentence_kind": kind,
                "sentence_count": 0,
                "families": [],
            },
        )
        group["sentence_count"] += 1
        group["families"].append(f"{target_family}->{related_family}")

    output.sort(
        key=lambda item: (
            item["reflection_sentence_kind"] != "open_lage_near_direction_candidate",
            -int(item["relation_source_count"]),
            -float(item["avg_relation_score"]),
            str(item["target_family"]),
            str(item["related_family"]),
        )
    )
    summary = [
        {
            "reflection_sentence_kind": group["reflection_sentence_kind"],
            "sentence_count": int(group["sentence_count"]),
            "families": "|".join(sorted(group["families"])),
            "passive_only": True,
            "influences_action": False,
        }
        for group in groups.values()
    ]
    summary.sort(key=lambda item: (-int(item["sentence_count"]), str(item["reflection_sentence_kind"])))
    return output, summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(rows: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "passive_sign_reflection_sentences.csv"
    summary_path = output_dir / "passive_sign_reflection_sentences_summary.csv"
    json_path = output_dir / "passive_sign_reflection_sentences.json"
    md_path = output_dir / "passive_sign_reflection_sentences.md"
    _write_csv(detail_path, rows, ["reflection_sentence_symbol", "target_family", "related_family"])
    _write_csv(summary_path, summary, ["reflection_sentence_kind", "sentence_count"])
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
        "# Passive Sign Reflection Sentences",
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
        lines.append(f"- {row['reflection_sentence_kind']}: {row['sentence_count']} {row['families']}")
    lines.extend(["", "## Sentences"])
    for row in rows[:20]:
        lines.append(f"- {row['reflection_sentence_symbol']}: {row['dio_sentence']}")
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build passive sign reflection sentences")
    parser.add_argument("--relation-stability", required=True)
    parser.add_argument("--sign-memory", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    rows, summary = build_sentences(
        _read_csv(Path(args.relation_stability)),
        _read_csv(Path(args.sign_memory)),
    )
    write_outputs(rows, summary, Path(args.output_dir))
    print(f"sentences={len(rows)} summary_rows={len(summary)}")
    for row in rows[:8]:
        print(f"{row['reflection_sentence_symbol']} {row['reflection_sentence_kind']} {row['target_family']}->{row['related_family']}")


if __name__ == "__main__":
    main()
