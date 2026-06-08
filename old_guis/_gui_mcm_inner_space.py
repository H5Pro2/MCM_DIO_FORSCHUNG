from __future__ import annotations

import argparse
import json
import math
import time
import tkinter as tk
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch


# ==================================================
# CONFIG
# ==================================================
REFRESH_MS = 800
SNAPSHOT_BUFFER_MS = 2200
SNAPSHOT_BUFFER_LIMIT = 32
HISTORY_LIMIT = 90

C = {
    "bg_root": "#0d0f13",
    "bg_panel": "#13161c",
    "bg_card": "#181c24",
    "bg_card2": "#1c2130",
    "bg_chart": "#0f1218",
    "border": "#252a36",
    "border_hi": "#2e3548",
    "text_hi": "#e8eaf0",
    "text_med": "#8b92a8",
    "text_lo": "#4a5168",
    "text_label": "#5c6480",
    "inn_green": "#4caf78",
    "inn_orange": "#d4894a",
    "inn_red": "#c05050",
    "inn_blue": "#5b8dd9",
    "inn_purple": "#8b72be",
    "grid": "#1a1f2b",
}

matplotlib.rcParams.update({
    "figure.facecolor": C["bg_panel"],
    "axes.facecolor": C["bg_chart"],
    "axes.edgecolor": C["border"],
    "axes.labelcolor": C["text_med"],
    "axes.titlecolor": C["text_hi"],
    "xtick.color": C["text_lo"],
    "ytick.color": C["text_lo"],
    "grid.color": C["grid"],
    "grid.linewidth": 0.5,
    "text.color": C["text_med"],
    "font.family": "monospace",
    "font.size": 8,
})


# ==================================================
# HELPERS
# ==================================================
def safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return float(default)


# --------------------------------------------------
def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(float(low), min(float(high), float(value)))


# --------------------------------------------------
def clamp_signed(value: float, scale: float = 1.0) -> float:
    safe_scale = max(float(scale), 1e-9)
    return max(-1.0, min(1.0, float(value) / safe_scale))


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
def clone_payload(payload: dict) -> dict:
    if not isinstance(payload, dict):
        return {}

    try:
        return json.loads(json.dumps(payload))
    except Exception:
        return dict(payload)


# --------------------------------------------------
def payload_signature(payload: dict) -> str:
    if not isinstance(payload, dict) or not payload:
        return ""

    try:
        return json.dumps(payload, sort_keys=True, ensure_ascii=False)
    except Exception:
        return str(payload)


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
def get_nested(data: dict, *keys, default=None):
    cur = data
    for key in keys:
        if not isinstance(cur, dict):
            return default
        if key not in cur:
            return default
        cur = cur.get(key)
    return cur if cur is not None else default


# --------------------------------------------------
def numeric_color(value: float, invert: bool = False) -> str:
    v = clamp(value)
    if invert:
        v = 1.0 - v
    if v >= 0.67:
        return C["inn_green"]
    if v >= 0.34:
        return C["inn_orange"]
    return C["inn_red"]


# --------------------------------------------------
def text_state_color(text: str) -> str:
    s = str(text or "").lower()
    if not s:
        return C["text_lo"]

    if any(word in s for word in ["stable", "calm", "clear", "aligned", "act", "ready", "cooperate", "forming", "settling"]):
        return C["inn_green"]
    if any(word in s for word in ["observe", "wait", "hold", "replan", "neutral", "transition", "reorganizing"]):
        return C["inn_orange"]
    if any(word in s for word in ["stress", "critical", "blocked", "threat", "chaotic", "over", "accelerating", "dissolving"]):
        return C["inn_red"]

    return C["inn_blue"]

# --------------------------------------------------
def _vector_norm(values) -> float:
    total = 0.0

    for value in list(values or []):
        try:
            total += float(value) * float(value)
        except Exception:
            continue

    return float(math.sqrt(max(0.0, total)))


# --------------------------------------------------
def _project_snapshot_point(position, scale: float = 2.2):
    coords = list(position or [])

    x = clamp_signed(coords[0] if len(coords) > 0 else 0.0, scale=scale)
    y = clamp_signed(coords[1] if len(coords) > 1 else 0.0, scale=scale)
    z = clamp_signed(coords[2] if len(coords) > 2 else 0.0, scale=scale)

    return float(x), float(y), float(z)

# ==================================================
# UI BLOCKS
# ==================================================
class CardFrame(tk.Frame):
    def __init__(self, parent, title: str = "", title_color: str | None = None, **kwargs):
        bg = kwargs.pop("bg", C["bg_card"])
        super().__init__(parent, bg=bg, highlightbackground=C["border"], highlightthickness=1, **kwargs)
        self._body = tk.Frame(self, bg=bg)

        if title:
            tk.Label(
                self,
                text=title.upper(),
                bg=bg,
                fg=title_color or C["text_label"],
                font=("Courier New", 8, "bold"),
                anchor="w",
                padx=8,
                pady=5,
            ).pack(fill="x")
            tk.Frame(self, bg=C["border"], height=1).pack(fill="x")

        self._body.pack(fill="both", expand=True)

    @property
    def body(self):
        return self._body


