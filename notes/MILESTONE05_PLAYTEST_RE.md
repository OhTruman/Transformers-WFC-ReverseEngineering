# Milestone 05 playtest RE: vehicles, modes, settings, frontend, loading, characters, bots (2026-10-04)

**Labels:**
- **C** = CONFIRMED (bytecode / AS2 / authored data / shipped config).
- **H** = HIGH.
- **P** = PARTIAL.
- **U** = UNKNOWN.

**Owners:** **GP** Gameplay, **FE** Frontend, **AT** AssetTools, **RN** Rendering.

**Prior notes reused, not re-derived:**
- `MILESTONE03_VEHICLE_BOOST_STEERING.md` (boost / tire model);
- `MILESTONE05_GAMEPLAY_UNKNOWNS.md` (transform, momentum, KOTH, CTF, markers, pickups);
- `MILESTONE05_FRONTEND_GAMEPLAY_BLOCKERS.md`.

---

## 1. Vehicle control model (GP)

### 1.1 Shipped bindings (`Xe-TransInput.ini`, C)

The Xbox file is coalesced with the shared PC defaults, so both are original.

| Original action (command) | Xbox 360 | Shipped PC default | Robot meaning | Vehicle meaning |
|---|---|---|---|---|
| `Transform` (PressTransform / ReleaseTransform) | Left stick click (Scheme B: **Y**) | **F** | transform | transform |
| `FineAim \| Boost` (StartBoost / StopBoost) | **Left trigger** | **Right mouse** (`ToggleFineAim \| Boost`) | fine aim | **Boost (hold)** |
| `Fire` | Right trigger | Left mouse | fire | vehicle weapon |
| `Ability0 \| VehicleSpecialMove` | **Right bumper** | **Shift** | ability 0 | **Dash** (hover) / **Nitro** (truck, while boosting) |
| `Ability1` | Left bumper | Ctrl | ability 1 | — |
| `PressJump \| Ascend` | A | Space / C | jump | vehicle **jump** (hover and boost) |
| `TossGrenade \| … \| Descend` | B | G / V | grenade | — |
| `NextWeapon` | Y (Scheme B: D-pad up) | wheel / PageUp/Down | — | — |
| `XButton` / interact | X | E / R (reload) | reload / interact | — |
| `Melee` | Right stick click | Q / middle mouse | melee | — |
| Move | Left stick (`aBaseY` deadzone 0.3, `aStrafe` 0) | WASD | move | hover: strafe in body space. Boost: **no throttle**; left X = `RollControl` only |
| Look / turn | Right stick (`aTurn`, `aLookUp`) | mouse | camera | hover: turns the **camera**, and the body follows the camera yaw. Boost: **steering** = right X |
| `ShowScores` | **Back** | **Tab** | scoreboard toggle | same |
| `showmenu` | Start (on release) | Escape | pause | same |
| `Focus` / Killstreak | D-pad down / left | B | — | — |

- Profile **Scheme B** (`UseAlternateControlScheme`, `TnGameViewportClient.MapInputKeyForController`): Y ↔ left-stick-click roles (transform on Y, weapon switch on D-pad up).
- Profile `SwitchRightThumbstickAndB` swaps RS-click ↔ B.

### 1.2 States (C, `TnCarForm` / `TnTruckForm`)

| state | entered | control | key constants |
|---|---|---|---|
| **Hovering** (default vehicle state) | transform; boost released (Drift 0.5 s) | `TnHoverCarSimulation`: body **yaw slaved to camera yaw every tick**; left stick = local XY strafe toward `MaxLinearSpeed` | HoverTruck_Physics: MaxLinearSpeed **1500**, MaxLinearAcceleration **3000**, JumpLinearSpeed 1200 (+pitch −1 rad/s), DashSpeed **3000** / DashDuration **0.5 s**, SuspensionRadius 185 |
| **Dash** (hover only) | VehicleSpecialMove while hovering, cooldown **2 s** | truck: **body-forward** dash (`Dash(vect(1,0,0))`); generic cars: dominant left-stick axis. Strafe toward 3000 with accel 100000; **cancelled if pitch or roll > 30°** (`IsUnstable`) | `TimeBetweenDashes 2.0` |
| **Boost / Driving** | hold Boost while hovering, once the drift has ended | `TnCarSimulation` 4-wheel car: **Accelerator always 1** (no throttle), steering = right X `sign(s)·s²`, front wheels ±25° | Truck_Physics MaxSpeed **3000**, MaxAcceleration 2500 (M03) |
| **Nitro** (truck only) | VehicleSpecialMove while boosting | SpeedScale 1.5 (4500), **SteeringScale 0.3**, Ram (damage + Z kick) | 3 s, 8 s cooldown; ram damage (Optimus) 175 vs player robots and vehicles, 300 vs AI; ExtraRamZVelocity 7000 |
| **Jump** | A while on the ground | hover: +1200 Z, −1 rad/s pitch; boost: (600, 0, 1400) local, pitch −2 rad/s | `TimeBetweenJumps 0.3 s` |

