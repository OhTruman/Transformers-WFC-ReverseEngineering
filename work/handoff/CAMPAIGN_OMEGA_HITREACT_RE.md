# Omega Supreme specifics and robot hit reactions (answers to Gameplay, RE, 2026-10-23)

**Labels:** C = script / authored data.

Builds on CAMPAIGN_SETPIECES §1 (the Omega state machine, OmegaStatus outputs) and CAMPAIGN_BOSSES D5 (the action timings).

## 1. Omega Supreme (D5)

**Template (C):**
- OmegaSupreme_AICD → **TnOmegaSupremePawn**; ActionSet TR_OmegaSupreme_Ai_p.OmegaSupreme_AiActionSet; GoalSet
  TR_AiGoalSet_OmegaSupreme; SensorSet TR_AiSensorSet_OmegaSupreme.
- **Goals:** Kill, HealSelf, React, Emote, Idle.
- **Actions:**
  - AreaOfEffectAttack;
  - Emote;
  - EquipWeapon ×3;
  - ExposeHeart;
  - Grab;
  - HealWithGrabbedObject;
  - LockedOnShootingFrenzy;
  - LockOnBattery;
  - LockOnTarget ×3;
  - LockOnTargetWhileHoldingObject;
  - OmegaDeath;
  - RocketBarrageOmega;
  - ScanningIdle;
  - ShootLockedOnWeapon;
  - ThrowDestructible;
  - ThrowEnemy.
- **Stationary:** the action set has no move / navigate actions, so he only turns, locks on and fires. The chassis lists
  BaseGroundSpeed 1500 and 5000 HP; he can't die from health (Critical at ≤ 1 HP, SETPIECES §1).

**Arms (weapons, C):**

| Arm | Weapon data | Projectile |
|---|---|---|
| **OmegaRocketArm** (LockOn → ShootLockedOnWeapon: lock 2 s, warning 1 s, Missile_Shoot every 1–5 s) | OMEGA_Arm_AI_WEPDATA: range 30000; damage × 1.0 to 8000 UU, × 0.5 at 30000; spread 0.1–0.2 (+0.05 / shot, 2 s cooldown); instant-hit 5 (IonBlaster) as the base fire | **OMEGA_HomingRocket_AI_PROJDATA**: homing, speed 7000, **damage 25, radius 10**, TnDamageTypeOmegaRocket, life 15 s |
| **OmegaShootingFrenzyArm** (tell ShootingFrenzy_Tell, lock 2 s, every 25 s) | Omega_ShootingFrenzy_AI_WEPDATA: **interval 0.25 s**, clip 15 / reserve 45 (max 75), spread 0.03–0.08, damage × 1.0 to 7500 / × 0.5 at 30000 | **OMEGA_ShootingFrenzyRocket_AI_PROJDATA**: homing, 7000, **damage 55, radius 1500**, TnDamageTypeOmegaShootingFrenzyRocket |
| **OmegaTractorBeamArm** (LockOn grab: 4 s warning, LOS, every 20 s → Grab → ThrowEnemy) | OMEGA_Arm_AI_WEPDATA | the grab itself: **1000 damage on release** (TnDamageTypeOmegaTractorBeamGrab, impulse 1e6) at **5.3 s** of Melee_ClawCrush_Omega |
| RocketBarrageOmega (every 15 s) | – | OMEGA_MangaRocket_AI_PROJDATA: 6000, **damage 40, radius 40** (OmegaRocket); fires OmegaStatus 5 |

- AoE: Melee_AOE within **3200 UU**.
- **Targets:** RoundRobin +3 for 7 s; downed −10; players who damage his sentries draw his attention (SentryGroupDamage); his own
  sentries are excluded.

**The battery cycle** (blueprint DES_NEU_Battery_p.DES_OmegaRobotBattery, C):
- **BaseBattery piece:** `EmptyMesh` (0.1 s) → **`FillingLiquid` (15 s, animated fill)** → **`FullMesh`**. Only a FullMesh battery
  can be taken.
