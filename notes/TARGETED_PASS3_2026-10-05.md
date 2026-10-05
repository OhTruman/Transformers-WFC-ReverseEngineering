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

## C. Vehicle simulations for car, tank and jet chassis (GP) (C, UnrealScript bytecode)

**These "native" sims are UnrealScript.** Full bytecode is in this repo: `work/script/decomp/TransGame.{TnHoverTankSimulation,TnHoverPlaneSimulation,TnPlaneSimulation,TnCarSimulation,TnHoverCarSimulation,TnTankForm,TnPlaneForm,TnCarForm,TnTruckForm}.txt`. Only the rigid-body primitives (`IRigidBody.Apply*`, PhysX) and `HoverPhysics.MoveTo/RotateTo` (AI path only) are native.

Common conventions:
- `Strafe` = "velocity servo": `a = ClampLength((dir·MaxSpeed − v)/dt, MaxAccel)`, applied as an acceleration.
- `Turn` = angular-velocity servo: `ω += (axisAngle(q⁻¹·q_target)/dt − ω_local) · TurnRate`.
- `SpeedModifier` hooks buffs.

### C1. Which chassis use which blueprints (authored VEHDEF)

| Class | Vehicle form | Hover sim blueprint | Second mode |
|---|---|---|---|
| Car (Car–Car7: Bumblebee, Sideswipe, Breakdown, Barricade, Arcee, Jazz, Deadend) | `TnCarFormBlueprint` | **`HoverCar_Physics`** (TnHoverCarSimulation) | boost `Car_Physics` (TnCarSimulation) |
| Truck (Truck–Truck7) | `TnTruckFormBlueprint` | `HoverTruck_Physics` | `Truck_Physics` |
| Tank (Tank–Tank5) | `TnTankFormBlueprint` | **`HoverTank_Physics`** (TnHoverTankSimulation) | none: boost is a speed cap |
| Jet (Jet–Jet8) | `TnPlaneFormBlueprint` | **`HoverPlane_Physics`** (TnHoverPlaneSimulation) | flight `Plane_Physics` (TnPlaneSimulation) |
| Car8–10 soldiers, Minion1/2 | `TnCarFormBlueprint` | `HoverTruck_Physics` | `Truck_Physics` |

**The car and the truck run the same `TnHoverCarSimulation` code.** Only the blueprints differ (C):
- **Car** `HoverCar_Physics`: MaxLinearAcceleration **4000**, MaxLinearSpeed 1500 (CDO), SuspensionRadius **100**, Dash 0.5 s @ 3000, AiMaxAngular 12. Suspension `HoverCar_Supension`: Stiffness **8000**, Damping 4000, RestingLength **200**.
- **Truck:** accel 3000 (CDO), radius 185; suspension Stiffness 10000 (CDO), Damping 4000, rest 250.
- **Form-level differences:**
  - `TnTruckForm.Hovering.DoDash` dashes **forward** `(1,0,0)`.
  - `TnCarForm.Hovering.DoDash` dashes along the **dominant stick axis**: `(sign(fwd),0,0)` or `(0,sign(right),0)`, in local space, so a sideways dash is possible. Cooldown 2.0 s (`TimeBetweenDashes`).
  - Truck boost Shift = Nitro; car boost Shift = barrel roll (C4).

### C2. Tank: `TnHoverTankSimulation` + `TnTankForm`

Blueprint `HoverTank_Physics`, with CDO values for unset fields:

| Field | Value |
|---|---|
| MaxLinearAcceleration | 2500 |
| MaxLinearSpeed | 1500 (CDO) |
| **MaxBoostSpeed** | **2500** |
| DriftDuration | 0.5 (CDO) |
| JumpLinearSpeed | 1200, JumpAngularSpeed 1.0 (CDO) |
| **RecoilVelocity** | **750** |
| SuspensionRadius | 250 |

Suspension `HoverTank_Suspension`: Stiffness 20000, Damping 6000, Rest 250. TerminalVelocity 3500. Turn rate `(0.05, 0.05, 1)`.

