"""Runtime entry helpers for meta-state integration.

These helpers keep the large runtime entry orchestration readable while
preserving the existing DIO mechanics exactly.
"""

import os

from config import Config
from debug_tools.audio_debug import record_market_melody_audio
from debug_tools.writers import dbr_append_text, dbr_path
from core.possibility_field import apply_possibility_field_to_meta, build_mcm_possibility_field


ACTIVE_MCM_CONTACT_META_KEYS = (
    "contact_interest",
    "contact_focus_pull",
    "contact_resonance_probe",
    "outer_inner_resonance",
    "outer_inner_coherence",
    "inner_change_from_contact",
    "contact_carrying_quality",
    "contact_overcoupling_risk",
    "contact_release_readiness",
    "contact_deepen_pull",
    "contact_replay_pull",
    "contact_curiosity",
    "contact_felt_shift",
    "contact_selected_depth",
    "contact_salience",
    "overcoupled_touch_score",
    "release_contact_score",
    "deepening_contact_score",
    "resonant_contact_score",
    "reflective_contact_score",
    "curious_touch_score",
    "contact_action_maturity",
    "contact_bearing_gap",
    "contact_impulse_vs_bearing",
    "contact_learning_need",
    "contact_reality_check",
    "contact_regime_mismatch",
    "contact_stability_carryover",
    "contact_context_maturity",
    "contact_context_reframe_need",
    "contact_presentness",
    "contact_future_watch",
    "contact_memory_depth",
    "contact_unlocated_pressure",
    "contact_temporal_bearing",
    "contact_temporal_reframe_need",
    "contact_future_to_present_readiness",
    "area_spacetime_fit",
    "area_multisensory_coherence",
    "area_attention_need",
    "area_felt_depth",
    "area_perception_overcoupling_risk",
    "sensory_sync",
    "sensory_desync_pressure",
    "area_selective_contact_pull",
    "area_selective_feel_permission",
    "area_selective_feel_risk",
)


STRATEGIC_WINDOW_META_FLOAT_KEYS = (
    "strategic_pressure_interpretation",
    "strategic_patience",
    "lookback_bearing_capacity",
    "area_bearing_quality",
    "area_order_intention",
)


def _melody_float(*sources, key, default=0.0):
    for source in sources:
        if not isinstance(source, dict):
            continue
        try:
            value = source.get(key, None)
            if value is None:
                continue
            return float(value or 0.0)
        except Exception:
            continue
    return float(default or 0.0)


def _melody_text(value, default="-"):
    text = str(value if value is not None else default)
    return text.replace("\n", " ").replace("\r", " ").replace(";", "|")


def _resolve_market_hearing_state(*sources):
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


def write_market_melody_protocol(
    bot,
    *,
    candle_state,
    tension_state,
    visual_market_state,
    outer_visual_perception_state,
    perception_state,
    processing_state,
):
    try:
        if not bool(getattr(Config, "MCM_MARKET_MELODY_PROTOCOL_DEBUG", False)):
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

        loudness = _melody_float(hearing, trace_metrics, perception_state, visual_market_state, core_trace, key="loudness")
        frequency_hz = _melody_float(hearing, trace_metrics, perception_state, visual_market_state, core_trace, key="frequency_hz")
        compression = _melody_float(hearing, trace_metrics, perception_state, visual_market_state, core_trace, key="compression")
        tone = _melody_text(hearing.get("tone", trace_metrics.get("market_tone", "silent_tone")), "silent_tone")

        timestamp = getattr(bot, "current_timestamp", None)
        if timestamp is None:
            timestamp = (visual_market_state or {}).get("timestamp", "-")

        candle_key = (
            _melody_text(timestamp, "-"),
            round(_melody_float(candle_state, key="open"), 8),
            round(_melody_float(candle_state, key="high"), 8),
            round(_melody_float(candle_state, key="low"), 8),
            round(_melody_float(candle_state, key="close"), 8),
            round(loudness, 6),
            round(frequency_hz, 4),
        )
        if getattr(bot, "_last_market_melody_candle_key", None) == candle_key:
            return
        setattr(bot, "_last_market_melody_candle_key", candle_key)

        count = int(getattr(bot, "_market_melody_protocol_count", 0) or 0) + 1
        setattr(bot, "_market_melody_protocol_count", count)

        every_n = max(1, int(getattr(Config, "MCM_MARKET_MELODY_PROTOCOL_EVERY_N", 1) or 1))

        state_key = (
            tone,
            round(loudness, 4),
            round(frequency_hz, 2),
            round(compression, 4),
        )
        previous_key = getattr(bot, "_last_market_melody_protocol_state", None)
        changed = state_key != previous_key
        if (count % every_n) != 0 and not changed:
            return
        setattr(bot, "_last_market_melody_protocol_state", state_key)

        header_needed = not bool(getattr(bot, "_market_melody_protocol_header_written", False))
        protocol_path = dbr_path("mcm_market_melody_protocol.csv")
        if header_needed:
            try:
                if os.path.exists(protocol_path):
                    os.remove(protocol_path)
            except Exception:
                pass
            dbr_append_text(
                protocol_path,
                "timestamp;tick;open;high;low;close;coherence;asymmetry;energy;energy_raw_amplitude;energy_limited_amplitude;energy_limiter_gain;energy_overdrive;market_loudness;market_frequency_hz;market_hearing_compression;market_tone;visual_attention_label;visual_mcm_contact_weight;visual_form_contact;visual_inspection_pull\n",
                operation="market_melody_header",
            )
            setattr(bot, "_market_melody_protocol_header_written", True)

        line = ";".join(
            [
                _melody_text(timestamp, "-"),
                str(count),
                f"{_melody_float(candle_state, key='open'):.8f}",
                f"{_melody_float(candle_state, key='high'):.8f}",
                f"{_melody_float(candle_state, key='low'):.8f}",
                f"{_melody_float(candle_state, key='close'):.8f}",
                f"{_melody_float(core_trace, tension_state, key='coherence'):.6f}",
                f"{_melody_float(core_trace, tension_state, key='asymmetry'):.6f}",
                f"{_melody_float(core_trace, tension_state, key='energy'):.6f}",
                f"{_melody_float(core_trace, trace_metrics, key='energy_raw_amplitude'):.6f}",
                f"{_melody_float(core_trace, trace_metrics, key='energy_limited_amplitude'):.6f}",
                f"{_melody_float(core_trace, trace_metrics, key='energy_limiter_gain', default=1.0):.6f}",
                f"{_melody_float(core_trace, trace_metrics, key='energy_overdrive'):.6f}",
                f"{loudness:.6f}",
                f"{frequency_hz:.4f}",
                f"{compression:.6f}",
                tone,
                _melody_text((processing_state or {}).get("visual_attention_label", (perception_state or {}).get("visual_attention_label", "-")), "-"),
                f"{_melody_float(processing_state, perception_state, key='visual_mcm_contact_weight'):.6f}",
                f"{_melody_float(processing_state, perception_state, key='visual_form_contact'):.6f}",
                f"{_melody_float(processing_state, perception_state, key='visual_inspection_pull'):.6f}",
            ]
        )
        dbr_append_text(protocol_path, line + "\n", operation="market_melody_append")
    except Exception:
        return


def write_area_perception_protocol(
    bot,
    *,
    candle_state,
    perception_state,
):
    try:
        if not bool(getattr(Config, "MCM_AREA_PERCEPTION_PROTOCOL_DEBUG", False)):
            return

        profile = dict((perception_state or {}).get("area_perception_profile", {}) or {})
        if not profile:
            return

        count = int(getattr(bot, "_area_perception_protocol_count", 0) or 0) + 1
        setattr(bot, "_area_perception_protocol_count", int(count))
        every_n = max(1, int(getattr(Config, "MCM_AREA_PERCEPTION_PROTOCOL_EVERY_N", 1) or 1))

        profile_state = _melody_text(profile.get("area_profile_state", "background_area_perception"), "background_area_perception")
        visual_profile = dict(profile.get("area_visual_profile", {}) or {})
        hearing_profile = dict(profile.get("area_hearing_profile", {}) or {})
        temporal_profile = dict(profile.get("area_temporal_profile", {}) or {})
        mcm_profile = dict(profile.get("area_mcm_contact_profile", {}) or {})
        sync_state = dict(profile.get("sensory_sync_state", {}) or {})
        state_key = (
            profile_state,
            _melody_text(visual_profile.get("dominant_visual_object", "-"), "-"),
            _melody_text(visual_profile.get("visual_cortex_label", "-"), "-"),
            _melody_text(visual_profile.get("visual_object_side", "-"), "-"),
            _melody_text(hearing_profile.get("tone", "-"), "-"),
        )
        previous_key = getattr(bot, "_last_area_perception_protocol_state", None)
        changed = state_key != previous_key
        if (count % every_n) != 0 and not changed:
            return
        setattr(bot, "_last_area_perception_protocol_state", state_key)

        header_needed = not bool(getattr(bot, "_area_perception_protocol_header_written", False))
        protocol_path = dbr_path("mcm_area_perception_protocol.csv")
        if header_needed:
            try:
                if os.path.exists(protocol_path):
                    os.remove(protocol_path)
            except Exception:
                pass
            dbr_append_text(
                protocol_path,
                "timestamp;tick;open;high;low;close;area_profile_id;area_profile_state;area_price_low;area_price_high;area_price_mid;area_multisensory_coherence;area_attention_need;area_felt_depth;area_overcoupling_risk;sensory_sync;sensory_desync_pressure;visual_hearing_fit;visual_felt_fit;hearing_felt_fit;temporal_visual_fit;multisensory_binding_state;visual_object;visual_label;visual_side;visual_score;hearing_tone;hearing_loudness;hearing_frequency_hz;temporal_score;felt_depth;profile_role\n",
                operation="area_perception_header",
            )
            setattr(bot, "_area_perception_protocol_header_written", True)

        timestamp = getattr(bot, "current_timestamp", None)
        if timestamp is None:
            timestamp = "-"

        line = ";".join(
            [
                _melody_text(timestamp, "-"),
                str(count),
                f"{_melody_float(candle_state, key='open'):.8f}",
                f"{_melody_float(candle_state, key='high'):.8f}",
                f"{_melody_float(candle_state, key='low'):.8f}",
                f"{_melody_float(candle_state, key='close'):.8f}",
                _melody_text(profile.get("area_profile_id", "-"), "-"),
                profile_state,
                f"{_melody_float(profile, key='area_price_low'):.8f}",
                f"{_melody_float(profile, key='area_price_high'):.8f}",
                f"{_melody_float(profile, key='area_price_mid'):.8f}",
                f"{_melody_float(profile, key='area_multisensory_coherence'):.6f}",
                f"{_melody_float(profile, key='area_attention_need'):.6f}",
                f"{_melody_float(profile, key='area_felt_depth'):.6f}",
                f"{_melody_float(profile, key='area_overcoupling_risk'):.6f}",
                f"{_melody_float(sync_state, profile, key='sensory_sync'):.6f}",
                f"{_melody_float(sync_state, profile, key='sensory_desync_pressure'):.6f}",
                f"{_melody_float(sync_state, profile, key='visual_hearing_fit'):.6f}",
                f"{_melody_float(sync_state, profile, key='visual_felt_fit'):.6f}",
                f"{_melody_float(sync_state, profile, key='hearing_felt_fit'):.6f}",
                f"{_melody_float(sync_state, profile, key='temporal_visual_fit'):.6f}",
                _melody_text(sync_state.get("multisensory_binding_state", profile.get("multisensory_binding_state", "-")), "-"),
                _melody_text(visual_profile.get("dominant_visual_object", "-"), "-"),
                _melody_text(visual_profile.get("visual_cortex_label", "-"), "-"),
                _melody_text(visual_profile.get("visual_object_side", "-"), "-"),
                f"{_melody_float(visual_profile, key='visual_score'):.6f}",
                _melody_text(hearing_profile.get("tone", "-"), "-"),
                f"{_melody_float(hearing_profile, key='loudness'):.6f}",
                f"{_melody_float(hearing_profile, key='frequency_hz'):.4f}",
                f"{_melody_float(temporal_profile, key='temporal_score'):.6f}",
                f"{_melody_float(mcm_profile, key='felt_depth'):.6f}",
                _melody_text(profile.get("area_profile_role", "perception_only"), "perception_only"),
            ]
        )
        dbr_append_text(protocol_path, line + "\n", operation="area_perception_append")
    except Exception:
        return


