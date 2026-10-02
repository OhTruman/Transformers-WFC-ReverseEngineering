# MILESTONE 03 — Vehicle / gameplay native fidelity (WFC, Xbox 360)

Pass date: 2026-10-02. Scope: priorities 1–10 of the narrow gameplay + audio pass. Audio priorities 11–15 are in
`notes/MILESTONE03_AUDIO_NATIVE_FIDELITY.md`.

Sources:
- Script: UnrealScript bytecode decompiled with `tools/ue3dis.py` into `work/script/decomp/<Pkg>.<Class>.txt`. Bytecode offsets are quoted as `@0x....`.
- Data: AssetTools `authored.db`, read-only.
- Native: headless read-only Ghidra snapshot, queried with `tools/wfcq.ps1`.

All of WFC's vehicle physics is UnrealScript driving a PhysX rigid body (`IRigidBody` interface). The only native pieces are
the PhysX integrator, the trace, and `Actor.GetGravityZ`. The rebuild's "native vehicle physics" therefore means "this script".

Confidence scale:
- **CONFIRMED**: read directly from bytecode or data.
- **HIGH**: one small inference.
- **PARTIAL**: algorithm known, but a number or link is missing.
- **UNKNOWN**: not recovered.

Shared constants:
| constant | value | source |
|---|---|---|
| DefaultGravityZ | −2940 | Xe-TransGame.ini |
| RBPhysicsGravityScaling | 0.66 | Xe-TransGame.ini |
| Rigid-body gravity (Physics = PHYS_RigidBody) | −2940 × 0.66 = **−1940.4 UU/s²** | `Actor.GetGravityZ` native; TnPawnNative × GravityScale 1.0 |
| Hover vehicle data (Optimus) | `HoverTruck_Physics` {DashDuration 0.5, DashSpeed 3000, SuspensionRadius 185}; class defaults MaxLinearSpeed 1500, MaxLinearAccel 3000, DriftDuration 0.5, JumpLinearSpeed 1200, JumpAngularSpeed 1.0, TerminalVelocity 3500 | authored.db |
| Hover suspension (Optimus) | `HoverTruck_Suspension` {RestingLength 250, Damping 4000}, Stiffness default 10000 | authored.db |
| Boost car data (Optimus) | `Truck_Physics` {Mass 2500, COM (−47,0,20), Inertia (22.7M, 46.4M, 58.9M), MaxAcceleration 2500, MaxSpeed 3000, JumpLinearVelocity (600,0,1400), AirControlTurnAcceleration 12, AirControlStrafeAcceleration 2600, RollDuration 0}; `Truck_Suspension` {Stiffness 120000, Damping 8000}; OptimusTruckForm ChassisOffset 15 | authored.db |

---

## P1 — HoverTruck suspension / ride height
- **CONFIDENCE:** CONFIRMED for the algorithm and constants. PARTIAL for the absolute ride height, because the hover rigid-body mass is taken from the RB at run time.
- **ADDRESS / FUNCTION:**
  - `TnHoverCarSimulation.UpdateSuspension`
  - `CalculateSuspensionLocation`
  - `InitializeSuspension`
  - `TnSuspension.Update`
  - `TnSpring.Update`
  - `TnSpring.CalculateSpringVelocity`
- **CLASS:** TransGame.TnHoverCarSimulation, TnSuspension, TnSpring
- **CALLERS:** `TnHoverCarSimulation.Update` (each physics tick, while SimulationMode ≠ 0)
- **CALLEES:** `TnSuspension.Update` → `MultiTrace(…, 32)` → `TnSpring.Update`; `RigidBody.ApplyForce(force, location)`
- **CONSTANTS:**
  - 4 probes.
  - Probe offset = Normal(1,1,0)·SuspensionRadius(185), rotated i·90°. This puts the probes at (±130.8, ±130.8) around the **local centre of mass**.
  - RestingLength 250, Stiffness 10000, Damping 4000.
  - WheelRadius **0.0** for hover.
  - Spring mass = **RB mass / 4** (`InitializeSuspension` @0x0016 `MassShare = Mass/4`).
  - Ground test: ContactNormal.Z > **0.707** × CosGroundAngleModifier.
