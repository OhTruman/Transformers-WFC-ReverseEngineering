# Milestone 05: Gameplay unknowns closed from script (2026-10-03)

**Scope:** Phase 8 of the long pass. These are items Gameplay's `FIDELITY.md` lists as PROVISIONAL or UNKNOWN (read-only). Every item comes from UnrealScript bytecode (`work/script/decomp`) plus authored defaults (`authored.db`).

**Labels:**
- **CONFIRMED** = read directly.
- **HIGH** = one inference step.

---

## 1. Transformation: mesh visibility, timing, blends (replaces `kTransformHandoffFrac = 0.5` PROVISIONAL)

### State flow (`TnPawn`, CONFIRMED)

**`TnPawn.Transform(TargetForm, CompleteEvent)`:**
1. If `!_TransformingEnabled`, refuse.
2. When going to vehicle, `DropHeavyWeapons()`.
3. `MoveToSafeTransformationLocation`.
4. Enter state `TransformingToVehicle` or `TransformingToRobot`.

**`Transforming.BeginTransformation(TargetForm, Transformation, CollisionMode)`:**
- `_CurrentForm = TargetForm`;
- `CollisionController.SetCollisionMode(4` to vehicle, `1` to robot`)`;
- `Transformation.Execute(!bPlayDownedAnimation)`;
- `SetMovementCapabilities(target)` (**the target form's movement applies from the first frame**);
- noise (`TransformNoiseRadius`) and an AI stimulus.

**`TnTransformation.Execute(bFaster)`** (`Rate` = 4.0 if downed-fast, else 1.0):
1. `SourceForm.EndPlay()` → robot: detach Targetable / LightEnv / BodyImpact, acrobatics off, unequip melee, hide attached destructibles. Vehicle: `PlayExitSound`, detach Targetable / BodyImpact / LightEnv.
2. `TargetForm.Activate()` → **attaches the target mesh component** and makes it `Pawn.Mesh`.
   - Vehicle target: clamp velocity to **3500 UU/s**, place the RB at the pawn, `SetLinearVelocity`.
   - Robot target: collision size, acrobatics on, and `AcrobaticsManager.Fall()` on the authority.
3. **Source** form animation `get_SourceAnimationName()`, BlendIn **0.115 s**, BlendOut 0. **Target** form animation, BlendIn 0, BlendOut **0.25 s**. (`TnTransformation` defaults `_BlendInTime 0.115`, `_BlendOutTime 0.25`; no subclass or instance overrides.)

| direction | source clip | target clip |
|---|---|---|
| Robot→vehicle | `Transform_ToVehicle_ROBO` | `Transform_ToVehicle_VEH` |
| Vehicle→robot | `Transform_ToRobot_VEH` | `Transform_ToRobot_ROBO` |

   - Animation params: `RootMotionMode 2`, `Priority 1`, `Override 2`, `PlayRate = Rate`.
4. **`Duration = min(len(source clip), len(target clip)) / Rate`**; `RemainingTime = Duration`.

**Ticking:**
- `Update`: `RemainingTime -= dt`. At ≤ 0 → `OnTransformationComplete`: `SourceForm.Deactivate()` (detaches the source mesh) and `TargetForm.BeginPlay()` (robot: `SetHidden(false)`; vehicle: `PlayEnterSound`).
- `TransformingTo*.OnUpdate`: once the transformation is inactive → `GotoState('InVehicleForm' / 'InRobotForm')`.

### Visibility (HIGH; script-complete, no notify-driven toggles checked)

| component | where it is hidden / shown |
|---|---|
| Vehicle mesh | hidden at `TnVehicleForm.Initialize`; shown only in **`InVehicleForm.BeginState`** (which also hides the robot mesh) |
| Robot mesh | hidden at `TnRobotForm.Initialize` and in `InVehicleForm.BeginState`; shown in **`InRobotForm.BeginState`** (which hides the vehicle mesh) and in `TnRobotForm.OnBeginPlay` (completion) |

- **So during the whole transformation only the *source* form's mesh is visible**, playing its fold clip. The target mesh is attached and animating, but hidden.
- **The swap is a single hard cut at completion**: target shown and source hidden in the same frame (`BeginPlay` + state `BeginState`).
- There is **no alpha cross-fade and no mid-point handoff**. The rebuild's `kTransformHandoffFrac = 0.5` should become **1.0** (swap at the end of `min(len)/Rate`).
- PARTIAL: AnimNotifies inside the four transform clips were not inspected (not in authored.db). A notify-driven visibility toggle would be the only way this differs.

### Other timing (CONFIRMED)

- **Robot weapon returns** (to-robot only) once `RemainingTimeAsFactor ≤ _RestoreWeaponTransformFractionRemaining = 0.75`, i.e. after **25 %** of the transform has elapsed and the weapon isn't still equipping (`InvManager.RestoreRobotWeapon`).
  - When going to vehicle, the robot weapon is stored at the start and the vehicle weapon is restored at once.
- **Collision cylinder:**
  - to robot: `TransformingToRobot.UpdateCylinderSize` lerps each frame between robot and vehicle radius / half-height by `RemainingTimeAsFactor` (vehicle size → robot size);
  - to vehicle: `VehicleForm.OnActivate` sets the vehicle cylinder at once.
- **Safe-location shift** (`MoveToSafeTransformationLocation`):
  - `FindSpotAwayFromPawns(target extent)`. If the pawn must move and the target is the robot, the meshes are offset by `(Old − Safe)` in pawn space and that offset decays linearly to 0 over **0.5 s** (`_TransformBlendTimeRemaining`, `OffsetMeshes`). The collision jumps; the visuals slide.
  - Then `SetLocation(Safe)` and `VehicleForm.Teleport(Safe, Rotation, Velocity)`.
- **Downed fast transform:** `Rate 4.0` when `bPlayDownedAnimation` is false (the `Execute(!bPlayDownedAnimation)` argument).

---

## 2. High-speed vehicle → robot: momentum carry-over (CONFIRMED script + authored data)

- **Vehicle → robot keeps the pawn velocity.** Nothing resets it: `VehicleForm.OnEndPlay` only rescales it (×0.1 of the RB velocity) when the vehicle motion is keyframed, i.e. on non-authoritative copies (HIGH).
- `RobotForm.OnActivate` calls `AcrobaticsManager.Fall()` on the authority. The robot leaves the transform falling or in air control, keeping its speed.
- Robot movement then runs **`TnPawn.CalcVelocity`**, the script override of `HmPawn.CalcVelocity` (HIGH that the native walking/falling physics calls it):
```
if |_OverrideAcceleration|² > 0: Velocity += OverrideAccel*dt; return
Mask = (Physics==Falling||Walking) ? (1,1,0) : (1,1,1)
Prev  = Velocity*Mask
DesN  = ClampLength(Acceleration*Mask, 1)                       // input direction, |.|<=1
Desired = |DesN|==0 ? (Physics==Falling ? Prev : 0) : Normal(DesN) * max(450, |DesN|*MaxSpeed)
P = MomentumPreservation:  0 if no MomentumBlueprint or |Prev| < MaxSpeed + 0.1
    else Params = (Physics==Falling || IsTransforming) ? MB.InAir : MB.OnGround
         P = dot(Normal(DesN),Normal(Prev)) > 0.866 ? Params.Forward : (|DesN|==0 ? Params.Neutral : Params.Backward)
MaxAccel = AccelRate / (1 + P)
LocalAcc = ((Desired - Prev)/dt) in pawn space, each axis clamped to ±MaxAccel   // per-axis box clamp, not a vector clamp
Velocity = Prev + (LocalAcc back to world)*dt
if Physics==Falling: Velocity.Z = max(oldZ + GravityZ*dt, -TerminalVelocity)
```
- **Optimus** (`TR_Optimus_ROBODEF_p.Optimus_ROBODEF`):
  - `BaseGroundSpeed 1400`, **`AccelRate 12000`**, `AirSpeed 1200`, `AirControl 0.4`, `TerminalVelocity 6000`;
  - `MomentumBlueprint TR_Acrobatics_p.TruckTransformerMomentum`: **OnGround Forward 7, Neutral 3, Backward 1; InAir Forward 100, Neutral 100, Backward 5**.
- **Other blueprints:**

| blueprint | OnGround F / N / B | InAir F / N / B |
|---|---|---|
| Car (Bumblebee, Sideswipe, Spider) | 7 / 3 / 1 | 100 / 100 / 5 |
| Plane | 5 / 3 / 0.5 | 1000 / 50 / 3 |
| Tank | 3 / 2 / 1 | 200 / 100 / 3 |
| Brute | Neutral 1 | Neutral 1 |

- **Effect for Optimus above robot top speed** (derived from the formula; HIGH):

| situation | max acceleration per axis |
|---|---|
| on ground, holding forward | 12000 / 8 = **1500 UU/s²** (slows slowly) |
| on ground, no input | 12000 / 4 = **3000 UU/s²** (decelerates toward 0) |
| on ground, steering away (> 30° off velocity) | 12000 / 2 = **6000** |
| in air or **while transforming**, forward / neutral | 12000 / 101 ≈ **119 UU/s²** (speed essentially preserved) |
| in air or while transforming, backward | 12000 / 6 = 2000 |
| below 1400.1 UU/s | P = 0, full 12000 |

- `MaxSpeed` here is the native caller's argument (ground or air speed of the current form): PARTIAL.
- **Robot → vehicle:** `TnVehicleForm.OnActivate` clamps the carried velocity to **3500 UU/s** and pushes it into the vehicle RB (`SetLinearVelocity`) when the vehicle simulates (`Physics == 10` and not keyframed).

**Gameplay handoff:**
1. Keep the pawn velocity through the transform.
2. Use the target form's movement capabilities from the first frame.
3. Apply the `CalcVelocity` momentum rule above with the per-character MomentumBlueprint (InAir params during the transform).
4. Vehicle entry clamps to 3500.

---

## 3. KOTH (Power Struggle) zone rotation (replaces Gameplay's "UNKNOWN: what triggers KOTH rotation")

`TnKingOfTheHillZoneBase` (CONFIRMED script). Defaults: `ZoneActiveTime 60`, `ScoreInterval 1`, `PointsPerInterval 1`, `MarkerString "Active Node"`, `AnnouncerMatchStartHysteresisTime 3`, `DefenderTeamIndex 255`, `bHidden`.

**Setup:**
- `PostBeginPlay`: if the game has `TnGameRules_ScoreKingOfTheHill`, `InitialState = Inactive`; `AllOtherZones = all KOTH zones − self` (Streets has 5 zones: NetworkIDs 15, 8, 30, 43, 28).
- **`MatchStarting`** (at match start; HIGH that it comes from GameInfo.StartMatch): the first zone to receive it picks `InitialZoneIndex = RandRange(−1, len(AllOtherZones))`.
  - −1 activates itself; otherwise it activates that other zone.
  - Every zone gets `SetupInitialZone(active?)` and ignores the announcer for 3 s. Later MatchStarting calls are ignored (`Initialized`).

**Active state:**
- On entry: `ZoneActive`, `HasBeenActive`, `SetHidden(false)`, announcer `MP_HillMovedDialog`, `UpdateClaim(true)`;
- GRI `AddObjectiveMarker("Active Node", TnObjectiveMarkerTypeKingOfTheHill)`; `TnKingOfTheHillMessage` switch 3;
- attach the spawn modifier (−50 / d within 5000, so players don't spawn near the active hill).
- **Tick:**
  1. `ActiveTimeLeft −= dt`, `PeriodTimeLeft −= dt`, `UpdateClaim(false)`.
  2. Every **1 s**, `ScoreZone`: if the zone has a single owning team (not 255 none / 254 contested), **each living pawn in the zone** gives `Game.ScoreObjective(PRI, 1)` and adds personal zone score.
  3. When `ActiveTimeLeft ≤ 0` → **`ActivateNewZone()`**.
- **`UpdateClaim`**: over the living pawns in the zone, one team gives that team, two teams give 254 (contested), none gives 255. The result is applied with `SetTeam`, which fires `DefendingTeamChanged`:

| new owner | announcer | message switch |
|---|---|---|
| Autobot capture | `MP_HillCapturedAutobotDialog` | 0 |
| Decepticon capture | `MP_HillCapturedDecepticonDialog` | 1 |
| contested | `MP_HillContestedDialog` | 2 |
| neutral | `MP_HillNeutralDialog` | — |

  - Each change also sets `ActiveMesh` vector params `MaterialParamNames` to `CaptureColor[team]` or `NeutralColor`.
- **`ActivateNewZone`**:
  - candidates = other zones with `!HasBeenActive`; deactivate self;
  - if there are none, clear `HasBeenActive` on self and all others and activate a **random other zone**; otherwise activate a random candidate.
  - Each cycle therefore visits every zone once in random order before repeating, and the same zone never repeats back-to-back.
- **Inactive:** `ZoneActive = false`, `SetHidden(true)`, remove the marker, detach the spawn modifier.
- **End of game:** `ScoreKingOfTheHill.CheckEndGame` deactivates every zone.
- Pawn membership is maintained by `Touch` / `UnTouch` into `PawnsInZone`. Eligible = not dead.

---

## 4. Code of Power (single-flag CTF): `FlagCapturePoint._Active` driver and rounds

**`TnGameRules_SingleFlagCTF`** (CONFIRMED). Default: `TimeBetweenRounds 5`.
- First attacking team = `RandomInt(2)`; it alternates every round (`SetNextAttackingTeam` on `BetweenRounds` entry).
- `GRI.set_AttackingTeam` → HUD observer `TnHudDataObserverOnAttackingTeam` (`_global.NotifyOnAttackingTeamChanged`). The client also adds `TnHudDataObserverSingleFlagCTF` ("Returning the Code of Power").
- **`SetupRoundStart`** (on entering `Active`):
  - every `TnFlagCapturePointBase.ActivateIfMatchingTeam(AttackingTeam)` → **`SetActive(DefenderTeamIndex == attacking team)`**. The capture point owned by the attackers becomes `_Active` and gets the GRI marker (`TnObjectiveMarkerTypeFlagCapturePoint`); the others lose it.
  - every `TnGameObjectiveWeaponPickupFactory.ActivateIfMatchingTeam(DefendingTeam)` → the defenders' flag factory goes to state `Pickup`, the others go to `Sleeping` (holder cleared).
  - `TnCTFMessage` switch = attacking team index.
- **Score:** `FlagCapturePoint.Touch` while `_Active` with a pawn holding a `TnWeaponFlagBase` → `Game.ScoreObjective(PRI, 1)`, `Flag.OnScore()`.
- **Rounds** (`TnGameRules_RoundsBase`):
  - `MatchStarting` → `SetTimer(SyncTimerTime 10, SyncTimer)`, `GRI.SetActiveGameRule`, state Active.
  - **Active**: `TimeTillNextReset = Game.TimeLimit` (CTF: 240 / **300** / 360 s); `SyncTimer` mirrors it to the GRI countdown (HUD clock); `RunGameTimer = false` (**the GRI match clock is stopped; the round timer replaces it**).
    - Ticks down; at 0 → `EndRound`: `CurrentRound++`.
    - If `CurrentRound ≥ GRI.Rounds`, `EndGame(none, "Score")`; otherwise `TnRoundBasedGameMessage` 2 → **BetweenRounds**.
  - **BetweenRounds**: `TimeBetweenRounds 5 s`; `TnGame.RoundEnded()` (UI event 8 → `WaitingOnNextRound` → PreGameCountdown; `RespawnHelper.RoundEnded`). After 5 s: `TnGame.RestartRound()` (SoftReset, UI event 3, every player respawns), message 3, back to Active.
  - **Mercy rule** (`SingleFlagCTF.CheckMercyRule`, checked each Active tick): on the last round, if the team that attacks last already leads → `EndGame(none, "Score")`.
  - `GoalScore` (Rounds) must be even (error log otherwise).
- **A capture does not end the round** (HIGH: across all decompiled script, the only `EndRound` caller is `Active.RoundTimeUp`).
  - The capture goes `ScoreObjective` → `TnGameRules_ScoreObjectives` → `Scorer.AddScore(IndividualScore 10, team +1)` + XP event, plus `ScoreFlags` → `PRI.AddFlagScore()`.
  - Then `Flag.OnScore` → `HomeBase.ReturnSpawnedObjective(scorer, 3)` → message, sleep `GetReturnSleepTime(3)` → `Pickup` again.
  - **Attackers can capture repeatedly until the round timer expires.**

---

## HANDOFFS

### Gameplay
- §1: hard swap at the end of `min(len) / Rate`; blend-in 0.115 s / blend-out 0.25 s; weapon restored at 25 %; cylinder lerp to robot; 0.5 s mesh-offset decay after a safe-location move; downed rate ×4.
- §2: momentum carry and the per-axis acceleration clamp with MomentumBlueprint values; vehicle entry clamp 3500.
- §3: KOTH rotation (60 s, random unvisited zone; 1 point per living pawn per second while uncontested).
- §4: CTF attacker alternation, capture-point and flag-factory activation, round timer, 5 s between rounds, mercy rule.

### Rendering
- §1: no cross-fade. The source mesh is drawn until the swap frame.
- §3: KOTH `ActiveMesh` colour = `CaptureColor[team]` / `NeutralColor` vector params on `MaterialParamNames`.

### Systems
- Announcer cues for KOTH (§3); vehicle enter / exit sounds at transform start (exit) and completion (enter) (§1).

### Still open
- AnimNotifies inside the transform clips (could toggle visibility).
- `CalcVelocity`'s `MaxSpeed` source per physics mode (native).
- CTF `GetReturnSleepTime` per reason (not read).
