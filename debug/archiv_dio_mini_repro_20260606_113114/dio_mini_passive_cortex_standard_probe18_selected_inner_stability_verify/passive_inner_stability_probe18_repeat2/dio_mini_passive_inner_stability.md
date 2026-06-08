# DIO Mini Passive Inner Stability

## Stabilitaet

### stable_state / inner_carried / positive_real_contact
- count: 4
- reward_sum: 5.539416
- best_reward_sum: 5.539416
- avg_reward: 1.384854
- actions: LONG
- families: dio_0arw

### transition_state / inner_carried / positive_real_contact
- count: 4
- reward_sum: 4.146636
- best_reward_sum: 4.146636
- avg_reward: 1.036659
- actions: LONG
- families: dio_0t0v

### start_state / inner_carried / positive_real_contact
- count: 4
- reward_sum: 3.577568
- best_reward_sum: 3.577568
- avg_reward: 0.894392
- actions: SHORT
- families: dio_1u7v

### transition_state / inner_cautious / observed_potential
- count: 4
- reward_sum: 0.000000
- best_reward_sum: 0.569932
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
- best_reward_sum: 2.516584
- avg_reward: 0.000000
- actions: WAIT
- families: dio_00qb

## Uebergaenge

### same_inner_state
- stability_kind: stable_state
- count: 4
- reward_sum: 5.539416
- positive_contacts: 4
- observed_potentials: 0
- actions: LONG
- families: dio_0arw

### inner_unknown_to_inner_carried
- stability_kind: transition_state
- count: 4
- reward_sum: 4.146636
- positive_contacts: 4
- observed_potentials: 0
- actions: LONG
- families: dio_0t0v

### timeline_start
- stability_kind: start_state
- count: 4
- reward_sum: 3.577568
- positive_contacts: 4
- observed_potentials: 0
- actions: SHORT
- families: dio_1u7v

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
- families: dio_00qb

### inner_open_observation_to_inner_cautious
- stability_kind: transition_state
- count: 4
- reward_sum: 0.000000
- positive_contacts: 0
- observed_potentials: 4
- actions: WAIT
- families: dio_1vpi

## Grenze
- kein Memory-Schreiben
- keine Motorik
- kein Gate
- keine harte Regel