from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

try:
    from PyQt6 import QtCore, QtWidgets
except Exception:
    try:
        from PyQt5 import QtCore, QtWidgets
    except Exception as exc:
        raise ModuleNotFoundError(
            "GPU-GUI benötigt PyQt6 oder PyQt5. Installiere zuerst PyQt6 oder PyQt5."
        ) from exc

try:
    import pyqtgraph as pg
except Exception as exc:
    raise ModuleNotFoundError(
        "GPU-GUI benötigt pyqtgraph. Installiere zuerst pyqtgraph."
    ) from exc


# ==================================================
# CONFIG
# ==================================================
REFRESH_MS = 10
MAX_DRAW_NEURONS = 1000
GRID_SIZE = 220
LINK_NEIGHBORS = 4
LINK_MAX_DISTANCE = 0.115
LINK_LOCAL_RADIUS_FACTOR = 1.36
LINK_SMALL_FIELD_NEIGHBORS = 3
HEAT_SIGMA = 0.030
SAMPLE_ACTIVITY_FLOOR = 0.018
TRACE_DECAY = 0.90
INPUT_HOTSPOT_COUNT = 8
INPUT_HOTSPOT_MIN_STRENGTH = 0.035
ACTIVE_LINK_FLOOR = 0.16
ACTIVE_LINK_MAX_DRAW = 260
ACTIVE_LINK_MIN_DRAW = 36
BASE_LINK_MAX_DRAW = 900
AREAL_FLOW_MAX_MARKERS = 10
AREAL_FLOW_MIN_ACTIVITY = 0.075
AREAL_FLOW_RADIUS = 0.075

C = {
    "bg_root": "#0d0f13",
    "bg_panel": "#13161c",
    "bg_card": "#181c24",
    "bg_chart": "#0b0f16",
    "border": "#252a36",
    "text_hi": "#e8eaf0",
    "text_med": "#8b92a8",
    "text_label": "#5c6480",
    "inn_green": "#4caf78",
    "inn_orange": "#d4894a",
    "inn_red": "#c05050",
    "inn_blue": "#5b8dd9",
    "inn_purple": "#8b72be",
}


# ==================================================
# HELPERS
# ==================================================
def safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return float(default)


# --------------------------------------------------
def safe_int(value, default: int = 0) -> int:
    try:
        return int(float(value))
    except Exception:
        return int(default)


# --------------------------------------------------
def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(float(low), min(float(high), float(value)))


# --------------------------------------------------
def safe_load_json(path: Path) -> dict:
    try:
        if not path.exists():
            return {}
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


# --------------------------------------------------
def fmt_ts(value) -> str:
    try:
        if value is None:
            return "–"
        ts = int(float(value))
        if ts > 10_000_000_000_000:
            ts = ts // 1000
        if ts > 10_000_000_000:
            dt = datetime.fromtimestamp(ts / 1000)
        else:
            dt = datetime.fromtimestamp(ts)
        return dt.strftime("%d.%m.%Y %H:%M:%S")
    except Exception:
        return "–"


# --------------------------------------------------
def fmt_num(value, digits: int = 3) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except Exception:
        return "–"


# --------------------------------------------------
def numeric_hex(value: float, invert: bool = False) -> str:
    v = clamp(value)
    if invert:
        v = 1.0 - v
    if v >= 0.67:
        return C["inn_green"]
    if v >= 0.34:
        return C["inn_orange"]
    return C["inn_blue"]


# --------------------------------------------------
def text_state_color(text: str) -> str:
    s = str(text or "").lower()
    if any(word in s for word in ["stress", "critical", "blocked", "over", "chaotic"]):
        return C["inn_red"]
    if any(word in s for word in ["observe", "wait", "hold", "neutral", "reorganizing"]):
        return C["inn_orange"]
    if any(word in s for word in ["stable", "active", "aligned", "ready", "settling"]):
        return C["inn_green"]
    return C["inn_blue"]


