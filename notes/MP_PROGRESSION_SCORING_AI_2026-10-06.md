# WFC multiplayer: scoring, XP, levels, challenges, medals, scoreboard, bots/AI, navigation (2026-10-06)

**Labels:** C = CONFIRMED from script/config/data; H = HIGH; P = PARTIAL; U = UNKNOWN.

**Provenance:**
- TransGame/Engine script: `work/script/decomp/`.
- **TransContent script (game classes) decompiled from the map packages:** `work/script/decomp_tc/MP_ORB_Debris_BASE_m.TransContent.txt` and `MP_IAC_Streets_BASE_m.TransContent.txt`. TransContent has no package of its own; its classes are cooked into every map.
- Config: `ExtractedAssets/config/Coalesced_ini.json` (Xe-TransGame.ini, TransChallenges.ini, TransCustomization.ini, TransPlaylists.ini) and `Coalesced_int.json` (INT text). Authored data: `AssetTools/manifests/authored.db`, `inventory.db`.

**Machine-readable tables** (regenerate with `tools/mp_progression_extract.py`):
- `notes/data/mp_xp_events.json`
- `mp_level_table.json`
- `mp_challenges.json`
- `mp_class_unlocks.json`
- `mp_game_modes.json`
- `mp_kill_awards.json`
- `mp_navigation_audit.json`

---

## 1. Match scoring (C unless marked)

### Mode composition

Settings CDOs are `TransGame.Default__TnOnlineGameSettings<TAG>`. The time-limit defaults are the `LocalizedSettings` index into the ini `TimeLimits`.

| Tag | Name | Game class | Rules (in order) | Points to win (default / options) | Time limit default (options) | Rounds |
|---|---|---|---|---|---|---|
| TDM | Team Deathmatch | TnVersusGame | ScoreKillsTDM, TrackKillsMP, ReportGameProgressTime, ReportGameProgressKills | **40** / 20, 30, 40, 50 | **900 s** (600/900/1200) | – |
| DM | Deathmatch | TnFreeForAllGame | ScoreKillsDM, TrackKillsMP, ReportGameProgressTime, ReportGameProgressKills | **20** / 10, 20, 30 | 900 (600/900/1200) | – |
| DOM | Conquest | TnVersusGame | ScoreKillsMP, ScoreDomination, TrackKillsMP, ReportGameProgressTime, ReportGameProgressPoints | **400** / 150–500 | 900 (explicit property) | – |
| CTF | Code of Power | TnVersusGame | ScoreKillsMP, SingleFlagCTF, ScoreFlags, TrackKillsMP, ReportGameProgressTimeCTF | – | **300 s per round** (240/300/360) | **2** / 2, 4, 6 |
| EXT | Countdown to Extinction | TnVersusGame | ScoreKillsMP, ScoreBombingRun, TrackKillsMP, ReportGameProgressTime | **3** / 1, 3, 5 | 900 | – |
| KOTH | Power Struggle | TnVersusGame | ScoreKillsMP, ScoreKingOfTheHill, TrackKillsMP, ReportGameProgressTime, ReportGameProgressPoints | **400** / 150–500 | 900 | – |
| SV | Escalation | TnSurvivalGame | CompetitiveScoring, TrackKills | – | – | waves |

- `TnMultiplayerGame.InitGame` reads URL options `PointsToWin` (→ GoalScore) and `Rounds`.
- Public variants carry StatsWriters `<Mode>, Kills, Accuracy`.
- Private variants set **`bUsesStats=false`**.
- MaxPlayersAllowed 10, NumRequiredPlayers 4 (versus).
- `MatchAutoStartCountdown` 10 s, `MatchOverCountdown` 15 s, then return to the lobby.

### Score sources

`PRI.AddScore(personal, team)` adds the personal amount to `PRI.Score`, and the team amount to `Team.Score` only when it is > 0.

- **Kill** (`TnGameRules_ScoreKills.ScoreKill`):
  - Requires DamageType ≠ `DmgType_Suicided`, Killer ≠ none, and `ShouldScoreKill`. MP variants require the victim to be a `TnPlayerController`, so AI/sentry kills score nothing.
  - Then **personal +1**, **team +TeamScoreAmount**: TDM and DM = 1; DOM/CTF/EXT/KOTH (`ScoreKillsMP`) = 0, i.e. kills never add team score in objective modes.
  - **Self-kill:** +0/+0.
  - **Suicided damage type / environment (Killer none):** no score.
  - **No negative score** anywhere.
- **Deaths:** `AddDeaths(1)` for every player death, including suicide and environment.
- **Objectives** (`TnGameRules_ScoreObjectives.ScoreObjective(Scorer, Score)`): `Scorer.AddScore(IndividualScore, Score)`.

| Mode | Event | Team | Personal | Source |
|---|---|---|---|---|
| CTF | Code captured (`TnFlagCapturePointBase` → ScoreObjective(PRI, 1)) | **+1** | **+10** | ini IndividualScore |
| EXT | Bomb detonated (`TnBombPlantPointBase` → ScoreObjective(Planter, 1)); fuse 15 s, defuse 5 s | +1 | +10 | |
| KOTH | Each second, each living pawn in the active zone (ScoreInterval 1, PointsPerInterval 1) | +1 | +1 | zone active 60 s (see MP_SWEEP S4) |
| DOM | Each held node, every **3 s** → ScoreTeamObjective(owner, 1) | +1 | 0 | CaptureTime 20 s (scaled by attacker count) |
| DOM | Capture | 0 | **+2** each capturing player (PersonalScoreAmount) | |

**Assists:**
- The *first* other damager in the victim's damage history gets `AddAssist(damage / HealthMax)`.
- More than 0.5 → Assist XP; more than 0.25 → WeakAssist XP; plus an assist stat.
- **Assists never add score.**

**End conditions:**
- `CheckScore` after every kill or objective: team games compare the **team** score, FFA compares the **personal** score, against `GoalScore` (when > 0). Then `EndGame(Scorer, "Score")`.
- **Time limit:** `GRI.RemainingTime ≤ 0` → `EndGame(none, "")` (not for CTF, whose rounds drive their own timer).
- **Forfeit:** a team with 0 players (`TnVersusGame.CheckForfeit`, 1.5 s after a logout) → that team's score is cleared → `EndGame(none, "Forfeit")`.
- **CTF:** rounds alternate attacker (the first is random). A round ends on time-up (round time = TimeLimit) and the game ends after `Rounds` rounds.
  - **Mercy:** in the last round, if the last attacking team already leads, the game ends early.
  - Between rounds: 5 s.
  - **An odd round count logs an error.**

**Winner, ties and overtime:**
- `TnGame.EndGame` substitutes `GetWinningPRI()` (highest individual `PRI.Score`; the first found wins a tie) when Winner is none.
- `TnVersusGame.PickWinningTeam`: the higher team score, or the team whose opponent is empty. **Equal → none → "Tie game"** (TnVersusGameOverMessage switch 1).
- **No overtime:** `bOverTime` is only set when CheckEndGame refuses, and no WFC rule refuses.
- DM: `TnFreeForAllGame.CheckEndGame` sets Winner = top PRI.
- Completion type per player (stats): 0 win, 1 loss, 2 draw (FFA: draw when another player has an equal score).

**Win/lose XP quirk (C):** `TnVersusGame.CheckEndGame` gives **GameWin XP to every player on `Winner.Team`**, where `Winner` is the PRI passed in. On a time-limit end that is the team of the **highest individual scorer**, even when the team scores are tied or that team lost on team score. Everyone else gets GameLose.
- **FFA (DM) awards no win/lose XP at all.** Its DeathmatchXpAmount values (150/75) are configured but unused.

