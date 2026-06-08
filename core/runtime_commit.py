"""Runtime commit helpers.

These helpers perform small, explicit bot-state commits for the runtime bridge.
The low-level advance functions are injected by `MCM_Brain_Modell.py` so this
module does not own the biological/mechanical formulas.
"""


def advance_runtime_perception_layers(
    runtime_result,
    *,
    bot=None,
    decision_tendency="hold",
    market_tick_advanced=True,
    temporal_advance=None,
    felt_advance=None,
    thought_advance=None,
):
    runtime_payload = dict(runtime_result or {})

    if temporal_advance is not None:
        temporal_state = temporal_advance(
            temporal_perception_state=dict(runtime_payload.get("temporal_perception_state", {}) or {}),
            bot=bot,
            decision_tendency=decision_tendency,
            market_tick_advanced=market_tick_advanced,
        )

        if temporal_state:
            runtime_payload["temporal_perception_state"] = dict(temporal_state)
            world_state = dict(runtime_payload.get("world_state", {}) or {})
            world_state["temporal_perception_state"] = dict(temporal_state)
            runtime_payload["world_state"] = dict(world_state)
            if bot is not None:
                bot.temporal_perception_state = dict(temporal_state)

    if felt_advance is not None:
        felt_state = felt_advance(
            felt_state=dict(runtime_payload.get("felt_state", {}) or {}),
            bot=bot,
            decision_tendency=decision_tendency,
            market_tick_advanced=market_tick_advanced,
        )

        if felt_state:
            runtime_payload["felt_state"] = dict(felt_state)
            if bot is not None:
                bot.felt_state = dict(felt_state)

    if thought_advance is not None:
        thought_state = thought_advance(
            thought_state=dict(runtime_payload.get("thought_state", {}) or {}),
            felt_state=dict(runtime_payload.get("felt_state", {}) or {}),
            temporal_perception_state=dict(runtime_payload.get("temporal_perception_state", {}) or {}),
            bot=bot,
            decision_tendency=decision_tendency,
            market_tick_advanced=market_tick_advanced,
        )

        if thought_state:
            runtime_payload["thought_state"] = dict(thought_state)
            if bot is not None:
                bot.thought_state = dict(thought_state)

    return runtime_payload


def commit_runtime_snapshot_state(
    bot,
    *,
    snapshot=None,
    decision_state=None,
    brain_snapshot=None,
    decision_tendency="hold",
    timestamp=None,
):
    if bot is None:
        return None

    snapshot = dict(snapshot or {})
    decision_state = dict(decision_state or {})
    brain_snapshot = dict(brain_snapshot or {})

    bot.mcm_runtime_market_ticks = int(snapshot.get("market_ticks", 0) or 0)
    bot.mcm_runtime_snapshot = dict(snapshot)
    bot.mcm_runtime_decision_state = dict(decision_state)
    bot.mcm_runtime_brain_snapshot = dict(brain_snapshot)

    if decision_tendency == "observe":
        bot.mcm_last_observe_timestamp = timestamp

    return {
        "snapshot": dict(snapshot),
        "decision_state": dict(decision_state),
        "brain_snapshot": dict(brain_snapshot),
    }


def commit_active_context_trace(bot, active_context_trace=None, *, signal_merger=None):
    if bot is None:
        return None

    active_context_trace = dict(active_context_trace or {})
    bot.active_context_trace = dict(active_context_trace)

    runtime_snapshot = dict(getattr(bot, "mcm_runtime_snapshot", {}) or {})
    runtime_decision_state = dict(getattr(bot, "mcm_runtime_decision_state", {}) or {})
    runtime_brain_snapshot = dict(getattr(bot, "mcm_runtime_brain_snapshot", {}) or {})
    entry_result = dict(runtime_decision_state.get("entry_result", {}) or {})

    runtime_snapshot["active_context_trace"] = dict(active_context_trace)
    runtime_decision_state["active_context_trace"] = dict(active_context_trace)
    entry_result["active_context_trace"] = dict(active_context_trace)
    runtime_decision_state["entry_result"] = dict(entry_result)
    runtime_brain_snapshot["active_context_trace"] = dict(active_context_trace)

    if signal_merger is not None:
        brain_signal_state = dict(runtime_brain_snapshot.get("signal", {}) or {})
        runtime_brain_snapshot["signal"] = signal_merger(brain_signal_state, active_context_trace)

    bot.mcm_runtime_snapshot = dict(runtime_snapshot)
    bot.mcm_runtime_decision_state = dict(runtime_decision_state)
    bot.mcm_runtime_brain_snapshot = dict(runtime_brain_snapshot)

    episode_internal_state = dict(getattr(bot, "mcm_decision_episode_internal", {}) or {})
    if signal_merger is not None:
        episode_signal_state = dict(episode_internal_state.get("signal", {}) or {})
        episode_internal_state["signal"] = signal_merger(episode_signal_state, active_context_trace)
    episode_internal_state["active_context_trace"] = dict(active_context_trace)
    bot.mcm_decision_episode_internal = dict(episode_internal_state)

    return {
        "active_context_trace": dict(active_context_trace),
        "runtime_snapshot": dict(runtime_snapshot),
        "runtime_decision_state": dict(runtime_decision_state),
        "runtime_brain_snapshot": dict(runtime_brain_snapshot),
        "episode_internal_state": dict(episode_internal_state),
    }


