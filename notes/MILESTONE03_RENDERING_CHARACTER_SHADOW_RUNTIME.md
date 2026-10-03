# MILESTONE 03 — Character shadow: normal-play creation / strength runtime (2026-10-02)

Context:
- Rendering checkpoint `agents/rendering 566a87f` (read-only).
- Follows on from `MILESTONE03_RENDERING_CHARACTER_SHADOW_PATH.md` and `MILESTONE03_RENDERING_LIGHTVIS_SHADOW.md`.

Evidence:
- Read-only headless Ghidra (`tools/wfcq.ps1`), raw PPC decode.
- Xenos microcode from `Engine.xxx` ShaderCache exports (global shaders live there, not in a GlobalShaderCache file).
- A new numeric microcode emulator, `tools/xenosemu.py`.

> **CORRECTION to the previous note (§4 "light render flag bit 0x4"):**
> - `ShadowInfo+0x364` is the **subject FPrimitiveSceneInfo**, not the light. `+0x360` is the light.
> - The value tested at projection and creation is `SubjectProxy->GetViewRelevance(View)` (`PSI+8 → vt+0x1C`), a 64-bit FPrimitiveViewRelevance:
>   - **bit 0x4 = bShadowRelevance = `FPrimitiveSceneProxy::IsShadowCast(View)`** (`0x82DD8D58`);
>   - **bits 5..8 = DPG relevance** (`1 << (5 + DPG)`).
>   - It is per proxy, per view and per frame. It is not a light flag.

---

## 1. SHADOWFACTOR → MODSHADOWCOLOR / FADEALPHA

**CONFIDENCE:** CONFIRMED for the chain and the constants. PARTIAL for the projection shader's final combine, whose straight-line decode is shown below; the branchy PCF path was not emulated.

**ADDRESS / FUNCTION:**

| address | proposed name | role |
|---|---|---|
| 0x82CD4540 | `BuildCompositeShadow` (earlier note) | computes `shadowFactor` per composite light |
| 0x82CCE0A8 | `FDirectLightEnv::BuildSceneProxyData` | packs one 0x80-byte shadow record per composite light (`0x82DBF2C8` → `0x82DBF200`) |
| 0x82DE6598 | `FDirectLightEnvRenderData::ApplyShadowRecords` (render side) | for each record, updates the env's **synthetic shadow light** |
| 0x82DDD128 / 0x82DDD240 / 0x82DDD368 | `UpdateShadowLight_{Directional,Point,Spot}` | write type, matrices, ModShadowColor, resolutions and flags into the synthetic FLightSceneInfo |
| 0x83056A20 | `FSceneRenderer::CreateProjectedShadow(interaction, OutPreShadows)` | constructs FProjectedShadowInfo with **FadeAlpha = 1.0** |
| 0x83055FD8 | `FProjectedShadowInfo::FProjectedShadowInfo` | stores Light +0x360, Subject +0x364, Resolution +0x374, **FadeAlpha +0x378**, bPreShadow 0x20000000 @ +0x37C |
| 0x82D077F8 | Mod-projection `SetParameters` | `ShadowModulateColor = W + (ModShadowColor − W)·FadeAlpha`, with W = `*0x8370AE88` (white) |

**STRUCTURE / OFFSET:**
- **Shadow record** (0x80 bytes, at env render data + 0xD0 + i·0x80; count at +4):

| offset | content |
|---|---|
| +0x00 | type (1 directional/other, 2 point, 3 spot) |
| +0x10..+0x4C | source light LightToWorld (component +0x90) |
| +0x50..+0x5C | **shadowFactor rgba** |
| +0x60 | Radius (point +0x160) |
| +0x64 | ShadowFalloffExponent (point +0x188) |
| +0x68 / +0x6C | spot InnerConeAngle / OuterConeAngle (+0x1E0 / +0x1E4) |
| +0x70 / +0x74 | **source LightComponent MinShadowResolution (+0x134) / MaxShadowResolution (+0x138)** |

- **Synthetic FLightSceneInfo** fields written:
  - `+0x34` type byte (via `vt+0x1C`, `0x82E016E8`);
  - matrices and position via `0x82DFF870`;
  - **`+0x10C..+0x118` ModShadowColor rgba = shadowFactor**;
  - `+0x100` MinShadowResolution and `+0x104` MaxShadowResolution;
  - `+0x174` Radius: directional **327680.0**;
  - `+0x178` ShadowFalloffExponent: directional **2.0**;
  - `+0x17C..+0x188` cone terms: directional (0, −1, −1, 0); spot via `0x82E00C38`;
  - `+0xF8 |= 0xA0000000`;
  - Scene.Lights compact entry `+0x20 |= 0x60000000`.

