# MILESTONE 03 addendum — Rendering native: LightsVisibilitiesVolume + character light/shadow selection

Pass date: 2026-10-02. Scope: the two Rendering requests only.

Sources:
- Read-only Ghidra snapshot via `tools/wfcq.ps1`. The new `dis` command disassembles in memory only.
- Package metadata via `tools/pkgload.py`.
- AssetTools `authored.db`, read-only.

Bool bitfields on this Xbox build are packed **MSB-first**: the first declared bool is 0x80000000. This was verified against SoundNodeRoot and AudioComponent, where it reproduces every bit seen in code.

**Name correction.** The class is `LightsVisibilitiesVolume` (plural "Lights"). Script properties: `Octree` (native pointer), `FineLength`, `CoarseLength`, `bDisplayOctree`.

**There is no DynamicLightEnvironmentComponent in WFC.** High Moon's `LightEnvironmentComponent` drives a native "DirectLightEnv" system:
- It uses LightsVisibilitiesVolume for baked light visibility.
- It uses BeastLightEnvironmentVolume SH probes for indirect light.
- Its console tunables are listed in §2.

---

## 1. LIGHTSVISIBILITIESVOLUME

**CONFIDENCE:**
- CONFIRMED for the layout, traversal, interpolation, encoding and outside-volume behaviour.
- PARTIAL for: the meaning of the octree float at +0x18; the archive flag that halves count bytes on load; how the time-sliced queue is drained.

### ADDRESSES
| address | name (proposed) | role |
|---|---|---|
| 0x82DE6C28 | `ALightsVisibilitiesVolume::StaticClass` registration | object size 0x1DC; InternalConstructor 0x82E11470; vtable **0x822DF6F0** |
| 0x82DF5AF8 | `ALightsVisibilitiesVolume::Serialize` (vt+0x38) | Super::Serialize (0x82BA8DF8), then `u8 bHasOctree`, then the octree |
| 0x82DF5748 | `FLightsVisibilityOctree::Serialize` | the whole blob |
| 0x82DF5590 | `FLVNode::Serialize` (recursive) | node format |
| 0x82DE6EE8 | `ALightsVisibilitiesVolume` destroy/unregister (vt+0x2C) | frees the octree; removes the volume from World+0x2C8 |
| 0x82DD7C08 / 0x82DD1F78 | bind a light to every octree | match LightComponent.LightGuid (+0xD0..0xDC) against the table GUIDs, then store the component pointer |
| 0x82DD2050 | rebind a whole light list | same as above |
| 0x82CCAC30 | `LightEnv::QueryLightsVisibility` | chooses the volume, then queries |
| 0x82DC05C8 | `Volume::OctreeContains(pos)` | strict root-cube test |
| 0x82DDE5F8 / 0x82DDE200 | `Volume::Query` / `Octree::Query` | outputs lights[] and visibility[] |
| 0x82DDDA08 | `Octree::QueryNode` (recursive) | descent and interpolation |
| 0x82DDD798 | `AccumulateSample(acc, sample, weight)` | weighted merge |
| 0x82E03238 | `Renormalize(acc, scale)` | — |
| 0x82DCB4A0 / 0x82DCB3E0 | `Octree::FindLeaf(point, outBounds)` | neighbour lookup |
| 0x82F62A50 | `ChildBounds(parent, childIdx)` | — |
| 0x82DC03C8 | `CellCorners(bounds) -> 8 positions` | — |
| 0x82DDE3F0 | `Octree::GetBoundLights` | every table entry with a bound component |

### STRUCT LAYOUT
`ALightsVisibilitiesVolume`: +0x1D8 = `FLightsVisibilityOctree*`. Volumes register on **World+0x2C8/+0x2CC**, a TArray.

`FLightsVisibilityOctree` (0x58 bytes, heap):
| off | type | meaning |
|---|---|---|
| 0x00 | ptr | owning volume |
| 0x04 | ptr | root holder (0x14 bytes; root node pointer at +0x10, tagged) |
| 0x08 | FVector | **root cube centre** |
| 0x14 | float | **root half-extent** (cube) |
| 0x18 | 4 bytes | serialized, not read by the query (UNKNOWN; possibly depth or Coarse/Fine) |
| 0x1C | float | **finest-cell half-extent** (used for the neighbour epsilon) |
| 0x20 | TArray<u16> | **corner-id → sample-id remap** |
| 0x2C | ptr | next octree (global list head `0x83832ACC`) |
| 0x30 | TArray<u8> | **per-sample pair count** (`& 0x7F`). Bit 7 is a flag (see below). |
| 0x3C | TArray<u32*> | per-sample pointer into the pair pool. Built at load from cumulative counts; not serialized. |
| 0x48 | u32* | **pair pool** (Σ(count & 0x7F) records) |
| 0x4C | TArray<Entry 0x18> | **light table**: {FGuid LightGuid (16 B), int index (−1, runtime), ULightComponent* (runtime bind)} |

Node, 0x14 bytes in memory. Children are allocated as 8 contiguous nodes.
- +0x00..+0x0F: `u16 corner[8]`; 0xFFFF = none.
- +0x10: `children_ptr | hasData(bit0)`.