- **The tractor beam** applies `TnTractorBeamDestructionTrigger` when he grabs it → `FullNonCorruptedMesh` (10 damage to dependents).
  The Kismet "Grabbed Battery" input then hides the placed battery.
- **The CorruptedSpikes piece** (5 HP): **`TnCorruptionDestructionTrigger` → "spikes"**. That trigger is carried by
  **TnDamageTypeCorruption** (its DestructionTrigger). In D5 it's applied by the player's interact `TnInteractCorruptOmegaBattery` →
  Kismet `SeqAct_TnCorruptOmegaBattery` (+ CorruptBatteryMaterial). A notification trigger then advances the spikes.
- **Heal:** he grabs a FullMesh battery while **Wounded** (LockOnBattery → HealWithGrabbedObject).
  - A **clean** battery: the "healthy heal" anim, then **`Sentries.Heal()`** (sentries vulnerable, healed, kill count reset) →
    **Healthy**. There's no HP number: he's invulnerable in Healthy and the "heal" is the sentry reset.
  - A **corrupted** battery: the corrupt heal anim, `Omega.Corrupt()`: **Corrupted**, vulnerable; corruption spikes attach at 0 / 1.5 /
    3.0 s.
- **To win:**
  1. destroy the 4 sentries (Healthy → Wounded);
  2. corrupt the battery he'll grab;
  3. damage him to ≤ 1 HP while Corrupted (→ Critical);
  4. destroy the heart armor (HeartShell) → OmegaDeath.
- **Kismet expects back:** the TnSeqEvent_OmegaStatus outputs 0–9 (SETPIECES §1), which drive the battery spawns, the jet waves and
  the post-process switch (Critical → CAMPAIGN_POSTPROCESS §1). `SetOmegaStage` is used for the checkpoint resumes.

## 2. Robot hit reactions (C, `TnHitReactionAnimator`)
- **Where:** each robot form whose blueprint has a `HitReactionBlueprint` creates a TnHitReactionAnimator on the
  **TnAdditiveAnimatorService**, the additive slot.
  - `TR_HitReactions_p.RobotHitReactions` is used by 54 robot defs: Normal_F / Normal_B / Turret_F / Turret_B
    (`HitReaction_React_Normal_F`, …), blend in 0.05 s, **out 0.4 s**.
  - `BruteRobotHitReactions` (8 defs): Normal F / B only.
  - **Vehicle forms have none.**
- **Trigger:**
  - `TnPawn.PlayHit` (from TakeDamage) records the hit (location, momentum, bone, damage type, `IsBlocking` = shield active);
  - **only when the hit component is the pawn's skeletal mesh** → `ClientPlayHit` → `Form.PlayHit` → `Animator.Play(HitInfo)`.
- **Gate (`CanPlay`):**
  - not interacting;
  - not holding a WeaponType 7 weapon;
  - **`_CanPlayHitReaction`**, which for AI is set per GOAP action: false while the action's CharacterState has bit 256;
  - **and the damage type's `ShouldCauseHitReaction`**: default **true**; false for TnDamageType (base), AudioBlast, DecoyDot,
    DownedDrain, Drain, TransformDisruptorDot and HealType.
  - **No damage threshold and no cooldown:** every qualifying hit re-enqueues the additive clip.
- **Which clip:**
  - **front vs back only** (no left / right): front if `(Momentum << Owner.Rotation).X > 0`;
  - type: **shield blocking → the Shield anims** (unset in both blueprints, so nothing plays); **holding a heavy (WeaponType 5) →
    Turret F / B**; else **Normal F / B**.
- **Playback:** EnqueueLocalAnimation (local, not replicated: each machine plays it from its own ClientPlayHit), MaskType 0, the
  mesh's root-motion modes, override 0.
- **Players and AI both** play them (same robot forms). The HitRX grunt is a separate AnimNotify_Dialog on the clips / anims.