- **Boost exits to Hovering:** on release, or on a hard frontal hit (`Driving.OnRigidBodyCollision`: contact normal · forward > **0.866**) (C).
- **Steering while boosting:** right stick only. Steering while Nitro: ×0.3. Dash while boosting = Nitro (truck); there is no hover dash in boost.
- **Propulsion visuals (C):**

| state | FX / audio |
|---|---|
| Hovering | 6 `HoverFX` boosters (`CarHover_A_01_FX` on HoverBooster_L/R Front / Back / Back2). Per-booster vector param `Size` = thruster contribution from the smoothed local acceleration (lerp 0.1/frame) vs `ThrusterLinearAccelerationLimit 3000` / `Angular 6`. Booster audio amount = the largest contribution |
| Boost | `BoostFx`, colour lerps from the energon colour to yellow by jump time |
| Jump | `JumpFX` (3 sockets) |
| Nitro | `RamFX` |

### 1.3 Mapping advice for PC (H, derived from the shipped PC defaults)

- Keep the original PC map: **RMB = Boost (hold)**, **Shift = Dash / Nitro**, mouse X = camera (hover) / steering (boost), WASD = hover strafe, **W does not throttle in boost**.
- Any "throttle" key is a rebuild invention.

## 2. Vehicle collision / ground contact: why ramps catch the truck (GP)

### 2.1 Hover mode (`TnHoverCarSimulation` + `TnSuspension` + `TnSpring`, C)

**Suspension rays:**
- **4 rays** from `COM + 185·normalize(1, 1, 0)` rotated 0 / 90 / 180 / 270°, i.e. the **diagonal corners**, cast along **body −Z**.
- Length = `RestingLength + WheelRadius` = **250 + 0** (`HoverTruck_Suspension`: RestingLength **250**, Damping **4000**, Stiffness default **10000**).
- `MultiTrace` keeps the first hit whose component `BlockRigidBody` is set and `RBChannel != 6`, or the world.

**Spring:**
- Implicit damped spring per ray, mass = vehicle mass / 4: `v' = (v + dt·(K/m·(rest − len) + g)) / (1 + B/m·dt + K/m·dt²)`; force `F = m·((v' − v)/dt − g)`.
- Applied at the ray origin along body up, scaled by `max(0, up · contactNormal)`.
- **The chassis floats on 250 UU of travel**, so curbs and ramp lips are absorbed by the rays, not by the collision hull.

**Ground and gravity:**
- **On ground** = average contact normal Z > **0.707** (45°).
- Gravity is applied by physics; vertical speed is clamped at −3500.

**Orientation (`UpdateTurn`):**
- Target = camera yaw with **zero pitch and roll**. Each tick, angular velocity is set to `axisAngle(error)·(0.05, 0.05, 1)/dt − current`.
- **Only yaw is applied while any ray has contact**, so pitch and roll follow the springs and terrain.
- **Full 3-axis correction** (5 % of the pitch/roll error per tick, all of the yaw) applies **only when no ray hits or the vehicle is upside down** (up.Z < 0.01): the "upright" logic.

**Strafe:**
- Acceleration limit is scaled by **`(up.Z)²`**, so it weakens on steep slopes and when tilted.
- It is also scaled by `(1 − drift/0.5)²` after boost.

**Roll input:** local roll acceleration = `RightLeft − ω_z` (small).

