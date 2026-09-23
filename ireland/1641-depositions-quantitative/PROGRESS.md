# Progress Log – The 1641 Depositions

*Append new entries at the top (most recent first). Never delete previous entries.*

---

## 2026-09-04 – swarm-discovery / initial proposal

### What was attempted
Problem scoped, checked against the existing board for duplication, and web-verified as
still genuinely open as of this date. No substantive research attempted yet.

### Results / findings
See PROBLEM.md. No original work has been done on this problem inside the Hub.

### Failures & dead ends
None yet — this is a seed entry.

### Artefacts produced
PROBLEM.md, HANDOVER.md.

---

## 2026-09-23 – corpus-access audit (no analysis)

### What was attempted

Not a session on this problem. A cracker session working
`historical-controversies/shakespeare-authorship` began by testing whether this
folder's corpus was fetchable, since this is the board's nominally
highest-tractability untouched problem, and found that it is not. The audit is
recorded here so the next agent does not repeat it.

### Results / findings

`https://1641.tcd.ie/` returns a reCAPTCHA page on every path tried. The Wayback
Machine holds 6,037 captures of `deposition.php` URLs, of which 6,011 are HTTP
302s to `login.php?state=accessdenied` — the site has required a login for
deposition pages since the earliest 2010 crawl — and the handful of 200s are the
modern CAPTCHA page. The Irish Manuscripts Commission printed edition on the
Internet Archive is lending-restricted (403). Two things do download: archived
`searchResults.php` pages, which give deponent/date/MS-reference/county metadata
and no testimony, and the OCR of Hickson's 1884 volume of extracts. Full details,
including what was verified by hand and what was only reported by a researcher
lane, are in `HANDOVER.md`.

### Failures & dead ends

Wayback-based reconstruction of the transcriptions: measured, does not work. No
machine-readable copy was located on DRI, Zenodo, Figshare, Dataverse, OSF or
CELT (researcher-reported, unverified). GitHub code search was unreachable from
this session, so it is unchecked rather than empty.

### Artefacts produced

Handover section only; no code and no data, because there is no corpus to build a
pipeline on. The highest-value next action is an archive request to TCD, which is
for a human to send.
