# Milestone 05: frontend → TDM match bootstrap (2026-10-03)

**Goal:** boot → original frontend → Multiplayer → mode → map → loading → map/rules init → spawn → TDM → end → results / return. MP_IAC_Streets is the first map.

## Sources (all read in place)

- **UnrealScript bytecode** via `tools/ue3dis.py`:
  - TransGame / Engine classes are in `work/script/decomp`.
  - TransContent classes are cooked into maps, so they were decompiled from:
    - `UI_FrontEnd_m` (TnFrontEndGame);
    - `UI_PartyLobby_m` (TnPartyLobbyGame);
    - `UI_Lobby_m` (TnGameLobbyGame*);
    - `MP_IAC_Streets_BASE_m` (TnMultiplayerGame / TnTeamGame / TnVersusGame / TnUIControllerMultiplayer).
  - Dumps are in `work/q/frontendgame.txt`, `work/q/UI_*_script.txt` and `work/q/streets_base_gameclasses.txt` (not committed; regenerate with ue3dis).
- **Authored defaults and Kismet:** AssetTools `authored.db`.
- **Shipped config and localization:** `ExtractedAssets/config/Coalesced_ini` (Xe-TransGame.ini, Xe-TransEngine.ini, TransPlaylists.ini, TransLevels.ini) and `Coalesced_int` (TransGame.int, UIText.int).
- **Scaleform AS2** from `ExtractedAssets/content/UI_GFx*/*.gfx`, read with the new `tools/gfxpool.py` (constant-pool dumper) and `tools/gfxcallgraph.py`, which writes **`notes/data/frontend_gfx_callbacks.json`**.
- **default.xex** (read-only headless Ghidra) for the loading-movie natives.

**Labels:**
- **CONFIRMED** = read directly from bytecode, authored data, config or AS2 pools.
- **HIGH** = one inference step from confirmed code.
- **PARTIAL / UNKNOWN** as stated.
- Stock-UE3 behaviour is never used as proof unless it is labelled as such.

### Important framing for Integration (CONFIRMED)

**WFC has no offline "local multiplayer" path.**
- Every versus match is reached the same way: frontend → **party lobby map** → **game lobby map** → match map.
- Every one of those maps is a listen server (`?listen`), and the online subsystem creates sessions along the way (`TnPartyLobbyGame.HostingGame`).
- A **private match** (`PlayPrivateGame`, `TnOnlineGameSettings*Private`) is the original's closest equivalent of a local match: host's-choice map, no matchmaking.

For the rebuild, the faithful non-networked reduction is to keep the **same game-side state machines, URLs and data** and drop the session / reservation calls. Everything below marks where those calls sit so they can be bypassed.

---

## 1. Boot → title → main menu (Phase 1)

### 1.1 Engine boot (CONFIRMED config)
- `Xe-TransEngine.ini [URL]`: `Map=UI_FrontEnd_m`, `LocalMap=UI_FrontEnd_m`, `TransitionMap=UI_FrontEnd_m`.
- `GameViewportClientClassName=TransGame.TnGameViewportClient`, `LocalPlayerClassName=TransGame.TnLocalPlayer`.
- `UI_FrontEnd_m`'s WorldInfo game is **`TransContent.TnFrontEndGame`**. Its script is cooked in that map. `[TransContent.TnFrontEndGame] MaxPlayers=1`.
- **Native startup / loading movie** (`Xe-TransGame.ini [LoadingMovie]`):
  - `InitialStartupFileName=TF_InitialStartup`, `DefaultFileName=TF_LoadingScreen`, `AlphaFileName=UI_GFxLoading_p.LoadScreenAlpha_GFX`.
  - Bink files `Movies/TF_InitialStartup_{NA,EU}_{INT,FRA}.bik` and `TF_LoadingScreen_{INT,FRA}.bik`.
  - Native readers (PARTIAL; located, not fully traced):
    - `0x826F13B8` → `0x82CD32A0` (InitialStartupFileName);
    - `0x82CEB908` creates the movie player with `DefaultFileName` (called from `0x82CEBA88`);
    - `0x82CD3660` plays the `AlphaFileName` GFx overlay (called from `0x82D61E08`).

### 1.2 Frontend map Kismet (`UI_FrontEnd_m` Main_Sequence, CONFIRMED)

```
SeqEvent_GameplayStarted → SeqAct_Interp "Black-Out" (client-side) → (Completed|Aborted) → GFxAction_OpenMovie UI_GFxFrontEnd_p.MovieLoader_GFX_1
MovieLoader_GFX AS2: Game.HasWatchedIntroMovie()  (TnGameActionScriptBinding)
   ├─ fscommand "enterMovieSequence" → RemoteEvent closeMovieLoader (→ GFxAction_CloseMovie)
   │      → SeqAct_MoviePlayer Logo_Activision → (Stopped) Logo_Hasbro → (Stopped) Logo_HighMoon → (Stopped) FMV_intro → (Stopped) ⇒ [FRONTEND START]
   └─ fscommand "enterFrontEnd" ⇒ [FRONTEND START] + RemoteEvent closeMovieLoader
[FRONTEND START] (same 9 targets from both paths):
   SeqAct_Interp "Fade In" (rewind), "Primary Camera" (looping, CameraActor_6585), "Camera Orbiter" (looping, InterpData_6478; its event track fires AUDIO_START → sub-sequences AMB_IACON + AMB_KAON, and 7 debris whoosh one-shots),
   RemoteEvent "StartFireworks", SeqAct_Reverb (REVERB_TRANS_FRONT_END), SeqAct_PlayMusic, PlaySound FRONTEND_WHSH_REVEAL,
   SeqAct_SetLoadingMovieFilename(String "UI_GFxLoading_p.LoadScreen_GFX"),
   SeqAct_ToggleHUD(Player) → SeqAct_ToggleHidden(Player) → TnSeqAct_OpenFrontEnd → SeqAct_InstallGame → (Finished) 3× SetMatInstScalarParam on UI_FrontEndMaterials_p.Energon* (DownScaleUVs 12, ring Opacity)
SeqEvent_PreGameplaySetup → SeqAct_SetLoadingMovieFilename (same string)
GFxEvent_FsCommand FrontEnd_GFX "startMainMenuCamera" → SeqAct_Interp_9395 (energon ring / circuit materials + meshes)
```

- `Engine.MovieSettings MoviesToAlwaysPlaySound` = the three logos. `MovieMixerPreset=CINE_MUTE_FOR_BINK`.
- **The logos play only until the intro has been watched once**: `TnFrontEndGame.WaitingForController.Tick` calls `TnGameActionScriptBinding.SetHasWatchedIntroMovie()` once a controller is assigned.
- After that, MovieLoader takes the `enterFrontEnd` branch (HIGH: the AS2 pool is `hasWatchedMovie | checkForMovieWatch | Game.HasWatchedIntroMovie`; the branch body is not disassembled).

### 1.3 Frontend game state machine (`TnFrontEndGame`, CONFIRMED)

1. `InitGame` sets a 1 s repeating timer `CheckForAutomatedTestingStart`.
2. `PostLogin` → `GotoState('WaitingForController')`. `ShouldSpectateOnLogin` = true, so there is **no pawn in the frontend**. `AllowGameRules` = false.
3. **WaitingForController.Tick:**
   - honours a deferred invite controller;
   - otherwise, on console with `HasInstalledGame`, assigns the first connected controller (0..6) via `TnGameViewportClient.AssignControllerToLocalPlayer`;
   - once `VP._HasAssignedControllerId`: if `NeedsLogIn()`, go to `WaitingForBaseOnlineService` (console) or `WaitingForNetwork` (PC); otherwise go to state None.
4. **Login states:** `WaitingForNetwork` → `ReadingAccountNames` → `LoggingInPC` / `LoggingInConsole`. These are online-only; **bypass in the rebuild.**
5. **Login change:** `NotifyLoginChange` → `LoginChangeOnXbox`:
   - `VC.ForceControllerSelection()`, `DisallowControllerSelection()`;
   - `PC.UIController.OnUIEvent(1)` (ResetFrontEnd);
   - `RestartFrontEnd()` → back to `WaitingForController`.

### 1.4 UI controller (`TransGame.TnUIController`, a StateFullObject; CONFIRMED)

**`Initialize(OpenUIDelegate, CloseUIDelegate, PC, UseInGameLobby, OldUIController)`** → `GotoState(StartingState)`.

Base defaults:

| field | value |
|---|---|
| StartingState | `NotInGame` |
| MessageBoxUI | `UI_GFxShared_p.MessagePrompt_GFX_1` |
| NotificationPopupUI | `UI_GFxOnlineNotifies_p.OnlineNotify_GFX_1` |
| TextPopupUI | `UI_GFxShared_p.TextPrompt_GFX_1` |
| MouseCursorUI | `UI_GFxMouseCursor_p.Cursor_GFX_1` |

**`OnUIEvent(code)`** dispatch:

| code | handler | code | handler |
|---|---|---|---|
| 0 | OnFrontEnd | 10 | OnPlayAgain |
| 1 | OnResetFrontEnd | 11 | OnGotoMainMenu |
| 2 | OnEnterLobby | 12 | OnShowHud(false) |
| 3 | OnBeginGame | 13 | OnShowHud(true) |
| 4 | OnSpectating | 14 | OnCampaignGameOver (only if the character has ChassisTypes) |
| 5 | OnRespawn | 15 | OnGRIAvailable |
| 6 | OnPause | 16 | OnGameInviteAccepted |
| 7 | OnClearPause | 17 | OnJoinGameInviteFailed |
| 8 | OnRoundEnd | 18 / 19 | invite failed (secondary / primary service) |
| 9 | OnEndGame | | |

**States:**

