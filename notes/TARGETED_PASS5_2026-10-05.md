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
