# ==================================================
# bot.py
# Pipeline:
# OHLC
# -> Exit / Pending Handling
# -> Dummy Entry Slot
# -> TradeValueGate
# -> Order / Pending Entry
# ==================================================
import time

from MCM_Brain_Modell import (
    apply_outcome_stimulus,
    build_runtime_pipeline_snapshot,
    build_visualization_snapshot_bundle,
    capture_runtime_regulation_transition,
    commit_runtime_regulation_snapshot,
    create_mcm_brain,
    create_mcm_runtime,
    mark_runtime_episode_event,
    prepare_visualization_snapshot_state,
    step_mcm_runtime,
    step_mcm_runtime_idle,
    write_visualization_snapshot_bundle,
)
from config import Config
from bot_engine.active_position import handle_active_position
from bot_engine.action_context import (
    apply_runtime_action_state,
    build_runtime_action_context,
    build_runtime_action_context_flags,
    build_runtime_action_payload_state,
    build_runtime_execution_payload,
    normalize_runtime_action_context,
    prepare_runtime_action_context,
    resolve_runtime_action_context_state,
    resolve_runtime_action_window_state,
    run_runtime_action_cycle,
)
from bot_engine.entry_attempt import handle_entry_attempt
from bot_engine.entry_attempt_context import build_entry_attempt_context
from bot_engine.exit_candidate_observe import build_exit_candidate_observe_state
from bot_engine.execution_outcomes import (
    finalize_active_position_cancel,
    finalize_active_position_resolution,
    finalize_entry_attempt_abandoned,
    finalize_entry_attempt_submission,
    finalize_pending_fill_handoff,
    handle_decision_tendency,
)
from bot_engine.execution_paths import (
    run_decision_execution_path,
    run_entry_execution_path,
    run_existing_trade_execution_paths,
    run_pending_execution_path,
    run_position_execution_path,
    run_runtime_execution_paths,
)
from bot_engine.exit_engine import ExitEngine
from bot_engine.feed_runtime import (
    consume_feed_windows,
    iter_row_windows,
    process_market_packet_and_followup,
    process_market_window_and_followup,
    publish_market_window,
    run_rows_buffer_loop,
    run_runtime_loop,
    run_window_feed_loop,
)
from bot_engine.idle_thinking_protocol import (
    clip01,
    resolve_idle_phase_from_state,
    write_idle_thinking_protocol,
)
from bot_engine.live_recovery import recover_live_state_on_boot
from bot_engine.market_packets import (
    build_live_market_packet_key,
    build_outer_market_state_packet,
    build_runtime_market_packet,
    is_duplicate_live_market_packet,
    normalize_market_window,
)
from bot_engine.world_motion_afterimage import build_world_motion_afterimage, build_world_motion_observation
from bot_engine.market_perception import (
    apply_market_perception_state,
    build_candle_state_packet,
    build_market_component_bundle,
    build_market_perception_packet,
    build_structure_perception_packet,
    build_temporal_perception_state,
    build_tension_state_packet,
    build_visual_market_state_packet,
    resolve_market_packet_payload,
)
from bot_engine.matured_exit import resolve_matured_exit_signal
from bot_engine.mcm_core_engine import build_tension_state_from_window
from core.visual_perception import build_visual_market_state
from bot_engine.pending_entry import handle_pending_entry
from bot_engine.position_intervention import build_position_intervention_state
from bot_engine.regulation_snapshot import build_regulation_state_delta, build_regulation_state_snapshot
from bot_engine.restart_recovery import apply_restart_recovery_snapshot
from bot_engine.runtime_followup import (
    flush_runtime_followup,
    run_runtime_idle_followup,
    run_runtime_market_followup,
    step_runtime_idle,
)
from bot_engine.runtime_processing import (
    advance_runtime_from_resolved_packet,
    build_prepared_runtime_action_context,
    compose_runtime_perception_packet,
    finalize_market_packet_processing,
    process_market_packet,
    process_runtime_packet,
    run_runtime_packet_action_cycle,
    seed_runtime_window,
)
from bot_engine.runtime_thread import (
    get_queue_empty_exception,
    initialize_runtime_thread_state,
    start_runtime_thread,
    stop_runtime_thread,
    wait_until_runtime_idle,
)
from bot_engine.runtime_timing import (
    runtime_dynamic_load,
    runtime_idle_cycles,
    runtime_idle_sleep_seconds,
    runtime_market_followup_cycles,
)
from bot_engine.state_initialization import initialize_bot_state
from bot_engine.strukture_engine import StructureEngine
from bot_engine.target_expectation import build_target_expectation_state
from bot_engine.visual_cortex_protocol import record_visual_cortex_protocol
from bot_engine.visualization_snapshots import (
    build_bot_visualization_snapshot_bundle,
    build_inner_pipeline_snapshot,
    flush_visualization_snapshots,
    resolve_visualization_snapshot_write_due,
    write_visualization_snapshots,
)
from debug_tools.writers import dbr_append_text, dbr_debug, dbr_path
from bot_gates.entry_decision import evaluate_entry_decision
from bot_gates.trade_value_gate import TradeValueGate
from memory.form_symbol_memory import _flush_form_symbol_memory_if_due
from memory.memory_state import (
    ensure_memory_state_loaded,
    flush_memory_state_if_due,
    initialize_memory_state_bootstrap,
    mark_memory_state_dirty,
    read_memory_state,
    save_bot_memory_state,
)
from memory.thought_memory_store import _flush_thought_memory_if_due
from trading.csv_feed import CSVFeed
from trading.exchange_data import _build_candle_state
from trading.order_logic import (
    cancel_order_by_id,
    consume_cancelled_cause,
    get_active_order_snapshot,
    is_order_active,
    place_order,
)
from trading.trade_stats import TradeStats