```
Update(dt, fwd, right, cameraYaw):
  if SimulationMode==0: cancel gravity; return
  F = (0, cameraYaw, 0)
  UpdateSuspension: 4 rays at COM + normal(1,1,0)*SuspensionRadius rotated 0/90/180/270° yaw (diagonals), cast along body -Z;
      on contact: ApplyForce(-dir * max(0, spring.Force), probe point); OnTheGround = any contact
  UpdateTerminalVelocity: clamp vz >= -3500
  UpdateStrafe: Drift -= dt (floor 0); if !IsStable (|pitch|>=30° or |roll|>=30°) return
      maxA = MaxLinearAcceleration * (1 - Drift/DriftDuration)^2
      maxV = Boosting ? MaxBoostSpeed : MaxLinearSpeed
      input = Boosting ? (1,0,0) : (fwd, right, 0)      // boosting = full forward, the stick does not strafe
      Strafe(input, mask (1,1,0) in yaw frame F)
  UpdateRoll(right): local angular accel X = 1.0*right + 1*(-ωz)
  UpdateTurn(F): heading slaved to camera yaw (TurnRate Z = 1 → full correction each tick);
      if IsStable && OnTheGround: only the yaw component is applied; else pitch/roll are also corrected at 0.05
```

TnTankForm:
- **Boost** (LT/RMB): `StartBoost` when input is held and the tank isn't drifting. Releasing calls StopBoost + **Drift()** (0.5 s with reduced acceleration).
- **Firing (`OnWeaponFired`)** = StopBoost + `Recoil()` (local velocity −750 on X) + Drift.
- **Jump** (A/Space): only on the ground, every **0.5 s**. Adds +1200 vertical velocity and local angular velocity Y −1.0 (nose up).
- **Special move** (RB/Shift) = **"180"**: camera recentre (`TnCamera.RecenterCamera = true`), cooldown **1.2 s**. Because heading is slaved to camera yaw, the hull follows.

### C3. Jet: `TnPlaneForm` (states Hovering / Flying)

- **Activation:** Flying if boost is held, else Hovering. `bIsFlying = true` in both.
- **Hovering → Flying:** boost held and not drifting, or `_ForceJetBoostInput`.
- **Flying → Hovering:** boost released; or a rigid-body hit with ContactSpeed > **ReturnToHoverCrashSpeed 3000** (players only).
- **Hovering.BeginState:** `Activate` + `Drift()`.

**Hover:** `TnHoverPlaneSimulation`, `HoverPlane_Physics`:

| Field | Value |
|---|---|
| MaxLinearAcceleration | 2500 |
| MaxLinearSpeed | 1500 (CDO) |
| Dash | **0.1 s @ 1000** |
| Roll | 0.6 s @ 3000 (CDO) |
| DriftDuration | 0.25 |
| MotionPhysicsScale | 1 |
| MaxAngularVelocity | 50 |
| AngularDamping | 6 |
| TurnRate | (0.1, 0.5, 0.5) |

```
Update: cancel gravity (always hovers);
  if Rolling: UpdateRoll(view rot) else { if Dashing: UpdateDash; UpdateStrafe; UpdateTurn }
UpdateStrafe: maxA = 2500 * max(driftScale, max(|fwd|,|right|)); Strafe((fwd,right,0), mask (1,1,1), frame = full VIEW rotation incl. pitch)
   → pushing forward flies along the camera's pitched forward
UpdateTurn: target = view rotation + motion lean (roll += smoothedLocalAccel.Y*1*s + smoothedLocalAngVelZ*1000*s; pitch -= smoothedLocalAccel.X*0.5*s)
Ascend / Descend held → Dash(±Z) every frame → vertical servo at DashSpeed 1000, accel 10000, mask (0,0,1)
Roll (RB/Shift with |stick X|>=0.5): RollTime = 0.6 s; strafe sideways at RollLinearSpeed 3000 (accel 10000);
   barrel-roll angular speed 2π/RollDuration about local X (accel 80); cooldown 1.2 s
```

