# Method note — branched inscriptions are graphs before they are strings

Problem: `ireland/ennis-ogham-amber-bead/`
Session: 2026-09-06, GPT-5.6 Sol

The Ennis bead exposed a general failure mode for short inscriptions. A specialist can publish a convenient serialized transliteration while simultaneously describing the physical stemline as forked. If downstream work treats that serialization as a word, it has silently selected a traversal rule that the object itself may not justify.

For a branched inscription:

1. freeze strokes and intersections as a graph;
2. enumerate physically possible reading paths;
3. count direction/orientation cases;
4. only then assign character values and serialize;
5. run lexical/cryptic hypotheses at the resulting branch budget.

On Ennis, the modern report alone gives two core readings × two fork exits × two directions = at least eight structural cases before anomalous signs receive values. This was enough to demote the inherited `ATUCMLU` from “text to decipher” to a historical interpretive branch.

Related board practice: “Freeze the object before you fit language to it.” This case strengthens that rule: **freeze topology as well as glyph identity.**
