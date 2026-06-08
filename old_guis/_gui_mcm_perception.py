"""
# ==================================================
# mcm_perception_gui.py
# Standalone READ-ONLY GUI für Außen- und Innenwahrnehmung
# ==================================================
# Liest ausschließlich:
#   debug/bot_visual_snapshot.json
#   debug/bot_inner_snapshot.json
#
# Start:
#   python mcm_perception_gui.py
#   python mcm_perception_gui.py --base /pfad/zum/projekt
# ==================================================
"""

from __future__ import annotations

import argparse
import json
import math
import time
import tkinter as tk
from pathlib import Path
from datetime import datetime

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch


# ==================================================
# CONFIG
# ==================================================
REFRESH_MS = 800
VISIBLE_CANDLES = 80
SNAPSHOT_BUFFER_MS = 2400
SNAPSHOT_BUFFER_LIMIT = 24

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
    "out_hi": "#7ab3d4",
    "out_med": "#4d7fa0",
    "out_lo": "#2a4a5e",
    "inn_green": "#4caf78",
    "inn_orange": "#d4894a",
    "inn_red": "#c05050",
    "inn_blue": "#5b8dd9",
    "inn_purple": "#8b72be",
    "candle_up": "#3d7a5c",
    "candle_dn": "#7a3d3d",
    "candle_wick": "#505870",
    "grid": "#1a1f2b",
}

plt_rc = {
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
}
matplotlib.rcParams.update(plt_rc)


# ==================================================
# HELPERS
# ==================================================
def safe_float(value, default=0.0) -> float:
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
def fmt_num(value, digits=3) -> str:
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
def is_numeric(value) -> bool:
    try:
        float(value)
        return True
    except Exception:
        return False


# --------------------------------------------------
def normalize_metric(value, key_name: str = "") -> float:
    key = str(key_name or "").lower()
    v = safe_float(value, 0.0)

    if "confidence" in key or "quality" in key or "capacity" in key or "need" in key:
        return clamp(v)

    if "density" in key or "stability" in key or "pressure" in key or "release" in key:
        return clamp(v)

    if "lock" in key or "drift" in key or "relevance" in key:
        return clamp(abs(v))

    if "coherence" in key or "direction" in key or "bias" in key:
        return clamp((v + 1.0) / 2.0)

    return clamp(abs(v))


# --------------------------------------------------
def metric_color(value: float, invert: bool = False) -> str:
    v = clamp(value)
    if invert:
        v = 1.0 - v
    if v >= 0.67:
        return C["inn_green"]
    if v >= 0.34:
        return C["inn_orange"]
    return C["inn_red"]


# --------------------------------------------------
def state_color(text: str) -> str:
    s = str(text or "").lower()
    if not s:
        return C["text_lo"]

    if any(word in s for word in ["stable", "calm", "clear", "aligned", "released", "carry", "ready", "plan", "act"]):
        return C["inn_green"]
    if any(word in s for word in ["observe", "wait", "hold", "replan", "neutral", "transition", "boundary"]):
        return C["inn_orange"]
    if any(word in s for word in ["stress", "over", "critical", "blocked", "fail", "threat", "chaotic"]):
        return C["inn_red"]

    return C["inn_blue"]


# ==================================================
# UI BLOCKS
# ==================================================
class CardFrame(tk.Frame):
    def __init__(self, parent, title="", title_color=None, **kwargs):
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
    def __init__(self, parent, key="", value="–", bg=None):
        _bg = bg or parent.cget("bg")
        super().__init__(parent, bg=_bg)
        self.key_lbl = tk.Label(self, text=key, bg=_bg, fg=C["text_label"], font=("Courier New", 9), anchor="w")
        self.val_lbl = tk.Label(self, text=value, bg=_bg, fg=C["text_hi"], font=("Courier New", 9, "bold"), anchor="e")
        self.key_lbl.pack(side="left", padx=(8, 2))
        self.val_lbl.pack(side="right", padx=(2, 8))

    def update(self, value, color=None):
        self.val_lbl.config(text=str(value), fg=color or C["text_hi"])


