# WFC native walking / step-up / ledge / falling — 2026-10-01 (follow-up pass)

Everything in this note is native PPC in `default.xex`, read with headless Ghidra (read-only snapshot) because ReVa was down.
Labels: CONFIRMED = read from decompiled code. HIGH = code plus stock-UE3 structure. INFERRED = bit/field naming guess.

## Key structural fact (CONFIRMED)
WFC moved the stock `APawn` fields `MaxStepHeight` / `WalkableFloorZ` into the struct
`Engine.Pawn._WorkingMovementCapabilities` (`Engine.Pathing.MovementCapabilities`).
In native memory the struct sits at pawn+0x200:

| offset | field | robot form value (Default__TnRobotForm, used by Optimus) |
|---|---|---|
| +0x200 | MaxStepHeight | **35** |
| +0x204 | MaxFallHeight | 3400 (AI/pathing) |
| +0x208 | MaxJumpHeight | set by ApplyTransformer = Acrobatics JumpHeight (500) |
| +0x20C | WalkableFloorZ | **0.7** (≈45.57°) |
| +0x210 | bitfield bJumpCapable, bHighJumpCapable, bCanJump, … (MSB-first, INFERRED order) | |

`TnPawn.Transforming.BeginTransformation → SetMovementCapabilities(TargetForm.FormMovementCapabilities)` swaps the struct per form.
Vehicle form: MaxStepHeight 35, WalkableFloorZ 0.7, bCanJump false. The vehicle uses RB physics, so these don't apply to it.
Other APawn offsets confirmed in passing: GroundSpeed +0x2F8, AirSpeed +0x300, AccelRate +0x308, AirControl +0x318, Controller +0x1D4, Base +0x68, Physics byte +0x64.

Native function map (APawn vtable at 0x820A8398; TnPawn-family vtables share the same physics entries):

| addr | function | vtable slot | conf |
|---|---|---|---|
| 0x82F9C598 | APawn::physWalking (WFC rewrite) | +0x23C | CONFIRMED |
| 0x82F71D88 | APawn::physFalling | +0x238 | CONFIRMED |
| 0x82F65358 | APawn::stepUp | +0x250 | CONFIRMED |
| 0x82F6F838 | APawn::CheckForLedges | +0x384 | CONFIRMED |
| 0x82F701C0 | APawn::CalcVelocity (native) | +0x3A8 | CONFIRMED |
| 0x8275C240 | AHmPawn::CalcVelocity override → script event, fallback native | +0x3A8 in 2 vtables | CONFIRMED |
| 0x827993D8 | event thunk (interface vtable +0x2D4) → script `CalcVelocity` | — | HIGH |
| vt +0x230 / +0x234 | processHitWall / processLanded | | HIGH |
| vt +0x220 / +0x388 | setPhysics / startNewPhysics | | HIGH |
| vt +0x394 | slide-delta helper used by physFalling | | HIGH |
| 0x82FA5068 | TwoWallAdjust | | HIGH |
| 0x82C2C5C8 | ULevel::MoveActor | | HIGH |
| 0x82C16E10 | ULevel::SingleLineCheck (trace flags 0x20DF/0x22DF/0x2086) | | HIGH |

Constants: MAXSTEPHEIGHTFUDGE / floor gap **2.0** (0x82034160), MAXSTEPSIDEZ **0.08**, LEDGECHECKTHRESHOLD **4.0** (0x823FBB3C),
physFalling max substep **0.05 s**, 8 iterations max, minimum air-control speed 10.0, zero epsilon 1e-4.