# --------------------------------------------------
class KVRow(tk.Frame):
    def __init__(self, parent, key: str = "", value: str = "–", bg: str | None = None):
        _bg = bg or parent.cget("bg")
        super().__init__(parent, bg=_bg)
        self.key_lbl = tk.Label(self, text=key, bg=_bg, fg=C["text_label"], font=("Courier New", 9), anchor="w")
        self.val_lbl = tk.Label(self, text=value, bg=_bg, fg=C["text_hi"], font=("Courier New", 9, "bold"), anchor="e")
        self.key_lbl.pack(side="left", padx=(8, 2))
        self.val_lbl.pack(side="right", padx=(2, 8))

    def update(self, value, color: str | None = None):
        self.val_lbl.config(text=str(value), fg=color or C["text_hi"])


# --------------------------------------------------
class MetricRow(tk.Frame):
    def __init__(self, parent, label: str, bg: str | None = None):
        _bg = bg or parent.cget("bg")
        super().__init__(parent, bg=_bg)
        self.label = tk.Label(self, text=label, bg=_bg, fg=C["text_label"], font=("Courier New", 8), width=21, anchor="w")
        self.canvas = tk.Canvas(self, width=150, height=10, bg=_bg, highlightthickness=0)
        self.value = tk.Label(self, text="0.00", bg=_bg, fg=C["text_hi"], font=("Courier New", 8, "bold"), width=7, anchor="e")
        self.label.pack(side="left", padx=(8, 4))
        self.canvas.pack(side="left", padx=4)
        self.value.pack(side="right", padx=(4, 8))

    def update(self, raw_value: float, normalized_value: float, invert: bool = False):
        color = numeric_color(normalized_value, invert=invert)
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, 150, 10, fill=C["border"], outline="")
        self.canvas.create_rectangle(0, 0, int(150 * clamp(normalized_value)), 10, fill=color, outline="")
        self.value.config(text=fmt_num(raw_value, 3), fg=color)


