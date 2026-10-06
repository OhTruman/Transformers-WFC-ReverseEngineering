# Targeted pass 5 — newest playtest discrepancies (2026-10-05)

Labels:
- **C** = confirmed (script / cooked data / native);
- **H** = high confidence;
- **P** = partial;
- **U** = unknown.

No Rebuild code was touched.

Sources:
- `work/script/decomp`, `work/q/streets_base_gameclasses.txt`;
- `authored.db`;
- shipped `Coalesced_ini`;
- ExtractedAssets (read in place).

New data files:
- `notes/data/weapon_effect_bindings.json` (every weapon class → mesh template, muzzle FX + sockets, tracers, default squib, MP data, fire types, projectile classes);
- `notes/data/projectile_effect_bindings.json` (every projectile class → PROJMESH, static mesh, flight FX, explosion FX, flight sound, MP/SP data, speed, damage).

---

## 1. Title-scene Cybertron: dark / star-like look (RD)

**Meshes and materials (C, authored):**
- The planet is ten static meshes from `ENV_NEU_CybertronOrbit_P` in `UI_FrontEnd_m`, all at Scale3D 4: Core, Crust, Web, SurfaceA/B, CybertronShellLow, IoconBuildings, KaonBuildings, BlastBuildings, BlastDebris.
- Section materials are `ENV_NEU_CybertronLow{Core,Crust,Web,Surface,Shell,Iocon,Kaon,Blast,Debris}_Mat`.
- **SurfaceA and SurfaceB carry a component override, `ENV_NEU_CybertronLowShell_Mat`**, which replaces the mesh's own LowSurface material.

**Material structure (C).** All are lit (Phong) opaque materials:
- Diffuse: the `*_CLR` map.
- Emissive: sparse "city light" textures × gain:
  - Crust/Web `*_Illum` × 0.5 + Shell_Emiss × 1;
  - Surface_Emiss × 7;
  - Core_Emmis × (1, 1, 2);
  - Iocon/Kaon EMISS maps.
- **Fresnel rim:** a ShaderCode node on (Normal, CameraVector), power 4, with a blue VectorParameter:
  - LowSurface: (0.080, 0.154, 0.208) × 70;
  - LowShell: (0.101, 0.334, 0.632).
- **LowShell** adds a reflection-vector cubemap term (`Iacon_Streets_CubeMap`).

**Emissive texture coverage (C, measured):**

| Texture | Pixels > 0.5 | Pixels < 0.05 |
|---|---|---|
| Crust_Illum | 2.8 % | 84 % |
| Iocon EMISS | 4.0 % | 92 % |
| Surface_Emiss | 0.8 % | 97 % |
| Shell_Emiss | 0.02 % | 99 % |

**So the emissive layer on its own is a dark sphere covered in point-like lights.**

**Lighting (C):**
- Every planet component except the two Blast pieces has a 153-byte native LOD tail (light/shadow-map data). `UI_FrontEnd_m_LM` holds **6 LightMapTexture2D**.
- The level's 14 static point lights (radius 4000–40000, in a StaticLightCollectionActor) are baked into them.
- `LightingChannels` = {Static}. The SkyLight (Brightness 2, (142, 173, 210)) has Static = false, so it does not light the planet.

**Conclusion (H):**
- The planet's diffuse brightness in the original comes **only from the baked lightmaps**.
- A "dark sphere with star-like specks" is exactly what these materials give **when the lightmap term is missing**, i.e. emissive + rim only. It is therefore probably **not authentic**.
- Rendering should verify, on the planet components:
  1. their lightmap is bound;
  2. the SurfaceA/B → LowShell override is applied.
- **P:** the lightmap texel contents were not decoded, so the absolute brightness of the lit side is unverified.

