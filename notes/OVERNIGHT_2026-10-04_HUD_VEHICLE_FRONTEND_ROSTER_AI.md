# Overnight RE handoff (2026-10-04): HUD, vehicles, settings/input, frontend backgrounds, roster, AI, mode gaps

**Labels:**
- **C** = CONFIRMED (bytecode / AS2 / authored data / shipped config read directly).
- **H** = HIGH.
- **P** = PARTIAL.
- **U** = UNKNOWN.

**Owners:** **GP** Gameplay, **FE** Frontend, **RN** Rendering, **AT** AssetTools.

**Builds on** (not repeated here):
- `MILESTONE05_PLAYTEST_RE.md` (vehicle states, suspension, mode table, settings, bots);
- `MILESTONE05_GAMEPLAY_UNKNOWNS.md` (markers, pickups, transform, KOTH, CTF);
- `MILESTONE05_FRONTEND_GAMEPLAY_BLOCKERS.md`.

**New tools:**
- `tools/gfxplace.py`: named PlaceObject placements with matrices.

**New data:**
- `notes/data/mp_chassis_roster.json`.

---

## A. In-match HUD (FE / RN)

### A0. Ownership

| System | What it draws | Source |
|---|---|---|
| **Scaleform** `UI_GFxHud_p.Hud_GFX_1` (`TnHUD.HudMovie`) | everything in A1 | `Default__TnHUD` |
| **Scaleform** `UI_GFxInGameStats_p.InGameStats_GFX_1` | scoreboard (toggle) | `TnHUD.ScoreboardMovie` |
| **Scaleform** UIController movies | pre-match countdown, respawn screen, end-game stats, pause | B §1.4 |
| **Canvas** (UnrealScript `TnObjectiveMarkerType*`, materials in `UI_HudMarkers_p`) | player name tags, objective markers, tombstones, lock-on markers | Phase 8 note §5 |
| **Material / post-process** | damage and low-health effects | P (not traced this pass) |

**Stage:** 1120×720. **The HUD root `hud_mc` places 9 safe-frame anchors** (C, `gfxplace.py`):

|  | left | center | right |
|---|---|---|---|
| top | topLeft (84, 54) | topCenter (560, 54) | topRight (1036, 54) |
| middle | midLeft (84, 360) | midCenter (560, 360) | midRight (1036, 360) |
| bottom | bottomLeft (84, 666) | bottomCenter (560, 666) | bottomRight (1036, 666) |

Anchor positions are re-aligned on stage resize (`alignLeft` / `Center` / `Right`, `alignTop` / `Mid` / `Bottom`). `incapacitated_mc` (downed screen) sits at the root (560, 360).

### A1. Element map (C: element clip + offset from its anchor = absolute position at 1120×720)