### 2.2 Boost mode (`TnCarSimulation` / `TnWheelAssembly`, C)

- **Per-wheel** suspension rays at the 4 wheel positions (Truck_Suspension K 120000, D 8000, RestingLength **30**, wheel radius 45).
- The spring force is applied along **body +Z, not filtered by the contact normal**.
- Tire lateral force is applied **below the COM** (wheel position − suspension length), so the body rolls physically.

**Short travel.** Boost has only 30 UU of suspension. **Ramp lips and steps contact the chassis hull**, and a frontal hit (normal · forward > 0.866) **drops the truck back to Hovering**. This is the original's own guard against wedging (C).

**Air:**
- Steering gives yaw acceleration (12 rad/s²) and strafe (2600).
- Nose-down pitch acceleration of 3 while pitch > −25° (`PitchForwardLimit`).
- Landing terminal velocity is lerped 2000 → 3500 over 1000 UU of ground distance.

**No auto-upright in boost.** Roll correction (50 rad/s² · 0.5·(1 − up.Z)) applies only while **`RollControl` (left X) is held** and the roll is < 45° or opposite in sign. **Without input, nothing rights the truck in boost** (C). Releasing boost returns to hover, whose upright rule needs zero contacts or upside-down.

### 2.3 Diagnosis for the playtest symptoms (H)

If the rebuild uses a short single-ray or hull-based ground test in **hover**, it is missing:
- the 250 UU 4-corner diagonal rays;
- the contact-normal-weighted spring;
- the 45° ground threshold;
- yaw-only orientation control on contact;
- the airborne / upside-down-only 3-axis upright.

Without these, the hull catches ramps and angle changes and the truck can nearly flip.

In **boost**, catching on lips is original behaviour, but it is resolved by the frontal-collision → Hovering exit.

**Steps and slopes:** there is no explicit step-up or slope-limit code. Steps are handled entirely by the suspension rays (hover travel 250, boost 30) plus the `(up.Z)²` strafe falloff and the 45° ground flag (C, by absence).

**Contact filter:** rays ignore non-`BlockRigidBody` components and `RBChannel` 6. H: 6 = `RBCC_EffectPhysics` (debris) in the stock enum order.

## 3. Versus mode specification (GP)

All modes share the TDM framework from the bootstrap note:
- PendingMatch 10 s → InProgress;
- spawn clusters and modifiers; Wave respawn 5 s (spectate at 3 s); pickups reset at StartMatch;
- MatchOver 15 s → lobby;
- **no overtime** (`EndGame` only flags `bOverTime` when `CheckEndGame` fails, and no versus rule fails it).

Objective actors **hide and disable themselves unless their rule is present** (`HasRule` in `PostBeginPlay`, Inactive state) (C). ETnGameType decides which spawn clusters are active (`ActiveGameTypes`) and which are faction-neutral (TDM / KOTH / DOM).

