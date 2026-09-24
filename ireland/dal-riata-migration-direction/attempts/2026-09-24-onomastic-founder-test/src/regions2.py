# -*- coding: utf-8 -*-
"""Irish provincial groups, added to the frozen three-way north-channel gazetteer.

The frozen design used a resampling null: draw n tokens from the Irish pool and score
coverage against the rest of the pool.  That null is IN-SAMPLE -- the draw and the
reference come from one distribution -- while IONA/DALR/PICT are scored OUT-OF-SAMPLE.
Any group that differs from the Irish pool in any way at all is then depressed relative
to the null, so the null cannot distinguish "not Irish" from "not the Irish pool".
That is why all three north-channel groups fell below it, positive control included.

The correct baseline is a real Irish region scored by the identical out-of-sample
procedure: hold the region out of the reference, then score it.  The spread across five
Irish provinces is the empirical band for "an Irish population measured from outside",
and it is what IONA, DALR and PICT are placed against.

Regions are intended to be broad and mutually exclusive in practice; entries matching
more than one are counted in each, and the sensitivity run drops them.
"""
import re
from regions import region, IRISH, TAGSETS   # north-channel sets unchanged

def _rx(t): return re.compile("|".join(t))

PROVINCE = {
    "ULSTER": _rx([r"Ulaid", r"Ulidia", r"\bUlster\b", r"Dál Araid", r"Dál nAraide",
                   r"Dál Fiatach", r"Dún Lethglaise", r"Bennchor", r"\bBangor\b",
                   r"Mag Roth", r"Uí Echach", r"Conaille", r"Mugdorna", r"Cuailnge",
                   r"Lethglenn", r"Airthir", r"Uí Thuirtri", r"Fir Lí", r"Eilne"]),
    "MIDLAND": _rx([r"Brega", r"\bMide\b", r"\bMeath\b", r"Ard Macha", r"Armagh",
                    r"Tailtiu", r"Temair", r"Temuir", r"\bTara\b", r"Lusca", r"Slane",
                    r"Lugmad", r"\bLouth\b", r"Fir Rois", r"Cianacht", r"Ciannacht",
                    r"Cluain Iraird", r"Dermag", r"Durrow", r"Dam Liac", r"Fine Gall",
                    r"Uí Néill", r"Loch Gabor", r"Gailenga", r"Luigne", r"Tethba",
                    r"Uí Moccu Uais", r"Delbna"]),
    "NORTHWEST": _rx([r"\bAilech\b", r"Cenél Conaill", r"Cenél nEógain", r"Cenel Conaill",
                      r"Inis Eógain", r"Doire", r"\bDerry\b", r"Ráith Both", r"Tír Conaill",
                      r"Tír Eógain", r"Cenél Cairpri", r"Druim Cliab", r"Airgialla",
                      r"\bOriel\b", r"Uí Chremthainn", r"Uí Méith", r"Fernmag", r"Uí Nialláin"]),
    "LEINSTER": _rx([r"Laigin", r"Leinster", r"Osraige", r"Ossory", r"Uí Cheinnselaig",
                     r"Uí Chennselaig", r"Uí Failg", r"Uí Fhailgi", r"Uí Failge",
                     r"Glenn Dá Locha", r"Glendalough", r"Ferna", r"Cell Dara",
                     r"\bKildare\b", r"Uí Máil", r"Uí Bairrche", r"Uí Drona",
                     r"Uí Fhaeláin", r"Uí Muiredaig", r"Laíges", r"Cualu"]),
    "MUNSTER": _rx([r"\bMumu\b", r"Munster", r"Caisel", r"\bCashel\b", r"\bEmly\b",
                    r"Imlech", r"Ciarraige", r"Éoganacht", r"Eoganacht", r"Corcu",
                    r"Luimnech", r"Lismore", r"Les Mór", r"Iarmumu", r"Desmumu",
                    r"Uí Fhidgeinte", r"Uí Fidgente", r"Uí Liatháin", r"Múscraige",
                    r"Ara Tíre", r"Arad Tíre", r"Déisi", r"Uí Chonaill Gabra"]),
    "CONNACHT": _rx([r"Connacht", r"Connachta", r"Uí Briúin", r"Uí Maine", r"Uí Maini",
                     r"Uí Fhiachrach", r"Uí Fiachrach", r"Cruachan", r"Síl Muiredaig",
                     r"Cluain Ferta", r"Clonfert", r"Uí Amalga", r"Luigne Connacht",
                     r"Corcu Modruad", r"Síl Anmchada", r"Bréifne", r"Umall"]),
}

def provinces(text, tagset="STRICT"):
    """Irish provinces an entry matches.  Empty if the entry is north-channel."""
    if region(text, tagset):
        return set()
    return {k for k, rx in PROVINCE.items() if rx.search(text)}

def is_irish_pool(text, tagset="STRICT"):
    """Reference pool membership: any in-window entry with NO north-channel marker.
    (Defect D2: the frozen version also demanded a positive Irish marker, which
    discarded 1,800 name-bearing entries -- bare obits with no toponym.)"""
    return not region(text, tagset)
