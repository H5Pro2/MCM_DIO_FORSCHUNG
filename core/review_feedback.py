"""Runtime review feedback resolution.

This module contains the review/experience feedback bridge used by the
runtime-entry path. It is kept separate from MCM_Brain_Modell.py so the brain
file stays a runtime bridge instead of owning the full review computation.
"""

from config import Config
from core.mcm_field import _resolve_affective_context_modulation


def resolve_review_decision_feedback(bot=None, runtime_result=None):

    if bot is None:
        return {
            "review_label": "mixed",
            "review_score": 0.0,
            "uncertainty_recognition_quality": 0.0,
            "observation_quality": 0.0,
            "correction_timing_quality": 0.0,
            "structural_bearing_quality": 0.0,
            "felt_bearing_score": 0.0,
            "felt_profile_label": "mixed_unclear",
            "inner_pattern_support": 0.0,
            "inner_pattern_conflict": 0.0,
            "inner_pattern_fragility": 0.0,
            "inner_pattern_bearing": 0.0,
            "inner_pattern_state": "bearing",
            "pattern_action_support": 0.0,
            "pattern_observe_pressure": 0.0,
            "pattern_replan_pressure": 0.0,
            "reinforcement": 0.0,
            "attenuation": 0.0,
            "bearing_effect": 0.0,
            "carry_capacity": 0.0,
            "caution_load": 0.0,
            "act_push": 0.0,
            "observe_pull": 0.0,
            "replan_pull": 0.0,
            "hold_pull": 0.0,
            "tendency_hint": "hold",
            "observation_maturity_trust": 0.0,
            "observation_action_pressure": 0.0,
            "hypothesis_observed_outcome": "hypothesis_observed_open",
            "hypothesis_confirmation_without_action": 0.0,
            "hypothesis_rejection_without_action": 0.0,
            "hypothesis_neutral_without_action": 0.0,
            "hypothesis_observation_maturity": 0.0,
            "possibility_maturity": 0.0,
            "possibility_caution": 0.0,
            "possibility_contact_bearing": 0.0,
            "possibility_action_support": 0.0,
            "possibility_reality_check_need": 0.0,
            "hypothesis_observed_stability": 0.0,
            "hypothesis_trust_score": 0.0,
            "hypothesis_trust_score_raw": 0.0,
            "hypothesis_trust_priority": 0.0,
            "hypothesis_trust_priority_raw": 0.0,
            "hypothesis_trust_matches_form": False,
            "borrowed_hypothesis_trust_pressure": 0.0,
            "hypothesis_frustration_risk": 0.0,
            "hypothesis_distance_risk": 0.0,
            "hypothesis_trust_state": "hypothesis_trust_unformed",
            "dominant_hypothesis_trust_key": "-",
            "dominant_hypothesis_trust_score": 0.0,
            "dominant_hypothesis_reality_bearing": 0.0,
            "dominant_hypothesis_action_readiness": 0.0,
            "dominant_possibility_variant_key": "-",
            "dominant_possibility_variant_trust": 0.0,
            "dominant_possibility_variant_caution": 0.0,
            "dominant_possibility_variant_maturity": 0.0,
            "dominant_possibility_variant_evidence": 0,
        }

    result = dict(runtime_result or {})
    review_notes = dict((getattr(bot, "mcm_decision_episode_internal", {}) or {}).get("review_notes", {}) or {})
    experience_space = dict(getattr(bot, "mcm_experience_space", {}) or {})
    attempt_feedback = {}
    stats_obj = getattr(bot, "stats", None)
    if stats_obj is not None and hasattr(stats_obj, "get_attempt_feedback"):
        try:
            attempt_feedback = dict(stats_obj.get_attempt_feedback() or {})
        except Exception:
            attempt_feedback = {}
    context_links = dict(experience_space.get("context_links", {}) or {})
    inner_context_links = dict(experience_space.get("inner_context_links", {}) or {})

    context_cluster_id = str(result.get("context_cluster_id", getattr(bot, "last_context_cluster_id", "-")) or "-").strip()
    inner_context_cluster_id = str(result.get("inner_context_cluster_id", getattr(bot, "last_inner_context_cluster_id", "-")) or "-").strip()
    context_item = dict(context_links.get(context_cluster_id, {}) or {})
    inner_context_item = dict(inner_context_links.get(inner_context_cluster_id, {}) or {})
    affective = _resolve_affective_context_modulation(
        bot=bot,
        fused_state={
            "context_cluster_id": context_cluster_id,
            "inner_context_cluster_id": inner_context_cluster_id,
        },
    )

    review_label = str(review_notes.get("review_label", "mixed") or "mixed").strip().lower()
    review_score = float(review_notes.get("review_score", 0.0) or 0.0)
    uncertainty_recognition_quality = float(review_notes.get("uncertainty_recognition_quality", 0.0) or 0.0)
    observation_quality = float(review_notes.get("observation_quality", 0.0) or 0.0)
    correction_timing_quality = float(review_notes.get("correction_timing_quality", 0.0) or 0.0)
    structural_bearing_quality = float(review_notes.get("structural_bearing_quality", 0.0) or 0.0)
    action_inhibition = float(review_notes.get("action_inhibition", 0.0) or 0.0)
    action_clearance = float(review_notes.get("action_clearance", 0.0) or 0.0)
    felt_bearing_score = float(affective.get("felt_bearing_score", 0.0) or 0.0)
    felt_profile_label = str(affective.get("felt_profile_label", "mixed_unclear") or "mixed_unclear").strip().lower()
    inner_pattern_support = float(affective.get("inner_pattern_support", 0.0) or 0.0)
    inner_pattern_conflict = float(affective.get("inner_pattern_conflict", 0.0) or 0.0)
    inner_pattern_fragility = float(affective.get("inner_pattern_fragility", 0.0) or 0.0)
    inner_pattern_bearing = float(affective.get("inner_pattern_bearing", 0.0) or 0.0)
    inner_pattern_state = str(affective.get("inner_pattern_state", "bearing") or "bearing").strip().lower()
    pattern_action_support = float(affective.get("pattern_action_support", 0.0) or 0.0)
    pattern_observe_pressure = float(affective.get("pattern_observe_pressure", 0.0) or 0.0)
    pattern_replan_pressure = float(affective.get("pattern_replan_pressure", 0.0) or 0.0)
    observation_maturity_trust = float(attempt_feedback.get("observation_maturity_trust", 0.0) or 0.0)
    observation_action_pressure = float(attempt_feedback.get("observation_action_pressure", 0.0) or 0.0)
    observation_low_count = int(attempt_feedback.get("observation_low_count", 0) or 0)
    hypothesis_observed_outcome = str(attempt_feedback.get("hypothesis_observed_outcome", "hypothesis_observed_open") or "hypothesis_observed_open").strip()
    hypothesis_confirmation_without_action = float(attempt_feedback.get("hypothesis_confirmation_without_action", 0.0) or 0.0)
    hypothesis_rejection_without_action = float(attempt_feedback.get("hypothesis_rejection_without_action", 0.0) or 0.0)
    hypothesis_neutral_without_action = float(attempt_feedback.get("hypothesis_neutral_without_action", 0.0) or 0.0)
    hypothesis_observation_maturity = float(attempt_feedback.get("hypothesis_observation_maturity", 0.0) or 0.0)
    possibility_maturity = float(attempt_feedback.get("possibility_maturity", 0.0) or 0.0)
    possibility_caution = float(attempt_feedback.get("possibility_caution", 0.0) or 0.0)
    hypothesis_observed_stability = float(attempt_feedback.get("hypothesis_observed_stability", 0.0) or 0.0)
    hypothesis_trust_score_raw = float(attempt_feedback.get("hypothesis_trust_score", 0.0) or 0.0)
    hypothesis_trust_priority_raw = float(attempt_feedback.get("hypothesis_trust_priority", 0.0) or 0.0)
    hypothesis_frustration_risk = float(attempt_feedback.get("hypothesis_frustration_risk", 0.0) or 0.0)
    hypothesis_distance_risk = float(attempt_feedback.get("hypothesis_distance_risk", 0.0) or 0.0)
    hypothesis_trust_state = str(attempt_feedback.get("hypothesis_trust_state", "hypothesis_trust_unformed") or "hypothesis_trust_unformed").strip()
    dominant_hypothesis_trust_key = str(attempt_feedback.get("dominant_hypothesis_trust_key", "-") or "-").strip()
    dominant_hypothesis_trust_score_raw = float(attempt_feedback.get("dominant_hypothesis_trust_score", 0.0) or 0.0)
    dominant_hypothesis_action_readiness_raw = float(attempt_feedback.get("dominant_hypothesis_action_readiness", 0.0) or 0.0)
    dominant_possibility_variant_key = str(attempt_feedback.get("dominant_possibility_variant_key", "-") or "-").strip()
    dominant_possibility_variant_trust = float(attempt_feedback.get("dominant_possibility_variant_trust", 0.0) or 0.0)
    dominant_possibility_variant_caution = float(attempt_feedback.get("dominant_possibility_variant_caution", 0.0) or 0.0)
    dominant_possibility_variant_maturity = float(attempt_feedback.get("dominant_possibility_variant_maturity", 0.0) or 0.0)
    dominant_possibility_variant_evidence = int(attempt_feedback.get("dominant_possibility_variant_evidence", 0) or 0)
    current_form_symbol_id = str(
        result.get("form_symbol_id", (result.get("form_symbol_state", {}) or {}).get("form_symbol_id", "-")) or "-"
    ).strip()
    current_form_state = dict(result.get("form_symbol_state", {}) or {})
    current_side = str(result.get("proposed_decision", result.get("decision", "-")) or "-").strip().upper()
    current_entry_mode = str(result.get("entry_mode", "") or "").strip()
    current_entry_choice_state = str(result.get("entry_choice_state", "") or "").strip()
    current_area_focus_id = str(result.get("strategic_area_focus_id", "") or "").strip()
    current_entry_location = str(result.get("strategic_entry_location", "") or "").strip()
    current_meta_state = dict(result.get("meta_regulation_state", {}) or {})
    current_possibility_state = dict(current_meta_state.get("mcm_possibility_field_state", {}) or {})
    current_possibility_variant_id = str(
        current_possibility_state.get(
            "possibility_dominant_variant_id",
            current_meta_state.get("possibility_dominant_variant_id", ""),
        )
        or ""
    ).strip()
    current_hypothesis_keys = {
        key for key in (
            current_form_symbol_id,
            str(current_form_state.get("form_symbol_compound_id", "") or "").strip(),
            str(current_form_state.get("form_symbol_semantic_profile", "") or "").strip(),
        )
        if key and key != "-"
    }
    dominant_hypothesis_trust_matches_form = bool(
        dominant_hypothesis_trust_key
        and dominant_hypothesis_trust_key != "-"
        and dominant_hypothesis_trust_key in current_hypothesis_keys
    )
    dominant_hypothesis_trust_score = (
        dominant_hypothesis_trust_score_raw
        if dominant_hypothesis_trust_matches_form
        else dominant_hypothesis_trust_score_raw * 0.12
    )
    dominant_hypothesis_action_readiness = (
        dominant_hypothesis_action_readiness_raw
        if dominant_hypothesis_trust_matches_form
        else dominant_hypothesis_action_readiness_raw * 0.12
    )
    dominant_hypothesis_reality_bearing = float(dominant_hypothesis_action_readiness)
    hypothesis_trust_matches_form = bool(
        dominant_hypothesis_trust_matches_form
        or dominant_hypothesis_trust_key in ("", "-")
        or current_form_symbol_id in ("", "-")
    )
    hypothesis_trust_score = (
        hypothesis_trust_score_raw
        if hypothesis_trust_matches_form
        else hypothesis_trust_score_raw * 0.18
    )
    hypothesis_trust_priority = (
        hypothesis_trust_priority_raw
        if hypothesis_trust_matches_form
        else hypothesis_trust_priority_raw * 0.18
    )
    borrowed_dominant_hypothesis_pressure = max(
        0.0,
        min(1.0, dominant_hypothesis_trust_score_raw - dominant_hypothesis_trust_score),
    )
    borrowed_hypothesis_trust_pressure = max(
        0.0,
        min(
            1.0,
            max(
                hypothesis_trust_score_raw - hypothesis_trust_score,
                hypothesis_trust_priority_raw - hypothesis_trust_priority,
            ),
        ),
    )
    observation_maturity_balance = max(0.0, min(1.0, observation_maturity_trust - observation_action_pressure))
    structure_state = dict(result.get("structure_perception_state", {}) or {})
    actual_structure_quality = float(structure_state.get("structure_quality", result.get("structure_quality", 0.0)) or 0.0)
    if actual_structure_quality <= 0.0:
        actual_structure_quality = float(max(structural_bearing_quality, felt_bearing_score))
    observation_maturity_scope = max(0.0, min(1.0, (0.56 - actual_structure_quality) / 0.18))
    observation_scoped_balance = float(observation_maturity_balance * observation_maturity_scope)
    hypothesis_action_influence_enabled = bool(getattr(Config, "MCM_HYPOTHESIS_ACTION_INFLUENCE_ENABLED", False))
    raw_possibility_action_support = max(
        0.0,
        min(
            1.0,
            (possibility_maturity * 0.52)
            + (hypothesis_confirmation_without_action * hypothesis_observation_maturity * 0.32)
            + (hypothesis_trust_priority * 0.22)
            + (dominant_possibility_variant_trust * 0.08)
            + (dominant_possibility_variant_maturity * 0.06)
            + (dominant_hypothesis_trust_score * 0.08)
            + (dominant_hypothesis_action_readiness * 0.06)
            + (hypothesis_neutral_without_action * 0.04)
            - (observation_maturity_scope * 0.18)
            - (dominant_possibility_variant_caution * 0.07)
            - (possibility_caution * 0.14),
        ),
    )
    possibility_action_support = float(raw_possibility_action_support if hypothesis_action_influence_enabled else 0.0)
    possibility_contact_bearing = float(possibility_action_support)
    hypothesis_action_bearing = float(hypothesis_trust_priority if hypothesis_action_influence_enabled else 0.0)
    possibility_reality_check_need = max(
        0.0,
        min(
            1.0,
            (possibility_caution * 0.46)
            + (dominant_possibility_variant_caution * 0.14)
            + (max(0.0, 3 - dominant_possibility_variant_evidence) / 3.0 * 0.04 if dominant_possibility_variant_key not in ("", "-") else 0.0)
            + (hypothesis_rejection_without_action * hypothesis_observation_maturity * 0.32)
            + (hypothesis_frustration_risk * 0.18)
            + (hypothesis_distance_risk * 0.16)
            + (borrowed_dominant_hypothesis_pressure * 0.08)
            + (borrowed_hypothesis_trust_pressure * 0.06)
            + (observation_maturity_scope * 0.12)
            + (max(0.0, 0.38 - actual_structure_quality) * 0.10),
        ),
    )
    reinforcement = float(context_item.get("reinforcement", 0.0) or 0.0)
    attenuation = float(context_item.get("attenuation", 0.0) or 0.0)
    bearing_effect = float(context_item.get("bearing_effect", 0.0) or 0.0)

    if inner_context_item:
        reinforcement = float((reinforcement * 0.56) + (float(inner_context_item.get("pattern_reinforcement", 0.0) or 0.0) * 0.44))
        attenuation = float((attenuation * 0.56) + (float(inner_context_item.get("pattern_attenuation", 0.0) or 0.0) * 0.44))
        bearing_effect = float((bearing_effect * 0.58) + ((inner_pattern_bearing - inner_pattern_conflict) * 0.42))

    carry_capacity = max(
        0.0,
        min(
            1.0,
            (review_score * 0.22)
            + (structural_bearing_quality * 0.24)
            + (felt_bearing_score * 0.20)
            + (max(0.0, bearing_effect) * 0.16)
            + (max(0.0, reinforcement) * 0.10)
            + (action_clearance * 0.08),
        ),
    )

    caution_load = max(
        0.0,
        min(
            1.0,
            (action_inhibition * 0.20)
            + (max(0.0, attenuation) * 0.18)
            + (max(0.0, -bearing_effect) * 0.16)
            + (max(0.0, 1.0 - review_score) * 0.10)
            + (0.10 if felt_profile_label in ("burdened", "euphoric_risk", "volatile_bearing") else 0.0),
        ),
    )

    act_push = max(
        0.0,
        min(
            1.0,
            carry_capacity
            - (caution_load * 0.68)
            + (pattern_action_support * 0.18)
            + (observation_action_pressure * 0.033)
            + (possibility_action_support * 0.070)
            + (hypothesis_action_bearing * 0.060)
            - (observation_maturity_trust * 0.052)
            - (observation_scoped_balance * 0.080)
            - (possibility_reality_check_need * 0.055),
        ),
    )
    observe_pull = max(
        0.0,
        min(
            1.0,
            (observation_quality * 0.34)
            + (uncertainty_recognition_quality * 0.20)
            + (pattern_observe_pressure * 0.22)
            + (inner_pattern_fragility * 0.08)
            + (0.10 if review_label == "observe_was_correct" else 0.0)
            + (observation_maturity_trust * 0.075)
            + (observation_scoped_balance * 0.110)
            + (possibility_reality_check_need * 0.080)
            + (hypothesis_distance_risk * 0.050)
            - (possibility_action_support * 0.020),
        ),
    )
    replan_pull = max(
        0.0,
        min(
            1.0,
            (correction_timing_quality * 0.36)
            + (uncertainty_recognition_quality * 0.12)
            + (pattern_replan_pressure * 0.26)
            + (inner_pattern_conflict * 0.10)
            + (0.12 if review_label == "correction_was_correct" else 0.0)
            + (observation_scoped_balance * 0.050)
            + (possibility_reality_check_need * 0.060)
            + (hypothesis_frustration_risk * 0.050),
        ),
    )
    hold_pull = max(
        0.0,
        min(
            1.0,
            (caution_load * 0.46)
            + (pattern_observe_pressure * 0.10)
            + (pattern_replan_pressure * 0.08)
            + (max(0.0, 1.0 - act_push) * 0.14),
        ),
    )

    tendency_hint_pressures = {
        "act": max(0.0, min(1.0, (act_push * 0.56) + (max(0.0, act_push - max(observe_pull, replan_pull)) * 0.18))),
        "replan": max(0.0, min(1.0, (replan_pull * 0.54) + (max(0.0, replan_pull - observe_pull) * 0.16))),
        "observe": max(0.0, min(1.0, (observe_pull * 0.54) + (pattern_observe_pressure * 0.12))),
        "hold": max(0.0, min(1.0, (hold_pull * 0.48) + (max(0.0, 1.0 - max(act_push, observe_pull, replan_pull)) * 0.18))),
    }
    tendency_hint = max(tendency_hint_pressures, key=tendency_hint_pressures.get)

    return {
        "review_label": str(review_label),
        "review_score": float(review_score),
        "uncertainty_recognition_quality": float(uncertainty_recognition_quality),
        "observation_quality": float(observation_quality),
        "correction_timing_quality": float(correction_timing_quality),
        "structural_bearing_quality": float(structural_bearing_quality),
        "felt_bearing_score": float(felt_bearing_score),
        "felt_profile_label": str(felt_profile_label),
        "inner_pattern_support": float(inner_pattern_support),
        "inner_pattern_conflict": float(inner_pattern_conflict),
        "inner_pattern_fragility": float(inner_pattern_fragility),
        "inner_pattern_bearing": float(inner_pattern_bearing),
        "inner_pattern_state": str(inner_pattern_state or "bearing"),
        "pattern_action_support": float(pattern_action_support),
        "pattern_observe_pressure": float(pattern_observe_pressure),
        "pattern_replan_pressure": float(pattern_replan_pressure),
        "reinforcement": float(reinforcement),
        "attenuation": float(attenuation),
        "bearing_effect": float(bearing_effect),
        "carry_capacity": float(carry_capacity),
        "caution_load": float(caution_load),
        "act_push": float(act_push),
        "observe_pull": float(observe_pull),
        "replan_pull": float(replan_pull),
        "hold_pull": float(hold_pull),
        "tendency_hint": str(tendency_hint),
        "tendency_hint_pressures": dict(tendency_hint_pressures),
        "observation_maturity_trust": float(observation_maturity_trust),
        "observation_action_pressure": float(observation_action_pressure),
        "observation_maturity_balance": float(observation_maturity_balance),
        "observation_maturity_scope": float(observation_maturity_scope),
        "observation_scoped_balance": float(observation_scoped_balance),
        "observation_low_count": int(observation_low_count),
        "hypothesis_action_influence_enabled": bool(hypothesis_action_influence_enabled),
        "raw_possibility_action_support": float(raw_possibility_action_support),
        "hypothesis_observed_outcome": str(hypothesis_observed_outcome),
        "hypothesis_confirmation_without_action": float(hypothesis_confirmation_without_action),
        "hypothesis_rejection_without_action": float(hypothesis_rejection_without_action),
        "hypothesis_neutral_without_action": float(hypothesis_neutral_without_action),
        "hypothesis_observation_maturity": float(hypothesis_observation_maturity),
        "possibility_maturity": float(possibility_maturity),
        "possibility_caution": float(possibility_caution),
        "possibility_contact_bearing": float(possibility_contact_bearing),
        "possibility_action_support": float(possibility_action_support),
        "possibility_reality_check_need": float(possibility_reality_check_need),
        "hypothesis_observed_stability": float(hypothesis_observed_stability),
        "hypothesis_trust_score": float(hypothesis_trust_score),
        "hypothesis_trust_score_raw": float(hypothesis_trust_score_raw),
        "hypothesis_trust_priority": float(hypothesis_trust_priority),
        "hypothesis_trust_priority_raw": float(hypothesis_trust_priority_raw),
        "hypothesis_trust_matches_form": bool(hypothesis_trust_matches_form),
        "borrowed_hypothesis_trust_pressure": float(borrowed_hypothesis_trust_pressure),
        "hypothesis_frustration_risk": float(hypothesis_frustration_risk),
        "hypothesis_distance_risk": float(hypothesis_distance_risk),
        "hypothesis_trust_state": str(hypothesis_trust_state),
        "dominant_hypothesis_trust_key": str(dominant_hypothesis_trust_key),
        "dominant_hypothesis_trust_score": float(dominant_hypothesis_trust_score),
        "dominant_hypothesis_trust_score_raw": float(dominant_hypothesis_trust_score_raw),
        "dominant_hypothesis_trust_matches_form": bool(dominant_hypothesis_trust_matches_form),
        "dominant_hypothesis_reality_bearing": float(dominant_hypothesis_reality_bearing),
        "dominant_hypothesis_action_readiness": float(dominant_hypothesis_action_readiness),
        "dominant_hypothesis_action_readiness_raw": float(dominant_hypothesis_action_readiness_raw),
        "borrowed_dominant_hypothesis_pressure": float(borrowed_dominant_hypothesis_pressure),
        "dominant_possibility_variant_key": str(dominant_possibility_variant_key),
        "dominant_possibility_variant_trust": float(dominant_possibility_variant_trust),
        "dominant_possibility_variant_caution": float(dominant_possibility_variant_caution),
        "dominant_possibility_variant_maturity": float(dominant_possibility_variant_maturity),
        "dominant_possibility_variant_evidence": int(dominant_possibility_variant_evidence),
    }