DEBUG = True
STRUCTURE_ENGINE = StructureEngine()
consume_cancelled = lambda order_id: consume_cancelled_cause(order_id) is not None
# --------------------------------------------------


class Bot:
    # ==================================================
    # INITIALISIERUNG / BOT-LIFECYCLE
    # ==================================================
    def __init__(self, filepath: str):

        self._initialize_bot_state(filepath)
        initialize_memory_state_bootstrap(self)
        self.mcm_runtime = create_mcm_runtime(self)
        self._initialize_runtime_thread_state()
        self._recover_live_state_on_boot()
    # --------------------------------------------------    
    def _recover_live_state_on_boot(self):

        return recover_live_state_on_boot(
            self,
            config=Config,
            active_order_snapshot_getter=get_active_order_snapshot,
        )
    # --------------------------------------------------    
    def start_runtime_thread(self):

        return self._start_runtime_thread()
    # --------------------------------------------------
    def stop_runtime_thread(self, save_memory=True):

        return self._stop_runtime_thread(save_memory=save_memory)
    # --------------------------------------------------
    def wait_until_runtime_idle(self):

        return self._wait_until_runtime_idle()
    # --------------------------------------------------
    def _initialize_bot_state(self, filepath: str):

        return initialize_bot_state(
            self,
            filepath,
            csv_feed_cls=CSVFeed,
            exit_engine_cls=ExitEngine,
            trade_value_gate_cls=TradeValueGate,
            trade_stats_cls=TradeStats,
            brain_factory=create_mcm_brain,
            config=Config,
        )

    # ==================================================
    # RUNTIME THREAD / IDLE
    # ==================================================
    def _build_runtime_execution_payload(self, action_context, candle_state=None):

        return build_runtime_execution_payload(
            self,
            action_context,
            candle_state=candle_state,
        )
    # --------------------------------------------------
    def _sync_last_outcome_decomposition_from_stats(self):
        try:
            stats_data = getattr(self.stats, "data", {}) or {}
            payload = dict(
                stats_data.get("last_outcome_decomposition_enriched", {})
                or stats_data.get("last_outcome_decomposition", {})
                or {}
            )
            if payload:
                self.last_outcome_decomposition = payload
            entry_contact_learning = dict(stats_data.get("entry_contact_learning", {}) or {})
            if entry_contact_learning:
                self.entry_contact_preference_memory = entry_contact_learning
        except Exception:
            pass
    # --------------------------------------------------
    def _resolve_runtime_action_window_state(self, action_context):

        return resolve_runtime_action_window_state(action_context)
    # --------------------------------------------------
    def _start_runtime_thread(self):

        return start_runtime_thread(self)
    # --------------------------------------------------
    def _run_runtime_packet_action_cycle(self, resolved_packet, seed_runtime: bool = False):

        return run_runtime_packet_action_cycle(
            self,
            resolved_packet,
            seed_runtime=seed_runtime,
        )
    # --------------------------------------------------
    def _build_current_runtime_packet(self, window, candle_state, visual_market_state=None, structure_perception_state=None):

        local_window = [dict(item or {}) for item in list(window or []) if isinstance(item, dict)]
        if not local_window:
            return None

        return self._build_runtime_market_packet(
            {
                "timestamp": local_window[-1].get("timestamp", None),
                "window": [dict(item or {}) for item in list(local_window or []) if isinstance(item, dict)],
                "candle_state": dict(candle_state or {}),
                "tension_state": dict(getattr(self, "tension_state", {}) or {}),
                "visual_market_state": dict(visual_market_state or {}),
                "structure_perception_state": dict(structure_perception_state or {}),
                "temporal_perception_state": dict(getattr(self, "temporal_perception_state", {}) or {}),
                "world_motion_afterimage_state": dict(getattr(self, "world_motion_afterimage_state", {}) or {}),
                "outer_market_state": dict(getattr(self, "outer_market_state", {}) or {}),
            }
        )
    # --------------------------------------------------
    def _build_runtime_market_packet(
        self,
        packet,
        candle_state=None,
        visual_market_state=None,
        structure_perception_state=None,
        tension_state=None,
        temporal_perception_state=None,
    ):

        return build_runtime_market_packet(
            packet,
            candle_state=candle_state,
            visual_market_state=visual_market_state,
            structure_perception_state=structure_perception_state,
            tension_state=tension_state,
            temporal_perception_state=temporal_perception_state,
            outer_market_state_builder=self._build_outer_market_state_packet,
        )
    # --------------------------------------------------
    def _stop_runtime_thread(self, save_memory=True):

        return stop_runtime_thread(
            self,
            config=Config,
            debug_enabled=DEBUG,
            debug_writer=dbr_debug,
            save_memory=bool(save_memory),
        )
    # --------------------------------------------------
    def _wait_until_runtime_idle(self):

        return wait_until_runtime_idle(
            self,
            config=Config,
            debug_enabled=DEBUG,
            debug_writer=dbr_debug,
        )
    # --------------------------------------------------
    def _initialize_runtime_thread_state(self):

        return initialize_runtime_thread_state(self)
    # -------------------------------------------------
    def _runtime_loop(self):

        return run_runtime_loop(
            self,
            queue_empty_exception=get_queue_empty_exception(),
        )
    # --------------------------------------------------
    def _run_runtime_execution_paths(self, prepared_context, candle_state):

        return run_runtime_execution_paths(self, prepared_context, candle_state)        
    # --------------------------------------------------    
    def _runtime_dynamic_load(self):

        return runtime_dynamic_load(self)
    # --------------------------------------------------
    def _runtime_idle_sleep_seconds(self):

        return runtime_idle_sleep_seconds(
            self,
            config=Config,
            dynamic_load_func=self._runtime_dynamic_load,
        )
    # --------------------------------------------------
    def _runtime_idle_cycles(self):

        return runtime_idle_cycles(
            self,
            config=Config,
            dynamic_load_func=self._runtime_dynamic_load,
        )
    # --------------------------------------------------
    def _step_runtime_idle(self, cycles=None):

        return step_runtime_idle(
            self,
            cycles=cycles,
            idle_cycle_resolver=self._runtime_idle_cycles,
            idle_stepper=step_mcm_runtime_idle,
            memory_loader=self._ensure_memory_state_loaded,
        )
    # --------------------------------------------------
    def _flush_runtime_followup(self):

        return flush_runtime_followup(
            self,
            visualization_flusher=self._flush_visualization_snapshots,
            memory_flusher=self._flush_memory_state_if_due,
        )
    # --------------------------------------------------
    def _run_runtime_idle_followup(self):

        return run_runtime_idle_followup(
            self,
            idle_cycle_resolver=self._runtime_idle_cycles,
            idle_stepper=step_mcm_runtime_idle,
            memory_loader=self._ensure_memory_state_loaded,
            idle_protocol_writer=self._write_idle_thinking_protocol,
            followup_flusher=self._flush_runtime_followup,
        )
    # --------------------------------------------------
    @staticmethod
    def _clip01(value):

        return clip01(value)
    # --------------------------------------------------
    @staticmethod
    def _idle_phase_from_state(reflection_need, replay_need, hypothesis_need, pause_maturity, depth_efficiency, decision_tendency, pre_action_phase="hold", plan_pressure=0.0, act_watch_readiness=0.0):

        return resolve_idle_phase_from_state(
            reflection_need,
            replay_need,
            hypothesis_need,
            pause_maturity,
            depth_efficiency,
            decision_tendency,
            pre_action_phase=pre_action_phase,
            plan_pressure=plan_pressure,
            act_watch_readiness=act_watch_readiness,
        )
    # --------------------------------------------------
    def _write_idle_thinking_protocol(self, runtime_result):

        return write_idle_thinking_protocol(
            self,
            runtime_result,
            config=Config,
            debug_enabled=DEBUG,
            dbr_path_func=dbr_path,
            dbr_append_text_func=dbr_append_text,
            dbr_debug_func=dbr_debug,
        )
    # --------------------------------------------------
    def _run_runtime_market_followup(self):

        return run_runtime_market_followup(
            self,
            market_cycle_resolver=self._runtime_market_followup_cycles,
            idle_step_func=self._step_runtime_idle,
            followup_flusher=self._flush_runtime_followup,
        )
    # -------------------------------------------------- 
    def _build_runtime_action_context_flags(self):

        return build_runtime_action_context_flags(
            self,
            config=Config,
            is_order_active_func=is_order_active,
            debug_enabled=DEBUG,
            dbr_debug_func=dbr_debug,
        )
    # --------------------------------------------------
    def _resolve_runtime_action_context_state(self, action_context):

        return resolve_runtime_action_context_state(
            action_context,
            window_state_resolver=self._resolve_runtime_action_window_state,
        )   
    # ==================================================
    # WINDOW EINGANG / FEED
    # ==================================================  
    def _build_market_packet_from_window(self, window):

        packet = self._build_market_perception_packet(window)
        if packet is None:
            return None

        return dict(packet or {}) 
    # --------------------------------------------------    
    def _consume_feed_windows(self, windows):

        return consume_feed_windows(self, windows)
    # --------------------------------------------------
    def _iter_row_windows(self, window_size: int = 2, delay_seconds: float = 0.0):

        yield from iter_row_windows(
            self,
            window_size=window_size,
            delay_seconds=delay_seconds,
        )
    # --------------------------------------------------
    def _process_market_packet_and_followup(self, packet):

        return process_market_packet_and_followup(self, packet)
    # --------------------------------------------------  
    def publish_market_window(self, window):

        return publish_market_window(self, window)
    # --------------------------------------------------
    def _process_market_window_and_followup(self, window):

        return process_market_window_and_followup(self, window)
    # --------------------------------------------------
    def _process_window(self, window):

        return self._process_market_window_and_followup(window)
    # --------------------------------------------------   
    def _run_rows_buffer_loop(self, window_size: int = 2, delay_seconds: float = 0.0):

        return run_rows_buffer_loop(
            self,
            window_size=window_size,
            delay_seconds=delay_seconds,
        )
    # --------------------------------------------------
    def _run_window_feed_loop(self, size: int, delay_seconds: float = 0.0):

        return run_window_feed_loop(
            self,
            size=size,
            delay_seconds=delay_seconds,
        )
    # --------------------------------------------------
    def run_rows(self, window_size: int = 2, delay_seconds: float = 0.0):

        return self._run_rows_buffer_loop(
            window_size=window_size,
            delay_seconds=delay_seconds,
        )
    # -------------------------------------------------- 
    def run_window(self, size: int, delay_seconds: float = 0.0):

        return self._run_window_feed_loop(
            size=size,
            delay_seconds=delay_seconds,
        )
    # --------------------------------------------------     
    def _run_existing_trade_execution_paths(self, prepared_context):

        return run_existing_trade_execution_paths(self, prepared_context)  
    # --------------------------------------------------       
    def _run_entry_execution_path(self, prepared_context, candle_state):

        return run_entry_execution_path(self, prepared_context, candle_state)    
    # ==================================================
    # MARKET WINDOW NORMALISIERUNG / AUSSENWAHRNEHMUNG
    # ==================================================
    def _build_outer_market_state_packet(
        self,
        timestamp,
        candle_state=None,
        tension_state=None,
        visual_market_state=None,
        structure_perception_state=None,
        temporal_perception_state=None,
        world_motion_afterimage_state=None,
        base_state=None,
    ):

        return build_outer_market_state_packet(
            timestamp,
            candle_state=candle_state,
            tension_state=tension_state,
            visual_market_state=visual_market_state,
            structure_perception_state=structure_perception_state,
            temporal_perception_state=temporal_perception_state,
            world_motion_afterimage_state=world_motion_afterimage_state,
            base_state=base_state,
        )
    # --------------------------------------------------
    def _build_market_component_bundle(self, window, base_packet=None):

        return build_market_component_bundle(self, window, base_packet=base_packet)      
    # --------------------------------------------------        
    def _publish_market_packet(self, packet):

        payload = dict(packet or {})
        if not payload:
            return None

        if self._is_duplicate_live_market_packet(payload):
            return None

        self.world_published_ticks = int(getattr(self, "world_published_ticks", 0) or 0) + 1
        max_queue_size = max(0, int(getattr(Config, "RUNTIME_MAX_QUEUE_SIZE", 0) or 0))
        dropped = 0
        if max_queue_size > 0:
            while int(self._market_packet_queue.qsize() or 0) >= max_queue_size:
                try:
                    dropped_packet = self._market_packet_queue.get_nowait()
                    self._market_packet_queue.task_done()
                    self.world_motion_afterimage_state = build_world_motion_afterimage(
                        getattr(self, "world_motion_afterimage_state", {}) or {},
                        dropped_packet,
                        dropped_count=1,
                    )
                    dropped += 1
                except Exception:
                    break

        if dropped:
            self.world_missed_ticks = int(getattr(self, "world_missed_ticks", 0) or 0) + int(dropped)
            self.cognitive_lag_pressure = min(
                1.0,
                float(getattr(self, "cognitive_lag_pressure", 0.0) or 0.0) + (0.08 * float(dropped)),
            )
            self.last_cognitive_lag_state = {
                "dropped_world_ticks": int(dropped),
                "world_missed_ticks": int(getattr(self, "world_missed_ticks", 0) or 0),
                "queue_size": int(self._market_packet_queue.qsize() or 0),
                "cognitive_lag_pressure": float(getattr(self, "cognitive_lag_pressure", 0.0) or 0.0),
            }
        else:
            current_lag = float(getattr(self, "cognitive_lag_pressure", 0.0) or 0.0)
            if current_lag > 0.0:
                lag_decay = max(0.0, float(getattr(Config, "MCM_COGNITIVE_LAG_DECAY_PER_TICK", 0.035) or 0.0))
                self.cognitive_lag_pressure = max(0.0, current_lag - lag_decay)
                self.last_cognitive_lag_state = {
                    "dropped_world_ticks": 0,
                    "world_missed_ticks": int(getattr(self, "world_missed_ticks", 0) or 0),
                    "queue_size": int(self._market_packet_queue.qsize() or 0),
                    "cognitive_lag_pressure": float(getattr(self, "cognitive_lag_pressure", 0.0) or 0.0),
                }

        self.world_motion_afterimage_state = build_world_motion_observation(
            getattr(self, "world_motion_afterimage_state", {}) or {},
            payload,
        )
        payload["world_motion_afterimage_state"] = dict(getattr(self, "world_motion_afterimage_state", {}) or {})
        self._market_packet_queue.put(dict(payload))
        return dict(payload)
    # --------------------------------------------------
    def _is_duplicate_live_market_packet(self, packet):

        return is_duplicate_live_market_packet(
            self,
            packet,
            config=Config,
            key_builder=self._build_live_market_packet_key,
            debug_writer=dbr_debug,
        )
    # --------------------------------------------------
    def _build_live_market_packet_key(self, packet):

        return build_live_market_packet_key(packet)
    # --------------------------------------------------
    def _normalize_market_window(self, window):

        return normalize_market_window(window)
    # --------------------------------------------------
    def _build_market_perception_packet(self, window):

        return build_market_perception_packet(self, window)
    # --------------------------------------------------
    def _resolve_market_packet_payload(self, packet):

        return resolve_market_packet_payload(self, packet)    
    # --------------------------------------------------
    def _build_candle_state_packet(self, window):

        return build_candle_state_packet(
            self,
            window,
            candle_state_builder=_build_candle_state,
        )
    # --------------------------------------------------
    def _build_tension_state_packet(self, window):

        return build_tension_state_packet(
            self,
            window,
            tension_state_builder=build_tension_state_from_window,
        )
    # --------------------------------------------------
    def _build_structure_perception_packet(self, window):

        return build_structure_perception_packet(
            self,
            window,
            structure_engine=STRUCTURE_ENGINE,
        )
    # -------------------------------------------------- 
    def _build_visual_market_state_packet(self, window):

        return build_visual_market_state_packet(
            self,
            window,
            visual_market_state_builder=build_visual_market_state,
        )
    # --------------------------------------------------
    def _record_visual_cortex_protocol(self, window, visual_market_state):

        return record_visual_cortex_protocol(
            self,
            window,
            visual_market_state,
            config=Config,
            dbr_path_func=dbr_path,
            dbr_append_text_func=dbr_append_text,
            normalize_market_window_func=self._normalize_market_window,
        )
    # --------------------------------------------------     
    def _build_temporal_perception_state(self, window):

        return build_temporal_perception_state(self, window)    
    # --------------------------------------------------
    def _apply_market_perception_state(self, resolved_packet):

        return apply_market_perception_state(self, resolved_packet)
    # ==================================================
    # RUNTIME ADVANCE / INNENVERARBEITUNG
    # ==================================================
    def _compose_runtime_perception_packet(self, perception_packet, candle_state=None, visual_market_state=None, structure_perception_state=None):

        return compose_runtime_perception_packet(
            self,
            perception_packet,
            candle_state=candle_state,
            visual_market_state=visual_market_state,
            structure_perception_state=structure_perception_state,
        )
    # --------------------------------------------------
    def _advance_runtime_from_resolved_packet(self, resolved_packet):

        return advance_runtime_from_resolved_packet(
            self,
            resolved_packet,
            runtime_stepper=step_mcm_runtime,
        )    
    # --------------------------------------------------
    def _seed_runtime_window(self, resolved_packet):

        return seed_runtime_window(self, resolved_packet)
    # --------------------------------------------------
    def _build_prepared_runtime_action_context(self, window):

        return build_prepared_runtime_action_context(self, window)    
    # --------------------------------------------------
    def _process_market_packet(self, packet):

        return process_market_packet(self, packet)
    # --------------------------------------------------
    def _process_runtime_packet(self, window, candle_state, visual_market_state=None, structure_perception_state=None):

        return process_runtime_packet(
            self,
            window,
            candle_state,
            visual_market_state=visual_market_state,
            structure_perception_state=structure_perception_state,
        )
    # --------------------------------------------------
    def _runtime_market_followup_cycles(self):

        return runtime_market_followup_cycles(
            self,
            config=Config,
            dynamic_load_func=self._runtime_dynamic_load,
        )
    # --------------------------------------------------
    def _finalize_market_packet_processing(self, resolved_packet):

        return finalize_market_packet_processing(self, resolved_packet)   
    # ==================================================
    # ACTION CONTEXT / RUNTIME HANDLUNGSVORBEREITUNG
    # ==================================================
    def _build_runtime_action_payload_state(self, action_context, candle_state=None, allow_empty: bool = False):

        return build_runtime_action_payload_state(
            action_context,
            candle_state=candle_state,
            allow_empty=allow_empty,
            context_state_resolver=self._resolve_runtime_action_context_state,
        )   
    # --------------------------------------------------  
    def _build_runtime_action_context(self, window):

        return build_runtime_action_context(
            window,
            flags_builder=self._build_runtime_action_context_flags,
        )
    # --------------------------------------------------
    def _normalize_runtime_action_context(self, action_context):

        return normalize_runtime_action_context(
            action_context,
            payload_state_builder=self._build_runtime_action_payload_state,
        )    
    # --------------------------------------------------
    def _apply_runtime_action_state(self, action_context):

        return apply_runtime_action_state(
            self,
            action_context,
            window_state_resolver=self._resolve_runtime_action_window_state,
        )
    # --------------------------------------------------
    def _prepare_runtime_action_context(self, action_context):

        return prepare_runtime_action_context(self, action_context) 
    # --------------------------------------------------
    def _run_runtime_action_cycle(self, window, candle_state):

        return run_runtime_action_cycle(self, window, candle_state)   
    # --------------------------------------------------
    def _run_position_execution_path(self, action_context):

        return run_position_execution_path(self, action_context)
    # --------------------------------------------------
    def _run_pending_execution_path(self, action_context):

        return run_pending_execution_path(self, action_context)
    # --------------------------------------------------
    def _run_decision_execution_path(self, action_context, candle_state):

        return run_decision_execution_path(self, action_context, candle_state)
    # ==================================================
    # ENTSCHEIDUNGSBAHN / HANDLUNGSBAHN
    # ==================================================
    def _finalize_pending_fill_handoff(self, side, entry_price, tp_price, sl_price, entry_ts, order_id, position_meta, reason: str):

        return finalize_pending_fill_handoff(
            self,
            side,
            entry_price,
            tp_price,
            sl_price,
            entry_ts,
            order_id,
            position_meta,
            reason,
            episode_marker=mark_runtime_episode_event,
        )
    # --------------------------------------------------   
    def _handle_decision_tendency(self, entry_result: dict):

        return handle_decision_tendency(
            self,
            entry_result,
            episode_marker=mark_runtime_episode_event,
        )               
    # --------------------------------------------------   
    def _finalize_active_position_cancel(self, resolved_position, exit_context, order_id, cancel_cause):

        return finalize_active_position_cancel(
            self,
            resolved_position,
            exit_context,
            order_id,
            cancel_cause,
            outcome_stimulus=apply_outcome_stimulus,
            episode_marker=mark_runtime_episode_event,
        )
    # --------------------------------------------------   
    def _finalize_active_position_resolution(self, resolved_position, exit_context, reason, live_mode: bool):

        return finalize_active_position_resolution(
            self,
            resolved_position,
            exit_context,
            reason,
            live_mode,
            config=Config,
            outcome_stimulus=apply_outcome_stimulus,
            episode_marker=mark_runtime_episode_event,
        )    
    # --------------------------------------------------   
    def _build_position_intervention_state(
        self,
        *,
        close_price: float,
        entry_price: float,
        side: str,
        risk_value: float,
        mfe_r: float,
        mae_r: float,
        fill_ratio: float,
        pressure_to_capacity: float,
        bars_open: int,
    ) -> dict:

        return build_position_intervention_state(
            self,
            close_price=close_price,
            entry_price=entry_price,
            side=side,
            risk_value=risk_value,
            mfe_r=mfe_r,
            mae_r=mae_r,
            fill_ratio=fill_ratio,
            pressure_to_capacity=pressure_to_capacity,
            bars_open=bars_open,
            config=Config,
            debug_writer=dbr_debug,
        )
    # --------------------------------------------------   
    def _build_target_expectation_state(
        self,
        *,
        position_intervention_state: dict,
        side: str,
        entry_price: float,
        close_price: float,
        tp_price: float,
        risk_value: float,
        bars_open: int,
    ) -> dict:

        return build_target_expectation_state(
            self,
            position_intervention_state=position_intervention_state,
            side=side,
            entry_price=entry_price,
            close_price=close_price,
            tp_price=tp_price,
            risk_value=risk_value,
            bars_open=bars_open,
            config=Config,
            debug_writer=dbr_debug,
        )
    # --------------------------------------------------   
    def _build_exit_candidate_observe_state(self, position_intervention_state: dict, side: str, entry_price: float, close_price: float, target_expectation_state: dict = None) -> dict:

        return build_exit_candidate_observe_state(
            self,
            position_intervention_state,
            side,
            entry_price,
            close_price,
            target_expectation_state,
            config=Config,
            debug_writer=dbr_debug,
            episode_marker=mark_runtime_episode_event,
        )
    # --------------------------------------------------   
    def _resolve_matured_exit_signal(self, last: dict, exit_context: dict, fill_ratio: float, pressure_to_capacity: float, risk_value: float, bars_open: int, live_mode: bool = False):

        return resolve_matured_exit_signal(
            self,
            last,
            exit_context,
            fill_ratio,
            pressure_to_capacity,
            risk_value,
            bars_open,
            live_mode,
            config=Config,
            debug_enabled=DEBUG,
            debug_writer=dbr_debug,
            episode_marker=mark_runtime_episode_event,
        )

    # --------------------------------------------------   
    def _handle_active_position(self, window, last, live_mode: bool):

        return handle_active_position(
            self,
            window,
            last,
            live_mode,
            config=Config,
            debug_writer=dbr_debug,
            episode_marker=mark_runtime_episode_event,
            cancelled_cause_consumer=consume_cancelled_cause,
            cancelled_checker=consume_cancelled,
            active_order_snapshot_getter=get_active_order_snapshot,
        )
    # --------------------------------------------------
    def _handle_pending_entry(self, window, last, live_mode: bool):

        return handle_pending_entry(
            self,
            window,
            last,
            live_mode,
            outcome_stimulus=apply_outcome_stimulus,
            episode_marker=mark_runtime_episode_event,
            cancelled_cause_consumer=consume_cancelled_cause,
            order_cancel_func=cancel_order_by_id,
            active_order_snapshot_getter=get_active_order_snapshot,
        )
    # --------------------------------------------------
    def _finalize_entry_attempt_abandoned(self, entry_result: dict, reason: str, state_before, state_after, state_delta):

        return finalize_entry_attempt_abandoned(
            self,
            entry_result,
            reason,
            state_before,
            state_after,
            state_delta,
            episode_marker=mark_runtime_episode_event,
        )    
    # --------------------------------------------------
    def _finalize_entry_attempt_submission(self, entry_result: dict, side, entry_price, tp_price, sl_price, risk, order_id, state_before, state_after, state_delta):

        return finalize_entry_attempt_submission(
            self,
            entry_result,
            side,
            entry_price,
            tp_price,
            sl_price,
            risk,
            order_id,
            state_before,
            state_after,
            state_delta,
            config=Config,
            episode_marker=mark_runtime_episode_event,
        )    
    # --------------------------------------------------
    def _handle_entry_attempt(self, window, candle_state, last, live_mode: bool, external_order_active: bool):

        return handle_entry_attempt(
            self,
            window,
            candle_state,
            last,
            live_mode,
            external_order_active,
            config=Config,
            debug_enabled=DEBUG,
            debug_writer=dbr_debug,
            entry_decision_evaluator=evaluate_entry_decision,
            order_placer=place_order,
            outcome_stimulus=apply_outcome_stimulus,
            episode_marker=mark_runtime_episode_event,
        )
    # --------------------------------------------------    
    def _build_entry_attempt_context(self, entry_result: dict, state_before: dict | None = None, state_after: dict | None = None, state_delta: dict | None = None) -> dict:

        return build_entry_attempt_context(
            self,
            entry_result,
            state_before=state_before,
            state_after=state_after,
            state_delta=state_delta,
        )
    # ==================================================
    # REGULATIONSZUSTAND / ZUSTANDSÜBERGANG
    # ==================================================   
    def _build_regulation_state_snapshot(self) -> dict:

        return build_regulation_state_snapshot(self)
    # --------------------------------------------------    
    def _build_regulation_state_delta(self, state_before: dict, state_after: dict) -> dict:

        return build_regulation_state_delta(state_before, state_after)
    # --------------------------------------------------
    def _capture_regulation_transition(self, state_before: dict | None = None, state_after: dict | None = None) -> tuple[dict, dict, dict]:

        return capture_runtime_regulation_transition(
            self,
            state_before=state_before,
            state_after=state_after,
        )
    # --------------------------------------------------    
    def _commit_regulation_state_snapshot(self, state_after: dict | None = None) -> dict:

        return commit_runtime_regulation_snapshot(
            self,
            state_after=state_after,
        )
    # ==================================================
    # SNAPSHOT / VISUALISIERUNG
    # ==================================================
    def _resolve_visualization_snapshot_write_due(self, window=None, candle_state=None):

        return resolve_visualization_snapshot_write_due(
            self,
            window=window,
            candle_state=candle_state,
            config=Config,
            time_module=time,
        )
    # --------------------------------------------------
    def _apply_restart_recovery_snapshot(bot, snapshot):

        return apply_restart_recovery_snapshot(
            bot,
            snapshot,
            config=Config,
            episode_marker=mark_runtime_episode_event,
            time_module=time,
        )
    # --------------------------------------------------  
    def _build_inner_pipeline_snapshot(self):

        return build_inner_pipeline_snapshot(
            self,
            pipeline_snapshot_builder=build_runtime_pipeline_snapshot,
        )
    # --------------------------------------------------  
    def _build_visualization_snapshot_bundle(self, window, candle_state):

        return build_bot_visualization_snapshot_bundle(
            self,
            window,
            candle_state,
            visualization_snapshot_builder=build_visualization_snapshot_bundle,
        )
    # --------------------------------------------------
    def _write_visualization_snapshots(self, window, candle_state):

        return write_visualization_snapshots(
            self,
            window,
            candle_state,
            write_due_resolver=resolve_visualization_snapshot_write_due,
            snapshot_state_preparer=prepare_visualization_snapshot_state,
            config=Config,
            time_module=time,
        )
    # --------------------------------------------------  
    def _flush_visualization_snapshots(self, force: bool = False):

        return flush_visualization_snapshots(
            self,
            force=force,
            snapshot_bundle_writer=write_visualization_snapshot_bundle,
        ) 
    # ==================================================
    # MEMORY STATE / PERSISTENZ
    # ==================================================   
    def _ensure_memory_state_loaded(self):

        return ensure_memory_state_loaded(
            self,
            payload=self._memory_state_payload,
        )
    # --------------------------------------------------
    def _mark_memory_state_dirty(self):

        return mark_memory_state_dirty(self)
    # --------------------------------------------------
    def _flush_memory_state_if_due(self, force: bool = False):

        return flush_memory_state_if_due(
            self,
            force=force,
        )
    # --------------------------------------------------
    def _save_memory_state(self, force: bool = False):

        return save_bot_memory_state(
            self,
            force=force,
            form_symbol_flusher=_flush_form_symbol_memory_if_due,
            thought_memory_flusher=_flush_thought_memory_if_due,
        )
