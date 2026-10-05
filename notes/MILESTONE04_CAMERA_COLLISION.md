# WFC third-person camera collision / obstruction (2026-10-03)

**Sources:**
- UnrealScript bytecode: `TransGame.TnThirdPersoncollisionCameraBehavior` (robot), `TransGame.TnAvoidClippingCameraBehavior` (vehicles / turrets), `Engine.Actor.TraceCamera` (native).
- Authored strategy objects in `CAM_*_Strategies_p` (`authored.db`).
- Native primitive trace filter `0x82E287C0` (default.xex).

**Key point:** the obstruction logic is **script**, not native. It is the **last behaviour** in each camera strategy, so it runs after orbit, offset, smoothing, recoil, wiggle and shake.

## Which behaviour runs (CONFIRMED)

| strategy | collision behaviour | constants |
|---|---|---|
| Robot `OverTheShoulder_STRATEGY` (also Spectate, Death, Death_Vehicle) | `TnThirdPersoncollisionCameraBehavior` | class defaults `_QuickMoveSpeed` **2000**, `_SlowMoveSpeed` **500** UU/s (instances override nothing) |
| Vehicles (`HoverTruck_Optimus`, `Truck_Optimus`, cars, tanks, planes) | `TnAvoidClippingCameraBehavior` | per instance `_OriginOffset`: HoverTruck / Truck Optimus **(−200, 0, 75)**; Quick **2000**, Slow **500**. The class default is 1000 / 200, overridden on every vehicle instance |
| Turrets | `TnAvoidClippingCameraBehavior` | `_OriginOffset` (0, 0, 200), class-default speeds |

For context, the robot's desired camera before collision comes from:
- anchor = pawn + (0, 0, 200) (`HmOffsetAnchorPointRelativeToActor`);
- orbit distance **800** (100 in fine aim with sniper / heavy pistol / burst rifle);
- the screen-space offset curve (X 150, Y 300, Z 150 / −35 / 150 over pitch −75..75);
- smoothing.

## Trace primitive

**`Actor.TraceCamera(HitLocation, HitNormal, TraceEnd, TraceStart, bTraceActors, Extent, …)`** is native.

### Trace shape
Every call omits `bTraceActors` (script default false), so only world geometry is traced. **Pawns, weapons, vehicles, movers and other non-world actors are not traced.** HIGH: stock UE3 meaning of bTraceActors = false.

Two shapes are used:
- **zero-extent ray** (origin → desired clip-plane centre);
- **axis-aligned box** sweeps / overlap tests whose half-extent is the world AABB of the camera's near-plane rectangle:
  - local half-extent `(0.01, tan(FOV/2)·100, tan(FOV/2)·100 / max(1, aspect))`;
  - rotated by the camera rotation;
  - AABB taken of the 8 rotated corners.

### Flags
- **CONFIRMED:** the native primitive filter `0x82E287C0` has a WFC-specific trace flag **0x2000000** that accepts a primitive only if its `PrimitiveComponent.BlockCameras` is set (`+0xF0 & 0x4`).
- **CONFIRMED:** filter flag 0x4000000 rejects `ForcePawnSeeThrough` (`+0xF0 & 0x2`) primitives and actors.
- **HIGH:** `TraceCamera` is the trace that sets 0x2000000. The exec native's function pointer is registered at runtime (natives slot 0x837116CC is empty in the image), so the exact flag word is **PARTIAL**.

