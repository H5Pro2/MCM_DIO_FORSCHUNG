"""Hypothesis learning helpers.

This module contains the pure calculation parts for DIO's observed hypotheses:
open-hypothesis consequence reading, observation maturity, trust, frustration,
and distance pressure. TradeStats keeps ownership of persistence and counters.
"""

from config import Config


def _hypothesis_learning_enabled() -> bool:
    return bool(getattr(Config, "MCM_HYPOTHESIS_LEARNING_ENABLED", False))


def _empty_open_hypothesis_learning() -> dict:
    return {
        "open_hypothesis_learning_state": "-",
        "open_hypothesis_consequence_score": 0.0,
        "open_hypothesis_burden_score": 0.0,
        "open_hypothesis_reorganization_score": 0.0,
        "open_hypothesis_replay_need": 0.0,
        "open_hypothesis_distance_need": 0.0,
        "open_hypothesis_reinterpretation_need": 0.0,
        "open_hypothesis_reorganization_posture": "-",
    }


def _neutralize_hypothesis_summary(learning: dict) -> dict:
    result = dict(learning or {})
    result["open"] = 0
    result["resolved"] = int(result.get("resolved", 0) or 0)
    result["saved_loss"] = int(result.get("saved_loss", 0) or 0)
    result["missed_gain"] = int(result.get("missed_gain", 0) or 0)
    result["neutral"] = int(result.get("neutral", 0) or 0)
    result["maturity_trust"] = 0.0
    result["action_pressure"] = 0.0
    result["hypothesis_observed_outcome"] = "hypothesis_disabled"
    result["hypothesis_confirmation_without_action"] = 0.0
    result["hypothesis_rejection_without_action"] = 0.0
    result["hypothesis_neutral_without_action"] = 0.0
    result["hypothesis_observation_maturity"] = 0.0
    result["possibility_maturity"] = 0.0
    result["possibility_caution"] = 0.0
    result["hypothesis_observed_stability"] = 0.0
    result["hypothesis_trust_score"] = 0.0
    result["hypothesis_trust_priority"] = 0.0
    result["hypothesis_frustration_risk"] = 0.0
    result["hypothesis_distance_risk"] = 0.0
    result["hypothesis_trust_state"] = "hypothesis_disabled"
    result["dominant_hypothesis_trust_key"] = "-"
    result["dominant_hypothesis_trust_score"] = 0.0
    result["dominant_hypothesis_action_readiness"] = 0.0
    result["dominant_hypothesis_trust_evidence"] = 0
    result["dominant_possibility_variant_key"] = "-"
    result["dominant_possibility_variant_trust"] = 0.0
    result["dominant_possibility_variant_caution"] = 0.0
    result["dominant_possibility_variant_maturity"] = 0.0
    result["dominant_possibility_variant_evidence"] = 0
    result["hypothesis_trust_family_count"] = 0
    result["declined_hypothesis_resolved"] = 0
    result["declined_hypothesis_saved_loss"] = 0
    result["declined_hypothesis_missed_gain"] = 0
    result["declined_hypothesis_neutral"] = 0
    result["declined_hypothesis_confirmation_without_action"] = 0.0
    result["declined_hypothesis_rejection_without_action"] = 0.0
    result["declined_hypothesis_neutral_without_action"] = 0.0
    result["declined_hypothesis_maturity"] = 0.0
    result["hypothesis_trust_families"] = {}
    result["possibility_trust_families"] = {}
    result["declined_hypothesis_families"] = {}
    result["declined_hypothesis_side_families"] = {}
    return result


def _float(value, default=0.0):
    try:
        if value is None:
            return float(default)
        return float(value)
    except Exception:
        return float(default)


def _clip01(value):
    value = _float(value)
    if value != value:
        value = 0.0
    return max(0.0, min(1.0, float(value)))


def _hypothesis_family_keys(obs: dict) -> list[str]:
    source = dict(obs or {})
    keys = []
    side = str(source.get("side", "-") or "-").strip().upper()
    form_symbol_id = str(source.get("form_symbol_id", "") or "").strip()
    compound_id = str(source.get("form_symbol_compound_id", "") or "").strip()
    semantic_profile = str(source.get("form_symbol_semantic_profile", "") or "").strip()

    # Reality anchor: only real perceived form/MCM families may mature as trust
    # families. Entry thoughts, areas and variants are stored as traces on this
    # anchor, not as independent "thesis" realities.
    for raw in (
        form_symbol_id,
        compound_id,
        semantic_profile,
    ):
        key = str(raw or "").strip()
        if key and key != "-" and key not in keys:
            keys.append(key)
    if not keys:
        bucket = str(source.get("structure_bucket", "unknown") or "unknown").strip()
        keys.append(f"{side}:{bucket}")
    return keys


def _hypothesis_thought_trace(obs: dict) -> dict:
    source = dict(obs or {})
    return {
        "side": str(source.get("side", "-") or "-").strip().upper(),
        "entry_mode": str(source.get("entry_mode", "") or "").strip(),
        "entry_choice_state": str(source.get("entry_choice_state", "") or "").strip(),
        "strategic_area_focus_id": str(source.get("strategic_area_focus_id", "") or "").strip(),
        "strategic_entry_location": str(source.get("strategic_entry_location", "") or "").strip(),
        "possibility_family_key": str(source.get("possibility_family_key", "") or "").strip(),
        "possibility_dominant_variant_id": str(source.get("possibility_dominant_variant_id", "") or "").strip(),
        "possibility_collapse_reason": str(source.get("possibility_collapse_reason", "") or "").strip(),
    }