(Separately, the 51 title InterpActors with {Dynamic} channels are Rendering's existing CONFIRMED item.)

## 2. Multiplayer match-start staging and countdown (GP / FE)

All C unless marked. This was mostly already in `MILESTONE05_FRONTEND_MATCH_BOOTSTRAP.md` §4–§5.2; the new items are marked **new**.

**Lobby, before travel (§4):**
- **Public** match:
  - `BeginIntermissionCountdown` = `LobbyIntermissionTime` **45 s**;
  - ticks below **10 s** (`BL_HUD_INTERFACE.CTF_ROUND_TIMER_01`);
  - `FinalCountdown`, then `StartLevel`.
- **Private / offline** match:
  - status 3, "Waiting for host to start game";
  - host start → `BeginShortCountdown` = **10 s** → `FinalCountdown`;
  - `AutostartCountdown = !IsPrivateGame()`.
- `FinalCountdown` assigns teams (`AssignTeams` / `ForceToTeam` → `PickTeam`).

**In the match map** (`TnMultiplayerGame.PendingMatch`; the same code for public and private):
- `bWaitingToStartMatch`, `GRI.bMatchHasBegun = false`, GameStatus 2;
- `GRI.ResetCountdown(true, MatchAutoStartCountdown = 10)` (shipped ini `[TransContent.TnMultiplayerGame]`; Survival uses 15);
- `DecrementCountdown` every 1.0 s. Every value 10…0 plays the low-countdown tick, since `LowCountdownTickThreshold` is 10;
- **`TrySpawnPlayer` returns false: no pawn exists during the countdown;**
- `ReadyToStartMatch` = `CurrentCountdown <= 0` → `StartMatch`;
- client UI: character select (`CustomTransformers_GFX`), then `PreGameCountdown_GFX` (mode icon, mode name, countdown).

**Countdown post-process — new (was PARTIAL):**
- `TnPlayerControllerMultiplayer.SpawnPlayerCamera` → `ActivatePostProcessModification(GameCountdownPostProcess)`, local player only.
- It starts **when the local camera is created on map load**:
  - ActiveTime 6;
  - RampIn 0.1, RampOut 3;
  - bloom 5, DOF, full desaturation.
- So the first ~6 s (+3 s ramp-out) of the 10 s countdown is the desaturated / blurred look.

**Match start — `InProgress.BeginState`:**
- `ElapsedTime = 0`, status 3, `ResetPlayerStats`;
- UI event 3, then the clock;
- `SpawnHelper.Tick(0)`, which **spawns everyone at once**;
- `GameRulesModifiers.HandleStartGame` → `BroadcastGameTypeMessage(0)`. **The mode announcer line plays at match start, after the countdown, not during it.**

**Offline / private versus online:** the in-map staging has **no separate path**. The only difference is the lobby countdown (45 s public auto-start vs 10 s host-start).

## 3. Null Ray (`TnWeaponSniperRifle`, "Null Ray (10x Scope)") fine aim (GP / FE / RD)

**Input (C, shipped Xe-TransInput):**
- PC **RightMouseButton = `ToggleFineAim | Boost`**: a **toggle** on PC (Boost applies in vehicle form).
- Pad LeftTrigger = `FineAim | Boost`, with `FineAim | OnRelease StopFineAim`: **hold** on pad.

**Gating (C):** `PlayerWalking.FineAim`:
- with the Magma Frag Launcher equipped it **detonates grenades** instead;
- ignored while downed or reviving.

`CanFineAim` is false while:
- meleeing;
- reloading;
- dodging.

`TnFineAimManager.Tick` starts or stops fine aim against that each frame.

**On start (C):**
- `PP.StartFineAim`;
- ground speed ×**0.5** (`_GroundSpeedMultiplier`, ini);
- camera state `TnPCS_FineAim` is added. The weapon already holds `WeaponPCS = TnPCS_SniperRifle` while equipped.
- **Target snap** is **disabled** for scoped weapons (`HasFineAimScope` = true for the Null Ray). Other weapons snap with a 1.0 s timeout.

**Stops automatically when:**
- the weapon overheats (`CheckSnipingOverheat`);
- taking a hit applies `TnBuffScrambleHudOnDamageWhenSnipingInFineAim` (0.1 s HUD scramble).

**Camera (C, `CAM_Strategies_p.OverTheShoulder_STRATEGY`, used by every MP chassis CAMSET for robot form):**

| Setting | Default | Sniper + FineAim | FineAim (other) | HeavyPistol / BurstRifle + FineAim |
|---|---|---|---|---|
| FOV | 80 (smooth 0.4) | **20** (smooth 0.1) | 45 | 30 |
| Orbit distance | 800 | **100** | 800 | 100 |
| Screen offset (X, Y, Z by pitch) | (150, 300, 150 / −35 / 150) | **(350, 300, 150 / −35 / 150)**, smooth 0.1 | (−50, 300, 80 / −35 / 80) | as sniper |
| Look speed yaw / pitch | 50 / 25 | **6.5 / 3.25** | 25 / 12.5 | 9.375 / 4.6875 |
| Wiggle (scope sway) | rot amp 0.1°, 8 / 18 / 12 Hz | **0.45°, 3 / 10 / 6 Hz**, random | — | — |

- **There is one zoom stage only.** No zoom levels exist anywhere; "10x" is marketing text.
- The FOV ratio 80 → 20 is 4× in tan terms.
- Look-speed changes blend over `SpeedTransitionTime` 0.5 s.

**Mouse sensitivity (C, script + ini):**
- `TnOrbitRotationCameraBehavior` under mouse and keyboard:
  - yaw += mouseDelta × `MouseCameraSensitivityX` **0.00114286** × LookSpeed.Yaw × lerp(**0.03, 0.2**, sensitivity setting) × modifier × 182.04.
  - **There is no ramp and no dt.**
- So the Null Ray in fine aim turns at **6.5 / 50 = 0.13×** the normal mouse rate, and pitch likewise.
- Pad uses `RampSpeedMultiplier` 2.5 and Low/High multipliers 0.8 / 1.5 with a ramp.

**Scope presentation (C, Hud_GFX):**
- `NotifyFineAimChanged(1)` with CurrentWeapon `TnWeaponSniperRifle` → `showScope('long')`. `'short'` is HeavyPistol and `'medium'` is BurstRifle.
- Sounds: `WP_StartFineAim` = `BL_WPN_GUN_SNIPER.ZOOM_IN`, `WP_EndFineAim` = `ZOOM_OUT`.

**Weapon (C, `SniperRifle_MP_WEPDATA`):**
- instant hit **162** (`TnDamageTypeSniperRifle`);
- fire interval **1.25 s**;
- clip **4**, reserve 8, max 12, reload 2.5 s;
- range 30000, damage ×1.0 to 20000, ×0.5 at 30000;
- per-shot spread 0.2→0.4 (+0.1/shot, 4 s cooldown);
- heat +25/shot, loss 200/s after 4 s, overheat delay 3 s;
- recoil camera: FOV +0.5, pitch 1°, 0.7 s.

## 4. Vehicle archetypes (GP)

Default MP chassis: Scout = Car2 Sideswipe / Car4 Barricade; Scientist = Jet4 AirRaid / Jet Starscream; Leader = Truck3 Ironhide / Truck4 Soundwave; Soldier = Tank3 Warpath / Tank2 Brawl. All values C (authored blueprints + class CDOs + script).

| | **Car (Scout)** | **Jet (Scientist)** | **Truck (Leader)** | **Tank (Soldier)** |
|---|---|---|---|---|
| Hover sim | `HoverCar_Physics`: accel 4000, **max speed 1500** (CDO), suspension r100, k 8000 / d 4000, rest 200 | `HoverPlane_Physics`: accel 2500, max 1500 | `HoverTruck_Physics`: accel 3000 (CDO), max 1500, suspension r185, k 10000 (CDO) / d 4000, rest 250 | `HoverTank_Physics`: accel 2500, max 1500, **boost 2500**, suspension r250, k 20000 / d 6000, rest 250, recoil 750 |
| Boost | `Car_Physics` wheels: mass 1500, MaxSpeed **3000**, MaxAccel 3000, steer 20° front | **Flying** state: `Plane_Physics` MaxSpeed 4000, accel 3000, drag 600 | `Truck_Physics`: mass 2500, MaxSpeed 3000, accel 2500 | stays in hover sim at **MaxBoostSpeed 2500**, input forced forward |
| Jump | hover: +1200 Z Δv, 0.3 s grounded cooldown (pass 4 §A1); boost: local (600, 0, 1400) | none (vertical **Ascend / Descend** = hover dash ±Z; PC C / V) | as car | hover sim jump, **cooldown 0.5 s** |
| Special move (PC Shift / pad RB) | hover: **dash** 3000 for 0.5 s along the dominant stick axis, cooldown **2.0 s**; boost: **barrel roll** (1200 sideways, +1000 up, 100 rad/s roll impulse) along sign(strafe), cooldown **2.0 s** | **barrel roll** if \|strafe\| ≥ 0.5, cooldown **1.2 s** (hover roll 0.6 s @3000; flying 0.8 s @3000, 8 rad/s) | hover: dash (truck form); boost: **Nitro** ×1.5 speed, steering ×0.3 for 3 s, cooldown 8 s, RamFX (truck `RollDuration` 0, so **no barrel roll**) | **quick-turn 180°** (below), cooldown **1.2 s** |
| Turning | hover: body yaw driven to camera yaw (mask (0.05, 0.05, 1)); boost: front-wheel steering, steer = sign(s)·s² | hover: same yaw drive; flying: `PlaneSimulation` pitch / yaw / roll from input | as car | **hull yaw snaps to camera yaw every step** (TurnRate (0.05, 0.05, 1), no rate cap) |
| Self-righting | full upright only when airborne or upside down (pass 4 §A4) | hover: same; flying: plane sim | as car | `IsStable` = \|pitch\|, \|roll\| < 30°; if stable and grounded, yaw only; else 5 % pitch / roll pull |
| Leave boost | release, or head-on wall hit (cos 0.866) | release, or crash ContactSpeed > **3000** | as car | release; firing the cannon also stops boost |

## 5. Tank "rapid 360" (GP) (C)

**Trigger:**
- `PlayerInTankForm.StartVehicleSpecialMove`: if `CanUseSpecialMove`, set `TnCamera.RecenterCamera = true` → `TankForm.OnSpecialMove`.
- That starts the **1.2 s** cooldown (`TimeBetween180s`) and plays `PlayOneEightySound`.
- Binding: PC **LeftShift / RightShift** (`Ability0 | VehicleSpecialMove`), pad RB.

**Camera:** every tank CAMSET driving strategy has `TnQuickTurnCameraBehavior` (`_Duration` **0.3 s**).
- On ResetCamera with no turn active, the target = **tank rotation + 180° yaw**.
- The orbit rotation is lerped to it linearly over 0.3 s.

**Hull:** `TnHoverTankSimulation.UpdateTurn` drives hull yaw to camera yaw every physics step, so the **hull spins 180° in 0.3 s**.

**So:**
- The authentic quick-turn is **180°, not 360°**. One per press, at most one per 1.2 s.
- Because the hull is slaved to camera yaw with no rate limit, **a fast mouse flick also spins the tank at the same speed in the original**. Continuous 360° spinning comes only from mouse input.
- If the rebuild spins 360° per press, or repeats while the key is held, that is not original. The trigger is press-edge (`StartVehicleSpecialMove`) and gated by the cooldown.

## 6. Authored effect relationships (RD / SY)

### 6a. Vehicle FX (C: blueprint data + form scripts)

| Archetype | HoverFX (sockets → template) | BoostFx | JumpFX | Other |
|---|---|---|---|---|
| Car (Sideswipe) | Hover_LB/RB/LF/RF → `CarHover_A_01_FX` | BoostSocket_C/R/L → `Booster_1_FX` | JumpBoostSocket_C/L/R → `CarJump_Small_FX` | — |
| Jet (AirRaid) | Hover_F/L/R/RightSide/LeftSide → `hover_plane_FX` | BoostSocket_L/R → `Afterburner_A_FX`; WingTip_L/R + VaporTrail_L/R → `FX.Trails_Jet_A_FX` | — | `WingDeathExplosionFXTemplate` `TF_Plane_Death_FX` |
| Truck (Ironhide) | 4× `CarHover_A_01_FX` | BoostSocket_L/R → `Afterburner_A_FX` | 3× `CarJump_01_FX` | **RamFX** RamSocket → `FX.Truck_ram_FX` (Nitro start → stop) |
| Tank (Warpath) | Hover_RF/RB/LF/LB → `hover_tank01_FX`, Hover_C → `hover_tank_02_FX` | BoostSocket_R/L → `Afterburner_A_FX` | Hover_* → `Jump_tank01_FX` | — |

**Parameters:**
- **Car and truck hover**: vector 'Size' = min(1, thruster linear + angular contribution) × socket RelativeScale (smoothing VLerp 0.1).
- **Jet hover**: the same, with **VLerp 0.3**, constants 3000 / 6.
- **Tank hover**: **no parameters**. The FX play constantly while `FxAllowed`.
- **Boost**:
  - car / truck Driving: 'Color' lerps EnergonColor → Yellow, alpha 100→255 by jump time;
  - jet Flying: play / stop only;
  - tank: plays while `IsBoosting`.
- The consumer of 'Size' is `ParticleModuleSizeMultiplyLife` (pass 4 E addendum).

### 6b. Weapons and projectiles (C: `notes/data/*_effect_bindings.json`)

**Spawning (C, `HmProjectile`):**
- `Init` → `ClientSpawnFlightEffect`: a ParticleSystemComponent with `PROJMESH.FlightEffect` is **attached to the projectile actor**, so it moves and rotates with it, plus a looping `FlightSound`.
- `UpdateMesh` sets the StaticMeshComponent mesh **only if `PROJMESH.StaticMesh` is set**.
- `Explode` → `SpawnExplosionEffect`: `EmitterPool.SpawnEmitter(ExplosionEffect, HitLocation, rotator(HitNormal))` + ExplosionSound. The flight sound fades out over 0.25 s.
- `Destroyed` without a hit explodes at its location with normal = −forward.
- **Most MP projectiles have no static mesh. Their visible body is the flight particle system.** A cube or box means the rebuild is drawing a placeholder where the original draws only the flight FX:

| Weapon (MP) | Fire | Muzzle FX (socket) | Tracer / flight FX | Impact / explosion | Static mesh |
|---|---|---|---|---|---|
| **Null Ray** `TnWeaponSniperRifle` | **instant hit, not a projectile** | `FX_Sniper_p.FX.MuzzleFlash_Sniper_FX` (MuzzleFlash) + muzzle light | tracer `FX_Sniper_p.FX.Tracer_SniperRifle_FX` | squib `FX_AssaultRifle_p.FX.Impact_AssaultRifle_FX` | — |
| **Magma Frag Launcher** `TnWeaponGrenadeLauncher` | projectile `TnProjectileGrenadeLauncher` (MP PROJDATA: speed 35000, gravity ×0.3, bounce 0.6, **fuse 15 s**, 145 dmg / r1500; fine-aim button **remote-detonates**) | `MuzzleFlash_GrenadeLauncher_FX` | flight `FX_GrenadeLauncher_p.FX.Tracer_GrenadeLauncher_FX`, loop `TRAIL_LP` | `Explosion_GrenadeLauncher_01_FX`; bounce `GRENADE_FOLEY_SHELL_BOUNCE_HEAVY` | **none** (cylinder r50 / h50 collision) |
| Fusion Cannon `TnWeaponBazooka` | `TnProjectileBazooka` 16000 | `Muzzleflash_FusionCannon_FX` | `FX_FusionCannon_p.FX.Trail_FusionCannon_FX` | `Exp_FusionCannon_FX` | none |
| Thermo Rocket Launcher | `TnProjectileHomingRocket` 9000 | `MuzzleFlash_HomRocket_FX` | `Tracer_HomRocket_FX` | `Squib_HomRocket_01_FX` | none |
| Plasma Cannon | Charge1 / 2 / 3 projectiles (8000 / 15000 / 23000) | `PowerUp_PlasmaCannon_FX` + `MuzzleFlash_PlasmaCannon_FX` | `Trail_PlasmaCannon_Sm / Med / Lrg_FX` | `Squib_PlasmaCannon_Sm / Med / Lrg_FX` | none |
| Tank cannon `TnWeaponTankCannon` | `TnProjectileTankShell` 20000 | `D_MuzzleFlash_TankCannon_FX` (WeaponSocket_Primary) | tracer + flight `Trail_TankCannon_FX` | `FX_Explosives_p.FX.Martyrdom_Grenade_FX` | none |
| Jet / car rockets `TnWeaponRocketVehicle` / `RocketPlane` | `TnProjectilePlaneRocketTemp` 18000 | `MuzzleFlash_Blaster_FX` (WeaponSocket_Primary / Primary2, alternating) | `Tracer_HomRocket_FX` | `Squib_HomRocket_01_FX` | none |
| Homing rocket vehicle | `TnProjectileHomingRocketVehicle` 10000 | `MuzzleFlash_HomRocket_FX` (Primary / Primary2) | `Tracer_HomRocket_FX` | `Squib_HomRocket_01_FX` | none |
| Vehicle MG (`AssaultRifleVehicle` / `Plane`) | instant hit | `MuzzleFlash_AssaultRifle_FX` (Primary / Primary2) | `Tracer_AssaultRifle_FX` | — | — |
| Heavy rocket turret / RocketTurret streak | `TnProjectileMangaRocketTurret` 12000 | `MuzzleFlash_TurretIon_FX` | `Trail_PlasmaCannon_Lrg_FX` | `Squib_PlasmaCannon_Lrg_FX` | none |
| Flak grenade | `TnProjectileGrenade` | — | `A_Plasma_Trail_FX` | `Explosion_GrenadeLauncher_01_FX` | `WEP_Grenade_Flak_STAT` |
| EMP (Flashbang) grenade | `TnProjectileFlashBang` | — | `Flashbang_Trail_FX` | `Exp_Energy_MED_FX` | `WEP_Grenade_Flashbang_STAT` |
| Heal grenade | `TnProjectileHealGrenade` | — | `HealGrenade_Trail_FX` | `Squib_HealGrenade_FX` | `WEP_Grenade_Heal_STAT` |
| Kamikaze mine | `TnProjectileKamikazeMine` 2500 | — | `Trail_KamikazeMine_FX` | `Exp_2500cb_FX` | none (mine-specific mesh not in PROJMESH: **P**) |
| AbilityJammer | `TnProjectileAbilityJammer` 10000 | — | `Trail_PlasmaCannon_Lrg_FX` | `FX_Multiplayer_p.FX.WarCry_AOE_FX` | none |

**Sockets (C):**
- Vehicle weapons list `MuzzleFlashSockets` (`WeaponSocket_Primary`, `WeaponSocket_Primary2`) on the vehicle mesh. `TnVehicleFormBlueprint.WeaponSockets` / `RequiredSockets` = `WeaponSocket_Primary`.
- Robot weapons use the weapon mesh's `MuzzleFlash` socket (HeavyMG uses `MuzzleFlash_1/2/3`; grenades use `MuzzleFlash_R/L`).
- **P:** Primary vs Primary2 alternation per shot is not traced (H: round-robin).

## 7. Scout transform intermediate frame (RD / GP)

**Notifies (C), Sideswipe (Car2):**

| Clip | Length | Notifies |
|---|---|---|
| ROBO `Transform_ToVehicle_ROBO` | 1.7 s / 51 f | Show @0, sound @0.0037, **Hide @0.4143** |
| VEH `Transform_ToVehicle_VEH` | 1.7 s | Hide @0, **Show @0.3508**, wheels-land sound @0.7275, ToggleVehicleFx(enable) @1.47 |
| ROBO `Transform_ToRobot_ROBO` | 1.0 s / 30 f | **Show @0.0**, sound @0.01, land footstep @0.70 |
| VEH `Transform_ToRobot_VEH` | 1.0 s | DisableFx @0, Show @0, **Hide @0.2789** |

**Barricade (Car4):**
- R→V: robot Hide @0.8487, vehicle Show @0.7049 (2.0 s clips).
- V→R: robot Show @0.394, vehicle Hide @0.6663 (1.0333 s).

**Sequencing (C, `TnTransformation.Execute`):**
1. Source form `EndPlay`; target form `Activate`.
2. The **source** clip is enqueued with **BlendIn 0.115 s** (from the current locomotion pose).
3. The **target** clip with **BlendIn 0** and **BlendOut 0.25 s**.
4. RootMotionMode 2, Priority 1, Override 2, Rate 1 (4 if downed).
5. Duration = min(source length, target length) / Rate. On completion: source `Deactivate`, target `BeginPlay`.

**Implications:**
- In V→R the **robot mesh must appear on the very first frame already posed at frame 0 of `Transform_ToRobot_ROBO`**. That is the folded shape, with no blend from idle, because target blend-in is 0.
- Sideswipe's robot clip has **only a t = 0 Show**. Two rebuild behaviours would produce a "strange frame":
  - **Not firing notifies at exactly t = 0:** the robot stays hidden for the whole transform and pops in at the end.
  - **Showing the robot before its clip is applied:** one frame of idle or bind pose.
- In R→V, the robot clip blends in over 0.115 s from the current pose (legitimate). The vehicle appears only at 0.3508 s, again with no blend.
- At the end the robot clip blends **out** over 0.25 s into locomotion. A hard snap here is another candidate.

**Verdict:**
- H: the authored data is consistent and contains no odd frame, so the strange frame is **runtime sequencing**: notify edge handling at t = 0, blend-in on the target clip, or mesh visibility before the first pose.
- P: the clip bone keys were not inspected frame-by-frame for an authored glitch.

## 8. Molten floor / lava and Orbital Debris sky (RD)

**Molten (C, materials):**
- **`MoltenFloorBurn_MAT`** (floor, 22 components) is **not glowing lava**. It is a lit metal floor:
  - Diffuse = pow(TextureSet colour, 1.3) + 5 × (`ENV_Metals_CUBEMAP`(reflection) × 0.005 × (1 − TextureSet.R));
  - Emissive = the cubemap term only (×0.005 × (1 − R));
  - specular = TextureSet × mask.G × 10, power 15;
  - the normal comes from the TextureSet (UV ×0.35).
  - The heat look comes from lighting, fog sheets and FX, not from floor emissive.
- **Lava falls**: `LavaFall1_MATINST` → `LavaFall_Parent_MAT`:
  - **Additive, Unlit, distortion**;
  - two panned `WaterFall_CLR` layers (speeds (0.01, −0.2) and (−0.008, −0.5) × Speed 0.25, Scale 1.3), summed ×0.65, then pow 5;
  - + 4 × ReflectionColor (1, 0.263, 0.048) × 0.5 × Brightness 1.5 × `IaconCity_Cubemap`;
  - opacity = DepthBiasedAlpha (bias 300) × VertexColor;
  - distortion = VertexColor × 20 × panned normals.
- Also present:
  - `MoltenRain_MatInst` (58), `MoltenRainPuddle_MatInst` (20);
  - fog sheets `FogSheet_LavaRoom / Bright / lessBright`;
  - `LightRays_MATINST`;
  - sky `ENV_KON_StarDome_p.Test.KON_newSky_MAT`: emissive starfield ×400 × panning clouds + `KaonNebula_testColor06_CLR` on UV1.

**Orbital Debris sky (C, `MP_ORB_Art_m`):**
- `ENV_ORB_Spacedome_p.SpaceDome_STATMESH` with component material **`Spacedome_Nebula_MAT`**, bAcceptsLights false, no shadow. Emissive =
  - 400 × (Starfield_CLR rotating at 0.0006 + Starfield ×2 tiling + ×3 tiling)
  - × Cloud_Mask (panner 1e-4 on rotator 0.001)
  - + Cloud_Mask(×0.5 tiling) × 2,
  - all × `Nebula_01_CLR` on **UV1**.
- `ENV_ORB_CybertronPlanet_p.MATTE.Cybertron_MATTE_STAT` with component material `Cybertron_2D_Planet_MAT`: **translucent unlit**, emissive `CybertronORBIT_2D_EMISS`, opacity `CybertronORBIT_2D_MASK`, no lights, no shadow.
- The haze comes from the map CLUT `MP_OrbitalDebris_CLUT` plus fog (Rendering already has it).

**H:** the star points in both skies need **UV1** for the nebula colour and a ×400 emissive gain. Without UV1 the nebula tint is wrong; without the gain the stars vanish.