**Flight:** `TnPlaneSimulation`, `Plane_Physics`: **MaxSpeed 4000, MaxAcceleration 3000, DragCoefficient 600**. CDO: PitchDueToPitchValue 27, YawDueToYawValue 16, RollDueToYawValue 77, ExtraRotationLerpValue 0.1, MaxPitchValue 60°, FullPitchThreshold 45°, RollDuration 0.8, RollLinearSpeed 3000, RollAngularSpeed 8. AngularDamping 8.

```
Update(dt, viewRot, yawIn, pitchIn): cancel gravity;
  UpdateFly: Strafe((1,0,0), mask (1,0,0), frame viewRot, 3000, 4000)  // always thrusting forward along view
             ApplyDrag: lateral+vertical local velocity v⊥ → solve A·s²+s−|v⊥|=0, A = dt*600/Mass; accelerate v⊥ to s
  target = viewRot ⊕ RLerp(prev, (-pitch²·27, yaw²·16, yaw²·77) deg, 0.1)   (signed squares of the stick)
     pitch term fades linearly from 45° to 0 at 60° body pitch
  Rolling ? UpdateRoll (sideways strafe 3000 + barrel roll 8 rad/s) : Turn(target, TurnRate (0.1,0.5,0.5))
```

Player inputs (`PlayerInPlaneForm.SetLocalInputs`):
- left stick → strafe;
- `GetNormalizedTurn` / `GetNormalizedLookUp` → yaw / pitch inputs;
- RB/Shift → roll;
- Ascend / Descend → hover vertical dash.

### C4. Car boost mode: `TnCarSimulation` (`Car_Physics`)

| Field | Value |
|---|---|
| Mass | 1500 |
| COM | (12, 0, −16) |
| MaxAcceleration | 3000 |
| MaxSpeed | 3000 |
| Jump | (600, 0, 1400) |
| AirControl | turn 12, strafe 2600 |
| **RollDuration** | **0.7** (CDO; the truck overrides it to 0, so CanRoll is false) |

**Barrel roll:** `TnCarForm.Driving.UpdateRolling`. Requires `CanRoll` (RollDuration > 0), the special move off cooldown, and **Shift/RB (Dashing input) while boosting** → `TnCarSimulation.Roll()`; cooldown **2.0 s**.

```
Roll(): dir = sign(RollControl = stick X)
  v += yawFrame(0, dir*1200, 1000 - vz)     (vertical part dropped if a Jump happened this same frame)
  JumpTimeRemaining = RollDuration (0.7)
  local angular velocity X += -dir*100 (clamped by the rigid body's max angular velocity)
UpdateRolling (while JumpTime>0 and |dir|==1): local angular accel X = -dir*100; lateral accel yawFrame(0, dir*1000, 0)
   → replaces air control and leveling for that period
```

With the stick centred (dir = 0) Shift gives a straight **1000 UU/s hop** with no spin.

Other boost-mode functions:
- `UpdateLeveling`: when |RollControl| > 0.1 and (stick opposes the roll, or |roll| < 45°), local roll acceleration = sign(roll) · 50 · (−0.5 · (up.z − 1)).
- `UpdateBoost` (ground only): `a = lerp(MaxAccel, drag(MaxSpeed), fwdSpeed/MaxSpeed) + lowSpeedBoost`, × BoostScale (slope fade) × Accelerator.
- `UpdateTerminalVelocity`: lerp(LandingVelocity, TerminalVelocity, groundDist / LandingTraceDistance).

### C5. Notes (FIDELITY)

- **The tank has no separate "boost car" physics.** Boost only raises the strafe cap to 2500 and forces forward input. Recoil and drift happen on every shot.
- **The jet's flight mode has gravity cancelled** and always thrusts toward the view direction. Releasing boost returns to VTOL hover.
- **Car hover:** a lighter, shorter (rest 200, radius 100) and softer (8000) spring than the truck's, at the same code path.