| Mode (tag, TNGT) | Team | Score source | Limit (default; choices) | Time | Objectives / actors | Spawn | HUD markers | End / winner |
|---|---|---|---|---|---|---|---|---|
| **TDM** (2) | 2 teams (TnVersusGame) | +1 team per non-suicide kill | **40**; 20/30/40/50 points | 600/**900**/1200 s | none | clusters (faction-neutral) | ally tags | team score; tie = none |
| **DM** (1) | FFA (`TnFreeForAllGame`); **every player resolves to the Decepticon faction** (`GetResolvedCharacterFaction = 1`) | +1 personal per kill (`ScoreKillsDM`, `TeamScoreAmount 1` with no team) | **20**; 10/20/30 | 600/**900**/1200 s | none | **only `TnFreeForAllPlayerStart`** (`RatePlayerStart` −1 otherwise; no cluster manager) | — | `TnFreeForAllGameOverMessage`; winner = top PRI (`GetWinningPRI`); equal top = draw (completion type 2) |
| **DOM / Conquest** (6) | 2 teams | each owned node gives **+1 team every 3 s** (`ScoreInterval 3`, `ScoreAmount 1`) | **400**; 150–500 | **900** (property; 600/900/1200) | `TnDominationPoint` ×N (PointNumber 0–4) | clusters (neutral) + domination spawn modifiers | Domination markers (§G5 of the Phase 8 note) | team score |
| **KOTH / Power Struggle** (4) | 2 teams | each living pawn in an uncontested hill: **+1 / s** | **400**; 150–500 | 600/**900**/1200 | `TnKingOfTheHillZone` (Streets: 5), active 60 s, random rotation | clusters (neutral) + hill avoidance (−50 within 5000) | "Active Node" marker | team score; zones deactivate at end |
| **CTF / Code of Power** (3) | 2 teams, alternating attack | capture **+1 team, +10 personal** (`IndividualScore 10`) | **Rounds 2**; 2/4/6 | **per round** 240/**300**/360 s (round timer replaces the match clock) | `TnGameObjectivePickupFactoryFlag` (defender side active), `TnFlagCapturePoint` (attacker side `_Active`) | clusters per faction | flag / carrier / capture-point markers | after the last round or mercy rule; captures don't end rounds; 5 s between rounds |
| **EXT / Countdown to Extinction** (5) | 2 teams | **bomb detonation**: +1 team, +10 personal, plus a bomb-plant stat | **3**; 1/3/5 | 600/**900**/1200 | `TnGameObjectivePickupFactoryBomb` (neutral bomb, `WaitAfterScoreTime 5`), `TnBombPlantPoint` per team | clusters | Bomb / BombPlantPoint markers | team score |

**DOM capture** (C, `TnDominationPointBase`):
- Attackers inside, with no living defender inside, accumulate `CaptureTime` at `dt × attackers`. **20 s** for one attacker; two attackers halve it.
- A neutral node is captured as if the other team owned it.
- Leaving resets capture progress to 0. If defenders are present, progress holds (no increment).
- On capture: `SetTeam`, each capturer `PersonalScore +2` and a capture stat; `TnDominationMessage` per node (switch + 10·PointNumber).
- "Capturing" announcement throttle 15 s.

**EXT bomb** (C, `TnBombPlantPointBase`):
1. An attacker carrying the bomb touches the enemy plant point.
2. Planted: **fuse 15 s** (objective countdown on the HUD).
3. Defenders standing on it accumulate **5 s** to defuse; the progress resets when nobody is on it.
4. On detonation: `ScoreObjective(planter, 1)`, **HurtRadius 9999 dmg, radius 5000, AOE**, momentum 99999; the bomb returns home.
5. On defuse, the bomb spawns at the point (`DefuseBombSpawnClass`).

**Announcers (C):**

| mode | message classes |
|---|---|
| shared | `TnGameTypeMessage<Mode>` StartGame / NearlyComplete / EndGame; progress messages (time 30 / 60 / 120 s; kills 1 / 3 / 5 left; points 25 / 50 left for KOTH / DOM) |
| KOTH | hill dialog |
| DOM | `TnDominationMessage` |
| CTF | `TnCTFMessage` / `TnFlagMessage` |
| EXT | `TnBombMessage` |
| rounds | `TnRoundBasedGameMessage` |

**Pickups:** the same factories in every mode. Objective factories (flag, bomb) have RespawnTime 9999999, so they return only through their own return logic (C).

**Escalation (SV)** is co-op waves (`TnSurvivalGame`, iconic characters, `UI_CampaignLobby_m`). It is not versus.

## 4. Settings menu (FE)

Source: SettingsMenu_GFX AS2 (`mc_rootMenu` → submenus built with `mc_lateralSelectorInc`), defaults from `TnProfileSettings` (C).