- **SCRIPT/NATIVE:** All script. PhysX integrates the forces.
- **PSEUDOCODE:**
```
dir = RB.RotateToWorldSpace((0,0,-1))                       // body-down, tilts with the truck
for i in 0..3:
  P = RB.TransformToWorldSpace(RB.LocalCOM + rot(i*90°) * Normal(1,1,0)*185)
  hit = MultiTrace(P, P + dir*(RestingLength + WheelRadius))  // accept BlockRigidBody && RBChannel!=6, or WorldInfo
  if hit: len = max(0, |hit-P| - WheelRadius); HasContact = true
  else:   len = RestingLength; HasContact = false
  g  = -dir.Z * GetGravityZ()                                // ≈ -1940.4 when level
  vel = (Length>=0) ? (len - Length)/dt : 0 ; Length = len    // Reset() sets Length=-1 on Activate
  k = K/m ; b = B/m
  v' = (vel + dt*(k*(L0-len) + g)) / (1 + b*dt + k*dt*dt)      // implicit (backward-Euler) spring-damper
  F  = m*((v'-vel)/dt - g)
  if HasContact: RB.ApplyForce(-dir * max(0, (-dir·N_contact) * F), P)
ContactNormal = average of contacting normals ; NumContacts = count
```
- **ORIGINAL WFC BEHAVIOR:**
  - Each probe is a critically stiff implicit spring that already includes gravity compensation.
  - At rest each probe pushes up m·|g|, so the 4 probes carry the full weight.
  - The equilibrium compression satisfies k(L0−L)+g = 0, which gives **L_eq = L0 − |g|·m/K = 250 − 1940.4·(M/4)/10000**.
    - With M = 2500 (Truck_Physics Mass, if that is the hover RB mass): **L_eq ≈ 128.7 UU** from the COM-plane probe points to the ground.
    - The mass link is HIGH, not CONFIRMED.
  - The probe ray tilts with the body. The force acts along body-down, scaled by the cosine to the contact normal, and is never pulling (max 0).
  - Linear and angular damping are set to **0** on Activate. All damping comes from the springs.
- **CURRENT REBUILD COMPARISON:** Not inspected; this lane does not read Rebuild worktrees. The rebuild must use COM-relative probe points, WheelRadius 0, the implicit formula, and per-probe mass M/4. A fixed "ride height" target must not be used.
- **PRIMARY HANDOFF:** Gameplay (vehicle sim).
- **EXPERIMENTAL ASSERTION THAT CAN NOW CHANGE:**
  - Hover rest height = L0 − |g|·(M/4)/K.
  - Probe square 261.6 UU per side, centred on COM.
  - Zero RB damping in Hovering.

## P2 — Body pitch / roll / attitude
- **CONFIDENCE:** CONFIRMED
- **FUNCTION:**
  - `TnHoverCarSimulation.UpdateRoll`, `UpdateTurn`, `get_ShouldUpright`, `get_IsUnstable`, `get_IsUpsideDown`
  - Visual layer `TnAccelerationAnimBlend` (VEH_Car_ANIMTREE)
- **CONSTANTS:**
  - Turn gain vector (0.05, 0.05, 1)/dt.
  - Roll input gain 1.0.
  - StabilityThreshold 30° × modifier.
  - UpsideDown test: up.Z < 0.01.
  - AnimBlend MaxVelocity 2000.
- **PSEUDOCODE:**
```
UpdateRoll(RightLeft):  RB.ApplyLocalAngularAcceleration( (1.0*RightLeft + 1*(-RB.LocalAngVel.Z)), 0, 0 )   // rad/s², local X (roll)
UpdateTurn(dt, FrameOfReference=(0,CameraYaw,0)):
  q* = Quat(FrameOfReference); if dot(q*,q)<0: q* = -q*
  d  = inv(q) * q*
  w  = AxisWithAngle(d) * (0.05, 0.05, 1) / dt  -  RB.LocalAngVel
  RB.ApplyLocalAngularVelocity( w * (ShouldUpright ? (1,1,1) : (0,0,1)) )
ShouldUpright = (NumContacts == 0) || (up.Z < 0.01)
IsUnstable    = |Pitch°| > 30 || |Roll°| > 30
```
- **ORIGINAL WFC BEHAVIOR:**
  - **On the ground, pitch and roll are not script-controlled.** They come entirely from the 4 spring forces following terrain, plus the small roll torque from strafe input.
    - Strafe right adds +1 rad/s² roll acceleration.
    - The current local yaw rate is subtracted from it, which gives lean opposite the yaw rate.
  - Yaw is matched to camera yaw every tick: the angular velocity is set to the full heading error per dt.
  - **In the air** (no probe contact) or when upside down, pitch and roll are also corrected, at **5 % of the error per tick**, as a velocity applied each tick.
  - The visible "lean" is mostly the additive animation `ADD_Nav_Hover_VEH`. `TnAccelerationAnimBlend` Tick:
    - Weights = ClampLength(Velocity, 2000) rotated into local space /2000, × max(0, up.Z).
    - child0 = 1 − |m|; directional children = max(0, ±sign·m²/|m|).
    - It is velocity-driven, not acceleration-driven, despite the class name.
