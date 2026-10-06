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

## Addendum: beam emitter module references (H, raw scan of `MP_IAC_Streets_BASE_m`)

**`FX_RepairBeam_p.FX.Tracer_RepairBeam_FX`.** In each beam emitter's LOD blob, the two `TypeDataBeam2` references are followed by module references at a 17-byte stride:
- `ParticleModuleBeamSource`;
- `ParticleModuleBeamTarget` (`PEB2STM_UserSet`, TargetName "TargetLocation");
- `ParticleModuleBeamSineWave`, present on emitters 13998 and 4113 only.

Non-beam LODs reference only their `Required` module.

**Interpretation:**
- These are AssetTools' module_id-0 "PMI_Unknown" entries.
- `ParticleModuleBeamSineWave` is not a stock UE3 class (H: a WFC addition). Its SineWaves data is authored: Amplitude ±25/50 and 10, Period 500, Speed −3000, Direction (1, 0, 0).

**Fine-aim FOV source** (asked again by AssetTools): `TnFovCameraBehavior.FOVsByPCS` in the camera strategy (§3). It is not in the `TnPCS_*` class defaults.

## 9. Beam2 taper / Trail2 tessellation (RD) — native + data

### 9a. Class layouts (C)

Read from the Engine package property chain, with offsets confirmed by native field use.

**`ParticleModuleTypeDataBeam2`:**

| Offset | Field |
|---|---|
| +0x30 | BeamMethod (byte) |
| +0x31 | **TaperMethod** (byte) |
| +0x34 | TextureTile |
| +0x38 | TextureTileDistance |
| +0x3C | Sheets |
| +0x40 | MaxBeamCount |
| +0x44 | Speed |
| +0x48 | **InterpolationPoints** |
| +0x4C | bAlwaysOn |
| — | BillboardSettings (**WFC addition**) |
| — | BranchParentName |
| +0x58 | Distance |
| +0x6C | **TaperFactor** |
| +0x80 | **TaperScale** |

Distributions are 0x14 bytes each.

**`ParticleModuleTypeDataTrail2`:**

| Offset | Field |
|---|---|
| +0x30 | **TessellationFactor** |
| +0x34 | **TessellationFactorDistance** |
| +0x38 | **TessellationStrength** |
| +0x3C | TextureTile |
| +0x40 | bits: bTilePerParticle, bEmitterXAxisOrientation, bEmitOnlyWhenMoving, bConnectToSource |
| +0x44 | Sheets |
| +0x48 | MaxTrailCount |
| +0x4C | MaxParticleInTrailCount |
| — | BillboardSettings (WFC) |

### 9b. Beam taper (C, native)

**`Function_8302E898`** = Beam2 TypeData Spawn, run **once per particle at spawn**:
- No source module: source = component location, plus a direction vector at component +0x50.
- No target module and no user target: target = source + normalise(dir) × `Distance`. The distribution is evaluated at the particle's RelativeTime.
- **If TaperMethod != 0:**
  - `TaperCount` = max(InterpolationPoints, Noise.Frequency) + 1 (`FUN_83014348`). The taper array lives in the particle payload at TypeDataOffset + 0x68 + 12 × InterpolationPoints.
  - For i = 0 … TaperCount − 1: r = i / (TaperCount − 1), and **`TaperValues[i] = TaperFactor(r) × TaperScale(r)`**. Both distributions are evaluated at the ratio along the beam, not over time.
  - Index 0 is the source end; the last index is the target end.

So taper is a per-point width multiplier along the beam, fixed at spawn. PEBTM_Full and PEBTM_Partial are treated identically here. **H:** the renderer multiplies the particle size at interpolated point i by `TaperValues[i]` (stock UE3).

**Beam module binding:** `Function_830504B0`.
- The type checks run in this order: source → +0x144; target → +0x148; noise → +0x14C; modifier (byte +0x30: 0 = source modifier +0x150, 1 = target modifier +0x154).
- **`BeamSineWave`**: each SineWaves entry (0x1C bytes: Amplitude, Period, Speed, PhaseOffset, Direction xyz) is appended to the instance array at +0x1C0.
- **FillReplayData** (`Function_83045800`) copies to replay data:
  - that array → replay +0x13C;
  - Sheets (min 1) → +0x100;
  - TextureTile → +0x12C;
  - TextureTileDistance → +0x130;
  - TaperMethod → +0x134;
  - noise settings → +0xE4…+0x128.
  - Replay vertex count per beam = 2 + Sheets × Steps (+4 per extra beam).
- **U:** the render-thread sine formula. H: displacement = Σ Amplitude × sin(2π·d / Period + Speed·t + PhaseOffset) × Direction, in beam space.

### 9c. Trail2 tessellation (C, native)

**FillReplayData** (`Function_83035770`) copies:

| Replay offset | Value |
|---|---|
| +0xB0 | TessellationFactor (**0 → 1**) |
| +0xB4 | TessellationStrength |
| +0xB8 | TessellationFactorDistance |
| +0xAC | Sheets (0 → 1) |
| +0xA2 | source-particle offset, only when the TrailSource module's SourceMethod byte == 1 |

**Vertex / triangle count** (`Function_83019600`), for each trail (head particle) walked through the linked list:
- the trail start adds 2 vertices;
- **each segment between consecutive trail particles adds Sheets × TessellationFactor × 2 vertices**;
- the segment from the head back to the source is included unless the bConnectToSource bit differs;
- triangles per trail = (vertices − 2) plus 4 per sheet for joins, and 4 × trails − 6 overall;
- the trail particle count is clamped so the total stays under the vertex buffer limit `DAT_837188E0`.

So **tessellation is a fixed count per segment, `TessellationFactor`**. `TessellationFactorDistance` is copied but does **not** affect the vertex count in this build (H: unused for geometry). No MP effect authors it anyway.

**H (stock UE3), not decoded natively:**
- interpolated points use Hermite / CubicInterp between trail particles, with tangents scaled by `TessellationStrength` (default 1.0);
- size and colour are lerped per step.

### 9d. Authored values for MP effects (C, `authored.db`; full dump in `notes/data/beam_trail_params.txt`)

**Beams** (`Tracer_RepairBeam_FX`, `DrainRay_Beam_FX`; 3 beam emitters × 2 LODs). All have:
- BeamMethod Target (CDO);
- **TaperMethod PEBTM_Full**;
- **InterpolationPoints 50**;
- Sheets 1, TextureTile 1, MaxBeamCount 1, Speed 0.

The emitters differ:
- **Core**: TaperScale curve 0 → 1 over the first half, then 1 → 0.5 or held at 1; TaperFactor CDO 1.
- **Electric**: TaperFactor **10** × TaperScale ramp 0.025 → ~1.05 (or decaying 0.025 → 0).
- SineWaves on two of the three emitters: three waves with Period 500, Speed −3000 / 0 / −2500, Amplitude ±25/50, ±10, ±100, Direction X, −0.5X, 0.5Y.

`Squib_RepairEnemy_FX`: PEBTM_Full, 50 points, Speed 1000, Distance 100, TaperFactor curve, plus BeamNoise (low-frequency, Frequency 10).

**Trails:**

| Effect | TessellationFactor | Other |
|---|---|---|
| Sniper (Null Ray) tracer | **10** | bConnectToSource **false** |
| AssaultRifle / IonBlaster tracer | **5** | bConnectToSource false, bEmitOnlyWhenMoving false |
| EMP Shotgun | 10 | — |
| Homing rocket | 5 | — |
| Grenade Launcher | 5 | — |
| Kamikaze mine | 5 | — |
| A_Plasma_Trail (flak) | 5 | — |
| Plasma Lrg | 3 | — |
| Jet wingtip trails | 3 | — |
| Fusion Cannon, Tank Cannon | CDO 1 | — |

For all of these, TessellationStrength = CDO **1.0**, TessellationFactorDistance = **0**, MaxParticleInTrailCount 100.

### 9e. BeamSineWave render formula — trace status (2026-10-05)

**What is C:**
- The SineWaves data is bound at init (`Function_830504B0` → instance +0x1C0, 0x1C-byte records).
- It is copied every frame into the beam replay data at +0x13C/+0x140 (`Function_83045800`).

**What is not found (U):**
- **No native reader of that array has been located.** Searched:
  - every non-stack `lwz` of the replay offsets, at base offsets 0…0x200;
  - every 0x1C-stride float-record loop (`addi 0x1C` / `mulli 28`);
  - every reference to the trig constants (2π, 1/2π, sine-polynomial coefficients) in engine code.
- None reaches the array.
- The consumer is not on the game thread: `UParticleModuleTypeDataBeam2::Update` (`0x8302EAD0`, below) has no sine term.

**Remaining hypotheses (H/U):**
- the render-thread beam fill reads it through VMX / indexed loads that the displacement scans cannot see;
- or the data is copied but never used in this build.

**Until it is traced:** d, t, Speed, Period and the beam-space axes stay **U**. Rendering should keep its implementation labelled **H** (Σ A·sin(2π·d/Period + Speed·t + Phase)·Direction).

### 9f. `UParticleModuleTypeDataBeam2::Update` (C, `0x8302EAD0`; vtable `0x82338BD8` +0x134, Spawn at +0x130)

Runs per particle every tick:

1. **Source:** with no source module, source = component location and direction (or the origin plus +X in local space).
2. **Target:** with no target module and no user target, target = source + normalise(dir) × `Distance` (evaluated at RelativeTime).
3. **Beam travel:** if `Speed` (TypeData +0x44) == 0, or the beam has already reached its target, the beam end = target. Otherwise the end moves toward the target at **Speed × dt** per tick and snaps once within range.
4. **Direction:** direction = normalise(target − source); length = |target − source|.
5. **Noise step count** (`BeamNoise` bound):
   - steps = `Frequency` (from the payload flags);
   - if `FrequencyDistance` (noise +0x9C) > 0: steps = min(Frequency, int(length / FrequencyDistance));
   - if the `bApplyNoiseScale` bit (noise +0x30 & 0x800000) is set, the payload noise scale = `NoiseScale`(steps / Frequency) (noise +0xA0).
   - With no noise, steps = `InterpolationPoints` (instance +0x48).
6. **Step size:** step size = length / steps.
7. **While travelling:** the rendered step count = ceil(travelled / length × steps), at least 1, plus the fractional last step.
8. **Triangles:** = steps × 2 × (NoiseTessellation if > 0).

This matches stock UE3. The noise point generation itself (NoiseRange, NoiseSpeed, NoiseLockTime, tension) was not traced in this pass; H: stock.

### 9g. Vehicle weapon muzzle socket alternation (C, script; answered to Rendering and Gameplay)

**Sockets:**
- The vehicle form `WeaponSockets` is the CDO default ["WeaponSocket_Primary"], so each weapon has one mesh.
- The WEPMESH `MuzzleFlashSockets` = [Primary, Primary2] for the vehicle MG, rockets, homing rockets and the plane MG / rockets.

**Advance:**
- `HmWeapon.OnPlayFireEffects` plays the flash and tracer at `CurrentSocket`, then `HmWeaponMesh.ChangeSocket` advances it ((i + 1) % N).
- This runs **once per shot**, via IncrementFlashCount → Pawn.WeaponFired.

**Projectile start:**
- `Weapon.ProjectileFire` takes RealStartLoc = `GetMuzzleLoc()` (the current socket) **before** the effects advance it, then aims toward the camera-trace hit point.
- So a projectile and its flash share a socket, and consecutive shots alternate L/R.
- The instant-hit MG traces from the pawn's start-trace location; only its flash and tracer alternate.

### 9h. BeamNoise point generation (C, native) + correction to 9f

**Layout:** `ParticleModuleBeamNoise` is 0xB4 bytes. The offsets were checked against native use.

| Offset | Field |
|---|---|
| +0x30 | flag bits, MSB first: bLowFreq_Enabled 0x80000000, bNRScaleEmitterTime 0x40000000, **bSmooth 0x20000000**, bNoiseLock 0x10000000, bOscillate 0x08000000, bUseNoiseTangents 0x04000000, bSourceNoise 0x02000000, bTargetNoise 0x01000000, **bApplyNoiseScale 0x00800000** |
| +0x34 | **Frequency** |
| +0x38 | **Frequency_LowRange** |
| +0x3C | **NoiseRange** (vector distribution) |
| +0x50 | NoiseRangeScale |
| +0x64 | NoiseSpeed (vector) |
| +0x78 | NoiseLockRadius |
| +0x7C | **NoiseLockTime** |
| +0x80 | NoiseTension |
| +0x84 | NoiseTangentStrength |
| +0x98 | NoiseTessellation |
| +0x9C | **FrequencyDistance** |
| +0xA0 | **NoiseScale** |

**Vtable:** `0x82338F98`. Spawn = **`0x8301F6F8`**, Update = **`0x8301F928`**.

**Spawn (per particle; skipped if Frequency == 0):**
- N = Frequency. If Frequency_LowRange > 0: N = int(r × (Frequency − LowRange) + LowRange), where r is the next **`appSRand`** value. The LCG is GSRandSeed = seed × 0x0BB38435 + 0x3619636B, so stock UE3 appSRand.
- N is stored in the payload flag bits 12–23.
- **N + 1 noise points.** Point[i] = **NoiseRange.GetValue(i / (N + 1))**, a vector-distribution evaluation, i = 0…N. For a uniform or uniform-curve distribution this draws randomly within the range at that ratio along the beam.
- If **bSmooth**: the same values are also written to a second (target) point array.

**Update (per particle, every tick):**
- **NoiseLockTime < 0:** points never change (locked).
- **NoiseLockTime ≤ KINDA_SMALL:** all N + 1 points are re-drawn from NoiseRange(i / (N + 1)) every tick.
- **NoiseLockTime > 0:** the payload timer += dt. When it exceeds NoiseLockTime, the points are re-drawn and the timer resets to 0. With bSmooth, the new draw goes into the **target** array; the render side moves the current points toward it.
- **NoiseSpeed is not used on the game thread** (H: render-side smoothing toward the target points).
- **U:** the render-side use (frame of the NoiseRange offsets, NoiseSpeed smoothing, tension / tangent spline, NoiseTessellation sub-steps).

**Correction to 9f — noise scale.** Read again from `0x8302EAD0`, it is computed **once per beam per tick**, not per point:
- if bApplyNoiseScale is **clear**: no scale is stored;
- if **FrequencyDistance ≤ 0**: payload noise scale = **1.0**, and the NoiseScale curve is **ignored**;
- if FrequencyDistance > 0: steps = min(N, int(length / FrequencyDistance)), and scale = **NoiseScale(steps / N)**.

So every authored noisy beam (none sets FrequencyDistance) renders with **noise scale 1.0**.

### 9i. Render-side beam fill: noise + BeamSineWave (C unless marked)

**Locating it:**
- The render fill is **`0x830298E8`** (5,584 bytes). Ghidra had never defined it as a function, which is why the earlier scans missed it.
- It is called only from `0x83055E88`, a slot in the beam dynamic-data vtable at ~`0x823365CC`, with (`this` = replay data, `r4` = the second argument). The second argument is probably the scene proxy (H).
- It was decompiled in memory with the new read-only `tools/ghidra_scripts/WfcDecompAt.java` (explicit body, no-return cleared, never saved). Raw listings: `work/q/beam_fill_830298e8.dis`, `work/q/beam_fill_830299ac.c`.

