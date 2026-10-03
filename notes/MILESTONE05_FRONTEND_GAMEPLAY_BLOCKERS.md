# Milestone 05: Frontend / Gameplay blocker answers (2026-10-03)

This is a concise consumption note. Deep evidence is in:
- `MILESTONE05_FRONTEND_MATCH_BOOTSTRAP.md` (B);
- `MILESTONE05_GAMEPLAY_UNKNOWNS.md` (G);
- `notes/data/frontend_menu_graph.json`, `objective_marker_types.json`.

Items already confirmed there are only referenced, not re-derived.

**Labels:**
- **C** = CONFIRMED (bytecode / AS2 / authored data read directly).
- **H** = HIGH (one inference step).
- **P** = PARTIAL.
- **U** = UNKNOWN.

**Owner:** **FE** = Frontend lane, **GP** = Gameplay lane.

---

## A. Navigation into Multiplayer (FE)

| # | Behaviour | Source | Constants | Conf |
|---|---|---|---|---|
| A1 | Boot map `UI_FrontEnd_m` → MovieLoader → (logos first time only) → `FrontEnd_GFX` Press Start → main menu `mc_menuMain360/PS3/PC` | B §1.2–1.5 | — | C |
| A2 | **Multiplayer** = `if Online.CheckCanPlayOnlineModes() → Online.OpenPartyLobby('GTS_TeamGame')` → `ConfirmOpenPartyLobby` → `ClientTravelToMap("UI_PartyLobby_m?game=TransContent.TnPartyLobbyGame?listen")`. Offline: skip the checks and warnings and go straight to the party-lobby screen | FrontEnd_GFX sprite 29; `TnOnlineActionScriptBinding` | — | C |
| A3 | Party lobby root → **Host Game** (`hostGame_mc`) → mode list | PartyLobby_GFX sprite 83 | Back = `Game.QuitToMainMenu` | C |
| A4 | Every menu: open = `attachMovie` + hide parent + `giveInput(this)`; **B** = `closeMenu()` (show parent, `giveInput(parent)`, remove self, `BUTTON_BACK` sound) | HmMenu (`inputEvent`) | sounds `BUTTON_UP / DOWN / ACCEPT / BACK` | C |

## B. Mode selection and settings (FE)

| # | Behaviour | Source | Constants | Conf |
|---|---|---|---|---|
| B1 | Mode list = `<TnMenuItems:GameModes>` rows in provider order **TDM, DM, DOM, CTF, EXT, KOTH** | Xe-TransGame.ini `TnDataProvider_GameModeInfo` sections; PartyLobby sprite 79 | — | C (rows) / H (order = section order) |
| B2 | **Initial focus = item 0 (TDM)**. Up/down **wraps** (first ↔ last). Each focus change calls `Online.EditGameMode(SettingsConfigName)`, which publishes the mode and shows its description | `HmDataListMenu.createListSelections` (`listItem0_mc`; focusUp of item 0 = last) | — | C |
| B3 | Click → settings screen. One row per `TnGameSettings` field with a column header. Each row's default = current data-store value. **Rows clamp at the ends (no wrap)**: they're attached as `mc_lateralSelector` with the class default `loopNavigation = false` | PartyLobby sprite 82; `HmLateralSelector` (SharedComponents) | — | C (flow) / H (no wrap: no per-instance override for attached rows) |
| B4 | **TDM rows and defaults** (Private settings class `TnOnlineGameSettingsTDMPrivate`) | `TnDataStore_GameSettings`; TDM defaults | see table below | C |
| B5 | **Create Game** → `DataStores.WriteValue(field, choice)` per row → `Online.PlayPrivateGame('TDM')` → `TnPartyLobbyGame.HostOnlineGame` (session steps: skip offline) → `BuildLobbyURL $ "?listen"` → `ServerTravelToMap` | B §2.1 | — | C |

**B4 TDM rows and defaults:**

| row | choices | default |
|---|---|---|
| Team Balancing | Manual / **Autobalanced** | Autobalanced |
| Map Selection | Rotate / **Host's Choice** | Host's Choice |
| Time Limit | 10 / **15** / 20 min | 15 min |
| Points to Win | 20 / 30 / **40** / 50 | 40 |

## C. Map selection in the game lobby (FE)

