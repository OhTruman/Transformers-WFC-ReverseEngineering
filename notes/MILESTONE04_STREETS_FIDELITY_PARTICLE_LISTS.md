# MP_IAC_Streets fidelity — compiled particle module lists (2026-10-03)

**Scope:** item 4 of the Streets fidelity request ("which particle modules exist / spawn / update").

**Items 1, 2, 3, 5 and 6 were not reached.** The user re-prioritized to the camera-collision pass (`MILESTONE04_CAMERA_COLLISION.md`). They remain open:
- DefaultMaterial BSP faces;
- the mirrored Arch_4096 vertex-light patch;
- the MonitorScreen materials;
- the wall-panel destruction presentation (the actor is ~139k UU off the play space);
- remaining LV / vertex-light unknowns.

## Result (CONFIRMED data structure; HIGH that the runtime iterates exactly these lists, as stock UE3 `FParticleEmitterInstance` does with `LODLevel->SpawnModules / UpdateModules`)

The ParticleLODLevel native tail carries the UE3 derived module lists explicitly:

```
records (N x {ModuleId, flagA, flagB, 5 x 0, payload offset})
u8  nSpawn  + nSpawn  module indices      = SpawnModules   (the list AssetTools calls "list_after_records")
u32 nUpdate + nUpdate module indices      = UpdateModules  (first bytes of AssetTools' raw "between_list_and_groups")
... further u32-counted lists (0 in the pickup FX) ...
u32 payload/extra size, then per-entry u32 flags (not decoded)
float group, vector group (distributions, as AssetTools decodes)
```

### Proof, across every Streets pickup and totem LOD checked (40+ LODs)
- **SpawnModules** = exactly the records with flagA = 1 **and** class default `bSpawnModule = True`.
- **UpdateModules** = exactly the records with flagA = 1 **and** class default `bUpdateModule = True`.
  - Example: `SizeScale` (bUpdateModule only) appears only in UpdateModules.
  - Example: `ColorScaleOverLife` / `SizeMultiplyLife` (both flags) appear in both lists when flagA = 1.
- A record with **flagA = 0 appears in neither list.** **flagA = bEnabled.**
- flagB (0 only on MeshRotation / MeshRotationRate) does not affect list membership. It stays **UNKNOWN** and is **irrelevant to execution**.

## RENDERING HANDOFF (implementable now)
Execute exactly the modules in each LOD's SpawnModules at spawn and UpdateModules per tick. Ignore modules in neither list. For the emitters currently withheld:

| system / emitter | SpawnModules | UpdateModules | not executed (disabled) |
|---|---|---|---|
| **Pickup_FX** beam (emitter_14185) | Lifetime, Size, Color, ColorScaleOverLife, MeshRotation, Location | ColorScaleOverLife | LocationPrimitiveSphere, **SizeMultiplyLife**, Velocity |
| HealthPickup_FX glow (emitter_10406) | Lifetime, Size, Color, SizeMultiplyLife, Location, Rotation, ColorScaleOverLife | SizeMultiplyLife, ColorScaleOverLife | — |
| HealthPickup_FX mesh (emitter_14185) | Lifetime, Size, Color, MeshRotation, Location, MeshRotationRate | — | SizeMultiplyLife |
| HealthPickup_FX GlowADD (emitter_8423) | Lifetime, Size, Color (first), SizeMultiplyLife, Location | SizeMultiplyLife | Color (second), Rotation, **ColorScaleOverLife** |
| OvershieldPickup_FX glow (emitter_10406) | as the health glow | SizeMultiplyLife, ColorScaleOverLife | — |
| OvershieldPickup_FX mesh (emitter_14185) | Lifetime, Size, Color, Location, MeshRotation, MeshRotationRate | — | **SizeMultiplyLife** |
| OvershieldPickup_FX GlowADD (emitter_8423) | Lifetime, Size, Color, SizeMultiplyLife, Location, Rotation | SizeMultiplyLife | **ColorScaleOverLife** |

The ammo highlight beam, both GlowADDs and the overshield mesh can now be drawn: the flag ambiguity that blocked them is resolved.

## ASSETTOOLS CORRECTION
- In `pstream.py`, label `list_after_records` as **SpawnModules**.
- Decode the u32-counted list that follows as **UpdateModules**.
- Label `raw_flags[0]` as **bEnabled**. `raw_flags[1]` stays unknown (no execution effect).