def build_internal_episode_state(
    runtime_result,
    *,
    previous_internal=None,
    visible_episode_id="",
    decision_tendency="hold",
    timestamp=None,
    runtime_tick_seq=0,
):
    result = dict(runtime_result or {})
    previous_internal = dict(previous_internal or {})
    focus = dict(result.get("focus", {}) or {})
    signal = {
        "signature_bias": float(result.get("signature_bias", 0.0) or 0.0),
        "signature_block": bool(result.get("signature_block", False)),
        "signature_quality": float(result.get("signature_quality", 0.0) or 0.0),
        "signature_distance": float(result.get("signature_distance", 0.0) or 0.0),
        "context_cluster_id": str(result.get("context_cluster_id", "-") or "-"),
        "context_cluster_bias": float(result.get("context_cluster_bias", 0.0) or 0.0),
        "context_cluster_quality": float(result.get("context_cluster_quality", 0.0) or 0.0),
        "context_cluster_distance": float(result.get("context_cluster_distance", 0.0) or 0.0),
        "context_cluster_block": bool(result.get("context_cluster_block", False)),
        "inhibition_level": float(result.get("inhibition_level", 0.0) or 0.0),
        "habituation_level": float(result.get("habituation_level", 0.0) or 0.0),
        "competition_bias": float(result.get("competition_bias", 0.0) or 0.0),
        "observation_mode": bool(result.get("observation_mode", False)),
        "long_score": float(result.get("long_score", 0.0) or 0.0),
        "short_score": float(result.get("short_score", 0.0) or 0.0),
    }

    return {
        "episode_id": str(visible_episode_id or ""),
        "timestamp": timestamp,
        "runtime_tick_seq": int(runtime_tick_seq or 0),
        "learning_state": str(previous_internal.get("learning_state", "open") or "open"),
        "decision_tendency": str(decision_tendency or "hold"),
        "proposed_decision": str(result.get("proposed_decision", result.get("decision", "WAIT")) or "WAIT"),
        "world_state": dict(result.get("world_state", {}) or {}),
        "structure_perception_state": dict(result.get("structure_perception_state", {}) or {}),
        "outer_visual_perception_state": dict(result.get("outer_visual_perception_state", {}) or {}),
        "inner_field_perception_state": dict(result.get("inner_field_perception_state", {}) or {}),
        "processing_state": dict(result.get("processing_state", {}) or {}),
        "perception_state": dict(result.get("perception_state", {}) or {}),
        "felt_state": dict(result.get("felt_state", {}) or {}),
        "thought_state": dict(result.get("thought_state", {}) or {}),
        "meta_regulation_state": dict(result.get("meta_regulation_state", {}) or {}),
        "expectation_state": dict(result.get("expectation_state", {}) or {}),
        "state_signature": dict(result.get("state_signature", {}) or {}),
        "focus": dict(focus or {}),
        "signal": dict(signal or {}),
        "last_event": str(previous_internal.get("last_event", "") or ""),
        "last_payload": dict(previous_internal.get("last_payload", {}) or {}),
        "non_action_type": previous_internal.get("non_action_type", None),
        "internal_events": list(previous_internal.get("internal_events", []) or [])[-24:],
        "review_notes": dict(previous_internal.get("review_notes", {}) or {}),
        "visible_episode_id": str(visible_episode_id or ""),
    }


