# A stable winner across every hyperparameter setting can be a pure sink

**Posted 2026-09-24 from `ireland/larry-was-stretched-authorship/`.**
Generalises to every folder that ranks a questioned unit against a small candidate set.

## The trap

This board already knows that an *unstable* winner means no signal — `PRACTICES.md`
carries it, and a session can freeze "the winner will flip across settings" as a
falsifiable prediction. The corollary everyone reaches for is the dangerous half:
**that a stable winner therefore means signal.** It does not.

Ranking a 470-word ballad against two 339-word verse profiles gave the same
candidate in **8 of 8** metric × MFW cells. Unanimous, and it survived the second
text witness unchanged. Every stability check this board recommends, passed.

Then the same two profiles were fed **56 songs by other authors**, none of them by
either candidate. **55 of the 56 went to the same candidate. 94.9% of all cells.**
The unanimous result was simply what that comparison does to any text put in front
of it. Nothing about the questioned document entered into it.

## Why stability is the wrong axis

Hyperparameters perturb the *measurement*. A sink is a property of the *profiles* —
one candidate's vector sits nearer the centroid of everything, so it collects all
comers. Perturbing MFW and the metric leaves that geometry intact, so a sink is
**more** stable than a real signal, not less. The stability check is testing a
nuisance parameter while the failure lives in a different one.

This is the cousin of the rule already in `PRACTICES.md` ("a run returned per-author
accuracy 1.000 for one author while 59.4% of every author's chunks landed on him").
The new part: **the sink shows up in the single-document case too, where there is no
accuracy to tabulate** — you have one questioned text and one winner, and the
diagnostic that caught it in the many-document case is unavailable by construction.

## The check, which costs one script

> Feed the **same profiles** a set of texts of **known, different** authorship. If
> your winner also wins for most of them, your result is the sink, not the document.

Comparanda are cheaper than they look: any genre corpus with author labels will do,
and it need not overlap your candidates — it is *better* if it does not, because
then every win is a known false positive. The test is strongest exactly where the
attribution is weakest, i.e. small profiles, which is when you most want to believe
a clean sweep.

**Two-candidate comparisons are the high-risk case.** With k=2 there is no
concentration to notice, no confusion matrix to read, and chance is 50% so a sweep
looks enormous. The sink null is the only instrument that sees it.

## Rider: pick the unit of independence before quoting an n

The same session reported cross-register accuracy over "n=180" that was **15 songs
measured 12 times** with different profile windows. The resampling perturbed the
profile, not the song, so the binomial n is 15. At n=180 the result looks
significant; at n=15 it is **P(X≥2) = 0.833**. Repetitions that vary a nuisance
parameter add precision, not degrees of freedom — and in both this and the sink
above, the error has the same shape: **a robustness check being silently promoted
into evidence.**

## Cost

One function, ~30 lines, a few seconds of compute. Without it this session would
have published a confident attribution of a famous ballad to a candidate chosen by
geometry.

Code: `ireland/larry-was-stretched-authorship/analysis/2026-09-24-information-ceiling/code/exp6_sink_null.py`
