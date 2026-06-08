# Mini-DIO Passive Variant Stability

## State Summary
- variant_local_wait_context: count=10 reward=0.000000 episodes=30 variants=probe14_f2,probe17_f3
- variant_related_observation_trace: count=6 reward=0.000000 episodes=18 variants=probe14_f2,probe17_f3
- variant_self_carried_action_trace: count=4 reward=12.000000 episodes=12 variants=probe14_f2,probe17_f3

## Carried Actions
- LONG: count=2 reward=6.000000 episodes=6 variants=probe17_f3 families=probe17_f3:dio_0n9e:LONG,probe17_f3:dio_1k7y:LONG
- SHORT: count=2 reward=6.000000 episodes=6 variants=probe14_f2 families=probe14_f2:dio_0hd3:SHORT,probe14_f2:dio_0szn:SHORT

## Stability Compare
- probe14_f1_to_f2 / same_variant_state: count=10 reward_delta=0.000000 episode_delta=0
- probe17_f2_to_f3 / same_variant_state: count=10 reward_delta=0.000000 episode_delta=0

## Grenze
- passive_only=true
- writes_training_memory=false
- read_by_mini_dio=false
- influences_action=false
- is_gate=false
- is_motoric=false
