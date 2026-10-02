# MILESTONE 03 — Rendering native: character shadow-mask write path, DLAC, bias/PCF, enable gates

Pass date: 2026-10-02. Scope: the four blockers listed by Rendering checkpoint `agents/rendering 3232bbb`.

Sources:
- Read-only Ghidra snapshot via `tools/wfcq.ps1`. The new `rawdis` command decodes one instruction at a time, in memory only. It is needed because Ghidra wrongly treats `0x830101E0` as no-return and truncates every caller.
- Shipped config `ExtractedAssets/config/Coalesced_ini/TransGame/Config/Xenon/Cooked/Xe-TransEngine.ini`, read-only.
- AssetTools `authored.db`, read-only.

Enum decoding uses UE3 RHI order:
- **EBlendFactor:** Zero 0, One 1, SrcColor 2, InvSrcColor 3, SrcAlpha 4, InvSrcAlpha 5, DestAlpha 6, InvDestAlpha 7, DestColor 8, InvDestColor 9.
- **ECompareFunction:** Less 0, LessEqual 1, Greater 2, GreaterEqual 3, Equal 4, NotEqual 5, Never 6, Always 7.
- **EStencilOp:** Keep 0, Zero 1, Replace 2, SatInc 3, SatDec 4, Invert 5, Inc 6, Dec 7.
- **EPixelFormat:** A8R8G8B8 = 2.

GEngine field offsets: `GEngine = *0x8382DCD4`. The `Engine` class layout was computed from its declared properties with object base +0x2C. It is validated by `GEngine+0x34C = Client`, which matches that field's earlier use. Results:
- `+0x190` = MaskedShadowsDepthBias
- `+0x3E0` = ShadowFilterRadius
- `+0x3E4` = DepthBias
- `+0x230` = bool group; the halfword test `&1` at +0x230 = dword bit 0x10000 = **bEnableBranchingPCFShadows** (verified)

---

## 1. COMPOSITE SHADOW → SHADOW-MASK WRITE PATH

**CONFIDENCE:** CONFIRMED for the target, format, clear, blend, stencil, combine rule, resolve and blur. PARTIAL for how the light-environment record's `shadowFactor` reaches the projection shader (§1.6).

### ADDRESSES
| address | proposed name | role |
|---|---|---|
| 0x83037390 | `FSceneRenderTargets::InitDynamicRHI` | allocates ShadowMask = target **0x11**, format **2 (A8R8G8B8)**, size (SceneRT+0x24, +0x28) = the downsampled buffer size; aliased in EDRAM with target 0 |
| 0x83010218 | `FSceneRenderTargets::BeginRenderingShadowMask(bClear)` | binds ShadowMask surface (SceneRT+0x2D4) with SceneDepth (+0x2F8); if bClear → `RHIClear(color = *0x8370AE88 = (1,1,1,1))` |
| 0x830102B8 | `FSceneRenderTargets::FinishRenderingShadowMask` | resolve ShadowMask surface → texture (SceneRT+0x2D0 = `0x83862680`) |
| 0x82DEC190 | `FSceneRenderer::RenderShadowMask(DPG, bNoBlur)` | begin + clear, then each light with shadows → `RenderLightShadowProjections`; resolve; then blur if anything was drawn |
| 0x8304F628 | `RenderLightShadowProjections(light, DPG, bTranslucentPass)` | collects visible projected shadows of the light, renders their depths, then projects them |
| 0x8304EBE8 | `FProjectedShadowInfo::RenderDepth` | shadow-depth pass, per shadow |
| 0x8304EF70 | `FProjectedShadowInfo::RenderProjection(view, DPG)` | stencil mark, then multiplicative projection into ShadowMask |
| 0x82DDB070 | `BlurShadowMask(W, H)` | 2-pass separable blur (horizontal, then vertical), each pass re-begins the mask (no clear), draws a full-screen quad, and resolves |
| 0x82CF8048 | projection blend-state InitRHI | `BO_Add, Src = DestColor, Dst = Zero; alpha Src = Zero, Dst = One; alpha test Always` |
| 0x82DDAEF0 | lighting-pass ShadowMask binder | binds `0x83862680` as `ShadowMaskTexture`, with `ShadowMaskTexelOffset = (0.5/W, 0.5/H)` |

