# MILESTONE 03 — Runtime semantics for AssetTools checkpoint 7a69756

Pass date: 2026-10-02. Inputs:
- `AssetTools/docs/EVIDENCE_M03.md` and the M03 manifests, read-only.
- Script bytecode decompiled with `tools/ue3dis.py` (`work/script/decomp`).
- Read-only Ghidra queries via `tools/wfcq.ps1`.

Bool bitfields are MSB-first (verified in earlier passes).

> **Correction to AssetTools §2:** `TnPickupFactory.SetPickupVisible / SetPickupHidden / IsReadyToPickup / GiveTo / TakePickUp / GetRespawnTime` **do have bytecode**. They are not native stubs; the decompiled bodies are quoted below.

---

## P1. Vehicle audio loop enable / FSB-XMA runtime

**CONFIDENCE:**
- CONFIRMED: the per-wave loop flag, the FMOD mode, the absence of loop-point code, the stop/fade path and the state switching.
- HIGH: whole-sample looping. FMOD uses the FSB `loopstart = 0` / `loopend = N−1` header; WFC never overrides it.

**ADDRESS:**
- `0x82788768`: SoundNodeWaveEvent → wave instance.
- `0x8276C1E0`: wave-instance init.
- `0x82768820`: FMOD channel create.
- `0x82742D08`: per-tick FMOD voice update.
- `0x82E770E0` / `0x82E76698`: `UAudioComponent::FadeIn` / `FadeOut` (execs `0x82C5D420` / `0x82C5D500`).
- `0x82E764D0`: immediate stop.

**FUNCTION / PROPOSED NAME:** `USoundNodeWaveEvent::ParseNodes`, `FWaveInstance::Init`, `FFmodSoundSource::Init`, `FFmodSoundSource::Update`.

**CALLERS / CALLEES:**
- AudioComponent update (`0x827881D8`) → the cue node graph → `0x82788768` → `0x8276C1E0`.
- The device then creates the FMOD voice (`0x82768820`) and updates it every frame (`0x82742D08`).

**CONSTANTS:**
- SoundNodeWaveEvent bools at node+0x34:

| bit | flag |
|---|---|
| 0x80000000 | **bLooping** |
| 0x40000000 | OverrideSpatialization |
| 0x20000000 | OverridePriority |
| 0x10000000 | PlayWhenSilent |

- FMOD modes:

| value | mode |
|---|---|
| 1 | LOOP_OFF |
| 2 | LOOP_NORMAL |
| 8 | FMOD_2D |
| 0x10 | FMOD_3D |

- Start offset: playback time × 1000 is passed to `setPosition` with timeunit MS.
- Channel priority: `int(255 − clamp(Priority, −1, 255))`.
- Pitch is clamped to [0.125, 8] × the base frequency.

**PSEUDOCODE:**
```
WaveEvent.ParseNodes(AC, playbackTime):                                     // 0x82788768
  if !(node.bLooping) and playbackTime >= wave.Duration (+0x34): skip         // one-shots are not restarted past their end
  wave.bUseSpatialization = (spatialType != k2D) ; wave.bSmartPan = type in {2,3}
  wave.LoopMode = node.bLooping ? 2 : 0                                       // wave+0x14
  wave.StartMs  = (int)(playbackTime * 1000)                                  // resume offset
  wave.Priority = node.OverridePriority ? node.Priority : root.Priority
CreateChannel(wave):                                                        // 0x82768820
  if wave.StartMs > 0 and StartMs >= sound.getLength(ms): return no-play
  playSound(paused) ; mode = (3D?0x10:0x08) | (wave.LoopMode==2 ? LOOP_NORMAL : LOOP_OFF) ; setMode(mode)
  setSpeakerMix(6 authored dB → linear) ; if StartMs: setPosition(StartMs, MS)
  // NO setLoopPoints / setLoopCount call: FMOD uses the FSB header loop region and its default loop count (infinite)
Update(wave): set3DAttributes, setFrequency(clamp(pitch,0.125,8)*base), setVolume(clamp(vol,0,1)),
              setPriority(int(255-clamp(prio,-1,255))), SmartPan pan level, doppler level
```