| state | on entry | transitions |
|---|---|---|
| NotInGame | — | 0 → FrontEnd |
| FrontEnd | `OpenUI(FrontEndUI)`; 1 reopens it | 2 → InLobby |
| InLobby | `OpenUI(LobbyUI)` | — |
| WaitingOnGameStart | once the GRI exists, `OpenUI(GameStartUI)`, or `InGameLobbyUI` if `_InGameLobby` | 3 → InGame (when not an in-game lobby); 4 → Spectating; 5 → InGame; 0 → FrontEnd |
| InGame | `SetHudVisible(true)` unless hiding | 6 → Paused; 8 → WaitingOnNextRound; 9 → GameEnded; 4 → Spectating; 0 → FrontEnd |
| Spectating | HUD visible + `OpenUI(SpectatingUI)` | 5 → InGame; 9 → GameEnded; 6 → PausedSpectating |
| Paused | `SetPause(true)` + `OpenUI(PauseUI)`; closing the UI returns to InGame | 11 → NotInGame |
| WaitingOnNextRound | `OpenUI(GameStartUI)` | 3 → InGame |
| GameEnded | HUD hidden + `OpenUI(EndGameUI)` | 10 → WaitingOnGameStart |

**Subclasses** (authored defaults):

| subclass | movies | StartingState |
|---|---|---|
| TnUIControllerFrontEnd | FrontEndUI `UI_GFxFrontEnd_p.FrontEnd_GFX_1` | (base) |
| TnUIControllerPartyLobby | LobbyUI `UI_GFxLobbies_p.PartyLobby_GFX_1` | InLobby |
| TnUIControllerGameLobby | LobbyUI `UI_GFxLobbies_p.GameLobby_GFX_1` | InLobby |
| **TnUIControllerMultiplayer** | InGameLobbyUI `UI_GFxCustomize_p.CustomTransformers_GFX_1`; GameStartUI `UI_GFxPreGameCountdown_p.PreGameCountdown_GFX_1`; PauseUI `UI_GFxPause_p.PauseMenu_GFX_1`; SpectatingUI `UI_GFxRespawn_p.MultiplayerRespawn_GFX_1`; EndGameUI `UI_GFxEndGameStats_p.EndGameStats_GFX_1` | **WaitingOnGameStart** |
| TnUIControllerCoop / TnUIControllerSurvival | (not expanded) | — |

**TnUIControllerMultiplayer overrides** (cooked in the MP map):
- `WaitingOnGameStart.OpenGameStartUI` → `OpenUI(InGameLobbyUI)`;
- `WaitingOnGameStart.OnCharacterSelected` → if `!GRI.bMatchHasBegun`: `CloseCurrentUI()`, `OpenUI(GameStartUI)`;
- global `OnCharacterSelected` → notification "CharacterSelectedInGame".

**Senders of the events:**

| event | sender |
|---|---|
| 0 | `TnSeqAct_OpenFrontEnd` → `TnPlayerController.OnOpenFrontEnd` |
| 1 | `TnFrontEndGame.LoginChangeOnXbox` |
| 3 | `TnMultiplayerGame.InProgress.BeginState`, `TnGame.RestartRound`, and late-join via `UpdateUiController` |
| 4 / 5 | `TnPlayerController` `PlayerSpectating` / `PlayerWaitingSpectating` Begin/EndState (5 also from `PlayerWaitingWatchingMatinee`) |
| 6 | `TnPlayerController.ShowMenu`, `TnGame.SetPause` |
| 8 | `TnGame.RoundEnded` |
| 9 | `TnMultiplayerGame.MatchOver.BeginState` |
| 11 | `TnPlayerController` (quit path) |
| 12 / 13 | cinematic mode and debug |
| 15 | `TnGameReplicationInfo.PostBeginPlay` |
| 16–19 | invite handling |

- `TnPlayerController.UpdateUiController` selects the controller from **`GRI.GameClass.default.UIControllerClass`**:

| game class | UIControllerClass |
|---|---|
| TnGame (base) | TnUIController |
| TnFrontEndGame | (inherits) |
| TnGameLobbyGameTeam | **TnUIControllerGameLobby** |
| TnMultiplayerGame / TnVersusGame | **TnUIControllerMultiplayer** |

  If `GRI.GetGameStatus() == 3` (in progress), it also sends `OnUIEvent(3)` at once (late join).
- **Frontend:** Kismet `TnSeqAct_OpenFrontEnd` → `TnPlayerController.OnOpenFrontEnd` → `UIController.OnUIEvent(0)` → state FrontEnd → `OpenUI(FrontEndUI = UI_GFxFrontEnd_p.FrontEnd_GFX_1)`.

### 1.5 Main menu (CONFIRMED from AS2 disassembly, `tools/as2dis.py`; screen graph in **`notes/data/frontend_menu_graph.json`**)

**Press Start** (`mc_menuPressStart`, `$UIText.MainMenu.PressStart`):
- shown when `Online.ShouldShowStartScreen()`;
- START → `Online.ShowDeviceSelectionUI()`, `attachMainMenu()`, `Sound.PlaySound('BUTTON_START')`.

**`attachMainMenu`** picks `mc_menuMain360`, `mc_menuMainPS3` or `mc_menuMainPC` by `HmUtility.Platform`.
- Each is registered as class `HmMenu`. Focus starts on `campaignBtn_mc`. The footer shows no Back hint (`noBack`).
- `onOver` sets `Footer.hint_mc.HintText = $UIText.MainMenu.<X>Desc`.

**Shipped 360 menu buttons:**

| button | action |
|---|---|
| campaignBtn_mc | `Online.CheckIsProfileReady(1)`; the engine answers with `_global.ProfileIsReady(1)` → attach `mc_menuCampaign` |
| **multiplayerBtn_mc** | **`if (Online.CheckCanPlayOnlineModes()) Online.OpenPartyLobby('GTS_TeamGame')`** |
| escalationBtn_mc | same check → `OpenPartyLobby('GTS_SingleTeamGame')` |
| settingsBtn_mc | `CheckIsProfileReady(2)` → `ProfileIsReady(2)` → `_root.attachMovie('mc_settingsMenuLoader', …, {hideClip: Footer, parentMenu})`; hides the menu and sets Footer alpha 0 |
| extrasBtn_mc | `CheckIsProfileReady(3)` → `ProfileIsReady(3)` → `mc_extrasMenuLoader` |
| accountsBtn_mc, exitGameBtn_mc (`Game.ExitGame`) | PC menu only |

**Campaign submenu:**
- Solo (`Online.ProceedToSoloPlay` → `mc_menuSolo`: Resume Autobot / Resume Decepticon / Mission Select → difficulty → `Online.OpenCampaignGameLobby`);
- Cooperative (`OpenPartyLobby('GTS_CampaignGame')`).

**Unused variant:** `mc_menuMain` / `mc_menuOnline` (Play Online → `OpenPartyLobby` by `onlineMode`; Play With Friends) is exported but not attached by `attachMainMenu` (HIGH: not used).

**Menu conventions** (every HmMenu, CONFIRMED):
- **Opening a submenu:** `parent.attachMovie(clip, inst, depth, initObj)`. The new menu stores `ParentMenu = _global.currentMenu`, hides it, and calls `_root.inputHandler.giveInput(this)`.
- **Back = `closeMenu()`:** `ParentMenu._visible = true`, `giveInput(ParentMenu)`, `removeMovieClip()`. Root lobby menus instead call `Sound.PlaySound('BUTTON_BACK')` + `Game.QuitToMainMenu()`.
- **Confirmation prompts:** `HmUtility.DisplayMessagePrompt(title, body, "label,callbackPath,label,callbackPath,…")`, closed via `_global.CloseMessagePrompt`. Engine-side prompts use `UIController.ShowPopupUI` (MessagePrompt_GFX) with `SetAButton` / `SetBButton` delegates (e.g. the OpenPartyLobby warnings).

- **`TnOnlineActionScriptBinding.OpenPartyLobby(GTS)`** (CONFIRMED script):
  1. `CheckOnlineWarningPart0` (profile / online check; `TnOnlineStatusMessageBox` if `!CanPlayOnlineModes`);
  2. → Part1 (console `CanCommunicate` warning);
  3. → Part2 (first-time "RecommendPlayingCampaignFirst" for non-campaign);
  4. → **`ConfirmOpenPartyLobby`**:
     - `GRI.SetGameTeamStatus(GTS)`;
     - `URL = PC.BuildPartyLobbyURL()` = `"UI_PartyLobby_m?game=TransContent.TnPartyLobbyGame?listen"` (`Engine.PlayerController.BuildPartyLobbyURL`; `TnPlayerController.GetPartyMapName` = "UI_PartyLobby_m"; `PartyLobbyGameType` from `[TransGame.TnPlayerController]`);
     - `TnGame.static.ClientTravelToMap(URL)`.

---

## 2. Party lobby → mode selection → game lobby (Phases 1, 4)

### 2.1 Party lobby (`UI_PartyLobby_m`, `TnPartyLobbyGame`, CONFIRMED)
- `InitGame` gets the PlaylistManager and calls `DownloadPlaylist()`.
- `PostLogin` (local) → `WaitingForTasksToIdle` → `CreatingPartySessions` → **`Ready`**. These are online session steps.
- UI: `TnUIControllerPartyLobby` → `UI_GFxLobbies_p.PartyLobby_GFX_1`. The movie lists `<TnMenuItems:Playlists>` and `<TnMenuItems:GameModes>`. Its AS→engine calls:
  - `Online.PlayPlaylist(id, forceHost)` (matchmaking);
  - `Online.EditGameMode(ConfigName)` → `SettingsDataStore.SetCurrentByName` + `GRI.PublishGameInfo(tag, settings)`;
  - **`Online.PlayPrivateGame(SettingsName)`** → `TnPartyLobbyGame.HostOnlineGame(settings)`;
  - `Online.EditPlaylist`, `Online.SetPartyLobbyType`.
- **Party lobby menu** (AS2, CONFIRMED). Root `mc_menuMultiplayer360 / PS3 / PC`; Back → `Game.QuitToMainMenu()`.