def build_runtime_field_metrics(field_state):
    field = dict(field_state or {})
    return {
        "field_stimulus_density": float(field.get("field_stimulus_density", 0.0) or 0.0),
        "field_density": float(field.get("field_density", 0.0) or 0.0),
        "field_stability": float(field.get("field_stability", 0.0) or 0.0),
        "regulatory_load": float(field.get("regulatory_load", 0.0) or 0.0),
        "action_capacity": float(field.get("action_capacity", 0.0) or 0.0),
        "recovery_need": float(field.get("recovery_need", 0.0) or 0.0),
        "survival_pressure": float(field.get("survival_pressure", 0.0) or 0.0),
    }


def resolve_runtime_external_perception(window, visual_market_state, structure_perception_state, *, visual_builder, structure_engine):
    visual = dict(visual_market_state or {})
    structure = dict(structure_perception_state or {})

    if not visual:
        visual = dict(visual_builder(window) or {})

    if not structure:
        structure = dict(structure_engine.build_structure_perception_state(window) or {})

    return visual, structure


def build_runtime_entry_state_stack(
    *,
    bot,
    window,
    candle_state,
    tension_state,
    stimulus,
    snapshot,
    fused_preview,
    visual_market_state,
    structure_perception_state,
    temporal_perception_state,
    pause_mode,
    visual_builder,
    structure_engine,
    world_state_builder,
    outer_visual_builder,
    inner_field_builder,
    perception_builder,
    processing_builder,
    expectation_builder,
    felt_builder,
    form_symbol_builder,
    state_signature_builder,
    temporal_builder,
    active_context_refresher,
    pending_learning_register,
    signature_reinterpreter,
    thought_builder,
    meta_regulation_builder,
    review_feedback_resolver,
    strategic_window_builder,
    active_contact_builder,
):
    visual_market_state, structure_perception_state = resolve_runtime_external_perception(
        window,
        visual_market_state,
        structure_perception_state,
        visual_builder=visual_builder,
        structure_engine=structure_engine,
    )

    perception_stack = build_runtime_perception_stack(
        candle_state=candle_state,
        tension_state=tension_state,
        stimulus=stimulus,
        snapshot=snapshot,
        bot=bot,
        visual_market_state=visual_market_state,
        structure_perception_state=structure_perception_state,
        temporal_perception_state=temporal_perception_state,
        world_state_builder=world_state_builder,
        outer_visual_builder=outer_visual_builder,
        inner_field_builder=inner_field_builder,
        perception_builder=perception_builder,
        processing_builder=processing_builder,
    )
    world_state = perception_stack["world_state"]
    outer_visual_perception_state = perception_stack["outer_visual_perception_state"]
    inner_field_perception_state = perception_stack["inner_field_perception_state"]
    perception_state = perception_stack["perception_state"]
    processing_state = perception_stack["processing_state"]
    area_perception_profile = dict(perception_state.get("area_perception_profile", {}) or {})

    affective_symbol_stack = build_runtime_affective_symbol_stack(
        bot=bot,
        candle_state=candle_state,
        stimulus=stimulus,
        snapshot=snapshot,
        fused_preview=fused_preview,
        visual_market_state=visual_market_state,
        structure_perception_state=structure_perception_state,
        perception_state=perception_state,
        processing_state=processing_state,
        inner_field_perception_state=inner_field_perception_state,
        expectation_builder=expectation_builder,
        felt_builder=felt_builder,
        form_symbol_builder=form_symbol_builder,
    )
    expectation_state = affective_symbol_stack["expectation_state"]
    felt_state = affective_symbol_stack["felt_state"]
    form_symbol_state = affective_symbol_stack["form_symbol_state"]

    temporal_context_stack = build_runtime_temporal_context_stack(
        bot=bot,
        candle_state=candle_state,
        tension_state=tension_state,
        snapshot=snapshot,
        stimulus=stimulus,
        temporal_perception_state=temporal_perception_state,
        visual_market_state=visual_market_state,
        structure_perception_state=structure_perception_state,
        form_symbol_state=form_symbol_state,
        world_state=world_state,
        perception_state=perception_state,
        fused_preview=fused_preview,
        state_signature_builder=state_signature_builder,
        temporal_builder=temporal_builder,
        active_context_refresher=active_context_refresher,
        pending_learning_register=pending_learning_register,
        signature_reinterpreter=signature_reinterpreter,
    )
    state_signature = temporal_context_stack["state_signature"]
    temporal_perception_state = temporal_context_stack["temporal_perception_state"]
    early_active_context_trace = temporal_context_stack["active_context_trace"]
    world_state = temporal_context_stack["world_state"]
    perception_state = temporal_context_stack["perception_state"]
    fused = temporal_context_stack["fused"]

    cognitive_regulation_stack = build_runtime_cognitive_regulation_stack(
        bot=bot,
        candle_state=candle_state,
        tension_state=tension_state,
        fused=fused,
        perception_state=perception_state,
        felt_state=felt_state,
        snapshot=snapshot,
        processing_state=processing_state,
        pause_mode=pause_mode,
        thought_builder=thought_builder,
        meta_regulation_builder=meta_regulation_builder,
    )
    thought_state = cognitive_regulation_stack["thought_state"]
    meta_regulation_state = cognitive_regulation_stack["meta_regulation_state"]

    contact_regulation_stack = build_runtime_contact_regulation_stack(
        bot=bot,
        window=window,
        candle_state=candle_state,
        fused=fused,
        visual_market_state=visual_market_state,
        structure_perception_state=structure_perception_state,
        temporal_perception_state=temporal_perception_state,
        form_symbol_state=form_symbol_state,
        meta_regulation_state=meta_regulation_state,
        perception_state=perception_state,
        processing_state=processing_state,
        felt_state=felt_state,
        thought_state=thought_state,
        review_feedback_resolver=review_feedback_resolver,
        strategic_window_builder=strategic_window_builder,
        active_contact_builder=active_contact_builder,
    )
    review_feedback_state = contact_regulation_stack["review_feedback_state"]
    strategic_window_state = contact_regulation_stack["strategic_window_state"]
    active_mcm_contact_state = contact_regulation_stack["active_mcm_contact_state"]
    possibility_field_state = contact_regulation_stack["possibility_field_state"]
    meta_regulation_state = contact_regulation_stack["meta_regulation_state"]

    commit_runtime_entry_bot_state(
        bot,
        visual_market_state=visual_market_state,
        temporal_perception_state=temporal_perception_state,
        perception_state=perception_state,
        outer_visual_perception_state=outer_visual_perception_state,
        inner_field_perception_state=inner_field_perception_state,
        structure_perception_state=structure_perception_state,
        processing_state=processing_state,
        expectation_state=expectation_state,
        form_symbol_state=form_symbol_state,
        strategic_window_state=strategic_window_state,
        area_perception_profile=area_perception_profile,
        active_mcm_contact_state=active_mcm_contact_state,
        possibility_field_state=possibility_field_state,
        felt_state=felt_state,
        thought_state=thought_state,
        meta_regulation_state=meta_regulation_state,
    )

    return {
        "visual_market_state": dict(visual_market_state or {}),
        "structure_perception_state": dict(structure_perception_state or {}),
        "temporal_perception_state": dict(temporal_perception_state or {}),
        "world_state": dict(world_state or {}),
        "outer_visual_perception_state": dict(outer_visual_perception_state or {}),
        "inner_field_perception_state": dict(inner_field_perception_state or {}),
        "perception_state": dict(perception_state or {}),
        "processing_state": dict(processing_state or {}),
        "expectation_state": dict(expectation_state or {}),
        "felt_state": dict(felt_state or {}),
        "form_symbol_state": dict(form_symbol_state or {}),
        "state_signature": dict(state_signature or {}),
        "early_active_context_trace": dict(early_active_context_trace or {}),
        "fused": dict(fused or {}),
        "thought_state": dict(thought_state or {}),
        "meta_regulation_state": dict(meta_regulation_state or {}),
        "review_feedback_state": dict(review_feedback_state or {}),
        "strategic_window_state": dict(strategic_window_state or {}),
        "area_perception_profile": dict(area_perception_profile or {}),
        "active_mcm_contact_state": dict(active_mcm_contact_state or {}),
        "possibility_field_state": dict(possibility_field_state or {}),
    }


