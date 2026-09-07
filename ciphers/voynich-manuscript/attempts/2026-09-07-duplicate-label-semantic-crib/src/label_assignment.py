#!/usr/bin/env python3
"""Exact assignment test for image-anchored Voynich pharma labels.

The seven candidate Herbal pages are an independently selected strict duplicate-
drawing set (Jorge Stolfi / Rene Zandbergen catalogue). Three corresponding
pharmaceutical fragments carry individual labels. The koldarod/f18v relation was
already noted publicly in 2024, so the primary confirmatory test in this script
uses only the two other labels: odalydary and loralody.

Scoring rule, fixed before assignment:
    score(label, page) = minimum raw Levenshtein distance from the label to any
                         single EVA running-text word on that Herbal page.

The page strings below are the cleaned first-alternative EVA readings from the
Takeshi Takahashi transcription for the seven strict image-matched Herbal pages.
The same 3x7 distance matrix was independently checked against ZL3b.
"""

from itertools import permutations

LABELS = {
    "koldarod": "f18v",      # known prior observation; sensitivity only
    "odalydary": "f23r",     # strict duplicate fragment 213
    "loralody": "f19r",      # strict duplicate fragment 240
}

# Dots and commas are token boundaries here; apostrophes/uncertain glyph markup
# have already been reduced to the displayed EVA first reading where relevant.
PAGES_RAW = {
    "f1v": """
    kchsy chydaiin ol o l tchey char cfhar am
    yteey char or ochy dcho lkody okodar chody
    da ckhy ckhockhy shy dksheey cthy kotchody dal
    dol chokeo dair dam sochey chokody
    potoy shol dair cphoal dar chey tody otoaiin shoshy
    choky chol ctho l shol okal dolchey chodo lol chy cthy
    qo ol choees cheol dol cthey ykol dol dolo ykol do lchiody
    okolshol kol kechy chol ky chol cthol chody chol daiin
    shor okol chol dol ky dar shol dchor o tcho dar shody
    taor chotchey dal chody schody pol chodar
    """,
    "f18v": """
    told shor ytshy otchdal dchal dchy ytdg
    qoeees or oaiin shy okshy qokchy qokchy s g
    orshy qoky qoky chkchy qokshy qokam
    qotchy qokay qokchy ykcho ydl dar
    ychoees ykchy qol kchy qotchol daiir om
    qotor chor otchy qokeees chy s ar ykar
    ychol dor chod qokol daiin qokol dar dy
    tolol sh cphoy daror ddy ytor ykam
    okchor qotchy qokchy ytol doky dy
    yko dshy dair ykol dom
    """,
    "f19r": """
    pchor qodchy qotshy dy tchy qotchy qoky daiin dchydy
    dshy chor y tchy chol dytchy chordy daiin dyty cho
    oscheor shy tdaiin chol dor yky
    qokorar daiin chckhy shy kchor
    otchy tchy qoky daiin
    yshor shy daiin otytchy daiin
    qo k cho ky cthar dor chan dar
    or chor daky dal chor dorl shy
    qotchor dy dor y tchy kchy shdaiin
    daiin cthor chol ykchor chordy
    qotchy qolody choldy cthyd
    ykchor chor daiin daiinol
    os octhor ytchor
    """,
    "f23r": """
    pydchdom chy fcholdy oty otchol shy opyaiin y yfchy daiin ololdy dal
    to ar chor daiin chk dain otchy lolchor daiin dam okchol dain g
    dchar ykor y kaiin daiin cth g
    qokoldy okaiir ykaiil g qokeey ofchol dain yfchor olfchor otchald
    ychor qokchol ytym chol dair chol ar ol ol dol dain
    tshol y kor qokaiin yky dar okol dchey daiidal dam ytcho ldals
    okar olchar shaiin qokchol dar qokchol dairo r ol daiin alg
    qokshy char daiir qokaiin olol qoaiin ykchy s dal okchy
    okol ok shy qokol dy dal dshe qokeees y oly daiin dal
    qok okaiin chkchy s yteain odal chal dy dar ykain
    ykyka dalory
    """,
    "f32v": """
    kcheodaiin chol kechy qotaiin daiioam o chofchody
    daiin odar chy daiin chey tchy l dy dain teor
    shor daiin chckhy dsho dain daiin s shokey ka
    or chr chor dor chaiin qotcho r chy dcho daiin
    chokchy daiin shy chor qo kaiin dain dchol dosg
    o kchan chol shal dchcthy
    ksho cphos she sheaiin otshcho r dain shckhy s odan
    otchol daiin daiin ctho daiin qotaiin otchy d shan
    qotchy cfhy skey chocthy daiin cthaiin daiin
    sho keol chor chol daiin cpho l cthol da ar
    ol sho chy
    """,
    "f37v": """
    tshody qocthy qotoldy chopdain sol
    dor chol cthor orchochor daiin
    qokchon shy chon daiin dy
    dshor dytory dshor daiin
    dchor qotol ykchon dain
    yokor ytchor saiin oty
    qotchor daiin
    qotor choiin chetchy daiin
    dor chor sho daiiin daiin
    soiin ch ey o koiin chey tom
    qotoiin choror cthol daiin
    chor shyly sheaiin do tody
    sotoiiin
    todain cphaiin cphorods
    soiiin cheoky daiin dain
    qotor daiin chotaiin
    sokchor qokoiiin ykeeols
    oyteey daiin daiinody
    daiin qkaiin qotal daiin
    y chocthhy ykol daiin s
    oshctho do daiin cthols
    qotol ytoiin chocthhy
    yto chol daiin
    """,
    "f47v": """
    psheot cheor cholsho chopchy sal sary
    dsheey shy cphy otchey daiidy chory daiiy
    shol char oteol dor otchol chkchy daiin
    qotol sheey kol sho keechy qoty cthy
    dsholy shees chor ody shy sy sary
    chody cheor saiin dochod chol
    pchodaiin dair dcthy
    daiin cheotar chodaly sal
    qotcheey chety chol chol dain
    chotcho ltchey o tcho tchy dy chol chody dar
    oteey cho chdy chy key chyky dchy daiin chy
    chy cho keesy chy chy cheky chochy daiin
    dshy daiin chdlety chaiin dcheey otald
    chol ctchey
    """,
}


