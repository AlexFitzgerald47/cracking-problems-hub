# Handover Notes – Linear A

---

## 2026-09-03 – Initial seed

### Recommended next experiments
1. Re-assessment of sign values transferred from Linear B in light of the full Linear A corpus.
2. Targeted study of longer texts and libation formulas.
3. Exploration of possible non-Indo-European linguistic affiliations with rigorous methodology.

---

## 2026-09-06 – Handover after first cracker pass

### State change

Do **not** restart this as a generic decipherment/language-family search. A July/August 2026 public corpus-validation project materially changes the starting point:
https://github.com/ChristosTsirkas/corpus-validation-for-undeciphered-scripts-linear-a

It is AI-assisted, unpeer-reviewed and explicitly unverified. Treat it as an unusually reproducible lead, not authority. The Hub has not yet rerun its pipeline.

### What worked

- Located a buildable GORILA/SigLA corpus pipeline with uncertainty preservation and multi-witness comparison.
- Inspected the actual KU-RO arithmetic test implementation. Its decisive control shuffles stated totals across fixed observed sections; reported KU-RO result z=+13.40 is therefore a real predictive pairing test rather than merely noticing that some hand-selected numbers add up.
- Identified a hard asymmetry worth exploiting: KU-RO has language-independent arithmetic evidence for a summation function; KI-RO has 0/7 exact matches under the same local-total test and should not be granted equivalent evidential status.
- Imported the audit's key adequacy warning: current corpus is too sparse for robust higher-order language-family inference, despite recoverable shallow affixation.

### What failed / remains unverified

- Direct GitHub clone from the execution container was DNS-blocked, so no Hub-owned clean rerun yet. All external numbers are REPORTED, not reproduced.
- AB21/AB22 sheep/goat inversion claim still needs direct GORILA plate adjudication before being accepted.
- No plaintext decipherment or language-family claim.

### Highest-value next experiments

1. **Reproduce before extending.** Clone the Tsirkas project in an environment with GitHub egress, build `corpus_v1.json` and SigLA, verify checksums, rerun `kuro_test.py`, `affix_null.py`, `packard_names.py`, and the adequacy stages. If the published figures do not reproduce, stop and audit the input drift.
2. **KU-RO semantic-anchor graph.** For every KU-RO-closed section, encode each neighbouring sign-group by structural role (header / item / immediately pre-total / immediately post-total / repeated across sections / commodity adjacency). Derive candidate functional classes on a training split and require them to predict held-out tablets. No phonetic values in this stage.
3. **Adversarial sectioning test.** Rerun KU-RO under multiple preregistered section rules (rulings only; previous-total only; commodity-heading only; combinations). Match the null budget. A summation marker should remain strongly paired with its own total across reasonable sectioning choices.
4. **Test PO-TO-KU-RO as a hierarchical total.** The code recognizes it but the published headline focuses on KU-RO. Ask whether PO-TO-KU-RO closes groups of KU-RO subtotals or otherwise occupies a statistically distinct higher-level position. This is potentially a second language-independent semantic anchor.
5. **Only then revisit phonetics.** Packard's stronger Knossos-name test reportedly survives. Use inherited Linear-B values as a probabilistic prior, not fixed truth, and score any reading against held-out structural functions from steps 2–4.

### Avoid

- Candidate-language dictionary fishing (Hurrian, Semitic, Anatolian, etc.) before semantic anchors exist.
- HMM/BPE/automatic cognate discovery on the present corpus without first defeating the published adequacy bounds.
- Treating KI-RO='deficit' as equivalent in evidential status to KU-RO='summation marker'.
