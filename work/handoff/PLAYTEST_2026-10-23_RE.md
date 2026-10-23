# User playtest 2026-10-23: original values for #11, #12, #15, #8 (RE)

Data: `notes/data/weapon_mp_table.json` (`tools/weapon_mp_table.py`). Labels: C = authored data / script; H = inference.

**The data rule** (C, TnWeapon.GivenTo): versus uses each weapon's **MultiplayerData**. **If a weapon has none, it uses PlayerData**,
the campaign row: AssaultRifle, BurstRifle, EmpShotgun, Shotgun, HeavyMG, RepairRay. Projectile damage comes from the
projectile's own MultiplayerData / Data (`*_PROJDATA`).

## #11 Spread, recoil, aim assist

### Spread (C, TnWeapon)
- `CurrentSpread` starts at **Modifier.Min**; **each shot adds ModifierChangePerShot** (clamped to Max).
- When not firing it **recovers by (Max − Min) × dt / Cooldown**, i.e. a full recovery in *Cooldown* seconds.
- The aim offset = X + rand·spread·Y + rand·spread·Z: spread is the **tangent of the cone half-angle**.
- Multipliers:
  - **fine aim** (zoom) × FineAimSpreadModifier;
  - the pawn's spread modifier: **airborne × 2.0** (0.25 s ramp-up, 0.5 s ramp-down on landing, 0.1 s from hover);
  - the TnBuffDecreaseWeaponSpread buff;
  - per-difficulty SpreadMultipliers (the MP index 0).

### Spread application, exact (C, added after Gameplay's question)
- **Offset = the stock UE3 Weapon.AddSpread:** RandY = FRand() − 0.5; RandZ = Sqrt(0.5 − RandY²)·(FRand() − 0.5); aim = X + RandY·S·Y +
  RandZ·S·Z. That's a roughly disc-shaped cone of about **±0.5·S** (a uniform ±1 square would be twice as wide).
- **S** = Data.Spread[mode] (0) + Pawn.GetWeaponSpreadModifier()
  = CurrentSpread × SpreadMultipliers[0] × the DecreaseWeaponSpread buff, then × airborne (1 → 2) × FineAimSpreadModifier when zoomed.
  The airborne and zoom factors apply **in robot form only**.
- IncrementSpread runs once per fire call, after all pellets.
- **Shotgun / EMPShotgun use a fixed SpreadPattern** (8 / 13 offsets, no randomness), scaled by GetSpread() / GetInitialSpread().

### Recoil (C)
- `RecoilCameraParams`: PitchAdjustmentDeg (camera kick up per shot), RecoilTime, RecoilDelay. Plus CameraShakeParams
  (WEAPON_CAMERA_SHAKE_RE).

### Per weapon (versus; TTK assumes 300 HP and every hit landing, no range falloff / headshots: H)

