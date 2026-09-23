"""Multiply-recorded obits in the fifth-to-seventh-century stratum.

The spread analysis in run_spread_dist.py depends on the matcher finding both
halves of a pair, and a matcher finds close pairs more easily than distant
ones -- which biases the comparison distribution downwards exactly where the
Patrician comparison needs it not to be.  This builds the same comparison
class a second way, by name, with no similarity search at all:

  1. take every entry in the window whose text carries a death formula;
  2. extract its capitalised name tokens;
  3. group entries that share a name token;
  4. a group with entries in >= 2 distinct years is a multiply-dated obit.

Groups are hand-audited (results/obit_audit.txt): Irish dynastic naming means
a shared forename is not a shared person, so a group survives only if the
entries plainly concern one individual.
"""
import re, collections

DEATH = re.compile(r"\b(repose|reposes|died|dies|death|dormitatio|quies|quievit|"
                   r"rested|rests|falling asleep|fell asleep|sleeping|pausavit|"
                   r"dormitation|slain|killed|drowning)\b", re.I)

# tokens that are capitalised but are not personal names
STOP = set("""Kl K Kalends Kalendae January February March April May June July August
September October November December Ireland Irish Hibernia Scoti Christ Lord God
Saint St Bishop Abbot King Repose Death The A In On Of And Or Here Some Others
Thus Book Anno Year Age Rome Roman Britain Scotland Alba Mumu Laigin Connacht
Connachta Ulaid Mide Brega Temair Ard Cluain Cell Cenel Dal Ui Moccu Son Sons
Daughter Feast Battle Kalend Jesus Easter Pentecost Ides Nones Passion Incarnation
Leinster Munster Meath Ulster Picts Cruithin Saxons Britons Franks Angels Gospel
Sunday Monday Tuesday Wednesday Thursday Friday Saturday Abbess""".split())

NAME = re.compile(r"\b([A-ZÁÉÍÓÚÖ][a-záéíóúöáäëïà-ɏ]{3,})")


def names(text):
    return {w for w in NAME.findall(text) if w not in STOP}


def obit_groups(entries, lo, hi, witness=None):
    pool = [e for e in entries
            if lo <= e["year"] < hi and DEATH.search(e["text"])
            and (witness is None or e["witness"] == witness)]
    by_name = collections.defaultdict(list)
    for e in pool:
        for nm in names(e["text"]):
            by_name[nm].append(e)
    out = {}
    for nm, es in by_name.items():
        yrs = sorted({e["year"] for e in es})
        if len(yrs) >= 2:
            out[nm] = sorted(es, key=lambda e: (e["year"], e["witness"]))
    return out
