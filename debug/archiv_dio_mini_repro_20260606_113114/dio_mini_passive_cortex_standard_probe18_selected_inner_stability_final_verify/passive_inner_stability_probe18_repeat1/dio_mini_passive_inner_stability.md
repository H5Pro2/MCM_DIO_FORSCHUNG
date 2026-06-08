# DIO Mini Passive Inner Stability

## Stabilitaet

### stable_state / inner_carried / positive_real_contact
- count: 4
- reward_sum: 5.539416
- best_reward_sum: 5.539416
- avg_reward: 1.384854
- actions: LONG
- families: dio_0arw

### stable_state / inner_unknown / positive_real_contact
- count: 2
- reward_sum: 0.667386
- best_reward_sum: 0.667386
- avg_reward: 0.333693
- actions: LONG
- families: dio_0120

### start_state / inner_carried / positive_real_contact
- count: 4
- reward_sum: 3.577568
- best_reward_sum: 3.577568
- avg_reward: 0.894392
- actions: SHORT
- families: dio_1u7v

### transition_state / inner_unknown / positive_real_contact
- count: 2
- reward_sum: 1.551314
- best_reward_sum: 1.551314
- avg_reward: 0.775657
- actions: LONG
- families: dio_0akd

### transition_state / inner_carried / observed_potential
- count: 2
- reward_sum: 0.000000
- best_reward_sum: 2.073318
- avg_reward: 0.000000
- actions: WAIT
- families: dio_0t0v

### transition_state / inner_cautious / observed_potential
- count: 2
- reward_sum: 0.000000
- best_reward_sum: 0.284966
- avg_reward: 0.000000
- actions: WAIT
- families: dio_1vpi

### transition_state / inner_open_observation / observed_potential
- count: 4
- reward_sum: 0.000000
- best_reward_sum: 0.378060
- avg_reward: 0.000000
- actions: WAIT
- families: dio_14xc

### transition_state / inner_unknown / observed_potential
- count: 4
- reward_sum: 0.000000
- best_reward_sum: 1.993172
- avg_reward: 0.000000
- actions: WAIT
- families: dio_00qb,dio_02qu

### transition_state / inner_cautious / negative_real_contact
- count: 2
- reward_sum: -0.684966
- best_reward_sum: 0.284966
- avg_reward: -0.342483
- actions: SHORT
- families: dio_1vpi

## Uebergaenge

### same_inner_state
- stability_kind: stable_state
- count: 6
- reward_sum: 6.206802
- positive_contacts: 6
- observed_potentials: 0
- actions: LONG
- families: dio_0120,dio_0arw

### timeline_start
- stability_kind: start_state
- count: 4
- reward_sum: 3.577568
- positive_contacts: 4
- observed_potentials: 0
- actions: SHORT
- families: dio_1u7v

### inner_carried_to_inner_unknown
- stability_kind: transition_state
- count: 2
- reward_sum: 1.551314
- positive_contacts: 2
- observed_potentials: 0
- actions: LONG
- families: dio_0akd

### inner_carried_to_inner_open_observation
- stability_kind: transition_state
- count: 4
- reward_sum: 0.000000
- positive_contacts: 0
- observed_potentials: 4
- actions: WAIT
- families: dio_14xc

### inner_cautious_to_inner_unknown
- stability_kind: transition_state
- count: 4
- reward_sum: 0.000000
- positive_contacts: 0
- observed_potentials: 4
- actions: WAIT
- families: dio_00qb,dio_02qu

### inner_unknown_to_inner_carried
- stability_kind: transition_state
- count: 2
- reward_sum: 0.000000
- positive_contacts: 0
- observed_potentials: 2
- actions: WAIT
- families: dio_0t0v

### inner_open_observation_to_inner_cautious
- stability_kind: transition_state
- count: 4
- reward_sum: -0.684966
- positive_contacts: 0
- observed_potentials: 2
- actions: SHORT,WAIT
- families: dio_1vpi

## Grenze
- kein Memory-Schreiben
- keine Motorik
- kein Gate
- keine harte Regel