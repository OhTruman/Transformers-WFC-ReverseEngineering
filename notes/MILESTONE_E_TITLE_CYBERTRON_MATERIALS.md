# Title / menu Cybertron planet materials (Milestone E, 2026-10-06)

Labels: C = from material graphs in authored.db (`tools/matgraph.py <Material> EmissiveColor`); H = high confidence; U = unknown.

**Inner city layers** (`ENV_NEU_CybertronOrbit_P.ENV_NEU_CybertronLow{Kaon,Blast,Iocon,Surface,Web,Crust}_Mat`, Kaon shown; the others follow the same template with their own textures and tiling):

```
Emissive = <Region>Buildings_EMISS(UV0) * EMISSMask(UV1*7, pan U 0.005/s) * EMISSMask(UV1*7, pan V 0.005/s) * 1.0   // twinkling sparse lights
         + <Region>Buildings_Illum(UV1) * 0.5                                                                          // base city glow (dense)
         + pow(saturate(dot(N, CameraVector)), 70) * VectorParam(0.0802, 0.1542, 0.2084) * 2.0                         // view-facing sheen
Diffuse  = Buildings_clr(UV0)  (lit)
```
- EMISSMask tiling per material: Kaon 7, Blast 5, Iocon 15 (UV1).
- **The `_Illum` term uses UV channel 1** and is not masked, so it lights the whole region at 0.5×. The masked EMISS term only adds the sparse twinkles.
- So "near-black with sparse orange speckles" = Illum missing (or sampled with UV0 / a mesh without UV1) and only the masked EMISS visible. H: not original.
- **Core** (`LowCore_Mat`): Emissive = Core_Emmis × (1, 1, 2). The diffuse is lit.
- **Shell** (`LowShell_Mat`):
  - Fresnel cubemap rim: `pow(1 − N·V, 3) × Iacon_Streets_CubeMap(swizzled reflection) × (0.101, 0.334, 0.632) × 1.5`;
  - plus the packed Shell_Emiss channel terms (`pow(x, 4) + x` on a float3(A, B·3, C·C)), plus anisotropic spec params (AnisoIntensity 50, Aniso_X/Y/Z 1 / 0.1 / 0.1).
- **No scalar parameters on the inner-layer materials** (only the sheen VectorParameter). There are no MICs over them in this package. Title Matinee `InterpTrackFloatMaterialParam` tracks (Opacity, DownScaleUVs, PulseEmissiveMultiplier in `UI_FrontEnd_m` Main_Sequence) name parameters these materials do not have. So **no Matinee-driven parameter can be holding the city layers dark**.
- Original captures: none in the read scope (only campaign FMV .bik in the dump).
