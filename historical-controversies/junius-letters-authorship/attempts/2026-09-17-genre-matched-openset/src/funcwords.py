"""Function-word inventory for topic-robust authorship features.

Content words carry subject matter, and subject matter is the confound here: Junius
writes about Grafton, Mansfield and the Middlesex election; Francis's letters are
about family, India and money. A most-frequent-word list built from the raw corpus
would be half topic. This list is closed-class only -- determiners, pronouns,
prepositions, conjunctions, auxiliaries, degree adverbs and a few high-frequency
discourse items. No proper nouns, no period-topic vocabulary.
"""
FUNCTION_WORDS = """
a about above after again against all almost alone along already also although always
am among amongst an and another any anybody anyone anything are around as at
be because been before being below beneath beside besides between betwixt beyond both
but by
can cannot could
did do does doing done down during
each either else enough even ever every everybody everyone everything except
far few for former formerly from further furthermore
had has hardly hath have having he hence her here hers herself him himself his how
however
i if in indeed instead into is it its itself
just
lest less lest like likewise little
many may me merely might mine more moreover most much must my myself
near nearly neither never nevertheless no nobody none nor not nothing notwithstanding
now
of off often on once one only or other others otherwise ought our ours ourselves out
over own
perhaps
quite
rather
same scarcely seldom several shall she should since so some somebody someone something
sometimes somewhat still such
than that the their theirs them themselves then thence there therefore these they this
those though thus till to together too toward towards
under unless until unto up upon us
very
was we were what whatever when whence whenever where whereas wherein whether which
while whilst who whoever whole whom whose why will with within without would
yes yet you your yours yourself yourselves
""".split()
FUNCTION_WORDS = sorted(set(FUNCTION_WORDS))