# --------------------------------------------------
class GaugeBar(tk.Canvas):
    def __init__(self, parent, width=150, height=12, bg=None):
        _bg = bg or parent.cget("bg")
        super().__init__(parent, width=width, height=height, bg=_bg, highlightthickness=0)
        self._width = width
        self._height = height
        self.set_value(0.0)

    def set_value(self, value: float, color: str | None = None):
        self.delete("all")
        v = clamp(value)
        fill = color or metric_color(v)
        self.create_rectangle(0, 0, self._width, self._height, fill=C["border"], outline="")
        fill_width = int(self._width * v)
        if fill_width > 0:
            self.create_rectangle(0, 0, fill_width, self._height, fill=fill, outline="")


# --------------------------------------------------
class MetricBar(tk.Frame):
    def __init__(self, parent, label: str, bg=None):
        _bg = bg or parent.cget("bg")
        super().__init__(parent, bg=_bg)
        self.label = tk.Label(self, text=label, bg=_bg, fg=C["text_label"], font=("Courier New", 8), anchor="w", width=22)
        self.bar = GaugeBar(self, width=130, height=10, bg=_bg)
        self.value = tk.Label(self, text="0.00", bg=_bg, fg=C["text_hi"], font=("Courier New", 8, "bold"), width=7, anchor="e")
        self.label.pack(side="left", padx=(8, 4))
        self.bar.pack(side="left", padx=4)
        self.value.pack(side="right", padx=(4, 8))

    def update(self, value, key_name: str = ""):
        raw = safe_float(value, 0.0)
        normalized = normalize_metric(raw, key_name=key_name or self.label.cget("text"))
        color = metric_color(normalized)
        self.bar.set_value(normalized, color=color)
        self.value.config(text=fmt_num(raw, 3), fg=color)