| Element | Clip (char) | Anchor + offset → abs | Engine → AS input | Notes |
|---|---|---|---|---|
| **Health / overshield bar** | 572 | topLeft +(20, 10) → (104, 64) | `_global.NotifySegmentedHealthChanged(fullSegments, curSegNorm, totalSegments)`, `NotifyOverShieldChanged` | one `mc_vitalBarHealthSegment` per segment, **spacing 38 px**, whole widget **skewed −8°**; background width `31 + 38·N`; damage leaves a `mc_vitalBarActiveBarDrained` ghost (red 0xFF3333 if segments remain, white otherwise); **low health**: last segment ≤ **0.9** → segments red 0xFF3333, `lowHealthFlash_mc` loops (normal colour 0x50B5D5); a hidden number text = `segFull·50 + ceil(cur·50) + ceil(overshield·100)` |
| Team chat / speaking list | 573 | topLeft +(15, 130) | `<CurrentGame:Players>` | `mc_teamchatPlayer` |
| Ability 1 | 588 | topLeft +(24, 70) | `NotifyAbilityType1Changed`, `…UpdateCooldown`, `AbilityType1Jammed` | — |
| **Kill feed / game messages** | 591 | bottomLeft +(0, −40) → (84, 626) | `_global.GameMessage(html)` | §A2 |
| Ammo pickup notify | 593 | topRight +(−115, 65) | `NotifyAmmoAdded` | — |
| **Ammo** | 600 | topRight +(−20, 10) → (1016, 64) | `NotifyWeaponClipAmmoChanged(clip, cap)`, `NotifyWeaponReserveAmmoChanged` | §A3 |
| Grenades | 601 | topRight +(10, 46) | `NotifyGrenadeAmmoChanged`, `ShowGrenades` | `mc_grenadeIcon` (Frag / KMine / Heal / Flashbang) |
| Ability 0 / vehicle ability (2) | 603 / 605 | topRight +(−24, 70) | `NotifyAbilityType0/2Changed`, cooldown, jammed | robot form shows 0, 1 and grenades; vehicle form shows 2 (`NotifyCurrentFormChanged`) |
| Objective list | 607 | bottomRight +(−340, −124) | `AddObjective` | `mc_objectiveNew` |
| Killstreak | 608 / 609 | bottomRight +(−100, −27) / (−50, −97) | `NotifyKillstreakChanged`, `ApplyKillstreakBuff` | D-pad prompt `mc_killstreakDpadXbox360` |
| Wave indicator (Escalation) | 610 / 639 | — | `<CurrentGame:_CurrentWave>`, `_NextWaveTime` | SV only |
| **Crosshair / hit markers** | 621 | midCenter (560, 360) | `SetWeaponCrosshair`, `NotifyWeaponSpreadChanged`, `NotifyTargetTypeChanged`, `CausedDamage`, `NotifyDamageIncrease`, `DisplayRangeFinder`, `DisplayTurretReticule`, `NotifyFineAimChanged` | per-weapon crosshairs `mc_crosshairIonBlaster / Bazooka / Shotgun / Generic`, scopes `mc_short / medium / long / zoomScope` |
| **Damage direction arrows** | 622 | midCenter | `NotifyDamageIndicatorAdded`, `NotifyPlayerRotationChanged` | `mc_damageArrow` (the only directional threat display) |
| **Score widget** | 633 | topCenter +(0, 5) → (560, 59) | `<CurrentGame:GameTeamStatus>` | TDM → `mc_scoreTeam` (Phase-8 §HUD) |
| **Match / round clock** | `countdown_mc` (632) | topCenter +(0, 50) → (560, 104) (y 10 without a scoreboard) | `<CurrentGame:CurrentCountdown>` | MM:SS, red flash ≤ 10 s |
| **Game / reward announcements** | 638 | topCenter +(0, 112) → (560, 166) | `_global.GameAnnouncement(text)`, `_global.RewardAnnouncement(text)` | §A4 |
| **Score / XP popups** | 640 | topCenter +(0, 175) → (560, 229) | `_global.PointEvent(id, award, announcement, description, extra)` | §A4 |
| Level up | 643 | midRight +(−80, 0) | `NotifyLevelUp` | — |
| Bad connection | 644 | midRight +(−30, −90) | `NotifyBadConnection` | — |
| Contextual prompt ("Press X to …") | `notifyManager_mc` (646) | bottomCenter +(0, −30) | `NotifyContextualCommand` | `mc_notify` fades in 0.2 s, out 0.5 s |
| Flag-return progress | `returnFlagNotifyTime_mc` (652) | bottomCenter +(0, −100) | `TnHudDataObserverSingleFlagCTF` | CTF only |

### A2. Kill feed (C)

**Generation** (`TnDeathMessage.GetColoredString`):
- Template = the damage type's `DeathString` (or `Suicide` when switch 1), from `TransGame.int`. Examples:
  - `[TnDamageTypeIonBlaster] DeathString=` `` `k [IonBlast] `o ``, `Suicide=` `` `o [Suicide][IonBlast] ``;
  - generic `` `k destroyed `o ``;
  - `DmgType_Suicided` → `` [Suicide] `o ``.
- `` `k`` = killer `GetPlayerAlias()`, `` `o`` = victim. AI names go through `Localize("AICharacterNames", …)`.
- **Colours** (`TnMessageTextColors`):

| who | colour |
|---|---|
| **local player** | **white** (255, 255, 255) |
| **teammate** | (80, 181, 213) |
| **enemy** | (240, 60, 60) |
| plain words | neutral (255, 147, 51) |

- Each part is wrapped as `<font color='#RRGGBB'>…</font>`; `TnHUD.ColoredLocalizedMessage` → `_global.GameMessage`.

