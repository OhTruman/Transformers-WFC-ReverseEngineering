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

---

## 5. HUD markers: player tags and objective markers (Canvas, not Scaleform)

**Hud_GFX itself draws only debug and lock-on markers** (`getMarkerClip`: `LockOn` → `mc_markerLockOn`, otherwise debug clips).

All gameplay markers are **Canvas material tiles** drawn by `TnObjectiveMarkerTypeSprite.Draw`:
- They are registered through `GRI.AddObjectiveMarker(Description, MarkerBase, MarkerTypeClass, DoNotReplicate)` → `_ObjectiveManager`.
- Materials live in `UI_HudMarkers_p`.
- All authored setups are in **`notes/data/objective_marker_types.json`**.

### Common sprite behaviour (CONFIRMED script + defaults)

**Placement:**
- Project `MarkerBase.Location + (0, 0, MarkerZOffsetWS)`.

**Off-screen:**
- Shown only if `DrawWhenOffscreen`.
- Direction from the canvas centre is flipped when the marker is behind the camera. The marker sits on the safe frame (`SafeFramePaddingPercent 0.08`).
- `RotationParam 'ArrowAngle'` = `acos(dir.y)·sign(dir.x) + 180`.
- Size `OffscreenMarkerSize 0.0625`.

**Focus:**
- Focused when the marker is within `DistanceFromCenterFocusThreshold` (default **0.0625**) of the screen centre, or within the type's auto-focus range.
- Focus is held for **`FocusHysterisis 0.2 s`**.

| | marker size | label | material params |
|---|---|---|---|
| focused | `FocusedMarkerSize` (0.05 typ.) | alpha fades with the hysteresis unless `DrawLabelWhenUnfocused` | `Over = 1`, `OnScreen = 1` |
| unfocused | `UnfocusedMarkerSize` | — | `Over = 0` |

- Sizes are fractions of the canvas (`SizeInPixels`). The label is drawn at `LabelOffset`, in `UI_TransEngineFonts_p.MarkerFont`.

**Label colours** (`TnObjectiveMarkerTypeSprite`):

| label | colour |
|---|---|
| Friendly | (80, 181, 213) |
| Enemy | (240, 60, 60) |
| Neutral | white |

### TDM player tags: `TnMultiplayerGame.TransformerMarkerClass = TnObjectiveMarkerTypeTransformerVersus`

**Registration:** every pawn registers it (`TnPawn` adds `GameClass.default.TransformerMarkerClass` with the character name).

**Hidden for:** yourself, and dead pawns.

**Marker type** (`GetEMT`): Ally = same team; Disguised = enemy with `TnBuffDisguise`; otherwise Enemy.

| type | setup | when drawn |
|---|---|---|
| **Ally** | `AllyMarkerSetup` (`MarkerAlly_MAT` + `TargetHealthBar_MAT`) | label always drawn; **off-screen only while that ally is downed** |
| **Enemy** | `EnemyMarkerSetup` (`MarkerEnemy_MAT`, size 0.03125, label colour (240, 20, 20)) | **marker disabled** (size 0) unless the viewer has `TnBuffSeeEnemyObjectiveMarkers` (and the target has no Warcry-derived buff), or the target is `TnBuffHardLocked` by the viewer or a teammate, or the target has `TnBuffRevengeMarker` |
| **Disguised** | ally setup | hidden without line of sight (`TnLineOfSightDetector.HasLOSToActor` from the player camera) |

- Enemy label: also hidden while the target is cloaked or out of line of sight.
- Label height for all types: `LabelZOffsetWS = collision height × 0.5`.

### Objective markers (state → material params)

**Domination** (`MPMarkerDominationNode_MAT`):

| point owner | `TeamID` | label colour | label |
|---|---|---|---|
| viewer's team | 0 | friendly | "Defend" |
| neutral (255) | 2 | neutral | "Capture" |
| enemy | 1 | enemy | "Capture" |

- `NodeID = PointNumber`; `Flashing = BeingCaptured`.