**ORIGINAL WFC BEHAVIOR:**
- **What loops:** looping is a **per-wave** flag, `SoundNodeWaveEvent.bLooping`. It becomes **FMOD_LOOP_NORMAL on that wave's channel**. The cue root and its `LoopStart` / `LoopEnd` are not involved.
- **Loop region:** FMOD's default region for the sample, which in the FSB4 header is `0 … N−1`. So **the whole decoded XMA sample loops**. No WFC code alters loop points, and nothing parsed here reads XMA seek or tail data.
- **Loop count:** never set (FMOD default, infinite).
- **Intro → loop → outro:** these are **separate cues on separate AudioComponents**, driven by script state machines.
  - `HmVehicleAudioComponent`:
    - `PlayBoostSound` = `PlayLoopingSound(_BoostAudioComponent, BoostSound, BoostFadeInTime)`, plus BoostWheels when on the ground.
    - `StopBoostSound` = `StopLoopingSound(…, BoostFadeOutTime)` on both components, then a one-shot `PlaySoundEvent(BoostStopSound)`.
  - `HmPlayerVehicleAudioComponentImpl` engine states:
    - **States:** `Boosting`, `JumpReving`, `ForwardOnLoad/OffLoad`, `ReverseOnLoad/OffLoad`.
    - **Per-tick selection** (`UpdateEngineSound`): boosting > jump-rev > direction/load.
    - **BeginState:** starts that state's loops with `EngineFadeInTime` (`BoostFadeInTime` for boost). It fires the one-shots only if `EngineOneshotSpazTimer ≤ 0` and the previous state was not Boosting/JumpReving; the timer resets to `EngineOneshotSpazTime`.
    - **EndState:** stops that state's loops with `EngineFadeOutTime` (`BoostFadeOutTime` for boost).
- **State change:** an overlapped **crossfade** between the old state's components (fading out) and the new state's (fading in). `PlayLoopingSound` doesn't restart a component already playing the same cue.
- **Stop:** `StopLoopingSound` sets `bAutoDestroy` and calls `FadeOut(time, 0)`.
  - **FadeOut** (`0x82E76698`): if the component is playing and not finished, and time > 0, record `[start = PlaybackTime, stop = PlaybackTime + time, target 0]` and stop when reached. Otherwise stop immediately.
  - **FadeIn** (`0x82E770E0`): `[0 → time]`, then Play.
  - The wave keeps looping during the fade. **The stop does not wait for a loop boundary.**
  - Optimus values: EngineFadeOutTime **0.2**, BoostFadeOutTime **0.15**, EngineFadeInTime / BoostFadeInTime **0.1**.

**CURRENT REBUILD IMPACT:**
- Loop whole samples for waves whose WaveEvent has `bLooping`.
- Do not use the root LoopStart/LoopEnd.
- Crossfade components on state changes.

**HANDOFF TARGET:** Systems (audio).

---

## P2. Pickup factory runtime state machine

**CONFIDENCE:** CONFIRMED (script bytecode + authored defaults).

**ADDRESS:**
- `Engine.PickupFactory`: states `Pickup`, `Sleeping`, `Disabled`, `WaitingForMatch`.
- `TransGame.TnPickupFactory` and `TnHealthPickupFactory`, in `work/script/decomp`.

**FUNCTION / PROPOSED NAME:**
- `PreBeginPlay → InitializePickup → SetPickupMesh`
- `SetInitialState`
- `Pickup.Touch → ValidTouch → GiveTo → PickedUpBy → SetRespawn → StartSleeping`
- `Sleeping` latent code
- `SetPickupHidden` / `SetPickupVisible`
- `ReplicatedEvent('bPickupHidden')`

**CONSTANTS:**
- RespawnTime: ammo 30, health 60, overshield 120.
- `RespawnEffectTime` = 0 (unset).
- `ShouldDisplayHighlightFx` = **True only on `TnAmmoCratePickupFactory`**; the base and the health/overshield factories are False. No Streets placement overrides it.
- `PickupRotationRate` (ammo) Yaw 10000.
- Base defaults: RemoteRole SimulatedProxy, bAlwaysRelevant, NetUpdateFrequency 1.

