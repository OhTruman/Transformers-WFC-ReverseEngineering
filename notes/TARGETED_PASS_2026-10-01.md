# WFC targeted native-behaviour pass — 2026-10-01

Scope: the 7 isolated questions from Experimental (transform momentum, fast robot movement, fine aim,
boost, input edges, fire cadence, weapon restore). Not a whole-program pass.

## 0. Where this behaviour actually lives (read first)

**Most of the requested gameplay logic is UnrealScript bytecode in `TransGame.xxx`. It is not PPC
code in `default.xex`.** WFC's `Tn*` gameplay classes (TnPawn, TnPlayerController, TnTransformation,
Tn*Form, TnFineAimManager, TnCarSimulation, TnHoverCarSimulation, TnWeapon) have only a handful of
natives (see `data/native_functions.tsv`: TnPawnNative.GetTerminalVelocity, TnVelocitySwitch, …).
`default.xex` supplies the VM, physics, timers and RB integration.

What I did:
- Wrote a read-only **UE3 v511/licensee-144 bytecode decompiler**, `tools/ue3dis.py`, which reuses AssetTools'
  `ue3pkg.py` in place. It decompiles ~18k functions from Core/Engine/HM_Engine/TransGame with
  about 0.2% decode failures. Output is in `work/script/decomp/<Pkg>.<Class>.txt`.
- Confirmed the timer semantics that cadence depends on in **native code**, at the addresses below.
- Read authored archetype values from AssetTools `authored.db` in place (read-only) wherever the script logic
  consumes them.

Provenance labels: **CONFIRMED** means read directly from compiled bytecode or decompiled native code.
**HIGH** means a strong inference from that code plus stock UE3 semantics. **INFERRED** and
**UNKNOWN** are as named. Script "addresses" are `Package:Class.Function @ bytecode offset`.
Native addresses are virtual addresses in `default.xex`.

ReVa (127.0.0.1:8080) was **not reachable** this session. Native queries ran through headless Ghidra
in `-readOnly` mode against `work/ghidra-snapshot` using `tools/ghidra_scripts/WfcQuery.java`, driven by
`tools/wfcq.ps1`.

Units: UU (1 m = 100 UU). Physics enum: 1=Walking, 2=Falling, 4=Flying, 10=RigidBody. Role 3=Authority.
Form type 0=Robot, 1=Vehicle.

---

## 1. TRANSFORMATION MOMENTUM

### 1a. Call chain (CONFIRMED)
```
L3 "Transform" -> PressTransform | OnRelease ReleaseTransform          (Xe-TransInput.ini)
TnPlayerController.PressTransform        refuse if !Pawn._ReceivedWeapon, interacting, reviving;
                                         TnBuffTransformDisruptor -> fail sound
 -> (state) PlayerWalking.Transform -> StartTransform(1)   / PlayerInVehicleForm.Transform -> StartTransform(0)
TnPlayerController.StartTransform        refuse if IsTransforming or !TransformingEnabled;
                                         refuse if !MoveToSafeTransformationLocation(target)  (HUD "can't transform")
                                         client: ServerTransform(target, loc, rot); then DoTransform
TnPlayerController.DoTransform           EndBlock; AbortMelee; GotoNewFormState(target)  <-- controller state switches NOW
                                         Pawn.Transform(target)
TnPawn.Transform                         target==Vehicle: DropHeavyWeapons; _TargetForm=target; OnTransformationChanged
TnPawn.InRobotForm.OnTransformationChanged   -> GotoState('TransformingToVehicle')
TnPawn.InVehicleForm.OnTransformationChanged -> GotoState('TransformingToRobot')
```
The controller state flips at transform **start**: `PlayerWalking` changes to `PlayerInCarForm`, or the reverse.
From frame 0 of a transform, input therefore drives the **target** form.

### 1b. TnPawn.Transforming.BeginTransformation (CONFIRMED)
```
_CurrentForm = TargetForm                       // form handoff happens at START, not mid-way
_CurrentTransformation = T
_CollisionController.SetCollisionMode(mode)     // R->V: 4 (PhysicalVehicleMesh -> SetPhysics(10 RigidBody))
                                                // V->R: 1 (AnimatedCylinderRobotMeshHybrid -> SetPhysics(2 Falling))
T.Execute(!bPlayDownedAnimation)
SetMovementCapabilities(TargetForm.FormMovementCapabilities)
MakeNoise(TransformNoiseRadius); restore Base; stimulus
```
`TransformingToVehicle.BeginState` runs StoreRobotWeapon, then BeginTransformation(VehicleForm, R2V, 4), then SelectVehicleWeapon.
`TransformingToRobot.BeginState` runs StoreVehicleWeapon, then BeginTransformation(RobotForm, V2R, 1), then `Cylinder.SetBlockRigidBody(false)`.

