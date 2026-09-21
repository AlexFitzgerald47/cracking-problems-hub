# Reproduction of the 2026-09-17 register self-match result

**Run:** 2026-09-21, fresh container, nothing cached from the previous session.

`data/chunks.json` is gitignored, so the 2026-09-17 attempt had to be rebuilt from
source before it could be extended. That rebuild is the reproduction check the
board's practices require, and it is reported here rather than assumed.

## What was re-run, unchanged

```
curl .../textcreationpartnership/Texts/master/TCP.csv      # 29 MB catalogue
git clone --depth 1 dracor-org/engdracor                   # 268 MB
python fetch_tcp.py       # 774 TCP texts, 774 ok, 0 failed, ~227 MB
python build_corpus.py
python analysis.py
python wide_panel.py
```

`numpy` had to be installed (2.4.6); the 2026-09-17 run's version is not recorded.

## Result: identical

**Corpus.** `data/manifest.json` rebuilt **byte-identically** to the committed
copy — same 74 kept non-dramatic texts, same 42 drops with the same reasons
(14 markup, 6 too short, 19 pageant, 3 manual). 943 non-dramatic chunks, 3,062
drama chunks, 27 authors. This also confirms that the engdracor `sourceid`
exclusion set has not drifted since 2026-09-17 in a way that touches this corpus.

**Distance cells** (2,000-word chunks, drama-scaled, same-work pairs excluded):

| cell | 2026-09-17 | 2026-09-21 |
|---|---|---|
| same author, same register | 415.80 | 415.80 |
| different author, same register | 447.92 | 447.92 |
| same author, cross register | 470.52 | 470.52 |
| different author, cross register | 486.20 | 486.20 |

**Attribution, 8-author panel:** within-register micro 0.666 / macro 0.717;
cross-register 0.169 / 0.337; reverse 0.268 / 0.326. All identical.

**Permutation null:** mean macro 0.119, p95 0.222, max 0.315. Identical.

**Wide panel:** Lyly 41.0%, Peele 18.6%, Glapthorne 11.1%, Chapman 11.0%;
Spearman(verse density, absorption) +0.039; 27-author macro 0.345, micro 0.141.
All identical.

The 2026-09-17 session is reproducible from the committed manifest and code alone.

## One correction found during the rebuild

`../2026-09-17-register-self-match/RESULTS.md` states that on the 27-author panel
"**fourteen** of the twenty-seven dramatists absorb nothing at all". Its own stored
`results/wide_panel.json` gives **twelve** authors with a share of exactly zero
(Behn, Brome, Crowne, D'Urfey, Fletcher, Ford, Middleton, Otway, Pix, Settle,
Shadwell, Shirley). Dryden and Lee each absorb one chunk of 943 and print as
`0.1%` in the session's own table; they appear to have been read off the printed
table as zeros.

The error is small and does not touch any argument in that file — the point is that
a large minority of the panel is unreachable, and twelve makes it as well as
fourteen. It is recorded because this board corrects forward rather than quietly.
The corrected figure, twelve, is the baseline used for prediction B2.