def build_runtime_perception_stack(
    *,
    candle_state,
    tension_state,
    stimulus,
    snapshot,
    bot,
    visual_market_state,
    structure_perception_state,
    temporal_perception_state,
    world_state_builder,
    outer_visual_builder,
    inner_field_builder,
    perception_builder,
    processing_builder,
):
    world_state = world_state_builder(
        candle_state,
        tension_state,
        stimulus,
        visual_market_state=visual_market_state,
        structure_perception_state=structure_perception_state,
        temporal_perception_state=temporal_perception_state,
    )
    outer_visual_perception_state = outer_visual_builder(world_state)
    inner_field_perception_state = inner_field_builder(snapshot, bot=bot)
    perception_state = perception_builder(world_state, bot=bot)
    processing_state = processing_builder(
        outer_visual_perception_state,
        inner_field_perception_state,
        perception_state,
    )
    write_market_melody_protocol(
        bot,
        candle_state=candle_state,
        tension_state=tension_state,
        visual_market_state=visual_market_state,
        outer_visual_perception_state=outer_visual_perception_state,
        perception_state=perception_state,
        processing_state=processing_state,
    )
    write_area_perception_protocol(
        bot,
        candle_state=candle_state,
        perception_state=perception_state,
    )
    record_market_melody_audio(
        bot,
        candle_state=candle_state,
        tension_state=tension_state,
        visual_market_state=visual_market_state,
        outer_visual_perception_state=outer_visual_perception_state,
        perception_state=perception_state,
        processing_state=processing_state,
    )

    return {
        "world_state": dict(world_state or {}),
        "outer_visual_perception_state": dict(outer_visual_perception_state or {}),
        "inner_field_perception_state": dict(inner_field_perception_state or {}),
        "perception_state": dict(perception_state or {}),
        "processing_state": dict(processing_state or {}),
    }


def build_runtime_affective_symbol_stack(
    *,
    bot,
    candle_state,
    stimulus,
    snapshot,
    fused_preview,
    visual_market_state,
    structure_perception_state,
    perception_state,
    processing_state,
    inner_field_perception_state,
    expectation_builder,
    felt_builder,
    form_symbol_builder,
):
    preview_decision = str((fused_preview or {}).get("decision", "WAIT") or "WAIT")
    expectation_state = expectation_builder(
        bot,
        candle_state,
        stimulus,
        snapshot,
        decision=preview_decision,
        visual_market_state=visual_market_state,
    )
    felt_state = felt_builder(
        bot,
        candle_state,
        stimulus,
        snapshot,
        perception_state,
        decision=preview_decision,
        processing_state=processing_state,
        expectation_state=expectation_state,
        inner_field_perception_state=inner_field_perception_state,
    )
    form_symbol_state = form_symbol_builder(
        bot,
        visual_market_state=visual_market_state,
        structure_perception_state=structure_perception_state,
        perception_state=perception_state,
        felt_state=felt_state,
        snapshot=snapshot,
    )

    return {
        "expectation_state": dict(expectation_state or {}),
        "felt_state": dict(felt_state or {}),
        "form_symbol_state": dict(form_symbol_state or {}),
    }


def build_runtime_temporal_context_stack(
    *,
    bot,
    candle_state,
    tension_state,
    snapshot,
    stimulus,
    temporal_perception_state,
    visual_market_state,
    structure_perception_state,
    form_symbol_state,
    world_state,
    perception_state,
    fused_preview,
    state_signature_builder,
    temporal_builder,
    active_context_refresher,
    pending_learning_register,
    signature_reinterpreter,
):
    state_signature = state_signature_builder(candle_state, tension_state, snapshot, stimulus, bot=bot)
    updated_temporal_perception_state = temporal_builder(
        temporal_perception_state=temporal_perception_state,
        bot=bot,
        visual_market_state=visual_market_state,
        structure_perception_state=structure_perception_state,
        form_symbol_state=form_symbol_state,
        state_signature=state_signature,
        candle_state=candle_state,
    )

    updated_world_state = dict(world_state or {})
    updated_perception_state = dict(perception_state or {})
    updated_world_state["temporal_perception_state"] = dict(updated_temporal_perception_state or {})
    updated_perception_state["temporal_perception_state"] = dict(updated_temporal_perception_state or {})
    bot.temporal_perception_state = dict(updated_temporal_perception_state or {})

    active_context_trace = active_context_refresher(
        getattr(bot, "active_context_trace", {}) or {},
        bot=bot,
        runtime_result={
            "temporal_perception_state": dict(updated_temporal_perception_state or {}),
        },
        market_tick_advanced=True,
    )
    bot.active_context_trace = dict(active_context_trace or {})
    updated_world_state["active_context_trace"] = dict(active_context_trace or {})
    updated_perception_state["active_context_trace"] = dict(active_context_trace or {})

    pending_learning_register(bot, state_signature)

    fused = dict(fused_preview or {})
    fused = signature_reinterpreter(bot, fused, state_signature)
    fused["form_symbol_state"] = dict(form_symbol_state or {})
    fused["active_context_trace"] = dict(active_context_trace or {})

    return {
        "state_signature": dict(state_signature or {}),
        "temporal_perception_state": dict(updated_temporal_perception_state or {}),
        "active_context_trace": dict(active_context_trace or {}),
        "world_state": updated_world_state,
        "perception_state": updated_perception_state,
        "fused": dict(fused or {}),
    }


def build_runtime_cognitive_regulation_stack(
    *,
    bot,
    candle_state,
    tension_state,
    fused,
    perception_state,
    felt_state,
    snapshot,
    processing_state,
    pause_mode,
    thought_builder,
    meta_regulation_builder,
):
    thought_state = thought_builder(
        candle_state,
        tension_state,
        fused,
        perception_state,
        felt_state,
        snapshot,
        processing_state=processing_state,
        bot=bot,
    )
    meta_regulation_state = meta_regulation_builder(
        perception_state,
        processing_state,
        felt_state,
        thought_state,
        fused,
        pause_mode=pause_mode,
        bot=bot,
    )

    return {
        "thought_state": dict(thought_state or {}),
        "meta_regulation_state": dict(meta_regulation_state or {}),
    }


