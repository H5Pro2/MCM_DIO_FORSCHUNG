# DIO Mini Passive Inner Coherence Map

## Innenzustand

### inner_carried
- count: 3
- reward_sum: 3.315905
- best_reward_sum: 3.315905
- contact_qualities: positive_real_contact
- families: dio_0arw,dio_0t0v,dio_1u7v
- avg_sehen_form_stability: 0.000000
- avg_hoeren_energy_tone: -0.019726
- avg_fuehlen_mcm_coherence: 0.387061
- avg_fuehlen_mcm_tension: 0.143080

### inner_open_observation
- count: 1
- reward_sum: 0.000000
- best_reward_sum: 0.094515
- contact_qualities: observed_potential
- families: dio_14xc
- avg_sehen_form_stability: 1.000000
- avg_hoeren_energy_tone: 0.010545
- avg_fuehlen_mcm_coherence: 0.997047
- avg_fuehlen_mcm_tension: 0.377032

### inner_unfinished
- count: 2
- reward_sum: 0.000000
- best_reward_sum: 0.771629
- contact_qualities: observed_potential
- families: dio_00qb,dio_1vpi
- avg_sehen_form_stability: 0.500000
- avg_hoeren_energy_tone: -0.065427
- avg_fuehlen_mcm_coherence: 0.681681
- avg_fuehlen_mcm_tension: 0.324150

## Familien

### dio_0arw / inner_carried / positive_real_contact
- count: 1
- reward_sum: 1.384854
- avg_reward: 1.384854
- actions: LONG
- transitions: same_inner_state
- avg_sehen_form_flow: -0.447325
- avg_sehen_form_stability: 0.000000
- avg_hoeren_energy_tone: -0.005360
- avg_fuehlen_mcm_coherence: 0.398499
- avg_fuehlen_mcm_tension: 0.275533
- note: getragen_sensorisch_bestaetigt

### dio_0t0v / inner_carried / positive_real_contact
- count: 1
- reward_sum: 1.036659
- avg_reward: 1.036659
- actions: LONG
- transitions: inner_unfinished_to_inner_carried
- avg_sehen_form_flow: 0.043335
- avg_sehen_form_stability: -1.000000
- avg_hoeren_energy_tone: -0.093547
- avg_fuehlen_mcm_coherence: -0.226193
- avg_fuehlen_mcm_tension: 0.112880
- note: getragen_sensorisch_bestaetigt

### dio_1u7v / inner_carried / positive_real_contact
- count: 1
- reward_sum: 0.894392
- avg_reward: 0.894392
- actions: SHORT
- transitions: timeline_start
- avg_sehen_form_flow: 0.032622
- avg_sehen_form_stability: 1.000000
- avg_hoeren_energy_tone: 0.039728
- avg_fuehlen_mcm_coherence: 0.988876
- avg_fuehlen_mcm_tension: 0.040826
- note: getragen_sensorisch_bestaetigt

### dio_00qb / inner_unfinished / observed_potential
- count: 1
- reward_sum: 0.000000
- avg_reward: 0.000000
- actions: WAIT
- transitions: same_inner_state
- avg_sehen_form_flow: 0.402576
- avg_sehen_form_stability: 0.000000
- avg_hoeren_energy_tone: -0.078022
- avg_fuehlen_mcm_coherence: 0.378154
- avg_fuehlen_mcm_tension: 0.299928
- note: offen_lesen

### dio_14xc / inner_open_observation / observed_potential
- count: 1
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

### dio_1vpi / inner_unfinished / observed_potential
- count: 1
- reward_sum: 0.000000
- avg_reward: 0.000000
- actions: WAIT
- transitions: inner_open_observation_to_inner_unfinished
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