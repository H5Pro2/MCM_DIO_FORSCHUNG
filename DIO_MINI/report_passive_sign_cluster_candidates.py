"""Report passive sign-cluster candidates from recurring sign relations.

This diagnostic reads passive sign-relation stability rows and optional
passive sign memory. It creates cluster candidates only as passive inner-map
diagnosis. It does not write runtime memory and does not influence Mini-DIO
action logic.
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
from pathlib import Path


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


def _split(value: object) -> set[str]:
    return {item.strip() for item in str(value or "").split("|") if item.strip()}


def _make_cluster_symbol(payload: dict) -> str:
    identity = "|".join(
        [
            str(payload.get("target_family", "") or ""),
            str(payload.get("related_family", "") or ""),
            str(payload.get("cluster_candidate_state", "") or ""),
            str(payload.get("target_sign_symbol", "") or ""),
            str(payload.get("related_sign_symbol", "") or ""),
            str(payload.get("shared_field_trace", "") or ""),
        ]
    )
    hash_value = 2166136261
    for char in identity:
        hash_value ^= ord(char) + 73
        hash_value = (hash_value * 16777619) & 0xFFFFFFFF
    return f"dio_cluster_{_base36(hash_value).rjust(7, '0')}"


def _cluster_state(row: dict) -> str:
    relation_state = str(row.get("relation_stability_state", "") or "")
    source_count = _safe_int(row.get("relation_source_count"))
    field_overlap = _safe_float(row.get("avg_field_overlap"))
    relation_score = _safe_float(row.get("avg_relation_score"))
    if "recurring_strong" in relation_state and source_count >= 2 and field_overlap >= 0.75:
        return "passive_cluster_candidate_stable_field_relation"
    if "recurring_mixed" in relation_state and source_count >= 2 and field_overlap >= 0.60:
        return "passive_cluster_candidate_mixed_field_relation"
    if relation_state.startswith("recurring") and source_count >= 2 and relation_score >= 0.30:
        return "passive_cluster_candidate_weak_relation"
    if source_count <= 1:
        return "single_relation_not_cluster"
    return "not_cluster_candidate"


def _cluster_sentence(row: dict) -> str:
    target = str(row.get("target_family", "") or "")
    related = str(row.get("related_family", "") or "")
    state = str(row.get("cluster_candidate_state", "") or "")
    if state == "passive_cluster_candidate_stable_field_relation":
        return (
            f"{target}+{related}: Diese Zeichen bilden wiederkehrend eine stabile "
            "Feldnaehe. Ich halte das als passiven Clusterkeim, nicht als Handlung."
        )
    if state == "passive_cluster_candidate_mixed_field_relation":
        return (
            f"{target}+{related}: Diese Zeichen bilden wiederkehrend Naehe, "
            "aber die Beziehung ist gemischt. Ich halte sie als offenen Clusterkeim."
        )
    if state == "passive_cluster_candidate_weak_relation":
        return (
            f"{target}+{related}: Diese Zeichen beruehren sich wiederholt schwach. "
            "Ich speichere das nur als Randnaehe."
        )
    return f"{target}+{related}: Diese Zeichennaehe ist noch kein Cluster."


def build_cluster_candidates(relation_rows: list[dict], sign_rows: list[dict]) -> tuple[list[dict], list[dict]]:
    signs = {str(row.get("symbol_family", "") or ""): dict(row) for row in sign_rows}
    rows: list[dict] = []
    groups: dict[str, dict] = {}

    for relation in relation_rows:
        target = str(relation.get("target_family", "") or "")
        related = str(relation.get("related_family", "") or "")
        if not target or not related:
            continue
        state = _cluster_state(relation)
        target_sign = signs.get(target, {})
        related_sign = signs.get(related, {})
        target_fields = _split(target_sign.get("stable_fields"))
        related_fields = _split(related_sign.get("stable_fields"))
        shared_fields = sorted(target_fields & related_fields)
        payload = {
            "target_family": target,
            "related_family": related,
            "cluster_candidate_state": state,
            "relation_stability_state": str(relation.get("relation_stability_state", "") or ""),
            "relation_source_count": _safe_int(relation.get("relation_source_count")),
            "available_relation_sources": _safe_int(relation.get("available_relation_sources")),
            "avg_relation_score": round(_safe_float(relation.get("avg_relation_score")), 6),
            "avg_field_overlap": round(_safe_float(relation.get("avg_field_overlap")), 6),
            "avg_afterlook_overlap": round(_safe_float(relation.get("avg_action_overlap")), 6),
            "target_sign_symbol": str(target_sign.get("passive_sign_symbol", "") or ""),
            "related_sign_symbol": str(related_sign.get("passive_sign_symbol", "") or ""),
            "target_sign_state": str(target_sign.get("sign_state", "") or ""),
            "related_sign_state": str(related_sign.get("sign_state", "") or ""),
            "target_stable_fields": str(target_sign.get("stable_fields", "") or ""),
            "related_stable_fields": str(related_sign.get("stable_fields", "") or ""),
            "shared_field_trace": "|".join(shared_fields),
            "cluster_is_pair_seed": True,
            "passive_only": True,
            "writes_runtime_memory": False,
            "read_by_mini_dio": False,
            "influences_action": False,
            "is_gate": False,
            "is_motoric": False,
            "is_entry_signal": False,
            "is_direction_signal": False,
        }
        payload["passive_cluster_symbol"] = _make_cluster_symbol(payload)
        payload["dio_sentence"] = _cluster_sentence(payload)
        rows.append(payload)

        group = groups.setdefault(
            state,
            {
                "cluster_candidate_state": state,
                "cluster_count": 0,
                "families": [],
            },
        )
        group["cluster_count"] += 1
        group["families"].append(f"{target}+{related}")

    rows.sort(
        key=lambda row: (
            row["cluster_candidate_state"] != "passive_cluster_candidate_stable_field_relation",
            row["cluster_candidate_state"] != "passive_cluster_candidate_mixed_field_relation",
            -int(row["relation_source_count"]),
            -float(row["avg_field_overlap"]),
            -float(row["avg_relation_score"]),
            str(row["target_family"]),
            str(row["related_family"]),
        )
    )
    summary = [
        {
            "cluster_candidate_state": group["cluster_candidate_state"],
            "cluster_count": int(group["cluster_count"]),
            "families": "|".join(sorted(group["families"])),
            "passive_only": True,
            "influences_action": False,
        }
        for group in groups.values()
    ]
    summary.sort(key=lambda row: (-int(row["cluster_count"]), str(row["cluster_candidate_state"])))
    return rows, summary


def _write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(rows[0].keys()) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(rows: list[dict], summary: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = output_dir / "passive_sign_cluster_candidates.csv"
    summary_path = output_dir / "passive_sign_cluster_candidates_summary.csv"
    json_path = output_dir / "passive_sign_cluster_candidates.json"
    md_path = output_dir / "passive_sign_cluster_candidates.md"
    _write_csv(detail_path, rows, ["target_family", "related_family", "cluster_candidate_state"])
    _write_csv(summary_path, summary, ["cluster_candidate_state", "cluster_count"])
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
                "clusters": rows,
                "summary": summary,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Passive Sign Cluster Candidates",
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
            f"- {row['cluster_candidate_state']}: {row['cluster_count']} "
            f"({row.get('families', '')})"
        )
    lines.extend(["", "## Kandidaten"])
    for row in rows[:20]:
        lines.append(
            f"- {row['target_family']} + {row['related_family']}: "
            f"{row['cluster_candidate_state']} symbol={row['passive_cluster_symbol']} "
            f"field={row['avg_field_overlap']} score={row['avg_relation_score']}"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--relation-stability", nargs="+", required=True)
    parser.add_argument("--sign-memory", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    relation_paths = _expand_patterns(args.relation_stability)
    relation_rows: list[dict] = []
    for path in relation_paths:
        relation_rows.extend(_read_csv(path))
    sign_rows = _read_csv(Path(args.sign_memory))
    rows, summary = build_cluster_candidates(relation_rows, sign_rows)
    write_outputs(rows, summary, Path(args.output_dir))
    print(f"relation_sources={len(relation_paths)} clusters={len(rows)} summary_rows={len(summary)}")
    for row in rows[:8]:
        print(
            f"{row['target_family']}+{row['related_family']} "
            f"{row['cluster_candidate_state']} {row['passive_cluster_symbol']}"
        )


if __name__ == "__main__":
    main()
