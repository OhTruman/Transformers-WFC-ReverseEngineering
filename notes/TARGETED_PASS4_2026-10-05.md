# Targeted pass 4 — runtime discrepancies (2026-10-05)

Scope: answers for vehicle handling, weapon swap, localized VO, Scout body height, vehicle FX/audio events and match score reset.
- No networking work.
- No Rebuild or AssetTools code was changed.

Labels:
- **C** = confirmed from script, cooked data or native code;
- **H** = high confidence (stock UE3 behaviour or one inference step);
- **P** = partial;
- **U** = unknown.

Sources:
- `work/script/decomp/*.txt` (TransGame / Engine / HM_Engine);
- `work/q/streets_base_gameclasses.txt` (TransContent classes cooked into Streets);
- `authored.db`;
- shipped `Coalesced_ini`;
- ExtractedAssets PSA/glTF (read in place).

---

## A. Vehicle physics / handling (GP)

### A1. Hover jump (C)

`TnCarForm.Hovering.UpdateJumping`:
- `_JumpCooldown` counts down **only while on the ground**.
- A jump fires when **all** of these hold:
  - `_Jumping` is set (transient input, cleared every update by `ClearTransientInputs`, so one press means one request);
  - cooldown ≤ 0;
  - `HoverSimulation.IsOnTheGround`.
- On jump:
  - `HoverSimulation.Jump()`;
  - cooldown = `TimeBetweenJumps` **0.3 s**;
  - force feedback, `JumpFX`, `PlayAscendSound`.

`TnHoverCarSimulation.Jump`:
- `ApplyLinearVelocity((0, 0, JumpLinearSpeed))`. This is an **additive world-Z Δv of 1200** (CDO). Neither `HoverCar_Physics` nor `HoverTruck_Physics` overrides it.
- `ApplyLocalAngularVelocity((0, −JumpAngularSpeed, 0))` with JumpAngularSpeed **1.0 rad/s**, nose-up.

`IsOnTheGround`:
- = (number of suspension contacts > 0) **and** average contact normal Z > **0.707**.
- So no jump on slopes steeper than 45°, and no air jump.

Gravity on the body: `DefaultGravityZ` −2940 × `RBPhysicsGravityScaling` 0.66 = **−1940.4 UU/s²**.
- Apex from rest ≈ 1200² / (2 × 1940.4) ≈ **371 UU**.
- The additive Δv stacks with any upward velocity the springs already give. Upward spring velocity at the moment of the jump adds to the height.

**Likely rebuild causes of "jumps too high":**
- jump Δv applied with world gravity −2940 instead of the scaled −1940 (gives a *lower* apex, so check the reverse case too);
- jump applied **as a set velocity plus spring force on the same frame**;
- several jumps from a held key (the original needs a fresh press, a 0.3 s grounded cooldown, and ground contact);
- suspension force not cut when the probes leave the ground.

### A2. Boost (Driving) jump (C)

`Driving.UpdateJumping`: same gate (`CarSimulation.IsOnTheGround`, cooldown 0.3 s), then `CarSimulation.Jump`.
- `Car_Physics` / `Truck_Physics` `JumpLinearVelocity` = **local (600, 0, 1400)**.
- CDO `JumpAngularVelocity` 2.0.

### A3. Hover suspension and ground traces (C)

**Probes:**
- Four probes at COM + normalised (1, 1, 0) × radius, rotated 90° apart. They sit on the **diagonals**, not on the axes.
- `TnSuspension.Update` runs a **MultiTrace** along the probe direction.
- The first hit counts if the hit component has `BlockRigidBody` and `RBChannel != 6`, or if the hit is WorldInfo (BSP/terrain).
- Length = hit distance − wheel radius.

**Spring** (`TnSpring`, implicit integration):
- m = mass / 4 (per probe), K = stiffness / m, B = damping / m.
- vPred = (v + dt·(K·(rest − len) + g)) / (1 + B·dt + K·dt²), with g = −dir.Z·GravityZ.
- Force = m·((vPred − v)/dt − g).

**Applied force** = max(0, (−dir · contactNormal) × springForce):
- **never pulls down**;
- scaled by how square-on the surface is.

A probe with no hit gives no force; there is no ray clamping.

### A4. Angular damping, self-righting and airborne orientation (C)

**Damping:**
- `TnHoverCarSimulation.Activate` sets **angular damping 0 and linear damping 0** on the rigid body.
- `DefaultAngularDamping` 0.1 applies only on the AI path.

**`UpdateTurn`** (corrected 2026-10-06; the earlier text here misread the two masks):
- Δω = axisAngle(current → target) × **(0.05, 0.05, 1)** / dt − ω, then multiplied by **`ShouldUpright ? (1,1,1) : (0,0,1)`** and applied as a velocity change.
- `ShouldUpright` = `NumContacts == 0` (airborne) **or** upside down (up.Z < 0.01).

