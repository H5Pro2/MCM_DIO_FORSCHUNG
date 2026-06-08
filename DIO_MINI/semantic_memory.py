"""Semantic episodic memory for the mini DIO core.

The memory stores DIO-owned symbols. Human-readable labels are only generated
for reports; the decision loop uses the symbols and their learned action
statistics.
"""

from __future__ import annotations

import json
from pathlib import Path


ACTION_NAMES = ("WAIT", "LONG", "SHORT")


def _clip(value: float, lo: float = -1.0, hi: float = 1.0) -> float:
    try:
        value = float(value)
    except Exception:
        value = 0.0
    if value != value:
        value = 0.0
    return max(lo, min(hi, value))


def _base36(number: int) -> str:
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    number = abs(int(number))
    if number == 0:
        return "0"
    chars = []
    while number:
        number, rem = divmod(number, 36)
        chars.append(alphabet[rem])
    return "".join(reversed(chars))


def make_syntax_vector(senses: dict, field_signature: float) -> list[float]:
    """Return DIO's compact sensory vector.

    This is not a strategy description. It is a normalized form of
    sehen/hoeren/fuehlen plus the current MCM field signature.
    """

    return [
        _clip(value)
        for value in [
            senses.get("sehen", {}).get("form_flow", 0.0),
            senses.get("sehen", {}).get("form_stability", 0.0),
            senses.get("sehen", {}).get("form_change", 0.0),
            senses.get("hoeren", {}).get("energy_tone", 0.0),
            senses.get("hoeren", {}).get("energy_shift", 0.0),
            senses.get("fuehlen", {}).get("mcm_coherence", 0.0),
            senses.get("fuehlen", {}).get("mcm_tension", 0.0),
            senses.get("fuehlen", {}).get("mcm_asymmetry", 0.0),
            field_signature,
        ]
    ]


def make_syntax_symbol(senses: dict, field_signature: float) -> str:
    """Create a compact internal symbol from sensed state.

    The buckets are not strategy labels. They only compress sehen/hoeren/
    fuehlen into a repeatable internal word.
    """

    values = make_syntax_vector(senses, field_signature)
    buckets = [int(round((_clip(v) + 1.0) * 8.0)) for v in values]
    hash_value = 2166136261
    for bucket in buckets:
        hash_value ^= bucket + 17
        hash_value = (hash_value * 16777619) & 0xFFFFFFFF
    return f"dio_{_base36(hash_value).rjust(7, '0')}"


def make_contact_lage_symbol(payload: dict) -> str:
    """Create DIO-owned syntax for a passive contact-lage."""

    state = str(payload.get("contact_lage_state", "") or "")
    values = [
        len(state),
        int(payload.get("runs", 0) or 0),
        int(payload.get("trades_total", 0) or 0),
        int(payload.get("direct_positive_action", 0) or 0),
        int(payload.get("observation_to_positive_action", 0) or 0),
        int(payload.get("held_observation", 0) or 0),
        int(round(float(payload.get("contact_reward_sum", 0.0) or 0.0) * 1000.0)),
    ]
    hash_value = 2166136261
    for value in values:
        hash_value ^= abs(int(value)) + 31
        hash_value = (hash_value * 16777619) & 0xFFFFFFFF
    return f"dio_contact_{_base36(hash_value).rjust(7, '0')}"


def make_reflection_seed_symbol(payload: dict) -> str:
    """Create DIO-owned syntax for a passive reflection seed."""

    family = str(payload.get("symbol_family", "") or "")
    state = str(payload.get("reflection_state", "") or "")
    values = [
        len(family),
        len(state),
        int(payload.get("prior_observation_count", 0) or 0),
        int(payload.get("prior_execution_count", 0) or 0),
        int(payload.get("followup_seen_count", 0) or 0),
        int(payload.get("followup_executed_aligned_count", 0) or 0),
        int(round(float(payload.get("prior_execution_reward_sum", 0.0) or 0.0) * 1000.0)),
        int(round(float(payload.get("followup_executed_reward", 0.0) or 0.0) * 1000.0)),
    ]
    hash_value = 2166136261
    for char in f"{family}|{state}":
        hash_value ^= ord(char) + 43
        hash_value = (hash_value * 16777619) & 0xFFFFFFFF
    for value in values:
        hash_value ^= abs(int(value)) + 43
        hash_value = (hash_value * 16777619) & 0xFFFFFFFF
    return f"dio_reflect_{_base36(hash_value).rjust(7, '0')}"


def make_reflection_map_symbol(payload: dict) -> str:
    """Create DIO-owned syntax for a passive reflection-map snapshot."""

    family = str(payload.get("symbol_family", "") or "")
    state = str(payload.get("reflection_map_state", "") or "")
    reason = str(payload.get("reflection_map_reason", "") or "")
    source_probe = str(payload.get("source_probe", "") or "")
    values = [
        len(family),
        len(state),
        len(reason),
        len(source_probe),
        int(payload.get("seen_count", 0) or 0),
        int(payload.get("executed_count", 0) or 0),
        int(payload.get("observed_count", 0) or 0),
        int(round(float(payload.get("reward_sum", 0.0) or 0.0) * 1000.0)),
        int(round(float(payload.get("best_reward_sum", 0.0) or 0.0) * 1000.0)),
    ]
    hash_value = 2166136261
    for char in f"{family}|{state}|{reason}|{source_probe}":
        hash_value ^= ord(char) + 47
        hash_value = (hash_value * 16777619) & 0xFFFFFFFF
    for value in values:
        hash_value ^= abs(int(value)) + 47
        hash_value = (hash_value * 16777619) & 0xFFFFFFFF
    return f"dio_rmap_{_base36(hash_value).rjust(7, '0')}"


