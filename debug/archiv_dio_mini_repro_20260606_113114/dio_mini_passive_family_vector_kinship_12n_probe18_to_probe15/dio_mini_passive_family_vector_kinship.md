# DIO Mini Passive Family Vector Kinship

- left: probe18_12n (debug\dio_mini_12n_livecheck_probe18)
- right: probe15_transfer_12n (debug\dio_mini_12n_transfer_probe15)

## Zusammenfassung
- single_to_quiet: families=3 avg_similarity=0.876315623 same_action=1 same_outcome=1 pairs=dio_0arw->dio_173s,dio_0fiy->dio_07rf,dio_1g2t->dio_07rf
- single_to_single: families=4 avg_similarity=0.924972309 same_action=0 same_outcome=0 pairs=dio_0igh->dio_0hd3,dio_143d->dio_0hd3,dio_14xc->dio_0hd3,dio_1qwp->dio_0hd3
- single_to_trust: families=1 avg_similarity=0.95884419 same_action=0 same_outcome=1 pairs=dio_0x1o->dio_1g18
- trust_to_quiet: families=1 avg_similarity=0.737113127 same_action=0 same_outcome=0 pairs=dio_02qu->dio_173s
- trust_to_single: families=1 avg_similarity=0.941886839 same_action=1 same_outcome=1 pairs=dio_1vpi->dio_0hd3
- variant_to_quiet: families=1 avg_similarity=0.82884948 same_action=0 same_outcome=1 pairs=dio_16yc->dio_0izw
- variant_to_variant: families=1 avg_similarity=0.965920524 same_action=1 same_outcome=1 pairs=dio_1txv->dio_0cgn

## Beste Naehe je linker Familie
- dio_02qu -> dio_173s: similarity=0.737113 distance=0.356644 state=trust->quiet action=LONG->WAIT outcome=TP->NO_TRADE
- dio_0arw -> dio_173s: similarity=0.915397 distance=0.092422 state=single->quiet action=LONG->WAIT outcome=TP->NO_TRADE
- dio_0fiy -> dio_07rf: similarity=0.877590 distance=0.139484 state=single->quiet action=LONG->WAIT outcome=SL->NO_TRADE
- dio_0igh -> dio_0hd3: similarity=0.894108 distance=0.118433 state=single->single action=WAIT->SHORT outcome=NO_TRADE->TP
- dio_0x1o -> dio_1g18: similarity=0.958844 distance=0.042922 state=single->trust action=LONG->SHORT outcome=TP->TP
- dio_143d -> dio_0hd3: similarity=0.955679 distance=0.046376 state=single->single action=WAIT->SHORT outcome=NO_TRADE->TP
- dio_14xc -> dio_0hd3: similarity=0.955679 distance=0.046376 state=single->single action=WAIT->SHORT outcome=NO_TRADE->TP
- dio_16yc -> dio_0izw: similarity=0.828849 distance=0.206492 state=variant->quiet action=SHORT->WAIT outcome=NO_TRADE->NO_TRADE
- dio_1g2t -> dio_07rf: similarity=0.835960 distance=0.196230 state=single->quiet action=WAIT->WAIT outcome=NO_TRADE->NO_TRADE
- dio_1qwp -> dio_0hd3: similarity=0.894422 distance=0.118041 state=single->single action=WAIT->SHORT outcome=NO_TRADE->TP
- dio_1txv -> dio_0cgn: similarity=0.965921 distance=0.035282 state=variant->variant action=WAIT->WAIT outcome=NO_TRADE->NO_TRADE
- dio_1vpi -> dio_0hd3: similarity=0.941887 distance=0.061699 state=trust->single action=SHORT->SHORT outcome=TP->TP

## Grenze
- passive Sinnes-/MCM-Verwandtschaft
- kein Memory-Schreiben
- keine Motorik
- kein Gate
- keine harte Regel
- Familiennamen werden nicht als Identitaetsbeweis benutzt