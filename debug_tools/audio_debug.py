"""Optional WAV export for DIO's market hearing trace.

The exporter is diagnostic only. It records the compact market-hearing state
that already exists in the runtime and writes a mono PCM WAV at process exit.
It does not feed back into entry logic, regulation, memory, or trade planning.
"""

from __future__ import annotations

import atexit
import math
import os
import threading
import time
import wave
from collections import Counter

from config import Config
from debug_tools.writers import dbr_file_write_profile, dbr_path

_LOCK = threading.Lock()
_SAMPLES: list[dict] = []
_COUNT = 0
_LAST_KEY = None
_WROTE = False


def _clip(value: float, low: float, high: float) -> float:
    try:
        value = float(value)
    except Exception:
        value = 0.0
    return max(float(low), min(float(high), float(value)))


def _as_float(source, key: str, default: float = 0.0) -> float:
    if not isinstance(source, dict):
        return float(default or 0.0)
    try:
        value = source.get(key, None)
        if value is None:
            return float(default or 0.0)
        return float(value or 0.0)
    except Exception:
        return float(default or 0.0)


def _resolve_market_hearing_state(*sources) -> dict:
    for source in sources:
        if not isinstance(source, dict):
            continue
        candidate = source.get("market_hearing_state")
        if isinstance(candidate, dict) and candidate:
            return dict(candidate)
        metrics = source.get("perception_trace_metrics")
        if isinstance(metrics, dict):
            candidate = metrics.get("market_hearing_state")
            if isinstance(candidate, dict) and candidate:
                return dict(candidate)
    return {}


def _clean_text(value, default: str = "-") -> str:
    text = str(value if value is not None else default)
    return text.replace("\n", " ").replace("\r", " ").replace(";", "|")


def _world_seconds_per_tick() -> float:
    """Audio sample duration follows the dominant outer world time."""

    return max(0.001, float(getattr(Config, "WORLD_TIME_SECONDS", 0.015) or 0.015))


def _max_sample_count() -> int:
    seconds_per_tick = _world_seconds_per_tick()
    max_seconds = max(0.0, float(getattr(Config, "MCM_MARKET_MELODY_WAV_MAX_SECONDS", 180.0) or 180.0))
    if max_seconds <= 0.0:
        return 0
    return max(1, int(max_seconds / seconds_per_tick))


def record_market_melody_audio(
    bot,
    *,
    candle_state,
    tension_state,
    visual_market_state,
    outer_visual_perception_state,
    perception_state,
    processing_state,
):
    """Collect one market-hearing sample for the optional WAV debug trace."""

    global _COUNT, _LAST_KEY

    try:
        if not bool(getattr(Config, "MCM_MARKET_MELODY_WAV_DEBUG", False)):
            return

        max_count = _max_sample_count()
        if max_count <= 0:
            return

        hearing = _resolve_market_hearing_state(
            processing_state,
            perception_state,
            outer_visual_perception_state,
            visual_market_state,
            tension_state,
        )
        trace_metrics = dict((perception_state or {}).get("perception_trace_metrics", {}) or {})
        core_trace = dict((tension_state or {}).get("core_trace_state", {}) or {})

        loudness = _as_float(hearing, "loudness", _as_float(trace_metrics, "market_loudness", 0.0))
        frequency_hz = _as_float(hearing, "frequency_hz", _as_float(trace_metrics, "market_frequency_hz", 0.0))
        compression = _as_float(hearing, "compression", _as_float(trace_metrics, "market_hearing_compression", 0.0))
        tone = _clean_text(hearing.get("tone", trace_metrics.get("market_tone", "silent_tone")), "silent_tone")
        timestamp = getattr(bot, "current_timestamp", None)
        if timestamp is None:
            timestamp = (visual_market_state or {}).get("timestamp", "-")

        candle_key = (
            _clean_text(timestamp, "-"),
            round(_as_float(candle_state, "open"), 8),
            round(_as_float(candle_state, "high"), 8),
            round(_as_float(candle_state, "low"), 8),
            round(_as_float(candle_state, "close"), 8),
            round(loudness, 6),
            round(frequency_hz, 4),
        )
        if _LAST_KEY == candle_key:
            return
        _LAST_KEY = candle_key

        _COUNT += 1
        every_n = max(1, int(getattr(Config, "MCM_MARKET_MELODY_WAV_EVERY_N", 1) or 1))
        if (_COUNT % every_n) != 0:
            return

        sample = {
            "timestamp": _clean_text(timestamp, "-"),
            "frequency_hz": max(0.0, float(frequency_hz or 0.0)),
            "loudness": max(0.0, float(loudness or 0.0)),
            "compression": _clip(compression, 0.0, 1.0),
            "tone": tone,
            "coherence": _as_float(core_trace, "coherence", _as_float(tension_state, "coherence", 0.0)),
            "asymmetry": _as_float(core_trace, "asymmetry", _as_float(tension_state, "asymmetry", 0.0)),
            "energy": _as_float(core_trace, "energy", _as_float(tension_state, "energy", 0.0)),
        }

        with _LOCK:
            if len(_SAMPLES) >= max_count:
                return
            _SAMPLES.append(sample)
    except Exception:
        return


