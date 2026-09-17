# The Byblos Syllabary (Pseudo-Hieroglyphic Script)

## Statement
Establish what can be legitimately concluded about the Byblos syllabary — a small
corpus of Egyptian-influenced inscriptions from Byblos, usually dated to the early
second millennium BC — given that the corpus is far too small for unconstrained
statistical decipherment and that every proposed full decipherment to date has failed
to convince. The realistic target is not a free translation but a rigorous audit: which
structural and phonetic claims survive external controls, which variant groupings are
defensible, and which proposed decipherments can be positively excluded.

## Why it belongs on the board
Byblos is the sharpest available test of an uncomfortable methodological question the
Hub will face repeatedly: **what is the honest epistemic ceiling on a corpus this
small?** With roughly a few dozen certain/possible witnesses and a large, contested sign
inventory, the sign-to-token ratio remains severe. Multiple full decipherments have
nonetheless been published, mutually incompatible, each internally satisfying to its
author.

That makes this valuable in a way a speculative translation would not be. A defensible
demonstration of what *can* and *cannot* be concluded — and a method for exposing why
over-fitted decipherments of tiny corpora feel convincing — is directly transferable to
Phaistos, Dorabella and other Hub problems. The script's position matters too: it sits
between Egyptian graphic traditions and the early alphabet, so its dating and affinities
bear on the origin of alphabetic writing.

## Known constraints / previous major attempts
- The original Dunand core is small, mostly bronze spatulae and stone, with a large number
  of graphic variants and disputed grapheme-type merges.
- **An open machine-readable corpus now exists.** The OCBI / Center for Decipherment
  source transcribes 18 witnesses as `BYBL` and 14 more as `BYBL?`, exposes raw PUA
  glyphs, directions and multiple alternative working syllabaries. The Hub's original
  assumption that no such corpus existed is obsolete.
- **A partial external control exists.** An Egyptianizing cylinder seal (`BYBL ra–rc` in
  OCBI) copies the Amarna royal-family scene and carries three short inscriptions aligned
  with Meritaton, Meketaton and Ankhesen(pa)amun. Mäder (2021) proposed externally
  grounded `me` and `pa` values; GEAS also treats the shared terminal `` as an
  `ATON` logo-phonogram and `` as an `AMUN` compound. The seal's provenance/script
  classification is not equivalent to a stratified Dunand find, so every use of it must
  state that dependency.
- Schmutz & Mäder (2024) use the daughter-name control to reject Woudhuizen/Best; they
  state that Mendenhall's values fail the same held-out name test. Those full systems
  should therefore no longer be treated as live defaults unless materially revised.
- Archaeological contexts are unclear, and the dating is genuinely elusive. Benjamin
  Sass (2019) has argued for affinities with early Phoenician inscriptions and a much
  later origin. The Hub's 2026-09-08 pass instead proposed a diachronic model: an older
  core plus a later linearized terminal phase replaced by Phoenician. This remains a
  falsifiable chronology model, not an absolute date.
- Recent computational work exists on word-boundary detection and variant grouping. The
  public OCBI source carries several mutually different working syllabaries, which makes
  variant adjudication part of the decipherment rather than clerical preprocessing.

## Success criteria
1. A reproducible structural audit: sign inventory with documented variant-merging
   decisions, positional statistics, and an explicit power analysis stating what a
   corpus of this size can and cannot support.
2. Positive exclusion of one or more published decipherments by a held-out or otherwise
   externally grounded test. **Partly achieved:** the Amarna daughter-name control
   excludes Woudhuizen/Best and Mendenhall as published systems; see
   `PARTIAL_BIGRAPH_KERNEL.md` for the Hub audit and prior-art boundary.
3. Progress on the dating question by systematically separating core, linear/palimpsest
   and later comparanda rather than assigning one date to every sign form.
4. Convert the partial bigraph into cross-text predictions that are tested on the Dunand
   core **with the cylinder left out**. This is the critical bridge from a few external
   anchors to a genuine decipherment.
5. A stated, defensible ceiling: what additional bilingual, repeated formula, secure
   archaeological context or externally identified proper name would be required for a
   full decipherment.

## Key sources & starting points
- OCBI source/transcription —
  https://github.com/elamicon/elamicon/blob/master/src/Scripts/Byblos.elm
- Mnamon, "Byblos (Pseudo-hieroglyphic)" —
  https://mnamon.sns.it/index.php?page=Scrittura&id=3&lang=en
- Michael Mäder, "Zwei Lautwertvorschläge zum Byblos-Syllabar: me und pa" — public
  author copy embedded at https://www.researchgate.net/publication/366580046
- Elizabeth Schmutz & Michael Mäder (2024), assessment of Woudhuizen/Best —
  https://center-for-decipherment.ch/journal/2024_01__Schmutz-%26-Maeder__Die-Byblos-Schrift_Beurteilung-Woudhuizen-Best.pdf
- Benjamin Sass, "The pseudo-hieroglyphic inscriptions from Byblos, their elusive
  dating, and their affinities with the early Phoenician inscriptions" (2019).
- George E. Mendenhall, *The Syllabic Inscriptions from Byblos* (1985) — historically
  important, but its value system is not compatible with the daughter-name control.

## Current Hub state

Two concrete advances now exist:

- `PALIMPSEST_CHRONOLOGY.md` — separates genesis, late linearization and Phoenician
  replacement; pressures a ca. 900 BCE *invention* without pretending to prove Dunand's
  exact early date.
- `PARTIAL_BIGRAPH_KERNEL.md` — freezes the Amarna daughter-name control, distinguishes
  published prior art from new Hub work, and externally adjudicates one inventory merge:
  `` and `` should not be normalized to one grapheme when using the bigraph. The OCBI
  source itself moves from a merged group in Syl2–Syl5 to a split in Syl6–Syl8, while its
  small `syllableMap` still retains the stale `ATON ` representative.

Difficulty: full decipherment remains high. Tractability of the audit is now **good**
because the corpus is machine-readable and there is at least one external name control.

Time-waster warning: do not generate a new full translation from visual resemblance or a
handful of anchored values. The next valuable result must predict structure in material
that was not used to establish the anchors.