| Category | Option (profile field) | Choices | Default | Xbox? | Runtime effect |
|---|---|---|---|---|---|
| Graphics | Brightness (opens Brightness_GFX) | gamma slider | **GammaSetting 50**; `HasAdjustedGamma` false (first-boot brightness prompt) | **yes (only Graphics item on Xbox)** | display gamma |
| Graphics | Resolution / Fullscreen / Texture Quality (Low / Med / High) / VSync / Commit | — | engine | **PC only** (`platform == 'WIN'`) | `PCSettings.*` |
| Audio | FX Volume | 0–100 step 10 | **80** | yes | — |
| Audio | Dialogue Volume | 0–100 step 10 | **80** | yes | — |
| Audio | Music Volume | 0–100 step 10 | **80** | yes | — |
| Audio | Subtitles | On / Off | **Off** | yes | — |
| Controls | Vibration (`Controller Vibration`) | On / Off | **On** (value 3) | yes | — |
| Controls | Layout | controller map per form: Robot / Car / Truck / Plane / Tank; console: **Scheme A / B** (`UseAlternateControlScheme`, default **A**) | — | yes (PC shows a keyboard list) | — |
| Controls | Invert Y Car / Jet / Tank / Robot | On / Off | **Off** | yes | applied per form to `PlayerInput.bInvertMouse` on form change |
| Controls | Camera Sensitivity | 0–100 step 10 | **30** | yes | `HmCamera.SetCameraSensitivity(normalized)` → `Lerp(Low, High)` per strategy: robot 0.8–1.5, hover truck 0.875–1.4375 |

- Hidden profile flag `SwitchRightThumbstickAndB` (default false) exists but is **not in the menu** (C: no binding in SettingsMenu).
- **Not in the original:** FOV slider, mouse-specific sensitivity UI (PC mouse uses `MouseCameraSensitivityX/Y 0.00114286` from config), key rebinding (PC shows a fixed list), difficulty for MP, network/account settings in this menu (accounts are a separate PC menu).

## 5. Frontend background (FE / RN)

**The background is a live 3D level, `UI_FrontEnd_m`, not a movie** (C). The level (TnWorldInfo, `TnFrontEndGame`) contains:
- **Cybertron orbit**: `ENV_NEU_CybertronOrbit_P` Core / Crust / SurfaceA / SurfaceB / IaconBuildings / KaonBuildings / BlastBuildings / Web / BlastDebris / CybertronShellLow;
- a `UI_FrontEndMaterials_p.SpaceDome` and 4 BlueNebulae cards;
- about 50 asteroid / debris meshes (`DES_ORB_Asteroids_p`);
- 20 glow spheres and 9 light-beam cones;
- 3 lens flares;
- FX: `Debris_Field_2_FX` ×2, `FX_cyberhalo`, `Lightning_Ripple_01_FX`, `UI_AntiAirFire_FX`;
- HeightFog ×2, a PostProcessVolume, and `SetPostProcessChain ENV_NEU_CybertronLow_P.CybertronSky_PostProcess_PP`;
- 48 InterpActors, 5 StaticMeshCollectionActors and a StaticLightCollectionActor.

**Camera:** Kismet starts the looping matinees "Primary Camera" (`CameraActor_6585`, FOV **45**) and "Camera Orbiter" (CameraDummy plus `CameraActor_6585`, with event track audio). "Fade In" runs after the logos / MovieLoader. `startMainMenuCamera` (fscommand) drives the energon ring / circuit matinee. Details are in bootstrap §1.2.

**The Scaleform menus are an overlay** on that 3D scene. Rendering them over black means the scene and its matinee cameras aren't running (H).

## 6. Loading behaviour (FE / Integration)

| finding | source | conf |
|---|---|---|
| The loading movie is a **Bink played by a rendering-thread movie player**, so it keeps animating while the game thread blocks loading packages | xex strings `HmCreateRenderingThreadFullScreenBinkMoviePlayerCommand`, `HmDestroyRenderingThreadFullScreenMoviePlayerCommand`, `EnableLoadingMovieCommand`, `IsLoadingMoviePlayingCommand`, `SetLoadingMovieFileNameCommand`, `SetDefaultLoadingMovieRenderer`; `[LoadingMovie] DefaultFileName=TF_LoadingScreen` | C (names) / H (semantics) |
| GFx text overlay `AlphaFileName=UI_GFxLoading_p.LoadScreenAlpha_GFX` plus LoadScreen_GFX (title / map / tips with a `setInterval` cycle), fed by deferred calls `_global.SetLevelText` / `AddEngageText` queued before travel (`HmMoviePlayer.AddDeferredMethod`) | bootstrap §3.3 | C (data) / P (how the overlay renders during the block) |
| Movie options per load: `LoadingMovieLoadStreamed` / `LoadingMovieLoadPreloaded`, `LoadingMovieSkipAllowed` / `Disallowed` (URL options and SeqAct) | xex strings, `SeqAct_LoadMap.BuildLoadingMovieURLOptions` | C |
| **Close condition:** `PlayerController.CanCloseLoadingMovie` = (not a client waiting on initial streaming state) && `HasCompleteGameContext()` | Engine script | C |
| Async / streaming: `bUseBackgroundLevelStreaming=True`, texture streaming on; `FlushAsyncLoading` exists; seamless travel (`TnGame.bUseSeamlessTravel`) via `TransitionMap=UI_FrontEnd_m`; lobby **prestreams** the selected map (`UpdateMapPrestreaming`) | config / script | C |