**Replay fields used:**

| Offset | Field |
|---|---|
| +0xD8 | noise-module payload offset |
| +0xDA | current noise points |
| +0xDC | target noise points |
| +0xDE | taper values |
| +0xE0 | payload noise scale |
| +0xE4 | bLowFreq_Enabled |
| +0xEC | bSmooth |
| +0xF8 | bSourceNoise |
| +0xFC | bTargetNoise |
| +0x100 | Sheets |
| +0x104 | Frequency |
| +0x108 | NoiseTessellation |
| +0x10C | NoiseRangeScale |
| +0x110 | NoiseTangentStrength |
| +0x114 | NoiseSpeed |
| +0x120 | NoiseLockTime |
| +0x124 | NoiseLockRadius |
| +0x128 | NoiseTension |
| +0x134 | TaperMethod |
| +0x13C | **SineWaves** |

**Per beam, per frame:**

1. Base path points at ratio r_i = i / steps come from `Function_82B5B040`. This is the source → target curve using the payload's source and target tangents × strengths; H: stock CubicInterp.
2. **BeamSineWave** (`0x83029618`, called at every point with r, d = r × |target − source|, and t = particle age = RelativeTime / OneOverMaxLifetime):
   - **Frame:** dir = normalise(lerp(sourceTangent × sourceStrength, targetTangent × targetStrength, r)). A quaternion rotates local **+Z onto dir**: axis = normalise(cross((0,0,1), dir)), angle = acos(clamp(dir.z, −1, 1)).
   - **Sum:** for each wave, `offset += Direction × Amplitude × sin(2π × ((Speed × t + d) / Period + PhaseOffset))`.
     - **Period** is in UU along the beam.
     - **Speed** is in UU/s, so the wave travels along the beam.
     - **PhaseOffset** is in cycles.
     - **d** is the distance from the source in UU.
     - **t** is the particle's age in seconds.
   - **Rotation:** offset' = offset × M(quat), using the UE3 row-vector TransformNormal. So wave **Direction X/Y are perpendicular to the beam, and Z runs along it**.
   - **Endpoint fade:** offset' × min(6r, 1) × min(6(1 − r), 1). It is zero at both ends and full strength over the middle two-thirds.
   - The sine offset is added to every interpolated point; it is skipped when no waves are bound.
3. **Noise** (only when **bLowFreq_Enabled**, the stock noise master switch):
   - **Smoothing** (bSmooth and NoiseLockTime ≥ 0), per noise point each frame:
     - step = normalise(target − current) × **NoiseSpeed (per axis)** × noiseTimer, where noiseTimer is the payload time since the last refresh, in seconds;
     - candidate = current + step;
     - if |step| ≥ NoiseLockRadius, current = candidate; otherwise **current snaps to target**.
   - **Offset** = current point i × payload noise scale (§9h: 1.0 unless FrequencyDistance is set) × **NoiseRangeScale**. It is transformed by the 3×3 rotation of the matrix built from **second argument + 0x20**. H: the proxy's LocalToWorld, i.e. **component/emitter space, not beam-aligned**; reasoned from the call chain, not proven.
   - The **source** point gets noise only if **bSourceNoise**; the **target** point only if **bTargetNoise**. Neither is authored on the MP noisy beams, so both endpoints stay put.
   - **Between noise points:** NoiseTessellation (min 1) sub-steps via the same curve helper. Width is linearly interpolated between point taper values. NoiseTension / NoiseTangentStrength feed the sub-step tangents (H: stock; exact use not decoded).
4. **Width** = particle size × TaperValues[i] (when TaperMethod != 0) × sheet factor. The vertex tangent = normalise(P_i − P_{i−1}).

This supersedes §9e: the BeamSineWave formula is no longer UNKNOWN.

### 9j. Noise curve between noise points: NoiseTension and NoiseTangentStrength (C, raw disassembly of `0x830298E8`)

**Noisy point.** N_i = basePath(r_i) + sine(r_i) + R · (current noise point i × payload noise scale) × NoiseRangeScale. R is the 3×3 rotation described in §9i.

**Tangent at N_i** (raw code at `0x8302A0A8…0x8302A190` for the first point and `0x8302A5F0…0x8302A6F8` per point):
- v = (N_{i+1} − N_{i−1}) × (1 − **NoiseTension**) × **0.5** (the constant 0.5 is at `0x8209DD8C`);
- **v is then normalised**;
- T_i = v̂ × lerp(**SourceStrength**, **TargetStrength**, r_i). These are payload +0x18 and +0x34, the beam source/target tangent strengths.

**Hence:**
- **NoiseTension only scales v before normalisation**, so it has no effect on the curve. The exceptions:
  - Tension = 1 makes v zero; the normalise is skipped (length below epsilon), so T = 0 and the segments are straight.
  - Tension > 1 reverses the tangents.
  - Authored values are 0.5 (CDO) or unset, so tension is effectively irrelevant.
- **NoiseTangentStrength is never read by the render fill.** Replay +0x110 is written by FillReplayData but has no load in `0x830298E8`, the only beam fill. It is effectively unused. The tangent magnitude comes from the beam's source/target strengths instead.

**Sub-steps between N_i and N_{i+1}:**
- NoiseTessellation (min 1) samples, using **`0x82B5B040` = Hermite CubicInterp(P0 = N_i, T0 = T_i, P1 = N_{i+1}, T1 = T_{i+1}, α)**.
- The basis is h00 = 2α³ − 3α² + 1, h10 = α³ − 2α² + α, h01 = −2α³ + 3α², h11 = α³ − α² (standard UE3 CubicInterp).
- α advances by a per-step increment held on the stack (H: 1/NoiseTessellation).
- Width is interpolated linearly between the endpoint taper values. The vertex direction = normalise(current − previous).

## 10. SetAudioGroupVolume — native FMOD path (SY) (C unless marked)

**Call chain:**
1. **Exec:** `execSetAudioGroupVolume` = **`0x82C7E5E8`**. It is registered in `Function_83656C58` (slot `0x83710144`) and calls `0x82BE9D08(volume, GroupName)`.
2. → `GEngine.Client.GetAudioDevice()` → `UFmodAudioDevice` vtable **+0x17C** (`0x82741B90`). The device vtable is `0x820BB4A8`; its constructor is `0x827B4488`, and the class is registered at `0x8278B6A0`.
3. If the device is initialised (+0x128): inner audio object (+0x160; vtable `0x820B3688`, created by device vtable +0x234) → vtable +0x4C = **`0x827666B0`**.

**`0x827666B0` (SetGroupVolume):**
- If the audio system is not initialised: no-op.
- Iterates the group mappings: 16-byte entries {GroupName, CategoryNames data, count}, built from `[HM_Engine.SoundMixerProperties] SoundGroupCategoryMappings`.
- **Match:** `entry.GroupName.index == arg.index`. This is an **FName index compare** (H: case-insensitive, since UE3 FNames share one case-insensitive table, so 'Dialog' == 'DIALOG').
- **GroupName None matches every group.** An unknown group matches nothing, so it is a **no-op**.
- For each CategoryName in the entry: node = categoryTree.Find(name). The tree is a recursive search by FName index (`0x82766148`). Then `node->vfunc+0x20(volume, 0.0)` → `node.fader(+0x40)->SetTarget(volume, time = 0.0)`.

**The fader** (`0x82759490` creates it; vtable `0x820A1C48`):
- {current +0x08, target +0x0C, rate +0x10, remaining +0x14, active +0x04};
- `SetTarget(t, time)` (`0x827560A8`): time ≤ 0 → current = target **immediately**; time > 0 → linear ramp over `time`;
- `Tick` (`0x827560F8`) advances active ramps.
- **So SetAudioGroupVolume is immediate (no ramp).**

**Per category:**
- Each category node (`0x82771920`) gets its own fader, **initialised to the config category `Volume` clamped to [0, 1]**. SetAudioGroupVolume **replaces** that fader's value. It is not a separate multiplier.
- `GetAudioGroupVolume` (`0x827667C8`) returns the first mapped category's fader value, or 1.0 if the group is unknown.

**Hierarchy:**
- Each node's DSP/channel group (+0x50) is attached to its parent node's group at construction. H: FMOD ChannelGroup volumes multiply down the tree, so children of DX_DRY etc. inherit.
- Only the listed categories' faders are written, not their descendants' faders.

**Mixer presets — U:**
- Not traced: whether mixer presets act on this same fader (in which case a preset ramp would overwrite the user volume) or on a separate component.
- H suggestion: presets drive their own ramps; verify before relying on it.

**§10 addendum — mixer presets vs the group fader** (C for the code path; H for audible semantics)

**EnableMixerPreset path:**
- device vtable +0x130 (`0x82742400`) → +0x1DC getter returns the same inner object (+0x160) → vtable +0x24 = **`0x82772778`**;
- it finds the preset and resets its timer (+0x1C = 0);
- it inserts the preset into the active list **sorted by Priority** (+0x04);
- it calls `categoryTree->vfunc+0x1C(activeList)` = **`0x8276A868`**, then fires an optional callback.

**`0x8276A868`, per category node, recursive:**
- `0x827661C8` blends the active presets. When it applies, each node's **DSP effect slots** (+0x54 … +0x80) are reset and re-set through their vtable +0x18. The DSP preset properties include Reverb, Echo, EQ, FastEQ, Compressor, Distortion, Flange, FastLowPass, LowPass, HighPass, Pitch and **Volume**.
- It then recurses into the children.

**It never touches the category's +0x40 fader** that SetAudioGroupVolume writes.

**Conclusion:**
- Preset volume is a **separate DSP stage** that multiplies with the user fader (H for audible semantics).
- A preset cannot overwrite the slider value, and the slider does not cancel a preset.

**§9j addendum — sub-step α (C, raw `0x830298E8`):**
- **T** = replay NoiseTessellation (+0x108); **0 → 1** (`0x83029964…0x83029974`).
- **Increment** = **1.0 / T**, computed once per beam fill and stored at 0x1D4(r1) (`0x830299A0`).
- **T ≤ 1:** the Hermite sub-step loop is **skipped** (`0x8302A760` → `0x8302AA70`). Consecutive noise points are joined directly by one segment.
- **T ≥ 2:** α starts at **0.0**. The noise point N_i itself is emitted beforehand at α = 0. The loop then runs **T times** (counter r30, `subic.`/`bne` at `0x8302AA58`); **α += 1/T before each sample**, so the samples fall at **α = 1/T, 2/T, …, T/T = 1**. The last sample coincides with N_{i+1}.
- **Each sample:** CubicInterp(N_i, T_i, N_{i+1}, T_{i+1}, α). It emits 2 vertices (one per sheet side). Width = lerp(taper_i, taper_{i+1}, α).
- **V coordinate:** a running texture coordinate (stack +0x80 increment) advances per sample.

## 11. Beam2 source / target resolution (RE) (C unless marked)

**Code:**
- ResolveSourceData **`0x8302F320`**, ResolveTargetData **`0x8302F738`**.
- Callers:
  - source module Spawn `0x83040578` (spawning = 1; beam index = ActiveParticles at spawn) and Update `0x83040620`;
  - target module Spawn `0x83040888` and Update `0x830408F8`;
  - also `0x83045800`.
- Update runs every tick for every active beam. The beam index is its active slot, and spawning = 0. The source Update is skipped entirely when bLockSource, bLockSourceTangent and bLockSourceStength are all set.
- Lazy name resolvers: `0x8301D6B0` (source) and `0x8301D7A0` (target). Each resolves once and caches the result:
  - Emitter / Particle methods: the emitter instance in the same component whose `EmitterName == Name`;
  - Actor method: the Actor from the component InstanceParameters entry with `Name == Name` (36-byte FParticleSysParam).

**Enums (Engine package):**
- Beam2SourceTargetMethod: Default 0, UserSet 1, Emitter 2, Particle 3, Actor 4.
- TangentMethod: Direct 0, UserSet 1, Distribution 2, Emitter 3.
- EBeam2Method: Distance 0, Target 1, Branch 2. The CDO default is **PEB2M_Target**.
- Module layout:
  - +0x30 method, +0x31 tangent method, +0x34 name;
  - Source: bits at +0x38 (0x80000000 bAbsolute, 0x40000000 bLock, 0x20000000 bLockTangent, 0x10000000 bLockStrength); Source distribution +0x3C, Tangent +0x50, Strength +0x64;
  - Target: Target distribution +0x38, bits at +0x4C (same order), Tangent +0x50, Strength +0x64.
- CDO defaults: Source/Target (50, 50, 50); tangents (1, 0, 0); strengths 25.

### Point: Source

| Method | Result |
|---|---|
| **Default** | `Source` distribution at the instance time `+0xD4` (H: EmitterTime, not particle RelativeTime). If !bSourceAbsolute it gets the **full component LocalToWorld** (offset in component space); otherwise it is used as-is. |
| **UserSet** | `UserSetSourceArray[beamIndex]`; if beamIndex ≥ count, `[0]`; an **empty array → the Default path**. The name is ignored. |
| **Emitter** | This emitter instance's `+0x70` (H: FParticleEmitterInstance::Location = the component's world origin). SourceName is ignored. |
| **Particle** | **No particle is ever read.** Only when TypeData BeamMethod == **Branch**: the named emitter instance's Component LocalToWorld origin. Otherwise (or if the name is unresolved) → the Default path. |
| **Actor** | The InstanceParameter actor → `Actor->vfunc+0x1D0()` matrix row 3 (H: LocalToWorld origin ≈ Location). Unresolved → the Default path. |

**Particle sources in practice:** every authored Particle source ('Orbit2' ×18, 'Orbit3' ×6) is in a system with the default BeamMethod Target. Those systems are Squib_RepairEnemy / Squib_TurretRepairEnemy, MuzzleFlash_DeathBeam, Starscream_Reveal and Hologram_startup. All of them therefore **use their Source distribution** (Default path).

### Point: Target

- **Distance mode first.** If `inst+0x174 ≥ 0` (H: SetBeamDistance override; default < 0) **or BeamMethod == Distance**:
  - Target = Source + normalize(component X axis) × d;
  - d = override, else `TypeData.Distance` at particle RelativeTime; |d| < ε → constant;
  - the method is ignored.
- **Otherwise:**

| Method | Result |
|---|---|
| **Default** | **WFC extension:** if TargetName ≠ None, the component InstanceParameter with that name is used. **Vector** → that point, absolute world (no transform). **Scalar** → component origin + X axis × value. No match → `Target` distribution at `+0xD4`, full LocalToWorld unless bTargetAbsolute. |
| **UserSet** | `UserSetTargetArray[beamIndex]` or `[0]`; **empty → the Default distribution path** (the instance-parameter lookup is not reached). **TargetName is not consulted.** |
| **Emitter** | Requires TargetName; that emitter instance's `+0x70`. **No name → the Target distribution.** |
| **Particle** | **Unsupported** → always the Target distribution (e.g. TF_Death_Buildup 'ZapGlow' uses its Target curve). |
| **Actor** | As for the source. |

### Tangents and strength (both ends)

| Tangent method | Result |
|---|---|
| **Direct** and **Emitter** | The **component LocalToWorld X axis** (row 0, unnormalised). Direct is *not* (target − source) in this resolver. |
| **UserSet** | Per-index array; empty → the Tangent distribution at particle **RelativeTime**, then **rotated** by LocalToWorld (no translation) unless bAbsolute. |
| **Distribution** | Tangent distribution at RelativeTime, **never transformed**, whatever bAbsolute is. |

