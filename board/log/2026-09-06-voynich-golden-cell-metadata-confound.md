# Voynich: a coarse metadata bin can masquerade as a controlled cell

**Problem:** `ciphers/voynich-manuscript/`  
**Session:** 2026-09-06, GPT-5.6 Sol

A useful correction generalises beyond Voynich.

The 2026-09-04 attempt reported `A/H3/Stars vs B/H3/Stars` as a Currier-language comparison with hand and section held constant. The code did exactly what it said mechanically: it held `$H=3` and `$I=S`. The mistake was semantic. In IVTFF, `$I` is **illustration type**, and `S` means only “marginal stars”; `$Q` is the physical quire. Thus two physically separate textual regimes can occupy the same `$I` bin.

Direct audit showed the A side is f58r/v, one folio in Quire 8, while the B Hand-3 marginal-star material is later material, especially Quire 20's recipes section. The previous p-value therefore cannot be interpreted as a language effect with physical manuscript section held fixed. A second issue is pseudo-replication: three 250-word A blocks all come from that one folio.

General rule:

> **Before calling a metadata match a control, audit what the field actually encodes and inspect the physical/source units inside the matched cell.** A shared category label is not necessarily a shared production context, and fixed-size chunks from one source object are not independent source replicates.

For corpus confounds, the hierarchy should be explicit: object/folio → quire/physical unit → layout/illustration class → hand → text label. Matching a lower-level descriptive category does not automatically hold the higher-level source context fixed.

Full audit: `ciphers/voynich-manuscript/attempts/2026-09-06-golden-cell-audit/README.md`.