## 1. Walking = one-pass "lift → sweep → drop" (CONFIRMED, WFC-specific)
WFC's physWalking is **not** the stock iterative UE3 walker. There are no 0.05 s substeps: it does **one pass per tick** with the full dt.
```
physWalking(dt):
  if !Controller && !bRunPhysicsWithNoController: Velocity=Accel=0; return
  Velocity.Z = 0; Accel.Z = 0
  CalcVelocity(AccelDir, dt, MaxSpeed = vt+0x334 (GroundSpeed x MaxSpeedModifier),
               Friction = PhysicsVolume.GroundFriction)          // -> HmPawn hook -> TnPawn.CalcVelocity (script)
  Delta = (Velocity [+ ZoneVelocity*25 if volume flag]) * dt
  Up    = (0,0, MaxStepHeight + 2)                              // 37 UU for robots
  if Delta == 0: just re-check floor
  else:
     if Controller && Controller.WantsLedgeCheck():             // vt +0x358 on controller
         Delta = CheckForLedges(AccelDir, Delta, GravDir, bCheckedFall, bMustJump)
     // horizontal sweep done LIFTED by Up -> automatic step-up of anything <= MaxStepHeight+2
     Sweep(Loc+Up -> Loc+Up+Delta)
     on hit (up to 3 sweeps total):
         if hit Base-chain actor / pawn: bump events (vt+0x1F4/0x1F8)
         SlideDelta = Delta - N*(Delta.N) + N*2.0                // slide along wall, pushed out 2 UU
         re-sweep with SlideDelta; second hit -> slide again along new normal (+2 UU push)
         if final wall normal.Z < WalkableFloorZ: processHitWall(N)  -> script HitWall (TnPawn.InRobotForm.HitWall -> RobotForm.HitWall)
         movement truncated so the cylinder stops 2 UU short of the contact
  // DROP: trace down from lifted end point to (end - Up): reach = MaxStepHeight + 2 below the start height
  Floor = trace(Lifted end -> end - Up)
  final position = floor hit, pulled back 2 UU along the trace (stands 2 UU above floor)
  Unwalkable-slope case (Floor.Z < WalkableFloorZ and Delta.N < 0): re-trace along slope-projected delta
  Low-friction slope slide: if Floor.Z < 0.99 && GroundFriction*Floor.Z < 3.3:
        extra slide of GravityZ*dt*dt / (max(0.5,GroundFriction)*2) along the slope plane   (ice-type volumes only)
  if bMustJump || no floor in reach || Floor.Z < WalkableFloorZ:      -> LEDGE / FALL (section 3)
  else: MoveActor(final - start); Floor = N; set Base (mover check)
        Velocity = (newLoc - oldLoc) / dt  (X,Y only); Velocity.Z = 0; (|comp| < 1e-4 -> 0)
```
Consequences for the rebuild:
- **Step-up height = MaxStepHeight + 2 = 37 UU** (0.37 m) for the robot. It is **instant**: the pawn pops up within one frame, with no vertical easing and no step-up speed limit.
- **Step-down / ground snap = 37 UU.** Walking off anything lower stays glued to the floor. Anything deeper than 37 UU makes the pawn fall.
- **Walkable slope limit**: Floor normal Z ≥ 0.7. Steeper surfaces are walls: you slide along them and start falling once nothing walkable lies under the cylinder.
- **Wall sliding** is a projection: Delta − N(Delta·N), plus 2 UU push-out, at most 3 sweeps per frame. Velocity is rebuilt from the actual displacement, so the into-wall component is lost each frame.
- Walking movement is **single-step, not substepped**, so very low frame rates give larger sweeps. Velocity integration itself is the script CalcVelocity (explicit, clamped).

