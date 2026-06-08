"""Create related controlled Mini-DIO probe variant G.

Variant G is a near-world continuation after F. It mutates only OHLCV data and
does not touch Mini-DIO logic, memory, entries, direction, gates, or runtime
behavior.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


PROBES = {
    20: "emergenz_richtungsvarianz",
    21: "emergenz_hoervarianz",
    22: "emergenz_skalenvarianz",
    23: "emergenz_temporalvarianz",
    24: "emergenz_minimalsensorik",
    25: "emergenz_kontrastvarianz",
    26: "emergenz_signaturdrift",
}


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        result = float(value if value not in (None, "") else default)
    except Exception:
        return default
    if result != result:
        return default
    return result


def _read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _write_rows(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _fmt_price(value: float) -> str:
    return f"{value:.2f}"


def _fmt_volume(value: float) -> str:
    return f"{value:.1f}"


def mutate_rows(rows: list[dict], probe: int) -> list[dict]:
    """Return a deterministic near-world continuation of variant F."""

    if not rows:
        return []
    timestamp_shift = 1_500_000_000_000 + (probe * 12_000_000)
    probe_bias = (23 - probe) * 0.0018
    mutated: list[dict] = []

    for index, row in enumerate(rows):
        open_price = _safe_float(row.get("open"), 100.0)
        high_price = _safe_float(row.get("high"), open_price)
        low_price = _safe_float(row.get("low"), open_price)
        close_price = _safe_float(row.get("close"), open_price)
        volume = _safe_float(row.get("volume"), 0.0)

        center = (open_price + close_price) / 2.0
        body = close_price - open_price
        upper_wick = max(0.0, high_price - max(open_price, close_price))
        lower_wick = max(0.0, min(open_price, close_price) - low_price)

        phase = ((index % 11) - 5) / 5.0
        pulse = ((index // 4) % 5 - 2) / 2.0
        local_breath = ((index % 5) - 2) / 2.0

        center_shift = (phase * 0.011) + (pulse * 0.008) + probe_bias
        body_scale = 1.0 + (local_breath * 0.038) - (phase * 0.018)
        upper_scale = 1.0 + (phase * 0.045) + (pulse * 0.02)
        lower_scale = 1.0 - (phase * 0.04) + (abs(local_breath) * 0.025)
        volume_scale = 1.0 + (abs(pulse) * 0.052) + (abs(phase) * 0.034)

        new_center = center + center_shift
        new_body = body * body_scale
        new_open = new_center - (new_body / 2.0)
        new_close = new_center + (new_body / 2.0)
        new_high = max(new_open, new_close) + max(0.02, upper_wick * upper_scale)
        new_low = min(new_open, new_close) - max(0.02, lower_wick * lower_scale)
        new_volume = max(1.0, volume * volume_scale)

        new_row = dict(row)
        try:
            new_row["timestamp_ms"] = str(int(float(row.get("timestamp_ms", 0))) + timestamp_shift)
        except Exception:
            new_row["timestamp_ms"] = str(timestamp_shift + index * 300_000)
        new_row["open"] = _fmt_price(new_open)
        new_row["high"] = _fmt_price(new_high)
        new_row["low"] = _fmt_price(new_low)
        new_row["close"] = _fmt_price(new_close)
        new_row["volume"] = _fmt_volume(new_volume)
        mutated.append(new_row)

    return mutated


def create_variant_g(data_dir: Path) -> list[Path]:
    written: list[Path] = []
    for probe, label in PROBES.items():
        source = data_dir / f"kontrolliert_sensor_relation_probe{probe}_{label}_6episoden_varianteF_verwandt_5m_SOLUSDT.csv"
        target = data_dir / f"kontrolliert_sensor_relation_probe{probe}_{label}_6episoden_varianteG_verwandt_5m_SOLUSDT.csv"
        rows = _read_rows(source)
        if not rows:
            continue
        _write_rows(target, mutate_rows(rows, probe), list(rows[0].keys()))
        written.append(target)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Create controlled Mini-DIO variant G CSVs.")
    parser.add_argument("--data-dir", default="data")
    args = parser.parse_args()
    for path in create_variant_g(Path(args.data_dir)):
        print(path)


if __name__ == "__main__":
    main()
