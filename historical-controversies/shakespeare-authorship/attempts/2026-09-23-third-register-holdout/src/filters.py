"""Authorship-validity filters for the holdout arm, applied from metadata only.

A holdout arm is worth nothing if its labels are wrong, and a panel dramatist's
TCP author string collects more than that dramatist wrote. Three hard filters,
all mechanical, all applied before any attribution is run:

E1 POSTHUMOUS. Drop a text printed after the author's death year, where the TCP
   author string carries one. This is the filter that matters most: it removes
   `A59994` (1692) - "The true impartial history ... of the Kingdom of Ireland",
   filed under `Shirley, James, 1596-1666.` twenty-six years after that Shirley
   died - and `A09230` (1627), the jest-book *about* George Peele (d. 1596),
   which is a book about him and not by him. Both would have entered the arm as
   confidently mislabelled training-free test data. It also costs five genuine-
   looking posthumous Behn novels; that is the price of a rule with no hand in it.

E2 MISCELLANY. Drop a title announcing itself as a miscellany. `Sylvae` and
   `The Annual Miscellany for 1694` are Dryden's volumes but not Dryden's words -
   they collect other hands - and a multi-author volume in a single-author arm is
   a label error by construction.

E3 TRANSLATION. Drop a title announcing itself as a translation. The 2026-09-17
   build excluded a Greene translation on exactly this ground ("a translation,
   not Greene's own composition"); applying the same rule here keeps the two arms
   comparable.

And one SOFT filter, reported as a sensitivity arm rather than applied:

S1 NOT NAMED ON THE TITLE PAGE. Whether the TCP `Title` field names the author is
   a metadata fact, not a judgement, and it separates the attributions that rest
   on a title-page claim from those that rest on later scholarly inference
   (`S'too him, Bayes`, `Scandalum magnatum`, pieces signed `T. D.`). The main
   result is reported on the full filtered arm; the S1-restricted arm is reported
   beside it so a reader can see whether it depends on the weak attributions.
"""
import re

MISC = re.compile(r'miscellan', re.I)
TRANS = re.compile(r"turn'?d (from|in?to)\b|translated|englished|out of the (french|latin|italian|spanish|greek)"
                   r"|paraphras|done into english", re.I)


def death_year(author_string):
    """Death year from a TCP author string, or None.

    Forms seen: 'Behn, Aphra, 1640-1689.', 'Crown, Mr. (John), 1640?-1712.',
    'Ford, John, 1586-ca. 1640.', 'Shadwell, Thomas, 1642?-1692.',
    'Glapthorne, Henry.' (none), 'Brome, Richard, d. 1652?'.
    """
    m = re.search(r'\d{4}\??\s*-\s*(?:ca\.\s*)?(\d{4})', author_string)
    if m:
        return int(m.group(1))
    m = re.search(r'\bd\.\s*(?:ca\.\s*)?(\d{4})', author_string)
    if m:
        return int(m.group(1))
    return None


def year(date_field):
    m = re.search(r'\d{4}', str(date_field))
    return int(m.group(0)) if m else None


def surname(author_string):
    return author_string.split(',')[0].strip().strip('.')


def hard_drop(row, author_string):
    """Return a reason string, or None to keep."""
    d, y = death_year(author_string), year(row['Date'])
    if d and y and y > d:
        return 'E1 posthumous: printed %d, author died %d' % (y, d)
    if MISC.search(row['Title']):
        return 'E2 miscellany: multi-author volume'
    if TRANS.search(row['Title']):
        return 'E3 translation: not the author own composition'
    return None


def named_on_title(row, author_string):
    sn = surname(author_string)
    sn = re.sub(r"[^A-Za-z']", '', sn)
    return bool(re.search(re.escape(sn), row['Title'], re.I))