**Announcements:**
- `TnGameRules_ReportGameProgressTime` at 120 / 60 / 30 s left; the 60 s one notifies "nearly complete", which switches to the final-stretch music.
- `ReportGameProgressKills` at 5 / 3 / 1 kills left.
- `ReportGameProgressPoints` at 50 / 25 left.
- Cues in `TnGameProgressAnnouncementMessage.Sounds` (MP_2MinutesLeft … MP_1KillRemaining).
- Mode intro dialogs, music and win/tie music: `TnGameTypeMessage<Mode>`.

**MVP (achievement 37):** at match over, every PRI tied for the top personal score, provided there is more than one player and the match can gain XP (versus also needs both teams non-empty).

---

## 2. XP (C)

**Award rule** (`TnXpEventType.GetAwardAmount`):
- 0 if `!GRI.CanGainXp()`.
- Otherwise `GlobalXpMultiplier (1) × (DeathmatchXpAmount if ≥0 and !bTeamGame else XpAmount)`.
- Full table, with localized Announcement/Description: `mp_xp_events.json`. 71 types.

| Source | XP (team / DM) | Notes |
|---|---|---|
| Kill | 50 / 25 | every kill on a player (TnKillAwardManager.AwardKill first) |
| Assist (>50 % HealthMax) / weak (>25 %) | 25/15 · 15/10 | |
| Headshot ("Domed") | 75 | not for ExemptFromAccuracyKills damage types |
| Long range (>8000 UU) | 50 | |
| First kill / first death | 100 / 75 | once per match |
| Kill streak 3 / 5 / 7 (exactly at 3, 5, 7 kills) | 100/50 · 150/100 · 200/150 | |
| Multikill 2 / 3 / 4 (kills ≤ **3.0 s** apart; PRI MultiKillDetector) | 100/50 · 150/100 · 200/150 | exact level |
| End an enemy's streak (victim streak > 2) | 75 | |
| Payback / payback after domination | 50 / 50 | |
| Domination 2 / 3 / 4 (same victim repeatedly) | 20 / 40 / 60 | |
| Melee kill, per class (Scout/Scientist/Soldier/Leader) | 25 | + per-class stat |
| Killer low health (<50 HP) / killer downed / kill after death | 75 / 150 / 25 | |
| Backstab (melee with TnBuffIncreaseMeleeDamageFromBehind effective) | 100 | |
| Hover-melee kill (victim hovering, melee) | 50 | |
| Buff kills | 25–100 | killer buffs: disguise 100, hover 100, surprise attack 50, warcry 25, flashbang 50; victim defensive: warcry 50, hover 50, disguise 100; offensive (victim debuffed by killer): transform disruptor 50, mark target 100, drain 50, flashbang 50, decoy trap 100; **assist XP to the debuffer** if someone else kills |
| Damage-type kills | 50 / 50 / 150 | whirlwind / shockwave / ram |
| Objective-carrier kills | 100 / 100 | flag carrier (CTF only), bomb carrier (EXT only) |
| Zone / node kill | 20 / 20 | KOTH active zone, DOM enemy-held node |
| Sentry / mine / roller-mine kill | 25 (sentry DM 15) / 25 / 25 | |
| Flag capture / return | 200 / 75 | |
| Bomb plant / detonate / defuse | 50 / 200 / 75 | |
| Node capture | 150 | |
| Zone hold (at zone exit/deactivate, by points/10: 0–9, 10–19 … ≥50) | 5 / 10 / 15 / 20 / 25 / 30 | |
| Heal grenade on teammates / repair-ray low-health heal | 50 / 15 | |
| Game win / lose (versus only, see the quirk above) | 300 / 150 | |
| Challenge tier | per challenge (§6) | Prime challenges give that XP to **all four** specialties |

**Configured but never awarded (no callers in script or data):** FlagDefend (100; `PRI.AddFlagDefend` has no caller), KillGuidedMissile (100). Everything else in the table is reachable.

**Where and when XP is committed:**
1. On the server, `PC.NotifyXpEvent` → `Game.NotifyXpGained` (stats table) → reliable client RPC `ClientNotifyXpEvent`.
2. On the client, the event is added to the XP transaction (popup group; one transaction per kill).
3. If `CanGainXp`: `XpManager.NotifyXpEvent(currentSpecialty)` → `AddXpForSpecialty`, capped at 355000, **written immediately** to the profile stats key archive (`SetKeyArchiveValue`, property = specialty XpPropertyId 0x50 Scout, 0x51 Soldier, 0x52 Scientist, 0x53 Leader).
4. Then `CheckForLevelUp`.
5. At match end: `ClientWriteLeaderboardStats` → `SaveProfileSettings`, refresh character slots, add newly unlocked skills, write the customization file, then the TnStatsWrite classes.
6. XP earned this match per specialty (`CurrentGameXpEntries`) feeds the results screen.

**Only the currently played specialty earns XP** (except Prime challenges).

---

## 3. Public / private / offline XP (C for ORIGINAL)

- **ORIGINAL:**
  - `TnGameReplicationInfoMultiplayer.CanGainXp() = !IsPrivateGame()`.
  - **Public online matches earn XP, challenges and stats.**
  - **Private matches: no XP, no challenge progress** (stat ids 0x1500–0x1FFF are dropped by `PRI.ShouldUpdateState`), and private settings `bUsesStats=false`. XP popups still show (`ShowXpEvents=true`) but award 0.
  - Base `TnGameReplicationInfo.CanGainXp() = false`, so campaign, co-op, lobbies and anything not multiplayer earn **no MP XP**.
  - No offline/local versus mode exists (versus requires an online session; `NumRequiredPlayers` 4).
  - The leave-match prompt warns about losing XP only when CanGainXp.
- **Suggested PC ADAPTATION** (not original): treat local/LAN or bot matches as "public" (CanGainXp true) if offline progression is wanted; or keep the original rule (private = no XP) and add an explicit option.

---

## 4. Levels ("rank") (C)

- **There is no single rank ladder.** Each of the four specialties has its own XP and level 0–25 (`TnXpManager.LevelTable`, 25 thresholds; level = number of thresholds ≤ XP).
- The **displayed player level** (`PRI.PlayerLevel`) = **sum of the four specialty levels (0–100)**. The four values are packed into one int (Scout<<24 | Scientist<<16 | Soldier<<8 | Leader) and sent to the server, which replicates them.
- Level-up is broadcast as `TnPlayerLevelUpMessage` "`p is now a level `l `s" (specialty level), plus the HUD `NotifyLevelUp`.

Level thresholds (XP to reach level n):

| Level | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| XP | 500 | 1500 | 3000 | 5000 | 7500 | 11000 | 15500 | 21000 | 27500 | 35000 | 44000 | 54500 | 66500 |

| Level | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| XP | 80000 | 95000 | 112000 | 131000 | 152000 | 175000 | 200000 | 227000 | 256000 | 287000 | 320000 | 355000 (cap) |

- **No rank names** exist in config or loc.
- **No rank-icon textures** were found: levels are numbers. U: GFx may draw level badges internally (not traced).
- Achievements:
  - 38: any specialty level ≥ 5;
  - 39: any specialty level 25;
  - 40 / 41 / 42: level sum ≥ 50 / 75 / 100.
- Character slots per specialty: 1 + (level ≥ 5) + (level ≥ 10), i.e. up to 3 (`UnlockCharacterSlotLevels` 5, 10). There are 5 colour palettes.