def _bump_observation_bucket(learning: dict, bucket_name: str, bucket_key: str, result: str, sample_weight: float) -> None:
    key = str(bucket_key or "-").strip() or "-"
    bucket = dict(learning.get(bucket_name, {}) or {})
    item = dict(bucket.get(key, {}) or {})
    item["resolved"] = int(item.get("resolved", 0) or 0) + 1
    item[result] = int(item.get(result, 0) or 0) + 1
    item[f"{result}_weight"] = _float(item.get(f"{result}_weight", 0.0)) + float(sample_weight)
    item["last_result"] = str(result)
    total = max(1, int(item.get("resolved", 0) or 0))
    item["confirmation_share"] = float(_clip01(int(item.get("missed_gain", 0) or 0) / float(total)))
    item["rejection_share"] = float(_clip01(int(item.get("saved_loss", 0) or 0) / float(total)))
    item["neutral_share"] = float(_clip01(int(item.get("neutral", 0) or 0) / float(total)))
    bucket[key] = dict(item)
    learning[bucket_name] = dict(list(bucket.items())[-80:])


def _bucket_share(learning: dict, bucket_name: str, bucket_key: str, field: str) -> float:
    bucket = dict(learning.get(bucket_name, {}) or {})
    item = dict(bucket.get(str(bucket_key or "-").strip() or "-", {}) or {})
    return _clip01(item.get(field, 0.0))


def _bucket_count(learning: dict, bucket_name: str, bucket_key: str) -> int:
    bucket = dict(learning.get(bucket_name, {}) or {})
    item = dict(bucket.get(str(bucket_key or "-").strip() or "-", {}) or {})
    return int(item.get("resolved", 0) or 0)


def derive_open_hypothesis_learning(record: dict, emergent_state: str | None = None) -> dict:
    if not _hypothesis_learning_enabled():
        return _empty_open_hypothesis_learning()

    source = dict(record or {})
    state = str(emergent_state or source.get("emergent_structure_state", "") or "").strip()
    reason = str(source.get("reason", "") or "").strip().lower()

    if state not in ("open_structure_contact", "open_structural_hypothesis"):
        return {
            "open_hypothesis_learning_state": "-",
            "open_hypothesis_consequence_score": 0.0,
            "open_hypothesis_burden_score": 0.0,
            "open_hypothesis_reorganization_score": 0.0,
            "open_hypothesis_replay_need": 0.0,
            "open_hypothesis_distance_need": 0.0,
            "open_hypothesis_reinterpretation_need": 0.0,
            "open_hypothesis_reorganization_posture": "-",
        }

    pnl = _float(source.get("pnl", 0.0))
    rr_value = _float(source.get("rr_value", 0.0))
    reading = _clip01(source.get("emergent_structure_reading", 0.0))
    confirmation = _clip01(source.get("emergent_structure_confirmation", 0.0))
    grounding = _clip01(source.get("thought_seed_structural_grounding", 0.0))
    open_pressure = _clip01(source.get("thought_seed_open_hypothesis_pressure", 0.0))
    lag = _clip01(source.get("thought_seed_reality_lag", 0.0))
    balance = max(-1.0, min(1.0, _float(source.get("thought_seed_consequence_balance", 0.0))))

    positive = reason == "tp_hit" or pnl > 0.0
    negative = reason == "sl_hit" or pnl < 0.0
    pnl_magnitude = _clip01(abs(pnl) / max(0.5, abs(pnl) + 1.0))
    consequence_score = _clip01(
        (0.42 if positive else 0.0)
        + (confirmation * 0.18)
        + (grounding * 0.14)
        + (max(0.0, balance) * 0.12)
        + (_clip01(rr_value / 4.0) * 0.08)
        + (pnl_magnitude * 0.06)
    )
    burden_score = _clip01(
        (0.42 if negative else 0.0)
        + (open_pressure * 0.18)
        + (lag * 0.16)
        + (max(0.0, -balance) * 0.12)
        + ((1.0 - grounding) * 0.08)
        + (pnl_magnitude * 0.04)
    )
    reorganization_score = _clip01(
        (open_pressure * 0.26)
        + (lag * 0.22)
        + ((1.0 - confirmation) * 0.16)
        + ((1.0 - grounding) * 0.14)
        + (reading * 0.12)
        + (burden_score * 0.10)
        - (consequence_score * 0.12)
    )
    replay_need = _clip01(
        (reorganization_score * 0.38)
        + (lag * 0.24)
        + (open_pressure * 0.16)
        + ((1.0 - grounding) * 0.12)
        + ((1.0 - confirmation) * 0.10)
    )
    distance_need = _clip01(
        (burden_score * 0.34)
        + (max(0.0, -balance) * 0.20)
        + (open_pressure * 0.16)
        + (lag * 0.14)
        + ((1.0 - grounding) * 0.10)
        + (0.06 if negative else 0.0)
    )
    reinterpretation_need = _clip01(
        (reorganization_score * 0.34)
        + (max(0.0, burden_score - consequence_score) * 0.20)
        + ((1.0 - confirmation) * 0.16)
        + (reading * 0.12)
        + (lag * 0.10)
        + ((1.0 - grounding) * 0.08)
    )

    if max(replay_need, distance_need, reinterpretation_need) < 0.28:
        reorganization_posture = "low_reorganization_need"
    elif reinterpretation_need >= max(replay_need, distance_need):
        reorganization_posture = "reinterpretation_dominant"
    elif distance_need >= replay_need:
        reorganization_posture = "distance_dominant"
    else:
        reorganization_posture = "replay_dominant"

    if positive and consequence_score >= max(0.34, burden_score):
        learning_state = "open_hypothesis_carried"
    elif reorganization_score >= 0.46 and (burden_score - reorganization_score) < 0.18:
        learning_state = "open_hypothesis_reorganizing"
    elif negative and burden_score >= 0.42:
        learning_state = "open_hypothesis_burdened"
    elif reorganization_score >= 0.34:
        learning_state = "open_hypothesis_reorganizing"
    else:
        learning_state = "open_hypothesis_reorganizing"

    return {
        "open_hypothesis_learning_state": str(learning_state),
        "open_hypothesis_consequence_score": float(consequence_score),
        "open_hypothesis_burden_score": float(burden_score),
        "open_hypothesis_reorganization_score": float(reorganization_score),
        "open_hypothesis_replay_need": float(replay_need),
        "open_hypothesis_distance_need": float(distance_need),
        "open_hypothesis_reinterpretation_need": float(reinterpretation_need),
        "open_hypothesis_reorganization_posture": str(reorganization_posture),
    }


