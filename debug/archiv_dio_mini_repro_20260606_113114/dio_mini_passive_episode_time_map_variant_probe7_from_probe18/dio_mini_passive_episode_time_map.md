# DIO Mini Passive Episode Time Map

## Grenze
- passiv
- kein Memory-Schreiben
- keine Motorik
- kein Gate

## Quellen
- probe7_f1: debug\dio_mini_12n_inner_map_variant_probe7_from_probe18

## Zusammenfassung
- dio_0u8f:LONG: fresh_local_episode_trace; Quellen=probe7_f1; Episoden=3; Outcome=TP:3; RewardSumme=3.000000.
- dio_0x52:SHORT: fresh_local_episode_trace; Quellen=probe7_f1; Episoden=3; Outcome=TP:3; RewardSumme=3.000000.
- dio_1h5y:LONG: fresh_local_episode_trace; Quellen=probe7_f1; Episoden=2; Outcome=TP:2; RewardSumme=2.000000.
- dio_0qrm:SHORT: fresh_local_episode_trace; Quellen=probe7_f1; Episoden=1; Outcome=TP:1; RewardSumme=1.000000.
- dio_0lyu:WAIT: fresh_local_episode_trace; Quellen=probe7_f1; Episoden=3; Outcome=NO_TRADE:3; RewardSumme=0.000000.
- dio_19i4:WAIT: fresh_local_episode_trace; Quellen=probe7_f1; Episoden=1; Outcome=NO_TRADE:1; RewardSumme=0.000000.
- dio_19p6:WAIT: fresh_local_episode_trace; Quellen=probe7_f1; Episoden=1; Outcome=NO_TRADE:1; RewardSumme=0.000000.
- dio_19i4:SHORT: fresh_local_episode_trace; Quellen=probe7_f1; Episoden=2; Outcome=SL:2; RewardSumme=-2.000000.

## Detailauszug
- probe7_f1 run=180 tick=1: dio_0x52 SHORT/TP; Zeitspur=no_prior_phase; reward=1.000000.
- probe7_f1 run=180 tick=6: dio_0u8f LONG/TP; Zeitspur=executed_temporal_contact; reward=1.000000.
- probe7_f1 run=180 tick=11: dio_0lyu WAIT/NO_TRADE; Zeitspur=different_contact_afterimage; reward=0.000000.
- probe7_f1 run=180 tick=12: dio_19i4 SHORT/SL; Zeitspur=executed_temporal_contact; reward=-1.000000.
- probe7_f1 run=180 tick=17: dio_1h5y LONG/TP; Zeitspur=executed_temporal_contact; reward=1.000000.
- probe7_f1 run=181 tick=1: dio_0x52 SHORT/TP; Zeitspur=no_prior_phase; reward=1.000000.
- probe7_f1 run=181 tick=6: dio_0u8f LONG/TP; Zeitspur=executed_temporal_contact; reward=1.000000.
- probe7_f1 run=181 tick=11: dio_0lyu WAIT/NO_TRADE; Zeitspur=different_contact_afterimage; reward=0.000000.
- probe7_f1 run=181 tick=12: dio_19i4 SHORT/SL; Zeitspur=executed_temporal_contact; reward=-1.000000.
- probe7_f1 run=181 tick=17: dio_1h5y LONG/TP; Zeitspur=executed_temporal_contact; reward=1.000000.
- probe7_f1 run=182 tick=1: dio_0x52 SHORT/TP; Zeitspur=no_prior_phase; reward=1.000000.
- probe7_f1 run=182 tick=6: dio_0u8f LONG/TP; Zeitspur=executed_temporal_contact; reward=1.000000.
- probe7_f1 run=182 tick=11: dio_0lyu WAIT/NO_TRADE; Zeitspur=different_contact_afterimage; reward=0.000000.
- probe7_f1 run=182 tick=12: dio_19i4 WAIT/NO_TRADE; Zeitspur=different_contact_afterimage; reward=0.000000.
- probe7_f1 run=182 tick=13: dio_0qrm SHORT/TP; Zeitspur=executed_temporal_contact; reward=1.000000.
- probe7_f1 run=182 tick=18: dio_19p6 WAIT/NO_TRADE; Zeitspur=different_contact_afterimage; reward=0.000000.