def apply_review_feedback_to_meta(meta_regulation_state, review_feedback_state):
    meta = dict(meta_regulation_state or {})
    review = dict(review_feedback_state or {})

    pattern_action_support = float(review.get("pattern_action_support", 0.0) or 0.0)
    pattern_observe_pressure = float(review.get("pattern_observe_pressure", 0.0) or 0.0)
    pattern_replan_pressure = float(review.get("pattern_replan_pressure", 0.0) or 0.0)

    non_economic_plan_modulation_reasons = list(meta.get("non_economic_plan_modulation_reasons", []) or [])
    if bool(meta.get("allow_plan", False)):
        if pattern_replan_pressure >= 0.58 and pattern_action_support < 0.48:
            non_economic_plan_modulation_reasons.append("inner_pattern_replan")
            meta["allow_ruminate"] = True
            meta["allow_observe"] = False
            meta["allow_block"] = False
            meta["pre_action_phase"] = "replan"
            meta["rejection_reason"] = "inner_pattern_replan"
        elif pattern_observe_pressure >= 0.54 and pattern_action_support < 0.44:
            non_economic_plan_modulation_reasons.append("inner_pattern_observe")
            meta["allow_ruminate"] = False
            meta["allow_observe"] = True
            meta["allow_block"] = False
            meta["pre_action_phase"] = "observe"
            meta["rejection_reason"] = "inner_pattern_observe"

    if non_economic_plan_modulation_reasons:
        meta["allow_plan"] = True
        meta["allow_block"] = False
        meta["non_economic_plan_modulated"] = True
        meta["non_economic_plan_modulation_reasons"] = non_economic_plan_modulation_reasons
        meta["non_economic_gate_policy"] = "field_modulation_only"

    meta["review_feedback_state"] = dict(review or {})
    meta["review_carry_capacity"] = float(review.get("carry_capacity", 0.0) or 0.0)
    meta["review_caution_load"] = float(review.get("caution_load", 0.0) or 0.0)
    meta["review_tendency_hint"] = str(review.get("tendency_hint", "hold") or "hold")
    meta["inner_pattern_support"] = float(review.get("inner_pattern_support", 0.0) or 0.0)
    meta["inner_pattern_conflict"] = float(review.get("inner_pattern_conflict", 0.0) or 0.0)
    meta["inner_pattern_fragility"] = float(review.get("inner_pattern_fragility", 0.0) or 0.0)
    meta["inner_pattern_bearing"] = float(review.get("inner_pattern_bearing", 0.0) or 0.0)
    meta["inner_pattern_state"] = str(review.get("inner_pattern_state", "bearing") or "bearing")
    meta["pattern_action_support"] = float(pattern_action_support)
    meta["pattern_observe_pressure"] = float(pattern_observe_pressure)
    meta["pattern_replan_pressure"] = float(pattern_replan_pressure)
    meta["observation_maturity_trust"] = float(review.get("observation_maturity_trust", 0.0) or 0.0)
    meta["observation_action_pressure"] = float(review.get("observation_action_pressure", 0.0) or 0.0)
    meta["observation_maturity_balance"] = float(review.get("observation_maturity_balance", 0.0) or 0.0)
    meta["observation_maturity_scope"] = float(review.get("observation_maturity_scope", 0.0) or 0.0)
    meta["observation_scoped_balance"] = float(review.get("observation_scoped_balance", 0.0) or 0.0)
    meta["observation_low_count"] = int(review.get("observation_low_count", 0) or 0)
    hypothesis_learning_enabled = bool(getattr(Config, "MCM_HYPOTHESIS_LEARNING_ENABLED", False))
    if not hypothesis_learning_enabled:
        meta["hypothesis_observed_outcome"] = "hypothesis_disabled"
        meta["hypothesis_confirmation_without_action"] = 0.0
        meta["hypothesis_rejection_without_action"] = 0.0
        meta["hypothesis_neutral_without_action"] = 0.0
        meta["hypothesis_observation_maturity"] = 0.0
        meta["possibility_maturity"] = 0.0
        meta["possibility_caution"] = 0.0
        meta["possibility_contact_bearing"] = 0.0
        meta["possibility_action_support"] = 0.0
        meta["possibility_reality_check_need"] = 0.0
        meta["hypothesis_observed_stability"] = 0.0
        meta["hypothesis_trust_score"] = 0.0
        meta["hypothesis_trust_score_raw"] = 0.0
        meta["hypothesis_trust_priority"] = 0.0
        meta["hypothesis_trust_priority_raw"] = 0.0
        meta["hypothesis_trust_matches_form"] = False
        meta["borrowed_hypothesis_trust_pressure"] = 0.0
        meta["hypothesis_frustration_risk"] = 0.0
        meta["hypothesis_distance_risk"] = 0.0
        meta["hypothesis_trust_state"] = "hypothesis_disabled"
        meta["dominant_hypothesis_trust_key"] = "-"
        meta["dominant_hypothesis_trust_score"] = 0.0
        meta["dominant_hypothesis_trust_score_raw"] = 0.0
        meta["dominant_hypothesis_trust_matches_form"] = False
        meta["dominant_hypothesis_reality_bearing"] = 0.0
        meta["dominant_hypothesis_action_readiness"] = 0.0
        meta["dominant_hypothesis_action_readiness_raw"] = 0.0
        meta["borrowed_dominant_hypothesis_pressure"] = 0.0
        meta["dominant_possibility_variant_key"] = "-"
        meta["dominant_possibility_variant_trust"] = 0.0
        meta["dominant_possibility_variant_caution"] = 0.0
        meta["dominant_possibility_variant_maturity"] = 0.0
        meta["dominant_possibility_variant_evidence"] = 0
        return meta

    meta["hypothesis_observed_outcome"] = str(review.get("hypothesis_observed_outcome", "hypothesis_observed_open") or "hypothesis_observed_open")
    meta["hypothesis_confirmation_without_action"] = float(review.get("hypothesis_confirmation_without_action", 0.0) or 0.0)
    meta["hypothesis_rejection_without_action"] = float(review.get("hypothesis_rejection_without_action", 0.0) or 0.0)
    meta["hypothesis_neutral_without_action"] = float(review.get("hypothesis_neutral_without_action", 0.0) or 0.0)
    meta["hypothesis_observation_maturity"] = float(review.get("hypothesis_observation_maturity", 0.0) or 0.0)
    meta["possibility_maturity"] = float(review.get("possibility_maturity", 0.0) or 0.0)
    meta["possibility_caution"] = float(review.get("possibility_caution", 0.0) or 0.0)
    meta["possibility_contact_bearing"] = float(review.get("possibility_contact_bearing", review.get("possibility_action_support", 0.0)) or 0.0)
    meta["possibility_action_support"] = float(meta["possibility_contact_bearing"])
    meta["possibility_reality_check_need"] = float(review.get("possibility_reality_check_need", 0.0) or 0.0)
    meta["hypothesis_observed_stability"] = float(review.get("hypothesis_observed_stability", 0.0) or 0.0)
    meta["hypothesis_trust_score"] = float(review.get("hypothesis_trust_score", 0.0) or 0.0)
    meta["hypothesis_trust_score_raw"] = float(review.get("hypothesis_trust_score_raw", meta["hypothesis_trust_score"]) or 0.0)
    meta["hypothesis_trust_priority"] = float(review.get("hypothesis_trust_priority", 0.0) or 0.0)
    meta["hypothesis_trust_priority_raw"] = float(review.get("hypothesis_trust_priority_raw", meta["hypothesis_trust_priority"]) or 0.0)
    meta["hypothesis_trust_matches_form"] = bool(review.get("hypothesis_trust_matches_form", False))
    meta["borrowed_hypothesis_trust_pressure"] = float(review.get("borrowed_hypothesis_trust_pressure", 0.0) or 0.0)
    meta["hypothesis_frustration_risk"] = float(review.get("hypothesis_frustration_risk", 0.0) or 0.0)
    meta["hypothesis_distance_risk"] = float(review.get("hypothesis_distance_risk", 0.0) or 0.0)
    meta["hypothesis_trust_state"] = str(review.get("hypothesis_trust_state", "hypothesis_trust_unformed") or "hypothesis_trust_unformed")
    meta["dominant_hypothesis_trust_key"] = str(review.get("dominant_hypothesis_trust_key", "-") or "-")
    meta["dominant_hypothesis_trust_score"] = float(review.get("dominant_hypothesis_trust_score", 0.0) or 0.0)
    meta["dominant_hypothesis_trust_score_raw"] = float(review.get("dominant_hypothesis_trust_score_raw", meta["dominant_hypothesis_trust_score"]) or 0.0)
    meta["dominant_hypothesis_trust_matches_form"] = bool(review.get("dominant_hypothesis_trust_matches_form", False))
    meta["dominant_hypothesis_reality_bearing"] = float(review.get("dominant_hypothesis_reality_bearing", review.get("dominant_hypothesis_action_readiness", 0.0)) or 0.0)
    meta["dominant_hypothesis_action_readiness"] = float(meta["dominant_hypothesis_reality_bearing"])
    meta["dominant_hypothesis_action_readiness_raw"] = float(review.get("dominant_hypothesis_action_readiness_raw", meta["dominant_hypothesis_action_readiness"]) or 0.0)
    meta["borrowed_dominant_hypothesis_pressure"] = float(review.get("borrowed_dominant_hypothesis_pressure", 0.0) or 0.0)
    meta["dominant_possibility_variant_key"] = str(review.get("dominant_possibility_variant_key", "-") or "-")
    meta["dominant_possibility_variant_trust"] = float(review.get("dominant_possibility_variant_trust", 0.0) or 0.0)
    meta["dominant_possibility_variant_caution"] = float(review.get("dominant_possibility_variant_caution", 0.0) or 0.0)
    meta["dominant_possibility_variant_maturity"] = float(review.get("dominant_possibility_variant_maturity", 0.0) or 0.0)
    meta["dominant_possibility_variant_evidence"] = int(review.get("dominant_possibility_variant_evidence", 0) or 0)
    return meta


def apply_strategic_window_to_meta(meta_regulation_state, strategic_window_state):
    meta = dict(meta_regulation_state or {})
    strategic = dict(strategic_window_state or {})

    meta["strategic_window_state"] = str(strategic.get("strategic_window_state", "no_area_focus") or "no_area_focus")
    for strategic_key in STRATEGIC_WINDOW_META_FLOAT_KEYS:
        meta[strategic_key] = float(strategic.get(strategic_key, 0.0) or 0.0)
    return meta


def apply_active_mcm_contact_to_meta(meta_regulation_state, active_mcm_contact_state, strategic_window_state=None):
    meta = dict(meta_regulation_state or {})
    contact = dict(active_mcm_contact_state or {})
    strategic = dict(strategic_window_state or {})

    meta["active_mcm_contact"] = dict(contact or {})
    meta["active_mcm_contact_state"] = str(contact.get("active_mcm_contact_state", "background_scan") or "background_scan")
    meta["contact_posture"] = str(contact.get("contact_posture", "background_scan") or "background_scan")
    for contact_key in ACTIVE_MCM_CONTACT_META_KEYS:
        meta[contact_key] = float(contact.get(contact_key, 0.0) or 0.0)
    meta["contact_temporal_mode"] = str(contact.get("contact_temporal_mode", "open_time_contact") or "open_time_contact")
    meta["area_profile_state"] = str(contact.get("area_profile_state", "background_area_perception") or "background_area_perception")
    meta["area_temporal_contact_mode"] = str(
        contact.get("area_temporal_contact_mode", strategic.get("area_temporal_contact_mode", "open_time_contact"))
        or "open_time_contact"
    )
    return meta


