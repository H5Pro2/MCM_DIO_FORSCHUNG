# ==================================================
# bot_engine/state_initialization.py
# Bot startup state initialization
# ==================================================

def initialize_bot_state(bot, filepath: str, *, csv_feed_cls, exit_engine_cls, trade_value_gate_cls, trade_stats_cls, brain_factory, config):

    bot.feed = csv_feed_cls(filepath)
    bot.exit_engine = exit_engine_cls()
    bot.value_gate = trade_value_gate_cls()
    bot.stats = trade_stats_cls(
        path="debug/trade_stats.json",
        csv_path="debug/trade_equity.csv",
        reset=True,
    )

    bot.position = None
    bot.pending_entry = None
    bot.processed = 0
    bot.current_timestamp = None

    bot.mcm_brain = brain_factory() if bool(getattr(config, "MCM_ENABLED", True)) else None
    bot.mcm_last_state = None
    bot.mcm_last_action = None
    bot.mcm_last_attractor = None
    bot.mcm_snapshot = None
    bot.mcm_pause_left = 0
    bot.field_density = 0.0
    bot.field_stability = 0.0
    bot.regulatory_load = 0.0
    bot.action_capacity = 0.0
    bot.recovery_need = 0.0
    bot.survival_pressure = 0.0

    bot.focus_point = None
    bot.focus_confidence = 0.0
    bot.target_lock = 0.0
    bot.target_drift = 0.0

    bot.entry_expectation = 0.0
    bot.target_expectation = 0.0
    bot.approach_pressure = 0.0
    bot.pressure_release = 0.0
    bot.experience_regulation = 0.0
    bot.reflection_maturity = 0.0
    bot.load_bearing_capacity = 0.0
    bot.protective_width_regulation = 0.0
    bot.protective_courage = 0.0

    bot.signature_memory = {}
    bot.last_signature_key = None
    bot.last_signature_outcome = None
    bot.last_signature_context = None

    bot.context_clusters = {}
    bot.context_cluster_seq = 0
    bot.last_context_cluster_id = None
    bot.last_context_cluster_key = None

    bot.inner_context_clusters = {}
    bot.inner_context_cluster_seq = 0
    bot.last_inner_context_cluster_id = None
    bot.last_inner_context_cluster_key = None

    bot.inhibition_level = 0.0
    bot.habituation_level = 0.0
    bot.competition_bias = 0.0
    bot.observation_mode = False
    bot.last_signal_relevance = 0.0

    bot.tension_state = {}
    bot.visual_market_state = {}
    bot.structure_perception_state = {}
    bot.temporal_perception_state = {}
    bot.outer_market_state = {}
    bot.perception_state = {}
    bot.outer_visual_perception_state = {}
    bot.inner_field_perception_state = {}
    bot.processing_state = {}
    bot.expectation_state = {}
    bot.felt_state = {}
    bot.thought_state = {}
    bot.meta_regulation_state = {}
    bot.mcm_possibility_field_state = {}
    bot.action_intent_state = {}
    bot.execution_state = {}
    bot.last_outcome_decomposition = {}
    bot.mcm_thought_memory = {}
    bot.mcm_thought_family_memory = {}
    bot.mcm_form_mcm_family_memory = {}
    bot.mcm_thought_memory_summary = {}
    bot._thought_memory_loaded = False
    bot._thought_memory_dirty = False
    bot._thought_memory_updates = 0
    bot._thought_memory_last_save_ts = 0.0

    bot.mcm_runtime_snapshot = {}
    bot.mcm_runtime_decision_state = {}
    bot.mcm_runtime_brain_snapshot = {}
    bot.mcm_runtime_market_ticks = 0
    bot.world_published_ticks = 0
    bot.world_missed_ticks = 0
    bot.cognitive_lag_pressure = 0.0
    bot.last_cognitive_lag_state = {}
    bot.world_motion_afterimage_state = {}
    bot.mcm_episode_seq = 0
    bot.mcm_decision_episode = {}
    bot.mcm_decision_episode_internal = {}
    bot.mcm_experience_space = {}
    bot.mcm_last_observe_timestamp = None
    bot.mcm_runtime = None
    return True
