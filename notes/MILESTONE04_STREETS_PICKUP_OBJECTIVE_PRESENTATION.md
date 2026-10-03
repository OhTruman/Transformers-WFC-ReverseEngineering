# MILESTONE 04 — Streets pickup / objective presentation evidence (2026-10-02)

Sources (read-only):
- Script bytecode (`tools/ue3dis.py`).
- `TransContent` classes, which are cooked inside `MP_IAC_Streets_BASE_m.xxx` (there is no TransContent.xxx).
- `AssetTools/manifests/authored.db`, `streets_pickup_factories.json`, `streets_pickup_fx.json` (a23c675).
- Ghidra (read-only).

## 1. Flag / bomb objective highlight effect

**CONFIDENCE:** CONFIRMED.

### Class chains
- `TransContent.TnGameObjectivePickupFactoryFlag` → `TnGameObjectiveWeaponPickupFactory` → **`TnWeaponPickupFactory`** → `TnPickupFactory` → `Engine.PickupFactory`.
- `TransContent.TnGameObjectivePickupFactoryBomb` → the same chain.

### Highlight flag
- **`ShouldDisplayHighlightFx = True` is authored on `TransGame.Default__TnWeaponPickupFactory`.** Flag and bomb inherit it; no class or placed instance overrides it.
- **My earlier statement** (`MILESTONE03_RUNTIME_SEMANTICS_ASSETTOOLS_7a69756.md` P2, "True only for ammo crates; flag/bomb inherit False") **was wrong.** I missed the TnWeaponPickupFactory default.
- The **AssetTools property value is correct.**

### Effect object
- `PickupEffect` resolves through the archetype chain to `TnPickupFactory.PickupEffect0`: Template **`FX_Pickups_p.FX.Pickup_FX`**, `bAutoActivate = false`, SecondsBeforeInactive 1.0.
- The placed Streets components override only CullDistance 300000, LightingChannels Dynamic and bAcceptsDynamicLights false:
  - Flag_3951 → PSC_4143;
  - Flag_9703 → PSC_12331;
  - Bomb_7067 → PSC_1025.
- The component is listed in `Components` (attached).

### Script that controls it
- **No class between TnPickupFactory and TransContent overrides `SetPickupVisible` / `SetPickupHidden`.**
  - TnWeaponPickupFactory has no script functions.
  - TransContent Flag defines only `Pickup.ValidTouch`, `AddObjectiveCarryTime`, `InstantiateInventory`.
  - TransContent Bomb defines only `ObjectiveHolderChanged`, `AddObjectiveCarryTime`, `GetReturnSleepTime`.
- So the beam follows exactly `TnPickupFactory.SetPickupVisible` → `PickupEffect.ActivateSystem()` and `SetPickupHidden` → `PickupEffect.DeactivateSystem()`.

### PSEUDOCODE
```
PreBeginPlay -> InitializePickup -> SetPickupMesh -> (bPickupHidden = bHidden = false) SetPickupVisible -> beam ON   // every mode
PostBeginPlay (TnGameObjectiveWeaponPickupFactory): if !Game.HasRule(RequiredGameRuleClass) InitialState = 'Disabled'
SetInitialState -> GotoState(InitialState):
   'Disabled'  : SetHidden(true); SetCollision(false,false)    // beam component stays activated but the actor is hidden; no touch
   default 'Pickup' (auto): Pickup.BeginState -> SetCurrentObjectiveHolder(self) (marker on factory) ; rotating ; touchable
CTF round start (TnGameRules_SingleFlagCTF.SetupRoundStart):
   for every TnGameObjectiveWeaponPickupFactory: ActivateIfMatchingTeam(DefendingTeam)
      DefenderTeamIndex == defending team -> GotoState('Pickup')      // visible + beam (Sleeping.EndState -> SetPickupVisible)
      else -> SetCurrentObjectiveHolder(none); GotoState('Sleeping')  // Sleeping.BeginState -> SetPickupHidden -> beam OFF
      (Disabled.ActivateIfMatchingTeam is a no-op, so the bomb factory in CTF stays Disabled)
picked up: PickedUpBy -> holder = pawn (marker moves to carrier) -> SetRespawn: RespawnTime 9999999 -> 'Sleeping' -> beam OFF, mesh hidden,
           collision kept, touches ignored (no timed respawn in practice)
returned:  Sleeping.ReturnSpawnedObjective(reason): sleep = GetReturnSleepTime(reason)
           flag: 0 -> GotoState('Pickup') immediately -> beam ON
           bomb: reason 3 -> WaitAfterScoreTime 5.0 s timer -> 'Pickup' -> beam ON ; other reasons -> immediately
```

### ORIGINAL WFC BEHAVIOR
- **Flag factory and bomb factory both show the same `Pickup_FX` highlight beam as the ammo crates** whenever they are in the `Pickup` (available) state.
- **Mode gating:**
  - flag only in CTF (SingleFlagCTF);
  - bomb only in EXT (ScoreBombingRun);
  - in other modes the factory is Disabled: hidden, no collision. The beam is technically activated but hidden with the actor.
- **CTF:** only the factory owned by the defending team is available each round. The other one sleeps with its beam off.
- **Collision and availability:** collision stays on while Sleeping (touches ignored) and is off only in Disabled.

**HANDOFF:**
- Gameplay / Rendering: treat flag and bomb exactly like the ammo crates for the beam (ActivateSystem on visible, Deactivate on hidden), plus the mode and round gating above.
- AssetTools: the authored property is the controlling value.

---

## 2. Pickup particle module flags (`streets_pickup_fx.json` compiled module stream)

**CONFIDENCE:** PARTIAL. The native consumer of the compiled stream was not located: the switch candidates found belong to the property system, not particles. What follows is data correlation plus tagged-property semantics.

