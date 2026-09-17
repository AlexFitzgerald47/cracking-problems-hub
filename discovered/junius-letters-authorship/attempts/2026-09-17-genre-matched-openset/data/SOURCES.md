# Source manifest

Every file below was downloaded and its byte size checked in this session
(2026-09-17). `long_s_rate` is the fraction of tokens matching a list of
common words whose eighteenth-century long-s (ſ) has been OCR'd as `f`
(`fhall`, `thefe`, `becaufe` ...). It is a direct, cheap measure of how
badly a scan is damaged, and it splits this corpus in two: nineteenth- and
twentieth-century reprints sit near 0.0001, while texts scanned from
eighteenth-century printings sit near 0.02 — a two-hundred-fold difference
in token corruption that is perfectly confounded with printing era.

archive.org items: `https://archive.org/download/<id>/<id>_djvu.txt`
gutenberg_<n>: `https://www.gutenberg.org/cache/epub/<n>/pg<n>.txt`
wikisource_text/: rendered from `en.wikisource.org` *Letters of Junius*
(Woodfall 1772), one file per letter — see `src/fetch_wikisource_text.py`.

| identifier | bytes | long_s_rate |
|---|---:|---:|
| `administrationb01wargoog` | 399,344 | 0.01693 |
| `bim_eighteenth-century_english-liberty-being-a_wilkes-john_1769_1` | 489,782 | 0.00037 |
| `correspondencer01burkgoog` | 1,069,524 | 0.00013 |
| `cu31924088010958` | 1,751,459 | 5e-05 |
| `cu31924088024439` | 1,187,894 | 3e-05 |
| `cu31924088024447` | 1,457,406 | 6e-05 |
| `francisletters01franiala` | 594,769 | 1e-05 |
| `francisletters01franuoft` | 591,771 | 1e-05 |
| `francisletters02franuoft` | 637,653 | 1e-05 |
| `gutenberg_11397` | 954,420 | 0.00034 |
| `gutenberg_15043` | 937,555 | 1e-05 |
| `gutenberg_15198` | 979,272 | 5e-05 |
| `gutenberg_2173` | 297,329 | 0.0001 |
| `gutenberg_36120` | 234,513 | 0.00016 |
| `gutenberg_43656` | 1,071,095 | 0.00023 |
| `juniusincluding07junigoog` | 1,747,453 | 4e-05 |
| `juniusincludingl0001vari` | 879,302 | 4e-05 |
| `juniusincludingl01` | 1,341,702 | 4e-05 |
| `juniusincludingl02` | 1,380,840 | 6e-05 |
| `juniusincludingl02juniiala` | 1,757,377 | 6e-05 |
| `lettersdavidhum00humegoog` | 1,218,430 | 0.00011 |
| `letterslaterevm00stergoog` | 329,689 | 0.013 |
| `lettersofhoracew03walp` | 865,682 | 6e-05 |
| `lettersofjamesbo00boswuoft` | 781,912 | 0.0002 |
| `lettersofthomasg00gray` | 684,470 | 5e-05 |
| `letterssamueljo00johngoog` | 1,121,050 | 7e-05 |
| `letterstohisson01chesiala` | 1,078,111 | 1e-05 |
| `letterswilliamc00cowpgoog` | 606,237 | 9e-05 |
| `memoirsofsirphil01parkuoft` | 1,183,328 | 3e-05 |
| `miscellaneouswor01boydiala` | 794,607 | 0.01925 |
| `observationsonna00pric` | 211,694 | 0.01676 |
| `privatelettersof02gibb` | 1,215,310 | 7e-05 |
| `twospeechesinhou00franiala` | 155,867 | 0.02026 |
