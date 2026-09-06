# Primary-image adjudication of the cross-page plaintext signature

**Session:** 2026-09-05, GPT-5.6 Sol  
**Status:** hard primary-source correction to the candidate crib spelling

## Primary evidence

The full-resolution Wikimedia Commons scan `Debosnys-Cryptogram-4b.png` (1105×563) was inspected directly after the shifted-phonetic hypothesis was developed.

At the foot of the sheet, Debosnys writes an unencrypted stylized signature bounded by dots. The best reading from the primary image is:

**`. Hênêcos Debosnostys .`**

Both e's in the first word/name carry circumflex-like marks. The final group in the surname is visually **`tys`**, not `tya`.

Primary image:
`https://upload.wikimedia.org/wikipedia/commons/4/4f/Debosnys-Cryptogram-4b.png`

## Relation to the independent 2015 reading

A Cipher Mysteries commenter in December 2015 independently noticed the same unusual signature and wrote that `Henecos` had accent marks over the e's and that the surname was spaced:

`DE BOS NOS TYA`

That observation remains extremely valuable because it predates Sektu's 2017 decomposed cipher transcription and independently supplies the internal segmentation `DE | BOS | NOS | ...`.

However, for the final letters **the primary scan outranks the commenter's palaeographic reading**. The working normalized plaintext target should therefore be:

`HENECOSDEBOSNOSTYS`

with the 2015 `...TYA` retained only as an alternate historical reading.

## Effect on the shifted-phonetic partial key

None of the high-value internal assignments changes. Re-running the same segmentation with final syllable `TYS` gives:

Syllables:

`HE | NE | COS | DE | BOS | NOS | TYS`

Sektu-style shifted units:

`H | EN | EC | OSD | EB | OSN | OST | YS`

The two surviving atom branches remain identical except that:

`CROSSB = YS`

instead of the older-comment variant `CROSSB = YA`.

Shared candidate assignments are therefore:

- `C2 = H`
- `B2 = EN`
- `X = EC`
- `DOT = OS`
- `N = D`
- `U = EB`
- `CROSSB = YS`

and the unresolved middle branch remains either:

A. `O=O, Z=SN, O2RNO=ST`, or
B. `O=OS, Z=N, O2RNO=T`.

## Consequence

The cross-page crib no longer depends on an Internet spelling for its full target. The actual public primary scan supplies the string **Hênêcos Debosnostys** directly. The 2015 comment is now used only for the independently observed segmentation, not for the final spelling.
