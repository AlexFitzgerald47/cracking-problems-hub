# 2026-10-02 — VALIDATOR 3 (refuter) attack suite, Linear A

Verdict: `board/log/2026-10-02-validation-linear-a-v3-refuter.md`

Everything here is offline-reproducible against the vendored `data/`:

    python3 run_all.py        # all attacks -> out.txt
    python3 corpus.py fetch   # re-download witness A and witness B
    ./fetch_priorart.sh       # re-download the prior-art / adjudication documents

`inherited_refute_scribe9.py` is the unfinished 2026-09-25 harness, copied in
(not read from the other validator's directory) and verified to reproduce its
recorded `out.txt` bit-identically: `inherited_out.txt`.

Witnesses, both independent of the claimant's `analysis/` files:

* witness A — `mwenge/lineara.xyz` `LinearAInscriptions.js` (GORILA via George
  Douros's tabulation), carrying numerals, scribe, findspot, support and damage
  markers. 1,721 records.
* witness B — SigLA (Salgarella & Castellan) per-document word views for the
  eleven faces under dispute.
* adjudication — John Younger's GORILA commentary table for HT34, from the same
  repository as witness A, saved under `priorart/`.
* prior art — `dbourdeau/cyphersolver` `targets/lineara/` notes and report,
  saved under `priorart/`.

Files: `corpus.py` is the shared loader; `attack_*.py` are the attacks;
`dump.py` / `dump2.py` print raw tablet records for hand inspection.
