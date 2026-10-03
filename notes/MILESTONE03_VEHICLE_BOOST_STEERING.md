# MILESTONE 03 — HoverTruck BOOST steering / turn authority (2026-10-02)

**Question:** while boosting, does left/right turning authority really feel restricted in WFC, or is that a reconstruction error?

Sources (all read-only):
- UnrealScript bytecode via `tools/ue3dis.py`:
  - `TnCarForm`, `TnTruckForm`, `TnCarSimulation`, `TnWheelAssembly`, `TnTire`, `TnSuspension`;
  - `TnPlayerController`, `HmPlayerInput`, `Engine.PlayerInput`, `HmPlayerController`;
  - `TnCameraStrategyManager`, `TnDrivingOrbitRotationCameraBehavior`.
- Authored data from `AssetTools/manifests/authored.db`.
- Shipped decoded config `ExtractedAssets/config/Coalesced_ini/.../Xe-TransInput.ini` and `Xe-TransGame.ini`.
- Comparison target: `Rebuild-Gameplay` @ 0762f01 (`src/game/CharacterMovement.cpp` vehicleStep, `src/game/PlayerController.cpp`, `src/core/Config.h`). Not modified.

All of this vehicle logic is script, not native.

## Summary answer
- **Boost is a completely different control model from hovering.** Hovering slaves the body yaw to the camera, strafes with the left stick, and lets the right stick turn the camera.
- **Boost = `TnCarForm.Driving` → `TnCarSimulation`:** a 4-wheel car.
  - Front wheels steer up to **25°**.
  - Tires produce lateral force.
  - **The steering input is the RIGHT stick X (`aTurn`)**, curved `s·|s|`.
  - The camera yaw is **locked to the truck's yaw**.
  - **The LEFT stick X does not steer during boost.** It only becomes `RollControl` (barrel-roll direction). The truck has no barrel roll (RollDuration 0), so the left stick only feeds a weak leveling torque.
- **What is authentic:**
  - turning with the left stick in boost does essentially nothing;
  - half stick gives only 25 % steering (squared curve);
  - **Nitro** (Dash during boost) cuts steering to **30 %** for 3 s.
- **What is not authentic:** if the tester steers with the right stick, the current rebuild has *more* yaw authority than WFC, not less. It is instantaneous 180°/s at full stick, against roughly 100–137°/s peak in WFC after a 0.25–0.5 s build-up. The rebuild's lateral grip is also stiffer.
- **Conclusion:** the rebuild's yaw dynamics are wrong (provisional), but in the opposite direction from "too stiff". The "stiff" report most likely comes from left-stick steering (authentic: no steering) or from Nitro (authentic: 0.3×). See the comparison section below.

---

## CONFIDENCE
- **CONFIRMED (bytecode + config + authored data):**
  - input routing, steering curve, wheel steering, tire law, angular damping;
  - Nitro, camera yaw lock, state transitions, air control;
  - all constants listed below.
- **HIGH:**
  - per-wheel static Load = (M/4)·|g| (same implicit spring as the hover probes);
  - `bEnableFOVScaling` = false (absent from the shipped ini, so the class default applies). This makes FOVScale = 1.
- **MODELLED (not a recovered value):** the yaw-rate / slip numbers in the table. They come from a planar simulation of the recovered force laws: static loads, no roll, pitch or load transfer.

## ADDRESSES / FUNCTIONS (script)

