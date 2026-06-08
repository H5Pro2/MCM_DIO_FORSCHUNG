# DIO Mini Passive Development Diagnosis

## Grenze
- liest nur die passive Reife-Timeline
- schreibt kein Memory
- beeinflusst keine Handlung
- kein Gate

## Zusammenfassung
- development_stable_carried: families=4 rows=9 reward_sum=9.0 families_list=dio_02qu,dio_0arw,dio_0t0v,dio_1u7v
- development_observation_to_carried: families=1 rows=3 reward_sum=1.0 families_list=dio_1vpi
- development_quiet_observation: families=2 rows=5 reward_sum=0.0 families_list=dio_00qb,dio_14xc

## Familien
- dio_02qu: stabil getragen; Pfad=moment_carried; Aktionen=LONG; reward_sum=1.000000.
- dio_0arw: stabil getragen; Pfad=moment_carried -> moment_carried -> moment_carried; Aktionen=LONG -> LONG -> LONG; reward_sum=3.000000.
- dio_0t0v: stabil getragen; Pfad=moment_carried -> moment_carried; Aktionen=LONG -> LONG; reward_sum=2.000000.
- dio_1u7v: stabil getragen; Pfad=moment_carried -> moment_carried -> moment_carried; Aktionen=SHORT -> SHORT -> SHORT; reward_sum=3.000000.
- dio_1vpi: Entwicklung von Beobachtung/Halten zu getragenem Kontakt; Pfad=moment_quiet_held -> moment_quiet_held -> moment_carried; Aktionen=WAIT -> WAIT -> SHORT; reward_sum=1.000000.
- dio_00qb: ruhig beobachtet/gehalten; Pfad=moment_quiet_held -> moment_quiet_held; Aktionen=WAIT -> WAIT.
- dio_14xc: ruhig beobachtet/gehalten; Pfad=moment_quiet_observed -> moment_quiet_held -> moment_quiet_held; Aktionen=WAIT -> WAIT -> WAIT.