def build_runtime_contact_regulation_stack(
    *,
    bot,
    window,
    candle_state,
    fused,
    visual_market_state,
    structure_perception_state,
    temporal_perception_state,
    form_symbol_state,
    meta_regulation_state,
    perception_state,
    processing_state,
    felt_state,
    thought_state,
    review_feedback_resolver,
    strategic_window_builder,
    active_contact_builder,
):
    review_feedback_state = review_feedback_resolver(
        bot=bot,
        runtime_result={
            "context_cluster_id": str((fused or {}).get("context_cluster_id", "-") or "-"),
            "inner_context_cluster_id": str(getattr(bot, "last_inner_context_cluster_id", "-") or "-"),
            "form_symbol_id": str((form_symbol_state or {}).get("form_symbol_id", "-") or "-"),
            "form_symbol_state": dict(form_symbol_state or {}),
        },
    )
    updated_meta_regulation_state = apply_review_feedback_to_meta(meta_regulation_state, review_feedback_state)

    strategic_window_state = strategic_window_builder(
        window,
        candle_state=candle_state,
        visual_market_state=visual_market_state,
        structure_perception_state=structure_perception_state,
        form_symbol_state=form_symbol_state,
        meta_regulation_state=updated_meta_regulation_state,
        bot=bot,
    )
    updated_meta_regulation_state = apply_strategic_window_to_meta(updated_meta_regulation_state, strategic_window_state)

    active_mcm_contact_state = active_contact_builder(
        perception_state=perception_state,
        processing_state=processing_state,
        felt_state=felt_state,
        thought_state=thought_state,
        meta_regulation_state=updated_meta_regulation_state,
        strategic_window_state=strategic_window_state,
    )
    updated_meta_regulation_state = apply_active_mcm_contact_to_meta(
        updated_meta_regulation_state,
        active_mcm_contact_state,
        strategic_window_state=strategic_window_state,
    )
    possibility_field_state = build_mcm_possibility_field(
        temporal_perception_state=temporal_perception_state,
        form_symbol_state=form_symbol_state,
        meta_regulation_state=updated_meta_regulation_state,
        perception_state=perception_state,
        thought_state=thought_state,
        review_feedback_state=review_feedback_state,
        strategic_window_state=strategic_window_state,
        active_mcm_contact_state=active_mcm_contact_state,
    )
    updated_meta_regulation_state = apply_possibility_field_to_meta(
        updated_meta_regulation_state,
        possibility_field_state,
    )

    return {
        "review_feedback_state": dict(review_feedback_state or {}),
        "strategic_window_state": dict(strategic_window_state or {}),
        "active_mcm_contact_state": dict(active_mcm_contact_state or {}),
        "possibility_field_state": dict(possibility_field_state or {}),
        "meta_regulation_state": dict(updated_meta_regulation_state or {}),
    }


def commit_runtime_entry_bot_state(
    bot,
    *,
    visual_market_state,
    temporal_perception_state,
    perception_state,
    outer_visual_perception_state,
    inner_field_perception_state,
    structure_perception_state,
    processing_state,
    expectation_state,
    form_symbol_state,
    strategic_window_state,
    area_perception_profile,
    active_mcm_contact_state,
    possibility_field_state,
    felt_state,
    thought_state,
    meta_regulation_state,
):
    bot.visual_market_state = dict(visual_market_state)
    bot.temporal_perception_state = dict(temporal_perception_state)
    bot.perception_state = dict(perception_state)
    bot.outer_visual_perception_state = dict(outer_visual_perception_state)
    bot.inner_field_perception_state = dict(inner_field_perception_state)
    bot.structure_perception_state = dict(structure_perception_state)
    bot.processing_state = dict(processing_state)
    bot.expectation_state = dict(expectation_state or {})
    bot.form_symbol_state = dict(form_symbol_state or {})
    bot.strategic_window_state = dict(strategic_window_state or {})
    bot.area_perception_profile = dict(area_perception_profile or {})
    bot.active_mcm_contact_state = dict(active_mcm_contact_state or {})
    bot.mcm_possibility_field_state = dict(possibility_field_state or {})
    bot.felt_state = dict(felt_state)
    bot.thought_state = dict(thought_state)
    bot.meta_regulation_state = dict(meta_regulation_state)
    bot.neurochemical_state = dict(meta_regulation_state.get("neurochemical_state", {}) or {})


def record_runtime_entry_rejection_protocol(
    bot,
    *,
    decision,
    rejection_reason,
    meta_regulation_state,
    processing_state,
    felt_state,
    thought_state,
    fused,
    form_symbol_state,
    strategic_window_state,
    area_perception_profile,
    active_mcm_contact_state,
    early_active_context_trace,
    record_field_decision_protocol,
    record_strategic_window_protocol,
    record_active_mcm_contact_protocol,
):
    field_payload = {
        "decision": str(decision or "WAIT"),
        "meta_regulation_state": dict(meta_regulation_state or {}),
        "processing_state": dict(processing_state or {}),
        "felt_state": dict(felt_state or {}),
        "thought_state": dict(thought_state or {}),
        "memory_complexity_state": dict((fused or {}).get("memory_complexity_state", {}) or {}),
        "form_symbol_state": dict(form_symbol_state or {}),
        "strategic_window_state": dict(strategic_window_state or {}),
        "area_perception_profile": dict(area_perception_profile or {}),
        "active_mcm_contact_state": dict(active_mcm_contact_state or {}),
        "active_context_trace": dict(early_active_context_trace or {}),
        "context_cluster_id": str((fused or {}).get("context_cluster_id", "-") or "-"),
        "rejection_reason": str(rejection_reason or "runtime_entry_rejected"),
    }
    record_field_decision_protocol(
        bot,
        field_payload,
        meta_regulation_state=meta_regulation_state,
        processing_state=processing_state,
        felt_state=felt_state,
        thought_state=thought_state,
    )
    record_strategic_window_protocol(
        bot,
        {
            "decision": str(decision or "WAIT"),
            "meta_regulation_state": dict(meta_regulation_state or {}),
            "strategic_window_state": dict(strategic_window_state or {}),
            "active_mcm_contact_state": dict(active_mcm_contact_state or {}),
            "active_context_trace": dict(early_active_context_trace or {}),
            "context_cluster_id": str((fused or {}).get("context_cluster_id", "-") or "-"),
            "rejection_reason": str(rejection_reason or "runtime_entry_rejected"),
        },
    )
    record_active_mcm_contact_protocol(
        bot,
        {
            "decision": str(decision or "WAIT"),
            "meta_regulation_state": dict(meta_regulation_state or {}),
            "active_mcm_contact_state": dict(active_mcm_contact_state or {}),
            "active_context_trace": dict(early_active_context_trace or {}),
            "rejection_reason": str(rejection_reason or "runtime_entry_rejected"),
        },
    )


def record_runtime_entry_result_protocol(
    bot,
    result,
    *,
    meta_regulation_state,
    processing_state,
    felt_state,
    thought_state,
    record_field_decision_protocol,
    record_strategic_window_protocol,
    record_active_mcm_contact_protocol,
):
    if bool(getattr(Config, "MCM_FIELD_DECISION_PROTOCOL_DEBUG", False)):
        record_field_decision_protocol(
            bot,
            result,
            meta_regulation_state=meta_regulation_state,
            processing_state=processing_state,
            felt_state=felt_state,
            thought_state=thought_state,
        )
    if bool(getattr(Config, "MCM_STRATEGIC_WINDOW_PROTOCOL_DEBUG", False)):
        record_strategic_window_protocol(bot, result)
    if bool(getattr(Config, "MCM_ACTIVE_CONTACT_PROTOCOL_DEBUG", False)):
        record_active_mcm_contact_protocol(bot, result)


def build_virtual_observation_plan(
    *,
    decision,
    candle_state,
    fused,
    stimulus,
    snapshot,
    bot,
    strategic_window_state,
    form_symbol_state,
    thought_state=None,
    derive_trade_plan_from_brain,
):
    if decision not in ("LONG", "SHORT"):
        return {}

    try:
        virtual_prices = derive_trade_plan_from_brain(
            decision,
            candle_state,
            fused,
            stimulus,
            snapshot,
            bot=bot,
            strategic_window_state=strategic_window_state,
            form_symbol_state=form_symbol_state,
            thought_state=thought_state,
        )
    except Exception:
        virtual_prices = None

    if not isinstance(virtual_prices, dict):
        return {}

    return {
        "entry_price": float(virtual_prices.get("entry_price", 0.0) or 0.0),
        "sl_price": float(virtual_prices.get("sl_price", 0.0) or 0.0),
        "tp_price": float(virtual_prices.get("tp_price", 0.0) or 0.0),
        "rr_value": float(virtual_prices.get("rr_value", 0.0) or 0.0),
        "entry_validity_band": dict(virtual_prices.get("entry_validity_band", {}) or {}),
        "target_conviction": float(virtual_prices.get("target_conviction", 0.0) or 0.0),
        "risk_model_score": float(virtual_prices.get("risk_model_score", 0.0) or 0.0),
        "reward_model_score": float(virtual_prices.get("reward_model_score", 0.0) or 0.0),
        "entry_mode": str(virtual_prices.get("entry_mode", "no_mature_entry_thesis") or "no_mature_entry_thesis"),
        "entry_choice_state": str(virtual_prices.get("entry_choice_state", "no_entry_choice") or "no_entry_choice"),
        "strategic_area_focus_id": str(virtual_prices.get("strategic_area_focus_id", "-") or "-"),
        "strategic_area_price_low": float(virtual_prices.get("strategic_area_price_low", 0.0) or 0.0),
        "strategic_area_price_high": float(virtual_prices.get("strategic_area_price_high", 0.0) or 0.0),
        "strategic_entry_location": str(virtual_prices.get("strategic_entry_location", "-") or "-"),
    }