**KOTH** (`MPMarkerBase_MAT`, label "Active Node"):
- Owned by the viewer's team, or neutral / contested (index > 1): `Neutral = 1`, friendly label colour.
- Owned by the enemy: `Neutral = 0`, neutral label colour.
- Label: "Defend" if owned by the viewer's team, else "Capture".

**Flag capture point:**
- Shown only to a pawn carrying a `TnWeaponFlagBase`.
- `Neutral = 0`, `Flashing = 1`. Label only when focused.

**Carried objective** (flag `MPMarkerCOP_MAT`, bomb `MPMarkerBomb_MAT`):
- Not shown to the carrier itself.
- `IsAttacking = viewer team == GRI.AttackingTeam`.

| state | Neutral | Flashing | other |
|---|---|---|---|
| at factory | 0 attacking / 1 defending | 0 | — |
| dropped | 0 | 1 attacking / 0 defending | — |
| carried by a teammate | 1 | — | — |
| carried by an enemy | 0 | — | `PingOpacity` pulse `((2.5 − t mod 2.5) / 2.5)^5` |

- Label colour: friendly if `Neutral == 1`, else enemy, with alpha × pulse.
- Labels: Flag = Capture / Escort / Defend / Return / Kill; Bomb = Bomb / Escort / Kill.

**Flag/bomb factory marker timing** (`TnGameObjectiveWeaponPickupFactory.SetCurrentObjectiveHolder(Holder, AddMarker = true)`):
- The marker (and the objective spawn modifier) **follows the current holder**:
  - the factory itself while in `Pickup` (set in `Pickup.BeginState`);
  - the carrying pawn after pickup;
  - the dropped pickup when dropped;
  - none while `Sleeping` / inactive (`ActivateIfMatchingTeam` → `SetCurrentObjectiveHolder(none)`).
- On every change the old holder's marker is removed and the new one added in the same call.

**Tombstone** (`DeathIndicator_MAT`, size 0.03125, `FadeOutTime 3 s`): at each death location.

---

## 6. Pickups: "nothing to gain" rejection and factory mesh placement (replaces Gameplay `[PROV]` and Rendering "attach offset UNKNOWN")

### Accept / reject chain (CONFIRMED)

`PickupFactory.Pickup.ValidTouch`:
1. **Reject** if hidden.
2. **Reject** if the pawn can't pick up inventory.
3. **Reject** if the pawn has no Controller (recheck in 0.2 s).
4. **Reject** if the touch is through a wall: `FastTrace(pawn, factory)` fails (recheck in 0.5 s).
5. Then `Game.PickupQuery`.

`PickupQuery`:
- GameRules `OverridePickupQuery`: **none of the MP rules override it**.
- Then `InvManager.HandlePickupQuery`:
  - `ItemClass.static.PickupAllowed(pawn, pickup)`;
  - **no inventory item may `DenyPickupQuery`** (same-class weapon with full reserve ammo, or same-class projectile bag with maxed ammo).

`TnPickupFactory.Pickup.ValidTouch` additionally rejects non-AI pawns for `AiUseOnly` factories.

**`PickupAllowed` per type:**

| type | allowed when | on give |
|---|---|---|
| **Health** | `Health < HealthMax` | `HealDamage(AddedHealth, TnHealTypeHealthPickup)`. **The heal type is `SHT_AddAllSegments`, so `Health = max(Health, HealthMax)`: a full heal. The amount is ignored, so `AddedHealth = 50` has no effect.** |
| **Overshield** | the pawn is a `TnPlayerPawn` with SegmentedHealth and **NormalizedOverShieldHealth < 1.0** | `HealDamage(1.0, TnHealTypeOverShieldPickup)`. The heal type is `SHT_AddOverShield`, so **`Health = HealthMax + Blueprint.Overshield`** (`TR_Health_p.SharedHealth`: Overshield **550**) and the active segment is set to the top one. **[Corrected 2026-10-05, TARGETED_PASS3 §A4: in versus the specialty health blueprint replaces SharedHealth. Overshield is 200 and max health depends on class: Leader 300, Scientist 180, Scout 200, Soldier 330.]** |
| **Ammo crate** | at least one inventory `TnWeapon` with WeaponType in `{WT_Primary, WT_Secondary, WT_Vehicle}` and `!AmmoMaxed(0)` | `FillReserveAmmo()` on every such weapon |