### PSEUDOCODE
```
RenderShadowMask(DPG, bNoBlur):                                  // 0x82DEC190
  BeginRenderingShadowMask(clear = true)                          // ShadowMask := (1,1,1,1)
  anyDrawn = false
  for light in Scene.Lights (+0x1CF0):
     if light has projected shadows visible in any view for this DPG:
        anyDrawn |= RenderLightShadowProjections(light, DPG)
  FinishRenderingShadowMask()                                     // resolve
  if anyDrawn and !bNoBlur: BlurShadowMask(SceneRT.W(+0x24), SceneRT.H(+0x28))   // two passes, H then V

RenderLightShadowProjections(light, DPG):                         // 0x8304F628
  shadows = [s in Renderer.ProjectedShadows (+0x5C) where s.Light (+0x360) == light
             and s visible in some view and (light flags (+0x364 → vt+0x1C) has the DPG bit:
                 bit5 = DPG0, bit6 = DPG1, bit7 = DPG2, bit8 = DPG3)]
  (translucent pre-pass: drop shadows whose subject opacity < 1 and that lack flag 0x40000000)
  for s in shadows: s.RenderDepth()                               // into ShadowDepth target
  resolve the shadow depth
  BeginRenderingShadowMask(clear = false)
  for view in views:
     set viewport = view rect / SceneRT downsample factor (+0x2C)  // mask is downsampled
     for s in shadows: s.RenderProjection(view, DPG)
     RHIClear(stencil = 0)

RenderProjection(view, DPG):                                      // 0x8304EF70
  require (light flags & 4) and the DPG bit
  verts = 8 frustum corners of the shadow
  colour writes OFF
  if !(s.flags (+0x37C) & 0x20000000):                             // ordinary shadow: z-fail volume of the frustum
     stencil = {front: Always, zfail = Inc; back: Always, zfail = Dec; two-sided; mask 0xFF}
     draw frustum box (8 verts, 12 tris, index table 0x82308518)
  else:                                                            // receiver-only shadow
     stencil = {Always, pass = Replace, ref 1}; draw the receiver primitives (s+0x38C list)
  colour writes ON; depth state per view flag (view+0x478)
  stencil = {NotEqual 0, keep}
  blend   = dest.rgb = dest.rgb * src.rgb ; dest.a unchanged          // 0x82CF8048
  pixel shader = light->GetProjectionShader (vt+0x48), or the BranchingPCF variant (vt+0x4C) when
                 UseBranchingPCF(light.ShadowFilterQuality byte @ +0xFC)    // 0x8300A830, see §3
  shader.SetParameters(view, s); draw frustum box
  stencil reset
```

### ORIGINAL WFC BEHAVIOR
- **Render target:**
  - `ShadowMask`, A8R8G8B8, at the scene's downsampled buffer size (SceneRT+0x24 × +0x28).
  - Projections use a viewport divided by the downsample factor (SceneRT+0x2C).
  - The lighting pass samples it with a half-texel offset.
- **Clear / initial value:** (1, 1, 1, 1), once per mask build.
- **Encoding:** **visibility** (1 = fully lit), not occlusion.
- **Blend:** **multiplicative.** `mask.rgb ← mask.rgb · projectionOutput.rgb`; alpha untouched.
- **Masking:** writes happen only inside the stencil-marked shadow frustum (or on receivers). Outside it the mask stays 1.
- **Multiple shadows:** every projected shadow of every light in the depth-priority group goes into **the same** mask, combined as a **product**. They accumulate rather than replace.
- **Clamp:** none beyond the 8-bit UNORM storage, so values are implicitly in [0, 1].
- **Blur:** after all projections, if anything was drawn, two separable blur passes run (horizontal, then vertical; full-screen quads with texel-step constants derived from 0.5/size). The kernel is in `BlurShadowMaskPixelShader` (not decoded here).
- **What the lighting shader sees:** the shader-side `mask` = the resolved, blurred **product of all projected shadow visibilities** at that screen texel. So `S = (1 − mask)(1 − DSLS)` (§4 of the previous note) applies the combined shadowing.