| weapon | data | damage | pellets | interval s | auto | clip | reload s | DPS | shots to kill | TTK s | spread min | spread max | +/shot | recover s | fine-aim × | recoil ° | snap range | equip s | put-down s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AssaultRifle | Player | 18 | 1 | 0.095 | | 32 | 1.5 | 189.5 | 17 | 1.52 | 0.06 | 0.15 | 0.005 | 3 | 0.5 | 0.05 | 1000–10000 | 0.2 | 0.5 |
| BurstRifle | Player | 29 | 1 | 0.1 | burst | 24 | 1.5 | 290 | 11 | 1.0 | 0.05 | 0.12 | 0.01 | 2 | | | 1000–10000 | 0.2 | 0.2 |
| HeavyPistol | MP | 80 | 1 | 0.6 | semi | | 1.5 | 133 | 4 | 1.8 | 0.02 | 0.08 | 0.02 | 3 | 0.25 | 1.5 | 1000–10000 | 0.2 | 0.5 |
| SniperRifle | MP | 162 | 1 | 1.25 | semi | 4 | 2.5 | 130 | 2 | 1.25 | 0.2 | 0.4 | 0.1 | 4 | (scope) | 1 | 1000–10000 | 0.2 | 0.2 |
| IonBlaster | MP | 15 | 1 | 0.065 | auto | 50 | 1.5 | 231 | 20 | 1.23 | 0.08 | 0.18 | 0.005 | 2 | 0.5 | 0.1 | 1000–10000 | 0.2 | 0.5 |
| EmpShotgun | Player | 13 | 13 | 0.5 | semi | 2 | 2.5 | 338 | 2 | 0.5 | 0.09 | 0.15 | 0.02 | 4 | 0.5 | 4 | 1000–10000 | 0.2 | 0.5 |
| Shotgun | Player | 13 | 8 | 0.4 | | 6 | 2.5 | 260 | 3 | 0.8 | 0.08 | 0.14 | 0.02 | 4 | 0.5 | 2 | 1000–10000 | 0.2 | 0.5 |
| HeavyMG | Player | 32 | 1 | 0.4 (wind-up) | | 60 | 2.5 | 80+ | 10 | 3.6 | 0.08 | 0.18 | 0.004 | 4 | 0.5 | 0.2 | 1000–10000 | 0.2 | 0.2 |
| PlasmaCannon | MP | 115 (proj) | 1 | 0.15 | charge | 100 | 2.5 | – | 3 | – | 0.04 | 0.09 | 0.02 | 3 | 0.5 | | 1000–10000 | 0.2 | 0.5 |
| RocketLauncher | MP | 135 (proj, splash) | 1 | 1.2 | semi | 4 | 2.5 | 112 | 3 | 2.4 | 0.04 | 0.08 | 0.02 | 3 | 0.5 | 0.25 | 0–16852 | 0.2 | 0.5 |
| GrenadeLauncher | MP | 145 (r 1500) | 1 | 1.1 | semi | 3 | 2.5 | 132 | 3 | 2.2 | 0.04 | 0.04 | 0.06 | 5 | 0.75 | 0.5 | | 0.2 | 0.2 |
| Bazooka (Fusion) | MP | 70 | 1 | 0.75 | | 5 | 2.5 | 93 | 5 | 3.0 | 0.05 | 0.11 | 0.02 | 5 | 0.75 | 1.5 | 1000–10000 | 0.2 | 0.2 |
| GatlingGun (turret) | MP | 25 | 1 | 0.065 | auto | 300 | | 385 | 12 | 0.71 | 0.02 | 0.1 | 0.005 | 4 | 0.5 | 0.15 | | 0.2 | 0.2 |
| RepairRay | Player | 100 / s (beam) | | 0.1 | | 100 | 2.5 | | | | 0.02 | 0.02 | | | | | 0–5000 | 0.2 | 0.5 |
| car AR (vehicle) | MP | 12 | 1 | 0.065 | auto | 60 | 1.5 | 185 | 25 | 1.56 | 0.02 | 0.1 | 0.005 | 1.5 | 0.5 | | | 0.2 | 0.2 |
| car rockets | MP | 55 × 2 | 2 | 0.7 | | 10 | 1.5 | 157 | 3 | 1.4 | 0.02 | 0.02 | | 3 | | | | | |
| jet MG | MP | 10 | 1 | 0.06 | auto | 80 | 2 | 167 | 30 | 1.74 | 0.02 | 0.08 | 0.005 | 2 | | | | 0.1 | 0.1 |
| homing rockets (jet) | MP | 125 | 1 | 1.0 | | 5 | 2.5 | 125 | 3 | 2.0 | 0.02 | 0.08 | 0.02 | 4 | | | 0–16852 | 0.2 | 0.2 |
| tank cannon | MP | 170 | 1 | 2.0 | | 1 | 2 | 85 | 2 | 2.0 | 0.02 | 0.08 | 0.06 | 2.5 | | | | 0.2 | |

The full 75-weapon table, including all fields, range-damage modifiers and burst / fire-interval ramp data, is in the json.

### Aim assist (C; 360 build)
- **No target snap in versus:** `TnGame.CanTargetSnap` = false. The campaign and Escalation return true (TnSurvivalGame), which
  enables FineAim snap-to-target (TnFineAimManager, 1 s timeout).
