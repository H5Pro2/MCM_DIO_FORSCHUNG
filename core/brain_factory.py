"""Factory helpers for the MCM brain object graph."""

from __future__ import annotations


def create_mcm_brain(
    config,
    *,
    field_cls,
    cluster_detector_cls,
    memory_cls,
    self_model_cls,
    attractor_system_cls,
    regulation_layer_cls,
):
    field = field_cls(
        n_agents=int(getattr(config, "MCM_FIELD_NEURON", 80) or 80),
        dims=int(getattr(config, "MCM_FIELD_DIMS", 3) or 3),
    )

    field.coupling = float(getattr(config, "MCM_COUPLING", field.coupling) or field.coupling)
    field.noise = float(getattr(config, "MCM_NOISE", field.noise) or field.noise)
    field.k_center = float(getattr(config, "MCM_CENTER_FORCE", field.k_center) or field.k_center)

    return {
        "field": field,
        "cluster": cluster_detector_cls(),
        "memory": memory_cls(),
        "self_model": self_model_cls(),
        "attractor": attractor_system_cls(),
        "regulation": regulation_layer_cls(),
    }