## D. Multiplayer modes: setup and layer attribution (GP)

The per-mode behaviour table (scoring, limits, timers, objectives, spawns, markers, end, announcers, DOM capture, EXT bomb) is in `MILESTONE05_PLAYTEST_RE.md` §3. CTF flag return and bomb return rules are in `OVERNIGHT_2026-10-04` §G. This section adds **creation/setup** and **which layer owns what**.

### D1. Creation (authored data: `TnOnlineGameSettings<MODE>` CDOs; C)

| Mode tag | GameClass | Lobby | TeamType | Rules (exact `Rules[]`) |
|---|---|---|---|---|
| TDM | `TransContent.TnVersusGame` | `UI_Lobby_m` + `TnGameLobbyGameTeam` | GTS_TeamGame | ScoreKillsTDM, TrackKillsMP, ReportGameProgressTime, ReportGameProgressKills |
| DM | `TransContent.TnFreeForAllGame` | `TnGameLobbyGameFreeForAll` | GTS_FreeForAllGame | ScoreKillsDM, TrackKillsMP, ReportGameProgressTime, ReportGameProgressKills |
| DOM (Conquest) | TnVersusGame | Team | GTS_TeamGame | ScoreKillsMP, **ScoreDomination**, TrackKillsMP, ReportGameProgressTime, ReportGameProgressPoints |
| KOTH (Power Struggle) | TnVersusGame | Team | GTS_TeamGame | ScoreKillsMP, **ScoreKingOfTheHill**, TrackKillsMP, ReportGameProgressTime, ReportGameProgressPoints |
| CTF (Code of Power) | TnVersusGame | Team | GTS_TeamGame | ScoreKillsMP, **SingleFlagCTF**, **ScoreFlags**, TrackKillsMP, ReportGameProgressTimeCTF |
| EXT (Countdown to Extinction) | TnVersusGame | Team | GTS_TeamGame | ScoreKillsMP, **ScoreBombingRun**, TrackKillsMP, ReportGameProgressTime |
| SV (Escalation) | `TnSurvivalGame` | `UI_CampaignLobby_m` + `TnGameLobbyGameSurvival` | GTS_SingleTeamGame | CompetitiveScoring, TrackKills |