So the original:
- **Grounded and upright:** only **yaw** ω is set to the target. Pitch/roll ω get **no correction at all**: no weak pull, and momentum carries over. Grounded attitude comes from the four diagonal springs alone, since RB angular damping is 0.
- **Airborne or inverted:** yaw is set fully. Pitch/roll ω is **set to 0.05 × angleError / dt**, a gentle pull of 5 % of the error per tick, **not** a one-step snap.
- The airborne target is upright with the current yaw, so the jump's nose-up spin (A1) is pulled back gradually once the probes lose contact.
- Riser pitch estimate: see the 2026-10-06 addendum at the end of this note.

**`UpdateRoll`:** local-X angular acceleration = 1.0 × strafe stick + (−local ωz). This is the barrel-roll/lean input, damped by yaw rate.

**`UpdateStrafe`:** acceleration = max × driftScale × (up.Z)². Strafing fades as the car tilts.

**Likely rebuild causes of teetering/rolling:**
- a grounded pitch/roll correction stronger than 5 % per step;
- non-zero angular damping fighting the springs;
- probes on the X/Y axes instead of the diagonals;
- springs allowed to pull down (negative force);
- the airborne upright drive missing (the vehicle keeps the jump nose-up spin).

### A5. Wall impacts (C for data; H/U for the PhysX combine)

**Physical materials:**

| Material | Restitution | Friction | AngularDamping | LinearDamping |
|---|---|---|---|---|
| `VEH_Car_PHYSMAT` / `VEH_Truck_PHYSMAT` | **0.05** | 0.2 | 0.2 | — |
| `VEH_Tank_PHYSMAT` | 0.05 | 0.2 | 0.6 | 0.3 |
| `VEH_Plane_PHYSMAT` | 0.1 | 0 | 0.1 | 0.1 |

Body setups: the car, truck, tank and plane bodies use their own physmat.

**Script response:**
- `TnVehicleForm.OnRigidBodyCollision` gives force feedback when ContactSpeed > 500 (scale /2000) and sends an AI bump notify. **There is no bounce or impulse logic in script.**
- `Driving.OnRigidBodyCollision`: if −normal(TotalNormalForce) · forward > **0.866** (head-on within 30°), **`GotoState('Hovering')`**. A frontal boost crash ends boost.

**H:** the PhysX restitution combine with world materials is not traced (default PhysX combine is average). With 0.05 vehicle restitution the original barely bounces.

**Likely rebuild cause of strong wall bounce:** default restitution (≈0.3–0.5) instead of 0.05, or an explicit reflect impulse that the original does not have.

### A6. Boost versus normal movement, input and state transitions (C)

| From | To | Condition |
|---|---|---|
| Hovering | Driving | boost held **and** (SimulationMode 0 **or** not drifting) |
| Driving | Hovering | boost released, **or** a head-on wall hit (A5) |

- `Hovering.BeginState`: `HoverSimulation.Activate` + `Drift`.
- `Driving.BeginState`: `_Boosting = true`, `CarSimulation.Activate`. `EndState` stops the boost FX.
- Driving inputs:
  - accelerator forced to **1**;
  - Steering = signed square of the steer input;
  - RollControl = strafe X.
- **Alternate movement input:** in Hovering, strafe X drives roll/strafe (`UpdateRoll` / `UpdateStrafe`) and forward/back are throttle. In Driving, strafe X is roll control only.
- **Centre/rotation:** forces are applied at the COM. The probes are placed around the COM (A3), so the turn pivot is the COM.

---

## B. Weapon swap — shipped PC path (GP) (C)

**Bindings** (shipped `DefaultInput` / Coalesced):
- `NextWeapon` on Xbox **Y**, and on PC **PageUp, PageDown, MouseScrollUp, MouseScrollDown**.
- **No `PrevWeapon` binding exists**, so both wheel directions cycle forward. With two weapons this is a toggle.

**Call chain:**
1. `TnPlayerController.NextWeapon` → `PreWeaponSwitch()`.
2. If allowed: `PlayerController.NextWeapon`. This returns if paused, and calls `SwitchToBestWeapon` if there is no weapon.
3. `InvManager.NextWeapon`.

**`PreWeaponSwitch` blocks the switch** (returns false) when:
- there is no pawn or inventory manager;
- the pawn is **transforming**;
- `!Form.CanSwitchWeapons`:
  - robot form: blocked while `MeleeManager.IsAttacking`;
  - **vehicle form: always blocked**;
  - plane form: allowed;
- the current weapon has `DisallowWeaponSwitching` (e.g. Poke).

Otherwise it calls **`AbortMelee`** and returns true.

**Inventory** (`HmInventoryManager.FindNextWeapon`):
- Start at the current weapon (or the pending weapon); take the next weapon in `InventoryActors` order that passes `CanCycleToWeapon`; wrap to the first.
- `TnWeapon.CanBeCycledTo` is false if:
  - `ExcludeFromWeaponCycling` is set;
  - it is a robot weapon and the pawn is not in robot form;
  - it is a vehicle weapon and the pawn is not in vehicle form.
