# DIO Mini Passive Inner Stability

## Stabilitaet

### stable_state / inner_carried / positive_real_contact
- count: 4
- reward_sum: 5.812000
- best_reward_sum: 5.812000
- avg_reward: 1.453000
- actions: LONG
- families: dio_0ofo

### stable_state / inner_open_observation / observed_potential
- count: 4
- reward_sum: 0.000000
- best_reward_sum: 0.700112
- avg_reward: 0.000000
- actions: WAIT
- families: dio_1mym

### transition_state / inner_carried / positive_real_contact
- count: 4
- reward_sum: 4.347040
- best_reward_sum: 4.347040
- avg_reward: 1.086760
- actions: LONG
- families: dio_04z7

### start_state / inner_carried / positive_real_contact
- count: 4
- reward_sum: 3.647524
- best_reward_sum: 3.647524
- avg_reward: 0.911881
- actions: SHORT
- families: dio_1bwb

### transition_state / inner_open_observation / observed_potential
- count: 4
- reward_sum: 0.000000
- best_reward_sum: 0.378512
- avg_reward: 0.000000
- actions: WAIT
- families: dio_14xc

### transition_state / inner_unfinished / observed_potential
- count: 4
- reward_sum: 0.000000
- best_reward_sum: 2.780168
- avg_reward: 0.000000
- actions: WAIT
- families: dio_1k7y

## Uebergaenge

### same_inner_state
- stability_kind: stable_state
- count: 8
- reward_sum: 5.812000
- positive_contacts: 4
- observed_potentials: 4
- actions: LONG,WAIT
- families: dio_0ofo,dio_1mym

### inner_unfinished_to_inner_carried
- stability_kind: transition_state
- count: 4
- reward_sum: 4.347040
- positive_contacts: 4
- observed_potentials: 0
- actions: LONG
- families: dio_04z7

### timeline_start
- stability_kind: start_state
- count: 4
- reward_sum: 3.647524
- positive_contacts: 4
- observed_potentials: 0
- actions: SHORT
- families: dio_1bwb

### inner_carried_to_inner_open_observation
- stability_kind: transition_state
- count: 4
- reward_sum: 0.000000
- positive_contacts: 0
- observed_potentials: 4
- actions: WAIT
- families: dio_14xc

### inner_open_observation_to_inner_unfinished
- stability_kind: transition_state
- count: 4
- reward_sum: 0.000000
- positive_contacts: 0
- observed_potentials: 4
- actions: WAIT
- families: dio_1k7y

## Grenze
- kein Memory-Schreiben
- keine Motorik
- kein Gate
- keine harte Regel