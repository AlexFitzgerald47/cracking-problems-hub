# The information ceiling for "The Night Before Larry Was Stretched"

**Session: 2026-09-24. Mode: starting (first working session on this folder).**

## One-line result

**The authorship of this ballad is not decidable by stylometry, and the reason is
structural rather than a shortage of effort: no candidate has an attested text in
the ballad's register, and the register displacement in this corpus is 1.5× the
author displacement — larger than the gap that defeated Junius.** The right answer
under `PROBLEM.md` criterion 2 is *untestable*, and it is now measured rather than
asserted.

## Why this is not a null result about Delta

The same pipeline, unchanged, reproduces the canonical Federalist attribution
(11/11 disputed papers to Madison) and recovers a real, weak author signal inside
the canting-song genre (p = 0.016 against a 1,000-draw permutation null). It fails
on Larry in the specific cell Larry occupies, and the failure is localised.

## Experiments

| # | Question | Result |
|---|----------|--------|
| 1 | Does the pipeline work at all? | Cosine and Burrows's Delta both put **11/11** of the Gutenberg Federalist's `HAMILTON OR MADISON` papers on Madison, reproducing Mosteller & Wallace (1964). Leave-one-paper-out on the undisputed papers, **0.903** (Burrows, MFW=300, k=3). Paper 55 — the known hard case — is the only one that flips, and only at MFW=100. |
| 2 | How much text does attribution need? | Power surface over questioned length L × training words per candidate T, holdout by paper, k=3 (chance 0.333). At **L=470** (Larry's length): T=6,000 → **0.634**; T=1,500 → 0.604; T=750 → 0.523; T=470 → 0.433. This is a **best case** — one genre, one register, one decade. |
| 3 | Can a canting song be attributed *in its own genre*? | Leave-one-song-out over the 13 *Musa Pedestris* authors with ≥2 songs (36 songs, 8,334 words, k=13, chance 0.077): **0.194** (cosine, MFW=100). Label-permutation null, 1,000 draws: **0.066 ± 0.047, p = 0.016**. Real signal, far too weak to attribute on, and unstable across hyperparameters (0.083–0.306 across six settings). |
| 4 | How big is the cant-verse ↔ prose gap? | Five authors are attested in both. Same candidate set (k=5, chance 0.200), same test texts, only the profile's register permuted. **C prose→prose at matched length 0.797; A song→song 0.389; B song→prose 0.232.** Predicted C > A > B before running; confirmed. |
| 4b | Is B distinguishable from chance? | No. Unit of independence is the song, not the draw: **2/15** songs correct in a majority of draws, exact binomial **P(X≥2) = 0.833**. 43% of all predictions sink onto one author; Henley's three songs are attributed correctly **0.00** of the time. |
| 5 | What happens if you rank Larry anyway? | Against the three candidates with attested text (Curran's oratory, Burrowes's sermons, Lysaght's verse): **two distinct winners across eight metric × MFW cells** — exactly the instability frozen as a prediction in `FREEZE.md`. |
| 6 | The one stable-looking result — is it real? | **No, it is a sink.** The register-homogeneous test (Curran's 339 words of verse vs an equal slice of Lysaght's) sends Larry to Lysaght in 8/8 cells. Fed the same two profiles, **55 of 56** *Musa* songs by other authors also go to Lysaght, **94.9%** of all cells. Larry's sweep is what this comparison does to everything. Both Larry witnesses (Farmer 1896, *Universal Songster* 1828) rank identically, so transmission variation is not what drives it. |
| 7 | The ceiling, in the board's Junius form | Over 72 units of 470 words in one common z-space: same-author **cross**-register 1.036 vs different-author **same**-register 0.938 — **the gap exceeds the signal**. d′author = 0.829, d′register = 1.274, **register is 1.5× author**. Junius was 0.588 vs 0.471. |

## The evidential situation, corrected

Work on the printings and the attribution record changed several things this
folder had recorded. Each was verified by fetching the bytes, not by search:

- **First attestation is 1787, not 1789.** The annual index of *Walker's Hibernian
  Magazine* for 1787 carries the song (OCR-damaged but unmistakable: "he'Nig
  befose Larry was, firetch'd, fet to Matic"). `PROBLEM.md`'s 1789 *Festival of
  Anacreon* date is later, and Farmer's own table of contents date of **1816 is
  wrong by nearly thirty years** — and contradicts Farmer's own note, which says
  the date is not known.
- **The earliest substantive source is Walsh (1847), not Farmer (1896)**, and it
  names **four** candidates: Burrowes, Curran, **Lysaght**, and Maher. Lysaght has
  dropped out of the modern retellings entirely.
- **Stubbs (1889)** states that Dean Burrowes, "with Edward Lysaght and Maher of
  Waterford, was known as the writer of slang songs of great humour" — direct
  period testimony against Farmer's flat "certainly did not".
- **O'Donoghue reversed himself**: the 1892 *Poets of Ireland* favours Maher; the
  1912 revision gives Burrowes a dedicated entry as "generally believed to have
  been the author... but he is understood to have denied it."
- **The 1828 byline is exactly `(Curren.)`**, confirmed in two independent scans at
  *Universal Songster* vol. III p. 141.
- **Maher's attested corpus is three lines.** Walsh's footnote quotes an inscription
  he implies Maher wrote; nothing else in Maher's name survives anywhere searched.
  Walsh calls him a **clothier**; Farmer's "shoemaker" appears to be Farmer's own
  slip. Criterion 2 is answered: Maher is untestable, and not marginally so.
- **The two printings are different recensions**, not OCR variants: *Universal
  Songster* has "he'd **fence** all the togs", "what **gownsmen** invented",
  "skuttle your nob with my **daddle**", "the **nubbling chit**", "at **darkee** we
  waked him" where Farmer has pawn / clargy / fist / nubbing-cheat / night. The
  1828 text is markedly more cant-heavy.

## What would change the answer

Nothing about method. The binding constraint is that **no candidate has a second
attested canting song**. Condition A — the only cell with measurable signal — is
empty for every one of them. Recovering an attested slang song by Burrowes or
Lysaght would populate it; per exp 2 and 3, roughly 1,500–6,000 words of
genre-matched text per candidate would be needed before a ranking meant anything,
and even then a 470-word questioned text caps accuracy near 0.6 in a 3-way.

## Reproducing

```
python3 code/parse_musa.py <gutenberg-8466.txt> data/musa_songs.json
python3 code/parse_federalist.py <gutenberg-18.txt> data/federalist.json
python3 code/exp1_validate.py         # Federalist reproduction
python3 code/exp2_power.py            # power surface
python3 code/exp3_musa_ceiling.py     # genre-matched ceiling + permutation null
python3 code/exp4_register_gap.py     # the gap
python3 code/exp4b_sink.py            # significance + sink
python3 code/exp5_larry.py            # the Larry ranking
python3 code/exp6_sink_null.py        # the sink null that kills exp5's stable cell
python3 code/exp7_ceiling.py          # d' ceiling, Junius form
```

`code/iadl.sh <archive-id> <out>` fetches an Internet Archive OCR text via the
item's own node (the `archive.org/download/...` path returns zero bytes here).

## Sources, all fetched and verified in-session

| What | Identifier |
|---|---|
| Farmer, *Musa Pedestris* (1896) | Gutenberg 8466; archive.org `musapedestristhr00farmuoft`, `musapedestristh00farmgoog` |
| *Universal Songster* vol. III | `universalsongste03crui` (byline `(Curren.)`, p. 141) |
| *Walker's Hibernian Magazine* 1787 | `sim_walkers-hibernian-magazine_1787-12_16` |
| Walsh, *Ireland Sixty Years Ago* (1847) | `sketchesofirelan00wals_0` |
| Stubbs, *History of the University of Dublin* (1889) | `historyofunivers00stubrich` |
| O'Donoghue, *Poets of Ireland* (1912) | `poetsofireland0000djod` |
| W. H. Curran, *Life of J. P. Curran* (1819) | `liferighthonour00currgoog` |
| Curran, *Speeches* (1811) | `speechesofrighth00curr_2` |
| Burrowes, *Sermons* (1829) / *Twelve Discourses* (1834) | `sermonsonfirstl00burrgoog`, `twelvediscourse00ddgoog` |
| Lysaght, *Poems* (1811) | `poems00lysagoog` |
| Federalist Papers | Gutenberg 18 |
| Prose for the gap test | `rookwoodaromanc00ainsgoog`, `lifeinlondonorda00eganuoft`, `viewsreviewsessays00henl`, `howpoorliveandho00sims`, `cu31924064950557` |