- If the candidate is the current weapon or none, nothing happens; otherwise `SetCurrentWeapon`.

**During reload:**
- `HmWeapon.TryPutDown` while the `WeaponReloaded` timer is active puts the weapon down **immediately**; EndState clears the timer, so **the reload is cancelled**.
- During refire it waits for `MinReloadPct`.

**Deactivate:**
- `WeaponPuttingDown.BeginState` → `OwnerAnimator.OnUnequip` (put-down animation).
- `EndState`: weapon hidden; ground-speed multiplier removed.
- **Heavy (type 5) weapons are tossed**: switching drops the flag, bomb or turret.
- Immediate put-down if the pending weapon is melee (type 3).

**Activate:**
- `WeaponEquipping.BeginState` → `OnEquip` animation.
- `WeaponEquipped` → `SetGroundSpeedMultiplier(weapon data)`.
- Then `TnPlayerPawn.NotifyWeaponChanged`: left-arm IK socket, and `PC.NotifyWeaponChanged` (`IsAllowedToFire = true`).

**HUD:** `TnHudDataObserverWeapon.CheckData` **polls** `GetWeaponByType(WeaponType)` and pushes the class name to the Flash movie on change. There is no event; the weapon panel updates on the next observer poll.

---

## C. Localized announcer / dialogue audio (SY) (C)

### C1. Gameplay VO path (packages)

- The announcer event `SoundEvents_Dialog.Announcer.MP_GameTypeTeamDeathMatchDialog` is an `HmSoundEvent` in a non-localized package. It is referenced by `Default__TnGameTypeMessageTDM.GameTypeDialog`.
- The event maps through `SoundEvents_Dialog.Announcer.CHR_ANNOUNCER_DIALOG` (`SoundEventSet`, 153 entries) to `BL_DX_SWITCHBOARD.SC002657`.
  - That is a `SoundCue` with `IsDialog`, a 2D root, `DX_DRY` category and volume −4.
  - Its two `SoundNodeWaveEvent` children are chosen by `DialogCharacter`: `DialogCharacters.OPRIME` → `WL_DX_OPRIME.DX_OPRIME_LK002657`, and `DialogCharacters.MGTRON` → `WL_DX_MGTRON.DX_MGTRON_LK002666` (faction announcer).
- **The `SoundNodeWave`s (the actual audio) live only in localized packages.** Every map package has twins in the Game Dump: `<Map>_LOC_int.xxx` and `<Map>_LOC_FRA.xxx` (213 of each, e.g. `MP_IAC_Streets_BASE_m_LOC_int` / `_LOC_FRA`), plus `Startup_int` / `Startup_FRA`.
  - The cue lives in the base package.
  - The engine loads exactly one `_LOC_<GLanguage>` twin; the xex has the `_LOC` suffix string at `0x82002C39`.
  - So the **gameplay language is GLanguage**: the same value as the movie path (`LANGUAGEFORCOOKING` override, else `appGetLanguageExt` from XGetLanguage). There is one language variable, but the **resolution is separate**:
    - movies pick a **Bink audio track** (track 5 + L, pass-3 §E);
    - VO picks a **package twin** (`_LOC_int` vs `_LOC_FRA`).
- Only INT and FRA exist in this dump.

### C2. Why the rebuild plays one French line (C, data provenance)

- `authored.db` keys objects by path only. Wave paths are the same in both twins, so **whichever twin was indexed last wins**. That pick is arbitrary per wave.
- Count of `SoundNodeWave*` rows: **3445 from `_LOC_FRA` packages, 2836 from `_LOC_int`**.
- The TDM match-start waves resolve to FRA: both `DX_OPRIME_LK002657` and `DX_MGTRON_LK002666` have package `MP_ESC_BrokenHope_Base_m_LOC_FRA`. This is exactly the "one non-English match-start line" symptom.
- **Fix belongs to AssetTools/Systems:** resolve every localized wave from the `_LOC_int` twin (or from the twin selected by the language setting), never from the merged manifest row.

---

## D. Scout idle/run body height (RD/GP)

**Setup (C):**
- The default MP Scout is `Car2` Sideswipe (Autobot) or `Car4` Barricade (Decepticon).
- ROBODEF `AnimSets` (in order):
  - `TR_LightMedium_ANM_p.Shared_ROBO_ANIM`;
  - `TR_LightSmall_ANM_p.SideSwipe_ROBO_ANIM` (or `Barricade_ROBO_ANIM`);
  - `Death_LightMed`, `Reacts_*`.

