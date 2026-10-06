# Energon colour ownership in MP (2026-10-06, milestone 09) — for Integration / Frontend / Gameplay / Systems

Labels: C = read from script or data; H = high confidence.

## (a) Body energon path (C)
- `TnCharacterApplier.ApplyCharacter(CD, P)` → `SaveColors(CD, P.RobotMeshComponent)` → `ExtractColors`:
  - Primary / Secondary: CD colour if ≠ (0,0,0,255), else the mesh material param.
  - **Energon:** `CD.EnergonColor` if ≠ (0,0,0,1) and ≠ (0,0,0,0), else `RobotMesh.GetVectorParam('EnergonColor')`.
  - `MeshComponent.GetVectorParam` walks material slots 0..N−1 and returns the first material (or MIC parent chain) that has the parameter.
- `ApplyColorsToCharacter` → `ApplyColorsToMesh` writes `Cust_Color_A`, `Cust_COLOR_B` and `EnergonColor` back to the meshes. The disguise override colours replace them only while disguised (`TnBuffDisguise` → `SetColorOverride`).
- Faction / replication: `TnCharacterDataHelpers.ResolveReplicatedCharacterData(CD, Faction)` picks per-faction chassis, PrimaryColors[i], SecondaryColors[i] and MeleeWeapons[i]. **EnergonColor is a single value, copied unchanged.**
- **No team override exists:**
  - no script sets a pawn mesh's EnergonColor from a TeamInfo, PRI or game mode (all `SetVectorParam` / `SetColorParameter` sites enumerated);
  - natively, the "EnergonColor" strings are referenced only by class/property registration (`0x83612160`).
- Same source for: vehicle FX (`TnVehicleFxPlayer`), faction-effect notifies (`TnAnimNotify_PlayFactionEffect`), the car boost colour (lerp energon → yellow), particle params (`TnParticleSystemParameterEnergonColor`), and the sentry / roller-mine / kamikaze-mine meshes (instigator's `ApplyColorsToMesh`).

## (b) Uses of the team EnergonColor class defaults (C)
- `TnTeamInfo` (0.843, 0.302, 0.029), `TnFactionTeamAutobots` (1.25, 0.05, 0.05), `TnFactionTeamDecepticons` (0.2, 0.1, 1.5). They are read in only two places, both fallbacks:
  1. `TnProjectileKamikazeMine.ClientSetEnergonColor`: the mine mesh uses `Team.default.EnergonColor` **only when it has no instigator pawn** (e.g. its owner is dead or gone). Otherwise it uses the instigator's character colours.
  2. `TnParticleSystemParameterEnergonColor.Apply`: for a PSC owned by a kamikaze mine with a team, the team energon is used.
- Not used for HUD, name plates, markers or bodies.
  - `Engine.TeamInfo.TeamColor` / `GetHUDColor` have no script callers.
  - Objective meshes use their own `CaptureColor[team]`:
    - Domination `EnergonColor` param: (0.7299, 0.1275, 0.1275) / (0.2673, 0.1869, 0.7593);
    - KOTH `Color` + `RayColor`: same values; NeutralColor (0.805, 0.302, 0.029).
  - H: HUD team colours live in the GFx movies.

## (c) Character with no customisation (C path; H on data)
- `CD.EnergonColor` (0,0,0,0) → the **robot mesh material's `EnergonColor` default**: first material slot defining it, after any component material overrides.
- The ini sets no per-character energon; AI character definitions carry their own `EnergonColor` (`notes/data/ai_definitions.json`).
- So the default is per chassis material, not a class or team constant. AssetTools should export the material defaults.