| function | role |
|---|---|
| `TnPlayerController.PlayerInCarForm.SetLocalInputs` | StrafeForwardBack = RawJoyUp, StrafeLeftRight = RawJoyRight, **SteeringInput = TnPlayerInput.GetNormalizedTurn()**, ViewRotation = controller rotation |
| `HmPlayerInput.PreProcessInput` / `ApplyDeadZone` | radial 0.25 deadzone on (aTurn, aLookUp); `aTurn = aStrafe` **only if !ShouldStrafe()**, but `TnPlayerController.ShouldStrafe()` = **true**, so no remap |
| `Engine.PlayerInput.PlayerInput` | aTurn *= LookRightScale (× FOVScale) |
| `HmPlayerInput.GetNormalizedTurn` | clamp(aTurn / LookRightScale, −1, 1), i.e. the deadzoned right-stick X |
| `TnCarForm.Hovering.UpdateBoosting` | Boosting && (SimMode==0 \|\| !Hover.IsDrifting) → GotoState('Driving') |
| `TnCarForm.Driving.BeginState / UpdateBoosting` | _Boosting = true, CarSimulation.Activate (JumpTimeRemaining 0, linear damping 0); boost released → 'Hovering' (Hover.Activate + Drift 0.5 s) |
| `TnCarForm.Driving.OnRigidBodyCollision` | contact normal · forward > CosCollisionNormalThreshold → 'Hovering' |
| `TnCarForm.Driving.UpdateSimulationInputs` | Accelerator = 1, **Steering = Sign(s)·s²**, RollControl = StrafeRightLeft |
| `TnCarForm.Driving.DoUpdate` | Jumping, Rolling, Sounds, SimulationInputs, `CarSimulation.Update(dt, ViewRotation)`, visual wheels, Boosting |
| `TnTruckForm.Driving.DoUpdate / UpdateNitro / StartNitro / StopNitro` | Dash during boost → Nitro |
| `TnCarSimulation.get_Steering` | _Steering · _SteeringScale |
| `TnCarSimulation.Update` | wheels → terminal velocity → (SimMode≠0) AngularDamping → [!Rolling: AirControl, Leveling] → Drag → Boost |
| `TnWheelAssembly.Update / UpdateSteering / UpdateTransform / UpdateTire` | per wheel |
| `TnTire.UpdateLateralForce` | lateral force law |
| `TnCarSimulation.UpdateAngularDamping` | ground yaw damping |
| `TnCarSimulation.UpdateAirControl` | airborne steering |
| `TnCameraStrategyManager.CarFormDriving` → `TnDrivingCameraStrategyType` | camera in boost |
| `TnDrivingOrbitRotationCameraBehavior.Update` | **OrbitRotation.Yaw = Pawn.Rotation.Yaw** |

## CALLERS / CALLEES
`PlayerController.PlayerTick` → `PlayerInput` (scaling) → `PlayerInVehicleForm.PlayerMove` → `ProcessInput` → `SetLocalInputs`.
Then `TnCarForm.OnUpdate` → `Driving.DoUpdate` → `TnCarSimulation.Update` → `TnWheelAssembly.Update` ×4 → `TnTire.Update`.

## STATE VARIABLES
- `TnCarInputState._Steering`, `_StrafeRightLeft`, `_StrafeForwardBack`, `_Boosting`, `_Dashing`, `_Jumping`.
- `TnCarSimulation._Steering`, `_SteeringScale` (1.0; Nitro 0.3), `_SpeedScale` (1.0; Nitro 1.5), `_Accelerator` (1), `_RollControl`, `_JumpTimeRemaining`, `_AnyWheelOnTheGround`.
- `TnWheelAssembly._SteeringAngle` (rad), `_LocalSpaceVelocity`.
- `TnTire._LateralForce`, `_LateralForceScale` (1, or DriftFrictionScale when `_Drifting`; never set by player code).
- `TnTruckForm._NitroTimeRemaining`.
- `TnCarForm._Boosting`, `_TimeBeforeNextJump`.

## CONSTANTS
- **Input:**
  - `XboxTypeS_RightX → aTurn` (Speed 1, DeadZone 0); `XboxTypeS_LeftX → aStrafe` (`^BARRELL_ROLL_DIRECTION`).
  - HmPlayerInput.DeadZone **0.25**, radial with aLookUp: `v' = n·(min(1,|v|) − 0.25)/0.75`.
  - LookRightScale 300 and the TnLookScales ramp (StepThreshold 0.95, BelowStepMultiplier 0.52) **cancel** in GetNormalizedTurn.
  - FOVScale = 1 (HIGH).
- **Truck_Physics** (`VEH_SHARED_p.Truck_Physics`, TnCarPhysicsBlueprint):
  - Mass 2500;
  - Inertia (22.7e6, 46.4e6, **58.9e6**);
  - COM (−47, 0, 20);
  - MaxAcceleration 2500, MaxSpeed 3000;
  - AngularDamping **5.0** (class default);
  - AirControlTurnAcceleration **12** rad/s², AirControlStrafeAcceleration **2600**;
  - JumpLinearVelocity (600, 0, 1400), JumpAngularVelocity 2.0;
  - RollDuration **0** (no barrel roll).