**What each set holds (C, PSA):**
- The character set holds **only** idles, pivots, hover and transforms: SideSwipe has 12 sequences (`NAV_Idle*`, `Nav_IdlePivot90_*`, `Nav_Hover`, `Transform_*`); Barricade has 7.
- **All walk/jog/sprint locomotion comes from `Shared_ROBO_ANIM`**, which was authored on the Starscream skeleton (`PreviewSkelMeshName RB_Starscream_SKEL`).

**Hip height (`C_Spine00_Hips_XB` Z, parent-relative, UU), from the PSA keys (C):**

| Source | Value |
|---|---|
| Sideswipe/Barricade ref skeleton | **192.1** |
| Starscream ref skeleton | **240.1** |
| SideSwipe `NAV_Idle` | 139.7–154.2 |
| SideSwipe `NAV_Idle_01` | 153–154 |
| Shared `NAV_Idle` (Starscream; overridden for the Scout) | 213.8–215 |
| Shared `Nav_StrafeJog_F/L/R` | **194–232** |
| Shared `Nav_StrafeJog_B` | 186–212 |
| Shared `Nav_StrafeWalk_*` | 192–219 |
| Shared `AI_Nav_Sprint_F_01` | 183–234 |

**Translation handling (C data; H for semantics):**
- `bAnimRotationOnly = False` on all these AnimSets (CDO default True, overridden).
- `UseTranslationBoneNames` and `ForceMeshTranslationBoneNames` are empty.
- In stock UE3 that means **bone translations come from the animation**: there is no ref-pose retargeting.
- **H: the shipped Scout's hips really ride about 40–80 UU higher while jogging than in its own idle.** The run uses Starscream-proportioned translations on a 192-UU skeleton. The rebuild's height jump is therefore probably **faithful**, not a bug.
- **P:** AnimSet search order. Stock `FindAnimSequence` searches the last set first, so the character set's `NAV_Idle` wins. This doesn't matter for the jog, which exists only in Shared.

**Root (C):**
- `C_Root_Reference_XR` translation is (0, 0, 0) in every idle/locomotion key.
- The robot tree's locomotion nodes leave `RootBoneOption` at default. Only four `AnimNodeSequence`s in `Robot_ANIMTREE` set `RBA_Translate` ×3 + `RRO_Extract` (no anim names authored; set at runtime, e.g. Whirlwind `RMM_Translate`).
- So **no root motion moves the pawn during idle/run**, and root motion plays no part in body height.

**U:** whether a native post-process (FootIK / mesh Z offset) compensates. Nothing was found in script, and `TnPawn` has no per-anim mesh offset. Before "fixing" the height, compare a shipped capture.

---

## E. Vehicle FX / audio event relationships (RD/SY) (C)

**Hovering (`TnCarForm.Hovering`):**
- `UpdateFx`:
  - for each `HoverFX` socket PSC: vector parameter **`Size`** = min(1, thrusterLinear + thrusterAngular) × socket RelativeScale;
  - the contributions come from `HoverPhysics.CalculateThrusterLinear/AngularContribution`, using local linear and angular acceleration smoothed by VLerp 0.1;
  - FX start or stop with `FxAllowed`.
- Audio:
  - `BoosterAmount` = the larger contribution;
  - `UpdateSounds`: `_IsOnGround` = IsOnTheGround, `_WheelSlipRatio` = 0, `_EngineLoadState` = 1 forward-throttle / 2 reverse / 0 none;
  - Dash → `PlayBoosterSound`;
  - Jump → `JumpFX` + `PlayAscendSound`.

**Driving (boost):**
- `Driving.UpdateFx`: `PlayBoostFx` when allowed and none are playing, `StopBoostFx` when disallowed.
- `PlayBoostFx` = `FxPlayer.Play(Blueprint.BoostFx)` + `PlayBoostSound`; `StopBoostFx` mirrors it (also on `EndState`).
- `UpdateBoostFx` on every PSC:
  - `Color` = lerp(EnergonColor → Yellow, NormalizedJumpTimeRemaining);
  - alpha = lerp(100, 255, same).
- `UpdateSounds`: `_IsOnGround`, `_WheelSlipRatio` = `CarSimulation.SlipAngle`.

**Engine audio state machine** (`HmPlayerVehicleAudioComponentImpl.UpdateEngineSound`, each tick):
1. `IsBoosting` → **Boosting**.
2. Else `JumpRevSounds.UseJumpRev` and airborne for ≥ `JumpRevTime` → **JumpReving**. The timer resets on ground contact.
3. Else, movement direction:
   - if `_VehicleSpeed` > 1 and velocity·forward ≥ 0 → Forward; < 0 → Reverse; speed ≤ 1 → none, treated as ForwardOffLoad;
   - Forward → **ForwardOnLoad** if `_EngineLoadState` == 1, else ForwardOffLoad;
   - Reverse → **ReverseOnLoad** if load state == 2, else ReverseOffLoad.
4. Every tick, all loop components in all sets get float parameter `SpeedSoundParameter.Name` = `_VehicleSpeed`.
5. Gear = the first `DriveSounds[i]` with speed ≤ MaxSpeed, clamped to the last.

