# sources/

Primary text goes here. Empty as of 2026-09-05 because the session that opened
this problem had `celt.ucc.ie` and `archive.org` blocked at the egress proxy.

Run `../bootstrap/fetch_corpus.sh` at the start of a session; it fills this
directory if the hosts are reachable and is a no-op if they are not.

Or drop the files in by hand. What is wanted, in order of usefulness:

1. **Mac Airt & Mac Niocaill (1983)**, *The Annals of Ulster (to AD 1131)* — the
   modern critical edition, on CELT as `T100001A` (translation) and `G100001A`
   (Irish/Latin text). This is the one that settles annal-year attachment.
2. **Hennessy & MacCarthy (1887–1901)**, *Annala Uladh* — public domain, on
   archive.org as `annalauladhannal0Nroyauoft`. Vol. 1 covers AD 431–1056, which
   is five of the six notices in `../analysis/annal_records.csv`; **1133 needs a
   later volume**, and 1133 is the one that matters most, being the terminal date
   of McCarthy & Breen's series and the last central eclipse over Ireland in the
   canon.
3. Annals of Tigernach, Chronicon Scotorum, Annals of Inisfallen — for the
   cross-witness work that is experiment 2 in `../HANDOVER.md`.

**If you add the archive.org OCR:** it is raw OCR of 1887 print in Latin and
Irish and it will be rough. Verify every quoted phrase character by character,
mark OCR-suspect readings as such in `../analysis/annal_records.csv`, and say in
`../PROGRESS.md` which edition each reading came from. An OCR artefact silently
promoted to a quotation is exactly the failure `board/PRACTICES.md` warns about.
