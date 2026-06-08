# DIO Mini Passive Development Diagnosis

## Grenze
- liest nur die passive Reife-Timeline
- schreibt kein Memory
- beeinflusst keine Handlung
- kein Gate

## Zusammenfassung
- development_stable_carried: families=4 rows=8 reward_sum=8.0 families_list=dio_02qu,dio_0arw,dio_0x1o,dio_1vpi
- development_observation_to_carried: families=2 rows=5 reward_sum=2.0 families_list=dio_16yc,dio_1txv
- development_quiet_observation: families=5 rows=5 reward_sum=0.0 families_list=dio_0igh,dio_143d,dio_14xc,dio_1g2t,dio_1qwp
- development_negative_open: families=1 rows=1 reward_sum=-1.0 families_list=dio_0fiy

## Familien
- dio_02qu: stabil getragen; Pfad=moment_carried -> moment_carried -> moment_carried; Aktionen=LONG -> LONG -> LONG; reward_sum=3.000000.
- dio_0arw: stabil getragen; Pfad=moment_carried; Aktionen=LONG; reward_sum=1.000000.
- dio_0x1o: stabil getragen; Pfad=moment_carried; Aktionen=LONG; reward_sum=1.000000.
- dio_1vpi: stabil getragen; Pfad=moment_carried -> moment_carried -> moment_carried; Aktionen=SHORT -> SHORT -> SHORT; reward_sum=3.000000.
- dio_16yc: Entwicklung von Beobachtung/Halten zu getragenem Kontakt; Pfad=moment_quiet_observed -> moment_carried; Aktionen=WAIT -> SHORT; reward_sum=1.000000.
- dio_1txv: Entwicklung von Beobachtung/Halten zu getragenem Kontakt; Pfad=moment_quiet_observed -> moment_quiet_observed -> moment_carried; Aktionen=WAIT -> WAIT -> SHORT; reward_sum=1.000000.
- dio_0igh: ruhig beobachtet/gehalten; Pfad=moment_quiet_observed; Aktionen=WAIT.
- dio_143d: ruhig beobachtet/gehalten; Pfad=moment_quiet_observed; Aktionen=WAIT.
- dio_14xc: ruhig beobachtet/gehalten; Pfad=moment_quiet_held; Aktionen=WAIT.
- dio_1g2t: ruhig beobachtet/gehalten; Pfad=moment_quiet_observed; Aktionen=WAIT.
- dio_1qwp: ruhig beobachtet/gehalten; Pfad=moment_quiet_observed; Aktionen=WAIT.
- dio_0fiy: negative offene Entwicklung; Pfad=moment_open; reward_sum=-1.000000.