**Land sound:**
- On the ground→air→ground edge, play the **highest-index `HoverLandSound[i]` whose `TimeInAirThreshold` ≤ time in air**.
- `LandTimer` accumulates while airborne.

---

## F. Match initial score and reset ownership (GP/SY) (C)

**Storage:**
- Per-player score is `PlayerReplicationInfo.Score` (with Kills and Deaths).
- Team score is `TeamInfo.Score`.
- CDOs set neither (`Default__TnTeamInfo` has only `_AllowRespawn` and `EnergonColor`), so **both start at 0.0** on a fresh spawn.

**TDM kill scoring** (`TnGameRules_ScoreKills.ScoreKill`, TDM rules `TeamScoreAmount 1`):
- Only if the damage type ≠ `DmgType_Suicided`, there is a killer PRI, and `ShouldScoreKill`. The MP rule: the victim is a `TnPlayerController` or none, so **AI or bot kills don't score**.
- `PRI.AddScore(selfKill ? 0 : 1, selfKill ? 0 : 1)` → `Score += 1`, `Team.AddScore(1)`. `TnPRI.AddScore` also increments game stat `0x10000009`.
- **Suicide and self-kill give 0, not −1.**
- End: `CheckScore` → `ReachedGoalScore` (GoalScore > 0 and score ≥ GoalScore) → `EndGame` → **MatchOver**.
  - MatchOver ignores ScoreKill and ScoreObjective.
  - Team winner = `GameReplicationInfo.Winner`; ties reported by `GetGameCompletionType` (0 win / 1 loss / 2 tie).

**Fresh match:**
- `TnMultiplayerGame.InProgress.BeginState`:
  - `GRI.ElapsedTime = 0`;
  - `SetGameStatus(3)`;
  - **`GRI.ResetPlayerStats()`**, which clears **only `TnPRI.GameStats[]`** (not `Score`);
  - `SendUIEventToControllers(3)`;
  - timer (`bStopCountDown` unless the rules modifier runs the timer);
  - `GameRulesModifiers.HandleStartGame`.
- `TnTeamGame.StartMatch` resets every Pawn, DroppedPickup and PickupFactory, then forces GC.

**Between matches:**
- `MatchOver.BeginState`: MVP achievement, status 5, UI event 9, stats write, then timer `MatchOverCountdown` (**15 s**, shipped ini) → `ReturnToGameLobby` → `ServerTravel(lobbyURL?MapId=…)`. `TnGame` CDO **`bUseSeamlessTravel = True`**.
- Seamless travel carries controllers but **zeroes scores**:
  - `GameInfo.HandleSeamlessTravelPlayer` (same PC class) or `PlayerController.SeamlessTravelFrom` (new PC class) calls **`OldPRI.Reset()`** *before* `SeamlessTravelTo(NewPRI)`;
  - `PlayerReplicationInfo.Reset` (`ShouldResetScore` true) sets Score 0, Kills 0, Deaths 0, `bReadyToPlay` false, `bOutOfLives` false;
  - `TnPRI.Reset` also zeroes `_CurrentKillStreak` and sets `NumKillsSinceDowned` −1, resets the multi-kill detector, and sets `ForcedIntoLevel`;
  - `CopyPropertiesTo` then copies the zeroed values. `TnPRI` also keeps the character selection if `RetainSelectedCharacterOnTransition`, plus PlayerLevel and TeamName.
- `TnTeamInfo.PostMoveToSeamlessTravelWorld` → **Score = 0**, and `TnTeamInfo.Reset` → Score = 0.
- An in-place restart (`MatchOver.ResetLevel`) goes to state None, runs `GameInfo.ResetLevel` (Reset on every controller, PRI and TeamInfo; the Kismet sequence is reset), then **PendingMatch**.

**Reset ownership:**
- **GameInfo** owns it: the seamless-travel handlers plus `ResetLevel`.
- PRI and TeamInfo carry the actual zeroing in their `Reset` / `PostMoveToSeamlessTravelWorld`.
- The GRI only clears `GameStats` at InProgress.

**Rebuild rule:**
- at match start: PRI score, kills and deaths = 0; team scores = 0;
- clear per-match stats when InProgress begins;
- kill = +1 player, +1 team;
- suicide = 0.

### E addendum — the consumer of the HoverFX `Size` parameter (C data, H semantics)

**Data (C):**
- `ParticleModuleSizeMultiplyLife.LifeMultiplier` = `DistributionVectorParticleParameter` "Size". It appears in `FX_Navigation_p.CarHover_A_01_FX`, `CarHover_D_01_FX` and `hover_plane_FX` (×2).
- The mapping is identity: Max input = output = 1000, min 0.
- Constant (1, 1, 1) is the fallback when the parameter is not set.