- **Wheels:**
  - front (±126 Y, +83 X) MaxSteeringAngle **25°**, DriftFrictionScale 0.8;
  - rear (±137 Y, −177 X) MaxSteeringAngle 0, DriftFrictionScale 0.5;
  - all wheels: TireFrictionCoefficient **0.0015**, WheelRadius 45, Truck_Suspension K 120000, D 8000, RestingLength 30.
  - The axles are symmetric about the COM: a = b = 130 UU, wheelbase 260.
- **Tire:**
  - per-wheel MaxForce = 2·(M/4)·|g|, with |g| = 1940.4 (−2940 × 0.66);
  - Load = max(0, suspension force) ≈ (M/4)·|g| at rest;
  - the force saturates at a wheel lateral slip of 2/0.0015 = **1333 UU/s**;
  - lateral relaxation rate Σcoef·Load/M = 0.0015·|g| ≈ **2.91 s⁻¹** (time constant 0.34 s).
- **Nitro:**
  - NitroSteeringScale **0.3**, NitroSpeedScale **1.5**;
  - NitroDuration **3.0 s**, TimeBetweenNitros **8.0 s**;
  - adds camera state TnPCS_Boosting (FOV 100, orbit distance 650).
- **Other car constants:**
  - JumpBoostDuration 0.7;
  - TerminalVelocity 3500, LandingVelocity 2000, LandingTraceDistance 1000;
  - PitchForwardLimit −25°, PitchForwardAcceleration 3;
  - SineBoostScale angles sin 0.5 / 0.866;
  - LowSpeedBoostScale 8, LowSpeedBoostThreshold 0.5, MaxExtraAcceleration 5000;
  - RollCorrectionAngularAcceleration 50.
- **Boost camera** (`Truck_Optimus_STRATEGY`):
  - TnDrivingOrbitRotationCameraBehavior MatchRotationSpeed 3.0, PitchVelocityBlend 1.0, PitchRange −25..25;
  - HmOrbitSmoother SmoothTime **0.25** (hover 0.1);
  - FOV 85 (Nitro 100);
  - orbit 1050 (Nitro 650).

## PSEUDOCODE
```
// input (each frame)
(rx, ry) = radialDeadZone(RightStickX, RightStickY, 0.25)
steerIn  = clamp(rx * FOVScale(=1), -1, 1)                      // GetNormalizedTurn
// Driving.UpdateSimulationInputs
Steering    = sign(steerIn) * steerIn^2                           // stick 0.5 -> 0.25
RollControl = LeftStickX(raw aStrafe)                            // NOT steering
SteeringEff = Steering * SteeringScale                            // 1.0, Nitro 0.3
// TnCarSimulation.Update
for wheel in 4:                                                   // same Steering to all; rear MaxSteeringAngle 0
   wheel.SteeringAngle = SteeringEff * MaxSteeringAngle * pi/180  // front ±25°
   wheel frame = body rotation * yaw(SteeringAngle); vLocal = PointVelocity(wheelPos) in wheel frame
   suspension spring along wheel -Z; Load = max(0, springForce)
   F = clamp(-vLocal.Y * 0.0015 * LateralForceScale(1) * Load, ±2*(M/4)*|g|)
   ApplyLocalForce((0, F, 0) in BODY space, wheelLocalPos + (0,0,-SuspensionLength))   // below COM -> roll torque
if SimMode != 0:
   AngularDamping = 5 * (anyWheelDown ? (1-|SteeringEff|)^2 : 1)                         // full lock -> 0 yaw damping
   if not rolling:
      if no wheel down:  linAcc += yawRot(0, SteeringEff*2600, 0);  angAcc.z += SteeringEff*12
                         if Pitch > -25°: localAngAcc.y += 3
      Leveling(RollControl)        // only when |RollControl|>0.1: roll accel sign(Roll)*50*0.5*(1-Up.Z)
   if on ground: drag -v̂·v²|g|/TV², forward boost accel (Lerp(2500, drag(MaxSpeed), fwd/MaxSpeed) + extra) * BoostScale * 1
// camera (boost)
Camera.Yaw = Pawn.Yaw  (then OrbitSmoother 0.25)  ; right-stick Y only biases pitch inside ±25°
```

## ORIGINAL NORMAL DRIVING (Hovering) — earlier note P2/P3, unchanged
- **Heading:** body yaw = camera yaw every tick.
- **Right stick:** turns the camera (HoverTruck strategy YawSpeed 50°/s, RampSpeedMultiplier 2.5).
- **Left stick:** strafes in body space, toward 1500 UU/s with |a| ≤ 3000.
- **No tire or slip model.**