- **CURRENT REBUILD COMPARISON:** Any procedural lean or pitch spring that the rebuild adds on top is not original. On the ground, attitude = physics + additive animation.
- **PRIMARY HANDOFF:** Gameplay (physics), Rendering/Animation (additive blend).
- **EXPERIMENTAL ASSERTION:** Grounded pitch and roll have no upright controller. Airborne upright correction is 5 % per tick. Dash refuses or cancels when |pitch| or |roll| > 30°.

## P3 — Velocity / heading / lateral grip
- **CONFIDENCE:** CONFIRMED
- **FUNCTION:** `TnHoverCarSimulation.Update`, `UpdateStrafe`, `Strafe`, `CalculateDriftScale`, `UpdateTerminalVelocity`. Boost: `TnWheelAssembly` / `TnTire`, `TnCarSimulation.UpdateAngularDamping`.
- **PSEUDOCODE (Hovering):**
```
Update: Suspension; TerminalVelocity; if Dashing: UpdateDash else UpdateStrafe; UpdateRoll; UpdateTurn(camera yaw)
UpdateStrafe:
  Drift = max(0, Drift - dt)
  Stab  = (up.Z)^2
  MaxAccel = MaxLinearAccel(3000) * (1 - Drift/0.5)^2 * Stab
  Strafe(dt, (Fwd, Right, 0), mask (1,1,0), MaxAccel, MaxLinearSpeed 1500)
Strafe: vLocal = RB.LocalLinVel*mask ; vDes = dir*SpeedModifier(MaxSpeed)*mask
        RB.ApplyLocalLinearAcceleration( ClampLength((vDes - vLocal)/dt, MaxAccel) )
TerminalVelocity: if Vz < -3500: add (0,0, -Vz-3500)
```
- **ORIGINAL WFC BEHAVIOR:**
  - **There is no separate lateral-grip model while hovering.**
    - Body-local X/Y velocity is driven toward stick × 1500 with a single |a| ≤ 3000 clamp that applies to both axes together.
    - With the stick released, the target is 0. The truck therefore brakes sideways and forward at the same ≤3000 UU/s².
  - Heading = camera yaw. Travel direction does not affect it.
  - Authority is scaled by (up.Z)², so tilted bodies have less grip.
  - After boost ends, authority ramps up over 0.5 s following (1−t/0.5)².
  - **Boost (Driving)** uses tire lateral force:
    - F = clamp(−v_lat · coeff · scale · Load, ±2·(M/4)·|g|), applied at the wheel contact.
    - Steering angle = steer · MaxSteeringAngle · π/180.
    - Ground angular damping = 5·(1−|steer|)².
    - `_Drifting` is never set by player code.
- **PRIMARY HANDOFF:** Gameplay.
- **EXPERIMENTAL ASSERTION:**
  - Hovering coast-down from 1500 reaches 0 in 0.5 s (3000 UU/s²) on flat ground.
  - Sideways stop uses the same deceleration as forward.