**PSEUDOCODE:**
```
PreBeginPlay: InitializePickup(): (server) bPickupHidden = bHidden; SetPickupMesh() → attach mesh; bPickupHidden ? SetPickupHidden() : SetPickupVisible()
SetInitialState: no InventoryType → 'Disabled'; bIsSuperItem (InventoryType.bDelayedSpawn) → 'WaitingForMatch'; else auto state 'Pickup'
state Pickup:
  BeginState: (server) SeqEvent_PickupStatusChange(0 = available); RotationRate = Inventory.PickupRotationRate; SetPhysics(PHYS_Rotating)
  latent: CheckTouching()                              // pick up anyone already standing in it
  Touch(P): if Inventory.PickupWhenTouched(P) && ValidTouch(P): GiveTo(P)
  ValidTouch: !bHidden, P.bCanPickupInventory, P.Controller (else retry in 0.2 s), FastTrace line of sight (else retry 0.5 s),
              Game.PickupQuery(P, InventoryType, self); TnPickupFactory adds: AiUseOnly → reject non-AI
  EndState: SetPhysics(PHYS_None)
GiveTo(P) [Tn]: SpawnCopyFor(P) (Inventory.GiveTo + AnnouncePickup → P.PlaySound(PickupSound)); PickedUpBy(P); TnGame.PickedUp(P, self, type)
PickedUpBy(P): SetRespawn(); SeqEvent_PickupStatusChange(1 = taken)
SetRespawn: if GetRespawnTime() != 0 and Game.ShouldRespawn(self): StartSleeping() → 'Sleeping' else 'Disabled'
state Sleeping:
  BeginState: SetPickupHidden()                        // immediately on pickup
  Touch: ignored
  latent: Sleep(RespawnTime - RespawnEffectTime); RespawnEffect() (empty); Sleep(RespawnEffectTime)
          if ShouldRespawn() (= !bHidden): GotoState('Pickup') else loop
  EndState: SetPickupVisible()
state Disabled: SetHidden(true); SetCollision(false,false)
SetPickupHidden [base]: bForceNetUpdate; bPickupHidden = true; PickupMesh.SetHidden(true)
  [Tn]: CustomPickupEffect.SetHidden(true); CustomPickupEffect.DeactivateSystem(); if ShouldDisplayHighlightFx: PickupEffect.DeactivateSystem()
SetPickupVisible [base]: bForceNetUpdate; bPickupHidden = false; PickupMesh.SetHidden(false)
  [Tn]: CustomPickupEffect.SetHidden(false); CustomPickupEffect.ActivateSystem(); if ShouldDisplayHighlightFx: PickupEffect.ActivateSystem()
  [Health]: then CheckTouching()                       // instant re-grab if someone is standing on it at respawn
Client: ReplicatedEvent('bPickupHidden') → SetPickupHidden()/SetPickupVisible()   // same effect toggles on clients
```

**ORIGINAL WFC BEHAVIOR:**
- **Initial state:** available (`Pickup`), visible, with effects active. The rotating physics (ammo crate yaw 10000) applies only in `Pickup`.
- **On pickup:** the **same frame** enters `Sleeping`:
  - the mesh is hidden;
  - the custom FX (energon cube / overshield) is hidden and deactivated;
  - the highlight beam is deactivated.
- **Collision is NOT disabled** while sleeping; touches are simply ignored. Collision is disabled only in `Disabled`.
- **Respawn:** the timer starts at pickup and lasts exactly `RespawnTime`. On expiry the factory returns to `Pickup` and becomes visible: mesh shown, custom FX shown and activated, beam re-activated.
  - There is no respawn effect or sound.
  - The pickup sound is played on the **picker pawn**: ammo `HEALTH_PU_AMMO`, health `HEALTH_PU_ENERGON`, overshield `OVERSHIELD_POWER_UP`.