### What obstructs (BlockCameras authored data, CONFIRMED)
- `PrimitiveComponent` default `BlockCameras = True`.
- **252 Streets SMCA meshes and 8 InterpActor components are authored `BlockCameras = False`.** All of them are also `CollideActors = False` and `BlockZeroExtent = False` (non-colliding decorative props). **They do not obstruct the camera.**
- BlockingVolumes: `BrushComponent0` has `BlockCameras = True` (68 Streets volumes also author `BlockZeroExtent = True`; BlockNonZeroExtent comes from the Volume default). **Invisible player blockers DO obstruct the camera** (HIGH).
- Generic Volumes / TriggerVolumes have `BlockCameras = False` and do not obstruct.
- Thin / one-sided surfaces: BSP and static meshes are traced by the engine's collision (static-mesh collision geometry / BSP). One-sidedness of the render mesh is not a factor (HIGH, stock).
- Pawns are `ForcePawnSeeThrough` (Pawn default) and never world geometry, so they are ignored.

## Robot algorithm (`TnThirdPersoncollisionCameraBehavior.Update`, CONFIRMED script)

```
In: Result (desired camera Location/Rotation from the earlier behaviours), DeltaTime
R      = Result.Rotation ; F = forward(R)
Desired= Result.Location + F*100                 // near-clip-plane centre (100 UU in front of the camera)
Origin = Target.Location                         // pawn location (cylinder centre); no offset for the robot
Ext    = AABB half-extent of near-plane box (see above)

if IsClearPath(Origin, Desired):                 // ray Origin->Desired hits nothing AND box overlap at Desired hits nothing
    Clip = Desired
else:
    SmoothTimeRemaining = 1.0                    // seconds
    OffCS = (Desired - Origin) in camera space (R)
    Up    = R up axis
    dUp   = BoxSweep(Origin, Origin + Up*OffCS.Z)               // distance to first hit (or full length)
    Diag  = (OffCS.X, OffCS.Y, 0) rotated by R                  // horizontal (camera-plane) part of the offset
    P     = Origin + Up*dUp
    dDiag = BoxSweep(P, P + Diag)
    Clip  = P + normalize(Diag)*dDiag
Cam = Clip - F*100                               // camera stays 100 UU behind the clip-plane centre

// smoothing in target space: T = (rotation R, translation Target.Location)
SmoothTimeRemaining = max(0, SmoothTimeRemaining - DeltaTime)
O = inverse(T) * Cam
if !OldValid or SmoothTimeRemaining == 0: Old = O ; OldValid = true      // no smoothing once 1 s has passed without obstruction
D = O - Old
Old.X += sign(D.X) * min(|D.X|, (D.X < 0 ? Slow : Quick) * dt)          // moving back (away from the pawn): 500 UU/s ; forward: 2000
Old.Y += sign(D.Y) * min(|D.Y|, (D.Y > 0 ? Slow : Quick) * dt)          // +Y: 500, -Y: 2000
Old.Z += sign(D.Z) * min(|D.Z|, (D.Z > 0 ? Slow : Quick) * dt)          // up: 500, down: 2000
Result.Location = T * Old
```

### ORIGINAL BEHAVIOUR (robot)
- **When obstructed:** the camera is **not** pulled straight in along the line to the pawn.
  - It first rises along camera-up from the pawn centre, as far as the camera-space Z offset allows (box sweep).
  - Then it sweeps horizontally toward the desired offset, ignoring the vertical part.
  - So it ends above and toward the desired spot, stopped at the first box hit.
- **Shortening:** limited by the box sweep's hit distance. **There is no minimum distance:** the clip centre can reach the pawn centre, putting the camera 100 UU behind it along the view direction.
- **Interpolation:**
  - while obstructed and for **1.0 s after** the last obstructed frame, movement is rate-limited per axis in pawn camera space: toward the pawn / downward / −Y at **2000 UU/s**, away / upward / +Y at **500 UU/s**;
  - so it pulls in quickly and recovers slowly;
  - after 1 s with a clear path the offset **snaps** to the desired value each frame (the rate limiter is bypassed).
- **Starting inside geometry:** the ray or box overlap reports a hit, so the fallback runs.
  - If the pawn origin is itself inside collision, the up and horizontal sweeps can return 0 and the clip centre equals the origin. PARTIAL: the engine's start-inside sweep result is not traced.