## P4 — Vehicle jump (JumpLinearSpeed 1200 at run time?)
- **CONFIDENCE:** CONFIRMED
- **FUNCTION:** `TnCarForm.Hovering.UpdateJumping` → `TnHoverCarSimulation.Jump`. `TnCarForm.Driving.UpdateJumping` → `TnCarSimulation.Jump`.
- **PSEUDOCODE:**
```
Hovering.UpdateJumping:
  if OnGround && T>0: T = max(0, T-dt)
  if !Jumping || T != 0 || !OnGround: return
  Hover.Jump(): RB.ApplyLinearVelocity((0,0, JumpLinearSpeed*mod))          // world +Z, ADDITIVE Δv = 1200
                RB.ApplyLocalAngularVelocity((0, -JumpAngularSpeed*mod, 0))  // Δω = -1.0 rad/s local pitch axis
  T = TimeBetweenJumps = 0.3*mod ; JumpFX ; PlayAscendSound ; force feedback
Driving (boost) Jump: ApplyLocalLinearVelocity(JumpLinearVelocity (600,0,1400)) + local ang (0,-2.0,0); JumpTimeRemaining 0.7
```
- **ORIGINAL WFC BEHAVIOR:**
  - **Yes, 1200 is used at run time** (`get_JumpLinearSpeed` = Blueprint.JumpLinearSpeed × modifier). HoverTruck_Physics does not override it.
  - It is an **added** world-Z velocity change, not a set velocity.
  - The cooldown counts down only while on the ground (0.3 s).
  - Boost-mode jump uses a different, body-local (600, 0, 1400) and 2.0 rad/s pitch.
- **PRIMARY HANDOFF:** Gameplay.
- **EXPERIMENTAL ASSERTION:**
  - Hover jump Δvz = +1200 (additive).
  - Pitch kick −1.0 rad/s.
  - 0.3 s ground-time cooldown.
  - Ballistic apex for a pure hop from rest: 1200²/(2·1940.4) ≈ 371 UU above the rest height, before the springs re-engage.

## P5 — Hover Dash direction
- **CONFIDENCE:** CONFIRMED
- **FUNCTION:** `TnTruckForm.Hovering.DoDash` → `TnHoverCarSimulation.Dash`, `UpdateDash`, `Strafe`.
- **CONSTANTS:**
  - Direction **(1,0,0) body-local** for the truck.
  - DashSpeed 3000, DashDuration 0.5.
  - DashAcceleration = DashDeceleration = **100000** × modifier.
  - Cooldown 2 s (pass 2).
- **PSEUDOCODE:**
```
DoDash (Truck): Hover.Dash((1,0,0)); PlayBoosterSound
Dash(dir): if SimMode==0 or IsUnstable: return ; DashTime=0.5 ; DashDirection=dir
UpdateDash: if IsUnstable: DashTime=0 else DashTime=max(0,DashTime-dt)
  a = DashTime>0 ? 100000 : 100000 ; vmax = DashTime>0 ? 3000 : 1500
  Strafe(dt, DashDirection, mask (1,1,1), a, vmax)       // NOTE mask includes Z
```
- **ORIGINAL WFC BEHAVIOR:**
  - The dash goes **along the truck's local forward**. Because heading is slaved to camera yaw, local forward is camera-yaw forward, **pitched/rolled with the body**. Stick direction is ignored.
    - The generic `TnCarForm` dash picks the dominant stick axis. The truck overrides this.
    - The plane form dashes ±Z.
  - Because the mask is (1,1,1), lateral and vertical local velocity are driven to 0 during the dash. Acceleration of 100000 makes this effectively instant: 3000 is reached in one 30 Hz tick.
  - On the tick where DashTime reaches 0, velocity is snapped toward forward·1500, with lateral and vertical removed. Normal strafe resumes after that.
- **PRIMARY HANDOFF:** Gameplay.
- **EXPERIMENTAL ASSERTION:**
  - Dash vector = body forward.
  - Lateral and vertical velocity zeroed during the dash.
  - Exit velocity = forward 1500.

## P6 — Fine Aim camera offset semantics (TnScreenSpaceOffsetByPitchCameraBehavior)
- **CONFIDENCE:** CONFIRMED
- **FUNCTION:**
  - `TnScreenSpaceOffsetByPitchCameraBehavior.Update`, `GetCameraOffset`, `GetPitchFractionOfLimits`, `BuildCurves`
  - `HmCurveVector.Build`
  - `HmC2SmootherV.Smooth`
  - `TnLocationOffsetCameraBehavior`
  - `HmOrbitUpdateLocationRotationCameraBehavior`