### SERIALIZED BLOB (big-endian; licensee version ≥ 0x72 path, which is WFC's)
```
u8   bHasOctree                                  // volume Serialize; 0 => no octree
Node(root)                                       // recursive, below
f32  center.x, center.y, center.z                // +0x08
f32  rootHalfExtent                              // +0x14
u32  unk18                                       // +0x18
f32  finestHalfExtent                            // +0x1C
i32  nLights ; nLights * { u32 a,b,c,d }         // FGuid per light; table index = order
i32  nCorners ; nCorners * u16                   // corner-id -> sample-id remap
i32  nSamples ; nSamples * u8                    // per-sample count byte
for s in 0..nSamples-1: (count[s] & 0x7F) * u32  // pair records, concatenated in sample order

Node:
  8 * i32   corner ids (low 16 bits used; 0xFFFF = none)   // each u16 is stored as int32
  i32       hasData (licensee >= 0x62; else hasData = (corner[0] != 0xFFFF))
  u8        hasChildren
  if hasChildren: 8 * Node                       // child index = (x>c.x)<<2 | (y>c.y)<<1 | (z>c.z)
```
- Licensee < 0x72 used an older body format, which is converted on load and is not relevant to WFC (licensee 144).
- On load, if archive field +0x20 is non-zero, every count byte is shifted right by 1 (PARTIAL: the flag's identity is unknown). Check the blob: Σ(count & 0x7F) must equal the number of pair records.

**Pair record (u32):**
- `lightIndex = (int16)(rec >> 16)` — index into the light table, in serialized order (0..267 in Streets).
- `visibility = (rec & 0xFFFF) / 65535.0`.
- Records inside a sample **must be sorted by ascending lightIndex**, because the merge relies on it.
- 1/20-step visibilities are bake-time quantization; the runtime treats the value as 16-bit fixed point.

### OCTREE TRAVERSAL + INTERPOLATION (PSEUDOCODE)
```
Volume selection (0x82CCAC30): pos = LightEnv bounds origin (component +0x08)
  vol = LAST volume in World.LightsVisibilitiesVolumes with |pos - center| < rootHalf on every axis (strict)
  if none: no baked visibility (all baked lights -> visibility 0, see §2)
Octree::Query(pos):
  if pairPool == null or pos outside root cube: return false
  acc = [] (sorted u32 list, reserve 100)
  if !QueryNode(root, bounds{center, rootHalf}, pos, acc): return false
  for r in acc: li = (int16)(r>>16); if li != -1 and table[li].component != null:
      outLights.add(table[li].component); outVis.add((r & 0xFFFF)/65535)
  return true

QueryNode(node, B{c,h}, p, acc):
  if node.children:
     i = (p.x>c.x)<<2 | (p.y>c.y)<<1 | (p.z>c.z)
     return QueryNode(children[i], {c + (±h/2 per bit, -1 if bit 0 else +1), h/2}, p, acc)
  if !node.hasData: return false
  corners k=0..7: pos_k = c + ((k&1)?+h:-h, (k&2)?+h:-h, (k&4)?+h:-h)   // corner bit0=X, bit1=Y, bit2=Z
  eps = finestHalf * 0.5
  // T-junction test: probe the 6 face neighbours only when this leaf is not finest
  tj = false
  if finestHalf < h:
     for axis in X,Y,Z, side in (-,+):
        q = p ; q[axis] = c[axis] ± (h + eps)
        nb = FindLeaf(q)                     // null if q outside root
        if nb and nb.h <= h - eps: tj = true  // a finer neighbour exists
  emptyW = 0 ; inv = 1/(2h)
  if !tj:   // plain trilinear
     for k in 0..7:
        s = remap[node.corner[k]]; cnt = counts[s] & 0x7F
        w = (1-|p.x-pos_k.x|*inv)(1-|p.y-pos_k.y|*inv)(1-|p.z-pos_k.z|*inv)
        if cnt == 0: emptyW += w
        else Accumulate(acc, pairs[s][0..cnt), w)
  else:     // face-blended: 6 faces x 4 corners, bilinear in each face plane, face weight 1/3
     t = (p - (c - h)) / (2h)               // normalized 0..1 per axis
     faces: 0:-X{0,2,4,6} 1:+X{1,3,5,7} 2:-Y{0,1,4,5} 3:+Y{2,3,6,7} 4:-Z{0,1,2,3} 5:+Z{4,5,6,7}
     for f in 0..5: axis = f>>1
        fw = ((f&1) ? t[axis] : 1 - t[axis]) * (1/3)
        src = (nb_f == null or nb_f.h >= h - eps) ? (this node, this bounds) : (nb_f node, nb_f bounds)
        invS = 1/(2*src.h)
        for k in face corners:
           cid = src.corner[k]; if cid == 0xFFFF: invalid
           else s = remap[cid]; flag = counts[s]>>7; cnt = counts[s]&0x7F
           w3 = per-axis (1-|p-pos_k|*invS), with the face-normal axis forced to 1   // bilinear
           if invalid or flag: emptyW += w3*fw
           else Accumulate(acc, pairs[s][0..cnt), w3*fw)
  if emptyW > 0: for r in acc: vis16 = (u16)(vis16 * 1/(1-emptyW))   // renormalize away empty/invalid corners
  return true

Accumulate(acc, recs, w):       // both lists sorted by light index; 16-bit fixed point
  merged value = (int)(( rec.vis/65535 * w + acc.vis/65535 ) * 65535)   // truncation at every step
  lights absent from acc are inserted at their sorted position with (int)(rec.vis/65535*w*65535)
```
Notes:
- On the plain trilinear path, a corner sample with **0 pairs counts as empty** and is renormalized away, not treated as "all lights invisible".
- On the face path, a 0-pair sample with bit 7 clear contributes nothing and is **not** renormalized.
- The sample-flag bit 7 is honoured only on the face path.

### ORIGINAL WFC BEHAVIOR
- **Lookup position:** the LightEnvironment bounds origin, i.e. the owner bounds centre at the last full update. It is not per sample point.
- **Outside every volume, or in an empty leaf:**
  - the query fails, so **every baked light (present in that octree's table) gets visibility 0**;
  - unbaked lights are ray-traced (§2).
- **Overlapping volumes:** the last-registered volume that contains the point wins.
- **Actor classes:** all use the same query. The only per-actor differences are the component settings (§2).

### RENDERING HANDOFF
- Implement the decoder and query exactly as above:
  - child index uses X-high (bit 2 = X);
  - corner index uses X-low (bit 0 = X);
  - corner ids go through the `u16` remap before indexing counts and pairs;
  - pair = (int16 light, u16 vis);
  - light index = position in the serialized GUID table;
  - bind lights by `LightComponent.LightGuid`;
  - T-junction face blend weight is 1/3;
  - renormalize empty corners away;
  - query once at the bounds origin.
- **Constants:** 65535 (and 1/65535 = 1.5259e-5); 0.5 (child half and eps factor); 2.0 (edge = 2h); 1/3 (face weight); accumulator reserve 100; licensee gates 0x52 / 0x62 / 0x72.

### EXPERIMENTAL CHECKS NOW SAFE TO PROMOTE
1. Σ(count & 0x7F) equals the number of pair records, and nLights equals the number of distinct GUIDs. Streets: about 7,679 pairs, 268 lights.
2. Pair indices inside each sample are strictly ascending.
3. Child and corner bit order as specified.
4. Visibility is 0 for baked lights outside all volumes.

### STILL UNKNOWN
- The meaning of the octree float at +0x18.
- The identity of the archive flag at +0x20 that halves count bytes on load. Check empirically with Experimental check 1.
- The meaning of count-byte bit 7. It is consumed as "invalid" only on the face path.

---

## 2. WFC CHARACTER LIGHT / SHADOW SELECTION (DirectLightEnv)

**CONFIDENCE:**
- CONFIRMED: gathering, visibility, weighting, ranking, composite-shadow selection, update cadence, constants.
- PARTIAL: the scene light-gather callback (owner vtable +0x174), the time-sliced queue drain rate, and the spot-light intensity function.

### ADDRESSES
| address | name (proposed) | role |
|---|---|---|
| 0x82DD19F0 | `ULightEnvironmentComponent::Tick` | per-tick driver |
| 0x82DD17C8 | `ULightEnvironmentComponent::GetUpdateMode` | 0 none / 1 full / 2 incremental |
| 0x82DD1B00 | `ULightEnvironmentComponent::UpdateLight(mode)` (vt slot at 0x822DEBC0) | bounds, then env update |
| 0x82CE4E78 | `FDirectLightEnv::Update(bFull, bounds, …)` | the core |
| 0x82CCACE0 | `BuildSamplePoints` | origin + NormalizedSampleOffsets[i] ⊙ extent, max 8, padded with origin |
| 0x82CE1918 | `FDirectLightEnv::AddLight` | per-light visibility and colour |
| 0x82CDDE70 | `FDirectLightEnv::SmoothAndRank` | temporal fade, then ranked lists |
| 0x82CD4108 | insert into **DirectLights** (env+0x50, cap env+4 = TotalLightCount) | — |
| 0x82CD4038 | insert into **OverflowLights** (env+0x5C) → SH | — |
| 0x82CD42B8 | insert into **CompositeShadowLights** (env+0x6C, cap `DirectShadowLightCount` = 1); overflow → env+0x78 | — |
| 0x82CCB098 / 0x82CC6EE8 | overflow lights → SH (env+0x108), as directional SH from the light toward the origin | — |
| 0x82CCB110 | boundary-light crossfade factor (env+0x68) | — |
| 0x82CCB488 / 0x82CCB228 | SH: sky upper/lower + Beast probe (BeastLightEnvironmentVolume, highest Priority, averaged) | — |
| 0x82CD4540 | `BuildCompositeShadow` | — |
| 0x82CCE0A8 | `BuildSceneProxyData` | SH, direct lights, composite shadow → render thread |
| 0x82DF25F8 | `exec DirectLightEnv <key> <value>` | console tunables |
| 0x82D32DB8 | `CreateDefaultShadowLight` (World+0x1E0) | — |
| 0x82DBEAC0 | DirectionalLightComponent vt+0x194 `IntensityAt(p)` | = Brightness |
| 0x82DC1F60 | PointLightComponent vt+0x194 `IntensityAt(p)` | — |

### STRUCT LAYOUT

`ULightEnvironmentComponent`:
| off | field |
|---|---|
| +0x40 | bools: bEnabled 0x80000000, bDisallowForcedUpdates 0x40000000, bNoRayCasts 0x20000000, bUpdateIfBoundsChange 0x10000000 |
| +0x4C | native env |
| +0x50 | EnvironmentTransitionTime |
| +0x54 | UpdateDistanceThreshold |
| +0x5C/+0x60 | NormalizedSampleOffsets |
| +0x68 | TotalLightCount |
| +0x6C | bools: bHasAlreadyDisplayedBoundingRadiusWarning 0x80000000, bWasMoving 0x40000000 |
| +0x7C | LastUpdateOwnerWorldPosition |
| +0x88 | LastUpdateOwnerBoundingSphereRadius |
| +0x8C | ForceNextUpdateTime |

`LightComponent`:
| off | field |
|---|---|
| +0xC0 | world position |
| +0xD0 | LightGuid |
| +0xF0 | Brightness |
| +0xF4 | LightColor, stored as a big-endian ARGB dword: A +0xF4, R +0xF5, G +0xF6, B +0xF7 (consistent with 0.3/0.59/0.11 weights) |
| +0xF8 | Function (LightFunction*) |
| +0xFC | bools: bEnabled 0x80000000, CastShadows 0x40000000, CastStaticShadows 0x20000000, bEnablePlayerRelevant 0x10000000, CastDynamicShadows 0x08000000, **bCastCompositeShadow 0x04000000**, … |
| +0x124 | ModShadowColor |

Light subclasses:
- **PointLight:** +0x160 Radius, +0x164 FalloffExponent.
- **SpotLight:** +0x1E0 / +0x1E4 cone angles, consumed by the proxy.
- **SkyLight:** +0x160 LowerBrightness, +0x164 LowerColor.

### CONSTANTS / DEFAULTS
- **DirectLightEnv tunables** (`exec DirectLightEnv <key> <value>`):
  - `DirectShadowLightCount` = 1 (0x83711CC4)
  - `ShadowLuminanceScale` = **0.0** (0x8382DDF0; BSS; no shipped config or level sets it)
  - `DynamicShadowLuminanceScale` (0x8382DDF4; a shader constant)
  - `ShadowFadeLuminanceDifference` = **0.2**
  - `IndirectIlluminationOnly` = 0
  - `FadeShadowsWithLights` = **1**
  - `EnableLightsVisibilityVolumes` = 1
- **Component defaults:** EnvironmentTransitionTime 0.5, UpdateDistanceThreshold 50, TotalLightCount 1, offsets [(0,0,0)].
- **WFC overrides:**
  - `Default__TnRobotForm.LightEnvironment0`: **6 offsets, TotalLightCount 2, UpdateDistanceThreshold 30**.
  - `Default__TnVehicleForm.MyLightEnv`: **5 offsets, TotalLightCount 2, UpdateDistanceThreshold 30**.
  - Both use transition 0.5.
- **Ray-count rule:** N = round(15·√(lum(color·maxIntensity)) + 0.5), clamped to [1, numSamplePoints]. lum = 0.3R + 0.59G + 0.11B; colour bytes × 1/255.
- **Per-sample visibility test:**
  - intensity ≥ **0.03** → shadow ray (unless bNoRayCasts);
  - 0.01 < intensity < 0.03 → counted visible with no ray;
  - ≤ 0.01 → invisible.
- **Stagger:** random slot mod **5** per light.
- **Temporal fade rate:** clamp(|ownerVelocity|·**0.002**, **0.2**, 1) / EnvironmentTransitionTime, per second.
- **Update thresholds:**
  - Detail scale table [1, 2, 3, 5].
  - Not rendered for > **0.1 s** → threshold² × **100**.
  - Bounds radius clamp **5000**.
- **Composite shadow:**
  - remove when within **0.05** of neutral;
  - neutral factor (1,1,1,1).
- **DefaultShadowLight:** directional, Brightness 0, CastShadows + bCastCompositeShadow, ModShadowColor (0.5,0.5,0.5,1), direction (0,0,−1).

### PSEUDOCODE
```
Tick(dt):                                             // 0x82DD19F0
  if !bEnabled or !Owner or paused: return
  mode = GetUpdateMode()
  if ForceNextUpdateTime > 0 and (ForceNextUpdateTime -= dt) <= 0: ForceNextUpdateTime = 0; immediate update
  elif mode == 1: enqueue in the global time-sliced updater (0x83833084)  -> later UpdateLight(1) = FULL re-gather
  elif mode == 2: UpdateLight(2) now                  // INCREMENTAL: re-evaluate already-known lights, no re-gather
  TickTransitions(dt)

GetUpdateMode:                                        // 0x82DD17C8
  if Owner hidden-flag: return 0
  T = DetailScale[detailMode] * UpdateDistanceThreshold ; k = (Now - Owner.LastRenderTime > 0.1) ? 100 : 1
  if |BoundsOrigin - LastUpdateOwnerWorldPosition|^2 > T^2*k: bWasMoving = 1; return 1
  if bWasMoving and |Owner.Velocity| ~ 0 (each axis < 1e-4): bWasMoving = 0; return 1   // one settle update
  if bUpdateIfBoundsChange: return (|ΔBoundsRadius| > T) ? 1 : 0
  return (env has known lights) ? 2 : 0

Update(full):                                         // 0x82CE4E78
  if full: candidates = Owner/scene gather (vt+0x174) by bounds   // PARTIAL: callback body not traced
  else:    candidates = lights already attached to this env
  if candidates and EnableLightsVisibilityVolumes:
     (bakedHit[], bakedVis[]) = LightsVisibilitiesVolume.Query(boundsOrigin)       // §1
     bakedAll[] = all lights bound in that octree's table
  samples = BuildSamplePoints()          // origin + offset_i * extent (component-space normalized), <=8
  for L in candidates: AddLight(L)
  OverflowToSH(); BoundaryCrossfade(); FinalizeSH(sky + Beast probe); BuildCompositeShadow(); BuildSceneProxyData()

AddLight(L):                                          // 0x82CE1918
  if L is SkyLight: SH ambient upper += Color*Brightness ; lower += LowerColor*LowerBrightness ; return
  if L in bakedAll:                                   // baked light
     I = L.IntensityAt(origin) ; vis = (L in bakedHit) ? min(1, bakedVis) : 0
  else:                                               // dynamic / unbaked light
     if L.position inside the owner's bounding box: I = L.IntensityAt(origin); vis = 1
     else:
        Imax = max_i L.IntensityAt(sample_i)
        N = clamp(round(15*sqrt(lum(Color*Imax)) + 0.5), 1, numSamples)
        if N > 1 and the light was invisible last time and its stagger counter > 0: counter--; N = 1
        hits = count over N samples: I_i >= 0.03 ? (bNoRayCasts or ShadowRay(L, sample_i)) : (I_i > 0.01)
        vis = hits / N ; I = Imax
  color = LightColor/255 * I
  SmoothAndRank(L, vis, color)

SmoothAndRank(L, visTarget, color):                   // 0x82CDDE70
  if L has a previous visibility v0: step = clamp(|OwnerVel|*0.002, 0.2, 1)/TransitionTime * dt
                                     vis = move v0 toward visTarget by step (linear, no overshoot)
  if vis > 0:
     remember (L, vis, rand%5)
     if L.Function == null: insert into DirectLights by score = lum(color)*vis   (descending; cap TotalLightCount;
                                                                                   the displaced tail goes to Overflow)
  if L.bCastCompositeShadow: insert into CompositeShadow by score = lum(color)   // NOT multiplied by visibility
                                    (descending; cap DirectShadowLightCount = 1; the displaced tail goes to ShadowOverflow)

Lights ranked by luminance: PointLight.IntensityAt(p) = Brightness * max(0, 1 - (|p-pos|/Radius)^2)^FalloffExponent
                            DirectionalLight.IntensityAt(p) = Brightness (no distance term)

BoundaryCrossfade:                                    // 0x82CCB110
  if DirectLights is full and Overflow is non-empty:
     last = DirectLights[N-1], o = Overflow[0]
     f = (N<2) ? 1 - o.score/last.score : (last.score - o.score)/(DirectLights[N-2].score - o.score)
     DirectLights[N-1].color *= f (in the proxy) ; SH += (1-f)*last.color
  else f = 1
  Overflow lights -> SH as directional lobes

BuildCompositeShadow:                                 // 0x82CD4540
  for the (single) CompositeShadow entry S:
     fade = 1
     if S is the last entry and S.score - ShadowOverflow[0].score < 0.2: fade *= (S.score - next)/0.2
     if FadeShadowsWithLights: fade *= S.vis (smoothed visibility)
     S.shadowFactor.rgb = lerp(1, ShadowLuminanceScale(=0), fade) ; .a = 1
     if every component is within 0.05 of 1: drop S
  if none and Owner.vt+0x2E4() (TnPawnNative returns 0 -> never for WFC pawns):
     use World.DefaultShadowLight (straight down, ModShadowColor 0.5)
Proxy: SH, up to TotalLightCount direct lights (the last scaled by f), and the composite-shadow light with
       shadowFactor and a type tag: 1 = directional/other, 2 = point (Radius, FalloffExponent), 3 = spot (cones).
```

### ORIGINAL WFC BEHAVIOR (answers)
- **Candidate gathering:**
  - Full re-gather happens only on mode-1 updates: movement beyond 30 UU × detail scale, the settle after stopping, or a forced update.
  - Otherwise the known lights are re-evaluated.
  - Sky lights go to the SH ambient.
  - Lights with a LightFunction never become direct lights, but can still be composite-shadow lights.
- **Visibility requirement:**
  - **Baked lights:** only visibility from the LightsVisibilitiesVolume at the bounds origin. There are no rays, and visibility is 0 outside volumes.
  - **Unbaked lights:** N-of-M sample-point shadow rays.
  - The smoothed visibility must be > 0 to be a direct light. It is **not** required for composite-shadow ranking.
- **Weighting:**
  - Direct lights rank by Rec.601-style luminance (0.3, 0.59, 0.11) × intensity-at-origin × visibility.
  - Composite-shadow ranking uses the same luminance **without** visibility.
- **Directional vs point/spot:**
  - Directional intensity is plain Brightness, with no falloff.
  - Point uses the UE3 radial falloff above.
  - Spot is a separate type in the proxy; its IntensityAt was not traced (PARTIAL).
- **Dominant / shadow light:** exactly **one** composite-shadow light (`DirectShadowLightCount` = 1): the brightest **bCastCompositeShadow** light by unoccluded luminance at the bounds origin.
- **Priority/order:** strictly by those scores, descending. Ties keep insertion order.
- **Sample points:**
  - Used only for unbaked-light ray visibility and for the max-intensity estimate. They play no part in baked visibility.
  - Robot: 6 points. Vehicle: 5 points.
- **Partial visibility:** the fractional visibility scales the direct-light colour, after linear temporal smoothing.
- **Shadow fade:**
  - Shadow strength = fade × visibility. The fade drops linearly when the runner-up is within 0.2 luminance.
  - Shadow factor = 1 − fade (because ShadowLuminanceScale = 0).
- **Distance/radius:** only through IntensityAt (point radius and falloff). There is no other distance cutoff in the selection.
- **Character vs vehicle:**
  - The only differences are the sample count (6 vs 5).
  - Both use TotalLightCount 2, threshold 30, and transition 0.5.
  - The DefaultShadowLight fallback is disabled for TnPawnNative (vt+0x2E4 returns 0).
- **Refresh:** see GetUpdateMode/Tick above. Full updates are time-sliced through a global queue; incremental ones run immediately.
- **WFC-specific overrides:**
  - the whole DirectLightEnv system;
  - the LightsVisibilitiesVolume;
  - Beast SH probes;
  - the composite-shadow single slot;
  - the console tunables.

### RENDERING HANDOFF
- Select the character shadow light per the CompositeShadow rules above:
  - the single brightest bCastCompositeShadow light by `lum(LightColor/255 · IntensityAt(boundsOrigin))`, ignoring visibility;
  - shadow strength = smoothed visibility × runner-up fade (0.2 luminance window);
  - shadow factor 1 − strength.
- **Direct lights:** the top 2 by lum × visibility. The 2nd is crossfaded into SH against the 3rd.
- Baked-light visibility comes from §1 at the bounds origin.
- Re-gather on 30 UU movement (× detail scale). The visibility fade rate is clamp(speed·0.002, 0.2, 1)/0.5 per second.

### EXPERIMENTAL CHECKS NOW SAFE TO PROMOTE
1. Exactly one composite-shadow light per character.
2. TotalLightCount 2 for both robot and vehicle.
3. Baked lights outside any LightsVisibilitiesVolume contribute nothing directly.
4. The point-light intensity formula.
5. Composite ranking ignores visibility.
6. Robot 6 / vehicle 5 sample points used only for unbaked-light rays.

### STILL UNKNOWN
- The body of the scene gather callback (owner vtable +0x174, light-channel/relevance filtering).
- The time-sliced queue budget (0x83833084: 0x82CD2538 / 0x82CD2658).
- Spot-light IntensityAt.
- How the render thread applies `shadowFactor` and `DynamicShadowLuminanceScale` in the shader.
- What `TickTransitions` (0x82CD3840) does between updates.


---

## 3. Follow-up: remaining items from b52dca9 (2026-10-02)

### 3.1 Scene light-gather callback and channel/relevance filtering
**CONFIDENCE:** CONFIRMED. The identities of the three light lists are HIGH.

**ADDRESSES:**
- `ULightEnvironmentComponent` vtable **0x822DEA48**:
  - +0x174 = **0x82DF5068** `GatherLights`
  - +0x178 = 0x82DD1B00 `UpdateLight` (matches the Tick call)
- Light scene query **0x82E19678**; hash-grid walk **0x82E16D78**.
- Filter **0x82CC2608** `LightAffectsEnv`.
- Level test **0x82DD11D8**; volume test **0x82DD1100**.
- Per-type `AffectsBounds` (light vtable +0x180):
  - point **0x82DD3EF0**
  - spot **0x82E2CDF8**
  - directional = volume test only (0x82DD1100)
- Shadow-ray gate **0x82CC2700**.

```
GatherLights(bounds{origin,extent,radius}, envChannels, out):        // 0x82DF5068
  scene = Owner.World.LightScene (+0x1E4)                              // 0x82E2FA40
  filter = {bounds, owner component, envChannels}
  for L in scene.list44: if LightAffectsEnv(filter,L): out.add(L)      // global list, no spatial test
  for L in scene.list38: if LightAffectsEnv(filter,L): out.add(L)      // global list, no spatial test
  HashGridQuery(bounds): integer cells floor(min*k)..floor(max*k) per axis, test grid lights   // 0x82E16D78
  for L in scene.list50 (lights outside the hash grid):
      if bounds AABB overlaps L.HashGridBBox (+0x168 min, +0x174 max) and LightAffectsEnv: out.add(L)

LightAffectsEnv(f, L):                                                // 0x82CC2608
  if !L.bEnabled (0x80000000 @ +0xFC): false
  if L.Function (+0xF8) != null and !L.bCastCompositeShadow (0x04000000): false
  ch = L.LightingChannels (+0x118)
  if ch & CompositeDynamic(0x08000000): ch = (ch & ~0x18000000) | Dynamic(0x10000000)
  if (f.envChannels & ch & 0x7FFFFFFF) == 0: false                    // must share at least one channel
  if (ch & ~f.envChannels & 0x03FFFFFF) != 0: false                   // every special channel on the light
                                                                       // (Unnamed1-6, Cinematic1-6, Gameplay1-4,
                                                                       //  Crowd, PlayerOnly, NPCOnly) must be on the env
  if L.bOnlyAffectSameAndSpecifiedLevels (0x00200000):
     if L.level != owner.level and owner.level not in L.OtherLevelsToAffect (+0x10C): false
  return L.AffectsBounds(f.bounds)                                     // vt+0x180

Point.AffectsBounds:  |center - L.pos| <= L.RadiusOfInfluence(+0x184) + bounds.radius, and VolumeTest
Spot.AffectsBounds:   point test, then a sphere-vs-cone test with the clamped outer cone (3.2)
Directional/other:    VolumeTest only
VolumeTest (only if L.bUseVolumes 0x00080000):
   false if the bounds hit any ExclusionConvexVolume (+0x148)
   true  if they hit any InclusionConvexVolume (+0x13C)
   false if inclusion volumes exist and none are hit
ShadowRay gate (0x82CC2700): a ray is traced only if L.CastShadows (0x40000000) and L.CastStaticShadows (0x20000000);
   otherwise the sample counts as visible. The trace runs from the sample point to light.pos minus 15 x direction
   (trace flags 0x1002386).
```
- **Channel bits** (MSB-first): bInitialized 0x80000000, BSP 0x40000000, Static 0x20000000, Dynamic 0x10000000, CompositeDynamic 0x08000000, Skybox 0x04000000, Unnamed_1..6 0x02000000..0x00100000, Cinematic_1..6 0x80000..0x4000, Gameplay_1..4 0x2000..0x400, Crowd 0x200, PlayerOnly 0x100, NPCOnly 0x80.
- **Where the environment's channels come from:**
  - on a full update, from the owner's primitive bounds pass (0x82DD1690);
  - on incremental updates, from the cached env+0x24.
- **Correction to the +0xFC bit map below bit 26:** the code's usage pins `0x00200000` = bOnlyAffectSameAndSpecifiedLevels and `0x00080000` = bUseVolumes. Bits 31..26, used in §2, are unchanged.

### 3.2 Spot-light intensity and falloff
**CONFIDENCE:** CONFIRMED. Spot vtable 0x822E8960; `IntensityAt` (+0x194) is **0x82E2CFE0**.
```
inner = clamp(InnerConeAngle(+0x1E0), 0, 89) deg -> rad
outer = clamp(OuterConeAngle(+0x1E4) deg -> rad, inner + 0.001, 1.5543429 rad)
cosI = cos(inner) ; cosO = cos(outer)
axis = spot direction (WorldToLight elements +0x58/+0x68/+0x78)
d = normalize(P - L.pos)
cone = clamp((dot(axis, d) - cosO) / (cosI - cosO), 0, 1)
IntensityAt(P) = PointIntensity(P) * cone^2
   PointIntensity = Brightness * max(0, 1 - (|P-pos|/Radius)^2)^FalloffExponent
```
- The sphere-vs-cone relevance test (0x82E2CDF8) uses the same clamped outer cone.

### 3.3 Time-sliced light-environment update queue
**CONFIDENCE:** CONFIRMED.
- **Queue:** global TArray at **0x83833084**. Entries are 0x14 bytes: {component, accumulatedDt, mode, deadlineFrame (u64)}.
- **Enqueue (0x82CD2538):**
  - If the component is already queued: add dt to its entry, and if the entry's mode was 2, set it to the new mode.
  - Otherwise append {comp, dt, mode, GFrameCounter + 2}.
- **Dequeue/cancel (0x82CD2658):** removes the entry and returns its accumulated dt.
  - Callers use it on immediate updates and on light attach, detach or toggle.
  - Those callers also set ForceNextUpdateTime = 0.001.
- **Per-frame service (0x82CDD438, called through 0x82DBF0E0 from 0x82D2C708):**
  1. `0x82CD26F8`: every entry with deadline ≤ the current frame → `UpdateLight(accumDt, mode)` and removal. **No budget applies to these.**
  2. `0x82CD2798`: the remaining entries in FIFO order, updated and removed until wall time since the service started reaches the **budget**; it stops at the first entry over budget.
- **Budget values passed to 0x82D2C708:**
  - **0.002 s (2 ms)** from the main loop (0x826ED270), only when frame time remains above 0.002 s;
  - 0.001 s from 0x82DC5A48 (a wait loop);
  - 0.0 from 0x826F45C8 (deadline flush only).
- **Net effect:** a full re-gather is delayed by at most 2 frames, and runs sooner when the idle budget allows.
- **First update after attach (0x82DBEF90):**
  - ForceNextUpdateTime = 0.001 if the owner rendered within the last 1 s, or if forced;
  - otherwise rand()·(1/32767)·[1, 1.5, 2, 2.5][detailMode] seconds, a randomized stagger.

### 3.4 Per-tick environment transition
**CONFIDENCE:** CONFIRMED. `0x82CD3840`, called from Tick every frame.
- It does work **only** when the single composite-shadow entry is the World DefaultShadowLight:
  - fade (env+0x84) = min(1, fade + dt·**5.0**), so it reaches full strength in 0.2 s;
  - shadow factor = lerp((1,1,1,1), DefaultShadowLight.ModShadowColor (0.5,0.5,0.5,1), fade) (lerp helper 0x82B5AE50);
  - then the proxy is rebuilt.
- In every other case there is **no between-update interpolation**. Visibility smoothing (§2 SmoothAndRank) advances only inside updates, using the dt accumulated since the last update.
- Incremental updates (mode 2) run every tick whenever the env has lights, so for WFC characters the smoothing is effectively per-tick.
- WFC pawns never use DefaultShadowLight (TnPawnNative vt+0x2E4 returns 0), so this function is a no-op for them.

### 3.5 Shader-side shadow factor / DynamicShadowLuminanceScale
**CONFIDENCE:** PARTIAL.
- **0x82DDAEF0** (light-attenuation shader parameter binder) uploads:
  - a float4 `(0.5/width, 0.5/height, 0, 0)` half-texel offset of `LightAttenuationTexture`;
  - **`DynamicShadowLuminanceScale` = float4(global 0x8382DDF4, 0, 0, 0)**.
- That global defaults to 0. It is settable only via `DirectLightEnv DynamicShadowLuminanceScale <0..1>`, and no shipped config sets it.
- The composite shadow's per-light 4-float `shadowFactor` goes to the render-thread proxy (0x82DBF2C8 appends a 0x80-byte shadow record; type tag and cones as in §2).
- **STILL UNKNOWN:** the in-shader arithmetic. That needs the compiled Xenon shader microcode from the map ShaderCache (`ShaderCache_944` carries `DynamicShadowLuminanceScale`, `DirectLightAmbientContribution` and `LightColorsAndFalloffEx`).

### EXPERIMENTAL CHECKS NOW SAFE TO PROMOTE (follow-up)
- The channel rule (shared channel, plus the subset rule for special channels, with CompositeDynamic treated as Dynamic).
- Point relevance by RadiusOfInfluence.
- The spot cone² falloff with clamped cones.
- A full re-gather lands within 2 frames.
- No between-update interpolation for WFC pawns.


---

## 4. Shader bytecode: how `DynamicShadowLuminanceScale` is consumed (2026-10-02)

**CONFIDENCE:**
- CONFIRMED: decoded from shipped Xenos microcode for every shader in the MP_IAC_Streets_BASE_m ShaderCache that declares the constant.
- The instruction-format decoding follows the public Xenia ucode layout. The scalar const-op temp-register encoding was validated statistically: 98% of decoded reads hit registers written earlier, versus 61% and 32% for the alternative encodings.

### Method and provenance
- **Package:** `MP_IAC_Streets_BASE_m.xxx` (it holds the Optimus cook). The decompressed copy is kept locally and not committed.
- **Exports:** `ShaderCache_10920/13847/3907/4433/717/7389/7771/7828/8031`.
- **Shader record:** `[type FName][GUID 16][skip u32][target u16][code size u32][code]`.
- **Code blob:**
  - magic `0x102A1100`;
  - `+0x24` constant-table size, `+0x28` big-endian D3DX constant table without the `CTAB` fourcc (`ps_3_0`, creator `2.0.9328.0`);
  - literal-constant vectors (allocated downward from c255);
  - Xenos microcode: control-flow pairs, then 3-dword ALU/fetch instructions.
- **New tools (read-only):**
  - `tools/xenosdis.py`: CF / ALU / fetch disassembler, plus constant-table parser.
  - `tools/xenostrace.py`: symbolic forward trace of the DSLS constant and the ShadowMask fetch through to `oC0`.

### Shaders using the constant
- **Declaration count:** 372 shader blobs declare it. **All are `ps_3_0` (pixel stage). No vertex shader reads it.**
- **Register:** **`c6`** in 351 blobs; `c5`/`c4`/`c10` in 12/6/3 blobs, depending on parameter allocation.
- **Read only through `.x`.** The CPU uploads `float4(DSLS, 0, 0, 0)` (0x82DDAEF0).
- **Readers:** every shader that reads it uses **ShadowMaskPolicy**. In two families:

| family | shader types | vertex factories incl. characters |
|---|---|---|
| **A: DirectLightEnv "uber-light" pass** | `TLightPixelShader<One/Two/ThreeLightUberLightPolicy, FShadowMaskPolicy>` | FLocal, **FGPUSkin, FGPUSkinMorph**, FGPUSkinMorphDecal, particles, terrain |
| **B: per-light shadowed pass** | `TLightPixelShader<FDirectionalLightPolicy / FSpotLightPolicy, FShadowMaskPolicy>` | FLocal, **FGPUSkin, FGPUSkinMorph**, decals, particles, terrain |

- **Declared but unread:** a handful of blobs, e.g. FShadowTexturePolicy, base-pass and velocity variants.

### Register-level provenance (family A, `TLightPixelShader<OneLightUberLightPolicy,FShadowMaskPolicy>`, blob `0x1C75F2C`)
- **Constant table:**
  - `DynamicShadowLuminanceScale` c6
  - `DirectLightAmbientContribution` c38
  - `AmbientCubeIrradiance` c32..c37
  - `LightColorsAndFalloffExponents` c40
  - `SceneColorBiasFactor` c7
  - `ScreenPositionScaleBias` c1, `ShadowMaskTexelOffset` c5
  - `ShadowMaskTexture` = sampler tf0
- **Literals:** c251 = (2, 1, −π, 1.25), c254 = (0.11, 0.3, 0.59, −1), c255 = (0.5, 1, 1, 2π).

```
 13 ADDv    r5.zw  = c5.xy + c1.wz                 ; shadow-mask texel offset + screen bias
 15 MULADDv r2.xy  = (1/r2.w)*c1.xy * r2.xy + r5.zw ; screen UV
 16 tfetch  r11.z  = tf0(r2.xy).x                  ; ShadowMaskTexture.x
 22 ADDv    r8.w   = -c6.x + c255.y                ; 1 - DSLS
 43 ADDv    r16.z  = -r11.z + c255.y               ; 1 - mask
 57 MULv    r0.x   = r16.z * r8.w                  ; S = (1-mask)(1-DSLS)
 77 MULv    r1.w   = r8.w * c38.x                  ; (1-DSLS)*DLAC.x
100 MAXs    PS     = r1.w                          ; (scalar, mask 0)
101 MUL_PREVs r2.x = PS * -r16.z                   ; -DLAC.x*S
102 MAXs    PS     = r0.x
103 MUL_PREVs r2.y = PS * -c38.y                   ; -DLAC.y*S
105 MAXs    PS     = r0.x
106 MUL_PREVs r2.z = PS * -c38.z                   ; -DLAC.z*S
107 ADDv    r2.xyz = r2.xzy + c251.yyy             ; 1 - DLAC*S  (colour held in xzy order)
126-133    r4.xyz = (diffuse*NdotL + spec) * atten * c40.rgb      ; direct light
 89-94,120 r5.xyz = AmbientCube(N; c32..c37) * diffuse            ; ambient / SH irradiance
140 SUB_CONST_0 r3.w = c255.y - r0.x               ; 1 - S
143 MULADDv r3.xyz = r5 * r2 + r3                  ; + ambient*(1 - DLAC*S)
144 MULADDv r3.xyz = r4 * r3.w + r3                ; + direct*(1 - S)
145 MULv    oC0.xyz = r3 * c7.x                    ; * SceneColorBiasFactor
```

- **Two-light character variant** (`TwoLightUberLightPolicy`, FGPUSkinMorphVertexFactory, blob `0x1C6898C`):
  - It is identical, except that `1 − DSLS` is formed through `ADD_PREVs` and DLAC is in c40.
  - The direct term is the **sum of both lights**: `r4 = light0·c43.rgb + light1·c44.rgb` (lines 152–153), multiplied by the same `1 − S`. **One shadow mask attenuates both direct lights.**
- **Family B** (e.g. `0x1C80B9B` directional, `0x1CA0EE0` spot, skinned `0x1C8D576` / `0x1C72C1C`):

```
oC0.rgb = ( (DSLS*(1 - mask) + mask) * lightRGB * materialRGB ) * SceneColorBiasFactor     // = lightRGB*(1 - S)
```

### Mathematical expression (implementation-ready)
```
mask = ShadowMaskTexture.Sample(ScreenUV + ShadowMaskTexelOffset).x      // 0 = fully shadowed, 1 = lit
S    = (1 - mask) * (1 - DynamicShadowLuminanceScale)                     // shadow amount
Family A (DirectLightEnv uber pass, characters):
  direct  = Σ_lights (diffuse*N·L + specular) * attenuation * LightColor_i
  ambient = AmbientCubeIrradiance(N) * diffuse                            // SH / ambient-cube term
  colour  = direct * (1 - S) + ambient * (1 - DirectLightAmbientContribution.rgb * S) + other material terms
Family B (per-light shadowed pass):
  colour  = light * material * (1 - S)        // == lerp(mask, 1, DSLS)
oC0.rgb = colour * SceneColorBiasFactor.x
```

### Answers
- **Stage:** pixel only.
- **Register:** c6.x, in most blobs.
- **Operands:** only `1 − c6.x` and `c6.x·(1 − mask)`. It is always combined with the ShadowMask texture's `.x` channel and nothing else.
- **Direct light:** multiplied by `1 − S = lerp(mask, 1, DSLS)`. In uber-light shaders this is the sum of all dynamic lights.
- **Composite shadow / shadow factor:** DSLS acts on the screen-space **ShadowMaskTexture**, the projected-shadow attenuation buffer. How the composite shadow's `shadowFactor` reaches that buffer happens in the projection pass, not in these shaders.
- **Luminance:** despite the name, **no luminance computation involves DSLS**. The 0.11/0.3/0.59 dot products in these shaders belong to the material's saturation math. DSLS is a linear **shadow-strength lift**.
- **Ambient/SH:** in family A, the ambient term is darkened in shadow by `DirectLightAmbientContribution.rgb · S`, which is the share of the ambient attributed to the dominant direct light. DSLS reduces that darkening equally.
- **Character material output:** the expression above is applied before `SceneColorBiasFactor`. There is no separate clamp.
- **Value 0 (shipped):** `S = 1 − mask`. The direct light gets the full shadow (`× mask`), and the ambient is reduced by `DLAC·(1 − mask)`.
- **Nonzero values:** linear interpolation toward unshadowed. At 1, shadows vanish entirely: direct × 1 and ambient × 1.
- **Clamps:** none on DSLS in the shader. The CPU clamps it to [0, 1] in `DirectLightEnv`. The only saturates in these shaders are unrelated, such as N·L and the spot cone.
- **Colour space:** linear lighting space (HDR scene colour before SceneColorBiasFactor); there is no gamma conversion around it.
- **Scope:** **shadows only.** It does not scale total character luminance. Unshadowed pixels (`mask = 1`) are unaffected for any DSLS value.

### RENDERING HANDOFF
- With the shipped value (0), apply the screen-space shadow mask fully to the summed dynamic direct light, and darken the ambient/SH by `DirectLightAmbientContribution · (1 − mask)`.
- Implement DSLS only as `S = (1 − mask)(1 − DSLS)` with the formulas above.

### EXPERIMENTAL CHECKS NOW SAFE TO PROMOTE
- DSLS is pixel-stage only and has no effect where `mask = 1`.
- Shipped DSLS = 0 means full-strength shadows.
- Ambient darkening in shadow equals `DLAC · (1 − mask)`.
- Both dynamic lights share one shadow mask.

### STILL UNKNOWN
- How the ShadowMask buffer is produced from the composite shadow's `shadowFactor` (projection shaders, not part of this pass).
- The CPU derivation of `DirectLightAmbientContribution` (HIGH: it is the SH-ratio computed in proxy build 0x82CCE0A8).

## Addendum (2026-10-06, milestone 09): character ambient floor in shadow

Question from Rendering: "entering shadow makes the character nearly black". Is that authentic?

- **No ambient-floor properties exist (C, schema).** WFC `Engine.LightEnvironmentComponent` has only:
  - TotalLightCount, NormalizedSampleOffsets, SamplingPreset;
  - UpdateDistanceThreshold, EnvironmentTransitionTime;
  - bUpdateIfBoundsChange, bNoRayCasts, bDisallowForcedUpdates, bEnabled.
  - There is no AmbientGlow, AmbientShadowColor, bSynthesizeSHLight or Light/ShadowDistance, and no DynamicLightEnvironmentComponent class.
- **Pawn templates:**
  - `TnRobotForm.LightEnvironment0`: TotalLightCount 2, threshold 30, 6 sample offsets.
  - `TnVehicleForm.MyLightEnv`: TotalLightCount 2, threshold 30, 5 offsets.
  - Both inherit EnvironmentTransitionTime 0.5 from the CDO.
- **Ambient (SH) assembly** (`0x82CCB488`, `0x82CCB228`, C):
  - Start from zero.
  - Add the sky light upper/lower terms. This is skipped when the global `DAT_8382ddf8` ≠ 0 (U: probably a console tunable).
  - Add the Beast probe SH: RGB L2 SH, 3×9 floats (0x6C bytes).
    - Taken from every enabled `BeastLightEnvironmentVolume` whose lookup (vt+300) contains the bounds origin.
    - Only the highest `Priority` counts; volumes tied at that priority are averaged (×1/n).
    - The probe SH is zero if no volume contains the origin.
  - Overflow lights and the crossfaded 2nd light are added as directional SH (earlier).
  - **There is no minimum or floor constant.**
- **A light occluded by geometry** (smoothed visibility → 0) leaves DirectLights. Its colour is **not** moved into SH; only rank overflow goes to SH. So a fully occluded character keeps **0 % of that light**: the floor is sky + Beast probe + other lights.
- **Probe coverage on MP maps** (inventory.db):
  - With BeastLightEnvironmentVolume: Berth (1), ORB_Art (2 volumes + 2 `_LM` boxes, 1024×1024×512 spacing), UND_Complex (1), UND_Gorge (1).
  - With none: **Streets, Seed, Rust, Molten**. There, shadowed characters get only the sky light: Brightness 0.05 (Seed), 0.1 (Streets, Molten, Complex), BrokenHope 0.1, Remnant 0.2. Rust has no SkyLight component in MP packages (H: unlit ambient).
- Beast probe point data is natively serialised: it is not in authored props (U: format and location undecoded).