- **Aim friction ("pan sticky", TnPanStickyAdjuster)** whenever the aim is over a target-assist target:
  - turn rate × the target component's stickiness: MP chassis **yaw 0.5, pitch 0.8**; the HmTargetableComponent default is 1 / 1;
  - × 0.9 if you're moving (× 0.9 if both move), × 1.5 when jumping;
  - clamped to [0.1, 1];
  - blended to 1 with distance up to IdealDistance 1000 UU, so it's strongest close in;
  - ramps out over 1 s after the target leaves.
- **Target pickers** (per chassis TnTargetableComponent): TargetCone and TargetAssist 4° with a 100–375 cm radius (by chassis);
  Snap; Dodge / Melee assist; Homing lock 8°.
- `TargetSnapRange` per weapon (above; 1000–10000 typical) applies only where snap is allowed.
- **PC:** this dump is the Xbox 360 build. The PC-version rules for mouse aim assist aren't present (H: the PC release disabled
  stickiness with the mouse, but that's not verifiable here).

## #12 Damage / TTK
- The original columns are above (damage, pellets, interval, DPS, shots / TTK at 300 HP).
- **Gameplay:** please add your values per row for the comparison.
- Caveats:
  - the MP character health and armour differ per class: H, 300 is a reference value;
  - RangeDamageModifiers reduce damage at range for some weapons (json);
  - headshot multipliers aren't included.

## #15 Weapon switch (C)
- Switching = **old weapon PutDownTime, then new weapon EquipTime**. The weapon can't fire during either (WeaponPuttingDown /
  WeaponEquipping states).
  - **Robot weapons: equip 0.2 s; put-down 0.5 s** for AR, HeavyPistol, IonBlaster, EmpShotgun, Shotgun, PlasmaCannon, RocketLauncher,
    RepairRay; **0.2 s** for BurstRifle, SniperRifle, GrenadeLauncher, HeavyMG, Bazooka.
  - So switching from an AR takes **0.7 s**; from a 0.2 s weapon, **0.4 s**.
  - The visual holster detach happens at DetachDelay (0.5 / 0.2 s, same as the put-down).
- **Animations** (TnWeaponOwnerAnimator, additive, **upper-body mask**):
  - equip `ADD_Shooting_equip_weapon` (blend in 0.2, out 0.3);
  - unequip `ADD_Shooting_UnEquip_Weapon` (blend in 0.3, out 0.0). IonBlaster / RepairRay / Sniper reuse the equip anim for
    unequip;
  - vehicle weapons: `ADD_AssaultRifleVH_Equip_VEH` / `_Drop_VEH` (0.1 s timings);
  - turrets: `Nav_PickUp_Weapon_Turret` (attach delay 0.3 s).
- **Reload** = WeaponReloadAnimTime (1.5 s rifles / pistols, 2.5 s heavy / launchers / shotguns) with `Shooting_Reload_<Weapon>_ROBO`.

## #8 Teammate health bars / names through walls (C, TnObjectiveMarkerTypeTransformerVersus)
- **Allies: always drawn, with no line-of-sight test:** the marker (MarkerAlly_MAT), the name label (focused and unfocused) and
  the **health bar** (TargetHealthBar_MAT). **They show through walls.**
  - Off-screen arrows only for a **downed** ally.
  - Focused size 0.08, unfocused 0.04 (screen fraction); label colour (100, 210, 250).