Behavioural summary: the original never shows a frozen frame. The Bink runs independently of the game thread until the new world reports a complete game context.

## 7. Multiplayer character selection (GP / FE / AT)

**Default MP characters** (`TR_MPPlayerCharacterData_p.*_PCD_MP`, C). One entry per specialty; each carries both factions.

| Specialty | Chassis (Autobot / Decepticon) | Weapons | Abilities | Vehicle weapon | Melee |
|---|---|---|---|---|---|
| **Leader** | Truck3 / Truck4 | IonBlaster, GrenadeLauncher, KamikazeMines | Warcry, Barrier | RocketVehicle | Axe / ViciousAxe |
| **Scientist** | Jet4 / Jet | BurstRifle, RepairRay, HealGrenades | SpawnSentry, Shockwave | HomingRocketVehicle | BeatDownClub / SpikedBat |
| **Scout** | Car2 / Car4 | Shotgun, HeavyPistol, FlashBangs | Cloaking, Dodge | AssaultRifleVehicle | ShortSword / TortureSword |
| **Soldier** | Tank3 / Tank2 | AssaultRifle, HomingRocket, FlakGrenades | Whirlwind, Hover | TankCannon | Maul / Hammer |

**Faction resolution (C):**
- `TnGame.GetResolvedCharacterFaction = TeamNum` (0 Autobot, 1 Decepticon); FFA forces 1.
- At spawn, `ResolveReplicatedCharacterData` picks the per-faction chassis, colours and melee from the selected character's parallel arrays.
- **The same custom character becomes an Autobot or a Decepticon body depending on team.**

**Flow (C):**
1. In the match, UI state WaitingOnGameStart opens **CustomTransformers_GFX** ("Select a Transformer").
2. `Customize.SelectCharacter` → `TnPlayerController.SelectCharacter(name, type)`, where type 0 = custom and 1 = iconic.
3. → `ReplicateCharacterData` → `PRI._SelectedCharacter`.
4. **Spawn waits until `HasSelectedCharacter()`.** In-match changes notify "CharacterSelectedInGame" and apply at the next spawn.
5. Iconic mode uses `GetPlayableIconicCharacterNames`; a `?Character=` URL option auto-selects (`SelectPieCharacter`).

**Customization:**
- Slots unlock at levels **5 and 10** (`UnlockCharacterSlotLevels`), with 5 colour palettes.
- Saved in the customization file (`CharacterCustomizationFilename`).
- Skills, weapons and abilities are chosen per specialty in CustomTransformers.

**Persistence:** `TnGameReplicationInfoMultiplayer.RetainSelectedCharacterOnTransition = false` (the base GRI is true). `TnPRI.CopyProperties` only carries the selection when that flag is set, so **in MP the choice is not carried across travel** (H: depends on which GRI is current during the copy).

**Preview model:** CustomTransformers uses `Customize.UpdatePreviewCharacter` / `TransformPreviewCharacter` (the `TnCustomizationPawn` in `UI_CharacterCustomization_m`). U: the default list focus.

**AT:** map chassis IDs (Truck3, Car2, …) to `TnTransformer` defs through `TnCustomCharacterOptions.FindChassis` (config `defaultgame` UniqueIds; P).

## 8. Bots / AI (GP)

**Shipped WFC multiplayer had no bots** (C by exhaustive absence):
- No bot count, AddBots or skill settings anywhere in the MP game, lobby or settings classes, the TDM settings, the settings menu or the playlists.
- `NumBots` and `bBot` are stock Engine fields. `bBot` is set by the stock PRI when its owner is an AIController and is only **read** to filter AI out of lists (debug, testing).
- Automated MP testing used real test clients driven by `TnMultiplayerGameTestingPolicy` (playlist joins, auto character pick), not bots.