def words(text):
    return [w.lower() for w in text.split() if w]


def levenshtein(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(
                cur[-1] + 1,
                prev[j] + 1,
                prev[j - 1] + (ca != cb),
            ))
        prev = cur
    return prev[-1]


def page_score(label, page):
    scored = [(levenshtein(label, w), w) for w in words(PAGES_RAW[page])]
    return min(scored)


def assignment_null(labels):
    pages = list(PAGES_RAW)
    correct = tuple(LABELS[l] for l in labels)
    correct_score = sum(page_score(l, p)[0] for l, p in zip(labels, correct))
    vals = []
    for perm in permutations(pages, len(labels)):
        score = sum(page_score(l, p)[0] for l, p in zip(labels, perm))
        vals.append((score, perm))
    vals.sort()
    n_le = sum(score <= correct_score for score, _ in vals)
    return correct_score, n_le, len(vals), vals[:10]


def main():
    pages = list(PAGES_RAW)
    print("distance matrix (distance; nearest word)")
    print("label," + ",".join(pages))
    for label in LABELS:
        cells = []
        for p in pages:
            d, w = page_score(label, p)
            cells.append(f"{d}:{w}")
        print(label + "," + ",".join(cells))

    print("\nPRIMARY TEST: two not-previously-used labels")
    primary = ("odalydary", "loralody")
    score, n_le, total, top = assignment_null(primary)
    print(f"correct total={score}; assignments <= correct={n_le}/{total}; exact p={n_le/total:.9f}")
    print("top assignments:")
    for x in top:
        print(x)

    print("\nSENSITIVITY: all three labels, including known koldarod/f18v")
    all3 = ("koldarod", "odalydary", "loralody")
    score, n_le, total, top = assignment_null(all3)
    print(f"correct total={score}; assignments <= correct={n_le}/{total}; exact p={n_le/total:.9f}")
    print("top assignments:")
    for x in top:
        print(x)


if __name__ == "__main__":
    main()
