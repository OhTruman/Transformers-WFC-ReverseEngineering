# Pawn render-cost rules in the original (Milestone E, 32 v 32 perf; 2026-10-07)

Labels: C = authored.db / script / prior native notes (M03 light-vis note §3); H = high confidence; U = unknown.

## 1. Light environment (not stock DLE) (C)
- WFC has **no `DynamicLightEnvironmentComponent`** and none of its fields: InvisibleUpdateTime, MinTimeBetweenFullUpdates, bSynthesizeSHLight, LightShadowMode, ModShadowFadeoutTime, NumVolumeVisibilitySamples, bForceNonCompositeDynamicLights, bCastShadows.
- `LightEnvironmentComponent` fields: bEnabled, TotalLightCount, NormalizedSampleOffsets, UpdateDistanceThreshold, EnvironmentTransitionTime, bUpdateIfBoundsChange, bNoRayCasts, bDisallowForcedUpdates, SamplingPreset.
- **Per owner:**
  - Robot form `LightEnvironment0`: TotalLightCount 2, threshold 30, 6 samples, transition 0.5.
  - Vehicle `MyLightEnv`: 2 / 30 / 5 samples.
  - Weapon mesh and pickups: CDO defaults (threshold 50 per Engine CDO, 1 sample, TotalLightCount 1); TnWeaponMesh.MyLightEnvironment is unmodified.
  - Kamikaze mine: bNoRayCasts, threshold 100.
- **Update rule** (`GetUpdateMode` 0x82DD17C8; M03 §3):
  - hidden → none;
  - moved more than T = DetailScale [1, 2, 3, 5] × UpdateDistanceThreshold → FULL re-gather. **If not rendered for > 0.1 s the move threshold² is ×100**, i.e. 10× the distance; this is the "invisible" throttle;
  - one settle update after stopping;
  - else INCREMENTAL (re-evaluate known lights) every tick when it has lights.
- FULL updates go through a global time-sliced queue: due entries (deadline frame + 2) always run; the others FIFO within a **2 ms** per-frame budget.
- Between updates the per-light visibility is smoothed linearly at clamp(|v|·0.002, 0.2, 1) / 0.5 per second (EnvironmentTransitionTime 0.5).
- Shadow rays per light: N = round(15·√lum + 0.5), clamped to the sample count, with a stagger slot mod 5. Baked lights use the LightsVisibilitiesVolume (no rays).

## 2. Visibility / distance / LOD (C)
- **Every skeletal mesh in WFC has exactly one LOD** (all 399: TR characters 207, TPRO 65, WEP 64, …). **Bots / players never drop to lower LODs at distance.** `LODInfo[0]`: DisplayFactor 0, hysteresis 0.02, shadow casting on.
- **No cull distances on pawn / vehicle / weapon components:** the CDOs set no CachedMaxDrawDistance / CullDistance / MinDrawDistance (0 = unlimited). Cull distances exist only on level static meshes (e.g. 19000 / 40000 / 60000 in campaign maps); MP map placements author none.
- Robot `RobotMeshComponent0` and `VehicleMesh`: **`bUpdateSkelWhenNotRendered` = true** (bones update even when not rendered); robot also `bAlwaysTickFaceFX`; `LightingChannels.PlayerOnly`.
- **Character shadows:** one composite-shadow projector per light environment, with **no distance or resolution fade** in shadow creation (FadeAlpha 1.0; M03 shadow runtime note). The only fades are the 0.2-luminance runner-up window and light visibility. Pickup meshes: CastShadow false.
- **Occlusion:** `PrimitiveComponent` CDO `bAllowApproximateOcclusion` true and `bAllowCullDistanceVolume` true. No pawn component disables them.
  - H: stock UE3 hardware occlusion queries apply to pawns like any primitive. `bUseAsOccluder` defaults false.

## 4. LastRenderTime write site (native, 2026-10-07)
- **Writer `0x82ECE818`** (batched 3 at a time from `0x82ED3F60`, the last step of the scene render `0x82ED4820`, after InitViews `0x82EC2100` and all draw passes `0x82ED32B8`). For each primitive index, from the view's visibility bitmap (view +0x4E4 / +0x4F4 data, +0x4F8 count):
  - `if (SceneInfo.LastVisibleFrame (+0xA8) < GFrame − 1) SceneInfo.LastVisibilityChangeTime (+0xAC) = CurrentWorldTime`; then `+0xA8 = GFrame`;
  - **`Component.LastRenderTime (+0x18C) = CurrentWorldTime`**;
  - **`if (Owner) Owner.LastRenderTime (+0xA4) = CurrentWorldTime`** (the field the light-env `GetUpdateMode` reads: owner +0xA4 vs now, > 0.1 s).
- C: it is written only for primitives set in the view's visibility bitmap, the same bitmap the draw passes iterate (readers in `0x82EAE088`, `0x82ECC9E0`, `0x82EFA510`, `0x82EFBAD8`, `0x83038EC8`), at end of frame. **Frustum alone does not set it.**
- H: occlusion-culled primitives are cleared from that bitmap during InitViews (stock UE3; the bit-clear site was not isolated), so a pawn hidden behind a wall stops updating LastRenderTime.
- **U → H (stock): query results not ready** are treated as visible (UE3 reads the previous frame's query; unavailable → visible). WFC's buffering depth was not traced.