| # | Behaviour | Source | Constants | Conf |
|---|---|---|---|---|
| C1 | List = `<TnMenuItems:Maps>` rows that are **enabled** and whose `CompatibleGameTypes` contains `<CurrentGame:MapCompatibilityTag>`, in TransLevels.ini section order | GameLobby sprite 151 `updateMapArray` | — | C |
| C2 | **TDM order** (6 maps in the dump; the DLC maps 511–512 are disabled): **Seed of Corruption 501, Berth 502, Complex 503, Rust 504, Orbital Debris 507, Streets 508, Molten 509, Gorge 510**. Streets = index 5 | TransLevels.ini + package presence | — | C (order) / H (DLC disabled via native `HasRequiredAssets`) |
| C3 | Widget `selectMap_mc` = `HmLateralSelector`, **`loopNavigation = true`** on the 360 / PS3 / PC versus menus (false only on the unused base clip). Left / right step ±1 **with wrap**; A also advances (wraps). `displaySelection = 'never'`: the selector shows its label "$UIText.Lobby.SelectMap", not the map name | GameLobby PlaceObject clip params, sprites 149–151; SharedComponents `HmLateralSelector.widgetInputEvent` | `currentSelectionIndex = 0` | C |
| C4 | **Default selection:** building the list calls `createSelectionData` → `updateCurrentData` at **index 0** → `selectionUpdated` → `Online.SetSelectedMapID(list[0])`. In Host's Choice this **overrides the server's initial random pick**, so the lobby opens on **Seed of Corruption (501)** for TDM. The list is rebuilt, and index 0 re-sent, whenever MapCompatibilityTag changes | same | — | C (code path) / H (that the movie builds after the GRI exists) |
| C5 | **Stored vs displayed:** the selector index is UI-local. The authoritative selection is `GRI.SelectedMapID` (`SetMapId` → `UpdatePrestreaming`). The map panel (name label and thumbnail via `SetExternalTextureWithPath('MapImage'+id, ImagePath)`) is driven only by `<CurrentGame:SelectedMapID>` change callbacks, so it shows the server value, not the selector index | B §2.4; `updateSelectedMap` | label colour 0xFF9333 (0xFF3333 unavailable) | C |
| C6 | `SetSelectedMapID` is honoured only when `MapSelectionMethod == 1` (Host's Choice); in Rotate it is ignored. `selectMap_mc` is enabled only for the host, in Host's Choice, while not counting down | `GRI.HostRequestMapID`; `updateMenu` | — | C |
| C7 | **Return from a match (Host's Choice):** the server keeps the previous MapId (`OnEnterLobbyFromMap`), but the rebuilt lobby movie sends index 0 again, **so the selection resets to the first compatible map**. Rotate: a random different compatible map; the UI push is ignored | C4 + B §2.4 | — | H |
| C8 | **Start Game** (host, `CanHostRequestGameStart`, not counting down) → `BeginLobbyExitCountdown` → `HostRequestsGameStart` → **10 s** short countdown → `FinalCountdown` (teams) → `StartLevel` | B §2.4 | `LowCountdownTickThreshold 10` | C |

## D. Match bootstrap payload and sequence (GP + FE)

**D1. URL the match reads** (B §3.1; C for keys):
`<MapFilename>?Game=TransContent.TnVersusGame?GameModeTag=TDM?GameTeamStatus=3?PointsToWin=<20|30|40|50>?TimeLimit=<600|900|1200>?MaxPlayers=10?MapId=<id>?listen`

**D2. Settings override path** (C):
- `PointsToWin` property → `TnMultiplayerGame.InitGame` → `GoalScore` → `GRI.GoalScore`.
- TimeLimit index → `TimeLimits[i]` seconds → `GameInfo.TimeLimit` → `GRI.RemainingTime`.
- With no URL value, `GoalScore` and `TimeLimit` stay at the class defaults (0 = no limit). So **the rebuild must pass both explicitly**.

**D3. Rules** come only from `GetOnlineGameSettings().Rules` (C). Offline the bootstrap must create them, in order:
1. `ScoreKillsTDM`
2. `TrackKillsMP`
3. `ReportGameProgressTime`
4. `ReportGameProgressKills`

**D4. Server order** (C):
1. `GameInfo.InitGame` (MaxPlayers, TimeLimit, rules), then `TnGame.InitGame` (spawn / respawn helpers, spawn-point manager), with `TnMultiplayerGame.InitGame` reading PointsToWin / Rounds.
2. `InitGameReplicationInfo` (TeamHandler, GameTeamStatus, MapId, autobalance flag, `PublishGameInfo`, GoalScore, RemainingTime).
3. Players log in / travel in.
4. `PendingMatch` (10 s).
5. `StartMatch` → `InProgress`.

**D5. Client order** (C):
1. GRI `PostBeginPlay` → UI event 15.
2. `UpdateUiController` → `TnUIControllerMultiplayer` (WaitingOnGameStart → character select → PreGameCountdown).
3. Event 3 → InGame → HUD visible.

## E. Teams, spawn, respawn, death (GP)

| # | Behaviour | Source | Constants | Conf |
|---|---|---|---|---|
| E1 | Team objects: `Teams[0] = TnFactionTeamAutobots`, `Teams[1] = TnFactionTeamDecepticons` | `TnTeamHandlerTwoTeams.SpawnTeams` | — | C |
| E2 | **Lobby FinalCountdown:** Autobalanced → `AssignTeams` (**teams from the online reservation only**; offline nobody gets a team); Manual → `ForceToTeam` = `PickTeam(255)` for every team-less human | `TnTeamHandlerTwoTeams` | — | C |
| E3 | **`PickTeam`:** keep current if < 2; else the smaller team; **tie → `RandomInt(2)`** | same | — | C |
| E4 | **In the match:** seamless-travelled players keep their team (`TnTeamGame.HandleSeamlessTravelPlayer`); **a player arriving with no team is not given one** by the travel path (stock `GameInfo.HandleSeamlessTravelPlayer` has no team pick). A fresh login uses `?Team=` (default 255) → reservation → else `PickTeam` → `ChangeTeam` | Engine `GameInfo.Login` / `HandleSeamlessTravelPlayer` | — | C |
| E4 → rebuild | **Offline, call `PickTeam(255)` for every player before `StartMatch`** (the faithful replacement for the reservation step) | — | — | H |
| E5 | Initial spawn: no spawns in PendingMatch. In InProgress, `SpawnHelper` (ready = can restart + has selected a character) → `RespawnHelper.InitialSpawn` → **immediate** (`TimeToAllowInstantInitialSpawns = −1`) | G / B §5.3 | — | C |
| E6 | Spawn point: team's active cluster, round-robin, ≤ 4 safe tries. Initial clusters locked 15 s. TDM: every cluster usable by both teams (`FactionNeutralGameTypes`). Re-pick every 0.1 s, switch at score +5 or after 10 s | B §5.3 | Streets initial: Autobot `TnSpawnCluster_7810`, Decepticon `_4159` | C |
| E7 | **Death flow** (pawn killed): | `TnPlayerController.Dead.BeginState`, `Dead.StartSpectating`, `PlayerSpectating`; `TnRespawnHelperWave` | `MinRespawnDelay 3.0` (TnPlayerController default); `WaveRespawnTime 5.0` | C |
| | 1. Server: `TnGame.Killed` → `RespawnHelper.Died` → queue **5.0 s** (0 if `_ShouldInstantRespawn`, the kill-streak reward); `PRI.TimeToRespawn` counts down | | | |
| | 2. Controller enters `Dead`: death camera (`CameraStrategyManager.Died`), full-screen effects removed | | | |
| | 3. In MP, after **`MinRespawnDelay = 3.0 s`** → `PlayerSpectating` → UI event 4 → Spectating UI (`MultiplayerRespawn_GFX` shows `<PlayerOwner:TimeToRespawn>`), with the spectate camera | | | |
| | 4. At 5.0 s → `RestartPlayer` → leaves spectating → UI event 5 → InGame | | | |
| | 5. Pressing fire / use in `Dead` → `ServerRestartPlayer` → `RequestRespawn`, which **does nothing** for the Wave helper (empty `OnRequestRespawn`) | | | |
| E8 | **`PlayerRestartDelay=6.0` (Xe-TransGame.ini) is dead config**: no property of that name exists in the TransGame / Engine / HM_Engine name tables. Use 3.0 s (spectate) and 5.0 s (respawn) | package name tables | — | C (absence) |
| E9 | Downed state exists only for pawns with `TnSkillCanBeDowned` (`TnMultiplayerGame.AllowDowned`). Standard TDM characters: P (skill lists not checked) | B §5.5 | — | P |

## F. Scoring, end, results, restart (GP)

| # | Behaviour | Source | Constants | Conf |
|---|---|---|---|---|
| F1 | Kill: killer PRI `Score += 1`, **team score += 1** (`TeamScoreAmount 1`), `Kills += 1`; victim `Deaths += 1`. **Suicide / environment: no score.** Teammate damage is ignored except AOE | B §5.5 | — | C |
| F2 | **Assists:** the first other damager in the victim's damage history gets `AddAssist(damage / HealthMax)`: an XP event above 0.5 (Assist) or 0.25 (WeakAssist) and an assist stat. **Assists never add Score** and are **not on the scoreboard** | `TnPlayerReplicationInfo.AddAssist` | — | C |
| F3 | End triggers: team score ≥ GoalScore (`CheckScore` after every kill); `GRI.RemainingTime` reaches 0 (1 Hz GRI timer); forfeit (a team empty 1.5 s after a logout). **No overtime:** `GameInfo.EndGame` sets `bOverTime` only if `CheckEndGame` fails, and Versus never fails it. Equal scores = winner none = "Tie game" | `GameInfo.EndGame` / `TnVersusGame.CheckEndGame` | — | C |
| F4 | **End state:** | `PlayerController.GameHasEnded`, `RoundEnded.BeginState` (+ Tn override); `MatchOver` | `MatchOverCountdown 15` | C |
| | 1. Every controller `GameHasEnded` → state **`RoundEnded`**: `bFrozen`, `StopFiring`, death camera, view target kept. Pawns stay in the world | | | |
| | 2. Game → `MatchOver`: `GRI.SetGameStatus(5)`, UI event 9 (HUD hidden, `EndGameStats_GFX`), stats; after **15 s** → `ReturnToGameLobby` | | | |
| | 3. Kills and scoring are no-ops in MatchOver | | | |
| F5 | **Results screen:** IconicMode ? scoreboard : XP earnings first; X toggles; **B does nothing in-match** (no parent menu). Scoreboard: teams sorted Score↓ then TeamIndex; players sorted **Score↓, Kills↓, Deaths↑, Name**; columns Level · Name · **Score · Kills · Deaths** (Kills / Deaths only in ViewMode InGame) | EndGameStats_GFX, PlayerList_GFX | — | C |
| F6 | **Restart semantics:** a new TDM match always **reloads**: `ReturnToGameLobby` = `ServerTravel` to `UI_Lobby_m?...?MapId=`, then a new `StartLevel` travel to the map. In-place reset exists only for round modes (`RestartRound` = `SoftReset` + UI event 3 + respawn all) and `MatchOver.ResetLevel` (not used by TDM). `StartMatch` itself resets pawns, dropped pickups and pickup factories in place | B §5.7–5.8; `TnTeamGame.StartMatch` | — | C |

## G. HUD state ownership (FE)

| Data | Owner (engine side) | Delivery to Scaleform | Conf |
|---|---|---|---|
| Health / segments | `TnSegmentedHealth` via `TnHudDataObserverSegmentedHealth` | push `_global.NotifySegmentedHealthChanged` | C |
| Overshield | same (`Health − HealthMax`, max 550) | push `_global.NotifyOverShieldChanged` (normalized) | C |
| Ammo | weapon via observers | push `NotifyWeaponClipAmmoChanged` / `NotifyWeaponReserveAmmoChanged` / `NotifyGrenadeAmmoChanged` | C |
| Crosshair | weapon spread / reticule / lock-on / target observers | push `NotifyWeaponSpreadChanged`, `NotifyWeaponReticuleTypeChanged`, `NotifyLockOnStateChanged`, `NotifyTargetTypeChanged` | C |
| Match clock | `GRI.RemainingTime` → `OnRemainingTimeUpdated` → `ResetCountdown` | **pull / subscribe** `<CurrentGame:CurrentCountdown>` + `<CurrentGame:IsCountingDown>`, rendered `MM:SS` (≤ 10 s flashes red) | C |
| Team score | `TeamInfo.Score` | **poll every 500 ms** `<CurrentGame:Teams>` (TeamIndex, Score) + `<CurrentGame:GoalScore>`; bar width `25 + Score/GoalScore × 141` | C |
| Player score | `PRI.Score` | `<PlayerOwner:Score>`; scoreboard `<CurrentGame:Players>` Score / Kills / Deaths | C |
| K / D / A | PRI Kills / Deaths; assists are stats only | scoreboard only (no on-HUD K/D); assists not displayed; kill events via `_global.PointEvent` / `RewardAnnouncement` / `GameAnnouncement` | C |
| Respawn timer | `PRI.TimeToRespawn` | `<PlayerOwner:TimeToRespawn>` in MultiplayerRespawn_GFX | C |
| Player / objective markers | **Canvas (UnrealScript `TnObjectiveMarkerType*`)**, not Scaleform | — | C |

## H. TDM player markers (Canvas; FE / Rendering)

Source: `TnObjectiveMarkerTypeTransformerVersus` + Sprite base + authored defaults (C).

**Registration and visibility:**
- **Registration:** each pawn on `SetupMarker` → label = **`PRI.PlayerName`**, or if empty the localized iconic character name. Marker class = `GameClass.TransformerMarkerClass`.
- **Hidden:** for yourself, and **while the marked pawn is dead**.
- **Ally:** always drawn.
  - `MarkerAlly_MAT`; **focused size 0.08, unfocused 0.04** (fraction of canvas **width**).
  - Label always drawn, colour (100, 210, 250, 220), offset −0.04.
  - **Off-screen only while that ally is downed.**
  - Health bar under the label **only if the viewer's specialty is "Scientist"**.
- **Enemy:** **not drawn** (size forced to 0) unless the viewer has `TnBuffSeeEnemyObjectiveMarkers` (not if the target has a Warcry buff), the target is HardLocked by the viewer or the viewer's team, or the target has `TnBuffRevengeMarker`. Label hidden when the target is cloaked or out of camera line of sight.
  - Setup: `MarkerEnemy_MAT` 0.03125, label (240, 20, 20, 220), no off-screen.
- **Disguised enemy:** drawn as an ally with the disguise name; hidden without line of sight.

**Focus and placement:**
- Focused if within **0.02734 × canvas width** of the screen centre, **or within 3000 UU** of the viewer (`AutoFocusRange`).
- Focus is kept **1.0 s** (`FocusHysterisis`) after it ends; the label alpha fades over that time when unfocused labels are off.
- Label anchor: pawn location + half collision height.
- **No distance text** on player tags (distance labels belong to `TnObjectiveMarkerTypeObjective` only).

**Team score colours** (Hud_GFX, for the HUD): own-team bar is ally colour, other team enemy colour.

| own team | ally colour | enemy colour |
|---|---|---|
| Autobot | 0xF03C3C | 0xA06FFF |
| Decepticon | 0xA06FFF | 0xF03C3C |

## I. Pickups (GP)

| # | Behaviour | Source | Constants | Conf |
|---|---|---|---|---|
| I1 | Health pickup: allowed if `Health < HealthMax`; **full heal** (`SHT_AddAllSegments`, `AddedHealth = 50` unused) | G §6 | — | C |
| I2 | Overshield: allowed if overshield < 550; sets `Health = HealthMax + 550`. **No time limit or decay** (no tick drains it); it is consumed only by damage first. Regen never refills it | `TnSegmentedHealth`, `TnHealthRegener` (stops at `Health ≥ HealthMax`) | Overshield 550 | C (no script decay) / H (no native decay) |
| I3 | Health regen: after **2.0 s** without damage, **20 HP/s**, segment-limited (`TnHealTypeRegen` = `SHT_HealSegment`: refills only the current segment). Any damage resets the delay. Not while downed | `TnHealthRegener`; Optimus `HealthRegenParameters`; segments `[175, 125, 125, 125]` | — | C |
| I4 | Ammo crate: allowed if any primary / secondary / vehicle weapon is not maxed; refills all of them | G §6 | — | C |
| I5 | **Respawn:** after pickup → `SetRespawn` → `Sleeping` for the instance `RespawnTime` → `Pickup` | `PickupFactory.SetRespawn`; Streets instances | **Streets: ammo ×14 = 30 s, health ×9 = 60 s, overshield ×1 = 120 s** | C (values) / H (Sleeping latent timer is stock) |
| I6 | **Match start resets every factory:** `TnTeamGame.StartMatch` → `Reset()` → `GotoState('Pickup')` (non-super items), so **all pickups are available at match start and any running timer is cancelled** | `PickupFactory.Reset` | — | C |

## STILL UNKNOWN / PARTIAL (not blockers for the first TDM pass)

- Native `HasRequiredAssets` result per map (assumed: maps present in the dump are enabled).
- Whether standard MP characters have `TnSkillCanBeDowned`.
- The in-match scoreboard toggle input (InGameStats open / close binding).
- Exact Scaleform movie teardown timing on travel (native).
