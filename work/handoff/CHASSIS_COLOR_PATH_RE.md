# Custom chassis colour: from the picked swatch to the material (RE, 2026-10-23; QC item 22)

**Labels:** C = script bytecode / authored.db.

## 1. Where the colour comes from (C)
- **Not from a colour table.** Character create stores **FColor PrimaryColors / SecondaryColors** per faction, plus the palette id
  and pixel coordinates (`PrimaryColorPalettes`, `PrimaryColorCoords`).
- The UI shows `GetPixelColor(palette, x, y)`: **the swatch texture's pixel** (sRGB) when the stored colour is the "use default"
  value. Otherwise it shows the stored hex.
- **So the palette values are the palette textures' pixels** (UI_CustomChar_p). AssetTools can dump them.

## 2. The transform (C, `TnCharacterApplier.ExtractColors` → `Object.SRGBColorToLinearColor`)
- **Formula:** `linear = (c / 255) ^ 2.2` per channel; alpha c / 255. That's a **plain 2.2 power, not the piecewise sRGB curve**.
- **No multiplier or intensity scalar in script.**
- **"Use default"** = FColor (0, 0, 0, **255**). That colour reads the mesh's existing parameter (`GetVectorParam`) instead.
- **Energon:** stored as a LinearColor, used raw. The default is (0, 0, 0, 1) or (0, 0, 0, 0).
- **Your piecewise sRGB → linear step matches within ~2 %** (0.5 → 0.214 piecewise vs 0.218 with 2.2), so **it isn't the cause of
  "too subtle".**

## 3. Where it's applied (C, `ApplyColorsToCharacter`)
- The **same three values** (`Cust_Color_A`, `Cust_COLOR_B`, `EnergonColor`; the CDO names) are set on:
  - the robot mesh;
  - the vehicle mesh;
  - the robot-form arm mesh;
  - the current weapon's animated mesh.
- They're applied on every material of those components (SetVectorParam on the MeshComponent).

## 4. What the material does with it: the likely "subtle" cause (C, TR_AllShader_p.Release.CHR_Transformer_NormSpec_Cust_E_Mat)
- **The colour isn't a straight albedo:**
  - `Cust_Color_A` → StaticSwitch `Use_Neutral_Lut` / `Enable_Autobot_Lut` (A = a LUT texture, B = the parameter);
  - `Cust_COLOR_B` → StaticSwitch `Enable_Decepticon_Lut` (A = `Decepticon_SoldierCustomColorLUT`, B = the parameter).
  - When an instance turns a LUT switch on, **the custom colour is ignored** and the LUT is used. H: AI-soldier instances.
- **The mix:** `lerp(lerp(Grunge_Map, ColA, CustClrAlphasMap), ColB, CustClrAlphasMap)` (separate mask channels).
- **Then:**
  - **× `Lum_Map`** (a per-model luminance texture);
  - **× `ColorBrightness`**: master 1.0. **Per-instance values:** 1.0 (47 instances), **2.0 (27)**, 1.5 (13), 0.5 (7), 0.6–0.75 (10).
    For example Optimus robot INST_B is 1.5 and Optimus vehicle Cust2 is 0.6.
  - `Desaturation(Percent = Color_Saturation)`: master **−0.15**, i.e. **boosted** saturation. Optimus INST_B is −0.05.
  - the specular path has its own `SpecularColor_Desaturation`.
- **So if the rebuild's translated graph drops or defaults `ColorBrightness`, `Color_Saturation` or the static LUT switches, or
  samples `Lum_Map` / `CustClrAlphasMap` channels wrongly, the custom colour reads weak on exactly the models whose instances use
  1.5–2.0.**
- Check those instance scalars first.