# ==================================================
# MAIN GUI
# ==================================================
class InnerSpaceGUI:

    def __init__(self, root: tk.Tk, base_dir: Path):
        self.root = root
        self.base_dir = Path(base_dir)
        self.inner_path = self.base_dir / "debug" / "bot_inner_snapshot.json"
        self._after_id = None

        self._inner_buffer: list[dict] = []
        self._display_inner = {}
        self._last_inner_signature = ""
        self._history: list[dict] = []

        self.root.title("MCM Inner Space Monitor")
        self.root.configure(bg=C["bg_root"])
        self.root.minsize(1280, 880)

        self._build_layout()
        self._refresh()

    # --------------------------------------------------
    def _build_layout(self):
        self._build_header()

        self.main = tk.Frame(self.root, bg=C["bg_root"])
        self.main.pack(fill="both", expand=True, padx=6, pady=(0, 6))
        self.main.rowconfigure(0, weight=6)
        self.main.rowconfigure(1, weight=3)
        self.main.columnconfigure(0, weight=1)

        self.card_field = CardFrame(self.main, title="Innenraum / Feldbewegung", title_color=C["inn_purple"], bg=C["bg_card"])
        self.card_field.grid(row=0, column=0, sticky="nsew", pady=(0, 6))

        self.field_fig = Figure(figsize=(10, 6), dpi=100)
        self.field_ax = self.field_fig.add_subplot(111)
        self.field_canvas = FigureCanvasTkAgg(self.field_fig, master=self.card_field.body)
        self.field_canvas.get_tk_widget().pack(fill="both", expand=True)

        self.bottom = tk.Frame(self.main, bg=C["bg_root"])
        self.bottom.grid(row=1, column=0, sticky="nsew")
        self.bottom.columnconfigure(0, weight=3)
        self.bottom.columnconfigure(1, weight=3)
        self.bottom.columnconfigure(2, weight=2)
        self.bottom.rowconfigure(0, weight=1)

        self.card_trace = CardFrame(self.bottom, title="Zeitspur / Feldzentrum", title_color=C["inn_blue"], bg=C["bg_card"])
        self.card_trace.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
        self.trace_fig = Figure(figsize=(4, 3), dpi=100)
        self.trace_ax = self.trace_fig.add_subplot(111)
        self.trace_canvas = FigureCanvasTkAgg(self.trace_fig, master=self.card_trace.body)
        self.trace_canvas.get_tk_widget().pack(fill="both", expand=True)

        self.card_load = CardFrame(self.bottom, title="Druck / Tragfähigkeit", title_color=C["inn_orange"], bg=C["bg_card"])
        self.card_load.grid(row=0, column=1, sticky="nsew", padx=4)
        self.load_fig = Figure(figsize=(4, 3), dpi=100)
        self.load_ax = self.load_fig.add_subplot(111)
        self.load_canvas = FigureCanvasTkAgg(self.load_fig, master=self.card_load.body)
        self.load_canvas.get_tk_widget().pack(fill="both", expand=True)

        self.card_metrics = CardFrame(self.bottom, title="Aktiver Innenzustand", title_color=C["inn_green"], bg=C["bg_card"])
        self.card_metrics.grid(row=0, column=2, sticky="nsew", padx=(4, 0))

        metrics_top = tk.Frame(self.card_metrics.body, bg=self.card_metrics.body.cget("bg"))
        metrics_top.pack(fill="x", pady=(6, 4))
        self.status_rows = {
            "self_state": KVRow(metrics_top, "self_state", "–", bg=metrics_top.cget("bg")),
            "decision": KVRow(metrics_top, "decision", "–", bg=metrics_top.cget("bg")),
            "attractor": KVRow(metrics_top, "attractor", "–", bg=metrics_top.cget("bg")),
            "pattern": KVRow(metrics_top, "pattern", "–", bg=metrics_top.cget("bg")),
            "reorg": KVRow(metrics_top, "reorg", "–", bg=metrics_top.cget("bg")),
            "clusters": KVRow(metrics_top, "clusters", "–", bg=metrics_top.cget("bg")),
            "timestamp": KVRow(metrics_top, "timestamp", "–", bg=metrics_top.cget("bg")),
        }
        for row in self.status_rows.values():
            row.pack(fill="x", pady=1)

        tk.Frame(self.card_metrics.body, bg=C["border"], height=1).pack(fill="x", pady=4)

        metrics_bottom = tk.Frame(self.card_metrics.body, bg=self.card_metrics.body.cget("bg"))
        metrics_bottom.pack(fill="both", expand=True, pady=(4, 8))
        self.metric_rows = {
            "field_density": MetricRow(metrics_bottom, "field_density", bg=metrics_bottom.cget("bg")),
            "field_stability": MetricRow(metrics_bottom, "field_stability", bg=metrics_bottom.cget("bg")),
            "regulatory_load": MetricRow(metrics_bottom, "regulatory_load", bg=metrics_bottom.cget("bg")),
            "action_capacity": MetricRow(metrics_bottom, "action_capacity", bg=metrics_bottom.cget("bg")),
            "recovery_need": MetricRow(metrics_bottom, "recovery_need", bg=metrics_bottom.cget("bg")),
            "survival_pressure": MetricRow(metrics_bottom, "survival_pressure", bg=metrics_bottom.cget("bg")),
            "neuron_activation_mean": MetricRow(metrics_bottom, "neuron_activation_mean", bg=metrics_bottom.cget("bg")),
            "neuron_stability_mean": MetricRow(metrics_bottom, "neuron_stability_mean", bg=metrics_bottom.cget("bg")),
            "neuron_regulation_pressure_mean": MetricRow(metrics_bottom, "neuron_reg_pressure_mean", bg=metrics_bottom.cget("bg")),
            "neuron_memory_norm_mean": MetricRow(metrics_bottom, "neuron_memory_norm_mean", bg=metrics_bottom.cget("bg")),
        }
        for row in self.metric_rows.values():
            row.pack(fill="x", pady=3)
    
    # --------------------------------------------------
    def _build_header(self):
        header = tk.Frame(self.root, bg=C["bg_panel"], highlightbackground=C["border"], highlightthickness=1)
        header.pack(fill="x", padx=6, pady=6)

        left = tk.Frame(header, bg=C["bg_panel"])
        left.pack(side="left", fill="x", expand=True)
        tk.Label(left, text="MCM INNER SPACE MONITOR", bg=C["bg_panel"], fg=C["text_hi"], font=("Courier New", 14, "bold")).pack(anchor="w", padx=10, pady=(8, 0))
        tk.Label(left, text="isolierte Innenraum-Visualisierung · Feld / Zonen / Dynamik · READ ONLY", bg=C["bg_panel"], fg=C["text_med"], font=("Courier New", 9)).pack(anchor="w", padx=10, pady=(0, 8))

        right = tk.Frame(header, bg=C["bg_panel"])
        right.pack(side="right", padx=10)
        self.lbl_base = tk.Label(right, text=str(self.base_dir), bg=C["bg_panel"], fg=C["text_label"], font=("Courier New", 8), anchor="e")
        self.lbl_inner_ts = tk.Label(right, text="INNER: –", bg=C["bg_panel"], fg=C["inn_blue"], font=("Courier New", 8, "bold"), anchor="e")
        self.lbl_base.pack(anchor="e", pady=(8, 0))
        self.lbl_inner_ts.pack(anchor="e", pady=(0, 8))

    # --------------------------------------------------
    def _push_snapshot_buffer(self, payload: dict):
        if not isinstance(payload, dict) or not payload:
            return

        signature = payload_signature(payload)
        if not signature or signature == self._last_inner_signature:
            return

        self._inner_buffer.append({
            "queued_at": time.time(),
            "signature": signature,
            "payload": clone_payload(payload),
        })

        if len(self._inner_buffer) > SNAPSHOT_BUFFER_LIMIT:
            del self._inner_buffer[:-SNAPSHOT_BUFFER_LIMIT]

        self._last_inner_signature = signature

    # --------------------------------------------------
    def _resolve_buffered_payload(self) -> dict:
        now_ts = time.time()

        if not self._inner_buffer:
            return clone_payload(self._display_inner)

        latest_ready_index = None
        for idx, item in enumerate(self._inner_buffer):
            queued_at = float(item.get("queued_at", 0.0) or 0.0)
            if (now_ts - queued_at) >= (SNAPSHOT_BUFFER_MS / 1000.0):
                latest_ready_index = idx

        if latest_ready_index is None:
            return clone_payload(self._display_inner)

        ready_item = dict(self._inner_buffer[latest_ready_index] or {})
        del self._inner_buffer[:latest_ready_index + 1]
        return clone_payload(ready_item.get("payload", {}) or {})

    # --------------------------------------------------
    def _read_buffered_snapshot(self) -> dict:
        inner_live = safe_load_json(self.inner_path)
        self._push_snapshot_buffer(inner_live)

        resolved = self._resolve_buffered_payload()
        if resolved:
            self._display_inner = clone_payload(resolved)

        return clone_payload(self._display_inner)

    # --------------------------------------------------
    def _append_history(self, inner: dict):
        if not isinstance(inner, dict) or not inner:
            return

        field = dict(inner.get("field_state", {}) or {})
        inner_field = dict(inner.get("inner_field_perception_state", {}) or {})
        outer_visual = dict(inner.get("outer_visual_perception_state", {}) or {})
        meta_state = dict(inner.get("meta_regulation_state", {}) or {})
        runtime_state = dict(inner.get("runtime_state", {}) or {})

        field_center_vector = list(inner_field.get("field_center_vector", []) or [])
        field_agent_points = [dict(item or {}) for item in list(inner_field.get("field_agent_points", []) or []) if isinstance(item, dict)]
        field_cluster_links = [dict(item or {}) for item in list(inner_field.get("field_cluster_links", []) or []) if isinstance(item, dict)]

        center_energy = field_center_vector[0] if len(field_center_vector) > 0 else inner_field.get("field_mean_energy", 0.0)
        center_motivation = field_center_vector[1] if len(field_center_vector) > 1 else inner_field.get("field_mean_motivation", 0.0)
        center_risk = field_center_vector[2] if len(field_center_vector) > 2 else inner_field.get("field_mean_risk", 0.0)

        point = {
            "timestamp": inner.get("timestamp"),
            "energy": clamp_signed(center_energy, scale=2.2),
            "motivation": clamp_signed(center_motivation, scale=2.2),
            "risk": clamp_signed(center_risk, scale=2.2),
            "velocity": clamp(safe_float(inner_field.get("field_mean_velocity", 0.0)) / 1.2),
            "cluster_count": max(0, int(inner_field.get("field_cluster_count", 0) or 0)),
            "cluster_mass_mean": clamp(inner_field.get("field_cluster_mass_mean", 0.0)),
            "cluster_mass_max": clamp(inner_field.get("field_cluster_mass_max", 0.0)),
            "cluster_center_spread": clamp(safe_float(inner_field.get("field_cluster_center_spread", 0.0)) / 1.2),
            "cluster_separation": clamp(safe_float(inner_field.get("field_cluster_separation", 0.0)) / 1.4),
            "cluster_center_drift": clamp(safe_float(inner_field.get("field_cluster_center_drift", 0.0)) / 0.6),
            "cluster_count_drift": clamp(inner_field.get("field_cluster_count_drift", 0.0)),
            "field_velocity_trend": clamp_signed(inner_field.get("field_velocity_trend", 0.0), scale=0.35),
            "field_reorganization_direction": str(inner_field.get("field_reorganization_direction", "stable") or "stable"),
            "regulation_pressure": clamp(safe_float(inner_field.get("field_regulation_pressure", 0.0)) / 2.6),
            "focus_direction": clamp_signed(outer_visual.get("focus_direction", 0.0), scale=1.0),
            "focus_strength": clamp(outer_visual.get("focus_strength", 0.0)),
            "signal_relevance": clamp(outer_visual.get("signal_relevance", 0.0)),
            "field_density": clamp(field.get("field_density", 0.0)),
            "field_stability": clamp(field.get("field_stability", 0.0)),
            "regulatory_load": clamp(field.get("regulatory_load", 0.0)),
            "action_capacity": clamp(field.get("action_capacity", 0.0)),
            "recovery_need": clamp(field.get("recovery_need", 0.0)),
            "survival_pressure": clamp(field.get("survival_pressure", 0.0)),
            "field_neuron_count": int(inner_field.get("field_neuron_count", 0) or 0),
            "field_neuron_activation_mean": clamp(inner_field.get("field_neuron_activation_mean", 0.0)),
            "field_neuron_activation_max": clamp(inner_field.get("field_neuron_activation_max", 0.0)),
            "field_neuron_stability_mean": clamp(inner_field.get("field_neuron_stability_mean", 0.0)),
            "field_neuron_regulation_pressure_mean": clamp(inner_field.get("field_neuron_regulation_pressure_mean", 0.0)),
            "field_neuron_memory_norm_mean": clamp(safe_float(inner_field.get("field_neuron_memory_norm_mean", 0.0)) / 1.4),
            "inner_pattern_label": str(inner_field.get("inner_pattern_label", "") or ""),
            "inner_self_state": str(inner_field.get("inner_self_state", inner_field.get("self_state", "stable")) or "stable"),
            "inner_attractor": str(inner_field.get("inner_attractor", inner_field.get("attractor", "neutral")) or "neutral"),
            "agent_count": int(len(field_agent_points)),
            "cluster_link_count": int(len(field_cluster_links)),
            "decision": str(runtime_state.get("proposed_decision", meta_state.get("decision", "WAIT")) or "WAIT"),
        }

        if self._history:
            last = dict(self._history[-1] or {})
            if (
                fmt_num(last.get("energy", 0.0), 4) == fmt_num(point["energy"], 4)
                and fmt_num(last.get("motivation", 0.0), 4) == fmt_num(point["motivation"], 4)
                and fmt_num(last.get("regulatory_load", 0.0), 4) == fmt_num(point["regulatory_load"], 4)
                and fmt_num(last.get("action_capacity", 0.0), 4) == fmt_num(point["action_capacity"], 4)
                and fmt_num(last.get("field_neuron_activation_mean", 0.0), 4) == fmt_num(point["field_neuron_activation_mean"], 4)
                and str(last.get("decision", "")) == str(point["decision"])
                and str(last.get("field_reorganization_direction", "stable")) == str(point["field_reorganization_direction"])
                and str(last.get("inner_pattern_label", "")) == str(point["inner_pattern_label"])
                and int(last.get("agent_count", 0) or 0) == int(point["agent_count"])
            ):
                return

        self._history.append(point)
        if len(self._history) > HISTORY_LIMIT:
            del self._history[:-HISTORY_LIMIT]
   
    # --------------------------------------------------
    def _draw_inner_space(self, inner: dict):
        self.field_ax.clear()
        self.field_ax.set_facecolor(C["bg_chart"])
        self.field_ax.grid(True, alpha=0.35)
        self.field_ax.set_title("Inneres Zustandsfeld / Snapshot-Feldtopologie")
        self.field_ax.set_xlim(-1.12, 1.12)
        self.field_ax.set_ylim(-1.12, 1.12)
        self.field_ax.set_aspect("equal", adjustable="box")
        self.field_ax.axhline(0.0, color=C["border_hi"], linewidth=0.9, alpha=0.95)
        self.field_ax.axvline(0.0, color=C["border_hi"], linewidth=0.9, alpha=0.95)

        inner_field = dict(inner.get("inner_field_perception_state", {}) or {})
        meta_state = dict(inner.get("meta_regulation_state", {}) or {})
        runtime_state = dict(inner.get("runtime_state", {}) or {})
        field_state = dict(inner.get("field_state", {}) or {})

        projection_axes = list(inner_field.get("field_projection_axes", []) or [])
        x_axis_label = str(projection_axes[0] if len(projection_axes) > 0 else "energy")
        y_axis_label = str(projection_axes[1] if len(projection_axes) > 1 else "motivation")

        self.field_ax.set_xlabel(f"{x_axis_label}-projektion")
        self.field_ax.set_ylabel(f"{y_axis_label}-projektion")
        self.field_ax.set_xticks([-1.0, -0.5, 0.0, 0.5, 1.0])
        self.field_ax.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])

        field_center_vector = list(inner_field.get("field_center_vector", []) or [])
        field_agent_points = [dict(item or {}) for item in list(inner_field.get("field_agent_points", []) or []) if isinstance(item, dict)]
        field_cluster_centers = [dict(item or {}) for item in list(inner_field.get("field_cluster_centers", []) or []) if isinstance(item, dict)]
        field_cluster_links = [dict(item or {}) for item in list(inner_field.get("field_cluster_links", []) or []) if isinstance(item, dict)]
        projection_bounds = dict(inner_field.get("field_projection_bounds", {}) or {})

        center_x, center_y, center_risk = _project_snapshot_point(
            field_center_vector if field_center_vector else [
                inner_field.get("field_mean_energy", 0.0),
                inner_field.get("field_mean_motivation", 0.0),
                inner_field.get("field_mean_risk", 0.0),
            ]
        )

        cluster_count = max(0, int(inner_field.get("field_cluster_count", 0) or 0))
        cluster_mass_mean = clamp(inner_field.get("field_cluster_mass_mean", 0.0))
        cluster_mass_max = clamp(inner_field.get("field_cluster_mass_max", 0.0))
        cluster_center_spread = clamp(safe_float(inner_field.get("field_cluster_center_spread", 0.0)) / 1.2)
        cluster_separation = clamp(safe_float(inner_field.get("field_cluster_separation", 0.0)) / 1.4)
        cluster_center_drift_raw = safe_float(inner_field.get("field_cluster_center_drift", 0.0))
        cluster_count_drift_raw = safe_float(inner_field.get("field_cluster_count_drift", 0.0))
        field_velocity_trend_raw = safe_float(inner_field.get("field_velocity_trend", 0.0))
        cluster_center_drift = clamp(cluster_center_drift_raw / 0.6)
        cluster_count_drift = clamp(cluster_count_drift_raw)
        field_velocity_trend = clamp_signed(field_velocity_trend_raw, scale=0.35)
        reorganization_direction = str(inner_field.get("field_reorganization_direction", "stable") or "stable")
        regulation_pressure = clamp(safe_float(inner_field.get("field_regulation_pressure", 0.0)) / 2.6)

        field_density = clamp(field_state.get("field_density", 0.0))
        field_stability = clamp(field_state.get("field_stability", 0.0))
        regulatory_load = clamp(field_state.get("regulatory_load", 0.0))
        action_capacity = clamp(field_state.get("action_capacity", 0.0))
        survival_pressure = clamp(field_state.get("survival_pressure", 0.0))

        reorg_color = text_state_color(reorganization_direction)

        energy_bounds = dict(projection_bounds.get("energy", {}) or {})
        motivation_bounds = dict(projection_bounds.get("motivation", {}) or {})

        energy_span = max(0.0, safe_float(energy_bounds.get("max", 0.0)) - safe_float(energy_bounds.get("min", 0.0)))
        motivation_span = max(0.0, safe_float(motivation_bounds.get("max", 0.0)) - safe_float(motivation_bounds.get("min", 0.0)))

        self.field_ax.add_patch(
            Circle(
                (0.0, 0.0),
                1.00,
                facecolor=C["inn_blue"],
                edgecolor=C["border_hi"],
                linewidth=1.0,
                alpha=0.03,
            )
        )

        if self._history:
            hist_x = [item["energy"] for item in self._history]
            hist_y = [item["motivation"] for item in self._history]
            self.field_ax.plot(hist_x, hist_y, linewidth=0.8, color=C["inn_blue"], alpha=0.12, zorder=2)

        footprint_width = min(1.90, 0.20 + (clamp(energy_span / 4.0) * 1.45) + (cluster_count_drift * 0.18))
        footprint_height = min(1.70, 0.20 + (clamp(motivation_span / 4.0) * 1.30) + (cluster_center_drift * 0.18))
        footprint_angle = float(max(-22.0, min(22.0, (field_velocity_trend * 18.0) + (center_risk * 7.0))))

        self.field_ax.add_patch(
            Ellipse(
                (center_x, center_y),
                width=footprint_width,
                height=footprint_height,
                angle=footprint_angle,
                facecolor=C["inn_purple"],
                edgecolor=reorg_color,
                linewidth=1.0,
                alpha=0.08 + (cluster_center_spread * 0.05),
                zorder=3,
            )
        )

        center_map = {}

        for item in field_cluster_centers:
            cluster_index = int(item.get("cluster_index", len(center_map)) or 0)
            cx, cy, _ = _project_snapshot_point(item.get("center", []))
            center_map[cluster_index] = {
                "x": float(cx),
                "y": float(cy),
                "size": int(item.get("size", 0) or 0),
                "max_radius": float(item.get("max_radius", 0.0) or 0.0),
            }

        for item in field_cluster_links:
            source_index = int(item.get("source_index", -1) or -1)
            target_index = int(item.get("target_index", -1) or -1)

            if source_index not in center_map or target_index not in center_map:
                continue

            source = dict(center_map.get(source_index, {}) or {})
            target = dict(center_map.get(target_index, {}) or {})
            distance_level = clamp(safe_float(item.get("distance", 0.0)) / 2.4)

            self.field_ax.plot(
                [float(source.get("x", 0.0)), float(target.get("x", 0.0))],
                [float(source.get("y", 0.0)), float(target.get("y", 0.0))],
                color=C["inn_blue"],
                linewidth=0.7 + ((1.0 - distance_level) * 0.7),
                alpha=0.08 + ((1.0 - distance_level) * 0.18),
                zorder=4,
            )

        for item in field_agent_points:
            px, py, pr = _project_snapshot_point(item.get("position", []))
            velocity_level = clamp(_vector_norm(item.get("velocity", [])) / 1.4)

            point_color = C["inn_blue"]
            if pr <= -0.28:
                point_color = C["inn_red"]
            elif pr >= 0.28:
                point_color = C["inn_green"]

            self.field_ax.scatter(
                [px],
                [py],
                s=8 + (velocity_level * 14),
                color=point_color,
                alpha=0.14 + (velocity_level * 0.18),
                zorder=5,
            )

        total_agents = max(1, int(len(field_agent_points) or 1))

        for cluster_index, item in center_map.items():
            relative_size = clamp(float(item.get("size", 0) or 0) / float(total_agents))
            radius = min(0.18, 0.04 + (clamp(safe_float(item.get("max_radius", 0.0)) / 1.8) * 0.10))

            self.field_ax.add_patch(
                Circle(
                    (float(item.get("x", 0.0)), float(item.get("y", 0.0))),
                    radius,
                    facecolor=C["inn_purple"],
                    edgecolor=reorg_color,
                    linewidth=0.9,
                    alpha=0.08 + (relative_size * 0.14),
                    zorder=6,
                )
            )

            self.field_ax.scatter(
                [float(item.get("x", 0.0))],
                [float(item.get("y", 0.0))],
                s=18 + (relative_size * 52),
                color=reorg_color,
                edgecolors=C["text_hi"],
                linewidths=0.3,
                alpha=0.94,
                zorder=7,
            )

        stress_radius = 0.08 + (regulation_pressure * 0.14) + (survival_pressure * 0.08) + ((1.0 - action_capacity) * 0.06)
        self.field_ax.add_patch(
            Circle(
                (center_x, center_y),
                stress_radius,
                facecolor=C["inn_red"],
                edgecolor=C["inn_red"],
                linewidth=0.9,
                alpha=0.04 + (regulation_pressure * 0.07),
                zorder=6,
            )
        )

        self.field_ax.scatter(
            [center_x],
            [center_y],
            s=34 + (field_density * 70) + (cluster_mass_max * 28),
            color=C["text_hi"],
            edgecolors=reorg_color,
            linewidths=0.8,
            alpha=0.98,
            zorder=8,
        )

        if len(self._history) >= 2:
            previous_point = dict(self._history[-2] or {})
            prev_x = float(previous_point.get("energy", center_x) or center_x)
            prev_y = float(previous_point.get("motivation", center_y) or center_y)

            self.field_ax.add_patch(
                FancyArrowPatch(
                    (prev_x, prev_y),
                    (center_x, center_y),
                    arrowstyle="->",
                    mutation_scale=11,
                    linewidth=1.0,
                    color=reorg_color,
                    alpha=0.70,
                    zorder=8,
                )
            )

        regulation_dx = float(max(-0.28, min(0.28, field_velocity_trend * 0.24)))
        regulation_dy = float(max(-0.28, min(0.28, ((action_capacity - regulatory_load) * 0.20) - (survival_pressure * 0.12) + (field_stability * 0.06))))

        self.field_ax.add_patch(
            FancyArrowPatch(
                (center_x, center_y),
                (center_x + regulation_dx, center_y + regulation_dy),
                arrowstyle="->",
                mutation_scale=11,
                linewidth=1.0,
                color=C["inn_green"] if regulation_dy >= 0 else C["inn_red"],
                alpha=0.74,
                zorder=8,
            )
        )

        info_left = (
            f"pts={len(field_agent_points)} | links={len(field_cluster_links)}\n"
            f"e_span={fmt_num(energy_span)} | m_span={fmt_num(motivation_span)}"
        )
        info_right = (
            f"center_drift={fmt_num(cluster_center_drift_raw)} | count_drift={fmt_num(cluster_count_drift_raw)}\n"
            f"vel_trend={fmt_num(field_velocity_trend_raw)} | reorg={reorganization_direction}"
        )

        self.field_ax.text(-1.08, 1.04, "oben = Tragfähigkeit", color=C["text_lo"], fontsize=7, ha="left", va="top")
        self.field_ax.text(-1.08, -0.98, info_left, color=C["text_med"], fontsize=7, ha="left", va="bottom")
        self.field_ax.text(1.08, 1.04, f"clusters={cluster_count} | state={str(inner_field.get('self_state', '–'))}", color=C["text_med"], fontsize=7, ha="right", va="top")
        self.field_ax.text(1.08, -0.98, info_right, color=reorg_color, fontsize=7, ha="right", va="bottom")
        self.field_ax.text(0.0, -1.10, f"decision={str(runtime_state.get('proposed_decision', meta_state.get('decision', 'WAIT')))} | attractor={str(inner_field.get('attractor', runtime_state.get('attractor', '–')))}", color=C["text_lo"], fontsize=7, ha="center", va="top")

        self.field_canvas.draw_idle()
    
    # --------------------------------------------------
    def _draw_trace_panel(self):
        self.trace_ax.clear()
        self.trace_ax.set_facecolor(C["bg_chart"])
        self.trace_ax.grid(True, alpha=0.35)
        self.trace_ax.set_title("Feldzentrum über Zeit")

        if not self._history:
            self.trace_canvas.draw_idle()
            return

        indices = list(range(len(self._history)))
        energy = [item["energy"] for item in self._history]
        motivation = [item["motivation"] for item in self._history]
        risk = [item["risk"] for item in self._history]

        self.trace_ax.plot(indices, energy, color=C["inn_blue"], linewidth=1.3, label="energy")
        self.trace_ax.plot(indices, motivation, color=C["inn_green"], linewidth=1.3, label="motivation")
        self.trace_ax.plot(indices, risk, color=C["inn_red"], linewidth=1.1, alpha=0.85, label="risk")
        self.trace_ax.set_ylim(-1.05, 1.05)
        self.trace_ax.legend(loc="upper left", fontsize=7, frameon=False)
        self.trace_canvas.draw_idle()

    # --------------------------------------------------
    def _draw_load_panel(self):
        self.load_ax.clear()
        self.load_ax.set_facecolor(C["bg_chart"])
        self.load_ax.grid(True, alpha=0.35)
        self.load_ax.set_title("Druck / Tragfähigkeit / Neuronen")

        if not self._history:
            self.load_canvas.draw_idle()
            return

        indices = list(range(len(self._history)))
        regulatory_load = [item["regulatory_load"] for item in self._history]
        action_capacity = [item["action_capacity"] for item in self._history]
        recovery_need = [item["recovery_need"] for item in self._history]
        survival_pressure = [item["survival_pressure"] for item in self._history]
        neuron_activation_mean = [item["field_neuron_activation_mean"] for item in self._history]
        neuron_stability_mean = [item["field_neuron_stability_mean"] for item in self._history]

        self.load_ax.plot(indices, regulatory_load, color=C["inn_red"], linewidth=1.2, label="regulatory_load")
        self.load_ax.plot(indices, action_capacity, color=C["inn_green"], linewidth=1.3, label="action_capacity")
        self.load_ax.plot(indices, recovery_need, color=C["inn_blue"], linewidth=1.1, alpha=0.9, label="recovery_need")
        self.load_ax.plot(indices, survival_pressure, color=C["inn_orange"], linewidth=1.1, alpha=0.9, label="survival_pressure")
        self.load_ax.plot(indices, neuron_activation_mean, color=C["inn_purple"], linewidth=1.0, alpha=0.95, linestyle="--", label="neuron_activation")
        self.load_ax.plot(indices, neuron_stability_mean, color=C["text_hi"], linewidth=1.0, alpha=0.85, linestyle=":", label="neuron_stability")
        self.load_ax.set_ylim(0.0, 1.02)
        self.load_ax.legend(loc="upper left", fontsize=7, frameon=False)
        self.load_canvas.draw_idle()

    # --------------------------------------------------
    def _update_metric_cards(self, inner: dict):
        inner_field = dict(inner.get("inner_field_perception_state", {}) or {})
        runtime_state = dict(inner.get("runtime_state", {}) or {})
        meta_state = dict(inner.get("meta_regulation_state", {}) or {})
        field_state = dict(inner.get("field_state", {}) or {})

        agent_count = len([dict(item or {}) for item in list(inner_field.get("field_agent_points", []) or []) if isinstance(item, dict)])
        link_count = len([dict(item or {}) for item in list(inner_field.get("field_cluster_links", []) or []) if isinstance(item, dict)])
        cluster_count = int(inner_field.get("field_cluster_count", 0) or 0)
        neuron_count = int(inner_field.get("field_neuron_count", 0) or 0)

        self_state_value = str(inner_field.get("inner_self_state", inner_field.get("self_state", "–")) or "–")
        attractor_value = str(inner_field.get("inner_attractor", inner_field.get("attractor", runtime_state.get("attractor", "–"))) or "–")
        pattern_value = str(inner_field.get("inner_pattern_label", "") or "–")
        reorg_value = str(inner_field.get("field_reorganization_direction", "stable") or "stable")

        self.status_rows["self_state"].update(
            self_state_value,
            color=text_state_color(self_state_value),
        )
        self.status_rows["decision"].update(
            str(runtime_state.get("proposed_decision", meta_state.get("decision", "WAIT")) or "WAIT"),
            color=text_state_color(str(runtime_state.get("decision_tendency", meta_state.get("pre_action_phase", "hold")) or "hold")),
        )
        self.status_rows["attractor"].update(
            attractor_value,
            color=text_state_color(attractor_value),
        )
        self.status_rows["pattern"].update(
            pattern_value,
            color=text_state_color(pattern_value),
        )
        self.status_rows["reorg"].update(
            reorg_value,
            color=text_state_color(reorg_value),
        )
        self.status_rows["clusters"].update(
            f"{cluster_count} / p={agent_count} / n={neuron_count} / l={link_count}",
            color=text_state_color(reorg_value),
        )
        self.status_rows["timestamp"].update(fmt_ts(inner.get("timestamp")))

        self.metric_rows["field_density"].update(
            safe_float(field_state.get("field_density", 0.0)),
            clamp(field_state.get("field_density", 0.0)),
        )
        self.metric_rows["field_stability"].update(
            safe_float(field_state.get("field_stability", 0.0)),
            clamp(field_state.get("field_stability", 0.0)),
        )
        self.metric_rows["regulatory_load"].update(
            safe_float(field_state.get("regulatory_load", 0.0)),
            clamp(field_state.get("regulatory_load", 0.0)),
            invert=True,
        )
        self.metric_rows["action_capacity"].update(
            safe_float(field_state.get("action_capacity", 0.0)),
            clamp(field_state.get("action_capacity", 0.0)),
        )
        self.metric_rows["recovery_need"].update(
            safe_float(field_state.get("recovery_need", 0.0)),
            clamp(field_state.get("recovery_need", 0.0)),
            invert=True,
        )
        self.metric_rows["survival_pressure"].update(
            safe_float(field_state.get("survival_pressure", 0.0)),
            clamp(field_state.get("survival_pressure", 0.0)),
            invert=True,
        )
        self.metric_rows["neuron_activation_mean"].update(
            safe_float(inner_field.get("field_neuron_activation_mean", 0.0)),
            clamp(inner_field.get("field_neuron_activation_mean", 0.0)),
        )
        self.metric_rows["neuron_stability_mean"].update(
            safe_float(inner_field.get("field_neuron_stability_mean", 0.0)),
            clamp(inner_field.get("field_neuron_stability_mean", 0.0)),
        )
        self.metric_rows["neuron_regulation_pressure_mean"].update(
            safe_float(inner_field.get("field_neuron_regulation_pressure_mean", 0.0)),
            clamp(inner_field.get("field_neuron_regulation_pressure_mean", 0.0)),
            invert=True,
        )
        self.metric_rows["neuron_memory_norm_mean"].update(
            safe_float(inner_field.get("field_neuron_memory_norm_mean", 0.0)),
            clamp(safe_float(inner_field.get("field_neuron_memory_norm_mean", 0.0)) / 1.4),
        )
        
    # --------------------------------------------------
    def _refresh(self):
        inner = self._read_buffered_snapshot()
        self.lbl_inner_ts.config(text=f"INNER: {fmt_ts(inner.get('timestamp'))}")

        if inner:
            self._append_history(inner)
            self._draw_inner_space(inner)
            self._draw_trace_panel()
            self._draw_load_panel()
            self._update_metric_cards(inner)

        self._after_id = self.root.after(REFRESH_MS, self._refresh)

    # --------------------------------------------------
    def run(self):
        self.root.mainloop()

# ==================================================
# MAIN
# ==================================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default=".", help="Projektbasis mit debug/bot_inner_snapshot.json")
    args = parser.parse_args()

    root = tk.Tk()
    app = InnerSpaceGUI(root=root, base_dir=Path(args.base))
    app.run()


if __name__ == "__main__":
    main()
