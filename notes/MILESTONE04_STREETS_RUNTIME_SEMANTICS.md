# MILESTONE 04 — MP_IAC_Streets runtime semantics (AssetTools a23c675) — 2026-10-02

Sources (all read-only):
- Ghidra: `tools/wfcq.ps1`.
- UnrealScript bytecode: `tools/ue3dis.py` → `work/script/decomp`.
- `AssetTools/manifests/authored.db`, `mp_iac_streets_complete.json`, `streets_kismet.json`.
- Shipped config: `ExtractedAssets/config/Coalesced_ini/...`.
- Earlier native note: `MILESTONE03_RENDERING_LIGHTVIS_SHADOW.md` §1–3.

> **Key correction:** except for item 1, none of the "native" behaviours asked about here are native. Marker-type selection, totem visibility and objective mode filtering are all **UnrealScript** (TransGame), keyed on `GameInfo.HasRule(<exact rule class>)`. Each mode's rule set comes from `TnOnlineGameSettings*.Rules`.

### Mode → rule table (authored `TnOnlineGameSettings*` defaults, CONFIRMED)

| tag | name | objective rule in Rules[] |
|---|---|---|
| CTF | Code of Power | **TnGameRules_SingleFlagCTF** (+ ScoreFlags, ReportGameProgressTimeCTF) |
| EXT | Countdown to Extinction | **TnGameRules_ScoreBombingRun** |
| DOM | Conquest | **TnGameRules_ScoreDomination** |
| KOTH | Power Struggle | **TnGameRules_ScoreKingOfTheHill** |
| DM / TDM | Deathmatch / Team Deathmatch | none (ScoreKillsDM / ScoreKillsTDM) |

Every MP mode also has ScoreKillsMP or DM/TDM, plus TrackKillsMP and ReportGameProgress*.

`GameInfo.HasRule(C)` walks `GameRulesModifiers` and compares `RulesNode.Class == C`. It is an **exact class match** (`Engine.GameInfo.HasRule`).

---

## 1. LightsVisibilitiesVolume (`LightsVisibilitiesVolume_2224`, ART level)

**CONFIDENCE:**
- CONFIRMED: class, serialization, query path and query semantics. These are from the earlier native pass and are not repeated in full here.
- CONFIRMED: there is a single caller (re-checked this pass).

**ADDRESS:** see the earlier note §1 for the full table. The ones that matter here:
- `0x82DE6C28` class registration (size 0x1DC, vtable 0x822DF6F0);
- `0x82DF5AF8` Serialize;
- `0x82DD7C08` / `0x82DD1F78` / `0x82DD2050` bind lights by LightGuid;
- `0x82DE6EE8` unregister (removes the volume from `World+0x2C8`);
- `0x82CCAC30` `LightEnv::QueryLightsVisibility`;
- `0x82DC05C8` root-cube contains test;
- `0x82DDE5F8` → `0x82DDE200` → `0x82DDDA08` octree query.

**FUNCTION / CLASS:**
- `Engine.LightsVisibilitiesVolume`, whose script parent is **`Engine.Actor`** (not Volume, not Brush).
- Script fields: `Octree` (native pointer), `FineLength`, `CoarseLength`, `bDisplayOctree`, `LightsVisibilitiesVolumeDebugProxyComponent` (editor debug).
- **No UnrealScript functions:** no BeginPlay, Touch or UnTouch script.
- The Streets instance: Location (19072, −43008, −72448), DrawScale3D 26729.2. The octree root cube is serialized; the actor transform is not used by the query.

**CALLERS / CALLEES:**
- Re-check this pass: `refs` to `0x82DDE5F8` / `0x82DDE200` / `0x82DC05C8` have **only one caller chain**: `0x82CE4E78` (the light-environment update) → `0x82CCAC30` → Query.
- Nothing in rendering, particles, visibility or culling queries it.