- **Enemies:** no marker unless you have TnBuffSeeEnemyObjectiveMarkers (and the enemy isn't under a Warcry), your team hard-locked
  it, or a revenge marker is on it.
  - The enemy **name label shows only on focus**, and **only with line of sight** and if not cloaked (HasLineOfSightTo → hidden
    otherwise).
  - No enemy health bar.
- Disguised enemies (TnBuffDisguise): ally style, shown only with line of sight, with the disguise name.

### #8 correction and details (C, added after Frontend's follow-up)
- **The ally health bar is drawn only for a Scientist viewer.**
  - TnObjectiveMarkerTypeTransformerVersus.DrawLabel draws the bar only when EMT == ally (0), the marker has a name, and
    **Owner.GetSpecialty() == "Scientist"** (the medic class).
  - Other classes see ally names / markers through walls, but **no health bars**.
- **No draw-distance cap and no distance fade.**
  - AutoFocusRange **3000 UU**: allies within it draw "focused" (size 0.08, label opaque).
  - Beyond it they draw unfocused (0.04, label still shown).
  - Focus also comes from the marker being within 0.0273 of screen size of the centre.
  - FocusHysterisis 1 s: the label alpha fades over 1 s after focus is lost (only for setups without unfocused labels).
- **The LOS test** (enemy labels / disguise) = TnObjectiveMarkerTypeTransformer.HasLineOfSightTo
  → TnLineOfSightDetector.HasLOSToActor(markerPawn, PlayerCamera) → native Engine.LinesOfSightManager.StaticHasLineOfSight.
  - It's from the marked pawn to the viewer's camera actor.
  - The trace end points and channel are inside the native manager: not decoded.

## #14 Water (C: authored graph + shader-cache scan; H where marked)

**Where "water" exists in MP** (shader-cache scan for water / river / pool / liquid / waterfall / lava names):
- The only liquid materials cooked into MP maps are **energon / coolant waterfalls**:
  - `ENV_CORE_Complex_p.ComplexWaterfall_MATINST` (Remnant, Seed, Molten, Complex);
  - `ENV_CORE_Wall_p.Waterfall_Parent_MAT` (Gorge).
- `WEP_Shared_p.Electric_Lava_Tech_B_Mat` is in every MP base package, but it's a weapon / effect material, not a surface.
- No standing-water / river / pool material is cooked into any MP map.
- If the playtest surface is something else, it's another energon liquid under a different name: tell me the map and spot.

**Waterfall_Parent_MAT** (ORB CoolantRoom; ComplexWaterfall_MATINST's parent; the Gorge copy differs only in its textures, exponent
6 vs 5 and the default colour):
- **BLEND_Additive, MLM_Unlit, bUsesDistortion**, used with decals. Beast opacity source = emissive.
- **Flow:** two pans of WaterFall_CLR / WaterFall_NORM:
  - pan A: speed (0.01, −0.2), tiling Scale;
  - pan B: speed (−0.008, −0.5), tiling 0.5·Scale;
  - both × Time·Speed (MATINST: Speed 1.2, Scale 2.5).
- **Emissive** = 4 · (ReflectionColor · 0.5) · Brightness · **CubeMap(world reflection vector)**^1 + ((CLR_A + CLR_B) · 0.65)^5.
  - The cube is IaconCity_Cubemap.
  - MATINST: Brightness 0.4, ReflectionColor (0.085, 1, 1).
  - The ^5 makes the flowing streaks sharp and bright.
- **Normal** = lerp of the two panned normal samples (0.5), blended again (lerp chain): animated ripples feeding the reflection
  vector.
- **Opacity** = **DepthBiasedAlpha**(alpha 1, bias = desaturate(reflection term), BiasScale 200, DepthBiasBlend 800) × **vertex colour
  R**.
  - That's a soft fade where it meets geometry (scene-depth based), masked by painted vertex colour.
- **Distortion (refraction)** = vertex colour R × 20 × desaturate(normal blend): screen-space refraction in the distortion pass.

**What to restore** (H: compare with our current render):
1. The **distortion pass** (bUsesDistortion: the Modulate / Distortion accumulate path, MODULATE_DISTORTION_CACHE_RE).
2. **DepthBiasedAlpha** soft edges (needs scene depth).
3. The **cube-map reflection** on the world reflection vector, with the panned normals.
4. The **two-speed panning**, using the MATINST Speed / Scale.
5. **Vertex-colour R** masking of opacity and distortion.

### #14 shipped pixel shaders (C: Xenos microcode, tools/shader_by_guid.py; raw dumps in work/handoff/water_ps/)
- **Shaders:**
  - ComplexWaterfall_MATINST (MP_UND_Complex_ART_m): base pass PS `de8001b6…` (FLocalVertexFactory, NoLightMap); distortion PS
    `1ec1c57f…` (TDistortionMeshPixelShader<FDistortMeshAccumulatePolicy>, shared by local and decal VF).
  - Gorge Waterfall_Parent_MAT (MP_UND_Gorge_ART_m): base `1f059d2a…`, distortion `4f8feca2…`.
- **Base-pass PS:**
  - **Normal:** 4 normal fetches (the two pans, each sampled twice through the lerp chain), unpacked ×2 − 1, lerped at 0.5. The
    world-space normal comes from the TBN.
  - **Reflection:** reflection vector R = reflect(−V, N), V from WorldCameraPosition (c3) − (PreViewTranslation-adjusted)
    position → **cube fetch**.
  - **Reflection term** = ReflectionColor (c7) × 0.5 × Cube × Brightness (c11).
  - **Streaks** = x = (CLR_A + CLR_B) × 0.65 (Gorge 0.62); max(|x|, 0.0001).
    - **x^5 = (x²)²·|x|** (Gorge **x^6 = (x²)²·x²**).
    - Plus UniformVector_0 (c6) = **SelectionColor** (the stock UE3 editor selection tint: first entry of the cooked uniform
      expression set; 0 at runtime, so add nothing).
  - **Emissive** = streaks + reflection term × **4**.
- **DepthBiasedAlpha, exactly the UE3 template:**
  - sceneDepth = 1 / (depthSample·c2.z − c2.w) (DeviceDepthConversion);
  - DepthBias = (1 − desaturate(reflection term)) × **c12** (the DepthBiasBlend param, 800), floored at 0.001;
  - blend = **saturate((sceneDepth − pixelDepth) / DepthBias)**.
  - The graph constant BiasScale 200 doesn't appear separately: c12 is the scale input.
- **Opacity** = blend × **interpolator r1.x (vertex colour R)**. **clip if opacity < 1/255.**
- **Output:** oC0.rgb = emissive × fog factor (r4.w) × opacity × SceneColorBiasFactor.x (c5.x: the HDR bias, WFC_HDR_SCENE_PATH);
  oC0.a = SceneColorBiasFactor.y × blend × VC.R. Additive blend, so the RGB is premultiplied by opacity.
- **Distortion PS:**
  - the same 4 normal fetches, unpacked and lerped (0.5);
  - **desaturate** → scalar d: ORB / Complex parent with the default (0.3, 0.59, 0.11); the **Gorge parent with its authored
    LuminanceFactors (0.041452, 0.21952, 0.47044)** (corrected after Rendering checked the Gorge literal pool);
  - × the distortion scale (the literal 80 = graph 20 × a template factor of 4: PARTIAL);
  - × VC.R;
  - written as the UE3 accumulate encoding: oC0.xy = max(d, 0) (positive offset), oC0.zw = |d| clamped (negative offset);
    **clip when negligible**.
  - Both screen axes get the same scalar offset (desaturated normal, so no direction).

## Rust floor tessellation (per-vertex fog question; C for the data, H where marked)
- **The Rust walkable floor is mostly BSP:** MP_IAC_Rust_Art_m has 76 brushes and 280 ModelComponents. The rest is coarse static
  meshes:
  - ENV_CORE_CanyonFloor_F ×89 (104 verts / 68 tris);
  - CanyonFloor_A / B ×11 each (A: 672 / 440);
  - Terminal_Floor_4096 ×13 (**54 verts / 36 tris for 4096 UU**);
  - Panel_01_2048 ×7 (24 / 12).
  Vertex counts are from the extracted cooked LOD0, which is the only LOD these meshes ship with.
- **The original isn't finer.**
  - It renders BSP from the Model's node polygons (fan-triangulated per node; BSP cuts are the only extra vertices), and static
    meshes from that same cooked LOD0.
  - The rebuild's BSP comes from the same node polygon walk, position-matched to the shipped BSPCollision on all 10 maps
    (MP_COLLISION_PHYSMAT).
  - H: if the render path uses that walk too, the triangle density is identical.
- **The fog is per-vertex in the original too** (height-fog VS, LENS_FLARE / fog notes: uniform slabs, evaluated in the base-pass VS).
  So large floor triangles interpolate the fog linearly in the original as well.
- If our floor shows fog banding that the original doesn't, look at the fog inputs (layer heights / start distance /
  ExtinctionDistance cut-off per vertex), not the tessellation.