### Flag-byte census over Streets pickup FX (Pickup_FX, HealthPickup_FX, OvershieldPickup_FX)

| module | flags (A,B) | in post-record index list |
|---|---|---|
| Lifetime, Size, Location, Color, Rotation, SizeMultiplyLife, ColorScaleOverLife | (1, 1) | yes (all 14 / 14 / 14 / 14 / 6 / 8 / 6) |
| MeshRotation (6), MeshRotationRate (4) | **(1, 0)** | yes |
| Color (2), ColorScaleOverLife (4), SizeMultiplyLife (6), Rotation (2), Velocity (2), LocationPrimitiveSphere (2) | **(0, 1)** | **no** |

### Interpretation
- **flagA == membership in the post-record module-index list, without exception.**
  - HIGH: the list is the module set actually executed, and flagA = 0 marks a disabled module (UE3 `bEnabled`; the class default `bEnabled = True` is overridden per instance by the artist).
  - The (0,1) modules still carry distributions, which is consistent with editor-disabled modules being cooked anyway.
  - **Presentation consequence (HIGH):** do not evaluate flagA = 0 modules (e.g. the Velocity and LocationPrimitiveSphere entries).
  - Not proven natively, hence HIGH rather than CONFIRMED.
- **flagB:** 0 only on MeshRotation and MeshRotationRate.
  - It does **not** match stock `bSpawnModule` / `bUpdateModule`. Class defaults give spawn-only for Lifetime, Color, Rotation and Velocity too, yet those have flagB = 1.
  - It does not match `bSupportsUpdateOnLODChange` either.
  - **UNKNOWN.**
  - Both flagB = 0 modules are mesh-orientation spawn modules, so it does not change sprite / colour / visibility behaviour.

### Presentation-relevant flags that are decoded (tagged properties; stock UE3 semantics, not re-traced natively)
- `ParticleModuleRequired.bUseLocalSpace = True` on every pickup emitter:
  - particles simulate in the component's space;
  - so the ammo beam and glows **follow the factory actor's transform**, including the Pickup-state PHYS_Rotating yaw (ammo crate PickupRotationRate Yaw 10000).
  - HIGH.
- `ScreenAlignment = PSA_Rectangle` on the `GlowMut` sprite emitters (camera-facing rectangle using X/Y size); others use the default PSA_Square. HIGH.
- `BurstList [{Count 1, Time 0}]` on HealthPickup_FX `GlowADD` and its mesh emitter: a single particle bursts at emitter start. Lifetime and loop behaviour are per the decoded Lifetime / SpawnRate. HIGH.
- **Pickup_FX beam:**
  - SpawnRate 2/s, Lifetime 3.0 s, PeakActiveParticles 1 (LOD0);
  - TypeDataMesh `LightBeam_WepPickup_STAT`, **bOverrideMaterial unset (false)**, so the mesh's own material is used (stock). The RequiredModule material `LightVolume_WepPickup_MAT` applies only if overridden.
  - Health/overshield mesh emitters have `bOverrideMaterial = True`. The native fallback when RequiredModule.Material is unset is **UNKNOWN** (it was already UNKNOWN in the 7a69756 note).
- **Spawn/update gating:** `bAutoActivate = false` on PickupEffect, and activation comes from script (item 1).
  - Health/overshield `CustomPickupEffect` auto-activates and is shown/hidden by `TnPickupFactory.SetPickupVisible` / `SetPickupHidden` (`SetHidden` + Activate / DeactivateSystem).
  - `SecondsBeforeInactive = 1.0` on PickupEffect0: a stock component tick-skip when not rendered.

**HANDOFF (Rendering):**
- Skip flagA = 0 modules (HIGH).
- Treat flagB as UNKNOWN and do not gate on it.
- bUseLocalSpace, PSA_Rectangle, BurstList and bOverrideMaterial semantics as above.

---

## 3. Audio edge cases

**NOT REACHED.** Neither question (equal-priority FMOD voice stealing; listener creation vs. first ambient emitter start) lies on the pickup/objective paths traced here. Left UNKNOWN for Systems, per scope.

---

## RENDERING HANDOFF
- **CONFIRMED:**
  - flag and bomb factories show `Pickup_FX` (the same beam as ammo) while available;
  - beam ON at `SetPickupVisible`, OFF at `SetPickupHidden`;
  - Disabled factories (wrong mode) are hidden with no collision.
- **HIGH:**
  - flagA = 0 modules are disabled: don't simulate them;
  - pickup emitters are local-space, so they follow the actor's rotation;
  - GlowMut uses PSA_Rectangle;
  - Health GlowADD and the mesh emitter use a single burst at t = 0.
- **UNKNOWN:**
  - flagB meaning (mesh-rotation modules only);
  - the native mesh-material fallback with bOverrideMaterial and no RequiredModule material.

## SYSTEMS HANDOFF
- Flag/bomb pickups make no beam-related sound; pickup sounds are per the inventory (earlier note).
- The audio edge cases were not reached (UNKNOWN).

## ASSETTOOLS CORRECTIONS
- **None needed on the highlight flag.** AssetTools' `ShouldDisplayHighlightFx = True` inherited from TnWeaponPickupFactory is right. The disagreement came from my earlier RE note, which is corrected here.
- **Still standing from the earlier pass:** the "native stubs (no bytecode)" note on `TnPickupFactory.SetPickupVisible / SetPickupHidden / …` is wrong. These are script functions, and they are what activates the beam.
- **Suggested addition:** in `streets_pickup_fx.json`, label `raw_flags[0]` as "enabled (equals membership in the post-record module list)" (HIGH) and keep `raw_flags[1]` UNKNOWN.
