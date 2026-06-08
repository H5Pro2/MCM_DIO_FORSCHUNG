# REGULATIONS-REKONSTRUKTION CHECKLISTE

Ziel:
Das aktuelle Projekt nach dem Funktionssplit gegen die Konstruktion pruefen.
Der alte Code ist nur Quelle der Extraktion, nicht die Referenz selbst.

## A. Harte Refactor-Invarianten

- [ ] `proposed_decision` erzeugt nie allein einen Trade.
- [ ] `decision_tendency != act` ruft keinen Brain-Entry-Plan auf.
- [ ] `allow_plan = False` kann spaeter nicht zu `act` umgebogen werden.
- [ ] `act_watch` wird als Beobachtungs-/Reifungsphase behandelt, nicht als Entry.
- [ ] `decision_strength` wird aus tragenden Hypothesen gebildet, nicht aus `abs(long_score/short_score)`.
- [ ] Non-Action (`observe`, `replan`, `hold`) wird als Attempt/Episode gespeichert.
- [ ] Trade-Plan entsteht erst nach Meta-Regulation.
- [ ] Value-Gate ersetzt nicht die MCM-Regulation.

## B. Runtime-State muss synchron bleiben

Diese Felder muessen nach jedem Runtime-Tick in sich stimmig sein:

- [ ] `bot.mcm_runtime_snapshot["timestamp"]`
- [ ] `bot.mcm_runtime_decision_state["timestamp"]`
- [ ] `bot.mcm_runtime_decision_state["decision_tendency"]`
- [ ] `bot.mcm_runtime_decision_state["allow_plan"]`
- [ ] `bot.mcm_runtime_decision_state["entry_result"]`
- [ ] `bot.mcm_runtime_brain_snapshot["decision_tendency"]`
- [ ] `bot.mcm_runtime_brain_snapshot["meta_regulation_state"]`
- [ ] `bot.active_context_trace`
- [ ] `bot.felt_state`
- [ ] `bot.thought_state`
- [ ] `bot.temporal_perception_state`

## C. Gate-Pruefung

Im aktuellen Projekt muss `bot_gates/entry_decision.py` folgendes Verhalten zeigen:

- [ ] `build_runtime_decision_tendency(...)` wird zuerst aufgerufen.
- [ ] Wenn `None`: kein Entry.
- [ ] Wenn `decision_tendency != act`: Non-Action-Paket.
- [ ] Wenn `decision_tendency == act` aber `allow_plan == False`: Non-Action-Paket.
- [ ] Erst danach `decide_mcm_brain_entry(...)`.
- [ ] Ungueltige Geometrie wird nicht gehandelt.

## D. Meta-Regulation-Pruefung

In `core/decision_regulation.py` pruefen:

- [ ] `long_hypothesis` und `short_hypothesis` kommen aus `thought_state`.
- [ ] `decision_strength = max(long_hypothesis, short_hypothesis, optional_explicit_strength)`.
- [ ] kein `abs(...)` auf Gegensignale.
- [ ] `allow_plan`, `allow_observe`, `allow_ruminate`, `allow_block` werden nicht spaeter durch einen Reset ueberschrieben.
- [ ] `pre_action_phase` bleibt Quelle fuer `observe/replan/hold/act`.
- [ ] nachgelagerte Schichten duerfen `allow_plan` zuruecknehmen:
  - Zero Point
  - Strukturunsicherheit
  - visuelle Unsicherheit
  - Transfer-/Regimebruch
  - Formsymbol-Reifung
  - Feldfragmentierung
  - open hypothesis Reifung

## E. Debug-Nachweis nach Wiederaufbau

Ein vollstaendiger Lauf ist erst plausibel, wenn diese Verteilung sichtbar ist:

- [ ] `attempts` deutlich hoeher als `trades`
- [ ] `attempts_observed` sichtbar
- [ ] `attempts_replanned` sichtbar
- [ ] `attempts_withheld` sichtbar
- [ ] `attempts_skipped` oder gleichwertige Non-Action sichtbar
- [ ] `trades` nicht explosiv hoeher als die rekonstruierte organische Tendenz erlaubt
- [ ] `max_drawdown_pct` nicht durch reines Overtrading dominiert
- [ ] `decision_tendency` nicht dauerhaft `act`
- [ ] `pre_action_phase` nicht dauerhaft `act`

## F. Referenzsymptom fuer Bruch

Wenn ein Lauf zeigt:

- sehr viele Trades bei wenig Daten
- `withheld = 0`
- `skipped = 0`
- kaum `observe/replan`
- starke negative Equity trotz vieler Aktionen

dann ist wahrscheinlich einer dieser Pfade gebrochen:

1. Runtime-Tendenz wird ignoriert.
2. `allow_plan=False` wird ueberfahren.
3. `proposed_decision` wird als Handlung gelesen.
4. `decision_strength` liest Gegensignal als Staerke.
5. Non-Action wird nicht als Versuch/Episode gespeichert.
6. Gate ruft Brain-Plan zu frueh auf.

## G. Rekonstruktionsziel

Nicht Ziel:

- alte PnL exakt kopieren
- alten Code blind nachbauen
- monolithische Kopplungen wieder einfuehren
- harte Trading-Regel bauen
- Impuls mechanisch blockieren

Ziel:

- extrahierte organische Reihenfolge wiederherstellen
- Hypothese von Handlung trennen
- MCM-Regulation vor Motorik setzen
- Nicht-Handlung als reife Information erhalten
- Outcome wieder sauber in Feld, Memory und Form-Sprache zurueckfuehren