**Semantics (H, stock UE3):**
- Particle size = base size × the Size parameter.
- The Size parameter is min(1, thruster contribution) × socket RelativeScale.
- So a thruster at rest emits zero-size particles.

#### Which emitters use the shared Size module (H, raw package bytes)

**Method:** raw int32 scan of every ParticleLODLevel blob in `MP_IAC_Streets_BASE_m` for the module's big-endian export index. Module `CarHover_A_01_FX.ParticleModuleSizeMultiplyLife_9193` is export 16983.

**Result:**
- The index appears exactly once in the **LOD 0** blob of every one of the 7 emitters:

  | Emitter | LOD 0 level |
  |---|---|
  | 10606 | LODLevel_902 |
  | 1062 | LODLevel_9828 |
  | 12613 | LODLevel_6243 |
  | 13443 | LODLevel_16144 |
  | 1517 | LODLevel_13205 |
  | 8261 | LODLevel_8474 |
  | 854 | LODLevel_13897 |

- It appears in **no** LOD 1 blob.
- So one module object is shared by all 7 emitters, at LOD 0 only.

## Addendum (2026-10-06): A4 hover car, UpdateTurn ordering vs suspension springs (GP)

**Order inside `TnHoverCarSimulation.Update`** (called from `TnCarForm.Hovering.DoUpdate`, player-controlled only) (C):
1. `UpdateSuspension`: per probe, `ApplyForce(−Dir · max(0, (−Dir·N)·Force), probeLocation)`.
2. `UpdateTerminalVelocity`.
3. `UpdateDash` **or** `UpdateStrafe`.
4. `UpdateRoll`: input roll acceleration minus yaw rate.
5. **`UpdateTurn` last.**

**UpdateTurn mask (C):** `Velocity = axisAngle(q⁻¹·target) × (0.05, 0.05, 1) / dt − LocalAngularVelocity` is applied × **`(ShouldUpright ? (1,1,1) : (0,0,1))`**.
- `ShouldUpright = (NumContacts == 0) || IsUpsideDown` (IsUpsideDown: up.Z < 0.01).
- **So while at least one suspension probe has contact and the car is upright, only yaw ω is replaced.** Pitch/roll ω are **not touched**: they carry over between ticks and are driven by the spring forces, UpdateRoll and the RB angular damping (DefaultAngularDamping).
- The (0.05, 0.05, ·) pitch/roll correction applies **only airborne (no contacts) or upside-down**.

**How it reaches PhysX (C for the native calls; H for the step semantics):**
- `TnRigidBodyMesh.ApplyLocalAngularVelocity` → `PrimitiveComponent.AddLocalAngularVelocity` (native `0x82D31128`) → **`NxActor::addLocalTorque(v, NX_VELOCITY_CHANGE (2), wakeup)`**.
- `ApplyForce` → `AddForce` (native `0x82D2B838`) → **`addForceAtPos(F × unitScale, pos × unitScale, NX_FORCE (0), wakeup)`**, or `addForce` without a position.
- `LocalAngularVelocity` is the value cached by `TnRigidBodyMesh.Update` from `GetRBAngularVelocity`, i.e. the **previous physics step's result**.
- So the spring forces and the yaw velocity-change are both **queued in the same script update** and applied together by the next PhysX simulate. Neither is applied "after" the other within script.
- H (PhysX 2.x semantics): the velocity change lands at step start; the spring forces integrate over the step (including substeps).

**Riser pitch:** a < 1° pitch over a 0.25 m riser is **not** consistent with the original logic.
- The grounded body is free in pitch/roll apart from the springs and damping, so the body should tilt visibly as the front probes compress.
- H for the magnitude: it depends on spring Force, probe geometry, inertia and DefaultAngularDamping; not computed here.

### Addendum (2026-10-06): hover spring/damping values and riser pitch estimate

**Mass, inertia and COM (C):**
- `TnCarForm` initializes `CarSimulation` **before** `HoverSimulation`.
- `TnCarSimulation.InitializeFromBlueprint` sets the shared rigid body's COM, **Mass** and **LocalInertiaTensor** from the CarBlueprint.
- `TnHoverCarSimulation.InitializeSuspension` then uses MassShare = Mass / 4.
- The hover sim never sets mass or inertia itself.

| Blueprint | Mass | InertiaTensor (X, Y, Z) | COM |
|---|---|---|---|
| `VEH_SHARED_p.Car_Physics` | 1500 | (5.6e6, **9.8e6**, 1.27e7) | (12, 0, −16) |
| `VEH_SHARED_p.Truck_Physics` | 2500 | (2.27e7, **4.64e7**, 5.89e7) | (−47, 0, 20) |

**Hover blueprints (C)** (`HoverBlueprint` refs: all MP cars → HoverCar_Physics; trucks → HoverTruck_Physics):

