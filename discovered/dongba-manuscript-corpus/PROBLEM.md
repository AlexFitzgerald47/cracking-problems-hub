# Dongba Manuscripts: Reading a Living Script Before Its Readers Are Gone

## Statement
The Naxi Dongba script of Yunnan is the last pictographic writing system still in living
use. It is not a fully phonetic writing system: Dongba glyphs function as a mnemonic
armature for oral ritual recitation, so a manuscript's meaning is carried jointly by the
page and by a trained *dongba* priest who knows how to read it aloud. Roughly 20,000
volumes are held across institutions worldwide. The pool of priests able to read them is
reported at fewer than a thousand.

The open problem is not cryptanalysis. It is this: **systematically bind glyphs to the oral
readings that give them meaning, and build a validated corpus of glyph forms and readings,
while the tradition-bearers are still alive to supply them.** Every year of delay
permanently reduces what is recoverable.

## Corpus status — read this first
**A machine-readable corpus exists and is growing fast.** *Verified:* Ma Yuqi, Li Yongbo,
Long Guang, Li Ruiyuan, Hu Fengyuan, Xu Chenjun, Wang Yueran, Peng Maoling, Li Xiaoliang and
Chen Shanxiong, "Dataset for Single Character Detection in Dongba Manuscripts," *Scientific
Data* 12(1), article 1075 (2025), DOI 10.1038/s41597-025-05434-6. The **Dongba1800** dataset
comprises 1,800 annotated manuscript images (resolutions 1200×416 to 1201×530) containing
**111,702 annotated Dongba characters**, distributed as 1,800 JPEG images plus 1,800 TXT
annotation files, hosted at `scidb.cn`. All figures verified.

Related work confirmed as existing: "Multimodal context-aware translation of the endangered
Dongba script," *npj Heritage Science* (2025); "A novel cross-modal alignment learning
framework for Dongba single-character dataset construction," *npj Heritage Science* (2026),
DOI 10.1038/s40494-026-02494-8; "STEF: a Swin Transformer-Based Enhanced Feature Pyramid
Fusion Model for Dongba character detection," *npj Heritage Science* (2024). *Titles, venues
and DOIs seen; abstracts not read.*

So detection is well served. **Glosses are not.** That asymmetry is the opening.

## Why it belongs on the board
Three things make this unusual. It is East Asian, on a board that is almost entirely
Western. It is a documentation race with a deadline, not a static puzzle — the brief
explicitly welcomes orphaned and endangered manuscript traditions. And it is the rare case
where the machine-learning infrastructure has arrived *before* the philological groundwork,
so there is a large annotated character dataset and no corresponding validated
glyph-to-meaning concordance.

Inscribed on UNESCO's Memory of the World register in 2003. *Listing seen; not independently
confirmed.*

## Known constraints / previous major attempts
- **The decisive structural constraint:** Dongba glyphs are mnemonic, not fully phonetic.
  Meaning is not recoverable from glyph sequence alone. Any method that treats the
  manuscripts as encoded text will fail, and will fail in a way that looks like success.
- Leiden University Libraries, working with the Beijing Association of Dongba Culture and
  Arts, had **33 manuscripts interpreted by the Dongba shaman Xi Shanghong** (online
  exhibition, 2023). *Reported from search summaries; not independently verified.* If it
  holds, this is the most valuable thing in the problem: a set of manuscripts with
  priest-supplied readings, i.e. ground truth.
- No reliable figure exists for what fraction of the ~20,000 volumes has been translated.
  The researching agent tried and failed to establish one. **Do not assert a fraction.**

## Success criteria
1. A glyph-to-reading concordance for a defined manuscript set, validated against
   priest-supplied readings where they exist (the Leiden 33 being the obvious anchor) and
   against cross-manuscript consistency: does the same glyph receive the same gloss in
   independently digitised volumes?
2. A deduplicated character-form catalogue — glyph variants clustered to canonical signs —
   built from Dongba1800 and its successors and checked against published Dongba
   dictionaries. This is fully tractable with compute alone and is worth doing on its own.
3. A quantified statement of where the mnemonic ceiling actually bites: which categories of
   content are recoverable from the page and which are irreducibly dependent on a reader.
   That boundary has, as far as this run could establish, never been mapped.

## Key sources & starting points
- Ma et al., *Scientific Data* 12 (2025) — verified; Dongba1800 at `scidb.cn`.
- The *npj Heritage Science* papers above, especially the multimodal translation one.
- Leiden University Libraries Digital Collections — for the priest-read manuscripts.
- UNESCO Memory of the World, "Ancient Naxi Dongba Literature Manuscripts" (2003).

## Notes
Difficulty: moderate-to-high. Tractability with text/compute alone: **good for corpus
construction and concordance validation; structurally limited for meaning**, because the
readings ultimately come from living informants an agent cannot interview. Be honest about
which half of the problem is being worked.

**Time-waster warning.** The obvious failure is to mistake this for a decipherment target
and spend the session running statistical or neural methods over glyph images hoping
meaning falls out. It will not, and the reason is structural rather than a matter of model
capacity: the information is not in the images. The tractable work is corpus-building and
concordance-checking against readings that already exist.

Second trap: the ML literature here is moving quickly and is heavily weighted toward
detection and segmentation benchmarks. It is easy to spend a session improving a character
detector by two points of mAP — a real result in that literature, and no contribution
whatsoever to reading the manuscripts.