- **PSEUDOCODE:**
```
f = clamp((pitch_deg - PitchMin)/(PitchMax - PitchMin), 0, 1)
target = curve.Eval(f)        // keys at InVal i/(n-1); CurveAutoClamped-style: end tangents 0, inner (next-prev)/2, InterpMode 3
LocationOffset = C2Smooth(LocationOffset, target, SmoothTime, dt)
Result.OrbitLocationOffset += LocationOffset
-- later --
OrbitLocationOffset base = (-CurrentOrbitDistance, HorizontalOffset 0, VerticalOffset 0)
CameraLocation = Anchor + (OrbitLocationOffset >> CombinedRotation)       // rotated by full camera rotation (yaw+pitch)
Anchor = Pawn.Location + COMoffset>>rot + (Offset(0,0,200) - COMoffset)>>anchorRot
C2Smooth(from,to,T,dt): T'=T/2; ω=2/T'; x=ω·dt; e=1/(1+x+0.48x²+0.235x³)
   c=from-to; tmp=(vel+ω·c)·dt; vel=(vel-ω·tmp)·e; return to+(c+tmp)·e
```
- **ORIGINAL WFC BEHAVIOR:**
  - The offset is a **camera-space (orbit-space) translation**, not a projection shift: X = toward the pawn along the view axis, Y = right, Z = camera-up.
    - Default (150, 300, {150, −35, 150} at pitch −75/0/75, smooth 0.3) moves the camera 150 forward from the 800 orbit, 300 right, and 150 up when looking down or up.
    - Fine aim (−50, 300, {80, −35, 80}, smooth 0.1) puts the camera **50 farther back** than the base orbit.
  - The FOV narrows separately (45).
  - The smoother is Unity-style critically damped with SmoothTime **halved** internally.
- **PRIMARY HANDOFF:** Gameplay/Camera.
- **EXPERIMENTAL ASSERTION:** Fine-aim X −50 means farther from the pawn, not closer. The offset is rotated by camera pitch.

## P7 — Hand-shrink control (Optimus right hand)
- **CONFIDENCE:** CONFIRMED
- **FUNCTION:** `TnArmAttachment.Initialize`, `Update`, `UpdateHand`, `ShouldEquipHand`, `ShouldAlwaysEquip`.
- **CONSTANTS:**
  - Robot_ANIMTREE `SkelControlSingleBone` "HandSkelControl" on R_Arm04_Hand_XB.
  - BoneScale set to **0.1** in script.
  - Strength switches 0↔1 with **blend time 0.0**.
- **PSEUDOCODE:**
```
Initialize: HandBoneControl = FindSkelControl('HandSkelControl'); HandBoneControl.BoneScale = 0.1
Update (per tick): UpdateArm(); UpdateHand()
UpdateHand: SetSkelControlStrength( ShouldEquipHand() ? 0.0 : 1.0 , 0.0 )
ShouldEquipHand = ShouldAlwaysEquip() || ActiveWeapon.IsHandRequired()
ShouldAlwaysEquip = (no weapon) || !weapon.IsAttached() || (weapon.IsHolstered() && !weapon.IsEquipping())
```
- **ORIGINAL WFC BEHAVIOR:**
  - The hand bone is scaled to 0.1 **instantly**, on the same tick that the weapon becomes attached and not holstered (or not mid-equip).
  - It is restored instantly when no weapon is drawn, during holster, or when the weapon requires a hand.
  - There is no fade.
- **PRIMARY HANDOFF:** Rendering/Animation.
- **EXPERIMENTAL ASSERTION:** Hand scale is binary 1.0/0.1 with a 0 s blend, evaluated every tick.

## P8 — Ram / Nitro impulse and knockback (source re-check)
- **CONFIDENCE:** CONFIRMED (script). Damage numbers are from pass 2.
- **FUNCTION:**
  - `TnTruckForm.AttemptToRam`, `CalculateRamDamage`
  - `TnAcrobaticsManager.Rammed`, `RammedReaction`
  - `Pawn.TakeDamage`
  - `TnPawn.InVehicleForm.AddVelocity`
