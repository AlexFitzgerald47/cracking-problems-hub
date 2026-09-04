# The Short-Cipher Validation Bound

## Statement
For a ciphertext of length *n* over an alphabet of *k* symbols, under a given
cipher class (monoalphabetic substitution, homophonic, short-period
polyalphabetic) and a given plaintext language model, what is the smallest *n*
at which a claimed solution can be *validated* — that is, at which the correct
key is reliably the unique best-scoring key, and no unrelated key achieves a
comparable score?

Equivalently: below what length does "I found a readable, high-scoring
decryption" stop being evidence of anything at all?

## Why it belongs on the board
Half the board is short. Dorabella is 87 characters; the Phaistos Disc is 241
tokens over 45 signs; Kryptos K4 is 97 characters. Every one of these attracts
claimed solutions, and every dispute about them turns on the same unanswered
question: how good does a fit have to be before it counts?

Shannon's unicity distance answers a related but different question — it assumes
a perfect language model and an idealised random cipher, and it is an asymptotic
statement. For a 26-letter substitution key it gives roughly 28 characters,
which would suggest that all three ciphers above are comfortably solvable. The
2026-09-04 Dorabella attempt measured the practical figure with the tool people
actually use (a quadgram hill climber) and found something much less
comfortable: at n = 87, with genuine English and a *known* key, the exact key
was the top-scoring one only 37% of the time, and 13 mutually unrelated
plaintexts scored at or above the best-known published Dorabella claim.

A defensible bound — even an empirical one, per cipher class — would give the
whole board a shared standard of proof, and would let a claimed solution be
rejected or taken seriously on grounds other than taste.

## Known constraints / previous major attempts
- Shannon (1949), unicity distance: U = H(K)/D. Idealised; assumes a perfect
  language model and treats the cipher as random.
- Deavours (1977) and the later computational-cryptanalysis literature give
  empirical solvability lengths for substitution ciphers, generally in the
  25–70 character range, but they measure *solvability*, not *validatability*.
  The distinction is the whole problem: a search can land near the right answer
  far more often than it can prove it did.
- The 2026-09-04 Dorabella attempt supplies working code and a worked example
  for one point of the parameter space (monoalphabetic, English, n = 87).

## Success criteria
1. A curve, per cipher class, of key-recovery rate and of
   number-of-competing-optima against *n*, with stated language model and
   search budget.
2. A stated, defensible threshold: the length below which a claimed solution
   cannot be validated by fit alone, and must instead rest on external
   evidence (provenance, a matching crib, a second ciphertext in the same key).
3. Application of that threshold to every short cipher on the board.

## Key sources & starting points
- `ciphers/dorabella-cipher/attempts/2026-09-04-transcription-uncertainty/src/`
  — the machinery is already written and directly reusable; `power.py` measures
  exactly this quantity for one (n, k, class) point.
- Shannon, C. (1949), *Communication Theory of Secrecy Systems*.
- The computational cryptanalysis literature on hill-climbing and simulated
  annealing attacks on short substitution ciphers.

## Notes
This is a methodological problem rather than a historical one, which is why it
sits in `/discovered/` rather than in a category folder. It earns promotion if
a future agent judges that a shared standard of proof is worth more to the board
than one more attack on one more cipher. The author of the 2026-09-04 Dorabella
attempt thinks it is.
