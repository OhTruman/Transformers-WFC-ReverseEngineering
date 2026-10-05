# Targeted pass 3 (2026-10-05): character → pawn, preview camera, transform collision, modes, Bink language, title scene, PC settings

**Labels:**
- **C** = CONFIRMED (bytecode / native / authored data read directly).
- **H** = HIGH CONFIDENCE.
- **P** = PARTIAL.
- **U** = UNKNOWN.

**Owners:** GP Gameplay · FE Frontend · RN Rendering · SY Systems · AT AssetTools.

**Sources:**
- Script: `work/script/decomp/*` (TransGame / Engine).
- TransContent classes cooked into maps: `work/q/streets_base_gameclasses.txt`.
- Authored data: `authored.db`.
- Shipped config: `ExtractedAssets/config/Coalesced_ini/.../Xenon/Cooked`.
- Native code: Ghidra snapshot, read-only.

---

## A. Multiplayer character selection → spawned pawn (GP / FE / AT)

### A1. Runtime chain (C)

| Step | Where | What happens |
|---|---|---|
| 1. Pick | `TnPlayerController.SelectCharacter(name, type)`: 0 = custom (`FindCustomCharacter`), 1 = iconic (`FindIconicCharacter`) | → `TnCharacterDataHelpers.ReplicateCharacterData` → `SetCharacterData` → `ServerSetCharacterData` → `PRI.SelectCharacter` → **`PRI._SelectedCharacter`** (a *compressed* `CharacterData` with string IDs) |
| 2. Spawn gate | `TnPlayerSpawnHelperMultiplayer.CheckReadySpawn` | requires `PC.CanRestartPlayer()` **and `PRI.HasSelectedCharacter()`** (`_SelectedCharacter.CharacterName != ""`). Until then: no pawn. `TnPlayerControllerMultiplayer.CanBeKicked` returns true when the match has begun and no character is picked |
| 3. Faction | `TnGame.GetResolvedCharacterFaction(A) = A.GetTeamNum()`; `TnFreeForAllGame` override returns **1** (Decepticon) | 0 = Autobot, 1 = Decepticon |
| 4. Resolve | `TnCharacterDataHelpers.ResolveReplicatedCharacterData(CDIn, Faction)` | finds **Index = position of Faction in `CDIn.Factions[]`** and takes `ChassisTypes[Index]`, `PrimaryColors[Index]`, `SecondaryColors[Index]`, `MeleeWeapons[Index]`. If the faction is not in the list, it logs "ERROR: Could not resolve replicated character" and **returns an empty CharacterData** (no chassis) |
| 5. Chassis ID → asset | same function | `_CustomCharacterOptions.FindChassis(id)`: `GetChassisObjectPath(id)` (the `TnDataProvider_Chassis` UniqueId → ObjectPath in `TransCustomization.ini`) → `FindObject(path, TnTransformer)`. Fallback: `FindObject(id, TnTransformer)` (the ID used as a full path). If both fail: log "Could not find Chassis…", `ChassisType = none` |
| 6. Spawn | `TnGame.SpawnDefaultPawnFor` | `Spawn(DefaultPlayerClass, , , StartSpot.Location, (0, StartSpot.Yaw, 0), , , Character.ChassisType)`. **The 8th Spawn argument is the HM "actor blueprint"**; native code stores it in `Actor._ActorBlueprint` before PostBeginPlay. `DefaultPawnClass` = `TransContent.TnPlayerPawnMultiplayer` |
| 7. Body | `TnPawn.PostBeginPlay` | `ChassisType = TnTransformer(_ActorBlueprint)`. If it is set: `_Blueprint = ChassisType` and `ApplyTransformer()` |
| 8. Forms / stats | `TnPawn.ApplyTransformer` | `CreateRobotForm(_Blueprint)` (robot skeletal mesh, AnimTree, AnimSets from the TnTransformer), `CreateVehicleForm(_Blueprint.TransformerVehicle)`, `InitializeTransformations`, collision size, `BaseEyeHeight`, Mass, AccelRate, ground/air speed, jump height (acrobatics blueprint), Health, regen, damage multiplier, hit effects. `TnPlayerPawn` adds `InitializeSegmentedHealth(_Blueprint.SegmentedHealth)` |
| 9. Loadout | `TransContent.TnMultiplayerGame.SetPlayerDefaults` (called by `GameInfo.RestartPlayer` after Possess) | re-resolves the selected character for the pawn's team, **forces `StartingForm = 0` (robot)**, then `TnPawn.ApplyCharacter(CD)` |
| 10. Apply | `TnPawn.ApplyCharacter` → `TnCharacterApplier.ApplyCharacter` | sound set, `InitializeState`, colours (below), opacity, **abilities** (Role ≥ 2), `ApplySpecialty` (Scout / Scientist / Soldier / Leader → `TnSpecialty*`.Apply), `PRI.CurrentCharacter`. Authority: **skills, weapons** (`ApplyWeapons`), class tracker. Simulated proxies: melee weapon only. It also sets `_CurrentCharacterCompressed`, which replicates |
| 11. Clients | `TnPawn.ReplicatedEvent('_CurrentCharacterCompressed')` | resolves the struct again (no faction argument; the compressed copy holds one entry) → `ApplyCharacter` on every client |
| 12. Local player | `TnPlayerPawn.ApplyCharacter` | texture loader (`_CharacterTextureLoader.UpdateTransformer(_Blueprint)`), health-ramp meshes, `PC.SetCamerasTemplate(_Blueprint.Cameras, StartingForm)`, `PC.GotoNewFormState(StartingForm)` |