## 2. stepUp (APawn::stepUp 0x82F65358, CONFIRMED)
Used by the falling/flying movers (it is not called by WFC's walker, which steps through the lifted sweep).
```
Down = GravDir * (MaxStepHeight + 2)
if (-(HitN . GravDir) < 0.08) || HitN.Z >= WalkableFloorZ:   // NOTE: signed test (stock uses Abs) -> overhangs count as steps
    MoveActor(-Down); MoveActor(Delta)                        // step up, then move
elif Physics != Walking:
    Delta.Z += |Delta| * HitN.Z  ; MoveActor(Delta); bStepDown = false   // ramp-climb
if Hit.Time < 1:
    processHitWall; if Physics == Falling: return
    N.Z = 0; normalize
    NewDelta = (Delta - N*(Delta.N)) * (1 - Time)
    if NewDelta.Delta >= 0: MoveActor(NewDelta); if hit: processHitWall; TwoWallAdjust; MoveActor
if bStepDown: MoveActor(Down)
```
The stock recursive "step again" branch (MINSTEPSIZESQUARED) is absent.

## 3. Ledges (CONFIRMED structure; bit names INFERRED)
- `CheckForLedges` (0x82F6F838) runs only if `Controller.WantsLedgeCheck()` is true.
  In stock UE3 the player version returns `bIsWalking || bIsCrouched`. WFC has no walk/crouch button on Xenon, so it is normally **false for the player** (HIGH).
  AI controllers use it to stop or skirt ledges.
  Algorithm: probe ahead to Loc + Delta + AccelDir·Radius, then trace down `CollisionHeight + max(MaxStepHeight, Radius+|Delta|) + 4`.
  If there's no floor or the floor Z < WalkableFloorZ: `Controller.StopAtLedge()` (vt+0x35C) returns zero delta.
  Otherwise it tries the two perpendiculars (±(Delta.Y, −Delta.X)) for a walkable direction; otherwise it sets bCheckedFall, bMustJump = caps.bCanJump.
  **WFC removed `eventMayFall`**: the string "MayFall" does not exist in the exe.
- Floor lost in physWalking (no floor within 37 UU, or floor too steep, or bMustJump):
  ```
  if !bCheckedFall && !bJustTeleported && !bMustJump &&
     ( !caps.bCanJump || ( !bCanWalkOffLedges && (bIsWalking || bIsCrouched) ) ):   // bit test 0x20000000 / 0x20000 / 0x40000000|0x10000000
        STOP AT LEDGE: Velocity = Acceleration = 0; Controller.MoveTimer = -1
  else WALK OFF:
        MoveActor to the lifted-sweep end point
        Velocity.Z = Base's velocity Z (0 on static floor)    // horizontal velocity kept
        setPhysics(PHYS_Falling, floor normal (0,0,1))       // -> script Falling / acrobatics
        startNewPhysics(remaining = (1 - moved/|Delta|) * dt) // rest of the frame continues as falling
  ```
  Robot form has bCanJump = true and the player is never "walking", so **the player robot always walks off ledges.** There is no edge-stop.
  Ledges up to 37 UU are simply stepped down.
- On the script side, when falling starts, `TnRobotForm` / AcrobaticsManager pick the falling animation. Landing anims depend on fall height and speed:
  SharedAcrobatics LandingAnims MinHeight/MinSpeed 1200/1200 (blend 0.65, blocks movement), 1000/1200 (0.25),
  4500/0 (0.6, blocks), 500/0 (0.4), 250/0 (0.25).

## 4. Falling / jump integration (CONFIRMED)
```
physFalling(dt, Iterations):
  if !rootMotion:
     AirControl test: if AirControl > 0.05, trace the air-control displacement; if blocked -> TickAirControl = 0  (no wall-climbing by air control)
     maxAccel = AccelRate * TickAirControl; if |Vel2D| < 10: maxAccel += (10-|Vel2D|)/dt;
     if |Vel2D| >= GroundSpeed && TickAirControl <= 0.05: maxAccel = 1
     Acceleration clamped to maxAccel
  while remaining > 0 && Iterations < 8:
     t = min(0.05, remaining)                                   // 0.05 s substeps
     OldVel = Velocity
     CalcVelocity(dt=t, MaxSpeed = AirSpeed)                    // script TnPawn.CalcVelocity: gravity + clamp to -TerminalVelocity
     Delta = 0.5*(OldVel + NewVel)*t  (+ 0.5*ZoneVelocity*t)    // trapezoidal = exact for constant gravity
     MoveActor(Delta)
     if hit:
        if HitN.Z >= WalkableFloorZ: Velocity = Delta/t; processLanded(remaining) -> PHYS_Walking   // landing
        else processHitWall; slide (vt+0x394), TwoWallAdjust; land if the slide finds a walkable floor
             (or the two-wall "crease" case where both normals face up and oppose -> treated as landed)
     if still falling: Velocity = (actual displacement)/t, clamped to vt+0x178 (max fall speed)
```
Jump: `JumpZ = sqrt(2*|g|*JumpHeight)` (script). With trapezoidal integration in ≤0.05 s substeps, the apex is exactly JumpHeight (Optimus **500 UU**) at any frame rate.
**Jump height is frame-rate independent.** The only frame-rate effect is the ≤0.05 s collision substep.
Air wall-slide removes the into-wall velocity (velocity is rebuilt from the displacement).

CalcVelocity hook (resolves last pass's UNKNOWN):
- Walking: MaxSpeed = vt+0x334 (GroundSpeed × MaxSpeedModifier).
- Falling: MaxSpeed = **AirSpeed** (Optimus 1200).
- `AHmPawn::CalcVelocity` (0x8275C240) calls the script event unless skeletal root motion is active (Mesh+0x310 RootMotionMode 1 or 3, Mesh+0x311 ≠ 2, and a pawn flag).
  If the script returns false, it falls back to native APawn::CalcVelocity.
- Interaction worth knowing: physFalling pre-scales Acceleration by AccelRate·AirControl, but TnPawn.CalcVelocity then does `ClampLength(Acceleration,1)`.
  The air-control *magnitude* is therefore effectively discarded. Only its direction and the zero case (blocked air control) matter.
  Air steering is governed by AccelRate/(1+P) (12000 for Optimus when not over speed). This is HIGH; validate against the original's feel.

## GAMEPLAY / EXPERIMENTAL HANDOFF
- Robot step-up: instant pop of up to **37 UU**. Ground snap down to 37 UU. Walkable floor normal Z ≥ **0.7**. Steeper surfaces behave as walls.
- Walls: project the delta onto the wall plane, push out 2 UU, at most 3 sweeps; velocity = actual displacement/dt.
- Ledges: the player robot **always walks off**. Keep horizontal velocity, set Vz = 0, switch to falling for the remainder of the frame. No ledge-stop, no MayFall.
- Falling: 0.05 s substeps, max 8. Trapezoidal position integration. Gravity −2940. Terminal velocity −6000 (Optimus). Land when the floor normal Z ≥ 0.7.
- Air steering: script CalcVelocity with MaxSpeed = AirSpeed 1200; momentum InAir table only when over AirSpeed.
- Walking: one physics pass per tick. The rebuild can keep its fixed-step loop, but the step and snap limits should be 37 UU.