**FIELDS / CONSTANTS:** octree blob as in the earlier note: GUID light table, (int16 light, u16 vis/65535) pairs, child bit X-high, corner bit X-low, face weight 1/3.

**PSEUDOCODE:**
```
// on level load: Serialize -> octree; register in World+0x2C8; bind each table GUID to the LightComponent with that LightGuid
// per light-environment full update (time-sliced queue, earlier note §3.3):
pos = LightEnv.OwnerBounds.Origin
vol = last registered volume whose octree root cube strictly contains pos
if vol and leaf found: vis[light] = interpolated corner samples (0..1) for every light in vol's table
else:                  vis[light] = 0 for every baked light in the table ; unbaked lights -> ray traced
// vis feeds: direct-light selection/weighting, SH overflow, and the composite-shadow fade (shadowFactor *= smoothed vis)
```

**ORIGINAL WFC BEHAVIOR:**
- **It is a baked light-visibility (PVS-like) lookup for light environments only.** It is the same `LightsVisibilitiesVolume` system already recovered. There is no other culling system.
- **Effects by consumer:**
  - Affects **dynamic primitives with a (Dynamic)LightEnvironment:** pawns, vehicles, pickups, and the domination totems, which have `ActiveMeshLightEnvironment`.
  - **Baked lights:** gives their per-position visibility.
  - **Dynamic (unbaked) lights:** not covered; they are ray traced.
  - **Projected character shadows:** only **indirectly**, through the composite light choice and the smoothed-visibility fade of `shadowFactor`.
  - **Particles, BSP, static meshes, static or baked lighting, visibility culling:** no effect.
- **Association:** by **position query** (LightEnv bounds origin). There are no actor lists, touch events, zones or bitsets on actors. Lights are bound by `LightGuid`.
- **When queried:** on a light environment's full update (time-sliced). Crossing the volume boundary takes effect on the next full update of that environment, then goes through the existing per-tick smoothing and transition (earlier note §3.4). It is **not instantaneous**.
- **Outside the volume:** baked lights get visibility 0.

**ASSETTOOLS RELATIONSHIP:** AssetTools lists it as "semantics UNKNOWN". It is the `LightsVisibilitiesVolume` octree already decoded natively. The actor needs its serialized octree blob, which is Rendering's existing decoder input.

**IMPLEMENTATION HANDOFF (Rendering):** wire Streets' volume blob into the existing LV decoder and light-environment query. Add no touch, cull or particle behaviour.

---

## 2. Objective marker type selection

**CONFIDENCE:** CONFIRMED (bytecode + authored defaults + HUD bindings). The Scaleform-side drawing of state is not recovered.

**FUNCTION / CLASS / CALLERS:**

| objective class (Base) | marker add path | marker class (hard-coded) |
|---|---|---|
| TnFlagCapturePoint | `TnFlagCapturePointBase.OnChangeActiveState`: _Active → Add, else Remove. PostBeginPlay returns early unless HasRule(SingleFlagCTF) | `TnObjectiveMarkerTypeFlagCapturePoint` |
| TnBombPlantPoint | `TnBombPlantPointBase.PostBeginPlay`: only if HasRule(ScoreBombingRun) | `TnObjectiveMarkerTypeBombPlantPoint` |
| TnDominationPoint | `TnDominationPointBase.PostBeginPlay`: authority, only if HasRule(ScoreDomination), description "" | `TnObjectiveMarkerTypeDomination` |
| TnKingOfTheHillZone | `TnKingOfTheHillZoneBase.Active.BeginState` adds; `Inactive.BeginState` removes | `TnObjectiveMarkerTypeKingOfTheHill` |
| flag / bomb factories | `TnGameObjectiveWeaponPickupFactory` (authored `MarkerType`) | `TnObjectiveMarkerTypeFlag` / `TnObjectiveMarkerTypeBomb` |

