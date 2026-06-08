# DIO Mini Passive Inner Coherence Map

## Innenzustand

### inner_carried
- count: 14
- reward_sum: 11.335684
- best_reward_sum: 13.409002
- contact_qualities: observed_potential,positive_real_contact
- families: dio_0120,dio_0akd,dio_0arw,dio_0t0v,dio_1u7v
- avg_sehen_form_stability: 0.142857
- avg_hoeren_energy_tone: 0.006414
- avg_fuehlen_mcm_coherence: 0.471882
- avg_fuehlen_mcm_tension: 0.161438

### inner_open_observation
- count: 6
- reward_sum: 0.000000
- best_reward_sum: 1.112940
- contact_qualities: observed_potential
- families: dio_02qu,dio_14xc
- avg_sehen_form_stability: 0.666667
- avg_hoeren_energy_tone: 0.024934
- avg_fuehlen_mcm_coherence: 0.793018
- avg_fuehlen_mcm_tension: 0.315406

### inner_unfinished
- count: 2
- reward_sum: 0.000000
- best_reward_sum: 1.258292
- contact_qualities: observed_potential
- families: dio_00qb
- avg_sehen_form_stability: 0.000000
- avg_hoeren_energy_tone: -0.078022
- avg_fuehlen_mcm_coherence: 0.378154
- avg_fuehlen_mcm_tension: 0.299928

### inner_cautious
- count: 4
- reward_sum: -0.684966
- best_reward_sum: 0.569932
- contact_qualities: negative_real_contact,observed_potential
- families: dio_1vpi
- avg_sehen_form_stability: 1.000000
- avg_hoeren_energy_tone: -0.052832
- avg_fuehlen_mcm_coherence: 0.985207
- avg_fuehlen_mcm_tension: 0.348372

## Familien

### dio_0arw / inner_carried / positive_real_contact
- count: 4
- reward_sum: 5.539416
- avg_reward: 1.384854
- actions: LONG
- transitions: same_inner_state
- avg_sehen_form_flow: -0.447325
- avg_sehen_form_stability: 0.000000
- avg_hoeren_energy_tone: -0.005360
- avg_fuehlen_mcm_coherence: 0.398499
- avg_fuehlen_mcm_tension: 0.275533
- note: getragen_sensorisch_bestaetigt

### dio_1u7v / inner_carried / positive_real_contact
- count: 4
- reward_sum: 3.577568
- avg_reward: 0.894392
- actions: SHORT
- transitions: timeline_start
- avg_sehen_form_flow: 0.032622
- avg_sehen_form_stability: 1.000000
- avg_hoeren_energy_tone: 0.039728
- avg_fuehlen_mcm_coherence: 0.988876
- avg_fuehlen_mcm_tension: 0.040826
- note: getragen_sensorisch_bestaetigt

### dio_0akd / inner_carried / positive_real_contact
- count: 2
- reward_sum: 1.551314
- avg_reward: 0.775657
- actions: LONG
- transitions: same_inner_state
- avg_sehen_form_flow: -0.021613
- avg_sehen_form_stability: -1.000000
- avg_hoeren_energy_tone: -0.046190
- avg_fuehlen_mcm_coherence: -0.212933
- avg_fuehlen_mcm_tension: 0.063058
- note: getragen_sensorisch_bestaetigt

### dio_0120 / inner_carried / positive_real_contact
- count: 2
- reward_sum: 0.667386
- avg_reward: 0.333693
- actions: LONG
- transitions: inner_open_observation_to_inner_carried
- avg_sehen_form_flow: 0.606218
- avg_sehen_form_stability: 1.000000
- avg_hoeren_energy_tone: 0.115901
- avg_fuehlen_mcm_coherence: 0.967548
- avg_fuehlen_mcm_tension: 0.321409
- note: getragen_sensorisch_bestaetigt

### dio_0t0v / inner_carried / observed_potential
- count: 2
- reward_sum: 0.000000
- avg_reward: 0.000000
- actions: WAIT
- transitions: inner_unfinished_to_inner_carried
- avg_sehen_form_flow: 0.043335
- avg_sehen_form_stability: -1.000000
- avg_hoeren_energy_tone: -0.093547
- avg_fuehlen_mcm_coherence: -0.226193
- avg_fuehlen_mcm_tension: 0.112880
- note: offen_lesen

### dio_00qb / inner_unfinished / observed_potential
- count: 2
- reward_sum: 0.000000
- avg_reward: 0.000000
- actions: WAIT
- transitions: inner_cautious_to_inner_unfinished
- avg_sehen_form_flow: 0.402576
- avg_sehen_form_stability: 0.000000
- avg_hoeren_energy_tone: -0.078022
- avg_fuehlen_mcm_coherence: 0.378154
- avg_fuehlen_mcm_tension: 0.299928
- note: offen_lesen

### dio_02qu / inner_open_observation / observed_potential
- count: 2
- reward_sum: 0.000000
- avg_reward: 0.000000
- actions: WAIT
- transitions: inner_cautious_to_inner_open_observation
- avg_sehen_form_flow: 0.291659
- avg_sehen_form_stability: 0.000000
- avg_hoeren_energy_tone: 0.053713
- avg_fuehlen_mcm_coherence: 0.384960
- avg_fuehlen_mcm_tension: 0.192154
- note: offen_beobachtet_potenzial

### dio_14xc / inner_open_observation / observed_potential
- count: 4
- reward_sum: 0.000000
- avg_reward: 0.000000
- actions: WAIT
- transitions: inner_carried_to_inner_open_observation
- avg_sehen_form_flow: 0.822477
- avg_sehen_form_stability: 1.000000
- avg_hoeren_energy_tone: 0.010545
- avg_fuehlen_mcm_coherence: 0.997047
- avg_fuehlen_mcm_tension: 0.377032
- note: offen_beobachtet_potenzial

### dio_1vpi / inner_cautious / observed_potential
- count: 2
- reward_sum: 0.000000
- avg_reward: 0.000000
- actions: WAIT
- transitions: inner_open_observation_to_inner_cautious
- avg_sehen_form_flow: 0.742634
- avg_sehen_form_stability: 1.000000
- avg_hoeren_energy_tone: -0.052832
- avg_fuehlen_mcm_coherence: 0.985207
- avg_fuehlen_mcm_tension: 0.348372
- note: vorsicht_beobachtet_potenzial

### dio_1vpi / inner_cautious / negative_real_contact
- count: 2
- reward_sum: -0.684966
- avg_reward: -0.342483
- actions: SHORT
- transitions: inner_open_observation_to_inner_cautious
- avg_sehen_form_flow: 0.742634
- avg_sehen_form_stability: 1.000000
- avg_hoeren_energy_tone: -0.052832
- avg_fuehlen_mcm_coherence: 0.985207
- avg_fuehlen_mcm_tension: 0.348372
- note: hohe_sicht_feld_kohärenz_ohne_handlung

## Grenze
- kein Memory-Schreiben
- keine Motorik
- kein Gate
- keine harte Regel