## ORIGINAL BOOST (Driving)
- **Steering input:**
  - Steering stays enabled for the whole boost. There is **no start lockout and no phase change**: startup, sustained and ending phases all use the same law.
  - Steering comes from the **right stick X**, after the radial 0.25 deadzone, through `s·|s|`.
  - The left stick X does not steer.
  - There is no steering clamp other than |s| ≤ 1, no speed-dependent steering scale, and no input smoothing.
- **Steering authority:**
  - It comes only from the 25° front-wheel angle and the tire forces.
  - The camera is not followed. The camera follows the truck instead (`Camera.Yaw = Pawn.Yaw`, 0.25 s smoothing).
- **Heading and velocity:**
  - Body yaw comes from the tire torques (yaw inertia 58.9e6).
  - The velocity vector rotates only through the tire lateral forces, so the **velocity lags the heading**.
  - Lateral velocity relaxes at about 2.9 s⁻¹ and saturates at a total of 2|g| ≈ 3880 UU/s².
  - At speed, a hard turn becomes a slide (slip angle 20–36° in the model), and forward speed bleeds off.
- **Speed dependence:**
  - The authority is emergent. In the linear regime the yaw rate is about u·tanδ/L (neutral steer, since a = b).
  - Above roughly 1500 UU/s, lateral acceleration is grip-capped (2|g|).
- **Damping:**
  - Yaw damping is 5·(1−|s|)²: none at full lock, 5 s⁻¹ with the stick released.
  - Releasing the stick lets the yaw rate decay; it does not stop instantly.
- **Body roll:** tire forces are applied at the contact point (below the COM), so the body rolls physically on the stiff springs. No animation limit on steering was found.
- **Jump during boost:** body-local Δv (600, 0, 1400) plus pitch −2 rad/s, with JumpTimeRemaining 0.7 (FX only).
- **Airborne steering:** the same `s` gives 12 rad/s² world-yaw acceleration and 2600 UU/s² yaw-relative strafe.
- **Leaving boost:** release → Hovering with Drift 0.5 s. Hover authority ramps back as (1−t/0.5)², and boost can't be re-entered until the drift ends.
- **Modelled response** (planar sim of the recovered laws, from straight-line speed u0, Nitro off):

| u0 | stick | yaw rate at 0.1 / 0.25 / 0.5 / 1.0 / 3.0 s (°/s) | slip at 1 s |
|---|---|---|---|
| 1000 | 1.0 | 18 / 46 / 82 / 112 / 97 | 20° |
| 3000 | 1.0 | 48 / 101 / 137 / 108 / 98 | 36° |
| 3000 | 0.5 | 12 / 21 / 27 / 28 / 27 | 6° |

## ORIGINAL DASH (Hovering only)
- `TnTruckForm.Hovering.DoDash` → body-forward hover dash: 3000 UU/s for 0.5 s, 2 s cooldown (earlier note P5).
- It does not exist while boosting.

## ORIGINAL NITRO / RAM (Dash pressed while boosting, truck only)
- **Conditions:** `_Dashing && !IsUsingNitro && CanUseSpecialMove`.
- **Effect:** SpeedScale 1.5 (MaxSpeed 4500) and **SteeringScale 0.3** for 3.0 s. The cooldown is 8 s.
- **Visuals:** Ram FX, and the TnPCS_Boosting camera (FOV 100, distance 650).
- **Ram:** RamState = 1 (ram damage on collision).
- **Ends** when the time runs out or boost is released (Driving.EndState → StopNitro).
- **During Nitro, steering authority really is cut to 30 %:** full stick acts like 0.55 stick normally.

---

## CURRENT REBUILD COMPARISON (Rebuild-Gameplay 0762f01, read-only)