**Marker pipeline:**
- `TnGameReplicationInfoGameBase.AddObjectiveMarker(desc, base, class, bDoNotReplicate)` → `TnObjectiveManager.AddObjectiveMarker`.
  - It assigns a MarkerId and stores the entry in the **replicated array `ObjectiveMarkers[16]`**.
  - Overflow logs "Maximum number of objective markers exceeded".
  - On clients, `ClientInitializeObjectiveMarker` spawns the MarkerType object.
- `TnObjectiveManager.Update(HUD)` runs every HUD tick. For each marker:
  - the authority removes markers whose base is gone;
  - if `MarkerType.ShouldDisplayMarker(observerPawn, data)` → `TnHUD.UpdateObjectiveMarker(data)`.
- **`TnHUD.UpdateObjectiveMarker`:**
  - unless `MarkerType.DrawsSelf` (false for these 4), builds Scaleform args `[MarkerId, Distance(observer pawn → marker), screenX, screenY, screenZ, MarkerTypeString, Description, +AddDynamicParameters]`;
  - calls `HudMovie.Invoke("_global.UpdateMarker", args)`;
  - it is bracketed by `_global.StartMarkerUpdate` / `_global.FinishMarkerUpdate`.
- **Marker type string** = class name with "TnObjectiveMarkerType" removed: **"Domination", "KingOfTheHill", "BombPlantPoint", "FlagCapturePoint"**.
- **Marker location** = the base's `TnTargetableComponent.GetTargetSnapDesiredLocation()`, else `Actor.Location`.

**Visibility (ShouldDisplayMarker):**
- **Domination:** always true.
- **KOTH:** always true; it exists only while its zone is Active.
- **BombPlantPoint:**
  - false if `GRI.AttackingTeam` is 255 or −1;
  - true if the bomb is planted;
  - otherwise true only for the point whose `TeamNum != AttackingTeam` (the defended point).
- **FlagCapturePoint:** true only when the observing pawn holds a flag (`TnWeaponFlagBase`).

**Team / state data present in the marker classes** (`GetMarkerSetup` / `GetLabelText` / `SetupParameters`):
- **Domination:**
  - state 2 friendly (owner team == defender) → TeamID 0, label "Defend";
  - state 0 neutral (defender 255) → TeamID 2;
  - state 1 enemy → TeamID 1;
  - labels for states 0/1 are "Capture";
  - params: `NodeID = PointNumber`, `Flashing = BeingCaptured (CurrentCaptureTime > 0)`;
  - material `UI_HudMarkers_p.MPMarkerDominationNode_MAT`.
- **KOTH:** `Neutral = 1` if (owner team == defender or defender > 1), else 0; labels Defend / Capture; `MPMarkerBase_MAT`.
- **BombPlant:** attacking = (owner team ≠ point team); Neutral 0 if attacking, else 1; Flashing 1; labels Plant / Defuse / Defend.
- **FlagCapturePoint:** Neutral 0, Flashing 1.
- **Note:** **these setup and label functions have no caller in TransGame script.** The Scaleform path passes only the type string and the description. The friendly/enemy/contested presentation is therefore either decided inside the HUD movie or comes from the canvas-path setup, which is not invoked.
- **Separate HUD observer:** in-zone capture progress is a HUD data observer. `TnDominationPointBase.Touch` adds `TnHudDataObserverDominationCapture`, which reports `NormalizedCaptureTime` to non-defenders.

**ORIGINAL WFC BEHAVIOR:**
- The marker type is fixed by the objective's class. It is added or removed by mode gating (HasRule) and by state (KOTH Active; CTF capture-point `_Active`).
- Distance is sent to the movie every tick. No script-side distance cut-off exists for these types.

**ASSETTOOLS RELATIONSHIP:**
- Matches the `future_hud_handoff.json` resources.
- The type strings and the `_global.UpdateMarker` argument order above are the selection key.

