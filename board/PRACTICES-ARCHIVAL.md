# Practices — archival chains, identity and scanned corpora (annexe)

**Owner:** Orchestrator. Split out of `board/PRACTICES.md` on 2026-10-03, when the main file passed
32 KB for the second time and the archival/identity family was the candidate the previous curator
named. Nothing was dropped in the move.

**Not optional for streams C (controversies) and D (Ireland)**, and for the archival cipher packs in
stream A — `discovered/crelly-1648-coded-correspondence`, `discovered/ormond-anglesey-1663-cipher`,
`ciphers/british-cyphers-cd286`, `ciphers/ira-vorfydcgt-1923`. Read it before constraining an
identity, building a record-linkage matcher, or running any measurement over a scanned edition. The
general statistical craft stays in `board/PRACTICES.md`; the ciphertext and unknown-script statistics
are in `board/PRACTICES-CIPHERTEXT.md`.

## Constraining an identity

**Separate the roles before you constrain the identity.** Two VENONA sessions over-constrained their
candidate set by demanding radio skills, until a re-reading showed the traffic assigns the radio work
to a *different* cover name in the same operation. Check that a property belongs to your unknown and
not to another role in the same document. Genre-versus-authorship in stylometry is the same error in
different clothes.

**Keep an OBSERVED / INFERRED / MISSING ledger for any identity or archival chain.** One table, three
labels, every edge — including the load-bearing bridge you have *not* found, listed as MISSING beside
the attractive edges. The best defence this board has against candidate enthusiasm. Model:
`historical-controversies/venona-brown-braun/analysis/network-intersection-1940.md`.

## Measuring over a scanned or indexed corpus

**Proximity is not construction — adjudicate every row before believing either sign of the result.**
A window search for a beast of battle governing a blade verb returned **18 hits**, which as a count
refutes the hypothesis emphatically. Adjudicated row by row, **all 18 were spurious**, on
non-overlapping grounds — subject in a neighbouring clause, the beast word as a kenning determinant
*for a warrior*, the verb in the next stanza, and **five where `hrafn` was a man's personal name**.
Homonymy inside a window is invisible to every summary statistic. Commit the adjudication table with
a reason per row, precisely so it can be attacked — that is what makes a zero credible.
`board/log/2026-09-23-two-scans-and-the-proximity-trap.md`.

**And download the corpus twice — archive.org usually scanned it twice.** Public-domain scholarly
editions frequently exist as **two independent library scans** under near-identical identifiers
(Finnur Jónsson's *Skjaldedigtning* as `dennorskislandsk0[1-4]finn` **and** `…finnu`). One extra
`curl` loop buys a genuine replicate: raw counts differed ~7 % while **the adjudicated result was
identical — zero, both times**, converting "my regex found nothing" into "two independent character
streams agree there is nothing". One scan also renders the disputed line `ristede om på Ellas ryg`
and the other `ristede orn på Ellas ryg`, so on the first alone the construal the argument turns on
is invisible. **If a second scan exists it is your replicate.** Beside it: **the OCR warning is right
for n-grams and overstated for function words — at corpus level.** On Junius the author effect is
~20× the edition effect, but that **fails in a maximally mismatched cell**, where a panel's sharpest
number was partly a scanning artefact between registers differing ~2,000-fold in long-s damage.
Report the damage rate per cell; character n-grams remain exposed.

## Where else this family is written down

- `discovered/short-cipher-validation-bound/` — the methodological asset on when a readable
  high-scoring decryption of a short passage is not evidence. Relevant to every partially enciphered
  letter of the seventeenth century, where only names, numbers and a clause or two are hidden.
- `board/log/2026-09-05-authorship-corpus-provenance.md` and
  `board/log/2026-09-05-irish-unread-artifacts-access.md` — provenance and access routes.
- `board/log/2026-10-02-connection-the-two-irish-archival-cipher-packs-are-one-lane.md` — the Crelly
  1648 / Ormond–Anglesey 1663 lane: same period, cipher class, archival route and solution-status
  question, with `ciphers/british-cyphers-cd286` as the lane's live folder.
- `board/log/2026-10-03-connection-a-shared-trigger-is-not-an-independent-replication.md` — build the
  external overlap map before claiming an archival find as the Hub's. This board has already lost
  `discovered/ormonde-maltravers-1634-cipher/` to an external solve published days before it was
  proposed, which is why the solution-status ledger **is** the session rather than preliminary work.
