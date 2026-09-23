"""Hand-audit verdicts on the 58 candidate alternative-dating pairs.

Every candidate pair produced by src/run_spreads.py was read.  ACCEPT means the
two entries record the SAME event at different years, so the pair measures a
real dating disagreement.  REJECT means they record different events and the
pair measures only the matcher.  Reciprocal duplicates (A->B and B->A) are
collapsed by CANON.

Two pairs are added by hand (ADDED) where the marked entry plainly duplicates
another entry but the matcher chose a different partner; both are recorded
because leaving them out would flatter the comparison distribution, which is
the distribution this analysis measures the Patrician spread against.
"""

ACCEPT = {
 "AI485.1": "AI487.1", "AI597.2": "AI604.1", "AI1251.1": "AI1209.6",
 "AT715.1": "AT690.8",
 "AU435.2": "AU436.2", "AU436.1": "AU435.1", "AU436.3": "AU435.1",
 "AU452.1": "AU439.2", "AU456.1": "AU452.1",
 "AU467.2": "AU469.1", "AU468.2": "AU476.1", "AU469.1": "AU470.1",
 "AU475.1": "AU473.3", "AU496.4": "AU494.1", "AU499.4": "AU497.2",
 "AU504.3": "AU500.2", "AU521.1": "AU527.1", "AU528.3": "AU526.1",
 "AU535.3": "AU533.3", "AU536.5": "AU534.1", "AU539.2": "AU535.2",
 "AU545.2": "AU542.1", "AU545.4": "AU540.1", "AU548.4": "AU543.2",
 "AU553.4": "AU551.1", "AU565.2": "AU572.6", "AU573.2": "AU566.1",
 "AU577.6": "AU570.2", "AU587.3": "AU581.2", "AU591.2": "AU585.1",
 "AU601.3": "AU602.4", "AU622.5": "AU618.3", "AU630.3": "AU636.1",
 "AU656.7": "AU648.1", "CS565.3": "CS573.2",
}

# marked entry -> wrong partner chosen by the matcher, and why rejected
REJECT = {
 "AI455.2":  "Brigit's birth paired with Secundinus's repose",
 "AI1193.2": "two different castles",
 "AT564.2":  "Brenann of Birr paired with Aed son of Brenann",
 "AU440.2":  "Maine son of Niall paired with the elder Patrick",
 "AU446.1":  "Mac Cairthinn son of Caelub is not Mac Cairthinn of Clochar",
 "AU457.2":  "the elder Patrick paired with the battle of Ard Corann",
 "AU471.1":  "the second Saxon prey is not the first",
 "AU483.2":  "battle of Ocha paired with the death of Conall of Cremthann",
 "AU485.1":  "first battle of Granairet is not the second",
 "AU497.4":  "second battle of Granairet is not the first",
 "AU507.1":  "first battle of Ard Corann is not the second",
 "AU511.1":  "second battle of Ard Corann is not the first",
 "AU512.4":  "Lugaid's death paired with the start of his reign",
 "AU520.3":  "Comgall's birth paired with Colum Cille's birth",
 "AU523.1":  "battle of Dethna paired with the death of Conall of Cremthann",
 "AU537.3":  "Mochta paired with Brigit",
 "AU545.3":  "Diarmait's accession paired with Colman Mor",
 "AU611.3":  "paired on the residue of 'Book of Cuanu'",
 "AU629.4":  "paired on the residue of 'Book of Cuanu'",
 "AU643.5":  "accession of Cellach and Conall paired with Conall's killing",
}

# marked entry -> correct partner the matcher missed
ADDED = {
 "AU512.4": "AU507.1",   # 'Or here, the death of Lugaid son of Laegaire'
 "AU537.3": "AU535.1",   # 'Or here, the falling asleep of St Mochta'
}

# reciprocal pairs to collapse: keep the first, drop the second
CANON_DROP = {"AU436.2", "AU470.1", "AU572.6"}
