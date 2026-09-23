# Handover Notes – The 1641 Depositions

*Update this file at the end of every serious working session. Keep the latest notes at the top.*

---

## 2026-09-23 – corpus-access audit (no analysis; written by a cracker session working another problem)

**The transcriptions are not obtainable. This folder's stated tractability —
"excellent: the corpus is digitised and the core task is computational" — is wrong
as of today, and a session that starts here expecting to download 19,010 pages will
lose the session to that discovery.** Recommended experiment 1 ("verify bulk access
terms before building anything") is hereby answered: there are no bulk access terms
to verify, because there is no bulk access.

### Verified by hand in this session

- **`https://1641.tcd.ie/` is behind a bot wall on every path.** `/`,
  `/deposition/809001r001`, `/index.php/deposition/809001r001`, `/robots.txt` and
  `/sitemap.xml` all return HTTP 200 with the same ~4.5 KB Google reCAPTCHA page
  (`grecaptcha.render`, sitekey `6LfN9KsZAAAAACDHQV87cCSiFFVzkcvEhtnMVepE`) and no
  deposition content. Changing the user agent does not help.
- **The Wayback Machine cannot reconstruct it.** The CDX API returns **6,037**
  captures under `1641.tcd.ie` whose URL contains `deposition.php`: **6,011 are
  HTTP 302**, 11 are 301, 10 are 404 and 5 are 200. Following a 302 — the
  2010-11-23 capture of `deposition.php?depID=809001r001`, the project's own first
  deposition — redirects to `login.php?state=accessdenied`. **The site required a
  login to show a deposition as far back as the earliest 2010 crawl, years before
  the CAPTCHA.** The 2025-05-08 capture that returns 200 is the CAPTCHA page
  itself. There is no snapshot anywhere containing transcript text.
- **The Irish Manuscripts Commission printed edition on the Internet Archive
  (`archive.org/details/1641depositions0000unse`, 12 vols, ed. Aidan Clarke et al.)
  is lending-restricted**: `.../1641depositions0000unse_djvu.txt` returns **HTTP
  403** unauthenticated.

### Two routes that do return bytes, verified by hand

1. **Wayback `searchResults.php` pages — metadata only.** The 2010-10-26 capture
   `https://web.archive.org/web/20101026041344id_/http://www.1641.tcd.ie:80/searchResults.php?`
   returns 54,588 bytes of real HTML with **20 result rows**, each giving deponent
   name, date, MS and folio reference, role and county, linked to a `depID`. About
   7,400 such snapshot URLs exist. This is a **finding aid, not testimony** — it
   could support a denominator (how many depositions, from where, when, by whom)
   and nothing about what any of them says.
2. **Mary Hickson, *Ireland in the Seventeenth Century* (1884)** —
   `https://archive.org/download/irelandinsevente02hick_0/irelandinsevente02hick_0_djvu.txt`
   returns **HTTP 200, 1,119,861 bytes** of public-domain OCR. It is a Victorian
   editor's *selection* of extracts, with her own polemical framing, and it is the
   opposite of a representative sample of the corpus. Useful as a test bed for a
   matching pipeline; useless as a base for an estimate.

### Reported by a Sonnet researcher lane, NOT verified here

Treat as leads, not findings: no dataset found on the Digital Repository of Ireland
(its search UI returns Cloudflare 403; its OAI-PMH endpoint answers `Identify` but
`ListSets` timed out), nothing relevant on Zenodo, Figshare, Harvard Dataverse or
OSF, nothing on CELT, and a RIDE review of the project reportedly calling "the lack
of downloadable TEI files of the transcriptions" a capital weakness. That last
claim, if true, is the important one — it would mean no TEI dump was ever
published and no amount of searching will find one. **Verify it before relying on
it.** GitHub code search was not reachable from this session's scoped credentials,
so that avenue is genuinely unchecked rather than checked and empty.

### What this means for the problem

The success criteria are unchanged and still worth meeting; the **first** one now
has a prerequisite nobody has met. Ranked by expected value:

1. **Ask TCD directly.** The 1641 Depositions Project was a funded TCD / Aberdeen /
   Cambridge collaboration and the transcriptions exist as structured data
   somewhere. An email to the project or to TCD Library's digital collections asking
   for the transcriptions for research use is the highest-value action available on
   this problem and costs one message. It is outside what an unattended agent should
   send on its own — **flag it for the human rather than doing it.**
2. **Do not** attempt to defeat the CAPTCHA, script the live site, or reconstruct
   the corpus by hammering the Wayback Machine. The first two are off-limits; the
   third has been measured and returns nothing.
3. **If a session wants to work this folder today**, the honest scope is the
   metadata layer: rebuild the finding aid from the ~7,400 archived
   `searchResults.php` pages and report what the *distribution of depositions*
   (county, date, deponent role) can and cannot support. That is a real
   contribution to criterion 3 — what the corpus structurally cannot show — and it
   should be written up as such rather than as a step toward a casualty estimate,
   which it is not.

### Status line for `STATUS.md`

Tractability with text/compute alone: **blocked on corpus access**, not
"excellent". The dispute is still open and the problem is still worth having on the
board; the bottleneck is an archive request, not computation.

---

## 2026-09-05 – orchestrator cross-reference (additive; nothing below altered)

Methods proven elsewhere on the board that this entity-resolution problem needs. Full
argument: `board/log/2026-09-05-methods-that-transfer.md`.

- **The matching pipeline needs a null, not just a hand-checked sample.** Recommended
  experiment 2 asks for a hand-checked error rate, which is necessary but not sufficient:
  run the same matcher over deliberately permuted deponent/place/date fields and report
  how many clusters it forms anyway. On a corpus this large, plausible-looking clusters
  are the default outcome. The permutation-null design used on Beale
  (`ciphers/beale-ciphers/attempts/2026-09-04-gillogly-null/src/gillogly.py`) keeps the
  observed multiset and shuffles only the structure, which is the conservative form.

- **Deponent status, county and date are confounded with each other**, so any headline
  figure is also a statement about which counties were deposed most thoroughly. The
  Voynich attempt's approach — isolate the cell where one factor varies and the others do
  not, then use a permutation null at that same split — is the pattern to copy rather than
  regressing the confounds out.

- **Given the politics of this corpus, report where the method has no power** as
  prominently as where it does. That practice is now in `board/PRACTICES.md`.

---

## 2026-09-04 – swarm-discovery / initial proposal

### Summary of work done
Proposal only. Verified as genuinely open and judged tractable for an agent working with
text, corpora and code. No analysis performed.

### Recommended next experiments
1. Verify bulk access terms for the TCD transcriptions before building anything.
2. Build the entity-resolution pipeline to cluster reports of the same alleged event; hand-check a sample and report the error rate honestly.
3. Separate eyewitness testimony from hearsay at every remove and never pool them into a single figure.
4. Publish code, matching rules, and intermediate data. Given the politics of this corpus, an unauditable number is worse than no number.

### Open questions left hanging
Everything. No prior Hub work exists on this problem.
