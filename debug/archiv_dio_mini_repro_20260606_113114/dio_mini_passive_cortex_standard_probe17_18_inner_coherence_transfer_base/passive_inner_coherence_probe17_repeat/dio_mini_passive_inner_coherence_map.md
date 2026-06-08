# DIO Mini Passive Inner Coherence Map

## Innenzustand

### inner_carried
- count: 12
- reward_sum: 13.806564
- best_reward_sum: 13.806564
- contact_qualities: positive_real_contact
- families: dio_04z7,dio_0ofo,dio_1bwb
- avg_sehen_form_stability: 0.000000
- avg_hoeren_energy_tone: -0.002640
- avg_fuehlen_mcm_coherence: 0.387410
- avg_fuehlen_mcm_tension: 0.143766

### inner_open_observation
- count: 8
- reward_sum: 0.000000
- best_reward_sum: 1.078624
- contact_qualities: observed_potential
- families: dio_14xc,dio_1mym
- avg_sehen_form_stability: 1.000000
- avg_hoeren_energy_tone: -0.023591
- avg_fuehlen_mcm_coherence: 0.986824
- avg_fuehlen_mcm_tension: 0.378155

### inner_unfinished
- count: 4
- reward_sum: 0.000000
- best_reward_sum: 2.780168
- contact_qualities: observed_potential
- families: dio_1k7y
- avg_sehen_form_stability: 0.000000
- avg_hoeren_energy_tone: -0.077778
- avg_fuehlen_mcm_coherence: 0.378222
- avg_fuehlen_mcm_tension: 0.290899

## Familien

### dio_0ofo / inner_carried / positive_real_contact
- count: 4
- reward_sum: 5.812000
- avg_reward: 1.453000
- actions: LONG
- transitions: same_inner_state
- avg_sehen_form_flow: -0.458776
- avg_sehen_form_stability: 0.000000
- avg_hoeren_energy_tone: 0.023375
- avg_fuehlen_mcm_coherence: 0.393455
- avg_fuehlen_mcm_tension: 0.298608
- note: getragen_sensorisch_bestaetigt

### dio_04z7 / inner_carried / positive_real_contact
- count: 4
- reward_sum: 4.347040
- avg_reward: 1.086760
- actions: LONG
- transitions: inner_unfinished_to_inner_carried
- avg_sehen_form_flow: 0.021684
- avg_sehen_form_stability: -1.000000
- avg_hoeren_energy_tone: -0.071409
- avg_fuehlen_mcm_coherence: -0.219994
- avg_fuehlen_mcm_tension: 0.087641
- note: getragen_sensorisch_bestaetigt

### dio_1bwb / inner_carried / positive_real_contact
- count: 4
- reward_sum: 3.647524
- avg_reward: 0.911881
- actions: SHORT
- transitions: timeline_start
- avg_sehen_form_flow: 0.038108
- avg_sehen_form_stability: 1.000000
- avg_hoeren_energy_tone: 0.040115
- avg_fuehlen_mcm_coherence: 0.988768
- avg_fuehlen_mcm_tension: 0.045048
- note: getragen_sensorisch_bestaetigt

### dio_14xc / inner_open_observation / observed_potential
- count: 4
- reward_sum: 0.000000
- avg_reward: 0.000000
- actions: WAIT
- transitions: inner_carried_to_inner_open_observation
- avg_sehen_form_flow: 0.845244
- avg_sehen_form_stability: 1.000000
- avg_hoeren_energy_tone: 0.023468
- avg_fuehlen_mcm_coherence: 0.993429
- avg_fuehlen_mcm_tension: 0.389748
- note: offen_beobachtet_potenzial

### dio_1k7y / inner_unfinished / observed_potential
- count: 4
- reward_sum: 0.000000
- avg_reward: 0.000000
- actions: WAIT
- transitions: inner_open_observation_to_inner_unfinished
- avg_sehen_form_flow: 0.359266
- avg_sehen_form_stability: 0.000000
- avg_hoeren_energy_tone: -0.077778
- avg_fuehlen_mcm_coherence: 0.378222
- avg_fuehlen_mcm_tension: 0.290899
- note: offen_lesen

### dio_1mym / inner_open_observation / observed_potential
- count: 4
- reward_sum: 0.000000
- avg_reward: 0.000000
- actions: WAIT
- transitions: same_inner_state
- avg_sehen_form_flow: 0.754296
- avg_sehen_form_stability: 1.000000
- avg_hoeren_energy_tone: -0.070649
- avg_fuehlen_mcm_coherence: 0.980218
- avg_fuehlen_mcm_tension: 0.366561
- note: offen_beobachtet_potenzial

## Grenze
- kein Memory-Schreiben
- keine Motorik
- kein Gate
- keine harte Regel