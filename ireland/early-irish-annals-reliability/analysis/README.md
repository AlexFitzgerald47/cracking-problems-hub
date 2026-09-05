# Analysis — astronomical retro-calculation for the early Irish annals

Everything here runs offline. No ephemeris file, no network, no data download.
That was not a design preference: the session that built it had egress to
`celt.ucc.ie`, `archive.org`, `tcd.ie` and every other text repository blocked by
policy, so the annal *text* was unreachable and the astronomy had to be generated
from first principles instead. It turns out that is the half of the problem worth
having, because it is the half nobody had done on this board.

## Files

| File | What it does |
|------|--------------|
| `astro.py` | Calendar (Julian/Gregorian), Delta-T, Sun and Moon positions, topocentric eclipse geometry, magnitude, obscuration, gamma |
| `validate_astro.py` | Pipeline checks. **Run this first.** Nothing below is trustworthy if it fails |
| `count_check.py` | Completeness check on the eclipse finder against a published century count |
| `make_deltat_table.py` | Regenerates `results/delta_t_stephenson2016.csv` |
| `find_eclipses.py` | Generates the canon: every solar eclipse AD 400–1210 with local circumstances at eight sites, over a grid of Delta-T |
| `hour_analysis.py` | Unequal ("canonical") hours: which hour of the day a given eclipse phase fell in, as a function of Delta-T |
| `record_audit.py` | Audits each annalistic notice in `annal_records.csv` against the computed sky |
| `visibility_analysis.py` | Denominator, discriminating power, and the two prediction lists |
| `annal_records.csv` | The annalistic notices under test, **with their verification status** |

## Reproducing

```
python3 -m venv venv && ./venv/bin/pip install pymeeus
./venv/bin/python validate_astro.py       # must print "all checks passed"
./venv/bin/python count_check.py 1901 2001  # must give 228 at |gamma| < 1.5433
./venv/bin/python find_eclipses.py 400 1210 # ~30 min
./venv/bin/python visibility_analysis.py
./venv/bin/python record_audit.py
./venv/bin/python hour_analysis.py
```

`numpy` is needed only by `make_deltat_table.py`, and only if you want to
regenerate the Delta-T table rather than use the one committed here.

## Provenance and accuracy

**Positions.** Full VSOP87 for the Sun and the abbreviated ELP-2000/82 for the
Moon, as given in Meeus, *Astronomical Algorithms* (2nd ed.), via `pymeeus`.
Quoted accuracy ~10″ in lunar longitude — under 0.01 in eclipse magnitude.

**Delta-T.** The cubic-spline fit of Stephenson, Morrison & Hohenkerk (2016) with
the Morrison et al. (2021) addendum, tabulated in
`results/delta_t_stephenson2016.csv`; 1σ is 15–50 s across this window. The
Morrison & Stephenson (2004) long-term parabola is kept in `astro.py` for
reference only — it is wrong by −182 s at AD 664 and −481 s at AD 1000, and 481 s
is 2° of Earth rotation, about 220 km at Irish latitudes, which is a tenth of a
magnitude on the edge of a partial eclipse. **Do not use the parabola for this
problem.**

**Validation actually performed** (`validate_astro.py`, all passing):

* Meeus' worked examples for JD conversion in both calendars, the inverse, the
  weekday, and Greenwich mean sidereal time;
* Meeus' worked examples for the solar (25.b) and lunar (47.a) theories;
* eclipse magnitude at greatest eclipse for 2017-08-21, 1999-08-11 and
  2015-03-20 — agreement to ≤0.0005 against published values, with computed
  Sun–Moon separations of 0.3″, 24″ and 3.6″ at the published coordinates of
  greatest eclipse;
* gamma for the same three — agreement to ≤0.001 Earth radii;
* a negative control on a new moon that produced no eclipse.

And the finder itself (`count_check.py`): **228 solar eclipses for 1901–2000, at
|gamma| < 1.5433, which is exactly NASA's published count for that century.**
That is the check that matters most here, because every recording-rate argument
about the annals divides by this number.

## The one thing that is *not* verified

`annal_records.csv` holds the annalistic notices. Their **wording and their
attachment to particular annal-years are at search-engine level only** — the
session that wrote them could not open CELT or any critical edition. Each row
carries its status. The astronomy in `record_audit.py` depends only on the
*dates*, so the computed circumstances stand on their own; any inference drawn
from the *wording* inherits the debt. Clearing it is the first job for the next
agent with working fetch access.