**CALLERS:** DLE update → `0x82CCE0A8` → (render thread) `0x82DE6598` → the updaters. The renderer calls `0x83057028` (from `0x82EC2100`) → `0x83056A20` → `0x83055FD8`.

**CONSTANTS:**
- Not-white tolerance **1e‑4** (`0x820A1AE0`), applied in proxy build `0x82CCE0A8` and in the creation loop `0x83057028`.
- Earlier drop threshold **0.05** (`BuildCompositeShadow`).
- FadeAlpha literal **1.0** (`0x82000D3C`).

**PSEUDOCODE:**
```
// game thread (earlier note, 0x82CD4540)
fade = 1
if S is last composite entry and S.score - nextOverflow.score < 0.2 (ShadowFadeLuminanceDifference): fade *= (S.score - next)/0.2
if FadeShadowsWithLights(=1): fade *= S.smoothedVisibility
S.shadowFactor = (lerp(1, ShadowLuminanceScale(=0), fade) x3, 1)
drop S if all comps within 0.05 of 1
// proxy build 0x82CCE0A8
for each composite S: if any |S.shadowFactor - (1,1,1,1)| >= 1e-4: AppendRecord(type(S.Light), S.Light.LightToWorld, S.shadowFactor,
                         Radius, ShadowFalloffExponent, Inner/OuterCone, S.Light.MinShadowResolution, S.Light.MaxShadowResolution)
// render thread 0x82DE6598 (one synthetic light slot per light environment; slot array at +0x1C, MAX = 1)
if record count == 1: UpdateShadowLight_<type>(slot[0], record)
     slot.type = type; slot.LightToWorld = record.matrix; slot.ModShadowColor = record.shadowFactor
     slot.MinShadowResolution = record.minRes; slot.MaxShadowResolution = record.maxRes
     slot.Radius/Falloff/Cones = record values (directional: 327680, 2.0)
     slot.flags(+0xF8) |= 0x80000000 | 0x20000000 ; Scene.Lights[slot.Id].flags(+0x20) |= 0x40000000 | 0x20000000
else (no record): slot.flags &= ~0xA0000000 ; Scene.Lights[slot.Id].flags &= ~0x60000000      // shadow switched off
// shadow creation 0x83056A20
ShadowInfo.FadeAlpha = 1.0                                                     // constant; no distance/resolution fade
// projection 0x82D077F8
ShadowModulateColor = (1,1,1,1) + (Light.ModShadowColor - (1,1,1,1)) * FadeAlpha   // == shadowFactor
// Mod projection pixel shader (spot variant, Engine ShaderCache_10303 @17501), final instructions 113..129:
atten = SpotCone^2 * (1 - (saturate(|LightPos-P|*InvRadius)^2)^ShadowFalloffExponent)   // ShadowFalloffExponent = c24.x
shadowColor = lerp(1, ShadowModulateColor, atten)
oC0 = shadowColor + (1 - shadowColor) * P                      // P = PCF result (17-tap weighted: (5*edge + 12*refine)/17)
// blend: mask.rgb *= oC0.rgb
```

