# The 3 April 1941 date collision — a preregistered hypothesis

*Opened 2026-09-07. This file is written **before** the evidence that would test it is
available, deliberately. `PRACTICES.md`: "Preregister the falsifier before you take the
leap." Everything here is `[INFERRED]` on top of `[SEARCH]`-grade inputs.*

## The observation

Two things are dated **3 April 1941**:

1. **London GRU No. 649**, the cable carrying BARON's reporting connected with British
   decryption of German Enigma traffic. `[HUB]`/`[SEARCH]`
2. **Churchill's personal warning to Stalin**, sent through Ambassador Cripps: *"I have sure
   information from a trusted agent that when the Germans thought they had got Yugoslavia in
   the net, that is to say, after 20th March, they began to move 3 out of the 5 Panzer
   Divisions from Roumania to Southern Poland."* The intelligence was Enigma-derived; the
   phrase "a trusted agent" was a deliberate cover for the SIGINT source. `[SEARCH]`

This is the only message Churchill sent Stalin directly before Barbarossa. `[SEARCH]`

## Why it is worth writing down

Churchill's entire security design for that message was **to conceal that Britain was
reading Enigma**. He invented a human agent to protect the machine. If, on the same day, the
London GRU residency cabled Moscow material tied to British Enigma decryption, then the
concealment had already failed at the point that mattered — not the product, the
**provenance**.

That reframes what BARON was worth to Moscow. A source who supplies German order-of-battle
is one of many. A source who tells Moscow *that the British warnings are machine
decryption, not a British agent's story* is answering the exact question Stalin's staff were
asking when they discounted the warnings as British provocation. Provenance is the scarce
commodity here, and it implies a much smaller access set than product does.

## Hypothesis H-COLLISION

> London GRU No. 649 concerns the same body of Enigma-derived intelligence that Churchill
> ordered passed to Stalin on 3 April 1941 — reported to Moscow through the GRU residency,
> with the provenance attached that Churchill had stripped off.

## Honest prior — do not skip this section

The observation was found **post hoc**, by noticing a date already in hand. That is exactly
the search-budget error `PRACTICES.md` warns about, so the budget is stated:

- Naive same-day probability, one BARON Enigma cable against one named 1941 event:
  **~1/365 ≈ 0.3%.**
- But the honest denominator is not one event. 1941 contains a **series** of British
  Enigma-derived disclosures toward Moscow — the 3 April Cripps message, the subsequent
  Eden→Maisky messages, the detailed 10 June Maisky cable, and further pre-Barbarossa
  warnings. `[SEARCH]` Call it *k* such events with *k* not yet enumerated; a ±1-day
  tolerance would multiply the window again.
- The match is nevertheless with the **first and most consequential** member of that series,
  and it is exact rather than approximate.

**Conclusion: hypothesis-generating, not evidence.** It earns one cheap test. It does not
earn a candidate list, and this file must not be cited as support for one.

## Preregistered tests — frozen 2026-09-07, before reading either document

These are written so that H-COLLISION can lose. Run them in order.

| Test | Prediction if H-COLLISION is true | Prediction if false | Verdict recorded |
|---|---|---|---|
| **T1 — Subject matter of No. 649** | Content concerns German ground/air movements toward the USSR or the Balkans, especially armoured formations moving out of Romania after ~20 March | Content is unrelated (British forces, cryptanalytic method, some third subject) | *pending* |
| **T2 — Provenance attribution** | The cable attaches the Enigma origin to material Britain was presenting as agent-derived | The Enigma reference is the VENONA translator's editorial note, or a separate topic | *pending* |
| **T3 — Direction of the claim** | BARON is reporting on *British activity* (that Britain reads Enigma) | BARON is reporting *German product* and Enigma is incidental | *pending* |
| **T4 — The July document** | The 29 Jul 1941 report shows the same shape: British-source material with provenance attached | Unrelated shape; the two BARON documents are thematically disconnected | *pending* |
| **T5 — Timing direction** | Any onward Soviet handling shows Moscow knew the provenance **before** Cripps delivered Churchill's message (delivery was delayed well past 3 April) | No such priority establishable | *pending* |

**T1 alone kills or keeps this.** It costs one page of reading.

## If H-COLLISION survives T1–T3

Then the access requirement is **provenance knowledge in London in early April 1941**, and
`provenance-knowledge-constraint.md` becomes the operative candidate frame. Note the sharp
consequence for West's identification: a man in Lucerne is a poor fit for knowing what
Churchill told Eden in London on 3 April.

## If H-COLLISION fails

Then B1 should be re-read as "BARON's material was Enigma-derived and someone downstream
knew it", H3 becomes the leading reading, and the historical stakes of the target drop
considerably — which is itself worth reporting to the board, because BARON's number-one
Dominic ranking rests on the provenance reading being right.
