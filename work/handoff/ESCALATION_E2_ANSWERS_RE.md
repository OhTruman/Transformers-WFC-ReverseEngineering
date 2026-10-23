# Escalation E2: generators, factories, power (answers to Gameplay, RE, 2026-10-23)

**Labels:** C = bytecode / authored data / map Kismet (`next_map/MP_ESC_*_kismet.json`); H = stock UE3 / inference.

**Sources:**
- TnSurvivalGeneratorBase, TnPlayerReplicationInfoSurvival, TnPlayerControllerSurvival, HmButtonInputStateHandler,
  Engine.PickupFactory, TnPickupFactory (`work/script/decomp`);
- TnSurvivalGame (`decomp_tc/MP_ESC_BrokenHope_BASE_m.TransContent.txt`).

## 1. Item factories behind generators (C)
**Map Kismet hides them, not the CDO or the game.** Each generator sequence (e.g. `Genarators.AmmoGenerator_Seq_0`) has three
chains:
1. **`SeqEvent_PreGameplaySetup` → `SeqAct_ToggleHidden` input 0 (Hide)** on the factory.
2. **Generator `New Power Level`** (TnSeqEvent_SurvivalGenerator) → ToggleHidden **input 1 (UnHide)** → **SeqAct_Toggle input 1
   (Turn Off)** on the generator's activation **TriggerVolume**: no draining while the item is out.
3. **`SeqEvent_PickupStatusChange` "Taken"** →
   - **Hide** again;
   - **`TnSeqAct_ModifySurvivalGeneratorPower` PowerToAdd = −(the level cost)**, e.g. −50 ammo or −200 weapon. CheckPower drops
     the generator back to level 0, so it's chargeable again;
   - **Delay 2 s** → Toggle **Turn On** the TriggerVolume.

~~So a factory is purchased once per generator charge.~~ **Corrected (REVIEW_ESCALATION_E2A_RE G1):** the −cost drop re-fires
`New Power Level` (OnPowerLevelChange(false) also activates the event). That UnHides the factory again, so the item stays
out after the first purchase and the generator is merely re-chargeable.

**What "hidden" does** (Engine.PickupFactory):
- `SetHidden(true)` → SetPickupHidden: the mesh and pickup effects are hidden, `bPickupHidden`.
- In state Pickup, **`ValidTouch` returns false while bHidden** and `ReadyToPickup` = !bHidden. So **untouchable while hidden**.
- **The respawn timer is not gated by hidden.** H, stock: after a pickup the factory sleeps RespawnTime (2.0 s here), then
  returns to Pickup, but it's still hidden by Kismet, so it isn't takeable until the next UnHide.
- Weapon factories (TnWeaponPickupFactory) in the same groups follow the same pattern.

## 2. DrainRate None (C)
**The generator class CDO has no DrainRate, so it inherits `TnSurvivalGeneratorBase` = 10.0.** The base's default PowerLevels
are [100, 200, 300, 400, 500]; each placed generator overrides them.

## 3. Drain per tick (C formula; tick rate from our 30 Hz note)
- Per tick, per occupying pawn:
  `AmountToDrain = int(max(1.0, DeltaTime × DrainRate))` (a float → int **truncation**), then `min(that, level cost − CurrentPower)`.
- The game ticked at **30 Hz** on 360 (RE memory: the 30 Hz game tick; dt = the frame dt, H: variable if a frame ran long).
- **Emulate 30 Hz with truncation:**

  | DrainRate | per tick at 30 Hz | per second |
  |---|---|---|
  | 10 / 25 | 1 | 30 |
  | 50 | 1 | 30 |
  | 100 | 3 | 90 |
  | 125 | 4 | 120 |
  | 200 | 6 | 180 |

- **The clamp matters:** the formula at 60 Hz would double the low rates.

## 4. Who drains, and how (C)
- **The occupying set:** the generator's `AreaTracker` (HmOccupiedAreaTracker, **ClassFilter TnPlayerPawn**), fed by the
  generator's Touch / UnTouch.
  - The ActivationVolume is linked with `SetAssociatedActor(generator)`. H: the volume forwards its touches.
  - **Turning that TriggerVolume off** (§1) therefore stops all draining.
- **Gate:** `TnPlayerReplicationInfoSurvival.DrainPower` returns 0 unless **`_AllowDraining`**.
  - Entering: `NotifyUseableGenerator` sets `_AllowDraining = false` and registers the contextual command (`_WatchForGeneratorInput`).
  - **X / keyboard Interact press** (HmButtonInputStateHandler event 1) → server `_AllowDraining = true`, **unless a revivable
    pawn is targeted** (revive takes priority).
  - **Release** (event 2, or 4 after the hold timeout) → false. **Draining = while the button is held.**
- **No facing / line test, no alive / downed / form check in script.** H: a downed pawn's input goes to the downed controls,
  so in practice no.
- Each drained amount comes from that player's power (`min(Amount, _CurrentPower)`). **0 drained** → the fail sound (if draining)
  + StopDraining (beam off).
- **Two players draining at once: each pawn drains its own amount per tick, so the rate adds up** (up to 4 beam slots,
  ReplicatedDrainingPawns). Each pays from their own power.
- Overflow: CheckPower carries the excess into the next level. At max → CurrentPower 0, and Tick returns early (no draining at
  max).

## 5. PowerReward (C, plus H for indirect kills)
- `TnSurvivalGame.Killed`, for a horde enemy (`FindEnemy`):
  - `SpawnPickupRewards(KilledPawn)`: loot on every kill, whoever the killer;
  - then **if Killer (Controller) != none and its PRI is a `TnPlayerReplicationInfoSurvival` → `AddPower(PowerReward)`**
    (clamped to 0..9999).
- **AI killers never get power:** their PRI isn't a Survival PRI. There's **no assist share**.
- **Turret / mine / grenade kills:** H, stock: `Killer` = the damage's InstigatedBy controller, so projectiles and thrown or
  placed weapons credit the owner. A deployed sentry with its own AI controller would not (its controller's PRI isn't Survival).

## 6. MatchAutoStartCountdown 15 (C property, H UI)
- `TnSurvivalGame` CDO **MatchAutoStartCountdown = 15**, the same property versus has at 10 (TnMultiplayerGame). So it
  replaces it one for one: the PendingMatch countdown, the PreGameCountdown screen 15 → 0.
- Remember F1: TnSurvivalGame.ElapsedTime also counts during these 15 s.

## 7. ActivateSequenceEvent consumers (C)
- **Only the map Kismet.** `ActivateSequenceEvent(EventType)` finds every `TnSeqEvent_SurvivalEvents` in the game sequence and
  `CheckActivate`s output index EventType: **0 = Round End** (from RoundEnded), **1 = Round Begin** (InWave.BeginState).
- No announcer or music path. The HUD's wave number comes from `GRI.set_CurrentWave(DisplayWave + 1)` in IncrementWave, which
  also unlocks achievement 45 at DisplayWave 15.