| button | action |
|---|---|
| `findGame_mc` | `mc_menuMultiplayerPlaylists` (public matchmaking) |
| **`hostGame_mc`** | `mc_menuMultiplayerGameModes` |
| `customCharacters_mc` | character customisation |
| `teletraan1_mc` | Teletraan-1 |
| `selectMatchmaking_mc` | region toggle |

  - **`mc_menuMultiplayerGameModes`** lists `<TnMenuItems:GameModes>` (FriendlyName, SettingsConfigName). These are the `TnDataProvider_GameModeInfo` sections in this order:
    - TDM "Team Deathmatch"
    - DM
    - DOM
    - CTF
    - EXT
    - KOTH

    (TransGame.int also names TnSVGame "Escalation" and an unshipped **TnOMFGame "One Must Fall"**, neither of which has a provider.)
  - **Focus change** → `Online.EditGameMode(SettingsConfigName)` (publishes the mode to `<CurrentGame:*>`) and shows `<CurrentGame:GameModeFriendlyDescription>`.
  - **Click** → **`mc_menuMultiplayerGameModeSettings`**. It builds one lateral selector per `TnGameSettings` data-store field that has a column header.
    - TDM rows: **Team Balancing** (Manual / Autobalanced), **Map Selection** (Rotate / Host's Choice), **Time Limit** (10 / 15 / 20 minutes), **Points to Win** (20 / 30 / 40 / 50).
    - Defaults come from `TnOnlineGameSettingsTDMPrivate`: Autobalanced, **Host's Choice**, 15 minutes, 40.
  - **`createGame_mc`** → `DataStores.WriteValue(field, choice)` for each row → **`Online.PlayPrivateGame(SettingsConfigName)`**.
  - `TnDataStore_GameSettings` maps the name to the **Private** class: DM→DMPrivate, TDM→TDMPrivate, CTF→CTFPrivate, KOTH→KOTHPrivate, DOM→DOMPrivate, SV→SVPrivate, EXT→EXTPrivate, CP→CPPrivate, SOLO→CPSolo, CCP→CCPPrivate.
  - In the Escalation / Campaign host menus, the privacy selector "Public" calls `Online.PlayPlaylist(id, true)` (host a public playlist game) instead.
- **Private (custom) path** — the one to mirror locally:
  1. `HostOnlineGameInternal(settings)`: `CheckCanPlayGameType` (party size ≤ `GetNumPlayersAllowedInParty`); `StartOnlineGame('Party')`; then `HostingGame`.
  2. `HostingGame`: destroy presence session; `CreateReservationHost(NumTeams = TeamType==GTS_TeamGame ? 2 : 1, MaxPlayers / NumTeams, MaxPlayers)`; `CreateOnlineGame`. **[online — bypass]**
  3. `OnCreateOnlineGameComplete`:
     - `TellPartyToJoinSession`;
     - `GameSettings.BuildLobbyURL(URL)`; `URL $= "?listen"`;
     - **`TnGame.static.ServerTravelToMap(URL, true, false)`**.
- **Public path:** `PlayPlaylistInternal`:
  - settings = `PlaylistManager.GetGameSettings(PlaylistId, 0)`;
  - HostType 1 → host;
  - otherwise build a search (`VERSUS`, `PlaylistId` property `0x10000023`) → `FindingGames` → join or `ReservingSpace.HostPlaylist`.

### 2.2 Playlists (TransPlaylists.ini, CONFIRMED)

`DefaultQuickmatchPlaylistId=1`. Each playlist has one `ConfiguredGames` entry, `ContentIds=(0)`.

| PlaylistId | Name | settings class | tag | VisibleInMenu |
|---|---|---|---|---|
| **1** | CivilWarPlaylist | TnOnlineGameSettings**TDMPublic** | TDM | true |
| 2 | DeathmatchPlaylist | DMPublic | DM | true |
| 7 | ConquestPlaylist | DOMPublic | DOM | true |
| 3 | CodeOfPowerPlaylist | CTFPublic | CTF | true |
| 5 | CountdownToExtinctionPlaylist | EXTPublic | EXT | true |
| 4 | PowerStrugglePlaylist | KOTHPublic | KOTH | true |
| 6 | SurvivalPlaylist | SVPublic | SV | false |
| 100 | CoopPlaylist | CPPublic | CP | false |
| 101 | CompetitiveCoopPlaylist | CCPPublic | CCP | false |

- Menu order = the order of the `TnDataProvider_OnlinePlaylist` sections: TDM, DM, DOM, CTF, EXT, KOTH, SV, CP, CCP. HIGH that the UI lists providers in section order.
- `TnOnlinePlaylistManager.PlaylistIdToGroupId(id) = id + 2000` (player counts; online).

### 2.3 Lobby URL (CONFIRMED script + data)
- `TnOnlineGameSettingsBase.BuildLobbyURL`:
  `LobbyMapName ?Game=LobbyGameClass ?GameModeTag=<tag> ?GameTeamStatus=<int TeamType> ?MaxPlayers=<Public+Private> ?IconicMode=<0|1>`
- For TDM: `UI_Lobby_m?Game=TransContent.TnGameLobbyGameTeam?GameModeTag=TDM?GameTeamStatus=3?MaxPlayers=10?IconicMode=0?listen`.
  - LobbyMapName comes from `[TransGame.TnOnlineGameSettingsBase]` (`UI_Lobby_m`). Survival and campaign settings override it with `UI_CampaignLobby_m`.

### 2.4 Game lobby (`UI_Lobby_m`, `TnGameLobbyGame` → `TnGameLobbyGameTeamBase` → `TnGameLobbyGameTeam`, CONFIRMED)
- Defaults: PC `TnPlayerControllerGameLobby`, GRI `TnGameReplicationInfoGameLobby`, PRI `TnPlayerReplicationInfoGameLobby`, `bDelayedStart`, `bTeamGame` (TeamBase), TeamHandler `TnTeamHandlerTwoTeamsLobby`, UIController `TnUIControllerGameLobby` → `UI_GFxLobbies_p.GameLobby_GFX_1`.
- `InitGame`: `NumRequiredPlayers = settings.NumRequiredPlayers` (TDM 4).
- `InitGameReplicationInfo`:
  - `AutostartCountdown = !IsPrivateGame()`;
  - `MapSelectionMethod` = setting `0x40000014` (**Public 0 = Rotate, Private 1 = Host's Choice**);
  - `AllowMapVeto = (method == 0)`; `VetoQuarum = NumRequired / 2 + 1` (public);
  - then `GRI.OnEnterLobbyFromMap(GRI.GetMapID())`.
- **Map selection:**
  - `OnEnterLobbyFromMap(MapId)`: if `MapId == -1 || MapSelectionMethod == 0 || campaign` → `ChooseNextMap(MapId)`; else `SetMapId(MapId)`, which keeps the previous map in host's-choice mode.
  - **`SelectRandomMap(prev)`:**
    - `GetCompatibleMaps()` = every `TnDataProvider_MapInfo` in `TnMenuItems:Maps` whose `CompatibleGameTypes` contains `GRI.GameModeTag`, skipping those where `IsProviderDisabled()`. Disabled = `!HasRequiredAssets()` (native) or `!GRI.MapCanBePlayed(map)` (playlist ContentIds must contain map `DlcId`; always true when `SelectedPlaylistID == -1`).
    - `RandomMap(cur, n)`: `cur == -1` → `RandRange(0, n)`; else `(cur + RandRange(1, n)) % n`. That is a uniformly random **different** compatible map; it is not sequential rotation.
  - **Host's choice (AS2 CONFIRMED, GameLobby_GFX versus menu):**
    - `selectMap_mc` is a lateral selector. Its items are every `<TnMenuItems:Maps>` row with `IsCollectionValueEnabled` **and** `CompatibleGameTypes` containing `<CurrentGame:MapCompatibilityTag>`, as `{FriendlyName, ImagePath, MapId}` in provider order. The list is rebuilt when MapCompatibilityTag changes.
    - It is enabled only for the host when `MapSelectionMethod == 1` and not counting down.
    - **Each selection change immediately calls `Online.SetSelectedMapID(MapId)`** → `TnGameLobbyGame.HostRequestMapID` → `GRI.HostRequestMapID` (ignored unless `MapSelectionMethod == 1`) → `SetMapId` → `UpdatePrestreaming()`.
    - `startGame_mc` (host && `CanHostRequestGameStart` && `!IsCountingDown`) → `Online.BeginLobbyExitCountdown()` → `HostRequestsGameStart`.
    - Selected-map panel (`updateSelectedMap` on `<CurrentGame:SelectedMapID>`): label `mc_mapLabelMultiplayer` (colour 0xFF9333, or 0xFF3333 if unavailable) and a thumbnail via `Self.SetExternalTextureWithPath('MapImage'+id, ImagePath)`; `UI_LevelThumbnails_p.LevelUnavailable` if disabled.
    - Faction logo only for faction maps (Survival).
  - **`UpdatePrestreaming()`** (non-campaign): `GameEngine.UpdateMapPrestreaming(ConvertMapIdToMapFilename(id))`, `WorldInfo.bHighPriorityLoading = true`. **The match map starts streaming while still in the lobby.**
  - Veto (public): `Online.SubmitMapVeto` → `MapVetos++`; `RequiredVetos = max(VetoQuarum, humans / 2 + 1)`.
- **Start:**
  - Public: `PendingMatch.Tick` → `AreGameAutoStartConditionsMet`:
    - `NumPlayers ≥ NumRequiredPlayers` (status 1, "waiting for N");
    - teams balanced (status 4);
    - then `CountingDown` (`BeginIntermissionCountdown` = **`LobbyIntermissionTime` 45 s**) → below **`LowCountdownTickThreshold` 10 s** (tick sound `BL_HUD_INTERFACE.CTF_ROUND_TIMER_01`) → `FinalCountdown`. Both values are CONFIRMED (Xe-TransGame.ini and authored defaults).
  - Private: `IsPrivateMatch` → `LobbyStatus 3` ("Waiting for host to start game"); the host presses start → `HostRequestsGameStart` → `CountdownRubicon = true`, **`BeginShortCountdown` = 10 s** → `FinalCountdown`.
  - `FinalCountdown.BeginState`: `AutobalanceTeams` → `TeamHandler.AssignTeams()`, else `ForceToTeam()`.
  - `ShouldStartGame` = `HasCountdownExpired() && !PC.IsJoiningASession()` → **`StartLevel()`**:
    ```
    GameSettings.BuildURL(MapURL)          // see 3.1
    LobbyGRI.ModifyURL(MapURL)             // MapURL = GetMapFilename() $ MapURL $ "?MapId=" $ GetMapID() [$ "?Checkpoint=" ...]
    TnGame.static.ServerTravelToMap(MapURL, true, false)
    ```
- `TnPlayerControllerGameLobby`: if `!TnDataStore_MenuItems.HasRequiredMapAssets(GRI.GetMapID())` → `ShowContentMissingMessageBox`.

---

## 3. Selection → gameplay data path (Phases 3, 4, 7)

### 3.1 Match URL (CONFIRMED script; HIGH for the native property appending)
`TnOnlineGameSettingsBase.BuildURL(OutURL)`:
```
AppendPropertiesToURL(OutURL)   // native; HIGH: appends "?<PropertyMappings.Name>=<value>" → ?PlaylistId=-1?GamerRegion=0?PointsToWin=40
AppendContextsToURL(OutURL)     // native; localized settings (GameMode, AutobalanceTeams, MapSelectionMethod, TimeLimit) – exact text PARTIAL
?Game=<GameClass>?GameModeTag=<tag>?GameTeamStatus=<TeamType int>?GameRules=<GetGameRules()>?MaxPlayers=<n>?StatsWriters=<..>?LobbyGameClassName=<LobbyGameClass>?IconicMode=<0|1>
[?TimeLimit=<TimeLimits[TimeLimit setting index]>]   // float → string
[?listen]   // if NumPublic+NumPrivate > 0
```
- `GetGameRules()` is the empty 7-byte body (`return ReturnValue`), so `?GameRules=` is empty. HIGH: same shape as `IsInFinalCountdown`'s default false, whose state override returns true.
- **Rules therefore come only from `GameInfo.InitGame` → `AllowGameRules()` → `AddGameRulesFromSettings(GetOnlineGameSettings())`.** That spawns each class in `settings.Rules` in order and chains them via `GameRulesModifiers.AddGameRules`, so the first entry is the head. CONFIRMED.
- **Rebuild note:** with no online session, `GetOnlineGameSettings()` is none and **no rules would be created**. The local bootstrap must supply the settings object (or the rule list) itself.

**Streets TDM, private, defaults** (assembled; the native-appended part is HIGH):
```
MP_IAC_Streets_Base_m?PlaylistId=-1?GamerRegion=0?PointsToWin=40?Game=TransContent.TnVersusGame?GameModeTag=TDM?GameTeamStatus=3?GameRules=?MaxPlayers=10?StatsWriters=?LobbyGameClassName=TransContent.TnGameLobbyGameTeam?IconicMode=0?TimeLimit=900.00?listen?MapId=508
```
- StatsWriters is empty only when `bIsLanMatch`; otherwise it carries the public writers.

### 3.2 Map catalog (CONFIRMED: TransLevels.ini `TnDataProvider_MapInfo` + TransGame.int FriendlyName + cooked package presence)

| MapId | MapFilename | FriendlyName | PresenceId | ImagePath | CompatibleGameTypes | in dump |
|---|---|---|---|---|---|---|
| 501 | MP_IAC_Seed_Base_m | Seed Of Corruption | 10 | UI_LevelThumbnails_p.MP_SeedOfCorruption | DM TDM CTF KOTH EXT DOM | yes |
| 502 | MP_IAC_Berth_Base_m | Berth | 11 | …MP_Berth | 6 modes | yes |
| 503 | MP_UND_Complex_BASE_m | Complex | 12 | …MP_Complex | 6 modes | yes |
| 504 | MP_IAC_Rust_BASE_m | Rust | 13 | …MP_Rust | 6 modes | yes |
| 505 | MP_ESC_BrokenHope_BASE_m | Broken Hope | 14 | …MP_Brokenhope | SV (Faction 0, Autobot campaign chars) | yes |
| 506 | MP_ESC_Remnant_BASE_m | Remnant | 15 | …MP_Remnant | SV (Faction 1) | yes |
| 507 | MP_ORB_Debris_BASE_m | Orbital Debris | 16 | …MP_Orbital | 6 modes | yes |
| **508** | **MP_IAC_Streets_Base_m** | **Streets** | **17** | **UI_LevelThumbnails_p.MP_Streets** | **DM TDM CTF KOTH EXT DOM** | **yes** |
| 509 | MP_KON_Molten_Base_m | Molten | 20 | …MP_Molten | 6 modes | yes |
| 510 | MP_UND_Gorge_BASE_m | Gorge | 18 | …MP_Gorge | 6 modes | yes |
| 512 | MP_KON_Fortress_BASE_m | Fortress | 21 | (none) | 6 modes | **no** (DLC) |
| 511 | MP_ORB_Havoc_BASE_m | Havoc | 22 | (none) | 6 modes | **no** (DLC) |
| 513 | MP_ESC_Tranquillity_BASE_m | Forsaken | 23 | (none) | SV | **no** (DLC) |

- `MP_KON_Sector_Base_m` "Sector" has a localization entry only: no provider section and no package.
- **Order** = section order above (HIGH: config per-object sections are enumerated in file order).
- **No per-map descriptions** exist (no Description key).
- **Loading art is not per map.** The loading screen is the shared Bink plus the LoadScreen_GFX text (3.3).
- Per-map game settings: none in the provider. Per-mode objects inside each map are filtered by mode (`MILESTONE04_STREETS_RUNTIME_SEMANTICS.md`).
- `HasRequiredAssets()` is native (2-byte stub). For the three DLC maps it is presumably false, so they are disabled and never chosen (HIGH).
- Lookups (`TnDataStore_MenuItems`, CONFIRMED): `ConvertMapIdToMapFilename / FriendlyName / PresenceId`, `GetMapFaction`, `HasRequiredMapAssets`. All are linear scans of the `Maps` providers.

### 3.3 Loading presentation (CONFIRMED script; PARTIAL native)
- **`TnGame.ServerTravelToMap(URL)`**:
  - `TnMoviePlayer.StartLoadingMovie(URL)`, then `WorldInfo.ServerTravel(URL, bAbsolute, bSkipGameNotify)`.
  - Clients use `ClientTravelToMap` (party-lobby entry, invite joins).
- **`StartLoadingMovie`** parses `Game`, `GameModeTag` and `MapId`:

| URL contains | call |
|---|---|
| `TnPartyLobbyGame` | `EnqueuePartyLobbyLoadingMovie` (empty title / message + 3 base engage texts) |
| `TnGameLobbyGame` | `EnqueueGameLobbyLoadingMovie` (same) |
| MapId ≠ −1 | **`EnqueueLoadingMapMovie(MapId, tag)`** |
| otherwise | generic |

- **`EnqueueLoadingMapMovie`**:
  - title = `TnOnlineGameSettings<tag>.default.FriendlyName` ("Team Deathmatch"), via `TnDataStore_GameSettings`;
  - message = `Repl(Localize("LoadScreen", "LoadingMap", "UIText") = "in `m", "`m", "Streets")` → **"in Streets"**;
  - `HmMoviePlayer.AddDeferredMethod("_global.SetLevelText", [title, message])`;
  - then **3×** `_global.AddEngageText(EngageText[RandomInt(len)])` from the mode's `EngageText` (TDM: 26 tips), with repeats possible.
- LoadScreen_GFX AS2: `SetLevelText` → `levelInfo_mc.UpdateLevelInfo(Title, Description)` (title upper-cased); `AddEngageText` pushes to `EngageTextArray`; a `setInterval` cycles `UpdateEngageText`. Text: `$UIText.LoadScreen.Loading` = "Loading".
- **Movie source:** the frontend Kismet sets `SetLoadingMovieFilename "UI_GFxLoading_p.LoadScreen_GFX"` (both at PreGameplaySetup and at frontend start). The native loading movie is the `[LoadingMovie] DefaultFileName=TF_LoadingScreen` Bink. PARTIAL: how the Bink and the GFx overlay are composited is native (`0x82CEB908` / `0x82CD3660`) and not traced.
- **Close:** `PlayerController.CanCloseLoadingMovie` (Engine script) gates it. The world is fully loaded before gameplay because of seamless travel through `TransitionMap=UI_FrontEnd_m` (`TnGame.bUseSeamlessTravel = true`). HIGH.
- **Prestreaming** started in the lobby (2.4) shortens the load.

---

## 4. Mode catalog (Phase 4; CONFIRMED authored defaults + ini + int)

All Public / Private pairs use **10** connections (Public = NumPublicConnections, Private = NumPrivateConnections), except SV 4 and CP / CCP 3. Private differs only in `MapSelectionMethod = 1` (host's choice) and `bUsesStats = false`.

| tag (ETnGameType) | FriendlyName | GameClass | LobbyGameClass | TeamType | Rules (head first) | score setting (default; choices) | time (default idx 1) |
|---|---|---|---|---|---|---|---|
| **TDM (2)** | Team Deathmatch | TransContent.TnVersusGame | TnGameLobbyGameTeam | GTS_TeamGame | ScoreKillsTDM, TrackKillsMP, ReportGameProgressTime, ReportGameProgressKills | PointsToWin **40**; 20/30/40/50 | 600/**900**/1200 s |
| DM (1) | Deathmatch | TnFreeForAllGame | TnGameLobbyGameFreeForAll | GTS_FreeForAllGame | ScoreKillsDM, TrackKillsMP, ReportGameProgressTime, ReportGameProgressKills | 20; 10/20/30 | 600/900/1200 |
| CTF (3) | Code of Power | TnVersusGame | TnGameLobbyGameTeam | GTS_TeamGame | ScoreKillsMP, SingleFlagCTF, ScoreFlags, TrackKillsMP, ReportGameProgressTimeCTF | Rounds 2; 2/4/6 | 240/300/360 |
| KOTH (4) | Power Struggle | TnVersusGame | TnGameLobbyGameTeam | GTS_TeamGame | ScoreKillsMP, ScoreKingOfTheHill, TrackKillsMP, ReportGameProgressTime, ReportGameProgressPoints | 400; 150–500 | 600/900/1200 |
| DOM (6) | Conquest | TnVersusGame | TnGameLobbyGameTeam | GTS_TeamGame | ScoreKillsMP, ScoreDomination, TrackKillsMP, ReportGameProgressTime, ReportGameProgressPoints | 400; 150–500 | **property** TimeLimit 900 (600/900/1200) |
| EXT (5) | Countdown to Extinction | TnVersusGame | TnGameLobbyGameTeam | GTS_TeamGame | ScoreKillsMP, ScoreBombingRun, TrackKillsMP, ReportGameProgressTime | 3; 1/3/5 | 600/900/1200 |
| SV | Escalation | TnSurvivalGame | TnGameLobbyGameSurvival | GTS_SingleTeamGame | CompetitiveScoring, TrackKills | — | — (iconic only, `UI_CampaignLobby_m`) |
| CP / CCP | Campaign | TnCoopGame | TnGameLobbyGameCoop | GTS_CampaignGame | ScoreKills, TrackKills / TrackKills, CompetitiveScoring | — | — |
| SOLO | Campaign (Solo Adventure) | TnCampaignGameSolo | TnGameLobbyGameSolo | — | — | — | — |

Notes on the table:
- RulesFormat strings (TransGame.int) use the tokens `` `p`` (PointsToWin `0x40000008`), `` `t`` (TimeLimit `0x40000007`) and `` `r`` (Rounds `0x40000006`). The tokens are replaced in `FormatedRules`. TDM: "Kill `p enemies from the other team to win."
- The mode → TNGT value comes from `TnGame.GetGameType()` = `GameRulesModifiers.GetGameType()`, walking the chain until a rule overrides it:

| rule | ETnGameType |
|---|---|
| ScoreKillsDM | 1 |
| ScoreKillsTDM | 2 |
| SingleFlagCTF | 3 |
| ScoreKingOfTheHill | 4 |
| ScoreBombingRun | 5 |
| ScoreDomination | 6 |

  The enum `TnGame.ETnGameType` = {NONE, DM, TDM, CTF, KOTH, EXT, DOM} was decoded from the TransGame package.
- TNGT is what objective actors and spawn clusters filter on (`ActiveGameTypes`, `FactionNeutralGameTypes`).
- **Game-mode HUD message classes** (`TnGameRules.BroadcastGameTypeMessage`, `EGameTypeMessageType` = {StartGame, GameNearlyComplete, EndGame}):

| mode | message class |
|---|---|
| TDM | TnGameTypeMessageTDM (FFA variant TnGameTypeMessageDM) |
| CTF | TnGameTypeMessageCTF |
| KOTH | TnGameTypeMessageKOTH |
| DOM | TnGameTypeMessageDOM |
| EXT | TnGameTypeMessageEXT |

- **Match start / end entry points:** shared by every versus mode (section 5): `TnMultiplayerGame.StartMatch` → `InProgress`; `EndGame` → `MatchOver`. Objective-mode specifics are in the earlier Streets notes. CTF / EXT round logic is in `TnGameRules_RoundsBase` (`SyncTimerTime 10`) and is not expanded here.

---

## 5. TDM lifecycle (Phase 5; CONFIRMED unless noted)

**Classes:** `TnGame` → `TnMultiplayerGame` → `TnTeamGame` → **`TnVersusGame`**.
- `TnVersusGame` defaults: TeamHandler `TnTeamHandlerTwoTeams`, `ForfeitDelay 1.5`.
- `TnMultiplayerGame` defaults:
  - `MatchAutoStartCountdown 10`, `MatchOverCountdown 15`, `bDelayedStart`, `MaxPlayersAllowed 10`;
  - DefaultPawnClass `TransContent.TnPlayerPawnMultiplayer`, PC `TnPlayerControllerMultiplayer`, GRI `TnGameReplicationInfoMultiplayer`;
  - RespawnHelper `TnRespawnHelperWave`, SpawnHelper `TnPlayerSpawnHelperMultiplayer`, `_SpawnPointManager` `TnSpawnPointManager`;
  - UIController `TnUIControllerMultiplayer`, `TransformerMarkerClass TnObjectiveMarkerTypeTransformerVersus`, `PresenceId 1`.
- `TnGame` defaults: HUDType `TransGame.TnHUD`, `bUseSeamlessTravel`, `bPauseable false`, `ApplySpecialtyBuffs`.

### 5.1 Initialization
1. **`TnMultiplayerGame.InitGame`:**
   - `GoalScore = max(0, GetIntOption("PointsToWin", GoalScore))`;
   - `_Rounds = max(0, GetIntOption("Rounds", _Rounds))`;
   - then **`TnGame.InitGame`**: `SpawnHelper.Initialize`, `RespawnHelper.Initialize`, `_SpawnPointManager.Initialize`.
   - That calls **`GameInfo.InitGame`**: MaxPlayers, `TimeLimit = max(0, GetIntOption("TimeLimit"))` in **seconds** (900 for TDM default), `?GameRules`, **`AddGameRulesFromSettings`**, StatsWriters.
2. **`TnGame.InitGameReplicationInfo`:**
   - `TeamHandler.Initialize`;
   - from the local URL: `GRI.SetGameTeamStatus(GameTeamStatus)`, `GRI.SetMapId(MapId)`;
   - `GRI.AutobalanceTeams` (setting `0x40000012`, default 1 = Autobalanced);
   - `GRI.SetPlaylistId`;
   - `GRI.PublishGameInfo(GameModeTag, settings)` feeds `<CurrentGame:GameModeFriendlyName / Rules / Tag>`.
3. **`TnMultiplayerGame.InitGameReplicationInfo`:** `GRI.GoalScore = GoalScore`, `GRI.RemainingTime = TimeLimit`, `GRI.Rounds`.
4. **`TnSpawnPointManager.Initialize`:**
   - `CurrentGameType = Game.GetGameType()` (TDM = 2);
   - register every `TnSpawnCluster` whose `ActiveGameTypes` is empty or contains it;
   - clusters with `InitialSpawn` become each faction's first active cluster (5.3).

### 5.2 Pre-match (`TnMultiplayerGame.PendingMatch`)
- `BeginState`:
  - `bWaitingToStartMatch = true`, `GRI.bMatchHasBegun = false`;
  - `GRI.SetGameStatus(2)`;
  - **`GRI.ResetCountdown(true, MatchAutoStartCountdown = 10)`**;
  - statistics session start.
- `TrySpawnPlayer` → false, so **no one spawns before the start**.
- `Tick`: `ReadyToStartMatch` = `GRI.HasCountdownExpired()` → `StartMatch()`.
- `GRI.ResetCountdown` sets a 1 s repeating `DecrementCountdown` timer. The value is `<CurrentGame:CurrentCountdown>` (PreGameCountdown_GFX).
- **Client UI during pre-match:**
  1. `TnUIControllerMultiplayer` starts in **WaitingOnGameStart**;
  2. `OpenGameStartUI` → **`InGameLobbyUI` = `UI_GFxCustomize_p.CustomTransformers_GFX_1`** (character select);
  3. on `OnCharacterSelected`, if the match hasn't begun: close it and open **`GameStartUI` = `UI_GFxPreGameCountdown_p.PreGameCountdown_GFX_1`**. That shows the mode icon (`mc_gameModeIconTDM`), `GameModeFriendlyName`, "`$UIText.Lobby.MultiplayerCountdownLabel`" and the countdown.
- `PlayerControllerMultiplayer.GameCountdownPostProcess` (ini): ActiveTime 6, RampIn 0.1, RampOut 3, Bloom Scale 5, DOF (FocusDistance 500, near / far falloff 400, kernel 26), full desaturation. PARTIAL: its trigger is not traced.

### 5.3 Teams and spawn
- **Teams:** the lobby's `FinalCountdown` already ran `AssignTeams()` (autobalanced) or `ForceToTeam()`.
  - Teams survive seamless travel: `TnTeamGame.HandleSeamlessTravelPlayer` → `TeamHandler.SetTeam(PRI.Team.TeamIndex, …)`.
  - Team 0 = Autobots, team 1 = Decepticons (`TnVersusGame.PickWinningTeam` uses `GetTeam(0)` as the Autobot team; `TnVersusGameOverMessage` Autobot / Decepticon win sounds).
  - **Team assignment** (`TransContent.TnTeamHandlerTwoTeams`, CONFIRMED):
    - `SpawnTeams` creates `Teams[0] = TnFactionTeamAutobots` and `Teams[1] = TnFactionTeamDecepticons`.
    - `AssignTeams` (autobalanced lobby) takes each human's team **from the online reservation** (`GetTeamIndexForPlayer`). With no reservation it logs "ERROR: Fail to assign team from reservation" and leaves the player unassigned. **[online — replace locally]**
    - `ForceToTeam` (manual) puts every human without a team through `PickTeam(255)`.
    - **`PickTeam`**: keep the current team if it is < 2; else the smaller team; **on a tie, `RandomInt(2)`**.
    - The local rebuild should use `PickTeam` for every player (HIGH as the faithful offline reduction).
- **`TnTeamGame.StartMatch`:**
  1. `Reset()` every Pawn, DroppedPickup and PickupFactory;
  2. `ForceGarbageCollection`;
  3. `GameInfo.StartMatch` (`TnMultiplayerGame.StartHumans` is empty);
  4. **`GotoState('InProgress')`**.
- **`InProgress.BeginState`:**
  - `ElapsedTime = 0`, `GRI.SetGameStatus(3)`, `GRI.ResetPlayerStats()`;
  - **`SendUIEventToControllers(3)`** (OnBeginGame);
  - weapon-stat sampling timer;
  - **`GRI.bStopCountDown = (GameRulesModifiers == none) ? true : !GameRulesModifiers.RunGameTimer()`**. `GameRules.RunGameTimer` defaults to true (chain), so the clock runs for TDM;
  - `SpawnHelper.Tick(0)`;
  - `GameRulesModifiers.HandleStartGame()` → `BroadcastGameTypeMessage(GTMT_StartGame)` (`TnGameTypeMessageTDM`).
- **Spawn pipeline** (`TnPlayerSpawnHelper.Tick`, per player, GameState 0 → 3; called each `TnGame.Tick`):
  1. `CheckReadySpawn` (MP: `PC.CanRestartPlayer()` and `PRI.HasSelectedCharacter()`);
  2. `FindSpawnPoint` (MP: `Game.FindInitialPlayerStart(PC) != none`);
  3. `TrySpawn` → `Game.TrySpawnPlayer(PC)` → InProgress: `PC.ClientStartSpectating()` + **`RespawnHelper.InitialSpawn(PC)`** → `NotifyPlayerAdded`.
  - `TnRespawnHelperDelayed.OnInitialSpawn`: if `WithinInitialSpawnWindow()` (Wave: `TimeToAllowInstantInitialSpawns = −1`, so **always**) → `Respawn(PC)` immediately (`Game.RestartPlayer`). Otherwise it queues like a death.
- **Spawn point** (`TnTeamGame.FindPlayerStart`):
  - `_SpawnPointManager.FindSpawnPoint(Player)`; falls back to stock `FindPlayerStart`, with `TnTeamGame.RatePlayerStart` returning −1 for non-`TnTeamPlayerStart` or wrong-team starts.
  - `FindSpawnPoint`: take the controller team's **active cluster**; up to `MaxSpawnPointsToConsider = 4` times, `NP = Cluster.GetSpawnPoint()` (**round-robin** `SpawnIterator` over the cluster's `SpawnPoints`) and reject it if `!LocationValidator.IsSafeSpawnLocation(NP.Location, radius, height)`; return the first safe one or none.
- **Active cluster** (`TnSpawnPointManager.UpdateClusters`, every `UpdateInterval = 0.1` s):
  - While `UsingInitialSpawn` and accumulated time < `InitialSpawnTime = 15` s, the initial clusters stay locked. `TimeSinceLastUpdate` isn't reset in this branch, so the lock lasts 15 s of game time.
  - Otherwise, for each faction, every cluster is scored. Clusters of the other faction are skipped **unless the game type is in `FactionNeutralGameTypes`** (class default **TDM, KOTH, DOM**), so in TDM both teams can use every cluster.
  - `ScoreCluster` = Σ over registered `TnSpawnModifierComponent`s of Σ rules `Factor × Score`, with:
    - `SRT_AffectFriend` counting only owners of the same team;
    - `SRT_AffectEnemy` only other teams;
    - `CutoffDistance` (−1 = none, else 0 beyond it);
    - `InverseDistance.Score = 1 / |cluster._CenterPoint − owner.Location|` (1 if 0).
  - Switch to the top cluster only if `DeltaTime == 0`, `TopScore − CurrentScore ≥ EarlyCutoffScoreDifference (5)`, or that faction's `Uptime ≥ ActiveClusterTime (10 s)`.
  - Modifiers (authored defaults):

| owner | rule | factor | cutoff |
|---|---|---|---|
| `TnPlayerPawn` | SpawnNearFriend (Friend) | +1 | — |
| `TnPlayerPawn` | SpawnAwayFromEnemy (Enemy) | −3 | — |
| `TnTombstone` (spawned at each player death, team set) | All | −5 | 5000 |
| `TnGameObjectiveWeaponPickupFactory` | All | −50 | 5000 |
| `TnKingOfTheHillZoneBase` | — | −50 | 5000 |
| `TnDominationPointBase` | Friend | +1 | — |
| `TnProjectileKamikazeMine` | Enemy | −50 | 2500 |

  - `TnPlayerPawnMultiplayer.SpawnModifierComponent0` inherits the TnPlayerPawn rules (HIGH, subobject archetype).
  - **Derived (HIGH):** 1/d with d in thousands of UU yields scores around 1e-3. So the 5-point early cutoff is practically unreachable, and **the active cluster re-evaluates every 10 s**, picking the best-scored cluster at that moment.
- **Streets TDM data** (authored): 12 `TnSpawnCluster`s (5 spawn points each, one with 4; 60 `TnTeamPlayerStart`, 30 Decepticon, 30 default team = Autobot):
  - 6 clusters are `ActiveGameTypes = [TNGT_TDM]` (13095, 2116, 3174 Decepticon; 4035, 8478, 9493 Autobot);
  - 6 are unrestricted;
  - `InitialSpawn`: **4159 (Decepticon, centre ≈ (38030, −32659, −70582))** and **7810 (Autobot, ≈ (10624, −65280, −71552))**;
  - all 12 register in TDM.
  - Cluster faction = team of its first spawn point.

### 5.4 Clock
- `GameReplicationInfo.Timer` (1 s × TimeDilation): `ElapsedTime++` while `MatchIsInProgress`; if `RemainingTime > 0 && !bStopCountDown`, `RemainingTime--` → `OnRemainingTimeUpdated()`.
- **`TnGameReplicationInfo.OnRemainingTimeUpdated`:** `ResetCountdown(true, RemainingTime)`, so **the HUD timer is `<CurrentGame:CurrentCountdown>`**. On the server, if `!bStopCountDown && RemainingTime <= 0` → **`Game.EndGame(none, "")`**.
- `TnGameRules_ReportGameProgressTime.Tick`: when `GRI.RemainingTime` equals 30 / 60 / 120 s → `TnGameProgressAnnouncementMessage` switch 0 / 1 / 2. The 60 s entry also calls `Game.NotifyGameNearlyComplete()` → `HandleGameNearlyComplete` → `BroadcastGameTypeMessage(GTMT_GameNearlyComplete)`. PARTIAL: Tick is per frame, so the match condition can fire on several frames within the same second.

### 5.5 Kills, deaths, score
`GameInfo.Killed(Killer, KilledPlayer, KilledPawn, DamageType)` runs in this order:
1. **`TnMultiplayerGame.Killed`**: stats `RecordKill`; if the victim is a `TnPlayerController`, `Spawn(TnTombstone, at KilledPawn.Location)` with `set_TeamNum(victim team)`.
2. **`TnGame.Killed`** → `GameInfo.Killed`:
   - `ScoreKill(Killer, Victim, DamageType)` → rule chain (below);
   - `Victim.PRI.AddDeaths(1)`;
   - death message;
   - **`CheckScore(Killer.PRI)`** if a killer exists;
   - discard inventory.
   - Then `RespawnHelper.Died(Victim)` (if the victim was a `TnPlayerPawn`) and kill achievements.
3. **The rule chain for a TDM kill:**
   - **ScoreKillsTDM** (`ScoreKills.ScoreKill`):
     - if `DamageType != DmgType_Suicided`, Killer and Killer.PRI exist, and `ShouldScoreKill(Killed)` (MP: `Killed == none || Killed is TnPlayerController`):
     - `Killer.PRI.AddScore(KilledSelf ? 0 : 1, KilledSelf ? 0 : TeamScoreAmount = 1)`.
     - `PlayerReplicationInfo.AddScore`: `Score += Amount`; if `TeamAmount > 0 && Team` → **`Team.AddScore(1)`**. `TnPRI.AddScore` also increments game stat `0x10000009`.
   - **TrackKillsMP**:
     - `ShouldScoreKill` = victim is a `TnPlayerController`;
     - `Score = (Killer == Killed) ? −1 : +1`;
     - if +1: `TnPRI.AddKills(1, DamageType, Killed)` + `CheckKills` (kill-streak announcer, 27 kill-award rules) when XP events are shown;
     - always `ScoreAssists`: the first damager in the victim's `DamageHistory.Aggregate()` that is neither killer nor victim gets `AddAssist(damage / victim.HealthMax)`.
   - **ReportGameProgressTime**: (tick only).
   - **ReportGameProgressKills.ScoreKill** → `HandleProgress(Killer.PRI)`: `NumScoresLeft = GoalScore − TeamScore`. At 1 / 3 / 5 left → announcement switch 5 / 6 / 7; 5 left also calls `NotifyGameNearlyComplete`.
4. **CheckScore** (`TnMultiplayerGame`): `CurrentScore = GetCurrentScore(PRI)` (`TnTeamGame`: **`PRI.Team.GetScore()`**). `ReachedGoalScore = GoalScore > 0 && score ≥ GoalScore` → **`EndGame(PRI, "Score")`**.

- **Suicide:** `DmgType_Suicided` or `Killer == Killed` gives no score, no kill, no team point. TrackKills computes −1 but subtracts nothing. The death still counts (`AddDeaths`).
- **Environmental death** (Killer none): no score; death counts; CheckScore isn't called.
- **Team kills:** `TnPlayerPawn.TakeDamage` **discards all teammate damage except `TnDamageTypeAOE`** (and own spawned sentries' damage). It calls `Controller.NotifyHitByFriendlyFire` instead.
  - If a teammate AOE kill does happen, ScoreKills would award +1 to the killer and their team. **No team-kill penalty exists in the TDM rules** (CONFIRMED by absence in ScoreKills / TrackKills; the outcome is HIGH).
- **Downed state:** `TnMultiplayerGame.AllowDowned(P) = P.HasSkill(TnSkillCanBeDowned)`. While downed with `_DownedInvulnerableCountdown > 0`, damage other than `TnDamageTypeDownedDrain` is zeroed.

### 5.6 Respawn (`TnRespawnHelperWave` : Delayed; `WaveRespawnTime 5.0`)
- `Died` → `OnDeath(C)`: unless the team's `_AllowRespawn` is false → `Add(C)` with `TimeToRespawn = GetTimeToRespawn(C)`:
  - **0 if `PC.ShouldInstantRespawn()`**, else **5.0 s**;
  - `PRI.SetTimeToRespawn(t)` drives the MultiplayerRespawn_GFX `<PlayerOwner:TimeToRespawn>`.
- `OnTick`: each pending entry `TimeToRespawn −= dt`, and the PRI is updated. At ≤ 0 → `Respawn(C)` = `Game.RestartPlayer(C)`. `TnMultiplayerGame.RestartPlayer` sets the voice channel and stats, then runs stock RestartPlayer → `FindPlayerStart` (5.3).
- "Wave" is **per-player** here: there is no shared wave clock in this class.
- `[TransGame.TnPlayerController] PlayerRestartDelay=6.0` exists in config. PARTIAL: whether it gates `CanRestartPlayer` was not traced.
- **Death UI:** the PC enters `PlayerWaitingSpectating` / `PlayerSpectating` → `OnUIEvent(4)` (OnSpectating) → UI state Spectating: HUD visible + **`SpectatingUI` = `UI_GFxRespawn_p.MultiplayerRespawn_GFX_1`**. On leaving → `OnUIEvent(5)` (OnRespawn) → InGame.

### 5.7 End of match
- **Triggers:** score limit (`CheckScore` → `EndGame(PRI, "Score")`), clock (`EndGame(none, "")`), or forfeit.
  - Forfeit: `TnVersusGame.Logout` → after `ForfeitDelay 1.5` s, `InProgress.CheckForfeit` → if a team has 0 players: `ClearScore()` on it, `EndGame(none, "Forfeit")`.
- **`TnGame.EndGame`:** reset voice muting; `HandleGameCompletionStats`; `GameInfo.EndGame(Winner ?? GetWinningPRI(), Reason)`. Stock GameInfo.EndGame calls `CheckEndGame`.
- **`TnVersusGame.CheckEndGame`:**
  - `WinningTeam = PickWinningTeam()`:
    - Autobots if `A.Score > D.Score || D.Size == 0`;
    - Decepticons if `D.Score > A.Score || A.Size == 0`;
    - **else none (a tie)**.
  - `GRI.Winner = WinningTeam`; `BroadcastWin`:
    - `TnVersusGameOverMessage` switch 1 if Winner none (Tie game);
    - switch 2 if a team is empty (forfeit);
    - otherwise 0 (win);
    - win sounds `MP_GameAutobotWin` / `MP_GameDecepticonWin`; texts "Your team won" / "Your team lost" / "Enemy team forfeits" / "Tie game".
  - XP events: controllers with `PRI.Team == Winner.Team` get `TnXpEventTypeGameWin`, others `TnXpEventTypeGameLose`.
- **No overtime exists** (CONFIRMED: no overtime state; on timeout with equal scores the result is a tie).
- `TnMultiplayerGame.EndGame` then:
  - `RecordSessionComplete`;
  - **`GameRulesModifiers.HandleEndGame(Winner)`** → `BroadcastGameTypeMessage(GTMT_EndGame)`;
  - **`GotoState('MatchOver')`**.
- **`MatchOver.BeginState`:**
  - `AwardMVPAchievement` (top PRI score; Versus requires both teams non-empty);
  - **`GRI.SetGameStatus(5)`**;
  - **`SendUIEventToControllers(9)`** (OnEndGame): UI state GameEnded: HUD hidden, **`EndGameUI` = `UI_GFxEndGameStats_p.EndGameStats_GFX_1`**;
  - write stats;
  - **`SetTimer(MatchOverCountdown = 15 s, 'OnCountdownComplete')`**.
- In MatchOver, `ScoreKill`, `ScoreObjective` and `EndGame` are no-ops and `TnTeamGame.MatchOver.RestartPlayer` is empty.
- **EndGameStats_GFX:**
  - title `<CurrentGame:GameOverMessage>`; `$UIText.EndGameStats.FinalScores`;
  - two views toggled by X: **scoreboard** (the loaded `PlayerList.swf`, ViewMode InGame) and **XP earnings** per specialty (Scout / Scientist / Leader / Soldier, `Customize.GetXpEarnedForSpecialtyLastMatch` …);
  - the first view is the scoreboard if `<CurrentGame:_bIconicMode>`, otherwise earnings;
  - B → `closeEndGameStats`, which only does something when the movie was opened with a `parentMenu` (the lobby's `_global.showXpScreen`). **In the match the screen stays until the ReturnToGameLobby travel** (AS2 CONFIRMED).
- **Return:** `MatchOver.OnCountdownComplete` → **`TnGame.ReturnToGameLobby()`**: `settings.BuildLobbyURL(URL)`; `WorldInfo.ServerTravel(URL $ "?MapId=" $ GRI.GetMapID(), true)`.
  - Back in `UI_Lobby_m`, `OnEnterLobbyFromMap(prevMapId)`: **Rotate → a random different compatible map**; **host's choice → the same map preselected**. Then the next countdown.
  - `UIController` OnPlayAgain (10) → WaitingOnGameStart exists for the in-place path. PARTIAL: its sender was not found.
- **Quit:** `OnQuitGame` → `RecordSessionComplete("Quit")` → `MatchQuit`.
  - `Game.QuitToMainMenu` (Pause / GameLobby AS) → TnGameActionScriptBinding → … → `TnGame` line 661: **`ClientTravelToMap("UI_FrontEnd_m")`**.
  - `ClientReturnToParty` / `QuitToPartyLobby` → party lobby.

### 5.8 Map restart in place
`TnGame.RestartRound` = `SoftReset()` + `SendUIEventToControllers(3)` + `SpawnHelper.RestartingMatch()` (every player back to spawn state 0). It is used by round modes, not by TDM (HIGH).

---

## 6. HUD connection (Phase 6)

- **Class:** `TnGame.HUDType = TransGame.TnHUD` (super `HM_Engine.HmHUD`).
- **Movies:** `DefaultHudMovie = HudMovie = UI_GFxHud_p.Hud_GFX_1`; `ScoreboardMovie = UI_GFxInGameStats_p.InGameStats_GFX_1`. `HudVisible` and `ToggleHudFlag` default to true.
- **Activation:** UI state InGame → `SetHudVisible(true)` (unless hiding); Spectating also keeps the HUD visible; GameEnded hides it.
  - Events 12 / 13 hide / show it (`TnPlayerController` cinematic mode, ToggleHUD).
- **Engine → AS (push)**, from `TnHUD` defaults and data observers (full list in `notes/data/frontend_gfx_callbacks.json` → `engine_to_as`):

| callback | data |
|---|---|
| `_global.NotifySegmentedHealthChanged` | health |
| `_global.NotifyOverShieldChanged` | overshield |
| `NotifyWeaponClipAmmoChanged` / `NotifyWeaponReserveAmmoChanged` / `NotifyGrenadeAmmoChanged` / `NotifyActiveGrenadeCount` / `NotifyAmmoAdded` | ammo |
| `NotifyWeaponReticuleTypeChanged`, `NotifyWeaponSpreadChanged`, `NotifyLockOnStateChanged`, `NotifyTargetTypeChanged` | crosshair |
| `NotifyPrimary / Secondary / MeleeWeaponChanged`, `NotifyCurrentWeaponChanged`, `NotifyFineAimChanged`, `NotifyWeaponJammedChanged`, `NotifyHeatChanged`, `NotifyNormalizedHeatChanged` | weapons |
| `NotifyAbilityType0/1/2Changed`, `UpdateAbilityCooldown`, `SetAbility` | abilities |
| `NotifyCurrentFormChanged`, `NotifyCantTransform` | form |
| `NotifyDamageIndicatorAdded`, `NotifyPlayerRotationChanged`, `CausedDamage` | damage indicators |
| `ApplyBuff`, `ReapplyBuff`, `UnapplyBuff`, `NotifyDamageIncrease`, `NotifyHudScrambledChanged` | buffs |
| `NotifyKillstreakChanged`, `PointEvent` (XP transactions), `RewardAnnouncement`, `GameAnnouncement`, `GameMessage`, `NotifyLevelUp` | kill feed / awards |
| `AddObjective`, `CompleteObjective`, `StartMarkerUpdate`, `UpdateMarker`, `FinishMarkerUpdate` | objective markers |
| `NotifySpectating`, `NotifyFirstSpawn`, `NotifyContextualCommand`, `NotifyNormalizedDownedHealthChanged`, `NotifyProgressBarChanged`, `UpdatePlayerListData`, `NotifyBadConnection`, `WaveformData`, `NotifyTutorialMessage` | misc |

- **AS ← data stores (pull and subscribe):** Hud_GFX reads and registers:
  - `<CurrentGame:CurrentCountdown>` (**match timer**), `<CurrentGame:IsCountingDown>`;
  - `<CurrentGame:GoalScore>`, `<CurrentGame:Teams>` (**team scores**), `<CurrentGame:Players>`;
  - `<PlayerOwner:Score>` (**personal score**), `<PlayerOwner:TeamID>`, `<PlayerOwner:PlayerName>`;
  - `<CurrentGame:GameTeamStatus>`, `<CurrentGame:Rounds>`, `<CurrentGame:CurrentRound>`, `<CurrentGame:CurrentObjectiveCountdown>`, `<CurrentGame:CompetitiveScoreEnabled>`, `<CurrentGame:_CurrentWave>`, `<CurrentGame:_NextWaveTime>`, `<TnMenuItems:Weapons>`.
- **HUD score and clock widgets** (Hud_GFX AS2, CONFIRMED):
  - **Scoreboard widget choice** (`UpdateScoreboardDisplay`, re-run on `<CurrentGame:GameTeamStatus>` / `CompetitiveScoreEnabled` change):

| GameTeamStatus | widget |
|---|---|
| `GTS_TeamGame` | **`mc_scoreTeam`** |
| `GTS_FreeForAllGame` | `mc_scoreFreeForAll` |
| `GTS_SingleTeamGame` | `mc_scoreSurvival` |
| otherwise, if CompetitiveScoreEnabled | `mc_scoreCoop` |

    With a scoreboard present, the countdown clip sits at y = 50 (otherwise 10).
  - **`mc_scoreTeam`** (sprite 499) **polls every 500 ms** (`setInterval UpdateTeamScores 500`); it does not use callbacks.
    - `GoalScore = <CurrentGame:GoalScore>` (if ≤ 0 it uses 10); `TeamID = <PlayerOwner:TeamID>`.
    - On team change it attaches `mc_scoreLogoAutobot` (team 0) or `mc_scoreLogoDecepticon` (team 1). Ally colour 0xF03C3C and enemy 0xA06FFF for Autobots, swapped for Decepticons.
    - For each `<CurrentGame:Teams>` row (TeamIndex 0 / 1, Score): the own team goes to `allyNumber_mc` / `allyBar_mc`, the other to the enemy widgets.
    - On a score change: set the number text, flash the bar white → team colour (0.5 s), and animate the bar width to `25 + Score / GoalScore × 141` px (minimum 25) over 0.2 s.
  - **Round / match clock** (`UpdateRoundCountdown` on `<CurrentGame:CurrentCountdown>`, `ShowRoundCountdown` on `<CurrentGame:IsCountingDown>`):
    - visible while `IsCountingDown && time > 0`;
    - text `secondsToMinutesSeconds(t, true)` = `MM:SS` (zero-padded minutes and seconds);
    - at ≤ 10 s each update flashes 0xFF3333 → 0x50B5D5 with a shadow pulse.
    - During the match `GRI.OnRemainingTimeUpdated` re-arms `ResetCountdown(true, RemainingTime)` every second, so this is the TDM match clock. In PendingMatch the same widget shows the 10 s start countdown.
    - An objective clock (`<CurrentGame:CurrentObjectiveCountdown>`, `M:SS`) is used by objective modes.
  - Personal score `<PlayerOwner:Score>` and `<CurrentGame:Players>` (Score, TeamID, PlayerName) feed the FFA widget and the player-list blocks.
- **Scoreboard** (InGameStats_GFX): `GameModeFriendlyName`, `GameModeFriendlyRules`, `SelectedMapID` + `<TnMenuItems:Maps>`. The player rows come from the `PlayerList.swf` component. PARTIAL: its open/close input binding was not traced.
- **Pause:** `TnPlayerController.ShowMenu` → `OnUIEvent(6)` → Paused: `SetPause(true)` + `PauseUI = UI_GFxPause_p.PauseMenu_GFX_1`. `TnGame.SetPause` also sends 6.
  - `bPauseable = false` for TnGame, so the world doesn't pause in MP (HIGH).
  - The pause menu uses `Online.SwitchTeam`, `Game.QuitToMainMenu`, invites, settings.
- **Results:** EndGameStats_GFX (5.7). The kill/death columns come from PRI data (PlayerList).
- **Other in-game movies:**

| movie | role |
|---|---|
| `UI_GFxShared_p.MessagePrompt_GFX_1` | message box |
| `UI_GFxOnlineNotifies_p.OnlineNotify_GFX_1` | `_global.DisplayMessage` notifications |
| `UI_GFxShared_p.TextPrompt_GFX_1` | text prompt |
| `UI_GFxMouseCursor_p.Cursor_GFX_1` | mouse cursor |

---

## 7. Loading / return timeline (Phase 7)

```
[FrontEnd UI_FrontEnd_m, TnFrontEndGame, UI state FrontEnd, FrontEnd_GFX]
  Multiplayer → OpenPartyLobby(GTS_TeamGame) → ClientTravelToMap("UI_PartyLobby_m?game=TransContent.TnPartyLobbyGame?listen")
      loading: StartLoadingMovie → EnqueuePartyLobbyLoadingMovie (no map text)
[UI_PartyLobby_m, TnPartyLobbyGame, TnUIControllerPartyLobby (StartingState InLobby) → PartyLobby_GFX]
  choose mode (EditGameMode / playlist) → PlayPrivateGame(settings) → HostingGame … → ServerTravelToMap("UI_Lobby_m?Game=TransContent.TnGameLobbyGameTeam?GameModeTag=TDM?GameTeamStatus=3?MaxPlayers=10?IconicMode=0?listen")
[UI_Lobby_m, TnGameLobbyGameTeam, TnUIControllerGameLobby (InLobby) → GameLobby_GFX]
  map list = <TnMenuItems:Maps> filtered by MapCompatibilityTag; host SetSelectedMapID(508) → prestream MP_IAC_Streets_Base_m
  host start → short countdown → FinalCountdown (teams assigned) → StartLevel → ServerTravelToMap(match URL 3.1)
      loading: Bink TF_LoadingScreen + LoadScreen_GFX: "TEAM DEATHMATCH" / "in Streets" + 3 random TDM tips
[MP_IAC_Streets_Base_m, TnVersusGame]
  InitGame (rules, GoalScore 40, TimeLimit 900) → InitGameReplicationInfo → PostLogin/HandleSeamlessTravelPlayer (teams kept)
  client: GRI PostBeginPlay → OnUIEvent(15); UpdateUiController → TnUIControllerMultiplayer (WaitingOnGameStart)
  PendingMatch: 10 s countdown; CustomTransformers (character select) → PreGameCountdown
  StartMatch → InProgress → UI event 3 → InGame → Hud_GFX; spawns via SpawnHelper → RespawnHelper.InitialSpawn → RestartPlayer
  … kills / respawn (5 s) …
  EndGame → MatchOver → UI event 9 → EndGameStats_GFX; 15 s → ReturnToGameLobby → UI_Lobby_m?…?MapId=508
```

- **Frontend / HUD destruction:** every travel replaces the world and its PlayerController. The UIController is created per PC (`InitializeUIController`). PARTIAL: Scaleform movie teardown on travel is native.
- **Player / controller creation:** seamless travel keeps controllers. `HandleSeamlessTravelPlayer` → team restore; `SpawnHelper.SeamlessTravel` inserts the player at spawn state 0.
- **Audio transitions:** the frontend Kismet starts music, reverb `REVERB_TRANS_FRONT_END` and ambience. In the match, per-map audio packages are loaded (`MP_IAC_Streets_AUDIO_m`). `MovieMixerPreset=CINE_MUTE_FOR_BINK` mutes the game mix during Bink. UNKNOWN: the exact crossfade points.
- **Input ownership:**
  - The frontend assigns the controller (`AssignControllerToLocalPlayer`). Each GFx menu takes input through `_root.inputHandler.giveInput(menu)`.
  - In game, input goes to the pawn when no UI is open. PARTIAL: GFx focus capture is native.

---

## HANDOFFS

### Frontend implementation
- **CONFIRMED:**
  - **Boot:** load `UI_FrontEnd_m`; Kismet order in 1.2 (logos only until the intro has been watched).
  - **UI state machine:** `TnUIController` and its subclasses (1.4).
  - **Main menu buttons** and their exact AS→engine calls (1.5).
  - `OpenPartyLobby(GTS_TeamGame)` → party lobby → PlayPrivateGame / EditGameMode → game lobby → `SetSelectedMapID` → host start.
  - **Data bindings per movie:** `notes/data/frontend_gfx_callbacks.json` (`as_to_engine`, `localized_and_datastore_strings`).
  - Loading text: `SetLevelText(FriendlyName, "in <Map>")` + 3 random `AddEngageText`.
- **HIGH:** playlist and map menu order = ini section order.
- **CONFIRMED (AS2):** menu graph and enable rules in `notes/data/frontend_menu_graph.json`. Full disassembly can be regenerated with `tools/as2dis.py <movie.gfx>`.
- **PARTIAL:** the Bink + GFx composite of the loading screen.

### Gameplay / TDM
- **CONFIRMED:**
  - settings → URL → InitGame (sections 3.1, 5.1);
  - PendingMatch 10 s → InProgress (5.2–5.3);
  - spawn clusters and modifiers with exact constants (5.3);
  - clock end (5.4);
  - kill / score / assist / suicide rules (5.5);
  - 5 s respawn (5.6);
  - score 40 / time 900 s end, tie = no winner, forfeit, MatchOver 15 s → lobby (5.7).
  - The bootstrap **must create the TDM settings/rules itself**, because `GetOnlineGameSettings()` is none without a session.
- **HIGH:**
  - the cluster switch is effectively every 10 s;
  - teammate AOE kills score.
- **PARTIAL:**
  - `PlayerRestartDelay`;
  - `IsSafeSpawnLocation` (native validator).

### Rendering
- No new items. The loading screen is Bink (`TF_LoadingScreen_INT.bik`) with the `LoadScreen_GFX` overlay.
- The frontend scene uses `ENV_NEU_CybertronLow_P.CybertronSky_PostProcess_PP` (`SeqAct_SetPostProcessChain`) and Energon material params (1.2).

### Systems
- Audio cues:

| cue | source |
|---|---|
| frontend ambience | `BL_LVL_HUD_INTERFACE.FRONTEND_AMB_ORBIT_01/02_BED_LP`, PP_SPACE_IACON / KAON positional loops, `FRONTEND_WHSH_*` |
| announcer | `TnGameProgressAnnouncementMessage` switches 0–7 (time 30 / 60 / 120 s; kills 1 / 3 / 5 left), `TnGameTypeMessageTDM` Start / NearlyComplete / End |
| win sounds | `SoundEvents_Dialog.Announcer.MP_GameAutobotWin` / `MP_GameDecepticonWin` |
| countdown tick | `BL_HUD_INTERFACE.EXTINCTION_ROUND_TIMER_01` (objective countdown ≤ 5) |

### AssetTools
- New read-only tools: `tools/gfxpool.py` (AS2 constant pools) and `tools/gfxcallgraph.py` (callback table). Suggest manifesting the GFx data-store bindings per movie.
- Map catalog: section 3.2. DLC maps 511–513 have providers but no packages.

### Integration
- The original has **no offline MP**. Mirror the private-match path with the session steps removed:
  1. FrontEnd →
  2. (party lobby: mode pick) →
  3. game lobby (host's-choice map, `MapSelectionMethod 1`) →
  4. `StartLevel` URL →
  5. match →
  6. `ReturnToGameLobby`.
- The URL keys `PointsToWin`, `TimeLimit`, `GameModeTag`, `GameTeamStatus` and `MapId` are what the match reads.

## STILL OPEN
- HUD AS2 internals (Hud_GFX) were not walked button by button; the bindings are listed.
- Native loading-movie composition and close timing.
- `PlayerRestartDelay` usage.
