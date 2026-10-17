# Campaign material gaps: shipped shader decodes for the translator (RE, 2026-10-18)

For Rendering's translator. These are the 38 campaign materials that don't compile today (Rebuild CAMPAIGN_ASSETS_SUMMARY: 23
new-expression-node, 12 DecalMaterial-rooted, 3 ShaderCode ddy / acos).

Method:
- `tools/shadermap_scan.py` finds each material's cooked shader map (per vertex factory);
- `tools/shader_by_guid.py` dumps the Xenos microcode and CTAB.

Labels: C = microcode / CTAB read; H = inference. Raw dumps: work/q/decal_ps.txt.

## Batch A: DecalMaterial roots (12)

### A.0 What a DecalMaterial is (C)
- Each DecalMaterial is cooked with **two VF sets**: FLocalVertexFactory / GPU-skin (the material on ordinary meshes) **and**
  FLocalDecalVertexFactory / FGPUSkinDecalVertexFactory / FGPUSkinMorphDecalVertexFactory (projected onto receivers).
- The pixel-shader body is the ordinary material graph. **Translate it exactly like a Material**; accept DecalMaterial as a
  chain root.
- The decal-specific part is all in the **decal vertex factory**:
  - **UV0** (decal VS 9c56c0b4… / 8930f347…):
    `uv = 0.5 − (DecalWorldToTexCoordMatrix · (WorldPos − DecalWorldLocation)).xy + DecalOffset`.
    - The matrix rows are c5–c8; WorldPos includes PreViewTranslation.
    - H: the 4th row enters through a term derived from the vertex w, which is 0 for normal geometry.
    - So the texture is projected from the decal frame, centred at 0.5.
  - **Tangent frame in the PS:** `DecalWorldTangent` (c20) and `DecalWorldBitangent` (c21), normalised, replace the mesh tangents.
    The normal comes from the receiver. This matters only for graphs that use tangent-space normals (DarkEnergon below).
  - The translucent decal VS also computes the 4-layer height fog (Fog* constants), like other translucency.
- Blend mode comes from the material (Translucent / Modulate / Masked below).

### A.1 PROP_FloorStains_p.DECAL_stains_02 / 03 / 04_MAT (Translucent, Unlit; PS f73099fc / 4fae11fe / f6095cb5, identical code)
- `t = Texture2D_0(uv).r`.
- `a = (1 − t) · UniformScalar_0`; **clip if a < 1/255**.
- `rgb = (VC.rgb + VC.a · UniformVector_0.rgb) · SceneColorBiasFactor`, where VC = the interpolated vertex-colour input of the decal VF.
- out = (rgb, a).

### A.2 PROP_FloorStains_p.DECAL_stains_01_MAT (Translucent, Unlit; PS 133e1daf)
- Like A.1, but the mask uses the green channel scaled: `t = tex.g · (1 + UniformVector_1.x)`.
- `a = (1 − t) · UniformScalar_0`; clip below 1/255.
- rgb as A.1.

### A.3 ENV_KON_arrowDecal_MAT, ENV_KON_HazardSignDecal_MAT, ENV_IAC_LightSources CustomShadowDecal_01_MAT (Modulate; one shared PS 9bfcffb4)
- All three compile to the **same** shader (only textures / params differ):
  `rgb = (tex.rgb + UniformVector_0.rgb) + (1 − UniformVector_0.rgb) · NoLightMapColor`; alpha unchanged.
- Modulate-blended (dest × src): white = no change.
- Lightmapped permutations exist (vertex / texture directional lightmap policies, 9 PS total). Use the NoLightMap form for decals
  projected at runtime.

### A.4 ENV_KON_GrungeDecals_p.DarkEnergon_Spread_MAT + 4 instances (Masked, Unlit; PS ed761550)
- A full graph:
  - 5 textures + a cube map;
  - **tangent-space normal** (two normal fetches blended, one at UV × const), built with the decal tangent / bitangent frame;
  - a view vector from WorldPos − PreViewTranslation → **reflection vector into TextureCube_0** with an explicit LOD (UniformScalar);
  - **Fresnel / specular** via pow (log / exp) with UniformScalar exponents;
  - a luminance desaturate (0.3, 0.59, 0.11) lerp.
  - **Opacity mask:** clip if `mask − OpacityMaskClipValue < 0`.
  - Output × SceneColorBiasFactor.
- The node graph already translates (it's the same nodes as other env materials). Only the root type and the decal tangent frame
  are new.
- Instances: DarkEnergon_Spreading / 01 / 02 / 03_MAT_INST (parameter overrides only).

### A.5 Two of the 12 aren't DecalMaterial in the cache (C)
- `ENV_IAC_Ground_p.Decal_Crater_Orange_MAT` and `ENV_KON_PrisonBarge_p.DomeDeco_01_Warm_Alt_Decal` are labelled **Material** in the
  shader cache. They have full lit permutations (spot / directional shadow-mask light shaders, depth, velocity) plus the decal VF
  set.
- So they are ordinary lit Materials with bUsedWithDecals, and they need no special root. If AssetTools reports them as "no
  master", that's a parent-chain lookup issue, not a decal root. Check their chain in authored.db.