| Hover blueprint | SuspensionRadius | Suspension | Stiffness | Damping | RestingLength |
|---|---|---|---|---|---|
| `HoverCar_Physics` | 100 (lever ±70.7 per axis) | `HoverCar_Supension` | **8000** | **4000** | **200** |
| `HoverTruck_Physics` | 185 | `HoverTruck_Suspension` | **10000** (inherits CDO) | 4000 | 250 |

- `TnSuspensionBlueprint` CDO: Stiffness 10000, RestingLength 30, Damping 0.
- Wheel radius passed to TnSuspension = 0.
- Other suspension blueprints for reference: HoverTank 20000/6000/250; SoldierTank hover 400000/50000/400.

**Damping (C):**
- RB angular and linear damping = **0** while hovering (`Activate`).
- Spring damping is the only pitch damping (TnSpring B = Damping / (Mass / 4)).
- `DefaultAngularDamping` is AI path only.

**Riser estimate (H; `tools/hover_pitch_est.py`):**
- Model: pitch-plane rigid body with the four diagonal probes, the TnSpring law per tick, forces held over PhysX substeps, gravity −1940.4, no grounded pitch correction, step riser.
- Units assumed consistent in UU (the blueprint inertia is mass·UU²).
- Peak nose-up pitch for the **car** over a 12.5 UU riser (0.25 m at 50 UU/m):

| Speed (UU/s) | Peak pitch |
|---|---|
| 500 | **5.4°** |
| 1000 | **4.0°** |
| 1500 | **2.6–2.8°** |
| 3000 | **1.0–1.7°** |

- A 25 UU riser roughly doubles these (5.5° at 1500).
- **Truck:** 2.0° (12.5 UU) and 4.0° (25 UU) at 1500.
- The small rear dip afterwards is −0.1° to −0.3°, settling in about 1 s.
- Sanity check: at low speed the peak approaches the static geometric tilt atan(riser / (2 × 70.7)) = 5.05°.
- Insensitive to tick rate (1/30 or 1/60 s; 1–8 substeps) and to the spring-gravity term.
- **Conclusion: the original should pitch several degrees over such a riser**; 0.47° is the effect of the rebuild's grounded pitch/roll ω replacement.

### Addendum (2026-10-06): A5, PhysX material combine (C for the UE3 calls; H for PhysX-internal semantics)

**UE3 NxMaterial builder:** `0x82EC5D08` (8 callers in the physics-init paths).
- It creates a scene material (or reuses a freed index), then fetches it via `NxScene::getMaterialFromIndex` (vtable +0x140) and configures it through the `NxMaterial` vtable (base `0x823F10C0` = `NpMaterial`).

| NxMaterial setter (vtable offset) | Value |
|---|---|
| +0x24 setRestitution | `PhysicalMaterial.Restitution` (+0x30) |
| +0x1C setStaticFriction | `Friction` (+0x2C) |
| +0x14 setDynamicFriction | `Friction` (+0x2C) |
| **+0x4C setFrictionCombineMode** | **2** |
| **+0x54 setRestitutionCombineMode** | **2** |
| +0x44 setFlags | bit NX_MF_ANISOTROPIC set iff `bEnableAnisotropicFriction` (bit 0x40000000 of +0x34), else cleared |
| +0x34 / +0x2C setDynamic/StaticFrictionV | `FrictionV` (+0x44) |
| +0x3C setDirOfAnisotropy | `AnisoFrictionDir` (+0x38) |

- `NxCombineMode` 2 = **NX_CM_MULTIPLY** (PhysX 2.x: AVERAGE 0, MIN 1, MULTIPLY 2, MAX 3; H that the enum is stock).
- **Every UE3 material uses MULTIPLY for both friction and restitution.** (This corrects the earlier "default PhysX combine is average" guess.)
- PhysicalMaterial field offsets in this build: MaterialIndex +0x28, Friction +0x2C, Restitution +0x30, bool bitfield +0x34 (bForceConeFriction, bEnableAnisotropicFriction, …), AnisoFrictionDir +0x38, FrictionV +0x44.

**Vehicle vs world contact** (both MULTIPLY, so the pair uses the product):

| World material | Friction (car × world) | Restitution (car × world) |
|---|---|---|
| `ENV_PHYSMAT_p` Default / Concrete / Metal etc. (16 materials: 0.5 / 0.1) | **0.2 × 0.5 = 0.10** | **0.05 × 0.1 = 0.005** |
| Engine default PhysicalMaterial (CDO 0.7 / 0.3; used where nothing is assigned, H) | 0.14 | 0.015 |

- The truck uses the same physmat values as the car.
- `VEH_Car_PHYSMAT` authors AnisoFrictionDir (1, 0, 0) but **not** `bEnableAnisotropicFriction`, so friction is isotropic.
- **So wall contacts are effectively inelastic (restitution ≈ 0.005) with low sliding friction (μ ≈ 0.1).** A glancing hit slides along the wall with almost no bounce.
- Remaining H (PhysX internals, not traced): the bounce-threshold velocity below which restitution is ignored, and contact skin width.