**Presentation** (Hud_GFX sprite 591 / row 318):
- Bracket tokens are replaced by bitmaps (`setImageSubstitutions`, **scale 0.85, baseline 23**). Token → icon:

| tokens | icon |
|---|---|
| `[Bazooka] [HvyPistol] [PlasCannon] [GrenLaunch] [HvyMG] [AssRifle] [IonBlast] [BrstRifle] [HmgRocket] [EMPShotgun] [Shotgun] [RepairRay] [SnprRifle]` | `death_<weapon>` |
| `[Melee]` | `death_Melee` |
| `[Car] [Truck] [Jet] [Tank]` | ram / vehicle |
| `[FragGren] [KamiMine]` | `GrenadeIconFrag` / `GrenadeIconKMine` |
| `[Decoy] [RollSphere] [TransDisrupt] [Shockwave] [Drain] [Sentry] [Rocket] [HvyTurret]` | `death_*` |
| `[Suicide]` | `death_Suicide` |

- **Newest row at slot 0** (anchor y); older rows move up **22 px** per slot (0.2 s ease). **More than 5 rows** → the oldest fade out.
- **Each row lives 5.0 s**, then fades over 1.0 s and is removed.
- Text shadow: alpha 0.6, strength 2.5, blur 5.
- Spectating moves the whole feed up 160 px (`GameMessageSpectatorMode`).
- **No assist line.** Environment kills use the damage type's string with no killer.

### A3. Ammo widget (C, sprite 600)

- Skewed **+8°**. Clip bar: `mc_ammoBar` segments, **ClipSegmentCap 60**, bar colour **0xFFA033**.
- **Low clip** (≤ **25 %**) → bar 0xFF5555, icon flashes red, reload prompt (`displayReloadPrompt`).
- **Low total** → weapon icon and number turn red (0xFF3333).
- Number = clip + reserve; **infinite reserve (<0) shows the ∞ bitmap** (26×13).
- Warnings (`updateAmmoWarning` 0 / 1 / 2: none / low / empty): `mc_ammoWarningTextLow` / `Empty` / `Reload`.

### A4. Announcements and popups (C, sprites 638 / 640)

- **GameAnnouncement:** scales from 500 % → 100 % and fades in over 0.4 s; **holds 4.5 s**; then scales to 500 % and fades out over 0.4 s.
  - Used for the game-type start text (`TnGameTypeMessage` switch 0, e.g. "Team Deathmatch") and kill-streak / mode texts.
- **RewardAnnouncement:** slides y 28 → 18 and fades in over 0.4 s; **holds 4.8 s**; fades out over 1 s.
  - Also used for "$UIText.Hud.TeamAttacking / TeamDefending" in round modes.
- **PointEvent (XP / score popups)** (from `TnHudDataObserverXpTransactions` per XP event: award amount, `Announcement`, `Description`, `ExtraData`):
  - queued; each popup shows **2.0 s** (**4.0 s** for `ExtraData[0]=='Killstreak'`, and those jump the queue);
  - 0.2 s between items; consecutive events with the same TransactionId update the current popup;
  - popup scales in over 0.5 s, rises 100 px over 1 s, fades out over 1 s.
  - **Values:** Kill 50 XP (DM 25), FirstKill 100, KillerLowHealth 75, EndKillStreak 75, flag / bomb carrier kill 100 (`Xe-TransGame.ini [TnXpEventType*]`).

### A5. Match start / end presentation (C)

- **Start** (`TnGameTypeMessage` switch 0): HUD GameAnnouncement with the mode name; announcer `GameTypeDialog` + `GameDescriptionDialog`; music `GameTypeMusic`.
  - TDM: "Team Deathmatch", `MP_GameTypeTeamDeathMatchDialog`, `MP_GameDescriptionTeamDeathMatchDialog`, `BL_LVL_MP_MX.DM_START`.
