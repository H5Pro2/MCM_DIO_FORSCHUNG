# Passive Bridge Separation Lupe

Passive Diagnose. Keine Runtime-Lesung, keine Handlung, kein Gate, kein Entry, keine Richtung.

## Summary

- L_FOLGEKONTAKT3 -> M_FOLGEKONTAKT4: family_carried:1|family_not_carried:1|family_visible_but_decoupled:2; edges=edge_absent:3|edge_carried:1|edge_lost:2

## Families

- dio_0325: family_visible_but_decoupled; lost=1; new=0; carried=0; sehen_delta=0.0; hoeren_delta=0.006059; mcm_delta=0.001279667
- dio_10qz: family_visible_but_decoupled; lost=1; new=0; carried=1; sehen_delta=0.001232; hoeren_delta=0.0028875; mcm_delta=0.001296
- dio_114i: family_carried; lost=0; new=0; carried=1; sehen_delta=0.0; hoeren_delta=0.0058715; mcm_delta=0.001249
- dio_1ytc: family_not_carried; lost=2; new=0; carried=0; sehen_delta=0.0; hoeren_delta=0.0; mcm_delta=0.0

## Pairs

- dio_0325 <-> dio_10qz: edge_absent
- dio_0325 <-> dio_114i: edge_absent
- dio_0325 <-> dio_1ytc: edge_lost
- dio_10qz <-> dio_114i: edge_carried
- dio_10qz <-> dio_1ytc: edge_lost
- dio_114i <-> dio_1ytc: edge_absent