- **Strength:** if the tangent method is UserSet and the strength array is non-empty → the array; else the Strength distribution at RelativeTime.

### Locks (re-evaluation when not spawning)

| Field | Re-evaluated each tick when |
|---|---|
| Position | !bLock |
| Tangent | !bLockTangent |
| Target strength | !bLockTargetStength |
| **Source strength** | **bLockSourceStength is TRUE** (inverted; raw `0x8302F6C4`: `rlwinm …,3,3; beq skip`) |

- With the default (false), the source strength is evaluated **only at spawn**.
- LockRadius is not read here.

### Who fills the UserSet arrays

| Native | Native implementation | Writes |
|---|---|---|
| `SetBeamSourcePoint` | `0x83041E58` | source array |
| `SetBeamTargetPoint` | `0x83042110` → `0x83039748` | target array |
| `SetBeamEndPoint` | `0x83041DE0` → `0x83039548` | `UserSetTargetArray[0]` |

- Native callers other than the execs:
  - SetBeamSourcePoint / SetBeamTargetPoint: none;
  - SetBeamEndPoint: `0x8295B1F8` (a weapon beam PSC at +0x918, called from `0x829627E0`).
- Script: only `TnAiPawn._LaserSightPSC.SetBeamEndPoint`.
- **SetVectorParameter('TargetLocation') does not feed UserSet targets.** Only a Default target with that TargetName reads it.
- **Shockwave_Melee_FX** (source UserSet, no caller found → U for the TransContent scripts that weren't dumped):
  - empty array → Source (0, 0, 0) → component origin;
  - target Emitter with no name → uniform box ±200 in component space;
  - TargetTangent UserSet → empty → uniform (−1…1) at RelativeTime, rotated;
  - strengths uniform 150–300, source strength at spawn only.

## 12. Ability and buff sound semantics (SY) (C from script/CDO unless marked)

`Actor.PlaySound(Cue, bNotReplicated, bNoRepToOwner, bStopWhenOwnerDestroyed, …)` and `CreateAudioComponent(Cue, bPlay, bStopWhenOwnerDestroyed, …)` are the stock UE3 signatures.

### TnAbility.OnTriggerSound

- Played in **`TnAbility.ServerTriggerAbility`** (offset 0x0008) as `OwnerPawn.PlaySound(OnTriggerSound, false, false, false)`. This is **replicated to all relevant clients including the owner**, and positional at the pawn.
- `LocalTriggerAbility` plays nothing.
- **Gating:**
  - The client's `TnAbilityManager.TriggerAbility` must pass spam cooldown, availability (resource/cooldown) and `Ability.LocalTriggerAbility()` before it RPCs `ServerTriggerAbility`.
  - The server manager returns if the pawn is dead or dying.
  - Subclass `ServerTriggerAbility`s do their work and call the base **last**. Their early returns therefore skip the sound: SpawnProjectile (no Controller), SpawnInventory (no pawn).
  - Barrier and LargeExplosive call the base first.
  - **A refused trigger plays no sound.**
- The base also fires `AbilityStimulusType` and `AnnouncementMessageType`.

### TnBuff ApplySound / UnapplySound

- **`TnBuff.Apply`:**
  - If ApplySound is set, there is no existing component, and `CanPlaySounds()`: `ApplyAudioComponent = OwnerPawn.CreateAudioComponent(ApplySound, bPlay = true, bStopWhenOwnerDestroyed = true)`.
  - It is **attached to the buffed pawn** (positional), local to the machine running Apply, and **loops for the buff's life**.
- **`ReApply`** (same class re-added, level ≥ current) calls Apply, but the component already exists, so there is no restart.
- **`Unapply`:** StopEffectsAndSounds (stops the component) → if CanPlaySounds: `OwnerPawn.PlaySound(UnapplySound, bNotReplicated = true)` (local, positional).
- **`OwnerDied`:** stops the sound, and **no Unapply sound** plays.
- **`CanPlaySounds`** = `!OnlyPlaySoundOnLocalPlayer || (OwnerController != none && OwnerController.IsLocalPlayerController())`. So with the flag set, the sound plays only on the buffed player's own machine; remote pawns have no Controller on clients.
- **Default flags:**
  - `TnBuff` default `OnlyPlaySoundOnLocalPlayer = True`. Only `TnBuffCloak` overrides it, to **False**.
  - `BuffReplicationType`: the base default is 0 = ToOwner. ToAll: HardLocked, TransformDisruptor, WarcryBase, LockOnThreat*, Cloak, DrainTarget. HealthOnBlock: ToNone.
  - Apply runs on the server and on each client that receives the replicated buff (`ClientRecieveReplicateTo*Buff` → `DoAddBuff` → `Apply`).
- **Net effect:**
  - All listed buffs except Cloak: heard only by the **buffed local player**, at their own pawn. This covers FlashBang EMP static, HardLocked warning loop, ScrambleHud, TransformDisruptor hit, Warcry start/stop, AoeHeal patient loop and LockOnThreat loops.
  - **Cloak:** heard by **everyone** who has the buff replicated (all clients), positional on the cloaked pawn.
- **Cloak variant:** chosen in `TnBuffCloak.Apply` by the **buffed pawn's team**: TnFactionTeamAutobots → Autobot cues; Decepticons → Decepticon cues; no team → `_CurrentCharacter.Faction == 0` → Autobot, else Decepticon. The cloaked pawn's faction decides, not the listener's.

### Drain

- **`TnBuffDrainSource.HealSound`:** `ClientTickBuff` → `UpdateEffects()` every **TnBuffManager.Tick** (H: per frame). It plays only if the owner is locally controlled and has ≥ 1 target, using `PlaySound(HealSound, bNotReplicated = true)` → **per tick** on the drainer's machine. It also cycles PlayHit through the targets.
- **`TnBuffDrainTarget.DamageSound`:** `ClientTickBuff` calls `PlaySound(DamageSound, true)` **every tick, unconditionally**, on every machine that has the buff (ToAll), positional at the victim.
- H: the cues must be non-restarting or short one-shots for per-tick calls to sound right. Not checked.

### TnBuffHealthOnBlock.ActivationSound

- `TnPawn.OnBlockDamage(PreDamage, PostDamage)` → `OnActivate`: it heals `(Pre − Post) × modifier`, then `Blocker.PlaySound(ActivationSound, bNotReplicated = true, bNoRepToOwner = true)`.
- It plays on **every blocked hit**, local to the machine running the damage code.
- H: the server, since the buff is ToNone. On a dedicated server nobody hears it; on a listen server, only the host.

### Abilities without OnTriggerSound

Their audio comes from **animation sound notifies** (HmAnimNotify_Sound on the ability anims) plus buff and spawned-actor sounds:

| Animation | Sound(s) |
|---|---|
| Skill_Shockwave / Skill_TransformDisruptor / Transform_ShieldPush_VEH | SHIELD_PUSH |
| Skill_Warcry | WAR_CRY_CHEST_HIT (+ servos) and WAR_CRY_STATE_START. The buff ApplySound is the same cue. |
| Skill_SpawnSentry / SentryBall_Out | SENTRY_ACTIVATE |
| Skill_GuidedMissile | GUIDED_MISSILE.SHOOT_BUILDUP |
| Skill_AbilityJammer | gun-butt whoosh |
| Transform_Whirlwind_ROBO | WHIRLWIND_WHOOSH_SINGLE / WHIRLWIND_COMPLETE / jumpjets |
| Nav_CloakActivate / Nav_CloakDeactivate | CQC_TRANSFORM_CLOAK_ACTIVATE / DEACTIVATE |

- Cloak and Warcry also have their buff sounds.
- Hover, Dodge, Shield and RollerSphere: no Skill_* sound notify found by sequence name (U). Their audio is presumably movement / spawned-actor sounds.

### §12 addendum: Hover / Dodge / Shield / RollerSphere audio (C unless marked)

**Jammed abilities:**
- `TnPlayerController.PlayerWalking.TriggerAbility`: if `!CanUseAbilities()` (jammed, disabled), it plays `Pawn.PlaySound(AbilitiesJammedSound, bNotReplicated = true)`. That is **`BL_TRANS_POWER.ENERGON_SLING_ABILITYFAILURE`**, local and positional at the pawn.
- So a refused trigger is not always silent. The refusals inside TnAbilityManager (cooldown/resource) are silent.

**Hover** (`TnAbilityHover.LocalTriggerAbility` → `PC.Hover()` → `TnRobotForm.Hover` → `TnAcrobaticsManager`):

| State change | Sound |
|---|---|
| `JumpingToHover.BeginState` | `_AudioService.PlayLoopingSound(_HoverLoopSound)` = **`BL_TRANS_POWER.HOVER_JUMP_LIFT`**: `CreateAudioComponent(cue, play, stopWhenOwnerDestroyed)` on the pawn (TnPawnAudioService), plus MakeNoise(HoverNoiseRadius) |
| `JumpingToHover.EndState` to anything except `Hovering` | Loop **fades out over 0.5 s** |
| Into `Hovering` | Loop keeps playing |
| `Hovering.EndState` | Loop fades out over 0.5 s, then `PlaySound(_HoverCooldownSound)` = **`HOVER_JUMP_LAND`** (default PlaySound args, so replicated from the server) |

- `_AcrobaticsState` replicates (`ReplicatedEvent` → `ClientUpdateState` → GotoState), so these state functions run on every machine. **Everyone hears the loop**, attached to the hovering pawn.
- H: on remote clients the LAND one-shot may sound twice: once locally, once replicated from the server.
- The Nav_Hover anims carry no sound notifies (FX only).

**Dodge** (`PC.Dodge` → `TnRobotForm.Dodge` → `TnAcrobaticsManager.Dodge` → `Dodging` state): no script sound. Audio comes from the dodge animations:
- `TnAcrobaticsSlotLogic.DodgeAnimations` → **Nav_Boost_F / B / L / R**, with EnergonHammer and Turret variants by stance.
- The shared robot animsets (TR_HeavyMedium / LightMedium Shared_ROBO_ANIM, Female) carry one **`HmAnimNotify_SoundEvent` `SoundEvents_Footsteps.FS_DEFAULT_JUMP_CHARGED`**, plus PlayEffect notifies. Turret variants are the same.
- The event resolves through `TnPawn.FindSoundCue`: character SoundEventSet → robot-form set → vehicle-form set. Examples: CHR_BUMBLEBEE → `BL_FS_SML_BOT.FS_JUMP_CHARGED`; CHR_OPTIMUS → `BL_FS_LRG_BOT.FS_JUMP_CHARGED`; 26 sets define it.
- Campaign-only animsets add their own sounds (Brute FS_JUMP, CQC_MOVEMENT, Frenzy boost/land).

**Shield** (`TnAbilityShield` has no script; referenced only by campaign maps, so it is **not an MP class-pool ability**):
- `PlayerWalking.TriggerAbility` → `PressBlock` → `StartBlock` → `TnShieldService.StartShield` → `BlockController.SetBlocking(true)` → `OnStartBlock` → `StartShield` → `ShieldMesh.PlayEvent(WP_Equip = 6)` + muzzle flash 9.
- Release (`UnTriggerAbility`) → `EndBlock` → `StopShield` → `PlayEvent(WP_PutDown = 7)` + muzzle flash 12.
- The shield templates define **only `WeaponEventAnims`** (Equip / Drop) and no `WeaponEventSounds`, so the sound comes from the shield-mesh anim notifies:
  - `SheildBruteA_Equip` → **`BL_SHIELD.ROBO_SHIELD_BRUTE_ON`**;
  - `SheildBruteA_Drop` → **`ROBO_SHIELD_BRUTE_OFF`**;
  - used by ShieldBrute_A and ShieldBrute_N.
- The ShieldBruteD_* and ShieldHeavy_D_* anims have **no sound notifies** (U whether that's intentional).
- Shield knocked out (health ≤ 0): KnockoutOfBlockAnimArray (`HitReactions_React_EnergonShield_Stand_R_05` / `L_05`) → their notifies, including `BL_SHIELD.ROBO_SHIELD_AUTOBOT_BREAK`, servo knockback and `ELEC_DMG_HV`.
- Blocked damage → HealthOnBlock (§12). Robot BlockingAnim default `Melee_Block_H2H`; Brute variants: None.

**RollerSphere** (`TnAbilityRollerSphere`; no OnTriggerSound; OnTriggerAnimParams = **Skill_AbilityJammer** → gun-butt whoosh notify):
- Sequence: base ServerTriggerAbility → after SpawnDelay **0.5 s**, spawn `TnRollerMineAbility` at +(500, 0, 100) with velocity (2750, 0, 0). If the location is unsafe it **retries every 1 s**.
- Mine sounds (all `bNotReplicated = true`, so they run on each machine where the actor exists):

| When | Sound | Stop rule |
|---|---|---|
| `PostBeginPlay` | `_IdleLoopingSound` **`BL_WPN_MINE.ROLLER_MINE_LP`** | stops when the mine is destroyed |
| ArmTimer, **3 s** | `ArmSound` **`BL_WPN_GRENADE.KAMIKAZE_FUSE_START`** | stops when the mine is destroyed |
| Fuse ≤ **1.5 s** (fuse 10 s → at 8.5 s; CDO, H not ini-overridden) | `_BuildupSound` **`ROLLER_MINE_FUSE_BUILD`**, once | stops when the mine is destroyed |
| `Destroyed` → `PlayExplosion` | **`ROLLER_MINE_EXPL`** + EXP_Mortar_FX | does not stop with the mine |

- The **FadingOut** state (instigator dead, dying or gone) overrides PlayExplosion with nothing, so the mine fades out **silently**.
- Buffs applied by proximity: TnBuffRollerSphere (enemies) and IncreaseSpeed (friendlies, with the skill). See the buff-sound table above.

**Decepticon shield sound gap: resolved. Not a gap; a different path.** (C unless marked)

**Decepticon animations:** `ShieldBruteD_Equip` / `_Drop` and `ShieldHeavy_D_Equip` / `_Drop` (in WEP_ShieldBruteD_ANIM and WEP_ShieldHeavy_D_ANIMSET) carry only `TnAnimNotify_ToggleHidden`. The Autobot `SheildBruteA_*` add HmAnimNotify_Sound BRUTE_ON / BRUTE_OFF at t = 0.

**Decepticon templates route sound through the muzzle flash.**
- Both D templates have `MuzzleFlashes = [{WP_Looping, PSTemplate FX_Shield_p.FX.ShieldD_01_FX}]`. The A/N templates have a WP_Looping entry with PSTemplate None.
- **ShieldBrute_D:** PSLoops = **false**. **ShieldHeavy_D:** PSLoops = **true**.
- `ShieldD_01_FX` is a ParticleSystem with **`SoundCue = BL_SHIELD.ROBO_SHIELD_DECEPTICON_ON_LP`** and `FadeOutTime 0.25` (FadeInTime default).

**Native ParticleSystem sound (WFC extension):**
- On activate (`execActivateSystem` → `0x83054520` → **`0x83028200`**): if no playing component, cue = `Template+0x7C` (SoundCue; or a PSC override at +0x1E8 when flag 0x800000).
- An audio component is created via `0x82E77A58(cue, scene, OwnerActor, …, bStopWhenOwnerDestroyed = Template+0x34 bit 26, Location = component origin)`, stored at PSC+0x1EC, then **FadeIn(Template+0x80, 1.0)**.
- On deactivate (`execDeactivateSystem` → `0x83035C18`): if playing → **FadeOut(Template+0x84 = FadeOutTime, 0.0)**, and the component is released.

**Block sequence (TnBlockController):**
- `StartShield` → `PlayEvent(WP_Equip)` → Equip animation (no sound) + `StartMuzzleFlash(WP_Looping = 9)` → ShieldD_01_FX activates → **DECEPTICON_ON_LP starts**.
- **Heavy_D (PSLoops):** loops until release.
- **Brute_D (PSLoops false):** `SetTimer(MuzzleFlashDuration = 0.1 s, StopMuzzleFlashInternal)` deactivates it after **0.1 s**, so the loop fades out over 0.25 s almost immediately. H: an audible short blip, likely an authoring slip.
- `StopShield` → `PlayEvent(WP_PutDown)` (Drop animation, no sound) + `StartMuzzleFlash(WP_LoopingTail = 12)`:
  - there is no entry for 12, and `OnlyStopMuzzleFlashWhenAnotherMuzzleFlashStarts` is false, so it calls `StopMuzzleFlash`;
  - that deactivates the PS → **0.25 s fade-out**;
  - there is **no Decepticon "off" one-shot**.
- `ROBO_SHIELD_DECEPTICON_OFF` is only on `FX_Shield_p.FX.shield_D_SML_END_FX`, used by `TR_HitEffectPlayer_p.SharedHitEffectPlayer` (hit effects; H: shield hit/break FX), and in the campaign BaseMapReferencers.
- `ROBO_SHIELD_DECEPTICON_ON_LP` is referenced **only** by ShieldD_01_FX.

### §12 addendum 2: TnPlayerController feedback sounds (SY) (C from script/CDO)

**Kill confirm:**
- Server `TnPlayerController.NotifyCausedDamage`: `IsFatalDamage` → `TellClientToPlayKilledPawnSound(victim)`.
- That uses `ClientPlaySound(cue)`, a client RPC to the **killer only**, which does `ClientHearSound(cue, PC, PC.Location, false)`. H: effectively non-positional.
- **Precedence:**
  1. `KilledPawn.WasLastHitHeadshot()` → KilledWithHeadshotSound;
  2. victim `IsInRobotForm` → KilledRobotSound;
  3. victim `_CurrentCharacter.CharacterType == CType_SoldierJet (6)` → KilledJetSound;
  4. `== CType_SoldierCar (5)` → KilledCarSound;
  5. otherwise → KilledVehicleSound.
- So the vehicle choice is by the victim's **character class**, not the vehicle class. Tank and all other classes in vehicle form → Vehicle.
- ECharacterType: Invalid, Buddy, Boss, Brute, CQCSpecialist, SoldierCar, SoldierJet, SoldierTank, Sniper, Rocketeer, Spider.

**DeathSound (`HUD_DEATH_POWER_DOWN`):**
- Only in `TnPlayerController.OnCampaignGameOver` (called from TnUIController): ClientStopMusic(0.25), `PlaySound(DeathSound, bNotReplicated = true)` on the PC, then GameOverMusic and GameOverMixerPreset, and dialog playback is disabled.
- **Campaign game over only; no MP use.** `TnVehicleForm` has a separate `_Blueprint.DeathSound`, played at the pawn locally.

**TransformFailedSound (`TRANSFORM_DISABLED`):** `PressTransform` decides as follows.
- **Silent early returns:** no TransformerPawn or `!_ReceivedWeapon`; PlayerInteractState ≠ 0; currently reviving someone (`RevivablePawn`).
- **Then `Pawn.PlaySound(TransformFailedSound, bNotReplicated = true)`** (local, positional) if the pawn **has TnBuffTransformDisruptor**, or if `Transform()` returns false:
  - **PlayerWalking:** pawn downed/reviving, or `StartTransform` fails;
  - **PlayerInVehicleForm:** `StartTransform` fails;
  - **PlaneDowned / Dead:** always false.
- **`StartTransform` fails when:**
  - already transforming, or `!IsTransformingEnabled` (H: covers melee and other disable flags);
  - **`!MoveToSafeTransformationLocation(TargetForm)`**: no room. This **also** calls `TnHUD.NotifyCantTransform()`.

**Roller mine arm sound:** `TnRollerMineAbility.ArmSound` = `BL_WPN_GRENADE.KAMIKAZE_FUSE_START` (CDO `TransGame.Default__TnRollerMineAbility`; it is a subclass field, not on TnRollerMine). Played by `TnRollerMineAbility.ArmTimer` (ArmTime 3.0) via `PlaySound(ArmSound, bNotReplicated = true, , bStopWhenOwnerDestroyed = true)`.

## 13. Beam2 / Trail2 vertex UV layout (RE) (C for CPU writes unless marked)

**Shared vertex format** (0x54-byte vertex, two vertices per path point, **both written with the same Position**):

| Offset | Field |
|---|---|
| +0x00 | Position |
| +0x0C | OldPosition |
| +0x18 | path direction |
| +0x24 | up vector, or (1, 0, 0) by flag |
| **+0x30** | **U** |
| **+0x34** | **V** |
| +0x38 | Color |
| +0x48 | Size × 3 |
| +0x54… | DynamicParameter (when flag 0x08000000) |

- The **side expansion happens in the vertex shader.** It is in compiled Xenon shaders, and no source is in the dump, so **which world side V = 0 lands on is UNKNOWN**. H: one side per vertex of the pair.
- Per-side width scales come from `0x8300F568(replay+0x90)`: default **(1, 1)**; other modes zero one side or both.

**V (across):** in every emitted pair, **first vertex V = 0.0** (stack 0x54/0x60 = DAT_82000D40) and **second vertex V = 1.0**. This holds for both fills.

**Beam (`0x830298E8`, the only beam fill; three emit sites — source pair, Hermite sub-step pair, noise-point pair):**
- **U runs along the beam, from 0 at the source.**
- step = **1 / (T × N)**, where T = NoiseTessellation (0 → 1) and N = the point count at payload +0x58 (`0x83029B80` `mullw`, `0x83029C64` `fdivs`, stored at 0x80(r1)).
- The running U (0x60(r1)) starts at step after the source pair and advances once per emitted pair, so **U = k / (T·N), ending at exactly 1.0 at the target**.
- **TextureTile is not applied** anywhere in the fill (C; irrelevant at the MP default of 1).
- There is no time term (no scrolling).

**Trail2 fill: `0x8301A700`** (not a Ghidra function; replay setup `0x83035770`; vertex count `0x83019600`; emit sites `0x8301B2F0`, `0x8301B59C`, `0x8301BC9C`):
- **U runs along the trail**, from 0.0 at the first emitted point (the trail-head record walk; **H: the head is the newest / source end, as in stock UE3**).
- **bTilePerParticle = false** (replay +0xC0 == 0):
  - max = TextureTile (replay +0xBC);
  - k = Tile / TotalTrailLength (head record +0x34; 0 if ≤ ε);
  - per-segment step = SegmentLength (particle payload +0x20) × k / SubSteps (replay +0xB0).
  - So **U = Tile × cumulative distance / total length, spanning the whole trail once (0 → 1 with Tile 1)**. Distance-based, not index-based.
- **bTilePerParticle = true:** max = count × Tile; step = Tile / SubSteps (each segment 0 → Tile).
- U is accumulated `U += step`, then **clamped to [0, max]** with `fsel` (`0x8301B460–0x8301B480`).
- No time term (no scrolling).

**§13 addendum: trail head direction (C)**

**Trail flags** are the stock layout (payload +0x00):
- bits 0xF0000000 = flags;
- PREV = bits 0x0FFFC000 (>> 14);
- NEXT = bits 0x00003FFF;
- null = 0x3FFF.

**Fill (`0x8301A700`):**
- `r17 = 0x0FFFC000` (`0x8301AC50`).
- It starts a strip only at a particle whose **PREV == null** (`0x8301AD40–0x8301AD48`).
- It skips dead trails (flag 0x10000000) and single-particle trails (NEXT == null, `0x8301AD5C`).
- It then walks NEXT.

**Spawn (`0x83048E40`, Trail2 instance vtable entry at `0x823380E0`):**
- `r28` = `ParticleIndices[ActiveParticles]` (the new particle); `r27 = 0x0FFFC000`.
- It finds the existing particle with PREV == null (the current head) (`0x83049470–0x830494A0`).
- **Old head:** PREV ← new index (`rlwimi …,14,4,17`), and if it was alone, NEXT ← null.
- **New particle:** NEXT ← old head, **PREV ← null** (`0x830494CC–0x830494F0`).
- The new particle's tangent ← normalize(oldHead.Location − new.Location) (`0x83049508–0x83049558`).

**Result: the head (U = 0) is always the most recently spawned particle**, i.e. the source end. U increases toward the oldest particle at the tail.

**§13 addendum 2: GPU side expansion of beam/trail vertices** (H overall: CPU-side facts C, shader numerics emulated)

**Vertex factory:**
- `FParticleBeamTrailVertexFactory` (type `0x83862280`; shader params class vtable `0x823351CC`).
- Bind `0x8305BB58`: CameraWorldPosition, **CameraViewVector**, ScreenAlignment, LocalToWorld, WorldToLocal.
- SetMesh `0x830129B0`: CameraViewVector = normalized view direction (view +0x270). If VF flag +0xA9 is set, it is instead normalize(cross) of two vectors stored at VF +0xAC…+0xC0.

**Shader:**
- vs_3_0 blobs with `CameraViewVector` in the D3DX CTAB are in the map ShaderCaches; analysed `MP_ORB_Debris_BASE_m` ShaderCache_12837 @ 0x1930.
- c5 = CameraViewVector, c6 = ScreenAlignment, c7–c10 = LocalToWorld.
- The fetch-semantic table at blob+0x210 gives POSITION, NORMAL, TANGENT, TEXCOORD0…4 in vfetch order. That maps in order onto the CPU vertex: Pos +0x00, OldPos +0x0C, direction +0x18, up +0x24, (U, V) +0x30, Color +0x38, Size +0x48, DynParam +0x54.
- Confirmed by use: TEXCOORD1 → oC2.xy (UV pass-through), TEXCOORD2 → oC1 (colour).

**Emulation** (new `tools/xenosvsemu.py`, CF/predicate aware; `xenosdis.py` vfetch decode extended):
- Default mode (ScreenAlignment c6 = 0) gives:

  **WorldPos = LocalToWorld·Pos + (2V − 1) · Size · normalize(cross(CameraViewVector, LocalToWorld·Dir))**

  where Dir is the +0x18 direction field. Position − OldPosition is **not** the axis.
- So **V = 1** is on the cross(view, dir) side and **V = 0** on the opposite side. The half-width = Size (the fill writes Size.xyz equal), so the full width = 2·Size.
- Checks: dir +X with view +Y → V = 1 at −Z; view −Z → V = 1 at −Y; view +Z → V = 1 at +Y; dir +Z with view +Y → V = 1 at +X.
- **c6.y ≠ 0** (up-vector mode): offset = (2V − 1)·Size·normalize(LocalToWorld·Up), using the +0x24 field.
- c6.x == 2.0 selects a Pos − OldPos path, degenerate for beams.
- What the CPU writes into ScreenAlignment for beams/trails is not traced (U); the default authored data suggests 0.

**One inferred op semantic** (`SUB_CONST_0` with the src3 negate bit at instruction 75: the negate applies to both operands → V − 0.5). It is the only reading that gives a symmetric ±Size strip; the alternative puts both vertices on the same side. That keeps this addendum at H rather than C.

## 14. LocationEmitter / LocationEmitterDirect and Trail2 chaining (RE) (C unless marked)

**Compiled-module records.** The UObject classes are stubs:
- `UParticleModuleLocationEmitter` (size 0x48, vtable `0x82333FF0`) and `…Direct` (size 0x34, vtable `0x82334130`) have empty Spawn/Update slots (`blr`).
- The real code runs in the compiled-module runners, keyed by record byte +0x0A:
  - **Spawn runner `0x8303E288`:** case **0x13 = LocationEmitter**, case **0x14 = LocationEmitterDirect**.
  - **Update runner `0x83039A18`:** case **0x14 = LocationEmitterDirect** only.
- Record (0x14 bytes, LOD+0x38 → +0x14 array): **+0x00 u16 payload offset** into the LOD payload blob (pointer at LOD+0x5C); **+0x06 u16 per-instance data offset** (base = emitter instance +0x12C); +0x0A u8 module id; +0x10 UObject pointer (used by the runner's default case).

**Payload layout (LocationEmitter, 0x18 bytes, big-endian):**

| Offset | Type | Field |
|---|---|---|
| +0x00 | int | **EmitterName** = index into the LOD's name list (LOD+0x38 → +0x68 = array of FName indices). The source is found by comparing with each component EmitterInstance's `SpriteTemplate.EmitterName` (+0x10 → +0x28). |
| +0x04 | float | InheritSourceVelocityScale |
| +0x08 | float | InheritSourceRotationScale |
| +0x0C | int | **SelectionMethod**: 0 = Random, 1 = Sequential, other values → particle 0 |
| +0x10 | int | bInheritSourceVelocity |
| +0x14 | int | bInheritSourceRotation |

- Direct reads only **+0x00** (the name index).

**LocationEmitter spawn (case 0x13; selection `0x830352D8`):**
- **Random:** uses the global appFrand state (`0x83775C7C` LCG); index = ⌊frac · count⌋, clamped to count − 1.
- **Sequential:** per-instance counter at instance+0x12C + rec+0x06. `counter += 1`; if counter ≥ the source's ActiveParticles → 0. So the sequence is **1, 2, …, n − 1, 0, 1, …**.
- **No source emitter, or no live source particle:** the module **does nothing**. The particle keeps the position the earlier modules gave it (the emitter origin); the spawn is **not** skipped.
- **Position:**
  - Normally: `Loc = M_src→this · (src.Location + (V − src.Velocity) · dt)`.
    - dt = min(spawn sub-frame time, src.RelativeTime / src[+0x1C]).
    - V = this instance's +0x88 vector, or 0 when instance flag 0x40000000.
    - Matrices from `0x8300CC48`.
  - A source particle with RelativeTime == 0 (spawned this frame) is instead extrapolated from the source **emitter's** location (+0x70).
  - H: the exact meanings of the dt and V fields are inferred. In effect it is sub-frame back-extrapolation to where the source particle was at this particle's spawn time.
- **bInheritSourceVelocity:** `BaseVelocity += M·src.Velocity · Scale` and `Velocity += …`. Note that M includes translation (a quirk of the build).
- **bInheritSourceRotation:** `Rotation += src.Rotation · Scale`.
- **There is no Update case**, so the position is set **only at spawn**.

**LocationEmitterDirect:**
- **Spawn (0x14):** the new particle (active index n − 1) copies the source particle with the **same active index**: Location, OldLocation and Velocity (each through `M = 0x8300CA48(src instance)`) and the field at +0x0C.
- **Update (0x14 in the update runner):** **every tick**, each live particle i (from last to 0, skipping flag 1) is re-snapped to source active particle i the same way.
- **Counts differ:** particles with i ≥ the source count are left untouched.

**Trail2 spawn with LocationEmitter (`0x83048E40`):**
- The spawn count per tick is computed from SpawnRate (or a spawn-per-unit helper `0x830178A8` when the instance has one at +0x148), capped by TypeData MaxTrailCount × MaxParticleInTrailCount, then **clamped to ≤ 1 particle per tick**.
- Flag TypeData+0x40 bit 0x20000000: no spawn when the component hasn't moved more than ε (H: spawn-only-if-moving).
- **Per new particle:**
  1. Required init → **compiled spawn modules (`0x8303E288`)**, where LocationEmitter places it → TypeData spawn → `vtable+0x40` post-spawn.
  2. Flags ← 0x0FFFFFFF (no PREV/NEXT).
  3. It becomes the **head of the first particle found with PREV == null** (old head.PREV = new, new.NEXT = old head).
  4. Tangent = normalize(oldHead.Location − new.Location), or the component X axis on the first spawn / with TypeData flag 0x40000000.
- **No per-source or per-trail filter exists**, so with several live source particles (several shells) it is **one chain**. Each new head sits at whichever source particle the selection picked, so the strip **zig-zags** between sources. With Sequential or Random selection it alternates.
- **The head does not track its source between spawns.** Positions are written only at spawn; LocationEmitter has no update case.

**§14 addendum: LocationEmitter sub-frame dt term (C; interpretation H)**

**Particle fields (this build):**
- From the compiled Lifetime module (spawn runner case 1): particle **+0x1C = OneOverMaxLifetime**, **+0x0C = RelativeTime = OneOverMaxLifetime × SpawnTime**.
- So the runner's float argument (dVar43) is **SpawnTime**, the sub-frame time already elapsed since this particle's spawn moment.
- Layout otherwise: OldLocation +0x00, Location +0x10, BaseVelocity +0x20, Rotation +0x2C, Velocity +0x30, Flags +0x5C.

**Emitter-instance motion** (`0x8300BF18`, called every tick from both emitter Ticks):
- +0x7C = OldLocation ← previous +0x70;
- **+0x70 = Location = component LocalToWorld origin**;
- **+0x88 = Velocity = (Location − OldLocation) / max(DeltaTime, ε)**, set to 0 on reset.
- Instance flag +0xA8 bit 0x40000000 = **bUseLocalSpace**.

**Space matrices:**
- `0x8300CA48(this, src)` = source-space → this-space:
  - both world, or both local → identity;
  - src world / this local → inverse(this.LocalToWorld (+0x30));
  - src local / this world → this.LocalToWorld.
- `0x8300CC48` also returns W = world → this-space: identity if this is world space; = the matrix above if src is world; else inverse(this.LocalToWorld).

**Spawn position (case 0x13),** with S = SpawnTime and V_e = this emitter's world velocity (+0x88), or 0 if this emitter is local-space:
- **Normal:** `age = src.RelativeTime / src.OneOverMaxLifetime`; `dt = min(S, age)`.

  **Loc = M_src→this · ( src.Location − src.Velocity·dt + V_e·dt )**
- **Uninitialised source** (src.RelativeTime == 0 **and** src.Location == (0, 0, 0)): **Loc = W · ( srcEmitter.Location − srcEmitter.Velocity·S + V_e·S )**.
- H interpretation:
  - `− src.Velocity·dt` rewinds the source particle to where it was at this particle's spawn moment (never before the source was born).
  - `+ V_e·dt` cancels the emitter-motion compensation that the post-spawn step applies, so trail points land on the source's path rather than lagging the moving component.

**§14 addendum 2: post-spawn step (C)**

**Call chain:**
- Trail2 instance vtable `0x823380D8` (+0x08 Spawn `0x83048E40`, +0x0C Tick `0x83048218`).
- **+0x40 PostSpawn = `0x830192D8`** first calls the **base PostSpawn `0x8300C4B8`** (args: particle, f1 = InterpolationFraction, f2 = SpawnTime). It then sets the trail payload's up vector (+0x24…+0x2C): zero when TypeData+0x50 is unset, otherwise lerp(prev, current, f2 / x) normalized.
- Trail2 Spawn passes **f1 = 1 − (i + 1)/n** and **f2 = this particle's SpawnTime**. With its ≤ 1-per-tick clamp, n = 1 → **f1 = 0**.

**Base PostSpawn**, with V_e = instance +0x88 emitter world velocity (0 if bUseLocalSpace):
- **Location += (Velocity − V_e) · SpawnTime**
- **OldLocation = Location − Velocity · f1** (= Location for Trail2)
- WFC differs from stock UE3: there is no OldLocation interpolation, and the V_e term is new.

**Combined with the LocationEmitter placement** (same space, dt = SpawnTime, i.e. the source is older than SpawnTime):

  final Loc = src.Location − src.Velocity·S + Velocity·S

- The **V_e terms cancel exactly**, so the earlier interpretation is now C.
- With **bInheritSourceVelocity, scale 1** (Velocity = src.Velocity, nothing else adding velocity): final Loc = **src.Location** exactly.
- With **no velocity** (no inherit, no velocity modules): final Loc = **src.Location − src.Velocity·S**, the source's position at this particle's spawn moment.
- H: the spawn runner's time argument and PostSpawn's SpawnTime come from the same rate accumulator in `0x83048E40` (dVar28 vs dVar30). Their exact equality is not checked.

**§14 addendum 3: SpawnTime equality (C)**

**Inputs** (raw `0x83048E40`):
- Old = leftover spawn fraction (instance +0xC8, f30 at `0x83049040`);
- DT = DeltaTime (f24);
- Inc = 1 / max(rate, ε) (f31, `0x8304908C`).

**Two computations:**
- **Spawn modules / TypeData spawn** receive f1 = **S_mod = DT − (1 − Old)·Inc**: `fsubs f0 = 1 − Old`; `fnmsubs f13 = −(f0·Inc − DT)`; `fsel` clamps it at 0 (`0x83049238–0x83049258`). It is passed at `0x830492E8` / `0x83049304`, then decremented by Inc after each actual spawn.
- **PostSpawn** receives f2 = **S_post − i·Inc**, where **S_post = (Inc·Old + DT) − Inc** (`fmadds` / `fsubs` at `0x83049090–0x83049094`), clamped at 0 (`0x830490A0`), via `fnmsubs f2,f6,f31,f25` at `0x8304937C`.

**Result:**
- They are **algebraically identical**, with identical clamps.
- They differ only by float rounding (different fused-op order, about 1 ulp).
- f30 is callee-saved across the intervening calls.
- For Trail2 (≤ 1 spawn per tick, i = 0) the spawn-module and PostSpawn SpawnTimes are the same value.
- They can only diverge for n > 1 with a skipped (random-rejected) spawn: the module time decrements per actual spawn, while PostSpawn uses the loop index.

**§13 addendum 3: ScreenAlignment / billboard inputs for beams and trails** (C unless marked)

**Vertex declaration (C):** the global decl resource `0x83718D28` (InitRHI `0x8305DD68`, elements `0x8305C738`). Stride 0x54; the dynamic-parameter variant adds TEXCOORD4.

| Offset | Format | Usage | Field |
|---|---|---|---|
| +0x00 | Float3 | POSITION | Position |
| +0x0C | Float3 | NORMAL | OldPosition |
| +0x18 | Float3 | TANGENT | Dir |
| +0x24 | Float3 | TEXCOORD0 | Up |
| +0x30 | Float2 | TEXCOORD1 | UV |
| +0x38 | Float4 | TEXCOORD2 | Color |
| +0x48 | Float3 | TEXCOORD3 | Size |

This confirms the addendum-2 fetch mapping.

**ScreenAlignment constant (c6)** = `(float VF[+0xA8], float VF[+0xC4], 0, 0)` (SetMesh `0x830129B0`).

Renderers:
- beam `0x8304AF58` (its dynamic data's fill wrapper `0x83055E88` calls the beam fill);
- trail `0x8304B208` (wrapper `0x83055F38` calls the trail fill).

Both set:
- **VF+0xA8 ← replay+0x34 = RequiredModule.ScreenAlignment** (RequiredModule = LOD+0x30; property order Material +0x30, ScreenAlignment +0x34);
- **VF+0xC4 ← replay+0x90 byte 0 = TypeData.BillboardSettings.Direction**;
- **VF+0xA9 (lock-axis flag) ← 0**.

`BillboardingSettings` (WFC struct on TypeDataBeam2/Trail2) = {Direction u8, Alignment u8, pad, pad}:
- EBillboardDirection: CameraFacing, LocalX, LocalY, LocalZ, WorldX, WorldY, WorldZ;
- EBillboardAlignment: Centered, Positive, Negative.

(Correction to the working note: `0x830526E0` / `0x8302C370` is a sprite dynamic-data path, not trail.)

**Shader behaviour by input** (emulated, `xenosvsemu`):
- **c6.x = PSA_Square (0) or PSA_Rectangle (1):** the default camera-facing path, offset = (2V − 1)·Size·normalize(cross(view, Dir)). The shader has no separate Rectangle branch.
- **c6.x = PSA_Velocity (2):**
  - The strip axis becomes Position − OldPosition (instructions 160–175).
  - **Both fills write OldPosition == Position at every emit site** (C: beam `0x8302A1D8…0x8302AB98`, trail `0x8301B28C…0x8301B638`).
  - So the axis normalizes to 0 (max(len², 0.01) then rsqrt → 0) and the **strip has zero width (invisible)**.
  - **H** (emulated shader; no fallback branch exists).
  - Authored: 33 Beam2 LODs and 22 Trail2 LODs. These include MP-visible effects: **Tracer_Blaster_FX, Tracer_AssaultRifle_FX, Tracer_SniperRifle_FX, Flashbang/HealGrenade trails, Trail_Missiles_FX, EXP_Mortar_FX**, and others.
- **c6.y = Direction ≠ 0:**
  - Offset = (2V − 1)·Size·scale_side·normalize(Up). The fill writes Up (+0x24) = the Direction axis from `0x8300F428`: Local X/Y/Z = normalized component LocalToWorld rows; World X/Y/Z = unit axes. CameraFacing → the fill writes (1, 0, 0) and it is unused.
  - Side scales (`0x8300F568`, replay+0x90 byte 1): Centered (1, 1); **Positive (0, 2)** (the V = 0 side collapses, the V = 1 side is 2·Size); **Negative (2, 0)**. They are applied CPU-side to Size per vertex.
  - Authored Direction: Beam2 LocalY 25, LocalX 21, LocalZ 4; Trail2 LocalY 3, LocalZ 3; all others CameraFacing.

**§13 addendum 4 (2026-10-06): CORRECTION, the PSA_Velocity beam/trail census was wrong** (C)

**What went wrong:** addendum 3 paired each Beam2/Trail2 TypeData with a RequiredModule by `outer_path`. Both modules are outered to the ParticleSystem, not the LOD, so the query took the system's *first* RequiredModule. The counts and the tracer list in addendum 3 are therefore **invalid**.

**Recount through `ParticleLODLevel.RequiredModule` / `.TypeDataModule`:**
- **Beam2:** PSA_Square 343, **PSA_Rectangle 26** (OmegaSpawn_AI_FX, Trypticon_EntranceArm_Electricity_FX), **PSA_TypeSpecific 8** (OmegaGate_Unlock_FX).
- **Trail2:** **PSA_Square 286**.
- **No Beam2/Trail2 LOD uses PSA_Velocity**, so the zero-width velocity path is never reached by authored data. **Retracted.**

**What the tracers actually are:**
- Tracer_AssaultRifle_FX / Tracer_SniperRifle_FX: a **sprite** emitter "Bolt" (PSA_Velocity, Bolt_ADD_MAT) plus a Trail2 "Trail_Smoke" (PSA_Square).
- Tracer_Blaster_FX: a **sprite** "BeamsSm" (PSA_Velocity, Spark_MAT) plus a Beam2 (PSA_Square, Tracer_MAT).
- The velocity alignment belongs to the sprite vertex factory, which is not affected by this finding.

**Effect on the shader rules:**
- The beam/trail shader only branches on c6.x == 2, so Rectangle and TypeSpecific behave like Square (camera-facing default) (H, emulated).
- The BillboardSettings.Direction census was per TypeData object and **stands**.
- The other addendum-3 findings stand: the vertex declaration, the c6 inputs and the Direction/Alignment behaviour.

## 15. Sprite PSA_Velocity alignment (RE) (CPU parts C; shader numerics H, emulated)

**Sprite vertex factory:**
- VFType `0x838622CC` ("ParticleSpriteVertexFactory"; GetType `0x8305D5E8`).
- Declaration (elements `0x8305C2D0`), stride 0x40:

| Offset | Format | Usage | Field |
|---|---|---|---|
| +0x00 | Float3 | POSITION | Position |
| +0x0C | Float3 | NORMAL | OldPosition |
| +0x18 | Float3 | TANGENT | Size |
| +0x24 | Float1 | BLENDWEIGHT | Rotation |
| +0x28 | Float4 | TEXCOORD1 | Color |
| +0x38 | Float2 | TEXCOORD0 | UV / corner |

**Parameters:**
- Bind `0x83059928`: CameraRight, CameraUp, ScreenAlignment, LocalToWorld, AxisRotationVectorSourceIndex, AxisRotationVectors, **ParticleUpRightResultScalars**, WorldToLocal.
- SetMesh `0x830198C8`, with no lock axis (VF+0xA9 == 0):
  - CameraRight / CameraUp = **negated normalized screen axes** from the view (stock UE3 convention: the names are swapped).
  - **Scalars = (0, 1, 0, 0) when VF+0xA8 (Required.ScreenAlignment) == PSA_Velocity, else (1, 0, 0, 0).**
  - Lock-axis modes 7–12 use the AxisRotationVectors path (scalars.z).

**Shader** (MP_ORB_Debris ShaderCache_12837 @ 0x10743, microcode at +0x2C4; `tools/xenosvsemu.py` with a new `mstart` argument and TRUNC/FRAC/SIN/COS):
- D = normalize(L2W·Pos − L2W·OldPos), C = normalize(WorldCameraPosition − L2W·Pos).
- Right′ = R_rot·s.x − D·s.y; Up′ = U_rot·s.x + cross(C, D)·s.y, where R_rot / U_rot are the camera axes rotated by the particle Rotation.
- **WorldPos = L2W·Pos + (V − ½)·Size.y·Right′ + (U − ½)·Size.x·(axis built from c6 / cross)**.

**Results (emulated):**
- **Camera-facing** (Square/Rectangle): U·Size.x along screen-right, V·Size.y along screen-down. Rotation rotates them.
- **PSA_Velocity:**
  - **Length = Size.y along the motion**: V = 0 at the **leading** edge, V = 1 at the tail.
  - **Width = Size.x** across, along cross(camera→particle, D).
  - **Particle Rotation is ignored.**
  - **No speed stretch** (D is normalized; the length is always Size.y).
  - Check: Size (10, 20) moving +X → ±10 along X, ±5 across; moving +Z → ±10 along Z.
- **Degenerate cases:**
  - Pos == OldPos (zero velocity): D → 0, so the sprite **collapses to a point (invisible)**.
  - Motion straight toward or away from the camera: cross(C, D) → 0, so it becomes a zero-width line.
  - Both are inherent to the original (H).

**MP velocity sprites:** e.g. Tracer_AssaultRifle / SniperRifle "Bolt" (Bolt_ADD_MAT) and Tracer_Blaster "BeamsSm" (Spark_MAT).

**H (not traced):** OldPosition in sprite vertices = particle OldLocation (stock fill), so D = the last tick's motion direction. PostSpawn sets OldLocation = Location − Velocity·f1 (§14 addendum 2).

**§15 addendum: sprite lock-axis modes** (CPU C; shader numerics H, emulated)

**Data source:**
- `ParticleEmitter.LockAxisFlags` is a **WFC emitter-level byte** (emitter +0x2D; there are no OrientationAxisLock module objects in the cooked data).
- Path: emitter-instance init `0x83046248` → instance +0x124 → replay +0x35 (`0x8300C890` / `0x8302C484`) → VF +0xA9.
- `EParticleAxisLock`: NONE, X, Y, Z, NEGATIVE_X/Y/Z, ROTATE_X/Y/Z, and **WFC-only ROTATE_X_U / Y_U / Z_U (10–12)**.
- Authored (emitters): Z 156, X 148, NEGATIVE_X 28, ROTATE_Z 8, Y 7, ROTATE_X 6, NEGATIVE_Z 4, ROTATE_Z_U 3, ROTATE_Y 1.
  - **X:** MP muzzle flashes and impacts (AssaultRifle / HeavyMG / BurstRifle / EMPShotgun …).
  - **Z:** explosions (EXP_MED_01, Exp_Energon_Crate …).
  - **ROTATE_Z:** WarCry_AOE_FX.

**Axes** (`0x8300FC80`): rows of M = component LocalToWorld when replay+0x30 bit 0x20000000 (H: bUseLocalSpace), else identity.

| Mode | Up (A) | Right (B) |
|---|---|---|
| X | Z | Y |
| Y | Z | −X |
| Z | X | −Y |
| −X | Z | −Y |
| −Y | Z | X |
| −Z | X | Y |

- ROTATE_X/Y/Z: A = X / Y / Z. ROTATE_*_U: A = −X / −Y / −Z.
- This matches stock UE3 for 1–9.

**SetMesh** (`0x830198C8`):
- **Modes 1–6:** CameraUp ← A, CameraRight ← B (not negated); scalars (1, 0, 0, 0).
- **Modes 7–12:** AxisRotationVectors[0] = [1] = (A, 1); AxisRotationVectorSourceIndex ← 0 (modes 7–9) or 1 (`_U`, 10–12) via `0x82CED560`; scalars (0, 0, 1, 0).

**World result** (emulated; Size = (x, y); C = normalize(camera − particle); P = normalize(cross(C, A))):
- **Lock 1–6:** Pos + (U − ½)·Size.x·(−A) + (V − ½)·Size.y·B. The quad lies in the A–B plane, fixed in the world (or component) frame, and **Rotation still spins it in-plane**. Example, X: a quad in the YZ plane facing ±X.
- **ROTATE_X/Y/Z:** Pos + (U − ½)·Size.x·**A** + (V − ½)·Size.y·**P**. The quad's U edge runs along the axis; it turns about the axis to face the camera.
- **ROTATE_*_U:** Pos + (U − ½)·Size.x·**P** + (V − ½)·Size.y·**A** (U and V roles swapped).
- **Degenerate:** viewing straight along A (e.g. ROTATE_Z from directly above) gives P → 0 and a zero-width quad (inherent).
- H: whether Rotation is ignored in the rotate modes was not tested.

**§15 addendum 2: lock-axis frame flag (C)**

**Where the flag comes from:**
- `FUN_8300FC80` uses the scene-proxy LocalToWorld (proxy + 0x20) as the axis frame when sprite replay +0x30 bit **0x20000000** is set, else identity (world axes).
- That bit is written in the sprite dynamic-data constructor `0x8302C370`: `(param[+0x3C] & 1) << 29`.
- `param[+0x3C]` is filled by the sprite GetDynamicData `0x830526E0` as `RequiredModule+0x38 >> 31`. That is the first bool of RequiredModule's bitfield, **`bUseLocalSpace`** (Material +0x30, ScreenAlignment +0x34, ParticleBurstMethod / InterpolationMethod / EmitterRenderMode bytes, then the bools starting with bUseLocalSpace at +0x38, MSB-first as in the Beam modules).

**So:** lock axes follow the **component rotation (and scale) only when the emitter LOD's RequiredModule.bUseLocalSpace is true**. Otherwise they are the **world** X/Y/Z, regardless of how the component is oriented.

**Other flags in the same word:**
- bit 0x10000000 = "has lock axis" (instance +0x124 ≠ 0);
- replay +0x34 = ScreenAlignment;
- replay +0x35 = LockAxisFlags.

**Census** (emitter LockAxisFlags × LOD0 RequiredModule.bUseLocalSpace, paired through the LOD pointer):

| Mode | Local space | World space |
|---|---|---|
| X | 146 | 2 |
| Z | 59 | 97 |
| NEGATIVE_X | 23 | 5 |
| ROTATE_Z | 1 | 7 |
| ROTATE_X | 6 | 0 |
| Y | 6 | 1 |
| NEGATIVE_Z | 0 | 4 |
| ROTATE_Z_U | 0 | 3 |
| ROTATE_Y | 1 | 0 |

- **All 22 muzzle-flash emitters are X + local space** (they face along the barrel/socket X axis).
- Most Z explosion rings are world-space (they lie flat on the world XY plane whatever the component orientation).

**§15 addendum 3: particle Rotation in the rotate / velocity modes** (H: emulated plus dataflow)

**Dataflow:** the sprite VS uses Rotation only as `angle = 2π·frac(rot/2π + ½) − π` → SIN/COS (instructions 19–32). These build the rotated camera axes R_rot = cos·c5 + sin·c6 (r13) and U_rot (r10). Those enter the position **only** through the `ParticleUpRightResultScalars.x` terms (instructions 41 and 46).

**Consequences:**
- **Camera-facing (Square/Rectangle) and lock modes 1–6** (scalars.x = 1): Rotation spins the quad in its plane.
- **PSA_Velocity** (scalars.y = 1) and **ROTATE_X/Y/Z / ROTATE_*_U** (scalars.z = 1): **Rotation is ignored.**

**Emulation check:** ROTATE_Z, ROTATE_Z_U and velocity give identical corners at Rotation 0, π/4, π/2 and π. RotationRate modules therefore have no visual effect on these sprites.

## 16. Sprite SubUV (RE) (C unless marked)

**Modules:** SubUV / SubUVSelect / SubUVDirect are **compiled records** (only CDOs exist as objects).
- Update runner `0x83039A18`: **case 0x1F = SubUV**, **0x20 = SubUVSelect**, **0x21 = SubUVDirect**.
- Each runs only if RequiredModule.InterpolationMethod (Required+0x36) ≠ 0.
- Each has a sprite and a mesh variant, chosen by `0x8305A068` (IsA FParticleMeshEmitterInstance):

| Module | Sprite | Mesh |
|---|---|---|
| SubUV | `0x83017E10` | `0x830181A8` |
| SubUVSelect | `0x830184C8` | `0x830188C8` |
| SubUVDirect | `0x83018C90` | `0x83018F28` |

- They update **every tick** for every live particle (flag bit 1 clear, RelativeTime ≤ 1).

**SubUV payload** (particle + instance payload offset):

| Offset | Field |
|---|---|
| +0x00 | last random-change RelativeTime |
| +0x04 | H (column) |
| +0x08 | V (row) |
| +0x0C | Interp |
| +0x10 | H2 |
| +0x14 | V2 |

**Index selection (`0x83017990`)**, total = SubImages_H × SubImages_V (Required +0x74 / +0x78):
- **PSUVIM_Linear / Linear_Blend:** `f = SubImageIndex(RelativeTime)`; idx = clamp(⌊f⌋, 0, total − 1); Interp = |f − idx|. **Linear forces Interp = 0.**
- **PSUVIM_Random / Random_Blend:**
  - A new pick happens if RandomImageTime (Required+0x7C) == 0, **or** RelativeTime − lastChange > RandomImageTime (**lifetime-fraction units, not seconds**), **or** this is the first time.
  - The pick is idx = ⌊total · r⌋ with Interp = r (the same RNG fraction; Random forces 0); then lastChange = RelativeTime.
  - Otherwise the old index is held (the function returns 0).
  - `RandomImageChanges` is not read.
- **PSUVIM_None:** idx 0, Interp 0 (but the module is skipped anyway when InterpolationMethod == 0).

**Cell mapping (`0x83017E10`):**
- H = idx mod SubImages_H, V = idx div SubImages_H (row-major, left to right, then top to bottom).
- If a new value was produced, (H2, V2) = the next cell: H + 1, wrapping to (0, V + 1), and after the last cell to (0, 0).
- On a Random hold, H2/V2 = H/V and Interp is reset to 0.

**SubUVSelect (`0x830184C8`):**
- Linear modes: (H, V) = ⌊SubImageSelect(RelativeTime).xy⌋.
- Random modes: H = ⌊r₁ · total⌋, V = ⌊r₂ · total⌋, **re-rolled every tick** (no RandomImageTime gate). Each axis ranges over **total**, not its own axis count, so it can exceed the grid. That is a WFC quirk; visible wrapping depends on the sampler (H).
- Interp = 0; (H2, V2) = the next cell.

**SubUVDirect (`0x83018C90`):** (H, V) ← SubUVPosition(RelativeTime), (H2, V2) ← SubUVSize(RelativeTime), Interp = 0.

**Render fill (`0x8305F7D8`, SubUV vertex stride 0x58, decl `0x8305BEF0`):**
- Vertex layout: Pos +0x00, OldPos +0x0C, Size +0x18, Rotation +0x24 (BLENDWEIGHT), Color +0x28 (TEXCOORD1), **(U, V, U2, V2) +0x38 (TEXCOORD0)**, **(Interp, pad, cornerU, cornerV) +0x48 (TEXCOORD2)**, then the dynamic parameter.
- Size = (Size.x, Size.y), with **Size.y = Size.x when ScreenAlignment == PSA_Square**.
- Normal mode: **U = ⌊H⌋ · (1/SubImages_H), V = ⌊V⌋ · (1/SubImages_V)**, and U2/V2 likewise. These are the cell's top-left corners.
- Direct mode (dynamic data +0x9C ≠ 0): UV = (Position + Size · corner) · scale. H: scale = 1/texture size, i.e. texel units.
- H: the shader adds corner·cellSize and lerps texture(UV1) → texture(UV2) by Interp (not traced).

**Authored RequiredModule.InterpolationMethod:** Linear_Blend 515, Random 459 (14 with RandomImageChanges set, which is unused), Linear 130, None 47, Random_Blend 28.

**Also noted:** `ParticleEmitter.SpriteEmitterRenderMode` (SERM_Quad / Octagon / BestFit, with `BestFitPolygons`) is a WFC polygon-sprite feature; the fill's 12 vertex-write sites cover it. **Not traced** (U).

## 17. Sprite polygon render modes (SERM_Quad / Octagon / BestFit) (RE) (C unless marked)

**Setting:** `ParticleEmitter.SpriteEmitterRenderMode` (WFC; emitter +0x2C), plus `BestFitPolygons`.
- Authored: Quad (default) 1640 emitters, **BestFit 1269**, Octagon 160.
- Every BestFit emitter has exactly **1** polygon. 38 Quad/Octagon emitters also carry a stale polygon, which is unused.

**Fill** (`0x8305F7D8`, mode = dynamic data `piVar33[4]`). It writes per-vertex corners into vertex +0x50 / +0x54, the same slot the shader expands with (`(corner − ½)·Size` along the sprite axes, §15). UVs are computed on the CPU as (cell + corner) × cellSize (SubUV, §16), so geometry and texture stay aligned.

| Mode | Vertices | Corners |
|---|---|---|
| **0 Quad** | 4 | (0,0), (0,1), (1,1), (1,0) |
| **1 Octagon** | 8 | (0.2929, 0), (0.7071, 0), (1, 0.2929), (1, 0.7071), (0.7071, 1), (0.2929, 1), (0, 0.7071), (0, 0.2929) |
| **2 BestFit** | VertexCount (3–8, H: max 8 from the index switch) | the polygon's vertices (x, y) in cell-local 0–1 texture space |

- Octagon constants are `0x82335B1C` = 1 − 1/√2 and `0x82335B20` = 1/√2, i.e. the unit square with corner triangles of leg 1 − 1/√2 cut off.
- BestFit polygon records: 0x68 bytes = {Time f32, VertexCount i32, Vertices[12] (x, y)}. Slots past VertexCount are stale data.
- **BestFit selection:** the last polygon whose `Time ≤ particle age in seconds` (RelativeTime / OneOverMaxLifetime). With one authored polygon it is always polygon 0.
- **Indices:** per-polygon lists built by vertex count. H: authored polygons are convex, so any triangulation covers the same area.

**Visual consequences (H):**
- **BestFit** clips the quad to a hull around the texture's visible texels. Where the excluded area is transparent it looks identical to a quad (it is a fill-rate optimisation). A renderer drawing plain quads is visually equivalent **provided** the texture is transparent outside the polygon.
- **Octagon** always removes the four corner triangles (leg 0.293 of the quad). Any texel there is never drawn. A quad renderer will show corner content the original hides (usually none, for round puff textures).

**§17 addendum: BestFit index triangulation (C)**

**Dispatch:** `0x8305FD88`: `VertexCount − 3` indexes a 10-entry jump table at `0x8305FDAC`.
- VertexCount **3–12** are supported (this corrects "max 8" above).
- Any other count goes to `default`: **no indices, so the polygon is not drawn**.
- Indices are u16, relative to the particle's first vertex, written in pairs.

| VertexCount | Triangles (vertex indices, in emission order) |
|---|---|
| 3 | (0, 1, 2) |
| 4 | (0, 2, 3), (0, 1, 2) |
| 5 | (0, 3, 4), (0, 1, 3), (1, 2, 3) |
| 6 | (0, 1, 5), (1, 3, 5), (1, 2, 3), (5, 3, 4) |
| 7 | (0, 5, 6), (0, 1, 5), (1, 3, 5), (1, 2, 3), (3, 4, 5) |
| 8–12 | shared block `0x83060434`: a **fan** (0, k, k + 1) for k = 1 … N − 2, with count checks after vertex 7 |

**Properties:**
- All triangles keep the polygon's vertex winding: (5, 3, 4) ≡ (3, 4, 5).
- The 5–7 patterns are "ear" splits that are only valid for **convex** polygons. H: the BestFit hulls are convex, so the drawn area equals the polygon and any convex triangulation is visually identical.
- The Quad/Octagon index lists are emitted by separate code; not decoded (both convex).

**§17 addendum 2: Quad and Octagon index lists (C)**
- Same fill, `0x8305F7D8`; u16 indices relative to the particle's first vertex.

**Quad** (4 vertices per particle; base = particle × 4):
- Triangles **(0, 2, 3), (0, 1, 2)**, written only when dynamic data `piVar33[0xB]` ≠ 0.
- Otherwise no per-particle indices are written. H: the quads are then drawn without them (Xenos quad-list primitive or a shared static quad index buffer).
- Corners v0 (0,0), v1 (0,1), v2 (1,1), v3 (1,0).

**Octagon** (8 vertices per particle; base = particle × 8):
- Triangles **(0, 7, 6), (0, 6, 5), (0, 5, 3), (0, 3, 2), (0, 2, 1), (3, 5, 4)**: a fan from v0 that skips v4, plus the ear (3, 5, 4).
- Corners v0 (0.293, 0) → v7 (0, 0.293), going around the cut square.

**Winding:**
- In corner space (x right, y down) every quad and octagon triangle has the same orientation sign (e.g. quad (0, 2, 3) and octagon (0, 7, 6) both have a negative z cross product).
- BestFit follows the authored polygon order instead (§17 addendum).
- H: sprite culling is off (two-sided), so winding doesn't affect visibility.

**§17 addendum 3: sprite draw path per render mode (C)**

**Mode source:**
- Dynamic data +0x7C = **SpriteEmitterRenderMode**, copied into the fill parameters by `0x83055D08` (sprite) / `0x83055D98` (SubUV) as `piVar33[4]`.
- The SubUV wrapper also sets 1/SubImages_H and 1/SubImages_V and the stride 0x58 (+0x10 with a dynamic parameter); the sprite wrapper uses stride 0x40 (+0x10).

**Buffer allocation (`0x830746D0`, N = particles to draw):**

| Mode | Vertices | Primitives | Index buffer |
|---|---|---|---|
| **Quad** | 4N | **N** | **none allocated** (fill `piVar33[0xB]` = 0) |
| **Octagon** | 8N | 6N triangles | 6N × 3 u16 |
| **BestFit** | maxVC × N (maxVC = largest VertexCount over the emitter's polygons) | (maxVC − 2) × N | sized to match |

**Primitive type (mesh batch, sprite renderer `0x8304A1D0`):** bits 26–27 = **3 (PT_QuadList, Xenon) when render mode == Quad**, else 0 (PT_TriangleList).

**Consequences:**
- **Quads always draw as an index-free quad list** (4 vertices per particle, the corner order of §17).
- The quad index code in the fill (§17 addendum 2) is never reached in practice.
- Octagon and BestFit draw as indexed triangle lists with the triangulations of addenda 1–2.

### §12 addendum 3: spawned-actor sounds (SY) (C from script/CDO unless marked)

**TnBarrierSpawnable** (BARRIER_LP / BARRIER_RETRACT):
- **Loop:** `Initialize` (from SetBlueprint on the server, and from ReplicatedEvent('BarrierBP') on clients) plays SpawnAnim, then `PlaySound(ActiveLoopSound, bNotReplicated = false, bNoRepToOwner = false, bStopWhenOwnerDestroyed = true)`.
  - It starts **at spawn**, together with the raise animation, not once the barrier is fully raised.
  - It is positional at the barrier and **stops when the actor is destroyed**.
  - H: a client may hear both its own call and the server-replicated one.
- **Retract:** `TakeDamage` → when Health ≤ 0 (or a flashbang hits) → `PlaySound(DestroySound, false, false, false)`, replicated to everyone, then fade-out and destroy.
  - **Lifetime expiry goes through the same path:** server Tick applies `TakeDamage(DegenRate·dt)` every tick, so it plays on both damage and timeout.
  - **No retract sound** on `ForceFadeout`: TnAbilityBarrier re-use, or the owner placing a new barrier.
  - Melee damage is ignored.
  - Quirk: further non-melee hits while fading re-trigger the retract.

**TnSentryPawnAbility** (SENTRY_ACTIVATE_LP / SENTRY_ACTIVATE_POSTDEPLOY):
- **Idle loop:** `ApplySentry` (deploy) → `IdleAudioComponent = CreateAudioComponent(IdleSound, play, stopWhenOwnerDestroyed)`. It is attached to the sentry and loops until **`PlayDying` → FadeOut 0.25 s** (clients via the `bStopIdleSound` replicated toggle).
- **Death triggers:** health ≤ 0, Lifetime drain (30 s CDO), or master dead/dying → `Kill`.
- **Activate:** `EnemyAcquired` → `PlaySound(ActivateSound)` with default args (replicated, positional), **every time** an enemy is acquired.
- **No dedicated death sound field.** H: destruction audio comes from the Destructible (`Sentry_DSYS` …).
- **Weapon:** blueprint `WeaponClass`:
  - Default_TURRETDEF → `TnWeaponDefaultSentryAbility`;
  - Rocket → `TnWeaponRocketSentryAbility`;
  - Repair → `TnWeaponRepairSentryAbility`.
  - Fire audio is that weapon's normal path (TnWeapon → HmWeaponMesh PlayEvent / WeaponEventSounds).

**TnAmmoCratePickup / TnDecoyTrap PickupSound:**
- Engine `Inventory.AnnouncePickup` → `Other.PlaySound(PickupSound)` with default args: **positional at the picker, replicated to everyone relevant**, once per pickup.
- Paths: DroppedPickup.GiveTo / PickupFactory.
- The ammo crate also plays `PickupObtainedDialog` via the dialog manager.
- The decoy trap's PickupSound = **DECOY_TRAP_EXPLODE**, played at the victim who picks it up.

**TnGuidedMissile:**
- The sounds come from its **projectile mesh** `WEP_GuidedMissile_p.GuidedMissile_PROJMESH`:
  - **FlightSound** = `BL_WPN_GUN_GUIDED_MISSILE.SHOOT_TRAIL`: `HmProjectile.ClientSpawnFlightEffect` → CreateAudioComponent + Play, attached to the missile. It is faded out over 0.25 s in `SpawnExplosionEffect`.
  - **ExplosionSound** = `EXPL_IMPT_WORLD`: `SpawnExplosionEffect` → `PlaySound(…, bNotReplicated = true)` (local on each machine).
  - FX: Trail_FusionCannon_FX / Exp_GenericLvl_LRG_FX.
- `TnGuidedMissile` script has **no** sound fields and **no** guide-camera loop. U: any camera-side audio (post-process / mixer) was not found.
- Its ability animation adds `SHOOT_BUILDUP` (§12 addendum).

**§12 addendum 4: sentry destruction audio** (C from data/script; H where marked)

**Destructibles** (`WEP_SentryAbility_p` Sentry_DSYS / SentryRocket_DSYS / SentryRepair_DSYS, all the same shape): one piece, "Turret".
- **Healthy** state: InitialHealth **135**.
  - Effects: the animated sentry mesh; the type FX (SentryAbility_NoUpgrade_FX / UpgradeRocekts_FX / UpgradeHeal_FX, at +240 Z, **terminated on state exit**); and the targetable component.
  - It transitions to **Destroyed** on `HmGenericDamageDestructionTrigger`.
- **Destroyed** state:
  - **HmSoundDestructionEffectFactory, Cue = `BL_TRANS_POWER.SENTRY_EXPL`**, TerminateSoundOnExitState = false;
  - particles **FX_OmegaSupremeAE_p.FX.OS_Death_LRG_FX**.

**Playback** (`HmSoundDestructionEffect.BeginEffect`):
- `AttachingActor.CreateAudioComponent(Cue, bPlay = false, bStopWhenOwnerDestroyed = TerminateSoundOnExitState)`, then `bAutoDestroy = true`, `Play()`.
- It is a one-shot **attached to the sentry**, positional, and **not stopped** on state exit or actor destruction (both flags false).
- H: played locally on every machine that runs the destructible's state change (server, and clients via destructible state replication).

**Triggers:**
- Damage to 0, and the **Lifetime drain** (`TnSentryPawnAbility.Tick` → `DestructibleComponent.NotifyTrigger(drain, HmGenericDamageDestructionTrigger)`), both go through Healthy → Destroyed, so both play **SENTRY_EXPL + OS_Death_LRG_FX**.
- H: the master-death `Kill()` path was not traced to the destructible transition.
- The idle loop fades separately (`PlayDying`, 0.25 s).
- The actor persists for `LifeSpanAfterDeath` 5 s (Default/Repair blueprints).

**§12 addendum 5: sentry master-death `Kill` path (C)**

**`TnSentryPawnAbility.Tick`** (server): master none, dying or dead → **`TnSentryPawn.Kill`**.

**`Kill`:**
- `DestructibleComponent.NotifyTrigger(GetHealthMax(), HmGenericDamageDestructionTrigger)`: a **full-health generic-damage trigger**, so the destructible goes **Healthy → Destroyed** and plays **SENTRY_EXPL + OS_Death_LRG_FX**, the same as damage and lifetime drain;
- then `HandleDeath(none, none, 0)`.
- `Kill` is a no-op in the Dying and WaitingForRevival states, so there is no double trigger.

**`HandleDeath`:**
- `NotifySentryKilledObservers`, then: revivable → WaitingForRevival, else `Died`.
- **Ability sentries are not revivable** (`IsRevivable` is unset in Default / Rocket / Repair_TURRETDEF).
- With Killer == none, no sentry-kill stat is credited.

**Result:** all three ends (damage, lifetime, owner death) play the same destruction audio and FX.

**Linger time:** `LifeSpanAfterDeath` is 5 s for Default and Repair. **Rocket_TURRETDEF does not author it**, so it inherits the TnSentry CDO **30 s**.

**§12 addendum 6: sentry linger time after death (C)**

**Mechanism:**
- `TnSentryPawn.ApplySentry` copies `LifeSpanAfterDeath` from the blueprint into the pawn.
- `TnSentryPawn.Dying.BeginState` sets **`LifeSpan = LifeSpanAfterDeath`**, so the actor auto-destroys after that many seconds.
- In Dying, `TakeDamage`, `Kill` and `StartFire` are no-ops.

**Values:**
- The TURRETDEF blueprints have no archetype, so their template is the `TnSentry` class default, and cooked UE3 objects serialise only properties that differ from it.
- **Rocket_TURRETDEF therefore has LifeSpanAfterDeath = 30 s** (the CDO value; it is absent because it equals the default).
- Default_TURRETDEF and Repair_TURRETDEF author **5 s**.

**During the linger:**
- The Destroyed destructible state carries only the explosion FX and sound.
- The Healthy-state type FX is terminated, and the targetable component lives only in the Healthy state.
- So the dead sentry is not targetable. H: what remains visible depends on the Healthy-state animated-mesh effect's exit behaviour; not traced.

**§12 addendum 7: what is visible while a sentry lingers** (C for script; H where marked)

**Body:**
- `TnSentryPawn.ApplySentry` binds `self.Mesh = DestructiblePiece.GetActiveMeshComponent()`, the Healthy state's **HmAnimatedMeshDestructionEffect** mesh (WEP_SentryDeploy_SKEL).
- The yaw/pitch skel controls and the weapon socket all live on it.

**On death** (`HmDestructiblePiece.TransitionToState` → `ExitCurrentState` → `HmDestructionState.EndEffects`), every Healthy-state effect's `EndEffect` runs:
- **`HmMeshDestructionEffect.EndEffect` detaches the sentry mesh from the actor unconditionally**, so the **turret body vanishes at the moment of death**;
- the type FX (NoUpgrade / Rockets / Heal) is deactivated (`TerminateEffectOnExitState`);
- the targetable component goes with the state.

**Destroyed state:** begins **OS_Death_LRG_FX** and **SENTRY_EXPL**. Neither is ended during the linger (the Destroyed state is never exited).

**Weapon (H):** it is socket-attached to `self.Mesh` and goes away with it (UE3 detaches socket attachments with their parent skeletal mesh). Its fire effects stop because Dying ignores StartFire.

**So during `LifeSpanAfterDeath`** (5 s Default/Repair, 30 s Rocket), **only the explosion particle (and the tail of the one-shot sound) is visible**. The actor is otherwise an invisible, untargetable, damage-ignoring shell until LifeSpan destroys it (H for the particle: it is not deactivated by the state, so it ends naturally or with the actor).

**§12 addendum 8: sentry weapon detaches with the body (C)**

**Attach (script):**
- `HmWeaponMesh.Attach(owner, BaseMesh, SocketName)` → `BaseMesh.AttachComponentToSocket(weaponMesh, SocketName)`, with BaseMesh = the pawn Mesh.
- For the sentry that is the destructible Healthy-state skeletal mesh (§12 addendum 7), socket = blueprint `WeaponSocketName` ("WeaponSocket" CDO).

**Native:**
- `USkeletalMeshComponent` keeps socket attachments at **+0x264** (count +0x268, 0x30-byte entries).
- `execDetachComponent` (`0x82DA0208`) removes one entry and calls `ConditionalDetach(child)` (`0x82E29290`).
- **The skeletal component's virtual Detach `0x82D762F0`** (in four skeletal-component vtables) calls the parent class's Detach, then **`ConditionalDetach(child, bWillReattach)` for every socket attachment**.

**Therefore:** when the Destroyed transition's `HmMeshDestructionEffect.EndEffect` detaches the sentry mesh from the actor, the socket-attached **weapon mesh is detached in the same call** and stops rendering. Upgrades §12 addendum 7's weapon point from H to **C**.

**§12 addendum 9: sentry timing on owner death** (C unless marked)

**Two mechanisms:**
1. **`TnSentryPawnAbility.Tick`** (server, every frame): `GetMaster()` = `TnAiSentryController._KillOwner.Pawn` (the owner's Controller, set at spawn). If none, IsDying or IsDead, it calls **`Kill()`**: the destructible goes to Destroyed (explosion FX + SENTRY_EXPL), then Died / Dying with LifeSpan = LifeSpanAfterDeath.
   - The owner's `HmPawn.Dying.BeginState` calls `Controller.PawnDied` immediately. H (stock UE3): the controller unpossesses, so `GetMaster()` returns none. Either way the IsDying/IsDead test fires.
   - **So the sentry explodes on its first server tick after the owner dies: same frame or the next.**
2. **`TnAbilitySpawnSentry.SpawnSentry`** also registers the sentry in the owner's **`DestroyOnDeathActors`**. That list is processed only in **`TnPawn.Destroyed`** (the owner's pawn *actor* being destroyed), which calls `DestroyActor()` on each entry.
   - This happens after the explosion, and it **cuts the sentry's (invisible) linger short** to the owner corpse's lifetime.
   - Owner corpse lifetime: `HmPawn.Dying.BeginState` clamps LifeSpan to ≤ 1 s **on a dedicated server** (bTearOff) or below KillZ.
   - U: on a listen server or offline no script sets a corpse lifespan (TnPawn defaults author none). The engine's `Pawn.Dying.BeginState` (LifeSpan 2 / 5 s visibility timer) is overridden and not called.

**Other ends:**
- Re-casting Spawn Sentry calls `ActiveSentry.Kill()` on the old sentry first, so it explodes too.
- `ForceEndAbility` also calls `Kill()`.

**H (visual):** if the sentry actor is destroyed early (mechanism 2) while OS_Death_LRG_FX is still playing, whether the particle is cut depends on whether the destructible effect's PSC is owned by the sentry actor. Not traced.

**§12 addendum 10: player corpse lifespan (and the sentry DestroyOnDeath cut)** (C unless marked)

**Mechanism (`TnDeathPlayer`, created by the form's death; `Activate` at death):**
- It picks a death entry (`TnDeathBlueprint`) and starts the motion and modifiers.
- It starts **`_GibTimer` = random in `TotalTime` [Min, Max]**; for non-player pawns it uses `TotalTimeForAI` if that is non-zero.
- When the timer fires: **`Owner.Gib`** → `TnPawn.Dying.Gib`. If LifeSpan is still 0, it sets **LifeSpan = 1.0**, hides the robot and vehicle meshes, runs the form's `PlayGib` (gibs, debris and decal via `Deactivate`) and a camera shake for nearby local players.
- **Corpse removed ≈ TotalTime + 1 s after death.**

**Authored TotalTime (`TR_Deaths_p`):**

| Death set | TotalTime (s) |
|---|---|
| SharedRobotDeaths | 1.25–3.5 (entries 1.25, 1.25–1.5, 1.25–2, 1.25–2.5, 1.25–3, 1.5, 1.5–2.5, 1.5–2.75, 1.5–3.5) |
| BruteRobotDeaths | 2–4 |
| HoloBrute | 1–2.5 |
| SharedCarDeaths | 0.2–0.75 |
| SharedVehicleDeaths | 0.3–0.4 |
| SharedJetDeaths | 4–5 (AI the same) |
| SpiderDeaths | 0 (gib on the first tick) |

- Entries without a value use the struct default **1.0**.

**Correction to addendum 9:**
- `HmPawn.Dying.BeginState`'s dedicated-server rule is `LifeSpan = FClamp(LifeSpan, 0, 1)`. With the default LifeSpan 0 (none) it **stays 0**, so it does **not** cap the corpse at 1 s; it only shortens an already-set lifespan.
- The corpse lifespan is set by the gib timer on every net mode. H: TnDeathPlayer also runs on a dedicated server.

**Therefore** the owner's `TnPawn.Destroyed` (which `DestroyActor`s the sentry from DestroyOnDeathActors) runs **≈ TotalTime + 1 s after the owner's death**: about 2.25–4.5 s for a robot owner, 1.2–1.75 s for a car owner, 5–6 s for a jet.
- That cuts the Default/Repair sentry's 5 s linger only for long robot deaths, and the Rocket sentry's 30 s linger always.
- Both are invisible (§12 addendum 7); the explosion FX may be cut (H, §12 addendum 9).

**§12 addendum 11: announcer, kill-streak, overshield and wall-hit sounds** (C from script/CDO unless marked)

**`TnKillstreakActivatedMessage.GetColoredString`** (runs on each receiving client):
- Role:
  - **Self** if `LocalPlayerPRI == RelatedPRI_1` (the activator);
  - else **Friendly** if `TnMessageHelpers.OnSameTeam(local, activator)`;
  - else **Enemy**.
- That role's cue is chosen. If it is none and `FactionAnnouncementSound` is non-empty (and the activator has a team), the cue is `FactionAnnouncementSound[activatorTeam]`.
- Then `TnWorldInfo._Announcer.PlayEvent(EventSound)`. **A role with no cue and no faction list is silent.**

**`TnAnnouncer`:**
- `PlayEvent(e)` → `SoundEventSet.FindSoundCue(e)` → `Play(cue)`; `Play(none)` returns.
- Playback is on an `HmDialogComponent` attached to the announcer owner, voiced by `Team0DialogCharacter` / `Team1DialogCharacter` (via `SetTeam`). H: non-positional dialog.
- `PlayInternal`:
  - if the dialog component is idle → play immediately;
  - if it is playing the **same** cue → dropped (and the queue cleared);
  - otherwise the cue goes into **one queue slot** if its SoundNodeRoot Priority ≥ the queued cue's (an empty slot always accepts); a lower-priority cue is dropped.
  - `Tick` plays the queued cue when the component is free.
- **The current line is never interrupted.**

**Kill-streak earn / acquire:**
- `TnPlayerController.AcquireKillstreak` only adds the class and updates the current id: **no sound**.
- `TnKillStreakAnnouncer` broadcasts `TnKillStreakMessage` at streak lengths **3, 5, 7, 10**, and `TnKillStreakEndedMessage`. **Both are text-only** (no sound fields).
- U: any GFx/HUD-side "available" sting was not traced (none in script).

**`TnPlayerPawn.OvershieldOffSound`** (`BL_HUD_INTERFACE.OVERSHIELD_POWER_DOWN`):
- `TnPlayerPawn.Tick`: when `OverShieldHealth == 0` while the overshield material (type 2) is active → `PlaySound(OvershieldOffSound)` (default args), then the material stops.
- It fires on **any** end: depletion by damage or expiry. It is positional at the pawn.
- H: Tick runs on server and clients, and the server PlaySound also replicates, so remote players may hear it twice.
- `TnAiPawn` has an equivalent.

**`TnPawn.HitWallSound`** (`BL_MELEE_IMPT.MTL_DASH_WALL_IMPT`):
- `TnPawn.InRobotForm.HitWall`: **only in robot form while `IsDodging`** → `PlaySound(HitWallSound)` (default args, positional), plus `StartCameraShake(_Blueprint.HitWallCameraShake)` for a player controller, then `RobotForm.HitWall()`.
- Any HitWall during a dodge triggers it (no speed or angle condition in script).
- **Faction list indexing (C):** the index is the **activator's** team (`RelatedPRI_1.GetTeamNum()`; Autobots TeamIndex 0, Decepticons 1), never the receiver's.
  - `TnKillstreakActivatedTeamAbilityJammer` = [MP_**Decepticon**AbilitiesJammed, MP_**Autobot**AbilitiesJammed]: an Autobot activator announces "Decepticon abilities jammed" (the victims), which is deliberate.
  - GuidedMissile / ImprovedOrbitalRecon lists name the activator's own faction.
  - The faction cue is used only where the role cue is none. So for GuidedMissile, Self hears MP_OmegaMissleOnline while every other receiver (friend or enemy) hears the activator-faction "fired" line. For Jammer and Beacon 2.0 everyone, including the activator, hears the faction line.

**§12 addendum 12: death sounds and granted-weapon sounds** (C from script/data unless marked)

**Vehicle death sound:**
- `TnVehicleForm.OnPlayDeath` (from `TnPawn.Dying.BeginState` → `_CurrentForm.PlayDeath`) starts the `_DeathPlayer`. If `_Blueprint.DeathSound` is set it plays `_OwnerPawn.PlaySound(DeathSound, bNotReplicated=true)`.
- **Vehicle form only** (`TnPawn.PlayDying` → `VehicleDying` vs `RobotDying` state by current form).
- The Dying path runs on the server (Died → PlayDying) **and on every client** via bTearOff → `Pawn.TornOff` → PlayDying.
- So each machine plays it **locally, positional at the wreck**: everyone with the pawn relevant hears it once, including the killer. A dedicated server is silent.

**Robot form:**
- `TnRobotForm.OnPlayDeath` has no sound.
- The only robot death sound is the death-entry modifier `TnDeathModifierPlaySound` → `_Owner.PlaySound(Sound)` (default args, positional). It is authored only on the **melee** death entries (`TnDeathTypeMelee`, TotalTime 1.5–2.75) of `SharedRobotDeaths` and `HoloBruteRobotDeaths`, with Sound = `BL_LVL_HUD_INTERFACE.hud_melee_death_disintegrate`.
- No Delay is authored, so it plays at death start. H: it can play twice on remote clients (local run plus the server's replicated PlaySound), the same as OvershieldOffSound.
- `TnPlayerController.DeathSound` is played only in `OnCampaignGameOver` (with GameOverMusic and GameOverMixerPreset): campaign only. There is no other MP "power down" sound in script.

**Granted weapons:**
- `TnAbilityCreateInventory.ServerTriggerAbility` (TnAbilityPoke → `TransContent.TnWeaponPoke`; TnKillstreakSpawnRocketTurret → `TransContent.TnWeaponRocketTurretKillStreak`) → `Pawn.CreateInventory` → `InventoryManager.CreateInventory` / `AddInventory` → `GivenTo` / `ClientGivenTo`.
- **No sound**: `TnWeapon.GivenTo` only sets the weapon-data type. `PickupSound` (`TnWeaponMesh.PickupSound`) and `PickupObtainedDialog` play only in `TnWeapon.AnnouncePickup`, which is called only by pickup factories and dropped pickups.

**§12 addendum 13: grenade toss sounds** (C unless marked)
- `HmWeaponMesh.EWeaponEvent` (from the HM_Engine enum export): 1 = **WP_Fire**, 22 = **WP_NoAmmoFire** (0 Default, 4 Reload, 6 Equip, 13 Overheat, 19 LowAmmoFire, …).

**Input path:**
- `TnPlayerController.PlayerWalking.TossGrenade` runs on the owning client.
- If the current weapon is the heavy turret type (WeaponType 5) **or** the pawn is downed or reviving → `GrenadeBag.PlayDryFireSound()`.
- Otherwise `TnGrenadeBag.TossGrenade`: `CanToss = HasAmmo(0) && !IsTimerActive()`. If false → `PlayDryFireSound()`, i.e. **out of ammo and the toss cooldown both give the dry-fire sound**.

**Successful toss: `PerformToss`** (owning client; a listen-server host for its own pawn):
- `LocalToss` (local toss animation on an autonomous proxy) → ConsumeAmmo (client prediction) → **`GrenadeBagMesh.PlaySoundEvent(WP_Fire)`** → `SetTimer(GetFireInterval(0))` (the cooldown) → reliable server RPC `ServerTossGrenade`.
- The server consumes ammo, `GrenadeThrower.ServerToss` (replicated toss animation; SpawnGrenade after TossDelay at the TossSocket), ThrowDialogNotify, the shots-fired stat and ExposeSelf.
- No sound is played on the server path.

**`PlayDryFireSound`:** `GrenadeBagMesh.PlaySoundEvent(WP_NoAmmoFire)`.

**`HmWeaponMesh.PlaySoundEvent`:**
- It looks up the event in `WeaponEventSounds`. For a one-shot: `GetSoundOwner().CreateAudioComponent(cue, bPlay=true, bStopWhenOwnerDestroyed=true)`, i.e. a **local** audio component positioned at the sound-owner actor (H: the pawn). It is not replicated.
- **So the toss WP_Fire and the dry fire are heard only by the tossing player.**
- U: remote players may hear sounds from AnimNotifies in the replicated toss animation or from the grenade projectile's own spawn and flight sounds (not traced).

**§12 addendum 14: grenade projectile sounds** (C unless marked)

All four cues live on the projectile's `HmProjectileMesh` (`TnProjectileMesh`) and are played with **bNotReplicated = true / a local audio component**. Each machine that simulates the projectile plays them itself, positional at the grenade. A dedicated server is silent.

**Flight loop: `HmProjectile.ClientSpawnFlightEffect`:**
- Skipped on a dedicated server. It creates the FlightEffect PSC and `CreateAudioComponent(FlightSound, bPlay=false, bStopWhenOwnerDestroyed=true).Play()`.
- Started by `Init` on the spawning machine (the server or listen host).
- On clients: `ReplicatedEvent('Instigator')` (pawn-thrown); or `PostBeginPlay` when `SpawnsFromNonPawn`.
- So everyone hears the flight loop from spawn.

**Bounce / fuse: `TnProjectileGrenadeBase.HitThing`** (from HitWall / Bump / ProcessTouch; overrides the HmProjectile HitWall bounce sound):
- If `ExplodeWhenHittingPawn` and a pawn is hit → Explode.
- Otherwise, on the **first** contact (LifeSpan == 0): LifeSpan = random(FuseTime), the AI grenade stimulus fires, and **`PlaySound(FuseSound, true)`**.
- Then `OnHitThing` reflects velocity × BounceDampening (stopping below LowSpeedThreshold 500, i.e. speed² < 500) and **`PlaySound(BounceSound, true)` on every contact**, including the first and the one that stops it.

**Explosion:**
- Fuse expiry → LifeSpan destroy → `HmProjectile.Destroyed` → Explode → `SpawnExplosionEffect`. A server TearOff → client `TornOff` → Explode; `bExploded` guards against a double.
- Not on a dedicated server: the ExplosionEffect comes from the emitter pool, the flight loop **fades out over 0.25 s** (auto-destroy), and `PlaySound(ExplosionSound, true)`.

**Authored (`*_PROJMESH`):**

| Projectile mesh | Flight | Fuse | Bounce | Explosion |
|---|---|---|---|---|
| FlashBang (EMP) | EMP_FLIGHT_LP | EMP_FUSE_BUILD | SHELL_BOUNCE_LIGHT | EMP_EXPL_IMPT_WORLD |
| GrenadeSkill (Magma/Flak) | MAGMA_FLIGHT_LP | MAGMA_FUSE | SHELL_BOUNCE_HEAVY | MAGMA_EXPL_IMPT_WORLD |
| HealGrenade | HEAL_FLIGHT_LP | none (silent) | SHELL_BOUNCE_LIGHT | HEAL_EXPL_IMPT_WORLD_PROTRACT |
| Grenade_Martyrdom | GL TRAIL_LP | none | SHELL_BOUNCE_HEAVY | GL EXPL_IMPT_WORLD |
| GrenadeLauncher | TRAIL_LP | PROJ_IMPT | SHELL_BOUNCE_HEAVY | EXPL_IMPT_WORLD |
| LargeExplosive | — | — | SHELL_BOUNCE_HEAVY only | — |

- Bank names: grenade cues are BL_WPN_GRENADE.*; GL cues are BL_WPN_GUN_GRENADE_LAUNCHER.*.
- FlashBang_Vig_PROJMESH is the same as FlashBang plus SpawnsFromNonPawn.
- H: which projectile class uses which PROJMESH (the per-class Mesh pointer was not traced for every class).

**§16 addendum 1: SubUV UV scale (corrects the direct-mode "texel units" H)** (C unless marked)

**Fill context:** the fill's context is set up by `0x83055D98` (the only caller of `0x8305F7D8`), at dynamic data +0xA0:
- ctx[0] = the dynamic data;
- **ctx[1] = 1.0 / (float)data+0x94**, **ctx[2] = 1.0 / (float)data+0x98**;
- vertex stride 0x58 (+0x10 with the dynamic parameter, flag 0x8000000).
- Dynamic-data layout +0x90 SubUVDataOffset, **+0x94 SubImages_Horizontal**, **+0x98 SubImages_Vertical**, +0x9C bDirectUV. This matches stock UE3 `FDynamicSpriteEmitterReplayDataBase` order (H: field names by that match).
- (Ghidra shows the context as the return of `0x830EAD74`, which is really an FPR-save stub; the context is r3.)

**Both modes use the same scale (1/SubImages_H, 1/SubImages_V)**, and **the CPU writes full per-corner UVs**: corner c ∈ {0, 1}², written as constants 0.0 / 1.0.
- Normal: U = (⌊H⌋ + cU) / SubImages_H, V = (⌊V⌋ + cV) / SubImages_V, and likewise for U2/V2 from the next cell.
  - This replaces the old H "the shader adds corner·cellSize": the CPU already does it.
- **Direct (bDirectUV): U = (Pos.x + Size.x · cU) / SubImages_H, V = (Pos.y + Size.y · cV) / SubImages_V.** U2/V2 = U/V and Interp = 0.
  - **Position and Size are in cell units.** There is no texture-size term.

**H2H_Punch01_FX "ChamberLeft_Dup"** (2×2, Pos uniform (0,0)..(1,1), Size 0.5): UV window = [Pos/2, (Pos + 0.5)/2], i.e. a **quarter-texture (half-cell) crop at a random offset within the top-left cell area (UV 0..0.75)**. It never passes 1.

**Address mode:** Sparks_Curved_CLR authors no AddressX/Y, so the Texture2D default **TA_Wrap** applies. H: the material sampler uses the texture's address mode, as in stock UE3. It is irrelevant here since UV ≤ 0.75.