### 1.6 Composite-shadow → projection link (PARTIAL)
- The DirectLightEnv proxy (`0x82CCE0A8`) appends one 0x80-byte record per composite-shadow light (`0x82DBF2C8` → `0x82DBF200`):
  - `+0x00` light type (1 directional/other, 2 point, 3 spot);
  - `+0x10..+0x4C` the light's LightToWorld matrix (light +0x90);
  - `+0x50` the **shadowFactor** float4;
  - `+0x60..+0x6C` radius / falloff / cone values;
  - `+0x70`, `+0x74` two more words.
- The modulated projection SetParameters (`0x82D077F8`, BranchingPCF *Mod* variants) uploads:

```
ShadowModulateColor.rgb = lerp((1,1,1), LightSceneInfo(+0x360).ModShadowColor(+0x110..+0x118), ShadowInfo.FadeAlpha(+0x378))
```

- That output would then be multiplied into the mask by the blend above. This path is consistent with `shadowFactor = lerp(1, ShadowLuminanceScale(=0), strength)` being the per-light modulate colour.
- **Not proven:** the render-thread code that turns the record into the projected shadow's light. The shadow-creation function was not traced.

### RENDERING HANDOFF
1. Allocate ShadowMask as RGBA8 at the downsampled scene size.
2. Clear it to (1, 1, 1, 1).
3. For each projected shadow: mark stencil with a z-fail frustum volume, then draw the frustum with stencil ≠ 0 and blend **DestColor × Src** (alpha untouched).
4. Multiply all shadows together, then run the 2-pass blur.
5. Sample `.r` with the 0.5-texel offset in the lighting pass.

---

## 2. DIRECTLIGHTAMBIENTCONTRIBUTION CPU FORMULA

**CONFIDENCE:** CONFIRMED for the arithmetic, inputs and upload. HIGH for the final copy of +0x1B0 into the render-side +0x1D0 (the 0x20-byte header offset was not traced byte by byte).

### ADDRESSES
| address | role |
|---|---|
| 0x82CCE0A8 | `FDirectLightEnv::BuildSceneProxyData`: computes DLAC |
| 0x82CED7F8 | adds two 6-face ambient-cube SH sets (24 floats) |
| 0x82CED980 | `CubeSum`: per channel, the sum of the 6 cube faces → float4 |
| 0x82DCA670 | proxy init: stores DLAC at proxy +0x1B0 |
| 0x82E54618 | binds the `WorldLightPositionAndInvRadius`, `LightColorsAndFalloffExponents`, `WorldSpotLightDirections`, `SpotLightAngles`, `DirectLightAmbientContribution` group |
| 0x82E2EDA8 | upload: `SetPixelShaderValue(DirectLightAmbientContribution, renderData+0x1D0, ≤16 bytes)` |

### PSEUDOCODE
```
A = env.AmbientSH      (+0xA8, 6 RGBA faces)   = sky upper/lower + Beast light-probe SH (averaged over the highest-priority volumes)
L = env.LightsSH       (+0x108, 6 RGBA faces)  = direct lights folded into SH:
                                                  lights ranked beyond TotalLightCount (overflow)
                                                  + (1 − f) of the last kept light (boundary crossfade)
T = A + L
DLAC = ( CubeSum(L).r / (CubeSum(T).r + 0.001),
         CubeSum(L).g / (CubeSum(T).g + 0.001),
         CubeSum(L).b / (CubeSum(T).b + 0.001), 0 )
```

### ORIGINAL WFC BEHAVIOR
- **Meaning:** DLAC is the **fraction of the ambient term that came from direct lights folded into SH**.
- **Shader use:** only that fraction is darkened by the shadow mask: `ambient · (1 − DLAC·S)`.
- **Scope:** per light environment, i.e. per character form (robot and vehicle each have one). It is recomputed on every light-environment update (full or incremental).
- **Interpolation:** no smoothing of its own. It follows the smoothed light visibilities that feed L.
- **Clamps:** none explicit. Mathematically it lies in [0, 1); the +0.001 avoids division by zero.
- **Light type and character state:** only indirectly, through which lights spill into SH (TotalLightCount = 2 for both Optimus forms) and their intensities.
- `IndirectIlluminationOnly = 1` makes L = 0, hence DLAC = 0.
- **Authored value:** none, so there is no shipped constant. The Optimus value in Streets is runtime-derived from the gathered lights.

### RENDERING HANDOFF
Compute DLAC exactly as above from the same two SH sets used to build `AmbientCubeIrradiance`, and upload it as a float4 with w = 0.