- **Effects** do not persist while unavailable; both systems are deactivated.
- **Factory actor:** stays alive and is never destroyed.
- **Replication:** availability replicates through the replicated `bPickupHidden` (bForceNetUpdate on change). Clients mirror the visuals via `ReplicatedEvent`. The authority alone runs the state machine.

**CURRENT REBUILD IMPACT:**
- Keep collision on while sleeping.
- Use a single exact `RespawnTime` delay.
- Re-check touching pawns on respawn (health factory).

**HANDOFF TARGET:** Gameplay (state machine), Systems (replication / sound), Rendering (visibility).

### Pickup beam (what activates it)
- **The beam is `TnPickupFactory.PickupEffect` (`FX_Pickups_p.FX.Pickup_FX`).**
- It is activated **only** by `TnPickupFactory.SetPickupVisible` → `PickupEffect.ActivateSystem()`, gated by `ShouldDisplayHighlightFx`.
- It is deactivated by `SetPickupHidden` → `PickupEffect.DeactivateSystem()`.
- `ShouldDisplayHighlightFx` is True only for **ammo-crate (weapon) factories**. **Health and overshield factories never activate the beam**, which matches their unattached PickupEffect copies.
- The flag and bomb objective factories inherit False, so no beam there either.
- `bAutoActivate = false` in the template is irrelevant, because the first `SetPickupVisible` in `PreBeginPlay` activates it.

---

## P3. Ion Blaster HUD / crosshair spread

**CONFIDENCE:** CONFIRMED for the script chain, values and bindings. The AS2 side was already confirmed by AssetTools.

**ADDRESS:**
- `TnHUD.Tick` → `TnHUD.CheckDataObservers`, every HUD tick.
- `TnHudDataObserverWeaponSpread.CheckData`.
- `TnHudDataObserverCurrentWeaponAndAim.CheckData/Update`.
- `TnHudDataObserverWeaponReticule.CheckData`.
- `HmWeapon.GetSpread`, `Weapon.GetSpread`, `TnPlayerPawn.GetWeaponSpreadModifier`, `TnWeaponSpreadModifier.ModifySpread/Tick`.
- `TnWeapon.GetCurrentSpreadModifier / IncrementSpread / CooldownSpread / GetFineAimSpreadModifier`.

**CONSTANTS:**
- **Observer:** `ConversionFactor = 1.0`; change threshold **0.002**.
- **Bindings (Scaleform):**
  - `_global.NotifyWeaponSpreadChanged(Number)`
  - `_global.NotifyCurrentWeaponChanged(String className)`
  - `_global.NotifyFineAimChanged(Number 0|1)`
  - `_global.NotifyWeaponReticuleTypeChanged(Number)` (unhandled in the movie)
- **Ion Blaster MP (`IonBlaster_WEPDATA`):**
  - PerShotSpreadModifier Min **0.08**, Max **0.18**, ChangePerShot **0.005**, Cooldown **2.0** s, Start = Min (enum 0).
  - FineAimSpreadModifier **0.5**; base `Data.Spread[]` unset (0).
- **Ion Blaster SP:** Min 0.09, Max 0.19.
- **Airborne:** `TnWeaponSpreadModifier` AirborneMultiplier 2.0, ramp-up 0.25 s, land ramp-down 0.5 s, hover ramp-down 0.1 s.

**PSEUDOCODE:**
```
every HUD tick:
  spread = Weapon.Data.Spread[CurrentFireMode]                                   // 0 for Ion Blaster
         + (robot form ? ModifySpread(CurrentSpread * SkillSpreadMultiplier * BuffDecreaseWeaponSpread) : CurrentSpread*…)
  ModifySpread(s) = s * CurrentAirborneMultiplier * (IsUsingFineAim ? FineAimSpreadModifier : 1)
  value = 1.0 * spread ; if |value - cached| > 0.002: cached = value; Movie.Invoke("_global.NotifyWeaponSpreadChanged", [value])
  aimType = Camera.HasPlayerCameraState(TnPCS_FineAim) ? 1 : 0 ; weaponClass = Pawn.Weapon.Class
  if either changed: Invoke("_global.NotifyCurrentWeaponChanged",[className]); Invoke("_global.NotifyFineAimChanged",[aimType])
per shot: CurrentSpread = clamp(CurrentSpread + 0.005, Min, Max)                 // IncrementSpread
per tick: CurrentSpread = clamp(CurrentSpread - (Max-Min)*dt/Cooldown, Min, Max)  // CooldownSpread: full range in 2 s
```

