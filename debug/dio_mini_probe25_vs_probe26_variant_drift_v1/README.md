# Probe25 vs Probe26 - kontrollierte Signaturdrift

Ziel: Pr?fen, ob Mini-DIO bei ?hnlicher, aber sensorisch leicht ver?nderter Welt nicht nur auswendig wiederholt.

Referenz: `debug/dio_mini_repro_fresh_probe25_20260606`
Variante: `debug/dio_mini_variant_probe26_fresh_20260606`

Befund:
- Episoden verglichen: 36
- gleiche exakte Symbole: 10 / 36
- gleiche Symbolfamilien: 10 / 36
- gleiche Trainingsrichtung: 34 / 36
- durchschnittliche Sensor-/MCM-Abweichung: 0.03798325
- maximale Sensor-/MCM-Abweichung: 0.131711

Zust?nde:
- controlled_family_drift: 14
- name_drift_low_sensor_delta: 8
- same_family_under_variation: 10
- strong_family_drift: 4

Interpretation:
Mini-DIO wiederholt die Probe25-Syntax nicht stumpf. Bei Probe26 bleiben einige Familien stabil, andere driften. Das ist fachlich das gew?nschte Verhalten: ?hnliche Form-/Feldlagen behalten N?he, echte Signatur?nderung erzeugt neue Benennung.

Wichtig: passiver Wahrnehmungstest, keine Handelsentscheidung.

Dateien:
- `probe25_vs_probe26_episode_drift.csv`
- `probe25_vs_probe26_summary.json`