---

## 3. SHADOW BIAS / PCF

**CONFIDENCE:** CONFIRMED for the CPU formulas, tables and shipped values. PARTIAL for how the parabolic bias term is used inside the compiled projection shader (not decoded).

### ADDRESSES
| address | role |
|---|---|
| 0x82CF1A00 | BranchingPCF projection PS constructor (vtable 0x822C6EBC). Binds `ScreenToShadowMatrix`, `InvRandomAngleTextureSize`, `ShadowDepthTexture`, `RandomAngleTexture`, `RefiningSampleOffsets`, `EdgeSampleOffsets`, `ShadowBufferSize`, `ShadowDepthBias`, and copies the static tables |
| 0x82CFB598 | its `SetParameters` (0x88C bytes; read with `rawdis`) |
| 0x830101E0 | `GetShadowDepthResolution()` = clamp(SystemSettings.MaxShadowResolution (`0x83857058`), 1, `0x83712314` = **2048**) |
| 0x83711DFC | **EdgeSampleOffsets** table: 4 × float2 |
| 0x83711EC0 | **RefiningSampleOffsets** table: 12 × float2 |
| 0x8300A830 | `UseBranchingPCF(light.ShadowFilterQuality)` |
| 0x830439E0 | non-branching `TShadowProjectionPixelShader<F4/F16 Sample Hw/Manual/Fetch4 PCF>` selector (quality + `ShadowFilterQualityBias`; Fetch4/HW from the HW-PCF flag). It has no static callers. |

### CONSTANTS (shipped Xe-TransEngine.ini)
- ShadowFilterRadius = **6**
- DepthBias = **0**
- MaskedShadowsDepthBias = **0.2**
- MinShadowResolution = 128, MaxShadowResolution = **1024**
- ShadowFilterQuality = 0, ShadowFilterQualityBias = 0
- bEnableBranchingPCFShadows = **True**
- ModShadowFadeDistanceExponent = 0.2
- ShadowTexelsPerPixel = 1.0

```
EdgeSampleOffsets     (4):  (-0.09673, 0.99531) (0.26020,-0.96556) (0.90176, 0.43224) (-0.97680,-0.21415)
RefiningSampleOffsets (12): (0.83831,-0.53516) (0.25047,-0.22063) (0.38774,-0.54880) (-0.51237, 0.57005)
                            (-0.90728, 0.11358) (-0.73834,-0.50544) (0.08519, 0.30562) (-0.29311,-0.01680)
                            (0.02770, 0.70874) (0.05331,-0.59401) (0.34538,-0.90947) (-0.58627,-0.22920)
```

### PSEUDOCODE (`0x82CFB598`)
```
Res      = clamp(MaxShadowResolution, 1, 2048)                    // 1024 shipped
texel    = 1 / Res                                               // fdivs f30 @0x82CFB708
k        = GEngine.ShadowFilterRadius * texel                     // 6/1024
EdgeSampleOffsets[i]     = EdgeTable[i]     * k   (i = 0..3, packed two per float4)
RefiningSampleOffsets[i] = RefiningTable[i] * k   (i = 0..11)
ShadowBufferSize         = (Res, Res, 0, 0)
InvRandomAngleTextureSize = (1/RandomAngleTexture.W, 1/RandomAngleTexture.H)
ShadowDepthBias          = (Res * GEngine.MaskedShadowsDepthBias / GEngine.ShadowFilterRadius)^2
                         = (1024 * 0.2 / 6)^2 = 1165.0 (shipped)        // "ShadowBiasTechnique_Parabolic"
ScreenToShadowMatrix     = screen → shadow-map UV/depth (built with a +0.5 offset; VMX math, not decoded)
```

### ORIGINAL WFC BEHAVIOR
- **Shader family:** projected character shadows use the **BranchingPCF** family:
  - 4 edge taps first; then 12 refining taps where the edge taps disagree;
  - per-pixel rotation from `RandomAngleTexture` (Global `BranchingPCFProjectionPixelShader` / `...ModProjection...`);
  - bias technique **Parabolic** (a NormalOffset variant also exists).