def _ensure_dir(path: str):
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def _write_meta(path: str, samples: list[dict], duration_seconds: float):
    try:
        meta_path = os.path.splitext(path)[0] + "_meta.txt"
        freqs = [float(item.get("frequency_hz", 0.0) or 0.0) for item in samples]
        loudness = [float(item.get("loudness", 0.0) or 0.0) for item in samples]
        tones = Counter(str(item.get("tone", "silent_tone") or "silent_tone") for item in samples)
        text = "\n".join(
            [
                "DIO market melody WAV debug",
                f"samples={len(samples)}",
                f"duration_seconds={duration_seconds:.3f}",
                f"frequency_min_hz={min(freqs) if freqs else 0.0:.4f}",
                f"frequency_max_hz={max(freqs) if freqs else 0.0:.4f}",
                f"loudness_min={min(loudness) if loudness else 0.0:.6f}",
                f"loudness_max={max(loudness) if loudness else 0.0:.6f}",
                "tones=" + ",".join(f"{key}:{value}" for key, value in sorted(tones.items())),
                "mechanic=debug_only_no_entry_effect",
                "",
            ]
        )
        start = time.perf_counter()
        with open(meta_path, "w", encoding="utf-8") as handle:
            handle.write(text)
        dbr_file_write_profile(
            meta_path,
            (time.perf_counter() - start) * 1000.0,
            bytes_written=len(text.encode("utf-8")),
            operation="market_melody_wav_meta",
        )
    except Exception:
        return


def flush_market_melody_wav(force: bool = False):
    """Write the collected hearing trace as a mono WAV file."""

    global _WROTE

    try:
        if not bool(getattr(Config, "MCM_MARKET_MELODY_WAV_DEBUG", False)):
            return
        with _LOCK:
            if not _SAMPLES:
                return
            if _WROTE and not force:
                return
            samples = list(_SAMPLES)
            _WROTE = True

        sample_rate = max(8000, int(getattr(Config, "MCM_MARKET_MELODY_WAV_SAMPLE_RATE", 22050) or 22050))
        seconds_per_tick = _world_seconds_per_tick()
        gain = _clip(float(getattr(Config, "MCM_MARKET_MELODY_WAV_GAIN", 0.22) or 0.22), 0.0, 1.0)
        max_hz = min(float(getattr(Config, "MCM_MARKET_HEARING_MAX_HZ", 17000.0) or 17000.0), (sample_rate / 2.0) - 100.0)
        frames_per_tick = max(1, int(sample_rate * seconds_per_tick))
        phase = 0.0
        frames = bytearray()
        glide_enabled = bool(getattr(Config, "MCM_MARKET_MELODY_WAV_GLIDE_ENABLED", True))
        previous_frequency_hz = 0.0
        previous_amplitude = 0.0

        for sample in samples:
            frequency_hz = _clip(float(sample.get("frequency_hz", 0.0) or 0.0), 0.0, max_hz)
            loudness = _clip(float(sample.get("loudness", 0.0) or 0.0) / 2.5, 0.0, 1.0)
            compression = _clip(float(sample.get("compression", 0.0) or 0.0), 0.0, 1.0)
            amplitude = gain * (0.10 + loudness * 0.90) * (1.0 - compression * 0.20)
            if frequency_hz <= 0.0 or str(sample.get("tone", "")) == "silent_tone":
                amplitude = 0.0

            for frame_index in range(frames_per_tick):
                if glide_enabled and frames_per_tick > 1:
                    mix = frame_index / float(frames_per_tick - 1)
                    frame_frequency_hz = previous_frequency_hz + ((frequency_hz - previous_frequency_hz) * mix)
                    frame_amplitude = previous_amplitude + ((amplitude - previous_amplitude) * mix)
                else:
                    frame_frequency_hz = frequency_hz
                    frame_amplitude = amplitude
                step = (2.0 * math.pi * frame_frequency_hz) / float(sample_rate)
                value = math.sin(phase)
                shaped = value * frame_amplitude
                int_value = int(_clip(shaped, -1.0, 1.0) * 32767.0)
                frames.extend(int_value.to_bytes(2, byteorder="little", signed=True))
                phase += step
                if phase > math.tau:
                    phase -= math.tau
            previous_frequency_hz = frequency_hz
            previous_amplitude = amplitude

        filename = str(getattr(Config, "MCM_MARKET_MELODY_WAV_FILENAME", "market_melody.wav") or "market_melody.wav")
        path = dbr_path(filename)
        _ensure_dir(path)
        start = time.perf_counter()
        with wave.open(path, "wb") as handle:
            handle.setnchannels(1)
            handle.setsampwidth(2)
            handle.setframerate(sample_rate)
            handle.writeframes(bytes(frames))
        dbr_file_write_profile(
            path,
            (time.perf_counter() - start) * 1000.0,
            bytes_written=len(frames),
            operation="market_melody_wav",
            extra=f"samples={len(samples)}",
        )
        _write_meta(path, samples, duration_seconds=len(frames) / 2 / sample_rate)
    except Exception:
        return


atexit.register(flush_market_melody_wav)


__all__ = [
    "flush_market_melody_wav",
    "record_market_melody_audio",
]