Rules-format strings use tokens `` `p `` points, `` `t `` time, `` `r `` rounds (`RulePairs`).

**Playlists** (`TransPlaylists.ini`): 1 TDM (CivilWar), 2 DM, 3 CTF, 4 KOTH, 5 EXT, 6 SV, 7 DOM, 100 CP, 101 CCP.

**Travel URL:** `…?Game=<GameClass>?GameModeTag=<tag>?…`. The bootstrap note has the full URL; the rules come from the settings object (`AddGameRulesFromSettings`).

### D2. Layer attribution

| Behaviour | Layer | Where |
|---|---|---|
| Match state machine (PendingMatch countdown → InProgress → MatchOver 15 s → lobby), goal score / time / rounds from URL, `SetPlayerDefaults` (character apply), weapon data type 3 | **UnrealScript** (TransContent, cooked in map) | `work/q/streets_base_gameclasses.txt`: TnMultiplayerGame / TnTeamGame / TnFreeForAllGame |
| Scoring per mode, objective activation, round logic, progress announcements | **UnrealScript** (TransGame rules) | `TransGame.TnGameRules_*` |
| Objective actors (domination point, KOTH zone, flag factory, dropped flag/bomb, plant point) | **UnrealScript** | `TnDominationPointBase`, `TnKingOfTheHillZone`, `TnGameObjectivePickupFactory*`, `TnDropped*`, `TnBombPlantPointBase` |
| Spawn choice / respawn waves | **UnrealScript** | `TnPlayerSpawnHelperMultiplayer`, `TnRespawnHelperWave`, `RatePlayerStart` overrides |
| Defaults (points, time, rounds, choices) | **Authored data / config** | settings CDO `PropertyMappings`, `Xe-TransGame.ini` |
| Objective placement, counts, PointNumber, spawn clusters per mode | **Authored map data** | `MP_*_m` actors (Streets: 5 KOTH zones, 60 player starts) |
| HUD presentation (scoreboard widget, markers, announcements) | **Scaleform AS2 + script observers** | `Hud_GFX`, `TnHudDataObserver*`, `TnObjectiveMarkerType*` |
| Physics, collision, travel, networking | **Native** | engine |

**No mode-specific native code was found.** Every mode rule is script or data.

## G. Shipped PC settings and input (FE / SY)

**Source:** the Xbox dump ships the **multi-platform** `SettingsMenu_GFX` (AS2 branches on `HmUtility.Platform == 'WIN' / 'XBOX360' / 'PS3'`). It also ships the shared PC script `HmPCSettingsActionScriptBinding` → `Engine.PCSettingManager`. The PC executable itself is not in the dump, so native PC defaults are UNKNOWN.

### G1. Settings screens

| Item | PC (WIN branch) | Source | Conf |
|---|---|---|---|
| **Graphics** | Brightness (calibration screen), **Resolution** (list from `PCSettings.GetResolutions()`, "WxH"), **Fullscreen** On/Off, **Texture Quality** Low / Medium / High (0 / 1 / 2), **VSync** On/Off, **Commit** button. Commit calls `SetResolution(w, h, fullscreen)`, `SetTextureQualityLevel(q)`, `SetVSyncState(b)` (the values are applied only on Commit) | `SettingsMenu_GFX` `graphicsMenuArray`, `writeGraphicsSettings` | C |
| Graphics (console) | Brightness only | same | C |
| **Audio** | identical on all platforms: FX / Dialogue / Music volume 0–100 in steps of 10, subtitles | `audioMenuArray` | C |
| **Controls** | identical list on all platforms: **Vibration** On/Off; **Layout** (button map); Invert Y **Car / Jet / Tank / Robot**; **Camera Sensitivity** 0–100 in steps of 10 | `controlsMenuArray` | C |
| **Layout screen, PC** | a static **`mc_WIN_Map`** keyboard and mouse diagram, scrolled per form (Robot / Car / Truck / Plane / Tank). Labels come from `TnPlayerInput.GetKeyDescription(key, form)`. **No Scheme A/B selector and no key rebinding** (the scheme list is console only) | `SettingsMenu_GFX` layout function; `TnPlayerInput.KeyDescriptions` | C |
| Keyboard rebinding UI | **none.** `showKeyboard = false` on WIN, and no movie calls `Input.SetBind`. Bindings are fixed by `[*.PlayerInput] Bindings=` in `TransInput.ini` | AS2, script | C (no UI) |
| Mouse sensitivity option | **no separate option.** The single Camera Sensitivity value (profile id 40, normalised 0–1) drives the mouse | see G2 | C |
| Vehicle-specific sensitivity | **none.** Only invert is per form | — | C |

### G2. Mouse / controller math (C, script)

- **Mouse look** (`HmPlayerInput.CalculateCameraRotation`): `CameraYaw = 0.00114286·mouseX`, `CameraPitch = 0.00114286·mouseY` (`MouseCameraSensitivityX/Y`). Pitch is negated if `bInvertMouse`.
- **Under mouse/keyboard control** (`IsUnderMouseAndKeyboardControl`: mouse moving, or a key down with no stick input):
  - orbit camera speed = `Lerp(0.03, 0.20, CameraSensitivity01) · CameraSensitivityModifier · 182.044` per input unit (`TnOrbitRotationCameraBehavior.GetCurrentSpeedMultiplier`);
  - no ramp;
  - target stickiness is disabled (`DisableTargetStickinessUnderMouseControl = true`).
- **Controller:** `Lerp(LowSensitivityMultiplier, HighSensitivityMultiplier, CameraSensitivity01) · ramp · 182.044 · dt`. Deadzone 0.25 (radial).
- **Invert:** `UpdateInvertMouseByRobotForm` / `…ByVehicleForm` set the one `bInvertMouse` flag from the profile per form: Car and Truck → InvertY_Car, Plane → InvertY_Plane, Tank → InvertY_Tank. Mouse and stick share it.
- `PlayerInput.MouseSensitivity = 15`, mouse smoothing off (`TransInput.ini`). Guided missile under mouse uses `GuidedMissileMouseSensitivity 1.0` × camera deltas.

### G3. PC keyboard presentation (C, `TransGame.int [TnPlayerInput] KeyDescriptions`)

**The PC Shift key label per form** (key index 24): Robot "Ability 1", Car **"Flip"**, Truck **"Ram"**, Tank **"Quick Turn"**, Plane "Roll Start". RMB: Robot "Fine Aim / Detonate Grenade", vehicles "Speed Boost".

Other keys:

| Key | Label |
|---|---|
| Ctrl | Ability 2 |
| Space | Jump |
| C | Hover Up (plane) |
| V | Hover Down (plane) |
| E | Interact / Pick Up / Revive / Add to Generator |
| F | Change Form |
| G | Throw Grenade / Detach Turret |
| Q | Melee |
| R | Reload |
| B | Look At / Kill Streak |
| Tab | Scoreboard |
| Esc | Pause |
| Wheel / PgUp / PgDn | Swap Weapons |

**UNKNOWN:** native `PCSettingManager` defaults (default resolution, default texture level, default VSync) and how the texture level maps to streaming settings (`SetTextureStreamingSettings` is native).

**PC extensions beyond the original:** FOV slider, key rebinding, separate mouse sensitivity.

## F. Title / menu scene timing (RN / FE) (C, authored Kismet)

**Boot chain** (`UI_FrontEnd_m` Main_Sequence): `SeqAct_MoviePlayer` Logo_Activision → Logo_Hasbro → Logo_HighMoon → **FMV_intro**. When FMV_intro reports **Stopped**, a single output fires all of the following **in the same frame**:
- `Fade In` (`InterpData_54`, 2.0 s);
- **`Primary Camera`** (`InterpData_799`, 1.0 s, looping; director cut at t = 0 to group `Camera` = `CameraActor_6585`, which sets the view target);
- **`Camera Orbiter`** (`InterpData_6478`, **393.551 s, looping**). Groups:
  - `NewCameraGroup` = `CameraActor_6585`: InterpTrackMove with **34 position and 34 rotation keys**, `IMF_RelativeToInitial`, `CIM_CurveUser`; an FOVAngle track with **no keys**, so FOV stays **45**;
  - `CameraDummy` = `CameraActor_2151`: two zero keys (static).
  - Its event outputs drive ambience: AUDIO_START → AMB_IACON on / AMB_KAON off, AUDIO_KAON_AMB → swap, plus seven `AUDIO_*DEBRIS_BY_*` whooshes.
- `ActivateRemoteEvent` **"StartFireworks"**;
- reverb, `PlayMusic`, `SetLoadingMovieFilename`;
- `ToggleHUD` → `ToggleHidden` → **`TnSeqAct_OpenFrontEnd`** (the title GFx opens).

**Vignette** (`UI_FrontEnd_capture_VIG_m`, streamed by `LevelStreamingKismet`): `SeqEvent_RemoteEvent` "StartFireworks" starts **1st QTR, 2nd QTR, 3rd QTR and Plane Fly By together**. All four are **393.551 s and looping**, the same length as the camera orbiter. **The whole scene is one synchronised 393.55 s loop**, started at the same instant as the camera.
- Plane Fly By event keys toggle visibility (show01 / hide01, togAjetFlyBy01/02, togDjetFlyBy02, togTrans, togDS, killaj09, seeFight) and Kill → `HideDogFight` (delay, then hide).
- DrawScale tracks animate emitter / actor scale (e.g. group 10941: 0.2 until 19.2 s → 0.05 at 25.09 s; group 15666: 0.08 → 0.4 at 253.4 s → 0.75 at 272.4 s). With the particle-scale rule (§ particle note), these scale the particles.
- The vignette also contains its own `CameraActor_1205` (FOV 45, same transform as `CameraActor_6585`) and the camera groups `CameraDummy` / `NewCameraGroup`, which are left **unbound** in the VIG matinees. **The view target is the persistent level's `CameraActor_6585`.**

**Other title sequences:**
- `SeqEvent_GameplayStarted` → `Black-Out` (0.001 s) → `GFxAction_OpenMovie` (movie loader).
- RemoteEvent `closeMovieLoader` → CloseMovie.
- `InterpData_14018` (1.1 s) animates the circuit / ring materials and meshes after `SeqAct_InstallGame` finishes.
- `(OLD) Orbiting Camera` (`InterpData_6054`, 74.8 s, PlayRate 0.2) is not linked from the boot chain, so it is unused.

**Lobby / customization camera:** §B2.

### C6. Transform fit test: relocation versus refusal (C, native + script)

**Script:**

`TnPawn.MoveToSafeTransformationLocation(TargetForm)`:
1. `Extent` = target form's `CollisionExtent` (robot or vehicle form).
2. `FindSpotAwayFromPawns(self, Extent, SafeLocation)`. If it fails: log "Find start spot failed" and return false. The caller then shows `NotifyCantTransform` and plays the fail sound; **no transform** happens.
3. If the location is unchanged: transform in place.
4. If moved:
   - to robot: mesh offset (`_TransformationPositionShift`, blended back over **0.5 s**);
   - `SetLocation(SafeLocation)` + vehicle-form `Teleport`.

After the transform, `InRobotForm.MoveToSafeLocation` runs the same test with the **cylinder bounds**. On failure it logs "Find end spot failed", and the caller forces the vehicle form. `OnTeleport` (vehicle) also runs it with the vehicle mesh bounds.

**Native:**
- `execFindSpotAwayFromPawns` = `0x82C49950` → `0x82E30D98`.
  - If the actor argument IsA the pawn class (lazily resolved class object), it is passed as the source actor. That adds **TRACE_Pawns** and ignores the pawn itself.
  - It then calls **`UWorld::FindSpot` `0x82C23498`**. This is the same routine `SpawnActor` uses for its "collision at spawn location" test.
- Trace flags `0x08006086 | (pawn ? 1 : 0)`: Movers (0x2), Level (0x4), LevelGeometry (0x80), Terrain (0x2000), Tessellation (0x4000), 0x08000000, plus Pawns. **World geometry is tested**, not just pawns.
- Complex collision follows the pawn's flag (`Actor+0x7C` bit 7).

**`FindSpot` algorithm** (stock UE3 shape, constants confirmed):
1. Gather primitives overlapping `Location ± 2·Extent`. If nothing overlaps the box at `Location`: success, no move.
2. Otherwise run **2 passes**, with the probe scale **1.0** then **0.5**. Each pass pushes out along **Z**, then **X**, then **Y**: two opposing sweeps per axis from `Location ∓ axis·Extent·scale`, then move by the hit-time difference.
3. Re-test after each pass; success as soon as nothing overlaps.
4. Then try **diagonal** pushes (±X±Y±Z combinations at 0.5 scale) with the same re-test.
5. If it is still overlapping, **fail**.

**Human-visible result:**
- Under a low overhang or in a tight gap, the original **nudges** the body up to about one extent per axis (first pass), plus half an extent (second pass), to a fitting spot. **Only if no fitting spot exists within that reach does it refuse with the "can't transform" prompt.** It never transforms into geometry.
- If the robot still ends up embedded, it is immediately pushed back into vehicle form.

**Rebuild guidance:** run a box overlap with the target-form extent at the current location. If blocked, try depenetration along Z, X, Y (full extent, then half), then diagonals. Accept the first clear spot, else refuse.
