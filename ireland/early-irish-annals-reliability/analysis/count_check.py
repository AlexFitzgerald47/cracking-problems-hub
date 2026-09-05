"""Completeness check: count solar eclipses over a modern century and compare
with the published total.  This tests the *denominator* of the whole study --
if the lunation walk drops eclipses, or invents them, every hit-rate below is
wrong."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from astro import SkyState, julian_day, calendar_date
from find_eclipses import refine_new_moon, greatest_eclipse, SYNODIC

def count(y0, y1, limit=1.58):
    jd0, jd1 = julian_day(y0,1,1.0), julian_day(y1,1,1.0)
    jd = refine_new_moon(jd0)
    while jd < jd0: jd = refine_new_moon(jd + SYNODIC)
    n_lun = 0; gammas = []
    while jd < jd1:
        n_lun += 1
        t, g, sep = greatest_eclipse(jd)
        if abs(g) < limit: gammas.append((t, g))
        jd = refine_new_moon(jd + SYNODIC)
    return n_lun, gammas

if __name__ == "__main__":
    y0, y1 = int(sys.argv[1]), int(sys.argv[2])
    n_lun, g = count(y0, y1)
    print("lunations %d" % n_lun)
    for lim in (1.5433, 1.55, 1.56, 1.57, 1.58):
        print("  |gamma| < %.4f : %d eclipses" % (lim, sum(1 for _, x in g if abs(x) < lim)))