def _vector_distance(left: list[float], right: list[float]) -> float:
    if not left or not right:
        return 1.0
    size = min(len(left), len(right))
    if size <= 0:
        return 1.0
    return sum(abs(_clip(left[i]) - _clip(right[i])) for i in range(size)) / size


def _update_vector(record: dict, vector: list[float], count: int) -> None:
    if not vector:
        return
    previous = record.get("vector")
    if not isinstance(previous, list) or len(previous) != len(vector):
        record["vector"] = [_clip(value) for value in vector]
        return
    weight_old = max(1, int(count) - 1)
    weight_new = 1
    denom = weight_old + weight_new
    record["vector"] = [
        _clip(((float(previous[i]) * weight_old) + (_clip(vector[i]) * weight_new)) / denom)
        for i in range(len(vector))
    ]


def _action_signal(record: dict, action: str) -> float:
    state = dict(dict(record.get("actions", {}) or {}).get(action, {}) or {})
    trust = float(state.get("trust", 0.0) or 0.0)
    caution = float(state.get("caution", 0.0) or 0.0)
    count = int(state.get("count", 0) or 0)
    familiarity = min(1.0, count / 6.0)
    return (trust - caution) * familiarity


def _observation_signal(record: dict, action: str) -> float:
    observations = _ensure_observations(record)
    state = dict(observations.get(action, {}) or {})
    count = int(state.get("count", 0) or 0)
    if count <= 0:
        return 0.0
    recognition_avg = float(state.get("recognition_sum", 0.0) or 0.0) / max(1, count)
    reward_avg = float(state.get("reward_sum", 0.0) or 0.0) / max(1, count)
    familiarity = min(1.0, count / 8.0)
    return _clip(recognition_avg * reward_avg * familiarity, -1.0, 1.0)


def _associative_signal(records: list[dict], action: str, vector: list[float]) -> float:
    if not vector:
        return 0.0
    weighted = 0.0
    weight_sum = 0.0
    for record in records:
        record_vector = record.get("vector")
        if not isinstance(record_vector, list):
            continue
        distance = _vector_distance(vector, record_vector)
        weight = 1.0 / (1.0 + (distance * distance * 12.0))
        signal = _action_signal(record, action)
        weighted += signal * weight
        weight_sum += weight
    if weight_sum <= 0.0:
        return 0.0
    return _clip(weighted / weight_sum, -1.0, 1.0)


def _sensor_relation_rank(item: dict) -> tuple:
    kind = str(item.get("relation_kind", "") or "")
    return (
        kind == "same_family_cross_phase",
        kind == "bearing_sensor_neighbor",
        float(item.get("sensor_relation_trace", 0.0) or 0.0),
        int(item.get("left_executed", 0) or 0) + int(item.get("right_executed", 0) or 0),
        float(item.get("left_reward", 0.0) or 0.0) + float(item.get("right_reward", 0.0) or 0.0),
    )


def _neighbor_consequence_rank(item: dict) -> tuple:
    state = str(item.get("neighbor_consequence_state", "") or "")
    return (
        state == "reifende_verwandtschaft",
        state == "vorsichtige_verwandtschaft",
        state == "beobachtete_verwandtschaft",
        float(item.get("sensor_similarity", 0.0) or 0.0),
        float(item.get("target_reward_sum", 0.0) or 0.0),
        float(item.get("reference_reward_sum", 0.0) or 0.0),
    )


def _contact_lage_rank(item: dict) -> tuple:
    state = str(item.get("contact_lage_state", "") or "")
    return (
        state == "exakte_wiederbegegnung",
        state == "nahe_aehnlichkeit",
        state == "ferne_aehnlichkeit",
        float(item.get("contact_reward_sum", 0.0) or 0.0),
        int(item.get("direct_positive_action", 0) or 0),
        int(item.get("observation_to_positive_action", 0) or 0),
        int(item.get("held_observation", 0) or 0),
    )


def _reflection_seed_rank(item: dict) -> tuple:
    state = str(item.get("reflection_state", "") or "")
    return (
        state == "reflection_seed_reconfirmed",
        state == "reflection_seed_overheld",
        float(item.get("followup_executed_reward", 0.0) or 0.0),
        int(item.get("followup_executed_aligned_count", 0) or 0),
        float(item.get("prior_execution_reward_sum", 0.0) or 0.0),
        int(item.get("prior_execution_count", 0) or 0),
    )


def _reflection_map_rank(item: dict) -> tuple:
    state = str(item.get("reflection_map_state", "") or "")
    return (
        state == "reflection_memory_reconfirmed",
        state == "reflection_memory_conflict",
        state == "reflection_memory_observed",
        float(item.get("reward_sum", 0.0) or 0.0),
        int(item.get("seen_count", 0) or 0),
        int(item.get("executed_count", 0) or 0),
    )


def _temporal_family_rank(item: dict) -> tuple:
    return (
        float(item.get("max_temporal_trust_support", 0.0) or 0.0),
        float(item.get("max_afterimage", 0.0) or 0.0),
        int(item.get("seen_count", 0) or 0),
        -float(item.get("max_temporal_caution_support", 0.0) or 0.0),
    )


def _compact_record(record: dict) -> dict:
    compact = dict(record)
    compact.pop("vector", None)
    return compact