### 1c. TnTransformation.Execute / Update / Complete (CONFIRMED)
```
Execute(bFasterDownedTransformation):
  _IsActive = true
  _SourceForm.EndPlay()            // source stops "playing" (hides attachments etc.) but stays Active (mesh still drawn)
  _TargetForm.Activate()           // target becomes Active immediately (physics/velocity handoff happens HERE)
  Rate = bFaster ? 4.0 : 1.0
  source anim: Params(name, BlendIn=_BlendInTime(0.115), BlendOut=0,   RootMotionMode=2, Priority=1, PlayRate=Rate, Override=2)
  target anim: Params(name, BlendIn=0, BlendOut=_BlendOutTime(0.25), ... same)
  anims: R->V  'Transform_ToVehicle_ROBO' + 'Transform_ToVehicle_VEH'
         V->R  'Transform_ToRobot_VEH'    + 'Transform_ToRobot_ROBO'
  _Duration = min(len(source anim), len(target anim)) / Rate
  _RemainingTime = _Duration
Update(dt):  _RemainingTime -= dt; if (_RemainingTime <= 0 && CanComplete) Complete()
Complete():  _SourceForm.Deactivate(); _TargetForm.BeginPlay(); _IsActive=false
RemainingTimeAsFactor = Duration==0 ? 0 : max(RemainingTime,0)/Duration     // 1 -> 0 over the transform
```
`TnPawn.Transforming.OnUpdate` ticks **both** forms every frame (`RobotForm.Update`, `VehicleForm.Update`)
and the transformation. It also blends `OffsetMeshes(TransformBlendTimeRemaining/0.5 * PositionShift)` over 0.5 s,
which is used only when the safe-location search moved the pawn.

### 1d. Robot → Vehicle velocity (CONFIRMED)
`TnVehicleForm.OnActivate` (called from Execute, frame 0):
```
Velocity = ClampLength(OwnerPawn.Velocity, 3500.0)          // preserved, clamped to 3500 UU/s
if (Pawn.Physics == RigidBody && !MotionIsKeyframed):        // MotionIsKeyframed = !IsLocallyControlled && !dead
    Mesh.SetRBPosition(Pawn.Location + (Mesh.Translation >> Pawn.Rotation))
    Mesh.SetRBRotation(Pawn.Rotation)                         // vehicle heading = robot pawn yaw at transform start
    Mesh.SetLinearVelocity(Velocity)
OnTeleport(Pawn.Rotation)                                     // car: InputState.ViewRotation = pawn rotation
Pawn.Velocity = Velocity
```
`TnCarForm.OnActivate` then runs `GotoState('Hovering')`, which calls `HoverSimulation.Activate()` (linear/angular damping 0)
followed by **`HoverSimulation.Drift()`**, setting DriftTimeRemaining = DriftDuration (HoverTruck/HoverCar default **0.5 s**).
Hover strafe acceleration is scaled by:
```
CalculateDriftScale = (1 - DriftTimeRemaining/DriftDuration)^2       // 0 at transform start -> 1 after 0.5 s
MaxAccel = MaxLinearAcceleration * DriftScale * (up.Z)^2
```
**Net result:** carried velocity (≤3500) is kept, and steering/throttle authority fades in quadratically over 0.5 s.
`TnCarForm.OnUpdate` runs only while `Pawn.Physics == RigidBody`, which BeginTransformation has already set.
Vehicle input is therefore live during the whole robot→vehicle transform.

### 1e. Vehicle → Robot velocity (CONFIRMED except where noted)
- `TnVehicleForm.OnEndPlay` (frame 0): `if MotionIsKeyframed: Pawn.Velocity = PhysicsState.LinearVelocity * 0.1`.
  This applies only to **non-locally-controlled** (remote/simulated) pawns.
  For the local player, Pawn.Velocity is whatever RB sync left, i.e. the vehicle's velocity (HIGH: stock UE3 RB→Actor velocity sync).