- **Nearly complete** (switch 1): music `DM_FINALSTRETCH_LP`.
- **End** (switch 2): music `DM_END_AUTOBOTS_WIN` / `DM_END_DECEPTICONS_WIN` / `DM_END_TIE` by winner team.
- **Victory / defeat text** (`TnVersusGameOverMessage.ClientReceive`):
  - announcer `MP_GameAutobotWin` / `MP_GameDecepticonWin`;
  - **`GRI.SetGameOverMessage`** = "Your team won" / "Your team lost" / "Tie game" / "Enemy team forfeits" (from the receiving player's perspective).
  - This text is shown by **EndGameStats_GFX** (`<CurrentGame:GameOverMessage>`), not by the HUD.
  - DM: `TnFreeForAllGameOverMessage` sets an **empty** game-over message.
- **Sequence:**
  1. `EndGame` → `CheckEndGame` → messages and music;
  2. after 1.5 s, end-game handling (stats);
  3. MatchOver: UI event 9 → **HUD hidden**, EndGameStats opens;
  4. all controllers in `RoundEnded` (frozen, death camera);
  5. after **15 s**, `ReturnToGameLobby` travel.

  The results screen belongs to the UIController (frontend movie), not to `TnHUD`.

### A6. Death and respawn screens (C)

- **Death:** death camera + death animation (`TnDeathBlueprint` 1.25–3.5 s by type); the HUD stays in UI state InGame.
- After **3.0 s** → Spectating: HUD visible plus **MultiplayerRespawn_GFX** (`<PlayerOwner:TimeToRespawn>`, team status). The kill feed shifts up.
- **Respawn at 5.0 s.**
- **Downed** (only with `TnSkillCanBeDowned`): `incapacitated_mc` screen.

### A7. Scoreboard (C)

- Back / Tab **toggles** InGameStats_GFX with input focus.
- **Columns:** Level · Name · Score · Kills · Deaths; team rows sorted by score.
- Auto-closes when the HUD is hidden.

### A8. HUD visibility (C)

| condition | HUD |
|---|---|
| UI states InGame, Spectating | visible |
| GameEnded, pre-match screens, pause | hidden |
| `ToggleHUD` (`ToggleHudFlag`), cinematic mode (UI events 12 / 13), `ForceHudInvisible` | hidden |

### A9. Minimap / radar (C, by exhaustive absence)

**Shipped WFC multiplayer has no minimap, radar or compass.** Searched:
- all decompiled UnrealScript;
- every UI GFx constant pool and export (Hud_GFX has no map clip);
- the `authored.db` object paths;
- `default.xex` strings (`Radar`, `MiniMap`, `Minimap`, `Compass`, `Blip`: 0 hits).

The only spatial cues are:
- **damage-direction arrows**;
- missile-lock warnings (`mc_missileWarningVictim*`);
- Canvas objective markers with off-screen edge arrows;
- ally name tags.

Enemy tags appear only through buffs such as the `OrbitalReconStreak` killstreak or HardLock. **The rebuild must not add a minimap as "original".**

## B. Vehicle behaviour gaps (GP)

### B1. LT / RMB in vehicle form

- **LT / RMB in vehicle form is Boost only** (C): `TnPlayerController.FineAim` / `CanFineAim` do nothing outside `PlayerWalking`, and `PlayerInCarForm.OnStartBoost` sets `CarForm.BoostingInput`.
- In robot form, `StartBoost` does nothing (base `OnStartBoost` is empty).
- **One physical key, two meanings by form. It does not change hover speed.**

### B2. Normal (hover) speed

- `HoverTruck_Physics` MaxLinearSpeed **1500**, accel **3000** (class defaults; the Optimus asset overrides only Dash, AI and suspension values) (C).
- Boost top speed is `Truck_Physics` MaxSpeed **3000**; Nitro ×1.5.

### B3. Vehicle → robot under an overhang

1. `StartTransform` → `MoveToSafeTransformationLocation(target)` → `FindSpotAwayFromPawns(target extent)`.
2. **If no spot:** HUD `NotifyCantTransform` (`mc_cantTransform`) + `TransformFailedSound`, and **no transform** (C).
3. If the spot is displaced: collision moves immediately and, for the robot target, the meshes slide back over **0.5 s**.
4. After the transform, `InRobotForm.BeginState` (authority) runs `MoveToSafeLocation`. If that fails → **"Still stuck in robot form. Transforming back to vehicle"** → `ForceIntoForm(vehicle)` (C).

P: whether the native `FindSpotAwayFromPawns` tests world geometry as well as pawns.

- `TnDisableTransformingVolume` disables transforming inside volumes (C, class exists).
- Ramps, suspension, upright and contact filtering: see `MILESTONE05_PLAYTEST_RE.md` §2 (no new contradictions found).

## C. Settings and input model (FE)

**Settings menu:** complete table in `MILESTONE05_PLAYTEST_RE.md` §4. **There are no HUD options and no gameplay options** in the original menu (C).

### Input command model (C, `Xe-TransInput.ini`)

Keys bind to **named aliases** (`Fire`, `Boost`, `FineAim`, `Transform`, `VehicleSpecialMove`, `Ability0`, `Ability1`, `PressJump`, `Ascend`, `Descend`, `TossGrenade`, `XButton`, `KeyboardInteractKey`, `Melee`, `NextWeapon`, `Focus`, `TriggerKillstreak`, `ShowScores`, `showmenu`, `DownedSuicide`, `SkipMatinee`). Each alias expands to exec pairs (`StartBoost | OnRelease StopBoost`).

- **The controller's current state decides the meaning.** For example `Ability0 | VehicleSpecialMove`: the state that implements the exec reacts and the others no-op.
- **Implement PC input as alias → exec, with per-state handlers, not per-key logic.**
- Button prompts use `TnInputCommandToBindingMapper` (`^SWITCH_WEAPON`, `^SPEED_BOOST`, … → key) and respect Scheme B / the thumbstick swap.
- **Menus** use `GFxUI.KeyMap` (A = Enter, B = Escape, X = F1, Y = F2, LT = Home, RT = End, LB = PageUp, RB = PageDown, Start = F3, Back = F4, LS = F5, RS = F6, D-pad = arrows), and AS2 `inputEvent(inputType)` names: `navigateLeft / Right / Up / Down`, `buttonA / B / X / Y`, ….

FOV, resolution and keyboard rebind are **PC implementation extensions** (the shipped PC menu had resolution / fullscreen / texture / VSync only).

## D. Frontend backgrounds (FE / RN)

| Screen | Background owner | Refs | Conf |
|---|---|---|---|
| Boot logos / intro | Bink movies via Kismet `SeqAct_MoviePlayer` | Logo_Activision / Hasbro / HighMoon, FMV_intro | C |
| **Title / main menu / settings / extras / accounts** | **live 3D level `UI_FrontEnd_m`** (Cybertron orbit scene, looping matinee cameras FOV 45) **+ streamed `UI_FrontEnd_capture_VIG_m`** (battle vignette: SoldierJet fly-bys, UI explosions, laser and anti-air fire; matinees "1st / 2nd / 3rd QTR", "Plane Fly By") | `TnWorldInfo.StreamingLevels` (`LevelStreamingKismet` → `UI_FrontEnd_capture_VIG_m`, state Start) | C |
| **Party lobby (Multiplayer root, Host Game, Escalation entry)** | level `UI_PartyLobby_m`: almost empty itself (BSP, camera director, `Fade In`, lobby music), and **streams `UI_CharacterCustomization_m`** (initial state Customize). GFx fscommand `backgroundFadeIn` → Kismet fade | `UI_PartyLobby_m` WorldInfo | C |
| **Game lobby (private match)** | `UI_Lobby_m`: same structure; streams **`UI_CharacterCustomization_m`** (state Customization) | `UI_Lobby_m` WorldInfo | C |
| Campaign / Escalation lobby | `UI_CampaignLobby_m`: own SpaceDome static mesh (`UI_LobbyMaterials_p.SpaceDome_STAT`) + BSP; no streaming | — | C |
| **Create character / customization** | 3D level `UI_CharacterCustomization_m`: SpaceDome, 4 CybertronCard planes, preview robots (Sideswipe, Barricade skeletal actors at (−286, 5588 / 4702)), `CameraActor` FOV 70; matinees per class / faction ("SCOUT - Autobot", "LEADER - Decepticon", Autobot / Decepticon Glow / Fade) | Kismet in that map | C |
| Friends / leaderboards / Teletraan / challenges | GFx overlays on whatever level is current (frontend or lobby); they hide the parent menu (`hideContainer`) | AS2 | H |
| Pause | GFx `PauseMenu_GFX` over the live match (no world pause in MP) | B §6 | C |
| Loading | Bink `TF_LoadingScreen` on the render thread + GFx `LoadScreenAlpha` / LoadScreen text | Playtest §6 | C / H |
| Post-match | EndGameStats_GFX over the frozen match world (death camera, `RoundEnded`) | §A5 | C |

**Black menus in the rebuild mean the owning 3D level (or its streamed sublevel and matinee camera) isn't running under the GFx layer** (H).

## E. Multiplayer roster / loadouts (GP / FE / AT)

**Data:** `notes/data/mp_chassis_roster.json`, 33 chassis from `TransCustomization.ini` `TnDataProvider_Chassis`, joined with ROBODEF / VEHDEF. Fields: UniqueId, iconic name, **FactionRestriction** (0 Autobot, 1 Decepticon, 3 neutral), **DefaultSpecialty**, **LockedChassis / LockedCharacter**, CustomizationCameraId, robot skeletal mesh, AnimTree, vehicle form / class / mesh, hover and car blueprints, collision, momentum, damage multipliers, melee set, camera set.

**Unlocked by default** (`LockedChassis=false`) (C):

| class | chassis |
|---|---|
| **Scout** (car) | Car Bumblebee, Car2 Sideswipe, Car3 Breakdown, Car4 Barricade |
| **Scientist** (jet) | Jet Starscream, Jet4 AirRaid, Jet5 Jetfire, Jet6 Silverbolt |
| **Soldier** (tank) | Tank Megatron, Tank2 Brawl, Tank3 Warpath |
| **Leader** (truck) | Truck Optimus Prime, Truck2 Ratchet, Truck3 Ironhide, Truck4 Soundwave |

- Locked: Arcee, Jazz, Deadend, Thundercracker, Skywarp, Shockwave, Slipstream, Scattershot, Demolishor, Zeta Prime, Onslaught, Truck7 Optimus, the soldier and minion bodies.
- Unlock source is outside this pass (P: likely DLC / pre-order / progression flags).

**Default MP loadouts** (`TR_MPPlayerCharacterData_p`): table in the playtest note §7. Leader → Truck3 / Truck4, Scientist → Jet4 / Jet, Scout → Car2 / Car4, Soldier → Tank3 / Tank2.

**Base stats** (C):
- Player chassis share `TR_Health_p.SharedHealth` (segments 175 / 125 / 125 / 125, overshield 550) and BaseGroundSpeed **1400**.
- Per-class differences live in the momentum blueprint (Car / Truck / Plane / Tank), damage multipliers and abilities.
- The Optimus robot (AccelRate 12000, AirSpeed 1200, collision radius 200 / height 200) is the reference.
- AT should export all ROBODEFs for exact per-chassis values.

**Class-specific HUD** (C):
- the ally **health bar on name tags only for Scientist viewers**;
- ability icons per character (`TnAbility*` exports in Hud_GFX);
- vehicle ability slot 2.

**Progression gates** (C): custom slots unlock at levels 5 and 10. Specialty levels and XP drive unlocks; the backend is not needed for local presentation.

## F. AI architecture for future offline bots (GP)

**Shipped multiplayer had no bots** (playtest §8). The reusable original AI:

| Category | Classes / data | Notes |
|---|---|---|
| **CONFIRMED REUSABLE (generic)** | `TnAiController` (AIController), `TnAiPawn`; GOAP: `HmGoap*` (planner, plan runner, world state, goal / action / sensor sets), `TnGoapGoal*` (Kill, DefendSelf, MoveTo, Transform, Revive, Heal, Cloak, React, StayInTacticalVolume, UseInteract), `TnAiAction*` (~140: ShootFromTactical, Navigate, Melee, ThrowGrenade, TriggerAbility, TransformToVehicle / Robo, Dodge, Hover, VehicleNavigation, ShootAtTarget, LockOnTarget, …), sensors (`TnAiThreatSensor`, `BiggestThreatSensor`, `LineOfSightSensor`, `RangeSensor`), `TnAiTargeter`, `TnAiWeaponAimer`, `TnAiWeaponShooter`; **tactical system** (`TnTacticalSystem`, `TnTactical*` path-node evaluators: LOS, distance, hot spot, keep-in-range, LOS-to-team, battle line, occlusion) | `TnMultiplayerGame` already instantiates `_AiPlanningScheduler`, `_AiTacticalEvaluationScheduler` and `_TacticalOctree` (inherited from `TnGame`) (C) |
| **POSSIBLY REUSABLE (strongest base)** | **Campaign buddy definitions for player chassis**: `TR_AiCharacterDefinition_p.*_Buddy_AICD` (Optimus, Bumblebee, Sideswipe, Ironhide, Ratchet, Warpath, AirRaid, Silverbolt, Jetfire, Megatron, Barricade, Brawl, Starscream, Skywarp, Thundercracker) with action sets `Soldier_Truck_Buddy` / `Soldier_Jet_Buddy` / `Soldier_Tank_Buddy` / `Engineer_Buddy` / `Soldier_Jet_Engineer_Buddy`, `Buddy_AiGoalSet`, `Buddy_AiSensorSet` | these drive **full player Transformers** (transform, abilities); goals are follow / support (`TnGoapGoalBuddyLead`) and would need versus goals (Kill exists) |
| **MULTIPLAYER-SPECIFIC** | none shipped. MP spawn modifiers, objective actors and the `bBot` filters only | — |
| **CAMPAIGN / ESCALATION-ONLY** | soldier / brute / titan / sniper / jet-soldier / tank / minion AICDs (`TnAiJetSoldierPawn`, `TnTankAiPawn`, `TnMinionAiPawn`), bosses (Trypticon, Omega Supreme, Starscream / Soundwave boss), Escalation waves (`TnSurvivalSpawnList`, `TR_AiEscalation_p.*`) | AI weapon data uses separate `AiData` WEPDATA |
| **NAV DATA GAP (C)** | **MP maps carry no AI navigation data.** `MP_IAC_Streets` has only **426 `TnReachSpec`** (between its 60 `TnTeamPlayerStart` and pickup NavigationPoints) and **0 PathNode / TnTactical / TnTacticalPathNode / TnTacticalVolume**. For comparison, campaign D1 maps have 696 PathNode, 2,871 TnTacticalPathNode, 3,029 TnTactical, 56 TnTacticalVolume and 16,462 ReachSpecs. The original GOAP / tactical AI would need **new navigation and tactical data authored for MP maps**; that would be a reconstruction addition | authored.db class counts |
| **UNKNOWN** | how AI receives a team and character in a versus game | — |

## G. Mode gaps resolved (GP)

**CTF flag (C)**:
- `TnGameObjectivePickupFactoryFlag`: defenders can't pick it up (`ValidTouch` rejects `DefenderTeamIndex`). The carrier gets `TnWeaponFlag1Hand`.
- **Dropped flag** (`TnDroppedPickupFlagBase`): **auto-returns after 30 s** (`AutoReturnTime`).
  - **Defenders standing near it** drain `TimeLeftToReturn` (**10 s**) at **dt × number of defenders**; with no defender it recovers +dt up to 10.
  - At 0 → returned, `AddFlagReturned` for each returning defender, sent home.
- Attackers can re-pick a dropped flag. Falling out of the world sends it home.
- On capture: home with reason 3, sleep 0 → immediately available.

**EXT bomb (C)**:
- Dropped bomb auto-returns after **30 s**.
- After a detonation the factory sleeps **`WaitAfterScoreTime` 5 s**.
- `ObjectiveHolderChanged`: `GRI.AttackingTeam` = holder's team (HUD "attacking / defending" announcements). A carrier already inside a plant volume triggers the plant.
- Plant / fuse / defuse / explosion: playtest §3.

**Overtime:** none in any versus mode (C).

**HUD events per mode:**
- marker add / remove follows objective holders;
- announcements via `TnGameTypeMessage` / `TnCTFMessage` / `TnFlagMessage` / `TnBombMessage` / `TnDominationMessage` / `TnKingOfTheHillMessage` / `TnRoundBasedGameMessage` (switch numbers in the respective notes);
- the objective clock is `<CurrentGame:CurrentObjectiveCountdown>` (bomb fuse).

**KOTH, DOM, rounds:** confirmed earlier (Phase 8 note, playtest §3).

## STILL OPEN

- Post-process damage and low-health screen effects (material / post side).
- `FindSpotAwayFromPawns` native world-collision behaviour.
- Chassis unlock source.
- Per-chassis ROBODEF stat export (AT).
- Kill-streak list and costs.
- AI team / character binding in versus contexts.