**IMPLEMENTATION HANDOFF (Gameplay/UI, later):**
- Feed `UpdateMarker(id, dist, sx, sy, sz, typeString, desc)` per visible marker each frame.
- Use the visibility rules above and the class → type mapping.

---

## 3. Domination totem mode visibility

**CONFIDENCE:** CONFIRMED (bytecode + defaults).

**FUNCTION / CLASS:** `TnDominationPointBase.PostBeginPlay`, `Inactive.BeginState / Touch / UnTouch`, `DefendingTeamChanged`, `UpdateAnimState`. The totem is `PointMesh` (component `PointMesh0`: SkeletalMesh `NEU_EnergonTotem_SKEL`, own `ActiveMeshLightEnvironment`, bCastDynamicShadow false, bForceDirectLightMap).

**PSEUDOCODE:**
```
PostBeginPlay (all net roles):
  PointMesh.StopAnim(); PointMesh.PlayAnim(DeactivatedLoopAnim, loop)          // animation always starts
  if Role != Authority: return
  if !Game.HasRule(TnGameRules_ScoreDomination): InitialState = 'Inactive'; return
  GRI.AddObjectiveMarker("", self, TnObjectiveMarkerTypeDomination)
(engine SetInitialState) -> GotoState(InitialState)
state Inactive: BeginState: SetHidden(true) ; Touch/UnTouch: ignored
DOM: DefendingTeamChanged -> CaptureAnims[team] loop + EnergonColor = CaptureColor[team] (red 0.73,0.13,0.13 / blue 0.27,0.19,0.76);
     neutral -> CaptureColor[0]? (index 0 when 255 path) ; losing -> DeactivateAnim then UpdateAnimState
```

**ORIGINAL WFC BEHAVIOR:**
- **Conquest (DOM):** visible and active. It plays `DeactivatedLoopAnim` until captured, then the team capture anim with the team colour.
- **Every other mode** (CTF, EXT, KOTH, DM, TDM): the whole actor is **hidden** (`SetHidden(true)`), so the totem is not rendered. The actor stays alive.
- **Not hidden in non-DOM modes:**
  - The animation was still started (hidden).
  - The collision cylinder is **not** disabled; only Touch/UnTouch are made no-ops.
  - It is not detached or destroyed.
- `bHidden` replicates: RemoteRole SimulatedProxy, bAlwaysRelevant, NetUpdateFrequency 10. Clients mirror the hidden state.
- No Kismet is involved.

**ASSETTOOLS RELATIONSHIP:** AssetTools' "placed in every mode; behaviour DOM-only" is right about placement. **Visibility is DOM-only too.**

**IMPLEMENTATION HANDOFF:** spawn the three totems only visible in DOM. Elsewhere, hide them (keep the collision cylinder, ignore touches).

---

## 4. Objective-base / objective actor mode filtering (Streets)

**CONFIDENCE:**
- CONFIRMED: script, rule sets and authored Kismet.
- HIGH: native `SeqAct_ToggleHidden` client replication and hidden-collision semantics, both stock UE3.

| actor (Streets count) | CTF | EXT | DOM | KOTH | DM / TDM | mechanism |
|---|---|---|---|---|---|---|
| objective-base InterpActors ×4 (authored bHidden) | **shown** | **shown** | hidden | hidden | hidden | Kismet: GameplayStarted → SeqCond_GameRuleActive(ScoreBombingRun "EXT") / (SingleFlagCTF "CTF") True → SeqAct_ToggleHidden **UnHide** |
| TnGameObjectivePickupFactoryFlag ×2 | active | Disabled | Disabled | Disabled | Disabled | `TnGameObjectiveWeaponPickupFactory.PostBeginPlay`: !HasRule(RequiredGameRuleClass = SingleFlagCTF) → InitialState 'Disabled' (SetHidden + SetCollision(false,false)) |
| TnGameObjectivePickupFactoryBomb ×1 | Disabled | active | Disabled | Disabled | Disabled | same, with RequiredGameRuleClass = ScoreBombingRun |
| TnFlagCapturePoint ×2 | active (marker when `_Active`) | inert | inert | inert | inert | PostBeginPlay returns before TnGameObjective setup unless SingleFlagCTF; no marker |
| TnBombPlantPoint ×2 | inert | active + marker | inert | inert | inert | PostBeginPlay gated on ScoreBombingRun |
| TnDominationPoint ×3 (totem) | hidden | hidden | **active, visible** | hidden | hidden | §3 |
| TnKingOfTheHillZone ×5 (default bHidden) | stays hidden | hidden | hidden | Inactive (hidden); one random zone Active (shown + marker), rotating via ActivateNewZone | hidden | `PostBeginPlay`: HasRule(ScoreKingOfTheHill) → InitialState 'Inactive'; `MatchStarting` → random initial zone |