# ==================================================
# MAIN GUI
# ==================================================
class PerceptionGUI:
    def __init__(self, root: tk.Tk, base_dir: Path):
        self.root = root
        self.base_dir = Path(base_dir)
        self.visual_path = self.base_dir / "debug" / "bot_visual_snapshot.json"
        self.inner_path = self.base_dir / "debug" / "bot_inner_snapshot.json"
        self._after_id = None
        self._visual_buffer = []
        self._inner_buffer = []
        self._display_visual = {}
        self._display_inner = {}
        self._last_visual_signature = ""
        self._last_inner_signature = ""

        self.root.title("MCM Perception Monitor")
        self.root.configure(bg=C["bg_root"])
        self.root.minsize(1400, 860)

        self._build_layout()
        self._refresh()
    # --------------------------------------------------
    def _push_snapshot_buffer(self, buffer_list: list, payload: dict, last_signature: str):
        if not isinstance(payload, dict) or not payload:
            return last_signature

        signature = payload_signature(payload)
        if not signature or signature == last_signature:
            return last_signature

        buffer_list.append({
            "queued_at": time.time(),
            "signature": signature,
            "payload": clone_payload(payload),
        })

        if len(buffer_list) > SNAPSHOT_BUFFER_LIMIT:
            del buffer_list[:-SNAPSHOT_BUFFER_LIMIT]

        return signature
    # --------------------------------------------------    
    def _resolve_buffered_payload(self, buffer_list: list, current_payload: dict) -> dict:
        now_ts = time.time()

        if not buffer_list:
            if isinstance(current_payload, dict) and current_payload:
                return clone_payload(current_payload)
            return {}

        latest_ready_index = None

        for idx, item in enumerate(buffer_list):
            queued_at = float(item.get("queued_at", 0.0) or 0.0)
            if (now_ts - queued_at) >= (SNAPSHOT_BUFFER_MS / 1000.0):
                latest_ready_index = idx

        if latest_ready_index is None:
            if isinstance(current_payload, dict) and current_payload:
                return clone_payload(current_payload)

            oldest = dict(buffer_list[0] or {})
            return clone_payload(oldest.get("payload", {}) or {})

        ready_item = dict(buffer_list[latest_ready_index] or {})
        del buffer_list[:latest_ready_index + 1]
        return clone_payload(ready_item.get("payload", {}) or {})
    # --------------------------------------------------    
    def _read_buffered_snapshots(self):
        visual_live = safe_load_json(self.visual_path)
        inner_live = safe_load_json(self.inner_path)

        self._last_visual_signature = self._push_snapshot_buffer(
            self._visual_buffer,
            visual_live,
            self._last_visual_signature,
        )
        self._last_inner_signature = self._push_snapshot_buffer(
            self._inner_buffer,
            inner_live,
            self._last_inner_signature,
        )

        if self._visual_buffer:
            self._display_visual = self._resolve_buffered_payload(self._visual_buffer, self._display_visual)
        elif visual_live:
            self._display_visual = clone_payload(visual_live)

        if self._inner_buffer:
            self._display_inner = self._resolve_buffered_payload(self._inner_buffer, self._display_inner)
        elif inner_live:
            self._display_inner = clone_payload(inner_live)

        return clone_payload(self._display_visual), clone_payload(self._display_inner)    
    # --------------------------------------------------
    def _build_layout(self):
        self._build_header()

        self.main = tk.Frame(self.root, bg=C["bg_root"])
        self.main.pack(fill="both", expand=True, padx=6, pady=(0, 6))

        self.main.columnconfigure(0, weight=7)
        self.main.columnconfigure(1, weight=6)
        self.main.rowconfigure(0, weight=1)

        self.left = tk.Frame(self.main, bg=C["bg_root"])
        self.right = tk.Frame(self.main, bg=C["bg_root"])
        self.left.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
        self.right.grid(row=0, column=1, sticky="nsew", padx=(4, 0))

        self.left.rowconfigure(0, weight=5)
        self.left.rowconfigure(1, weight=3)
        self.left.columnconfigure(0, weight=1)
        self.left.columnconfigure(1, weight=1)

        self.right.rowconfigure(0, weight=5)
        self.right.rowconfigure(1, weight=2)
        self.right.rowconfigure(2, weight=3)
        self.right.columnconfigure(0, weight=1)

        self._build_left_panel()
        self._build_right_panel()

    # --------------------------------------------------
    def _build_header(self):
        header = tk.Frame(self.root, bg=C["bg_panel"], highlightbackground=C["border"], highlightthickness=1)
        header.pack(fill="x", padx=6, pady=6)

        title = tk.Frame(header, bg=C["bg_panel"])
        title.pack(side="left", fill="x", expand=True)
        tk.Label(title, text="MCM PERCEPTION MONITOR", bg=C["bg_panel"], fg=C["text_hi"], font=("Courier New", 14, "bold")).pack(anchor="w", padx=10, pady=(8, 0))
        tk.Label(title, text="Außenbild links · Innenverarbeitung rechts · READ ONLY", bg=C["bg_panel"], fg=C["text_med"], font=("Courier New", 9)).pack(anchor="w", padx=10, pady=(0, 8))

        status = tk.Frame(header, bg=C["bg_panel"])
        status.pack(side="right", padx=10)
        self.lbl_base = tk.Label(status, text=str(self.base_dir), bg=C["bg_panel"], fg=C["text_label"], font=("Courier New", 8), anchor="e")
        self.lbl_visual_ts = tk.Label(status, text="VISUAL: –", bg=C["bg_panel"], fg=C["out_hi"], font=("Courier New", 8, "bold"), anchor="e")
        self.lbl_inner_ts = tk.Label(status, text="INNER: –", bg=C["bg_panel"], fg=C["inn_blue"], font=("Courier New", 8, "bold"), anchor="e")
        self.lbl_base.pack(anchor="e", pady=(8, 0))
        self.lbl_visual_ts.pack(anchor="e")
        self.lbl_inner_ts.pack(anchor="e", pady=(0, 8))

    # --------------------------------------------------
    def _build_left_panel(self):
        chart_card = CardFrame(self.left, title="Außenbild / Chart", title_color=C["out_hi"], bg=C["bg_card"])
        chart_card.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 6))

        self.fig = Figure(figsize=(8, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_card.body)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.card_candle = CardFrame(self.left, title="Candle State", title_color=C["out_hi"], bg=C["bg_card2"])
        self.card_tension = CardFrame(self.left, title="Tension State", title_color=C["out_hi"], bg=C["bg_card2"])
        self.card_visual = CardFrame(self.left, title="Visual Market State", title_color=C["out_hi"], bg=C["bg_card2"])
        self.card_structure = CardFrame(self.left, title="Structure Perception", title_color=C["out_hi"], bg=C["bg_card2"])

        self.card_candle.grid(row=1, column=0, sticky="nsew", padx=(0, 3))
        self.card_tension.grid(row=1, column=1, sticky="nsew", padx=(3, 0))
        self.card_visual.grid(row=2, column=0, sticky="nsew", padx=(0, 3), pady=(6, 0))
        self.card_structure.grid(row=2, column=1, sticky="nsew", padx=(3, 0), pady=(6, 0))

        self.left.rowconfigure(1, weight=1)
        self.left.rowconfigure(2, weight=1)

        self.candle_rows = self._make_rows(self.card_candle.body, [
            ("direction", "–"),
            ("body_ratio", "–"),
            ("close_position", "–"),
            ("range_ratio", "–"),
            ("volume_ratio", "–"),
        ])

        self.tension_rows = self._make_rows(self.card_tension.body, [
            ("energy", "–"),
            ("coherence", "–"),
            ("momentum", "–"),
            ("stability", "–"),
            ("perceived_pressure", "–"),
            ("volume_pressure", "–"),
        ])

        self.visual_rows = self._make_rows(self.card_visual.body, [
            ("trend_bias", "–"),
            ("range_pressure", "–"),
            ("impulse_bias", "–"),
            ("continuation_bias", "–"),
            ("volatility_regime", "–"),
            ("market_form", "–"),
        ])

        self.structure_rows = self._make_rows(self.card_structure.body, [
            ("structure_seen", "–"),
            ("swing_high_strength", "–"),
            ("swing_low_strength", "–"),
            ("zone_proximity", "–"),
            ("structure_stability", "–"),
            ("context_confidence", "–"),
        ])

    # --------------------------------------------------
    def _build_right_panel(self):
        card_field_visual = CardFrame(self.right, title="Innenfeld / emergente Zonen", title_color=C["inn_purple"], bg=C["bg_card"])
        card_field_visual.grid(row=0, column=0, sticky="nsew", pady=(0, 6))

        self.inner_fig = Figure(figsize=(6, 5), dpi=100)
        self.inner_ax = self.inner_fig.add_subplot(111)
        self.inner_canvas = FigureCanvasTkAgg(self.inner_fig, master=card_field_visual.body)
        self.inner_canvas.get_tk_widget().pack(fill="both", expand=True)

        card_field = CardFrame(self.right, title="Innenfeld / Zustandsachsen", title_color=C["inn_purple"], bg=C["bg_card"])
        card_field.grid(row=1, column=0, sticky="nsew", pady=(0, 6))

        field_top = tk.Frame(card_field.body, bg=card_field.body.cget("bg"))
        field_top.pack(fill="x", pady=6)

        self.field_bars = {}
        for label in [
            "field_density",
            "field_stability",
            "regulatory_load",
            "action_capacity",
            "recovery_need",
            "survival_pressure",
        ]:
            bar = MetricBar(field_top, label=label, bg=field_top.cget("bg"))
            bar.pack(fill="x", pady=3)
            self.field_bars[label] = bar

        card_summary = CardFrame(self.right, title="Aktive Innenrückmeldung", title_color=C["inn_green"], bg=C["bg_card"])
        card_summary.grid(row=2, column=0, sticky="nsew")

        summary_top = tk.Frame(card_summary.body, bg=card_summary.body.cget("bg"))
        summary_top.pack(fill="x", pady=(6, 2))
        self.summary_rows = self._make_rows(summary_top, [
            ("focus_confidence", "–"),
            ("target_lock", "–"),
            ("target_drift", "–"),
            ("competition_bias", "–"),
            ("observation_mode", "–"),
            ("decision_hint", "–"),
        ])

        summary_bottom = tk.Frame(card_summary.body, bg=card_summary.body.cget("bg"))
        summary_bottom.pack(fill="both", expand=True, pady=(4, 8))
        summary_bottom.columnconfigure(0, weight=1)
        summary_bottom.columnconfigure(1, weight=1)
        summary_bottom.rowconfigure(0, weight=1)
        summary_bottom.rowconfigure(1, weight=1)
        summary_bottom.rowconfigure(2, weight=1)
        summary_bottom.rowconfigure(3, weight=1)
        summary_bottom.rowconfigure(4, weight=1)

        self.pipeline_cards = {}
        blocks = [
            "outer_visual_perception_state",
            "inner_field_perception_state",
            "perception_state",
            "processing_state",
            "felt_state",
            "thought_state",
            "meta_regulation_state",
            "expectation_state",
        ]

        for idx, name in enumerate(blocks):
            row = idx // 2
            col = idx % 2
            sub = CardFrame(summary_bottom, title=name, title_color=C["inn_blue"], bg=C["bg_card2"])
            sub.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)
            self.pipeline_cards[name] = self._make_dynamic_rows(sub.body, limit=5)

        action_card = CardFrame(summary_bottom, title="action_intent_state", title_color=C["inn_green"], bg=C["bg_card2"])
        execution_card = CardFrame(summary_bottom, title="execution_state", title_color=C["inn_green"], bg=C["bg_card2"])
        action_card.grid(row=4, column=0, sticky="nsew", padx=(4, 4), pady=(4, 0))
        execution_card.grid(row=4, column=1, sticky="nsew", padx=(4, 4), pady=(4, 0))

        self.action_rows = self._make_dynamic_rows(action_card.body, limit=5)
        self.execution_rows = self._make_dynamic_rows(execution_card.body, limit=5)
    
    # --------------------------------------------------
    def _draw_inner_field(self, inner: dict):
        self.inner_ax.clear()
        self.inner_ax.set_facecolor(C["bg_chart"])
        self.inner_ax.grid(True, alpha=0.35)
        self.inner_ax.set_title("Inneres Zustandsfeld / emergente Zonen")
        self.inner_ax.set_xlim(-1.15, 1.15)
        self.inner_ax.set_ylim(-1.15, 1.15)
        self.inner_ax.set_aspect("equal", adjustable="box")
        self.inner_ax.axhline(0.0, color=C["border_hi"], linewidth=0.8, alpha=0.9)
        self.inner_ax.axvline(0.0, color=C["border_hi"], linewidth=0.8, alpha=0.9)
        self.inner_ax.set_xticks([-1.0, -0.5, 0.0, 0.5, 1.0])
        self.inner_ax.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
        self.inner_ax.set_xlabel("Energie / Richtung")
        self.inner_ax.set_ylabel("Motivation / Tragfähigkeit")

        inner_field = dict(inner.get("inner_field_perception_state", {}) or {})
        outer_visual = dict(inner.get("outer_visual_perception_state", {}) or {})
        thought_state = dict(inner.get("thought_state", {}) or {})
        meta_state = dict(inner.get("meta_regulation_state", {}) or {})
        field_state = {
            "field_density": safe_float(inner.get("field_density", 0.0)),
            "field_stability": safe_float(inner.get("field_stability", 0.0)),
            "regulatory_load": safe_float(inner.get("regulatory_load", 0.0)),
            "action_capacity": safe_float(inner.get("action_capacity", 0.0)),
            "recovery_need": safe_float(inner.get("recovery_need", 0.0)),
            "survival_pressure": safe_float(inner.get("survival_pressure", 0.0)),
        }

        center_x = clamp_signed(inner_field.get("field_mean_energy", 0.0), scale=2.2)
        center_y = clamp_signed(inner_field.get("field_mean_motivation", 0.0), scale=2.2)
        risk_signed = clamp_signed(inner_field.get("field_mean_risk", 0.0), scale=2.2)
        velocity_level = clamp(safe_float(inner_field.get("field_mean_velocity", 0.0)) / 1.2)
        cluster_count = max(0, int(inner_field.get("field_cluster_count", 0) or 0))
        regulation_pressure = clamp(safe_float(inner_field.get("field_regulation_pressure", 0.0)) / 2.6)

        focus_direction = clamp_signed(outer_visual.get("focus_direction", 0.0), scale=1.0)
        focus_strength = clamp(outer_visual.get("focus_strength", 0.0))
        focus_confidence = clamp(outer_visual.get("focus_confidence", 0.0))
        target_lock = clamp(outer_visual.get("target_lock", thought_state.get("target_lock", 0.0)))
        signal_relevance = clamp(outer_visual.get("signal_relevance", 0.0))
        target_map = clamp(outer_visual.get("visual_target_map", 0.0))
        threat_map = clamp(outer_visual.get("visual_threat_map", 0.0))
        optic_flow = clamp_signed(outer_visual.get("visual_optic_flow", 0.0), scale=1.0)
        competition_bias = clamp_signed(inner.get("competition_bias", inner_field.get("competition_bias", 0.0)), scale=1.0)
        target_drift = clamp_signed(inner.get("target_drift", thought_state.get("target_drift", 0.0)), scale=1.0)

        field_density = clamp(field_state["field_density"])
        field_stability = clamp(field_state["field_stability"])
        regulatory_load = clamp(field_state["regulatory_load"])
        action_capacity = clamp(field_state["action_capacity"])
        recovery_need = clamp(field_state["recovery_need"])
        survival_pressure = clamp(field_state["survival_pressure"])

        self.inner_ax.add_patch(Circle((0.0, 0.0), 1.0, facecolor=C["inn_blue"], edgecolor=C["border_hi"], linewidth=1.0, alpha=0.05))
        self.inner_ax.add_patch(Circle((center_x, center_y), 0.16 + (field_density * 0.20) + (velocity_level * 0.08), facecolor=C["inn_purple"], edgecolor=C["inn_purple"], alpha=0.20 + (regulation_pressure * 0.14), linewidth=1.1))
        self.inner_ax.scatter([center_x], [center_y], s=80 + (field_density * 180), color=C["inn_blue"], alpha=0.95, zorder=4)

        zone_count = max(1, min(4, cluster_count if cluster_count > 0 else int(round(1 + (field_density * 3.0)))))
        angle_seed = (focus_direction * 1.2) + (competition_bias * 0.9) + (risk_signed * 0.6)

        for idx in range(zone_count):
            angle = angle_seed + ((math.pi * 2.0) / max(1, zone_count)) * idx
            radial = 0.20 + (field_density * 0.24) + (velocity_level * 0.10) + (idx * 0.02)
            zone_x = center_x + (math.cos(angle) * radial)
            zone_y = center_y + (math.sin(angle) * (0.14 + (field_stability * 0.18) + (velocity_level * 0.10)))
            zone_radius = 0.04 + (field_density * 0.05) + ((1.0 - field_stability) * 0.03)
            self.inner_ax.add_patch(Circle((zone_x, zone_y), zone_radius, facecolor=C["inn_purple"], edgecolor=C["inn_blue"], alpha=0.16, linewidth=0.9))

        opportunity_x = center_x + (focus_direction * (0.28 + (target_lock * 0.26)))
        opportunity_y = center_y + ((action_capacity - 0.5) * 0.58) + (focus_strength * 0.18)
        opportunity_radius = 0.08 + (max(target_map, signal_relevance) * 0.16)
        self.inner_ax.add_patch(Circle((opportunity_x, opportunity_y), opportunity_radius, facecolor=C["inn_green"], edgecolor=C["inn_green"], alpha=0.16 + (focus_confidence * 0.18), linewidth=1.1))

        threat_x = center_x - (focus_direction * (0.18 + (threat_map * 0.22))) + (competition_bias * 0.14)
        threat_y = center_y - (survival_pressure * 0.42) - (regulatory_load * 0.16)
        threat_radius = 0.08 + (max(threat_map, survival_pressure) * 0.18)
        self.inner_ax.add_patch(Circle((threat_x, threat_y), threat_radius, facecolor=C["inn_red"], edgecolor=C["inn_red"], alpha=0.16 + (regulation_pressure * 0.18), linewidth=1.1))

        recovery_x = center_x - (competition_bias * 0.18)
        recovery_y = center_y - 0.22 - (recovery_need * 0.26) + (field_stability * 0.16)
        recovery_radius = 0.07 + (recovery_need * 0.14)
        self.inner_ax.add_patch(Circle((recovery_x, recovery_y), recovery_radius, facecolor=C["out_hi"], edgecolor=C["out_hi"], alpha=0.15 + (recovery_need * 0.14), linewidth=1.0))

        vector_dx = (focus_direction * 0.22) + (target_drift * 0.20) + (optic_flow * 0.10)
        vector_dy = ((action_capacity - regulatory_load) * 0.22) - (survival_pressure * 0.10)
        self.inner_ax.add_patch(FancyArrowPatch((center_x, center_y), (center_x + vector_dx, center_y + vector_dy), arrowstyle="->", mutation_scale=12, linewidth=1.3, color=C["inn_green"], alpha=0.92))

        counter_dx = (-focus_direction * 0.14) + (competition_bias * 0.18)
        counter_dy = -(regulation_pressure * 0.22) - (recovery_need * 0.12)
        self.inner_ax.add_patch(FancyArrowPatch((center_x, center_y), (center_x + counter_dx, center_y + counter_dy), arrowstyle="->", mutation_scale=11, linewidth=1.0, color=C["inn_red"], alpha=0.78))

        self.inner_ax.text(-1.08, 1.04, "oben = Tragfähigkeit", color=C["text_lo"], fontsize=7, ha="left", va="top")
        self.inner_ax.text(-1.08, -1.08, "rechts = Impuls / Ziel", color=C["text_lo"], fontsize=7, ha="left", va="bottom")
        self.inner_ax.text(1.08, 1.04, f"clusters={cluster_count} | state={str(inner_field.get('self_state', meta_state.get('decision', '–')))}", color=C["text_med"], fontsize=7, ha="right", va="top")

        self.inner_canvas.draw_idle()
    
    # --------------------------------------------------
    def _make_rows(self, parent, rows: list[tuple[str, str]]):
        mapping = {}
        for key, value in rows:
            row = KVRow(parent, key=key, value=value, bg=parent.cget("bg"))
            row.pack(fill="x", pady=1)
            mapping[key] = row
        return mapping

    # --------------------------------------------------
    def _make_dynamic_rows(self, parent, limit=6):
        mapping = {"__parent__": parent}
        for _ in range(limit):
            row = KVRow(parent, key="", value="", bg=parent.cget("bg"))
            row.pack(fill="x", pady=1)
            mapping.setdefault("__rows__", []).append(row)
        return mapping

    # --------------------------------------------------
    def _update_fixed_rows(self, mapping: dict, payload: dict, keys: list[str]):
        for key in keys:
            row = mapping.get(key)
            if row is None:
                continue
            value = payload.get(key, "–")
            if isinstance(value, bool):
                row.update(str(value), color=state_color(str(value)))
            elif is_numeric(value):
                row.update(fmt_num(value, 3), color=metric_color(normalize_metric(value, key)))
            else:
                row.update(str(value), color=state_color(str(value)))

    # --------------------------------------------------
    def _update_dynamic_rows(self, holder: dict, payload: dict):
        rows = list(holder.get("__rows__", []))
        items = []
        for key, value in dict(payload or {}).items():
            if isinstance(value, dict):
                continue
            items.append((str(key), value))

        items.sort(key=lambda entry: entry[0])

        for idx, row in enumerate(rows):
            if idx >= len(items):
                row.key_lbl.config(text="")
                row.update("", color=C["text_hi"])
                continue

            key, value = items[idx]
            row.key_lbl.config(text=key)
            if isinstance(value, bool):
                row.update(str(value), color=state_color(str(value)))
            elif is_numeric(value):
                row.update(fmt_num(value, 3), color=metric_color(normalize_metric(value, key)))
            else:
                row.update(str(value), color=state_color(str(value)))

    # --------------------------------------------------
    def _draw_chart(self, visual: dict):
        self.ax.clear()
        self.ax.set_facecolor(C["bg_chart"])
        self.ax.grid(True)
        self.ax.set_title("OHLC Außenwahrnehmung")

        window = list(visual.get("window", []) or [])[-VISIBLE_CANDLES:]
        if not window:
            self.ax.text(0.5, 0.5, "kein Snapshot", ha="center", va="center", transform=self.ax.transAxes, color=C["text_lo"])
            self.canvas.draw_idle()
            return

        lows = []
        highs = []
        closes = []

        for idx, candle in enumerate(window):
            o = safe_float(candle.get("open"))
            h = safe_float(candle.get("high"), o)
            l = safe_float(candle.get("low"), o)
            c = safe_float(candle.get("close"), o)
            lows.append(l)
            highs.append(h)
            closes.append(c)

            color = C["candle_up"] if c >= o else C["candle_dn"]
            self.ax.vlines(idx, l, h, color=C["candle_wick"], linewidth=1.0, zorder=1)
            body_low = min(o, c)
            body_height = max(abs(c - o), max((max(highs) - min(lows)) * 0.0008, 1e-9))
            self.ax.add_patch(Rectangle((idx - 0.32, body_low), 0.64, body_height, facecolor=color, edgecolor=color, linewidth=0.8, zorder=2))

        self.ax.plot(range(len(closes)), closes, linewidth=1.0, color=C["out_hi"], alpha=0.65)

        tension = dict(visual.get("tension_state", {}) or {})
        structure = dict(visual.get("structure_perception_state", {}) or {})
        last_close = closes[-1]
        price_span = max(max(highs) - min(lows), 1e-9)

        energy = safe_float(tension.get("energy", 0.0))
        coherence = safe_float(tension.get("coherence", 0.0))
        zone_proximity = safe_float(structure.get("zone_proximity", 0.0))

        coherence_offset = price_span * 0.08 * max(-1.0, min(1.0, coherence))
        energy_band = price_span * 0.03 * clamp(energy, 0.0, 1.5)
        zone_band = price_span * 0.04 * clamp(zone_proximity)

        self.ax.axhline(last_close + coherence_offset, color=C["inn_blue"], linestyle="--", linewidth=0.9, alpha=0.8)
        self.ax.axhspan(last_close - energy_band, last_close + energy_band, color=C["inn_orange"], alpha=0.10)
        self.ax.axhspan(last_close - zone_band, last_close + zone_band, color=C["inn_purple"], alpha=0.08)

        self.ax.set_xlim(-1, len(window))
        self.ax.set_ylabel("Preis")
        self.ax.set_xlabel("letzte Candles")

        try:
            self.ax.set_ylim(min(lows) - price_span * 0.05, max(highs) + price_span * 0.05)
        except Exception:
            pass

        self.canvas.draw_idle()

    # --------------------------------------------------
    def _refresh(self):
        visual, inner = self._read_buffered_snapshots()

        self.lbl_visual_ts.config(text=f"VISUAL: {fmt_ts(visual.get('timestamp'))}")
        self.lbl_inner_ts.config(text=f"INNER:  {fmt_ts(inner.get('timestamp'))}")

        self._draw_chart(visual)
        self._draw_inner_field(inner)

        candle_state = dict(visual.get("candle_state", {}) or {})
        tension_state = dict(visual.get("tension_state", {}) or {})
        visual_market_state = dict(visual.get("visual_market_state", {}) or {})
        structure_state = dict(visual.get("structure_perception_state", {}) or {})

        self._update_fixed_rows(self.candle_rows, candle_state, list(self.candle_rows.keys()))
        self._update_fixed_rows(self.tension_rows, tension_state, list(self.tension_rows.keys()))
        self._update_fixed_rows(self.visual_rows, visual_market_state, list(self.visual_rows.keys()))
        self._update_fixed_rows(self.structure_rows, structure_state, list(self.structure_rows.keys()))

        field_state = dict(inner.get("field_state", {}) or {})
        if not field_state:
            field_state = {
                "field_density": inner.get("field_density", 0.0),
                "field_stability": inner.get("field_stability", 0.0),
                "regulatory_load": inner.get("regulatory_load", 0.0),
                "action_capacity": inner.get("action_capacity", 0.0),
                "recovery_need": inner.get("recovery_need", 0.0),
                "survival_pressure": inner.get("survival_pressure", 0.0),
            }

        for key, bar in self.field_bars.items():
            bar.update(field_state.get(key, 0.0), key_name=key)

        for key, holder in self.pipeline_cards.items():
            self._update_dynamic_rows(holder, dict(inner.get(key, {}) or {}))

        decision_hint = get_nested(inner, "meta_regulation_state", "decision", default=None)
        if decision_hint is None:
            decision_hint = get_nested(inner, "review_tendency_hint", default="–")

        summary_payload = {
            "focus_confidence": inner.get("focus_confidence", get_nested(inner, "outer_visual_perception_state", "focus_confidence", default=0.0)),
            "target_lock": inner.get("target_lock", get_nested(inner, "thought_state", "target_lock", default=0.0)),
            "target_drift": inner.get("target_drift", get_nested(inner, "thought_state", "target_drift", default=0.0)),
            "competition_bias": inner.get("competition_bias", get_nested(inner, "inner_field_perception_state", "competition_bias", default=0.0)),
            "observation_mode": inner.get("observation_mode", get_nested(inner, "meta_regulation_state", "observation_mode", default=False)),
            "decision_hint": decision_hint if decision_hint is not None else "–",
        }
        self._update_fixed_rows(self.summary_rows, summary_payload, list(self.summary_rows.keys()))

        self._update_dynamic_rows(self.action_rows, dict(inner.get("action_intent_state", {}) or {}))
        self._update_dynamic_rows(self.execution_rows, dict(inner.get("execution_state", {}) or {}))

        self._after_id = self.root.after(REFRESH_MS, self._refresh)

    # --------------------------------------------------
    def close(self):
        if self._after_id is not None:
            try:
                self.root.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None


# ==================================================
# MAIN
# ==================================================
def parse_args():
    parser = argparse.ArgumentParser(description="Standalone GUI für MCM Außen- und Innenwahrnehmung")
    parser.add_argument("--base", default=".", help="Projektbasis mit debug/ Ordner")
    return parser.parse_args()


# --------------------------------------------------
def main():
    args = parse_args()
    root = tk.Tk()
    app = PerceptionGUI(root, Path(args.base))
    root.protocol("WM_DELETE_WINDOW", lambda: (app.close(), root.destroy()))
    root.mainloop()


if __name__ == "__main__":
    main()