- **PSEUDOCODE:**
```
Ram (only while Driving/nitro, target mass <= 1000): CalculateRamDamage -> 175/300 (+buff modifiers); momentum dir + 7000 Z
Robot victim: TnAcrobaticsManager.Rammed -> RammedReaction state(6): Physics=Falling(4), MaxAirSpeed=RammedSpeed,
              Velocity = dir*RammedSpeed + baseVel, for 0.5 s; EndState restores air movement, Velocity=(0,0,baseVel.Z)
Generic damage momentum: Pawn.TakeDamage: Momentum /= Mass ; (extra-Z rule if DamageType.bExtraMomentumZ) ; AddVelocity
Vehicle victim: TnPawn.InVehicleForm.AddVelocity(v): Mesh.AddLinearVelocity(v * 0.5)
```
- **ORIGINAL WFC BEHAVIOR:**
  - Knockback on robots is a scripted 0.5 s forced-velocity state, not an impulse. Horizontal velocity is cancelled at the end.
  - Vehicles receive half of the momentum/mass as an RB velocity change.
- **PRIMARY HANDOFF:** Gameplay.
- **EXPERIMENTAL ASSERTION:**
  - Robot ram reaction lasts 0.5 s; after it, horizontal velocity = 0.
  - Vehicle victims get ×0.5 Δv.

## P9 — Transform vehicle-clip hidden geometry (~39.5 m below, ~17 frames, V→R)
- **CONFIDENCE:**
  - CONFIRMED for the visibility mechanism.
  - PARTIAL for the frame overlap, because the clip bone keys are not in the executable and were not decoded in this lane.
- **FUNCTION:** `TnAnimNotify_ToggleHidden.Notify`, `TnPawn.InVehicleForm.BeginState`, `TnPawn.InRobotForm.BeginState`, `TnVehicleForm.Initialize`.
- **PSEUDOCODE:**
```
ToggleHidden.Notify: if Option==0 (Toggle_Show, default) SkelComp.SetHidden(false) else SetHidden(true)
Transform_ToRobot_VEH (1.1667 s): ToggleVehicleFx @0.0 ; ToggleHidden(Toggle_Hide) @0.6634 s
```
- **ORIGINAL WFC BEHAVIOR:**
  - During V→R the vehicle mesh stays visible only until **t = 0.6634 s** of the vehicle clip, divided by Rate (Rate = 4 when downed).
  - The notify then hides the mesh. Nothing re-shows it before `InRobotForm.BeginState`, which hides it again at the end.
  - Geometry the clip parks far below the truck after 0.6634 s is therefore never rendered in the original.
  - The ~17 frames the rebuild sees must be checked against this hide time:
    - 0.6634 → 1.1667 s = 0.503 s ≈ 15 frames at 30 fps, or ~17 frames if sampled at ~33.8 fps or with clip-relative rounding.
  - **Do not edit the animation.** Honour the notify.
- **PRIMARY HANDOFF:** Rendering/Animation (honour notifies), Experimental (verify the overlap).
- **EXPERIMENTAL ASSERTION:** The vehicle mesh is hidden from 0.6634 s/Rate in V→R, so offset-below frames after that point are not visible.

## P10 — Transformation mesh visibility cross-check
- **CONFIDENCE:** CONFIRMED (Optimus clips, notify data + script)
- **DATA (Optimus):**
| clip | length | notify | time | effect |
|---|---|---|---|---|
| Transform_ToVehicle_ROBO | 2.0 | ToggleHidden (Toggle_Hide) | 0.8796 | robot hidden |
| Transform_ToVehicle_VEH | 2.0 | ToggleHidden (Show, default) | 0.3958 | vehicle shown |
| Transform_ToRobot_ROBO | 1.1667 | ToggleHidden (Show) | 0.0984 | robot shown |
| Transform_ToRobot_VEH | 1.1667 | ToggleHidden (Toggle_Hide) | 0.6634 | vehicle hidden |
- **ORIGINAL WFC BEHAVIOR:**
  - Both form meshes start each transform in the state their last stable form set (`In*Form.BeginState`). Form `Initialize` hides both.
  - Transform states do not change visibility. Only notifies do.
  - Overlap windows:
    - **R→V 0.396–0.880 s** (both visible).
    - **V→R 0.098–0.663 s** (both visible).
  - All times are divided by the transform Rate (4 when downed).
  - The end-of-transform `In*Form.BeginState` enforces the final state.
  - The rebuild's quoted windows match exactly.
- **PRIMARY HANDOFF:** Rendering.
- **EXPERIMENTAL ASSERTION:** It can now assert the exact notify times and the Rate scaling.