**ORIGINAL WFC BEHAVIOR:**
- **What the HUD receives:** the **raw current spread** (ConversionFactor 1), not a normalised fraction. The AS2 maps it to the prong offset `spread × −300 px`, eased 0.2 s.
- **Fine aim** halves the spread modifier term, which is what visibly contracts the prongs. The reticle itself never changes.
- **Weapon change and fine-aim toggle** are sent together whenever either changes.
- **Update frequency:** every HUD tick, filtered by the 0.002 threshold.
- **Spin-in** on weapon change is authored AS2 animation, not code.

**CURRENT REBUILD IMPACT:**
- Feed raw spread (Ion Blaster 0.08–0.18 × airborne × fine-aim 0.5) through the 0.002 filter.
- No ADS.

**HANDOFF TARGET:** Gameplay (spread model), Rendering/UI.

---

## P4. Cue concurrency runtime (reconciled with `MILESTONE03_AUDIO_NATIVE_FIDELITY.md` P12)

**CONFIDENCE:** CONFIRMED.

**ADDRESS:**
- `USoundCue::RegisterInstanceLimiting` `0x82E767B8`, called from `UAudioComponent` Play internal `0x82E76D18`.
- Unregister `0x82E53338`; purge `0x82E498A0`; stop `0x82E766E0`.
- FMOD voice priority in `0x82742D08`.

**PSEUDOCODE:** see the earlier P12. In summary:
```
on AudioComponent.Play (cue start, before any wave is created):
  if cue.MaxConcurrentPlayCount == 0: no limit
  purge finished entries from cue.PlayingAudioComponents
  if Count >= Max:
     kKillOldest:   Stop(Playing[0])
     kKillNewest:   refuse the new play
     kKillFarthest: stop the farthest existing component whose dist² to the listener >= the new one's
                    (ties → the oldest); if none is farther, refuse the new one
  append the new component
```

**ORIGINAL WFC BEHAVIOR:**
- **Scope:** **global per SoundCue object.** The list lives on the cue; the grouping key is the cue asset. **Owner identity never participates.**
- **No priority comparison** at cue level; there is no "quietest" mode.
- **Replacement** is an immediate Stop, with no steal fade.
- **Checked at cue start** (AudioComponent Play). All waves of a cue instance share one AudioComponent, so **child waves count as one instance**.
- **Looping vehicle cues** use the same path. Each `PlayLoopingSound` creates an AudioComponent.
- **Fade-outs:** a component that is fading out still counts until it finishes.
- **Separate from instance limiting:** FMOD voice priority `255 − clamp(Priority, −1, 255)` governs hardware-voice stealing (FMOD internal).

**CURRENT REBUILD IMPACT:**
- Count per cue globally.
- Inherited `kKillFarthest` / `Max 5` apply to the vehicle engine loops.

**HANDOFF TARGET:** Systems.

---

## P5A. Mesh-emitter material fallback

**CONFIDENCE:** UNKNOWN (native).
- The selection happens in the native particle mesh renderer, which I couldn't reach cheaply from the code paths in this pass.
- Stock UE3 uses the RequiredModule material when `bOverrideMaterial`, else the mesh section material, else `DefaultMaterial`. **That has not been verified for WFC** and must not be treated as recovered.

**HANDOFF TARGET:** Rendering (keep provisional).

## P5B. Destructible initial state

**CONFIDENCE:** CONFIRMED.

**ADDRESS:** `HmDestructibleComponent.Initialize/Attached/AttachPiecesToOwner`, `HmDestructiblePiece.Reset/TransitionToState`, `HmDestructibleActorBase.PostBeginPlay`.