def build_runtime_no_plan_result(
    *,
    decision,
    virtual_observation_plan,
    energy,
    coherence,
    asymmetry,
    coh_zone,
    snapshot,
    stimulus,
    world_state,
    structure_perception_state,
    temporal_perception_state,
    outer_visual_perception_state,
    inner_field_perception_state,
    processing_state,
    perception_state,
    felt_state,
    thought_state,
    meta_regulation_state,
    expectation_state,
    form_symbol_state,
    strategic_window_state,
    area_perception_profile,
    active_mcm_contact_state,
    early_active_context_trace,
    state_signature,
    fused,
    neural_state,
    review_feedback_state,
):
    virtual_plan = dict(virtual_observation_plan or {})
    meta = dict(meta_regulation_state or {})
    signal = dict(fused or {})
    neural = dict(neural_state or {})
    vision_state = dict((stimulus or {}).get("vision", {}) or {})
    market_hearing_state = dict(vision_state.get("market_hearing_state", {}) or {})

    return {
        "decision": "WAIT",
        "proposed_decision": str(decision or "WAIT"),
        "entry_price": float(virtual_plan.get("entry_price", 0.0) or 0.0),
        "sl_price": float(virtual_plan.get("sl_price", 0.0) or 0.0),
        "tp_price": float(virtual_plan.get("tp_price", 0.0) or 0.0),
        "rr_value": float(virtual_plan.get("rr_value", 0.0) or 0.0),
        "entry_validity_band": dict(virtual_plan.get("entry_validity_band", {}) or {}),
        "target_conviction": float(virtual_plan.get("target_conviction", 0.0) or 0.0),
        "risk_model_score": float(virtual_plan.get("risk_model_score", 0.0) or 0.0),
        "reward_model_score": float(virtual_plan.get("reward_model_score", 0.0) or 0.0),
        "entry_mode": str(virtual_plan.get("entry_mode", "no_mature_entry_thesis") or "no_mature_entry_thesis"),
        "entry_choice_state": str(virtual_plan.get("entry_choice_state", "no_entry_choice") or "no_entry_choice"),
        "strategic_area_focus_id": str(virtual_plan.get("strategic_area_focus_id", "-") or "-"),
        "strategic_area_price_low": float(virtual_plan.get("strategic_area_price_low", 0.0) or 0.0),
        "strategic_area_price_high": float(virtual_plan.get("strategic_area_price_high", 0.0) or 0.0),
        "strategic_entry_location": str(virtual_plan.get("strategic_entry_location", "-") or "-"),
        "energy": float(energy),
        "market_hearing_state": dict(market_hearing_state),
        "market_loudness": float(market_hearing_state.get("loudness", vision_state.get("market_loudness", vision_state.get("auditory_stimulus", 0.0))) or 0.0),
        "market_frequency_hz": float(market_hearing_state.get("frequency_hz", vision_state.get("market_frequency_hz", 0.0)) or 0.0),
        "market_hearing_compression": float(market_hearing_state.get("compression", vision_state.get("market_hearing_compression", 0.0)) or 0.0),
        "market_tone": str(market_hearing_state.get("tone", vision_state.get("market_tone", "silent_tone")) or "silent_tone"),
        "coherence": float(coherence),
        "asymmetry": int(asymmetry),
        "coh_zone": float(coh_zone),
        "self_state": str((snapshot or {}).get("self_state", "stable")),
        "attractor": str((snapshot or {}).get("attractor", "neutral")),
        "memory_center": float(((snapshot or {}).get("strongest_memory") or {}).get("center", 0.0) or 0.0),
        "memory_strength": int(((snapshot or {}).get("strongest_memory") or {}).get("strength", 0) or 0),
        "vision": dict(vision_state or {}),
        "filtered_vision": dict((stimulus or {}).get("filtered_vision", {}) or {}),
        "focus": dict((stimulus or {}).get("focus", {}) or {}),
        "world_state": dict(world_state or {}),
        "structure_perception_state": dict(structure_perception_state or {}),
        "temporal_perception_state": dict(temporal_perception_state or {}),
        "outer_visual_perception_state": dict(outer_visual_perception_state or {}),
        "inner_field_perception_state": dict(inner_field_perception_state or {}),
        "processing_state": dict(processing_state or {}),
        "perception_state": dict(perception_state or {}),
        "felt_state": dict(felt_state or {}),
        "thought_state": dict(thought_state or {}),
        "meta_regulation_state": dict(meta or {}),
        "neurochemical_state": dict(meta.get("neurochemical_state", {}) or {}),
        "expectation_state": dict(expectation_state or {}),
        "form_symbol_state": dict(form_symbol_state or {}),
        "strategic_window_state": dict(strategic_window_state or {}),
        "area_perception_profile": dict(area_perception_profile or {}),
        "active_mcm_contact_state": dict(active_mcm_contact_state or {}),
        "active_context_trace": dict(early_active_context_trace or {}),
        "state_signature": dict(state_signature or {}),
        "memory_complexity_state": dict(signal.get("memory_complexity_state", {}) or {}),
        "signature_bias": float(signal.get("signature_bias", 0.0) or 0.0),
        "signature_block": bool(signal.get("signature_block", False)),
        "signature_quality": float(signal.get("signature_quality", 0.0) or 0.0),
        "signature_distance": float(signal.get("signature_distance", 0.0) or 0.0),
        "context_cluster_id": str(signal.get("context_cluster_id", "-") or "-"),
        "context_cluster_bias": float(signal.get("context_cluster_bias", 0.0) or 0.0),
        "context_cluster_quality": float(signal.get("context_cluster_quality", 0.0) or 0.0),
        "context_cluster_distance": float(signal.get("context_cluster_distance", 0.0) or 0.0),
        "context_cluster_block": bool(signal.get("context_cluster_block", False)),
        "inhibition_level": float(neural.get("inhibition_level", 0.0) or 0.0),
        "habituation_level": float(neural.get("habituation_level", 0.0) or 0.0),
        "competition_bias": float(neural.get("competition_bias", 0.0) or 0.0),
        "observation_mode": bool(neural.get("observation_mode", False)),
        "long_score": float(signal.get("long_score", 0.0) or 0.0),
        "short_score": float(signal.get("short_score", 0.0) or 0.0),
        "review_feedback_state": dict(review_feedback_state or {}),
        "rejection_reason": str(meta.get("rejection_reason", signal.get("reject_reason", "meta_block")) or "meta_block"),
    }