**So the body is determined only by (selected character's `ChassisTypes[]`, team).** The chassis ID strings (`Truck3`, `Car2`, …) are the runtime identity. The resolved `TnTransformer` object path is replicated as `ChassisTypes[0]` in the compressed struct (`ReplicateResolvedCharacterData`, using `GetChassisTypeFromObjectPath`).

### A2. Defaults (C)

- **Every new custom slot is a copy of the specialty preset.** `TnCharacterCustomizationData.GetDefaultCharacter`: DefaultScout / DefaultScientist / DefaultSoldier / DefaultLeader = `TR_MPPlayerCharacterData_p.{Scout,Scientist,Soldier,Leader}_PCD_MP`.
- `ResetCharacterFromName` names the slot `<Specialty><n>` (e.g. `Leader1`) and randomises the **colour palette indices and coordinates**:
  - Autobot palette = `RandomInt(5)`;
  - Decepticon palette = `5 + RandomInt(5)`;
  - coordinates are random in 0–254.
- Slot counts: 1, plus one at level 5 and one at level 10.
- **Preset arrays** (`Leader_PCD_MP`): `Factions = [kFactionAutobot, kFactionDecepticon]`, `ChassisTypes = [Truck3, Truck4]`, `MeleeWeapons = [Axe, ViciousAxe]`.
  - Primary and secondary colours are both `(0, 0, 0, 255)`, which equals `kUseDefaultColor`: `TnCharacterApplier.ExtractColors` then reads the **material's own default parameter** (keeps the chassis paint).
  - Scientist = Jet4 / Jet, Scout = Car2 / Car4, Soldier = Tank3 / Tank2 (earlier note §7).
- **The Autobot / Decepticon pairing is authored per character** (parallel arrays), not derived from the chassis. Any faction a character lacks fails resolution.

### A3. Failure behaviour (C)

| Failure | Result |
|---|---|
| No character selected | player is not spawned (stays spectating / selection UI); kickable after the match begins |
| Team not in `Factions[]` | empty CharacterData → `Spawn(..., none)` → TnPlayerPawnMultiplayer with **no body**: `PostBeginPlay` skips `ApplyTransformer`. **There is no fallback chassis anywhere in script** |
| Chassis ID unknown | logs, `ChassisType = none` → same as above |
| Spawn location blocked | native `SpawnActor` (0x82C31818) fails with "SpawnActor failed because of collision at the spawn location…" → `RestartPlayer` logs "failed to spawn player at", controller → `Dead` (retries through the respawn helper) |

`TnPawn` CDO has `bRequiresActorBlueprintOnSpawn = True`. P: I found no native message for a missing blueprint, so the enforcement point is not traced.

**Rebuild action (GP):** to stop always spawning Optimus, drive the chassis from `selected character × team` exactly as in A1 steps 3–5. Optimus (`Truck`) is **not** a default for any MP slot: the Leader preset is Ironhide (`Truck3`) / Soundwave (`Truck4`).

### A4. Specialty buffs replace the chassis health in versus (C; corrects earlier notes)

- `TnPlayerPawn.ApplySpecialty` (from `TnCharacterApplier`) maps `CD.Specialty` to a class:
  - Soldier → `TnSpecialtySoldier`;
  - Leader → `TnSpecialtyLeader`;
  - Scientist → `TnSpecialtyScientist`;
  - Scout → `TnSpecialtyScout`.
- If `GetGameClass()` is null it retries after 0.1 s. It then calls `Apply`.
- `TnSpecialty.Apply` runs only if `GameClass.default.ApplySpecialtyBuffs` is true. It calls `SetSpeedMultiplier(SpeedMultiplier)` and `InitializeSegmentedHealth(HealthBlueprint)`.
- `ApplySpecialtyBuffs`: `TnGame` CDO = **True**. Only `TnCampaignGame`, `TnSurvivalGame` and `TnGameLobbyGameCampaign` set it False. **Every versus mode applies the buffs.**
- `TnSegmentedHealth.Initialize` is script:
  - `HealthMax = sum(Segments)`;
  - on authority, `Health = HealthMax`;
  - `OverShieldHealth = clamp(Health − HealthMax, 0, bp.Overshield)`;
  - `AddOverShield`: `Health = HealthMax + bp.Overshield`.

| Specialty | `TR_Health_p` blueprint | Max | Overshield | SpeedMultiplier |
|---|---|---|---|---|
| Leader | `Health_Leader` 5×60 | 300 | 200 | 0.95 |
| Scientist | `Health_Scientist` 3×60 | 180 | 200 | 0.90 |
| Scout | `Health_Scout` 4×50 | 200 | 200 | 1.00 |
| Soldier | `Health_Soldier` 6×55 | 330 | 200 | 0.90 |

`SharedHealth` (175 / 125 / 125 / 125, OS 550) is only the value set by `ApplyTransformer` before the specialty overrides it. It is the effective value in campaign, Escalation and the campaign lobby. Corrected in `MILESTONE05_GAMEPLAY_UNKNOWNS`, `MILESTONE05_FRONTEND_GAMEPLAY_BLOCKERS`, `OVERNIGHT_2026-10-04` §E and `HANDOFF_2026-10-01`.

## B. Customization preview / camera (FE / RN)

All C unless marked. Sources: `UI_CharacterCustomization_m` authored Kismet and actors; `TnCharacterScriptBinding`; `SeqVar_TnCustomizationCameraId`.

### B1. Preview pawns

- **Two preview pawns**, spawned by Kismet `Preview_Characters` (`SeqAct_TnPawnFactory`).
  - Pawn class: `TransContent.TnCustomizationPawn`, an AI pawn using `TR_AiCharacterDefinition_p.Customization_AICD`. Its initial chassis is the AICD's `AiCharacterDataResolved.ChassisType = Breakdown_ROBODEF`.

| Slot | Kismet var | Spawn point | Location | Yaw |
|---|---|---|---|---|
| **Autobot** | `PreviewGuy0` | `PathNode_16191` | (−285.9, 5587.9, 179) | −11264 (−61.9°) |
| **Decepticon** | `PreviewGuy1` | `PathNode_7537` | (−286.9, 4701.9, 179) | 8192 (+45°) |

- The hidden `SkeletalMeshActor`s at the same spots (Sideswipe / Barricade meshes, Z 1.7) are editor placeholders: `bHidden = true`.
- **Updating the preview** (`Customize.UpdatePreviewCharacter(chassisCSV, primaryHexCSV, secondaryHexCSV)` from the AS) → `UpdateSinglePreviewCharacter` per index:
  1. Clears `bRotateTowardFocus`, Team = none.
  2. Builds the CD with `ParseStringDataIntoPreviewCharacter`: `ChassisTypes[0] = id`, **`Factions[0] = 0`**, colours from the hex strings (`0xRRGGBB`, or a packed palette string). Invalid or empty hex → (0, 0, 0, 255) = material default paint.
  3. **If the chassis changed:**
     - texture-streams the old chassis out and the new one in (`CharacterTextureLoader.UpdateTransformer`);
     - destroys the old pawn and spawns a new `TnCustomizationPawn` at **(100000, 0, 0)** with the spawn-point rotation and actor blueprint = chassis;
     - possesses it;
     - on its first tick (`OnPreviewPawnTick` → `FindGround`) traces down from the spawn point by 5 × collision height and sets Location = hit + collision height. On a miss: "Couldn't find ground", (0, 0, 0).
  4. `ApplyCharacter(CDR)`.
  5. If the chassis changed: `CreateAndInitializeVehicleAiControlStrategy`, then `SetupPreviewAnim` (`IdleNode.SetAnim('Cust_Idle')`, resolved through the AnimSet chooser groups; see B4), then a forced GC.
- **Rotation:** fixed at the spawn-point yaw. No script rotates the preview (`bRotateTowardFocus = false`; `TnCharacterScriptBinding` has no rotate API). H: the player cannot spin the model.
- **Robot / vehicle preview:** `Customize.TransformPreviewCharacter` toggles the first visible preview pawn between forms with a **real `Transform`** (`TransformToForm`). It first snaps X / Y back to the spawn point, keeping Z. `TransformPreviewCharacterToRobot` forces robot.
- **Weapons:** the preview CD carries no `WeaponTypes`, so `ApplyWeapons` gives nothing. **No weapon is shown on the preview** (H). The idle stays on the `WeapActive` / `IdleNode` branch because `_WeaponIdleState` defaults to 1.
- **Colour:** the preview faction is always 0. Colours come only from the UI hex values (custom primary / secondary), applied by `TnCharacterApplier.ApplyColorsToCharacter` exactly like in game. There is no team tint.

### B2. Camera

- **One `CameraActor_2082`:** location (784.1, 5252.1, 235.0), rotation (Pitch −544 = −3.0°, Yaw 33568 = −175.6°), **FOV 70**, aspect 1.7778.
- Matinee "Customization Camera Director" (`InterpData_2485`, 1.0 s, **looping**) holds a director cut to the `Camera` group. It is started by the AS fscommand `initStreamingLvl`, which also spawns the preview characters.
- **The base shot frames both robots.** Hiding one faction (AS fscommands `hideAutobot` / `hideDecepticon` / `unhide*`) fires a `Preview_Characters` output. The `Chassis_To_Cam_ID*` sub-sequence then reads `SeqVar_TnCustomizationCameraId` (the `TnDataProvider_Chassis.CustomizationCameraId` of that preview pawn's chassis) and **plays or reverses a 0.5 s class matinee** that dollies to the remaining robot:

| Event | Matinee | Direction |
|---|---|---|
| Decepticon hidden | Autobot matinee for the Autobot pawn's CameraId | **Play** |
| Decepticon unhidden | the same Autobot matinee | **Reverse** |
| Autobot hidden | Decepticon matinee for the Decepticon pawn's CameraId | **Play** |
| Autobot unhidden | the same Decepticon matinee | **Reverse** |

CameraId → class: **0 = Scout, 1 = Scientist, 2 = Leader, 3 = Soldier** (all Car* = 0, Jet* = 1, Truck* = 2, Tank* = 3, Minions = 2).

| Matinee (0.5 s, from the base pose) | End position | End FOV |
|---|---|---|
| SCOUT – Autobot | (659.1, 5424.6, 195) | 60 |
| SCIENTIST – Autobot | (659.1, 5434.6, 235) | 65 |
| LEADER – Autobot | (659.1, 5434.6, 215) | 60 |
| SOLDIER – Autobot | (639.1, 5454.6, 205) | 65 |
| SCOUT – Decepticon | (659.1, 5040.9, 195) | 60 |
| SCIENTIST – Decepticon | (659.1, 5020.9, 235) | 65 |
| LEADER – Decepticon | (659.1, 5020.9, 215) | 60 |
| SOLDIER – Decepticon | (639.1, 5000.9, 225) | 65 |

- Rotation stays (0, −3.0°, −175.6°) in every key. All matinees are `bClientSideOnly`, `bRewindOnPlay`, `bRewindIfAlreadyPlaying`.
- "OLD – Pan to Autobot / Decepticon" (`x = 834`, no FOV track) are unused leftovers.

### B3. Lighting / post (C)

- `StaticLightCollectionActor`:
  - DirectionalLight Brightness **6.0**, shadow filter High, shadow resolution 2048;
  - SkyLight Brightness 0, LowerBrightness 0.5, LowerColor (78, 148, 186).
- Both have `LightingChannels BSP = false`, `Static = false` (user-selected classification), so they light only dynamic primitives: the robots.
- PostProcessVolume: Bloom_Scale 0.01, **Scene_Desaturation 0.35**, DOF kernel 64.
- The preview pawns carry their own `DynamicLightEnvironment` (TnPawn components).
- Emblem material fades (`Emblem_Manipulation`: Autobot / Decepticon Icon + Glow, 0.3 / 0.5 s `FloatMaterialParam` matinees on `MaterialInstanceActor`s) are driven by AS fscommands `fadein*` / `fadeout*` / `glow*` / `dim*`.

### B4. Preview idle animation (C, native; answered to Rendering)

- `SetAnim` = `UAnimNodeSequence` vtable slot 96, `0x82E3FF48` (exec `0x82C7F598`). It resolves the requested name through **AnimSet `ChooserGroups`**:
  - `0x82A9E0F8` walks `SkelComp.AnimSets` from last to first;
  - the first group with that name supplies the anim (weighted pick);
  - otherwise the name is used literally.
- It then always clears `AnimSeq` and `LinkupIndex` and looks the sequence up (`0x82D76AC8`).
- Every playable chassis has a `Cust_Idle` group:
  - → `Cust_Idle` for Starscream, Optimus, Breakdown, Deadend, Thundercracker, Skywarp, Jetfire, Warpath, Scattershot, Ironhide, Soundwave, Zeta, Onslaught;
  - → `NAV_Idle` for Bumblebee, Megatron, Sideswipe, Barricade, Jazz, AirRaid, Silverbolt, Shockwave, Slipstream, Demolishor, Ratchet;
  - Brawl → `NAV_Idle` / `Nav_Idle_02`;
  - Arcee → `Cust_idle_active`.
- The Car8–10 soldiers and Minion1 / Minion2 have no group: missing sequence → NULL → reference pose (H).

## E. Movie language: file choice and Bink audio track (SY) (C, native)

### E1. Current language (`GLanguage`, buffer at `0x8370B4A8`)

At startup (`0x82BC04E0`):
- If the command line has `LANGUAGEFORCOOKING=xxx`, it calls `UObject::SetLanguage(xxx)` (`0x82B92930`).
- Otherwise it calls `SetLanguage(appGetLanguageExt())` (`0x829CD960`).

`appGetLanguageExt`:
1. `XGetLanguage()` (`0x83304BF8`): `ExGetXConfigSetting(3, 9)`. If that gives 0 or more than 12, it falls back to region: `XGetGameRegion` Japan (0x101) → 2, other Asia (0x1xx) → 7, otherwise 1.
2. Maps the index through table `0x83708E68`:

| Index | Language code |
|---|---|
| 0, 1 | INT |
| 2 | JPN |
| 3 | DEU |
| 4 | FRA |
| 5 | ESN |
| 6 | ITA |
| 7 | KOR |
| 8 | CHI |
| 9 | ini `[Engine.Engine] PortugueseLanguageExt` (default `POR`) |
| 10, 11 | INT |
| 12 | RUS |

3. Checks that the language is shipped (`0x829CD898`: `..\%sGame\CookedXenon\Startup_%s.xxx` exists). If not, it tries INT, then DEU, then ESN, and finally uses INT.

### E2. Which movie file (`0x82CD3348`, also used by the loading movie)

Base path `P = <base>Movies\<Name>.bik`. Seven candidates are tried in this order; **the first file that exists wins** (FileManager size ≠ −1):

1. `<Name>_360_<LANG>.bik`
2. `<Name>_360_INT.bik`
3. `<Name>_<REGION>_<LANG>.bik`
4. `<Name>_<LANG>.bik`
5. `<Name>_INT.bik`
6. `<Name>_360.bik`
7. `<Name>.bik`

- `_360` = platform string (`0x8370A1C8` → "360"; `"_%s"`).
- `<REGION>` (`0x82BD4420`, from the console country via `0x829B3FC8`): `_NA`, `_SA`, `_EU`, `_AS`, `_AU`, `_AF`, or nothing.
- The shipped `TF_InitialStartup_{NA,EU}_{INT,FRA}.bik` and `TF_LoadingScreen_{INT,FRA}.bik` are matched by candidates 3 and 4.

### E3. Which audio tracks play (`0x82CE0F00`, full-screen / loading movie player)

1. Before `BinkOpen` it calls **`BinkSetSoundTrack(count, tracks)`** (`0x836977C0`) with the list built by `0x82CDD4B0`: **`[0, 1, 2, 3, 4, 5 + L]`**.
2. L comes from `0x82CBEEE0`, a case-insensitive compare on `GLanguage`:

| GLanguage | L | Bink track |
|---|---|---|
| any other (INT, JPN, KOR, CHI, POR, …) | 0 | 5 |
| FRA | 1 | 6 |
| ITA | 2 | 7 |
| DEU | 3 | 8 |
| ESN | 4 | 9 |
| RUS | 5 | 10 |
| POL | 6 | 11 |

3. `BinkOpen` (`0x83697C30`) is called with flags `0x01104400` (from file, `0x82CCC668`) or `0x04104400` (from memory, `0x82CBF110` / `0x82CD2878`). Both include `BINKSNDTRACK` (`0x4000`). Without that flag Bink would default to track 0 only.

**So tracks 0–4 are always mixed in** (H: music, SFX or surround beds), plus exactly one language track at 5 + L.

- Volume: if `<Name>` matches an entry in `[Engine.MovieSettings] MoviesToAlwaysPlaySound`, the movie uses fixed volume 0xCCCC; otherwise the volume parameter × constant.
- Texture-only Bink users (`0x82C078D0` / `0x82BE81C0`, `UCodecMovieBink`) call `BinkSetSoundTrack(0, 0)`: no audio.
- **Systems action:** open the chosen .bik and enable tracks {0, 1, 2, 3, 4, 5 + L} with the table above. If the file has fewer tracks, Bink simply ignores the missing indices (H, Bink SDK behaviour).
