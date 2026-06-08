# Mini-DIO passive Kontexttransfer Probe25 zu Probe26

Ziel: Sichtbar machen, ob passive Wiederkehrkontexte bei Signaturdrift erhalten bleiben oder als neue Syntax erscheinen.

## Ergebnis
- family_missing_in_probe26: 13 Familien
- same_context: 5 Familien

## Deutung
- same_context: dieselbe Familie bleibt trotz Probe26 im gleichen passiven Kontext.
- context_lost_or_new_syntax: Probe26 erzeugt fuer diese Familie keine direkte Kandidatenbindung; das ist eher neue/verschobene Syntax als aktive Reife.
- context_shifted: Kontext wechselt aktiv in einen anderen bekannten Zustand.

## Grenze
- Nur Bericht.
- Keine Runtime-Rueckfuehrung.
- Keine Handlung.
- Kein Gate.
- Kein Trainingsmemory.