def refresh_observation_learning_summary(learning: dict, pending_observations: list | None = None) -> dict:
    if not _hypothesis_learning_enabled():
        return _neutralize_hypothesis_summary(dict(learning or {}))

    learning = dict(learning or {})
    resolved = int(learning.get("resolved", 0) or 0)
    saved = int(learning.get("saved_loss", 0) or 0)
    missed = int(learning.get("missed_gain", 0) or 0)
    neutral = int(learning.get("neutral", 0) or 0)
    open_count = int(len(pending_observations or []))
    evidence = max(0, saved + missed + neutral)
    family_map = dict(learning.get("hypothesis_trust_families", {}) or {})
    possibility_family_map = dict(learning.get("possibility_trust_families", {}) or {})

    if resolved > 0:
        learning["maturity_trust"] = float(_clip01((saved + neutral * 0.35) / float(resolved)))
        learning["action_pressure"] = float(_clip01(missed / float(resolved)))
    else:
        learning["maturity_trust"] = 0.0
        learning["action_pressure"] = 0.0

    if evidence > 0:
        confirmation_without_action = _clip01(missed / float(evidence))
        rejection_without_action = _clip01(saved / float(evidence))
        neutral_without_action = _clip01(neutral / float(evidence))
    else:
        confirmation_without_action = 0.0
        rejection_without_action = 0.0
        neutral_without_action = 0.0

    observation_maturity = _clip01(resolved / float(resolved + open_count)) if resolved + open_count > 0 else 0.0
    possibility_maturity = _clip01(
        (confirmation_without_action * 0.48)
        + (observation_maturity * 0.22)
        + (neutral_without_action * 0.08)
        - (rejection_without_action * 0.30)
    )
    possibility_caution = _clip01(
        (rejection_without_action * 0.48)
        + ((1.0 - observation_maturity) * 0.16)
        + (_clip01(open_count / float(max(1, resolved + open_count))) * 0.12)
    )
    evidence_confidence = _clip01(evidence / 12.0)
    observed_stability = _clip01(abs(confirmation_without_action - rejection_without_action) * evidence_confidence)
    hypothesis_trust_score = _clip01(
        (confirmation_without_action * 0.52)
        + (possibility_maturity * 0.24)
        + (observed_stability * 0.18)
        - (rejection_without_action * 0.34)
    )
    hypothesis_trust_priority = _clip01(
        (hypothesis_trust_score * 0.58)
        + (observed_stability * 0.18)
        + (observation_maturity * 0.12)
        - (possibility_caution * 0.20)
    )
    hypothesis_frustration_risk = _clip01(
        (rejection_without_action * 0.36)
        + (max(0.0, 0.46 - hypothesis_trust_score) * 0.20)
        + (_clip01(open_count / float(max(1, resolved + open_count))) * 0.12)
        - (confirmation_without_action * 0.12)
    )
    hypothesis_distance_risk = _clip01(
        (rejection_without_action * 0.34)
        + (possibility_caution * 0.28)
        + ((1.0 - observation_maturity) * 0.10)
        - (hypothesis_trust_score * 0.18)
    )

    dominant_family_key = "-"
    dominant_family_trust = 0.0
    dominant_family_action_readiness = 0.0
    dominant_family_evidence = 0
    for key, payload in family_map.items():
        item = dict(payload or {})
        seen = int(item.get("seen", 0) or 0)
        if seen <= 0:
            continue
        carried = int(item.get("carried", 0) or 0)
        hurt = int(item.get("hurt", 0) or 0)
        family_neutral = int(item.get("neutral", 0) or 0)
        family_evidence = max(1, carried + hurt + family_neutral)
        carried_weight = _float(item.get("carried_weight", carried))
        hurt_weight = _float(item.get("hurt_weight", hurt))
        neutral_weight = _float(item.get("neutral_weight", family_neutral))
        family_weight = max(1e-9, carried_weight + hurt_weight + neutral_weight)
        family_confirmation = carried_weight / family_weight
        family_rejection = hurt_weight / family_weight
        family_neutral_share = neutral_weight / family_weight
        family_confidence = _clip01((family_evidence / 10.0) * 0.58 + (family_weight / 10.0) * 0.42)
        family_stability = _clip01(abs(family_confirmation - family_rejection) * family_confidence)
        quality_samples = max(1.0, _float(item.get("quality_samples", 0.0), 0.0))
        avg_quality = _clip01(_float(item.get("quality_sum", 0.0)) / quality_samples)
        avg_confirmation_quality = _clip01(_float(item.get("confirmation_quality_sum", 0.0)) / quality_samples)
        avg_reality_binding = _clip01(_float(item.get("reality_binding_sum", 0.0)) / quality_samples)
        avg_afterimage_maturity = _clip01(_float(item.get("afterimage_maturity_sum", 0.0)) / quality_samples)
        family_trust = _clip01(
            (family_confirmation * 0.48)
            + (family_stability * 0.20)
            + (family_confidence * 0.12)
            + (avg_confirmation_quality * 0.10)
            + (avg_reality_binding * 0.06)
            + (avg_afterimage_maturity * 0.04)
            - (family_rejection * 0.30)
        )
        family_action_readiness = _clip01(
            (family_trust * 0.48)
            + (family_confirmation * 0.20)
            + (avg_quality * 0.12)
            + (avg_reality_binding * 0.10)
            + (avg_afterimage_maturity * 0.06)
            + (family_neutral_share * 0.04)
            - (family_rejection * 0.18)
        )
        family_caution = _clip01(
            (family_rejection * 0.42)
            + ((1.0 - avg_reality_binding) * 0.12)
            + ((1.0 - avg_quality) * 0.08)
            - (family_confirmation * 0.12)
        )
        item["trust_score"] = float(family_trust)
        item["action_readiness"] = float(family_action_readiness)
        item["caution"] = float(family_caution)
        item["confirmation"] = float(family_confirmation)
        item["rejection"] = float(family_rejection)
        item["neutral_share"] = float(family_neutral_share)
        item["stability"] = float(family_stability)
        item["avg_quality"] = float(avg_quality)
        item["avg_confirmation_quality"] = float(avg_confirmation_quality)
        item["avg_reality_binding"] = float(avg_reality_binding)
        item["avg_afterimage_maturity"] = float(avg_afterimage_maturity)
        family_map[str(key)] = dict(item)
        if family_evidence < 2:
            continue
        dominant_score = (family_trust * 0.68) + (family_action_readiness * 0.32)
        current_dominant_score = dominant_family_trust
        if dominant_family_key != "-":
            current = dict(family_map.get(dominant_family_key, {}) or {})
            current_dominant_score = (
                float(current.get("trust_score", dominant_family_trust) or 0.0) * 0.68
                + float(current.get("action_readiness", 0.0) or 0.0) * 0.32
            )
        if dominant_score > current_dominant_score:
            dominant_family_key = str(key)
            dominant_family_trust = float(family_trust)
            dominant_family_action_readiness = float(family_action_readiness)
            dominant_family_evidence = int(family_evidence)

    if evidence <= 0:
        hypothesis_trust_state = "hypothesis_trust_unformed"
    elif hypothesis_trust_priority >= max(0.42, hypothesis_distance_risk + 0.08):
        hypothesis_trust_state = "hypothesis_trust_prioritized"
    elif hypothesis_frustration_risk >= max(0.42, hypothesis_trust_score + 0.08):
        hypothesis_trust_state = "hypothesis_trust_frustrated"
    elif hypothesis_distance_risk >= 0.36:
        hypothesis_trust_state = "hypothesis_trust_distance_needed"
    else:
        hypothesis_trust_state = "hypothesis_trust_learning"

    if evidence <= 0:
        observed_outcome = "hypothesis_observed_open"
    elif confirmation_without_action >= max(0.52, rejection_without_action + 0.10):
        observed_outcome = "hypothesis_would_have_carried"
    elif rejection_without_action >= max(0.52, confirmation_without_action + 0.10):
        observed_outcome = "hypothesis_would_have_hurt"
    else:
        observed_outcome = "hypothesis_observed_mixed"

    learning["open"] = int(open_count)
    learning["hypothesis_observed_outcome"] = str(observed_outcome)
    learning["hypothesis_confirmation_without_action"] = float(confirmation_without_action)
    learning["hypothesis_rejection_without_action"] = float(rejection_without_action)
    learning["hypothesis_neutral_without_action"] = float(neutral_without_action)
    learning["hypothesis_observation_maturity"] = float(observation_maturity)
    learning["possibility_maturity"] = float(possibility_maturity)
    learning["possibility_caution"] = float(possibility_caution)
    learning["hypothesis_observed_stability"] = float(observed_stability)
    learning["hypothesis_trust_score"] = float(hypothesis_trust_score)
    learning["hypothesis_trust_priority"] = float(hypothesis_trust_priority)
    learning["hypothesis_frustration_risk"] = float(hypothesis_frustration_risk)
    learning["hypothesis_distance_risk"] = float(hypothesis_distance_risk)
    learning["hypothesis_trust_state"] = str(hypothesis_trust_state)
    learning["dominant_hypothesis_trust_key"] = str(dominant_family_key)
    learning["dominant_hypothesis_trust_score"] = float(dominant_family_trust)
    learning["dominant_hypothesis_action_readiness"] = float(dominant_family_action_readiness)
    learning["dominant_hypothesis_trust_evidence"] = int(dominant_family_evidence)
    learning["hypothesis_trust_family_count"] = int(len(family_map))
    learning["hypothesis_trust_families"] = dict(list(family_map.items())[-80:])
    dominant_possibility_key = "-"
    dominant_possibility_trust = 0.0
    dominant_possibility_caution = 0.0
    dominant_possibility_maturity = 0.0
    dominant_possibility_evidence = 0
    for key, payload in possibility_family_map.items():
        item = dict(payload or {})
        seen = int(item.get("seen", 0) or 0)
        if seen <= 0:
            continue
        carried = int(item.get("carried", 0) or 0)
        hurt = int(item.get("hurt", 0) or 0)
        neutral_seen = int(item.get("neutral", 0) or 0)
        evidence_count = max(1, carried + hurt + neutral_seen)
        carried_weight = _float(item.get("carried_weight", carried))
        hurt_weight = _float(item.get("hurt_weight", hurt))
        neutral_weight = _float(item.get("neutral_weight", neutral_seen))
        weight_total = max(1e-9, carried_weight + hurt_weight + neutral_weight)
        confirmation = carried_weight / weight_total
        rejection = hurt_weight / weight_total
        neutral_share = neutral_weight / weight_total
        confidence = _clip01((evidence_count / 10.0) * 0.60 + (weight_total / 10.0) * 0.40)
        quality_samples = max(1.0, _float(item.get("quality_samples", 0.0), 0.0))
        avg_observation_depth = _clip01(_float(item.get("observation_depth_sum", 0.0)) / quality_samples)
        avg_reality_contact = _clip01(_float(item.get("reality_contact_sum", 0.0)) / quality_samples)
        avg_variant_maturity = _clip01(_float(item.get("variant_maturity_sum", 0.0)) / quality_samples)
        avg_variant_trust = _clip01(_float(item.get("variant_trust_sum", 0.0)) / quality_samples)
        avg_variant_caution = _clip01(_float(item.get("variant_caution_sum", 0.0)) / quality_samples)
        avg_collapse_reversibility = _clip01(_float(item.get("collapse_reversibility_sum", 0.0)) / quality_samples)
        maturity = _clip01(
            (confirmation * 0.28)
            + (avg_reality_contact * 0.20)
            + (avg_variant_maturity * 0.20)
            + (avg_observation_depth * 0.12)
            + (confidence * 0.12)
            + (neutral_share * 0.04)
            - (rejection * 0.18)
        )
        trust = _clip01(
            (confirmation * 0.34)
            + (maturity * 0.24)
            + (avg_variant_trust * 0.18)
            + (avg_reality_contact * 0.12)
            + (confidence * 0.08)
            - (rejection * 0.24)
        )
        caution = _clip01(
            (rejection * 0.34)
            + (avg_variant_caution * 0.24)
            + (avg_collapse_reversibility * 0.12)
            + ((1.0 - avg_reality_contact) * 0.10)
            - (confirmation * 0.12)
        )
        item["maturity"] = float(maturity)
        item["trust"] = float(trust)
        item["caution"] = float(caution)
        item["confirmation"] = float(confirmation)
        item["rejection"] = float(rejection)
        item["neutral_share"] = float(neutral_share)
        item["avg_observation_depth"] = float(avg_observation_depth)
        item["avg_reality_contact"] = float(avg_reality_contact)
        item["avg_variant_maturity"] = float(avg_variant_maturity)
        item["avg_variant_trust"] = float(avg_variant_trust)
        item["avg_variant_caution"] = float(avg_variant_caution)
        possibility_family_map[str(key)] = dict(item)
        score = (trust * 0.58) + (maturity * 0.28) - (caution * 0.14)
        current_score = (dominant_possibility_trust * 0.58) + (dominant_possibility_maturity * 0.28) - (dominant_possibility_caution * 0.14)
        if score > current_score:
            dominant_possibility_key = str(key)
            dominant_possibility_trust = float(trust)
            dominant_possibility_caution = float(caution)
            dominant_possibility_maturity = float(maturity)
            dominant_possibility_evidence = int(evidence_count)

    learning["possibility_trust_families"] = dict(list(possibility_family_map.items())[-80:])
    learning["dominant_possibility_variant_key"] = str(dominant_possibility_key)
    learning["dominant_possibility_variant_trust"] = float(dominant_possibility_trust)
    learning["dominant_possibility_variant_caution"] = float(dominant_possibility_caution)
    learning["dominant_possibility_variant_maturity"] = float(dominant_possibility_maturity)
    learning["dominant_possibility_variant_evidence"] = int(dominant_possibility_evidence)
    declined_resolved = int(learning.get("declined_hypothesis_resolved", 0) or 0)
    declined_saved = int(learning.get("declined_hypothesis_saved_loss", 0) or 0)
    declined_missed = int(learning.get("declined_hypothesis_missed_gain", 0) or 0)
    declined_neutral = int(learning.get("declined_hypothesis_neutral", 0) or 0)
    declined_evidence = max(1, declined_saved + declined_missed + declined_neutral)
    learning["declined_hypothesis_confirmation_without_action"] = float(_clip01(declined_missed / float(declined_evidence)))
    learning["declined_hypothesis_rejection_without_action"] = float(_clip01(declined_saved / float(declined_evidence)))
    learning["declined_hypothesis_neutral_without_action"] = float(_clip01(declined_neutral / float(declined_evidence)))
    learning["declined_hypothesis_maturity"] = float(_clip01(declined_resolved / float(max(1, resolved))))
    for side in ("LONG", "SHORT"):
        count = _bucket_count(learning, "observation_outcome_by_side", side)
        maturity = _clip01(count / float(max(1, declined_resolved)))
        confirmation = _bucket_share(learning, "observation_outcome_by_side", side, "confirmation_share")
        rejection = _bucket_share(learning, "observation_outcome_by_side", side, "rejection_share")
        learning[f"declined_{side.lower()}_hypothesis_count"] = int(count)
        learning[f"declined_{side.lower()}_hypothesis_confirmation"] = float(confirmation)
        learning[f"declined_{side.lower()}_hypothesis_rejection"] = float(rejection)
        learning[f"declined_{side.lower()}_hypothesis_maturity"] = float(maturity)
        learning[f"declined_{side.lower()}_hypothesis_edge"] = float(_clip01(confirmation - rejection))
        learning[f"declined_{side.lower()}_hypothesis_protection_edge"] = float(_clip01(rejection - confirmation))
    return dict(learning)


