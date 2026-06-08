# Mini-DIO Kontrolllauf: passive Kandidaten ohne Rueckwirkung

Ziel: Pruefen, ob die existierende passive Kandidaten-Memory die Mini-DIO-Wahrnehmung veraendert, obwohl sie nicht an `run_mini.py` uebergeben wird.

Referenz: `debug/dio_mini_repro_fresh_probe25_20260606`
Kontrolle: `debug/dio_mini_control_existing_candidates_probe25_20260606`
Passive Kandidaten-Datei existiert: `bot_memory/dio_mini_passive_recurrence_maturity_candidates.json`

## Ergebnis
- Kandidaten-Datei wurde nicht an Mini-DIO uebergeben.
- Vergleichsfelder: 12
- Lauf 1: 18 / 18 exakt identisch.
- Lauf 2: 18 / 18 exakt identisch.
- Gesamtbefund: keine Rueckwirkung nachweisbar.

## Grenze
- passive Kandidaten existieren nur als Datei.
- Mini-DIO liest sie aktuell nicht.
- keine Handlung, kein Gate, kein Training-Memory.