Notes:
- **Shared base locations:** the flag capture point and bomb plant point share the same ObjectiveVolumes (TriggerVolume_13959 / _4887). That is consistent with the bases being both CTF and EXT bases, hence the two-rule UnHide.
- **InterpActor network role:** RemoteRole None and bNoDelete. Stock UE3 `SeqAct_ToggleHidden` force-net-relevants such actors so clients see the unhide (HIGH, not re-verified in the binary).
- **Hidden InterpActors still collide** (UE3 SetHidden does not change collision; HIGH). The authored instances set no collision overrides.

**ASSETTOOLS RELATIONSHIP:** this complements `streets_kismet.json`. The Kismet unhides the 4 bases in CTF and EXT. Script gates the factories, points, totems and zones as above.

**IMPLEMENTATION HANDOFF:** implement the table. The mode is defined by its Rules list, and every check is an exact rule-class match.

---

## LIGHT-VISIBILITY VOLUME HANDOFF
- CONFIRMED:
  - It is the existing `LightsVisibilitiesVolume` octree.
  - It is queried only by light-environment full updates at the bounds origin.
  - It affects baked-light visibility for light-environment primitives, and therefore character lighting and composite-shadow fading.
  - It has no touch events and no effect on culling, particles or static lighting.
  - Baked lights get visibility 0 outside the volume.
  - Boundary crossings apply on the next full update, then smooth.

## OBJECTIVE MARKER HANDOFF
- CONFIRMED:
  - the marker class is hard-coded per objective class;
  - the replicated marker array holds 16 entries;
  - per-tick `ShouldDisplayMarker`;
  - `_global.UpdateMarker(id, dist, sx, sy, sz, type, desc)`;
  - type strings "Domination" / "KingOfTheHill" / "BombPlantPoint" / "FlagCapturePoint";
  - the per-type visibility rules listed in §2.
- PARTIAL: the friendly/enemy/contested presentation. The script-side setup functions exist but are not called on the Scaleform path.

## DOMINATION TOTEM HANDOFF
- CONFIRMED:
  - visible only in Conquest (DOM);
  - hidden through the `Inactive` state in every other mode;
  - the collision cylinder is kept, touches are ignored;
  - the idle `DeactivatedLoopAnim` always starts;
  - team animations and colours come from `DefendingTeamChanged`.

## OBJECTIVE-BASE MODE HANDOFF
- CONFIRMED:
  - the 4 base InterpActors are unhidden only in CTF and EXT (Kismet);
  - flag and bomb factories are Disabled outside CTF and EXT respectively;
  - capture and plant points are inert outside their mode;
  - KOTH zones are hidden except the active zone in KOTH.

## STILL UNKNOWN
- How the HUD movie renders team, contested and flashing state for "Domination" and "KingOfTheHill" markers (AS2 side; not in this lane's scope).
- Native `SeqAct_ToggleHidden` force-relevance on WFC clients (assumed stock).
- The light-environment update cadence for the totems' own LightEnvironment (they are static actors, so likely updated once).
