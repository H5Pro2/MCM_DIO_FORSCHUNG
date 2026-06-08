"""Build compact DIO-owned sentence traces from contact family maps."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _base36(number: int) -> str:
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    number = abs(int(number))
    if number == 0:
        return "0"
    chars = []
    while number:
        number, rem = divmod(number, 36)
        chars.append(alphabet[rem])
    return "".join(reversed(chars))


def _trace_symbol(contact_symbol: str, family: str, state: str) -> str:
    hash_value = 2166136261
    for text in (contact_symbol, family, state):
        for char in str(text or ""):
            hash_value ^= ord(char)
            hash_value = (hash_value * 16777619) & 0xFFFFFFFF
    return f"dio_sentence_{_base36(hash_value).rjust(7, '0')}"


def _read_rows(paths: list[Path]) -> list[dict]:
    rows = []
    for path in paths:
        with path.open(newline="", encoding="utf-8") as handle:
            rows.extend(dict(row) for row in csv.DictReader(handle))
    return rows


def _aggregate(rows: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str, str], dict] = {}
    for row in rows:
        key = (
            str(row.get("contact_symbol", "") or ""),
            str(row.get("symbol_family", "") or ""),
            str(row.get("episode_contact_state", "") or ""),
        )
        item = grouped.setdefault(
            key,
            {
                "contact_symbol": key[0],
                "contact_lage_state": str(row.get("contact_lage_state", "") or ""),
                "symbol_family": key[1],
                "episode_contact_state": key[2],
                "count": 0,
                "reward_sum": 0.0,
                "actions": {},
            },
        )
        item["count"] += 1
        try:
            item["reward_sum"] += float(row.get("reward", 0.0) or 0.0)
        except Exception:
            pass
        action = str(row.get("action", "") or "-")
        item["actions"][action] = int(item["actions"].get(action, 0) or 0) + 1
    out = []
    for item in grouped.values():
        actions = ",".join(f"{key}:{value}" for key, value in sorted(item["actions"].items()))
        sentence_symbol = _trace_symbol(
            item["contact_symbol"],
            item["symbol_family"],
            item["episode_contact_state"],
        )
        out.append(
            {
                "sentence_symbol": sentence_symbol,
                "contact_symbol": item["contact_symbol"],
                "contact_lage_state": item["contact_lage_state"],
                "symbol_family": item["symbol_family"],
                "episode_contact_state": item["episode_contact_state"],
                "count": item["count"],
                "reward_sum": round(item["reward_sum"], 6),
                "actions": actions,
                "passive_only": 1,
            }
        )
    out.sort(
        key=lambda item: (
            item["contact_lage_state"],
            item["episode_contact_state"],
            -int(item["count"]),
            item["symbol_family"],
        )
    )
    return out


def _write(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "dio_mini_contact_sentence_trace.csv"
    json_path = output_dir / "dio_mini_contact_sentence_trace.json"
    md_path = output_dir / "dio_mini_contact_sentence_trace.md"
    fieldnames = [
        "sentence_symbol",
        "contact_symbol",
        "contact_lage_state",
        "symbol_family",
        "episode_contact_state",
        "count",
        "reward_sum",
        "actions",
        "passive_only",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    lines = ["# DIO Mini Contact Sentence Trace", ""]
    for row in rows[:40]:
        lines.extend(
            [
                f"## {row['sentence_symbol']}",
                f"- contact: {row['contact_symbol']} ({row['contact_lage_state']})",
                f"- form: {row['symbol_family']}",
                f"- erleben: {row['episode_contact_state']}",
                f"- count: {row['count']}",
                f"- reward_sum: {row['reward_sum']}",
                f"- actions: {row['actions'] or '-'}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", action="append", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    rows = _aggregate(_read_rows([Path(item) for item in args.map]))
    _write(rows, Path(args.output_dir))
    print(f"sentence_traces={len(rows)}")
    for row in rows[:12]:
        print(
            f"{row['sentence_symbol']} {row['contact_symbol']} "
            f"{row['symbol_family']} {row['episode_contact_state']} count={row['count']}"
        )


if __name__ == "__main__":
    main()