**Prime mode (the one-time prestige):**
- Offered when **all four specialties are at the XP cap** (`IsLevelMaxed`) and Prime is not yet unlocked (`IsPrimeModeAvailable`).
- `UnlockPrimeMode` (achievement 43):
  - clears the listed challenge stats (`PrimeModeStatsToClear`, + 4096 variants);
  - **resets XP of all specialties to 0**;
  - resets newly-unlocked skills and characters;
  - sets profile property 84 = 1;
  - replicates `PRI.PrimeModeActive`.
- Prime enables the **25 Prime challenges**.
- It is a boolean, so there is no second prestige.
- `FX_Multiplayer_p.FX.Prime_Target_FX` exists. U: its use was not traced.

---

## 5. Class progression (C)

- **Per-specialty XP and levels are the only progression state.** There is no separate global rank.
- **Unlocks:** `TnCustomCharacterOptions.GetSkillsForLevel(specialty, L)` = every `TnDataProvider_Ability` and `TnDataProvider_Skill` whose `SpecialtyRestriction` contains the specialty **and `LevelRestriction == L` exactly**.
  - Unlocks on level-up are collected into `SkillsUnlockedThisGame` and committed at match end.
  - Table: `mp_class_unlocks.json` (56 skills, 18 abilities, with FriendlyName/Description, level and specialty).
- **Kill-streak rewards are not level-gated:** `FindKillstreakProvider(specialty, KillsRequired)` picks the provider matching the specialty and the exact streak count (3 / 5 / 7). There are 12 providers (e.g. Scout 3 OrbitalRecon, 5 HealthRegen, 7 ImprovedOrbitalRecon; Leader 3 FastAbilityCooldown, 7 MinePooper; Soldier 5 TeamAbilityJammer; Scientist 7 SpawnRocketTurret …).
- Default secondary weapons: Scout EMPShotgun, Scientist RepairRay, Soldier HomingRocket, Leader HeavyPistol.
- **Weapon unlocks:** none in these providers. U: weapon availability is per-chassis data, not level.
- Challenges do not gate unlocks (no dependency fields).

---

## 6. Challenges (C)

**Definition:** 121 `TnDataProvider_Challenge` entries (TransChallenges.ini), each with:
- `ChallengeId` (0x27xx; the profile property holding the completed tier);
- `StatPropertyId` (0x15xx–0x17xx; the counter);
- `CategoryId`: Basic 11, Scout 22, Scientist 21, Soldier 21, Leader 21, **Prime 25**;
- **three tiers** `GoalValues[3]` / `XpRewardValues[3]`;
- `PrimeChallenge`.
- The name and description come from the INT section (`Description` uses `g for the goal). All 121 have text.

**Counters:**
- `PRI.ReportGameStat(amount, statId, when, UpdateType)`, where UpdateType 0 = add, lifetime (progress = saved archive value + this match); 1 = max within the match (single-match bests, e.g. kill streak); 2 = add within the match, compared without the saved value (single-match counters).
- The owning client's `ChallengeManager.SetValue` → `CheckChallenges`:
  - for each challenge on that stat (skipping Prime ones unless Prime is active), from the stored tier upward, **every tier whose goal ≤ value unlocks**;
  - `UnlockChallenge` writes tier+1 to `ChallengeId`, plays `UI_GFxChallengeNotifies_p.ChallengeNotify_GFX` `_global.ChallengeUnlocked(name, desc, tier, goal, xp)` and calls `PC.OnChallengeUnlocked` → XP.
- **Counters only update when CanGainXp** (public matches).
- Stat sources: the kill-award rules (headshots, backstab, buff kills, per-class weapon kills via `TnKillAwardRuleSpecialtySpecific`), PRI objective functions, ability use, etc. Rule data with stat ids: `mp_kill_awards.json`.
- Do not infer requirements from names: use `Description` + the `StatPropertyId` producer.

---

## 7. Medals / awards (C)

- **WFC has no separate medal system.** The "medals" are the **XP events**: a named popup `Announcement` (e.g. Domed, First Blood, Linebacker, Funkiller, Beat Down) + `Description` + XP amount.
- They are shown by `TnHudDataObserverXpTransactions` → GFx callback args `(transactionId, xp, announcement, description, extraData)`. Events of one kill are grouped in one transaction.
- Kill-streak events add extraData `"Killstreak,<providerId>"` and a description with the reward name (`k).
- Triggers, windows and thresholds: §2 table, `mp_kill_awards.json`, `mp_xp_events.json`.
- **No icons** are referenced by XP events (text only).
- **No per-medal sound.**
- **Repeats:** every qualifying kill, except first kill/death (once per match). Multikill and streak tiers trigger at exact counts.
- Streak text: `TnKillStreakMessage` at streaks 3/5/7/10 (text only, see pass 5 §12 add. 11).

---

## 8. Scoreboard

Already recovered in `MILESTONE05_FRONTEND_GAMEPLAY_BLOCKERS.md` F5 and `MILESTONE05_FRONTEND_MATCH_BOOTSTRAP.md` (C):
- columns Level · Name · Score · Kills · Deaths;
- teams sorted Score↓ then TeamIndex;
- players sorted Score↓, Kills↓, Deaths↑, Name;
- `InGameStats_GFX` scoreboard movie and the results screen with XP earnings per specialty;
- assists not shown.
- **Level** column = `PRI.PlayerLevel` (sum of the four specialty levels).
- **Bots:** `TnGameReplicationInfo.UsesPlayerDataProvider(PRI) = !PRI.bBot`, i.e. **bBot PRIs are excluded from the player data provider (player lists/scoreboard)** in the original (C). See §13.

---

## 9. Bot / AI architecture (C unless marked)

- **No multiplayer bots in shipped WFC.** The multiplayer automated-testing policies do not drive AI:
  - `TnMultiplayerGameTestingPolicy`: random character + `ClientStartRandomInput`;
  - `TnKillBasedMultiplayerTestingPolicy`: kills random players with random damage types on a timer;
  - `TnObjectiveBasedMultiplayerTestingPolicy`: `ScoreObjective(random, 1)` on a timer.
  - No AddBot path and no bot spawner in TnMultiplayerGame/TnVersusGame.
- **Reusable original AI = the campaign/Escalation GOAP AI:**
  - `TnAiController` / `TnAiPawn`, the HmGoap planner (`HmGoapPlanner`, `HmGoapPlanRunner`, `HmGoapSearchSpace`);
  - data-driven per character by **`TnAiCharacterDefinition`** (94 in TR_AiCharacterDefinition_p / TR_AiEscalation_p):
    - `ActionSet` (HmGoapActionSet of TnAiAction*Blueprints), `GoalSet` (TnGoapGoal*Blueprints), `SensorSet`;
    - `Buffs`, `ActionOverrides` (weapon class per form), `AiCharacterDataResolved` (chassis, CharacterType Buddy/Enemy/Boss).
  - Every versus game class still instantiates `_AiPlanningScheduler`, `_AiTacticalEvaluationScheduler` and `_TacticalOctree` (inherited from TnGame).
- **Best template for MP bots:** the **Buddy** definitions (`<Iconic>_Buddy_AICD` for Optimus, Bumblebee, Ironhide, Megatron, Starscream …). They are iconic MP chassis with player-like loadouts.
  - Example `Optimus_Buddy_AICD`: actions = shoot from tactical / at target (×2), stop-and-cooldown weapon, scanning idle, transform to robo/vehicle, navigate, step away, jump, enter/leave/shoot turret, use interact, stimulus reaction, turn to face focus;
  - goals = UseInteract ×2, React, ReactToStimulus ×2, ScriptedMoveTo, DefendSelf, **Kill**, **BuddyLead**, MoveTo ×2, Idle;
  - sensors = LineOfSight, Range, Threat, PreferredWeaponPicker (+ dynamic set);
  - buff TnBuffHealthOnBlock.
