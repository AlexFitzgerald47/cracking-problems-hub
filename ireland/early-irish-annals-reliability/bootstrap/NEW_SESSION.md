# Starting a new session on this problem

Three things: what to set in the cloud environment, what the environment does for
you automatically, and the prompt to paste. The prompt works whether or not the
environment changes were made — it checks rather than assumes.

---

## 1. Environment settings (one-time, in the UI)

An agent cannot change its own network policy; it is enforced at the egress
gateway from the environment's saved configuration. Set it at
**claude.ai/code → environment selector → edit the environment**.

**Network access:** change from **Trusted** to **Custom**, then in **Allowed
domains** paste:

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

**Tick "Also include default list of common package managers"** — without it you
lose PyPI and the eclipse engine cannot install `pymeeus`.

The `*.` prefix matters for archive.org: full-text downloads redirect to
`ia######.us.archive.org` nodes.

**Setup script:** paste the contents of `bootstrap/setup.sh`.

Changes apply when a VM is provisioned, so **a running session will not pick them
up** — start a new session.

## 2. What the setup script does for you

* creates `.venv` with `pymeeus` and `numpy`;
* clones the Stephenson Δ*T* reference implementation from GitHub (which works at
  every access level, because GitHub goes through its own proxy);
* probes every host the board depends on and writes `.session-environment.md` at
  the repo root, so the agent starts knowing what it can reach.

None of it fails the session. A blocked host is reported, not fatal.

---

## 3. The prompt

Paste this into a new session on branch `claude/irish-problems-progress-o6q34y`.

> You are a cracker in the Cracking Problems Hub. Read `AGENT_INSTRUCTIONS.md`,
> `STATUS.md`, `_roles/CRACKER.md` and `board/PRACTICES.md` first.
>
> **Before planning anything, establish your constraints.** Read
> `.session-environment.md` if the setup script wrote one; otherwise probe
> directly — `curl -sS -o /dev/null -w '%{http_code}' https://celt.ucc.ie/` and
> the same for `archive.org`. `000` means the egress proxy denied it; do not
> retry and do not route around it. Then run
> `ireland/early-irish-annals-reliability/bootstrap/fetch_corpus.sh`.
>
> You are continuing `ireland/early-irish-annals-reliability`, worked on
> 2026-09-05. Read `PROGRESS.md`, `HANDOVER.md` (including its amendment) and
> `analysis/RESULTS.md` before touching anything. Claim it in `board/active/`.
> Verify the pipeline before trusting it: `analysis/validate_astro.py` must print
> "all checks passed" and `analysis/count_check.py 1901 2001` must give 228 at
> |gamma| < 1.5433.
>
> **If CELT or archive.org are reachable**, your job is experiments 1–3 in
> `HANDOVER.md`, in that order: clear the verification debt on the six notices in
> `analysis/annal_records.csv` (their wording is search-level only, and Results 1
> and 2 rest on it); extend that file to the full 442–1133 astronomical corpus;
> then run the experiment already specified and priced in
> `analysis/results/prediction_irish.csv` and `prediction_borrowed.csv`. Note the
> base rate in `analysis/results/visibility_summary.txt` before you start — the
> test is blind on 28 of the 132 candidate eclipses and saying so is part of the
> result.
>
> **If they are blocked**, do not start a corpus problem and do not write a
> literature review. Read `board/log/2026-09-05-egress-blocked-corpora.md` and
> pick work whose evidence is computable rather than downloadable. On this problem
> that means experiment 5 in `HANDOVER.md` — inverting the annalistic hour
> statements into a Δ*T* constraint — or extending `analysis/lunar_eclipses.py` to
> the full lunar canon. Elsewhere on the board, Beale 3 and Kryptos K4 are pure
> compute and unaffected.
>
> Four traps, all paid for already:
> * Use `astro.delta_t()`, never the 2004 parabola — it is wrong by 481 s at
>   AD 1000, which is 2° of Earth rotation.
> * The magnitude of a *central* eclipse is the ratio of apparent diameters, not
>   the covered fraction. Getting this wrong biases every deep eclipse low.
> * The five-of-five hit rate in Result 2 is partly circular and is labelled as
>   such. Do not quote it as evidence.
> * archive.org text is raw 1887 OCR in Latin and Irish. Verify quotations
>   character by character; mark OCR-suspect readings.
>
> Append, never overwrite. If you find the previous session was wrong, say so
> plainly in `PROGRESS.md`, show why, and correct forward. Commit code and data
> alongside prose, update `HANDOVER.md`, post anything that generalises to
> `board/log/`, and delete your claim file when you finish.

---

## 4. Generic variant, for any Hub problem

Replace the middle three paragraphs with:

> Choose work per `_roles/CRACKER.md`. Weight your choice by what
> `.session-environment.md` says you can reach: a problem whose corpus is behind a
> blocked host cannot be started, and picking one anyway produces the literature
> review that `_roles/CRACKER.md` names as this board's most common failure mode.
> Prefer a problem whose evidence is computable, or make building a reachable
> corpus the deliverable.
