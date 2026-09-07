# Method note — scope direction before semantic negative controls

**Origin:** Linear A KI-RO / KU-RO pass, 2026-09-07.

A semantically related term is not a valid negative control merely because it occurs in the same document genre. First establish which side of the marker it scopes over.

In the Linear A administrative corpus, KU-RO is a closing marker: quantities before it are summed and compared with the quantity after it. A recent computational pipeline therefore uses a backwards-looking section for KU-RO. The same routine was also applied to KI-RO as a contrast. Direct tablet inspection shows that KI-RO often behaves differently: on HT88 and HT94b it opens a following list whose unit entries are later closed by KU-RO; the pattern then predicted the structure of held-out HT117 correctly.

So the reproducible result “KI-RO does not total the preceding section” was not a useful semantic negative control. The parser was pointed in the wrong direction for the contrast term.

## General rule

Before comparing two markers with the same statistic:

1. classify each marker's scope direction and structural role without using the target arithmetic/semantic outcome;
2. preregister the appropriate window for each role (preceding block, following block, scalar field, etc.);
3. apply the null model within that grammar rather than forcing both markers through one parser;
4. preserve the mis-specified control as a documented failure, because a perfectly reproducible null result can still be semantically meaningless.

Linear A write-up: `historical-texts/linear-a/analysis/2026-09-07-kiro-scope-residual.md`.
