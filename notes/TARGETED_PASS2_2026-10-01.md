# WFC targeted pass 2 — 2026-10-01 (post-AssetTools authored pass)

Builds on:
- `TARGETED_PASS_2026-10-01.md` (transform, boost, fine aim, input, cadence, weapon restore)
- `STEPUP_LEDGE_2026-10-01.md` (native walking/falling)
- `NETWORK_ARCHITECTURE_2026-10-01.md`

Where pass 1 already gave full pseudocode it is summarised here, not repeated.

Evidence classes:
- **NATIVE**: PPC in default.xex, read with headless Ghidra on the read-only snapshot. ReVa was still down.
- **SCRIPT**: compiled UnrealScript bytecode in TransGame.xxx etc., decompiled by `tools/ue3dis.py`. This is compiled code shipped in the game, not authored data.
- **AUTHORED**: AssetTools `authored.db`, read in place.

Labels: CONFIRMED / HIGH / INFERRED / UNKNOWN.

> Key framing for every agent: almost all of the gameplay logic asked about here is compiled UnrealScript. "Native constants" for vehicles, nitro and dashes are **float literals inside script getter functions**, so AssetTools' property dump cannot see them. See §2.4.

---

## 1. Transformation momentum and input (CONFIRMED SCRIPT; physics hook CONFIRMED NATIVE)

| question | R→V | V→R |
|---|---|---|
| velocity preserved | yes | yes (local player) |
| scaled | `ClampLength(Velocity, 3500)` | ×0.1 **only** for non-locally-controlled pawns (`MotionIsKeyframed`) |
| projected/reoriented | no; the world-space vector is written straight into the RB (`SetLinearVelocity`) | no; pawn velocity is taken from the RB state |
| physics switch | `SetCollisionMode(4)` → PhysicalVehicleMesh → `SetPhysics(PHYS_RigidBody)` at t=0 | `SetCollisionMode(1)` → hybrid cylinder → `SetPhysics(PHYS_Falling)` at t=0, then `AcrobaticsManager.Fall()` |
| acceleration | hover acceleration × `(1 − DriftRemaining/0.5)²` (Drift() on hover entry) × `(up.Z)²` | `TnPawn.CalcVelocity`: MaxAccel = AccelRate/(1+P) with **InAir** momentum params while `IsTransforming` or falling, but only when above MaxSpeed |
| input during transform | **accepted from frame 0**: PC state flips to PlayerInCarForm at DoTransform; hover sim runs (TnPawn.Transforming.OnUpdate ticks both forms) | **accepted from frame 0**: PC flips to PlayerWalking; robot CalcVelocity runs |
| input lock | only a second transform is refused (`StartTransform`: IsTransforming → false); weapon switching blocked (`PreWeaponSwitch`) | same |
| handoff | target form `Activate()` and physics swap at **t=0**; source `Deactivate()` and target `BeginPlay()` at **t=Duration** (min(src,dst clip)/Rate) | same |
| heading | vehicle RB rotation = Pawn.Rotation (robot yaw, i.e. camera yaw) via `SetRBRotation`; `TnCarForm.OnTeleport` sets InputState.ViewRotation = Pawn.Rotation; the hover then yaw-tracks the camera every step | robot faces controller yaw every frame (`InRobotForm.FaceRotation`) |

Optimus momentum table (TruckTransformerMomentum, AccelRate 12000). MaxAccel when over speed:
- OnGround: fwd 1500 / neutral 3000 / back 6000
- InAir: fwd 118.8 / neutral 118.8 / back 2000

**How `CalculateMomentumPreservation` is actually used** (CONFIRMED):
- It is called from `TnPawn.CalcVelocity` only, and only matters when |flat velocity| ≥ MaxSpeed + 0.1.
- That happens after vehicle→robot (vehicle speeds up to 3000 vs robot 1400) or after knock-backs and launches.
- The stick direction relative to velocity picks the column: dot > 0.866 → Forward, no input → Neutral, else Backward.
- The native hook `AHmPawn::CalcVelocity` (0x8275C240) dispatches to this script event unless root motion is active. MaxSpeed passed in = GroundSpeed×modifier when walking, AirSpeed (1200) when falling.