def _default_action_map() -> dict:
    return {
        action: {
            "count": 0,
            "reward_sum": 0.0,
            "trust": 0.0,
            "caution": 0.0,
            "last_reward": 0.0,
            "timing_improvement_sum": 0.0,
            "last_timing_improvement": 0.0,
        }
        for action in ACTION_NAMES
    }


def _default_observation_map() -> dict:
    return {
        action: {
            "count": 0,
            "recognition_sum": 0.0,
            "reward_sum": 0.0,
            "last_recognition": 0.0,
            "last_reward": 0.0,
        }
        for action in ACTION_NAMES
    }


def _ensure_action_defaults(record: dict) -> dict:
    actions = record.setdefault("actions", {})
    defaults = _default_action_map()
    for action in ACTION_NAMES:
        state = actions.setdefault(action, {})
        for key, value in defaults[action].items():
            state.setdefault(key, value)
    return actions


def _ensure_observations(record: dict) -> dict:
    observations = record.setdefault("observations", {})
    for action in ACTION_NAMES:
        observations.setdefault(
            action,
            {
                "count": 0,
                "recognition_sum": 0.0,
                "reward_sum": 0.0,
                "last_recognition": 0.0,
                "last_reward": 0.0,
            },
        )
    return observations


class SemanticMemory:
    def __init__(self, path: str | Path, max_symbols: int = 2048):
        self.path = Path(path)
        self.max_symbols = int(max_symbols)
        self.data = {
            "version": 1,
            "runs": 0,
            "symbols": {},
            "families": {},
            "relations": {},
            "sensor_relations": {},
            "neighbor_consequences": {},
            "contact_lagen": {},
            "sentence_traces": {},
            "reflection_seeds": {},
            "reflection_maps": {},
            "temporal_families": {},
        }
        self.max_sensor_relations = 128
        self.max_neighbor_consequences = 128
        self.max_contact_lagen = 64
        self.max_sentence_traces = 128
        self.max_reflection_seeds = 64
        self.max_reflection_maps = 96
        self.max_temporal_families = 128

    def load(self) -> None:
        if not self.path.exists():
            return
        try:
            loaded = json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return
        if isinstance(loaded, dict):
            self.data.update(loaded)
            self.data.setdefault("symbols", {})
            self.data.setdefault("families", {})
            self.data.setdefault("relations", {})
            self.data.setdefault("sensor_relations", {})
            self.data.setdefault("neighbor_consequences", {})
            self.data.setdefault("contact_lagen", {})
            self.data.setdefault("sentence_traces", {})
            self.data.setdefault("reflection_seeds", {})
            self.data.setdefault("reflection_maps", {})
            self.data.setdefault("temporal_families", {})

    def family_record(self, family: str) -> dict:
        family = str(family or "-") or "-"
        families = self.data.setdefault("families", {})
        record = families.get(family)
        if not isinstance(record, dict):
            record = {
                "family": family,
                "count": 0,
                "actions": _default_action_map(),
                "observations": _default_observation_map(),
            }
            families[family] = record
        _ensure_observations(record)
        _ensure_action_defaults(record)
        return record

    def set_relation_summary(self, support_pair: str, summary: dict) -> None:
        """Store passive relation memory.

        Relations are a reflection map only. They are intentionally not read by
        action_diagnostics, action_bias or action_readiness.
        """

        support_pair = str(support_pair or "-") or "-"
        if support_pair == "-":
            return
        relations = self.data.setdefault("relations", {})
        relations[support_pair] = {
            "support_pair": support_pair,
            "families": list(summary.get("families", []) or []),
            "phases": list(summary.get("phases", []) or []),
            "phase_count": int(summary.get("phase_count", 0) or 0),
            "rows": int(summary.get("rows", 0) or 0),
            "executed_local_confirmation": int(summary.get("executed_local_confirmation", 0) or 0),
            "observed_related_potential": int(summary.get("observed_related_potential", 0) or 0),
            "long_local": int(summary.get("long_local", 0) or 0),
            "short_local": int(summary.get("short_local", 0) or 0),
            "avg_local_confirmation": float(summary.get("avg_local_confirmation", 0.0) or 0.0),
            "max_local_confirmation": float(summary.get("max_local_confirmation", 0.0) or 0.0),
            "reward_sum": float(summary.get("reward_sum", 0.0) or 0.0),
            "passive_only": True,
        }

    def set_sensor_relation_summary(self, relation_key: str, summary: dict) -> None:
        """Store passive sensor-neighbor relation memory.

        Sensor relations are not read by action_diagnostics. They only preserve
        which DIO-owned families looked similar across sehen/hoeren/fuehlen.
        """

        relation_key = str(relation_key or "-") or "-"
        if relation_key == "-":
            return
        relations = self.data.setdefault("sensor_relations", {})
        relations[relation_key] = {
            "relation_key": relation_key,
            "left_family": str(summary.get("left_family", "-") or "-"),
            "right_family": str(summary.get("right_family", "-") or "-"),
            "left_phase": str(summary.get("left_phase", "-") or "-"),
            "right_phase": str(summary.get("right_phase", "-") or "-"),
            "relation_kind": str(summary.get("relation_kind", "-") or "-"),
            "sensor_relation_trace": float(summary.get("sensor_relation_trace", 0.0) or 0.0),
            "sensor_distance": float(summary.get("sensor_distance", 0.0) or 0.0),
            "visual_mcm_gap": float(summary.get("visual_mcm_gap", 0.0) or 0.0),
            "tone_tension_gap": float(summary.get("tone_tension_gap", 0.0) or 0.0),
            "left_reward": float(summary.get("left_reward", 0.0) or 0.0),
            "right_reward": float(summary.get("right_reward", 0.0) or 0.0),
            "left_executed": int(summary.get("left_executed", 0) or 0),
            "right_executed": int(summary.get("right_executed", 0) or 0),
            "passive_only": True,
        }
        self.compact_sensor_relations()

    def set_neighbor_consequence_summary(self, relation_key: str, summary: dict) -> None:
        """Store passive consequence-bound sensor-neighbor memory.

        Neighbor consequences are not read by action_diagnostics. They preserve
        whether a sensor-near relation is only observed, reifying, cautious, or
        still open.
        """

        relation_key = str(relation_key or "-") or "-"
        if relation_key == "-":
            return
        relations = self.data.setdefault("neighbor_consequences", {})
        relations[relation_key] = {
            "relation_key": relation_key,
            "target_family": str(summary.get("target_family", "-") or "-"),
            "reference_family": str(summary.get("reference_family", "-") or "-"),
            "neighbor_consequence_state": str(summary.get("neighbor_consequence_state", "-") or "-"),
            "sensor_distance": float(summary.get("sensor_distance", 0.0) or 0.0),
            "sensor_similarity": float(summary.get("sensor_similarity", 0.0) or 0.0),
            "target_reward_sum": float(summary.get("target_reward_sum", 0.0) or 0.0),
            "reference_reward_sum": float(summary.get("reference_reward_sum", 0.0) or 0.0),
            "target_executed_rows": int(summary.get("target_executed_rows", 0) or 0),
            "target_observed_rows": int(summary.get("target_observed_rows", 0) or 0),
            "reference_executed_rows": int(summary.get("reference_executed_rows", 0) or 0),
            "reference_observed_rows": int(summary.get("reference_observed_rows", 0) or 0),
            "target_class": str(summary.get("target_class", "-") or "-"),
            "reference_class": str(summary.get("reference_class", "-") or "-"),
            "target_phases": str(summary.get("target_phases", "-") or "-"),
            "reference_phases": str(summary.get("reference_phases", "-") or "-"),
            "passive_only": True,
        }
        self.compact_neighbor_consequences()

    def compact_neighbor_consequences(self, max_relations: int | None = None) -> dict:
        """Keep the passive neighbor-consequence map compact."""

        limit = int(max_relations if max_relations is not None else self.max_neighbor_consequences)
        limit = max(1, limit)
        relations = self.data.setdefault("neighbor_consequences", {})
        if not isinstance(relations, dict):
            self.data["neighbor_consequences"] = {}
            return {"before": 0, "after": 0, "removed": 0}
        before = len(relations)
        if before <= limit:
            return {"before": before, "after": before, "removed": 0}
        sorted_items = sorted(
            relations.items(),
            key=lambda item: _neighbor_consequence_rank(dict(item[1] or {})),
            reverse=True,
        )
        kept = dict(sorted_items[:limit])
        self.data["neighbor_consequences"] = kept
        after = len(kept)
        return {"before": before, "after": after, "removed": before - after}

    def compact_sensor_relations(self, max_relations: int | None = None) -> dict:
        """Keep the passive sensor relation map compact."""

        limit = int(max_relations if max_relations is not None else self.max_sensor_relations)
        limit = max(1, limit)
        relations = self.data.setdefault("sensor_relations", {})
        if not isinstance(relations, dict):
            self.data["sensor_relations"] = {}
            return {"before": 0, "after": 0, "removed": 0}
        before = len(relations)
        if before <= limit:
            return {"before": before, "after": before, "removed": 0}
        sorted_items = sorted(relations.items(), key=lambda item: _sensor_relation_rank(dict(item[1] or {})), reverse=True)
        kept = dict(sorted_items[:limit])
        self.data["sensor_relations"] = kept
        after = len(kept)
        return {"before": before, "after": after, "removed": before - after}

    def compact_contact_lagen(self, max_relations: int | None = None) -> dict:
        """Keep the passive contact-lage map compact."""

        limit = int(max_relations if max_relations is not None else self.max_contact_lagen)
        limit = max(1, limit)
        relations = self.data.setdefault("contact_lagen", {})
        if not isinstance(relations, dict):
            self.data["contact_lagen"] = {}
            return {"before": 0, "after": 0, "removed": 0}
        before = len(relations)
        if before <= limit:
            return {"before": before, "after": before, "removed": 0}
        sorted_items = sorted(relations.items(), key=lambda item: _contact_lage_rank(dict(item[1] or {})), reverse=True)
        kept = dict(sorted_items[:limit])
        self.data["contact_lagen"] = kept
        after = len(kept)
        return {"before": before, "after": after, "removed": before - after}

    def compact_sentence_traces(self, max_relations: int | None = None) -> dict:
        """Keep the passive sentence trace map compact."""

        limit = int(max_relations if max_relations is not None else self.max_sentence_traces)
        limit = max(1, limit)
        traces = self.data.setdefault("sentence_traces", {})
        if not isinstance(traces, dict):
            self.data["sentence_traces"] = {}
            return {"before": 0, "after": 0, "removed": 0}
        before = len(traces)
        if before <= limit:
            return {"before": before, "after": before, "removed": 0}
        sorted_items = sorted(
            traces.items(),
            key=lambda item: (
                float(dict(item[1] or {}).get("reward_sum", 0.0) or 0.0),
                int(dict(item[1] or {}).get("count", 0) or 0),
                str(dict(item[1] or {}).get("episode_contact_state", "") or "") == "kontakt_handlung_bestaetigt",
            ),
            reverse=True,
        )
        kept = dict(sorted_items[:limit])
        self.data["sentence_traces"] = kept
        after = len(kept)
        return {"before": before, "after": after, "removed": before - after}

    def compact_reflection_seeds(self, max_relations: int | None = None) -> dict:
        """Keep passive reflection seeds compact."""

        limit = int(max_relations if max_relations is not None else self.max_reflection_seeds)
        limit = max(1, limit)
        seeds = self.data.setdefault("reflection_seeds", {})
        if not isinstance(seeds, dict):
            self.data["reflection_seeds"] = {}
            return {"before": 0, "after": 0, "removed": 0}
        before = len(seeds)
        if before <= limit:
            return {"before": before, "after": before, "removed": 0}
        sorted_items = sorted(
            seeds.items(),
            key=lambda item: _reflection_seed_rank(dict(item[1] or {})),
            reverse=True,
        )
        kept = dict(sorted_items[:limit])
        self.data["reflection_seeds"] = kept
        after = len(kept)
        return {"before": before, "after": after, "removed": before - after}

    def compact_reflection_maps(self, max_relations: int | None = None) -> dict:
        """Keep passive reflection-map snapshots compact."""

        limit = int(max_relations if max_relations is not None else self.max_reflection_maps)
        limit = max(1, limit)
        maps = self.data.setdefault("reflection_maps", {})
        if not isinstance(maps, dict):
            self.data["reflection_maps"] = {}
            return {"before": 0, "after": 0, "removed": 0}
        before = len(maps)
        if before <= limit:
            return {"before": before, "after": before, "removed": 0}
        sorted_items = sorted(maps.items(), key=lambda item: _reflection_map_rank(dict(item[1] or {})), reverse=True)
        kept = dict(sorted_items[:limit])
        self.data["reflection_maps"] = kept
        after = len(kept)
        return {"before": before, "after": after, "removed": before - after}

    def compact_temporal_families(self, max_relations: int | None = None) -> dict:
        """Keep passive temporal family traces compact."""

        limit = int(max_relations if max_relations is not None else self.max_temporal_families)
        limit = max(1, limit)
        families = self.data.setdefault("temporal_families", {})
        if not isinstance(families, dict):
            self.data["temporal_families"] = {}
            return {"before": 0, "after": 0, "removed": 0}
        before = len(families)
        if before <= limit:
            return {"before": before, "after": before, "removed": 0}
        sorted_items = sorted(families.items(), key=lambda item: _temporal_family_rank(dict(item[1] or {})), reverse=True)
        kept = dict(sorted_items[:limit])
        self.data["temporal_families"] = kept
        after = len(kept)
        return {"before": before, "after": after, "removed": before - after}

    def save(self) -> None:
        self.compact_sensor_relations()
        self.compact_neighbor_consequences()
        self.compact_contact_lagen()
        self.compact_sentence_traces()
        self.compact_reflection_seeds()
        self.compact_reflection_maps()
        self.compact_temporal_families()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.path.with_suffix(self.path.suffix + ".tmp")
        temp_path.write_text(json.dumps(self.data, indent=2, sort_keys=True), encoding="utf-8")
        temp_path.replace(self.path)

    def mark_run(self) -> None:
        self.data["runs"] = int(self.data.get("runs", 0) or 0) + 1

    def symbol_record(self, symbol: str) -> dict:
        symbols = self.data.setdefault("symbols", {})
        record = symbols.get(symbol)
        if not isinstance(record, dict):
            record = {
                "symbol": symbol,
                "count": 0,
                "actions": _default_action_map(),
                "observations": _default_observation_map(),
                "syntax_family": symbol[:8],
            }
            symbols[symbol] = record
        _ensure_observations(record)
        _ensure_action_defaults(record)
        return record

    def action_diagnostics(self, symbol: str, action: str, vector: list[float] | None = None) -> dict:
        record = self.symbol_record(symbol)
        action_state = record.get("actions", {}).get(action, {})
        trust = float(action_state.get("trust", 0.0) or 0.0)
        caution = float(action_state.get("caution", 0.0) or 0.0)
        count = int(action_state.get("count", 0) or 0)
        familiarity = min(1.0, count / 8.0)
        family = str(record.get("syntax_family", symbol[:8]) or symbol[:8])
        family_state = self.family_record(family).get("actions", {}).get(action, {})
        family_trust = float(family_state.get("trust", 0.0) or 0.0)
        family_caution = float(family_state.get("caution", 0.0) or 0.0)
        family_count = int(family_state.get("count", 0) or 0)
        family_familiarity = min(1.0, family_count / 6.0)
        symbol_bias = (trust - caution) * (0.25 + familiarity * 0.45)
        family_bias = (family_trust - family_caution) * (0.20 + family_familiarity * 0.55)
        symbol_observation = _observation_signal(record, action)
        family_observation = _observation_signal(self.family_record(family), action)
        observation_signal = (symbol_observation * 0.35) + (family_observation * 0.65)
        family_records = list(self.data.get("families", {}).values())
        associative_raw = _associative_signal(family_records, action, vector or [])
        associative_bias = associative_raw * 0.16
        observation_bias = observation_signal * 0.08
        readiness = _clip(
            ((trust - caution) * min(1.0, count / 5.0) * 0.52)
            + ((family_trust - family_caution) * min(1.0, family_count / 5.0) * 0.41)
            + (associative_raw * 0.07),
            -1.0,
            1.0,
        )
        observation_readiness = observation_signal * 0.11
        readiness = _clip(
            readiness + observation_readiness,
            -1.0,
            1.0,
        )
        return {
            "symbol": symbol,
            "family": family,
            "action": action,
            "symbol_count": count,
            "family_count": family_count,
            "symbol_trust": trust,
            "symbol_caution": caution,
            "family_trust": family_trust,
            "family_caution": family_caution,
            "symbol_bias": symbol_bias,
            "family_bias": family_bias,
            "symbol_observation": symbol_observation,
            "family_observation": family_observation,
            "observation_signal": observation_signal,
            "observation_bias": observation_bias,
            "observation_readiness": observation_readiness,
            "associative_raw": associative_raw,
            "associative_bias": associative_bias,
            "action_bias": symbol_bias + family_bias + associative_bias + observation_bias,
            "readiness": readiness,
        }

    def action_bias(self, symbol: str, action: str, vector: list[float] | None = None) -> float:
        return float(self.action_diagnostics(symbol, action, vector=vector).get("action_bias", 0.0) or 0.0)

    def action_readiness(self, symbol: str, action: str, vector: list[float] | None = None) -> float:
        return float(self.action_diagnostics(symbol, action, vector=vector).get("readiness", 0.0) or 0.0)

    def learn(
        self,
        symbol: str,
        action: str,
        reward: float,
        *,
        shadow: bool = False,
        vector: list[float] | None = None,
        timing_improvement: float = 0.0,
    ) -> None:
        action = str(action or "WAIT").upper()
        if action not in ACTION_NAMES:
            action = "WAIT"
        record = self.symbol_record(symbol)
        record["count"] = int(record.get("count", 0) or 0) + (0 if shadow else 1)
        _update_vector(record, vector or [], int(record.get("count", 1) or 1))
        family = str(record.get("syntax_family", symbol[:8]) or symbol[:8])
        family_record = self.family_record(family)
        family_record["count"] = int(family_record.get("count", 0) or 0) + (0 if shadow else 1)
        _update_vector(family_record, vector or [], int(family_record.get("count", 1) or 1))
        actions = record.setdefault("actions", {})
        action_state = actions.setdefault(
            action,
            {
                "count": 0,
                "reward_sum": 0.0,
                "trust": 0.0,
                "caution": 0.0,
                "last_reward": 0.0,
                "timing_improvement_sum": 0.0,
                "last_timing_improvement": 0.0,
            },
        )
        family_actions = family_record.setdefault("actions", {})
        family_action_state = family_actions.setdefault(
            action,
            {
                "count": 0,
                "reward_sum": 0.0,
                "trust": 0.0,
                "caution": 0.0,
                "last_reward": 0.0,
                "timing_improvement_sum": 0.0,
                "last_timing_improvement": 0.0,
            },
        )
        alpha = 0.10 if shadow else 0.18
        family_alpha = 0.08 if shadow else 0.14
        reward = _clip(reward, -2.0, 2.0)
        timing_improvement = _clip(timing_improvement, 0.0, 1.0)
        action_state["count"] = int(action_state.get("count", 0) or 0) + 1
        action_state["reward_sum"] = float(action_state.get("reward_sum", 0.0) or 0.0) + reward
        action_state["last_reward"] = reward
        action_state["timing_improvement_sum"] = (
            float(action_state.get("timing_improvement_sum", 0.0) or 0.0) + timing_improvement
        )
        action_state["last_timing_improvement"] = timing_improvement
        family_action_state["count"] = int(family_action_state.get("count", 0) or 0) + 1
        family_action_state["reward_sum"] = float(family_action_state.get("reward_sum", 0.0) or 0.0) + reward
        family_action_state["last_reward"] = reward
        family_action_state["timing_improvement_sum"] = (
            float(family_action_state.get("timing_improvement_sum", 0.0) or 0.0) + timing_improvement
        )
        family_action_state["last_timing_improvement"] = timing_improvement
        positive = max(0.0, reward)
        negative = max(0.0, -reward)
        action_state["trust"] = _clip(
            (float(action_state.get("trust", 0.0) or 0.0) * (1.0 - alpha)) + (positive * alpha),
            0.0,
            1.0,
        )
        action_state["caution"] = _clip(
            (float(action_state.get("caution", 0.0) or 0.0) * (1.0 - alpha)) + (negative * alpha),
            0.0,
            1.0,
        )
        family_action_state["trust"] = _clip(
            (float(family_action_state.get("trust", 0.0) or 0.0) * (1.0 - family_alpha)) + (positive * family_alpha),
            0.0,
            1.0,
        )
        family_action_state["caution"] = _clip(
            (float(family_action_state.get("caution", 0.0) or 0.0) * (1.0 - family_alpha)) + (negative * family_alpha),
            0.0,
            1.0,
        )

    def learn_observation(
        self,
        symbol: str,
        action: str,
        reward: float,
        recognition: float,
        *,
        vector: list[float] | None = None,
    ) -> None:
        """Store recognized-but-unacted experience.

        This records observation and possible consequence without increasing
        direct action trust. It separates "I noticed this" from "I acted on
        this".
        """

        action = str(action or "WAIT").upper()
        if action not in ACTION_NAMES:
            action = "WAIT"
        recognition = _clip(recognition, 0.0, 1.0)
        reward = _clip(reward, -2.0, 2.0)
        if recognition <= 0.0:
            return
        record = self.symbol_record(symbol)
        family = str(record.get("syntax_family", symbol[:8]) or symbol[:8])
        family_record = self.family_record(family)
        _update_vector(record, vector or [], int(record.get("count", 0) or 0) + 1)
        _update_vector(family_record, vector or [], int(family_record.get("count", 0) or 0) + 1)
        for target in (record, family_record):
            observations = _ensure_observations(target)
            state = observations[action]
            state["count"] = int(state.get("count", 0) or 0) + 1
            state["recognition_sum"] = float(state.get("recognition_sum", 0.0) or 0.0) + recognition
            state["reward_sum"] = float(state.get("reward_sum", 0.0) or 0.0) + reward
            state["last_recognition"] = recognition
            state["last_reward"] = reward

    def store_contact_lage(self, contact_id: str, payload: dict) -> None:
        """Store passive contact-lage experience.

        This is not consumed by the motor loop. It only preserves whether a
        world contact behaved like exact recurrence, near similarity, or
        distant similarity.
        """

        contact_id = str(contact_id or "").strip()
        if not contact_id:
            return
        state = str(payload.get("contact_lage_state", "") or "")
        contact_lagen = self.data.setdefault("contact_lagen", {})
        current = dict(contact_lagen.get(contact_id, {}) or {})
        current.update(
            {
                "contact_id": contact_id,
                "contact_symbol": make_contact_lage_symbol(payload),
                "contact_lage_state": state,
                "debug_root": str(payload.get("debug_root", "") or ""),
                "passive_only": 1,
                "runs": int(payload.get("runs", current.get("runs", 0)) or 0),
                "trades_total": int(payload.get("trades_total", current.get("trades_total", 0)) or 0),
                "reward_total": float(payload.get("reward_total", current.get("reward_total", 0.0)) or 0.0),
                "contact_reward_sum": float(
                    payload.get("contact_reward_sum", current.get("contact_reward_sum", 0.0)) or 0.0
                ),
                "direct_positive_action": int(
                    payload.get("direct_positive_action", current.get("direct_positive_action", 0)) or 0
                ),
                "observation_to_positive_action": int(
                    payload.get(
                        "observation_to_positive_action",
                        current.get("observation_to_positive_action", 0),
                    )
                    or 0
                ),
                "held_observation": int(payload.get("held_observation", current.get("held_observation", 0)) or 0),
                "quiet_family": int(payload.get("quiet_family", current.get("quiet_family", 0)) or 0),
                "top_direct_action": list(payload.get("top_direct_action", current.get("top_direct_action", [])) or []),
                "top_observation_to_action": list(
                    payload.get("top_observation_to_action", current.get("top_observation_to_action", [])) or []
                ),
            }
        )
        contact_lagen[contact_id] = current

    def store_sentence_trace(self, sentence_symbol: str, payload: dict) -> None:
        """Store a passive DIO sentence trace."""

        sentence_symbol = str(sentence_symbol or "").strip()
        if not sentence_symbol:
            return
        traces = self.data.setdefault("sentence_traces", {})
        current = dict(traces.get(sentence_symbol, {}) or {})
        current.update(
            {
                "sentence_symbol": sentence_symbol,
                "contact_symbol": str(payload.get("contact_symbol", "") or ""),
                "contact_lage_state": str(payload.get("contact_lage_state", "") or ""),
                "symbol_family": str(payload.get("symbol_family", "") or ""),
                "episode_contact_state": str(payload.get("episode_contact_state", "") or ""),
                "count": int(payload.get("count", current.get("count", 0)) or 0),
                "reward_sum": float(payload.get("reward_sum", current.get("reward_sum", 0.0)) or 0.0),
                "actions": str(payload.get("actions", current.get("actions", "")) or ""),
                "passive_only": 1,
            }
        )
        traces[sentence_symbol] = current

    def store_reflection_seed(self, reflection_symbol: str, payload: dict) -> None:
        """Store a passive reflection seed.

        Reflection seeds are not consumed by action_diagnostics or choose_action.
        They preserve that a family was observed, later executed, and optionally
        reconfirmed in a follow-up world.
        """

        reflection_symbol = str(reflection_symbol or "").strip()
        if not reflection_symbol:
            return
        seeds = self.data.setdefault("reflection_seeds", {})
        current = dict(seeds.get(reflection_symbol, {}) or {})
        current.update(
            {
                "reflection_symbol": reflection_symbol,
                "symbol_family": str(payload.get("symbol_family", current.get("symbol_family", "")) or ""),
                "reflection_state": str(payload.get("reflection_state", current.get("reflection_state", "")) or ""),
                "prior_observation_count": int(
                    payload.get("prior_observation_count", current.get("prior_observation_count", 0)) or 0
                ),
                "prior_execution_count": int(
                    payload.get("prior_execution_count", current.get("prior_execution_count", 0)) or 0
                ),
                "prior_observation_reward_potential_sum": float(
                    payload.get(
                        "prior_observation_reward_potential_sum",
                        current.get("prior_observation_reward_potential_sum", 0.0),
                    )
                    or 0.0
                ),
                "prior_execution_reward_sum": float(
                    payload.get("prior_execution_reward_sum", current.get("prior_execution_reward_sum", 0.0)) or 0.0
                ),
                "followup_seen_count": int(
                    payload.get("followup_seen_count", current.get("followup_seen_count", 0)) or 0
                ),
                "followup_executed_aligned_count": int(
                    payload.get(
                        "followup_executed_aligned_count",
                        current.get("followup_executed_aligned_count", 0),
                    )
                    or 0
                ),
                "followup_executed_reward": float(
                    payload.get("followup_executed_reward", current.get("followup_executed_reward", 0.0)) or 0.0
                ),
                "followup_observed_count": int(
                    payload.get("followup_observed_count", current.get("followup_observed_count", 0)) or 0
                ),
                "followup_observed_potential": float(
                    payload.get("followup_observed_potential", current.get("followup_observed_potential", 0.0)) or 0.0
                ),
                "followup_overheld_count": int(
                    payload.get("followup_overheld_count", current.get("followup_overheld_count", 0)) or 0
                ),
                "followup_overheld_potential": float(
                    payload.get("followup_overheld_potential", current.get("followup_overheld_potential", 0.0)) or 0.0
                ),
                "followup_actions": str(payload.get("followup_actions", current.get("followup_actions", "")) or ""),
                "passive_only": 1,
            }
        )
        seeds[reflection_symbol] = current

    def store_reflection_map(self, reflection_map_symbol: str, payload: dict) -> None:
        """Store a passive reflection-map snapshot.

        Reflection maps are not consumed by action_diagnostics or choose_action.
        They preserve whether a known trace was quiet, reconfirmed, observed,
        conflicted, or unclear in a later world.
        """

        reflection_map_symbol = str(reflection_map_symbol or "").strip()
        if not reflection_map_symbol:
            return
        maps = self.data.setdefault("reflection_maps", {})
        current = dict(maps.get(reflection_map_symbol, {}) or {})
        current.update(
            {
                "reflection_map_symbol": reflection_map_symbol,
                "reflection_symbol": str(payload.get("reflection_symbol", current.get("reflection_symbol", "")) or ""),
                "symbol_family": str(payload.get("symbol_family", current.get("symbol_family", "")) or ""),
                "reflection_state": str(payload.get("reflection_state", current.get("reflection_state", "")) or ""),
                "reflection_map_state": str(
                    payload.get("reflection_map_state", current.get("reflection_map_state", "")) or ""
                ),
                "reflection_map_reason": str(
                    payload.get("reflection_map_reason", current.get("reflection_map_reason", "")) or ""
                ),
                "dio_sentence": str(payload.get("dio_sentence", current.get("dio_sentence", "")) or ""),
                "seen_count": int(payload.get("seen_count", current.get("seen_count", 0)) or 0),
                "executed_count": int(payload.get("executed_count", current.get("executed_count", 0)) or 0),
                "observed_count": int(payload.get("observed_count", current.get("observed_count", 0)) or 0),
                "reward_sum": float(payload.get("reward_sum", current.get("reward_sum", 0.0)) or 0.0),
                "best_reward_sum": float(payload.get("best_reward_sum", current.get("best_reward_sum", 0.0)) or 0.0),
                "actions": str(payload.get("actions", current.get("actions", "")) or ""),
                "runs": str(payload.get("runs", current.get("runs", "")) or ""),
                "source_probe": str(payload.get("source_probe", current.get("source_probe", "")) or ""),
                "passive_only": 1,
            }
        )
        maps[reflection_map_symbol] = current

    def store_temporal_family(self, family: str, temporal_state: dict) -> None:
        """Store passive time-depth for a DIO-owned family.

        This is not consumed by action_diagnostics. It preserves recurrence,
        time distance and afterimage so Mini-DIO can later be compared across
        controlled runs without mixing thought and reality.
        """

        family = str(family or "").strip()
        if not family:
            return
        traces = self.data.setdefault("temporal_families", {})
        current = dict(traces.get(family, {}) or {})
        seen_count = int(current.get("seen_count", 0) or 0) + 1
        trust_support = float(temporal_state.get("mini_temporal_trust_support", 0.0) or 0.0)
        caution_support = float(temporal_state.get("mini_temporal_caution_support", 0.0) or 0.0)
        afterimage = float(temporal_state.get("mini_afterimage", 0.0) or 0.0)
        current.update(
            {
                "family": family,
                "passive_only": 1,
                "seen_count": seen_count,
                "last_temporal_state": str(temporal_state.get("mini_temporal_state", "") or ""),
                "last_family_age": int(temporal_state.get("mini_family_age", 0) or 0),
                "last_ticks_since_seen": int(temporal_state.get("mini_ticks_since_family_seen", -1) or -1),
                "last_recurrence_strength": float(temporal_state.get("mini_recurrence_strength", 0.0) or 0.0),
                "last_afterimage": afterimage,
                "last_time_distance": float(temporal_state.get("mini_time_distance", 0.0) or 0.0),
                "last_temporal_form_distance": float(temporal_state.get("mini_temporal_form_distance", 0.0) or 0.0),
                "last_temporal_trust_support": trust_support,
                "last_temporal_caution_support": caution_support,
                "max_afterimage": max(float(current.get("max_afterimage", 0.0) or 0.0), afterimage),
                "max_temporal_trust_support": max(
                    float(current.get("max_temporal_trust_support", 0.0) or 0.0),
                    trust_support,
                ),
                "max_temporal_caution_support": max(
                    float(current.get("max_temporal_caution_support", 0.0) or 0.0),
                    caution_support,
                ),
            }
        )
        traces[family] = current
        self.compact_temporal_families()

    def compact_top(self, limit: int = 12) -> list[dict]:
        symbols = list(self.data.get("symbols", {}).values())
        symbols.sort(key=lambda item: int(item.get("count", 0) or 0), reverse=True)
        return [_compact_record(item) for item in symbols[:limit]]

    def compact_top_families(self, limit: int = 12) -> list[dict]:
        families = list(self.data.get("families", {}).values())
        families.sort(key=lambda item: int(item.get("count", 0) or 0), reverse=True)
        return [_compact_record(item) for item in families[:limit]]