def build_runtime_entry_trade_result(
    *,
    decision,
    prices,
    energy,
    coherence,
    asymmetry,
    coh_zone,
    snapshot,
    stimulus,
    world_state,
    structure_perception_state,
    temporal_perception_state,
    outer_visual_perception_state,
    inner_field_perception_state,
    processing_state,
    perception_state,
    felt_state,
    thought_state,
    meta_regulation_state,
    expectation_state,
    form_symbol_state,
    strategic_window_state,
    area_perception_profile,
    active_mcm_contact_state,
    early_active_context_trace,
    state_signature,
    fused,
    neural_state,
    review_feedback_state,
    field_stimulus_density,
    field_density,
    field_stability,
    regulatory_load,
    action_capacity,
    recovery_need,
    survival_pressure,
):
    plan = dict(prices or {})
    meta = dict(meta_regulation_state or {})
    signal = dict(fused or {})
    neural = dict(neural_state or {})
    vision_state = dict((stimulus or {}).get("vision", {}) or {})
    market_hearing_state = dict(vision_state.get("market_hearing_state", {}) or {})

    return {
        "decision": decision,
        "entry_price": float(plan["entry_price"]),
        "sl_price": float(plan["sl_price"]),
        "tp_price": float(plan["tp_price"]),
        "rr_value": float(plan["rr_value"]),
        "entry_validity_band": dict(plan.get("entry_validity_band", {}) or {}),
        "target_conviction": float(plan.get("target_conviction", 0.0) or 0.0),
        "risk_model_score": float(plan.get("risk_model_score", 0.0) or 0.0),
        "reward_model_score": float(plan.get("reward_model_score", 0.0) or 0.0),
        "entry_mode": str(plan.get("entry_mode", "no_mature_entry_thesis") or "no_mature_entry_thesis"),
        "contact_entry_mode": str(plan.get("contact_entry_mode", plan.get("entry_mode", "no_mature_entry_thesis")) or "no_mature_entry_thesis"),
        "impulse_entry_price": float(plan.get("impulse_entry_price", plan["entry_price"]) or plan["entry_price"]),
        "contact_entry_price": float(plan.get("contact_entry_price", plan.get("strategic_entry_price", plan["entry_price"])) or plan["entry_price"]),
        "strategic_entry_price": float(plan.get("strategic_entry_price", plan.get("contact_entry_price", plan["entry_price"])) or plan["entry_price"]),
        "area_contact_weight": float(plan.get("area_contact_weight", plan.get("strategic_entry_weight", 0.0)) or 0.0),
        "area_contact_fit": float(plan.get("area_contact_fit", plan.get("strategic_entry_fit", 0.0)) or 0.0),
        "area_contact_intention": float(plan.get("area_contact_intention", plan.get("area_motor_intention", 0.0)) or 0.0),
        "contact_entry_weight": float(plan.get("contact_entry_weight", plan.get("strategic_entry_weight", 0.0)) or 0.0),
        "contact_entry_fit": float(plan.get("contact_entry_fit", plan.get("strategic_entry_fit", 0.0)) or 0.0),
        "strategic_entry_weight": float(plan.get("strategic_entry_weight", plan.get("contact_entry_weight", 0.0)) or 0.0),
        "strategic_entry_fit": float(plan.get("strategic_entry_fit", plan.get("contact_entry_fit", 0.0)) or 0.0),
        "area_contact_distance_fit": float(plan.get("area_contact_distance_fit", plan.get("area_motor_distance_fit", 0.0)) or 0.0),
        "area_motor_intention": float(plan.get("area_motor_intention", 0.0) or 0.0),
        "area_motor_distance_fit": float(plan.get("area_motor_distance_fit", plan.get("area_contact_distance_fit", 0.0)) or 0.0),
        "impulse_perception_pressure": float(plan.get("impulse_perception_pressure", plan.get("impulse_entry_intention", 0.0)) or 0.0),
        "impulse_entry_intention": float(plan.get("impulse_entry_intention", 0.0) or 0.0),
        "area_order_geometry_intention": float(plan.get("area_order_geometry_intention", plan.get("area_entry_intention", 0.0)) or 0.0),
        "area_entry_intention": float(plan.get("area_entry_intention", 0.0) or 0.0),
        "entry_contact_pressure": float(plan.get("entry_contact_pressure", plan.get("entry_choice_pressure", plan.get("entry_choice_conflict", 0.0))) or 0.0),
        "entry_choice_pressure": float(plan.get("entry_choice_pressure", plan.get("entry_contact_pressure", plan.get("entry_choice_conflict", 0.0))) or 0.0),
        "entry_choice_conflict": float(plan.get("entry_choice_conflict", plan.get("entry_contact_pressure", 0.0)) or 0.0),
        "entry_contact_bearing": float(plan.get("entry_contact_bearing", plan.get("entry_choice_bearing", 0.0)) or 0.0),
        "entry_choice_bearing": float(plan.get("entry_choice_bearing", 0.0) or 0.0),
        "area_contact_readiness": float(plan.get("area_contact_readiness", plan.get("area_direct_readiness", 0.0)) or 0.0),
        "area_direct_readiness": float(plan.get("area_direct_readiness", 0.0) or 0.0),
        "area_contact_restraint": float(plan.get("area_contact_restraint", plan.get("area_motor_restraint", 0.0)) or 0.0),
        "area_motor_restraint": float(plan.get("area_motor_restraint", 0.0) or 0.0),
        "entry_geometry_bearing": float(plan.get("entry_geometry_bearing", 0.0) or 0.0),
        "entry_geometry_state": str(plan.get("entry_geometry_state", "contact_offer_only") or "contact_offer_only"),
        "thought_seed_bearing": float(plan.get("thought_seed_bearing", 0.0) or 0.0),
        "thought_state_bearing": float(plan.get("thought_state_bearing", 0.0) or 0.0),
        "thought_state_carrier_factor": float(plan.get("thought_state_carrier_factor", 0.0) or 0.0),
        "thought_contact_bearing": float(plan.get("thought_contact_bearing", 0.0) or 0.0),
        "pre_geometry_thought_bearing": float(plan.get("pre_geometry_thought_bearing", 0.0) or 0.0),
        "pre_geometry_felt_bearing": float(plan.get("pre_geometry_felt_bearing", 0.0) or 0.0),
        "pre_geometry_reality_bearing": float(plan.get("pre_geometry_reality_bearing", 0.0) or 0.0),
        "pre_geometry_preference_bearing": float(plan.get("pre_geometry_preference_bearing", 0.0) or 0.0),
        "visual_reality_bearing": float(plan.get("visual_reality_bearing", 0.0) or 0.0),
        "felt_reality_bearing": float(plan.get("felt_reality_bearing", 0.0) or 0.0),
        "thought_reality_bearing": float(plan.get("thought_reality_bearing", 0.0) or 0.0),
        "form_mcm_reality_fit": float(plan.get("form_mcm_reality_fit", 0.0) or 0.0),
        "uncoupled_area_contact_pressure": float(plan.get("uncoupled_area_contact_pressure", 0.0) or 0.0),
        "hypothesis_reality_binding": float(plan.get("hypothesis_reality_binding", 0.0) or 0.0),
        "hypothesis_reality_binding_gap": float(plan.get("hypothesis_reality_binding_gap", 0.0) or 0.0),
        "hypothesis_reality_binding_state": str(plan.get("hypothesis_reality_binding_state", "hypothesis_reality_unread") or "hypothesis_reality_unread"),
        "hypothesis_reality_binding_pressures": dict(plan.get("hypothesis_reality_binding_pressures", {}) or {}),
        "organic_contact_bearing": float(plan.get("organic_contact_bearing", 0.0) or 0.0),
        "entry_contact_state": str(plan.get("entry_contact_state", plan.get("entry_choice_state", "no_entry_choice")) or "no_entry_choice"),
        "entry_choice_state": str(plan.get("entry_choice_state", "no_entry_choice") or "no_entry_choice"),
        "entry_preference_state": str(plan.get("entry_preference_state", "no_entry_preference") or "no_entry_preference"),
        "entry_choice_basis": str(plan.get("entry_choice_basis", "no_contact_offer") or "no_contact_offer"),
        "entry_contact_option_count": int(plan.get("entry_contact_option_count", 0) or 0),
        "selected_entry_offer_score": float(plan.get("selected_entry_offer_score", 0.0) or 0.0),
        "selected_entry_learned_fit": float(plan.get("selected_entry_learned_fit", 0.0) or 0.0),
        "selected_entry_preference_key": str(plan.get("selected_entry_preference_key", "-") or "-"),
        "selected_entry_preference_trust": float(plan.get("selected_entry_preference_trust", 0.0) or 0.0),
        "selected_entry_preference_caution": float(plan.get("selected_entry_preference_caution", 0.0) or 0.0),
        "selected_entry_preference_maturity": float(plan.get("selected_entry_preference_maturity", 0.0) or 0.0),
        "selected_entry_preference_utility": float(plan.get("selected_entry_preference_utility", 0.0) or 0.0),
        "selected_entry_property_profile_id": str(plan.get("selected_entry_property_profile_id", "-") or "-"),
        "selected_entry_property_profile_similarity": float(plan.get("selected_entry_property_profile_similarity", 0.0) or 0.0),
        "selected_entry_property_profile_trust": float(plan.get("selected_entry_property_profile_trust", 0.0) or 0.0),
        "selected_entry_property_profile_caution": float(plan.get("selected_entry_property_profile_caution", 0.0) or 0.0),
        "selected_entry_property_profile_maturity": float(plan.get("selected_entry_property_profile_maturity", 0.0) or 0.0),
        "selected_entry_property_profile_utility": float(plan.get("selected_entry_property_profile_utility", 0.0) or 0.0),
        "entry_contact_options": list(plan.get("entry_contact_options", []) or []),
        "contact_learning_state": str(plan.get("contact_learning_state", "unformed_contact") or "unformed_contact"),
        "learned_contact_fit": float(plan.get("learned_contact_fit", 0.0) or 0.0),
        "entry_choice_sync": str(plan.get("entry_choice_sync", "-") or "-"),
        "hypothesis_reality_state": str(plan.get("hypothesis_reality_state", "hypothesis_context_unread") or "hypothesis_context_unread"),
        "pre_entry_emergent_structure_reading": float(plan.get("pre_entry_emergent_structure_reading", 0.0) or 0.0),
        "pre_entry_emergent_structure_confirmation": float(plan.get("pre_entry_emergent_structure_confirmation", 0.0) or 0.0),
        "pre_entry_emergent_structure_state": str(plan.get("pre_entry_emergent_structure_state", "ordinary_structure_contact") or "ordinary_structure_contact"),
        "hypothesis_reality_modulation": float(plan.get("hypothesis_reality_modulation", 0.0) or 0.0),
        "hypothesis_reality_bearing": float(plan.get("hypothesis_reality_bearing", plan.get("hypothesis_action_support", 0.0)) or 0.0),
        "open_hypothesis_reality_bearing": float(plan.get("open_hypothesis_reality_bearing", plan.get("open_hypothesis_reality_permission", 0.0)) or 0.0),
        "open_hypothesis_reality_fit": float(plan.get("open_hypothesis_reality_fit", plan.get("open_hypothesis_reality_bearing", plan.get("open_hypothesis_reality_permission", 0.0))) or 0.0),
        "open_hypothesis_reality_permission": float(plan.get("open_hypothesis_reality_permission", 0.0) or 0.0),
        "hypothesis_contact_restraint": float(plan.get("hypothesis_contact_restraint", 0.0) or 0.0),
        "hypothesis_action_support": float(plan.get("hypothesis_action_support", 0.0) or 0.0),
        "hypothesis_observation_pressure": float(plan.get("hypothesis_observation_pressure", 0.0) or 0.0),
        "order_geometry_source": str(plan.get("order_geometry_source", "area_contact_adapter") or "area_contact_adapter"),
        "impulse_role": str(plan.get("impulse_role", "perception_pressure_only") or "perception_pressure_only"),
        "strategic_area_focus_id": str(plan.get("strategic_area_focus_id", "-") or "-"),
        "strategic_area_price_low": float(plan.get("strategic_area_price_low", 0.0) or 0.0),
        "strategic_area_price_high": float(plan.get("strategic_area_price_high", 0.0) or 0.0),
        "strategic_entry_location": str(plan.get("strategic_entry_location", "-") or "-"),
        "energy": float(energy),
        "market_hearing_state": dict(market_hearing_state),
        "market_loudness": float(market_hearing_state.get("loudness", vision_state.get("market_loudness", vision_state.get("auditory_stimulus", 0.0))) or 0.0),
        "market_frequency_hz": float(market_hearing_state.get("frequency_hz", vision_state.get("market_frequency_hz", 0.0)) or 0.0),
        "market_hearing_compression": float(market_hearing_state.get("compression", vision_state.get("market_hearing_compression", 0.0)) or 0.0),
        "market_tone": str(market_hearing_state.get("tone", vision_state.get("market_tone", "silent_tone")) or "silent_tone"),
        "coherence": float(coherence),
        "asymmetry": int(asymmetry),
        "coh_zone": float(coh_zone),
        "self_state": str((snapshot or {}).get("self_state", "stable")),
        "attractor": str((snapshot or {}).get("attractor", "neutral")),
        "memory_center": float(((snapshot or {}).get("strongest_memory") or {}).get("center", 0.0) or 0.0),
        "memory_strength": int(((snapshot or {}).get("strongest_memory") or {}).get("strength", 0) or 0),
        "vision": dict(vision_state or {}),
        "filtered_vision": dict((stimulus or {}).get("filtered_vision", {}) or {}),
        "focus": dict((stimulus or {}).get("focus", {}) or {}),
        "world_state": dict(world_state or {}),
        "structure_perception_state": dict(structure_perception_state or {}),
        "temporal_perception_state": dict(temporal_perception_state or {}),
        "outer_visual_perception_state": dict(outer_visual_perception_state or {}),
        "inner_field_perception_state": dict(inner_field_perception_state or {}),
        "processing_state": dict(processing_state or {}),
        "perception_state": dict(perception_state or {}),
        "felt_state": dict(felt_state or {}),
        "thought_state": dict(thought_state or {}),
        "meta_regulation_state": dict(meta or {}),
        "neurochemical_state": dict(meta.get("neurochemical_state", {}) or {}),
        "expectation_state": dict(expectation_state or {}),
        "form_symbol_state": dict(form_symbol_state or {}),
        "strategic_window_state": dict(strategic_window_state or {}),
        "area_perception_profile": dict(area_perception_profile or {}),
        "active_mcm_contact_state": dict(active_mcm_contact_state or {}),
        "active_context_trace": dict(early_active_context_trace or {}),
        "state_signature": dict(state_signature or {}),
        "memory_complexity_state": dict(signal.get("memory_complexity_state", {}) or {}),
        "signature_bias": float(signal.get("signature_bias", 0.0) or 0.0),
        "signature_block": bool(signal.get("signature_block", False)),
        "signature_quality": float(signal.get("signature_quality", 0.0) or 0.0),
        "signature_distance": float(signal.get("signature_distance", 0.0) or 0.0),
        "context_cluster_id": str(signal.get("context_cluster_id", "-") or "-"),
        "context_cluster_bias": float(signal.get("context_cluster_bias", 0.0) or 0.0),
        "context_cluster_quality": float(signal.get("context_cluster_quality", 0.0) or 0.0),
        "context_cluster_distance": float(signal.get("context_cluster_distance", 0.0) or 0.0),
        "context_cluster_block": bool(signal.get("context_cluster_block", False)),
        "inhibition_level": float(neural.get("inhibition_level", 0.0) or 0.0),
        "habituation_level": float(neural.get("habituation_level", 0.0) or 0.0),
        "competition_bias": float(neural.get("competition_bias", 0.0) or 0.0),
        "observation_mode": bool(neural.get("observation_mode", False)),
        "long_score": float(signal.get("long_score", 0.0) or 0.0),
        "short_score": float(signal.get("short_score", 0.0) or 0.0),
        "review_feedback_state": dict(review_feedback_state or {}),
        "temporal_decision_state": dict(signal.get("temporal_decision_state", {}) or {}),
        "field_stimulus_density": float(field_stimulus_density),
        "field_density": float(field_density),
        "field_stability": float(field_stability),
        "regulatory_load": float(regulatory_load),
        "action_capacity": float(action_capacity),
        "recovery_need": float(recovery_need),
        "survival_pressure": float(survival_pressure),
    }