Addresses (script): `TnPawn.Transforming.BeginTransformation`, `TnTransformation.Execute/Update/OnTransformationComplete`, `TnVehicleForm.OnActivate/OnEndPlay`, `TnRobotForm.OnActivate`, `TnCarForm.OnActivate` → `Hovering.BeginState` → `TnHoverCarSimulation.Drift`, `TnPawn.CalcVelocity/CalculateMomentumPreservation/CalculateMaxAcceleration`.
Native: CalcVelocity hook 0x8275C240, native fallback 0x82F701C0, physFalling 0x82F71D88, physWalking 0x82F9C598.

## 2. Boost vs Hover Dash vs Ram/Nitro (CONFIRMED SCRIPT + AUTHORED)

Inputs (Xe-TransInput.ini, CONFIRMED):
- **LT** = `FineAim | Boost` (held; `StartBoost` / OnRelease `StopBoost`)
- **RB** = `Ability0 | VehicleSpecialMove` (`StartVehicleSpecialMove` / OnRelease `StopVehicleSpecialMove`). In car form this sets `InputState._Dashing`, which is cleared every update (edge-like).
- **A** = `PressJump` → `_InputState._Jumping`, also cleared every update.
- Keyboard (cooked Xenon ini): LeftShift/RightShift = `Ability0 | VehicleSpecialMove`. There is no keyboard Boost or FineAim binding.

### 2.1 Normal Boost (Hovering → Driving)
- Activation: `_Boosting` held **and** (SimulationMode==0 **or** not drifting). It can't engage during the 0.5 s hover-drift window that follows hover entry, transform start or a previous boost release.
  Holding LT through R→V starts boost as soon as the drift ends (PlayerInVehicleForm.BeginState re-issues OnStartBoost).
