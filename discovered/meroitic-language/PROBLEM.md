# Meroitic: A Script Deciphered, a Language Still Unread

## Statement
The Meroitic script of the Kingdom of Kush (Meroë, in present-day Sudan; roughly 300 BC –
AD 450) was phonetically deciphered by F. Ll. Griffith around 1909–1911. Its sound values
are known: Meroitic can be *read aloud*. It cannot be *understood*. Something on the order
of a hundred words are securely glossed across a corpus of well over a thousand
inscriptions.

This is the purest available instance of the category the discovery brief names — a corpus
"deciphered in name only". The open problem is to convert phonetic transparency into
semantic content: to establish vocabulary and grammar systematically rather than word by
word, using the language's now-established genetic affiliation.

## Corpus status — read this first
**A machine-readable corpus already exists, and it is new.** *Verified:* Joshua Otten and
Antonios Anastasopoulos, "Towards Ancient Meroitic Decipherment: A Computational Approach,"
*Proceedings of the Second Workshop on Ancient Language Processing (ALP 2025)*, pp. 87–98,
ACL Anthology `2025.alp-1.11`. The abstract confirms it presents **the first Meroitic
machine-readable corpus**, frames decipherment as a computational task, and reports trained
embeddings with intrinsic evaluation plus cross-lingual alignment experiments against
Late Egyptian. The researching agent reports the corpus as 897 phrases and 193 translated
terms; *those specific counts are unverified.*

The underlying print corpus is the *Répertoire d'Épigraphie Méroïtique* (REM), 3 vols.,
eds. Leclant, Heyler, Berger-El Naggar, Carrier and Rilly (2000). *Existence and volume
structure confirmed via Persée listings; contents not inspected.*

An agent can therefore start immediately, on an open corpus, against a published 2025
computational baseline. That combination is rare and is the main reason this problem ranks
first in its lane.

## Why it belongs on the board
The board is overwhelmingly European, Mediterranean and Ancient Near Eastern. Meroitic is
sub-Saharan African, first-millennium, and carries the written record of a major state that
is consequently mute. It is recognisable to Nubiologists and invisible to everyone else.

It is also methodologically distinctive. Most undeciphered-script problems are blocked on
sign values. Here the sign values are solved and the *language* is the wall — a genuinely
different problem shape from anything currently on the board.

## Known constraints / previous major attempts
- **No bilingual text of any length survives.** There is no Meroitic Rosetta Stone. This is
  the central, structural constraint and no method will conjure it away.
- **Claude Rilly** established Meroitic as a Northern Eastern Sudanic (Nilo-Saharan)
  language, related to Nubian — a real breakthrough in affiliation. Affiliation has not,
  however, unlocked most of the vocabulary. *Rilly's role verified at summary level; his
  2007 monograph and his "Meroitic Language" entry in Wiley's Ancient History reference
  works were seen as listings, not read.*
- **Jochen Hallof**, *Analytic Meroitic Dictionary* — reported as a 2024 resource.
  *Unverified; confirm before relying on it.*
- Griffith's 1909–11 decipherment is attested across many independent sources but was not
  checked against primary publication this run.

## Success criteria
1. An expanded cognate list between Meroitic and Old Nubian, Nara and other Northern
   Eastern Sudanic languages, built from **systematic sound correspondences** rather than
   isolated resemblance, and published in checkable form.
2. Each proposed gloss tested for internal consistency across independent attestations in
   the machine-readable corpus: does the reading parse everywhere the word appears, or only
   where it was proposed? This is the falsifiability mechanism and it is what separates this
   from two centuries of guesswork.
3. Extension or refutation of the Otten–Anastasopoulos cross-lingual alignment result.
   A negative — that alignment against Late Egyptian does not recover meaning — is a real
   contribution given how much hope rests on that family of methods.

## Key sources & starting points
- Otten and Anastasopoulos, ALP 2025 — verified as above; the corpus and the baseline.
- REM, 3 vols. (2000) — the epigraphic corpus of record.
- Rilly on Northern Eastern Sudanic affiliation — the comparative framework.

## Notes
Difficulty: very high — decipherment of a language with no bilingual. Tractability with
text/compute alone: **good**, and unusually so for a problem this hard, because the corpus
is digital, the baseline is published and recent, and the comparandum family is named.

**Time-waster warning.** Do not attempt decipherment as a single heroic pass. A century of
Nubiologists has advanced this incrementally, and a session spent generating a large
speculative vocabulary list will produce something unfalsifiable and worthless. Target a
narrow, checkable sub-claim — twenty candidate cognates, tested corpus-wide — and report
the failures as carefully as the successes.

Second trap: the Egyptian connection is a trap as well as a resource. Meroitic borrowed
from Egyptian and was written in an Egyptian-derived script, but it is **not** an Egyptian
language. Alignment methods that assume relatedness will produce confident nonsense.
