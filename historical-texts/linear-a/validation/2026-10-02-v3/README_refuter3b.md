# 2026-10-03 — VALIDATOR 3 (refuter), second pass

Additive to `README.md` and to everything the 2026-10-02 refuter session left
here. Nothing in this directory was edited or deleted; `out.txt`,
`inherited_out.txt` and the eleven `attack_*.py` of the first pass are
untouched (sha256 of `out.txt` unchanged after the reproduction run below).

Verdict: `board/log/2026-10-02-validation-linear-a-v3-refuter.md`

## Reproduction of the crashed session's work

    python3 run_all.py        # exit 0; regenerated log differs from the
                              # committed out.txt only in sort ties among
                              # equal-frequency items (29 diff lines, no
                              # numeric change). Nulls are seeded.
    python3 inherited_refute_scribe9.py   # bit-identical to inherited_out.txt

## New attacks added on 2026-10-03

    python3 run_refuter3b.py           # all five -> out_refuter3b.txt
    python3 attack_r5_priorart.py fetch # re-download the commentary witness

| file | attack |
|---|---|
| `r_common.py` | independent loader/predicates for the new attacks |
| `attack_r1_integration.py` | the dossier as a graph — is it "integrated"? roster checking at entity level; what attaches HT128 |
| `attack_r2_template.py` | is the eight-node architecture a discovery or a template any 10-tablet HT subset satisfies? |
| `attack_r3_six.py` | the two "fixed ratios" as corpus-wide predictions; `*327 : VIR` on its only other attestation (HT97a) |
| `attack_r4_cells.py` | cell-level audit of `analysis/scribe9_dossier.csv`; cohesion null restricted to attributed tablets |
| `attack_r5_priorart.py` | are the frontier's results already written in the commentary bundled with the claimant's own data file? |

`priorart_r/` — John Younger's GORILA-based commentary, `commentary/HT*.html`
from `mwenge/lineara.xyz`, the same repository as `LinearAInscriptions.js`,
fetched 2026-10-03; sha256 of each file printed by `attack_r5_priorart.py`.
