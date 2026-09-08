"""A fixed, author-blind orthographic key for early modern English.

Chosen from the known printing conventions of the period, not from the outcome:

  u/v      positional allographs of one letter until the mid-17th century
           (`haue`/`have`, `vpon`/`upon`, `vs`/`us`)  -> map both to `v`
  i/j      likewise                                    -> map both to `i`
  y/i      free variation in many words                -> map both to `i`
  final e  silent, and progressively dropped in print  -> strip
  doubles  `looke`/`look`, `keepe`/`keep`, `poore`/`poor`, `ee`/`e`
                                                       -> collapse runs

Nothing here targets a lexeme. `hath`/`has`, `doth`/`does`, `thou`/`you`, `ye`/`you`
are genuine morphosyntactic change and are deliberately left unmerged: the test is
whether removing *orthography* alone changes the period result.
"""
import re

_APOS = re.compile(r"'")
_RUN = re.compile(r'(.)\1+')


def key(w):
    w = _APOS.sub('', w)
    if not w:
        return w
    w = w.replace('u', 'v').replace('j', 'i').replace('y', 'i')
    while len(w) > 2 and w.endswith('e'):
        w = w[:-1]
    w = _RUN.sub(r'\1', w)
    return w or '_'
