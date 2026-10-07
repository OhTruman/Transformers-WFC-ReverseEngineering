# Objective / player markers: full handoff (Milestone E, 2026-10-07)

Labels: C = from script (`work/script/decomp`) + authored defaults (`notes/data/objective_marker_types.json`, INT localisation); H = high confidence; U = unknown.
This builds on `MILESTONE05_GAMEPLAY_UNKNOWNS.md` §5 (per-type state tables, still valid) and `MILESTONE04_STREETS_RUNTIME_SEMANTICS.md` §2.
**Correction to M04 §2:** gameplay markers are **not** drawn by Scaleform. See the draw path below.

## 1. Pipeline (C)
- **Registration:** `GRI.AddObjectiveMarker(Description, MarkerBase, MarkerTypeClass, bDoNotReplicate)` → `TnObjectiveManager.AddObjectiveMarker`.
  - It assigns a MarkerId and stores the entry in the replicated `ObjectiveMarkers[16]`. Overflow logs "Maximum number of objective markers exceeded".
  - **Correction (2026-10-07, C):** `bDoNotReplicate` entries go to the unbounded client-local list `LocalObjectiveMarkers` (`AddLocalObjectiveMarker`), not the replicated 16. Player tags (`TnPawn`, DoNotReplicate true) and tombstones are local, so the 16 cap applies only to replicated objective markers (flag / bomb / nodes / plant points / KOTH / capture points). **16 v 16 does not need a larger cap for tags.**
  - Clients spawn the MarkerType object in `ClientInitializeObjectiveMarker`.
- **Who registers what:**

