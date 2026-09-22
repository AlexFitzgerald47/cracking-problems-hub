# The Singapore Stone (Kallang Inscription)

## Statement
**The named unknown:** what language and script underlie the inscription on the Singapore
Stone — a large sandstone monolith, plausibly dated between the 10th and 14th centuries CE,
that stood at the mouth of the Singapore River until East India Company engineers blew it
apart in 1843 (final destruction sometimes dated 1848) to widen the river mouth? Of roughly
four fragments made at the time, only one survives (National Museum of Singapore, returned
from Calcutta in 1919); a related "Calcutta Stone" fragment is held at the Indian Museum,
Kolkata. The script resembles, but does not exactly match, the Kawi family of Old
Javanese/Sumatran Brahmic-derived scripts, and per the Wikipedia summary of the object "the
writing system on its surface is unique, never found anywhere else." The underlying language
is undetermined, with Old Javanese, Old Malay, Sanskrit and Tamil all proposed as candidates
in the literature. Over 90% of the inscribed surface is lost.

A genuine crack here is not "read the inscription" — the physical loss almost certainly
forecloses that — but a falsifiable, bounded structural question: does the surviving sign
repertoire statistically cluster closer to a specific dated regional Kawi variant (Old
Javanese vs. a Sumatran/Srivijayan-adjacent variant) than to unrelated scripts, under an
explicit similarity metric and null comparison?

## Corpus status — read this first
**Must largely be built.** No standardized public digital sign-inventory or comparative
dataset for this specific inscription is currently known to exist. What is available to build
one: photographs of the surviving fragment (museum-published); the 2024 academic
documentation of the object (below); 19th-century engravings and rubbings made before/at the
time of destruction (the Crawfurd/Laidlay-era record, reproduced in period journals such as
the *Journal of the Indian Archipelago and Eastern Asia*), which are themselves artist
renderings and a real source of transcription noise, not raw data; and comparative Kawi
corpora from dated Old Javanese and Sumatran inscriptions. A March 2026 computational
reconstruction effort (below) exists but performs reconstruction, not decipherment, by its own
authors' account, and should be independently checked rather than taken on faith.

## Why it belongs on the board
Southeast Asian and non-Western, an area repeatedly flagged across prior discovery runs as
under-represented on this board. It is also a structurally distinct problem from the
undeciphered-script cases already on the board or excluded as chestnuts (Indus, Rongorongo):
here the script family is plausible and partially constrained, but the exact sign values and
underlying language are not, which is a different and arguably more tractable shape of
problem than a wholly unknown script.

## Known constraints / previous major attempts
- **Verified directly (fetched 2026-09-22):** Chia, J. and Lee, I-S., "The Singapore Stone:
  Documenting the Origins, Destruction, Journey and Legacy of an Undeciphered Stone Monolith,"
  *Histories* 3(3):19 (2023/2024), MDPI, DOI `10.3390/histories3030019` — title, journal and
  DOI confirmed via direct search; the paper explicitly still treats the object as
  undeciphered. *Author initials as reported by research; not independently cross-checked
  against the paper's own byline.*
- **Verified directly (fetched 2026-09-22):** The Conversation / phys.org, "The Singapore
  Stone's carvings have been undeciphered for centuries — now we're trying to crack the
  puzzle" (June 2024), reporting work by Xi'an Jiaotong-Liverpool University researchers.
  `https://theconversation.com/the-singapore-stones-carvings-have-been-undeciphered-for-centuries-now-were-trying-to-crack-the-puzzle-231640`
