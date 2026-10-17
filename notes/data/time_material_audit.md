Ours: K = our GLSL keeps a time term (m.time; time source: WfcPipeline.cpp:8561 time_ = steady_clock seconds since the first rendered frame (process lifetime; never paused, not reset on map change); WFC_LOCKSTEP: (frameNo - lockBase) / 60), D = time dropped, E = translation error, ? = drawn, not translated. K means the term exists, not that speed / phase match. approx = FlipBook FBMethod other than TFBM_UL_ROW (ours is always row order).

### MP_ESC_BrokenHope: 317 time-driven materials (K 317)

| Material (master) | Ours | Time sources by output | Draws / tris | Lighting / blend |
|---|---|---|---|---|
| DES_IAC_WallPanelSign_p.Materials.WallPanelSign_EMISSOFF_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| DES_IAC_WallPanelSign_p.Materials.WallPanelSign_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| ENV_AllShader_p.Energon_River.Energon_Lava_Mat (Energon_Lava_Mat) | K | EmissiveColor: Panner(-0.015, 0.01), Panner(-0.02, -0.06) time-in, Panner(-0.02, 0.03), Panner(-0.09, 0.02), Panner(0.01, -0.01), Panner(0.01, -0.075), Panner(0.1, 0.05) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_AllShader_p.Release.ENV_ForceField_DEC_MATINST (ENV_ForceField_Fac_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_AllShader_p.Release.ENV_ForceField_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_CORE_Floors_p.Materials.ENV_CORE_EnergonPlasmaOrange_INST (Energon_River_Mat) | K | EmissiveColor: Panner(-0.02, -0.06), Panner(-0.02, 0.03), Panner(-0.09, 0.02), Panner(0.01, -0.075), Panner(0.1, 0.05); Opacity: Panner(-0.02, -0.06), Panner(0.1, 0.05) | 0 / 0 | Unlit / Translucent |
| ENV_CORE_Shader_p.Material.ENV_ForceFieldNoDestortionLessGlow_MATINST_INST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_CORE_Shader_p.Material.ENV_ForceFieldNoDestortion_MATINST_INST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2Cool_Lessdense_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2Cool_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2WarmInside_Lighter_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2Warm_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRays_V2_Parent_MAT (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumeCool_LessDense_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumeWarmThink_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumeYellow_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_IAC_LightSources_p.LightPlanes.BckSillouhetteSmoke_MATINST (SmokeCoolDepth_Mat) | K | EmissiveColor: Panner(0.02, 0.05) time-in, Time; Opacity: Panner(0.02, 0.05) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_IAC_LightSources_p.LightPlanes.BrightSmoke_MATINST (SmokeCoolDepth_Mat) | K | EmissiveColor: Panner(0.02, 0.05) time-in, Time; Opacity: Panner(0.02, 0.05) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_IAC_LightSources_p.LightPlanes.SmokeShadow_MATINST (SmokeCoolDepth_Mat) | K | EmissiveColor: Panner(0.02, 0.05) time-in, Time; Opacity: Panner(0.02, 0.05) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_IAC_Omega_p.Material.OmegaLava_Mat_INST (Molten_Parent_MAT) | K | Normal: Panner(-0.02, 0.06) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Opaque |
| ENV_IAC_Shader_p.Material.IAC_Glass2_light_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_IAC_Shader_p.Material.IAC_Glass_HiDISTORT_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_IAC_Shader_p.Material.IAC_Glass_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_IAC_Shader_p.Material.Iacon_CoolSmoke_MATINST (SmokeCoolDepth_Mat) | K | EmissiveColor: Panner(0.02, 0.05) time-in, Time; Opacity: Panner(0.02, 0.05) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_NEU_landmarking_p.landmark_chevrons_clr_Mat (landmark_chevrons_clr_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| ENV_ORB_PowerCorridor_p.Materials.PowerTube_doorMP_green_MATINST (PowerTube_EmissPulse_MAT) | K | EmissiveColor: Panner(0.4, 0) | 0 / 0 | Phong / Opaque |
| ENV_ORB_Spacedome_p.Spacedome_IaconSunset_MAT_INST (SkyDome_PARENT_MAT) | K | EmissiveColor: Panner(0.0001, 0.0001), Rotator(0.0006 rad/s @0.5,0.5), Rotator(0.001 rad/s @0.5,0.5) | 0 / 0 | Phong / Opaque |
| FX_IonBlaster_p.IonBlaster_Mag_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| FX_Materials_p.MatInst.Blaster_Trail_MAT_INST (Blaster_MAT) | K | EmissiveColor: Panner(2.5, 0.5), Panner(3, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.CaptureZone_Reverse_MAT_INST (CaptureZoneLight_Base_MAT) | K | EmissiveColor: Panner(-0.15, 0.18), Panner(0, -0.05), Panner(0.01, -0.02), Time; Opacity: Panner(-0.15, 0.18), Panner(0, -0.05), Panner(0.01, -0.02), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.CircuitRadial_MATINST (CircuitRadial_MAT) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5), Sine(period 1); Opacity: Rotator(0.25 rad/s @0.5,0.5), Sine(period 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Distortion_Cloud_DBA_MAT_INST (Distortion_Cloud_01_MAT) | K | EmissiveColor: Panner(0, 0.3); Distortion: Panner(0, 0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.FusionBlasterBeam_MAT_INST (IonBlasterTrail_MAT) | K | EmissiveColor: Panner(2.5, 0.5), Panner(3, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.LightCylinder_Rays_MAT_INST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.LightVolume_Rays_MAT_INST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Lightning_Anim_03_UP_MAT_INST (Lightning_Anim_03_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.MuzzleFlash_X_Mat_INST (MuzzleFlash_X_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.PROP_Shard_MATINST (PROP_NEU_EnergonCube_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.PickUp_LightVolume_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Smoke_Lrg_Mat_INST (SmokeThick_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.MatInst.Trail_Smoke_01_MAT_INST (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.MatInst.Trail_Smoke_10_MAT_INST (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.AmmoShell_MAT (AmmoShell_MAT) | K | EmissiveColor: Panner(0.04, 0.08), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.BlastShell_MAT (BlastShell_MAT) | K | EmissiveColor: Panner(0.5, 1); Opacity: Panner(0.5, 1); Distortion: Panner(0.5, 1) | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.BlastSphere_Death_MAT (BlastSphere_Death_MAT) | K | EmissiveColor: Time; Distortion: Time | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.Bolt_ADD_MAT (Bolt_ADD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Distortion_Cloud_01_MAT (Distortion_Cloud_01_MAT) | K | EmissiveColor: Panner(0, 0.3); Distortion: Panner(0, 0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.EMPBlastSphere_MAT (EMPBlastSphere_MAT) | K | EmissiveColor: Panner(-0.5, 0.5), Panner(0.1, -1), Panner(0.25, 0.5); Distortion: Panner(-0.5, 0.5), Panner(0.1, -1), Panner(0.25, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.EMPBlastWave_MAT (EMPBlastWave_MAT) | K | EmissiveColor: Panner(-0.5, 0.5), Panner(0.25, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.ElectroRing01_Mat (ElectroRing01_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.ElectroRing02_Mat (ElectroRing02_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Embers_Blue_MAT_INST (Fire_MAT) | K | EmissiveColor: Panner(-0.15, 0.8), Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Explosion_MAT (Explosion_MAT) | K | EmissiveColor: Panner(1, 1), Rotator(0.5 rad/s @0.5,0.5), Time; Opacity: Panner(1, 1), Rotator(0.5 rad/s @0.5,0.5), Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Fire_MAT (Fire_MAT) | K | EmissiveColor: Panner(-0.15, 0.8), Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Fire_Ring01_Mat (Fire_Ring01_Mat) | K | EmissiveColor: Panner(0.4, 0.4) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.HealBeam_MAT (HealBeam_MAT) | K | EmissiveColor: Panner(-0.15, 0), Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.15, 0), Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LaserScanner_MAT (LaserScanner_MAT) | K | EmissiveColor: Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LightVolume_Base_MAT (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LightVolume_WepPickup_MAT (LightVolume_WepPickup_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_01_MAT (Lightning_Anim_01_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_02_MAT (Lightning_Anim_02_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_03_MAT (Lightning_Anim_03_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MFlash_Side_Desat_MAT (MFlash_Side_Desat_MAT) | K | EmissiveColor: Panner(1, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_Mat (MuzzleFlash_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_White_Mat (MuzzleFlash_White_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_X_Mat (MuzzleFlash_X_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ram_model_MAT (Ram_model_MAT) | K | EmissiveColor: Panner(-0.6, 0), Panner(0.6, 1.4), Panner(0.8, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ring_Distort_Add_MAT (Ring_Distort_Add_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ring_Distort_MAT (Ring_Distort_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Opacity: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Ring_Distort_Mesh_MAT (Ring_Distort_Mesh_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Rings_Distort_MAT (Rings_Distort_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Opacity: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.SmokeCoolDepth_Mat (SmokeCoolDepth_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.SmokeThick_Mat (SmokeThick_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Spider_ooze_Mat (Spider_ooze_Mat) | K | Opacity: Panner(0.05, 0.05); Distortion: Panner(0.05, 0.05); Normal: Panner(0.05, 0.05) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Steam_Add_Mat (Steam_Add_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Steam_Mat (Steam_Mat) | K | EmissiveColor: Panner(0, 0.2); Opacity: Panner(0, 0.2) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Steam_Shade_Mat (Steam_Shade_Mat) | K | EmissiveColor: Panner(0, 0.2); Opacity: Panner(0, 0.2) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Tracer_ADD_MAT (Tracer_ADD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Tracer_MAT (Tracer_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Tracer_MOD_MAT (Tracer_MOD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.Tracer_Smoke_MAT (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.arcball01_MAT (arcball01_MAT) | K | EmissiveColor: Rotator(-2 rad/s @0.5,0.5), Rotator(1 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Afterburn_02_MAT (Afterburn_02_MAT) | K | EmissiveColor: Panner(0.2, 2); Opacity: Panner(0.5, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Afterburn_Circuitry_02_MAT (Afterburn_Circuitry_02_MAT) | K | EmissiveColor: Panner(0.2, 2); Opacity: Panner(0, 0.5), Panner(0.1, 0.1), Panner(0.2, 2), Panner(0.5, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Boostermaterial_02_MAT (Boostermaterial_02_MAT) | K | EmissiveColor: Panner(1, 2); Opacity: Panner(1, 2) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.tank_hover_pattern_MAT (tank_hover_pattern_MAT) | K | EmissiveColor: Sine(period 1), Time; Opacity: Panner(0.3, 0.3), Rotator(1 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| FX_RollerMine_p.Material.FX_RollerMine_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| FX_Screen_p.Materials.Static_MAT (Static_MAT) | K | EmissiveColor: Panner(-0.805, -0.942), Panner(0.42, 0.513), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.MuzzleFlash_01_MAT (MuzzleFlash_01_MAT) | K | EmissiveColor: Panner(-0.15, 0.8); Opacity: Panner(-0.15, 0.8) | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.MuzzleFlash_Side_MAT (MuzzleFlash_Side_MAT) | K | EmissiveColor: Panner(1, 0); Opacity: Panner(1, 0) | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.Tracer_MAT (Tracer_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65); Distortion: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| PROP_EnergonSigns_p.AnimSign1_CLR_Mat (AnimSign1_CLR_Mat) | K | EmissiveColor: FlipBook(AnimTest_CLR 4x4 @15 fps), Panner(0, -0.19), Panner(0.01, 0) | 0 / 0 | Unlit / Additive |
| PROP_EnergonSigns_p.AnimSign5_CLR_Mat (AnimSign5_CLR_Mat) | K | EmissiveColor: FlipBook(AnimTest5 3x3 @5 fps), Panner(0, -0.19), Panner(0.01, 0) | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.Barricade2.TPRO_NEU_Barricade2ForceField_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.BarricadeShield_MAT (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.RocketBarricade.TPRO_NEU_RocketBarrier_MATINST (Soundwave_ShieldBarrier_MAT) | K | EmissiveColor: Panner(-0.1, -0.5), Panner(0.1, -0.5), Panner(0.1, -0.75), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_BatteryOS_p.BatteryOmegaGlass_MATINST (ENV_Refractive_Glass_Trans_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Translucent |
| PROP_NEU_BatteryOS_p.OmegaLiquidSurface_MATINST (Coolant_Parent_MAT) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time; Normal: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_BatteryOS_p.OmegaLiquid_MATINST (TryptiGelGlass_Mat) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Translucent |
| PROP_NEU_EnergonCube_p.PROP_NEU_EnergonCube_Circuits_MATINST (PROP_NEU_EnergonCube_Circuits_MAT) | K | EmissiveColor: Panner(0, 1) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Interacts_p.PROP_ButtonInteract_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.Material.Neutral_Flipbook_MAT (Neutral_Flipbook_MAT) | K | EmissiveColor: FlipBook(Neutral_Flipbook_CLR 4x1 @10 fps), Panner(0, -0.5) | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreenActiveBrightBlue_MATINST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreenActiveOrange_MATINST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreenActive_MAT_INST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreen_Optimus_MAT (MonitorScreen_Optimus_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreen_Parent_MAT (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Pickups_p.AmmoPickup.PROP_NEU_AmmoPickup_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.CodeOfPower.CodeOfPowerCORE_MatINST (CodeOfPower_MAT) | K | EmissiveColor: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(-0.15, 0.18), Panner(0.1, -0.075), Panner(0.2, 0.1); Opacity: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(0.2, 0.1); Distortion: Panner(-0.15, 0.18), Panner(0.1, -0.075) | 0 / 0 | Unlit / Translucent |
| PROP_NEU_Pickups_p.EnergonTotem.Conquest_Ring_MATINST (Conquest_Ring_MAT) | K | EmissiveColor: Rotator(-0.3 rad/s @0.5,0.5), Rotator(0.5 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| PROP_NEU_Pickups_p.EnergonTotem.PROP_NEU_EnergonTotem_MATINST (ENV_Hologram_Mat) | K | EmissiveColor: Panner(0, 0.1) time-in, Sine(period 1), Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.MPBomb.BombCore_MATINST_BAT (BombCore_MAT) | K | DiffuseColor: Cosine(period 0.5), Cosine(period 1), Time; EmissiveColor: Cosine(period 0.5), Cosine(period 1), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Pickups_p.MPBomb.PROP_NEU_MPBombExplode_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.MPBomb.PROP_NEU_MPBomb_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.OvershieldPickup.PROP_NEU_Overshield_MATINST (WEP_Crates_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_WreckedBodies_p.RB_SoldierCarAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| PROP_VendingMachine_p.Ammo.PROP_VendingMachine_Ammo_MATINST (VendingMachine_Screen_MAT) | K | EmissiveColor: Cosine(period 1) in Noise_MF, Panner(0, 1) time-in, Panner(1, 1) time-in in Noise_MF, Sine(period 1) in Noise_MF, Time, Time in Noise_MF | 0 / 0 | Unlit / Opaque |
| PROP_VendingMachine_p.PROP_VendingMachine_EnergonCube_MATINST (VendingMachine_Screen_MAT) | K | EmissiveColor: Cosine(period 1) in Noise_MF, Panner(0, 1) time-in, Panner(1, 1) time-in in Noise_MF, Sine(period 1) in Noise_MF, Time, Time in Noise_MF | 0 / 0 | Unlit / Opaque |
| TPRO_KON_CorruptorSpike_p.Materials.DarkEnergonCrystalDark_MAT_INST (DarkEnergonCrystal_MAT) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| TPRO_KON_CorruptorSpike_p.Materials.DarkEnergonCrystal_MATINST (DarkEnergonCrystal_MAT) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| TPRO_KON_CorruptorSpike_p.Materials.DarkEnergonCrystal_MAT_INST (DarkEnergonCrystal_MAT) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| TR_AirRaid_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_AirRaid_ROBO_p.RB_AirRaid_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_AirRaid_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_AirRaid_VEH_p.VH_AirRaid_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Arcee_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Arcee_ROBO_p.RB_Arcee_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Arcee_VEH_p.VH_Arcee_InteriorEnergon_Mat_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Arcee_VEH_p.VH_Arcee_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Barricade_ROBO_p.MaterialInstanceConstant_679 (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Barricade_ROBO_p.RB_Barricade_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Barricade_VEH_p.VH_Barricade_NormSpec_Cust_B_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Brawl_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Brawl_ROBO_p.RB_Brawl_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Brawl_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Brawl_VEH_p.VH_Brawl_NormSpec_Cust_B_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Breakdown_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Breakdown_ROBO_p.RB_Breakdown_Cust_Mat_Inst_E (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Breakdown_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Breakdown_VEH_p.RB_BreadownVEH_Cust_Mat_INST_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_ROBO_p.RB_BumbleBee2_Cust2_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_ROBO_p.RB_BumblebeeEnergon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_VEH_p.Materials.Bumblebee_TransformInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_VEH_p.VEH_BumbleBee2_Cust2_Mat (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Deadend_ROBO_p.RB_DeadendInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Deadend_ROBO_p.RB_Deadend_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Deadend_VEH_p.VH_DeadendInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Deadend_VEH_p.VH_Deadend_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Demolishor_ROBO_p.RB_Demolishor_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Demolishor_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Demolishor_VEH_p.VH_Demolishor_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ironhide_ROBO_p.RB_IronhideInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ironhide_ROBO_p.RB_Ironhide_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ironhide_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ironhide_VEH_p.VH_Ironhide_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jazz_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jazz_ROBO_p.RB_Jazz_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jazz_VEH_p.VH_Jazz_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jetfire_ROBO_p.RB_Jetfire_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jetfire_ROBO_p.TR_JetfireInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jetfire_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jetfire_VEH_p.VH_Jetfire_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Laserbeak_VEH_p.VH_Laserbeak_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Megatron_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Megatron_ROBO_p.VH_Megatron_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Megatron_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Megatron_VEH_p.VH_Megatron_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Onslaught_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Onslaught_ROBO_p.RB_Onslaught_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Onslaught_VEH_p.MaterialInstanceConstant_4774 (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Onslaught_VEH_p.VH_Onslaught_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Optimus_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Optimus_ROBO_p.RB_OptimusPrime_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Optimus_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Optimus_VEH_p.RB_OptimusPrime_Cust2_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ratchet_ROBO_p.RB_RatchetEnergonInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ratchet_ROBO_p.RB_Ratchet_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ratchet_VEH_p.VH_RatchetEnergonInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ratchet_VEH_p.VH_Ratchet_Cust2_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.FrenzyWeapon_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.Frenzy_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.RumbleWeapon_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.Rumble_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Scattershot_ROBO_p.RB_ScattershotInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Scattershot_ROBO_p.RB_Scattershot_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Scattershot_VEH_p.Debug.VH_ScattershotInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Scattershot_VEH_p.VH_Scattershot_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Shockwave_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Shockwave_ROBO_p.RB_Shockwave_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Shockwave_VEH_p.VH_Shockwave_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_ROBO_p.RB_Sideswipe_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_VEH_p.VH_Sideswipe_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_ROBO_p.RB_Silverbolt_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_VEH_p.VH_Silverbolt_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Skywarp_ROBO_p.RB_Skywarp_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Skywarp_ROBO_p.TR_Skywarp_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Skywarp_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Skywarp_VEH_p.VH_Skywarp_NormSpec_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Slipstream_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Slipstream_ROBO_p.RB_Slipstream_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Slipstream_VEH_p.VH_Slipstream_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_ROBO_p.RB_SoldierCarAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_ROBO_p.RB_SoldierMultiAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_VEH_p.VH_SoldierCarAut_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_ROBO_p.RB_SoldierCarDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_ROBO_p.RB_SoldierMultiDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_VEH_p.VH_SniperDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_ROBO_p.RB_SoldierCarNeu_Robo_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_ROBO_p.RB_SoldierMultiNeu_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_VEH_p.VH_SoldierCarNeu_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierTankAut_VEH_p.VH_SoldierTankAutA_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierTankDec_VEH_p.VH_SoldierTankDec_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Soundwave_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Soundwave_ROBO_p.RB_Soundwave_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Soundwave_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Soundwave_VEH_p.VH_Soundwave_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_ROBO_p.TR_Starscream_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_ROBO_p.TR_Starscream_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_StarScream_VEH_p.CHR_Transformer_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_VEH_p.VH_StarscreamInterior_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_ROBO_p.TR_Thunder_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Thunder_ROBO_p.TR_Thunder_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_VEH_p.VH_Thunder_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Trypticon_ROBO_p.RB_TrypticonHead_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Warpath_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Warpath_ROBO_p.RB_Warpath1_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Warpath_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Warpath_VEH_p.RB_Warpath1_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_ROBO_p.TR_ZetaPrime_ROBO_Cust_Mat_Inst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_VEH_p.VH_ZetaPrimeInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_VEH_p.VH_ZetaPrime_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| UI_GFxHud_p.LowHealth.LowHealthScreenEffect_M (LowHealthScreenEffect_M) | K | EmissiveColor: Panner(0, -2), Panner(0, 1) | 0 / 0 | Unlit / Opaque |
| UI_GFxHud_p.StaticDischargeScreenEffect_M (StaticDischargeScreenEffect_M) | K | EmissiveColor: Panner(-0.805, -0.942), Panner(0.42, 0.513) | 0 / 0 | Unlit / Opaque |
| UI_HudMarkers_p.MPMarkerBase_MAT (MPMarkerBase_MAT) | K | Opacity: Cosine(period 1), Panner(0, -2) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MPMarkerCOP_MAT (MPMarkerCOP_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MPMarkerDominationNode_MAT (MPMarkerDominationNode_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MarkerDownedAlly_MAT (MarkerDownedAlly_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MarkerGrenade_MAT (MarkerGrenade_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| WEP_AssaultRifle_p.WEP_AssaultRifle_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Axe_p.Autobot.WEP_Axe_Energon_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_BazookaTemp1_p.WEP_Bazooka_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BeatDownClub_p.WEP_BeatDownClub_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BroadSword_p.WEP_BroadSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_BroadSword_p.WEP_BroadSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BurstRifle_p.Materials.WEP_BurstRifle_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ButterflyAxe_p.WEP_ButterflyAxeEnergon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ButterflyAxe_p.WEP_ButterflyAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_CeremonialStaff_p.WEP_CeremonialStaff_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_CodeOfPower_p.WEP_CodeOfPower_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_DetPack_p.WEP_DetPack_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_EMPShotgun_p.WEP_EMPShotgun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_FightingStaff_p.WEP_FightingStaff_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_GrenadeLauncher_p.WEP_GrenadeLauncher_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Grenade_p.WEP_Grenade_Flak_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HalberdAxe_p.WEP_HalberdAxe_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_HalberdAxe_p.WEP_HalberdAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Hammer_p.WEP_Hammer_D_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Hammer_p.WEP_Hammer_Spikes_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_HeavyMG_p.WEP_HeavyMG_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HeavyPistol_p.WEP_HeavyPistol_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HuntingDagger_p.WEP_HuntingDagger_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_IonBlaster_p.WEP_IonBlaster_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_KamikazeMine_p.WEP_KamikazeMine_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_LancingSpear_p.WEP_LancingSpear_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_LongSword_p.WEP_LongSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_LongSword_p.WEP_LongSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Maul_p.WEP_Maul_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_Maul_p.WEP_Maul_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_PlasmaCannon_p.WEP_PlasmaCannon_A_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ProngDagger_p.WEP_Energon_A_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_ProngDagger_p.WEP_ProngDagger_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_RepairBeam_p.WEP_RepairBeam_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_RocketLauncher_p.WEP_RocketLauncher_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryAbility_p.WEP_DeployedTurret_MATINST (WEP_SentryAbility_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Sine(period 1), Time; OpacityMask: Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryBase.WEP_GlassGlow_MATINST (ENV_Refractive_Glass_Opaque_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| WEP_SentryBlaster01_p.SentryBase.WEP_SentryBase_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryBlaster.WEP_SentryBlaster_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryRepair.WEP_SentryRepair_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryRocket.WEP_SentryRocket_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SerratedBlade_p.WEP_SerratedBlade_Energon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SerratedBlade_p.WEP_SerratedBlade_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shared_p.WEP_Energon_D_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_Shared_p.WEP_PhongMain_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_Frame_MATINST (WEP_Barrier_A_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(0.01, -0.02) time-in in ElectricArcs_MF, Sine(period 1) in ElectricArcs_MF, Sine(period 1) in ScanLines_MF, Time in ElectricArcs_MF, Time in ScanLines_MF | 0 / 0 | Unlit / Translucent |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_MASK_MATINST (WEP_ShieldBruteA_MASK_MAT) | K | EmissiveColor: Panner(-0.75, 0.25), Panner(0.75, -0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Barrier.ENV_ForceField_Defrag_MAT (ENV_ForceField_Defrag_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(1, -0.5), Panner(1, 0) time-in, Rotator(0.25 rad/s @0.5,0.5), Sine(period 1), Sine(period 1) in ScanLines_MF, Time, Time in ScanLines_MF; Opacity: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Barrier.WEP_Barrier_Defrag_MATINST (ENV_ForceField_Defrag_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(1, -0.5), Panner(1, 0) time-in, Rotator(0.25 rad/s @0.5,0.5), Sine(period 1), Sine(period 1) in ScanLines_MF, Time, Time in ScanLines_MF; Opacity: Rotator(0.25 rad/s @0.5,0.5); Distortion: Panner(-0.04, -0.12), Panner(0.2, 0.1) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_Frame_MATINST (WEP_Barrier_A_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(0.01, -0.02) time-in in ElectricArcs_MF, Sine(period 1) in ElectricArcs_MF, Sine(period 1) in ScanLines_MF, Time in ElectricArcs_MF, Time in ScanLines_MF | 0 / 0 | Unlit / Translucent |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_MASK_MATINST (WEP_ShieldBruteA_MASK_MAT) | K | EmissiveColor: Panner(-0.75, 0.25), Panner(0.75, -0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Decepticon.WEP_ShieldD_Energon_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_ShortSword_p.WEP_ShortSword_Energon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ShortSword_p.WEP_ShortSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shotgun_p.WEP_Shotgun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SniperRifle_p.WEP_SniperRifle_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SpikedBat_p.WEP_SpikedBat_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SpikedBat_p.WEP_SpikedBat_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SpikedMace_p.WEP_SpikedMace_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SpikedMace_p.WEP_SpikedMace_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TortureSword_p.WEP_TortureSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_TortureSword_p.WEP_TortureSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TrypticonMouthCannon_p.WEP_TrypMouthCannon_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TrypticonShoulderCannon_p.WEP_TrypShoulderCannon_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun01_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun_Overshield_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(-0.05, -0.1) time-in in Overshield_MFUNC, Panner(-0.1, -0.5) time-in in Overshield_MFUNC, Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Panner(0.2, 0.1) time-in in Overshield_MFUNC, Panner(0.5, 0.1) time-in in Overshield_MFUNC, Time, Time in Overshield_MFUNC | 0 / 0 | Phong / Masked |
| WEP_TurretRocket_p.WEP_TurretRocket_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ViciousAxe_p.WEP_ViciousAxe_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ViciousAxe_p.WEP_ViciousAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_WarHammer_p.WEP_WarHammer_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_WarHammer_p.WEP_WarHammer_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |

### MP_ESC_Remnant: 322 time-driven materials (K 322)

| Material (master) | Ours | Time sources by output | Draws / tris | Lighting / blend |
|---|---|---|---|---|
| DES_IAC_WallPanelSign_p.Materials.WallPanelSign_EMISSOFF_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| DES_IAC_WallPanelSign_p.Materials.WallPanelSign_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| DES_IAC_p.Material.LiftLock_MAT_INST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| ENV_AllShader_p.Release.ENV_ForceField_AUT_MATINST (ENV_ForceField_Fac_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_AllShader_p.Release.ENV_ForceField_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_CORE_Shader_p.Material.ENV_ForceFieldNoDestortionChamber_MATINST_INST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_CORE_Shader_p.Material.ENV_ForceField_MATINST_INST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_CORE_Wall_p.Textures.TunnelGlassBlue_MAT (TunnelGlassBlue_MAT) | K | EmissiveColor: Panner(0.6, 0), Time; Opacity: Panner(0.6, 0) | 0 / 0 | Unlit / Translucent |
| ENV_GLB_EnvEffects_p.Material.LightCylinder_Cool_Rays_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2Cool_Lessdense_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_IAC_Ground_p.Material.ENV_EngergonGlass_MAT_INST (ENV_EnergonCube_MAT) | K | EmissiveColor: Panner(-0.15, 0.18), Panner(0.1, -0.075) | 0 / 0 | Unlit / Opaque |
| ENV_IAC_Interior_1_p.Materials.WallPanel_MAT_INST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| ENV_IAC_LightSources_p.LightPlanes.OmegaSilhouette_MATINST (SmokeCoolDepth_Mat) | K | EmissiveColor: Panner(0.02, 0.05) time-in, Time; Opacity: Panner(0.02, 0.05) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_IAC_Orrery_p.cards.OrreryRings_BLUE_MAT (OrreryRings_BLUE_MAT) | K | EmissiveColor: Panner(0, -0.19), Panner(0.01, 0) | 0 / 0 | Unlit / Additive |
| ENV_IAC_Shader_p.Material.IAC_Glass2_light_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_IAC_Shader_p.Material.IAC_Glass_Trans_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_NEU_Variation_p.EnergonSignsD2_dot_CLR_Mat (EnergonSignsD2_dot_CLR_Mat) | K | EmissiveColor: Rotator(0.5 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| ENV_NEU_Variation_p.EnergonSignsD2_gear_CLR_Mat (EnergonSignsD2_gear_CLR_Mat) | K | EmissiveColor: Rotator(-0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| ENV_NEU_Variation_p.EnergonSignsD2_ring_CLR_Mat (EnergonSignsD2_ring_CLR_Mat) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| ENV_NEU_Variation_p.esigns_d2_CLR_Mat (esigns_d2_CLR_Mat) | K | EmissiveColor: Panner(0, -0.1), Panner(0.03, 0) | 0 / 0 | Unlit / Additive |
| ENV_NEU_Variation_p.fbook_readout2_CLR_Mat (fbook_readout2_CLR_Mat) | K | EmissiveColor: FlipBook(fbook_readout2_CLR 2x2 @4 fps), Panner(1, 1.5) | 0 / 0 | Unlit / Additive |
| ENV_NEU_Variation_p.fbook_sinewave2_CLR_Mat (fbook_sinewave2_CLR_Mat) | K | EmissiveColor: FlipBook(fbook_sinewave2_CLR 2x2 @2 fps) | 0 / 0 | Unlit / Additive |
| ENV_NEU_Variation_p.fbook_sinewave4_CLR_Mat (fbook_sinewave4_CLR_Mat) | K | EmissiveColor: FlipBook(fbook_sinewave4_CLR 2x2 @12 fps), Panner(-0.3, -0.5), Panner(0.5, 0.8) | 0 / 0 | Unlit / Additive |
| ENV_NEU_Variation_p.fbook_sinewave5_CLR_Mat (fbook_sinewave5_CLR_Mat) | K | EmissiveColor: FlipBook(fbook_sinewave5_CLR 3x3 @5 fps), Panner(-0.3, -0.5), Panner(0.5, 0.8) | 0 / 0 | Unlit / Additive |
| ENV_NEU_Variation_p.fbook_sinewave6_CLR_Mat (fbook_sinewave6_CLR_Mat) | K | EmissiveColor: FlipBook(fbook_sinewave6_CLR 2x2 @4 fps), Panner(-0.3, -0.5), Panner(0.5, 0.8) | 0 / 0 | Unlit / Additive |
| ENV_NEU_Variation_p.fbook_sinewave_CLR_Mat (fbook_sinewave_CLR_Mat) | K | EmissiveColor: FlipBook(fbook_sinewave_CLR 2x2 @12 fps) | 0 / 0 | Unlit / Additive |
| ENV_ORB_CoolantRoom_p.Material.CoolantPuddles_MATINST (Coolant_Parent_MAT) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time; Normal: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Additive |
| ENV_ORB_CoolantRoom_p.Material.Waterfall1_MATINST (Waterfall_Parent_MAT) | K | EmissiveColor: Panner(-0.008, -0.5) time-in, Panner(0.01, -0.2) time-in, Time; Distortion: Panner(-0.008, -0.5) time-in, Panner(-0.01, -0.05) time-in, Panner(0.008, -0.01) time-in, Panner(0.01, -0.2) time-in, Time; Normal: Panner(-0.008, -0.5) time-in, Panner(-0.01, -0.05) time-in, Panner(0.008, -0.01) time-in, Panner(0.01, -0.2) time-in, Time | 0 / 0 | Unlit / Additive |
| ENV_ORB_CoolantRoom_p.Material.Waterfall2_MATINST (Waterfall_Parent_MAT) | K | EmissiveColor: Panner(-0.008, -0.5) time-in, Panner(0.01, -0.2) time-in, Time; Distortion: Panner(-0.008, -0.5) time-in, Panner(-0.01, -0.05) time-in, Panner(0.008, -0.01) time-in, Panner(0.01, -0.2) time-in, Time; Normal: Panner(-0.008, -0.5) time-in, Panner(-0.01, -0.05) time-in, Panner(0.008, -0.01) time-in, Panner(0.01, -0.2) time-in, Time | 0 / 0 | Unlit / Additive |
| ENV_ORB_D1_Architecture_p.Materials.Spacedome_NebulaBright_A_MAT (Spacedome_NebulaBright_A_MAT) | K | EmissiveColor: Panner(0.0001, 0.0001), Rotator(0.0006 rad/s @0.5,0.5), Rotator(0.001 rad/s @0.5,0.5) | 0 / 0 | Phong / Opaque |
| ENV_ORB_D1_Architecture_p.Materials.WallPanelWarningSign_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| ENV_ORB_D1_Shader_p.Materials.GlassFloor_Glass_MAT (ENV_CustPhongPointLightUnlit_Reflect_Mat) | K | EmissiveColor: Panner(0, 0.5) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_ORB_D1_Shader_p.Materials.ORB_Glass_ElectricityOFF_MATINST (ENV_Refractive_Glass_Trans_Mat) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Translucent |
| ENV_ORB_WhiteMaterials_p.Materials.White_Tracks_orangeMATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| FX_IonBlaster_p.IonBlaster_Mag_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| FX_Materials_p.MatInst.Blaster_Trail_MAT_INST (Blaster_MAT) | K | EmissiveColor: Panner(2.5, 0.5), Panner(3, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.CaptureZone_Reverse_MAT_INST (CaptureZoneLight_Base_MAT) | K | EmissiveColor: Panner(-0.15, 0.18), Panner(0, -0.05), Panner(0.01, -0.02), Time; Opacity: Panner(-0.15, 0.18), Panner(0, -0.05), Panner(0.01, -0.02), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.CircuitRadial_MATINST (CircuitRadial_MAT) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5), Sine(period 1); Opacity: Rotator(0.25 rad/s @0.5,0.5), Sine(period 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Distortion_Cloud_DBA_MAT_INST (Distortion_Cloud_01_MAT) | K | EmissiveColor: Panner(0, 0.3); Distortion: Panner(0, 0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.FusionBlasterBeam_MAT_INST (IonBlasterTrail_MAT) | K | EmissiveColor: Panner(2.5, 0.5), Panner(3, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.LightCylinder_Rays_MAT_INST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.LightVolume_Rays_MAT_INST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Lightning_Anim_03_UP_MAT_INST (Lightning_Anim_03_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.MuzzleFlash_X_Mat_INST (MuzzleFlash_X_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.PROP_Shard_MATINST (PROP_NEU_EnergonCube_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.PickUp_LightVolume_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Smoke_Lrg_Mat_INST (SmokeThick_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.MatInst.Trail_Smoke_01_MAT_INST (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.MatInst.Trail_Smoke_10_MAT_INST (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.AmmoShell_MAT (AmmoShell_MAT) | K | EmissiveColor: Panner(0.04, 0.08), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.BlastSphere_Death_MAT (BlastSphere_Death_MAT) | K | EmissiveColor: Time; Distortion: Time | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.Bolt_ADD_MAT (Bolt_ADD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Distortion_Cloud_01_MAT (Distortion_Cloud_01_MAT) | K | EmissiveColor: Panner(0, 0.3); Distortion: Panner(0, 0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.EMPBlastSphere_MAT (EMPBlastSphere_MAT) | K | EmissiveColor: Panner(-0.5, 0.5), Panner(0.1, -1), Panner(0.25, 0.5); Distortion: Panner(-0.5, 0.5), Panner(0.1, -1), Panner(0.25, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.EMPBlastWave_MAT (EMPBlastWave_MAT) | K | EmissiveColor: Panner(-0.5, 0.5), Panner(0.25, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.ElectroRing01_Mat (ElectroRing01_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.ElectroRing02_Mat (ElectroRing02_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Embers_Blue_MAT_INST (Fire_MAT) | K | EmissiveColor: Panner(-0.15, 0.8), Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Explosion_MAT (Explosion_MAT) | K | EmissiveColor: Panner(1, 1), Rotator(0.5 rad/s @0.5,0.5), Time; Opacity: Panner(1, 1), Rotator(0.5 rad/s @0.5,0.5), Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Fire_MAT (Fire_MAT) | K | EmissiveColor: Panner(-0.15, 0.8), Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Fire_Ring01_Mat (Fire_Ring01_Mat) | K | EmissiveColor: Panner(0.4, 0.4) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Fire_Small_MAT (Fire_Small_MAT) | K | EmissiveColor: Panner(0.5, -0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.HealBeam_MAT (HealBeam_MAT) | K | EmissiveColor: Panner(-0.15, 0), Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.15, 0), Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LaserScanner_MAT (LaserScanner_MAT) | K | EmissiveColor: Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LightVolume_Base_MAT (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LightVolume_WepPickup_MAT (LightVolume_WepPickup_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_01_MAT (Lightning_Anim_01_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_02_MAT (Lightning_Anim_02_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_03_MAT (Lightning_Anim_03_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MFlash_Side_Desat_MAT (MFlash_Side_Desat_MAT) | K | EmissiveColor: Panner(1, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_Mat (MuzzleFlash_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_White_Mat (MuzzleFlash_White_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_X_Mat (MuzzleFlash_X_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ram_model_MAT (Ram_model_MAT) | K | EmissiveColor: Panner(-0.6, 0), Panner(0.6, 1.4), Panner(0.8, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ring_Distort_Add_MAT (Ring_Distort_Add_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ring_Distort_MAT (Ring_Distort_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Opacity: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Ring_Distort_Mesh_MAT (Ring_Distort_Mesh_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Rings_Distort_MAT (Rings_Distort_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Opacity: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.SmokeCoolDepth_Mat (SmokeCoolDepth_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.SmokeThick_Light_Center_Mat (SmokeThick_Light_Center_Mat) | K | EmissiveColor: Panner(-0.15, 0.5), Time; Opacity: Panner(-0.15, 0.5), Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.SmokeThick_Mat (SmokeThick_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Steam_Add_Mat (Steam_Add_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Steam_Mat (Steam_Mat) | K | EmissiveColor: Panner(0, 0.2); Opacity: Panner(0, 0.2) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Steam_Shade_Mat (Steam_Shade_Mat) | K | EmissiveColor: Panner(0, 0.2); Opacity: Panner(0, 0.2) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Tracer_ADD_MAT (Tracer_ADD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Tracer_MAT (Tracer_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Tracer_MOD_MAT (Tracer_MOD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.Tracer_Smoke_MAT (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.arcball01_MAT (arcball01_MAT) | K | EmissiveColor: Rotator(-2 rad/s @0.5,0.5), Rotator(1 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.bursting_MAT (bursting_MAT) | K | EmissiveColor: Panner(-1, 0); Opacity: Panner(-1, 0); Distortion: Panner(-1, 0); Normal: Panner(-1, 0) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Afterburn_02_MAT (Afterburn_02_MAT) | K | EmissiveColor: Panner(0.2, 2); Opacity: Panner(0.5, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Afterburn_Circuitry_02_MAT (Afterburn_Circuitry_02_MAT) | K | EmissiveColor: Panner(0.2, 2); Opacity: Panner(0, 0.5), Panner(0.1, 0.1), Panner(0.2, 2), Panner(0.5, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Boostermaterial_02_MAT (Boostermaterial_02_MAT) | K | EmissiveColor: Panner(1, 2); Opacity: Panner(1, 2) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.tank_hover_pattern_MAT (tank_hover_pattern_MAT) | K | EmissiveColor: Sine(period 1), Time; Opacity: Panner(0.3, 0.3), Rotator(1 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| FX_RollerMine_p.Material.FX_RollerMine_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| FX_Screen_p.Materials.Static_MAT (Static_MAT) | K | EmissiveColor: Panner(-0.805, -0.942), Panner(0.42, 0.513), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.MuzzleFlash_01_MAT (MuzzleFlash_01_MAT) | K | EmissiveColor: Panner(-0.15, 0.8); Opacity: Panner(-0.15, 0.8) | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.MuzzleFlash_Side_MAT (MuzzleFlash_Side_MAT) | K | EmissiveColor: Panner(1, 0); Opacity: Panner(1, 0) | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.Tracer_MAT (Tracer_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65); Distortion: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| PROP_EnergonSigns_p.AnimSign5_Decepticon_CLR_Mat (AnimSign5_Decepticon_CLR_Mat) | K | EmissiveColor: FlipBook(AnimTest5 3x3 @5 fps), Panner(0, -0.19), Panner(0.01, 0) | 0 / 0 | Unlit / Additive |
| PROP_EnergonSigns_p.AnimSign6_Decepticon_CLR_Mat (AnimSign6_Decepticon_CLR_Mat) | K | EmissiveColor: FlipBook(AnimTest6 2x2 @4 fps), Panner(0, -0.19), Panner(0.01, 0) | 0 / 0 | Unlit / Additive |
| PROP_EnergonSigns_p.Broken_Screen (Broken_Screen) | K | EmissiveColor: Panner(0.03, 0.01), Panner(0.05, -0.06) | 0 / 0 | Phong / Opaque |
| PROP_NEU_Barricade_p.Barricade2.TPRO_NEU_Barricade2ForceField_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.BarricadeShield_MAT (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.RocketBarricade.TPRO_NEU_RocketBarrier_MATINST (Soundwave_ShieldBarrier_MAT) | K | EmissiveColor: Panner(-0.1, -0.5), Panner(0.1, -0.5), Panner(0.1, -0.75), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_BatteryOS_p.BatteryOmegaGlass_MATINST (ENV_Refractive_Glass_Trans_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Translucent |
| PROP_NEU_BatteryOS_p.OmegaLiquidSurface_MATINST (Coolant_Parent_MAT) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time; Normal: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_BatteryOS_p.OmegaLiquid_MATINST (TryptiGelGlass_Mat) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Translucent |
| PROP_NEU_EnergonCube_p.PROP_NEU_EnergonCube_Circuits_MATINST (PROP_NEU_EnergonCube_Circuits_MAT) | K | EmissiveColor: Panner(0, 1) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Interacts_p.PROP_ButtonInteract_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreenActiveRed_MATINST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreenActiveReddish_MATINST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreenActive_MAT_INST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreenDead2_MAT_INST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreen_Dead_MAT (MonitorScreen_Dead_MAT) | K | EmissiveColor: Panner(0, -0.5), Panner(0, 0.05), Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Pickups_p.AmmoPickup.PROP_NEU_AmmoPickup_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.CodeOfPower.CodeOfPowerCORE_MatINST (CodeOfPower_MAT) | K | EmissiveColor: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(-0.15, 0.18), Panner(0.1, -0.075), Panner(0.2, 0.1); Opacity: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(0.2, 0.1); Distortion: Panner(-0.15, 0.18), Panner(0.1, -0.075) | 0 / 0 | Unlit / Translucent |
| PROP_NEU_Pickups_p.EnergonTotem.Conquest_Ring_MATINST (Conquest_Ring_MAT) | K | EmissiveColor: Rotator(-0.3 rad/s @0.5,0.5), Rotator(0.5 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| PROP_NEU_Pickups_p.EnergonTotem.PROP_NEU_EnergonTotem_MATINST (ENV_Hologram_Mat) | K | EmissiveColor: Panner(0, 0.1) time-in, Sine(period 1), Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.MPBomb.BombCore_MATINST_BAT (BombCore_MAT) | K | DiffuseColor: Cosine(period 0.5), Cosine(period 1), Time; EmissiveColor: Cosine(period 0.5), Cosine(period 1), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Pickups_p.MPBomb.PROP_NEU_MPBombExplode_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.MPBomb.PROP_NEU_MPBomb_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.OvershieldPickup.PROP_NEU_Overshield_MATINST (WEP_Crates_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Opaque |
| PROP_VendingMachine_p.Ammo.PROP_VendingMachine_Ammo_MATINST (VendingMachine_Screen_MAT) | K | EmissiveColor: Cosine(period 1) in Noise_MF, Panner(0, 1) time-in, Panner(1, 1) time-in in Noise_MF, Sine(period 1) in Noise_MF, Time, Time in Noise_MF | 0 / 0 | Unlit / Opaque |
| PROP_VendingMachine_p.PROP_VendingMachine_EnergonCube_MATINST (VendingMachine_Screen_MAT) | K | EmissiveColor: Cosine(period 1) in Noise_MF, Panner(0, 1) time-in, Panner(1, 1) time-in in Noise_MF, Sine(period 1) in Noise_MF, Time, Time in Noise_MF | 0 / 0 | Unlit / Opaque |
| TPRO_KON_CorruptorSpike_p.Materials.DarkEnergonCrystal_MAT_INST (DarkEnergonCrystal_MAT) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| TR_AirRaid_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_AirRaid_ROBO_p.RB_AirRaid_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_AirRaid_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_AirRaid_VEH_p.VH_AirRaid_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Arcee_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Arcee_ROBO_p.RB_Arcee_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Arcee_VEH_p.VH_Arcee_InteriorEnergon_Mat_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Arcee_VEH_p.VH_Arcee_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Barricade_ROBO_p.MaterialInstanceConstant_679 (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Barricade_ROBO_p.RB_Barricade_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Barricade_VEH_p.VH_Barricade_NormSpec_Cust_B_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Brawl_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Brawl_ROBO_p.RB_Brawl_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Brawl_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Brawl_VEH_p.VH_Brawl_NormSpec_Cust_B_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Breakdown_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Breakdown_ROBO_p.RB_Breakdown_Cust_Mat_Inst_E (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Breakdown_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Breakdown_VEH_p.RB_BreadownVEH_Cust_Mat_INST_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_ROBO_p.RB_BumbleBee2_Cust2_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_ROBO_p.RB_BumblebeeEnergon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_VEH_p.Materials.Bumblebee_TransformInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_VEH_p.VEH_BumbleBee2_Cust2_Mat (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Deadend_ROBO_p.RB_DeadendInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Deadend_ROBO_p.RB_Deadend_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Deadend_VEH_p.VH_DeadendInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Deadend_VEH_p.VH_Deadend_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Demolishor_ROBO_p.RB_Demolishor_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Demolishor_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Demolishor_VEH_p.VH_Demolishor_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ironhide_ROBO_p.RB_IronhideInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ironhide_ROBO_p.RB_Ironhide_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ironhide_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ironhide_VEH_p.VH_Ironhide_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jazz_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jazz_ROBO_p.RB_Jazz_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jazz_VEH_p.VH_Jazz_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jetfire_ROBO_p.RB_Jetfire_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jetfire_ROBO_p.TR_JetfireInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jetfire_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jetfire_VEH_p.VH_Jetfire_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Laserbeak_VEH_p.VH_Laserbeak_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Megatron_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Megatron_ROBO_p.VH_Megatron_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Megatron_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Megatron_VEH_p.VH_Megatron_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Onslaught_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Onslaught_ROBO_p.RB_Onslaught_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Onslaught_VEH_p.MaterialInstanceConstant_4774 (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Onslaught_VEH_p.VH_Onslaught_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Optimus_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Optimus_ROBO_p.RB_OptimusPrime_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Optimus_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Optimus_VEH_p.RB_OptimusPrime_Cust2_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ratchet_ROBO_p.RB_RatchetEnergonInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ratchet_ROBO_p.RB_Ratchet_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ratchet_VEH_p.VH_RatchetEnergonInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ratchet_VEH_p.VH_Ratchet_Cust2_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.FrenzyWeapon_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.Frenzy_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.RumbleWeapon_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.Rumble_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Scattershot_ROBO_p.RB_ScattershotInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Scattershot_ROBO_p.RB_Scattershot_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Scattershot_VEH_p.Debug.VH_ScattershotInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Scattershot_VEH_p.VH_Scattershot_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Shockwave_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Shockwave_ROBO_p.RB_Shockwave_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Shockwave_VEH_p.VH_Shockwave_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_ROBO_p.RB_Sideswipe_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_VEH_p.VH_Sideswipe_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_ROBO_p.RB_Silverbolt_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_VEH_p.VH_Silverbolt_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Skywarp_ROBO_p.RB_Skywarp_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Skywarp_ROBO_p.TR_Skywarp_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Skywarp_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Skywarp_VEH_p.VH_Skywarp_NormSpec_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Slipstream_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Slipstream_ROBO_p.RB_Slipstream_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Slipstream_VEH_p.VH_Slipstream_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_ROBO_p.RB_SoldierCarAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_ROBO_p.RB_SoldierMultiAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_VEH_p.VH_SoldierCarAut_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_ROBO_p.RB_SoldierCarDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_ROBO_p.RB_SoldierMultiDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_VEH_p.VH_SniperDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_ROBO_p.RB_SoldierCarNeu_Robo_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_ROBO_p.RB_SoldierMultiNeu_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_VEH_p.VH_SoldierCarNeu_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierTankAut_VEH_p.VH_SoldierTankAutA_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierTankDec_VEH_p.VH_SoldierTankDec_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Soundwave_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Soundwave_ROBO_p.RB_Soundwave_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Soundwave_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Soundwave_VEH_p.VH_Soundwave_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_ROBO_p.TR_Starscream_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_ROBO_p.TR_Starscream_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_StarScream_VEH_p.CHR_Transformer_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_VEH_p.VH_StarscreamInterior_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_ROBO_p.TR_Thunder_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Thunder_ROBO_p.TR_Thunder_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_VEH_p.VH_Thunder_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Trypticon_ROBO_p.RB_TrypticonHead_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Warpath_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Warpath_ROBO_p.RB_Warpath1_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Warpath_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Warpath_VEH_p.RB_Warpath1_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_ROBO_p.TR_ZetaPrime_ROBO_Cust_Mat_Inst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_VEH_p.VH_ZetaPrimeInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_VEH_p.VH_ZetaPrime_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| UI_GFxHud_p.LowHealth.LowHealthScreenEffect_M (LowHealthScreenEffect_M) | K | EmissiveColor: Panner(0, -2), Panner(0, 1) | 0 / 0 | Unlit / Opaque |
| UI_GFxHud_p.StaticDischargeScreenEffect_M (StaticDischargeScreenEffect_M) | K | EmissiveColor: Panner(-0.805, -0.942), Panner(0.42, 0.513) | 0 / 0 | Unlit / Opaque |
| UI_HudMarkers_p.MPMarkerBase_MAT (MPMarkerBase_MAT) | K | Opacity: Cosine(period 1), Panner(0, -2) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MPMarkerCOP_MAT (MPMarkerCOP_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MPMarkerDominationNode_MAT (MPMarkerDominationNode_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MarkerDownedAlly_MAT (MarkerDownedAlly_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MarkerGrenade_MAT (MarkerGrenade_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| WEP_AssaultRifle_p.WEP_AssaultRifle_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Axe_p.Autobot.WEP_Axe_Energon_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_BazookaTemp1_p.WEP_Bazooka_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BeatDownClub_p.WEP_BeatDownClub_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BroadSword_p.WEP_BroadSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_BroadSword_p.WEP_BroadSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BurstRifle_p.Materials.WEP_BurstRifle_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ButterflyAxe_p.WEP_ButterflyAxeEnergon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ButterflyAxe_p.WEP_ButterflyAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_CeremonialStaff_p.WEP_CeremonialStaff_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_CodeOfPower_p.WEP_CodeOfPower_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_DetPack_p.WEP_DetPack_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_EMPShotgun_p.WEP_EMPShotgun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_FightingStaff_p.WEP_FightingStaff_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_GrenadeLauncher_p.WEP_GrenadeLauncher_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Grenade_p.WEP_Grenade_Flak_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HalberdAxe_p.WEP_HalberdAxe_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_HalberdAxe_p.WEP_HalberdAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Hammer_p.WEP_Hammer_D_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Hammer_p.WEP_Hammer_Spikes_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_HeavyMG_p.WEP_HeavyMG_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HeavyPistol_p.WEP_HeavyPistol_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HuntingDagger_p.WEP_HuntingDagger_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_IonBlaster_p.WEP_IonBlaster_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_KamikazeMine_p.WEP_KamikazeMine_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_LancingSpear_p.WEP_LancingSpear_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_LongSword_p.WEP_LongSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_LongSword_p.WEP_LongSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Maul_p.WEP_Maul_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_Maul_p.WEP_Maul_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_PlasmaCannon_p.WEP_PlasmaCannon_A_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ProngDagger_p.WEP_Energon_A_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_ProngDagger_p.WEP_ProngDagger_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_RepairBeam_p.WEP_RepairBeam_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_RocketLauncher_p.WEP_RocketLauncher_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryAbility_p.WEP_DeployedTurret_MATINST (WEP_SentryAbility_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Sine(period 1), Time; OpacityMask: Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryBase.WEP_GlassGlow_MATINST (ENV_Refractive_Glass_Opaque_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| WEP_SentryBlaster01_p.SentryBase.WEP_SentryBase_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryBlaster.WEP_SentryBlaster_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryRepair.WEP_SentryRepair_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryRocket.WEP_SentryRocket_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SerratedBlade_p.WEP_SerratedBlade_Energon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SerratedBlade_p.WEP_SerratedBlade_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shared_p.WEP_Energon_D_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_Shared_p.WEP_PhongMain_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_Frame_MATINST (WEP_Barrier_A_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(0.01, -0.02) time-in in ElectricArcs_MF, Sine(period 1) in ElectricArcs_MF, Sine(period 1) in ScanLines_MF, Time in ElectricArcs_MF, Time in ScanLines_MF | 0 / 0 | Unlit / Translucent |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_MASK_MATINST (WEP_ShieldBruteA_MASK_MAT) | K | EmissiveColor: Panner(-0.75, 0.25), Panner(0.75, -0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Barrier.ENV_ForceField_Defrag_MAT (ENV_ForceField_Defrag_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(1, -0.5), Panner(1, 0) time-in, Rotator(0.25 rad/s @0.5,0.5), Sine(period 1), Sine(period 1) in ScanLines_MF, Time, Time in ScanLines_MF; Opacity: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Barrier.WEP_Barrier_Defrag_MATINST (ENV_ForceField_Defrag_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(1, -0.5), Panner(1, 0) time-in, Rotator(0.25 rad/s @0.5,0.5), Sine(period 1), Sine(period 1) in ScanLines_MF, Time, Time in ScanLines_MF; Opacity: Rotator(0.25 rad/s @0.5,0.5); Distortion: Panner(-0.04, -0.12), Panner(0.2, 0.1) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_Frame_MATINST (WEP_Barrier_A_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(0.01, -0.02) time-in in ElectricArcs_MF, Sine(period 1) in ElectricArcs_MF, Sine(period 1) in ScanLines_MF, Time in ElectricArcs_MF, Time in ScanLines_MF | 0 / 0 | Unlit / Translucent |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_MASK_MATINST (WEP_ShieldBruteA_MASK_MAT) | K | EmissiveColor: Panner(-0.75, 0.25), Panner(0.75, -0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Decepticon.WEP_ShieldD_Energon_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_ShortSword_p.WEP_ShortSword_Energon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ShortSword_p.WEP_ShortSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shotgun_p.WEP_Shotgun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SniperRifle_p.WEP_SniperRifle_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SpikedBat_p.WEP_SpikedBat_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SpikedBat_p.WEP_SpikedBat_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SpikedMace_p.WEP_SpikedMace_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SpikedMace_p.WEP_SpikedMace_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TortureSword_p.WEP_TortureSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_TortureSword_p.WEP_TortureSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TrypticonMouthCannon_p.WEP_TrypMouthCannon_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TrypticonShoulderCannon_p.WEP_TrypShoulderCannon_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun01_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun_Overshield_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(-0.05, -0.1) time-in in Overshield_MFUNC, Panner(-0.1, -0.5) time-in in Overshield_MFUNC, Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Panner(0.2, 0.1) time-in in Overshield_MFUNC, Panner(0.5, 0.1) time-in in Overshield_MFUNC, Time, Time in Overshield_MFUNC | 0 / 0 | Phong / Masked |
| WEP_TurretRocket_p.WEP_TurretRocket_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ViciousAxe_p.WEP_ViciousAxe_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ViciousAxe_p.WEP_ViciousAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_WarHammer_p.WEP_WarHammer_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_WarHammer_p.WEP_WarHammer_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |

### MP_IAC_Berth: 299 time-driven materials (K 299)

| Material (master) | Ours | Time sources by output | Draws / tris | Lighting / blend |
|---|---|---|---|---|
| DES_IAC_WallPanelSign_p.Materials.WallPanelSign_EMISSOFF_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| DES_IAC_WallPanelSign_p.Materials.WallPanelSign_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| ENV_GLB_EnvEffects_p.Material.LightRaysDarkCool_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2WarmInside_Lighter_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2Warm_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2Warm_SpaceStation_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2purple_Lessdense_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumeCool_LessLessDense_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumeWarmThink_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.TrainWarningLights_orange_MATINST (LightVolume_Parent_MAT) | K | Opacity: Time | 0 / 0 | Unlit / Additive |
| ENV_IAC_Interior_1_p.Materials.ENV_EnergyBridge_MAT_INST (ENV_Refractive_Glass_TransVrtxClr_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Translucent |
| ENV_IAC_Orrery_p.cards.OrreryLines_and_icons_MAT (OrreryLines_and_icons_MAT) | K | EmissiveColor: Panner(0, -0.19), Panner(0.01, 0) | 0 / 0 | Unlit / Additive |
| ENV_IAC_Orrery_p.cards.OrreryRings_MAT (OrreryRings_MAT) | K | EmissiveColor: Panner(0, -0.19), Panner(0.01, 0) | 0 / 0 | Unlit / Additive |
| ENV_IAC_Shader_p.Material.IAC_Glass2_Dark_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_KON_Deco_p.Materials.LightVolumeCool_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_KON_Deco_p.Materials.Plasma_Purple_MATINST (Plasma) | K | EmissiveColor: Panner(-0.01, 0.02), Panner(0.01, -0.02) | 0 / 0 | Phong / Opaque |
| ENV_NEU_landmarking_p.landmark_Dchevrons_clr_Mat (landmark_Dchevrons_clr_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_Dtarget_clr_Mat (landmark_Dtarget_clr_Mat) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_ablogo_clr_Mat (landmark_ablogo_clr_Mat) | K | EmissiveColor: Panner(-0.05, -0.03), Panner(0.02, 0.1) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_chevrons_clr_Mat (landmark_chevrons_clr_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_declogo_clr_Mat (landmark_declogo_clr_Mat) | K | EmissiveColor: Panner(-0.05, -0.03), Panner(0.02, 0.1) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_ring_clr_Mat (landmark_ring_clr_Mat) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_target_clr_Mat (landmark_target_clr_Mat) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| ENV_ORB_DebrisBase_p.Materials.ENV_ORB_SliceFloorBGlass_MATINST (ENV_CustPhongUnlit_Reflect_Mat) | K | EmissiveColor: Panner(0, 0.5) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_ORB_Spacedome_p.Spacedome_MAT (Spacedome_MAT) | K | EmissiveColor: Panner(0.0001, 0.0001), Rotator(0.001 rad/s @0.5,0.5) | 0 / 0 | Phong / Opaque |
| FX_IonBlaster_p.IonBlaster_Mag_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| FX_Materials_p.MatInst.Blaster_Trail_MAT_INST (Blaster_MAT) | K | EmissiveColor: Panner(2.5, 0.5), Panner(3, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.CaptureZone_Reverse_MAT_INST (CaptureZoneLight_Base_MAT) | K | EmissiveColor: Panner(-0.15, 0.18), Panner(0, -0.05), Panner(0.01, -0.02), Time; Opacity: Panner(-0.15, 0.18), Panner(0, -0.05), Panner(0.01, -0.02), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.CircuitRadial_MATINST (CircuitRadial_MAT) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5), Sine(period 1); Opacity: Rotator(0.25 rad/s @0.5,0.5), Sine(period 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Distortion_Cloud_DBA_MAT_INST (Distortion_Cloud_01_MAT) | K | EmissiveColor: Panner(0, 0.3); Distortion: Panner(0, 0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.FusionBlasterBeam_MAT_INST (IonBlasterTrail_MAT) | K | EmissiveColor: Panner(2.5, 0.5), Panner(3, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.LightCylinder_Rays_MAT_INST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.LightVolume_Rays_MAT_INST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Lightning_Anim_03_UP_MAT_INST (Lightning_Anim_03_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.MuzzleFlash_X_Mat_INST (MuzzleFlash_X_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Smoke_Lrg_Mat_INST (SmokeThick_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.MatInst.Trail_Smoke_01_MAT_INST (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.MatInst.Trail_Smoke_10_MAT_INST (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.AmmoShell_MAT (AmmoShell_MAT) | K | EmissiveColor: Panner(0.04, 0.08), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.BlastSphere_Death_MAT (BlastSphere_Death_MAT) | K | EmissiveColor: Time; Distortion: Time | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.Bolt_ADD_MAT (Bolt_ADD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Distortion_Cloud_01_MAT (Distortion_Cloud_01_MAT) | K | EmissiveColor: Panner(0, 0.3); Distortion: Panner(0, 0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.EMPBlastSphere_MAT (EMPBlastSphere_MAT) | K | EmissiveColor: Panner(-0.5, 0.5), Panner(0.1, -1), Panner(0.25, 0.5); Distortion: Panner(-0.5, 0.5), Panner(0.1, -1), Panner(0.25, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.EMPBlastWave_MAT (EMPBlastWave_MAT) | K | EmissiveColor: Panner(-0.5, 0.5), Panner(0.25, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.ElectroRing01_Mat (ElectroRing01_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.ElectroRing02_Mat (ElectroRing02_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Embers_Blue_MAT_INST (Fire_MAT) | K | EmissiveColor: Panner(-0.15, 0.8), Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Explosion_MAT (Explosion_MAT) | K | EmissiveColor: Panner(1, 1), Rotator(0.5 rad/s @0.5,0.5), Time; Opacity: Panner(1, 1), Rotator(0.5 rad/s @0.5,0.5), Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Fire_MAT (Fire_MAT) | K | EmissiveColor: Panner(-0.15, 0.8), Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Fire_Ring01_Mat (Fire_Ring01_Mat) | K | EmissiveColor: Panner(0.4, 0.4) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.HealBeam_MAT (HealBeam_MAT) | K | EmissiveColor: Panner(-0.15, 0), Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.15, 0), Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LaserScanner_MAT (LaserScanner_MAT) | K | EmissiveColor: Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LightVolume_Base_MAT (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LightVolume_WepPickup_MAT (LightVolume_WepPickup_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_01_MAT (Lightning_Anim_01_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_02_MAT (Lightning_Anim_02_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_03_MAT (Lightning_Anim_03_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MFlash_Side_Desat_MAT (MFlash_Side_Desat_MAT) | K | EmissiveColor: Panner(1, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_Mat (MuzzleFlash_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_White_Mat (MuzzleFlash_White_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_X_Mat (MuzzleFlash_X_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ram_model_MAT (Ram_model_MAT) | K | EmissiveColor: Panner(-0.6, 0), Panner(0.6, 1.4), Panner(0.8, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ring_Distort_Add_MAT (Ring_Distort_Add_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ring_Distort_MAT (Ring_Distort_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Opacity: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Ring_Distort_Mesh_MAT (Ring_Distort_Mesh_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Rings_Distort_MAT (Rings_Distort_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Opacity: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.SmokeCoolDepth_Mat (SmokeCoolDepth_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.SmokeThick_Mat (SmokeThick_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Steam_Add_Mat (Steam_Add_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Steam_Mat (Steam_Mat) | K | EmissiveColor: Panner(0, 0.2); Opacity: Panner(0, 0.2) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Steam_Shade_Mat (Steam_Shade_Mat) | K | EmissiveColor: Panner(0, 0.2); Opacity: Panner(0, 0.2) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Tracer_ADD_MAT (Tracer_ADD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Tracer_MAT (Tracer_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Tracer_MOD_MAT (Tracer_MOD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.Tracer_Smoke_MAT (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.arcball01_MAT (arcball01_MAT) | K | EmissiveColor: Rotator(-2 rad/s @0.5,0.5), Rotator(1 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Afterburn_02_MAT (Afterburn_02_MAT) | K | EmissiveColor: Panner(0.2, 2); Opacity: Panner(0.5, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Afterburn_Circuitry_02_MAT (Afterburn_Circuitry_02_MAT) | K | EmissiveColor: Panner(0.2, 2); Opacity: Panner(0, 0.5), Panner(0.1, 0.1), Panner(0.2, 2), Panner(0.5, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Boostermaterial_02_MAT (Boostermaterial_02_MAT) | K | EmissiveColor: Panner(1, 2); Opacity: Panner(1, 2) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.tank_hover_pattern_MAT (tank_hover_pattern_MAT) | K | EmissiveColor: Sine(period 1), Time; Opacity: Panner(0.3, 0.3), Rotator(1 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| FX_RollerMine_p.Material.FX_RollerMine_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| FX_Screen_p.Materials.Static_MAT (Static_MAT) | K | EmissiveColor: Panner(-0.805, -0.942), Panner(0.42, 0.513), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.MuzzleFlash_01_MAT (MuzzleFlash_01_MAT) | K | EmissiveColor: Panner(-0.15, 0.8); Opacity: Panner(-0.15, 0.8) | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.MuzzleFlash_Side_MAT (MuzzleFlash_Side_MAT) | K | EmissiveColor: Panner(1, 0); Opacity: Panner(1, 0) | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.Barricade2.TPRO_NEU_Barricade2ForceField_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.BarricadeShield_MAT (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.RocketBarricade.TPRO_NEU_RocketBarrier_MATINST (Soundwave_ShieldBarrier_MAT) | K | EmissiveColor: Panner(-0.1, -0.5), Panner(0.1, -0.5), Panner(0.1, -0.75), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_BatteryOS_p.BatteryOmegaGlass_MATINST (ENV_Refractive_Glass_Trans_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Translucent |
| PROP_NEU_BatteryOS_p.OmegaLiquidSurface_MATINST (Coolant_Parent_MAT) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time; Normal: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_BatteryOS_p.OmegaLiquid_MATINST (TryptiGelGlass_Mat) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Translucent |
| PROP_NEU_EnergonCube_p.PROP_NEU_EnergonCube_Circuits_MATINST (PROP_NEU_EnergonCube_Circuits_MAT) | K | EmissiveColor: Panner(0, 1) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Interacts_p.PROP_ButtonInteract_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| PROP_NEU_Pickups_p.AmmoPickup.PROP_NEU_AmmoPickup_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.CodeOfPower.CodeOfPowerCORE_MatINST (CodeOfPower_MAT) | K | EmissiveColor: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(-0.15, 0.18), Panner(0.1, -0.075), Panner(0.2, 0.1); Opacity: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(0.2, 0.1); Distortion: Panner(-0.15, 0.18), Panner(0.1, -0.075) | 0 / 0 | Unlit / Translucent |
| PROP_NEU_Pickups_p.EnergonTotem.Conquest_Ring_MATINST (Conquest_Ring_MAT) | K | EmissiveColor: Rotator(-0.3 rad/s @0.5,0.5), Rotator(0.5 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| PROP_NEU_Pickups_p.EnergonTotem.PROP_NEU_EnergonTotem_MATINST (ENV_Hologram_Mat) | K | EmissiveColor: Panner(0, 0.1) time-in, Sine(period 1), Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.MPBomb.BombCore_MATINST_BAT (BombCore_MAT) | K | DiffuseColor: Cosine(period 0.5), Cosine(period 1), Time; EmissiveColor: Cosine(period 0.5), Cosine(period 1), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Pickups_p.MPBomb.PROP_NEU_MPBombExplode_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.MPBomb.PROP_NEU_MPBomb_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.OvershieldPickup.PROP_NEU_Overshield_MATINST (WEP_Crates_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Opaque |
| PROP_VendingMachine_p.Ammo.PROP_VendingMachine_Ammo_MATINST (VendingMachine_Screen_MAT) | K | EmissiveColor: Cosine(period 1) in Noise_MF, Panner(0, 1) time-in, Panner(1, 1) time-in in Noise_MF, Sine(period 1) in Noise_MF, Time, Time in Noise_MF | 0 / 0 | Unlit / Opaque |
| PROP_VendingMachine_p.PROP_VendingMachine_EnergonCube_MATINST (VendingMachine_Screen_MAT) | K | EmissiveColor: Cosine(period 1) in Noise_MF, Panner(0, 1) time-in, Panner(1, 1) time-in in Noise_MF, Sine(period 1) in Noise_MF, Time, Time in Noise_MF | 0 / 0 | Unlit / Opaque |
| TPRO_KON_CorruptorSpike_p.Materials.DarkEnergonCrystal_MAT_INST (DarkEnergonCrystal_MAT) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| TR_AirRaid_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_AirRaid_ROBO_p.RB_AirRaid_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_AirRaid_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_AirRaid_VEH_p.VH_AirRaid_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Arcee_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Arcee_ROBO_p.RB_Arcee_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Arcee_VEH_p.VH_Arcee_InteriorEnergon_Mat_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Arcee_VEH_p.VH_Arcee_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Barricade_ROBO_p.MaterialInstanceConstant_679 (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Barricade_ROBO_p.RB_Barricade_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Barricade_VEH_p.VH_Barricade_NormSpec_Cust_B_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Brawl_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Brawl_ROBO_p.RB_Brawl_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Brawl_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Brawl_VEH_p.VH_Brawl_NormSpec_Cust_B_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Breakdown_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Breakdown_ROBO_p.RB_Breakdown_Cust_Mat_Inst_E (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Breakdown_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Breakdown_VEH_p.RB_BreadownVEH_Cust_Mat_INST_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_ROBO_p.RB_BumbleBee2_Cust2_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_ROBO_p.RB_BumblebeeEnergon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_VEH_p.Materials.Bumblebee_TransformInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_VEH_p.VEH_BumbleBee2_Cust2_Mat (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Deadend_ROBO_p.RB_DeadendInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Deadend_ROBO_p.RB_Deadend_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Deadend_VEH_p.VH_DeadendInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Deadend_VEH_p.VH_Deadend_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Demolishor_ROBO_p.RB_Demolishor_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Demolishor_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Demolishor_VEH_p.VH_Demolishor_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ironhide_ROBO_p.RB_IronhideInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ironhide_ROBO_p.RB_Ironhide_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ironhide_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ironhide_VEH_p.VH_Ironhide_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jazz_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jazz_ROBO_p.RB_Jazz_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jazz_VEH_p.VH_Jazz_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jetfire_ROBO_p.RB_Jetfire_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jetfire_ROBO_p.TR_JetfireInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jetfire_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jetfire_VEH_p.VH_Jetfire_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Laserbeak_VEH_p.VH_Laserbeak_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Megatron_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Megatron_ROBO_p.VH_Megatron_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Megatron_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Megatron_VEH_p.VH_Megatron_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Onslaught_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Onslaught_ROBO_p.RB_Onslaught_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Onslaught_VEH_p.MaterialInstanceConstant_4774 (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Onslaught_VEH_p.VH_Onslaught_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Optimus_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Optimus_ROBO_p.RB_OptimusPrime_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Optimus_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Optimus_VEH_p.RB_OptimusPrime_Cust2_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ratchet_ROBO_p.RB_RatchetEnergonInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ratchet_ROBO_p.RB_Ratchet_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ratchet_VEH_p.VH_RatchetEnergonInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ratchet_VEH_p.VH_Ratchet_Cust2_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.FrenzyWeapon_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.Frenzy_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.RumbleWeapon_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.Rumble_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Scattershot_ROBO_p.RB_ScattershotInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Scattershot_ROBO_p.RB_Scattershot_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Scattershot_VEH_p.Debug.VH_ScattershotInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Scattershot_VEH_p.VH_Scattershot_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Shockwave_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Shockwave_ROBO_p.RB_Shockwave_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Shockwave_VEH_p.VH_Shockwave_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_ROBO_p.RB_Sideswipe_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_VEH_p.VH_Sideswipe_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_ROBO_p.RB_Silverbolt_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_VEH_p.VH_Silverbolt_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Skywarp_ROBO_p.RB_Skywarp_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Skywarp_ROBO_p.TR_Skywarp_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Skywarp_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Skywarp_VEH_p.VH_Skywarp_NormSpec_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Slipstream_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Slipstream_ROBO_p.RB_Slipstream_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Slipstream_VEH_p.VH_Slipstream_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_ROBO_p.RB_SoldierCarAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_ROBO_p.RB_SoldierMultiAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_VEH_p.VH_SoldierCarAut_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_ROBO_p.RB_SoldierCarDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_ROBO_p.RB_SoldierMultiDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_VEH_p.VH_SniperDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_ROBO_p.RB_SoldierCarNeu_Robo_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_ROBO_p.RB_SoldierMultiNeu_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_VEH_p.VH_SoldierCarNeu_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierTankAut_VEH_p.VH_SoldierTankAutA_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierTankDec_VEH_p.VH_SoldierTankDec_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Soundwave_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Soundwave_ROBO_p.RB_Soundwave_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Soundwave_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Soundwave_VEH_p.VH_Soundwave_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_ROBO_p.TR_Starscream_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_ROBO_p.TR_Starscream_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_StarScream_VEH_p.CHR_Transformer_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_VEH_p.VH_StarscreamInterior_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_ROBO_p.TR_Thunder_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Thunder_ROBO_p.TR_Thunder_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_VEH_p.VH_Thunder_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Trypticon_ROBO_p.RB_TrypticonHead_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Warpath_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Warpath_ROBO_p.RB_Warpath1_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Warpath_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Warpath_VEH_p.RB_Warpath1_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_ROBO_p.TR_ZetaPrime_ROBO_Cust_Mat_Inst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_VEH_p.VH_ZetaPrimeInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_VEH_p.VH_ZetaPrime_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| UI_GFxHud_p.LowHealth.LowHealthScreenEffect_M (LowHealthScreenEffect_M) | K | EmissiveColor: Panner(0, -2), Panner(0, 1) | 0 / 0 | Unlit / Opaque |
| UI_GFxHud_p.StaticDischargeScreenEffect_M (StaticDischargeScreenEffect_M) | K | EmissiveColor: Panner(-0.805, -0.942), Panner(0.42, 0.513) | 0 / 0 | Unlit / Opaque |
| UI_HudMarkers_p.MPMarkerBase_MAT (MPMarkerBase_MAT) | K | Opacity: Cosine(period 1), Panner(0, -2) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MPMarkerCOP_MAT (MPMarkerCOP_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MPMarkerDominationNode_MAT (MPMarkerDominationNode_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MarkerDownedAlly_MAT (MarkerDownedAlly_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MarkerGrenade_MAT (MarkerGrenade_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| WEP_AssaultRifle_p.WEP_AssaultRifle_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Axe_p.Autobot.WEP_Axe_Energon_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_BazookaTemp1_p.WEP_Bazooka_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BeatDownClub_p.WEP_BeatDownClub_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BroadSword_p.WEP_BroadSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_BroadSword_p.WEP_BroadSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BurstRifle_p.Materials.WEP_BurstRifle_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ButterflyAxe_p.WEP_ButterflyAxeEnergon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ButterflyAxe_p.WEP_ButterflyAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_CeremonialStaff_p.WEP_CeremonialStaff_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_CodeOfPower_p.WEP_CodeOfPower_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_DetPack_p.WEP_DetPack_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_EMPShotgun_p.WEP_EMPShotgun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_FightingStaff_p.WEP_FightingStaff_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_GrenadeLauncher_p.WEP_GrenadeLauncher_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Grenade_p.WEP_Grenade_Flak_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HalberdAxe_p.WEP_HalberdAxe_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_HalberdAxe_p.WEP_HalberdAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Hammer_p.WEP_Hammer_D_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Hammer_p.WEP_Hammer_Spikes_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_HeavyMG_p.WEP_HeavyMG_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HeavyPistol_p.WEP_HeavyPistol_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HuntingDagger_p.WEP_HuntingDagger_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_IonBlaster_p.WEP_IonBlaster_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_KamikazeMine_p.WEP_KamikazeMine_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_LancingSpear_p.WEP_LancingSpear_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_LongSword_p.WEP_LongSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_LongSword_p.WEP_LongSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Maul_p.WEP_Maul_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_Maul_p.WEP_Maul_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_PlasmaCannon_p.WEP_PlasmaCannon_A_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ProngDagger_p.WEP_Energon_A_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_ProngDagger_p.WEP_ProngDagger_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_RepairBeam_p.WEP_RepairBeam_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_RocketLauncher_p.WEP_RocketLauncher_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryAbility_p.WEP_DeployedTurret_MATINST (WEP_SentryAbility_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Sine(period 1), Time; OpacityMask: Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryBase.WEP_GlassGlow_MATINST (ENV_Refractive_Glass_Opaque_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| WEP_SentryBlaster01_p.SentryBase.WEP_SentryBase_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryBlaster.WEP_SentryBlaster_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryRepair.WEP_SentryRepair_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryRocket.WEP_SentryRocket_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SerratedBlade_p.WEP_SerratedBlade_Energon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SerratedBlade_p.WEP_SerratedBlade_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shared_p.WEP_Energon_D_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_Shared_p.WEP_PhongMain_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_Frame_MATINST (WEP_Barrier_A_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(0.01, -0.02) time-in in ElectricArcs_MF, Sine(period 1) in ElectricArcs_MF, Sine(period 1) in ScanLines_MF, Time in ElectricArcs_MF, Time in ScanLines_MF | 0 / 0 | Unlit / Translucent |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_MASK_MATINST (WEP_ShieldBruteA_MASK_MAT) | K | EmissiveColor: Panner(-0.75, 0.25), Panner(0.75, -0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Barrier.ENV_ForceField_Defrag_MAT (ENV_ForceField_Defrag_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(1, -0.5), Panner(1, 0) time-in, Rotator(0.25 rad/s @0.5,0.5), Sine(period 1), Sine(period 1) in ScanLines_MF, Time, Time in ScanLines_MF; Opacity: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Barrier.WEP_Barrier_Defrag_MATINST (ENV_ForceField_Defrag_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(1, -0.5), Panner(1, 0) time-in, Rotator(0.25 rad/s @0.5,0.5), Sine(period 1), Sine(period 1) in ScanLines_MF, Time, Time in ScanLines_MF; Opacity: Rotator(0.25 rad/s @0.5,0.5); Distortion: Panner(-0.04, -0.12), Panner(0.2, 0.1) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_Frame_MATINST (WEP_Barrier_A_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(0.01, -0.02) time-in in ElectricArcs_MF, Sine(period 1) in ElectricArcs_MF, Sine(period 1) in ScanLines_MF, Time in ElectricArcs_MF, Time in ScanLines_MF | 0 / 0 | Unlit / Translucent |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_MASK_MATINST (WEP_ShieldBruteA_MASK_MAT) | K | EmissiveColor: Panner(-0.75, 0.25), Panner(0.75, -0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Decepticon.WEP_ShieldD_Energon_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_ShortSword_p.WEP_ShortSword_Energon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ShortSword_p.WEP_ShortSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shotgun_p.WEP_Shotgun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SniperRifle_p.WEP_SniperRifle_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SpikedBat_p.WEP_SpikedBat_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SpikedBat_p.WEP_SpikedBat_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SpikedMace_p.WEP_SpikedMace_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SpikedMace_p.WEP_SpikedMace_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TortureSword_p.WEP_TortureSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_TortureSword_p.WEP_TortureSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TrypticonMouthCannon_p.WEP_TrypMouthCannon_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TrypticonShoulderCannon_p.WEP_TrypShoulderCannon_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun01_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun_Overshield_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(-0.05, -0.1) time-in in Overshield_MFUNC, Panner(-0.1, -0.5) time-in in Overshield_MFUNC, Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Panner(0.2, 0.1) time-in in Overshield_MFUNC, Panner(0.5, 0.1) time-in in Overshield_MFUNC, Time, Time in Overshield_MFUNC | 0 / 0 | Phong / Masked |
| WEP_TurretRocket_p.WEP_TurretRocket_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ViciousAxe_p.WEP_ViciousAxe_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ViciousAxe_p.WEP_ViciousAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_WarHammer_p.WEP_WarHammer_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_WarHammer_p.WEP_WarHammer_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |

### MP_IAC_Rust: 313 time-driven materials (K 313)

| Material (master) | Ours | Time sources by output | Draws / tris | Lighting / blend |
|---|---|---|---|---|
| DES_IAC_WallPanelSign_p.Materials.WallPanelSign_EMISSOFF_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| DES_IAC_WallPanelSign_p.Materials.WallPanelSign_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| DES_IAC_p.Material.LiftLock_MAT_INST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| ENV_AllShader_p.Release.ENV_ForceField_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2Cool_Lessdense_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2Orange_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2purple_Lessdense_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumeMid_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_IAC_CleanMaterials_p.Materials.ENV_IAC_CleanDoor_Off_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| ENV_IAC_Ground_p.Material.ENV_EngergonGlass_MAT_INST (ENV_EnergonCube_MAT) | K | EmissiveColor: Panner(-0.15, 0.18), Panner(0.1, -0.075) | 0 / 0 | Unlit / Opaque |
| ENV_IAC_Interior_1_p.Materials.ENV_EngergonGlassV3_MAT_INST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_IAC_LightSources_p.LightPlanes.BckSillouhetteSmoke_MATINST (SmokeCoolDepth_Mat) | K | EmissiveColor: Panner(0.02, 0.05) time-in, Time; Opacity: Panner(0.02, 0.05) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_IAC_LightSources_p.LightPlanes.IntroVistaSmoke_MATINST (SmokeCoolDepth_Mat) | K | EmissiveColor: Panner(0.02, 0.05) time-in, Time; Opacity: Panner(0.02, 0.05) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_IAC_LightSources_p.LightPlanes.MachineSmokeCover_red_MATINST (SmokeCoolDepth_Mat) | K | EmissiveColor: Panner(0.02, 0.05) time-in, Time; Opacity: Panner(0.02, 0.05) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_IAC_LightSources_p.LightPlanes.StarScreamFightSmoke_MATINST (SmokeCoolDepth_Mat) | K | EmissiveColor: Panner(0.02, 0.05) time-in, Time; Opacity: Panner(0.02, 0.05) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_IAC_Shader_p.Material.IAC_Glass2_Dark_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_IAC_Shader_p.Material.IAC_Glass_Trans_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_Dchevrons_clr_Mat (landmark_Dchevrons_clr_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_Dtarget_clr_Mat (landmark_Dtarget_clr_Mat) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_ablogo_clr_Mat (landmark_ablogo_clr_Mat) | K | EmissiveColor: Panner(-0.05, -0.03), Panner(0.02, 0.1) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_chevrons_clr_Mat (landmark_chevrons_clr_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_declogo_clr_Mat (landmark_declogo_clr_Mat) | K | EmissiveColor: Panner(-0.05, -0.03), Panner(0.02, 0.1) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_target_clr_Mat (landmark_target_clr_Mat) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| ENV_ORB_D1_Architecture_p.Materials.WallPanelWarningSign_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| ENV_ORB_D1_Architecture_p.Materials.WallPanelWarningSign_purple_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| ENV_ORB_PowerCorridor_p.Materials.PowerTubeEmissPulse_BEAM_MATINST (PowerTube_EmissPulse_MAT) | K | EmissiveColor: Panner(0.4, 0) | 0 / 0 | Phong / Opaque |
| ENV_ORB_Spacedome_p.Spacedome_MAT (Spacedome_MAT) | K | EmissiveColor: Panner(0.0001, 0.0001), Rotator(0.001 rad/s @0.5,0.5) | 0 / 0 | Phong / Opaque |
| FX_IonBlaster_p.IonBlaster_Mag_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| FX_Materials_p.MatInst.Blaster_Trail_MAT_INST (Blaster_MAT) | K | EmissiveColor: Panner(2.5, 0.5), Panner(3, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.CaptureZone_Reverse_MAT_INST (CaptureZoneLight_Base_MAT) | K | EmissiveColor: Panner(-0.15, 0.18), Panner(0, -0.05), Panner(0.01, -0.02), Time; Opacity: Panner(-0.15, 0.18), Panner(0, -0.05), Panner(0.01, -0.02), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.CircuitRadial_MATINST (CircuitRadial_MAT) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5), Sine(period 1); Opacity: Rotator(0.25 rad/s @0.5,0.5), Sine(period 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Distortion_Cloud_DBA_MAT_INST (Distortion_Cloud_01_MAT) | K | EmissiveColor: Panner(0, 0.3); Distortion: Panner(0, 0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.FusionBlasterBeam_MAT_INST (IonBlasterTrail_MAT) | K | EmissiveColor: Panner(2.5, 0.5), Panner(3, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.LightCylinder_Rays_MAT_INST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.LightVolume_Rays_MAT_INST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Lightning_Anim_03_UP_MAT_INST (Lightning_Anim_03_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.MuzzleFlash_X_Mat_INST (MuzzleFlash_X_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Smoke_Lrg_Mat_INST (SmokeThick_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.MatInst.Trail_Smoke_01_MAT_INST (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.MatInst.Trail_Smoke_10_MAT_INST (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.AmmoShell_MAT (AmmoShell_MAT) | K | EmissiveColor: Panner(0.04, 0.08), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.BlastSphere_Death_MAT (BlastSphere_Death_MAT) | K | EmissiveColor: Time; Distortion: Time | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.Bolt_ADD_MAT (Bolt_ADD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Distortion_Cloud_01_MAT (Distortion_Cloud_01_MAT) | K | EmissiveColor: Panner(0, 0.3); Distortion: Panner(0, 0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.EMPBlastSphere_MAT (EMPBlastSphere_MAT) | K | EmissiveColor: Panner(-0.5, 0.5), Panner(0.1, -1), Panner(0.25, 0.5); Distortion: Panner(-0.5, 0.5), Panner(0.1, -1), Panner(0.25, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.EMPBlastWave_MAT (EMPBlastWave_MAT) | K | EmissiveColor: Panner(-0.5, 0.5), Panner(0.25, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.ElectroRing01_Mat (ElectroRing01_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.ElectroRing02_Mat (ElectroRing02_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Embers_Blue_MAT_INST (Fire_MAT) | K | EmissiveColor: Panner(-0.15, 0.8), Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Explosion_MAT (Explosion_MAT) | K | EmissiveColor: Panner(1, 1), Rotator(0.5 rad/s @0.5,0.5), Time; Opacity: Panner(1, 1), Rotator(0.5 rad/s @0.5,0.5), Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Fire_MAT (Fire_MAT) | K | EmissiveColor: Panner(-0.15, 0.8), Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Fire_Ring01_Mat (Fire_Ring01_Mat) | K | EmissiveColor: Panner(0.4, 0.4) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.HealBeam_MAT (HealBeam_MAT) | K | EmissiveColor: Panner(-0.15, 0), Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.15, 0), Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LaserScanner_MAT (LaserScanner_MAT) | K | EmissiveColor: Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LightVolume_Base_MAT (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LightVolume_WepPickup_MAT (LightVolume_WepPickup_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_01_MAT (Lightning_Anim_01_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_02_MAT (Lightning_Anim_02_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_03_MAT (Lightning_Anim_03_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MFlash_Side_Desat_MAT (MFlash_Side_Desat_MAT) | K | EmissiveColor: Panner(1, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_Mat (MuzzleFlash_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_White_Mat (MuzzleFlash_White_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_X_Mat (MuzzleFlash_X_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ram_model_MAT (Ram_model_MAT) | K | EmissiveColor: Panner(-0.6, 0), Panner(0.6, 1.4), Panner(0.8, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ring_Distort_Add_MAT (Ring_Distort_Add_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ring_Distort_MAT (Ring_Distort_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Opacity: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Ring_Distort_Mesh_MAT (Ring_Distort_Mesh_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Rings_Distort_MAT (Rings_Distort_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Opacity: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.SmokeCoolDepth_Mat (SmokeCoolDepth_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.SmokeThick_Mat (SmokeThick_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Steam_Add_Mat (Steam_Add_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Steam_Mat (Steam_Mat) | K | EmissiveColor: Panner(0, 0.2); Opacity: Panner(0, 0.2) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Steam_Shade_Mat (Steam_Shade_Mat) | K | EmissiveColor: Panner(0, 0.2); Opacity: Panner(0, 0.2) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Tracer_ADD_MAT (Tracer_ADD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Tracer_MAT (Tracer_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Tracer_MOD_MAT (Tracer_MOD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.Tracer_Smoke_MAT (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.arcball01_MAT (arcball01_MAT) | K | EmissiveColor: Rotator(-2 rad/s @0.5,0.5), Rotator(1 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Afterburn_02_MAT (Afterburn_02_MAT) | K | EmissiveColor: Panner(0.2, 2); Opacity: Panner(0.5, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Afterburn_Circuitry_02_MAT (Afterburn_Circuitry_02_MAT) | K | EmissiveColor: Panner(0.2, 2); Opacity: Panner(0, 0.5), Panner(0.1, 0.1), Panner(0.2, 2), Panner(0.5, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Boostermaterial_02_MAT (Boostermaterial_02_MAT) | K | EmissiveColor: Panner(1, 2); Opacity: Panner(1, 2) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.tank_hover_pattern_MAT (tank_hover_pattern_MAT) | K | EmissiveColor: Sine(period 1), Time; Opacity: Panner(0.3, 0.3), Rotator(1 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| FX_RollerMine_p.Material.FX_RollerMine_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| FX_Screen_p.Materials.Static_MAT (Static_MAT) | K | EmissiveColor: Panner(-0.805, -0.942), Panner(0.42, 0.513), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.MuzzleFlash_01_MAT (MuzzleFlash_01_MAT) | K | EmissiveColor: Panner(-0.15, 0.8); Opacity: Panner(-0.15, 0.8) | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.MuzzleFlash_Side_MAT (MuzzleFlash_Side_MAT) | K | EmissiveColor: Panner(1, 0); Opacity: Panner(1, 0) | 0 / 0 | Unlit / Additive |
| PROP_EnergonSigns_p.AnimSign1_CLR_Mat (AnimSign1_CLR_Mat) | K | EmissiveColor: FlipBook(AnimTest_CLR 4x4 @15 fps), Panner(0, -0.19), Panner(0.01, 0) | 0 / 0 | Unlit / Additive |
| PROP_EnergonSigns_p.AnimSign4_CLR_Mat (AnimSign4_CLR_Mat) | K | EmissiveColor: FlipBook(AnimTest4 4x4 @8 fps), Panner(0, -0.19), Panner(0.01, 0) | 0 / 0 | Unlit / Additive |
| PROP_EnergonSigns_p.AnimSign5_CLR_Mat (AnimSign5_CLR_Mat) | K | EmissiveColor: FlipBook(AnimTest5 3x3 @5 fps), Panner(0, -0.19), Panner(0.01, 0) | 0 / 0 | Unlit / Additive |
| PROP_EnergonSigns_p.AnimSign6_CLR_Mat (AnimSign6_CLR_Mat) | K | EmissiveColor: FlipBook(AnimTest6 2x2 @4 fps), Panner(0, -0.19), Panner(0.01, 0) | 0 / 0 | Unlit / Additive |
| PROP_EnergonSigns_p.AnimTes_static_CLR_Mat (AnimTes_static_CLR_Mat) | K | EmissiveColor: Panner(0.03, 0.01), Panner(0.05, -0.06) | 0 / 0 | Unlit / Opaque |
| PROP_EnergonSigns_p.EnergonSigns_line_CLR_Mat (EnergonSigns_line_CLR_Mat) | K | EmissiveColor: Panner(0, -0.19), Panner(0.01, 0) | 0 / 0 | Unlit / Additive |
| PROP_IAC_CityProps_p.VendingMachine.PROP_VendingMachineGlass_MATINST (ENV_Refractive_Glass_Trans_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Translucent |
| PROP_IAC_HospitalProps_p.ChemicalTank.PROP_ChemicalTankLiquid_MATINST (Energon_CubeB_Mat) | K | EmissiveColor: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(-0.15, 0.18), Panner(0.1, -0.075), Panner(0.2, 0.1); Normal: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(0.2, 0.1) | 0 / 0 | Phong / Opaque |
| PROP_IAC_HospitalProps_p.ChemicalTank.PROP_ChemicalTankLiquid_red_MATINST (Energon_CubeB_Mat) | K | EmissiveColor: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(-0.15, 0.18), Panner(0.1, -0.075), Panner(0.2, 0.1); Normal: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(0.2, 0.1) | 0 / 0 | Phong / Opaque |
| PROP_NEU_Barricade_p.Barricade2.TPRO_NEU_Barricade2ForceField_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.BarricadeShield_MAT (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.RocketBarricade.TPRO_NEU_RocketBarrier_MATINST (Soundwave_ShieldBarrier_MAT) | K | EmissiveColor: Panner(-0.1, -0.5), Panner(0.1, -0.5), Panner(0.1, -0.75), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_BatteryOS_p.BatteryOmegaGlass_MATINST (ENV_Refractive_Glass_Trans_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Translucent |
| PROP_NEU_BatteryOS_p.OmegaLiquidSurface_MATINST (Coolant_Parent_MAT) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time; Normal: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_BatteryOS_p.OmegaLiquid_MATINST (TryptiGelGlass_Mat) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Translucent |
| PROP_NEU_EnergonCube_p.PROP_NEU_EnergonCube_Circuits_MATINST (PROP_NEU_EnergonCube_Circuits_MAT) | K | EmissiveColor: Panner(0, 1) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Interacts_p.PROP_ButtonInteract_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreenActiveOrange_MATINST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreenActivePurple_MATINST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreenActiveRed_MATINST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Pickups_p.AmmoPickup.PROP_NEU_AmmoPickup_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.CodeOfPower.CodeOfPowerCORE_MatINST (CodeOfPower_MAT) | K | EmissiveColor: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(-0.15, 0.18), Panner(0.1, -0.075), Panner(0.2, 0.1); Opacity: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(0.2, 0.1); Distortion: Panner(-0.15, 0.18), Panner(0.1, -0.075) | 0 / 0 | Unlit / Translucent |
| PROP_NEU_Pickups_p.EnergonTotem.Conquest_Ring_MATINST (Conquest_Ring_MAT) | K | EmissiveColor: Rotator(-0.3 rad/s @0.5,0.5), Rotator(0.5 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| PROP_NEU_Pickups_p.EnergonTotem.PROP_NEU_EnergonTotem_MATINST (ENV_Hologram_Mat) | K | EmissiveColor: Panner(0, 0.1) time-in, Sine(period 1), Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.MPBomb.BombCore_MATINST_BAT (BombCore_MAT) | K | DiffuseColor: Cosine(period 0.5), Cosine(period 1), Time; EmissiveColor: Cosine(period 0.5), Cosine(period 1), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Pickups_p.MPBomb.PROP_NEU_MPBombExplode_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.MPBomb.PROP_NEU_MPBomb_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.OvershieldPickup.PROP_NEU_Overshield_MATINST (WEP_Crates_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Opaque |
| PROP_VendingMachine_p.Ammo.PROP_VendingMachine_Ammo_MATINST (VendingMachine_Screen_MAT) | K | EmissiveColor: Cosine(period 1) in Noise_MF, Panner(0, 1) time-in, Panner(1, 1) time-in in Noise_MF, Sine(period 1) in Noise_MF, Time, Time in Noise_MF | 0 / 0 | Unlit / Opaque |
| PROP_VendingMachine_p.PROP_VendingMachine_EnergonCube_MATINST (VendingMachine_Screen_MAT) | K | EmissiveColor: Cosine(period 1) in Noise_MF, Panner(0, 1) time-in, Panner(1, 1) time-in in Noise_MF, Sine(period 1) in Noise_MF, Time, Time in Noise_MF | 0 / 0 | Unlit / Opaque |
| TPRO_KON_CorruptorSpike_p.Materials.DarkEnergonCrystal_MAT_INST (DarkEnergonCrystal_MAT) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| TR_AirRaid_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_AirRaid_ROBO_p.RB_AirRaid_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_AirRaid_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_AirRaid_VEH_p.VH_AirRaid_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Arcee_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Arcee_ROBO_p.RB_Arcee_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Arcee_VEH_p.VH_Arcee_InteriorEnergon_Mat_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Arcee_VEH_p.VH_Arcee_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Barricade_ROBO_p.MaterialInstanceConstant_679 (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Barricade_ROBO_p.RB_Barricade_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Barricade_VEH_p.VH_Barricade_NormSpec_Cust_B_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Brawl_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Brawl_ROBO_p.RB_Brawl_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Brawl_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Brawl_VEH_p.VH_Brawl_NormSpec_Cust_B_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Breakdown_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Breakdown_ROBO_p.RB_Breakdown_Cust_Mat_Inst_E (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Breakdown_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Breakdown_VEH_p.RB_BreadownVEH_Cust_Mat_INST_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_ROBO_p.RB_BumbleBee2_Cust2_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_ROBO_p.RB_BumblebeeEnergon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_VEH_p.Materials.Bumblebee_TransformInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_VEH_p.VEH_BumbleBee2_Cust2_Mat (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Deadend_ROBO_p.RB_DeadendInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Deadend_ROBO_p.RB_Deadend_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Deadend_VEH_p.VH_DeadendInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Deadend_VEH_p.VH_Deadend_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Demolishor_ROBO_p.RB_Demolishor_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Demolishor_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Demolishor_VEH_p.VH_Demolishor_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ironhide_ROBO_p.RB_IronhideInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ironhide_ROBO_p.RB_Ironhide_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ironhide_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ironhide_VEH_p.VH_Ironhide_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jazz_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jazz_ROBO_p.RB_Jazz_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jazz_VEH_p.VH_Jazz_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jetfire_ROBO_p.RB_Jetfire_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jetfire_ROBO_p.TR_JetfireInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jetfire_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jetfire_VEH_p.VH_Jetfire_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Laserbeak_VEH_p.VH_Laserbeak_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Megatron_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Megatron_ROBO_p.VH_Megatron_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Megatron_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Megatron_VEH_p.VH_Megatron_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Onslaught_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Onslaught_ROBO_p.RB_Onslaught_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Onslaught_VEH_p.MaterialInstanceConstant_4774 (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Onslaught_VEH_p.VH_Onslaught_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Optimus_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Optimus_ROBO_p.RB_OptimusPrime_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Optimus_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Optimus_VEH_p.RB_OptimusPrime_Cust2_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ratchet_ROBO_p.RB_RatchetEnergonInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ratchet_ROBO_p.RB_Ratchet_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ratchet_VEH_p.VH_RatchetEnergonInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ratchet_VEH_p.VH_Ratchet_Cust2_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.FrenzyWeapon_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.Frenzy_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.RumbleWeapon_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.Rumble_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Scattershot_ROBO_p.RB_ScattershotInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Scattershot_ROBO_p.RB_Scattershot_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Scattershot_VEH_p.Debug.VH_ScattershotInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Scattershot_VEH_p.VH_Scattershot_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Shockwave_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Shockwave_ROBO_p.RB_Shockwave_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Shockwave_VEH_p.VH_Shockwave_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_ROBO_p.RB_Sideswipe_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_VEH_p.VH_Sideswipe_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_ROBO_p.RB_Silverbolt_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_VEH_p.VH_Silverbolt_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Skywarp_ROBO_p.RB_Skywarp_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Skywarp_ROBO_p.TR_Skywarp_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Skywarp_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Skywarp_VEH_p.VH_Skywarp_NormSpec_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Slipstream_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Slipstream_ROBO_p.RB_Slipstream_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Slipstream_VEH_p.VH_Slipstream_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_ROBO_p.RB_SoldierCarAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_ROBO_p.RB_SoldierMultiAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_VEH_p.VH_SoldierCarAut_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_ROBO_p.RB_SoldierCarDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_ROBO_p.RB_SoldierMultiDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_VEH_p.VH_SniperDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_ROBO_p.RB_SoldierCarNeu_Robo_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_ROBO_p.RB_SoldierMultiNeu_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_VEH_p.VH_SoldierCarNeu_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierTankAut_VEH_p.VH_SoldierTankAutA_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierTankDec_VEH_p.VH_SoldierTankDec_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Soundwave_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Soundwave_ROBO_p.RB_Soundwave_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Soundwave_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Soundwave_VEH_p.VH_Soundwave_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_ROBO_p.TR_Starscream_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_ROBO_p.TR_Starscream_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_StarScream_VEH_p.CHR_Transformer_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_VEH_p.VH_StarscreamInterior_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_ROBO_p.TR_Thunder_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Thunder_ROBO_p.TR_Thunder_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_VEH_p.VH_Thunder_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Trypticon_ROBO_p.RB_TrypticonHead_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Warpath_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Warpath_ROBO_p.RB_Warpath1_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Warpath_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Warpath_VEH_p.RB_Warpath1_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_ROBO_p.TR_ZetaPrime_ROBO_Cust_Mat_Inst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_VEH_p.VH_ZetaPrimeInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_VEH_p.VH_ZetaPrime_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| UI_GFxHud_p.LowHealth.LowHealthScreenEffect_M (LowHealthScreenEffect_M) | K | EmissiveColor: Panner(0, -2), Panner(0, 1) | 0 / 0 | Unlit / Opaque |
| UI_GFxHud_p.StaticDischargeScreenEffect_M (StaticDischargeScreenEffect_M) | K | EmissiveColor: Panner(-0.805, -0.942), Panner(0.42, 0.513) | 0 / 0 | Unlit / Opaque |
| UI_HudMarkers_p.MPMarkerBase_MAT (MPMarkerBase_MAT) | K | Opacity: Cosine(period 1), Panner(0, -2) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MPMarkerCOP_MAT (MPMarkerCOP_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MPMarkerDominationNode_MAT (MPMarkerDominationNode_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MarkerDownedAlly_MAT (MarkerDownedAlly_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MarkerGrenade_MAT (MarkerGrenade_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| WEP_AssaultRifle_p.WEP_AssaultRifle_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Axe_p.Autobot.WEP_Axe_Energon_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_BazookaTemp1_p.WEP_Bazooka_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BeatDownClub_p.WEP_BeatDownClub_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BroadSword_p.WEP_BroadSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_BroadSword_p.WEP_BroadSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BurstRifle_p.Materials.WEP_BurstRifle_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ButterflyAxe_p.WEP_ButterflyAxeEnergon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ButterflyAxe_p.WEP_ButterflyAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_CeremonialStaff_p.WEP_CeremonialStaff_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_CodeOfPower_p.WEP_CodeOfPower_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_DetPack_p.WEP_DetPack_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_EMPShotgun_p.WEP_EMPShotgun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_FightingStaff_p.WEP_FightingStaff_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_GrenadeLauncher_p.WEP_GrenadeLauncher_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Grenade_p.WEP_Grenade_Flak_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HalberdAxe_p.WEP_HalberdAxe_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_HalberdAxe_p.WEP_HalberdAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Hammer_p.WEP_Hammer_D_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Hammer_p.WEP_Hammer_Spikes_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_HeavyMG_p.WEP_HeavyMG_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HeavyPistol_p.WEP_HeavyPistol_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HuntingDagger_p.WEP_HuntingDagger_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_IonBlaster_p.WEP_IonBlaster_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_KamikazeMine_p.WEP_KamikazeMine_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_LancingSpear_p.WEP_LancingSpear_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_LongSword_p.WEP_LongSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_LongSword_p.WEP_LongSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Maul_p.WEP_Maul_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_Maul_p.WEP_Maul_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_PlasmaCannon_p.WEP_PlasmaCannon_A_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ProngDagger_p.WEP_Energon_A_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_ProngDagger_p.WEP_ProngDagger_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_RepairBeam_p.WEP_RepairBeam_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_RocketLauncher_p.WEP_RocketLauncher_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryAbility_p.WEP_DeployedTurret_MATINST (WEP_SentryAbility_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Sine(period 1), Time; OpacityMask: Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryBase.WEP_GlassGlow_MATINST (ENV_Refractive_Glass_Opaque_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| WEP_SentryBlaster01_p.SentryBase.WEP_SentryBase_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryBlaster.WEP_SentryBlaster_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryRepair.WEP_SentryRepair_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryRocket.WEP_SentryRocket_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SerratedBlade_p.WEP_SerratedBlade_Energon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SerratedBlade_p.WEP_SerratedBlade_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shared_p.WEP_Energon_D_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_Shared_p.WEP_PhongMain_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_Frame_MATINST (WEP_Barrier_A_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(0.01, -0.02) time-in in ElectricArcs_MF, Sine(period 1) in ElectricArcs_MF, Sine(period 1) in ScanLines_MF, Time in ElectricArcs_MF, Time in ScanLines_MF | 0 / 0 | Unlit / Translucent |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_MASK_MATINST (WEP_ShieldBruteA_MASK_MAT) | K | EmissiveColor: Panner(-0.75, 0.25), Panner(0.75, -0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Barrier.ENV_ForceField_Defrag_MAT (ENV_ForceField_Defrag_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(1, -0.5), Panner(1, 0) time-in, Rotator(0.25 rad/s @0.5,0.5), Sine(period 1), Sine(period 1) in ScanLines_MF, Time, Time in ScanLines_MF; Opacity: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Barrier.WEP_Barrier_Defrag_MATINST (ENV_ForceField_Defrag_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(1, -0.5), Panner(1, 0) time-in, Rotator(0.25 rad/s @0.5,0.5), Sine(period 1), Sine(period 1) in ScanLines_MF, Time, Time in ScanLines_MF; Opacity: Rotator(0.25 rad/s @0.5,0.5); Distortion: Panner(-0.04, -0.12), Panner(0.2, 0.1) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_Frame_MATINST (WEP_Barrier_A_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(0.01, -0.02) time-in in ElectricArcs_MF, Sine(period 1) in ElectricArcs_MF, Sine(period 1) in ScanLines_MF, Time in ElectricArcs_MF, Time in ScanLines_MF | 0 / 0 | Unlit / Translucent |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_MASK_MATINST (WEP_ShieldBruteA_MASK_MAT) | K | EmissiveColor: Panner(-0.75, 0.25), Panner(0.75, -0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Decepticon.WEP_ShieldD_Energon_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_ShortSword_p.WEP_ShortSword_Energon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ShortSword_p.WEP_ShortSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shotgun_p.WEP_Shotgun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SniperRifle_p.WEP_SniperRifle_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SpikedBat_p.WEP_SpikedBat_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SpikedBat_p.WEP_SpikedBat_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SpikedMace_p.WEP_SpikedMace_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SpikedMace_p.WEP_SpikedMace_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TortureSword_p.WEP_TortureSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_TortureSword_p.WEP_TortureSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TrypticonMouthCannon_p.WEP_TrypMouthCannon_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TrypticonShoulderCannon_p.WEP_TrypShoulderCannon_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun01_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun_Overshield_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(-0.05, -0.1) time-in in Overshield_MFUNC, Panner(-0.1, -0.5) time-in in Overshield_MFUNC, Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Panner(0.2, 0.1) time-in in Overshield_MFUNC, Panner(0.5, 0.1) time-in in Overshield_MFUNC, Time, Time in Overshield_MFUNC | 0 / 0 | Phong / Masked |
| WEP_TurretRocket_p.WEP_TurretRocket_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ViciousAxe_p.WEP_ViciousAxe_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ViciousAxe_p.WEP_ViciousAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_WarHammer_p.WEP_WarHammer_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_WarHammer_p.WEP_WarHammer_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |

### MP_IAC_Seed: 316 time-driven materials (K 316)

| Material (master) | Ours | Time sources by output | Draws / tris | Lighting / blend |
|---|---|---|---|---|
| DES_IAC_WallPanelSign_p.Materials.WallPanelSign_EMISSOFF_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| DES_IAC_WallPanelSign_p.Materials.WallPanelSign_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| ENV_ArchiveInterior_p.Courtyard.CourtyardFalls_MATINST (Waterfall_Parent_MAT) | K | EmissiveColor: Panner(-0.008, -0.5) time-in, Panner(0.01, -0.2) time-in, Time; Distortion: Panner(-0.008, -0.5) time-in, Panner(-0.01, -0.05) time-in, Panner(0.008, -0.01) time-in, Panner(0.01, -0.2) time-in, Time; Normal: Panner(-0.008, -0.5) time-in, Panner(-0.01, -0.05) time-in, Panner(0.008, -0.01) time-in, Panner(0.01, -0.2) time-in, Time | 0 / 0 | Unlit / Additive |
| ENV_ArchiveInterior_p.Courtyard.CourtyardPool_MATINST (Coolant_Parent_MAT) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time; Normal: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2Cool_Lessdense_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2Orange_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2WarmInside_Lighter_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2Warm_Lighter_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2Warm_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2purple_Lessdense_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumeCool_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumeMid_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumeWARM_lessDense_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_IAC_Interior_1_p.Materials.ENV_EngergonGlassV3_MAT_INST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_IAC_LightSources_p.LightPlanes.BckSillouhetteSmoke_MATINST (SmokeCoolDepth_Mat) | K | EmissiveColor: Panner(0.02, 0.05) time-in, Time; Opacity: Panner(0.02, 0.05) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_IAC_LightSources_p.LightPlanes.BrightSmokeDecagon2_MATINST (SmokeCoolDepth_Mat) | K | EmissiveColor: Panner(0.02, 0.05) time-in, Time; Opacity: Panner(0.02, 0.05) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_IAC_LightSources_p.LightPlanes.ChasmDepths_Light_MATINST (SmokeCoolDepth_Mat) | K | EmissiveColor: Panner(0.02, 0.05) time-in, Time; Opacity: Panner(0.02, 0.05) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_IAC_LightSources_p.LightPlanes.ChasmDepths_MATINST (SmokeCoolDepth_Mat) | K | EmissiveColor: Panner(0.02, 0.05) time-in, Time; Opacity: Panner(0.02, 0.05) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_IAC_Orrery_p.cards.OrreryLines_and_icons_MAT (OrreryLines_and_icons_MAT) | K | EmissiveColor: Panner(0, -0.19), Panner(0.01, 0) | 0 / 0 | Unlit / Additive |
| ENV_IAC_Orrery_p.cards.OrreryRings_MAT (OrreryRings_MAT) | K | EmissiveColor: Panner(0, -0.19), Panner(0.01, 0) | 0 / 0 | Unlit / Additive |
| ENV_IAC_Shader_p.Material.IAC_Glass2_Dark_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_IAC_Shader_p.Material.IAC_Glass2_light_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_IAC_Shader_p.Material.IAC_Glass2_light_thin_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_IAC_Shader_p.Material.IAC_Glass_Trans_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_Dchevrons_clr_Mat (landmark_Dchevrons_clr_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_Dtarget_clr_Mat (landmark_Dtarget_clr_Mat) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_ablogo_clr_Mat (landmark_ablogo_clr_Mat) | K | EmissiveColor: Panner(-0.05, -0.03), Panner(0.02, 0.1) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_chevrons_clr_Mat (landmark_chevrons_clr_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_declogo_clr_Mat (landmark_declogo_clr_Mat) | K | EmissiveColor: Panner(-0.05, -0.03), Panner(0.02, 0.1) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_ring_clr_Mat (landmark_ring_clr_Mat) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_target_clr_Mat (landmark_target_clr_Mat) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| ENV_ORB_Spacedome_p.Spacedome_ORBITAL_MAT (Spacedome_ORBITAL_MAT) | K | EmissiveColor: Panner(0.0001, 0.0001), Rotator(0.0006 rad/s @0.5,0.5), Rotator(0.001 rad/s @0.5,0.5) | 0 / 0 | Phong / Opaque |
| FX_IonBlaster_p.IonBlaster_Mag_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| FX_Materials_p.MatInst.Blaster_Trail_MAT_INST (Blaster_MAT) | K | EmissiveColor: Panner(2.5, 0.5), Panner(3, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.CaptureZone_Reverse_MAT_INST (CaptureZoneLight_Base_MAT) | K | EmissiveColor: Panner(-0.15, 0.18), Panner(0, -0.05), Panner(0.01, -0.02), Time; Opacity: Panner(-0.15, 0.18), Panner(0, -0.05), Panner(0.01, -0.02), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.CircuitRadial_MATINST (CircuitRadial_MAT) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5), Sine(period 1); Opacity: Rotator(0.25 rad/s @0.5,0.5), Sine(period 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Distortion_Cloud_DBA_MAT_INST (Distortion_Cloud_01_MAT) | K | EmissiveColor: Panner(0, 0.3); Distortion: Panner(0, 0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.FusionBlasterBeam_MAT_INST (IonBlasterTrail_MAT) | K | EmissiveColor: Panner(2.5, 0.5), Panner(3, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.LightCylinder_Rays_MAT_INST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.LightVolume_Rays_MAT_INST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Lightning_Anim_03_UP_MAT_INST (Lightning_Anim_03_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.MuzzleFlash_X_Mat_INST (MuzzleFlash_X_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Smoke_Lrg_Mat_INST (SmokeThick_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.MatInst.Trail_Smoke_01_MAT_INST (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.MatInst.Trail_Smoke_10_MAT_INST (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.AmmoShell_MAT (AmmoShell_MAT) | K | EmissiveColor: Panner(0.04, 0.08), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.BlastSphere_Death_MAT (BlastSphere_Death_MAT) | K | EmissiveColor: Time; Distortion: Time | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.Bolt_ADD_MAT (Bolt_ADD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Distortion_Cloud_01_MAT (Distortion_Cloud_01_MAT) | K | EmissiveColor: Panner(0, 0.3); Distortion: Panner(0, 0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.EMPBlastSphere_MAT (EMPBlastSphere_MAT) | K | EmissiveColor: Panner(-0.5, 0.5), Panner(0.1, -1), Panner(0.25, 0.5); Distortion: Panner(-0.5, 0.5), Panner(0.1, -1), Panner(0.25, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.EMPBlastWave_MAT (EMPBlastWave_MAT) | K | EmissiveColor: Panner(-0.5, 0.5), Panner(0.25, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.ElectroRing01_Mat (ElectroRing01_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.ElectroRing02_Mat (ElectroRing02_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Embers_Blue_MAT_INST (Fire_MAT) | K | EmissiveColor: Panner(-0.15, 0.8), Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Explosion_MAT (Explosion_MAT) | K | EmissiveColor: Panner(1, 1), Rotator(0.5 rad/s @0.5,0.5), Time; Opacity: Panner(1, 1), Rotator(0.5 rad/s @0.5,0.5), Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Fire_MAT (Fire_MAT) | K | EmissiveColor: Panner(-0.15, 0.8), Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Fire_Ring01_Mat (Fire_Ring01_Mat) | K | EmissiveColor: Panner(0.4, 0.4) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.HealBeam_MAT (HealBeam_MAT) | K | EmissiveColor: Panner(-0.15, 0), Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.15, 0), Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LaserScanner_MAT (LaserScanner_MAT) | K | EmissiveColor: Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LightVolume_Base_MAT (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LightVolume_WepPickup_MAT (LightVolume_WepPickup_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_01_MAT (Lightning_Anim_01_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_02_MAT (Lightning_Anim_02_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_03_MAT (Lightning_Anim_03_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MFlash_Side_Desat_MAT (MFlash_Side_Desat_MAT) | K | EmissiveColor: Panner(1, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_Mat (MuzzleFlash_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_White_Mat (MuzzleFlash_White_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_X_Mat (MuzzleFlash_X_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ram_model_MAT (Ram_model_MAT) | K | EmissiveColor: Panner(-0.6, 0), Panner(0.6, 1.4), Panner(0.8, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ring_Distort_Add_MAT (Ring_Distort_Add_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ring_Distort_MAT (Ring_Distort_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Opacity: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Ring_Distort_Mesh_MAT (Ring_Distort_Mesh_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Rings_Distort_MAT (Rings_Distort_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Opacity: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.SmokeCoolDepth_Mat (SmokeCoolDepth_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.SmokeThick_Mat (SmokeThick_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Steam_Add_Mat (Steam_Add_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Steam_Mat (Steam_Mat) | K | EmissiveColor: Panner(0, 0.2); Opacity: Panner(0, 0.2) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Steam_Shade_Mat (Steam_Shade_Mat) | K | EmissiveColor: Panner(0, 0.2); Opacity: Panner(0, 0.2) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Tracer_ADD_MAT (Tracer_ADD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Tracer_MAT (Tracer_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Tracer_MOD_MAT (Tracer_MOD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.Tracer_Smoke_MAT (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.arcball01_MAT (arcball01_MAT) | K | EmissiveColor: Rotator(-2 rad/s @0.5,0.5), Rotator(1 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.bursting_MAT (bursting_MAT) | K | EmissiveColor: Panner(-1, 0); Opacity: Panner(-1, 0); Distortion: Panner(-1, 0); Normal: Panner(-1, 0) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Afterburn_02_MAT (Afterburn_02_MAT) | K | EmissiveColor: Panner(0.2, 2); Opacity: Panner(0.5, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Afterburn_Circuitry_02_MAT (Afterburn_Circuitry_02_MAT) | K | EmissiveColor: Panner(0.2, 2); Opacity: Panner(0, 0.5), Panner(0.1, 0.1), Panner(0.2, 2), Panner(0.5, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Boostermaterial_02_MAT (Boostermaterial_02_MAT) | K | EmissiveColor: Panner(1, 2); Opacity: Panner(1, 2) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.tank_hover_pattern_MAT (tank_hover_pattern_MAT) | K | EmissiveColor: Sine(period 1), Time; Opacity: Panner(0.3, 0.3), Rotator(1 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| FX_RollerMine_p.Material.FX_RollerMine_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| FX_Screen_p.Materials.Static_MAT (Static_MAT) | K | EmissiveColor: Panner(-0.805, -0.942), Panner(0.42, 0.513), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.MuzzleFlash_01_MAT (MuzzleFlash_01_MAT) | K | EmissiveColor: Panner(-0.15, 0.8); Opacity: Panner(-0.15, 0.8) | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.MuzzleFlash_Side_MAT (MuzzleFlash_Side_MAT) | K | EmissiveColor: Panner(1, 0); Opacity: Panner(1, 0) | 0 / 0 | Unlit / Additive |
| PROP_EnergonSigns_p.AnimTes_static_CLR_Mat (AnimTes_static_CLR_Mat) | K | EmissiveColor: Panner(0.03, 0.01), Panner(0.05, -0.06) | 0 / 0 | Unlit / Opaque |
| PROP_IAC_HospitalProps_p.ChemicalTank.PROP_ChemicalTankLiquid_MATINST (Energon_CubeB_Mat) | K | EmissiveColor: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(-0.15, 0.18), Panner(0.1, -0.075), Panner(0.2, 0.1); Normal: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(0.2, 0.1) | 0 / 0 | Phong / Opaque |
| PROP_IAC_Statues_p.Materials.Statue_Energon_MATINST (energonbanner_Mat) | K | EmissiveColor: Panner(0, -0.19), Panner(0.01, 0) | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.Barricade2.TPRO_NEU_Barricade2ForceField_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.BarricadeShield_MAT (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.RocketBarricade.TPRO_NEU_RocketBarrier_MATINST (Soundwave_ShieldBarrier_MAT) | K | EmissiveColor: Panner(-0.1, -0.5), Panner(0.1, -0.5), Panner(0.1, -0.75), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_BatteryOS_p.BatteryOmegaGlass_MATINST (ENV_Refractive_Glass_Trans_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Translucent |
| PROP_NEU_BatteryOS_p.OmegaLiquidSurface_MATINST (Coolant_Parent_MAT) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time; Normal: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_BatteryOS_p.OmegaLiquid_MATINST (TryptiGelGlass_Mat) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Translucent |
| PROP_NEU_EnergonCube_p.PROP_NEU_EnergonCube_Circuits_MATINST (PROP_NEU_EnergonCube_Circuits_MAT) | K | EmissiveColor: Panner(0, 1) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Interacts_p.PROP_ButtonInteract_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreenActivePurple_MATINST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreenDead_MAT_INST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreen_DeathBumb_MATINST (MonitorScreen_Optimus_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreen_DeathOpt_MATINST (MonitorScreen_Optimus_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreen_DeathSide_MATINST (MonitorScreen_Optimus_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Pickups_p.AmmoPickup.PROP_NEU_AmmoPickup_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.CodeOfPower.CodeOfPowerCORE_MatINST (CodeOfPower_MAT) | K | EmissiveColor: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(-0.15, 0.18), Panner(0.1, -0.075), Panner(0.2, 0.1); Opacity: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(0.2, 0.1); Distortion: Panner(-0.15, 0.18), Panner(0.1, -0.075) | 0 / 0 | Unlit / Translucent |
| PROP_NEU_Pickups_p.EnergonTotem.Conquest_Ring_MATINST (Conquest_Ring_MAT) | K | EmissiveColor: Rotator(-0.3 rad/s @0.5,0.5), Rotator(0.5 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| PROP_NEU_Pickups_p.EnergonTotem.PROP_NEU_EnergonTotem_MATINST (ENV_Hologram_Mat) | K | EmissiveColor: Panner(0, 0.1) time-in, Sine(period 1), Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.MPBomb.BombCore_MATINST_BAT (BombCore_MAT) | K | DiffuseColor: Cosine(period 0.5), Cosine(period 1), Time; EmissiveColor: Cosine(period 0.5), Cosine(period 1), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Pickups_p.MPBomb.PROP_NEU_MPBombExplode_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.MPBomb.PROP_NEU_MPBomb_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.OvershieldPickup.PROP_NEU_Overshield_MATINST (WEP_Crates_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Opaque |
| PROP_VendingMachine_p.Ammo.PROP_VendingMachine_Ammo_MATINST (VendingMachine_Screen_MAT) | K | EmissiveColor: Cosine(period 1) in Noise_MF, Panner(0, 1) time-in, Panner(1, 1) time-in in Noise_MF, Sine(period 1) in Noise_MF, Time, Time in Noise_MF | 0 / 0 | Unlit / Opaque |
| PROP_VendingMachine_p.PROP_VendingMachine_EnergonCube_MATINST (VendingMachine_Screen_MAT) | K | EmissiveColor: Cosine(period 1) in Noise_MF, Panner(0, 1) time-in, Panner(1, 1) time-in in Noise_MF, Sine(period 1) in Noise_MF, Time, Time in Noise_MF | 0 / 0 | Unlit / Opaque |
| TPRO_KON_CorruptorSpike_p.Materials.DarkEnergonCrystal_MATINST (DarkEnergonCrystal_MAT) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| TPRO_KON_CorruptorSpike_p.Materials.DarkEnergonCrystal_MAT_INST (DarkEnergonCrystal_MAT) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| TR_AirRaid_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_AirRaid_ROBO_p.RB_AirRaid_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_AirRaid_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_AirRaid_VEH_p.VH_AirRaid_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Arcee_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Arcee_ROBO_p.RB_Arcee_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Arcee_VEH_p.VH_Arcee_InteriorEnergon_Mat_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Arcee_VEH_p.VH_Arcee_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Barricade_ROBO_p.MaterialInstanceConstant_679 (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Barricade_ROBO_p.RB_Barricade_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Barricade_VEH_p.VH_Barricade_NormSpec_Cust_B_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Brawl_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Brawl_ROBO_p.RB_Brawl_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Brawl_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Brawl_VEH_p.VH_Brawl_NormSpec_Cust_B_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Breakdown_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Breakdown_ROBO_p.RB_Breakdown_Cust_Mat_Inst_E (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Breakdown_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Breakdown_VEH_p.RB_BreadownVEH_Cust_Mat_INST_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_ROBO_p.RB_BumbleBee2_Cust2_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_ROBO_p.RB_BumblebeeEnergon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_VEH_p.Materials.Bumblebee_TransformInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_VEH_p.VEH_BumbleBee2_Cust2_Mat (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Deadend_ROBO_p.RB_DeadendInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Deadend_ROBO_p.RB_Deadend_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Deadend_VEH_p.VH_DeadendInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Deadend_VEH_p.VH_Deadend_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Demolishor_ROBO_p.RB_Demolishor_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Demolishor_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Demolishor_VEH_p.VH_Demolishor_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ironhide_ROBO_p.RB_IronhideInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ironhide_ROBO_p.RB_Ironhide_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ironhide_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ironhide_VEH_p.VH_Ironhide_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jazz_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jazz_ROBO_p.RB_Jazz_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jazz_VEH_p.VH_Jazz_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jetfire_ROBO_p.RB_Jetfire_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jetfire_ROBO_p.TR_JetfireInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jetfire_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jetfire_VEH_p.VH_Jetfire_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Laserbeak_VEH_p.VH_Laserbeak_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Megatron_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Megatron_ROBO_p.VH_Megatron_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Megatron_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Megatron_VEH_p.VH_Megatron_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Onslaught_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Onslaught_ROBO_p.RB_Onslaught_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Onslaught_VEH_p.MaterialInstanceConstant_4774 (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Onslaught_VEH_p.VH_Onslaught_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Optimus_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Optimus_ROBO_p.RB_OptimusPrime_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Optimus_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Optimus_VEH_p.RB_OptimusPrime_Cust2_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ratchet_ROBO_p.RB_RatchetEnergonInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ratchet_ROBO_p.RB_Ratchet_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ratchet_VEH_p.VH_RatchetEnergonInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ratchet_VEH_p.VH_Ratchet_Cust2_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.FrenzyWeapon_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.Frenzy_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.RumbleWeapon_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.Rumble_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Scattershot_ROBO_p.RB_ScattershotInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Scattershot_ROBO_p.RB_Scattershot_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Scattershot_VEH_p.Debug.VH_ScattershotInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Scattershot_VEH_p.VH_Scattershot_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Shockwave_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Shockwave_ROBO_p.RB_Shockwave_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Shockwave_VEH_p.VH_Shockwave_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_ROBO_p.RB_Sideswipe_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_VEH_p.VH_Sideswipe_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_ROBO_p.RB_Silverbolt_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_VEH_p.VH_Silverbolt_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Skywarp_ROBO_p.RB_Skywarp_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Skywarp_ROBO_p.TR_Skywarp_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Skywarp_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Skywarp_VEH_p.VH_Skywarp_NormSpec_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Slipstream_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Slipstream_ROBO_p.RB_Slipstream_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Slipstream_VEH_p.VH_Slipstream_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_ROBO_p.RB_SoldierCarAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_ROBO_p.RB_SoldierMultiAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_VEH_p.VH_SoldierCarAut_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_ROBO_p.RB_SoldierCarDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_ROBO_p.RB_SoldierMultiDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_VEH_p.VH_SniperDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_ROBO_p.RB_SoldierCarNeu_Robo_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_ROBO_p.RB_SoldierMultiNeu_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_VEH_p.VH_SoldierCarNeu_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierTankAut_VEH_p.VH_SoldierTankAutA_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierTankDec_VEH_p.VH_SoldierTankDec_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Soundwave_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Soundwave_ROBO_p.RB_Soundwave_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Soundwave_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Soundwave_VEH_p.VH_Soundwave_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_ROBO_p.TR_Starscream_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_ROBO_p.TR_Starscream_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_StarScream_VEH_p.CHR_Transformer_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_VEH_p.VH_StarscreamInterior_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_ROBO_p.TR_Thunder_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Thunder_ROBO_p.TR_Thunder_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_VEH_p.VH_Thunder_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Trypticon_ROBO_p.RB_TrypticonHead_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Warpath_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Warpath_ROBO_p.RB_Warpath1_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Warpath_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Warpath_VEH_p.RB_Warpath1_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_ROBO_p.TR_ZetaPrime_ROBO_Cust_Mat_Inst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_VEH_p.VH_ZetaPrimeInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_VEH_p.VH_ZetaPrime_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| UI_GFxHud_p.LowHealth.LowHealthScreenEffect_M (LowHealthScreenEffect_M) | K | EmissiveColor: Panner(0, -2), Panner(0, 1) | 0 / 0 | Unlit / Opaque |
| UI_GFxHud_p.StaticDischargeScreenEffect_M (StaticDischargeScreenEffect_M) | K | EmissiveColor: Panner(-0.805, -0.942), Panner(0.42, 0.513) | 0 / 0 | Unlit / Opaque |
| UI_HudMarkers_p.MPMarkerBase_MAT (MPMarkerBase_MAT) | K | Opacity: Cosine(period 1), Panner(0, -2) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MPMarkerCOP_MAT (MPMarkerCOP_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MPMarkerDominationNode_MAT (MPMarkerDominationNode_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MarkerDownedAlly_MAT (MarkerDownedAlly_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MarkerGrenade_MAT (MarkerGrenade_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| WEP_AssaultRifle_p.WEP_AssaultRifle_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Axe_p.Autobot.WEP_Axe_Energon_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_BazookaTemp1_p.WEP_Bazooka_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BeatDownClub_p.WEP_BeatDownClub_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BroadSword_p.WEP_BroadSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_BroadSword_p.WEP_BroadSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BurstRifle_p.Materials.WEP_BurstRifle_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ButterflyAxe_p.WEP_ButterflyAxeEnergon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ButterflyAxe_p.WEP_ButterflyAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_CeremonialStaff_p.WEP_CeremonialStaff_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_CodeOfPower_p.WEP_CodeOfPower_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_DetPack_p.WEP_DetPack_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_EMPShotgun_p.WEP_EMPShotgun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_FightingStaff_p.WEP_FightingStaff_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_GrenadeLauncher_p.WEP_GrenadeLauncher_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Grenade_p.WEP_Grenade_Flak_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HalberdAxe_p.WEP_HalberdAxe_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_HalberdAxe_p.WEP_HalberdAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Hammer_p.WEP_Hammer_D_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Hammer_p.WEP_Hammer_Spikes_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_HeavyMG_p.WEP_HeavyMG_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HeavyPistol_p.WEP_HeavyPistol_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HuntingDagger_p.WEP_HuntingDagger_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_IonBlaster_p.WEP_IonBlaster_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_KamikazeMine_p.WEP_KamikazeMine_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_LancingSpear_p.WEP_LancingSpear_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_LongSword_p.WEP_LongSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_LongSword_p.WEP_LongSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Maul_p.WEP_Maul_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_Maul_p.WEP_Maul_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_PlasmaCannon_p.WEP_PlasmaCannon_A_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ProngDagger_p.WEP_Energon_A_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_ProngDagger_p.WEP_ProngDagger_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_RepairBeam_p.WEP_RepairBeam_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_RocketLauncher_p.WEP_RocketLauncher_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryAbility_p.WEP_DeployedTurret_MATINST (WEP_SentryAbility_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Sine(period 1), Time; OpacityMask: Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryBase.WEP_GlassGlow_MATINST (ENV_Refractive_Glass_Opaque_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| WEP_SentryBlaster01_p.SentryBase.WEP_SentryBase_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryBlaster.WEP_SentryBlaster_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryRepair.WEP_SentryRepair_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryRocket.WEP_SentryRocket_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SerratedBlade_p.WEP_SerratedBlade_Energon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SerratedBlade_p.WEP_SerratedBlade_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shared_p.WEP_Energon_D_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_Shared_p.WEP_PhongMain_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_Frame_MATINST (WEP_Barrier_A_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(0.01, -0.02) time-in in ElectricArcs_MF, Sine(period 1) in ElectricArcs_MF, Sine(period 1) in ScanLines_MF, Time in ElectricArcs_MF, Time in ScanLines_MF | 0 / 0 | Unlit / Translucent |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_MASK_MATINST (WEP_ShieldBruteA_MASK_MAT) | K | EmissiveColor: Panner(-0.75, 0.25), Panner(0.75, -0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Barrier.ENV_ForceField_Defrag_MAT (ENV_ForceField_Defrag_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(1, -0.5), Panner(1, 0) time-in, Rotator(0.25 rad/s @0.5,0.5), Sine(period 1), Sine(period 1) in ScanLines_MF, Time, Time in ScanLines_MF; Opacity: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Barrier.WEP_Barrier_Defrag_MATINST (ENV_ForceField_Defrag_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(1, -0.5), Panner(1, 0) time-in, Rotator(0.25 rad/s @0.5,0.5), Sine(period 1), Sine(period 1) in ScanLines_MF, Time, Time in ScanLines_MF; Opacity: Rotator(0.25 rad/s @0.5,0.5); Distortion: Panner(-0.04, -0.12), Panner(0.2, 0.1) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_Frame_MATINST (WEP_Barrier_A_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(0.01, -0.02) time-in in ElectricArcs_MF, Sine(period 1) in ElectricArcs_MF, Sine(period 1) in ScanLines_MF, Time in ElectricArcs_MF, Time in ScanLines_MF | 0 / 0 | Unlit / Translucent |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_MASK_MATINST (WEP_ShieldBruteA_MASK_MAT) | K | EmissiveColor: Panner(-0.75, 0.25), Panner(0.75, -0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Decepticon.WEP_ShieldD_Energon_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_ShortSword_p.WEP_ShortSword_Energon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ShortSword_p.WEP_ShortSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shotgun_p.WEP_Shotgun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SniperRifle_p.WEP_SniperRifle_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SpikedBat_p.WEP_SpikedBat_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SpikedBat_p.WEP_SpikedBat_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SpikedMace_p.WEP_SpikedMace_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SpikedMace_p.WEP_SpikedMace_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TortureSword_p.WEP_TortureSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_TortureSword_p.WEP_TortureSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TrypticonMouthCannon_p.WEP_TrypMouthCannon_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TrypticonShoulderCannon_p.WEP_TrypShoulderCannon_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun01_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun_Overshield_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(-0.05, -0.1) time-in in Overshield_MFUNC, Panner(-0.1, -0.5) time-in in Overshield_MFUNC, Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Panner(0.2, 0.1) time-in in Overshield_MFUNC, Panner(0.5, 0.1) time-in in Overshield_MFUNC, Time, Time in Overshield_MFUNC | 0 / 0 | Phong / Masked |
| WEP_TurretRocket_p.WEP_TurretRocket_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ViciousAxe_p.WEP_ViciousAxe_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ViciousAxe_p.WEP_ViciousAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_WarHammer_p.WEP_WarHammer_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_WarHammer_p.WEP_WarHammer_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |

### MP_IAC_Streets: 311 time-driven materials (K 311)

| Material (master) | Ours | Time sources by output | Draws / tris | Lighting / blend |
|---|---|---|---|---|
| ENV_ORB_PowerCorridor_p.Materials.PowerTubeEmissPulse_MATINST (PowerTube_EmissPulse_MAT) | K | EmissiveColor: Panner(0.4, 0) | 3 / 1488 | Phong / Opaque |
| ENV_IAC_Shader_p.Material.IAC_Glass2_light_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 52 / 1212 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_Dchevrons_clr_Mat (landmark_Dchevrons_clr_Mat) | K | EmissiveColor: Panner(0, 0.2) | 10 / 1100 | Unlit / Additive |
| DES_IAC_WallPanelSign_p.Materials.WallPanelSign_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 2 / 1000 | Phong / Opaque |
| ENV_IAC_Decagon_p.Materials.IAC_Decagon_GlassPan2_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(0, 1) time-in, Sine(period 1), Time | 18 / 720 | Unlit / Additive |
| PROP_NEU_Pickups_p.AmmoPickup.PROP_NEU_AmmoPickup_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 1 / 676 | Phong / Masked |
| FX_Materials_p.MatInst.CaptureZone_Reverse_MAT_INST (CaptureZoneLight_Base_MAT) | K | EmissiveColor: Panner(-0.15, 0.18), Panner(0, -0.05), Panner(0.01, -0.02), Time; Opacity: Panner(-0.15, 0.18), Panner(0, -0.05), Panner(0.01, -0.02), Time | 1 / 640 | Unlit / Additive |
| FX_Navigation_p.Afterburn_02_MAT (Afterburn_02_MAT) | K | EmissiveColor: Panner(0.2, 2); Opacity: Panner(0.5, 0.5) | 1 / 600 | Unlit / Additive |
| FX_Navigation_p.Afterburn_Circuitry_02_MAT (Afterburn_Circuitry_02_MAT) | K | EmissiveColor: Panner(0.2, 2); Opacity: Panner(0, 0.5), Panner(0.1, 0.1), Panner(0.2, 2), Panner(0.5, 0.5) | 1 / 600 | Unlit / Additive |
| FX_Navigation_p.Boostermaterial_02_MAT (Boostermaterial_02_MAT) | K | EmissiveColor: Panner(1, 2); Opacity: Panner(1, 2) | 1 / 600 | Unlit / Additive |
| FX_Materials_p.Materials.LightVolume_WepPickup_MAT (LightVolume_WepPickup_MAT) | K | EmissiveColor: Time | 1 / 480 | Unlit / Additive |
| ENV_IAC_Decagon_p.DestroyedStairs.BurnHole_MAT (BurnHole_MAT) | K | EmissiveColor: Panner(0.02, 0.02) time-in, Rotator(0.001 rad/s @0.5,0.5), Sine(period 2), Time | 1 / 454 | Phong / Opaque |
| FX_Materials_p.Materials.Ram_model_MAT (Ram_model_MAT) | K | EmissiveColor: Panner(-0.6, 0), Panner(0.6, 1.4), Panner(0.8, 0) | 1 / 420 | Unlit / Additive |
| ENV_CORE_Shader_p.Material.ENV_ForceFieldNoDestortion_MATINST_INST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 2 / 288 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2Warm_Lighter_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 7 / 280 | Unlit / Additive |
| PROP_NEU_Pickups_p.OvershieldPickup.PROP_NEU_Overshield_MATINST (WEP_Crates_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 1 / 222 | Phong / Opaque |
| ENV_IAC_Background_p.Materials.Iacon_Nebula_D_MAT (Iacon_Nebula_D_MAT) | K | EmissiveColor: Panner(0.0001, 0.0001), Rotator(0.0006 rad/s @0.5,0.5), Rotator(0.001 rad/s @0.5,0.5) | 1 / 180 | Phong / Opaque |
| ENV_NEU_landmarking_p.landmark_chevrons_clr_Mat (landmark_chevrons_clr_Mat) | K | EmissiveColor: Panner(0, 0.2) | 4 / 153 | Unlit / Additive |
| ENV_IAC_Shader_p.Material.IAC_Glass_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 6 / 144 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2Orange_Light_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 3 / 120 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRays_RED_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 3 / 120 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumePurplish_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 3 / 120 | Unlit / Additive |
| PROP_NEU_EnergonCube_p.PROP_NEU_EnergonCube_Circuits_MATINST (PROP_NEU_EnergonCube_Circuits_MAT) | K | EmissiveColor: Panner(0, 1) time-in, Sine(period 1), Time | 1 / 120 | Unlit / Additive |
| ENV_IAC_Shader_p.Material.IAC_Glass2_dense_Dark_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 4 / 112 | Unlit / Additive |
| FX_IonBlaster_p.IonBlaster_Mag_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 1 / 100 | Phong / Masked |
| PROP_EnergonSigns_p.AnimTes_staticLong_CLR_Mat (AnimTes_staticLong_CLR_Mat) | K | EmissiveColor: Panner(0.03, 0.01), Panner(0.05, -0.06) | 1 / 96 | Unlit / Opaque |
| FX_Materials_p.MatInst.LightCylinder_Rays_MAT_INST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 1 / 80 | Unlit / Additive |
| ENV_IAC_Ground_p.Material.ENV_EngergonGlass_MAT_INST (ENV_EnergonCube_MAT) | K | EmissiveColor: Panner(-0.15, 0.18), Panner(0.1, -0.075) | 1 / 68 | Unlit / Opaque |
| PROP_EnergonSigns_p.AnimSign4_CLR_Mat (AnimSign4_CLR_Mat) | K | EmissiveColor: FlipBook(AnimTest4 4x4 @8 fps), Panner(0, -0.19), Panner(0.01, 0) | 1 / 60 | Unlit / Additive |
| WEP_GrenadeLauncher_p.WEP_GrenadeLauncher_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 1 / 60 | Phong / Masked |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2Orange_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 3 / 44 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2Cool_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 1 / 40 | Unlit / Additive |
| ENV_IAC_LightSources_p.LightPlanes.BckSillouhetteSmoke_MATINST (SmokeCoolDepth_Mat) | K | EmissiveColor: Panner(0.02, 0.05) time-in, Time; Opacity: Panner(0.02, 0.05) time-in, Time | 20 / 40 | Unlit / Translucent |
| ENV_AllShader_p.Release.ENV_ForceField_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 1 / 28 | Unlit / Additive |
| ENV_AllShader_p.Energon_River.Energon_Lava_Mat (Energon_Lava_Mat) | K | EmissiveColor: Panner(-0.015, 0.01), Panner(-0.02, -0.06) time-in, Panner(-0.02, 0.03), Panner(-0.09, 0.02), Panner(0.01, -0.01), Panner(0.01, -0.075), Panner(0.1, 0.05) time-in, Time | 2 / 24 | Unlit / Translucent |
| PROP_NEU_Monitors_p.MonitorScreenActive_MAT_INST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 9 / 18 | Phong / Opaque |
| PROP_EnergonSigns_p.AnimSign3_CLR_Mat (AnimSign3_CLR_Mat) | K | EmissiveColor: FlipBook(AnimTest3 4x4 @15 fps), Panner(0, -0.19), Panner(0.01, 0) | 1 / 12 | Unlit / Additive |
| PROP_EnergonSigns_p.AnimSign5_CLR_Mat (AnimSign5_CLR_Mat) | K | EmissiveColor: FlipBook(AnimTest5 3x3 @5 fps), Panner(0, -0.19), Panner(0.01, 0) | 1 / 12 | Unlit / Additive |
| PROP_EnergonSigns_p.AnimSign6_CLR_Mat (AnimSign6_CLR_Mat) | K | EmissiveColor: FlipBook(AnimTest6 2x2 @4 fps), Panner(0, -0.19), Panner(0.01, 0) | 1 / 12 | Unlit / Additive |
| PROP_EnergonSigns_p.AnimSign5_Decepticon_CLR_Mat (AnimSign5_Decepticon_CLR_Mat) | K | EmissiveColor: FlipBook(AnimTest5 3x3 @5 fps), Panner(0, -0.19), Panner(0.01, 0) | 3 / 6 | Unlit / Additive |
| PROP_EnergonSigns_p.AutobotLOGO_CLR_Mat (AutobotLOGO_CLR_Mat) | K | EmissiveColor: Panner(0, -0.19), Panner(0.01, 0) | 2 / 4 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightCylinder2_Rays_Red_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 1 / 2 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_Dtarget_clr_Mat (landmark_Dtarget_clr_Mat) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5) | 1 / 2 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_declogo_clr_Mat (landmark_declogo_clr_Mat) | K | EmissiveColor: Panner(-0.05, -0.03), Panner(0.02, 0.1) | 1 / 2 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_target_clr_Mat (landmark_target_clr_Mat) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5) | 1 / 2 | Unlit / Additive |
| PROP_NEU_Monitors_p.MonitorScreenActivePurple_MATINST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 1 / 2 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreenDead_MAT_INST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 1 / 2 | Phong / Opaque |
| DES_IAC_WallPanelSign_p.Materials.WallPanelSign_EMISSOFF_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| FX_Materials_p.MatInst.Blaster_Trail_MAT_INST (Blaster_MAT) | K | EmissiveColor: Panner(2.5, 0.5), Panner(3, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.CircuitRadial_MATINST (CircuitRadial_MAT) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5), Sine(period 1); Opacity: Rotator(0.25 rad/s @0.5,0.5), Sine(period 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Distortion_Cloud_DBA_MAT_INST (Distortion_Cloud_01_MAT) | K | EmissiveColor: Panner(0, 0.3); Distortion: Panner(0, 0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.FusionBlasterBeam_MAT_INST (IonBlasterTrail_MAT) | K | EmissiveColor: Panner(2.5, 0.5), Panner(3, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.LightVolume_Rays_MAT_INST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Lightning_Anim_03_UP_MAT_INST (Lightning_Anim_03_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.MuzzleFlash_X_Mat_INST (MuzzleFlash_X_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Smoke_Lrg_Mat_INST (SmokeThick_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.MatInst.Trail_Smoke_01_MAT_INST (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.MatInst.Trail_Smoke_10_MAT_INST (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.AmmoShell_MAT (AmmoShell_MAT) | K | EmissiveColor: Panner(0.04, 0.08), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.BlastSphere_Death_MAT (BlastSphere_Death_MAT) | K | EmissiveColor: Time; Distortion: Time | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.Bolt_ADD_MAT (Bolt_ADD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Distortion_Cloud_01_MAT (Distortion_Cloud_01_MAT) | K | EmissiveColor: Panner(0, 0.3); Distortion: Panner(0, 0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.EMPBlastSphere_MAT (EMPBlastSphere_MAT) | K | EmissiveColor: Panner(-0.5, 0.5), Panner(0.1, -1), Panner(0.25, 0.5); Distortion: Panner(-0.5, 0.5), Panner(0.1, -1), Panner(0.25, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.EMPBlastWave_MAT (EMPBlastWave_MAT) | K | EmissiveColor: Panner(-0.5, 0.5), Panner(0.25, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.ElectroRing01_Mat (ElectroRing01_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.ElectroRing02_Mat (ElectroRing02_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Embers_Blue_MAT_INST (Fire_MAT) | K | EmissiveColor: Panner(-0.15, 0.8), Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Explosion_MAT (Explosion_MAT) | K | EmissiveColor: Panner(1, 1), Rotator(0.5 rad/s @0.5,0.5), Time; Opacity: Panner(1, 1), Rotator(0.5 rad/s @0.5,0.5), Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Fire_MAT (Fire_MAT) | K | EmissiveColor: Panner(-0.15, 0.8), Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Fire_Ring01_Mat (Fire_Ring01_Mat) | K | EmissiveColor: Panner(0.4, 0.4) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.HealBeam_MAT (HealBeam_MAT) | K | EmissiveColor: Panner(-0.15, 0), Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.15, 0), Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LaserScanner_MAT (LaserScanner_MAT) | K | EmissiveColor: Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LightVolume_Base_MAT (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_01_MAT (Lightning_Anim_01_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_02_MAT (Lightning_Anim_02_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_03_MAT (Lightning_Anim_03_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MFlash_Side_Desat_MAT (MFlash_Side_Desat_MAT) | K | EmissiveColor: Panner(1, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_Mat (MuzzleFlash_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_White_Mat (MuzzleFlash_White_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_X_Mat (MuzzleFlash_X_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ring_Distort_Add_MAT (Ring_Distort_Add_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ring_Distort_MAT (Ring_Distort_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Opacity: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Ring_Distort_Mesh_MAT (Ring_Distort_Mesh_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Rings_Distort_MAT (Rings_Distort_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Opacity: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.SmokeCoolDepth_Mat (SmokeCoolDepth_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.SmokeThick_Mat (SmokeThick_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Steam_Add_Mat (Steam_Add_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Steam_Mat (Steam_Mat) | K | EmissiveColor: Panner(0, 0.2); Opacity: Panner(0, 0.2) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Steam_Shade_Mat (Steam_Shade_Mat) | K | EmissiveColor: Panner(0, 0.2); Opacity: Panner(0, 0.2) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Tracer_ADD_MAT (Tracer_ADD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Tracer_MAT (Tracer_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Tracer_MOD_MAT (Tracer_MOD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.Tracer_Smoke_MAT (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.arcball01_MAT (arcball01_MAT) | K | EmissiveColor: Rotator(-2 rad/s @0.5,0.5), Rotator(1 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.bursting_MAT (bursting_MAT) | K | EmissiveColor: Panner(-1, 0); Opacity: Panner(-1, 0); Distortion: Panner(-1, 0); Normal: Panner(-1, 0) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.tank_hover_pattern_MAT (tank_hover_pattern_MAT) | K | EmissiveColor: Sine(period 1), Time; Opacity: Panner(0.3, 0.3), Rotator(1 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| FX_RollerMine_p.Material.FX_RollerMine_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| FX_Screen_p.Materials.Static_MAT (Static_MAT) | K | EmissiveColor: Panner(-0.805, -0.942), Panner(0.42, 0.513), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.MuzzleFlash_01_MAT (MuzzleFlash_01_MAT) | K | EmissiveColor: Panner(-0.15, 0.8); Opacity: Panner(-0.15, 0.8) | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.MuzzleFlash_Side_MAT (MuzzleFlash_Side_MAT) | K | EmissiveColor: Panner(1, 0); Opacity: Panner(1, 0) | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.Barricade2.TPRO_NEU_Barricade2ForceField_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.BarricadeShield_MAT (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.RocketBarricade.TPRO_NEU_RocketBarrier_MATINST (Soundwave_ShieldBarrier_MAT) | K | EmissiveColor: Panner(-0.1, -0.5), Panner(0.1, -0.5), Panner(0.1, -0.75), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_BatteryOS_p.BatteryOmegaGlass_MATINST (ENV_Refractive_Glass_Trans_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Translucent |
| PROP_NEU_BatteryOS_p.OmegaLiquidSurface_MATINST (Coolant_Parent_MAT) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time; Normal: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_BatteryOS_p.OmegaLiquid_MATINST (TryptiGelGlass_Mat) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Translucent |
| PROP_NEU_Interacts_p.PROP_ButtonInteract_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| PROP_NEU_Pickups_p.CodeOfPower.CodeOfPowerCORE_MatINST (CodeOfPower_MAT) | K | EmissiveColor: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(-0.15, 0.18), Panner(0.1, -0.075), Panner(0.2, 0.1); Opacity: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(0.2, 0.1); Distortion: Panner(-0.15, 0.18), Panner(0.1, -0.075) | 0 / 0 | Unlit / Translucent |
| PROP_NEU_Pickups_p.EnergonTotem.Conquest_Ring_MATINST (Conquest_Ring_MAT) | K | EmissiveColor: Rotator(-0.3 rad/s @0.5,0.5), Rotator(0.5 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| PROP_NEU_Pickups_p.EnergonTotem.PROP_NEU_EnergonTotem_MATINST (ENV_Hologram_Mat) | K | EmissiveColor: Panner(0, 0.1) time-in, Sine(period 1), Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.MPBomb.BombCore_MATINST_BAT (BombCore_MAT) | K | DiffuseColor: Cosine(period 0.5), Cosine(period 1), Time; EmissiveColor: Cosine(period 0.5), Cosine(period 1), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Pickups_p.MPBomb.PROP_NEU_MPBombExplode_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.MPBomb.PROP_NEU_MPBomb_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_VendingMachine_p.Ammo.PROP_VendingMachine_Ammo_MATINST (VendingMachine_Screen_MAT) | K | EmissiveColor: Cosine(period 1) in Noise_MF, Panner(0, 1) time-in, Panner(1, 1) time-in in Noise_MF, Sine(period 1) in Noise_MF, Time, Time in Noise_MF | 0 / 0 | Unlit / Opaque |
| PROP_VendingMachine_p.PROP_VendingMachine_EnergonCube_MATINST (VendingMachine_Screen_MAT) | K | EmissiveColor: Cosine(period 1) in Noise_MF, Panner(0, 1) time-in, Panner(1, 1) time-in in Noise_MF, Sine(period 1) in Noise_MF, Time, Time in Noise_MF | 0 / 0 | Unlit / Opaque |
| TPRO_KON_CorruptorSpike_p.Materials.DarkEnergonCrystal_MAT_INST (DarkEnergonCrystal_MAT) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| TR_AirRaid_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_AirRaid_ROBO_p.RB_AirRaid_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_AirRaid_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_AirRaid_VEH_p.VH_AirRaid_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Arcee_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Arcee_ROBO_p.RB_Arcee_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Arcee_VEH_p.VH_Arcee_InteriorEnergon_Mat_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Arcee_VEH_p.VH_Arcee_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Barricade_ROBO_p.MaterialInstanceConstant_679 (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Barricade_ROBO_p.RB_Barricade_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Barricade_VEH_p.VH_Barricade_NormSpec_Cust_B_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Brawl_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Brawl_ROBO_p.RB_Brawl_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Brawl_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Brawl_VEH_p.VH_Brawl_NormSpec_Cust_B_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Breakdown_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Breakdown_ROBO_p.RB_Breakdown_Cust_Mat_Inst_E (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Breakdown_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Breakdown_VEH_p.RB_BreadownVEH_Cust_Mat_INST_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_ROBO_p.RB_BumbleBee2_Cust2_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_ROBO_p.RB_BumblebeeEnergon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_VEH_p.Materials.Bumblebee_TransformInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_VEH_p.VEH_BumbleBee2_Cust2_Mat (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Deadend_ROBO_p.RB_DeadendInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Deadend_ROBO_p.RB_Deadend_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Deadend_VEH_p.VH_DeadendInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Deadend_VEH_p.VH_Deadend_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Demolishor_ROBO_p.RB_Demolishor_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Demolishor_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Demolishor_VEH_p.VH_Demolishor_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ironhide_ROBO_p.RB_IronhideInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ironhide_ROBO_p.RB_Ironhide_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ironhide_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ironhide_VEH_p.VH_Ironhide_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jazz_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jazz_ROBO_p.RB_Jazz_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jazz_VEH_p.VH_Jazz_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jetfire_ROBO_p.RB_Jetfire_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jetfire_ROBO_p.TR_JetfireInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jetfire_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jetfire_VEH_p.VH_Jetfire_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Laserbeak_VEH_p.VH_Laserbeak_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Megatron_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Megatron_ROBO_p.VH_Megatron_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Megatron_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Megatron_VEH_p.VH_Megatron_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Onslaught_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Onslaught_ROBO_p.RB_Onslaught_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Onslaught_VEH_p.MaterialInstanceConstant_4774 (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Onslaught_VEH_p.VH_Onslaught_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Optimus_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Optimus_ROBO_p.RB_OptimusPrime_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Optimus_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Optimus_VEH_p.RB_OptimusPrime_Cust2_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ratchet_ROBO_p.RB_RatchetEnergonInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ratchet_ROBO_p.RB_Ratchet_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ratchet_VEH_p.VH_RatchetEnergonInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ratchet_VEH_p.VH_Ratchet_Cust2_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.FrenzyWeapon_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.Frenzy_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.RumbleWeapon_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.Rumble_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Scattershot_ROBO_p.RB_ScattershotInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Scattershot_ROBO_p.RB_Scattershot_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Scattershot_VEH_p.Debug.VH_ScattershotInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Scattershot_VEH_p.VH_Scattershot_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Shockwave_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Shockwave_ROBO_p.RB_Shockwave_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Shockwave_VEH_p.VH_Shockwave_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_ROBO_p.RB_Sideswipe_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_VEH_p.VH_Sideswipe_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_ROBO_p.RB_Silverbolt_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_VEH_p.VH_Silverbolt_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Skywarp_ROBO_p.RB_Skywarp_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Skywarp_ROBO_p.TR_Skywarp_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Skywarp_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Skywarp_VEH_p.VH_Skywarp_NormSpec_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Slipstream_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Slipstream_ROBO_p.RB_Slipstream_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Slipstream_VEH_p.VH_Slipstream_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_ROBO_p.RB_SoldierCarAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_ROBO_p.RB_SoldierMultiAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_VEH_p.VH_SoldierCarAut_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_ROBO_p.RB_SoldierCarDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_ROBO_p.RB_SoldierMultiDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_VEH_p.VH_SniperDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_ROBO_p.RB_SoldierCarNeu_Robo_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_ROBO_p.RB_SoldierMultiNeu_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_VEH_p.VH_SoldierCarNeu_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierTankAut_VEH_p.VH_SoldierTankAutA_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierTankDec_VEH_p.VH_SoldierTankDec_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Soundwave_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Soundwave_ROBO_p.RB_Soundwave_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Soundwave_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Soundwave_VEH_p.VH_Soundwave_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_ROBO_p.TR_Starscream_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_ROBO_p.TR_Starscream_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_StarScream_VEH_p.CHR_Transformer_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_VEH_p.VH_StarscreamInterior_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_ROBO_p.TR_Thunder_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Thunder_ROBO_p.TR_Thunder_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_VEH_p.VH_Thunder_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Trypticon_ROBO_p.RB_TrypticonHead_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Warpath_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Warpath_ROBO_p.RB_Warpath1_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Warpath_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Warpath_VEH_p.RB_Warpath1_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_ROBO_p.TR_ZetaPrime_ROBO_Cust_Mat_Inst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_VEH_p.VH_ZetaPrimeInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_VEH_p.VH_ZetaPrime_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| UI_GFxHud_p.LowHealth.LowHealthScreenEffect_M (LowHealthScreenEffect_M) | K | EmissiveColor: Panner(0, -2), Panner(0, 1) | 0 / 0 | Unlit / Opaque |
| UI_GFxHud_p.StaticDischargeScreenEffect_M (StaticDischargeScreenEffect_M) | K | EmissiveColor: Panner(-0.805, -0.942), Panner(0.42, 0.513) | 0 / 0 | Unlit / Opaque |
| UI_HudMarkers_p.MPMarkerBase_MAT (MPMarkerBase_MAT) | K | Opacity: Cosine(period 1), Panner(0, -2) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MPMarkerCOP_MAT (MPMarkerCOP_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MPMarkerDominationNode_MAT (MPMarkerDominationNode_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MarkerDownedAlly_MAT (MarkerDownedAlly_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MarkerGrenade_MAT (MarkerGrenade_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| WEP_AssaultRifle_p.WEP_AssaultRifle_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Axe_p.Autobot.WEP_Axe_Energon_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_BazookaTemp1_p.WEP_Bazooka_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BeatDownClub_p.WEP_BeatDownClub_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BroadSword_p.WEP_BroadSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_BroadSword_p.WEP_BroadSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BurstRifle_p.Materials.WEP_BurstRifle_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ButterflyAxe_p.WEP_ButterflyAxeEnergon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ButterflyAxe_p.WEP_ButterflyAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_CeremonialStaff_p.WEP_CeremonialStaff_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_CodeOfPower_p.WEP_CodeOfPower_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_DetPack_p.WEP_DetPack_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_EMPShotgun_p.WEP_EMPShotgun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_FightingStaff_p.WEP_FightingStaff_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Grenade_p.WEP_Grenade_Flak_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HalberdAxe_p.WEP_HalberdAxe_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_HalberdAxe_p.WEP_HalberdAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Hammer_p.WEP_Hammer_D_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Hammer_p.WEP_Hammer_Spikes_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_HeavyMG_p.WEP_HeavyMG_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HeavyPistol_p.WEP_HeavyPistol_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HuntingDagger_p.WEP_HuntingDagger_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_IonBlaster_p.WEP_IonBlaster_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_KamikazeMine_p.WEP_KamikazeMine_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_LancingSpear_p.WEP_LancingSpear_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_LongSword_p.WEP_LongSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_LongSword_p.WEP_LongSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Maul_p.WEP_Maul_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_Maul_p.WEP_Maul_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_PlasmaCannon_p.WEP_PlasmaCannon_A_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ProngDagger_p.WEP_Energon_A_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_ProngDagger_p.WEP_ProngDagger_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_RepairBeam_p.WEP_RepairBeam_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_RocketLauncher_p.WEP_RocketLauncher_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryAbility_p.WEP_DeployedTurret_MATINST (WEP_SentryAbility_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Sine(period 1), Time; OpacityMask: Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryBase.WEP_GlassGlow_MATINST (ENV_Refractive_Glass_Opaque_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| WEP_SentryBlaster01_p.SentryBase.WEP_SentryBase_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryBlaster.WEP_SentryBlaster_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryRepair.WEP_SentryRepair_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryRocket.WEP_SentryRocket_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SerratedBlade_p.WEP_SerratedBlade_Energon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SerratedBlade_p.WEP_SerratedBlade_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shared_p.WEP_Energon_D_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_Shared_p.WEP_PhongMain_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_Frame_MATINST (WEP_Barrier_A_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(0.01, -0.02) time-in in ElectricArcs_MF, Sine(period 1) in ElectricArcs_MF, Sine(period 1) in ScanLines_MF, Time in ElectricArcs_MF, Time in ScanLines_MF | 0 / 0 | Unlit / Translucent |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_MASK_MATINST (WEP_ShieldBruteA_MASK_MAT) | K | EmissiveColor: Panner(-0.75, 0.25), Panner(0.75, -0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Barrier.ENV_ForceField_Defrag_MAT (ENV_ForceField_Defrag_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(1, -0.5), Panner(1, 0) time-in, Rotator(0.25 rad/s @0.5,0.5), Sine(period 1), Sine(period 1) in ScanLines_MF, Time, Time in ScanLines_MF; Opacity: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Barrier.WEP_Barrier_Defrag_MATINST (ENV_ForceField_Defrag_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(1, -0.5), Panner(1, 0) time-in, Rotator(0.25 rad/s @0.5,0.5), Sine(period 1), Sine(period 1) in ScanLines_MF, Time, Time in ScanLines_MF; Opacity: Rotator(0.25 rad/s @0.5,0.5); Distortion: Panner(-0.04, -0.12), Panner(0.2, 0.1) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_Frame_MATINST (WEP_Barrier_A_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(0.01, -0.02) time-in in ElectricArcs_MF, Sine(period 1) in ElectricArcs_MF, Sine(period 1) in ScanLines_MF, Time in ElectricArcs_MF, Time in ScanLines_MF | 0 / 0 | Unlit / Translucent |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_MASK_MATINST (WEP_ShieldBruteA_MASK_MAT) | K | EmissiveColor: Panner(-0.75, 0.25), Panner(0.75, -0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Decepticon.WEP_ShieldD_Energon_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_ShortSword_p.WEP_ShortSword_Energon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ShortSword_p.WEP_ShortSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shotgun_p.WEP_Shotgun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SniperRifle_p.WEP_SniperRifle_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SpikedBat_p.WEP_SpikedBat_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SpikedBat_p.WEP_SpikedBat_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SpikedMace_p.WEP_SpikedMace_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SpikedMace_p.WEP_SpikedMace_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TortureSword_p.WEP_TortureSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_TortureSword_p.WEP_TortureSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TrypticonMouthCannon_p.WEP_TrypMouthCannon_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TrypticonShoulderCannon_p.WEP_TrypShoulderCannon_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun01_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun_Overshield_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(-0.05, -0.1) time-in in Overshield_MFUNC, Panner(-0.1, -0.5) time-in in Overshield_MFUNC, Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Panner(0.2, 0.1) time-in in Overshield_MFUNC, Panner(0.5, 0.1) time-in in Overshield_MFUNC, Time, Time in Overshield_MFUNC | 0 / 0 | Phong / Masked |
| WEP_TurretRocket_p.WEP_TurretRocket_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ViciousAxe_p.WEP_ViciousAxe_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ViciousAxe_p.WEP_ViciousAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_WarHammer_p.WEP_WarHammer_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_WarHammer_p.WEP_WarHammer_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |

### MP_KON_Molten: 308 time-driven materials (K 308)

| Material (master) | Ours | Time sources by output | Draws / tris | Lighting / blend |
|---|---|---|---|---|
| DES_IAC_WallPanelSign_p.Materials.WallPanelSign_EMISSOFF_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| DES_IAC_WallPanelSign_p.Materials.WallPanelSign_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| ENV_AllShader_p.Release.ENV_ForceField_AUT_MATINST (ENV_ForceField_Fac_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_AllShader_p.Release.ENV_ForceField_DEC_MATINST (ENV_ForceField_Fac_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_CORE_Floors_p.Materials.ENV_CORE_EnergonPlasmaOrange_INST (Energon_River_Mat) | K | EmissiveColor: Panner(-0.02, -0.06), Panner(-0.02, 0.03), Panner(-0.09, 0.02), Panner(0.01, -0.075), Panner(0.1, 0.05); Opacity: Panner(-0.02, -0.06), Panner(0.1, 0.05) | 0 / 0 | Unlit / Translucent |
| ENV_GLB_EnvEffects_p.Material.LightVolumeCool_LessDense_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumeWARM_lessDense_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumeWarmThick2_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumeWarmThink_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_IAC_Shader_p.Material.IAC_Glass2_Dark_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_KON_Molten_p.Material.CoreGlass_MatINST (ENV_CustPhongPointLightUnlit_Reflect_Mat) | K | EmissiveColor: Panner(0, 0.5) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_KON_Molten_p.Material.GlassEnergyA_MATINST (ENV_Refractive_Glass_Trans_Mat) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Translucent |
| ENV_KON_Molten_p.Material.KaonSmokeMolten_MATINST (SmokeCoolDepth_Mat) | K | EmissiveColor: Panner(0.02, 0.05) time-in, Time; Opacity: Panner(0.02, 0.05) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_KON_Molten_p.Material.LavaFall1_MATINST (LavaFall_Parent_MAT) | K | EmissiveColor: Panner(-0.008, -0.5) time-in, Panner(0.01, -0.2) time-in, Time; Distortion: Panner(-0.008, -0.5) time-in, Panner(-0.01, -0.05) time-in, Panner(0.008, -0.01) time-in, Panner(0.01, -0.2) time-in, Time; Normal: Panner(-0.008, -0.5) time-in, Panner(-0.01, -0.05) time-in, Panner(0.008, -0.01) time-in, Panner(0.01, -0.2) time-in, Time | 0 / 0 | Unlit / Additive |
| ENV_KON_Molten_p.Material.LightRays_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_KON_Molten_p.Material.MoltenMetal2_MATINST (Energon_Lava_Mat) | K | EmissiveColor: Panner(-0.015, 0.01), Panner(-0.02, -0.06) time-in, Panner(-0.02, 0.03), Panner(-0.09, 0.02), Panner(0.01, -0.01), Panner(0.01, -0.075), Panner(0.1, 0.05) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_KON_Molten_p.Material.MoltenMntr_Orange_MATINST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| ENV_KON_Molten_p.Material.MoltenRainPuddle_MatInst (RainPuddles_Mat) | K | EmissiveColor: Panner(-0.05, -0.055) time-in, Panner(-0.05, 0.05) time-in, Panner(-0.595, -0.65) time-in, Panner(-0.995, 0.4) time-in, Time; Normal: Panner(-0.05, -0.055) time-in, Panner(-0.05, 0.05) time-in, Panner(-0.595, -0.65) time-in, Panner(-0.995, 0.4) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_KON_Molten_p.Material.MoltenRain_MatInst (Rain_Mat) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, -0.3) time-in, Time | 0 / 0 | Unlit / Additive |
| ENV_KON_Molten_p.Material.PlasmaAqua_INST (Energon_River_Mat) | K | EmissiveColor: Panner(-0.02, -0.06), Panner(-0.02, 0.03), Panner(-0.09, 0.02), Panner(0.01, -0.075), Panner(0.1, 0.05); Opacity: Panner(-0.02, -0.06), Panner(0.1, 0.05) | 0 / 0 | Unlit / Translucent |
| ENV_KON_StarDome_p.Test.KON_newSky_MAT (KON_newSky_MAT) | K | EmissiveColor: Panner(0.0001, 0.0001), Rotator(0.0006 rad/s @0.5,0.5), Rotator(0.001 rad/s @0.5,0.5) | 0 / 0 | Phong / Opaque |
| ENV_NEU_landmarking_p.landmark_Dchevrons_clr_Mat (landmark_Dchevrons_clr_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_Dring_clr_Mat (landmark_Dring_clr_Mat) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_Dtarget_clr_Mat (landmark_Dtarget_clr_Mat) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_ablogo_clr_Mat (landmark_ablogo_clr_Mat) | K | EmissiveColor: Panner(-0.05, -0.03), Panner(0.02, 0.1) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_chevrons_clr_Mat (landmark_chevrons_clr_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_declogo_clr_Mat (landmark_declogo_clr_Mat) | K | EmissiveColor: Panner(-0.05, -0.03), Panner(0.02, 0.1) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_ring_clr_Mat (landmark_ring_clr_Mat) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_target_clr_Mat (landmark_target_clr_Mat) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| ENV_ORB_D1_Architecture_p.Materials.WallPanelWarningSign_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| ENV_ORB_D1_Architecture_p.Materials.WallPanelWarningSign_NoEmiss_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| ENV_ORB_D1_Deco_p.Materials.MoltenMetal_MATINST (Energon_Lava_Mat) | K | EmissiveColor: Panner(-0.015, 0.01), Panner(-0.02, -0.06) time-in, Panner(-0.02, 0.03), Panner(-0.09, 0.02), Panner(0.01, -0.01), Panner(0.01, -0.075), Panner(0.1, 0.05) time-in, Time | 0 / 0 | Unlit / Translucent |
| FX_IonBlaster_p.IonBlaster_Mag_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| FX_Materials_p.MatInst.Blaster_Trail_MAT_INST (Blaster_MAT) | K | EmissiveColor: Panner(2.5, 0.5), Panner(3, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.CaptureZone_Reverse_MAT_INST (CaptureZoneLight_Base_MAT) | K | EmissiveColor: Panner(-0.15, 0.18), Panner(0, -0.05), Panner(0.01, -0.02), Time; Opacity: Panner(-0.15, 0.18), Panner(0, -0.05), Panner(0.01, -0.02), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.CircuitRadial_MATINST (CircuitRadial_MAT) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5), Sine(period 1); Opacity: Rotator(0.25 rad/s @0.5,0.5), Sine(period 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Distortion_Cloud_DBA_MAT_INST (Distortion_Cloud_01_MAT) | K | EmissiveColor: Panner(0, 0.3); Distortion: Panner(0, 0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.FusionBlasterBeam_MAT_INST (IonBlasterTrail_MAT) | K | EmissiveColor: Panner(2.5, 0.5), Panner(3, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.LightCylinder_Rays_MAT_INST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.LightVolume_Rays_MAT_INST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Lightning_Anim_03_UP_MAT_INST (Lightning_Anim_03_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.MuzzleFlash_X_Mat_INST (MuzzleFlash_X_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Smoke_Lrg_Mat_INST (SmokeThick_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.MatInst.Trail_Smoke_01_MAT_INST (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.MatInst.Trail_Smoke_10_MAT_INST (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.AmmoShell_MAT (AmmoShell_MAT) | K | EmissiveColor: Panner(0.04, 0.08), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.BlastSphere_Death_MAT (BlastSphere_Death_MAT) | K | EmissiveColor: Time; Distortion: Time | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.Bolt_ADD_MAT (Bolt_ADD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Distortion_Cloud_01_MAT (Distortion_Cloud_01_MAT) | K | EmissiveColor: Panner(0, 0.3); Distortion: Panner(0, 0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.EMPBlastSphere_MAT (EMPBlastSphere_MAT) | K | EmissiveColor: Panner(-0.5, 0.5), Panner(0.1, -1), Panner(0.25, 0.5); Distortion: Panner(-0.5, 0.5), Panner(0.1, -1), Panner(0.25, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.EMPBlastWave_MAT (EMPBlastWave_MAT) | K | EmissiveColor: Panner(-0.5, 0.5), Panner(0.25, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.ElectroRing01_Mat (ElectroRing01_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.ElectroRing02_Mat (ElectroRing02_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Embers_Blue_MAT_INST (Fire_MAT) | K | EmissiveColor: Panner(-0.15, 0.8), Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Explosion_MAT (Explosion_MAT) | K | EmissiveColor: Panner(1, 1), Rotator(0.5 rad/s @0.5,0.5), Time; Opacity: Panner(1, 1), Rotator(0.5 rad/s @0.5,0.5), Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Fire_MAT (Fire_MAT) | K | EmissiveColor: Panner(-0.15, 0.8), Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Fire_Ring01_Mat (Fire_Ring01_Mat) | K | EmissiveColor: Panner(0.4, 0.4) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.HealBeam_MAT (HealBeam_MAT) | K | EmissiveColor: Panner(-0.15, 0), Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.15, 0), Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LaserScanner_MAT (LaserScanner_MAT) | K | EmissiveColor: Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LightVolume_Base_MAT (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LightVolume_WepPickup_MAT (LightVolume_WepPickup_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_01_MAT (Lightning_Anim_01_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_02_MAT (Lightning_Anim_02_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_03_MAT (Lightning_Anim_03_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MFlash_Side_Desat_MAT (MFlash_Side_Desat_MAT) | K | EmissiveColor: Panner(1, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_Mat (MuzzleFlash_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_White_Mat (MuzzleFlash_White_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_X_Mat (MuzzleFlash_X_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ram_model_MAT (Ram_model_MAT) | K | EmissiveColor: Panner(-0.6, 0), Panner(0.6, 1.4), Panner(0.8, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ring_Distort_Add_MAT (Ring_Distort_Add_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ring_Distort_MAT (Ring_Distort_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Opacity: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Ring_Distort_Mesh_MAT (Ring_Distort_Mesh_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Rings_Distort_MAT (Rings_Distort_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Opacity: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.SmokeCoolDepth_Mat (SmokeCoolDepth_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.SmokeThick_Mat (SmokeThick_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Steam_Add_Mat (Steam_Add_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Steam_Mat (Steam_Mat) | K | EmissiveColor: Panner(0, 0.2); Opacity: Panner(0, 0.2) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Steam_Shade_Mat (Steam_Shade_Mat) | K | EmissiveColor: Panner(0, 0.2); Opacity: Panner(0, 0.2) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Tracer_ADD_MAT (Tracer_ADD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Tracer_MAT (Tracer_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Tracer_MOD_MAT (Tracer_MOD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.Tracer_Smoke_MAT (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.arcball01_MAT (arcball01_MAT) | K | EmissiveColor: Rotator(-2 rad/s @0.5,0.5), Rotator(1 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.bursting_MAT (bursting_MAT) | K | EmissiveColor: Panner(-1, 0); Opacity: Panner(-1, 0); Distortion: Panner(-1, 0); Normal: Panner(-1, 0) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Afterburn_02_MAT (Afterburn_02_MAT) | K | EmissiveColor: Panner(0.2, 2); Opacity: Panner(0.5, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Afterburn_Circuitry_02_MAT (Afterburn_Circuitry_02_MAT) | K | EmissiveColor: Panner(0.2, 2); Opacity: Panner(0, 0.5), Panner(0.1, 0.1), Panner(0.2, 2), Panner(0.5, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Boostermaterial_02_MAT (Boostermaterial_02_MAT) | K | EmissiveColor: Panner(1, 2); Opacity: Panner(1, 2) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.tank_hover_pattern_MAT (tank_hover_pattern_MAT) | K | EmissiveColor: Sine(period 1), Time; Opacity: Panner(0.3, 0.3), Rotator(1 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| FX_RollerMine_p.Material.FX_RollerMine_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| FX_Screen_p.Materials.Static_MAT (Static_MAT) | K | EmissiveColor: Panner(-0.805, -0.942), Panner(0.42, 0.513), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.MuzzleFlash_01_MAT (MuzzleFlash_01_MAT) | K | EmissiveColor: Panner(-0.15, 0.8); Opacity: Panner(-0.15, 0.8) | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.MuzzleFlash_Side_MAT (MuzzleFlash_Side_MAT) | K | EmissiveColor: Panner(1, 0); Opacity: Panner(1, 0) | 0 / 0 | Unlit / Additive |
| PROP_EnergonSigns_p.DecepticonGraffiti_MATISNT (LaserMarks_CLR_Mat) | K | EmissiveColor: Panner(0.01, -0.33), Panner(0.04, 0) | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.Barricade2.TPRO_NEU_Barricade2ForceField_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.BarricadeShield_MAT (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.RocketBarricade.TPRO_NEU_RocketBarrier_MATINST (Soundwave_ShieldBarrier_MAT) | K | EmissiveColor: Panner(-0.1, -0.5), Panner(0.1, -0.5), Panner(0.1, -0.75), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_BatteryOS_p.BatteryOmegaGlass_MATINST (ENV_Refractive_Glass_Trans_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Translucent |
| PROP_NEU_BatteryOS_p.OmegaLiquidSurface_MATINST (Coolant_Parent_MAT) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time; Normal: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_BatteryOS_p.OmegaLiquid_MATINST (TryptiGelGlass_Mat) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Translucent |
| PROP_NEU_EnergonCube_p.PROP_NEU_EnergonCube_Circuits_MATINST (PROP_NEU_EnergonCube_Circuits_MAT) | K | EmissiveColor: Panner(0, 1) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Interacts_p.PROP_ButtonInteract_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| PROP_NEU_Pickups_p.AmmoPickup.PROP_NEU_AmmoPickup_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.CodeOfPower.CodeOfPowerCORE_MatINST (CodeOfPower_MAT) | K | EmissiveColor: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(-0.15, 0.18), Panner(0.1, -0.075), Panner(0.2, 0.1); Opacity: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(0.2, 0.1); Distortion: Panner(-0.15, 0.18), Panner(0.1, -0.075) | 0 / 0 | Unlit / Translucent |
| PROP_NEU_Pickups_p.EnergonTotem.Conquest_Ring_MATINST (Conquest_Ring_MAT) | K | EmissiveColor: Rotator(-0.3 rad/s @0.5,0.5), Rotator(0.5 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| PROP_NEU_Pickups_p.EnergonTotem.PROP_NEU_EnergonTotem_MATINST (ENV_Hologram_Mat) | K | EmissiveColor: Panner(0, 0.1) time-in, Sine(period 1), Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.MPBomb.BombCore_MATINST_BAT (BombCore_MAT) | K | DiffuseColor: Cosine(period 0.5), Cosine(period 1), Time; EmissiveColor: Cosine(period 0.5), Cosine(period 1), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Pickups_p.MPBomb.PROP_NEU_MPBombExplode_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.MPBomb.PROP_NEU_MPBomb_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.OvershieldPickup.PROP_NEU_Overshield_MATINST (WEP_Crates_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Opaque |
| PROP_VendingMachine_p.Ammo.PROP_VendingMachine_Ammo_MATINST (VendingMachine_Screen_MAT) | K | EmissiveColor: Cosine(period 1) in Noise_MF, Panner(0, 1) time-in, Panner(1, 1) time-in in Noise_MF, Sine(period 1) in Noise_MF, Time, Time in Noise_MF | 0 / 0 | Unlit / Opaque |
| PROP_VendingMachine_p.PROP_VendingMachine_EnergonCube_MATINST (VendingMachine_Screen_MAT) | K | EmissiveColor: Cosine(period 1) in Noise_MF, Panner(0, 1) time-in, Panner(1, 1) time-in in Noise_MF, Sine(period 1) in Noise_MF, Time, Time in Noise_MF | 0 / 0 | Unlit / Opaque |
| TPRO_KON_CorruptorSpike_p.Materials.DarkEnergonCrystal_MAT_INST (DarkEnergonCrystal_MAT) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| TR_AirRaid_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_AirRaid_ROBO_p.RB_AirRaid_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_AirRaid_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_AirRaid_VEH_p.VH_AirRaid_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Arcee_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Arcee_ROBO_p.RB_Arcee_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Arcee_VEH_p.VH_Arcee_InteriorEnergon_Mat_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Arcee_VEH_p.VH_Arcee_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Barricade_ROBO_p.MaterialInstanceConstant_679 (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Barricade_ROBO_p.RB_Barricade_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Barricade_VEH_p.VH_Barricade_NormSpec_Cust_B_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Brawl_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Brawl_ROBO_p.RB_Brawl_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Brawl_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Brawl_VEH_p.VH_Brawl_NormSpec_Cust_B_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Breakdown_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Breakdown_ROBO_p.RB_Breakdown_Cust_Mat_Inst_E (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Breakdown_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Breakdown_VEH_p.RB_BreadownVEH_Cust_Mat_INST_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_ROBO_p.RB_BumbleBee2_Cust2_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_ROBO_p.RB_BumblebeeEnergon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_VEH_p.Materials.Bumblebee_TransformInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_VEH_p.VEH_BumbleBee2_Cust2_Mat (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Deadend_ROBO_p.RB_DeadendInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Deadend_ROBO_p.RB_Deadend_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Deadend_VEH_p.VH_DeadendInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Deadend_VEH_p.VH_Deadend_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Demolishor_ROBO_p.RB_Demolishor_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Demolishor_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Demolishor_VEH_p.VH_Demolishor_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ironhide_ROBO_p.RB_IronhideInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ironhide_ROBO_p.RB_Ironhide_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ironhide_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ironhide_VEH_p.VH_Ironhide_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jazz_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jazz_ROBO_p.RB_Jazz_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jazz_VEH_p.VH_Jazz_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jetfire_ROBO_p.RB_Jetfire_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jetfire_ROBO_p.TR_JetfireInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jetfire_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jetfire_VEH_p.VH_Jetfire_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Laserbeak_VEH_p.VH_Laserbeak_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Megatron_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Megatron_ROBO_p.VH_Megatron_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Megatron_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Megatron_VEH_p.VH_Megatron_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Onslaught_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Onslaught_ROBO_p.RB_Onslaught_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Onslaught_VEH_p.MaterialInstanceConstant_4774 (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Onslaught_VEH_p.VH_Onslaught_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Optimus_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Optimus_ROBO_p.RB_OptimusPrime_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Optimus_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Optimus_VEH_p.RB_OptimusPrime_Cust2_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ratchet_ROBO_p.RB_RatchetEnergonInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ratchet_ROBO_p.RB_Ratchet_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ratchet_VEH_p.VH_RatchetEnergonInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ratchet_VEH_p.VH_Ratchet_Cust2_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.FrenzyWeapon_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.Frenzy_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.RumbleWeapon_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.Rumble_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Scattershot_ROBO_p.RB_ScattershotInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Scattershot_ROBO_p.RB_Scattershot_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Scattershot_VEH_p.Debug.VH_ScattershotInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Scattershot_VEH_p.VH_Scattershot_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Shockwave_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Shockwave_ROBO_p.RB_Shockwave_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Shockwave_VEH_p.VH_Shockwave_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_ROBO_p.RB_Sideswipe_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_VEH_p.VH_Sideswipe_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_ROBO_p.RB_Silverbolt_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_VEH_p.VH_Silverbolt_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Skywarp_ROBO_p.RB_Skywarp_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Skywarp_ROBO_p.TR_Skywarp_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Skywarp_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Skywarp_VEH_p.VH_Skywarp_NormSpec_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Slipstream_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Slipstream_ROBO_p.RB_Slipstream_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Slipstream_VEH_p.VH_Slipstream_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_ROBO_p.RB_SoldierCarAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_ROBO_p.RB_SoldierMultiAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_VEH_p.VH_SoldierCarAut_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_ROBO_p.RB_SoldierCarDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_ROBO_p.RB_SoldierMultiDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_VEH_p.VH_SniperDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_ROBO_p.RB_SoldierCarNeu_Robo_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_ROBO_p.RB_SoldierMultiNeu_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_VEH_p.VH_SoldierCarNeu_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierTankAut_VEH_p.VH_SoldierTankAutA_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierTankDec_VEH_p.VH_SoldierTankDec_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Soundwave_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Soundwave_ROBO_p.RB_Soundwave_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Soundwave_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Soundwave_VEH_p.VH_Soundwave_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_ROBO_p.TR_Starscream_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_ROBO_p.TR_Starscream_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_StarScream_VEH_p.CHR_Transformer_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_VEH_p.VH_StarscreamInterior_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_ROBO_p.TR_Thunder_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Thunder_ROBO_p.TR_Thunder_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_VEH_p.VH_Thunder_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Trypticon_ROBO_p.RB_TrypticonHead_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Warpath_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Warpath_ROBO_p.RB_Warpath1_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Warpath_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Warpath_VEH_p.RB_Warpath1_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_ROBO_p.TR_ZetaPrime_ROBO_Cust_Mat_Inst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_VEH_p.VH_ZetaPrimeInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_VEH_p.VH_ZetaPrime_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| UI_GFxHud_p.LowHealth.LowHealthScreenEffect_M (LowHealthScreenEffect_M) | K | EmissiveColor: Panner(0, -2), Panner(0, 1) | 0 / 0 | Unlit / Opaque |
| UI_GFxHud_p.StaticDischargeScreenEffect_M (StaticDischargeScreenEffect_M) | K | EmissiveColor: Panner(-0.805, -0.942), Panner(0.42, 0.513) | 0 / 0 | Unlit / Opaque |
| UI_HudMarkers_p.MPMarkerBase_MAT (MPMarkerBase_MAT) | K | Opacity: Cosine(period 1), Panner(0, -2) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MPMarkerCOP_MAT (MPMarkerCOP_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MPMarkerDominationNode_MAT (MPMarkerDominationNode_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MarkerDownedAlly_MAT (MarkerDownedAlly_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MarkerGrenade_MAT (MarkerGrenade_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| WEP_AssaultRifle_p.WEP_AssaultRifle_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Axe_p.Autobot.WEP_Axe_Energon_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_BazookaTemp1_p.WEP_Bazooka_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BeatDownClub_p.WEP_BeatDownClub_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BroadSword_p.WEP_BroadSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_BroadSword_p.WEP_BroadSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BurstRifle_p.Materials.WEP_BurstRifle_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ButterflyAxe_p.WEP_ButterflyAxeEnergon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ButterflyAxe_p.WEP_ButterflyAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_CeremonialStaff_p.WEP_CeremonialStaff_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_CodeOfPower_p.WEP_CodeOfPower_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_DetPack_p.WEP_DetPack_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_EMPShotgun_p.WEP_EMPShotgun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_FightingStaff_p.WEP_FightingStaff_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_GrenadeLauncher_p.WEP_GrenadeLauncher_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Grenade_p.WEP_Grenade_Flak_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HalberdAxe_p.WEP_HalberdAxe_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_HalberdAxe_p.WEP_HalberdAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Hammer_p.WEP_Hammer_D_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Hammer_p.WEP_Hammer_Spikes_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_HeavyMG_p.WEP_HeavyMG_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HeavyPistol_p.WEP_HeavyPistol_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HuntingDagger_p.WEP_HuntingDagger_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_IonBlaster_p.WEP_IonBlaster_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_KamikazeMine_p.WEP_KamikazeMine_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_LancingSpear_p.WEP_LancingSpear_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_LongSword_p.WEP_LongSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_LongSword_p.WEP_LongSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Maul_p.WEP_Maul_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_Maul_p.WEP_Maul_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_PlasmaCannon_p.WEP_PlasmaCannon_A_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ProngDagger_p.WEP_Energon_A_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_ProngDagger_p.WEP_ProngDagger_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_RepairBeam_p.WEP_RepairBeam_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_RocketLauncher_p.WEP_RocketLauncher_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryAbility_p.WEP_DeployedTurret_MATINST (WEP_SentryAbility_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Sine(period 1), Time; OpacityMask: Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryBase.WEP_GlassGlow_MATINST (ENV_Refractive_Glass_Opaque_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| WEP_SentryBlaster01_p.SentryBase.WEP_SentryBase_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryBlaster.WEP_SentryBlaster_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryRepair.WEP_SentryRepair_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryRocket.WEP_SentryRocket_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SerratedBlade_p.WEP_SerratedBlade_Energon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SerratedBlade_p.WEP_SerratedBlade_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shared_p.WEP_Energon_D_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_Shared_p.WEP_PhongMain_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_Frame_MATINST (WEP_Barrier_A_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(0.01, -0.02) time-in in ElectricArcs_MF, Sine(period 1) in ElectricArcs_MF, Sine(period 1) in ScanLines_MF, Time in ElectricArcs_MF, Time in ScanLines_MF | 0 / 0 | Unlit / Translucent |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_MASK_MATINST (WEP_ShieldBruteA_MASK_MAT) | K | EmissiveColor: Panner(-0.75, 0.25), Panner(0.75, -0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Barrier.ENV_ForceField_Defrag_MAT (ENV_ForceField_Defrag_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(1, -0.5), Panner(1, 0) time-in, Rotator(0.25 rad/s @0.5,0.5), Sine(period 1), Sine(period 1) in ScanLines_MF, Time, Time in ScanLines_MF; Opacity: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Barrier.WEP_Barrier_Defrag_MATINST (ENV_ForceField_Defrag_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(1, -0.5), Panner(1, 0) time-in, Rotator(0.25 rad/s @0.5,0.5), Sine(period 1), Sine(period 1) in ScanLines_MF, Time, Time in ScanLines_MF; Opacity: Rotator(0.25 rad/s @0.5,0.5); Distortion: Panner(-0.04, -0.12), Panner(0.2, 0.1) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_Frame_MATINST (WEP_Barrier_A_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(0.01, -0.02) time-in in ElectricArcs_MF, Sine(period 1) in ElectricArcs_MF, Sine(period 1) in ScanLines_MF, Time in ElectricArcs_MF, Time in ScanLines_MF | 0 / 0 | Unlit / Translucent |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_MASK_MATINST (WEP_ShieldBruteA_MASK_MAT) | K | EmissiveColor: Panner(-0.75, 0.25), Panner(0.75, -0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Decepticon.WEP_ShieldD_Energon_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_ShortSword_p.WEP_ShortSword_Energon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ShortSword_p.WEP_ShortSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shotgun_p.WEP_Shotgun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SniperRifle_p.WEP_SniperRifle_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SpikedBat_p.WEP_SpikedBat_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SpikedBat_p.WEP_SpikedBat_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SpikedMace_p.WEP_SpikedMace_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SpikedMace_p.WEP_SpikedMace_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TortureSword_p.WEP_TortureSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_TortureSword_p.WEP_TortureSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TrypticonMouthCannon_p.WEP_TrypMouthCannon_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TrypticonShoulderCannon_p.WEP_TrypShoulderCannon_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun01_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun_Overshield_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(-0.05, -0.1) time-in in Overshield_MFUNC, Panner(-0.1, -0.5) time-in in Overshield_MFUNC, Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Panner(0.2, 0.1) time-in in Overshield_MFUNC, Panner(0.5, 0.1) time-in in Overshield_MFUNC, Time, Time in Overshield_MFUNC | 0 / 0 | Phong / Masked |
| WEP_TurretRocket_p.WEP_TurretRocket_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ViciousAxe_p.WEP_ViciousAxe_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ViciousAxe_p.WEP_ViciousAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_WarHammer_p.WEP_WarHammer_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_WarHammer_p.WEP_WarHammer_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |

### MP_ORB_Debris: 300 time-driven materials (K 300)

| Material (master) | Ours | Time sources by output | Draws / tris | Lighting / blend |
|---|---|---|---|---|
| DES_IAC_WallPanelSign_p.Materials.WallPanelSign_EMISSOFF_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| DES_IAC_WallPanelSign_p.Materials.WallPanelSign_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| ENV_AllShader_p.Release.ENV_ForceField_AUT_MATINST (ENV_ForceField_Fac_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_AllShader_p.Release.ENV_ForceField_DEC_MATINST (ENV_ForceField_Fac_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_AllShader_p.Release.ENV_ForceField_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2Cool_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2Teal_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.MovingLightRays_Purp_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.MovingLightRays_Red_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_IAC_Shader_p.Material.IAC_Glass_Opaque_MATINST (ENV_Refractive_Glass_Opaque_Mat) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| ENV_IAC_Shader_p.Material.IAC_Glass_Trans_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_Dtarget_clr_Mat (landmark_Dtarget_clr_Mat) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_ablogo_clr_Mat (landmark_ablogo_clr_Mat) | K | EmissiveColor: Panner(-0.05, -0.03), Panner(0.02, 0.1) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_declogo_clr_Mat (landmark_declogo_clr_Mat) | K | EmissiveColor: Panner(-0.05, -0.03), Panner(0.02, 0.1) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_target_clr_Mat (landmark_target_clr_Mat) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| ENV_ORB_DebrisBase_p.Materials.ENV_ORB_SliceFloorBGlass_MATINST (ENV_CustPhongUnlit_Reflect_Mat) | K | EmissiveColor: Panner(0, 0.5) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_ORB_DecoTrim_p.Structural_Trim.PistonChamber_MATINST_BAT (PistonChamber_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| ENV_ORB_PowerCorridor_p.Materials.PowerTubeEmissPulse_MATINST (PowerTube_EmissPulse_MAT) | K | EmissiveColor: Panner(0.4, 0) | 0 / 0 | Phong / Opaque |
| ENV_ORB_Shader_p.ForceField.ENV_ORB_ForceField_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_ORB_Spacedome_p.Spacedome_Nebula_MAT (Spacedome_Nebula_MAT) | K | EmissiveColor: Panner(0.0001, 0.0001), Rotator(0.0006 rad/s @0.5,0.5), Rotator(0.001 rad/s @0.5,0.5) | 0 / 0 | Phong / Opaque |
| FX_IonBlaster_p.IonBlaster_Mag_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| FX_Materials_p.MatInst.Blaster_Trail_MAT_INST (Blaster_MAT) | K | EmissiveColor: Panner(2.5, 0.5), Panner(3, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.CaptureZone_Reverse_MAT_INST (CaptureZoneLight_Base_MAT) | K | EmissiveColor: Panner(-0.15, 0.18), Panner(0, -0.05), Panner(0.01, -0.02), Time; Opacity: Panner(-0.15, 0.18), Panner(0, -0.05), Panner(0.01, -0.02), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.CircuitRadial_MATINST (CircuitRadial_MAT) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5), Sine(period 1); Opacity: Rotator(0.25 rad/s @0.5,0.5), Sine(period 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Distortion_Cloud_DBA_MAT_INST (Distortion_Cloud_01_MAT) | K | EmissiveColor: Panner(0, 0.3); Distortion: Panner(0, 0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.FusionBlasterBeam_MAT_INST (IonBlasterTrail_MAT) | K | EmissiveColor: Panner(2.5, 0.5), Panner(3, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.LightCylinder_Rays_MAT_INST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.LightVolume_Rays_MAT_INST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Lightning_Anim_03_UP_MAT_INST (Lightning_Anim_03_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.MuzzleFlash_X_Mat_INST (MuzzleFlash_X_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Smoke_Lrg_Mat_INST (SmokeThick_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.MatInst.Trail_Smoke_01_MAT_INST (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.MatInst.Trail_Smoke_10_MAT_INST (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.AmmoShell_MAT (AmmoShell_MAT) | K | EmissiveColor: Panner(0.04, 0.08), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.BlastShell_MAT (BlastShell_MAT) | K | EmissiveColor: Panner(0.5, 1); Opacity: Panner(0.5, 1); Distortion: Panner(0.5, 1) | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.BlastSphere_Death_MAT (BlastSphere_Death_MAT) | K | EmissiveColor: Time; Distortion: Time | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.Bolt_ADD_MAT (Bolt_ADD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Distortion_Cloud_01_MAT (Distortion_Cloud_01_MAT) | K | EmissiveColor: Panner(0, 0.3); Distortion: Panner(0, 0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.EMPBlastSphere_MAT (EMPBlastSphere_MAT) | K | EmissiveColor: Panner(-0.5, 0.5), Panner(0.1, -1), Panner(0.25, 0.5); Distortion: Panner(-0.5, 0.5), Panner(0.1, -1), Panner(0.25, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.EMPBlastWave_MAT (EMPBlastWave_MAT) | K | EmissiveColor: Panner(-0.5, 0.5), Panner(0.25, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.ElectroRing01_Mat (ElectroRing01_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.ElectroRing02_Mat (ElectroRing02_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Embers_Blue_MAT_INST (Fire_MAT) | K | EmissiveColor: Panner(-0.15, 0.8), Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Explosion_MAT (Explosion_MAT) | K | EmissiveColor: Panner(1, 1), Rotator(0.5 rad/s @0.5,0.5), Time; Opacity: Panner(1, 1), Rotator(0.5 rad/s @0.5,0.5), Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Fire_MAT (Fire_MAT) | K | EmissiveColor: Panner(-0.15, 0.8), Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Fire_Ring01_Mat (Fire_Ring01_Mat) | K | EmissiveColor: Panner(0.4, 0.4) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.HealBeam_MAT (HealBeam_MAT) | K | EmissiveColor: Panner(-0.15, 0), Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.15, 0), Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LaserScanner_MAT (LaserScanner_MAT) | K | EmissiveColor: Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LightVolume_Base_MAT (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LightVolume_WepPickup_MAT (LightVolume_WepPickup_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_01_MAT (Lightning_Anim_01_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_02_MAT (Lightning_Anim_02_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_03_MAT (Lightning_Anim_03_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MFlash_Side_Desat_MAT (MFlash_Side_Desat_MAT) | K | EmissiveColor: Panner(1, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_Mat (MuzzleFlash_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_White_Mat (MuzzleFlash_White_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_X_Mat (MuzzleFlash_X_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ram_model_MAT (Ram_model_MAT) | K | EmissiveColor: Panner(-0.6, 0), Panner(0.6, 1.4), Panner(0.8, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ring_Distort_Add_MAT (Ring_Distort_Add_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ring_Distort_MAT (Ring_Distort_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Opacity: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Ring_Distort_Mesh_MAT (Ring_Distort_Mesh_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Rings_Distort_MAT (Rings_Distort_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Opacity: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.SmokeCoolDepth_Mat (SmokeCoolDepth_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.SmokeThick_Mat (SmokeThick_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Steam_Add_Mat (Steam_Add_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Steam_Mat (Steam_Mat) | K | EmissiveColor: Panner(0, 0.2); Opacity: Panner(0, 0.2) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Steam_Shade_Mat (Steam_Shade_Mat) | K | EmissiveColor: Panner(0, 0.2); Opacity: Panner(0, 0.2) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Tracer_ADD_MAT (Tracer_ADD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Tracer_MAT (Tracer_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Tracer_MOD_MAT (Tracer_MOD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.Tracer_Smoke_MAT (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.arcball01_MAT (arcball01_MAT) | K | EmissiveColor: Rotator(-2 rad/s @0.5,0.5), Rotator(1 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Afterburn_02_MAT (Afterburn_02_MAT) | K | EmissiveColor: Panner(0.2, 2); Opacity: Panner(0.5, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Afterburn_Circuitry_02_MAT (Afterburn_Circuitry_02_MAT) | K | EmissiveColor: Panner(0.2, 2); Opacity: Panner(0, 0.5), Panner(0.1, 0.1), Panner(0.2, 2), Panner(0.5, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Boostermaterial_02_MAT (Boostermaterial_02_MAT) | K | EmissiveColor: Panner(1, 2); Opacity: Panner(1, 2) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.tank_hover_pattern_MAT (tank_hover_pattern_MAT) | K | EmissiveColor: Sine(period 1), Time; Opacity: Panner(0.3, 0.3), Rotator(1 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| FX_RollerMine_p.Material.FX_RollerMine_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| FX_Screen_p.Materials.Static_MAT (Static_MAT) | K | EmissiveColor: Panner(-0.805, -0.942), Panner(0.42, 0.513), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.MuzzleFlash_01_MAT (MuzzleFlash_01_MAT) | K | EmissiveColor: Panner(-0.15, 0.8); Opacity: Panner(-0.15, 0.8) | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.MuzzleFlash_Side_MAT (MuzzleFlash_Side_MAT) | K | EmissiveColor: Panner(1, 0); Opacity: Panner(1, 0) | 0 / 0 | Unlit / Additive |
| PROP_EnergonSigns_p.EnergonSigns_Decepticon_CLR_Mat (EnergonSigns_Decepticon_CLR_Mat) | K | EmissiveColor: Panner(0, -0.19), Panner(0.01, 0) | 0 / 0 | Unlit / Additive |
| PROP_EnergonSigns_p.communications.Megatron_com_Mat (Megatron_com_Mat) | K | EmissiveColor: Cosine(period 5), FlipBook(DecepticonLogoFlip 2x3 @8 fps), FlipBook(MegatronComStatic_FLIP_CLR 3x5 @10 fps), Panner(-3, 0) time-in, Panner(0, -0.2) time-in, Panner(0.01, -0.1), Panner(0.05, 0.1), Panner(0.2, 0.1), Sine(period 10), Sine(period 5), Time | 0 / 0 | Unlit / Opaque |
| PROP_NEU_Barricade_p.Barricade2.TPRO_NEU_Barricade2ForceField_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.BarricadeShield_MAT (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.RocketBarricade.TPRO_NEU_RocketBarrier_MATINST (Soundwave_ShieldBarrier_MAT) | K | EmissiveColor: Panner(-0.1, -0.5), Panner(0.1, -0.5), Panner(0.1, -0.75), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_BatteryOS_p.BatteryOmegaGlass_MATINST (ENV_Refractive_Glass_Trans_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Translucent |
| PROP_NEU_BatteryOS_p.OmegaLiquidSurface_MATINST (Coolant_Parent_MAT) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time; Normal: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_BatteryOS_p.OmegaLiquid_MATINST (TryptiGelGlass_Mat) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Translucent |
| PROP_NEU_EnergonCube_p.PROP_NEU_EnergonCube_Circuits_MATINST (PROP_NEU_EnergonCube_Circuits_MAT) | K | EmissiveColor: Panner(0, 1) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Interacts_p.PROP_ButtonInteract_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreenActivePurple_MATINST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreenDead2_MAT_INST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Pickups_p.AmmoPickup.PROP_NEU_AmmoPickup_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.CodeOfPower.CodeOfPowerCORE_MatINST (CodeOfPower_MAT) | K | EmissiveColor: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(-0.15, 0.18), Panner(0.1, -0.075), Panner(0.2, 0.1); Opacity: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(0.2, 0.1); Distortion: Panner(-0.15, 0.18), Panner(0.1, -0.075) | 0 / 0 | Unlit / Translucent |
| PROP_NEU_Pickups_p.EnergonTotem.Conquest_Ring_MATINST (Conquest_Ring_MAT) | K | EmissiveColor: Rotator(-0.3 rad/s @0.5,0.5), Rotator(0.5 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| PROP_NEU_Pickups_p.EnergonTotem.PROP_NEU_EnergonTotem_MATINST (ENV_Hologram_Mat) | K | EmissiveColor: Panner(0, 0.1) time-in, Sine(period 1), Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.MPBomb.BombCore_MATINST_BAT (BombCore_MAT) | K | DiffuseColor: Cosine(period 0.5), Cosine(period 1), Time; EmissiveColor: Cosine(period 0.5), Cosine(period 1), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Pickups_p.MPBomb.PROP_NEU_MPBombExplode_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.MPBomb.PROP_NEU_MPBomb_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.OvershieldPickup.PROP_NEU_Overshield_MATINST (WEP_Crates_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_WreckedBodies_p.RB_SoldierCarAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| PROP_VendingMachine_p.Ammo.PROP_VendingMachine_Ammo_MATINST (VendingMachine_Screen_MAT) | K | EmissiveColor: Cosine(period 1) in Noise_MF, Panner(0, 1) time-in, Panner(1, 1) time-in in Noise_MF, Sine(period 1) in Noise_MF, Time, Time in Noise_MF | 0 / 0 | Unlit / Opaque |
| PROP_VendingMachine_p.PROP_VendingMachine_EnergonCube_MATINST (VendingMachine_Screen_MAT) | K | EmissiveColor: Cosine(period 1) in Noise_MF, Panner(0, 1) time-in, Panner(1, 1) time-in in Noise_MF, Sine(period 1) in Noise_MF, Time, Time in Noise_MF | 0 / 0 | Unlit / Opaque |
| TPRO_KON_CorruptorSpike_p.Materials.DarkEnergonCrystal_MAT_INST (DarkEnergonCrystal_MAT) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| TR_AirRaid_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_AirRaid_ROBO_p.RB_AirRaid_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_AirRaid_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_AirRaid_VEH_p.VH_AirRaid_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Arcee_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Arcee_ROBO_p.RB_Arcee_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Arcee_VEH_p.VH_Arcee_InteriorEnergon_Mat_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Arcee_VEH_p.VH_Arcee_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Barricade_ROBO_p.MaterialInstanceConstant_679 (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Barricade_ROBO_p.RB_Barricade_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Barricade_VEH_p.VH_Barricade_NormSpec_Cust_B_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Brawl_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Brawl_ROBO_p.RB_Brawl_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Brawl_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Brawl_VEH_p.VH_Brawl_NormSpec_Cust_B_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Breakdown_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Breakdown_ROBO_p.RB_Breakdown_Cust_Mat_Inst_E (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Breakdown_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Breakdown_VEH_p.RB_BreadownVEH_Cust_Mat_INST_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_ROBO_p.RB_BumbleBee2_Cust2_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_ROBO_p.RB_BumblebeeEnergon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_VEH_p.Materials.Bumblebee_TransformInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_VEH_p.VEH_BumbleBee2_Cust2_Mat (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Deadend_ROBO_p.RB_DeadendInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Deadend_ROBO_p.RB_Deadend_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Deadend_VEH_p.VH_DeadendInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Deadend_VEH_p.VH_Deadend_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Demolishor_ROBO_p.RB_Demolishor_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Demolishor_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Demolishor_VEH_p.VH_Demolishor_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ironhide_ROBO_p.RB_IronhideInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ironhide_ROBO_p.RB_Ironhide_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ironhide_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ironhide_VEH_p.VH_Ironhide_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jazz_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jazz_ROBO_p.RB_Jazz_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jazz_VEH_p.VH_Jazz_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jetfire_ROBO_p.RB_Jetfire_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jetfire_ROBO_p.TR_JetfireInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jetfire_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jetfire_VEH_p.VH_Jetfire_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Laserbeak_VEH_p.VH_Laserbeak_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Megatron_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Megatron_ROBO_p.VH_Megatron_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Megatron_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Megatron_VEH_p.VH_Megatron_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Onslaught_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Onslaught_ROBO_p.RB_Onslaught_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Onslaught_VEH_p.MaterialInstanceConstant_4774 (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Onslaught_VEH_p.VH_Onslaught_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Optimus_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Optimus_ROBO_p.RB_OptimusPrime_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Optimus_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Optimus_VEH_p.RB_OptimusPrime_Cust2_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ratchet_ROBO_p.RB_RatchetEnergonInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ratchet_ROBO_p.RB_Ratchet_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ratchet_VEH_p.VH_RatchetEnergonInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ratchet_VEH_p.VH_Ratchet_Cust2_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.FrenzyWeapon_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.Frenzy_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.RumbleWeapon_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.Rumble_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Scattershot_ROBO_p.RB_ScattershotInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Scattershot_ROBO_p.RB_Scattershot_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Scattershot_VEH_p.Debug.VH_ScattershotInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Scattershot_VEH_p.VH_Scattershot_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Shockwave_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Shockwave_ROBO_p.RB_Shockwave_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Shockwave_VEH_p.VH_Shockwave_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_ROBO_p.RB_Sideswipe_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_VEH_p.VH_Sideswipe_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_ROBO_p.RB_Silverbolt_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_VEH_p.VH_Silverbolt_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Skywarp_ROBO_p.RB_Skywarp_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Skywarp_ROBO_p.TR_Skywarp_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Skywarp_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Skywarp_VEH_p.VH_Skywarp_NormSpec_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Slipstream_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Slipstream_ROBO_p.RB_Slipstream_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Slipstream_VEH_p.VH_Slipstream_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_ROBO_p.RB_SoldierCarAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_ROBO_p.RB_SoldierMultiAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_VEH_p.VH_SoldierCarAut_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_ROBO_p.RB_SoldierCarDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_ROBO_p.RB_SoldierMultiDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_VEH_p.VH_SniperDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_ROBO_p.RB_SoldierCarNeu_Robo_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_ROBO_p.RB_SoldierMultiNeu_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_VEH_p.VH_SoldierCarNeu_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierTankAut_VEH_p.VH_SoldierTankAutA_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierTankDec_VEH_p.VH_SoldierTankDec_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Soundwave_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Soundwave_ROBO_p.RB_Soundwave_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Soundwave_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Soundwave_VEH_p.VH_Soundwave_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_ROBO_p.TR_Starscream_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_ROBO_p.TR_Starscream_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_StarScream_VEH_p.CHR_Transformer_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_VEH_p.VH_StarscreamInterior_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_ROBO_p.TR_Thunder_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Thunder_ROBO_p.TR_Thunder_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_VEH_p.VH_Thunder_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Trypticon_ROBO_p.RB_TrypticonHead_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Warpath_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Warpath_ROBO_p.RB_Warpath1_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Warpath_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Warpath_VEH_p.RB_Warpath1_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_ROBO_p.TR_ZetaPrime_ROBO_Cust_Mat_Inst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_VEH_p.VH_ZetaPrimeInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_VEH_p.VH_ZetaPrime_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| UI_GFxHud_p.LowHealth.LowHealthScreenEffect_M (LowHealthScreenEffect_M) | K | EmissiveColor: Panner(0, -2), Panner(0, 1) | 0 / 0 | Unlit / Opaque |
| UI_GFxHud_p.StaticDischargeScreenEffect_M (StaticDischargeScreenEffect_M) | K | EmissiveColor: Panner(-0.805, -0.942), Panner(0.42, 0.513) | 0 / 0 | Unlit / Opaque |
| UI_HudMarkers_p.MPMarkerBase_MAT (MPMarkerBase_MAT) | K | Opacity: Cosine(period 1), Panner(0, -2) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MPMarkerCOP_MAT (MPMarkerCOP_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MPMarkerDominationNode_MAT (MPMarkerDominationNode_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MarkerDownedAlly_MAT (MarkerDownedAlly_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MarkerGrenade_MAT (MarkerGrenade_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| WEP_AssaultRifle_p.WEP_AssaultRifle_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Axe_p.Autobot.WEP_Axe_Energon_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_BazookaTemp1_p.WEP_Bazooka_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BeatDownClub_p.WEP_BeatDownClub_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BroadSword_p.WEP_BroadSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_BroadSword_p.WEP_BroadSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BurstRifle_p.Materials.WEP_BurstRifle_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ButterflyAxe_p.WEP_ButterflyAxeEnergon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ButterflyAxe_p.WEP_ButterflyAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_CeremonialStaff_p.WEP_CeremonialStaff_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_CodeOfPower_p.WEP_CodeOfPower_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_DetPack_p.WEP_DetPack_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_EMPShotgun_p.WEP_EMPShotgun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_FightingStaff_p.WEP_FightingStaff_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_GrenadeLauncher_p.WEP_GrenadeLauncher_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Grenade_p.WEP_Grenade_Flak_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HalberdAxe_p.WEP_HalberdAxe_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_HalberdAxe_p.WEP_HalberdAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Hammer_p.WEP_Hammer_D_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Hammer_p.WEP_Hammer_Spikes_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_HeavyMG_p.WEP_HeavyMG_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HeavyPistol_p.WEP_HeavyPistol_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HuntingDagger_p.WEP_HuntingDagger_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_IonBlaster_p.WEP_IonBlaster_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_KamikazeMine_p.WEP_KamikazeMine_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_LancingSpear_p.WEP_LancingSpear_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_LongSword_p.WEP_LongSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_LongSword_p.WEP_LongSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Maul_p.WEP_Maul_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_Maul_p.WEP_Maul_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_PlasmaCannon_p.WEP_PlasmaCannon_A_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ProngDagger_p.WEP_Energon_A_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_ProngDagger_p.WEP_ProngDagger_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_RepairBeam_p.WEP_RepairBeam_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_RocketLauncher_p.WEP_RocketLauncher_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryAbility_p.WEP_DeployedTurret_MATINST (WEP_SentryAbility_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Sine(period 1), Time; OpacityMask: Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryBase.WEP_GlassGlow_MATINST (ENV_Refractive_Glass_Opaque_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| WEP_SentryBlaster01_p.SentryBase.WEP_SentryBase_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryBlaster.WEP_SentryBlaster_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryRepair.WEP_SentryRepair_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryRocket.WEP_SentryRocket_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SerratedBlade_p.WEP_SerratedBlade_Energon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SerratedBlade_p.WEP_SerratedBlade_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shared_p.WEP_Energon_D_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_Shared_p.WEP_PhongMain_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_Frame_MATINST (WEP_Barrier_A_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(0.01, -0.02) time-in in ElectricArcs_MF, Sine(period 1) in ElectricArcs_MF, Sine(period 1) in ScanLines_MF, Time in ElectricArcs_MF, Time in ScanLines_MF | 0 / 0 | Unlit / Translucent |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_MASK_MATINST (WEP_ShieldBruteA_MASK_MAT) | K | EmissiveColor: Panner(-0.75, 0.25), Panner(0.75, -0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Barrier.ENV_ForceField_Defrag_MAT (ENV_ForceField_Defrag_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(1, -0.5), Panner(1, 0) time-in, Rotator(0.25 rad/s @0.5,0.5), Sine(period 1), Sine(period 1) in ScanLines_MF, Time, Time in ScanLines_MF; Opacity: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Barrier.WEP_Barrier_Defrag_MATINST (ENV_ForceField_Defrag_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(1, -0.5), Panner(1, 0) time-in, Rotator(0.25 rad/s @0.5,0.5), Sine(period 1), Sine(period 1) in ScanLines_MF, Time, Time in ScanLines_MF; Opacity: Rotator(0.25 rad/s @0.5,0.5); Distortion: Panner(-0.04, -0.12), Panner(0.2, 0.1) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_Frame_MATINST (WEP_Barrier_A_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(0.01, -0.02) time-in in ElectricArcs_MF, Sine(period 1) in ElectricArcs_MF, Sine(period 1) in ScanLines_MF, Time in ElectricArcs_MF, Time in ScanLines_MF | 0 / 0 | Unlit / Translucent |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_MASK_MATINST (WEP_ShieldBruteA_MASK_MAT) | K | EmissiveColor: Panner(-0.75, 0.25), Panner(0.75, -0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Decepticon.WEP_ShieldD_Energon_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_ShortSword_p.WEP_ShortSword_Energon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ShortSword_p.WEP_ShortSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shotgun_p.WEP_Shotgun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SniperRifle_p.WEP_SniperRifle_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SpikedBat_p.WEP_SpikedBat_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SpikedBat_p.WEP_SpikedBat_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SpikedMace_p.WEP_SpikedMace_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SpikedMace_p.WEP_SpikedMace_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TortureSword_p.WEP_TortureSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_TortureSword_p.WEP_TortureSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TrypticonMouthCannon_p.WEP_TrypMouthCannon_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TrypticonShoulderCannon_p.WEP_TrypShoulderCannon_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun01_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun_Overshield_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(-0.05, -0.1) time-in in Overshield_MFUNC, Panner(-0.1, -0.5) time-in in Overshield_MFUNC, Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Panner(0.2, 0.1) time-in in Overshield_MFUNC, Panner(0.5, 0.1) time-in in Overshield_MFUNC, Time, Time in Overshield_MFUNC | 0 / 0 | Phong / Masked |
| WEP_TurretRocket_p.WEP_TurretRocket_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ViciousAxe_p.WEP_ViciousAxe_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ViciousAxe_p.WEP_ViciousAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_WarHammer_p.WEP_WarHammer_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_WarHammer_p.WEP_WarHammer_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |

### MP_UND_Complex: 303 time-driven materials (K 303)

| Material (master) | Ours | Time sources by output | Draws / tris | Lighting / blend |
|---|---|---|---|---|
| DES_IAC_WallPanelSign_p.Materials.WallPanelSign_EMISSOFF_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| DES_IAC_WallPanelSign_p.Materials.WallPanelSign_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| ENV_CORE_Complex_p.Material.ComplexWaterfall_MATINST (Waterfall_Parent_MAT) | K | EmissiveColor: Panner(-0.008, -0.5) time-in, Panner(0.01, -0.2) time-in, Time; Distortion: Panner(-0.008, -0.5) time-in, Panner(-0.01, -0.05) time-in, Panner(0.008, -0.01) time-in, Panner(0.01, -0.2) time-in, Time; Normal: Panner(-0.008, -0.5) time-in, Panner(-0.01, -0.05) time-in, Panner(0.008, -0.01) time-in, Panner(0.01, -0.2) time-in, Time | 0 / 0 | Unlit / Additive |
| ENV_CORE_Complex_p.Material.EnergonPlasmaAquaLight_INST (Energon_River_Mat) | K | EmissiveColor: Panner(-0.02, -0.06), Panner(-0.02, 0.03), Panner(-0.09, 0.02), Panner(0.01, -0.075), Panner(0.1, 0.05); Opacity: Panner(-0.02, -0.06), Panner(0.1, 0.05) | 0 / 0 | Unlit / Translucent |
| ENV_CORE_Complex_p.Material.Energy_Blue_Mat_INST (WEP_ForceField_B_Mat) | K | EmissiveColor: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(-0.15, 0.18), Panner(0.1, -0.075), Panner(0.2, 0.1); Distortion: Panner(-0.04, -0.12), Panner(0.2, 0.1) | 0 / 0 | Unlit / Translucent |
| ENV_CORE_Complex_p.Material.LightCylinder_Rays_Blue_less_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_CORE_Complex_p.Material.LightCylinder_Rays_less_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_CORE_Complex_p.Material.MonitorScreenActiveAqua_MATINST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| ENV_CORE_Deco_p.Materials.AngledSupportWarm_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2Cool_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumeCool_LessDense_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumeWARM_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumeWARM_lessDense_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumeWarmThick2_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_IAC_Interior_1_p.Materials.WallPanel_MAT_INST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| ENV_IAC_Shader_p.Material.IAC_Glass2_light_thin_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_KON_Molten_p.Material.MoltenMntr_Orange_MATINST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| ENV_NEU_landmarking_p.landmark_Dchevrons_clr_Mat (landmark_Dchevrons_clr_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_Dtarget_clr_Mat (landmark_Dtarget_clr_Mat) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_ablogo_clr_Mat (landmark_ablogo_clr_Mat) | K | EmissiveColor: Panner(-0.05, -0.03), Panner(0.02, 0.1) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_chevrons_clr_Mat (landmark_chevrons_clr_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_declogo_clr_Mat (landmark_declogo_clr_Mat) | K | EmissiveColor: Panner(-0.05, -0.03), Panner(0.02, 0.1) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_target_clr_Mat (landmark_target_clr_Mat) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| ENV_ORB_CoolantRoom_p.Material.AngledSupportBlue_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| ENV_ORB_CoolantRoom_p.Material.Waterfall2_MATINST (Waterfall_Parent_MAT) | K | EmissiveColor: Panner(-0.008, -0.5) time-in, Panner(0.01, -0.2) time-in, Time; Distortion: Panner(-0.008, -0.5) time-in, Panner(-0.01, -0.05) time-in, Panner(0.008, -0.01) time-in, Panner(0.01, -0.2) time-in, Time; Normal: Panner(-0.008, -0.5) time-in, Panner(-0.01, -0.05) time-in, Panner(0.008, -0.01) time-in, Panner(0.01, -0.2) time-in, Time | 0 / 0 | Unlit / Additive |
| ENV_ORB_D1_Architecture_p.Materials.WallPanelWarningSign_NoEmiss_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| ENV_ORB_Spacedome_p.Spacedome_ORBITAL_MAT (Spacedome_ORBITAL_MAT) | K | EmissiveColor: Panner(0.0001, 0.0001), Rotator(0.0006 rad/s @0.5,0.5), Rotator(0.001 rad/s @0.5,0.5) | 0 / 0 | Phong / Opaque |
| FX_IonBlaster_p.IonBlaster_Mag_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| FX_Materials_p.MatInst.Blaster_Trail_MAT_INST (Blaster_MAT) | K | EmissiveColor: Panner(2.5, 0.5), Panner(3, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.CaptureZone_Reverse_MAT_INST (CaptureZoneLight_Base_MAT) | K | EmissiveColor: Panner(-0.15, 0.18), Panner(0, -0.05), Panner(0.01, -0.02), Time; Opacity: Panner(-0.15, 0.18), Panner(0, -0.05), Panner(0.01, -0.02), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.CircuitRadial_MATINST (CircuitRadial_MAT) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5), Sine(period 1); Opacity: Rotator(0.25 rad/s @0.5,0.5), Sine(period 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Distortion_Cloud_DBA_MAT_INST (Distortion_Cloud_01_MAT) | K | EmissiveColor: Panner(0, 0.3); Distortion: Panner(0, 0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.FusionBlasterBeam_MAT_INST (IonBlasterTrail_MAT) | K | EmissiveColor: Panner(2.5, 0.5), Panner(3, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.LightCylinder_Rays_MAT_INST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.LightVolume_Rays_MAT_INST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Lightning_Anim_03_UP_MAT_INST (Lightning_Anim_03_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.MuzzleFlash_X_Mat_INST (MuzzleFlash_X_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Smoke_Lrg_Mat_INST (SmokeThick_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.MatInst.Trail_Smoke_01_MAT_INST (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.MatInst.Trail_Smoke_10_MAT_INST (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.AmmoShell_MAT (AmmoShell_MAT) | K | EmissiveColor: Panner(0.04, 0.08), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.BlastSphere_Death_MAT (BlastSphere_Death_MAT) | K | EmissiveColor: Time; Distortion: Time | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.Bolt_ADD_MAT (Bolt_ADD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Distortion_Cloud_01_MAT (Distortion_Cloud_01_MAT) | K | EmissiveColor: Panner(0, 0.3); Distortion: Panner(0, 0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.EMPBlastSphere_MAT (EMPBlastSphere_MAT) | K | EmissiveColor: Panner(-0.5, 0.5), Panner(0.1, -1), Panner(0.25, 0.5); Distortion: Panner(-0.5, 0.5), Panner(0.1, -1), Panner(0.25, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.EMPBlastWave_MAT (EMPBlastWave_MAT) | K | EmissiveColor: Panner(-0.5, 0.5), Panner(0.25, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.ElectroRing01_Mat (ElectroRing01_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.ElectroRing02_Mat (ElectroRing02_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Embers_Blue_MAT_INST (Fire_MAT) | K | EmissiveColor: Panner(-0.15, 0.8), Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Explosion_MAT (Explosion_MAT) | K | EmissiveColor: Panner(1, 1), Rotator(0.5 rad/s @0.5,0.5), Time; Opacity: Panner(1, 1), Rotator(0.5 rad/s @0.5,0.5), Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Fire_MAT (Fire_MAT) | K | EmissiveColor: Panner(-0.15, 0.8), Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Fire_Ring01_Mat (Fire_Ring01_Mat) | K | EmissiveColor: Panner(0.4, 0.4) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.HealBeam_MAT (HealBeam_MAT) | K | EmissiveColor: Panner(-0.15, 0), Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.15, 0), Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LaserScanner_MAT (LaserScanner_MAT) | K | EmissiveColor: Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LightVolume_Base_MAT (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LightVolume_WepPickup_MAT (LightVolume_WepPickup_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_01_MAT (Lightning_Anim_01_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_02_MAT (Lightning_Anim_02_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_03_MAT (Lightning_Anim_03_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MFlash_Side_Desat_MAT (MFlash_Side_Desat_MAT) | K | EmissiveColor: Panner(1, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_Mat (MuzzleFlash_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_White_Mat (MuzzleFlash_White_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_X_Mat (MuzzleFlash_X_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ram_model_MAT (Ram_model_MAT) | K | EmissiveColor: Panner(-0.6, 0), Panner(0.6, 1.4), Panner(0.8, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ring_Distort_Add_MAT (Ring_Distort_Add_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ring_Distort_MAT (Ring_Distort_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Opacity: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Ring_Distort_Mesh_MAT (Ring_Distort_Mesh_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Rings_Distort_MAT (Rings_Distort_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Opacity: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.SmokeCoolDepth_Mat (SmokeCoolDepth_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.SmokeThick_Mat (SmokeThick_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Steam_Add_Mat (Steam_Add_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Steam_Mat (Steam_Mat) | K | EmissiveColor: Panner(0, 0.2); Opacity: Panner(0, 0.2) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Steam_Shade_Mat (Steam_Shade_Mat) | K | EmissiveColor: Panner(0, 0.2); Opacity: Panner(0, 0.2) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Tracer_ADD_MAT (Tracer_ADD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Tracer_MAT (Tracer_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Tracer_MOD_MAT (Tracer_MOD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.Tracer_Smoke_MAT (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.arcball01_MAT (arcball01_MAT) | K | EmissiveColor: Rotator(-2 rad/s @0.5,0.5), Rotator(1 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.bursting_MAT (bursting_MAT) | K | EmissiveColor: Panner(-1, 0); Opacity: Panner(-1, 0); Distortion: Panner(-1, 0); Normal: Panner(-1, 0) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Afterburn_02_MAT (Afterburn_02_MAT) | K | EmissiveColor: Panner(0.2, 2); Opacity: Panner(0.5, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Afterburn_Circuitry_02_MAT (Afterburn_Circuitry_02_MAT) | K | EmissiveColor: Panner(0.2, 2); Opacity: Panner(0, 0.5), Panner(0.1, 0.1), Panner(0.2, 2), Panner(0.5, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Boostermaterial_02_MAT (Boostermaterial_02_MAT) | K | EmissiveColor: Panner(1, 2); Opacity: Panner(1, 2) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.tank_hover_pattern_MAT (tank_hover_pattern_MAT) | K | EmissiveColor: Sine(period 1), Time; Opacity: Panner(0.3, 0.3), Rotator(1 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| FX_RollerMine_p.Material.FX_RollerMine_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| FX_Screen_p.Materials.Static_MAT (Static_MAT) | K | EmissiveColor: Panner(-0.805, -0.942), Panner(0.42, 0.513), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.MuzzleFlash_01_MAT (MuzzleFlash_01_MAT) | K | EmissiveColor: Panner(-0.15, 0.8); Opacity: Panner(-0.15, 0.8) | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.MuzzleFlash_Side_MAT (MuzzleFlash_Side_MAT) | K | EmissiveColor: Panner(1, 0); Opacity: Panner(1, 0) | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.Barricade2.TPRO_NEU_Barricade2ForceField_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.BarricadeShield_MAT (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.RocketBarricade.TPRO_NEU_RocketBarrier_MATINST (Soundwave_ShieldBarrier_MAT) | K | EmissiveColor: Panner(-0.1, -0.5), Panner(0.1, -0.5), Panner(0.1, -0.75), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_BatteryOS_p.BatteryOmegaGlass_MATINST (ENV_Refractive_Glass_Trans_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Translucent |
| PROP_NEU_BatteryOS_p.OmegaLiquidSurface_MATINST (Coolant_Parent_MAT) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time; Normal: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_BatteryOS_p.OmegaLiquid_MATINST (TryptiGelGlass_Mat) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Translucent |
| PROP_NEU_EnergonCube_p.PROP_NEU_EnergonCube_Circuits_MATINST (PROP_NEU_EnergonCube_Circuits_MAT) | K | EmissiveColor: Panner(0, 1) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Interacts_p.PROP_ButtonInteract_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreenActive_MAT_INST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Pickups_p.AmmoPickup.PROP_NEU_AmmoPickup_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.CodeOfPower.CodeOfPowerCORE_MatINST (CodeOfPower_MAT) | K | EmissiveColor: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(-0.15, 0.18), Panner(0.1, -0.075), Panner(0.2, 0.1); Opacity: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(0.2, 0.1); Distortion: Panner(-0.15, 0.18), Panner(0.1, -0.075) | 0 / 0 | Unlit / Translucent |
| PROP_NEU_Pickups_p.EnergonTotem.Conquest_Ring_MATINST (Conquest_Ring_MAT) | K | EmissiveColor: Rotator(-0.3 rad/s @0.5,0.5), Rotator(0.5 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| PROP_NEU_Pickups_p.EnergonTotem.PROP_NEU_EnergonTotem_MATINST (ENV_Hologram_Mat) | K | EmissiveColor: Panner(0, 0.1) time-in, Sine(period 1), Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.MPBomb.BombCore_MATINST_BAT (BombCore_MAT) | K | DiffuseColor: Cosine(period 0.5), Cosine(period 1), Time; EmissiveColor: Cosine(period 0.5), Cosine(period 1), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Pickups_p.MPBomb.PROP_NEU_MPBombExplode_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.MPBomb.PROP_NEU_MPBomb_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.OvershieldPickup.PROP_NEU_Overshield_MATINST (WEP_Crates_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Opaque |
| PROP_VendingMachine_p.Ammo.PROP_VendingMachine_Ammo_MATINST (VendingMachine_Screen_MAT) | K | EmissiveColor: Cosine(period 1) in Noise_MF, Panner(0, 1) time-in, Panner(1, 1) time-in in Noise_MF, Sine(period 1) in Noise_MF, Time, Time in Noise_MF | 0 / 0 | Unlit / Opaque |
| PROP_VendingMachine_p.PROP_VendingMachine_EnergonCube_MATINST (VendingMachine_Screen_MAT) | K | EmissiveColor: Cosine(period 1) in Noise_MF, Panner(0, 1) time-in, Panner(1, 1) time-in in Noise_MF, Sine(period 1) in Noise_MF, Time, Time in Noise_MF | 0 / 0 | Unlit / Opaque |
| TPRO_KON_CorruptorSpike_p.Materials.DarkEnergonCrystal_MAT_INST (DarkEnergonCrystal_MAT) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| TR_AirRaid_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_AirRaid_ROBO_p.RB_AirRaid_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_AirRaid_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_AirRaid_VEH_p.VH_AirRaid_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Arcee_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Arcee_ROBO_p.RB_Arcee_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Arcee_VEH_p.VH_Arcee_InteriorEnergon_Mat_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Arcee_VEH_p.VH_Arcee_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Barricade_ROBO_p.MaterialInstanceConstant_679 (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Barricade_ROBO_p.RB_Barricade_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Barricade_VEH_p.VH_Barricade_NormSpec_Cust_B_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Brawl_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Brawl_ROBO_p.RB_Brawl_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Brawl_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Brawl_VEH_p.VH_Brawl_NormSpec_Cust_B_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Breakdown_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Breakdown_ROBO_p.RB_Breakdown_Cust_Mat_Inst_E (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Breakdown_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Breakdown_VEH_p.RB_BreadownVEH_Cust_Mat_INST_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_ROBO_p.RB_BumbleBee2_Cust2_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_ROBO_p.RB_BumblebeeEnergon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_VEH_p.Materials.Bumblebee_TransformInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_VEH_p.VEH_BumbleBee2_Cust2_Mat (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Deadend_ROBO_p.RB_DeadendInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Deadend_ROBO_p.RB_Deadend_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Deadend_VEH_p.VH_DeadendInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Deadend_VEH_p.VH_Deadend_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Demolishor_ROBO_p.RB_Demolishor_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Demolishor_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Demolishor_VEH_p.VH_Demolishor_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ironhide_ROBO_p.RB_IronhideInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ironhide_ROBO_p.RB_Ironhide_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ironhide_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ironhide_VEH_p.VH_Ironhide_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jazz_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jazz_ROBO_p.RB_Jazz_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jazz_VEH_p.VH_Jazz_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jetfire_ROBO_p.RB_Jetfire_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jetfire_ROBO_p.TR_JetfireInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jetfire_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jetfire_VEH_p.VH_Jetfire_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Laserbeak_VEH_p.VH_Laserbeak_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Megatron_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Megatron_ROBO_p.VH_Megatron_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Megatron_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Megatron_VEH_p.VH_Megatron_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Onslaught_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Onslaught_ROBO_p.RB_Onslaught_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Onslaught_VEH_p.MaterialInstanceConstant_4774 (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Onslaught_VEH_p.VH_Onslaught_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Optimus_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Optimus_ROBO_p.RB_OptimusPrime_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Optimus_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Optimus_VEH_p.RB_OptimusPrime_Cust2_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ratchet_ROBO_p.RB_RatchetEnergonInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ratchet_ROBO_p.RB_Ratchet_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ratchet_VEH_p.VH_RatchetEnergonInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ratchet_VEH_p.VH_Ratchet_Cust2_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.FrenzyWeapon_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.Frenzy_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.RumbleWeapon_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.Rumble_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Scattershot_ROBO_p.RB_ScattershotInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Scattershot_ROBO_p.RB_Scattershot_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Scattershot_VEH_p.Debug.VH_ScattershotInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Scattershot_VEH_p.VH_Scattershot_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Shockwave_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Shockwave_ROBO_p.RB_Shockwave_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Shockwave_VEH_p.VH_Shockwave_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_ROBO_p.RB_Sideswipe_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_VEH_p.VH_Sideswipe_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_ROBO_p.RB_Silverbolt_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_VEH_p.VH_Silverbolt_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Skywarp_ROBO_p.RB_Skywarp_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Skywarp_ROBO_p.TR_Skywarp_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Skywarp_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Skywarp_VEH_p.VH_Skywarp_NormSpec_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Slipstream_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Slipstream_ROBO_p.RB_Slipstream_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Slipstream_VEH_p.VH_Slipstream_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_ROBO_p.RB_SoldierCarAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_ROBO_p.RB_SoldierMultiAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_VEH_p.VH_SoldierCarAut_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_ROBO_p.RB_SoldierCarDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_ROBO_p.RB_SoldierMultiDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_VEH_p.VH_SniperDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_ROBO_p.RB_SoldierCarNeu_Robo_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_ROBO_p.RB_SoldierMultiNeu_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_VEH_p.VH_SoldierCarNeu_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierTankAut_VEH_p.VH_SoldierTankAutA_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierTankDec_VEH_p.VH_SoldierTankDec_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Soundwave_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Soundwave_ROBO_p.RB_Soundwave_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Soundwave_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Soundwave_VEH_p.VH_Soundwave_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_ROBO_p.TR_Starscream_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_ROBO_p.TR_Starscream_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_StarScream_VEH_p.CHR_Transformer_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_VEH_p.VH_StarscreamInterior_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_ROBO_p.TR_Thunder_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Thunder_ROBO_p.TR_Thunder_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_VEH_p.VH_Thunder_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Trypticon_ROBO_p.RB_TrypticonHead_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Warpath_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Warpath_ROBO_p.RB_Warpath1_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Warpath_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Warpath_VEH_p.RB_Warpath1_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_ROBO_p.TR_ZetaPrime_ROBO_Cust_Mat_Inst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_VEH_p.VH_ZetaPrimeInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_VEH_p.VH_ZetaPrime_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| UI_GFxHud_p.LowHealth.LowHealthScreenEffect_M (LowHealthScreenEffect_M) | K | EmissiveColor: Panner(0, -2), Panner(0, 1) | 0 / 0 | Unlit / Opaque |
| UI_GFxHud_p.StaticDischargeScreenEffect_M (StaticDischargeScreenEffect_M) | K | EmissiveColor: Panner(-0.805, -0.942), Panner(0.42, 0.513) | 0 / 0 | Unlit / Opaque |
| UI_HudMarkers_p.MPMarkerBase_MAT (MPMarkerBase_MAT) | K | Opacity: Cosine(period 1), Panner(0, -2) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MPMarkerCOP_MAT (MPMarkerCOP_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MPMarkerDominationNode_MAT (MPMarkerDominationNode_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MarkerDownedAlly_MAT (MarkerDownedAlly_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MarkerGrenade_MAT (MarkerGrenade_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| WEP_AssaultRifle_p.WEP_AssaultRifle_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Axe_p.Autobot.WEP_Axe_Energon_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_BazookaTemp1_p.WEP_Bazooka_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BeatDownClub_p.WEP_BeatDownClub_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BroadSword_p.WEP_BroadSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_BroadSword_p.WEP_BroadSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BurstRifle_p.Materials.WEP_BurstRifle_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ButterflyAxe_p.WEP_ButterflyAxeEnergon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ButterflyAxe_p.WEP_ButterflyAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_CeremonialStaff_p.WEP_CeremonialStaff_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_CodeOfPower_p.WEP_CodeOfPower_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_DetPack_p.WEP_DetPack_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_EMPShotgun_p.WEP_EMPShotgun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_FightingStaff_p.WEP_FightingStaff_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_GrenadeLauncher_p.WEP_GrenadeLauncher_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Grenade_p.WEP_Grenade_Flak_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HalberdAxe_p.WEP_HalberdAxe_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_HalberdAxe_p.WEP_HalberdAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Hammer_p.WEP_Hammer_D_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Hammer_p.WEP_Hammer_Spikes_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_HeavyMG_p.WEP_HeavyMG_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HeavyPistol_p.WEP_HeavyPistol_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HuntingDagger_p.WEP_HuntingDagger_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_IonBlaster_p.WEP_IonBlaster_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_KamikazeMine_p.WEP_KamikazeMine_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_LancingSpear_p.WEP_LancingSpear_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_LongSword_p.WEP_LongSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_LongSword_p.WEP_LongSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Maul_p.WEP_Maul_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_Maul_p.WEP_Maul_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_PlasmaCannon_p.WEP_PlasmaCannon_A_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ProngDagger_p.WEP_Energon_A_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_ProngDagger_p.WEP_ProngDagger_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_RepairBeam_p.WEP_RepairBeam_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_RocketLauncher_p.WEP_RocketLauncher_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryAbility_p.WEP_DeployedTurret_MATINST (WEP_SentryAbility_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Sine(period 1), Time; OpacityMask: Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryBase.WEP_GlassGlow_MATINST (ENV_Refractive_Glass_Opaque_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| WEP_SentryBlaster01_p.SentryBase.WEP_SentryBase_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryBlaster.WEP_SentryBlaster_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryRepair.WEP_SentryRepair_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryRocket.WEP_SentryRocket_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SerratedBlade_p.WEP_SerratedBlade_Energon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SerratedBlade_p.WEP_SerratedBlade_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shared_p.WEP_Energon_D_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_Shared_p.WEP_PhongMain_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_Frame_MATINST (WEP_Barrier_A_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(0.01, -0.02) time-in in ElectricArcs_MF, Sine(period 1) in ElectricArcs_MF, Sine(period 1) in ScanLines_MF, Time in ElectricArcs_MF, Time in ScanLines_MF | 0 / 0 | Unlit / Translucent |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_MASK_MATINST (WEP_ShieldBruteA_MASK_MAT) | K | EmissiveColor: Panner(-0.75, 0.25), Panner(0.75, -0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Barrier.ENV_ForceField_Defrag_MAT (ENV_ForceField_Defrag_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(1, -0.5), Panner(1, 0) time-in, Rotator(0.25 rad/s @0.5,0.5), Sine(period 1), Sine(period 1) in ScanLines_MF, Time, Time in ScanLines_MF; Opacity: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Barrier.WEP_Barrier_Defrag_MATINST (ENV_ForceField_Defrag_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(1, -0.5), Panner(1, 0) time-in, Rotator(0.25 rad/s @0.5,0.5), Sine(period 1), Sine(period 1) in ScanLines_MF, Time, Time in ScanLines_MF; Opacity: Rotator(0.25 rad/s @0.5,0.5); Distortion: Panner(-0.04, -0.12), Panner(0.2, 0.1) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_Frame_MATINST (WEP_Barrier_A_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(0.01, -0.02) time-in in ElectricArcs_MF, Sine(period 1) in ElectricArcs_MF, Sine(period 1) in ScanLines_MF, Time in ElectricArcs_MF, Time in ScanLines_MF | 0 / 0 | Unlit / Translucent |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_MASK_MATINST (WEP_ShieldBruteA_MASK_MAT) | K | EmissiveColor: Panner(-0.75, 0.25), Panner(0.75, -0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Decepticon.WEP_ShieldD_Energon_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_ShortSword_p.WEP_ShortSword_Energon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ShortSword_p.WEP_ShortSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shotgun_p.WEP_Shotgun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SniperRifle_p.WEP_SniperRifle_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SpikedBat_p.WEP_SpikedBat_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SpikedBat_p.WEP_SpikedBat_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SpikedMace_p.WEP_SpikedMace_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SpikedMace_p.WEP_SpikedMace_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TortureSword_p.WEP_TortureSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_TortureSword_p.WEP_TortureSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TrypticonMouthCannon_p.WEP_TrypMouthCannon_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TrypticonShoulderCannon_p.WEP_TrypShoulderCannon_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun01_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun_Overshield_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(-0.05, -0.1) time-in in Overshield_MFUNC, Panner(-0.1, -0.5) time-in in Overshield_MFUNC, Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Panner(0.2, 0.1) time-in in Overshield_MFUNC, Panner(0.5, 0.1) time-in in Overshield_MFUNC, Time, Time in Overshield_MFUNC | 0 / 0 | Phong / Masked |
| WEP_TurretRocket_p.WEP_TurretRocket_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ViciousAxe_p.WEP_ViciousAxe_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ViciousAxe_p.WEP_ViciousAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_WarHammer_p.WEP_WarHammer_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_WarHammer_p.WEP_WarHammer_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |

### MP_UND_Gorge: 304 time-driven materials (K 304)

| Material (master) | Ours | Time sources by output | Draws / tris | Lighting / blend |
|---|---|---|---|---|
| DES_IAC_WallPanelSign_p.Materials.WallPanelSign_EMISSOFF_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| DES_IAC_WallPanelSign_p.Materials.WallPanelSign_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| ENV_CORE_Floors_p.Materials.ENV_CORE_EnergonPlasma_INST (Energon_River_Mat) | K | EmissiveColor: Panner(-0.02, -0.06), Panner(-0.02, 0.03), Panner(-0.09, 0.02), Panner(0.01, -0.075), Panner(0.1, 0.05); Opacity: Panner(-0.02, -0.06), Panner(0.1, 0.05) | 0 / 0 | Unlit / Translucent |
| ENV_CORE_Floors_p.Materials.GutFloorC_MAT (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| ENV_CORE_Floors_p.Materials.SmokeCoolDepth_Mat_INST (SmokeCoolDepth_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| ENV_CORE_Wall_p.Textures.Waterfall_Slow_MATINST (Waterfall_Parent_MAT) | K | EmissiveColor: Panner(-0.008, -0.5) time-in, Panner(0.01, -0.2) time-in, Time; Distortion: Panner(-0.008, -0.5) time-in, Panner(-0.01, -0.05) time-in, Panner(0.008, -0.01) time-in, Panner(0.01, -0.2) time-in, Time; Normal: Panner(-0.008, -0.5) time-in, Panner(-0.01, -0.05) time-in, Panner(0.008, -0.01) time-in, Panner(0.01, -0.2) time-in, Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightCylinder2_Rays_Red_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2OrangeMid_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2WarmInside_Lighter_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2Warm_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightRaysV2purple_Lessdense_MATINST (LightRays_V2_Parent_MAT) | K | EmissiveColor: Panner(0.015, -0.025) | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumeCoolThick_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumeCool_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumeMid_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumeWarmThick2_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_GLB_EnvEffects_p.Material.LightVolumeWarmThink_MATINST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_IAC_Bridge_p.ENV_Bridge_Hallogram (ENV_Bridge_Hallogram) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| ENV_IAC_Bridge_p.ENV_IAC_TransBridge_LaserTarget_MATINST (ENV_CustPhongPointLightUnlit_Reflect_Mat) | K | EmissiveColor: Panner(0.5, 0) time-in, Time | 0 / 0 | Unlit / Translucent |
| ENV_IAC_Ground_p.EnergyFence.EnergyFencePurple_MAT_INST (EnergyFence_MAT) | K | EmissiveColor: Panner(0, 0.03) | 0 / 0 | Unlit / Translucent |
| ENV_IAC_Ground_p.EnergyFence.EnergyFence_MAT (EnergyFence_MAT) | K | EmissiveColor: Panner(0, 0.03) | 0 / 0 | Unlit / Translucent |
| ENV_IAC_Ground_p.EnergyFence.EnergyFence_MAT_INST (EnergyFence_MAT) | K | EmissiveColor: Panner(0, 0.03) | 0 / 0 | Unlit / Translucent |
| ENV_IAC_Shader_p.Material.IAC_Glass2_Dark_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_Dchevrons_clr_Mat (landmark_Dchevrons_clr_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_Dtarget_clr_Mat (landmark_Dtarget_clr_Mat) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_ablogo_clr_Mat (landmark_ablogo_clr_Mat) | K | EmissiveColor: Panner(-0.05, -0.03), Panner(0.02, 0.1) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_chevrons_clr_Mat (landmark_chevrons_clr_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_declogo_clr_Mat (landmark_declogo_clr_Mat) | K | EmissiveColor: Panner(-0.05, -0.03), Panner(0.02, 0.1) | 0 / 0 | Unlit / Additive |
| ENV_NEU_landmarking_p.landmark_target_clr_Mat (landmark_target_clr_Mat) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| FX_IonBlaster_p.IonBlaster_Mag_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| FX_Materials_p.MatInst.Blaster_Trail_MAT_INST (Blaster_MAT) | K | EmissiveColor: Panner(2.5, 0.5), Panner(3, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.CaptureZone_Reverse_MAT_INST (CaptureZoneLight_Base_MAT) | K | EmissiveColor: Panner(-0.15, 0.18), Panner(0, -0.05), Panner(0.01, -0.02), Time; Opacity: Panner(-0.15, 0.18), Panner(0, -0.05), Panner(0.01, -0.02), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.CircuitRadial_MATINST (CircuitRadial_MAT) | K | EmissiveColor: Rotator(0.25 rad/s @0.5,0.5), Sine(period 1); Opacity: Rotator(0.25 rad/s @0.5,0.5), Sine(period 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Distortion_Cloud_DBA_MAT_INST (Distortion_Cloud_01_MAT) | K | EmissiveColor: Panner(0, 0.3); Distortion: Panner(0, 0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.FusionBlasterBeam_MAT_INST (IonBlasterTrail_MAT) | K | EmissiveColor: Panner(2.5, 0.5), Panner(3, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.LightCylinder_Rays_MAT_INST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.LightVolume_Rays_MAT_INST (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Lightning_Anim_03_UP_MAT_INST (Lightning_Anim_03_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.MuzzleFlash_X_Mat_INST (MuzzleFlash_X_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.MatInst.Smoke_Lrg_Mat_INST (SmokeThick_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.MatInst.Trail_Smoke_01_MAT_INST (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.MatInst.Trail_Smoke_10_MAT_INST (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.AmmoShell_MAT (AmmoShell_MAT) | K | EmissiveColor: Panner(0.04, 0.08), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.BlastSphere_Death_MAT (BlastSphere_Death_MAT) | K | EmissiveColor: Time; Distortion: Time | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.Bolt_ADD_MAT (Bolt_ADD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Distortion_Cloud_01_MAT (Distortion_Cloud_01_MAT) | K | EmissiveColor: Panner(0, 0.3); Distortion: Panner(0, 0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.EMPBlastSphere_MAT (EMPBlastSphere_MAT) | K | EmissiveColor: Panner(-0.5, 0.5), Panner(0.1, -1), Panner(0.25, 0.5); Distortion: Panner(-0.5, 0.5), Panner(0.1, -1), Panner(0.25, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.EMPBlastWave_MAT (EMPBlastWave_MAT) | K | EmissiveColor: Panner(-0.5, 0.5), Panner(0.25, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.ElectroRing01_Mat (ElectroRing01_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.ElectroRing02_Mat (ElectroRing02_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Embers_Blue_MAT_INST (Fire_MAT) | K | EmissiveColor: Panner(-0.15, 0.8), Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Explosion_MAT (Explosion_MAT) | K | EmissiveColor: Panner(1, 1), Rotator(0.5 rad/s @0.5,0.5), Time; Opacity: Panner(1, 1), Rotator(0.5 rad/s @0.5,0.5), Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Fire_MAT (Fire_MAT) | K | EmissiveColor: Panner(-0.15, 0.8), Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Fire_Ring01_Mat (Fire_Ring01_Mat) | K | EmissiveColor: Panner(0.4, 0.4) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.HealBeam_MAT (HealBeam_MAT) | K | EmissiveColor: Panner(-0.15, 0), Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.15, 0), Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LaserScanner_MAT (LaserScanner_MAT) | K | EmissiveColor: Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LightVolume_Base_MAT (LightVolume_Base_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.LightVolume_WepPickup_MAT (LightVolume_WepPickup_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_01_MAT (Lightning_Anim_01_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_02_MAT (Lightning_Anim_02_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Lightning_Anim_03_MAT (Lightning_Anim_03_MAT) | K | EmissiveColor: Time | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MFlash_Side_Desat_MAT (MFlash_Side_Desat_MAT) | K | EmissiveColor: Panner(1, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_Mat (MuzzleFlash_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_White_Mat (MuzzleFlash_White_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.MuzzleFlash_X_Mat (MuzzleFlash_X_Mat) | K | EmissiveColor: Panner(0.15, 1) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ram_model_MAT (Ram_model_MAT) | K | EmissiveColor: Panner(-0.6, 0), Panner(0.6, 1.4), Panner(0.8, 0) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ring_Distort_Add_MAT (Ring_Distort_Add_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Ring_Distort_MAT (Ring_Distort_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Opacity: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Ring_Distort_Mesh_MAT (Ring_Distort_Mesh_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Rings_Distort_MAT (Rings_Distort_MAT) | K | EmissiveColor: Panner(0.1, -0.3); Opacity: Panner(0.1, -0.3); Distortion: Panner(0.1, -0.3) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.SmokeCoolDepth_Mat (SmokeCoolDepth_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.SmokeThick_Mat (SmokeThick_Mat) | K | EmissiveColor: Time; Opacity: Time | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Steam_Add_Mat (Steam_Add_Mat) | K | EmissiveColor: Panner(0, 0.2) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Steam_Mat (Steam_Mat) | K | EmissiveColor: Panner(0, 0.2); Opacity: Panner(0, 0.2) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Steam_Shade_Mat (Steam_Shade_Mat) | K | EmissiveColor: Panner(0, 0.2); Opacity: Panner(0, 0.2) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Tracer_ADD_MAT (Tracer_ADD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Additive |
| FX_Materials_p.Materials.Tracer_MAT (Tracer_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.Tracer_MOD_MAT (Tracer_MOD_MAT) | K | EmissiveColor: Panner(-0.5, 0), Panner(0, 0.65); Opacity: Panner(-0.5, 0), Panner(0, 0.65) | 0 / 0 | Unlit / Modulate |
| FX_Materials_p.Materials.Tracer_Smoke_MAT (Tracer_Smoke_MAT) | K | EmissiveColor: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5); Opacity: Panner(-0.3, -0.5), Panner(0.01, -0.05), Rotator(0.05 rad/s @0.5,0.5) | 0 / 0 | Unlit / Translucent |
| FX_Materials_p.Materials.arcball01_MAT (arcball01_MAT) | K | EmissiveColor: Rotator(-2 rad/s @0.5,0.5), Rotator(1 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Afterburn_02_MAT (Afterburn_02_MAT) | K | EmissiveColor: Panner(0.2, 2); Opacity: Panner(0.5, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Afterburn_Circuitry_02_MAT (Afterburn_Circuitry_02_MAT) | K | EmissiveColor: Panner(0.2, 2); Opacity: Panner(0, 0.5), Panner(0.1, 0.1), Panner(0.2, 2), Panner(0.5, 0.5) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.Boostermaterial_02_MAT (Boostermaterial_02_MAT) | K | EmissiveColor: Panner(1, 2); Opacity: Panner(1, 2) | 0 / 0 | Unlit / Additive |
| FX_Navigation_p.tank_hover_pattern_MAT (tank_hover_pattern_MAT) | K | EmissiveColor: Sine(period 1), Time; Opacity: Panner(0.3, 0.3), Rotator(1 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| FX_RollerMine_p.Material.FX_RollerMine_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| FX_Screen_p.Materials.Static_MAT (Static_MAT) | K | EmissiveColor: Panner(-0.805, -0.942), Panner(0.42, 0.513), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.MuzzleFlash_01_MAT (MuzzleFlash_01_MAT) | K | EmissiveColor: Panner(-0.15, 0.8); Opacity: Panner(-0.15, 0.8) | 0 / 0 | Unlit / Additive |
| FX_Weapons_p.Materials.MuzzleFlash_Side_MAT (MuzzleFlash_Side_MAT) | K | EmissiveColor: Panner(1, 0); Opacity: Panner(1, 0) | 0 / 0 | Unlit / Additive |
| PROP_EnergonSigns_p.AutobotLOGO_CLR_Mat (AutobotLOGO_CLR_Mat) | K | EmissiveColor: Panner(0, -0.19), Panner(0.01, 0) | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.Barricade2.TPRO_NEU_Barricade2ForceField_MATINST (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.BarricadeShield_MAT (ENV_ForceField_ALL_MAT) | K | EmissiveColor: Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Barricade_p.RocketBarricade.TPRO_NEU_RocketBarrier_MATINST (Soundwave_ShieldBarrier_MAT) | K | EmissiveColor: Panner(-0.1, -0.5), Panner(0.1, -0.5), Panner(0.1, -0.75), Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_BatteryOS_p.BatteryOmegaGlass_MATINST (ENV_Refractive_Glass_Trans_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Panner(1, 0) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Translucent |
| PROP_NEU_BatteryOS_p.OmegaLiquidSurface_MATINST (Coolant_Parent_MAT) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time; Normal: Panner(-0.02, 0.06) time-in, Panner(0.001, 0.005) time-in, Panner(0.002, 0.006) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_BatteryOS_p.OmegaLiquid_MATINST (TryptiGelGlass_Mat) | K | Distortion: Panner(-0.02, 0.06) time-in, Panner(0.05, -0.02) time-in, Time | 0 / 0 | Unlit / Translucent |
| PROP_NEU_EnergonCube_p.PROP_NEU_EnergonCube_Circuits_MATINST (PROP_NEU_EnergonCube_Circuits_MAT) | K | EmissiveColor: Panner(0, 1) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| PROP_NEU_Interacts_p.PROP_ButtonInteract_MATINST (ENV_PhongMain_NS_Mat) | K | EmissiveColor: Sine(period 1) in ENV_Emissive_MF, Time in ENV_Emissive_MF | 0 / 0 | Phong / Opaque |
| PROP_NEU_Monitors_p.MonitorScreenActiveOrange_MATINST (MonitorScreen_Parent_MAT) | K | EmissiveColor: Panner(0, -0.2) time-in, Panner(0, 0.2) time-in, Sine(period 0.5), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Pickups_p.AmmoPickup.PROP_NEU_AmmoPickup_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.CodeOfPower.CodeOfPowerCORE_MatINST (CodeOfPower_MAT) | K | EmissiveColor: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(-0.15, 0.18), Panner(0.1, -0.075), Panner(0.2, 0.1); Opacity: Panner(-0.02, 0.03), Panner(-0.04, -0.12), Panner(0.2, 0.1); Distortion: Panner(-0.15, 0.18), Panner(0.1, -0.075) | 0 / 0 | Unlit / Translucent |
| PROP_NEU_Pickups_p.EnergonTotem.Conquest_Ring_MATINST (Conquest_Ring_MAT) | K | EmissiveColor: Rotator(-0.3 rad/s @0.5,0.5), Rotator(0.5 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| PROP_NEU_Pickups_p.EnergonTotem.PROP_NEU_EnergonTotem_MATINST (ENV_Hologram_Mat) | K | EmissiveColor: Panner(0, 0.1) time-in, Sine(period 1), Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.MPBomb.BombCore_MATINST_BAT (BombCore_MAT) | K | DiffuseColor: Cosine(period 0.5), Cosine(period 1), Time; EmissiveColor: Cosine(period 0.5), Cosine(period 1), Time | 0 / 0 | Phong / Opaque |
| PROP_NEU_Pickups_p.MPBomb.PROP_NEU_MPBombExplode_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.MPBomb.PROP_NEU_MPBomb_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| PROP_NEU_Pickups_p.OvershieldPickup.PROP_NEU_Overshield_MATINST (WEP_Crates_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Opaque |
| PROP_VendingMachine_p.Ammo.PROP_VendingMachine_Ammo_MATINST (VendingMachine_Screen_MAT) | K | EmissiveColor: Cosine(period 1) in Noise_MF, Panner(0, 1) time-in, Panner(1, 1) time-in in Noise_MF, Sine(period 1) in Noise_MF, Time, Time in Noise_MF | 0 / 0 | Unlit / Opaque |
| PROP_VendingMachine_p.PROP_VendingMachine_EnergonCube_MATINST (VendingMachine_Screen_MAT) | K | EmissiveColor: Cosine(period 1) in Noise_MF, Panner(0, 1) time-in, Panner(1, 1) time-in in Noise_MF, Sine(period 1) in Noise_MF, Time, Time in Noise_MF | 0 / 0 | Unlit / Opaque |
| TPRO_KON_CorruptorSpike_p.Materials.DarkEnergonCrystal_MAT_INST (DarkEnergonCrystal_MAT) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| TR_AirRaid_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_AirRaid_ROBO_p.RB_AirRaid_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_AirRaid_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_AirRaid_VEH_p.VH_AirRaid_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Arcee_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Arcee_ROBO_p.RB_Arcee_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Arcee_VEH_p.VH_Arcee_InteriorEnergon_Mat_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Arcee_VEH_p.VH_Arcee_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Barricade_ROBO_p.MaterialInstanceConstant_679 (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Barricade_ROBO_p.RB_Barricade_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Barricade_VEH_p.VH_Barricade_NormSpec_Cust_B_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Brawl_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Brawl_ROBO_p.RB_Brawl_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Brawl_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Brawl_VEH_p.VH_Brawl_NormSpec_Cust_B_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Breakdown_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Breakdown_ROBO_p.RB_Breakdown_Cust_Mat_Inst_E (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Breakdown_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Breakdown_VEH_p.RB_BreadownVEH_Cust_Mat_INST_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_ROBO_p.RB_BumbleBee2_Cust2_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_ROBO_p.RB_BumblebeeEnergon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_VEH_p.Materials.Bumblebee_TransformInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_BumbleBee_VEH_p.VEH_BumbleBee2_Cust2_Mat (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Deadend_ROBO_p.RB_DeadendInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Deadend_ROBO_p.RB_Deadend_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Deadend_VEH_p.VH_DeadendInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Deadend_VEH_p.VH_Deadend_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Demolishor_ROBO_p.RB_Demolishor_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Demolishor_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Demolishor_VEH_p.VH_Demolishor_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ironhide_ROBO_p.RB_IronhideInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ironhide_ROBO_p.RB_Ironhide_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ironhide_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ironhide_VEH_p.VH_Ironhide_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jazz_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jazz_ROBO_p.RB_Jazz_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jazz_VEH_p.VH_Jazz_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jetfire_ROBO_p.RB_Jetfire_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Jetfire_ROBO_p.TR_JetfireInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jetfire_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Jetfire_VEH_p.VH_Jetfire_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Laserbeak_VEH_p.VH_Laserbeak_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Megatron_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Megatron_ROBO_p.VH_Megatron_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Megatron_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Megatron_VEH_p.VH_Megatron_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Onslaught_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Onslaught_ROBO_p.RB_Onslaught_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Onslaught_VEH_p.MaterialInstanceConstant_4774 (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Onslaught_VEH_p.VH_Onslaught_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Optimus_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Optimus_ROBO_p.RB_OptimusPrime_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Optimus_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Optimus_VEH_p.RB_OptimusPrime_Cust2_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ratchet_ROBO_p.RB_RatchetEnergonInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ratchet_ROBO_p.RB_Ratchet_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Ratchet_VEH_p.VH_RatchetEnergonInterior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Ratchet_VEH_p.VH_Ratchet_Cust2_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.FrenzyWeapon_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.Frenzy_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.RumbleWeapon_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_RumbleFrenzy_ROBO_p.Rumble_MatInst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Scattershot_ROBO_p.RB_ScattershotInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Scattershot_ROBO_p.RB_Scattershot_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Scattershot_VEH_p.Debug.VH_ScattershotInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Scattershot_VEH_p.VH_Scattershot_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Shockwave_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Shockwave_ROBO_p.RB_Shockwave_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Shockwave_VEH_p.VH_Shockwave_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_ROBO_p.RB_Sideswipe_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Sideswipe_VEH_p.VH_Sideswipe_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_ROBO_p.RB_Silverbolt_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SilverBolt_VEH_p.VH_Silverbolt_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Skywarp_ROBO_p.RB_Skywarp_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Skywarp_ROBO_p.TR_Skywarp_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Skywarp_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Skywarp_VEH_p.VH_Skywarp_NormSpec_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Slipstream_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Slipstream_ROBO_p.RB_Slipstream_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Slipstream_VEH_p.VH_Slipstream_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_ROBO_p.RB_SoldierCarAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_ROBO_p.RB_SoldierMultiAut_Robo_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarAut_VEH_p.VH_SoldierCarAut_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_ROBO_p.RB_SoldierCarDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_ROBO_p.RB_SoldierMultiDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarDec_VEH_p.VH_SniperDec_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_ROBO_p.RB_SoldierCarNeu_Robo_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_ROBO_p.RB_SoldierMultiNeu_MatINST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierCarNeu_VEH_p.VH_SoldierCarNeu_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierTankAut_VEH_p.VH_SoldierTankAutA_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_SoldierTankDec_VEH_p.VH_SoldierTankDec_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Soundwave_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Soundwave_ROBO_p.RB_Soundwave_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Soundwave_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Soundwave_VEH_p.VH_Soundwave_Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_ROBO_p.TR_Starscream_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_ROBO_p.TR_Starscream_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_StarScream_VEH_p.CHR_Transformer_NormSpec_Cust_F_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_StarScream_VEH_p.VH_StarscreamInterior_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_ROBO_p.TR_Thunder_2Cust_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Thunder_ROBO_p.TR_Thunder_Interior_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Thunder_VEH_p.VH_Thunder_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Trypticon_ROBO_p.RB_TrypticonHead_NormSpec_Cust_E_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Warpath_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Warpath_ROBO_p.RB_Warpath1_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_Warpath_VEH_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_Warpath_VEH_p.RB_Warpath1_Cust_Mat_INST_B (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_ROBO_p.InteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_ROBO_p.TR_ZetaPrime_ROBO_Cust_Mat_Inst (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_VEH_p.VH_ZetaPrimeInteriorAlt_Energon_MAT_INST (InteriorAlt_Energon_MAT) | K | EmissiveColor: Panner(0, 0.05), Panner(0, 0.08) | 0 / 0 | Phong / Opaque |
| TR_ZetaPrime_VEH_p.VH_ZetaPrime_Mat_INST (CHR_Transformer_NormSpec_Cust_E_Mat) | K | EmissiveColor: Panner(0.01, -0.02), Sine(period 1), Time | 0 / 0 | Phong / Opaque |
| UI_GFxHud_p.LowHealth.LowHealthScreenEffect_M (LowHealthScreenEffect_M) | K | EmissiveColor: Panner(0, -2), Panner(0, 1) | 0 / 0 | Unlit / Opaque |
| UI_GFxHud_p.StaticDischargeScreenEffect_M (StaticDischargeScreenEffect_M) | K | EmissiveColor: Panner(-0.805, -0.942), Panner(0.42, 0.513) | 0 / 0 | Unlit / Opaque |
| UI_HudMarkers_p.MPMarkerBase_MAT (MPMarkerBase_MAT) | K | Opacity: Cosine(period 1), Panner(0, -2) time-in, Sine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MPMarkerCOP_MAT (MPMarkerCOP_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MPMarkerDominationNode_MAT (MPMarkerDominationNode_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MarkerDownedAlly_MAT (MarkerDownedAlly_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| UI_HudMarkers_p.MarkerGrenade_MAT (MarkerGrenade_MAT) | K | Opacity: Cosine(period 1), Time | 0 / 0 | Unlit / Additive |
| WEP_AssaultRifle_p.WEP_AssaultRifle_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Axe_p.Autobot.WEP_Axe_Energon_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_BazookaTemp1_p.WEP_Bazooka_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BeatDownClub_p.WEP_BeatDownClub_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BroadSword_p.WEP_BroadSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_BroadSword_p.WEP_BroadSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_BurstRifle_p.Materials.WEP_BurstRifle_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ButterflyAxe_p.WEP_ButterflyAxeEnergon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ButterflyAxe_p.WEP_ButterflyAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_CeremonialStaff_p.WEP_CeremonialStaff_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_CodeOfPower_p.WEP_CodeOfPower_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_DetPack_p.WEP_DetPack_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_EMPShotgun_p.WEP_EMPShotgun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_FightingStaff_p.WEP_FightingStaff_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_GrenadeLauncher_p.WEP_GrenadeLauncher_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Grenade_p.WEP_Grenade_Flak_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HalberdAxe_p.WEP_HalberdAxe_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_HalberdAxe_p.WEP_HalberdAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Hammer_p.WEP_Hammer_D_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Hammer_p.WEP_Hammer_Spikes_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_HeavyMG_p.WEP_HeavyMG_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HeavyPistol_p.WEP_HeavyPistol_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_HuntingDagger_p.WEP_HuntingDagger_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_IonBlaster_p.WEP_IonBlaster_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_KamikazeMine_p.WEP_KamikazeMine_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_LancingSpear_p.WEP_LancingSpear_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_LongSword_p.WEP_LongSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_LongSword_p.WEP_LongSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Maul_p.WEP_Maul_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_Maul_p.WEP_Maul_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_PlasmaCannon_p.WEP_PlasmaCannon_A_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ProngDagger_p.WEP_Energon_A_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_ProngDagger_p.WEP_ProngDagger_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_RepairBeam_p.WEP_RepairBeam_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_RocketLauncher_p.WEP_RocketLauncher_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryAbility_p.WEP_DeployedTurret_MATINST (WEP_SentryAbility_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Sine(period 1), Time; OpacityMask: Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryBase.WEP_GlassGlow_MATINST (ENV_Refractive_Glass_Opaque_Mat) | K | EmissiveColor: Panner(0.04, 0.08), Sine(period 1), Time | 0 / 0 | Unlit / Opaque |
| WEP_SentryBlaster01_p.SentryBase.WEP_SentryBase_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryBlaster.WEP_SentryBlaster_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryRepair.WEP_SentryRepair_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SentryBlaster01_p.SentryRocket.WEP_SentryRocket_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SerratedBlade_p.WEP_SerratedBlade_Energon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SerratedBlade_p.WEP_SerratedBlade_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shared_p.WEP_Energon_D_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_Shared_p.WEP_PhongMain_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_Frame_MATINST (WEP_Barrier_A_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(0.01, -0.02) time-in in ElectricArcs_MF, Sine(period 1) in ElectricArcs_MF, Sine(period 1) in ScanLines_MF, Time in ElectricArcs_MF, Time in ScanLines_MF | 0 / 0 | Unlit / Translucent |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_MASK_MATINST (WEP_ShieldBruteA_MASK_MAT) | K | EmissiveColor: Panner(-0.75, 0.25), Panner(0.75, -0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Autobot.WEP_ShieldBruteA_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Barrier.ENV_ForceField_Defrag_MAT (ENV_ForceField_Defrag_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(1, -0.5), Panner(1, 0) time-in, Rotator(0.25 rad/s @0.5,0.5), Sine(period 1), Sine(period 1) in ScanLines_MF, Time, Time in ScanLines_MF; Opacity: Rotator(0.25 rad/s @0.5,0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Barrier.WEP_Barrier_Defrag_MATINST (ENV_ForceField_Defrag_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(1, -0.5), Panner(1, 0) time-in, Rotator(0.25 rad/s @0.5,0.5), Sine(period 1), Sine(period 1) in ScanLines_MF, Time, Time in ScanLines_MF; Opacity: Rotator(0.25 rad/s @0.5,0.5); Distortion: Panner(-0.04, -0.12), Panner(0.2, 0.1) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_Frame_MATINST (WEP_Barrier_A_MAT) | K | EmissiveColor: Panner(0, 0.1) time-in in ScanLines_MF, Panner(0.01, -0.02) time-in in ElectricArcs_MF, Sine(period 1) in ElectricArcs_MF, Sine(period 1) in ScanLines_MF, Time in ElectricArcs_MF, Time in ScanLines_MF | 0 / 0 | Unlit / Translucent |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_MASK_MATINST (WEP_ShieldBruteA_MASK_MAT) | K | EmissiveColor: Panner(-0.75, 0.25), Panner(0.75, -0.5) | 0 / 0 | Unlit / Additive |
| WEP_Shield_p.Decepticon.WEP_ShieldBruteD_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shield_p.Decepticon.WEP_ShieldD_Energon_MATINST (Energon_Base_01_MAT) | K | EmissiveColor: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time; Opacity: Panner(-0.6, 1) time-in, Panner(0, -0.2), Panner(0, 0.5), Panner(0.1, 0.2) time-in, Time | 0 / 0 | Unlit / Translucent |
| WEP_ShortSword_p.WEP_ShortSword_Energon_Tech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ShortSword_p.WEP_ShortSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_Shotgun_p.WEP_Shotgun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SniperRifle_p.WEP_SniperRifle_MAT (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SpikedBat_p.WEP_SpikedBat_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SpikedBat_p.WEP_SpikedBat_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_SpikedMace_p.WEP_SpikedMace_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_SpikedMace_p.WEP_SpikedMace_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TortureSword_p.WEP_TortureSword_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_TortureSword_p.WEP_TortureSword_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TrypticonMouthCannon_p.WEP_TrypMouthCannon_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TrypticonShoulderCannon_p.WEP_TrypShoulderCannon_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun01_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_TurretIonGun_p.WEP_TurretIonGun_Overshield_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(-0.05, -0.1) time-in in Overshield_MFUNC, Panner(-0.1, -0.5) time-in in Overshield_MFUNC, Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Panner(0.2, 0.1) time-in in Overshield_MFUNC, Panner(0.5, 0.1) time-in in Overshield_MFUNC, Time, Time in Overshield_MFUNC | 0 / 0 | Phong / Masked |
| WEP_TurretRocket_p.WEP_TurretRocket_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_ViciousAxe_p.WEP_ViciousAxe_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_ViciousAxe_p.WEP_ViciousAxe_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |
| WEP_WarHammer_p.WEP_WarHammer_EnergonTech_MATINST (Electric_Lava_Tech_B_Mat) | K | EmissiveColor: Time | 0 / 0 | Phong / Opaque |
| WEP_WarHammer_p.WEP_WarHammer_MATINST (WEP_PhongMain_MAT) | K | EmissiveColor: Panner(0, 0.08) time-in, Panner(0.01, 0.05) time-in, Time | 0 / 0 | Phong / Masked |

### Matinee property / material-parameter tracks in the MP map packages

| Track | Class | Param / property | Keys (span s) | Values |
|---|---|---|---|---|
| MP_ORB_Debris_BASE_m.TheWorld.PersistentLevel.Main_Sequence.Old.7_Kill_Streak_(Tryp_and_Omega)_0.InterpData_11520.InterpGroup_15901.InterpTrackFloatMaterialParam_9137 | FloatMaterialParam | Opacity | 1 ([0.0, 0.0]) | [0.0] |
| MP_ORB_Debris_BASE_m.TheWorld.PersistentLevel.Main_Sequence.Old.7_Kill_Streak_(Tryp_and_Omega)_0.InterpData_5164.InterpGroup_6806.InterpTrackFloatMaterialParam_9137 | FloatMaterialParam | Opacity | 6 ([0.0, 8.082770347595215]) | [0.0, 0.0, 0.05000000074505806, 4.0, 1.0, 0.0] |
| MP_ORB_Debris_BASE_m.TheWorld.PersistentLevel.Main_Sequence.Old.7_Kill_Streak_(Tryp_and_Omega)_0.InterpData_6584.InterpGroup_2756.InterpTrackFloatProp_11985 | FloatProp | DrawScale | 4 ([0.0, 6.0]) | [0.10000000149011612, 0.5, 0.5, 0.10000000149011612] |
| MP_ESC_BrokenHope_Base_m.TheWorld.PersistentLevel.Main_Sequence.Megatron.InterpData_6121.InterpGroup_11537.InterpTrackVectorProp_10563 | VectorProp | DrawScale3D | 15 ([0.0, 27.007600784301758]) | [{'X': 0.0010000000474974513, 'Y': 1.1988199949264526, 'Z': 1.1988199949264526}, {'X': 1.1988199949264526, 'Y': 1.198819 |
| MP_ORB_Debris_BASE_m.TheWorld.PersistentLevel.Main_Sequence.Old.7_Kill_Streak_(Tryp_and_Omega)_0.InterpData_5164.InterpGroup_14770.InterpTrackVectorProp_15415 | VectorProp | DrawScale3D | 5 ([0.0, 8.043399810791016]) | [{'X': 4.3260698318481445, 'Y': 7.911330223083496, 'Z': 1.3630499839782715}, {'X': 2.29967999458313, 'Y': 4.205560207366 |