### Addendum (2026-10-06): A5, PhysX SDK skin width and bounce threshold

**UE3 PhysX init `0x82E9D988` (C):**
- `NxCreatePhysicsSDK(0x02080300 = PhysX 2.8.3, …)`; SDK pointer stored at `0x83831390`.
- `setParameter` calls (vtable +0x08) on the SDK:

| Parameter id | Value | Identity |
|---|---|---|
| **1 (NX_SKIN_WIDTH)** | **0.025** | C |
| 96 | 1.0 | not identified (U) |
| 99 | 1.0 | not identified (U) |
| 68 | 0.0 | not identified (U) |

- The cooking params (`0x83831398` interface) get skinWidth 0.025 as well.
- **No NX_BOUNCE_THRESHOLD (id 4) call** exists on the SDK, here or elsewhere: no other `setParameter` on this global was found. The 0.025 constant has no other users, so no per-shape skin-width override was found either (H: shapes keep the SDK default).

**Units (C):** UE3 → PhysX length scale is **0.01** (constant `0x822D2CF4`, also used by `AddForce`).

**Effective values:**
- **Skin width = 0.025 PhysX = 2.5 UU**: contacts are generated or held about 2.5 UU before surfaces touch.
- **Bounce threshold = PhysX 2.8 default −2.0** (H, SDK documentation default; not overridden). Restitution applies only when the relative normal approach speed exceeds 2 PhysX units/s = **200 UU/s**. Slower contacts are fully inelastic.
- **With the A5 combine** (car-wall e = 0.005): even fast hits bounce back at ≤ 0.5 % of the approach speed.

**Addendum: the remaining SDK parameters, identified**
- Source: PhysX's own remote-debugger name table, `FUN_824F2288`, called from `NpPhysicsSDK::setParameter`.

| Id | Name | Value | Effect | Label |
|---|---|---|---|---|
| 68 | **NX_ADAPTIVE_FORCE** | 0 | **disabled.** PhysX's adaptive-force solver heuristic (which scales contact forces to stabilise stacks) is off, so contacts use the plain solver. Minor effect on resting/stacked contacts; none on single-body wall hits. | C (name from the binary) |
| 99 | NX_FAST_MASSIVE_BP_VOLUME_DELETION | 1 | broadphase performance option; no gameplay effect. | C (name from the binary) |
| 96 | NX_ASYNCHRONOUS_MESH_CREATION (H) | 1 | asynchronous collision-mesh creation; no gameplay effect. | H (not in the binary's name table, which falls through to the default string; named from the PhysX 2.8 `Nxp.h` enum order between FLUID params and FORCE_FIELD_CUSTOM_KERNEL_EPSILON = 97) |

- The same table confirms id 1 = NX_SKIN_WIDTH and id 4 = NX_BOUNCE_THRESHOLD.

**A4 addendum: how often UpdateTurn runs (hover correction rate)** (C unless marked)

**Call chain (once per game tick, no substep loop in script):**
- `TnPawn.Tick` → `_CurrentForm.Update(DeltaTime)` → `TnTransformerForm` → `OnUpdate(DeltaTime)`.
- `TnVehicleForm.OnUpdate` first sets `_PhysicsDeltaTime = WorldInfo.PredictNextPhysicsUpdateTime(DeltaTime)`.
- `TnCarForm.OnUpdate` → `DoUpdate(_PhysicsDeltaTime)` → hover simulation Update (incl. UpdateTurn).

**`WorldInfo.PredictNextPhysicsUpdateTime`:**
- `n = min(MaxSubSteps, int((RemainingTime + DeltaTime) / TimeStep + 1e-6))`; returns `TimeStep × n`.
- `PhysicsSceneTiming` (Engine.Default__WorldInfo; **no map overrides** across 460 WorldInfos): bFixedTimeStep = true, **TimeStep = 1/60**, MaxSubSteps = 5. MaxPhysicsDeltaTime = 1/3.
- So the script dt is a whole number of 1/60 s PhysX substeps, but the script runs once per frame.

**Frame rate (Xenon):** `[Engine.GameEngine] bSmoothFrameRate=TRUE, MinSmoothedFrameRate=15, MaxSmoothedFrameRate=30` (Xe-TransEngine.ini).
- The game ticks at ≤ 30 Hz, normally exactly 30 Hz. A tick sees n = 2 substeps, dt = 1/30.
- **The 5 %-per-call pull is therefore 5 % per 1/30 s (×0.95 per frame)** on console; it drops to fewer calls per second if the frame rate drops below 30 (still 5 % per call, frame-rate dependent).
- U: PC build cap (only Xenon configs present).

**Rebuild equivalent at a 60 Hz step:** per-step pull k = 1 − 0.95^(dt·30) = 0.02532 (= 1 − √0.95), or call the correction at 30 Hz.
- The same applies to any other per-call (non-dt-scaled) factor in the hover/car simulation.