- Collision mode 1 calls `SetPhysics(PHYS_Falling)`.
- `TnRobotForm.OnActivate`: resizes the collision cylinder, attaches components and runs `AcrobaticsManager.Activate()`.
  `if (Role != SimulatedProxy || AcrobaticsState == 9) AcrobaticsManager.Fall()`, so the **robot always enters Fall** on the authority/owner side.
- During `TransformingToRobot`, `UpdateCylinderSize` lerps the radius/half-height between robot and vehicle values
  using RemainingTimeAsFactor (1 → 0).

Deceleration afterwards comes from `TnPawn.CalcVelocity` (CONFIRMED script; native physics invokes it, HIGH:
`HmPawn.CalcVelocity` returns false = "use native", and TnPawn's override returns true):
```
CalcVelocity(dt, MaxSpeed):
  if dt==0 return
  if |_OverrideAcceleration|>0: Velocity += _OverrideAcceleration*dt; return
  Mask = (Physics==Falling||Physics==Walking) ? (1,1,0) : (1,1,1)
  Prev = Velocity*Mask
  DesiredN = ClampLength(Acceleration*Mask, 1.0)                     // input direction, magnitude<=1
  Desired  = |DesiredN|==0 ? (Physics==Falling ? Prev : 0)           // no air braking without input
                           : Normal(DesiredN) * max(450, |DesiredN|*MaxSpeed)   // 450 UU/s minimum move speed
  P = CalculateMomentumPreservation(DesiredN, Prev, MaxSpeed)
  MaxAccel = AccelRate / (1 + P)
  LocalA = ((Desired-Prev)/dt) << Rotation                           // into pawn-local axes
  LocalA.X/Y/Z = FClamp(each, -MaxAccel, MaxAccel)                    // per-axis box clamp, not radial
  Velocity = Prev + (LocalA >> Rotation)*dt   (Z restored)
  if Falling: Velocity.Z = max(oldZ + GravityZ*dt, -TerminalVelocity)  // terminal velocity IS applied

CalculateMomentumPreservation(DesiredN, FlatVel, MaxFlatSpeed):
  if MomentumBlueprint==none || |FlatVel| < MaxFlatSpeed+0.1: return 0   // only when OVER speed
  dot = Normal(DesiredN) . Normal(FlatVel)
  Params = (Physics==Falling || IsTransforming) ? MB.InAir : MB.OnGround
  if dot > 0.866            return Params.Forward        // stick within ~30 deg of travel
  else if |DesiredN|==0     return Params.Neutral
  else                      return Params.Backward
```
Optimus: AccelRate 12000, MomentumBlueprint `TR_Acrobatics_p.TruckTransformerMomentum`
(OnGround F7/N3/B1, InAir F100/N100/B5). Effective max acceleration while over-speed:

| situation | P | max accel (UU/s²) |
|---|---|---|
| ground, stick forward | 7 | 1500 |
| ground, no stick | 3 | 3000 |
| ground, stick back/sideways | 1 | 6000 |
| air **or transforming**, forward | 100 | 118.8 |
| air or transforming, neutral | 100 | 118.8 |
| air or transforming, back | 5 | 2000 |
| not over speed | 0 | 12000 |

Other momentum blueprints: Car F7/N3/B1, F100/N100/B5; Plane F5/N3/B0.5, F1000/N50/B3; Tank F3/N2/B1, F200/N100/B3; Brute N1/N1.

**Summary answers**
- Velocity preserved? **Yes, both directions.** R→V is clamped to 3500 UU/s.
  V→R is unclamped for the local player; remote/keyframed pawns get ×0.1.
- Movement input during transform: **yes**. The controller switches state at start. R→V gives hover input with a 0.5 s quadratic drift ramp.
  V→R gives robot input, with CalcVelocity using the **InAir** momentum params because `IsTransforming` is true.
- Acceleration change: R→V via DriftScale; V→R via the momentum table (≈119 UU/s² if pushing forward while over speed).
- Heading: R→V sets the vehicle RB rotation to Pawn.Rotation (the robot's controller-locked yaw).
  Hover then yaw-tracks the camera (see §4). V→R: the robot faces controller yaw every frame (`InRobotForm.FaceRotation`; pitch is zeroed while dodging/attacking/hovering).

## 2. FAST ROBOT MOVEMENT — no sprint state; wrong base constants in the rebuild
There is **no robot sprint/jog-run input** in WFC script. Robot "speed" mechanisms are:
1. **Base ground speed from the character blueprint** (CONFIRMED `TnPawn.ApplyTransformer`).
   It overwrites the TnPlayerPawn defaults the rebuild currently uses:

   | field (Optimus_ROBODEF) | original | rebuild (from Default__TnPlayerPawn) |
   |---|---|---|
   | BaseGroundSpeed | **1400** | 550 |
   | AccelRate | **12000** | 2048 |
   | AirSpeed | **1200** | 1500 |
   | AirControl | **0.4** | 0.7 |
   | TerminalVelocity | **6000** | "uncapped" |
   | JumpZ = √(2·2940·Acrobatics.JumpHeight 500) | **1714.6** | 1917 (from 625) |
   | BaseEyeHeight (TnTransformer default) | **150** | 80 |
   | Collision R/H | 200/200, MeshTranslation Z −200 | 175/200 |

   `GroundSpeed = BaseGroundSpeed × Π SpeedMultiplierFactors` (TnPawn.UpdateSpeeds). Factors come from fine aim (×0.5),
   weapons (TnWeapon.SetSpeedMultiplier), buffs, melee and block.
   Minimum commanded speed with any stick input is 450 (`CalculateDesiredFlatVelocity`).
2. **Dodge**: an ability (`TnAbilityDodge`, Ability0/1 = RB/LB per class loadout). `TnPlayerInput.Dodge` forces a DoubleClickDir from the stick
   (|up|>=|right|: back=4, fwd=3; else left=1, right=2) → `RobotForm.Dodge` → AcrobaticsManager.
   Shared acrobatics: DodgeSpeed **3000**, DodgeTime 0.5 (default), noise 3000. While dodging: fine aim is blocked and pitch is zeroed.
3. Hover (`TnAbilityHover`): HoverJumpHeight 500, HoverDuration 7, HoverAirSpeed 500.

Most likely, the "missing fast state" observed in the original is **just 1400 UU/s base speed with 12000 accel**
(INFERRED; check against capture). The camera has no sprint PCS.

## 3. FINE AIM (CONFIRMED script + authored camera data)
- Input: LT runs `FineAim | Boost` (both commands fire). `FineAim`'s OnRelease is `StopFineAim`.
  Robot state `PlayerWalking.FineAim`: if the weapon is a grenade launcher it calls `AttemptToDetonate` instead.
  If downed/reviving it is ignored. Otherwise it calls `_FineAimManager.SetWantsToFineAim(true)`. In vehicle states FineAim is a no-op.
- `TnFineAimManager.Tick` runs every PlayerTick:
  start if wants && !aiming && CanFineAim; stop if (!wants || !CanFineAim) && aiming.
  `PlayerWalking.CanFineAim` returns false if meleeing, **reloading**, or dodging.
  Reloading therefore drops fine aim, and it **resumes automatically** once the reload ends if LT is still held.
- StartFineAim: `PP.SetSpeedMultiplier(_GroundSpeedMultiplier=0.5)`; weapon.StartFineAim (WP_StartFineAim sound);
  camera `AddPlayerCameraState(TnPCS_FineAim)`; optional target snap (`_TargetSnapTimeout` 1.0, not for scoped weapons; weapon TargetSnapRange 1000–10000).
- StopFineAim: removes the multiplier and the PCS. `PlayerWalking.EndState` (transform to vehicle) calls StopFineAim.
- Spread: weapon `FineAimSpreadModifier` 0.5.
- Camera, Optimus robot = `CAM_Strategies_p.OverTheShoulder_STRATEGY` (via Truck_Optimus_CAMSET).
  Behaviors choose the first `…ByPCS` row whose PCS set is fully present. The Ion Blaster has **no WeaponPCS**, so the generic `[TnPCS_FineAim]` row applies:

  | parameter | normal | fine aim (Ion Blaster) |
  |---|---|---|
  | FOV (TnFovCameraBehavior) | **80**, SmoothTime 0.4 | **45**, SmoothTime 0.1 |
  | Orbit distance (TnLocationOffset) | 800 | 800 (100 only for Sniper/HeavyPistol/BurstRifle PCS) |
  | Screen-space offset (X,Y,Z) at pitch −75/0/+75 | (150,300,150)/(150,300,−35)/(150,300,150), smooth 0.3 | (−50,300,80)/(−50,300,−35)/(−50,300,80), smooth 0.1 |
  | Look speed yaw/pitch | 50/25, ramp ×2.5 | **25/12.5** (×0.5), ramp ×2.5 |
  | Look-speed blend | SpeedTransitionTime 0.5 s | |
  | Rotate-to-target | | snap, TargetingSpeed 10 |

  Other rows: Sniper FOV 20 / yaw 6.5; HeavyPistol/BurstRifle FOV 30 / yaw 9.375; Hovering+FineAim FOV 45 with offset row (150/−25,300,150/−100).
  Note: `Xe-TransCamera.ini` DefaultFOV 75 is the *class* default. The strategy archetype overrides it to **80**.
- The HUD reads fine-aim state from `HasPlayerCameraState(TnPCS_FineAim)`.

## 4. VEHICLE BOOST (CONFIRMED) — boost is a mode switch, not the Dash
- Input: LT runs `StartBoost`, which sets `IsBoostPressed=true` (unless TnBuffImpairVehicleSpeed), then `OnStartBoost`. Release runs `StopBoost`.
  `PlayerInCarForm.OnStartBoost/OnStopBoost` set `CarForm._InputState._Boosting`.
  Entering any vehicle state with IsBoostPressed already true calls OnStartBoost immediately.
  Holding LT while transforming R→V therefore boosts as soon as the car is active.
  PC: no LT mapping exists in the cooked Xenon ini. The rebuild should map boost to the same "LT" intent as fine aim.
- `TnCarForm` states:
  - **Hovering** (default on activate). HoverSimulation strafes in vehicle-local axes, uses MaxLinearSpeed (HoverTruck 1500) and MaxLinearAcceleration (3000),
    has the drift ramp, and **yaw tracks the camera/view yaw every physics step**.
    `UpdateTurn` gives angular velocity = axisAngle(q⁻¹·target)·(0.05,0.05,1)/dt − current, so yaw is matched in one step.
  - Hovering.UpdateBoosting: `if _Boosting && (SimulationMode==0 || !IsDrifting) → GotoState('Driving')`.
    Boost cannot engage during the 0.5 s drift window.
  - **Driving** (= boost). BeginState sets `_Boosting=true` and `CarSimulation.Activate()` (linear damping 0). Boost FX and sound follow.
    Inputs: `Accelerator = 1.0` (always full throttle), `Steering = sign(s)·s²`, `RollControl = strafeX`.
    Forward accel = `Lerp(MaxAccel, Drag(MaxSpeed), fwdSpeed/MaxSpeed) + ExtraBoost`, × BoostScale × Accelerator.
    It is only applied when wheels are on the ground.
    `Drag(v) = v²·|g_RB| / max(1,Pawn.TerminalVelocity)²`, applied opposite the velocity on ground.
    ExtraBoost is a quadratic from MaxAccel·8 at 0 speed down to 0 at 0.5·MaxSpeed, capped at 5000.
    BoostScale = 1 − (clamp(forward.Z,0.5,0.866)−0.5)/0.366, which fades boost on 30–60° climbs.
    Truck_Physics: MaxSpeed **3000**, MaxAccel 2500, Mass 2500. Car_Physics: 3000 / 3000 / 1500.
  - Driving.UpdateBoosting: when `_Boosting` goes false it **returns to Hovering**.
    The hover re-entry runs Drift() again, so there is a 0.5 s quadratic authority ramp after release and the velocity is kept.
    A frontal RB hit (`contactNormal·forward > 0.866`) also drops to Hovering.
- **Dash (RB "VehicleSpecialMove") is separate.** Hovering.UpdateDashing calls DoDash with a 2.0 s cooldown (`TimeBetweenDashes`).
  Truck dashes forward only, i.e. Dash(1,0,0). Car dashes along the dominant stick axis.
  UpdateDash uses DashSpeed for DashDuration with accel 100000, then decelerates (100000) back to MaxLinearSpeed. It is cancelled if unstable (|pitch|/|roll| > 30°).
  HoverTruck_Physics: DashSpeed **3000**, DashDuration **0.5**. Default__ blueprint values (5000 / 0.3) are **not** used by Optimus.
  In Driving, the truck's RB is **Nitro**: SpeedScale 1.5, SteeringScale 0.3, 3 s, cooldown 8 s, camera PCS `TnPCS_Boosting`. The car's RB is Roll (2 s cooldown).
- Hover jump (A): `ApplyLinearVelocity(0,0,JumpLinearSpeed 1200)` + pitch spin; 0.3 s between jumps; requires ground.
- Terminal velocity: hover 3500 down; car lerps from LandingVelocity 2000 to 3500 over a 1000 UU trace.

## 5. INPUT EDGE HANDLING
Stock UE3 (HIGH): input is polled once per frame and exec bindings run immediately, *before* that frame's world tick.
Every rendered frame is also exactly one simulation tick, so "render frames with no sim step" never happen in the original.
The commands themselves are **latches** that the simulation consumes later (CONFIRMED):

| input | binding | press handler | consumed |
|---|---|---|---|
| Fire (RT) | `Button bFire \| SetDeferredFire \| OnRelease StopDeferredFire` | `bDeferredFire=true` (latched) | `TnPlayerController.PlayerTick → CheckDeferredFire` every tick: if latched && !firing && IsAbleToFire then `StartFire(0)`; stops if !able. Release: StopFire, bDeferredFire=false, IsAllowedToFire=true. Semi-auto weapons clear IsAllowedToFire on each shot (re-press needed) |
| Reload (X) | `PressXButton \| OnRelease ReleaseXButton` | `HmButtonInputStateHandler` (ButtonTimeOut **0.3 s**) | **Reload fires on RELEASE of a tap <0.3 s** (event 2 → TryInteract else `ReloadWeapon()`). Hold ≥0.3 s gives event 3 (revive/pickup); release after the hold gives event 4 (AbortRevive). Timer updated in PlayerTick |
| Jump (A) | `PressJump \| Ascend` | `PlayerWalking.PressJump`: `bPressedJump=true` unless downed, jumping disabled, or shield active | `CheckJumpOrDuck` (move processing) → `RobotForm.Jump`, then clears the latch. Car form: `_InputState._Jumping=true`, consumed and cleared in DoUpdate (`ClearTransientInputs`) |
| Transform (L3) | `PressTransform \| OnRelease ReleaseTransform` | executes the transform **immediately** in the exec (no latch) | — |
| Boost/FineAim (LT) | held flags `IsBoostPressed` / `bWantsToFineAim` | | polled every tick |

Rebuild guidance: latch press events and keep them until the next sim step consumes them.
Implement X as a tap-on-release with a 0.3 s hold threshold.

## 6. FIRE CADENCE (CONFIRMED native + script)
Script: `Weapon.WeaponFiring.BeginState → TimeWeaponFiring` sets a looping `RefireCheckTimer` and **fires the first shot immediately**.
Every refire, `HmWeapon.WeaponFiring.RefireCheckTimer` re-arms the timer **non-looping**:
`SetTimer(GetFireInterval(0), false, 'RefireCheckTimer')`, then `ShouldRefire → FireAmmunition`.
`TnWeapon.GetFireInterval = FireIntervalLerper.Value × Pawn.FireIntervalModifier × skill multiplier`. The Ion Blaster MP interval is 0.065 (SP/SV 0.065, AI 0.07), with RampTime 0.

Native (CONFIRMED, default.xex):
- `0x82C49EE0` = `AActor::execSetTimer` (reached from the {name,PMF} table entry 0x83711660, name "intAActorexecSetTimer"; PMF filled by CRT init 0x83652420).
- `0x82F292A8` = `AActor::SetTimer(Rate,bLoop,FuncName,Obj)`. Timers TArray is at Actor+0x6C (Num +0x70, Max +0x74). FTimerData is 0x14 bytes:
  `{u32 bLoop(bit31) @0, FName @4, f32 Rate @8, f32 Count @0xC, UObject* Obj @0x10}`.
  If an existing (FuncName, Obj) timer is found: Rate==0 clears it; otherwise it sets bLoop, Rate and **Count = 0.0**.
- `0x82F867C8` = `AActor::TickTimers(dt)`:
  ```
  for t in Timers: t.Count += dt
  for t in Timers:
     if t.Rate == 0: remove
     elif t.Rate < t.Count:                          // strict
        n = t.bLoop ? int(t.Count/t.Rate) : 1
        if t.bLoop: t.Count -= t.Rate*n              // loop keeps remainder and catches up n calls
        call FuncName n times (stops early if actor deleted / timer cleared)
        non-loop: removed unless re-armed in the callback (Count==0 after SetTimer)
  ```
**Answer:** the fractional overshoot is **NOT preserved**. Each refire re-arms with Count=0, so the actual interval is the
first frame boundary where accumulated dt **strictly exceeds** 0.065. At 30 Hz that is 2 frames = 0.0667 s (15 shots/s); at 60 Hz it is 4 frames = 0.0667 s.
There is never more than one shot per tick from the refire path. The first shot comes on the same tick as fire start.

## 7. TRANSFORMATION WEAPON RESTORE (CONFIRMED)
- R→V start: `StoreRobotWeapon` remembers the robot weapon and calls **`InstantReload()`** on it, so transforming refills the clip.
  Then `SetCurrentWeapon(none)` and `RestoreVehicleWeapon`.
- V→R start: `StoreVehicleWeapon` (also InstantReload), then `UnEquipWeaponInstantly`.
- Every tick in `TransformingToRobot.OnUpdate` (Authority only), `AttemptRestoreRobotWeapon` runs once:
  it restores when `RemainingTimeAsFactor <= _RestoreWeaponTransformFractionRemaining`.
  The value is **0.75** (Default__TnPawn, no overrides), i.e. **25% elapsed**. It then calls `TnInventoryManager.RestoreRobotWeapon → SetCurrentWeapon(stored)`
  (or NextWeapon). The weapon enters the normal equip state: it is visible at 25% and usable after EquipTime (Ion Blaster 0.2 s; HIGH, stock UE3 equip timer).
  With Duration = min(ToRobot clips) ≈ 1.13 s: restore at ≈0.283 s, fire-ready ≈0.483 s.
- `InRobotForm.BeginState → ValidateWeapon` restores the weapon if it is still missing at the end.
- During any transform: weapon switching is blocked (`PreWeaponSwitch` returns false while IsTransforming).
  `IsAbleToFire` skips the masked-animation check while transforming.

---

## Native functions identified this pass
| addr | name | conf |
|---|---|---|
| 0x82C49EE0 | AActor::execSetTimer | CONFIRMED |
| 0x82C4A070 | AActor::execClearTimer | CONFIRMED |
| 0x82F292A8 | AActor::SetTimer | CONFIRMED |
| 0x82F867C8 | AActor::TickTimers | CONFIRMED |
| 0x83612160 | hardcoded-FName table init (6043 names → `data/fname_globals.tsv`, base 0x83826580) | CONFIRMED |
| 0x82BACD78 | FName::FName(const TCHAR*, EFindName, bool) / Init | HIGH |
| 0x826F0088 | cached class/type lookup by name (static ctor helper) | HIGH |
| 0x826ECCC8 | IsA / type check (args are obj-0x10, class-0x10) | HIGH |
| 0x82823C60 | Hm native type/factory registration (FName → factory object) | HIGH |
| 0x8291C508.. | static FName getters for TnPCS_* camera states (0x83753898..) | CONFIRMED |

## Structures
- FTimerData (0x14), Actor timer array @+0x6C. See §6.
- `TnTransformerMomentumBlueprint.MomentumParams {float Forward, Neutral, Backward}`; fields OnGround, InAir.
- UFunction export on disk (v511/lic144): `i32 ?, FName None, i32 SuperField, i32 Next, i32 ScriptText, i32 Children,
  i32 CppText, i32 Line, i32 TextPos, i32 ScriptSize, script[ScriptSize], u16 iNative, u8 OperPrec, …`.
  Bytecode differences from later UE3: Context = expr,u16 skip,u8 size,expr (no field ref); Switch = u8 size, expr; FName = 8 bytes.

## Follow-up (same day)
See `notes/STEPUP_LEDGE_2026-10-01.md`. Resolved there:
- The CalcVelocity hook is **CONFIRMED** native. `AHmPawn::CalcVelocity` 0x8275C240 calls the script event, with fallback 0x82F701C0.
- Falling MaxSpeed = **AirSpeed**; walking MaxSpeed = GroundSpeed × MaxSpeedModifier.
- Step-up/ledge/falling native behaviour is mapped.

## Blockers / unknowns (as of the first pass; see follow-up above)
- ReVa endpoint was down. Native confirmation of the CalcVelocity event call site was not found
  (the FName global 0x83750A40 has no direct lis/addi users), so it is rated HIGH, not CONFIRMED.
- Native AcrobaticsManager/physWalking step-up and ledge details were not covered this pass.
- `MaxSpeed` argument to CalcVelocity while Falling (AirSpeed vs GroundSpeed) is chosen natively and remains **UNKNOWN**.
- Exact transform clip lengths come from Experimental's glTF (1.97 / 1.13 s); Duration = min of each pair.