# --------------------------------------------------
def qcolor(hex_color: str, alpha: int = 255):
    color = pg.mkColor(hex_color)
    color.setAlpha(max(0, min(255, int(alpha))))
    return color


# --------------------------------------------------
def heat_lut() -> np.ndarray:
    stops = np.asarray(
        [
            [0, 0, 0, 0],
            [16, 23, 36, 90],
            [24, 48, 71, 140],
            [35, 83, 100, 190],
            [54, 116, 116, 220],
            [212, 137, 74, 255],
        ],
        dtype=np.ubyte,
    )
    x_old = np.linspace(0.0, 1.0, len(stops))
    x_new = np.linspace(0.0, 1.0, 256)
    lut = np.zeros((256, 4), dtype=np.ubyte)
    for channel in range(4):
        lut[:, channel] = np.interp(x_new, x_old, stops[:, channel]).astype(np.ubyte)
    return lut


# ==================================================
# GPU GUI
# ==================================================
class MCMNeuronFieldGPUGUI(QtWidgets.QMainWindow):

    # --------------------------------------------------
    def __init__(self, base_dir: Path):
        super().__init__()
        pg.setConfigOptions(useOpenGL=True, antialias=False)

        self.base_dir = Path(base_dir)
        self.inner_path = self.base_dir / "debug" / "bot_inner_snapshot.json"
        self.outcome_path = self.base_dir / "debug" / "trade_stats.json"
        self._fixed_layout_cache: dict[int, np.ndarray] = {}
        self._link_cache: dict[int, list[tuple[int, int]]] = {}
        self._heat_memory = None
        self._heat_trace = None
        self._lut = heat_lut()

        self.setWindowTitle("MCM Neuron Tissue Field · GPU")
        self.resize(1280, 820)

        self._build_layout()
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._refresh)
        self._timer.start(REFRESH_MS)
        self._refresh()

    # --------------------------------------------------
    def _build_layout(self):
        root = QtWidgets.QWidget()
        root.setStyleSheet(f"background:{C['bg_root']}; color:{C['text_med']}; font-family:Courier New;")
        self.setCentralWidget(root)

        root_layout = QtWidgets.QVBoxLayout(root)
        root_layout.setContentsMargins(6, 6, 6, 6)
        root_layout.setSpacing(6)

        header = QtWidgets.QFrame()
        header.setStyleSheet(f"background:{C['bg_panel']}; border:1px solid {C['border']};")
        header_layout = QtWidgets.QHBoxLayout(header)
        header_layout.setContentsMargins(10, 6, 10, 6)

        title = QtWidgets.QLabel("MCM NEURON TISSUE FIELD · GPU")
        title.setStyleSheet(f"color:{C['text_hi']}; font-size:14px; font-weight:bold;")
        self.lbl_outcome = QtWidgets.QLabel("OUTCOME: –")
        self.lbl_status = QtWidgets.QLabel("INNER: –")
        header_layout.addWidget(title, 1)
        header_layout.addWidget(self.lbl_outcome)
        header_layout.addWidget(self.lbl_status)
        root_layout.addWidget(header)

        body = QtWidgets.QHBoxLayout()
        body.setSpacing(6)
        root_layout.addLayout(body, 1)

        self.plot = pg.PlotWidget(background=C["bg_chart"])
        self.plot.setMenuEnabled(False)
        self.plot.hideAxis("bottom")
        self.plot.hideAxis("left")
        self.plot.setXRange(0.0, 1.0, padding=0.0)
        self.plot.setYRange(0.0, 1.0, padding=0.0)
        self.plot.setMouseEnabled(x=False, y=False)
        body.addWidget(self.plot, 1)

        self.trace_item = pg.ImageItem(axisOrder="row-major")
        self.heat_item = pg.ImageItem(axisOrder="row-major")
        self.base_links_item = pg.PlotDataItem(connect="finite")
        self.active_links_item = pg.PlotDataItem(connect="finite")
        self.areal_flow_item = pg.PlotDataItem(connect="finite")
        self.glow_item = pg.ScatterPlotItem(pxMode=True)
        self.node_item = pg.ScatterPlotItem(pxMode=True)
        self.top_glow_item = pg.ScatterPlotItem(pxMode=True)
        self.hotspot_glow_item = pg.ScatterPlotItem(pxMode=True)
        self.hotspot_node_item = pg.ScatterPlotItem(pxMode=True)

        for item in [
            self.trace_item,
            self.heat_item,
            self.base_links_item,
            self.active_links_item,
            self.areal_flow_item,
            self.glow_item,
            self.node_item,
            self.top_glow_item,
            self.hotspot_glow_item,
            self.hotspot_node_item,
        ]:
            self.plot.addItem(item)

        self.trace_item.setLookupTable(self._lut)
        self.heat_item.setLookupTable(self._lut)
        self.trace_item.setRect(QtCore.QRectF(0.0, 0.0, 1.0, 1.0))
        self.heat_item.setRect(QtCore.QRectF(0.0, 0.0, 1.0, 1.0))

        self.side_panel = QtWidgets.QFrame()
        self.side_panel.setFixedWidth(255)
        self.side_panel.setStyleSheet(f"background:{C['bg_panel']}; border:1px solid {C['border']};")
        side_layout = QtWidgets.QVBoxLayout(self.side_panel)
        side_layout.setContentsMargins(8, 8, 8, 8)
        side_layout.setSpacing(3)
        body.addWidget(self.side_panel)

        self.side_labels = {}
        for section, keys in [
            ("FELD", ["tissue", "snapshot", "density", "stability", "load", "capacity"]),
            ("AKTIVITÄT", ["activity", "coupling", "external", "input_drive"]),
            ("VERBINDUNG", ["links", "active_links", "areal_flow", "hotspots"]),
            ("OUTCOME", ["trades", "winrate", "pnl", "attempts"]),
            ("ZUSTAND", ["reorganization"]),
        ]:
            section_label = QtWidgets.QLabel(section)
            section_label.setStyleSheet(f"color:{C['inn_purple']}; font-weight:bold; padding-top:8px;")
            side_layout.addWidget(section_label)
            for key in keys:
                label = QtWidgets.QLabel(f"{key}: –")
                label.setStyleSheet(f"color:{C['text_med']};")
                side_layout.addWidget(label)
                self.side_labels[str(key)] = label
        side_layout.addStretch(1)

    # --------------------------------------------------
    def _set_side_value(self, key: str, value, color: str | None = None):
        label = self.side_labels.get(str(key))
        if label is None:
            return None
        label.setText(f"{key}: {value}")
        label.setStyleSheet(f"color:{color or C['text_med']};")
        return label

    # --------------------------------------------------
    def _resolve_neuron_points(self, inner: dict) -> list[dict]:
        inner_field = dict(inner.get("inner_field_perception_state", {}) or {})
        population = [dict(item or {}) for item in list(inner_field.get("field_neuron_population", []) or []) if isinstance(item, dict)]
        if population:
            return population[:MAX_DRAW_NEURONS]
        agents = [dict(item or {}) for item in list(inner_field.get("field_agent_points", []) or []) if isinstance(item, dict)]
        return agents[:MAX_DRAW_NEURONS]

    # --------------------------------------------------
    def _resolve_tissue_count(self, inner: dict, points: list[dict]) -> int:
        inner_field = dict(inner.get("inner_field_perception_state", {}) or {})
        configured_count = safe_int(inner_field.get("field_neuron_count", 0), 0)
        if configured_count <= 0:
            configured_count = safe_int(inner_field.get("field_agent_count", 0), 0)
        if configured_count <= 0:
            configured_count = len(points)
        return max(1, min(MAX_DRAW_NEURONS, int(configured_count or len(points) or 1)))

    # --------------------------------------------------
    def _fixed_tissue_layout(self, count: int) -> np.ndarray:
        n = max(1, int(count or 1))
        if n in self._fixed_layout_cache:
            return self._fixed_layout_cache[n]

        rng = np.random.default_rng(104729 + n)
        cols = int(math.ceil(math.sqrt(n * 1.82)))
        rows = int(math.ceil(n / max(1, cols)))
        points = []
        for row in range(rows):
            for col in range(cols):
                if len(points) >= n:
                    break
                base_x = col / max(1, cols - 1)
                base_y = row / max(1, rows - 1)
                if row % 2:
                    base_x += 0.5 / max(2, cols)
                x = max(0.020, min(0.980, base_x + rng.normal(0.0, 0.010)))
                y = max(0.030, min(0.970, base_y + rng.normal(0.0, 0.012)))
                points.append((float(x), float(y)))
        arr = np.asarray(points, dtype=float)
        self._fixed_layout_cache[n] = arr
        return arr

    # --------------------------------------------------
    def _links_for_layout(self, layout: np.ndarray) -> list[tuple[int, int]]:
        n = int(len(layout))
        if n in self._link_cache:
            return self._link_cache[n]
        links = set()
        if n <= 1:
            self._link_cache[n] = []
            return []

        nearest_distances = []
        for index in range(n):
            dist = np.sqrt(np.sum((layout - layout[index]) ** 2, axis=1))
            order = np.argsort(dist)
            for neighbor in order:
                ni = int(neighbor)
                if ni != index:
                    nearest_distances.append(float(dist[ni]))
                    break

        local_spacing = float(np.median(nearest_distances)) if nearest_distances else float(LINK_MAX_DISTANCE)
        dynamic_radius = min(float(LINK_MAX_DISTANCE), max(local_spacing * float(LINK_LOCAL_RADIUS_FACTOR), local_spacing + 0.010))
        max_neighbors = max(1, min(int(LINK_NEIGHBORS), int(LINK_SMALL_FIELD_NEIGHBORS) if n <= 120 else int(LINK_NEIGHBORS)))

        for index in range(n):
            dist = np.sqrt(np.sum((layout - layout[index]) ** 2, axis=1))
            linked = 0
            for neighbor in np.argsort(dist):
                ni = int(neighbor)
                if ni == index:
                    continue
                if float(dist[ni]) > dynamic_radius:
                    break
                links.add(tuple(sorted((index, ni))))
                linked += 1
                if linked >= max_neighbors:
                    break
        resolved = sorted(links)
        self._link_cache[n] = resolved
        return resolved

    # --------------------------------------------------
    def _activity_values(self, points: list[dict], count: int) -> np.ndarray:
        values = []
        for item in list(points or []):
            activation = clamp(safe_float(item.get("activation", 0.0)))
            impulse = clamp(safe_float(item.get("external_impulse_norm", 0.0)) / 0.8)
            coupling = clamp(safe_float(item.get("coupling_norm", 0.0)) / 0.8)
            pressure = clamp(safe_float(item.get("regulation_pressure", 0.0)))
            values.append(clamp((activation * 0.58) + (impulse * 0.22) + (coupling * 0.12) + (pressure * 0.08)))
        return self._resample_values(values, count)

    # --------------------------------------------------
    def _metric_values(self, points: list[dict], count: int, key: str, scale: float = 1.0) -> np.ndarray:
        values = [clamp(safe_float(item.get(key, 0.0)) / max(1e-9, float(scale or 1.0))) for item in list(points or [])]
        return self._resample_values(values, count)

    # --------------------------------------------------
    def _resample_values(self, values: list[float], count: int) -> np.ndarray:
        if not values:
            return np.zeros(max(1, int(count or 1)), dtype=float)
        source = np.asarray(values, dtype=float)
        target_count = max(1, int(count or len(source)))
        if len(source) == target_count:
            return source
        old_x = np.linspace(0.0, 1.0, len(source))
        new_x = np.linspace(0.0, 1.0, target_count)
        return np.asarray(np.interp(new_x, old_x, source), dtype=float)

    # --------------------------------------------------
    def _build_heat_field(self, layout: np.ndarray, activity: np.ndarray) -> np.ndarray:
        grid_x = np.linspace(0.0, 1.0, GRID_SIZE)
        grid_y = np.linspace(0.0, 1.0, GRID_SIZE)
        xx, yy = np.meshgrid(grid_x, grid_y)
        heat = np.zeros_like(xx, dtype=float)
        active_indices = np.argsort(activity)[-min(180, len(activity)):]
        sigma2 = float(HEAT_SIGMA * HEAT_SIGMA)

        for idx in active_indices:
            strength = float(activity[int(idx)] or 0.0)
            if strength <= SAMPLE_ACTIVITY_FLOOR:
                continue
            x, y = layout[int(idx)]
            heat += strength * np.exp(-(((xx - x) ** 2) + ((yy - y) ** 2)) / (2.0 * sigma2))

        max_value = float(np.max(heat)) if heat.size else 0.0
        if max_value > 1e-9:
            heat = heat / max_value

        if self._heat_memory is None or self._heat_memory.shape != heat.shape:
            self._heat_memory = heat
        else:
            self._heat_memory = (self._heat_memory * 0.64) + (heat * 0.36)

        current_heat = np.asarray(self._heat_memory, dtype=float)
        if self._heat_trace is None or self._heat_trace.shape != current_heat.shape:
            self._heat_trace = current_heat.copy()
        else:
            self._heat_trace = np.maximum(self._heat_trace * TRACE_DECAY, current_heat * 0.86)
        return current_heat

    # --------------------------------------------------
    def _input_drive_strength(self, inner: dict, inner_field: dict) -> float:
        outer = dict(inner.get("outer_visual_perception_state", {}) or {})
        perception = dict(inner.get("perception_state", {}) or {})
        processing = dict(inner.get("processing_state", {}) or {})
        return clamp(
            (abs(safe_float(inner_field.get("field_neuron_external_impulse_norm_mean", 0.0))) * 0.34)
            + (safe_float(outer.get("signal_relevance", 0.0)) * 0.22)
            + (safe_float(outer.get("visual_contrast", 0.0)) * 0.14)
            + (safe_float(perception.get("novelty_score", 0.0)) * 0.10)
            + (safe_float(processing.get("processing_intensity", 0.0)) * 0.10)
            + (safe_float(inner_field.get("replay_impulse", 0.0)) * 0.10)
        )

    # --------------------------------------------------
    def _input_hotspot_indices(self, points: list[dict], activity: np.ndarray, input_drive: float) -> np.ndarray:
        if len(activity) <= 0:
            return np.asarray([], dtype=int)
        scores = np.zeros(len(activity), dtype=float)
        for index, item in enumerate(list(points or [])[:len(activity)]):
            external = clamp(safe_float(item.get("external_impulse_norm", 0.0)) / 0.8)
            pressure = clamp(safe_float(item.get("regulation_pressure", 0.0)))
            activation = clamp(safe_float(item.get("activation", 0.0)))
            scores[index] = (external * 0.56) + (pressure * 0.22) + (activation * 0.22)
        if float(np.max(scores)) <= 1e-9:
            scores = np.asarray(activity, dtype=float)
        if float(np.max(scores)) <= max(INPUT_HOTSPOT_MIN_STRENGTH, input_drive * 0.35):
            return np.asarray([], dtype=int)
        return np.argsort(scores)[-min(INPUT_HOTSPOT_COUNT, len(scores)):]

    # --------------------------------------------------
    def _line_arrays(self, segments: list[list[np.ndarray]]) -> tuple[np.ndarray, np.ndarray]:
        if not segments:
            return np.asarray([], dtype=float), np.asarray([], dtype=float)
        xs = []
        ys = []
        for start, end in segments:
            xs.extend([float(start[0]), float(end[0]), np.nan])
            ys.extend([float(start[1]), float(end[1]), np.nan])
        return np.asarray(xs, dtype=float), np.asarray(ys, dtype=float)

    # --------------------------------------------------
    def _resolve_active_link_payload(self, layout: np.ndarray, links: list[tuple[int, int]], activity: np.ndarray, coupling: np.ndarray, external: np.ndarray, hotspot_indices: np.ndarray):
        if hotspot_indices is None:
            hotspot_source = []
        else:
            hotspot_source = np.asarray(hotspot_indices, dtype=int).tolist()

        hotspot_set = set(int(item) for item in list(hotspot_source or []) if 0 <= int(item) < len(activity))
        scored_links = []
        for a, b in list(links or []):
            ai = int(a)
            bi = int(b)
            if ai >= len(activity) or bi >= len(activity):
                continue
            link_activity = float((activity[ai] + activity[bi]) * 0.5)
            link_coupling = float((coupling[ai] + coupling[bi]) * 0.5) if len(coupling) > max(ai, bi) else 0.0
            link_external = float((external[ai] + external[bi]) * 0.5) if len(external) > max(ai, bi) else 0.0
            hotspot_boost = 0.030 if ai in hotspot_set or bi in hotspot_set else 0.0
            strength = float((link_activity * 0.48) + (link_coupling * 0.38) + (link_external * 0.11) + hotspot_boost)
            scored_links.append((strength, [layout[ai], layout[bi]]))
        if not scored_links:
            return [], []
        scored_links = sorted(scored_links, key=lambda item: item[0], reverse=True)
        strengths = np.asarray([float(value) for value, _ in scored_links], dtype=float)
        threshold = max(float(ACTIVE_LINK_FLOOR) * 0.34, float(np.mean(activity)) * 0.72, float(np.percentile(strengths, 78.0)))
        active_payload = [(value, line) for value, line in scored_links if float(value) >= threshold]
        if len(active_payload) < min(int(ACTIVE_LINK_MIN_DRAW), len(scored_links)):
            active_payload = scored_links[:min(int(ACTIVE_LINK_MIN_DRAW), len(scored_links))]
        return scored_links[:min(int(BASE_LINK_MAX_DRAW), len(scored_links))], active_payload[:min(int(ACTIVE_LINK_MAX_DRAW), len(active_payload))]

    # --------------------------------------------------
    def _resolve_areal_flow_segments(self, layout: np.ndarray, activity: np.ndarray) -> list[list[np.ndarray]]:
        if len(layout) <= 1 or len(activity) <= 1:
            return []
        threshold = max(float(AREAL_FLOW_MIN_ACTIVITY), float(np.mean(activity)) * 1.18)
        candidates = [int(idx) for idx in np.argsort(activity)[::-1] if float(activity[int(idx)]) >= threshold]
        centers = []
        for idx in candidates:
            point = layout[int(idx)]
            if any(float(np.linalg.norm(point - layout[int(existing)])) < AREAL_FLOW_RADIUS * 1.35 for existing in centers):
                continue
            centers.append(int(idx))
            if len(centers) >= int(AREAL_FLOW_MAX_MARKERS):
                break
        segments = []
        for idx in centers:
            point = layout[int(idx)]
            dist = np.sqrt(np.sum((layout - point) ** 2, axis=1))
            mask = (dist > 1e-9) & (dist <= float(AREAL_FLOW_RADIUS) * 1.8)
            if not np.any(mask):
                continue
            weights = np.maximum(activity - float(activity[int(idx)]) * 0.45, 0.0) * mask.astype(float)
            if float(np.sum(weights)) <= 1e-9:
                direction = layout[int(np.argsort(dist)[1])] - point
            else:
                direction = np.average(layout, axis=0, weights=weights) - point
            norm = float(np.linalg.norm(direction))
            if norm <= 1e-9:
                continue
            unit = direction / norm
            length = 0.018 + (clamp(activity[int(idx)]) * 0.035)
            segments.append([point - (unit * length * 0.38), point + (unit * length * 0.62)])
        return segments

    # --------------------------------------------------
    def _resolve_outcome_state(self, stats: dict) -> dict:
        data = dict(stats or {})
        trades = safe_int(data.get("trades", 0), 0)
        tp = safe_int(data.get("tp", 0), 0)
        pnl = safe_float(data.get("pnl_netto", 0.0), 0.0)
        attempts = safe_int(data.get("attempts", 0), 0)
        winrate = float(tp / trades) if trades > 0 else 0.0
        return {"trades": trades, "pnl_netto": pnl, "winrate": winrate, "attempts": attempts}

    # --------------------------------------------------
    def _draw_neuron_tissue(self, inner: dict, outcome: dict | None = None):
        inner_field = dict(inner.get("inner_field_perception_state", {}) or {})
        field_state = dict(inner.get("field_state", {}) or {})
        points = self._resolve_neuron_points(inner)
        source_count = len(points)
        tissue_count = self._resolve_tissue_count(inner, points)
        layout = self._fixed_tissue_layout(tissue_count)
        links = self._links_for_layout(layout)
        activity = self._activity_values(points, tissue_count)
        coupling = self._metric_values(points, tissue_count, "coupling_norm", scale=0.8)
        external = self._metric_values(points, tissue_count, "external_impulse_norm", scale=0.8)
        heat = self._build_heat_field(layout, activity)
        input_drive = self._input_drive_strength(inner, inner_field)
        hotspot_indices = self._input_hotspot_indices(points, activity, input_drive)
        base_payload, active_payload = self._resolve_active_link_payload(layout, links, activity, coupling, external, hotspot_indices)
        flow_segments = self._resolve_areal_flow_segments(layout, activity)

        self.trace_item.setImage(np.asarray(self._heat_trace * 255.0, dtype=np.ubyte), autoLevels=False)
        self.heat_item.setImage(np.asarray(heat * 255.0, dtype=np.ubyte), autoLevels=False)
        self.trace_item.setOpacity(0.34)
        self.heat_item.setOpacity(0.34)

        base_x, base_y = self._line_arrays([line for _, line in base_payload])
        active_x, active_y = self._line_arrays([line for _, line in active_payload])
        flow_x, flow_y = self._line_arrays(flow_segments)
        self.base_links_item.setData(base_x, base_y, pen=pg.mkPen(qcolor("#2f4058", 62), width=0.8))
        self.active_links_item.setData(active_x, active_y, pen=pg.mkPen(qcolor(C["inn_blue"], 166), width=1.45))
        self.areal_flow_item.setData(flow_x, flow_y, pen=pg.mkPen(qcolor(C["inn_blue"], 88), width=1.1))

        node_colors = [qcolor(numeric_hex(v), 200) for v in activity]
        glow_colors = [qcolor(numeric_hex(v), int(22 + (clamp(v) * 55))) for v in activity]
        self.glow_item.setData(x=layout[:, 0], y=layout[:, 1], size=18.0 + (activity * 95.0), brush=glow_colors, pen=None)
        self.node_item.setData(x=layout[:, 0], y=layout[:, 1], size=2.4 + (activity * 14.0), brush=node_colors, pen=pg.mkPen(qcolor("#102030", 210), width=0.4))

        top_indices = np.argsort(activity)[-min(36, tissue_count):]
        self.top_glow_item.setData(
            x=layout[top_indices, 0],
            y=layout[top_indices, 1],
            size=70 + (activity[top_indices] * 220),
            brush=[qcolor(numeric_hex(v), int(28 + (clamp(v) * 40))) for v in activity[top_indices]],
            pen=None,
        )

        if len(hotspot_indices) > 0:
            indices = np.asarray(hotspot_indices, dtype=int)
            values = np.asarray(activity[indices], dtype=float)
            self.hotspot_glow_item.setData(
                x=layout[indices, 0],
                y=layout[indices, 1],
                size=34.0 + (values * 96.0) + (float(input_drive) * 38.0),
                brush=qcolor(C["inn_orange"], int(12 + (14 * clamp(input_drive)))),
                pen=None,
            )
            self.hotspot_node_item.setData(
                x=layout[indices, 0],
                y=layout[indices, 1],
                size=4.0 + (values * 10.0),
                brush=qcolor(C["inn_orange"], 92),
                pen=pg.mkPen(qcolor(C["text_hi"], 80), width=0.4),
            )
        else:
            self.hotspot_glow_item.clear()
            self.hotspot_node_item.clear()

        field_density = clamp(field_state.get("field_density", 0.0))
        field_stability = clamp(field_state.get("field_stability", 0.0))
        regulatory_load = clamp(field_state.get("regulatory_load", 0.0))
        action_capacity = clamp(field_state.get("action_capacity", 0.0))
        reorganization_direction = str(inner_field.get("field_reorganization_direction", "stable") or "stable")
        outcome_state = self._resolve_outcome_state(dict(outcome or {}))

        self._set_side_value("tissue", tissue_count)
        self._set_side_value("snapshot", source_count)
        self._set_side_value("density", fmt_num(field_density))
        self._set_side_value("stability", fmt_num(field_stability), numeric_hex(field_stability))
        self._set_side_value("load", fmt_num(regulatory_load), numeric_hex(regulatory_load, invert=True))
        self._set_side_value("capacity", fmt_num(action_capacity), numeric_hex(action_capacity))
        self._set_side_value("activity", fmt_num(float(np.mean(activity)) if len(activity) else 0.0))
        self._set_side_value("coupling", fmt_num(float(np.mean(coupling)) if len(coupling) else 0.0))
        self._set_side_value("external", fmt_num(float(np.mean(external)) if len(external) else 0.0))
        self._set_side_value("input_drive", fmt_num(input_drive))
        self._set_side_value("links", len(links))
        self._set_side_value("active_links", len(active_payload), C["inn_blue"])
        self._set_side_value("areal_flow", len(flow_segments))
        self._set_side_value("hotspots", len(hotspot_indices), C["inn_orange"])
        self._set_side_value("trades", outcome_state["trades"])
        self._set_side_value("winrate", fmt_num(outcome_state["winrate"]), numeric_hex(outcome_state.get("winrate", 0.0)))
        self._set_side_value("pnl", fmt_num(outcome_state["pnl_netto"]))
        self._set_side_value("attempts", outcome_state["attempts"])
        self._set_side_value("reorganization", reorganization_direction, text_state_color(reorganization_direction))

    # --------------------------------------------------
    def _refresh(self):
        inner = safe_load_json(self.inner_path)
        outcome = safe_load_json(self.outcome_path)
        outcome_state = self._resolve_outcome_state(outcome)
        self.lbl_status.setText(f"INNER: {fmt_ts(inner.get('timestamp'))}")
        self.lbl_outcome.setText(f"OUTCOME: trades={outcome_state['trades']} pnl={fmt_num(outcome_state['pnl_netto'])} win={fmt_num(outcome_state['winrate'])}")
        self.lbl_outcome.setStyleSheet(f"color:{numeric_hex(outcome_state.get('winrate', 0.0))};")
        if inner:
            self._draw_neuron_tissue(inner, outcome=outcome)


# ==================================================
# MAIN
# ==================================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default=".", help="Projektbasis mit debug/bot_inner_snapshot.json")
    args = parser.parse_args()

    app = QtWidgets.QApplication(sys.argv)
    window = MCMNeuronFieldGPUGUI(base_dir=Path(args.base))
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