**Segmented health** (`TnSegmentedHealth`, CONFIRMED):
- `TR_Health_p.SharedHealth`: Segments **[175, 125, 125, 125]**, Overshield **550**. **[Corrected 2026-10-05, TARGETED_PASS3 §A4: in versus the specialty health blueprint replaces SharedHealth. Overshield is 200 and max health depends on class: Leader 300, Scientist 180, Scout 200, Soldier 330.]**
- `HealDamage` dispatches on `HealType.SegmentedHealType`:

| type | effect |
|---|---|
| AddHealthToAll (0) | up to HealthMax |
| AddHealthToSegment (1) | up to the current segment top |
| AddSegment (2) | raise to the next segment top |
| AddAllSegments (3) | full |
| AddOverShield (4) | HealthMax + Overshield |

- `AdjustDamage`: while overshield health > 0, damage is subtracted from Health directly and returns 0 to the normal path. Otherwise it is normal segmented damage.
- `GetActiveSegment(Health)` walks the segment list.
- The segment no-regeneration / regen rules were not read here.

**Instant respawn** (TDM respawn §5.6 of the bootstrap note): `TnPlayerController.TriggerInstantRespawn()` sets `_ShouldInstantRespawn`, which the kill-streak reward `TnKillStreakInstantRespawn` uses (`OwnerKilled` when killed by someone else). It is cleared on restart. Without it the wave delay is 5 s.

`[TransGame.TnPlayerController] PlayerRestartDelay=6.0` has **no script reader** (only native or unused): PARTIAL.

- `TnPlayerPawn.CanPickupInventory` (used by `TnPickupManager`) also refuses:
  - while downed;
  - during melee;
  - weapons while in vehicle form;
  - while reviving someone (`TnPlayerController.RevivablePawn != none`).

### Factory mesh and spin (CONFIRMED script; HIGH for the native AttachComponent transform)

- `PickupFactory.SetPickupMesh` = `InventoryType.static.CreatePickupFactoryMesh(self)`, i.e. **`new` component from the template `default.PickupFactoryMesh`**, then `AttachComponent` to the **factory actor**.
  - `TnPickupFactory.SetPickupMesh` then sets the factory LightEnvironment.
- The ammo-crate template `Default__TnAmmoCratePickup.MeshComponentA` (`PROP_NEU_AmmoPickup_STAT`, CullDistance 8000, no shadows, no collision) **authors no Translation, Rotation or Scale**. **The mesh sits at the factory actor origin with the actor's rotation and DrawScale: zero offset.**
- **Spin:**
  - `PickupFactory.Pickup.BeginState` sets `RotationRate = InventoryType.default.PickupRotationRate` (crate: Yaw **10000 UU/s ≈ 54.9°/s**) and `SetPhysics(PHYS_Rotating)`.
  - `Pickup.EndState` sets `PHYS_None`.
  - **The whole factory actor rotates while the pickup is available** (mesh, PickupEffect and CustomPickupEffect components with it) and **freezes at its current yaw when taken**. It resumes from that yaw on respawn.
  - Health and overshield define no `PickupRotationRate` and no `PickupFactoryMesh`: no mesh, and no spin (HIGH; `Inventory` default rotation rate not overridden).
- Highlight / custom FX: `SetPickupVisible` activates the `CustomPickupEffect` (health / overshield FX) and, if `ShouldDisplayHighlightFx`, the `PickupEffect` (`Pickup_FX`). `SetPickupHidden` hides and deactivates them.
- Factory collision: cylinder radius 200, height 100, translated +100 Z (`Default__TnPickupFactory`).