- **Robot ↔ vehicle transformation:** the camera strategy switches (OverTheShoulder ↔ HoverTruck strategies, `TransitionTime` 1.5 s / 1.0 s). Each behaviour's `Activate` clears the smoothing state (`_OldOffsetIsValid = false`). Blending between strategies is `HmCamera`'s; that weight curve is PARTIAL here.

## Vehicle algorithm (`TnAvoidClippingCameraBehavior`, CONFIRMED script)

The same as the robot, except for these differences:
- **`Origin = Target.Location + (_OriginOffset rotated by Target.Rotation)`.** For the Optimus truck forms that is (−200, 0, 75) local: behind and above the vehicle origin.
- **Two candidates when obstructed:**
  - `0` **diagonal:** BoxSweep(Origin, Origin + R·(OffCS.X, OffCS.Y, 0.5·OffCS.Z)), placed at Origin + normalize(dir)·dist;
  - `1` **up, then back:** dUp = BoxSweep(Origin, Origin + Up·OffCS.Z); dBack = BoxSweep(P, P + Back·(−OffCS.X)) with Back = R·(−1, 0, 0); placed at P + Back·dBack.
  - Weight = (1 − min(1, |cand − Desired|·0.002)) + min(1, |cand − Origin|·0.002). The higher weight wins; a tie keeps index 0.
- **Smoothing is always active** (there is no 1 s window):
  - X: Slow (500) when Diff.X < 0, else Quick (2000);
  - **Y: always Slow (500)**;
  - Z: Slow when rising, Quick when falling.

## GAMEPLAY HANDOFF
1. **Replace the provisional "snap to near pawn" logic** with the per-strategy algorithm above.
   - Robot: origin = pawn location, rise-then-horizontal fallback, 1 s smoothing window.
   - Vehicles: origin = vehicle + rotated `_OriginOffset`, two ranked candidates, always smoothed.
   - Constants 2000 / 500 UU/s. Near-plane distance 100 UU. Box half-extent from the FOV and aspect as given.
2. **Collision set:**
   - world geometry only (BSP, static meshes, BlockingVolumes);
   - exclude components with `BlockCameras = False` (the 252 + 8 Streets props listed in authored data);
   - ignore pawns, weapons, vehicles and movers.
3. The ray uses zero extent; sweeps and the final overlap test use the near-plane AABB extent.
4. On a strategy change (transform), reset the smoothing state.

## STILL UNKNOWN / PARTIAL
- The exact native trace-flag word of `TraceCamera` (only the BlockCameras gate 0x2000000 is proven to exist in the filter).
- The engine's result for sweeps that start inside geometry.
- HmCamera's strategy-transition blend curve.

## Addendum 2026-10-05: TraceCamera flag word (native, resolves the PARTIAL above)
- `execTraceCamera` = `0x82F21BA0`, registered at runtime by `0x83652420` (natives table slot `0x837116CC`).
- Parameters: HitLocation, HitNormal, TraceEnd, TraceStart (default: actor location), bTraceActors (default: an actor flag), Extent (default 0), one optional bool (default false), HitInfo.
- Body `0x82F1B5D8`:
  - flags = `World` (bTraceActors false) or `ProjTargets`-style set (true);
  - `| 0x800` if the optional bool is set (H: TRACE_Material, used to fill HitInfo.PhysMaterial);
  - `| 0x0A000000` always: **0x02000000 = the BlockCameras gate** (CONFIRMED in the filter) plus 0x08000000 (meaning unknown);
  - then `UWorld::SingleLineCheck` (`0x82C16E10`).
- **No complex/per-poly collision bit is ever set.** H: TRACE_ComplexCollision is 0x20000 in this UE3 generation.
- So the camera ray uses each static mesh's simple collision (`UseSimpleLineCollision` / `UseSimpleBoxCollision` defaults true), and box sweeps use simple box collision.
- **The camera clips into render geometry that has no simple collision. That is authentic.**