| aspect | rebuild | original | verdict |
|---|---|---|---|
| Steering source | look X (`padRX`) or mouse (PC); left stick ignored in Driving | right stick X; left stick = RollControl only | **MATCHES** for pad |
| Deadzone | none on `padRX` | radial 0.25 with right Y, rescaled | **DIFFERS** (minor) |
| Input filter | exponential, τ 0.08 s [PROV] | none | **DIFFERS** |
| Curve | `s·|s|` | `s·|s|` | MATCHES |
| Nitro scale | 0.3 | 0.3 (SpeedScale 1.5, 3 s, 8 s cooldown) | MATCHES |
| Steering authority | `angVel.z = steer · π` set directly (180°/s at full lock, instant) [PROV] | front-wheel 25° and tire forces; peak ≈100–137°/s after 0.25–0.5 s, sustained ≈97°/s while sliding | **DIFFERS** (rebuild is faster and instant) |
| Heading | yaw integrated from the forced rate | emergent rigid-body yaw | **DIFFERS** |
| Velocity rotation / lateral inertia | lateral velocity decays at 8 s⁻¹ (capped 2g) [PROV] | ≈2.91 s⁻¹ linear relaxation, per-wheel saturation at 1333 UU/s slip, applied at the wheels | **DIFFERS** (rebuild grips about 2.7× harder, so less slide) |
| Yaw on release | snaps to 0 (rate overwritten each tick) | decays with damping 5·(1−|s|)² and the tire aligning torque | **DIFFERS** |
| Angular damping | applied, then overwritten by the forced rate on the ground | 5·(1−|s|)², the only ground yaw damping | DIFFERS (in effect) |
| Air control | 12 rad/s² yaw, 2600 strafe, pitch assist | same | MATCHES |
| Camera following | orbit yaw follows truck; no stick yaw in Driving | Camera.Yaw = Pawn.Yaw, smoothing 0.25 s | MATCHES (smoothing not checked) |
| State transitions | boost ↔ hover with drift gate; frontal-hit drop | same | MATCHES |

**Verdict on "stiff boost turning":**
- **Authentic:**
  - no turning from the left stick during boost;
  - the squared curve: 50 % stick gives 25 % steering;
  - Nitro's 0.3× steering.
- **Reconstruction error, but in the other direction:** with the right stick, the rebuild's yaw authority is higher than WFC's and instant.
  - The trajectory feels "on rails" because the provisional lateral grip (8 s⁻¹) keeps the velocity glued to the heading. WFC slides noticeably (≈2.9 s⁻¹, slip 20–36° at speed).
  - The extra 0.08 s input filter and the missing deadzone are also non-original.

## GAMEPLAY HANDOFF
Replace the provisional Driving ground yaw-rate / lateral-grip block with the recovered wheel and tire model. Keep everything else in Driving as is.
1. **Input:**
   - `steerIn` = radial deadzone 0.25 applied jointly to (padRX, padRY), rescaled `(|v| − 0.25)/0.75`, clamped to 1.
   - No temporal filter on pad input. The PC mouse path is out of scope and stays provisional.
   - `steer = sign·steerIn²`, then × SteeringScale (Nitro 0.3).
2. **Each tick, for 4 wheels** at body-local positions FL (83, −126), FR (83, 126), RL (−177, −137), RR (−177, 137), z 21, relative to COM (−47, 0, 20 − ChassisOffset):
   - δ = steer·MaxSteeringAngle (front 25°, rear 0) in radians.
   - Wheel frame = body ∘ yaw(δ).
   - v_w = point velocity of the wheel position, expressed in the wheel frame.
   - Load = max(0, suspension force). Use the existing spring; ≈ (M/4)|g| at rest.
   - F = clamp(−v_w.y · 0.0015 · Load, ±2·(M/4)·|g|).
   - Apply body-space force (0, F, 0) at (wheelPos − (0, 0, suspensionLength)). Rotate it to world space, and apply both linear and angular parts (yaw inertia 58.9e6, mass 2500).
   - Note: the original applies the force along **body** +Y, not the steered wheel's lateral axis (`ApplyLocalForce((0, F, 0), …)` in body space). Reproduce that literally.
3. **Do not set the angular velocity.** Integrate the yaw from the torques. Apply angular damping `5·(1−|steer|)²` when any wheel touches, else 5.
4. **Remove** `kDriveTurnRate` and `kDriveLateralGrip`. Lateral behaviour must come only from step 2.
5. **Keep as is:** forward boost acceleration/drag, air control, Nitro, jump, transitions and the camera yaw lock.

## STILL UNKNOWN
- The exact PhysX angular-damping integration form (assumed `ω *= max(0, 1 − c·dt)`) and the physics substep rate.
- Dynamic load transfer and suspension force under cornering. The modelled table assumes static loads.
- Whether any additive animation (VEH_Car_ANIMTREE) adds visual lean in Driving. No steering limit was found in the animation code that was read.
- PC mouse → aTurn scale for boost steering (keyboard/mouse bindings not analysed).
