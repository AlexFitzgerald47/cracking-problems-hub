# VALIDATOR 1 reproduction — Linear A, 2026-10-02

Independent of `analysis/*.csv`. Verdict: `board/log/2026-10-02-validation-linear-a-v1.md`.

Run: `./run_all.sh > out.txt`  (offline, against `data/`; Python 3 stdlib only, deterministic)

| file | what it does |
|---|---|
| `load.py` | parses witness A (`data/LinearAInscriptions.js`) out of the JS Map |
| `census.py` | corpus census; coverage of the claim in documents / sign-group tokens / types |
| `arith.py` | first-pass scope-aware audit of every KU-RO / PO-TO-KU-RO total |
| `arith2.py` | the audit used in the verdict: two frozen segmentations, numeral-level damage flag |
| `tests.py` | KU-RO permutation null; KI-RO constructions + background rate; HT97 subset-sum; HT2; HT85 gang base rate; HT119 ratio; DI-KI-SE |
| `perm.py` | the label permutation the 2026-09-23 board cross-reference demands, with size-matched nulls |
| `lexemes.py` | every attestation of each glossed sign-group; HT95 polarity; HT86 A-KA-RU |
| `gorila_checks.md` | what I read off the GORILA vol. I plates and apparatus |
| `out.txt` | full output of `run_all.sh` |

## Witnesses

- `data/LinearAInscriptions.js` — fetched 2026-10-02 from
  `raw.githubusercontent.com/mwenge/lineara.xyz/master/LinearAInscriptions.js`.
  **It changed in 12 documents since the 2026-09-25 vendoring, HT34 among them
  (`KI-RO 37` -> `KI-RO 30 [[7]]`).** Its `translatedWords` field already carries Younger's
  glosses ("total", "assessment"?, "owed") as data; nothing here uses that field.
- `data/gorila_p*.png` — three pages rendered from GORILA vol. I, kept because they carry
  the editorial apparatus the verdict turns on. Re-fetch the full PDF (44 MB, not committed)
  with `curl -o GORILA-Vol1.pdf https://raw.githubusercontent.com/mwenge/lineara.xyz/master/papers/GORILA-Vol1.pdf`
  then `pdftoppm -f <page> -l <page> -r 150 -png GORILA-Vol1.pdf out`.
- SigLA (https://sigla.phis.me/) carries sign-groups only, no numerals, so it cannot
  adjudicate arithmetic; the 2026-09-25 session's vendored copies were used for spelling
  comparison only.