def build_visible_episode_state(
    runtime_result,
    *,
    previous_episode=None,
    episode_seq=0,
    decision_state=None,
    decision_tendency="hold",
    timestamp=None,
    runtime_tick_seq=0,
):
    result = dict(runtime_result or {})
    previous_episode = dict(previous_episode or {})
    decision_state = dict(decision_state or {})
    episode_timestamp = previous_episode.get("timestamp")

    if episode_timestamp != timestamp:
        episode = {
            "episode_id": f"ep_{int(episode_seq or 0)}",
            "timestamp": timestamp,
            "runtime_tick_seq": int(runtime_tick_seq or 0),
            "lifecycle_state": "tendency_formed",
            "action_status": "open",
            "perceived_at": timestamp,
            "internally_processed_at": timestamp,
            "tendency_formed_at": timestamp,
            "decision_tendency": str(decision_tendency or "hold"),
            "proposed_decision": str(decision_state.get("proposed_decision", "WAIT") or "WAIT"),
            "world_state": dict(result.get("world_state", {}) or {}),
            "perception_state": dict(result.get("perception_state", {}) or {}),
            "processing_state": dict(result.get("processing_state", {}) or {}),
            "felt_state": dict(result.get("felt_state", {}) or {}),
            "thought_state": dict(result.get("thought_state", {}) or {}),
            "meta_regulation_state": dict(result.get("meta_regulation_state", {}) or {}),
            "expectation_state": dict(result.get("expectation_state", {}) or {}),
            "form_symbol_state": dict(result.get("form_symbol_state", {}) or {}),
            "state_signature": dict(result.get("state_signature", {}) or {}),
            "events": [],
        }
        return episode

    episode = dict(previous_episode or {})
    episode["runtime_tick_seq"] = int(runtime_tick_seq or 0)
    episode["perceived_at"] = episode.get("perceived_at", timestamp)
    episode["internally_processed_at"] = episode.get("internally_processed_at", timestamp)
    episode["tendency_formed_at"] = timestamp
    episode["decision_tendency"] = str(decision_tendency or "hold")
    episode["proposed_decision"] = str(decision_state.get("proposed_decision", "WAIT") or "WAIT")

    locked_action_status = str(episode.get("action_status", "open") or "open")
    locked_lifecycle_state = str(episode.get("lifecycle_state", "tendency_formed") or "tendency_formed")
    episode_state_locked = locked_action_status not in ("", "open") or locked_lifecycle_state not in ("", "event_only", "tendency_formed")

    if not episode_state_locked:
        episode["lifecycle_state"] = "tendency_formed"
        episode["world_state"] = dict(result.get("world_state", {}) or {})
        episode["perception_state"] = dict(result.get("perception_state", {}) or {})
        episode["processing_state"] = dict(result.get("processing_state", {}) or {})
        episode["felt_state"] = dict(result.get("felt_state", {}) or {})
        episode["thought_state"] = dict(result.get("thought_state", {}) or {})
        episode["meta_regulation_state"] = dict(result.get("meta_regulation_state", {}) or {})
        episode["expectation_state"] = dict(result.get("expectation_state", {}) or {})
        episode["form_symbol_state"] = dict(result.get("form_symbol_state", {}) or {})
        episode["state_signature"] = dict(result.get("state_signature", {}) or {})

    return episode


def commit_runtime_episode_state(bot, *, episode=None, episode_internal=None):
    if bot is None:
        return None

    bot.mcm_decision_episode = dict(episode or {})
    bot.mcm_decision_episode_internal = dict(episode_internal or {})
    return {
        "episode": dict(bot.mcm_decision_episode or {}),
        "episode_internal": dict(bot.mcm_decision_episode_internal or {}),
    }


def refresh_runtime_context_state(
    bot,
    *,
    runtime_result=None,
    decision_tendency="hold",
    timestamp=None,
    market_tick_advanced=True,
    experience_refresher=None,
    active_context_refresher=None,
    active_context_signal_merger=None,
):
    if bot is None:
        return None

    if experience_refresher is not None:
        experience_refresher(
            bot,
            timestamp=timestamp,
            decision_tendency=decision_tendency,
        )

    active_context_trace = dict(getattr(bot, "active_context_trace", {}) or {})
    if active_context_refresher is not None:
        active_context_trace = active_context_refresher(
            active_context_trace,
            bot=bot,
            runtime_result=dict(runtime_result or {}),
            market_tick_advanced=market_tick_advanced,
        )

    active_context_commit = commit_active_context_trace(
        bot,
        active_context_trace,
        signal_merger=active_context_signal_merger,
    )

    return {
        "active_context_trace": dict(active_context_trace or {}),
        "active_context_commit": dict(active_context_commit or {}),
    }
