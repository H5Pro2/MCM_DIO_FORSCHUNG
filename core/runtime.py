"""MCM runtime loop.

This module owns the generic tick/advance runtime shell. Brain formulas and
debug protocols are injected as callbacks by `MCM_Brain_Modell.py`.
"""

from __future__ import annotations


class MCMBrainRuntime:
    def __init__(
        self,
        bot=None,
        *,
        normalize_active_context_trace=None,
        decay_active_context_trace=None,
        compute_runtime_result=None,
        apply_runtime_result=None,
        record_neuro_transition_protocol=None,
    ):
        self.bot = bot
        self.window = []
        self.candle_state = {}
        self.tension_state = {}
        self.visual_market_state = {}
        self.structure_perception_state = {}
        self.temporal_perception_state = {}
        self.timestamp = None
        self.runtime_tick_seq = 0
        self.last_result = None
        self.last_impulse = {}
        self.pending_impulse = None
        self.brain_snapshot = {}
        self.active_context_trace = {}
        self._market_tick_pending = False
        self._normalize_active_context_trace = normalize_active_context_trace
        self._decay_active_context_trace = decay_active_context_trace
        self._compute_runtime_result = compute_runtime_result
        self._apply_runtime_result = apply_runtime_result
        self._record_neuro_transition_protocol = record_neuro_transition_protocol

    def restore_from_bot(self):
        if self.bot is None:
            return None

        runtime_snapshot = dict(getattr(self.bot, "mcm_runtime_snapshot", {}) or {})
        runtime_decision_state = dict(getattr(self.bot, "mcm_runtime_decision_state", {}) or {})
        runtime_brain_snapshot = dict(getattr(self.bot, "mcm_runtime_brain_snapshot", {}) or {})

        self.timestamp = runtime_snapshot.get("timestamp", None)
        self.runtime_tick_seq = int(runtime_snapshot.get("runtime_tick_seq", 0) or 0)
        self.last_result = dict(runtime_decision_state.get("entry_result", {}) or {})
        self.brain_snapshot = dict(runtime_brain_snapshot or {})

        trace = runtime_snapshot.get(
            "active_context_trace",
            runtime_brain_snapshot.get("active_context_trace", {}),
        )
        if self._normalize_active_context_trace is not None:
            trace = self._normalize_active_context_trace(trace)
        self.active_context_trace = dict(trace or {})
        setattr(self.bot, "active_context_trace", dict(self.active_context_trace or {}))
        self.pending_impulse = None
        self._market_tick_pending = False

        world_state = dict(runtime_brain_snapshot.get("world_state", {}) or {})
        impulse_candle_state = dict(world_state.get("candle_state", {}) or {})
        impulse_tension_state = dict(world_state.get("tension_state", {}) or {})
        impulse_visual_market_state = dict(world_state.get("visual_market_state", {}) or {})
        impulse_structure_perception_state = dict(world_state.get("structure_perception_state", {}) or {})
        impulse_temporal_perception_state = dict(world_state.get("temporal_perception_state", {}) or {})

        self.tension_state = dict(impulse_tension_state or {})
        self.visual_market_state = dict(impulse_visual_market_state or {})
        self.structure_perception_state = dict(impulse_structure_perception_state or {})
        self.temporal_perception_state = dict(impulse_temporal_perception_state or {})

        if impulse_candle_state or impulse_tension_state or impulse_visual_market_state or impulse_structure_perception_state or impulse_temporal_perception_state:
            self.last_impulse = {
                "timestamp": self.timestamp,
                "window": [],
                "candle_state": dict(impulse_candle_state),
                "tension_state": dict(impulse_tension_state),
                "visual_market_state": dict(impulse_visual_market_state),
                "structure_perception_state": dict(impulse_structure_perception_state),
                "temporal_perception_state": dict(impulse_temporal_perception_state),
            }
        else:
            self.last_impulse = {}

        return self.read_snapshot()

    def has_impulse(self):
        pending_impulse = dict(self.pending_impulse or {})
        last_impulse = dict(self.last_impulse or {})

        if pending_impulse:
            return True
        if list(last_impulse.get("window", []) or []):
            return True
        if dict(last_impulse.get("candle_state", {}) or {}):
            return True
        if dict(last_impulse.get("tension_state", {}) or {}):
            return True
        if dict(last_impulse.get("visual_market_state", {}) or {}):
            return True
        if dict(last_impulse.get("structure_perception_state", {}) or {}):
            return True
        if dict(last_impulse.get("temporal_perception_state", {}) or {}):
            return True

        return False

    def ingest_market_impulse(
        self,
        window,
        candle_state,
        tension_state=None,
        visual_market_state=None,
        structure_perception_state=None,
        temporal_perception_state=None,
    ):
        self.window = [dict(item or {}) for item in list(window or []) if isinstance(item, dict)]
        self.candle_state = dict(candle_state or {})
        self.tension_state = dict(tension_state or {})
        self.visual_market_state = dict(visual_market_state or {})
        self.structure_perception_state = dict(structure_perception_state or {})
        self.temporal_perception_state = dict(temporal_perception_state or {})

        next_timestamp = (self.window[-1] or {}).get("timestamp") if self.window else None
        self._market_tick_pending = bool(next_timestamp != self.timestamp)
        self.timestamp = next_timestamp

        impulse = {
            "timestamp": self.timestamp,
            "window": [dict(item or {}) for item in list(self.window or []) if isinstance(item, dict)],
            "candle_state": dict(self.candle_state or {}),
            "tension_state": dict(self.tension_state or {}),
            "visual_market_state": dict(self.visual_market_state or {}),
            "structure_perception_state": dict(self.structure_perception_state or {}),
            "temporal_perception_state": dict(self.temporal_perception_state or {}),
        }

        self.pending_impulse = dict(impulse)
        self.last_impulse = dict(impulse)
        return dict(impulse)

    def tick(self):
        if self.bot is None:
            return None
        if self._compute_runtime_result is None or self._apply_runtime_result is None:
            return None

        impulse = dict(self.pending_impulse or self.last_impulse or {})
        window = [dict(item or {}) for item in list(impulse.get("window", []) or []) if isinstance(item, dict)]
        candle_state = dict(impulse.get("candle_state", {}) or {})
        tension_state = dict(impulse.get("tension_state", {}) or {})
        visual_market_state = dict(impulse.get("visual_market_state", {}) or {})
        structure_perception_state = dict(impulse.get("structure_perception_state", {}) or {})
        temporal_perception_state = dict(impulse.get("temporal_perception_state", {}) or {})

        if not window:
            return None

        if self._decay_active_context_trace is not None:
            self.active_context_trace = self._decay_active_context_trace(
                self.active_context_trace,
                market_tick_advanced=self._market_tick_pending,
            )
        setattr(self.bot, "active_context_trace", dict(self.active_context_trace or {}))

        runtime_result, decision_tendency, timestamp = self._compute_runtime_result(
            window,
            candle_state,
            bot=self.bot,
            tension_state=tension_state,
            visual_market_state=visual_market_state,
            structure_perception_state=structure_perception_state,
            temporal_perception_state=temporal_perception_state,
        )

        if runtime_result is None:
            return None

        self.runtime_tick_seq = int(self.runtime_tick_seq or 0) + 1
        result = self._apply_runtime_result(
            self.bot,
            runtime_result,
            decision_tendency,
            timestamp,
            runtime_tick_seq=self.runtime_tick_seq,
            market_tick_advanced=self._market_tick_pending,
        )

        if self._record_neuro_transition_protocol is not None:
            self._record_neuro_transition_protocol(self.bot, result, current_window=window)

        self._market_tick_pending = False
        self.pending_impulse = None
        self.last_result = dict(result or {})
        self.brain_snapshot = dict(getattr(self.bot, "mcm_runtime_brain_snapshot", {}) or {})
        return dict(result or {})

    def advance(self, cycles=1):
        last_result = None
        for _ in range(max(1, int(cycles or 1))):
            last_result = self.tick()
            if last_result is None:
                break
        return last_result

    def advance_idle(self, cycles=1):
        if not self.has_impulse():
            return None

        return self.advance(cycles=cycles)

    def read_snapshot(self):
        return {
            "timestamp": self.timestamp,
            "runtime_tick_seq": int(self.runtime_tick_seq or 0),
            "market_tick_pending": bool(self._market_tick_pending),
            "last_impulse_timestamp": dict(self.last_impulse or {}).get("timestamp", None),
            "brain_snapshot": dict(self.brain_snapshot or {}),
            "last_result": dict(self.last_result or {}),
        }
