# DIO Mini Passive Development Diagnosis

## Grenze
- liest nur die passive Reife-Timeline
- schreibt kein Memory
- beeinflusst keine Handlung
- kein Gate

## Zusammenfassung
- development_stable_carried: families=2 rows=4 reward_sum=4.0 families_list=dio_0hd3,dio_1g18
- development_observation_to_carried: families=1 rows=3 reward_sum=1.0 families_list=dio_0cgn
- development_quiet_observation: families=8 rows=17 reward_sum=0.0 families_list=dio_07rf,dio_0gmg,dio_0izw,dio_15ms,dio_173s,dio_1mn2,dio_1mx2,dio_1pfo
- development_repeated_burden: families=1 rows=2 reward_sum=-2.0 families_list=dio_0x52

## Familien
- dio_0hd3: stabil getragen; Pfad=moment_carried; Aktionen=SHORT; reward_sum=1.000000.
- dio_1g18: stabil getragen; Pfad=moment_carried -> moment_carried -> moment_carried; Aktionen=SHORT -> SHORT -> SHORT; reward_sum=3.000000.
- dio_0cgn: Entwicklung von Beobachtung/Halten zu getragenem Kontakt; Pfad=moment_quiet_observed -> moment_quiet_observed -> moment_carried; Aktionen=WAIT -> WAIT -> LONG; reward_sum=1.000000.
- dio_07rf: ruhig beobachtet/gehalten; Pfad=moment_quiet_observed -> moment_quiet_observed; Aktionen=WAIT -> WAIT.
- dio_0gmg: ruhig beobachtet/gehalten; Pfad=moment_quiet_observed -> moment_quiet_observed -> moment_quiet_observed; Aktionen=WAIT -> WAIT -> WAIT.
- dio_0izw: ruhig beobachtet/gehalten; Pfad=moment_quiet_observed -> moment_quiet_observed; Aktionen=WAIT -> WAIT.
- dio_15ms: ruhig beobachtet/gehalten; Pfad=moment_quiet_observed -> moment_quiet_held; Aktionen=WAIT -> WAIT.
- dio_173s: ruhig beobachtet/gehalten; Pfad=moment_quiet_observed -> moment_quiet_observed -> moment_quiet_observed; Aktionen=WAIT -> WAIT -> WAIT.
- dio_1mn2: ruhig beobachtet/gehalten; Pfad=moment_quiet_observed; Aktionen=WAIT.
- dio_1mx2: ruhig beobachtet/gehalten; Pfad=moment_quiet_observed -> moment_quiet_observed; Aktionen=WAIT -> WAIT.
- dio_1pfo: ruhig beobachtet/gehalten; Pfad=moment_quiet_observed -> moment_quiet_observed; Aktionen=WAIT -> WAIT.
- dio_0x52: wiederholt belastend/widerspruechlich; Pfad=moment_conflicted_burden -> moment_conflicted_burden; Aktionen=SHORT -> SHORT; reward_sum=-2.000000.