**Existing AI** (strongest base for a future, clearly non-original offline-bot feature):
- `TnAiController` (AIController) + `TnAiPawn` with **GOAP planning** (`TnAiPlanningScheduler`, `HmGoap*`, `TnGoapGoal*`, ~177 `TnAi*` classes including transform actions `TnAiActionTransformToVehicle` / `ToRobot`, hover, shooting, navigation) and a **tactical system** (`TnTacticalSystem`, `TnAiTacticalEvaluationScheduler`, HmOctree).
- **These schedulers are instantiated by every `TnGame`, including `TnMultiplayerGame`** (defaults `_AiPlanningScheduler`, `_TacticalOctree`).
- Campaign **buddy AI** (`TnGoapGoalBuddyLead`, `TnSeqVar_Buddy`, `TnCustomCostAwayFromBuddy`).
- Escalation wave AI (`TnSurvivalSpawnList`, `TnSurvivalSpawnPoint`).
- AI weapons use separate `AiData` WEPDATA.

Any MP bot is a **reconstruction feature**, not original WFC.

## 9. Regen, death presentation, scoreboard (GP / FE)

- **Regen** (C): 20 HP/s after 2.0 s without damage, current segment only. **Parameters come from the robot blueprint (`TnPawn._Blueprint`) in both forms.**
  - The truck form blueprint also authors `HealthRegenParameters` (12 HP/s / 7 s), but no script reads it (H: unused).
- **Death presentation** (C):
  - Death type → `TnDeathBlueprint` entry. `SharedRobotDeaths` `TotalTime` ranges from **1.25–1.5 s** (booster) to **1.5–3.5 s** (energy); e.g. headshot 1.25–2.0, melee 1.5–2.75, explosive 1.25–2.0. Car deaths: moving 0.3–0.75 s, stationary 0.2–0.5 s (`Death_Hover_VEH`).
  - The controller enters `Dead` (death camera) → after **3.0 s** spectating plus the respawn UI → **5.0 s** respawn.
- **Scoreboard** (C):
  - `ShowScores` (Back / Tab) is a **toggle**: `TnHUD.SetShowScores(!bShowScores)` starts InGameStats_GFX with **input focus** (`SetFocus(true, true)`) and pushes `_global.UpdatePlayerListData`. A second press closes it.
  - The scoreboard is force-closed when the HUD is hidden.
  - Disabled in non-competitive campaign games.

## HANDOFFS

### Gameplay
- §1 states and constants: hover yaw = camera, no throttle in boost, Dash / Nitro split, jumps.
- §2 hover suspension rewrite: 4 diagonal 250 UU rays, normal-weighted springs, 45° ground, yaw-only on contact, upright only when airborne or upside down.
  - Boost: short suspension, frontal-hit exit to hover, no auto-upright.
- §3 all versus modes.
- §8: no original bots.
- §9 timings.

### Frontend
- §1.1 bindings (keep the PC originals).
- §4 settings table: Xbox vs PC-only; FOV etc. are additions.
- §5 run the 3D `UI_FrontEnd_m` scene under the menus.
- §6 loading: an independent movie thread.
- §7 the CustomTransformers selection flow.
- §9 scoreboard toggle.

### AssetTools
- Export `TR_MPPlayerCharacterData_p` (4 MP presets).
- `HoverTruck_Physics` / `HoverTruck_Suspension` and `Truck_Physics` blueprints.
- The `UI_FrontEnd_m` scene actors and matinee data.
- Chassis-ID → TnTransformer mapping.

### Rendering
- Frontend scene and post chain (§5).
- Hover booster FX `Size` param driven by thruster contribution (§1.2).

## STILL OPEN
- Native `GetNormalizedPropertyValue` scale for CameraSensitivity (assumed value / 100).
- The Vibration "3" encoding.
- The default focus in CustomTransformers.
- Exact GFx overlay rendering during a blocking load.
- `TnCustomCharacterOptions` chassis table source.