**ORIGINAL WFC BEHAVIOR:**
- **Origin of shadowFactor:** the game-thread light environment (DLE) `BuildCompositeShadow`.
- **Where it ends up:** the DLE's **own synthetic projector light** has its ModShadowColor overwritten with shadowFactor on every proxy build.
- **FadeAlpha:** always 1.0. **All fading is inside shadowFactor**: the luminance gap to the next candidate (0.2), times the smoothed light visibility when FadeShadowsWithLights = 1.
- **No distance or resolution fade** happens in shadow creation.
- **Strength ownership:** it belongs to the **light** (the synthetic LightSceneInfo of that character's light environment). It is applied per projected shadow through ShadowModulateColor.
- **Clamps:**
  - 1e‑4 / 0.05 "is it white" culls;
  - `saturate` on the distance term in the shader;
  - 8-bit UNORM in the mask.
- **Interpolation timing:** only the smoothed visibility of the earlier note. There is no per-shadow time fade.

**RENDERING HANDOFF:**
- CONFIRMED:
  - ModShadowColor = shadowFactor;
  - FadeAlpha = 1;
  - ShadowModulateColor = shadowFactor.
- PARTIAL: the shader combine `oC0 = lerp(lerp(1, SMC, atten), 1, P)`. It is from a straight-line decode of the spot variant; the directional and point variants were not decoded.

---

## 2. PROJECTED-SHADOW CREATION GATES

**CONFIDENCE:**
- CONFIRMED: every gate listed in the pseudocode.
- HIGH: per-frame lifetime.
- PARTIAL: robot vs vehicle proxy identity, and ShadowParent behaviour during transform.

**ADDRESS / FUNCTION:**

| address | proposed name |
|---|---|
| 0x83057028 | `FSceneRenderer::InitDynamicShadows` (per frame; caller 0x82EC2100) |
| 0x83056A20 | `CreateProjectedShadow` |
| 0x82DBFA80 | `FLightPrimitiveInteraction::FLightPrimitiveInteraction(light, prim, bIsDynamic, bUncachedStaticLighting)` |
| 0x82DE9600 | `FPrimitiveSceneInfo::FPrimitiveSceneInfo(component, proxy, scene)` |
| 0x82DD8D58 | `FPrimitiveSceneProxy::IsShadowCast(View)` |
| 0x82DD8CC0 | `FPrimitiveSceneProxy::IsShown(View)` |
| 0x82C8BCF0 | `FPrimitiveSceneProxy::GetDepthPriorityGroup(View)` |
| 0x82DDF680 / 0x82C9E5C0 / … | per-proxy `GetViewRelevance` (14 callers of IsShadowCast all OR in 0x4) |
| 0x82DEA630 | `FSceneViewState::IsShadowOccluded(prim, light)` |
| 0x83056958 | `FProjectedShadowInfo::AddSubjectPrimitive` |

**STRUCTURE / OFFSET:**
- **PrimitiveComponent:**

| offset | field |
|---|---|
| +0xBC.. | Bounds |
| +0xD8 | LightEnvironment |
| +0xDC | CullDistance |
| +0xE0 | CachedCullDistance |
| +0xE4 | DepthPriorityGroup |
| +0xE5 | ViewOwnerDepthPriorityGroup |
| +0xEC | MotionBlurScale |
| +0xF0 | bool dword 1, MSB-first: bUseViewOwnerDPG 0x80000000 … HiddenGame 0x20000000, bOwnerNoSee 0x08000000, bOnlyOwnerSee 0x04000000, **CastShadow 0x40000**, bForceDirectLightMap 0x20000, **bCastDynamicShadow 0x10000**, **bCastHiddenShadow 0x8000**, bHighQualityShadowDepthBias 0x4000, **bAcceptsLights 0x2000**, **bAcceptsDynamicLights 0x1000**, bUsePrecomputedShadows 0x800, bAllowAmbientOcclusion 0x400 |
| +0xF8 | TranslucencySortPriority |
| +0xFC | SemiTransparentRenderingOpacity |
| **+0x100** | **DynamicShadowDepthBias** |
| +0x104 | LightingChannels |

- **FPrimitiveSceneInfo:**

| offset | field |
|---|---|
| +0x08 | Proxy |
| +0x20 | Id |
| +0x30 | flags: 0x80000000 = bUsePrecomputedShadows ∧ owner/static conditions ("static shadowing"); **0x40000000 = CastShadow ∧ bCastDynamicShadow**; **0x20000000 = CastShadow**; **0x10000000 = bCastHiddenShadow**; 0x08000000 bHighQualityShadowDepthBias; 0x04000000 bAcceptsLights; 0x02000000 bAcceptsDynamicLights |
| +0x34..+0x4C | Bounds (Origin, Extent, SphereRadius @ +0x4C) |
| +0x50 | CachedCullDistance (0 → default) |
| **+0x64** | **DynamicShadowDepthBias** |
| +0x68 | LightingChannels |
| +0x98 | ShadowParent |
| +0x9C | first shadow child (next at child +0xA0) |
| +0xB0 | SemiTransparentRenderingOpacity |

- **FLightPrimitiveInteraction:**

| offset | field |
|---|---|
| +0x00 | LightSceneInfo |
| +0x04 | PrimitiveSceneInfo |
| +0x08 | flags: 0x80000000 bCastShadow, 0x40000000 bUncachedStaticLighting, 0x20000000 uncached-static-shadow counter, **bits 0x18000000 DynamicShadowType (0x08000000 = 1 shadow volume, 0x10000000 = 2 PROJECTED)** |
| +0x10 | next in the light's list |

  The light's lists are `LSI+0xF0` (static) and `LSI+0xF4` (dynamic).
- **FLightSceneInfo:**

| offset | field |
|---|---|
| +0x04 | Id |
| +0x28 | Scene |
| +0x34 | type |
| +0xB0..+0xB8 | world position |
| +0xF8 | flags: **0x80000000 = projected (not volume)**, 0x40000000, **0x20000000 = cast dynamic shadow**, 0x10000000 = cast static shadow |
| +0x100 / +0x104 | Min / MaxShadowResolution |
| +0x10C..+0x118 | ModShadowColor |
| +0x174 | Radius |
| +0x178 | ShadowFalloffExponent |

  - Scene.Lights compact entry (0x30 bytes, at Scene+0x1CF0): +0x00 LSI, **+0x20 flags 0x40000000 ∧ 0x20000000 required**.
- **Proxy:**

| offset | field |
|---|---|
| +0x10 | PSI |
| +0x74 | material relevance |
| +0x78 | flags: 0x80000000 hidden, 0x10000000 bOnlyOwnerSee, 0x08000000 bOwnerNoSee, 0x200000 bUseViewOwnerDPG, DPG = (>>18)&7, ViewOwnerDPG = (>>15)&7 |
| +0x7C | owner list |
| +0x88 | MaxDrawDistance |

**PSEUDOCODE:**
```
// interaction type, 0x82DBFA80 (when a light/primitive pair is linked)
bCastShadow = PSI.staticShadowing ? (L.flags & 0x10000000) && PSI.CastShadow
                                  : (L.flags & 0x20000000) && PSI.CastShadow && PSI.bCastDynamicShadow
if bCastShadow && bIsDynamic:
   if PSI.staticShadowing:  DST = (L.flags&0x40000000 && PSI.CastShadow) ? 1 (+uncached counter) : (PSI.bCastDynamicShadow ? 1 : -)
   else:                    DST = (L.flags & 0x80000000) ? PROJECTED(2) : (PSI.bCastDynamicShadow ? VOLUME(1) : PROJECTED(2))
// synthetic DLE light has flags 0x80000000|0x20000000 → DST = PROJECTED for CastShadow && bCastDynamicShadow primitives

// per frame, 0x83057028
for light in Scene.Lights:
   if !(compact.flags & 0x40000000 && compact.flags & 0x20000000): continue
   if light.ModShadowColor within 1e-4 of (1,1,1,1) in all four comps: continue        // strength gate
   if light not in any view (VisibleLightInfos[light.Id] word0 == 0 in every view): continue
   for inter in light.DynamicPrimitiveList (+0xF4): CreateProjectedShadow(inter, PreShadows)
   for inter in light.StaticPrimitiveList (+0xF0): if inter.PSI.flags & 0x40000000 and bounds ∩ preshadow frustum (+0x140): preshadow.AddReceiver
   per view, per existing shadow: set the view's "shadow visible" bit (view+0x540) = relevant && !occluded;
   issue the shadow occlusion query (0x82F05210) if ShowFlags bit 52 && relevant && !occluded && !preshadow

CreateProjectedShadow(inter):                                                         // 0x83056A20
  if inter.DST != PROJECTED or PSI.ShadowParent: return
  for view: rel = PSI.Proxy.GetViewRelevance(view)
     relevant |= (rel & 7) != 0                    // static|dynamic|shadow bit
     visible  |= relevant && !IsShadowOccluded(view, PSI, light)
     subjectVisible |= view.PrimitiveVisibilityMap[PSI.Id]
  if !(relevant || visible): return
  bounds = PSI.Bounds ∪ bounds of every shadow child (PSI+0x9C list) visible in any view
  if !GetProjectedShadowInitializer(light, PSI, bounds, PSI.DynamicShadowDepthBias): return     // 0x82E22A38; type must be 1/2/3
  minR = light.MinShadowResolution > 0 ? it : SystemSettings.MinShadowResolution(128)
  maxR = light.MaxShadowResolution > 0 ? it : SystemSettings.MaxShadowResolution(1024)
  res = max over views of clamp((int)(ShadowTexelsPerPixel(1.0) * ScreenRadius), min(minR, Buf-10), min(maxR-10, Buf-10))
        ScreenRadius = max(0.5*View.SizeX*Proj[0][0], 0.5*View.SizeY*Proj[1][1]) * bounds.SphereRadius / max(clipW(bounds.Origin), 1)
        Buf = GetShadowDepthResolution() = clamp(SystemSettings.MaxShadowResolution, 1, 2048)
  shadow = new FProjectedShadowInfo(light, PSI, initializer, bPreShadow=0, res, FadeAlpha=1.0)  → Renderer.ProjectedShadows (+0x5C)
  if subjectVisible: preshadow = new FProjectedShadowInfo(..., bPreShadow=1, ...) → also OutPreShadows
  AddSubjectPrimitive(shadow, each shadow child); AddSubjectPrimitive(shadow, PSI); (preshadow: same prims as receivers list +0x38C)

IsShadowCast(view) (bit 0x4):                                                         // 0x82DD8D58
  if !(PSI.flags & (0x40000000|0x20000000)): return 0                              // CastShadow required
  if proxy hidden (0x80000000) or onlyOwnerSee-not-owner or ownerNoSee-owner: return PSI.bCastHiddenShadow
  return View.ViewOrigin.W > 0 && |PSI.Bounds.Origin - View.ViewOrigin|^2 * LODDistanceFactor^2 < MaxDrawDistance^2
```

**ORIGINAL WFC BEHAVIOR:**
- **Actor/component eligibility:**
  - The skeletal (or vehicle) mesh component needs **CastShadow and bCastDynamicShadow**.
  - It needs no ShadowParent; children are folded into the parent's single shadow.
  - It must not be hidden, unless bCastHiddenShadow is set.
  - It must be within MaxDrawDistance (proxy+0x88) for the view LOD factor.
  - It must be in a light environment, so that it interacts with that environment's synthetic light (see §5).
- **Light eligibility:** the DLE synthetic light, with flags set by the updater and ModShadowColor ≠ white. The light must also be in the view frustum of at least one view.
- **bAcceptsLights / bAcceptsDynamicLights:** copied to PSI (0x04000000 / 0x02000000), but **not tested** in any creation step traced here.
- **DPG:** creation needs no DPG. Projection needs the subject relevance bit (5 + DPG) for the DPG being rendered.
- **Culling:**
  - No screen-size cut-off. ScreenRadius only picks the resolution, clamped between [Min, Max].
  - Distance cull is via MaxDrawDistance in IsShadowCast.
  - The occlusion query result can hide a shadow for a view (IsShadowOccluded).
- **Lifetime:** shadows are **allocated every frame** in InitDynamicShadows (heap 0x3E0 bytes; no cache or reuse observed). Destruction is with the frame's renderer (HIGH, stock).
- **One projector per character:** see §5.
- **Robot vs vehicle:** the same code path. Only the proxy class's GetViewRelevance differs.
  - `0x82C9E5C0` (a proxy with its own DPG byte at +0x3E0, likely the skeletal proxy, unverified) has an early-out branch: proxy+0x3E4 bits (0x200000 ∧ 0x8000000) or (0x40000000 ∧ owner-view test).
  - That branch returns 0x8242: foreground DPG, **no shadow bit**.

**RENDERING HANDOFF:** CONFIRMED gates as listed. The skeletal early-out branch semantics are PARTIAL.

---

## 3. SHADOW-SPACE MATRIX CONSTRUCTION

**CONFIDENCE:**
- CONFIRMED: origin, push-back, MinLightW and MaxLightW, the depth-bias input, resolution and border.
- PARTIAL: the frustum fit (VMX128 code not decoded).
- UNKNOWN: the exact ScreenToShadowMatrix texel/half-texel terms.

**ADDRESS / FUNCTION:**

| address | proposed name |
|---|---|
| 0x82E22A38 | WFC `GetProjectedShadowInitializer(light, PSI, bounds, DynamicShadowDepthBias, out)` — not virtual; one function for all types |
| 0x82DBF678 | synthetic light `vt+0x3C` GetShadowOrigin(PSI) |
| 0x82DBF728 | `vt+0x40` GetMaxLightW |
| 0x82DBF768 | `vt+0x44` GetShadowFalloffExponent |
| 0x83038020 | `FProjectedShadowInitializer::CalcTransforms`-equivalent |
| 0x8301CD08 | bounding fit of the projected corners |
| 0x82CFB598 | ScreenToShadowMatrix (earlier note; VMX) |

**CONSTANTS:**
- √2 = sqrt(2.0) (cached at runtime);
- MinLightW **0.1** (`0x82001720`);
- W cut-off **1e‑5** (`0x8209E570`) → corner set to FLT_MAX;
- directional origin offset **300.0** (`0x82033B50`);
- radius 327680 and falloff 2.0 for directional;
- shadow buffer border **10 texels** (5 per side).

**PSEUDOCODE:**
```
GetProjectedShadowInitializer(L, PSI, B, depthBias):                            // 0x82E22A38
  if L.type not in {1,2,3}: return false
  O = L.GetShadowOrigin(PSI)            // point/spot: L.Position (+0xB0); directional: B.Origin - D*axis, D = 2*B.SphereRadius + 300,
                                        // axis = (L+0x48, L+0x58, L+0x68)
  v = B.Origin - O ; dist = |v| ; n = v/dist
  if dist <= sqrt(2)*B.SphereRadius:  dist = sqrt(2)*R ; O = B.Origin - n*dist   // keep the subject inside the frustum
  MaxW = L.GetMaxLightW(PSI)            // point/spot: Radius (+0x174); directional: 2*(2R + 300)
  build light-space matrix: translate(-O), rotate so +X/face axis = n  (VMX code, not decoded)
  return CalcTransforms(matrix, faceDir n, bounds-relative-to-O, dist, MinLightW 0.1, MaxW, depthBias)  // 0x83038020
CalcTransforms:  8 corners of B (Origin±Extent) → light space → W = WAxis·P ; if W < 1e-5 corner := FLT_MAX else P/W
                 bounding fit (0x8301CD08) of the projected corners → subject matrix (VMX, not decoded)
```

**ORIGINAL WFC BEHAVIOR:**
- **Projection type:** perspective for **all** projector types. A directional composite is a point projector placed `2R + 300` behind the subject along the light axis.
- **Minimum distance:** the projector is pulled back to `√2·R` when closer than that.
- **Depth range:** MinLightW 0.1; MaxLightW is the radius for point/spot and `2·D` for directional.
- **Depth bias input:** the component's DynamicShadowDepthBias is passed into the fit.
- **Resolution:** chosen per shadow (§2) with a 5-texel border.
- **Not found:** no stabilisation or snapping.

**RENDERING HANDOFF:**
- CONFIRMED: the origin, push-back and W-range rules above.
- PARTIAL/UNKNOWN: the frustum fit and the texture-space matrix. Do not treat a guess at either as recovered.

---

## 4. BLUR KERNEL WEIGHTS

**CONFIDENCE:**
- CONFIRMED for pass structure, offsets, constants, weights and normalisation. The main path was emulated and matches the closed form on 8192 tap combinations.
- PARTIAL for the tie branch: `S(−B) == S(−A) && S(+B) > S(−B)`. Its result depends on one decoded swizzle.

**ADDRESS / FUNCTION:**
- `0x82DDB070` BlurShadowMask(W, H): 2 passes.
- `0x82E0C8A0` FBlurShadowMaskPixelShader::SetParameters.
- `0x82C8A5F0` / `0x82C87F68`: sampler state.
- Shader: `Engine.xxx` ShaderCache_10303 + 367646 (0x2F0 bytes, GUID b4699b69…). It is identical in every Engine ShaderCache export.

**CONSTANTS:**
- `Offsets` (c3), pass 0 horizontal = `(0.5/W, 0, 1.5/W, 0)`.
- `Offsets` (c3), pass 1 vertical = `(0, 0.5/H, 0, 1.5/H)`.
- `Options` (c4) = `(4.0, 0, 0, 0)` (`0x823FBB3C`, static).
- Shader literal c255 = (4, 1, 0, 0).
- Sampler = {Filter 1 = bilinear, Address 1/1/1 = clamp, MipBias 0}.
- Texture = resolved ShadowMask (`0x83862680`).
- W, H = ShadowMask size (SceneRT+0x24 / +0x28, the downsampled scene size).

**PSEUDOCODE (pixel shader, one pass):**
```
A = c3.xy (0.5 texel), B = c3.zw (1.5 texel), C = 2A + B (2.5 texel)       // along the pass axis
s(±A), s(±B), s(±C) = ShadowMask.x bilinear at uv ± A/B/C                   // 6 bilinear taps ≈ 12 texels
w(±A) = 4*(4 - s), w(±B) = 2*(4 - s), w(±C) = 1*(4 - s)                      // data-dependent: darker samples weigh more
x = Σ w_i s_i / Σ w_i
tie case (PARTIAL): f = (s(-B) == s(-A)) && (s(+B) > s(-B));  x = x*(1-2f) + f*(s(-A) + s(+A))
out = (pass is horizontal: Offsets.y == Options.y(0)) ? x*x : x              // horizontal pass squares
CPU: for pass in (H, V): BeginRenderingShadowMask(no clear); set Offsets; draw full-screen quad (0,0,W,H); FinishRenderingShadowMask (resolve)
```

**ORIGINAL WFC BEHAVIOR:**
- **Pass structure:** a separable **6-tap bilinear** pass (12 texels), horizontal then vertical.
- **Weighting:** **non-linear, darkness-biased** normalised weights, with base weights 4/2/1 × (4 − s).
- **Squaring:** the first (horizontal) pass output is squared.
- **Render targets:** each pass reads the resolved mask texture and writes the same mask surface, then resolves.
- **No resolution dependence** except the texel size (W, H). It does not depend on shadow settings.
- **Scope:** one global pass, the same for every character and vehicle shadow.
- **When it runs:** only if a shadow was drawn and blur is not disabled.

**RENDERING HANDOFF:** implement exactly the decoded formula. The tie branch is PARTIAL.

---

## 5. NORMAL-PLAY SHADOW LIGHT SELECTION → PROJECTOR

**CONFIDENCE:** CONFIRMED for the handoff mechanics. PARTIAL for how the synthetic light is created and registered (slot allocation and interaction linking not traced).

**ADDRESS:** `0x82CCE0A8`, `0x82DE6598`, `0x82DDD128` / `0x82DDD240` / `0x82DDD368`. Synthetic-light vtable `0x822DD770` (type setter `0x82E016E8`, origin `0x82DBF678`, MaxW `0x82DBF728`).

**PSEUDOCODE:** see §1. Per light environment: **one** synthetic projector slot. If a composite light exists, it is updated in place with that light's type, LightToWorld, radius/falloff/cones, Min/MaxShadowResolution and shadowFactor. Otherwise its shadow flags are cleared.

**ORIGINAL WFC BEHAVIOR:**
- **What projects:** never the original scene light. The projector is a **synthetic per-environment FLightSceneInfo** that copies the selected composite light's geometry: its type and position/direction.
- **Composite selection:** the earlier note: brightest bCastCompositeShadow light, visibility ignored, maximum one.
- **Baked lights:** they *can* drive it, since selection ignores baked/unbaked status.
- **Replacing the selected light:**
  - When it changes, the same slot is overwritten the next proxy build.
  - There is **no projector crossfade**. Smoothness comes only from shadowFactor: the 0.2 luminance gap and the smoothed visibility.
- **No composite:** the slot's flags are cleared, so no shadow is created. The DefaultShadowLight fallback is never used for WFC pawns (earlier note).
- **Robot vs vehicle:** the same mechanism. Each light environment has its own slot. Transform continuity depends on whether the light-environment component survives the transform, which was not traced.

**Why the rebuild's opt-in path works but normal play has no projector:** normal play must create, per light environment, a dedicated projector light. It is not the scene light. Its geometry follows the composite selection, ModShadowColor = shadowFactor, FadeAlpha = 1, and its projected interactions apply to the environment's own CastShadow/bCastDynamicShadow primitives.

---

## 6. SOURCE FLAG / DPG REQUIREMENTS

**CONFIDENCE:** CONFIRMED.

| item | meaning | producer | scope | changes when |
|---|---|---|---|---|
| relevance bit **0x4** | bShadowRelevance = IsShadowCast(View) | each proxy's GetViewRelevance (`vt+0x1C`), via `0x82DD8D58` | per proxy × view, recomputed each call | CastShadow, hidden state, owner/view, distance vs MaxDrawDistance |
| relevance bits **5..8** | DPG mask, `1 << (5 + DPG)` | `0x82C8BCF0`: proxy+0x78 DPG (>>18 & 7), or ViewOwnerDPG (>>15 & 7) when bUseViewOwnerDPG and the view's owner is in the owner list | per proxy × view | component DPG or ViewOwnerDPG; the view owner |
| relevance bits 0 / 1 | static / dynamic relevance | GetViewRelevance | per proxy × view | — |
| LSI +0xF8 0x80000000 / 0x20000000 | projected / cast-dynamic-shadow | DLE updaters (set) / `0x82DE6598` (clear) | per synthetic light | each proxy build |
| Scene.Lights +0x20 0x40000000 / 0x20000000 | light may create shadows | same | per light | same |
| interaction +8 bits 0x18000000 | DynamicShadowType | `0x82DBFA80` | per light × primitive | on (re)link |
| ShadowInfo +0x37C 0x20000000 | bPreShadow | `0x83055FD8` | per shadow | per frame |

---

## SHADOW STRENGTH HANDOFF
- **CONFIRMED:**
  - shadowFactor (DLE) → synthetic light ModShadowColor (+0x10C) every proxy build;
  - FadeAlpha is always 1.0;
  - ShadowModulateColor = shadowFactor;
  - a light whose colour is within 1e‑4 of white creates no shadow.
- **CONFIRMED (earlier):** all fading is inside shadowFactor (0.2 luminance gap × smoothed visibility).
- **PARTIAL:** the shader combine `lerp(lerp(1, SMC, atten), 1, PCF)`. It is from the spot variant; the directional and point variants were not decoded.

## SHADOW CREATION HANDOFF
- **CONFIRMED:**
  - interaction DST = PROJECTED (synthetic light flags + PSI CastShadow ∧ bCastDynamicShadow);
  - light flags and the not-white test;
  - the light is in at least one view;
  - the subject has no ShadowParent;
  - the subject is relevant (relevance & 7) or visible (not occluded);
  - the initializer succeeds;
  - resolution = clamp(1.0 × ScreenRadius, min(Min, 1014), min(Max − 10, 1014));
  - shadows are rebuilt every frame;
  - a preshadow exists when the subject is visible.
- **PARTIAL:** the skeletal-proxy early-out (0x8242) conditions.

## SHADOW LIGHT-SELECTION HANDOFF
- **CONFIRMED:**
  - one synthetic projector per light environment;
  - it copies the composite light's type, transform, radius/falloff/cones and Min/MaxShadowResolution;
  - it is updated in place, with no crossfade;
  - its flags are cleared when there is no composite.
- **PARTIAL:** how the slot light is created, added to the scene and linked to the environment's primitives.

## SHADOW-SPACE MATRIX HANDOFF
- **CONFIRMED:**
  - perspective for every type;
  - origin = light position (point/spot) or `B.Origin − (2R + 300)·axis` (directional);
  - push-back to `√2·R`;
  - MinLightW 0.1, MaxLightW = radius or `2(2R + 300)`;
  - DynamicShadowDepthBias is passed in;
  - 5-texel border.
- **PARTIAL:** the CalcTransforms fit (corner projection is CONFIRMED; the bounding fit and the VMX matrix are not decoded).
- **UNKNOWN:** the ScreenToShadowMatrix texel and half-texel terms.

## BLUR KERNEL HANDOFF
- **CONFIRMED:**
  - 2 passes (H then V), each a bilinear/clamp 6-tap at ±0.5/±1.5/±2.5 texels;
  - weights `{4, 2, 1}·(4 − s)` with normalised sum;
  - the horizontal pass output is squared;
  - the same for all shadows; runs at mask resolution.
- **PARTIAL:** the tie branch.

## FLAG / DPG HANDOFF
- **CONFIRMED:**
  - 0x4 = subject proxy IsShadowCast(View); it is **not** a light flag;
  - DPG = relevance bits 5..8 from the proxy's (View)DPG;
  - light-side gating = LSI+0xF8 0x80000000 / 0x20000000 and compact +0x20 0x60000000, set and cleared by the DLE.

## STILL UNKNOWN
- Synthetic projector slot creation and registration, and its LightEnvironment interaction linking.
- Whether ordinary scene lights can also form PROJECTED interactions with light-environment primitives.
- The VMX128 frustum-fit and ScreenToShadowMatrix math.
- The directional and point Mod-projection shader variants.
- The blur tie-branch exact form.
- The identity of proxy `0x82C9E5C0` and its 0x8242 early-out conditions.
- Light-environment survival across robot↔vehicle transform.
