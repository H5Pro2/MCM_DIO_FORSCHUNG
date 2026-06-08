"""Create related controlled Mini-DIO probe variant F.

The generator only mutates OHLCV input data. It does not touch Mini-DIO logic,
memory, gates, entries, direction, or runtime behavior.
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
    """Return a related, harder variant with deterministic sensory drift."""

    if not rows:
        return []
    base_open = _safe_float(rows[0].get("open"), 100.0)
    mutated: list[dict] = []
    timestamp_shift = 1_200_000_000_000 + (probe * 10_000_000)
    probe_bias = (probe - 23) * 0.0025

    for index, row in enumerate(rows):
        open_price = _safe_float(row.get("open"), base_open)
        high_price = _safe_float(row.get("high"), open_price)
        low_price = _safe_float(row.get("low"), open_price)
        close_price = _safe_float(row.get("close"), open_price)
        volume = _safe_float(row.get("volume"), 0.0)

        center = (open_price + close_price) / 2.0
        body = close_price - open_price
        upper_wick = max(0.0, high_price - max(open_price, close_price))
        lower_wick = max(0.0, min(open_price, close_price) - low_price)

        phase = ((index % 9) - 4) / 4.0
        counter_phase = ((index % 7) - 3) / 3.0
        slow_wave = ((index // 6) % 4 - 1.5) / 1.5

        center_shift = (phase * 0.018) + (slow_wave * 0.012) + probe_bias
        body_scale = 1.0 + (counter_phase * 0.055)
        wick_scale = 1.0 + (phase * 0.075)
        volume_scale = 1.0 + (abs(phase) * 0.085) + (counter_phase * 0.035)

        new_center = center + center_shift
        new_body = body * body_scale
        new_open = new_center - (new_body / 2.0)
        new_close = new_center + (new_body / 2.0)

        new_upper = max(0.02, upper_wick * wick_scale + abs(center_shift) * 0.35)
        new_lower = max(0.02, lower_wick * (2.0 - wick_scale) + abs(counter_phase) * 0.025)
        new_high = max(new_open, new_close) + new_upper
        new_low = min(new_open, new_close) - new_lower
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


def create_variant_f(data_dir: Path) -> list[Path]:
    written: list[Path] = []
    for probe, label in PROBES.items():
        source = data_dir / f"kontrolliert_sensor_relation_probe{probe}_{label}_6episoden_varianteE_verwandt_5m_SOLUSDT.csv"
        target = data_dir / f"kontrolliert_sensor_relation_probe{probe}_{label}_6episoden_varianteF_verwandt_5m_SOLUSDT.csv"
        rows = _read_rows(source)
        if not rows:
            continue
        fieldnames = list(rows[0].keys())
        _write_rows(target, mutate_rows(rows, probe), fieldnames)
        written.append(target)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Create controlled Mini-DIO variant F CSVs.")
    parser.add_argument("--data-dir", default="data")
    args = parser.parse_args()

    written = create_variant_f(Path(args.data_dir))
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
