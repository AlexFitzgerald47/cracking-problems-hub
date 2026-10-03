"""The fast path must reproduce the audited pure-python fold exactly, on real data."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import mixed_lines_of
from crossfit import run_fold
from fastfold import Design, run_fold_fast

lines = mixed_lines_of(Path(sys.argv[1]))
d = Design(lines)
ok = True
for b in range(5):
    slow = sorted(c["pair"] for c in run_fold(lines, b)["confirmed"])
    fast = sorted(run_fold_fast(d, d.N, b))
    same = slow == fast
    ok &= same
    print(f"fold test_bucket={b}: slow={len(slow)} fast={len(fast)} "
          f"{'MATCH' if same else 'MISMATCH ' + str(set(slow) ^ set(fast))}")
assert ok, "fast path does not reproduce the audited path"
print("VERIFIED: fast path reproduces the audited 5-fold result exactly")
