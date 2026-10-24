# Pad X / keyboard E: tap and hold behaviour (RE, 2026-10-24; QC pad-mapping fix)

**Labels:** C = TransGame.TnPlayerController, HM_Engine.HmButtonInputStateHandler, authored.db.

## The handler (C)
- `PressXButton` / `ReleaseXButton` (pad X) and `PressKeyboardInteractKey` / `Release…` (keyboard E) feed one
  **HmButtonInputStateHandler** (`XButtonInputHandler`).
- **ButtonTimeOut 0.3 s** (CDO `Default__TnPlayerController.XButtonInputHandler0`).
- **Events:**

| Event | Meaning |
|---|---|
| 1 | pressed |
| **3** | **held for 0.3 s** |
| **2** | **released before 0.3 s (tap)** |
| 4 | released after the hold |

## What each input does (C)

| Input | Hold (3) | Tap (2) | Release after hold (4) |
|---|---|---|---|
| **Pad X** (`OnXButtonInputEvent`) | TryRevive, else TryPickup | TryInteract, **else ReloadWeapon** | AbortRevive |
| **Keyboard E** (`OnKeyboardInteractInputEvent`) | the same | TryInteract, else nothing (reload is R) | AbortRevive |

## State overrides (C)
- **ControllingTurret:** press = `InteractCommand0` (leave the turret); release does nothing.
- **Dead:** X / E do nothing.
- **Downed suicide:** a separate handler with a 1.0 s hold.