**PSEUDOCODE:**
```
Component.Attached: if Owner.bHidden: return; (Rebuild if needed) else AttachPiecesToOwner()
AttachPiecesToOwner: for each piece: SetBlueprint; AttachToActor(Owner); piece.Reset(0)
ActorBase.PostBeginPlay: … DestructibleComponent.Reset()  → piece.Reset(0) again
Piece.Reset(0): AccumulatedDamage = 0; TransitionToState(Blueprint.InitialStateHandle)   // Reset(≠0) → ReferenceStateHandle
TransitionToState(h): exit current; ActiveState = States[h]; CreateEffects; BeginEffects; Health = InitialHealth[h];
                      (server) if HasAutomaticTransition: SetTimer(AutoTime, 'OnTransitionTimerExpired'); observer.OnStateEnter
```

**ORIGINAL WFC BEHAVIOR:**
- `InitialStateHandle` is not authored on the WallPanelSign piece blueprint, so it defaults to **0**: the intact state, InitialHealth **20**.
- Its effects (static mesh `WallPanelSign_Base_STAT` + the hum loop cue) start at attach and again at PostBeginPlay.
- The editor-only display uses `ReferenceStateHandle` instead.

**HANDOFF TARGET:** Gameplay, Rendering.

---

## VEHICLE LOOP HANDOFF
- The loop flag is per wave (`SoundNodeWaveEvent.bLooping`) and becomes FMOD LOOP_NORMAL.
- The whole FSB sample loops (header 0…N−1); WFC sets no loop points or count.
- Intro, loop and outro are separate cues on separate components, switched by script engine states.
- State changes crossfade (fade-in 0.1, fade-out 0.2, boost fade-out 0.15).
- Stop is a linear fade from the current playback time and does not wait for a loop boundary.

## PICKUP STATE HANDOFF
- `Pickup` (visible, rotating, touchable) → on a valid touch the same frame goes to `Sleeping`.
- `Sleeping`: mesh and FX hidden, collision kept, touches ignored, for exactly `RespawnTime`; then back to `Pickup`, visible, with an immediate touch re-check for health.
- The actor stays alive; replicated via `bPickupHidden`.

## PICKUP BEAM HANDOFF
- `PickupEffect.ActivateSystem()` runs in `SetPickupVisible` and `DeactivateSystem()` in `SetPickupHidden`, only when `ShouldDisplayHighlightFx`.
- That flag is True **only for ammo-crate factories**.
- The beam is on while available and off while sleeping. Health and overshield never show it.

## HUD SPREAD HANDOFF
- `_global.NotifyWeaponSpreadChanged(rawSpread)`: rawSpread = CurrentSpread × airborne × (fine aim ? 0.5 : 1) + base (0). Sent when it changes by more than 0.002.
- Ion Blaster MP: 0.08–0.18, +0.005 per shot, full recovery in 2 s.
- `_global.NotifyFineAimChanged(0|1)` and `_global.NotifyCurrentWeaponChanged(class)` fire when either the weapon or the aim state changes.

## CONCURRENCY HANDOFF
- Global per cue asset; no owner key and no priority.
- Enforced at AudioComponent play; one instance per cue play (waves don't count separately).
- KillOldest / KillNewest / KillFarthest as earlier; replacement is an immediate stop.
- FMOD voice priority = 255 − Priority.

## PARTICLE MATERIAL FALLBACK HANDOFF
- UNKNOWN natively. Keep it provisional.

## DESTRUCTIBLE INITIAL-STATE HANDOFF
- Initial handle 0 (intact, health 20), entered on component attach via `Reset(0)` → `InitialStateHandle` (default 0).

## STILL UNKNOWN
- XMA decoder seam behaviour at the loop point (FMOD internal).
- The native particle mesh material fallback.
- The `TnGame.ShouldRespawn` / `PickupQuery` overrides were not traced.
- The overshield amount (native).

> **CORRECTION (2026-10-02, `MILESTONE04_STREETS_PICKUP_OBJECTIVE_PRESENTATION.md`):** `ShouldDisplayHighlightFx = True` is also authored on `TnWeaponPickupFactory`. The flag and bomb objective factories inherit it and show the Pickup_FX beam while available. The "ammo crates only" / "flag and bomb inherit False" statements above are wrong.
