"""Create controlled Mini-DIO probe variant N.

Variant N is a deterministic follow-up after M. It is a targeted passive
recoupling probe for the decoupled dio_0325 trace: can it stay isolated, attach
to dio_114i, or return toward dio_1ytc under another world contact?

This changes only OHLCV input data. It does not change Mini-DIO logic, memory,
gates, entries, direction, or runtime behavior.
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
    """Return a deterministic sixth-contact continuation of variant M."""

    if not rows:
        return []
    timestamp_shift = 4_100_000_000_000 + (probe * 37_000_000)
    probe_phase = ((probe % 15) - 7) / 7.0
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

        local_phase = ((index % 37) - 18) / 18.0
        slow_wave = ((index // 10) % 13 - 6) / 6.0
        pulse = ((index % 16) - 7.5) / 7.5
        recoupling_wave = ((index // 6) % 5 - 2) / 2.0

        center_shift = (
            (recoupling_wave * 0.0033)
            - (local_phase * 0.0022)
            + (slow_wave * 0.0025)
            - (probe_phase * 0.0011)
        )
        body_scale = max(0.55, 1.0 - (pulse * 0.018) + (recoupling_wave * 0.018))
        upper_scale = max(0.55, 1.0 + (abs(local_phase) * 0.013) - (slow_wave * 0.014))
        lower_scale = max(0.55, 1.0 + (abs(pulse) * 0.015) + (slow_wave * 0.011))
        volume_scale = max(0.78, min(1.22, 1.0 + (abs(recoupling_wave) * 0.018) + (abs(slow_wave) * 0.012)))

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


def create_variant_n(data_dir: Path) -> list[Path]:
    written: list[Path] = []
    for probe, label in PROBES.items():
        source = data_dir / f"kontrolliert_sensor_relation_probe{probe}_{label}_6episoden_varianteM_folgekontakt4_5m_SOLUSDT.csv"
        target = data_dir / f"kontrolliert_sensor_relation_probe{probe}_{label}_6episoden_varianteN_folgekontakt5_5m_SOLUSDT.csv"
        rows = _read_rows(source)
        if not rows:
            continue
        _write_rows(target, mutate_rows(rows, probe), list(rows[0].keys()))
        written.append(target)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Create controlled Mini-DIO variant N CSVs.")
    parser.add_argument("--data-dir", default="data")
    args = parser.parse_args()
    for path in create_variant_n(Path(args.data_dir)):
        print(path)


if __name__ == "__main__":
    main()
