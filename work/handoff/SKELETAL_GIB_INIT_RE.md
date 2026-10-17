# Skeletal gibs: count, gate, pose, rotation, velocity

WFC RE lane, 2026-10-17, for Gameplay patch 2 part 2.

Sources:
- script decompiles in `work/script/decomp`: TnSkeletalGibSpawner, TnDeathPlayer, TnDeathFactory, TnPawn, TnRobotForm,
  TnVehicleForm, HmSkeletalRigidBody, TnSkeletalRigidBody(Modifier*), Core.Random;
- authored.db;
- native decompiles noted in §7.

## 1. Call chain (CONFIRMED)

1. `TnPawn.Dying.Gib` hides the robot and vehicle meshes, sets LifeSpan 1, drops the cylinder's rigid-body blocking, triggers the
   explode-on-death buffs, then calls `_CurrentForm.PlayGib()`.
2. `TnTransformerForm.PlayGib` calls `OnPlayGib`:
   - **TnRobotForm.OnPlayGib:** `_DeathPlayer.Deactivate()`.
   - **TnVehicleForm.OnPlayGib:** `VehicleMesh.SetAnimTreeTemplate(none)`, then `_DeathPlayer.Deactivate()`.
3. `TnDeathPlayer.Deactivate`:
   - `Location = Owner.Mesh.GetSocketWorldLocation('PositionSocket')`;
   - gibs DSYS (HmDestructibleComponent at that location);
   - **`_ActiveDeath.SkeletalGibs.Spawn(Owner, Location)`**;
   - decal.

## 2. Count and gate (CONFIRMED)

1. `TnSkeletalGibSpawner.Spawn` returns early if `IsSpawnDisabled()` is true. That is the case when any of these holds:
   - `GetGameThrottle() >= 3`;
   - `Templates.Length == 0`;
   - `RandomFloat() > ChanceToSpawn` (FRand × 1).

   ChanceToSpawn defaults to 1.0 and no spawner overrides it, so the gate always passes when not throttled. **It is evaluated
   whether or not Impulses is empty.**
2. **It then spawns exactly one actor:** `SkeletalGib = Owner.Spawn(TnSkeletalRigidBody, , , Location)`, with
   `Index = Rand(Templates.Length)`.
3. The SharedRobot / BruteRobot / SecurityDrone spawners list GIB_Body and GIB_LowBody2, so each death spawns **ONE of them at
   50/50, not both**. SoldierTankRobot uses GIB_TankBody / GIB_TankLowBody. SpiderDeaths and HoloBruteRobot have no templates, so
   they spawn none.
4. **Template sources:**
   - `TnDeathFactory.CreateDefaultDeath` clones the blueprint's SkeletalGibs, then calls `Owner.AddDefaultSkeletalGibTemplates`.
     In robot form that returns early. In vehicle form it appends `_VehicleForm._Blueprint.DefaultSkeletalGibTemplate`, the hull.
     39 form blueprints author it.
   - A custom death with `UseCustomSkeletalGibs` replaces the spawner (`TnDeathFactory.AddCustomDeath`).

## 3. Spawn transform (location CONFIRMED; rotation HIGH)

- **Location:** the dying pawn's PositionSocket world location.
- **Rotation:** Spawn passes no rotation. The UE3 Actor.Spawn default is the spawning actor's Rotation, which here is the dying pawn
  (`Owner.Spawn`). See §7 for the native check.

## 4. Initial pose: the gib mesh's reference pose (CONFIRMED by script and data)

`InitializeMesh(Template, Owner, SkeletalGib.SkeletalMeshComponent)` runs these steps in order:

1. `SetSkeletalMesh(MeshTemplate)`
2. `SetPhysicsAsset(PhysicsTemplate, bForceReInit=true)`
3. `SetHasPhysicsAssetInstance(true)`
4. `WakeRigidBody()`
5. `Direction = RandomVectorInCone((0,0,1), ImpulseConeHalfAngle·π/180)`
6. per-impulse `AddLinearVelocity`
7. optional velocity transfer
8. optional radial force
9. `_CharacterApplier.ApplyColorsToMesh`

- No step reads or copies the dying pawn's bones.
- The gib actor's component (`TnSkeletalRigidBody.DefaultRigidBodyComponent`, inheriting from HmSkeletalRigidBody's) has no
  AnimTreeTemplate and no AnimSets. It has `bUpdateKinematicBonesFromAnimation=false`, `PhysicsWeight 1.0`, RBChannel
  `RBCC_EffectPhysics`, and doesn't collide with the Vehicle or EffectPhysics channels.
- So the bodies start in the **reference pose of the gib mesh**, at actor origin = PositionSocket, oriented by the pawn's Rotation.
- **Ref skeletons:** `ExtractedAssets/content/TR_Death_Gibs_p/Skeletal/GIB_Body_SKEL.gltf` (8 joints, root C_Reference_XR) and
  `GIB_LowBody2_SKEL.gltf` (11 joints, root C_Root_Reference_XR). In the export, bone names carry the `_XB` / `_XR` suffixes.

## 5. Initial velocity (CONFIRMED)

- `Direction` is always computed, which costs two FRand calls (phi, theta). It is used only inside `foreach Template.Impulses`, so
  **with empty Impulses the cone has no effect.**
- `TransferOwnerVelocityToMesh` runs only if `TransferVelocityMultiplier != 0`. It does
  `v = Owner.Mesh.GetRBLinearVelocity() × mult`, then `AddLinearVelocity(v, , bone)` for every name in `GetBoneNames`.
- `RadialForceStrength`: `Strength = RandRange(Min, Max)`. If it is non-zero, the spawner calls
  `AddRadialForce(Bounds.Origin, Bounds.SphereRadius, Strength, falloff 0)`.
- **Robots:** multiplier 0 and no RadialForceStrength, so the gibs start at rest and gravity is the only input.
- **Vehicles (hulls):**
  - multiplier 0.75 (StarscreamBoss 0.7);
  - radial force U(300, 700) for car and tank, {700, 400} for jet;
  - EnergyDeathMaterial modifier: car / tank Delay U(0.5, 1), TransitionTime 4.5; jet no delay, TransitionTime 6.
    - OnStart sets the owner's EnergyDeathMaterial on all elements, then calls ApplyColorsToMesh.
    - OnTick ramps the `Defrag` scalar from 1 to 0 over TransitionTime.

## 6. Lifetime (CONFIRMED)

1. `SetLifeSpan(RandRange(LifeSpan))` starts a timer that calls `LifeSpanExpired`.
2. LifeSpanExpired hides the mesh and turns actor collision off.
3. If there is a DestroyedEffect, it plays it and destroys the actor when the effect finishes; otherwise it destroys immediately.
4. Robot spawners author no Active/Destroyed effects.
5. `RandRangeFloat(Min, Max)` with Min > Max (BruteRobot {15, 5}) gives the same 5–15 range.

## 7. Native confirmation

PENDING: filled after the 04:00 headless run (natives SetSkeletalMesh 0x82C5B380, SetPhysicsAsset 0x82C5B470,
SetHasPhysicsAssetInstance 0x82C5BEE0, WakeRigidBody 0x82C7BC20, AddLinearVelocity 0x82C7B6F8, Actor.Spawn 0x82F15830,
GetRBLinearVelocity 0x82C4EE08).