- **Filter radius:** `ShadowFilterRadius / Res` in shadow-UV space, i.e. 6 texels.
- **No slope-scaled or receiver bias** appears on the CPU side of this path. `DepthBias = 0` is not referenced here. The only bias constant is the parabolic `ShadowDepthBias` above.
- **Same constants everywhere:** directional, spot, robot, vehicle and composite shadows. Nothing in this code branches on light type or subject.
- The PCF quality index passed to the light's BranchingPCF shader factory is `1 + ((light flags @+0x30 & 0x08000000) != 0)`.

### RENDERING HANDOFF
Use the tables, `k = 6/Res`, `Res = 1024`, and `ShadowDepthBias = (Res·0.2/6)²` with the parabolic shader. Verify the bias semantics in the projection shader microcode (`tools/xenosdis.py` on the global shader blobs).

---

## 4. NORMAL-PLAY ENABLE CONDITIONS

**CONFIDENCE:** CONFIRMED for the gates listed; PARTIAL for the shadow-creation gate, which was not traced.

**CONFIRMED gates** (this pass and the earlier ones):
- **Light-environment composite selection** (earlier note):
  - the light is `bEnabled` and `bCastCompositeShadow`;
  - it passes the channel / level / volume filter;
  - it is the single brightest by unoccluded luminance at the bounds origin;
  - its strength factor is ≥ 0.05 away from neutral (otherwise dropped).
  - Both baked and unbaked lights qualify, because composite ranking ignores visibility.
  - The DefaultShadowLight fallback is never used for WFC pawns.
- **Projection draw gate** (`0x8304EF70`): the light's render flags (`+0x364 → +8 → vt+0x1C`) must have **bit 2 (0x4)** set, plus the current DPG bit (bits 5..8).
  - In the translucent pre-pass, shadows with subject opacity < 1 lacking flag 0x40000000 are dropped.
- **Global:** the shadow mask is built only when at least one shadow is drawn. Otherwise it stays (1, 1, 1, 1) and the blur is skipped.
- **Robot vs vehicle:** identical code path. They differ only in their light-environment sample counts.

**NOT recovered:** the render-thread creation of `FProjectedShadowInfo` for the composite light, including any distance/resolution cut (ShadowTexelsPerPixel, Min/MaxShadowResolution, CastDynamicShadows / bCastDynamicShadow requirements).

### RENDERING HANDOFF
Do not add further gates beyond the confirmed ones until shadow creation is traced.

---

## SHADOW MASK WRITE HANDOFF
- RGBA8 mask at the downsampled scene size, cleared to 1 (visibility).
- Per shadow: z-fail stencil frustum, then a `DestColor × Src` multiplicative projection inside the stencil.
- All shadows multiply into the same mask, followed by a 2-pass separable blur.
- The lighting pass reads `.r` with a half-texel offset as `mask`.

## DLAC HANDOFF
`DLAC.rgb = CubeSum(LightsSH) / (CubeSum(AmbientSH + LightsSH) + 0.001)`, w = 0. It is runtime-derived per light environment with no authored value, and uploaded from render data +0x1D0.

## SHADOW BIAS HANDOFF
`ShadowDepthBias = (Res · MaskedShadowsDepthBias / ShadowFilterRadius)²` = (1024·0.2/6)² ≈ 1165 (parabolic technique). There is no slope-scaled or receiver bias on the CPU side. The engine DepthBias (0) is unused here.

## PCF HANDOFF
- BranchingPCF: 4 edge taps, then 12 refining taps; offsets = table × (6/Res).
- Per-pixel rotation from RandomAngleTexture.
- Res = clamp(MaxShadowResolution 1024, 1, 2048).
- The same for every light type and for robot and vehicle.

## SHADOW ENABLE HANDOFF
- Composite selection rules as previously reported, plus the light render-flag bit 0x4 and the DPG bit at projection time.
- Baked lights can be the composite-shadow light.
- Robot and vehicle use identical conditions.

## STILL UNKNOWN
- The render-thread conversion of the light-environment composite record (`shadowFactor`, matrix) into the projected shadow / light scene info (§1.6), and the full shadow-creation gating.
- The BlurShadowMask kernel weights and the projection-shader microcode use of `ShadowDepthBias`/offsets. These need decoding of the global shader cache blobs.
- The static depth-state field meanings (`0x82EDE438` / `0x82EDE3A0`: {2,1} / {2,2}).
- `ScreenToShadowMatrix` construction (VMX code in 0x82CFB598).
