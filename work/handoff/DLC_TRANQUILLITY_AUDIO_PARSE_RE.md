# MP_ESC_Tranquillity_AUDIO_m: why 125 exports fail to parse (RE, 2026-10-23)

**Labels:** C = measured on the cooked file.

**Package:** AssetTools/work/dlc/cooked/MP_ESC_Tranquillity_AUDIO_m.xxx (LZO, 6 chunks).

**One cause, two effects (C):**
- **Chunk 0, block 1** (uncompressed 131,181 … 262,253; header says 131,072 bytes) decodes to **104,644 bytes**.
  - lzallright and an independent pure-python LZO1X decoder (`tools/lzo1x_ref.py`) agree byte for byte.
  - The input is consumed exactly, ending in a valid end-of-stream marker.
  - It's every block in all 6 chunks that's checked; this is the only short one.

**Effect 1, a loader bug that recovers 82 of the 125:**
- `ue3pkg.decompress` advances the write position by `len(dec)` instead of the block's declared uncompressed size.
- So everything after the short block, through the end of chunk 0, is shifted 26,428 bytes early. That's exports 222 … 344
  (SeqEvent_Touch, SeqVar_Object, SeqAct_PlaySound / PlayerPositionalSound, Reverb, SequenceFrame…).
- **Fix:** `w += bus` (place each block at its declared offset), and log when `len(dec) != bus`.
- With that change, TypedReader parses everything except 43 exports.

**Effect 2, damaged shipped data (43 exports, unrecoverable from this file):**
- The short block is valid only up to block offset 57,569 (absolute **188,750**, the end of Model export 208). From there to the
  end of its output it holds no object headers.
- The corruption point is at file offset 46,696, which isn't on a 4 KB STFS block boundary. Every block also matches its SHA-1. So
  the damage is in the cooked package as shipped, not in the extraction.
- The lost range is 188,750 … 262,900: 43 exports, listed in `tranquillity_audio_unrecoverable.json`:

| Class | Count |
|---|---|
| Model (TriggerVolume brushes) | 14 |
| Package | 15 (12-byte group objects) |
| SeqAct_AmbientAudioZone | 6 |
| SeqAct_Delay | 3 |
| SeqAct_Gate | 2 |
| SeqAct_PlayFlybySound | 2 |
| SeqAct_Mixer | 1 |

- H: the original read the same damaged bytes, so these objects were broken or unused in the shipped game as well.

**For Systems:**
- Every SeqEvent_Touch, SeqVar_Object, SeqAct_PlaySound, PlayerPositionalSound and Reverb object parses after the fix.
- Only the 6 AmbientAudioZone, 3 Delay, 2 Gate, 2 FlybySound and 1 Mixer ops are lost.
- Treat those as defaults or skip them.

## Revision 2026-10-24: Static_ART has the same defect, and both point at a 4 KB block (C for the measurements, H for the cause)
- **MP_ESC_Static_ART_m:**
  - Chunk 17, block 3 (uncompressed 18,219,117 … 18,350,189) decodes to **112,855 of 131,072** bytes; the reference decoder agrees.
  - It lies inside the main BSP **Model_7832** (serial 17,972,558, size 1,874,980).
  - Model_7832's surf array: count **1983** at Model+314,428, FBspSurf **56 bytes**.
    - **Surfs 0–315 are valid.**
    - **316 … 1128 fall in the corrupt or missing part** of the short block (Model+332,128 … +377,631).
    - **With block-aligned placement (w += declared size), surfs 1129–1982 and the rest of the Model are correct.**
  - **There's no format change in the package:** no licensee field, no inline array, no second Model. The same 56-byte struct holds
    for the whole array.
- **Where the corruption starts in the compressed stream:**

| File | Starts at offset | 4 KB boundary |
|---|---|---|
| Static_ART | ≈ 5,578,752–5,578,767 | **block 1362 begins at 5,578,752** |
| Tranquillity_AUDIO | ≈ 44,714–46,696 | **block 11 begins at 45,056** |

- **Both corruption points sit on a 4 KB boundary of the extracted file**, i.e. on an STFS data-block boundary.
  - H: **one 4 KB STFS block in each file was taken from the wrong place.** The likely causes are a fragmented file whose hash-entry
    next-block chain wasn't followed, or a level-0 / level-1 hash-table skip error at that block.
  - The LZO stream then desyncs and happens to re-sync to the true end-of-stream marker, which is why it "decodes cleanly" but short.
  - **This revises the earlier "damaged in the shipped cook" conclusion:** the data is probably intact in the STFS container.
- **Check:** re-extract block 11 of Tranquillity_AUDIO and block 1362 of Static_ART (counting from each file's first block) by
  following the STFS hash entries' next-block chain and the level-1 tables, then re-decode. If the short blocks become 131,072
  bytes, the 43 Tranquillity exports and Static's surfs 316–1128 come back.

## Resolved 2026-10-24 (Integration, confirmed)
- **Both bad blocks are STFS data block 28,900 (0x70E4):** Static_ART = first block 27,538 + 1,362; Tranquillity_AUDIO = first block
  28,889 + 11.
- **Cause:** the extractor's backing-block formula used `>` instead of `>=` at the 0xAA / 0x70E4 hash-table boundaries, so that one
  block was read one table early.
- **This is an extraction bug; the shipped data is intact.**
- The affected files are being re-extracted. `tranquillity_audio_unrecoverable.json` and the "damaged in the shipped cook" note
  above are **superseded**; those exports are recoverable after re-extraction.