def synchronize_entry_choice_prices(
    prices,
    *,
    decision,
    candle_state,
    fused,
    stimulus,
    snapshot,
    bot,
    strategic_window_state,
    form_symbol_state,
    derive_trade_plan_from_brain,
):
    current_prices = dict(prices or {})
    strategic = dict(strategic_window_state or {})

    unresolved_contact_states = ("no_entry_contact", "no_mature_entry_thesis", "area_contact_weak", "impulse_only", "impulse_pressure_dominant")
    should_resolve_strategic_context = (
        str(current_prices.get("entry_contact_state", current_prices.get("entry_choice_state", "no_entry_contact")) or "no_entry_contact") in unresolved_contact_states
        and float(current_prices.get("area_contact_intention", current_prices.get("area_motor_intention", 0.0)) or 0.0) <= 0.0
        and float(strategic.get("area_price_low", 0.0) or 0.0) > 0.0
        and float(strategic.get("area_price_high", 0.0) or 0.0) > 0.0
    )

    if not should_resolve_strategic_context:
        current_prices["entry_choice_sync"] = "native_choice_state"
        return current_prices

    try:
        synchronized_prices = derive_trade_plan_from_brain(
            decision,
            candle_state,
            fused,
            stimulus,
            snapshot,
            bot=bot,
            strategic_window_state=strategic_window_state,
            form_symbol_state=form_symbol_state,
            thought_state=thought_state,
        )
    except Exception:
        synchronized_prices = None

    if (
        isinstance(synchronized_prices, dict)
        and str(synchronized_prices.get("entry_contact_state", synchronized_prices.get("entry_choice_state", "no_entry_contact")) or "no_entry_contact") not in unresolved_contact_states
    ):
        synchronized_prices = dict(synchronized_prices)
        synchronized_prices["entry_choice_sync"] = "contact_context_integrated"
        return synchronized_prices

    current_prices["entry_choice_sync"] = "contact_context_unresolved"
    return current_prices


RESULT_ENTRY_CHOICE_SYNC_KEYS = (
    "entry_price",
    "sl_price",
    "tp_price",
    "rr_value",
    "entry_validity_band",
    "target_conviction",
    "risk_model_score",
    "reward_model_score",
    "entry_mode",
    "contact_entry_mode",
    "impulse_entry_price",
    "contact_entry_price",
    "strategic_entry_price",
    "area_contact_weight",
    "area_contact_fit",
    "area_contact_intention",
    "contact_entry_weight",
    "contact_entry_fit",
    "strategic_entry_weight",
    "strategic_entry_fit",
    "area_contact_distance_fit",
    "area_motor_intention",
    "area_motor_distance_fit",
    "impulse_perception_pressure",
    "impulse_entry_intention",
    "area_order_geometry_intention",
    "area_entry_intention",
    "entry_contact_pressure",
    "entry_choice_pressure",
    "entry_choice_conflict",
    "entry_contact_bearing",
    "entry_choice_bearing",
    "area_contact_readiness",
    "area_contact_restraint",
    "entry_geometry_bearing",
    "entry_geometry_state",
    "pre_geometry_thought_bearing",
    "pre_geometry_felt_bearing",
    "pre_geometry_reality_bearing",
    "pre_geometry_preference_bearing",
    "visual_reality_bearing",
    "felt_reality_bearing",
    "thought_reality_bearing",
    "form_mcm_reality_fit",
    "uncoupled_area_contact_pressure",
    "hypothesis_reality_binding",
    "hypothesis_reality_binding_gap",
    "hypothesis_reality_binding_state",
    "hypothesis_reality_binding_pressures",
    "organic_contact_bearing",
    "entry_contact_state",
    "entry_choice_state",
    "entry_preference_state",
    "entry_choice_basis",
    "entry_contact_option_count",
    "selected_entry_offer_score",
    "selected_entry_learned_fit",
    "selected_entry_preference_key",
    "selected_entry_preference_trust",
    "selected_entry_preference_caution",
    "selected_entry_preference_maturity",
    "selected_entry_preference_utility",
    "selected_entry_property_profile_id",
    "selected_entry_property_profile_similarity",
    "selected_entry_property_profile_trust",
    "selected_entry_property_profile_caution",
    "selected_entry_property_profile_maturity",
    "selected_entry_property_profile_utility",
    "entry_contact_options",
    "contact_learning_state",
    "learned_contact_fit",
    "hypothesis_reality_state",
    "hypothesis_observation_pressure",
    "hypothesis_contact_restraint",
    "hypothesis_reality_modulation",
    "hypothesis_reality_bearing",
    "open_hypothesis_reality_bearing",
    "open_hypothesis_reality_fit",
    "open_hypothesis_reality_permission",
    "pre_entry_emergent_structure_state",
    "pre_entry_emergent_structure_reading",
    "pre_entry_emergent_structure_confirmation",
    "order_geometry_source",
    "impulse_role",
    "strategic_area_focus_id",
    "strategic_area_price_low",
    "strategic_area_price_high",
    "strategic_entry_location",
)


def synchronize_entry_choice_result(
    result,
    *,
    decision,
    candle_state,
    fused,
    stimulus,
    snapshot,
    bot,
    strategic_window_state,
    form_symbol_state,
    derive_trade_plan_from_brain,
):
    current_result = dict(result or {})
    strategic = dict(strategic_window_state or {})
    unresolved_contact_states = ("no_entry_contact", "no_mature_entry_thesis", "area_contact_weak", "impulse_only", "impulse_pressure_dominant")
    should_resolve_strategic_context = (
        str(current_result.get("entry_contact_state", current_result.get("entry_choice_state", "no_entry_contact")) or "no_entry_contact") in unresolved_contact_states
        and float(current_result.get("area_contact_intention", current_result.get("area_motor_intention", 0.0)) or 0.0) <= 0.0
        and float(strategic.get("area_price_low", 0.0) or 0.0) > 0.0
        and float(strategic.get("area_price_high", 0.0) or 0.0) > 0.0
    )

    if not should_resolve_strategic_context:
        return current_result

    try:
        synchronized_prices = derive_trade_plan_from_brain(
            decision,
            dict(current_result.get("world_state", {}).get("candle_state", candle_state) or candle_state),
            dict(current_result.get("signal", fused) or fused),
            {
                "focus": dict(current_result.get("focus", (stimulus or {}).get("focus", {})) or {}),
                "filtered_vision": dict(current_result.get("filtered_vision", (stimulus or {}).get("filtered_vision", {})) or {}),
                "vision": dict(current_result.get("vision", (stimulus or {}).get("vision", {})) or {}),
            },
            snapshot,
            bot=bot,
            strategic_window_state=dict(current_result.get("strategic_window_state", strategic_window_state) or strategic_window_state),
            form_symbol_state=dict(current_result.get("form_symbol_state", form_symbol_state) or form_symbol_state),
            thought_state=dict(current_result.get("thought_state", thought_state) or thought_state),
        )
    except Exception:
        synchronized_prices = None

    if (
        isinstance(synchronized_prices, dict)
        and str(synchronized_prices.get("entry_contact_state", synchronized_prices.get("entry_choice_state", "no_entry_contact")) or "no_entry_contact") not in unresolved_contact_states
    ):
        for sync_key in RESULT_ENTRY_CHOICE_SYNC_KEYS:
            if sync_key in synchronized_prices:
                current_result[sync_key] = synchronized_prices[sync_key]
        current_result["entry_choice_sync"] = "contact_context_integrated"
    else:
        current_result["entry_choice_sync"] = "contact_context_unresolved"

    return current_result