| Source | Marker class |
|---|---|
| every pawn (`GameClass.TransformerMarkerClass`) | versus: `TnObjectiveMarkerTypeTransformerVersus` (Description = character name) |
| DOM points (if `HasRule(ScoreDomination)`) | `TnObjectiveMarkerTypeDomination` |
| KOTH zone while Active (removed when Inactive) | `TnObjectiveMarkerTypeKingOfTheHill` |
| EXT plant points (if `HasRule(ScoreBombingRun)`) | `TnObjectiveMarkerTypeBombPlantPoint` |
| CTF capture point while `_Active` (the attackers' own capture point) | `TnObjectiveMarkerTypeFlagCapturePoint` |
| flag / bomb factory: the marker **follows the current holder** (factory in Pickup → carrying pawn → dropped pickup; none while Sleeping) | `TnObjectiveMarkerTypeFlag` / `TnObjectiveMarkerTypeBomb` |
| deaths | `TnObjectiveMarkerTypeTombstone` |
| sentry / ammo beacon / decoy / grenades | `…SentryAbility`, `…AmmoBeacon`, `…DecoyTrap`, `…Grenade` |

- **Removal:** explicit `RemoveObjectiveMarker` by the owner (state change, holder change). `TnObjectiveManager.Update` (authority) also removes entries whose `MarkerBase` is gone.
- **Per HUD frame:** `TnObjectiveManager.Update(HUD)`. For each entry with `MarkerType.ShouldDisplayMarker(viewerPawn, data)` → `TnHUD.UpdateObjectiveMarker(data)`, skipped while the HUD is hidden or the game is paused.
- **Draw path** (`TnHUD.UpdateObjectiveMarker`):
  - `MarkerType.DrawsSelf()` = **true for every `TnObjectiveMarkerTypeSprite` subclass**, i.e. all gameplay markers → `MarkerType.Draw(...)` on the **Canvas**.
  - Only non-sprite types (base `TnObjectiveMarkerType`, e.g. LockOn) go to Scaleform `_global.UpdateMarker` (id, distance, screen x/y/z, type string, description, dynamic params).
- **Position source:** `TnHUD.GetMarkerLocation` = the base's `TnTargetableComponent.GetTargetSnapDesiredLocation()` if present, else `MarkerBase.Location`. The sprite then adds `(0, 0, Setup.MarkerZOffsetWS)`, e.g. AmmoBeacon 300; most are 0.

## 2. Sprite drawing (C, `TnObjectiveMarkerTypeSprite`)
- **Sizes are fractions of canvas WIDTH:** `SizeInPixels(f) = f × Canvas.SizeX`, also used for 2-D offsets. **Constant on-screen size: no distance scaling and no distance fade on any MP marker.**
- `IsOffscreen`: projected Z < 0 (behind the camera), or outside the safe frame inset by `SafeFramePaddingPercent` 0.08 of the width (x) / height (y).
- **Off-screen:** drawn only if `Setup.DrawWhenOffscreen`. The direction from the screen centre (flipped if behind) is intersected with the safe-frame rectangle (`IntersectWithSafeFrame`).
  - Material param `ArrowAngle` = acos(dir.y)·sign(dir.x) + 180.
  - Size `OffscreenMarkerSize`. Label only if `DrawLabelWhenOffscreen`.
- **Focus:**
  - Focused if within `DistanceFromCenterFocusThreshold × SizeX` of the screen centre (default 0.0625; boss types 0.156), or if `AutoFocusRange` > 0 and the world distance is below it (TransformerVersus 3000 UU).
  - Focus persists `FocusHysterisis` (0.2 s; TransformerVersus 1.0 s), and the label alpha fades over it.
  - Focused: `FocusedMarkerSize` tile, material `Over = 1`. Unfocused: `UnfocusedMarkerSize`, `Over = 0`.
- **Tile:** `DrawMaterialTile(MatInst, size, size)` centred on the projected point.
- **Label:** `DrawTextCA` (centre-aligned) at Project(markerLoc + (0, 0, `LabelZOffsetWS`)) + `LabelOffset × SizeX`; font `UI_TransEngineFonts_p.MarkerFont`; colour from the setup, alpha × transparency.
  - Shown when focused if `DrawLabelWhenFocused`, unfocused if `DrawLabelWhenUnfocused`.
- **Label colours:** Friendly (80, 181, 213), Enemy (240, 60, 60), Neutral white; versus enemy tags (240, 20, 20).
- **Health bar** (`DrawHealthBar`): `HealthBarMat` tile at the label position + `HealthBarOffsetFromLabel × SizeX`, size `HealthBarSize × SizeX` (Transformer 0.06 × 0.015). Params `Health` = the pawn's normalised health (`GetNormalizedHealth`) and `Neutral` = (FillColor == HBFC_Blue ? 1 : 0).

## 3. Per-field semantics
1. **DistanceLabel** (`TnObjectiveMarkerTypeObjective` only; campaign objectives): text = `DistanceLabel` with "`d" replaced by int(|marker − viewer| / 10). INT value is "`d" (the number alone). Units are UU/10. No MP marker uses it.
2. **DrawCutoffDistance** (Grenade 4000 UU): `ShouldDisplayMarker` false beyond it, so the whole marker is hidden, including off-screen.
3. **FadeOutTime** (Tombstone 3 s): when `MarkerBase.LifeSpan < FadeOutTime`, material param `Alpha = LifeSpan / FadeOutTime` (linear to 0). There is no fade on generic removal.
4. **PulseFrequency 2.5 / PulseExpPower 5** (CarriedObjective: flag / bomb): pulse = ((P − (t mod P)) / P)^5, a sharp saw-tooth that decays from 1 every 2.5 s. Used while an enemy carries the objective, for material param `PingOpacity` and label alpha.
5. **FillColor** (`HBFC_Blue` = 0, `HBFC_Red`): health-bar material param `Neutral` = 1 for blue, 0 for red. TransformerHealthBar defaults Red; SentryAbility Blue.
6. **EnemyMarkerHysterisis** 0.25 s (`TnObjectiveMarkerTypeTransformerHealthBar`): shown only while `now − Mesh.LastRenderTime < 0.25` and the health-display service allows it, i.e. it vanishes 0.25 s after the target was last rendered.
7. **Action labels** (localised in the TransGame.int section of the same class name; INT values shown):

| Class | State → label |
|---|---|
| Flag (`GetObjectiveState`: 0 at factory, 1 dropped, 2 carried by viewer's team, 3 carried by enemy) | 0: viewer attacking → "Capture", else "Defend"; 1: attacking → "Capture", else "Return"; 2: "Escort"; 3: "Kill" |
| Bomb (same states) | 0/1: "Bomb"; 2: "Escort"; 3: "Kill" |
| BombPlantPoint | `IsAttacking` (point team ≠ viewer team): planted → "Defuse", not planted → "Plant"; otherwise "Defend" |
| Domination / KOTH | owned by the viewer's team → "Defend", else "Capture" |
| TransformerCampaign | downed non-buddy → "Revive"; AI with `_ShouldDisplayName` false → ""; else the name |
| Transformer tags (versus) | the character name (Description) |

- "Attacking" for Flag / Bomb / Carried = viewer team == `GRI.AttackingTeam`.

## 4. Visibility rules (ShouldDisplayMarker) (C)
- **Domination, KOTH, Tombstone:** always. They exist only while relevant: KOTH only for the active zone.
- **BombPlantPoint:** hidden when the GRI has no attacking team. Once a bomb is planted, shown to everyone. Otherwise only the point not owned by the attacking team (the defended target), shown to **both** teams.
- **FlagCapturePoint:** only for a viewer currently carrying a `TnWeaponFlagBase`.
- **Flag / Bomb (carried objective):** everyone except the carrier, in every state (home, dropped, carried).
- **Grenade:** within 4000 UU.
- **TransformerVersus:**
  - Not for yourself or dead pawns.
  - Allies always, but off-screen only while downed.
  - Enemies only with SeeEnemyObjectiveMarkers (unless the target has a Warcry-derived buff), HardLocked by the viewer or a teammate, or RevengeMarker.
  - Disguised enemies use the ally setup but need line of sight. Enemy labels are hidden while the target is cloaked or out of line of sight.

## 5. Per-viewer setup (team colours) (C)
- **Flag / Bomb:** by **viewer vs `GRI.AttackingTeam`** and by holder team.
  - At factory: `Neutral` 0 if the viewer is attacking, 1 if defending; Flashing 0.
  - Dropped: Neutral 0; Flashing 1 if attacking.
  - Carried by a teammate: Neutral 1. Carried by an enemy: Neutral 0 + `PingOpacity` pulse.
  - Label colour friendly if Neutral == 1, else enemy.
- **BombPlantPoint:** by viewer team vs the **point's authored team** (`TeamNum`): attacking ⇔ different team. Neutral 0 if attacking, else 1; Flashing 1.
- **Domination:** by viewer team vs the point's current **owner (DefenderTeamIndex)**: own → TeamID 0 (friendly, "Defend"), 255 → 2 (neutral), enemy → 1. `NodeID = PointNumber`, `Flashing = BeingCaptured` (CurrentCaptureTime > 0). Capture progress itself is the separate HUD observer `TnHudDataObserverDominationCapture` (`NormalizedCaptureTime`, non-defenders inside the zone).
- **KOTH:** owner == viewer team, or owner > 1 (neutral / contested) → Neutral 1, friendly colour; enemy-owned → Neutral 0.
- **FlagCapturePoint:** Neutral 0, Flashing 1.
- The colours themselves are inside the `UI_HudMarkers_p` materials (params above).

## 6. Crosshair target type / name / health (C)
- `TnHudDataObserverTargetType` → `_global.NotifyTargetTypeChanged(type)`, enum `ETargetTypeForHud` {0 TTFH_Friend, 1 TTFH_Enemy, 2 TTFH_None}.
  - Target = aim-assist target if valid → else the crosshair target if valid → else the repair target. Only `Pawn`s count (players, AI, sentries, vehicles-as-pawns); destructibles give None.
  - Type = Friend if `TnTeamInfo.AreOnSameTeam(viewer, target)`, else Enemy. A valid assist / crosshair target defaults to Enemy; nothing → None.
  - AS: the crosshair colour tweens over 0.2 s: Friend 0x50B5D5, Enemy 0xFF3333, None white.
- Target name: `PC.GetCurrentTargetName()` = the target pawn's `PRI.PlayerName`, only for a crosshair target that is a **direct hit** (`IsTargetDirectHit`) and has a PRI; else "".
- Target health: `PC.GetTargetHealthDisplay` → the target's `TnHealthDisplayService` (if `ShouldDisplayHealth`): `DisplayType` (`ETnHealthDisplayType` {HDT_Friendly, HDT_Enemy, HDT_None}) and `NormalizedHealth`; default None / −1.

## 7. Tombstones (C)
- `TnMultiplayerGame.Killed`: for every killed pawn whose controller is a **TnPlayerController** (all versus modes; AI deaths make none), spawn `TransContent.TnTombstone` at `KilledPawn.Location`, then `set_TeamNum(victim team)`.
- `TnTombstone` defaults: **LifeSpan 8 s**, bNetTemporary, SimulatedProxy. Its SpawnModifier rule: Factor −5 within 5000 UU.
- The marker is added locally on server and clients (`AddObjectiveMarker("", self, TnObjectiveMarkerTypeTombstone, DoNotReplicate = true)` from PostBeginPlay / `set_TeamNum` / `ReplicatedEvent(_TeamNum)`).
- **`ShouldDisplayMarker` = true: every viewer sees every tombstone**, with no team filter.
- Fade: material `Alpha` = LifeSpan / 3 over the last 3 s (fully visible for the first 5 s). It disappears when the actor expires.
- H: AddMarker can run more than once per tombstone (PostBeginPlay + TeamNum set / replication). The original has no de-dupe in `AddLocalObjectiveMarker`, so duplicates draw identically on the same spot.
- **No generic removal fade** exists for any other marker type.
