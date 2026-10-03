# MP_IAC_Streets fidelity — remaining items (2026-10-03)

**Sources:**
- Cooked `MP_IAC_Streets_{ART,BASE}_m` (read in place).
- AssetTools a23c675+ manifests and the corrected `world.glb` (2026-10-02 23:45).
- Rendering's read-only work data: `lighting.json`, `permutation_check.json`.
- New read-only tool `tools/glbray.py` (GLB loader and numpy ray caster).
- **Visibility method used below:** ray-cast from each face along the line to the nearest front-side gameplay viewpoints. Viewpoints: 282 player starts, pickups, objectives and nav points, each raised 3 m to approximate camera height. Occluders: every mesh and BSP triangle in the corrected `world.glb`. This is a coarse test (HIGH for "not visible", PARTIAL for "visible").

Item 4 (particle module lists) is in `MILESTONE04_STREETS_FIDELITY_PARTICLE_LISTS.md`.

---

## 1. EngineMaterials.DefaultMaterial BSP surfaces

**CONFIRMED (data) / HIGH (visibility).**
- They are **explicit cooked material references** to `EngineMaterials.DefaultMaterial` (62 surfaces, 87 polygon nodes, ~47,700 m²). They are not null pointers resolved at run time.
- Each node is in a cooked FModelElement with that material, so the original **renders** them with the engine default material. PolyFlags: none set; not invisible, not portal.
- **Visibility:** only **1 of 87 nodes** (≈33 m², the face at (35840, −38592, −70848) facing +Y) is visible from any gameplay viewpoint.
  - The rest are rooftops (+Z faces ~28 m above the street), undersides (−Z faces) and outward-facing shell walls.
  - Only 13 of 87 have a mesh within 1 m in front, so they are **structurally out of sight, not mesh-covered**.
- **Rendering handoff:** keep them rendered with DefaultMaterial, as in the original. Expect them to appear only outside normal camera reach.
  - The one possibly visible face is PARTIAL. Check it in a capture before treating it as a defect.

## 2. Mirrored `Arch_4096_STAT` black vertex-lit patch (SMCA_7201 / StaticMeshActor_2542_SMC)

**CONFIRMED: authentic shipped data.**
- Decoding the shipped vertex light map (522 samples, 3 directional coefficients each) gives **30 samples near zero in all three coefficients**: indices 98–101, 217–220, 237–244, 262–269, 275, 276, 437, 508, 517, 521. 12 more are zero in some coefficients.
- A sample that is zero in every directional coefficient is black for **any** normal or tangent basis. So no native mirroring, tangent-flip or winding rule can light it.
- The sibling in the same collection, `StaticMeshActor_15855_SMC`, is zero at **28 of the same 30 indices**. That is the bake's contact / occlusion pattern for this arch pair, not an instance-specific error.
- Native negative-scale handling (earlier note): winding swap plus cofactor normals. Rendering already applies both.
- **Rendering handoff:** leave it as authored. **No fix.**

## 3. Monitor / display screen materials

**CONFIRMED.**
- **Family:** `PROP_NEU_Monitors_p.MonitorScreen_Parent_MAT`, with instances in Streets:
  - `MonitorScreenActive_MAT_INST` (no overrides);
  - `MonitorScreenActivePurple_MATINST` (Edge_Burn 2.0, ScanlinePan 0.5, ImagePan 0.25, Screen_Color (0.22, 0.22, 1.0));
  - `MonitorScreenDead_MAT_INST` (ScanlinePan 3.0, ImagePan 0.05, Screen_Color (0.31, 0.30, 0.30); Edge_Burn inherits 1.2).
- **Graph:** emissive only.
  - Two `Panner`s (SpeedY +0.2 / −0.2) driven by `Time × ImagePan_Speed / ScanlinePan_Speed`.
  - Two plain `TextureSample`s of `ScreenText`, plus a `TextureSampleParameter2D 'Texture'` (default `ScreenText`).
  - `Edge_Burn` drives a Power term; tinted by `Screen_Color`.
  - **There is no render target, movie, script parameter or Kismet driver.** The screens change only through material Time. They are continuous scroll animations that loop by texture wrap.
- **Compiled resource** (cooked native tail):
  - scalar parameters Edge_Burn, ScanlinePan_Speed, ImagePan_Speed; vector parameters Screen_Color, SelectionColor; Time; FoldedMath and Clamp uniforms;
  - a separate texture-expression block: `u32 2`, then `FMaterialUniformExpressionTexture` → `ScreenText` and **`FMaterialUniformExpressionTextureParameter 'Texture'`** → default `ScreenText`.
- **So Rendering's translation (which reads `Texture`) is correct.** `verify_permutations.py` misses this texture block, so its "Texture: []" compiled list and the MonitorScreen PARTIAL are a verifier false negative.
- **Rendering handoff:**
  - mark the MonitorScreen family as matching;
  - fix the verifier to read the texture-expression block (count, then {FName class, number, [param FName, number,] texture ref});
  - animate with material Time only.

## 5. Destructible wall panel

**Not pursued.** `TnStaticDestructibleActor_14465` is at (896, 89968, −352), ~139k UU from the play space (Rendering's own finding), so it cannot be seen in normal play. Its state logic is in `MILESTONE03_RUNTIME_SEMANTICS_ASSETTOOLS_7a69756.md` P5B.

## 6. BSP elements without lightmaps (Rendering "PROV dynamic light environment")

**PARTIAL.**
- Of 889 BSP polygon nodes, **616** belong to elements with LightMapType 0 (no lightmap, shadow maps or irrelevant lights); 273 have texture lightmaps.
- **Visibility:** **26 of the 616 nodes (≈3,694 m², ~9 % of their area) are visible from gameplay viewpoints.**
  - They are mainly large vertical faces on the west perimeter (x = −3840, facing −X) and two +Y faces at (3456 / 13120, −26624).
  - The remaining 590 are structural or out of sight.
- **Runtime lighting of those 26:** UE3 decides a model element's interaction with each light from its lightmap GUIDs and IrrelevantLights list. A light in neither list gives an *uncached* interaction, which is rendered dynamically.
  - That is stock UE3 (HIGH as the engine rule). It is **not traced in WFC's native code** in this pass.
  - Whether any Streets light actually reaches these faces, and with which channels, is UNKNOWN.
- **Rendering handoff:**
  - only these 26 faces matter visually. The list is reproducible with `tools/glbray.py` and the method above.
  - Keep the current provisional treatment for them, and don't spend effort on the 590 out-of-sight elements.

## Not needed for visuals
- The LightsVisibilitiesVolume octree float at +0x18 is not read by the query (earlier note). No visible effect.

## SUMMARY HANDOFF
- **Rendering:**
  - DefaultMaterial BSP: render as-is (essentially never visible).
  - Arch patch: authentic.
  - Monitors: translation correct; the verifier needs a fix; Time-only animation.
  - Unlit BSP: only 26 visible faces matter (PARTIAL lighting rule).
  - Particle lists: see the separate note.
- **AssetTools:**
  - `m04_bsp` DefaultMaterial surfaces are explicit cooked references; label them "rendered, structurally hidden".
  - The material-resource texture-expression block layout above (for any material audits).
- **Gameplay:** nothing in these items.