- **Verified directly by full fetch (2026-09-22):** The Conversation, "Cracking the code: How a
  'prediction machine' is resurrecting the Singapore Stone" (~March 2026),
  `https://theconversation.com/cracking-the-code-how-a-prediction-machine-is-resurrecting-the-singapore-stone-276642`.
  Confirms the inscription is **still described as unresolved as of 2026** ("the Singapore
  Stone remains one of History's great unsolved codes"). The described tool, "Read-y
  Grammarian," together with a cross-inscription framework sometimes called "M-RADAR,"
  digitizes the inscription, predicts missing characters via frequency/statistical methods,
  and tests candidate languages by adjusting grammar rules — but the article explicitly states
  "this is not the same as actually reading the inscription," and separately that the surviving
  fragments are "too small to support reliable frequency analysis," a limitation stated by the
  researchers themselves. **Treat any specific "reconstructed reading" from this effort as an
  unconfirmed claim requiring direct verification against primary photographs, not as an
  established result** — it has not yet been shown to this run as peer-reviewed, and its own
  authors describe it as reconstruction/prediction rather than decipherment.
- Wikipedia's "Singapore Stone" article corroborates the 1843/1848 destruction, four fragments
  sent to Calcutta, one returned in 1919, and the script's uniqueness — used here as background
  orientation, not as a primary source in its own right.
- A related October 2023 comparative-paleography effort (Southeast Asian Archaeology blog),
  reportedly by a teenage independent researcher, compared the surviving fragment against the
  Calcutta Stone fragment. *Reported by initial research; not independently fetched or
  confirmed this run.*

## Success criteria
1. **A documented digital sign-inventory of the surviving fragment**, built directly from
   photographs, clearly distinguishing signs attested on the surviving stone from signs
   attested only in 19th-century engravings of the now-lost portions (the two have very
   different reliability and must not be merged silently).
2. **A comparative-paleography test** of that inventory against dated Old Javanese and
   Sumatran/Srivijayan-adjacent Kawi corpora, using an explicit similarity metric and a null
   comparison against an unrelated control script, reporting which regional variant (if any)
   the surviving signs resemble more closely than chance.
3. Explicitly **not** a claim of full-text recovery. A negative result — that the surviving
   evidence is too sparse to discriminate between candidate script variants or languages under
   any defensible statistical test — is an acceptable and valuable outcome given how little
   text physically survives.
4. Independent verification (not just citation) of any specific claim emerging from the 2026
   "Read-y Grammarian"/M-RADAR reconstruction work, checked against the primary photographs
   rather than accepted from press coverage.

## Key sources & starting points
- Chia & Lee, *Histories* 3(3):19 (2023/2024), DOI `10.3390/histories3030019` — the fullest
  documentary treatment located; *verified to exist, full text not yet read by this run*.
- The Conversation, June 2024 and ~March 2026 articles (URLs above) — *both fetched directly
  and verified*.
- Wikipedia, "Singapore Stone" — background orientation only.
- National Museum of Singapore — holder of the surviving fragment; museum photographs are the
  primary evidence base for any sign-inventory work.
- Indian Museum, Kolkata — holder of the related "Calcutta Stone" fragment.
- 19th-century engravings/rubbings in period journals (*Journal of the Indian Archipelago and
  Eastern Asia*; Straits Settlements-era records) — *existence well attested in the secondary
  literature; specific volume/page references not yet located by this run*.

## Notes
Difficulty: very high for full decipherment (structurally close to impossible given the extent
of physical loss). Tractability with text/compute alone for the bounded sign-inventory/
comparative-paleography sub-question: moderate — the raw materials are online, but assembling
a usable corpus from scattered museum photographs and 19th-century engravings is itself real,
nontrivial first-stage work, not a formality.

**Time-waster warning.** Do not chase "solve the inscription" — the object is so fragmentary
(over 90% lost) that any full-text claim will be unfalsifiable speculation dressed as
decipherment. Second, and specific to this problem right now: do not uncritically adopt the
2026 "Read-y Grammarian"/M-RADAR reconstruction as an established reading. It is recent, its
coverage so far is press/blog-level rather than a confirmed peer-reviewed publication this run
could independently verify, and its own authors state the underlying fragments are too small
for the statistical methods it depends on. Verify any specific claim from that work against the
primary photographs before building on it.
