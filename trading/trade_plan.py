"""Trade plan derivation.

This module is a transitional action adapter. It computes entry, stop and
target candidates from real form/contact proximity in the current DIO brain
state. It does not execute orders and does not treat hypotheses as reality.
"""

from config import Config
from core.mcm_field import _resolve_affective_context_modulation


def derive_trade_plan_from_brain(
    side,
    candle_state,
    fused,
    stimulus,
    snapshot,
    bot=None,
    strategic_window_state=None,
    form_symbol_state=None,
    thought_state=None,
):

    decision = str(side or "").upper().strip()
    if decision not in ("LONG", "SHORT"):
        return None

    candle = dict(candle_state or {})
    fused_state = dict(fused or {})
    stimulus_state = dict(stimulus or {})
    snapshot_state = dict(snapshot or {})

    open_price = float(candle.get("open", 0.0) or 0.0)
    high_price = float(candle.get("high", open_price) or open_price)
    low_price = float(candle.get("low", open_price) or open_price)
    close_price = float(candle.get("close", open_price) or open_price)

    if close_price <= 0.0:
        return None

    candle_span = max(high_price - low_price, close_price * 0.0005, 1e-9)
    base_move = max(candle_span, close_price * 0.0012)

    focus = dict(stimulus_state.get("focus", {}) or {})
    filtered_vision = dict(stimulus_state.get("filtered_vision", {}) or {})

    focus_direction = float(focus.get("focus_direction", 0.0) or 0.0)
    focus_confidence = float(focus.get("focus_confidence", 0.0) or 0.0)
    target_lock = float(focus.get("target_lock", 0.0) or 0.0)
    signal_relevance = float(focus.get("signal_relevance", 0.0) or 0.0)
    noise_damp = float(focus.get("noise_damp", 0.0) or 0.0)

    filtered_target_map = float(filtered_vision.get("target_map", 0.0) or 0.0)
    filtered_threat_map = float(filtered_vision.get("threat_map", 0.0) or 0.0)
    filtered_optic_flow = float(filtered_vision.get("optic_flow", 0.0) or 0.0)

    target_drift = float(getattr(bot, "target_drift", 0.0) or 0.0) if bot is not None else 0.0
    load_bearing_capacity = float(getattr(bot, "load_bearing_capacity", 0.0) or 0.0) if bot is not None else 0.0
    protective_width_regulation = float(getattr(bot, "protective_width_regulation", 0.0) or 0.0) if bot is not None else 0.0
    protective_courage = float(getattr(bot, "protective_courage", 0.0) or 0.0) if bot is not None else 0.0
    inhibition_level = float(fused_state.get("inhibition_level", 0.0) or 0.0)
    habituation_level = float(fused_state.get("habituation_level", 0.0) or 0.0)
    competition_bias = float(fused_state.get("competition_bias", 0.0) or 0.0)
    context_cluster_bias = float(fused_state.get("context_cluster_bias", 0.0) or 0.0)
    context_cluster_quality = float(fused_state.get("context_cluster_quality", 0.0) or 0.0)
    signature_bias = float(fused_state.get("signature_bias", 0.0) or 0.0)
    signature_quality = float(fused_state.get("signature_quality", 0.0) or 0.0)
    long_score = float(fused_state.get("long_score", 0.0) or 0.0)
    short_score = float(fused_state.get("short_score", 0.0) or 0.0)
    self_state = str(snapshot_state.get("self_state", "stable") or "stable")

    affective = _resolve_affective_context_modulation(
        bot=bot,
        fused_state=dict(fused_state or {}),
    )
    felt_bearing_score = float(affective.get("felt_bearing_score", 0.0) or 0.0)
    felt_profile_label = str(affective.get("felt_profile_label", "mixed_unclear") or "mixed_unclear")
    conviction_boost = float(affective.get("conviction_boost", 0.0) or 0.0)
    caution_penalty = float(affective.get("caution_penalty", 0.0) or 0.0)
    volatility_penalty = float(affective.get("volatility_penalty", 0.0) or 0.0)
    risk_shift = float(affective.get("risk_shift", 0.0) or 0.0)
    rr_shift = float(affective.get("rr_shift", 0.0) or 0.0)
    width_shift = float(affective.get("width_shift", 0.0) or 0.0)

    directional_score = long_score if decision == "LONG" else short_score
    directional_competition = max(0.0, competition_bias) if decision == "LONG" else max(0.0, -competition_bias)
    entry_pull = max(0.0, abs(target_drift)) * 0.35 + max(0.0, abs(focus_direction)) * 0.18 + max(0.0, filtered_optic_flow) * 0.08
    entry_shift = min(base_move * 0.55, base_move * entry_pull)

    if decision == "LONG":
        impulse_entry_price = float(close_price - entry_shift)
        validity_center = impulse_entry_price + min(entry_shift * 0.35, base_move * 0.15)
    else:
        impulse_entry_price = float(close_price + entry_shift)
        validity_center = impulse_entry_price - min(entry_shift * 0.35, base_move * 0.15)

    entry_price = 0.0
    contact_entry_price = 0.0
    contact_entry_weight = 0.0
    contact_entry_fit = 0.0
    area_contact_weight = 0.0
    area_contact_fit = 0.0
    area_contact_intention = 0.0
    area_contact_distance_fit = 0.0
    impulse_perception_pressure = 0.0
    area_order_geometry_intention = 0.0
    legacy_entry_pressure_alias = 0.0
    entry_contact_bearing = 0.0
    area_contact_readiness = 0.0
    area_contact_restraint = 0.0
    entry_geometry_bearing = 0.0
    entry_geometry_state = "contact_offer_only"
    entry_geometry_pressures = {"contact_offer_only": 1.0}
    area_contact_acceptance_pressure = 0.0
    area_contact_restraint_pressure = 1.0
    thought_seed_bearing = 0.0
    thought_state_bearing = 0.0
    thought_state_carrier_factor = 0.0
    thought_contact_bearing = 0.0
    pre_geometry_thought_bearing = 0.0
    pre_geometry_felt_bearing = 0.0
    pre_geometry_reality_bearing = 0.0
    pre_geometry_preference_bearing = 0.0
    organic_contact_bearing = 0.0
    area_contact_pull = 0.0
    area_contact_timing_fit = 0.0
    area_bearing_quality = 0.0
    area_replay_fit = 0.0
    area_patience_quality = 0.0
    area_invalidity_pressure = 0.0
    area_action_timing_fit = 0.0
    area_spacetime_fit = 0.0
    area_present_contact = 0.0
    area_afterimage = 0.0
    area_temporal_relevance = 0.0
    entry_contact_choice_state = "no_mature_entry_thesis"
    contact_entry_mode = "no_mature_entry_thesis"
    entry_contact_state = "no_mature_entry_thesis"
    entry_preference_state = "no_entry_preference"
    entry_preference_pressures = {"no_entry_preference": 1.0}
    entry_choice_basis = "no_contact_offer"
    entry_contact_options = []
    entry_contact_option_count = 0
    selected_entry_offer_score = 0.0
    selected_entry_learned_fit = 0.0
    selected_entry_preference_key = "-"
    selected_entry_preference_trust = 0.0
    selected_entry_preference_caution = 0.0
    selected_entry_preference_maturity = 0.0
    selected_entry_preference_utility = 0.0
    selected_entry_property_profile_id = "-"
    selected_entry_property_profile_similarity = 0.0
    selected_entry_property_profile_trust = 0.0
    selected_entry_property_profile_caution = 0.0
    selected_entry_property_profile_maturity = 0.0
    selected_entry_property_profile_utility = 0.0
    selected_memory_caution_pressure = 0.0
    selected_memory_bearing_pressure = 0.0
    mature_careful_contact_pressure = 0.0
    area_contact_focus_id = "-"
    area_contact_low = 0.0
    area_contact_high = 0.0
    area_contact_location = "no_mature_entry_thesis"
    hypothesis_reality_modulation = 0.0
    hypothesis_reality_bearing = 0.0
    hypothesis_reality_binding = 0.0
    hypothesis_reality_binding_gap = 0.0
    hypothesis_reality_binding_state = "hypothesis_reality_unread"
    hypothesis_reality_binding_pressures = {"hypothesis_reality_unread": 1.0}
    visual_reality_bearing = 0.0
    felt_reality_bearing = 0.0
    thought_reality_bearing = 0.0
    form_mcm_reality_fit = 0.0
    uncoupled_area_contact_pressure = 0.0
    hypothesis_observation_pressure = 0.0
    open_hypothesis_reality_bearing = 0.0
    open_hypothesis_reality_fit = 0.0
    open_hypothesis_reality_permission = 0.0
    open_structure_contact_maturity = 1.0
    receptive_contact_offer_pressure = 0.0
    receptive_contact_maturity = 1.0
    receptive_contact_immaturity_pressure = 0.0
    receptive_contact_restraint = 0.0
    hypothesis_contact_restraint = 0.0
    hypothesis_reality_state = "hypothesis_context_unread"
    pre_entry_emergent_structure_reading = 0.0
    pre_entry_emergent_structure_confirmation = 0.0
    pre_entry_emergent_structure_state = "ordinary_structure_contact"

    strategic_window = dict(strategic_window_state or {})
    if not strategic_window and bot is not None:
        strategic_window = dict(getattr(bot, "strategic_window_state", {}) or {})
    form_symbol = dict(form_symbol_state or {})
    if not form_symbol and bot is not None:
        form_symbol = dict(getattr(bot, "form_symbol_state", {}) or {})
    meta = dict(getattr(bot, "meta_regulation_state", {}) or {}) if bot is not None else {}
    thought_seed = dict(getattr(bot, "mcm_thought_seed_state", {}) or {}) if bot is not None else {}
    thought = dict(thought_state or {})
    entry_preference_memory = dict(getattr(bot, "entry_contact_preference_memory", {}) or {}) if bot is not None else {}
    entry_preference_styles = dict(entry_preference_memory.get("styles", {}) or {}) if isinstance(entry_preference_memory, dict) else {}
    entry_property_profiles = list(entry_preference_memory.get("property_profiles", []) or []) if isinstance(entry_preference_memory, dict) else []

    def _clip(value, lo=0.0, hi=1.0):
        try:
            value = float(value)
        except Exception:
            value = 0.0
        if value != value:
            value = 0.0
        return max(float(lo), min(float(hi), float(value)))

    contact_maturity = _clip(form_symbol.get("form_symbol_contact_maturity", 0.0))
    contact_utility = _clip(form_symbol.get("form_symbol_contact_utility", 0.0))
    contact_burden = _clip(form_symbol.get("form_symbol_contact_burden_evidence", 0.0))
    contact_carefulness = _clip(form_symbol.get("form_symbol_contact_carefulness", 0.0))
    contact_utility_evidence = _clip(form_symbol.get("form_symbol_contact_utility_evidence", 0.0))
    contact_learning_state = str(form_symbol.get("form_symbol_contact_learning_state", "unformed_contact") or "unformed_contact")
    learned_contact_fit = _clip(
        (contact_maturity * 0.30)
        + (contact_utility * 0.26)
        + (contact_utility_evidence * 0.16)
        - (contact_burden * 0.20)
        - (contact_carefulness * max(0.0, 0.36 - contact_maturity) * 0.10)
    )

    def _entry_contact_preference_for(side: str, location: str) -> dict:
        side = str(side or "-").upper().strip() or "-"
        location = str(location or "-").strip() or "-"
        legacy_return_word = "pull" + "back"
        legacy_location_aliases = {
            "long_return_area_upper_contact": f"long_{legacy_return_word}_area_upper_contact",
            "short_return_area_lower_contact": f"short_{legacy_return_word}_area_lower_contact",
        }
        legacy_location = legacy_location_aliases.get(location, "")
        keys = [f"{side}|{location}", f"-|{location}"]
        if legacy_location:
            keys.extend([f"{side}|{legacy_location}", f"-|{legacy_location}"])
        for key in keys:
            value = entry_preference_styles.get(key, {})
            if isinstance(value, dict) and value:
                return dict(value)
        return {}

    def _entry_property_profile_for(side: str, features: dict) -> dict:
        side = str(side or "-").upper().strip() or "-"
        feature_map = {str(key): _clip(value) for key, value in dict(features or {}).items()}
        best_profile = {}
        best_bearing = 0.0
        for raw_profile in entry_property_profiles:
            if not isinstance(raw_profile, dict):
                continue
            profile_side = str(raw_profile.get("side", "-") or "-").upper().strip() or "-"
            if profile_side not in (side, "-"):
                continue
            profile_features = dict(raw_profile.get("features", {}) or {})
            keys = [key for key in feature_map.keys() if key in profile_features]
            if not keys:
                continue
            distance = sum(
                abs(_clip(feature_map.get(key, 0.0)) - _clip(profile_features.get(key, 0.0)))
                for key in keys
            ) / max(1, len(keys))
            similarity = _clip(1.0 - distance)
            bearing = _clip(
                (similarity * 0.42)
                + (_clip(raw_profile.get("trust", 0.0)) * 0.22)
                + (_clip(raw_profile.get("utility", 0.0)) * 0.18)
                + (_clip(raw_profile.get("maturity", 0.0)) * 0.14)
                - (_clip(raw_profile.get("caution", 0.0)) * 0.22)
            )
            if bearing > best_bearing:
                best_bearing = float(bearing)
                best_profile = dict(raw_profile)
                best_profile["profile_similarity"] = float(similarity)
                best_profile["profile_bearing"] = float(bearing)
        return best_profile

    def _area_offer_from_candidate(candidate):
        candidate = dict(candidate or {})
        cand_low = float(candidate.get("area_price_low", 0.0) or 0.0)
        cand_high = float(candidate.get("area_price_high", 0.0) or 0.0)
        if cand_low <= 0.0 or cand_high <= 0.0 or cand_high < cand_low:
            return None
        cand_mid = float(candidate.get("area_price_mid", (cand_low + cand_high) * 0.50) or ((cand_low + cand_high) * 0.50))
        cand_span = max(1e-9, cand_high - cand_low)
        cand_contains = bool(cand_low <= close_price <= cand_high)
        if decision == "LONG":
            cand_directional_fit = _clip((close_price - cand_mid) / max(base_move * 3.4, cand_span, 1e-9))
            cand_side_fit = max(cand_directional_fit, 0.34 if cand_contains else 0.0)
            if close_price > cand_high:
                cand_anchor = cand_high - cand_span * 0.18
                cand_location = "long_return_area_upper_contact"
            elif cand_contains:
                cand_anchor = min(cand_mid, close_price - cand_span * 0.10)
                cand_anchor = max(cand_low + cand_span * 0.20, cand_anchor)
                cand_location = "long_inside_area_inner_contact"
            else:
                cand_anchor = cand_low + cand_span * 0.18
                cand_location = "long_forward_area_contact"
        else:
            cand_directional_fit = _clip((cand_mid - close_price) / max(base_move * 3.4, cand_span, 1e-9))
            cand_side_fit = max(cand_directional_fit, 0.34 if cand_contains else 0.0)
            if close_price < cand_low:
                cand_anchor = cand_low + cand_span * 0.18
                cand_location = "short_return_area_lower_contact"
            elif cand_contains:
                cand_anchor = max(cand_mid, close_price + cand_span * 0.10)
                cand_anchor = min(cand_high - cand_span * 0.20, cand_anchor)
                cand_location = "short_inside_area_inner_contact"
            else:
                cand_anchor = cand_high - cand_span * 0.18
                cand_location = "short_forward_area_contact"

        if cand_anchor <= 0.0:
            return None

        cand_preference = _entry_contact_preference_for(decision, cand_location)
        cand_preference_key = str(cand_preference.get("key", f"{decision}|{cand_location}") or f"{decision}|{cand_location}")
        cand_preference_trust = _clip(cand_preference.get("trust", 0.0))
        cand_preference_caution = _clip(cand_preference.get("caution", 0.0))
        cand_preference_maturity = _clip(cand_preference.get("maturity", 0.0))
        cand_preference_utility = _clip(cand_preference.get("utility", 0.0))
        cand_preference_fit = _clip(
            (cand_preference_trust * 0.34)
            + (cand_preference_utility * 0.28)
            + (cand_preference_maturity * 0.24)
            - (cand_preference_caution * 0.30)
        )

        cand_anchor_distance = abs(cand_anchor - close_price)
        cand_distance_fit = _clip(1.0 - (cand_anchor_distance / max(base_move * 3.8, cand_span * 1.6, 1e-9)))
        cand_contact_pull = _clip(candidate.get("area_contact_pull", candidate.get("area_order_intention", 0.0)))
        cand_contact_timing_fit = _clip(candidate.get("area_contact_timing_fit", candidate.get("area_action_timing_fit", 0.0)))
        cand_bearing_quality = _clip(candidate.get("area_bearing_quality", 0.0))
        cand_replay_fit = _clip(candidate.get("area_replay_fit", 0.0))
        cand_present_contact = _clip(candidate.get("area_present_contact", 0.0))
        cand_spacetime_fit = _clip(candidate.get("area_spacetime_fit", 0.0))
        cand_invalidity = _clip(candidate.get("area_invalidity_pressure", 0.0))
        cand_afterimage = _clip(candidate.get("area_afterimage", 0.0))
        cand_patience = _clip(candidate.get("area_patience_quality", 0.0))
        cand_temporal_relevance = _clip(candidate.get("area_temporal_relevance", 0.0))
        cand_area_intention = _clip(
            (cand_contact_pull * 0.20)
            + (cand_bearing_quality * 0.17)
            + (cand_contact_timing_fit * 0.14)
            + (cand_spacetime_fit * 0.12)
            + (cand_replay_fit * 0.10)
            + (cand_present_contact * 0.08)
            + (learned_contact_fit * 0.10)
            + (cand_preference_fit * 0.08)
            + (cand_side_fit * 0.07)
            + (cand_distance_fit * 0.06)
            - (cand_preference_caution * max(0.0, 0.42 - cand_preference_maturity) * 0.08)
            - (cand_invalidity * 0.16)
            - (cand_afterimage * 0.08)
        )
        cand_entry_fit = _clip(
            (cand_contact_pull * 0.20)
            + (cand_bearing_quality * 0.18)
            + (cand_replay_fit * 0.12)
            + (cand_patience * 0.08)
            + (cand_contact_timing_fit * 0.16)
            + (cand_present_contact * 0.09)
            + (cand_temporal_relevance * 0.06)
            + (learned_contact_fit * 0.16)
            + (cand_preference_fit * 0.10)
            + (cand_side_fit * 0.12)
            + (cand_distance_fit * 0.08)
            - (cand_preference_caution * max(0.0, 0.42 - cand_preference_maturity) * 0.10)
            - (cand_invalidity * 0.20)
            - (cand_afterimage * 0.10)
        )
        cand_property_profile = _entry_property_profile_for(
            decision,
            {
                "area_bearing_quality": cand_bearing_quality,
                "area_contact_timing_fit": cand_contact_timing_fit,
                "area_spacetime_fit": cand_spacetime_fit,
                "area_present_contact": cand_present_contact,
                "area_invalidity_pressure": cand_invalidity,
                "area_afterimage": cand_afterimage,
                "area_contact_distance_fit": cand_distance_fit,
                "contact_entry_fit": cand_entry_fit,
                "entry_contact_bearing": cand_bearing_quality,
                "area_contact_readiness": cand_contact_pull,
                "receptive_contact_maturity": contact_maturity,
                "receptive_contact_immaturity_pressure": 1.0 - contact_maturity,
                "visual_reality_bearing": cand_bearing_quality,
                "real_area_contact_bearing": cand_bearing_quality,
                "felt_reality_bearing": contact_utility,
                "form_mcm_reality_fit": learned_contact_fit,
                "energy_coherence_bearing": cand_contact_timing_fit,
                "structure_quality": cand_bearing_quality,
                "process_quality": cand_preference_utility,
                "position_consequence_burden": cand_preference_caution,
                "position_constructive_bearing": cand_preference_trust,
            },
        )
        cand_property_profile_id = str(cand_property_profile.get("profile_id", "-") or "-")
        cand_property_similarity = _clip(cand_property_profile.get("profile_similarity", 0.0))
        cand_property_bearing = _clip(cand_property_profile.get("profile_bearing", 0.0))
        cand_property_trust = _clip(cand_property_profile.get("trust", 0.0))
        cand_property_caution = _clip(cand_property_profile.get("caution", 0.0))
        cand_property_maturity = _clip(cand_property_profile.get("maturity", 0.0))
        cand_property_utility = _clip(cand_property_profile.get("utility", 0.0))
        cand_preference_score = _clip(
            (cand_entry_fit * 0.30)
            + (cand_area_intention * 0.20)
            + (cand_bearing_quality * 0.14)
            + (learned_contact_fit * 0.14)
            + (cand_preference_fit * 0.14)
            + (cand_property_bearing * 0.14)
            + (cand_property_trust * 0.06)
            + (cand_property_utility * 0.06)
            + (cand_spacetime_fit * 0.08)
            + (cand_distance_fit * 0.08)
            + (cand_present_contact * 0.06)
            - (cand_preference_caution * max(0.0, 0.42 - cand_preference_maturity) * 0.10)
            - (cand_property_caution * max(0.0, 0.42 - cand_property_maturity) * 0.08)
            - (cand_invalidity * 0.16)
            - (cand_afterimage * 0.08)
        )
        offer = dict(candidate)
        offer.update(
            {
                "entry_offer_price": float(cand_anchor),
                "entry_offer_location": str(cand_location),
                "entry_offer_side_fit": float(cand_side_fit),
                "entry_offer_distance_fit": float(cand_distance_fit),
                "entry_offer_intention": float(cand_area_intention),
                "entry_offer_fit": float(cand_entry_fit),
                "entry_offer_preference": float(cand_preference_score),
                "entry_offer_learned_fit": float(learned_contact_fit),
                "entry_preference_key": str(cand_preference_key),
                "entry_preference_trust": float(cand_preference_trust),
                "entry_preference_caution": float(cand_preference_caution),
                "entry_preference_maturity": float(cand_preference_maturity),
                "entry_preference_utility": float(cand_preference_utility),
                "entry_preference_fit": float(cand_preference_fit),
                "entry_property_profile_id": str(cand_property_profile_id),
                "entry_property_profile_similarity": float(cand_property_similarity),
                "entry_property_profile_bearing": float(cand_property_bearing),
                "entry_property_profile_trust": float(cand_property_trust),
                "entry_property_profile_caution": float(cand_property_caution),
                "entry_property_profile_maturity": float(cand_property_maturity),
                "entry_property_profile_utility": float(cand_property_utility),
            }
        )
        return offer

    selected_strategic_area = dict(strategic_window or {})
    raw_candidate_pool = list(strategic_window.get("area_focus_candidates", []) or []) if isinstance(strategic_window.get("area_focus_candidates", []), list) else []
    candidate_pool = list(raw_candidate_pool)
    if selected_strategic_area:
        candidate_pool.append(dict(selected_strategic_area))
    seen_offer_keys = set()
    for raw_candidate in candidate_pool:
        offer = _area_offer_from_candidate(raw_candidate)
        if not offer:
            continue
        offer_key = (
            round(float(offer.get("area_price_low", 0.0) or 0.0), 8),
            round(float(offer.get("area_price_high", 0.0) or 0.0), 8),
            str(offer.get("entry_offer_location", "")),
        )
        if offer_key in seen_offer_keys:
            continue
        seen_offer_keys.add(offer_key)
        entry_contact_options.append(offer)
    entry_contact_options.sort(key=lambda item: float(item.get("entry_offer_preference", 0.0) or 0.0), reverse=True)
    entry_contact_option_count = len(entry_contact_options)
    if entry_contact_options:
        selected_strategic_area = dict(entry_contact_options[0])
        selected_entry_offer_score = float(selected_strategic_area.get("entry_offer_preference", 0.0) or 0.0)
        selected_entry_learned_fit = float(selected_strategic_area.get("entry_offer_learned_fit", learned_contact_fit) or 0.0)
        selected_entry_preference_key = str(selected_strategic_area.get("entry_preference_key", "-") or "-")
        selected_entry_preference_trust = float(selected_strategic_area.get("entry_preference_trust", 0.0) or 0.0)
        selected_entry_preference_caution = float(selected_strategic_area.get("entry_preference_caution", 0.0) or 0.0)
        selected_entry_preference_maturity = float(selected_strategic_area.get("entry_preference_maturity", 0.0) or 0.0)
        selected_entry_preference_utility = float(selected_strategic_area.get("entry_preference_utility", 0.0) or 0.0)
        selected_entry_property_profile_id = str(selected_strategic_area.get("entry_property_profile_id", "-") or "-")
        selected_entry_property_profile_similarity = float(selected_strategic_area.get("entry_property_profile_similarity", 0.0) or 0.0)
        selected_entry_property_profile_trust = float(selected_strategic_area.get("entry_property_profile_trust", 0.0) or 0.0)
        selected_entry_property_profile_caution = float(selected_strategic_area.get("entry_property_profile_caution", 0.0) or 0.0)
        selected_entry_property_profile_maturity = float(selected_strategic_area.get("entry_property_profile_maturity", 0.0) or 0.0)
        selected_entry_property_profile_utility = float(selected_strategic_area.get("entry_property_profile_utility", 0.0) or 0.0)
        entry_choice_basis = "learned_multisensory_contact_offer"
        selected_preference_fit = _clip(
            (selected_entry_preference_trust * 0.34)
            + (selected_entry_preference_utility * 0.28)
            + (selected_entry_preference_maturity * 0.24)
            - (selected_entry_preference_caution * 0.30)
        )
        selected_property_fit = _clip(
            (selected_entry_property_profile_similarity * 0.30)
            + (selected_entry_property_profile_trust * 0.24)
            + (selected_entry_property_profile_utility * 0.20)
            + (selected_entry_property_profile_maturity * 0.16)
            - (selected_entry_property_profile_caution * 0.24)
        )
        selected_memory_caution_pressure = _clip(
            (selected_entry_preference_caution * 0.36)
            + (selected_entry_property_profile_caution * 0.36)
            + (max(0.0, selected_entry_preference_caution - selected_entry_preference_trust) * 0.18)
            + (max(0.0, selected_entry_property_profile_caution - selected_entry_property_profile_trust) * 0.18)
        )
        selected_memory_bearing_pressure = _clip(
            (selected_entry_preference_trust * 0.30)
            + (selected_entry_property_profile_trust * 0.30)
            + (selected_entry_preference_utility * 0.18)
            + (selected_entry_property_profile_utility * 0.18)
            + (selected_entry_learned_fit * 0.10)
            - (selected_memory_caution_pressure * 0.20)
        )
        mature_careful_contact_pressure = _clip(
            (selected_memory_caution_pressure * 0.46)
            + (selected_entry_preference_maturity * selected_entry_preference_caution * 0.20)
            + (selected_entry_property_profile_maturity * selected_entry_property_profile_caution * 0.20)
            - (selected_memory_bearing_pressure * 0.20)
        )
        entry_preference_pressures = {
            "learned_contact_preference": _clip(
                (selected_entry_learned_fit * 0.28)
                + (selected_preference_fit * 0.28)
                + (selected_property_fit * 0.16)
                + (selected_entry_offer_score * 0.24)
                + (selected_entry_preference_trust * 0.12)
                - (selected_entry_preference_caution * 0.18)
                - (mature_careful_contact_pressure * 0.14)
            ),
            "forming_contact_preference": _clip(
                (selected_entry_offer_score * 0.30)
                + (selected_preference_fit * 0.18)
                + (selected_property_fit * 0.12)
                + (selected_entry_preference_maturity * 0.12)
                + (selected_entry_preference_utility * 0.10)
                - (selected_entry_preference_caution * 0.10)
                - (mature_careful_contact_pressure * 0.08)
            ),
            "weak_contact_preference": _clip(
                ((1.0 - selected_entry_offer_score) * 0.18)
                + (selected_entry_preference_caution * 0.18)
                + (selected_entry_property_profile_caution * 0.12)
                + ((1.0 - selected_preference_fit) * 0.10)
                + (mature_careful_contact_pressure * 0.20)
            ),
        }
        entry_preference_state = max(entry_preference_pressures, key=entry_preference_pressures.get)

    area_low = float(selected_strategic_area.get("area_price_low", 0.0) or 0.0)
    area_high = float(selected_strategic_area.get("area_price_high", 0.0) or 0.0)
    if area_low > 0.0 and area_high > 0.0 and area_high >= area_low:
        area_mid = float(selected_strategic_area.get("area_price_mid", (area_low + area_high) * 0.50) or ((area_low + area_high) * 0.50))
        area_span = max(1e-9, area_high - area_low)
        area_contact_pull = _clip(selected_strategic_area.get("area_contact_pull", selected_strategic_area.get("area_order_intention", 0.0)))
        area_order_intention = float(area_contact_pull)
        area_bearing_quality = _clip(selected_strategic_area.get("area_bearing_quality", 0.0))
        area_replay_fit = _clip(selected_strategic_area.get("area_replay_fit", 0.0))
        area_patience_quality = _clip(selected_strategic_area.get("area_patience_quality", 0.0))
        area_invalidity_pressure = _clip(selected_strategic_area.get("area_invalidity_pressure", 0.0))
        area_contact_timing_fit = _clip(selected_strategic_area.get("area_contact_timing_fit", selected_strategic_area.get("area_action_timing_fit", 0.0)))
        area_action_timing_fit = float(area_contact_timing_fit)
        area_spacetime_fit = _clip(selected_strategic_area.get("area_spacetime_fit", 0.0))
        area_present_contact = _clip(selected_strategic_area.get("area_present_contact", 0.0))
        area_afterimage = _clip(selected_strategic_area.get("area_afterimage", 0.0))
        area_temporal_relevance = _clip(selected_strategic_area.get("area_temporal_relevance", 0.0))
        contact_fit = _clip((contact_maturity * 0.28) + (contact_utility * 0.32) + (contact_utility_evidence * 0.10) + (area_replay_fit * 0.20) + (area_patience_quality * 0.20) - (contact_burden * 0.18))
        area_contains_price = bool(area_low <= close_price <= area_high)
        if decision == "LONG":
            directional_fit = _clip((close_price - area_mid) / max(base_move * 3.4, area_span, 1e-9))
            containment_fit = 0.34 if area_contains_price else 0.0
            side_fit = max(directional_fit, containment_fit)
            if close_price > area_high:
                contact_anchor = area_high - area_span * 0.18
                area_contact_location = "long_return_area_upper_contact"
            elif area_contains_price:
                contact_anchor = min(area_mid, close_price - area_span * 0.10)
                contact_anchor = max(area_low + area_span * 0.20, contact_anchor)
                area_contact_location = "long_inside_area_inner_contact"
            else:
                contact_anchor = area_low + area_span * 0.18
                area_contact_location = "long_forward_area_contact"
        else:
            directional_fit = _clip((area_mid - close_price) / max(base_move * 3.4, area_span, 1e-9))
            containment_fit = 0.34 if area_contains_price else 0.0
            side_fit = max(directional_fit, containment_fit)
            if close_price < area_low:
                contact_anchor = area_low + area_span * 0.18
                area_contact_location = "short_return_area_lower_contact"
            elif area_contains_price:
                contact_anchor = max(area_mid, close_price + area_span * 0.10)
                contact_anchor = min(area_high - area_span * 0.20, contact_anchor)
                area_contact_location = "short_inside_area_inner_contact"
            else:
                contact_anchor = area_high - area_span * 0.18
                area_contact_location = "short_forward_area_contact"
        anchor_distance = abs(contact_anchor - close_price)
        anchor_distance_fit = _clip(1.0 - (anchor_distance / max(base_move * 3.8, area_span * 1.6, 1e-9)))
        area_contact_distance_fit = float(anchor_distance_fit)
        area_contact_intention = _clip(
            (area_order_intention * 0.22)
            + (area_bearing_quality * 0.18)
            + (area_contact_timing_fit * 0.16)
            + (area_spacetime_fit * 0.12)
            + (area_replay_fit * 0.10)
            + (area_present_contact * 0.08)
            + (contact_fit * 0.10)
            + (side_fit * 0.08)
            + (anchor_distance_fit * 0.06)
            - (area_invalidity_pressure * 0.16)
            - (area_afterimage * 0.08)
        )
        impulse_perception_pressure = _clip(
            (abs(focus_direction) * 0.20)
            + (focus_confidence * 0.16)
            + (target_lock * 0.16)
            + (filtered_optic_flow * 0.12)
            + (directional_competition * 0.10)
            + (max(0.0, directional_score) * 0.10)
            + (conviction_boost * 0.10)
            - (caution_penalty * 0.12)
            - (volatility_penalty * 0.08)
        )
        area_order_geometry_intention = _clip(
            (area_contact_intention * 0.34)
            + (area_order_intention * 0.16)
            + (area_bearing_quality * 0.14)
            + (area_spacetime_fit * 0.10)
            + (area_replay_fit * 0.10)
            + (anchor_distance_fit * 0.10)
            + (contact_fit * 0.08)
            - (area_invalidity_pressure * 0.12)
            - (area_afterimage * 0.06)
        )
        # Legacy pressure fields are kept neutral. Impulse pressure is a sensory
        # diagnostic only; entry geometry must come from real area/contact fit.
        legacy_entry_pressure_alias = 0.0
        entry_contact_bearing = _clip(
            (area_order_geometry_intention * 0.28)
            + (area_bearing_quality * 0.18)
            + (area_spacetime_fit * 0.14)
            + (area_contact_distance_fit * 0.12)
            + (contact_fit * 0.12)
            + (area_contact_timing_fit * 0.10)
            - (area_invalidity_pressure * 0.14)
            - (area_afterimage * 0.08)
        )
        area_contact_readiness = _clip(
            (area_order_geometry_intention * 0.22)
            + (entry_contact_bearing * 0.20)
            + (contact_fit * 0.18)
            + (area_contact_timing_fit * 0.14)
            + (area_spacetime_fit * 0.10)
            + (area_contact_distance_fit * 0.08)
            - (area_invalidity_pressure * 0.14)
            - (area_afterimage * 0.08)
        )
        area_contact_restraint = _clip(
            (contact_carefulness * max(0.0, 0.42 - contact_maturity) * 0.20)
            + (area_invalidity_pressure * 0.16)
            + (area_afterimage * 0.12)
            + (max(0.0, 0.34 - area_contact_readiness) * 0.20)
        )

        emergent_structure_state = str(thought_seed.get("emergent_structure_state", "") or "").strip()
        emergent_structure_aliases = {
            "confirmed_structural_interpretation": "confirmed_structure_contact",
            "open_structural_hypothesis": "open_structure_contact",
            "wide_target_without_structure": "wide_range_without_structure",
            "ordinary_structure_reading": "ordinary_structure_contact",
        }
        emergent_structure_state = emergent_structure_aliases.get(emergent_structure_state, emergent_structure_state)
        previous_open_hypothesis_learning_state = str(meta.get("previous_open_hypothesis_learning_state", "") or "").strip()
        open_hypothesis_reifung_state = str(meta.get("open_hypothesis_reifung_state", "") or "").strip()
        open_hypothesis_confirmation_weight = _clip(meta.get("open_hypothesis_confirmation_weight", 0.0))
        open_hypothesis_reality_bearing = _clip(
            meta.get(
                "open_hypothesis_reality_bearing",
                meta.get("open_hypothesis_reality_fit", meta.get("open_hypothesis_reality_permission", meta.get("open_hypothesis_action_permission", 0.0))),
            )
        )
        open_hypothesis_reality_fit = float(open_hypothesis_reality_bearing)
        open_hypothesis_reality_permission = float(open_hypothesis_reality_bearing)
        open_hypothesis_action_permission = float(open_hypothesis_reality_permission)
        open_hypothesis_reality_check_need = _clip(meta.get("open_hypothesis_reality_check_need", 0.0))
        open_hypothesis_learning_charge = _clip(meta.get("open_hypothesis_learning_charge", 0.0))
        open_hypothesis_motor_tension = _clip(meta.get("open_hypothesis_action_tension", meta.get("open_hypothesis_motor_tension", 0.0)))
        burdened_hypothesis_memory = previous_open_hypothesis_learning_state in (
            "open_hypothesis_burdened",
            "open_hypothesis_reorganizing",
        ) or open_hypothesis_reifung_state == "open_hypothesis_reorganizing_memory"
        carried_hypothesis_memory = previous_open_hypothesis_learning_state == "open_hypothesis_carried" or open_hypothesis_reifung_state == "open_hypothesis_carried_memory"
        confirmed_current_structure = emergent_structure_state == "confirmed_structure_contact"
        open_current_structure = emergent_structure_state == "open_structure_contact"

        if confirmed_current_structure:
            hypothesis_reality_state = "confirmed_structure_contact"
            hypothesis_reality_bearing = _clip(
                0.16
                + (open_hypothesis_confirmation_weight * 0.20)
                + (open_hypothesis_reality_permission * 0.16)
                + (0.10 if carried_hypothesis_memory else 0.0)
            )
        elif open_current_structure:
            hypothesis_reality_state = "open_structure_observation"
            hypothesis_observation_pressure = _clip(
                0.16
                + (max(0.0, 0.44 - open_hypothesis_confirmation_weight) * 0.34)
                + (open_hypothesis_reality_check_need * 0.22)
                + (open_hypothesis_learning_charge * 0.14)
                + (open_hypothesis_motor_tension * 0.12)
                + (0.18 if burdened_hypothesis_memory else 0.0)
                - (0.12 if carried_hypothesis_memory else 0.0)
            )
        else:
            hypothesis_reality_state = "ordinary_structure_contact"
            hypothesis_observation_pressure = _clip(
                (open_hypothesis_reality_check_need * 0.08)
                + (open_hypothesis_learning_charge * 0.06)
                + (0.10 if burdened_hypothesis_memory else 0.0)
            )

        hypothesis_reality_modulation = _clip(hypothesis_reality_bearing - hypothesis_observation_pressure, -1.0, 1.0)
        entry_contact_choice_pressures = {
            "area_contact_preferred": _clip(
                (area_order_geometry_intention * 0.34)
                + (entry_contact_bearing * 0.28)
                + (area_contact_readiness * 0.18)
                + (area_contact_distance_fit * 0.10)
                - (impulse_perception_pressure * 0.08)
                - (area_contact_restraint * 0.12)
            ),
            "area_contact_available": _clip(
                (area_order_geometry_intention * 0.24)
                + (entry_contact_bearing * 0.24)
                + (area_contact_readiness * 0.18)
                + (area_contact_timing_fit * 0.10)
                - (area_invalidity_pressure * 0.10)
            ),
            "area_contact_weak": _clip(
                (area_invalidity_pressure * 0.18)
                + (area_afterimage * 0.14)
                + ((1.0 - entry_contact_bearing) * 0.12)
                + ((1.0 - area_order_geometry_intention) * 0.10)
                + (area_contact_restraint * 0.16)
            ),
        }
        entry_contact_choice_state = max(entry_contact_choice_pressures, key=entry_contact_choice_pressures.get)
        entry_contact_state = str(entry_contact_choice_state)
        contact_entry_fit = _clip(
            (area_order_intention * 0.24)
            + (area_bearing_quality * 0.22)
            + (area_replay_fit * 0.14)
            + (area_patience_quality * 0.10)
            + (area_contact_timing_fit * 0.18)
            + (area_present_contact * 0.10)
            + (area_temporal_relevance * 0.08)
            + (contact_fit * 0.14)
            + (side_fit * 0.14)
            + (anchor_distance_fit * 0.08)
            - (area_invalidity_pressure * 0.22)
            - (area_afterimage * 0.12)
            - (contact_carefulness * max(0.0, 0.38 - contact_maturity) * 0.10)
        )
        area_contact_fit = float(contact_entry_fit)
        thought_seed_bearing = _clip(
            (float(thought_seed.get("thought_confirmation_score", 0.0) or 0.0) * 0.26)
            + (float(thought_seed.get("reality_binding_score", 0.0) or 0.0) * 0.24)
            + (float(thought_seed.get("thought_structural_grounding", 0.0) or 0.0) * 0.22)
            + (float(thought_seed.get("trust_return_readiness", 0.0) or 0.0) * 0.14)
            + (float(thought_seed.get("thought_digestive_returned_trust", 0.0) or 0.0) * 0.08)
            + (float(thought_seed.get("thought_digestive_integration_pull", 0.0) or 0.0) * 0.06)
            - (float(thought_seed.get("thought_open_hypothesis_pressure", 0.0) or 0.0) * 0.12)
            - (float(thought_seed.get("thought_reality_lag", 0.0) or 0.0) * 0.10)
        )
        thought_state_bearing = _clip(
            (float(thought.get("thought_alignment", 0.0) or 0.0) * 0.22)
            + (float(thought.get("decision_readiness", 0.0) or 0.0) * 0.18)
            + (float(thought.get("state_maturity", thought.get("maturity", 0.0)) or 0.0) * 0.16)
            + (float(thought.get("thought_areal_support", 0.0) or 0.0) * 0.16)
            + (float(thought.get("field_perception_clarity", 0.0) or 0.0) * 0.10)
            + (float(thought.get("field_perception_stability", 0.0) or 0.0) * 0.08)
            + (max(0.0, 1.0 - float(thought.get("decision_conflict", thought.get("conflict", 0.0)) or 0.0)) * 0.10)
            - (float(thought.get("thought_areal_pressure", 0.0) or 0.0) * 0.12)
            - (float(thought.get("decision_pressure", 0.0) or 0.0) * 0.08)
        )
        thought_state_carrier_factor = _clip(0.24 + (thought_seed_bearing * 0.46))
        thought_contact_bearing = _clip(
            (thought_seed_bearing * 0.62)
            + (thought_state_bearing * thought_state_carrier_factor)
        )
        if open_current_structure:
            hypothesis_contact_restraint = _clip(
                (hypothesis_observation_pressure * 0.34)
                + (0.10 if burdened_hypothesis_memory else 0.0)
                - (0.12 if carried_hypothesis_memory else 0.0)
            )
        elif not confirmed_current_structure:
            hypothesis_contact_restraint = _clip(hypothesis_observation_pressure * 0.16)
        pre_geometry_thought_bearing = _clip(
            max(
                thought_contact_bearing,
                meta.get(
                    "thought_trust_bearing",
                    meta.get(
                        "thought_confirmation_bearing",
                        meta.get("thought_contact_consent", 0.0),
                    ),
                ),
            )
        )
        pre_geometry_felt_bearing = _clip(
            meta.get(
                "contact_carrying_quality",
                meta.get(
                    "outer_inner_coherence",
                    meta.get("inner_outer_alignment", felt_bearing_score),
                ),
            )
        )
        pre_geometry_reality_bearing = _clip(
            meta.get(
                "real_area_contact_bearing",
                meta.get(
                    "contact_carrying_quality",
                    meta.get("inner_outer_alignment", felt_bearing_score),
                ),
            )
        )
        pre_geometry_preference_bearing = _clip(
            (selected_entry_preference_trust * 0.34)
            + (selected_entry_preference_utility * 0.28)
            + (selected_entry_preference_maturity * 0.24)
            + (selected_entry_learned_fit * 0.12)
            - (selected_entry_preference_caution * 0.30)
        )

        # Soft pre-entry interpretation of the same structure that is later
        # evaluated after TP/SL. This is not an action gate; it lets open
        # hypotheses add contact caution before they become trades.
        pre_entry_emergent_structure_reading = _clip(
            (area_bearing_quality * 0.20)
            + (entry_contact_bearing * 0.18)
            + (area_spacetime_fit * 0.14)
            + (area_replay_fit * 0.12)
            + (area_contact_timing_fit * 0.12)
            + (contact_entry_fit * 0.10)
            + (area_present_contact * 0.08)
            + (area_contact_distance_fit * 0.06)
            - (area_invalidity_pressure * 0.14)
            - (area_afterimage * 0.10)
        )
        pre_entry_emergent_structure_confirmation = _clip(
            (pre_entry_emergent_structure_reading * 0.34)
            + (pre_geometry_reality_bearing * 0.16)
            + (pre_geometry_preference_bearing * 0.12)
            + (contact_maturity * 0.10)
            + (contact_utility_evidence * 0.08)
            - (contact_burden * 0.12)
            - (hypothesis_observation_pressure * 0.10)
        )
        visual_reality_bearing = _clip(
            (area_bearing_quality * 0.20)
            + (area_contact_readiness * 0.18)
            + (area_spacetime_fit * 0.16)
            + (area_present_contact * 0.12)
            + (area_contact_distance_fit * 0.10)
            + (contact_entry_fit * 0.10)
            - (area_invalidity_pressure * 0.14)
            - (area_afterimage * 0.10)
        )
        felt_reality_bearing = _clip(
            (pre_geometry_felt_bearing * 0.34)
            + (contact_maturity * 0.16)
            + (contact_utility * 0.14)
            + (contact_utility_evidence * 0.12)
            + (felt_bearing_score * 0.10)
            - (contact_burden * 0.16)
            - (contact_carefulness * 0.08)
        )
        thought_reality_bearing = _clip(
            (thought_seed_bearing * 0.30)
            + (thought_state_bearing * 0.18)
            + (open_hypothesis_confirmation_weight * 0.16)
            + (open_hypothesis_reality_bearing * 0.14)
            + (pre_entry_emergent_structure_confirmation * 0.12)
            - (open_hypothesis_reality_check_need * 0.10)
            - (open_hypothesis_motor_tension * 0.08)
        )
        thought_motor_bearing = 0.0
        uncoupled_area_contact_pressure = _clip(
            (visual_reality_bearing * (1.0 - felt_reality_bearing) * 0.34)
            + (area_contact_readiness * (1.0 - pre_geometry_reality_bearing) * 0.20)
            + (area_contact_intention * (1.0 - pre_geometry_reality_bearing) * 0.16)
            + (hypothesis_observation_pressure * 0.16)
            + (area_invalidity_pressure * 0.10)
            + (contact_burden * 0.10)
        )
        form_mcm_reality_fit = _clip(
            (min(visual_reality_bearing, felt_reality_bearing) * 0.42)
            + (visual_reality_bearing * 0.18)
            + (felt_reality_bearing * 0.18)
            + (area_contact_timing_fit * 0.10)
            + (area_temporal_relevance * 0.08)
            - (uncoupled_area_contact_pressure * 0.12)
        )
        hypothesis_reality_binding = _clip(
            (visual_reality_bearing * 0.24)
            + (felt_reality_bearing * 0.22)
            + (form_mcm_reality_fit * 0.16)
            + (pre_entry_emergent_structure_confirmation * 0.12)
            - (hypothesis_observation_pressure * 0.12)
            - (hypothesis_contact_restraint * 0.08)
        )
        hypothesis_reality_binding_gap = _clip(
            (abs(visual_reality_bearing - felt_reality_bearing) * 0.32)
            + (hypothesis_observation_pressure * 0.22)
            + (uncoupled_area_contact_pressure * 0.12),
            0.0,
            1.0,
        )
        hypothesis_reality_binding_pressures = {
            "seen_form_mcm_thought_bound": _clip(
                (hypothesis_reality_binding * 0.44)
                + (form_mcm_reality_fit * 0.24)
                - (hypothesis_reality_binding_gap * 0.14)
            ),
            "seen_form_needs_feeling": _clip(
                (visual_reality_bearing * 0.34)
                + (max(0.0, visual_reality_bearing - felt_reality_bearing) * 0.24)
                + (hypothesis_observation_pressure * 0.10)
            ),
            "felt_field_without_clear_form": _clip(
                (felt_reality_bearing * 0.34)
                + (max(0.0, felt_reality_bearing - visual_reality_bearing) * 0.24)
                + (uncoupled_area_contact_pressure * 0.10)
            ),
            "thought_runs_ahead_of_reality": _clip(
                thought_motor_bearing
            ),
            "reality_probe_observes": _clip(
                (hypothesis_reality_binding_gap * 0.34)
                + (hypothesis_observation_pressure * 0.30)
                + ((1.0 - hypothesis_reality_binding) * 0.12)
            ),
        }
        hypothesis_reality_binding_state = max(
            hypothesis_reality_binding_pressures,
            key=hypothesis_reality_binding_pressures.get,
        )
        pre_entry_structure_pressures = {
            "confirmed_structure_contact": _clip(
                (pre_entry_emergent_structure_reading * 0.34)
                + (pre_entry_emergent_structure_confirmation * 0.34)
                + (pre_geometry_reality_bearing * 0.10)
                - (hypothesis_observation_pressure * 0.12)
            ),
            "open_structure_contact": _clip(
                (pre_entry_emergent_structure_reading * 0.28)
                + ((1.0 - pre_entry_emergent_structure_confirmation) * 0.22)
                + (hypothesis_reality_binding_gap * 0.14)
                + (hypothesis_observation_pressure * 0.18)
                + ((1.0 - thought_seed_bearing) * 0.10)
            ),
            "ordinary_structure_contact": _clip(
                (pre_entry_emergent_structure_reading * 0.22)
                + (pre_entry_emergent_structure_confirmation * 0.14)
                + (area_contact_readiness * 0.10)
            ),
            "wide_range_without_structure": _clip(
                ((1.0 - pre_entry_emergent_structure_reading) * 0.22)
                + ((1.0 - pre_entry_emergent_structure_confirmation) * 0.14)
                + (area_invalidity_pressure * 0.10)
            ),
        }
        pre_entry_emergent_structure_state = max(pre_entry_structure_pressures, key=pre_entry_structure_pressures.get)

        if pre_entry_emergent_structure_state == "confirmed_structure_contact":
            confirmed_current_structure = True
            if hypothesis_reality_state == "ordinary_structure_contact":
                hypothesis_reality_state = "pre_entry_confirmed_structure_contact"
            hypothesis_reality_bearing = max(
                hypothesis_reality_bearing,
                _clip(
                    (pre_entry_emergent_structure_confirmation * 0.24)
                    + (pre_entry_emergent_structure_reading * 0.16)
                    + (form_mcm_reality_fit * 0.16)
                ),
            )
        elif pre_entry_emergent_structure_state == "open_structure_contact" and not confirmed_current_structure:
            open_current_structure = True
            hypothesis_reality_state = "pre_entry_open_structure_observation"
            hypothesis_observation_pressure = max(
                hypothesis_observation_pressure,
                _clip(
                    0.10
                    + (pre_entry_emergent_structure_reading * 0.12)
                    + (max(0.0, 0.46 - pre_entry_emergent_structure_confirmation) * 0.30)
                    + (hypothesis_reality_binding_gap * 0.16)
                    + (0.10 if burdened_hypothesis_memory else 0.0)
                    - (0.08 if carried_hypothesis_memory else 0.0)
                ),
            )
        hypothesis_reality_modulation = _clip(hypothesis_reality_bearing - hypothesis_observation_pressure, -1.0, 1.0)
        pre_geometry_reality_bearing = max(pre_geometry_reality_bearing, hypothesis_reality_binding)
        if open_current_structure:
            hypothesis_contact_restraint = max(
                hypothesis_contact_restraint,
                _clip(
                    (hypothesis_observation_pressure * 0.44)
                    + (hypothesis_reality_binding_gap * 0.18)
                    + (0.12 if burdened_hypothesis_memory else 0.0)
                    - (0.10 if carried_hypothesis_memory else 0.0)
                ),
            )
        elif not confirmed_current_structure:
            hypothesis_contact_restraint = max(
                hypothesis_contact_restraint,
                _clip(hypothesis_observation_pressure * 0.18),
            )
        if open_current_structure and not confirmed_current_structure:
            open_structure_contact_maturity = _clip(
                (felt_reality_bearing * 0.32)
                + (form_mcm_reality_fit * 0.28)
                + (pre_geometry_reality_bearing * 0.18)
                + (contact_maturity * 0.12)
                + (contact_utility_evidence * 0.08)
                + (0.08 if carried_hypothesis_memory else 0.0)
                - (0.10 if burdened_hypothesis_memory else 0.0)
            )
            hypothesis_contact_restraint = max(
                hypothesis_contact_restraint,
                _clip(
                    (hypothesis_contact_restraint * 0.72)
                    + ((1.0 - open_structure_contact_maturity) * 0.30)
                    + (hypothesis_reality_binding_gap * 0.12)
                    + (uncoupled_area_contact_pressure * 0.10)
                ),
            )
        else:
            open_structure_contact_maturity = 1.0

        # Hypothesen sind vorerst vollstaendig aus der aktiven Entry-Motorik
        # entfernt. DIO handelt damit wieder aus rezeptivem Kontakt:
        # Sehen, Hoeren, MCM-Fuehlen, reale Bereichsnaehe und Value-Gate.
        # Die Debug-/Kompatibilitaetsfelder bleiben erhalten, tragen aber
        # keine Handlungsnaehe.
        confirmed_current_structure = False
        open_current_structure = False
        hypothesis_reality_state = "hypothesis_disabled_receptive_contact"
        hypothesis_reality_modulation = 0.0
        hypothesis_reality_bearing = 0.0
        hypothesis_reality_binding = 0.0
        hypothesis_reality_binding_gap = 0.0
        hypothesis_reality_binding_state = "hypothesis_disabled"
        hypothesis_reality_binding_pressures = {"hypothesis_disabled": 1.0}
        hypothesis_observation_pressure = 0.0
        hypothesis_contact_restraint = 0.0
        open_hypothesis_reality_bearing = 0.0
        open_hypothesis_reality_fit = 0.0
        open_hypothesis_reality_permission = 0.0
        open_hypothesis_action_permission = 0.0
        open_structure_contact_maturity = 1.0
        thought_seed_bearing = 0.0
        thought_state_bearing = 0.0
        thought_state_carrier_factor = 0.0
        thought_contact_bearing = 0.0
        thought_reality_bearing = 0.0
        thought_motor_bearing = 0.0
        pre_geometry_thought_bearing = 0.0
        pre_entry_emergent_structure_reading = 0.0
        pre_entry_emergent_structure_confirmation = 0.0
        pre_entry_emergent_structure_state = "hypothesis_disabled_receptive_contact"

        receptive_contact_offer_pressure = _clip(
            (area_contact_readiness * 0.24)
            + (entry_contact_bearing * 0.22)
            + (area_contact_intention * 0.18)
            + (contact_entry_fit * 0.12)
            + (area_contact_distance_fit * 0.10)
            + (area_contact_timing_fit * 0.08)
            + (pre_geometry_preference_bearing * 0.06)
        )
        receptive_contact_maturity = _clip(
            (felt_reality_bearing * 0.22)
            + (form_mcm_reality_fit * 0.22)
            + (pre_geometry_reality_bearing * 0.16)
            + (contact_maturity * 0.14)
            + (contact_utility_evidence * 0.10)
            + (area_contact_distance_fit * 0.08)
            + (contact_entry_fit * 0.08)
            - (uncoupled_area_contact_pressure * 0.14)
            - (area_invalidity_pressure * 0.10)
            - (area_afterimage * 0.08)
            - (mature_careful_contact_pressure * 0.22)
        )
        receptive_contact_immaturity_pressure = _clip(
            (receptive_contact_offer_pressure * (1.0 - receptive_contact_maturity) * 0.52)
            + (uncoupled_area_contact_pressure * 0.18)
            + (area_invalidity_pressure * 0.12)
            + (area_afterimage * 0.08)
            + (contact_burden * 0.08)
            + (mature_careful_contact_pressure * 0.26)
            + (selected_memory_caution_pressure * 0.12)
            - (contact_utility_evidence * 0.08)
            - (selected_memory_bearing_pressure * 0.08)
        )
        receptive_contact_restraint = _clip(
            (receptive_contact_immaturity_pressure * 0.58)
            + (uncoupled_area_contact_pressure * 0.16)
            + (area_invalidity_pressure * 0.10)
            + (mature_careful_contact_pressure * 0.22)
            + (selected_memory_caution_pressure * 0.08)
        )

        entry_geometry_bearing = _clip(
            (pre_geometry_felt_bearing * 0.30)
            + (pre_geometry_reality_bearing * 0.26)
            + (pre_geometry_preference_bearing * 0.14)
            + (contact_entry_fit * 0.16)
            + (area_contact_intention * 0.10)
            - (area_contact_restraint * 0.16)
            - (hypothesis_contact_restraint * 0.18)
            - (receptive_contact_restraint * 0.14)
        )
        organic_contact_bearing = _clip(
            (contact_entry_fit * 0.30)
            + (area_contact_intention * 0.24)
            + (area_contact_readiness * 0.20)
            + (entry_contact_bearing * 0.18)
            + (area_contact_timing_fit * 0.08)
            - (area_contact_restraint * 0.18)
            - (hypothesis_contact_restraint * 0.12)
            - (receptive_contact_restraint * 0.12)
        )
        entry_geometry_pressures = {
            "entry_geometry_ready": _clip(
                (entry_geometry_bearing * 0.30)
                + (contact_entry_fit * 0.18)
                + (area_contact_intention * 0.18)
                + (pre_geometry_preference_bearing * 0.14)
                + (area_contact_readiness * 0.12)
                - (area_contact_restraint * 0.16)
                - (hypothesis_contact_restraint * 0.10)
                - (receptive_contact_restraint * 0.10)
            ),
            "entry_geometry_organic_contact": _clip(
                (organic_contact_bearing * 0.30)
                + (contact_entry_fit * 0.20)
                + (area_contact_intention * 0.18)
                + (entry_contact_bearing * 0.12)
                + (area_contact_timing_fit * 0.10)
                - (area_contact_restraint * 0.14)
                - (hypothesis_contact_restraint * 0.08)
                - (receptive_contact_restraint * 0.08)
            ),
            "entry_geometry_forming": _clip(
                (entry_geometry_bearing * 0.20)
                + (entry_contact_bearing * 0.18)
                + (area_contact_readiness * 0.16)
                + (pre_geometry_preference_bearing * 0.12)
                + (area_contact_intention * 0.10)
            ),
            "contact_offer_only": _clip(
                (area_contact_restraint * 0.22)
                + (hypothesis_contact_restraint * 0.18)
                + (receptive_contact_restraint * 0.20)
                + ((1.0 - contact_entry_fit) * 0.10)
                + ((1.0 - area_contact_intention) * 0.10)
                + ((1.0 - side_fit) * 0.06)
            ),
        }
        entry_geometry_state = max(entry_geometry_pressures, key=entry_geometry_pressures.get)
        area_contact_acceptance_pressure = _clip(
            (entry_geometry_pressures.get("entry_geometry_ready", 0.0) * 0.30)
            + (entry_geometry_pressures.get("entry_geometry_organic_contact", 0.0) * 0.26)
            + (contact_entry_fit * 0.14)
            + (area_contact_intention * 0.14)
            + (pre_geometry_preference_bearing * 0.08)
            + (organic_contact_bearing * 0.10)
            + (side_fit * 0.06)
            - (area_contact_restraint * 0.16)
            - (hypothesis_contact_restraint * 0.12)
            - (receptive_contact_restraint * 0.14)
        )
        area_contact_restraint_pressure = _clip(
            (entry_geometry_pressures.get("contact_offer_only", 0.0) * 0.34)
            + (area_contact_restraint * 0.24)
            + (hypothesis_contact_restraint * 0.20)
            + (receptive_contact_restraint * 0.22)
            + ((1.0 - side_fit) * 0.08)
        )
        area_contact_acceptance_pressure = _clip(
            area_contact_acceptance_pressure
            * (1.0 - (receptive_contact_immaturity_pressure * 0.30))
            * (1.0 - (mature_careful_contact_pressure * 0.18))
        )
        area_contact_restraint_pressure = _clip(
            area_contact_restraint_pressure
            + (receptive_contact_immaturity_pressure * 0.24)
            + (mature_careful_contact_pressure * 0.18)
        )
        area_contact_ready = bool(
            contact_anchor > 0.0
            and area_contact_acceptance_pressure > area_contact_restraint_pressure
        )
        if area_contact_ready:
            area_contact_weight = min(
                0.58,
                max(
                    0.0,
                    (area_contact_fit * 0.42)
                    + (area_contact_intention * 0.28)
                    + (area_contact_acceptance_pressure * 0.22)
                    - (area_contact_restraint_pressure * 0.18),
                    (entry_contact_bearing * 0.28)
                    + (area_contact_readiness * 0.18)
                    - (area_contact_restraint * 0.16)
                ),
            )
            area_contact_weight *= 0.72 + (area_contact_readiness * 0.28)
            contact_entry_weight = float(area_contact_weight)
            contact_entry_price = float(contact_anchor)
            entry_price = float(contact_entry_price)
            if decision == "LONG":
                validity_center = entry_price + min(abs(close_price - entry_price) * 0.28, base_move * 0.18)
            else:
                validity_center = entry_price - min(abs(close_price - entry_price) * 0.28, base_move * 0.18)
            contact_entry_mode_pressures = {
                "area_contact_entry": _clip(
                    (area_contact_weight * 0.34)
                    + (area_contact_readiness * 0.24)
                    + (area_contact_acceptance_pressure * 0.22)
                    - (area_contact_restraint_pressure * 0.12)
                ),
                "area_contact_intention": _clip(
                    (area_contact_intention * 0.26)
                    + (entry_contact_bearing * 0.16)
                    + (area_contact_restraint_pressure * 0.10)
                ),
            }
            contact_entry_mode = max(contact_entry_mode_pressures, key=contact_entry_mode_pressures.get)
            contact_entry_mode = str(contact_entry_mode)
            area_contact_focus_id = str(selected_strategic_area.get("area_focus_id", "-") or "-")
            area_contact_low = float(area_low)
            area_contact_high = float(area_high)

    if entry_price <= 0.0:
        return None

    validity_halfwidth = max(
        base_move * 0.20,
        base_move * (
            0.22
            + (1.0 - focus_confidence) * 0.20
            + noise_damp * 0.08
            + inhibition_level * 0.10
            + max(0.0, width_shift)
        ),
    )

    risk_model_score = max(
        0.0,
        min(
            1.0,
            (filtered_threat_map * 0.28)
            + (noise_damp * 0.18)
            + (inhibition_level * 0.18)
            + (habituation_level * 0.10)
            + max(0.0, -context_cluster_bias) * 0.10
            + max(0.0, -signature_bias) * 0.08
            + max(0.0, abs(target_drift)) * 0.10
            + caution_penalty * 0.22
            + volatility_penalty * 0.18,
        ),
    )

    reward_model_score = max(
        0.0,
        min(
            1.0,
            (signal_relevance * 0.24)
            + (target_lock * 0.22)
            + (focus_confidence * 0.18)
            + (filtered_target_map * 0.14)
            + directional_competition * 0.08
            + max(0.0, context_cluster_bias) * 0.08
            + max(0.0, signature_bias) * 0.06
            + max(0.0, directional_score) * 0.06
            + conviction_boost * 0.20
            + felt_bearing_score * 0.12
            - caution_penalty * 0.10,
        ),
    )

    target_conviction = max(
        0.0,
        min(
            1.0,
            (target_lock * 0.28)
            + (focus_confidence * 0.22)
            + (signal_relevance * 0.18)
            + (context_cluster_quality * 0.10)
            + (signature_quality * 0.08)
            + max(0.0, directional_score) * 0.08
            + conviction_boost * 0.26
            + felt_bearing_score * 0.14
            - caution_penalty * 0.10,
        ),
    )

    stress_pressure = max(
        0.0,
        min(
            1.0,
            max(0.0, float(snapshot_state.get("regulation_pressure", 0.0) or 0.0) / 2.2),
        ),
    )

    risk_distance = max(
        base_move * (
            0.42
            + (risk_model_score * 0.58)
            + (1.0 - target_conviction) * 0.12
            + (1.0 - reward_model_score) * 0.06
        ),
        close_price * float(getattr(Config, "MCM_MIN_SL_DISTANCE", 0.0022) or 0.0022),
        candle_span * 0.42,
    )

    protective_width_factor = max(
        0.82,
        min(
            1.12,
            1.0
            + (protective_width_regulation * 0.14)
            + (load_bearing_capacity * 0.04)
            + (stress_pressure * 0.10)
            + max(0.0, risk_model_score - reward_model_score) * 0.08
            - (protective_courage * 0.10)
            - (target_conviction * 0.12)
            - (inhibition_level * 0.04)
            + width_shift,
        ),
    )
    risk_distance *= protective_width_factor

    max_sl_pct = float(getattr(Config, "MAX_SL_DISTANCE", 0.0) or 0.0)
    if max_sl_pct > 0.0:
        gate_aligned_sl = close_price * max_sl_pct * float(getattr(Config, "MCM_PLAN_GATE_ALIGN", 0.92) or 0.92)
        risk_distance = min(
            risk_distance,
            max(
                gate_aligned_sl,
                close_price * float(getattr(Config, "MCM_MIN_SL_DISTANCE", 0.0022) or 0.0022),
            ),
        )

    min_reward_distance = close_price * float(getattr(Config, "MIN_TP_DISTANCE", 0.008) or 0.008)
    min_rr_target = max(
        float(getattr(Config, "MIN_RR", 1.0) or 1.0),
        1.15 + (target_conviction * 0.18) + (reward_model_score * 0.12) - (risk_model_score * 0.08),
    )
    min_rr_target = max(
        float(getattr(Config, "MIN_RR", min_rr_target) or min_rr_target),
        min_rr_target * (1.0 + rr_shift/2),
    )

    reward_distance = max(
        base_move * (
            0.82
            + (reward_model_score * 1.18)
            + (target_conviction * 0.42)
            - (risk_model_score * 0.12)
        ),
        min_reward_distance * (
            1.0
            + (reward_model_score * 0.22)
            + (target_conviction * 0.12)
            - (risk_model_score * 0.06)
        ),
        risk_distance * min_rr_target,
        min_reward_distance,
    )

    if self_state == "stressed":
        reward_distance *= 0.94
        risk_distance *= 1.0 + (stress_pressure * 0.06)
    elif self_state == "excited":
        reward_distance *= 1.06

    risk_distance *= max(0.84, 1.0 + risk_shift)

    if decision == "LONG":
        sl_price = entry_price - risk_distance
        tp_price = entry_price + reward_distance
    else:
        sl_price = entry_price + risk_distance
        tp_price = entry_price - reward_distance

    reward = abs(tp_price - entry_price)
    risk = abs(entry_price - sl_price)
    rr_value = reward / max(risk, 1e-9)

    return {
        "entry_price": float(entry_price),
        "sl_price": float(sl_price),
        "tp_price": float(tp_price),
        "rr_value": float(rr_value),
        "entry_validity_band": {
            "center": float(validity_center),
            "lower": float(validity_center - validity_halfwidth),
            "upper": float(validity_center + validity_halfwidth),
            "halfwidth": float(validity_halfwidth),
        },
        "target_conviction": float(target_conviction),
        "risk_model_score": float(risk_model_score),
        "reward_model_score": float(reward_model_score),
        "felt_bearing_score": float(felt_bearing_score),
        "felt_profile_label": str(felt_profile_label),
        "entry_mode": str(contact_entry_mode),
        "contact_entry_mode": str(contact_entry_mode),
        "impulse_entry_price": float(impulse_entry_price),
        "contact_entry_price": float(contact_entry_price),
        "strategic_entry_price": float(contact_entry_price),
        "area_contact_weight": float(area_contact_weight),
        "area_contact_fit": float(area_contact_fit),
        "area_contact_intention": float(area_contact_intention),
        "contact_entry_weight": float(contact_entry_weight),
        "contact_entry_fit": float(contact_entry_fit),
        "strategic_entry_weight": float(contact_entry_weight),
        "strategic_entry_fit": float(contact_entry_fit),
        "area_contact_distance_fit": float(area_contact_distance_fit),
        "area_motor_intention": float(area_contact_intention),
        "area_motor_distance_fit": float(area_contact_distance_fit),
        "impulse_perception_pressure": float(impulse_perception_pressure),
        "impulse_entry_intention": float(impulse_perception_pressure),
        "area_order_geometry_intention": float(area_order_geometry_intention),
        "area_entry_intention": float(area_order_geometry_intention),
        "entry_contact_pressure": float(legacy_entry_pressure_alias),
        "entry_choice_pressure": float(legacy_entry_pressure_alias),
        "entry_choice_conflict": float(legacy_entry_pressure_alias),
        "entry_contact_bearing": float(entry_contact_bearing),
        "entry_choice_bearing": float(entry_contact_bearing),
        "area_contact_readiness": float(area_contact_readiness),
        "area_direct_readiness": float(area_contact_readiness),
        "area_contact_restraint": float(area_contact_restraint),
        "area_motor_restraint": float(area_contact_restraint),
        "entry_geometry_bearing": float(entry_geometry_bearing),
        "entry_geometry_state": str(entry_geometry_state),
        "entry_geometry_pressures": dict(entry_geometry_pressures),
        "area_contact_acceptance_pressure": float(area_contact_acceptance_pressure),
        "area_contact_restraint_pressure": float(area_contact_restraint_pressure),
        "thought_seed_bearing": float(thought_seed_bearing),
        "thought_state_bearing": float(thought_state_bearing),
        "thought_state_carrier_factor": float(thought_state_carrier_factor),
        "thought_contact_bearing": float(thought_contact_bearing),
        "pre_geometry_thought_bearing": float(pre_geometry_thought_bearing),
        "pre_geometry_felt_bearing": float(pre_geometry_felt_bearing),
        "pre_geometry_reality_bearing": float(pre_geometry_reality_bearing),
        "pre_geometry_preference_bearing": float(pre_geometry_preference_bearing),
        "visual_reality_bearing": float(visual_reality_bearing),
        "felt_reality_bearing": float(felt_reality_bearing),
        "thought_reality_bearing": float(thought_reality_bearing),
        "form_mcm_reality_fit": float(form_mcm_reality_fit),
        "uncoupled_area_contact_pressure": float(uncoupled_area_contact_pressure),
        "hypothesis_reality_binding": float(hypothesis_reality_binding),
        "hypothesis_reality_binding_gap": float(hypothesis_reality_binding_gap),
        "hypothesis_reality_binding_state": str(hypothesis_reality_binding_state),
        "hypothesis_reality_binding_pressures": dict(hypothesis_reality_binding_pressures),
        "organic_contact_bearing": float(organic_contact_bearing),
        "area_contact_pull": float(area_contact_pull),
        "area_contact_timing_fit": float(area_contact_timing_fit),
        "area_bearing_quality": float(area_bearing_quality),
        "area_replay_fit": float(area_replay_fit),
        "area_patience_quality": float(area_patience_quality),
        "area_invalidity_pressure": float(area_invalidity_pressure),
        "area_action_timing_fit": float(area_action_timing_fit),
        "area_spacetime_fit": float(area_spacetime_fit),
        "area_present_contact": float(area_present_contact),
        "area_afterimage": float(area_afterimage),
        "area_temporal_relevance": float(area_temporal_relevance),
        "entry_contact_state": str(entry_contact_state),
        "entry_contact_choice_state": str(entry_contact_choice_state),
        "entry_choice_state": str(entry_contact_choice_state),
        "entry_preference_state": str(entry_preference_state),
        "entry_preference_pressures": dict(entry_preference_pressures),
        "entry_choice_basis": str(entry_choice_basis),
        "entry_contact_option_count": int(entry_contact_option_count),
        "selected_entry_offer_score": float(selected_entry_offer_score),
        "selected_entry_learned_fit": float(selected_entry_learned_fit),
        "selected_entry_preference_key": str(selected_entry_preference_key),
        "selected_entry_preference_trust": float(selected_entry_preference_trust),
        "selected_entry_preference_caution": float(selected_entry_preference_caution),
        "selected_entry_preference_maturity": float(selected_entry_preference_maturity),
        "selected_entry_preference_utility": float(selected_entry_preference_utility),
        "selected_entry_property_profile_id": str(selected_entry_property_profile_id),
        "selected_entry_property_profile_similarity": float(selected_entry_property_profile_similarity),
        "selected_entry_property_profile_trust": float(selected_entry_property_profile_trust),
        "selected_entry_property_profile_caution": float(selected_entry_property_profile_caution),
        "selected_entry_property_profile_maturity": float(selected_entry_property_profile_maturity),
        "selected_entry_property_profile_utility": float(selected_entry_property_profile_utility),
        "selected_memory_caution_pressure": float(selected_memory_caution_pressure),
        "selected_memory_bearing_pressure": float(selected_memory_bearing_pressure),
        "mature_careful_contact_pressure": float(mature_careful_contact_pressure),
        "entry_contact_options": [
            {
                "area_focus_id": str(option.get("area_focus_id", "-") or "-"),
                "entry_offer_location": str(option.get("entry_offer_location", "-") or "-"),
                "entry_offer_price": float(option.get("entry_offer_price", 0.0) or 0.0),
                "entry_offer_preference": float(option.get("entry_offer_preference", 0.0) or 0.0),
                "entry_offer_fit": float(option.get("entry_offer_fit", 0.0) or 0.0),
                "entry_offer_intention": float(option.get("entry_offer_intention", 0.0) or 0.0),
                "entry_offer_distance_fit": float(option.get("entry_offer_distance_fit", 0.0) or 0.0),
                "entry_offer_learned_fit": float(option.get("entry_offer_learned_fit", 0.0) or 0.0),
                "entry_preference_key": str(option.get("entry_preference_key", "-") or "-"),
                "entry_preference_trust": float(option.get("entry_preference_trust", 0.0) or 0.0),
                "entry_preference_caution": float(option.get("entry_preference_caution", 0.0) or 0.0),
                "entry_preference_maturity": float(option.get("entry_preference_maturity", 0.0) or 0.0),
                "entry_preference_utility": float(option.get("entry_preference_utility", 0.0) or 0.0),
                "entry_property_profile_id": str(option.get("entry_property_profile_id", "-") or "-"),
                "entry_property_profile_similarity": float(option.get("entry_property_profile_similarity", 0.0) or 0.0),
                "entry_property_profile_bearing": float(option.get("entry_property_profile_bearing", 0.0) or 0.0),
                "entry_property_profile_trust": float(option.get("entry_property_profile_trust", 0.0) or 0.0),
                "entry_property_profile_caution": float(option.get("entry_property_profile_caution", 0.0) or 0.0),
                "entry_property_profile_maturity": float(option.get("entry_property_profile_maturity", 0.0) or 0.0),
                "entry_property_profile_utility": float(option.get("entry_property_profile_utility", 0.0) or 0.0),
            }
            for option in entry_contact_options[:5]
        ],
        "contact_learning_state": str(contact_learning_state),
        "learned_contact_fit": float(learned_contact_fit),
        "hypothesis_reality_state": str(hypothesis_reality_state),
        "pre_entry_emergent_structure_reading": float(pre_entry_emergent_structure_reading),
        "pre_entry_emergent_structure_confirmation": float(pre_entry_emergent_structure_confirmation),
        "pre_entry_emergent_structure_state": str(pre_entry_emergent_structure_state),
        "hypothesis_reality_modulation": float(hypothesis_reality_modulation),
        "hypothesis_reality_bearing": float(hypothesis_reality_bearing),
        "open_hypothesis_reality_bearing": float(open_hypothesis_reality_bearing),
        "open_hypothesis_reality_fit": float(open_hypothesis_reality_fit),
        "open_hypothesis_reality_permission": float(open_hypothesis_reality_permission),
        "open_structure_contact_maturity": float(open_structure_contact_maturity),
        "receptive_contact_offer_pressure": float(receptive_contact_offer_pressure),
        "receptive_contact_maturity": float(receptive_contact_maturity),
        "receptive_contact_immaturity_pressure": float(receptive_contact_immaturity_pressure),
        "receptive_contact_restraint": float(receptive_contact_restraint),
        "hypothesis_contact_restraint": float(hypothesis_contact_restraint),
        "hypothesis_action_support": float(hypothesis_reality_bearing),
        "hypothesis_observation_pressure": float(hypothesis_observation_pressure),
        "order_geometry_source": "area_contact_adapter",
        "impulse_role": "perception_pressure_only",
        "area_contact_focus_id": str(area_contact_focus_id),
        "strategic_area_focus_id": str(area_contact_focus_id),
        "area_contact_price_low": float(area_contact_low),
        "area_contact_price_high": float(area_contact_high),
        "strategic_area_price_low": float(area_contact_low),
        "strategic_area_price_high": float(area_contact_high),
        "area_contact_location": str(area_contact_location),
        "strategic_entry_location": str(area_contact_location),
    }

# --------------------------------------------------
# FUSION
# --------------------------------------------------


__all__ = ["derive_trade_plan_from_brain"]
