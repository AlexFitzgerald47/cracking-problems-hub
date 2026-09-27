# Starting a new session on this problem

Two pieces: what to set in the cloud environment, and the prompt to paste.
Written 2026-09-06, after the session that built the eclipse canons. If
`analysis/RESULTS.md` has grown past 14 sections since, trust it over this file.

---

## 1. Environment settings (one-time, in the UI)

An agent cannot change its own network policy — it is enforced at the egress
gateway from the environment's saved configuration.

**claude.ai/code → environment selector → edit the environment → Network access.**
Change from **Trusted** to **Custom**, and paste into **Allowed domains**:

```
celt.ucc.ie
archive.org
*.archive.org
1641.tcd.ie
downsurvey.tcd.ie
registers.nli.ie
militaryarchives.ie
chronhib.maynoothuniversity.ie
en.wikipedia.org
www.gutenberg.org
```

**Tick "Also include default list of common package managers."** Without it you
lose PyPI and the eclipse engine cannot install `pymeeus`.

The `*.` on archive.org is load-bearing: full-text downloads redirect to
`ia######.us.archive.org` nodes.

**Setup script:** paste the contents of `setup.sh` from this folder. It builds the
venv, clones the Δ*T* reference implementation, and probes every host the board
depends on into `.session-environment.md`.

Settings apply when a VM is provisioned, so **start a new session** — a running
one will not pick them up.

---

## 2. The prompt

Paste into a new session on branch `claude/irish-problems-progress-o6q34y`.

---

You are a cracker in the Cracking Problems Hub. Read `AGENT_INSTRUCTIONS.md`,
`_roles/CRACKER.md`, `_roles/README.md` and `board/PRACTICES.md` first, then
`ireland/early-irish-annals-reliability/analysis/RESULTS.md` — it has a contents
table and fourteen sections — followed by that folder's `PROGRESS.md` and
`HANDOVER.md`, including their amendments. Claim the problem in `board/active/`.

**Establish your constraints before planning.** Read `.session-environment.md` if
the setup script wrote one; otherwise probe directly with
`curl -sS -o /dev/null -w '%{http_code}' https://celt.ucc.ie/`. A `000` means the
egress proxy denied it — do not retry and do not route around it. Then run
`ireland/early-irish-annals-reliability/bootstrap/fetch_corpus.sh`, which pulls
the Annals of Ulster into `sources/` if the hosts are now reachable. **Its CELT
URL patterns are marked UNVERIFIED** because the session that wrote it could not
see the site; fix them from the live site and commit the correction.

**Verify the pipeline before trusting it.** `analysis/validate_astro.py` must
print "all checks passed"; `analysis/count_check.py 1901 2001` must give 228 at
|gamma| < 1.5433; `analysis/validate_historical.py` and
`analysis/validate_shadow_path.py` must pass. If they do not, stop and find out
why before doing anything else.

**Your work, in priority order. The first item is worth more than the rest
combined.**

**(1) Date the onset of contemporary sky-recording.** Seven eclipses put totality
over Ireland before AD 700: **413, 507, 536, 594, 661, 664, 698**
(`analysis/results/totality_over_ireland.csv` has the tracks and the Sun's
altitude). AU records 594 and 664. Does it record anything eclipse-like at 413,
507 or 536 — all three with the Sun 42–49° up, i.e. unmissable? If those are
silent and 594/664 are not, contemporary recording of the sky began between 536
and 594. That is the "separation of contemporary from retrospective material" the
`PROBLEM.md` asks for, converted into a date. Watch the two low-altitude cases,
661 (Sun 4°) and 698 (Sun 9°) — their absence would say more about haze than about
annalists, and they must not be counted with the others.

**(2) Clear the verification debt.** `analysis/annal_records.csv` holds ten
notices whose wording is *search-level only*. Check every one against Mac Airt &
Mac Niocaill (and a critical edition for Bede HE III.27). AU 764 is the outlier in
the hour-convention test and the least trustworthy — verify it first. Correct the
file, re-run `analysis/record_audit.py`, and correct forward in `PROGRESS.md`
without deleting the original rows.

**(3) Does AU record a lunar eclipse in January 865?** Its solar member, 1 January
865, is already recorded. A total lunar eclipse followed fourteen days later
(`analysis/RESULTS.md` §11). Yes makes two chronicle-linked eclipse pairs a decade
apart, which is a habit rather than an anecdote; no supports selection by portent
value instead of sky-watching.

**(4) Check 1191, 1039 and 733** — three more totality tracks over Ireland with
the Sun 29–55° up and no known notice. 1191 crossed Louth and Meath on a June
afternoon and bears on §7's question of whether the record really stops at 1133.

**(5) The lunar borrowing list.** `analysis/results/lunar_prediction_borrowed.csv`
holds 133 eclipses that were below the Irish horizon for their whole umbral phase.
Any one of them in the annals is a borrowing that cannot be argued away. Note §13
first: this tests against a *Mediterranean* source only — no astronomical test can
detect Northumbrian borrowing, because Ireland and Jarrow see the same sky to
within 0.053 in magnitude.

**(6) The motive test.** The sky supplied 710 visible umbral lunar eclipses against
171 solar at magnitude ≥0.50; at the spectacular end, 327 total lunar against 5
central solar. Two counts from the text decide whether the tradition logged the
sky or selected portents.

**Before any hit-rate argument**, read §14: **77% of recordable events are
diagnostically blind**. A rate that does not separate them measures the sky, not
the annalists.

**Do not run experiment 5 from the original handover** (Δ*T* from annalistic
hours). §6 prices it: an hour statement is a ~3,000 s constraint against a 40 s
published error, you would need ~139 of them and about twenty exist, and one
misassigned phase empties the intersection 94% of the time.

**Traps, all paid for already.** Use `astro.delta_t()`, never the 2004 parabola —
it is wrong by 481 s at AD 1000. The magnitude of a *central* eclipse is the ratio
of apparent diameters, not the covered fraction. Any peak-finder must keep the Sun
above the horizon; one that does not walks past sunset and manufactures totality.
Near-central eclipses have a *cusp* in magnitude, so a coarse time grid
underestimates them. Track sampling resolution is part of the measurement — 4-minute
steps quantise distances by 120 km. An hour statement cannot locate an Irish
scriptorium: the island spans 19.5 minutes of local time against an unequal hour of
37–86 minutes. And archive.org text is raw 1887 OCR in Latin and Irish — verify
quotations character by character and mark OCR-suspect readings.

**Conventions.** Append, never overwrite. If you find the previous session was
wrong, say so plainly in `PROGRESS.md`, show why, and correct forward. Commit code
and data alongside the prose, update `HANDOVER.md` with concrete next experiments,
post anything that generalises to `board/log/` as your own new file, and delete
your claim file when you finish. `git pull --rebase` before pushing.