def resolve_pending_observations(
    *,
    pending_observations: list,
    learning: dict,
    recent_observation_learning: list,
    current_price: float,
    now_attempt: int,
    horizon: int,
) -> dict:
    if not _hypothesis_learning_enabled():
        return {
            "pending_observations": [],
            "recent_observation_learning": list(recent_observation_learning or [])[-80:],
            "observation_learning": refresh_observation_learning_summary(dict(learning or {}), []),
        }

    price = float(current_price or 0.0)
    pending = [dict(item or {}) for item in list(pending_observations or [])]
    learning = dict(learning or {})
    recent = list(recent_observation_learning or [])
    possibility_family_map = dict(learning.get("possibility_trust_families", {}) or {})

    if price <= 0.0:
        return {
            "pending_observations": pending[-120:],
            "recent_observation_learning": recent[-80:],
            "observation_learning": refresh_observation_learning_summary(learning, pending),
        }

    still_open = []
    for obs in pending:
        side = str(obs.get("side", "") or "").strip().upper()
        entry_price = float(obs.get("entry_price", 0.0) or 0.0)
        tp_price = float(obs.get("tp_price", 0.0) or 0.0)
        sl_price = float(obs.get("sl_price", 0.0) or 0.0)
        age = int(now_attempt - int(obs.get("attempt_index", now_attempt) or now_attempt))
        result = None

        if side == "LONG":
            if tp_price > 0.0 and price >= tp_price:
                result = "missed_gain"
            elif sl_price > 0.0 and price <= sl_price:
                result = "saved_loss"
        elif side == "SHORT":
            if tp_price > 0.0 and price <= tp_price:
                result = "missed_gain"
            elif sl_price > 0.0 and price >= sl_price:
                result = "saved_loss"

        if result is None and age >= horizon:
            virtual_move = 0.0
            if entry_price > 0.0:
                if side == "LONG":
                    virtual_move = price - entry_price
                elif side == "SHORT":
                    virtual_move = entry_price - price
            if virtual_move > 0.0:
                result = "missed_gain"
            elif virtual_move < 0.0:
                result = "saved_loss"
            else:
                result = "neutral"

        if result is None:
            still_open.append(obs)
            continue

        learning["resolved"] = int(learning.get("resolved", 0) or 0) + 1
        learning[result] = int(learning.get(result, 0) or 0) + 1
        learning["last_result"] = str(result)
        family_map = dict(learning.get("hypothesis_trust_families", {}) or {})
        structure_quality = _clip01(obs.get("structure_quality", 0.0))
        hypothesis_confirmation = _clip01(obs.get("hypothesis_confirmation", 0.0))
        reality_binding = _clip01(obs.get("reality_binding", 0.0))
        structural_grounding = _clip01(obs.get("structural_grounding", 0.0))
        afterimage_maturity = _clip01(obs.get("afterimage_action_maturity", 0.0))
        future_variant_pressure = _clip01(obs.get("future_variant_pressure", 0.0))
        possibility_observation_depth = _clip01(obs.get("possibility_observation_depth", 0.0))
        possibility_reality_contact = _clip01(obs.get("possibility_reality_contact", 0.0))
        possibility_variant_maturity = _clip01(obs.get("possibility_variant_maturity", 0.0))
        possibility_variant_trust = _clip01(obs.get("possibility_variant_trust", 0.0))
        possibility_variant_caution = _clip01(obs.get("possibility_variant_caution", 0.0))
        possibility_collapse_reversibility = _clip01(obs.get("possibility_collapse_reversibility", 0.0))
        sample_weight = _clip01(
            0.42
            + (structure_quality * 0.18)
            + (hypothesis_confirmation * 0.14)
            + (reality_binding * 0.10)
            + (structural_grounding * 0.08)
            + (afterimage_maturity * 0.06)
            + (future_variant_pressure * 0.02)
            + (possibility_reality_contact * 0.05)
            + (possibility_observation_depth * 0.03)
        )
        quality_signal = _clip01(
            (structure_quality * 0.32)
            + (hypothesis_confirmation * 0.22)
            + (reality_binding * 0.18)
            + (structural_grounding * 0.16)
            + (afterimage_maturity * 0.08)
            + (future_variant_pressure * 0.04)
        )
        observation_status = str(obs.get("status", "-") or "-").strip().lower() or "-"
        rejection_reason = str(obs.get("rejection_reason", "-") or "-").strip() or "-"
        consent_state = str(obs.get("inner_action_consent_state", "-") or "-").strip() or "-"
        possibility_state = str(obs.get("possibility_field_state", "-") or "-").strip() or "-"
        possibility_observer_state = str(obs.get("possibility_observer_state", "-") or "-").strip() or "-"
        possibility_direction = str(obs.get("possibility_dominant_direction", "-") or "-").strip().upper() or "-"
        possibility_variant_id = str(obs.get("possibility_dominant_variant_id", "-") or "-").strip() or "-"
        possibility_reason = str(obs.get("possibility_collapse_reason", "-") or "-").strip() or "-"
        side_bucket = side if side in ("LONG", "SHORT") else "-"
        action_bucket = f"{side_bucket}:{observation_status}"
        reason_action_bucket = f"{side_bucket}:{rejection_reason}"
        possibility_family_key = str(obs.get("possibility_family_key", "") or "").strip()
        if not possibility_family_key:
            possibility_family_key = f"{possibility_direction}:{possibility_variant_id}:{possibility_reason}"
        _bump_observation_bucket(learning, "observation_outcome_by_status", observation_status, result, sample_weight)
        _bump_observation_bucket(learning, "observation_outcome_by_side", side_bucket, result, sample_weight)
        _bump_observation_bucket(learning, "observation_outcome_by_action_state", action_bucket, result, sample_weight)
        _bump_observation_bucket(learning, "observation_outcome_by_rejection_reason", rejection_reason, result, sample_weight)
        _bump_observation_bucket(learning, "observation_outcome_by_side_rejection_reason", reason_action_bucket, result, sample_weight)
        _bump_observation_bucket(learning, "observation_outcome_by_consent_state", consent_state, result, sample_weight)
        _bump_observation_bucket(learning, "observation_outcome_by_possibility_state", possibility_state, result, sample_weight)
        _bump_observation_bucket(learning, "observation_outcome_by_possibility_observer", possibility_observer_state, result, sample_weight)
        _bump_observation_bucket(learning, "observation_outcome_by_possibility_direction", possibility_direction, result, sample_weight)
        _bump_observation_bucket(learning, "observation_outcome_by_possibility_variant", possibility_family_key, result, sample_weight)
        if observation_status in ("observed_only", "replanned", "withheld") and (
            rejection_reason not in ("", "-") or consent_state not in ("", "-")
        ):
            learning["declined_hypothesis_resolved"] = int(learning.get("declined_hypothesis_resolved", 0) or 0) + 1
            learning[f"declined_hypothesis_{result}"] = int(learning.get(f"declined_hypothesis_{result}", 0) or 0) + 1
        thought_trace = _hypothesis_thought_trace(obs)
        for family_key in _hypothesis_family_keys(obs):
            family = dict(family_map.get(family_key, {}) or {})
            family["seen"] = int(family.get("seen", 0) or 0) + 1
            if result == "missed_gain":
                family["carried"] = int(family.get("carried", 0) or 0) + 1
                family["carried_weight"] = _float(family.get("carried_weight", 0.0)) + sample_weight
            elif result == "saved_loss":
                family["hurt"] = int(family.get("hurt", 0) or 0) + 1
                family["hurt_weight"] = _float(family.get("hurt_weight", 0.0)) + sample_weight
            else:
                family["neutral"] = int(family.get("neutral", 0) or 0) + 1
                family["neutral_weight"] = _float(family.get("neutral_weight", 0.0)) + sample_weight
            family["quality_samples"] = _float(family.get("quality_samples", 0.0)) + 1.0
            family["quality_sum"] = _float(family.get("quality_sum", 0.0)) + quality_signal
            family["confirmation_quality_sum"] = _float(family.get("confirmation_quality_sum", 0.0)) + hypothesis_confirmation
            family["reality_binding_sum"] = _float(family.get("reality_binding_sum", 0.0)) + reality_binding
            family["afterimage_maturity_sum"] = _float(family.get("afterimage_maturity_sum", 0.0)) + afterimage_maturity
            family["side"] = str(side or "-")
            family["structure_bucket"] = str(obs.get("structure_bucket", "") or "")
            family["last_result"] = str(result)
            family["last_structure_quality"] = float(structure_quality)
            family["last_quality_signal"] = float(quality_signal)
            family["last_thought_trace"] = dict(thought_trace)
            trace_counts = dict(family.get("thought_trace_counts", {}) or {})
            trace_key = ":".join(
                str(part or "-")
                for part in (
                    thought_trace.get("entry_mode", "-"),
                    thought_trace.get("entry_choice_state", "-"),
                    thought_trace.get("strategic_entry_location", "-"),
                )
            )
            trace_item = dict(trace_counts.get(trace_key, {}) or {})
            trace_item["seen"] = int(trace_item.get("seen", 0) or 0) + 1
            trace_item[result] = int(trace_item.get(result, 0) or 0) + 1
            trace_item["last_result"] = str(result)
            trace_counts[trace_key] = dict(trace_item)
            family["thought_trace_counts"] = dict(list(trace_counts.items())[-24:])
            family_map[family_key] = dict(family)
        possibility_family = dict(possibility_family_map.get(possibility_family_key, {}) or {})
        possibility_family["seen"] = int(possibility_family.get("seen", 0) or 0) + 1
        if result == "missed_gain":
            possibility_family["carried"] = int(possibility_family.get("carried", 0) or 0) + 1
            possibility_family["carried_weight"] = _float(possibility_family.get("carried_weight", 0.0)) + sample_weight
        elif result == "saved_loss":
            possibility_family["hurt"] = int(possibility_family.get("hurt", 0) or 0) + 1
            possibility_family["hurt_weight"] = _float(possibility_family.get("hurt_weight", 0.0)) + sample_weight
        else:
            possibility_family["neutral"] = int(possibility_family.get("neutral", 0) or 0) + 1
            possibility_family["neutral_weight"] = _float(possibility_family.get("neutral_weight", 0.0)) + sample_weight
        possibility_family["quality_samples"] = _float(possibility_family.get("quality_samples", 0.0)) + 1.0
        possibility_family["observation_depth_sum"] = _float(possibility_family.get("observation_depth_sum", 0.0)) + possibility_observation_depth
        possibility_family["reality_contact_sum"] = _float(possibility_family.get("reality_contact_sum", 0.0)) + possibility_reality_contact
        possibility_family["variant_maturity_sum"] = _float(possibility_family.get("variant_maturity_sum", 0.0)) + possibility_variant_maturity
        possibility_family["variant_trust_sum"] = _float(possibility_family.get("variant_trust_sum", 0.0)) + possibility_variant_trust
        possibility_family["variant_caution_sum"] = _float(possibility_family.get("variant_caution_sum", 0.0)) + possibility_variant_caution
        possibility_family["collapse_reversibility_sum"] = _float(possibility_family.get("collapse_reversibility_sum", 0.0)) + possibility_collapse_reversibility
        possibility_family["direction"] = str(possibility_direction)
        possibility_family["state"] = str(possibility_state)
        possibility_family["observer_state"] = str(possibility_observer_state)
        possibility_family["collapse_reason"] = str(possibility_reason)
        possibility_family["last_result"] = str(result)
        possibility_family_map[possibility_family_key] = dict(possibility_family)
        learning["hypothesis_trust_families"] = dict(list(family_map.items())[-80:])
        learning["possibility_trust_families"] = dict(list(possibility_family_map.items())[-80:])
        recent.append({
            "result": str(result),
            "age": int(age),
            "side": str(side or "-"),
            "structure_quality": float(obs.get("structure_quality", 0.0) or 0.0),
            "structure_bucket": str(obs.get("structure_bucket", "") or ""),
            "entry_price": float(entry_price),
            "tp_price": float(tp_price),
            "sl_price": float(sl_price),
            "rr_value": float(abs(tp_price - entry_price) / max(abs(entry_price - sl_price), 1e-9)),
            "entry_mode": str(obs.get("entry_mode", "") or ""),
            "entry_choice_state": str(obs.get("entry_choice_state", "") or ""),
            "strategic_area_focus_id": str(obs.get("strategic_area_focus_id", "") or ""),
            "strategic_entry_location": str(obs.get("strategic_entry_location", "") or ""),
            "current_price": float(price),
            "form_symbol_id": str(obs.get("form_symbol_id", "") or ""),
            "form_symbol_compound_id": str(obs.get("form_symbol_compound_id", "") or ""),
            "status": str(obs.get("status", "") or ""),
            "rejection_reason": str(obs.get("rejection_reason", "") or ""),
            "inner_action_consent_state": str(obs.get("inner_action_consent_state", "") or ""),
            "hypothesis_quality_signal": float(quality_signal),
            "possibility_field_state": str(possibility_state),
            "possibility_observer_state": str(possibility_observer_state),
            "possibility_dominant_direction": str(possibility_direction),
            "possibility_family_key": str(possibility_family_key),
            "possibility_reality_contact": float(possibility_reality_contact),
            "possibility_variant_maturity": float(possibility_variant_maturity),
        })

    learning = refresh_observation_learning_summary(learning, still_open)
    return {
        "pending_observations": still_open[-120:],
        "recent_observation_learning": recent[-80:],
        "observation_learning": dict(learning),
    }


__all__ = [
    "derive_open_hypothesis_learning",
    "refresh_observation_learning_summary",
    "resolve_pending_observations",
]