- Goal classes available (complete): BuddyLead, Cloak, DefendSelf, Heal, HunkerDown, Kill, MoveTo(+Blueprint), NavigatePath, React, ReactToDeathImminent, ReactToStimulus, Revive, ScriptedMoveTo, StayInTacticalVolume, Transform, TurretKill, UseInteract, Idle.
- Action blueprints include: dodge, barrel roll, melee/navigating melee, smash attack, shoot-from-air-tactical, transform-to-vehicle-from-jump, vehicle navigation, revive, EMP reaction.

**Difficulty:**
- `TnGame.MaxDifficultyLevel` 2.
- Projectile/weapon data has SP/MP/**AI** variants (`AiData`); AI weapon data adds `BurstRanges` (short/medium range bursts and pause durations) and `FireIntervalModifier`.
- `GetCurrentSkillDataIndex` selects the difficulty index (MP returns 0).
- ini `TnAiPawn`: AiVersusAiDamageScale 0.6, head ×3, DownedEnemySpreadModifier 2.5, DownedEnemyFireIntervalModifier 2, CloakedEnemySpreadModifier 5.
- Sensors: LineOfFire 2–4 s before registering, GrenadeDistance 400; confidence: 1.5 s unsafe → low, 1.5 s safe → medium; aggressive attack after 4 s.

---

## 10. Navigation (C)

Census in `mp_navigation_audit.json`.

**Versus maps** (Berth, Rust, Seed, Streets, Molten, Debris, Complex, Gorge):
- **No PathNodes, no NavigationCells, no tactical/cover nodes.**
- Only NavigationPoints: TnTeamPlayerStart (41–98), TnFreeForAllPlayerStart (11–28), pickup factories, flag/bomb objective factories, plus **TnReachSpec 175–865** built only between those points (radius 440, height 400, reachFlags 1).
- That sparse spawn/pickup graph is **not sufficient for bot navigation**: it is direct-reachability edges between spawns, pickups and objectives.
- **The original MP-capable navigation was never authored for versus maps (not stripped):** there were no MP bots.

**Escalation maps** (MP_ESC_BrokenHope, MP_ESC_Remnant):
- **full AI navigation**: PathNode 44/104, AirPathNode 40, MoverPathNode 26, **NavigationCell 469/625**, TnTacticalPathNode 540/514 with tactical evaluators/pickers, TnSurvivalSpawnPoint 58/62, ~3000 reach specs.
- These are the original reference for how WFC AI navigates (cells + tactical nodes + air nodes).

**To reconstruct (Gameplay/AssetTools):**
- a walk graph or navmesh per versus map from collision geometry;
- jump/fall links;
- vehicle-drivable areas;
- air volumes for jets;
- tactical/cover points;
- objective approach points.
- Spawn sets, pickup locations and objective locations already exist and can seed it.

---

## 11. Bot combat behaviour (P)

Reusable original pieces:
- action blueprints (above);
- sensors (`TnAiLineOfSightSensor`, `TnAiRangeSensor`, `TnAiThreatSensor`, `TnAiLineOfFireSensor`, confidence sensors);
- `TnPreferredWeaponPickerSensor` (weapon selection);
- AI weapon burst/pause data;
- `TnAiActionShootAtTarget` / `ShootFromTactical`;
- transform actions;
- cloak/heal/hunker goals;
- vehicle navigation.

Grenade use: `TnAiActionThrowGrenade` + LineOfFire GrenadeDistance 400.

Not traced in this pass (U): the per-blueprint numeric parameters (ranges, costs, preconditions).

---

## 12. Bot objective behaviour

- **No original AI for capture / hold / carry / escort / retrieve / return / contest of versus objectives (U, none found).**
- The goal list has no flag, bomb, node or zone goals.
- The closest reusable pieces: `TnGoapGoalStayInTacticalVolume` + `TnTacticalEvaluatorDefendActor` / `BattleLine` (defend an area/actor; used in Escalation), `MoveTo`, `UseInteract`, `BuddyLead`.

---

## 13. Participant state for non-local players (C)

`TnPlayerReplicationInfo` replicates:
- PlayerName, Team, Score, Deaths;
- `PlayerLevel` + four specialty levels;
- `PrimeModeActive`;
- ReplicatedCharacterData;
- TimeToRespawn, IsConnecting;
- **`bBot`**.

GameStats replicate to the owner only (`ClientUpdateGameStat`).

**bBot handling already in the original:**
- the kill feed localizes bot names through `[AICharacterNames]` (TnDeathMessage);
- no join sound and no claimed-character refresh (GRI.AddPRI);
- lobby "all players have a character" skips bots;
- players-met skips bots;
- toggling bBot re-adds the PRI;
- **the player data provider skips bots, so the original scoreboard/player list would not show them.**

A rebuild that wants bots on the scoreboard must deliberately diverge (**PC ADAPTATION**).

---

## Open (U)

- GFx-side presentation of level badges and medal popups (the ActionScript was not traced).
- Prime_Target_FX usage.
- Weapon unlock gating (none found).
- Per-action AI tuning numbers.
- `TnStatsWrite*` leaderboard columns.

---

## Addendum 1 (milestone 09 requests): AI internals, difficulty, nav formats, the XP switch, frame timing

### AI perception and decisions (C from script + Buddy data)

**Controller** (`TnAiController` CDO) subobjects:
- TacticalAnalyzer (`TnTacticalAnalyzer`);
- WeaponShooter (`TnAiWeaponShooter`);
- WeaponAimer (`TnAiWeaponAimer`);
- `AiWorldState` (GOAP facts: AtActor, LOSToEnemy, HealthStatus, TransformerForm, VehicleMode, WeaponOverheated, HasAmmo, InLineOfFire, LockedOnTarget, Cloak, Defending, MoveToObjective, MoveToTacticalVolume, Shield, HealTarget, Turret …);
- the PlanRunner.

**Target selection** (`TnAiThreatSensor.OnUpdate`):
- Skipped while `_ShootAtActor` is forced.
- For each enemy in the TacticalDatabase (excluding dormant/untargetable sentries and non-targetable pawns), threat = Σ evaluator scores. An evaluator can discard the target.
- The highest threat becomes `DesiredEnemy`.
- Buddy evaluators: DamageBased, DistanceBased (`_MaxThreatRange` **7000**), TurretTarget, CloakedTarget.

**LOS:** `TnAiLineOfSightSensor` sets the LOSToEnemy / AtActorLOS facts every update.

**Range:** `TnAiRangeSensor` puts the range bucket (RangeSet) for the AtActor and enemy into the world state.

**Weapon choice** (`TnPreferredWeaponPickerSensor`):
- Close weapon = the lowest `GetDesiredFiringRange`; far weapon = the highest.
- Switch to the far weapon after **5 s** at range ≥ OutOfRange; to the close weapon after **0.5 s** at range ≤ Medium.

**Aim model** (`TnAiWeaponAimer`):
- **No aim error.** It aims exactly at the target's TargetableLocation: the form-specific service (robot/vehicle) when the target is "dangerous", else its focal point.
- "Aiming" = muzzle dot target > 0.866 (30°).
- **Inaccuracy comes from weapon spread and burst pacing:**
  - AI weapon data (`*_AI_WEPDATA`): `BurstRanges` short/medium/long with burst counts and pause durations, `FireIntervalModifier`;
  - `TnAiPawn` ini: CloakedEnemySpreadModifier ×5, DownedEnemySpreadModifier ×2.5, DownedEnemyFireIntervalModifier ×2;
  - AiVersusAiDamageScale 0.6.

**Cover / movement:**
- Dynamic sensors `TnTacticalPathNodePickerSensor` per weapon class group (infantry weapons vs vehicle weapons) pick TnTacticalPathNodes via evaluators (LOS, LOSToTeam, DistanceFromRange, KeepInRange, AwayFromTarget, HotSpot, OutsideAim, DistanceFromDowned, MoveForward) for the `ShootFromTactical` action.
- **They need tactical nodes, which versus maps lack.**

**Abilities / transform:** GOAP goals Cloak, Heal, HunkerDown, Transform, Revive and action blueprints (TransformToRobo/Vehicle, TransformToVehicleFromJump, Dodge, BarrelRoll, Melee, SmashAttack …). Per-blueprint numeric preconditions and costs were not extracted (U).

### Difficulty (C)

- **Player-facing names** (UIText.int `[Difficulty]`):
  - **EASY** "For the new recruit…";
  - **MEDIUM** "For the experienced soldier…";
  - **HARD** "For the hardened veteran…".
- These are campaign only; multiplayer has no difficulty.
- **Mechanism:** not AI skill. `TnCampaignGame.GetDifficultyBuffLevel = difficulty × 3 + (numPlayers − 1)`, i.e. levels 0–8. These index buff values applied to pawns:

| Buff | Easy (+0/+1/+2 players) | Normal | Hard |
|---|---|---|---|
| PlayerDamageCaused | 1.5 / 1.25 / 1.0 | 1.0 / 0.9 / 0.8 | 0.7 / 0.6 / 0.5 |
| PlayerDamageTaken | 0.5 / 0.75 / 1.0 | 1.0 / 1.25 / 1.5 | 1.75 / 2.0 / 2.25 |
| PlayerDamageTakenDowned | 0.5 / 0.4 / 0.3 | 0.5 / 0.4 / 0.3 | 0.25 / 0.2 / 0.15 |
| DamageCausedAiVsAi | 0.45 / 0.35 / 0.25 | 0.3 / 0.2 / 0.1 | 0.25 / 0.15 / 0.05 |
| Revive: damage-taken buff / jam abilities | 0.15 · 5 s | 0.25 · 7 s | 0.35 · 10 s |

- Also AbilityResourceModifier (TransCustomization.ini).
- `GetSkillDataIndex` is **not difficulty**: it selects the data variant (MP 0, campaign 1; Survival has its own SV data).
- **For MP bots, any difficulty scale is a PC ADAPTATION.** The closest original knobs are the AI weapon data (burst/pause/spread) and these damage multipliers.

### MP AI remnants (C)

- The only AI in versus matches is `TnAiSentryController` (sentries, `_KillOwner`).
- `bBot` handling: §13.
- `TnGameReplicationInfo.UsesPlayerDataProvider = !bBot`.

### Navigation formats (C)

**Versus reach graph:** `TnReachSpec` (Engine ReachSpec subclass):
- `Start` = NavigationPoint;
- `End.Nav` = NavigationPoint;
- `Distance`;
- `CollisionRadius` 440 / `CollisionHeight` 400 / `MaxCollisionRadius`;
- `reachFlags` 1 (walk).
- Owned by the start point's `PathList`.
- Points = team/FFA player starts, pickup factories, flag/bomb factories only.

**Escalation reference format:**
- **`NavigationCell`**: a convex polygon cell with `_Edges[]` {Start, End, Normal, `Neighbor` (cell + Guid), Border, StartIsInner, EndIsInner}, `_Normal`, `_IsTacticalCell`, `PathList` (TnReachSpecs), `MaxPathSize`. A portal-linked cell mesh (navmesh-like).
- `PathNode` / `AirPathNode` / `MoverPathNode` with `StaticAnchor` → owning cell.
- `TnTacticalPathNode` (`Tactical` subobject, `_AutoGenerated`, anchored to a cell).
- Reconstruction can target this same schema (cells + portals + tactical nodes) from versus-map collision.

### Private-match XP switch (C): the code path to wrap

1. **`TnGameReplicationInfoMultiplayer.CanGainXp() = !get_IsPrivateGame()`** (`get_IsPrivateGame` → `GameSettings.IsPrivateGame()`). This is the single gate used by:
   - `TnXpEventType.GetAwardAmount` (amount 0);
   - `PC.ClientNotifyXpEvent` (no profile write);
   - `PC.ToggleXpTransaction`;
   - `PRI.ShouldUpdateState` (stats 0x1500–0x1FFF, i.e. challenge counters);
   - `MatchOver.CanAwardMVP`;
   - `GetQuitGameMessage`.
2. `ShowXpEvents()` (true in MP) is separate: popups still show, with 0 XP.
3. Private settings classes set `bUsesStats=false` (leaderboard writes).

**PC-OFFLINE ADAPTATION:** override `CanGainXp` (and, if wanted, the stats flag) in one place.

### Frame timing (C for Xenon config; H for engine behaviour)

- Xenon `[Engine.GameEngine]` bSmoothFrameRate=TRUE, MinSmoothedFrameRate 15, **MaxSmoothedFrameRate 30**.
- PhysX fixed 1/60 substeps (≤ 5), with the script dt = n/60 (pass 4 A4 addenda).
- **UE3 runs one game tick per rendered frame.** There is no fixed-tick/variable-render split and **no interpolation of camera or animation between ticks** (H, stock UE3: the render thread draws the state from the latest game tick). Camera and animation advance by DeltaTime each tick.
- PC original cap: UNKNOWN (no PC build in the dump; pass 4 A4 addendum 2).

## Addendum 2: AI tuning data dump and goal priority (C)

**Data** (regenerate with `tools/ai_definitions_extract.py`):
- `notes/data/ai_definitions.json`: all 94 `TnAiCharacterDefinition`s, each with its fully resolved ActionSet blueprints (WeaponClass, RequiredForm, ActionOverrideClass, CostModulators, DynamicPreconditions, nested navigation ActionSets), GoalSet blueprints (Description, WorldStateClass, RangeSensorClass, StimulusConditionSet …), sensors (threat evaluators, tactical node pickers + evaluators) and ActionOverrides (weapon class per form).
- `notes/data/ai_weapon_data.json`: the 38 `*_AI_WEPDATA` (FireIntervalModifier, PerShotSpreadModifier {Start, Min/Max, ChangePerShot, Cooldown}, BurstRanges, RangeDamageModifiers, TargetSnapRange, heat …).

**GOAP goal priority = position in the GoalSet** (`HmGoapPlanRunner.TryBetterPlan` → `FindPlanInRange(0 … current[-1])`):
- Goals are planned in index order. The first goal that yields a plan wins.
- A replan only looks at higher-priority goals (index < current), or the current goal too when `EvaluateCurrentGoalOnReplan`. For the current goal it compares against the running plan's cost.
- A plan whose action disallows interruption blocks replans.
- Buddy order: UseInteract(high) > React > ReactToStimulus(high) > ScriptedMoveTo > DefendSelf > **Kill** > UseInteract(low) > BuddyLead > MoveTo Objective > MoveTo Buddy > ReactToStimulus(low) > Idle.

## Addendum 3: original AI behaviour coverage vs MP needs, and team/slot rules (C from data/script)

Table: `notes/data/ai_behavior_summary.json` (90 action-blueprint classes → definitions + parameter sets).

| MP need | ORIGINAL reusable behaviour (definitions) | Gap → PC ADAPTATION |
|---|---|---|
| Shoot (robot) | `ShootAtTarget` / `ShootFromTactical` per weapon class (all soldiers + buddies) | needs tactical nodes on versus maps |
| Shoot (vehicle/jet) | `ShootAtTarget` RequiredForm TF_Vehicle (RocketVehicle …); jets `ShootFromAirTactical` (RocketVehicle / PlaneMachineGun), `ShootingStrafeFromHover` (Duration 4, every 2–3 s), `BombingRun` (every 7–10 s) | |
| Melee | `NavigatingMelee` (33 defs, UsageInterval 1 s); `Melee` (Brutes / CQC; cloak preconditions); Brute `SmashAttack` (2000–5000 UU, every 15–20 s) | |
| Grenades | `ThrowGrenade` only on Shotgun soldiers (FlakGrenades, AttackRange RANGE_Far) and the Starscream boss | other classes: none |
| Dodge / evasive | `BarrelRoll` (jets, MinDamageThreat Low, every 3–5 / 4.5–6.5 s); `DodgeNavigate` (CQC, DodgeTraceMinimumThreshold 0.7); `Dodge` (Laserbeak, drones, boss) | robot dodge for buddies: none |
| Transform | `TransformToRobo` (67 defs) / `TransformToVehicle` (53) / `TransformToVehicleFromJump` (jets) / `TransformToRoboWoundedReaction` (tanks); vehicle navigation (60 defs) | |
| Abilities | Cloak (CQC), AbilityJammer (Frenzy, every 5–7 s), Hover (Frenzy), Heal / repair ray (Ratchet, Jetfire, Soundwave buddies), Revive (9) | **Warcry, Shield, Decoy, Sentry, Mines, Hover (MP Scout/Leader/Scientist/Soldier abilities), Hard Lock, Barrier: no AI actions** |
| Turrets | Enter / Leave / ShootFromTurret / ScanForEnemies (41 defs) | |
| Team | `BuddyLead`, `MoveTo Buddy` (CloseToFriend), `LOSToTeam` tactical evaluator, Revive/Heal | |
| Objectives | `MoveTo Objective` (WorldState MoveToObjective), `StayInTacticalVolume` + DefendActor / BattleLine evaluators (Escalation) | **no capture / carry / plant / defuse / zone-hold behaviour** |
| Navigation | NavigationCell + PathNode / AirPathNode / MoverPathNode + TnTacticalPathNode (campaign / Escalation maps only) | **versus maps need reconstructed nav + tactical nodes** |
| Difficulty | campaign EASY/MEDIUM/HARD player-damage buffs (addendum 1); AI weapon spread / burst data | bot difficulty presets |

**Slots / teams:**
- MaxPlayersAllowed **10**; NumPublicConnections / NumPrivateConnections 10; NumRequiredPlayers 4.
- `TnTeamHandlerTwoTeams.PickTeam`: the smaller team, random on a tie (Autobots index 0, Decepticons 1); party reservations keep parties together.
- **No explicit per-team cap** (balance only), i.e. ≤ 5v5 at 10 players (H: the lobby enforces this).
- **AssignTeams / ForceToTeam / DisbandTeams skip `bBot` PRIs**, so bots need explicit team assignment (PC ADAPTATION).
- FFA: `TnFreeForAllGame.GetResolvedCharacterFaction = 1`, i.e. every DM player resolves to the Decepticon faction character set (C).

**Original bot UI:** none. There is no bot menu or option in the original; a Private Match Bot Settings screen is a PC ADAPTATION.

## Addendum 4: challenge counter producers; Prime presentation (C)

**`notes/data/mp_challenge_stat_producers.json`:** every one of the 121 challenge `StatPropertyId`s mapped to what increments it:
- script `IncrementGameStat` / `ReportGameStat` sites (incl. `IncrementKillstreakStats` for the Prime kill-streak counters);
- kill-award rule data (StatId fields);
- damage-type `KillStatId` (weapon kills);
- heal-type `HealStatId`;
- **`PRI.ChallengeStatReplacementMap`**, which mirrors general stats into challenge stats: 289→5388, 292→5389, 260→5391 (Scout dash), 321→5468, 273→5644, 308→5724, 268435459 (assists)→5893, 336 (vehicle time)→5896, 268435457 (kills)→5897, 337 (vehicle kills)→5898.

**Rank / Prime text:**
- UIText has **no rank names**. "Rank" appears only as the leaderboard column header.
- Prime strings: `PrimeMode` "Prime Mode"; `PrimeModeDesc` "Achieve max level in all classes to access Prime Mode."; `PrimeModeUnlockedDesc`; `PrimeModeMessage` "Activating Prime Mode will unlock new Prime Mode only challenges and will reset all of your current XP and challenge completions. **A medal will also appear next to your name** so that all can see your new status as a Prime."
- So Prime players show a **Prime medal next to their name** (presentation in GFx; the icon is U, inside the player-list/HUD SWF).
- Teletraan1 menu: "View game Challenges, Leaderboards, and Prime Mode options."

## Addendum 5: HUD progression sounds, AI-kill exclusion, movement constants for nav (C)

**Hud_GFX ActionScript** (`tools/as2dis.py ExtractedAssets/content/UI_GFxHud_p/Hud_GFX.gfx`). Sounds go through `HmExternalInterface.Sound.PlaySound(name)` → `BL_HUD_INTERFACE.<name>`:
- **`MP_LEVEL_UP_MX_STNG`**: in `_global.NotifyLevelUp(NewLevel, Specialty)` (sprite 643, attaches `mc_levelUpNotify`). Called from `TnHUD.NotifyLevelUp` ← `PC.CheckForLevelUp`, local player only, current specialty only.
- **`MP_REWARD_DIALOG_BOX`**: in the XP transaction label (under `_global.PointEvent`).
  - It plays once per XP-event line shown. Lines are queued; kill-streak events are put at the queue front and use `mc_pointTransactionKillstreakLabel`.
  - The running "+N" total scales up by 150 + amount, capped at 400 %, and eases back over 0.5 s.
  - H: empty-string descriptions also pass the `undefined` check.
- **`BL_HUD_INTERFACE.EXP_LEVEL_UP`** is unused (only preloaded by BaseMapReferencers).

**AI-controlled participants (C):** `TnGameRules_TrackKills.CheckKills` (kill awards / XP / medals + kill-streak announcer) runs only when killer **and** victim are `TnPlayerController`, and `ScoreKillsMP.ShouldScoreKill` needs a `TnPlayerController` victim.
- So original AI killers/victims produce no score, XP, medals or streak/progress announcements.
- Bots that count as players are a **PC ADAPTATION**.
- AI barks: `TnAiController._DialogManager` plays spawned, enemy-encountered, health, downed and revived dialog.

**Movement constants for nav generation** (from `STEPUP_LEDGE_2026-10-01.md`):
- The struct `Pawn._WorkingMovementCapabilities` is swapped per form.
- Robot: MaxStepHeight 35 (+2 fudge → **37 UU** step-up and snap-down), WalkableFloorZ **0.7**, MaxFallHeight 3400, MaxJumpHeight = acrobatics JumpHeight (**500 UU** apex; JumpZ 1714.6), TerminalVelocity 6000.
- Vehicles: RB/hover physics (the walker rules do not apply).

## Addendum 6: player-list level and award badges (PlayerList_GFX ActionScript) — corrects §4/§8 (C from AS; H noted)

- **Level shown per player:** the player-list entry for a non-iconic MP game has columns `PlayerLevel` (width 100) + `PlayerName` + `Score` (+ `Kills`, `Deaths` in game).
  - The level cell (sprites 82/88) attaches the **specialty icon** of the player's current character (`mc_specialtyIconScout / Leader / Scientist / Soldier`) and the text **`PlayerLevel<Specialty>`**, i.e. the level of the specialty being played (0–25), watched for changes.
  - So players see **specialty icon + that class's level**, not the 0–100 sum. H: the summed `PRI.PlayerLevel` still feeds the data-store column; the visible number is the specialty level.
  - Iconic mode (campaign/co-op) shows the character name instead.
- **Award badges next to the name** (sprite 85): `addAward(name, priority)` with clips `mc_awardPlace1st`, `mc_awardPlace2nd`, `mc_awardPlace3rd`, **`mc_awardPrimeMode`**; spacing −25 px from x −20, scale 80 %.
  - Only `PrimeMode` is added in this movie, from `PrimeModeActive`, so it is **the Prime medal**.
  - Place1st/2nd/3rd clips exist but nothing in PlayerList adds them (U: possibly unused).
- Prime unlock UI: `Customize.IsPrimeModeAvailable` / `Customize.UnlockPrimeMode` from GameLobby / PartyLobby (`primeMode_mc`, locked unless available), and also CharacterSelect / CustomTransformers / EndGameStats / Hud / InGameStats.
- Assets: badge and specialty-icon art is inside `PlayerList_GFX.gfx` (extracted images `PlayerList_GFX_I*.png`).

## Addendum 7: AI range bands, burst selection, DesiredFiringRange (C)

**`TnAiRangeDetector.ETnRange`** with `TnAiController.RangeSet` (CDO; must have exactly 8 entries; values in UU = cm):

| idx | name | Min–Max |
|---|---|---|
| 0 | RANGE_Invalid | −1 |
| 1 | RANGE_Touch | 0–175 |
| 2 | RANGE_Striking | 176–600 |
| 3 | RANGE_Close | 601–1500 |
| 4 | RANGE_Medium | 1501–3000 |
| 5 | RANGE_Far | 3001–5000 |
| 6 | RANGE_Retreated | 5001–7000 |
| 7 | RANGE_OutOfRange | 7001+ (also returned when nothing matches) |

**Range computation:**
- `GetRange`: CenterPointRange = band(|Δloc|). NearestRange = band(|Δloc| − (radius_src + radius_target)), clamped ≥ 0.
- A reached NavigationPoint returns Touch for both.
- `TnAiRangeSensor` stores both in the TacticalDatabase per enemy.

**Burst band** (`TnWeapon.GetBurstDataForRangeInternal`, using the enemy **CenterPointRange** from `TnAiWeaponShooter.GetCurrentRange`):
- Striking, Close → `BurstRanges.ShortRange`;
- Medium → `MediumRange`;
- Far and everything else (Touch, Retreated, OutOfRange, Invalid) → `LongRange`.
- So Short ≈ 1.76–15 m, Medium 15–30 m, Long > 30 m. Touch (< 1.75 m) uses Long, as written.

**DesiredFiringRange** (`TnWeaponData`, an ETnRange):
- "At desired range" ⇔ enemy CenterPointRange **==** the weapon's DesiredFiringRange (exact band, `TnAiController` ~line 1754).
- The weapon picker takes the lowest band as the close weapon and the highest as the far weapon.

**TargetSnapRange** (Min/Max UU): player-only aim-snap distance window (`TnPlayerTargeting` → `TnWeapon.IsWithinTargetSnapRangeSq`: Min² < d² < Max²). Not used by AI.

**Reaction / acquisition delay:** no data-driven reaction, notice or acquisition delay was found in the AI script. Enemies register through sight/noise, and the sensors update the facts every AI update. A bot reaction delay is therefore a **PC ADAPTATION**; inaccuracy remains weapon spread + burst data (addendum 1).

## Addendum 8 (Milestone E): respawn timing, chassis unlocks, capacity limits, bot-event rules (C unless marked)

**Respawn** (all versus/FFA/team games: `RespawnHelper0` = **`TnRespawnHelperWave`**, `WaveRespawnTime` **5 s**; Escalation: `TnRespawnHelperRoundEnd`):
- **On death:** the player is queued with a 5 s timer (`PRI.SetTimeToRespawn` drives the HUD countdown). Not queued if `TnTeamInfo._AllowRespawn` is false.
- **Each tick:** the timer counts down; at ≤ 0, `Respawn`. Per-player timers despite the class name; there is no shared wave clock.
- **Instant respawn:** `PC.ShouldInstantRespawn()` (`TnKillStreakInstantRespawn` reward; cleared on use) → 0 s.
- **Initial spawn:** `TimeToAllowInstantInitialSpawns` −1, so the initial spawn is always immediate.
  - Spawn-point manager: InitialSpawnTime 15, ActiveClusterTime 10, MaxSpawnPointsToConsider 4, UpdateInterval 0.1 (ini).
- **Rounds** (CTF): `OnRoundEnded` re-enables respawn for all teams and resets the initial window. `TnGame.DisallowRespawnForTeam` has no script caller (U: Kismet only).
- **Pre-match / results:** MatchAutoStartCountdown 10 s (Escalation 15), MatchOverCountdown 15 s; CTF between-round 5 s; no overtime (§1). Coop MissionCompleteCountdown 10; campaign game-over screen delay 1 s.

**Unlocks:**
- Skills/abilities by exact specialty level (§5; `mp_class_unlocks.json` has `LevelRestriction` / `SpecialtyRestriction` per entry). Kill streaks by specialty + count, not level.
- **Chassis:** 18 providers are `LockedChassis` (some also `LockedCharacter`). `IsChassisUnlocked` = not locked, or present in the profile's unlocked list. Script unlock sources:
  - **Car5** on completing the Autobot campaign (any difficulty, `TnProfileSettings.CheckForLevelCompletionAchievements`);
  - **Jet8** on completing the Decepticon campaign;
  - a developer-only cheat in `TnPlayerReliableReplicationInfoSurvival` (name whitelist + specific generator; unlocks Car5–7, Jet7–8, Tank4–5, Truck5 and 10000 XP per class); not shipping behaviour;
  - all others (Car6–10, Jet2/3/7, Tank4/5, Truck5–7, Minion1–3): no script unlock. U: DLC/entitlement content packages or never unlockable.
- **Prime:** see §4 (resets XP and challenge completions, unlocks 25 Prime challenges, Prime badge).

**Bot-involved events for the local player (original rules):** none count.
- Score, kill XP, medals, streaks and announcer require a `TnPlayerController` killer and victim (addendum 5).
- An assist is attributed in the same kill path, so an assist on an AI victim gives nothing.
- Damage to AI is still tracked in damage history, but produces no award.
- Counting bot kills is a **PC ADAPTATION** decision. Private matches give no XP anyway (`CanGainXp`).

**Capacity / limits to generalise for > 10 players (C):**
- `TnMultiplayerGame.MaxPlayersAllowed` 10 (CDO). Settings `NumPublicConnections` / `NumPrivateConnections` = 10 → `GetMaxPlayers()` = public + private → URL `?MaxPlayers=`.
- `GRI.MaxPlayers` = max(GRI.MaxPlayers, NumPlayers).
- Two teams fixed: `TnTeamHandlerTwoTeams`, team index 0/1, `TeamCounts[2]` in drafters. Party beacon `NumPlayersPerTeam` per team (online drafting only).
- No per-team cap in `PickTeam` (balance only).
- Player list and scoreboard rows are data-store driven (`GetCollectionRowCount('<CurrentGame:Players>')`), with no fixed row count in AS. H: on-screen layout space is the practical limit.
- Vote quorum: `GRI.VetoQuarum` = NumRequiredPlayers / 2 + 1.
- No fixed-size PRI arrays found in script. Native caps were not audited (U).

## Addendum 9: how locked MP chassis were unlocked in the shipped game (C unless marked)

- **Storage:** `TnCharacterCustomizationData.UnlockedChassis` (array of chassis UniqueIds, profile-saved). `IsChassisUnlocked` = `UnlockedChassis.Find(id) != -1`; script-binding `IsChassisUnlocked` returns true when the provider is not `LockedChassis`.
- **Only writer:** `TnCharacterCustomizationData.UnlockChassis` (AddItem + MarkAsDirty). Its callers (all script):
  1. `TnProfileSettings.CheckForLevelCompletionAchievements`: all Autobot campaign maps completed (any difficulty) → **Car5 (Arcee)**; all Decepticon maps → **Jet8 (Slipstream)**;
  2. `TnDebugManager` (debug console);
  3. `TnPlayerReliableReplicationInfoSurvival` dev cheat (developer-name whitelist, a specific generator, Barricade, console-build check; also 10000 XP per class). Not a retail path.
- `ResetAll` clears the list. Native code has no reference to `UnlockChassis`; the `UnlockedChassis` string appears only as property registration. No promo, pre-order, entitlement, stats or Demonware code touches chassis. DLC code in script concerns maps only (`DlcId` / content-removed prompts).
- **UI behaviour (CustomTransformers_GFX AS):**
  - The chassis picker lists only chassis with matching specialty and faction **and `IsChassisUnlocked`**. Locked chassis are **hidden**, not shown greyed.
  - The only "locked" presentation is an extra slot for Arcee / Slipstream with `UIText.Customization.Sprinter` / `Stalker` ("Complete the Autobot/Decepticon campaign to unlock a new chassis").
  - Escalation's CharacterSelect shows only `ArceeLocked` / `SlipstreamLocked` with `UnlockAutobot` / `UnlockDecepticon`.
  - Localisation has no other unlock hint.
- **Conclusion:** in the shipped disc data, Car6/7/9/10, Jet2/3/7, Tank4/5, Truck5/6/7 and Minion1–3 were **never unlockable for MP customisation**: no writer, hidden in the UI, no hint text.
  - H: they are iconic / campaign characters; those with `LockedCharacter` false (Truck7 Optimus, Jet2, Jet3) are still usable as iconic characters where `IsCharacterUnlocked` applies.
  - U: a later title update or DLC could have changed the provider flags; none are in the dump.

## Addendum 10: double jump (C, `TransGame.TnAcrobaticsManager`)

- **Exists for all robot-form pawns, MP included.** Data (`TnAcrobaticsManagerBlueprint`; MP shared `TR_Acrobatics_p.SharedAcrobatics`): JumpHeight **500**, **DoubleJumpHeight 450**, **DoubleJumpMinHeight 10**, HoverJumpHeight 500, HoverDuration 7, HoverAirSpeed 500, DodgeSpeed 3000.
- **Input path:** `TnPlayerController.CheckJumpOrDuck` → `RobotForm.Jump(, bUpdating)`.
  - The call is skipped while reviving.
  - `TnRobotForm.Jump` returns early while melee-attacking and needs MovementCapabilities `bCanJump && bJumpCapable`.
  - Robot form only: the vehicle forms do not use the acrobatics manager.
- **State machine:**
  - Ground `OnJump` → `Jumping`: Z velocity = √(2·|g|·JumpHeight) (+ base velocity), XY kept; records `_JumpBaseHeight` = height at take-off.
  - `Jumping` → `FallingFromJump` once Z velocity < 0.
  - **Second press in `Jumping` or `FallingFromJump`** → `DoubleJumping` iff `CanDoubleJump`:
    - the active weapon does **not** have `DisallowDoubleJump` (true on GatlingGun, HeavyRepairRay, HeavyRocketTurret);
    - **and** current height − `_JumpBaseHeight` > **DoubleJumpMinHeight (10 UU)**.
  - `DoDoubleJump`: Physics Falling; **velocity Z set (not added) to √(2·|g|·DoubleJumpHeight)**, XY kept. With |g| = 2940 → **1627 UU/s**, i.e. +450 UU above the second-jump point.
  - **Once per airtime:** `DoubleJumping` has no `OnJump`; it → `Falling` when descending, and `Falling` has no `OnJump`.
  - **Walking off a ledge** (`Falling` without a jump) gives **no double jump**.
  - Landing → OnTheGround / Skidding (skid if horizontal speed > MaxGroundSpeed).
- Max reachable rise ≈ 500 + 450 = 950 UU (second press at the apex).
- **AI:**
  - Jumps use `Jump(override, ForceJump=true)`: on ground → jump; in air → `DoubleJumping` with the override velocity (`TnAiActionNavigatePathSection` passes a computed JumpVel for jump links).
  - `TnAnchor.IsNavigationPointSupported` **rejects double-jump nav points** (`NavigationPoint.IsDoubleJump` = bNotBased with a jump link) as anchors.
  - So bots may double jump along jump-link path sections, but never anchor on unbased double-jump points.

## Addendum 11: knock-off kill credit and pawn collision (C unless marked)

**Fall / KillZ credit:**
- `TnPawn.FellOutOfWorld(DamageType)` defers until the pawn's tick (`_DeferredFellOutOfWorldRequested`), then calls stock `Pawn.FellOutOfWorld`: authority only, Health −1, `Died(none, KillZDamageType)`.
- `TnPawn.Died` → `HandleDied` → stock `Pawn.Died`: **if `DamageType.bCausedByWorld` and (Killer none or self) and `LastHitBy` ≠ none, then Killer = `LastHitBy`**.
  - `KillZDamageType` and `DmgType_Fell` both have `bCausedByWorld` true.
- `LastHitBy` is set by every `TakeDamage` from another controller (`InstigatedBy ≠ self.Controller`). Only `KilledBy` clears it. There is **no time window**: the last other player to damage this pawn during its life gets the kill, however long ago.
- The result is a normal kill: ScoreKill +1 (DamageType is not `DmgType_Suicided`, Killer set), Deaths +1, kill XP / medals via TrackKills (both PCs).
- KillZ is never downed (`CanBeDowned` excludes KillZDamageType) and is always insta-gib (`ShouldInstaGib`).
- Never damaged by another player → no killer → environment death, no score.

**Pawn-vs-pawn collision** (`TnPawnCollisionController`):
- Robot form: mode 1, `AnimatedCylinderRobotMeshHybrid`. The collision cylinder is the actor collision (`SetCollision(true, true)` = collide + **block actors**). It blocks traces only for zero-extent (`SetTraceBlocking(false, true)`). The robot mesh collides with actors but not as a rigid body.
  - The blueprint's `UseMeshCollision` → mode 2 (animated mesh); only Trypticon / Omega Supreme use it.
- **No team exception for pawn blocking:** teammates block each other like enemies.
- Team-specific rigid-body channels (RB 16–20 off, own `TeamCollisionChannel` on: `RBCC_Team0/1BlockingVolume`) only gate team blocking volumes for the RB meshes. Channel 15 is enabled for player pawns only.
- Vehicle form: mode 4, `PhysicalVehicleMesh`. The vehicle **mesh** is the collision (rigid body; the cylinder is disabled). Vehicle-vs-pawn contact is RB, plus the `Rammed` logic.
- Cylinders (`Blueprint.Collision`; robot form): Bumblebee-class 140×155, standard 175×225 / 175×240 / 175×200, Optimus-class 200×200, Brutes 200–225×265, Frenzy 100×120, CQC 140×170 (radius × half-height, UU).