- Driving state: `_Boosting=true`, `CarSimulation.Activate()` (linear damping 0, JumpTimeRemaining 0).
  - Inputs: Accelerator **1.0** (always full throttle), Steering = sign(s)·s², RollControl = strafe X.
  - Truck_Physics: MaxSpeed **3000**, MaxAcceleration **2500**, Mass 2500, AngularDamping 5, RollDuration 0 (truck can't roll).
  - Forward accel (ground only) = `Lerp(2500, Drag(3000), fwdSpeed/3000) + ExtraBoost`, × BoostScale.
  - `Drag(v) = v²·|g_RB|/TerminalVelocity²` (Pawn.TerminalVelocity 6000; g_RB = 2940×0.66). Drag is also applied opposite the velocity on ground.
  - ExtraBoost: quadratic from 2500×8 = 20000 at 0 speed to 0 at 1500 UU/s, capped at **5000**. BoostScale fades to 0 between forward.Z 0.5 and 0.866 (30°–60° climbs).
  - Braking: **no brake input**. Driving has no throttle-off path: decel comes only from drag, collisions, or leaving Driving.
- Exit: release LT → `Hovering` (Hover sim Activate + **Drift()** again: 0.5 s quadratic authority ramp, velocity kept). A frontal RB hit (contactNormal·forward > **0.866**) also exits to Hovering, unless the truck's ram consumed the hit.
- Camera: CameraStrategyManager `CarFormHovering`→`CarFormDriving` on IsBoosting.
  - Optimus Hover strategy: FOV **80**, orbit **950**.
  - Driving strategy: FOV **85**, orbit **1050**.
  - Strategy TransitionTime: into Driving **1.0 s**, into Hover **1.5 s**.
- FX/sound: Driving.BeginState/UpdateFx → `PlayBoostFx` (Blueprint.BoostFx at BoostSocket_L/R) + `VehicleAudio.PlayBoostSound`. EndState → StopBoostFx + StopBoostSound.
  Boost FX colour = ColorLerp(EnergonColor, Yellow, NormalizedJumpTimeRemaining), alpha Lerp(100,255,...).

### 2.2 Hover Dash (Hovering only; RB)
- `Hovering.UpdateDashing`: if `CanUseSpecialMove()` (no cooldown running) and `_Dashing` → `DoDash()` then `StartSpecialMoveCooldown(TimeBetweenDashes = 2.0 × mod)`.
- Truck override `TnTruckForm.Hovering.DoDash`: `HoverSimulation.Dash((1,0,0))`, **forward only**, then `PlayBoosterSound`. Car base: dash along the dominant stick axis.
- `TnHoverCarSimulation.Dash`: refused if unstable (|pitch| or |roll| > 30°). DashTimeRemaining = DashDuration (HoverTruck_Physics **0.5 s**). Default 0.3 belongs to other blueprints.
- `UpdateDash`: while remaining > 0 target speed = DashSpeed (**3000**) with accel limit 100000; afterwards target MaxLinearSpeed (1500) with decel limit 100000. All axes, local frame. An unstable state cancels it.
- The cooldown starts **at activation**. HUD ability slot 2 shows it (`SetAbilityResource(2, Duration, 0)`) and is set ready when it expires.

### 2.3 Truck Nitro / Ram (Driving only; RB)
- `TnTruckForm.Driving.UpdateNitro`: if `_Dashing` and not already in nitro and `CanUseSpecialMove()` → `StartNitro()`, then `StartSpecialMoveCooldown(TimeBetweenNitros)`.
  - It needs Boost/Driving to be active; in Hovering the same button is the forward dash.
  - It needs Driving, but there is no separate wheels-on-ground check for activation.
- `StartNitro`:
  - `CarSimulation._SpeedScale = NitroSpeedScale` → MaxSpeed = 3000×1.5 = **4500**.
  - `_SteeringScale = NitroSteeringScale` (**0.3**).
  - `UpdateNitroCameraState(true)` → add `TnPCS_Boosting`.
  - Play RamFX (RamSocket, `FX_Navigation_p.FX.Truck_ram_FX`) and `NitroForceFeedback`, then `PlayNitroSound`.
  - `_NitroTimeRemaining = NitroDuration` (**3.0 s**).
- Each Driving update: remaining −= dt; at 0 → `StopNitro`: SpeedScale=1, SteeringScale=1, remove PCS, stop RamFX, clear `_RammedPawns`.
  `Driving.EndState` (boost released) also calls StopNitro and sets `_RamState = 0`, so releasing LT ends nitro immediately.
- `UpdateRamState` (server): `_RamState = IsUsingNitro ? 1 : 0`. Ram collision is active only during nitro.
- `AttemptToRam` (from `Driving.OnRigidBodyCollision` with contact 0, and from `RigidBodyTrigger`):
  - Requires authority, not dead, RamState==1, target is a TnPawn, not the same team, Mass ≤ **1000** (MaxRamMass), not already rammed this nitro.
  - Then: momentum = RB velocity + (0,0,`ExtraRamZVelocity` **7000**); `ServerPlayRammingSound` (replicated toggle); `P.Rammed(owner)` (robot: acrobatics knock, RammedSpeed default 5000).
  - Damage `TnDamageTypeRammed`: player robot **175**, AI robot **300**, player vehicle **175**, AI vehicle **300**, × TnBuffIncreaseRamDamage.
  - A successful ram does not drop to Hovering. A failed attempt falls through to the base frontal-collision → Hovering rule.
- Camera during nitro (Truck_Optimus_STRATEGY): `TnPCS_Boosting` → FOV **100** (smooth 0.5); orbit distance **650** (in 0.5 s, out **2.0 s**).
- There is no ram animation: script plays only FX, sound and force feedback, consistent with AssetTools.

### 2.4 DISCREPANCY RESOLVED — nitro 3 s / ×1.5 / ×0.3 / 8 s
Both earlier claims were partly right:
- The base constants are **literal floats compiled into UnrealScript getter bytecode** in TransGame.xxx (CONFIRMED):
  ```
  TnTruckForm.get_NitroDuration       return 3.0 * NitroDurationModifier
  TnTruckForm.get_NitroSpeedScale     return 1.5 * NitroSpeedScaleModifier
  TnTruckForm.get_NitroSteeringScale  return 0.3 * NitroSteeringScaleModifier
  TnTruckForm.get_TimeBetweenNitros   return 8.0 * TimeBetweenNitrosModifier
  TnTruckForm.get_MaxRamMass          return 1000.0 * MaxRamMassModifier
  TnCarForm.get_TimeBetweenDashes 2.0, get_TimeBetweenRolls 2.0, get_TimeBetweenJumps 0.3,
           get_CosCollisionNormalThreshold 0.866, Thruster limits 3000 / 6.0
  TnCarSimulation: SineBoostScale 0.5/0.866, JumpBoostDuration 0.7, TerminalVelocity 3500, LandingVelocity 2000,
           LandingTraceDistance 1000, LowSpeedBoostScale 8, LowSpeedBoostThreshold 0.5, MaxExtraAcceleration 5000,
           Roll H/V velocity 1200/1000, RollAngularVelocity 100, PitchForwardLimit -25, PitchForwardAccel 3, ...
  TnHoverCarSimulation: CosGroundAngle 0.707, StabilityThreshold 30, Dash accel/decel 100000, TurnRate (0.05,0.05,1), TerminalVelocity 3500
  ```
- AssetTools is correct that the **cooked property data only holds the ×1.0 `*Modifier` fields**. Those are the per-character tuning multipliers (Default__TnTruckForm / TnCarForm).
- The effective values are therefore literal × 1.0 = 3 s, ×1.5, ×0.3, 8 s. They are script-native defaults, not authored data and not misreads.

## 3. Locomotion play rate / foot slide (CONFIRMED: no rate scaling)
- Robot_ANIMTREE (Optimus uses `TR_Shared_ANIMTREE_p.Robot_ANIMTREE`):
  - `TnVelocitySwitch` picks Idle/Moving.
  - `TnVelocityAnimBlend` blends **Walking → Jogging linearly by horizontal speed from MinSpeed 450 to MaxSpeed 1200 UU/s** (weight = clamp((v−450)/750)). Above 1200 it is 100 % jog.
  - Four `TnStraferAnimBlend` nodes produce F/B/L/R weights from `normal(localVel + localAccel)` (weights = sign·d², Lerp by _BlendSpeed).
- All 17 locomotion `AnimNodeSequence`s share `AnimNodeSynch` group **'Strafers'** with **RateScale 1.0**, and no sequence overrides Rate (1.0).
- No authored AnimTree instance uses `AnimNodeScalePlayRate`, `AnimNodeScaleRateBySpeed` or `TnAnimNodeScaleRateByDelegate`; they exist only as class defaults. No script writes Rate, RateScale or SetGroupRateScale for locomotion.
- **Conclusion:** the original plays jog at 1.0× regardless of speed (1400 UU/s for Optimus). The ~10 % foot slide is original behaviour. The rebuild should *not* add speed-based rate scaling (fidelity), but should match the 450→1200 walk/jog blend.
- Synch behaviour is stock UE3 AnimNodeSynch: the group follows the highest-weight master's play position by relative %, so walk and jog stay phase-aligned. (HIGH, stock engine.)

## 4. Fine aim (CONFIRMED SCRIPT + AUTHORED; recap with Optimus + Ion Blaster specifics)
- Activation: LT → `PlayerWalking.FineAim`.
  - A grenade launcher instead calls `AttemptToDetonate`. Downed or reviving: ignored.
  - Otherwise `SetWantsToFineAim(true)`. Release → `StopFineAim` → wants = false. In vehicle states FineAim is a no-op.
- `TnFineAimManager.Tick` (every PlayerTick):
  - Start if wants ∧ ¬aiming ∧ CanFineAim.
  - Stop if (¬wants ∨ ¬CanFineAim) ∧ aiming.
  - `PlayerWalking.CanFineAim` = not meleeing ∧ not reloading ∧ not dodging. The global/vehicle version returns false.
  - **Reload cancels fine aim and it auto-restores when the reload ends** if LT is still held.
  - Snipers drop out when overheating.
- Transform: PlayerWalking.EndState calls StopFineAim, so R→V ends it. After V→R it must be re-pressed (wants=false).
- Start:
  - `SetSpeedMultiplier(0.5)`; `Weapon.StartFineAim` (WP_StartFineAim sound; spread × FineAimSpreadModifier 0.5).
  - Camera `AddPlayerCameraState(TnPCS_FineAim)`.
  - Aim assist: target snap only if not scoped, `TnGameReplicationInfo.CanTargetSnap()`, and timeout elapsed (`_TargetSnapTimeout` 1.0 s). Weapon TargetSnapRange 1000–10000. Rotate-to-target `ShouldSnapToTarget` with TargetingSpeed 10.
- FOV band selection: TnFovCameraBehavior takes the **first FOVsByPCS row whose PCS list is fully present**.
  - The Ion Blaster has no WeaponPCS (no TnPCS_HeavyPistol / BurstRifle / SniperRifle), so the row is `[TnPCS_FineAim]` → **FOV 45**.
  - Hovering+FineAim is also 45. Other weapons: BurstRifle/HeavyPistol 30, Sniper 20.
- Interpolation:
  - FOV via `Smoother.Smooth(current, target, SmoothTime, dt)`: **0.1 s** into fine aim, **0.4 s** back to the default 80.
  - Orbit distance: TransitionSmoother with PCSTransitionInTime / OutTime (unchanged 800 for the Ion Blaster).
  - Screen offset (−50,300,{80,−35,80}) smooth 0.1. Look speed blends over SpeedTransitionTime 0.5.
- Sensitivity: look speed 25/12.5 vs 50/25 (×0.5); ramp ×2.5; pad sensitivity Lerp(0.8,1.5,CameraSensitivity).
- Camera collision: `TnThirdPersoncollisionCameraBehavior` is in the strategy for all states. No fine-aim-specific collision change was found.
- **Authored values actually used by Optimus + Ion Blaster:** FOV 80→45, orbit 800 (8 m, unchanged), look ×0.5, ground speed ×0.5 (`_GroundSpeedMultiplier`), spread ×0.5, offset row `[TnPCS_FineAim]`.

## 5. Input edge latching (CONFIRMED SCRIPT; frame-loop HIGH)
The original never has render frames without a simulation tick (UE3 = 1 tick per frame; input is processed before that tick).
The pattern to reproduce: **exec on edge, set a latch, consume in sim.**

| input | press | consumption |
|---|---|---|
| Fire | `SetDeferredFire` → `bDeferredFire=true` (stays until release) | `PlayerTick → CheckDeferredFire`: if latched ∧ ¬firing ∧ IsAbleToFire → StartFire(0). Release → StopFire, latch false, IsAllowedToFire=true. Semi-auto: OnFireAmmunition clears IsAllowedToFire until re-press |
| Reload (X) | HmButtonInputStateHandler: Released→Pressed (event 1) | **tap: release before 0.3 s → event 2 → TryInteract else ReloadWeapon()**; hold ≥0.3 s → event 3 (revive/pickup); release after hold → event 4. Timer advances in PlayerTick |
| Jump | `bPressedJump=true` (robot) / `_InputState._Jumping=true` (car) | robot: CheckJumpOrDuck in move processing, then cleared; car: consumed and cleared at the end of DoUpdate (ClearTransientInputs) |
| Transform | immediate in exec (StartTransform) | — |
| Dash / special move | `_InputState._Dashing=true` | consumed by UpdateDashing/UpdateNitro, cleared by ClearTransientInputs each update; release also sets false |

Gameplay should queue edges from the render/input loop until the next fixed step consumes them, and never clear on frames without a step.
Reload in particular must fire on **release of a tap (<0.3 s)**, not on press.

## 6. Fire cadence (CONFIRMED NATIVE + SCRIPT)
- First shot on the start tick (`WeaponFiring.BeginState → FireAmmunition`).
- Each `RefireCheckTimer` re-arms with **non-looping** `SetTimer(interval)`.
- Native `AActor::SetTimer` 0x82F292A8 resets **Count = 0** on an existing timer. Native `AActor::TickTimers` 0x82F867C8 fires when `Rate < Count` (strict).
- **Overshoot is discarded; never more than one shot per tick**: the catch-up path exists only for looping timers.
- At 0.065 s the effective interval is the first frame boundary > 0.065: 0.0667 s at 30 or 60 Hz, i.e. 15 rps.
- To reproduce: `t += dt; if (t > 0.065) { fire(); t = 0; }`. Do not subtract, and do not loop.

## 7. Transformation weapon restore (CONFIRMED SCRIPT)
- `TnPawn.TransformingToRobot.AttemptRestoreRobotWeapon`, called each OnUpdate, **authority only**.
  - Condition: restore when `RemainingTimeAsFactor <= 0.75`, i.e. **75 % remaining = 25 % elapsed**, in the **vehicle→robot** direction only.
  - It runs once (`_HasRestoredRobotWeapon`) and is skipped if a weapon is already equipping or a robot weapon is active.
- It then calls `TnInventoryManager.RestoreRobotWeapon` → `SetCurrentWeapon(stored)` (or NextWeapon). The weapon enters the normal equip path:
  - visible and attached at 25 %;
  - usable after EquipTime (Ion Blaster 0.2 s; HIGH, stock UE3 equip timer).
  - Firing can begin once Active. IsAbleToFire skips the masked-anim check while transforming, so the deferred-fire latch fires as soon as equip completes.
- R→V: the robot weapon is stored with **InstantReload()** and `SetCurrentWeapon(none)`. The vehicle weapon is restored immediately (`RestoreVehicleWeapon`) through the same equip path.
- `InRobotForm.BeginState → ValidateWeapon` re-restores if it is still missing at the end.

## 8. Team / Energon colour (CONFIRMED SCRIPT) — Rendering
`TnCharacterApplier` (Default__TnCharacterApplier):
- Material params: Primary `Cust_Color_A`, Secondary `Cust_COLOR_B`, Energon `EnergonColor`.
- When: `TnPawn.ApplyCharacter(CD)`. That runs on spawn/possess, and on clients when `_CurrentCharacterCompressed` replicates (`ReplicatedEvent` → `ResolveReplicatedCharacterData` → ApplyCharacter).
  It also runs on AI character resolution and the front-end preview.
- `ApplyCharacter` → `SaveColors(CD, RobotMesh)` → `ApplyColorsToCharacter(P)` → `ApplyColorsToMesh` on **robot mesh, vehicle mesh, arm mesh (if any), current weapon's animated mesh**.
  The vehicle and arm get the same robot-derived values.
- `ExtractColors` sentinel rules (**all-zero skips the override**):
  ```
  Primary   = (CD.PrimaryColor   != FColor(0,0,0,255))       ? sRGB->Linear(CD.PrimaryColor)   : RobotMIC.GetVectorParam('Cust_Color_A')
  Secondary = (CD.SecondaryColor != FColor(0,0,0,255))       ? sRGB->Linear(CD.SecondaryColor) : RobotMIC.GetVectorParam('Cust_COLOR_B')
  Energon   = (CD.EnergonColor != (0,0,0,1) && != (0,0,0,0)) ? CD.EnergonColor (linear)        : RobotMIC.GetVectorParam('EnergonColor')
  _EnergonColor (sRGB FColor) = LinearToSRGB(Energon)   // used for FX: boost FX, faction FX
  ```
  The fallback reads whatever the robot mesh's material instance already holds (the authored MIC default), then writes it back to every mesh, so all meshes match the robot MIC.
- Team: there is **no team-colour override in the applier**. Faction is chosen in character data: `ResolveReplicatedCharacterData` picks the per-faction index from `CD.Factions` / `PrimaryColors[]` / `SecondaryColors[]`.
  The only runtime override is `SetColorOverride` (Disguise buff), with `IsOverridingColors` toggling between override and saved colours.
- UI preview: an all-black primary/secondary (0,0,0,255) is replaced by a palette lookup `GetPixelColor(palette, coords)` (TnCharacterScriptBinding). That is a front-end customization concern only.

## 9. Optimus arm mesh (CONFIRMED SCRIPT + AUTHORED)
- `Optimus_ROBODEF.ArmBlueprint`: Mesh `CP_OptimusArm_SKEL`, AnimSet `OptimusArm_ROBO_ANIM`, socket `WeaponSocket_Secondary`, Equip `ARM_Equip`, Unequip `ARM_Unequip`.
  The robot body mesh is `RB_OptimusWeaponArm_SKEL`.
- `TnArmAttachment.Initialize` (from TnRobotForm init): set the mesh and append the anims. Find skel control `HandSkelControl` on the robot mesh and set **BoneScale 0.1**. Start in `ArmEquipped`.
- `ShouldAlwaysEquip` = no active weapon ∨ weapon not attached ∨ (holstered ∧ not equipping).
  - Arm shown iff `ShouldAlwaysEquip ∨ weapon.IsArmRequired()`.
  - Hand shown iff `ShouldAlwaysEquip ∨ weapon.IsHandRequired()`. Both flags come from TnWeaponMesh; melee weapons return true; the **Ion Blaster has neither**.
- States:
  - ArmEquipped: attach to WeaponSocket_Secondary, play ARM_Equip.
  - → ArmUnequipping when not needed: play ARM_Unequip, then detach.
  - The arm is detached whenever the robot mesh is hidden.
  - Hand: HandSkelControl strength 0 when the hand is needed (normal hand), strength 1 otherwise (hand scaled to 0.1).
- **Use cases:** while no robot weapon is active (start of V→R before the 25 % restore; holstered during interactions/cinematics via `HolsterWeapon`), and during melee.
  With the Ion Blaster drawn the arm is hidden and the hand bone is shrunk. The reconstruction needs it for transform-in and melee if those are shown. It is coloured like the robot (ApplyColorsToMesh) and gets the death/buff materials.

## 10. Streets steam colour (INFERRED; time-boxed)
- All 8 Streets emitters use template `FX_Level_Generic_p.FX.Steam_Sm_FX`. The coloured ones carry InstanceParameter `SteamColor` with a Color of ≈(100–124, 17–26, 253–255) (purple-blue) but **ParamType = PSPT_None**.
- Native `UParticleSystemComponent::SetColorParameter` (impl 0x83049980; InstanceParameters at +0x1F0, stride 0x24, ParamType byte +4, Color +0x18) matches an existing entry only when **name and ParamType==3 (PSPT_Color)**. The scalar/vector/actor/material siblings 0x83049770…0x83049B78 test types 1, 2, 4, 5.
- If the getter used by the template's parameter distribution checks type the same way (stock UE3 does), these authored colours are **ignored at runtime** and the steam uses the template's own colour.
- The template's colour module isn't in authored.db, so this was not proven. Low priority.

---

## GAMEPLAY HANDOFF
1. Transform:
   - R→V: velocity clamp 3500 into RB, hover authority ramp ((t/0.5)²), input live.
   - V→R: velocity kept (local), robot Falling, InAir momentum table while IsTransforming or above 1200 air / 1400 ground.
   - Handoff at t=0 (physics/controls), meshes swap at t=Duration.
2. Locomotion anim: no speed-based rate scaling. Walk/jog blend 450→1200 UU/s. One synch group 'Strafers' at RateScale 1.0. Accept the ~10 % slide at 14 m/s.
3. Input: latch edges until consumed. Reload on tap-release (<0.3 s). Car jump/dash flags cleared each car update.
4. Weapon restore: V→R at 25 % elapsed, then 0.2 s equip. R→V InstantReloads the stored weapon.
5. Arm: show CP_OptimusArm when no weapon is drawn (transform-in, melee, holster). Hide it and shrink the hand bone when the Ion Blaster is drawn.

## SYSTEMS HANDOFF
1. Fire: `t += dt; if t > 0.065 → fire; t = 0` (no overshoot carry, max 1 shot per tick). The first shot is immediate.
2. Boost (LT, Driving):
   - Full throttle; truck 3000 max / 2500 accel; low-speed extra accel ≤5000 to 1500 UU/s.
   - Squared steering; no brake. Release → Hovering with a 0.5 s drift ramp.
   - Can't engage during drift.
   - Camera 85 FOV / 1050 orbit (1.0 s strategy blend); hover 80 / 950 (1.5 s).
3. Hover dash (RB in hover): truck forward only, 3000 UU/s for 0.5 s, accel/decel 100000, 2 s cooldown from activation, refused if tilted > 30°.
4. Nitro/ram (RB while boosting):
   - 3 s, MaxSpeed ×1.5 (4500), steering ×0.3, cooldown 8 s from activation.
   - Ends early if LT is released.
   - Ram only during nitro: mass ≤ 1000, enemy only, once per pawn per nitro, +7000 Z momentum, damage 175 player / 300 AI.
   - Camera FOV 100 / orbit 650 (in 0.5, out 2.0). FX Truck_ram_FX at RamSocket, NitroForceFeedback, PlayNitroSound, replicated ramming sound.
5. Fine aim: confirmed values as in §4. Reload interrupts it and it auto-resumes.

## RENDERING HANDOFF
1. Character colours: params Cust_Color_A / Cust_COLOR_B / EnergonColor.
   - Sentinels: (0,0,0,255) for primary/secondary; (0,0,0,1) or (0,0,0,0) for energon. A sentinel → use the robot MIC's existing value.
   - Applied identically to robot, vehicle, arm and current weapon meshes on ApplyCharacter and on replicated character changes. No team override (faction picks the colour set; disguise is the only runtime override).
2. Boost FX colour = Lerp(EnergonColor, Yellow, jumpTimeRemaining/0.7), alpha 100→255.
3. Steam: authored SteamColor is probably ignored (PSPT_None); use the template colour. INFERRED.

## RESOLVED ASSETTOOLS UNKNOWN VALUES
- Nitro duration 3.0, speed ×1.5, steering ×0.3, cooldown 8.0, MaxRamMass 1000 (script literals × authored ×1.0 modifiers).
- Hover-dash cooldown **2.0 s** (TimeBetweenDashes); roll cooldown 2.0; jump interval 0.3; Driving frontal-collision threshold 0.866.
- Boost-driving: Accelerator 1.0, steering exponent 2, ExtraBoost 8×/0.5/5000, BoostScale angles 0.5/0.866, drag formula, jump boost 0.7 s, Driving TerminalVelocity 3500, landing velocity 2000 / trace 1000.
- Camera for boost/nitro: 85/1050, nitro 100/650, strategy transitions 1.0/1.5 s.
- Walk/jog blend speeds 450/1200; locomotion rate 1.0 (none).
- Colour sentinels and application timing.

## STILL UNKNOWN
- Native `UParticleSystemComponent` colour getter type check (steam colour) — not located.
- Truck-specific HoverTruck jump values beyond defaults; Car_Physics wheel blueprints (tire model) not decoded.
- `AmpAnimSwitch` native transition timing for Idle↔Moving (TnVelocitySwitch.ChildGetDesiredSelection is native at 0x82792860, not decompiled this pass).

## CONTRADICTIONS RESOLVED
- Systems' 3 / 1.5 / 0.3 / 8 vs AssetTools' "×1.0 only": both are correct. The ×1.0 values are authored multipliers; 3 / 1.5 / 0.3 / 8 are compiled script literals in the getter functions.
- "Weapon restores ~25 % into transform" vs "75 % remaining": the same thing (RemainingTimeAsFactor ≤ 0.75), V→R only.
- Hover dash 5000/0.3 (Default__) vs 3000/0.5: Optimus uses HoverTruck_Physics, so 3000 / 0.5.

## NEXT RECOMMENDED RE TARGET
Gameplay replication property conditions. Extend ue3dis to decode class-level `replication{}` bytecode for TnPawn, TnVehicleForm, TnWeapon and TnPlayerReplicationInfo.
Alternatively, the native `AmpAnimSwitch` / `TnVelocitySwitch` selection logic (0x82792860, 0x8279CFA0) for exact idle↔move transition thresholds.
