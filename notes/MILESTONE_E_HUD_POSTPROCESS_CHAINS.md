# HUD screen effects: GFx `ActivatePostProcessChain` / `DeactivePostProcessChain` (Milestone E, 2026-10-06)

Labels: C = from GFxUI script (`work/script/decomp_gfx/GFxUI.GFxMovie.txt`), Hud_GFX ActionScript (`tools/as2dis.py`), TransGame script and authored.db; H = high confidence.

## Mechanism (C)
- The movie asset `UI_GFxHud_p.Hud_GFX_1` (GFxMovie) has `PostProcessChains`:
  - [0] = `UI_GFxHud_p.StaticDischargeScreenEffect`;
  - [1] = `UI_GFxHud_p.LowHealth.LowHealthScreenEffect`.
  - Each chain holds one `MaterialEffect`.
- `GFxMovie.ActivatePostProcessChain(Index)`: `CurrentPostProcessChainIndex = Clamp(Index, 0, Len−1)`.
- `GFxMovie.DeactivePostProcessChain()` (note the spelling, **no parameter**): `CurrentPostProcessChainIndex = −1`.
- `GetCurrentPostProcessChain()`: the chain at the index, or none.
  - Its consumer is native (it is not called from script). H: the renderer applies the movie's current chain each frame while the movie is open.
  - It is **one slot**: activating one chain replaces the other.
- AS wrappers: `Self.ActivatePostProcessChain(id)`. `HmExternalInterface.Self.DeactivatePostProcessChain(x)` calls `'Self.DeactivePostProcessChain'` and **drops the argument**, so every deactivate clears whichever chain is active.
- No duration or fade in the chain logic: on or off immediately. Any temporal behaviour is inside the materials, plus the HUD clips fading over them.

## Callers in Hud_GFX (C)
| Event | Call |
|---|---|
| HUD movie load | `Deactivate()` (reset) |
| `_global.NotifyHudScrambledChanged(true)` ← `TnHudDataObserverHudScrambled` (player has buff TnBuffScrambleHud, TnBuffFlashBang or TnBuffDecoyTrap) | `Activate(0)` static discharge; `midCenter_mc` fades to alpha 0 over 0.5 s |
| … `(false)` | `Deactivate`; midCenter fades back to 100 over 0.5 s |
| `_global.NotifyDownedWarningFade(pct)`: health bar below `LowHealthWarnPercent`, pct = 100·(warn − value)/warn | first pct > 0: attach `mc_hurt` (alpha = pct) + `Activate(1)` low-health; later calls update `FadeWarningState(pct)` |
| … pct 0 (health back above the warn level) | `mc_hurt.RemoveMe()` + `Deactivate` |
| `_global.NotifySpectating(true)` (including death / spectating) | hide incapacitated screen + `Deactivate` |

- **Not a death-cam effect.** The death / respawn screen itself does not activate a chain. Death → spectating → `Deactivate`, which removes any low-health or scramble effect. On respawn the chain comes back only through new low-health or scramble events.
- Downed / incapacitated (`NotifyNormalizedDownedHealthChanged` < 1) attaches `mc_incapacitatedScreen` and toggles spectator HUD mode. It does not itself call Activate, but the low-health chain is normally already active from the health drop.

## Effect materials (C, graphs)
**LowHealthScreenEffect_M** (unlit, bUsesSceneColor):
- Emissive = Scene.rgb + (0, 0.5, 1) × [ScanlinePanner(pan V −2) × ScanlinePanner(pan V +1)] × [Scanline(UV, VTiling 80) × ScanlinesOpacityMask(screen UV)] — a cyan/blue scanline overlay.
- ScreenAlpha = Scene.a × clamp(TunnelVisionMask + 0.3 + 0.04·sin(Time, period 0.4 s)) — vignette ("tunnel vision") with a slight pulse.
- Textures: `UI_GFxHud_p.LowHealth.LowHealthScanlinePanner_CLR`, `LowHealthScanline_CLR`, `LowHealthScanlinesOpacityMask_CLR`, `LowHealthTunnelVisionMask_CLR`.

**StaticDischargeScreenEffect_M** (unlit, bUsesSceneColor):
- Two `StaticPanner1` samples: UTiling 0.03125, pans (0.42, 0.513) and (−0.805, −0.942).
- Screen UV offset = screenpos + ((s1.r − s2.g) × 0.15 × s2.b , (s2.r − s1.g) × 0.15 × s1.b). H: that channel mapping is from output indices 1/2/3.
- Emissive = clamp(s1.a + s2.a) × Scene(offset UV); ScreenAlpha = 1 − (1 − Scene.a) × clamp(s1.a + s2.a).
- Result: distorted, static-noise screen while jammed, flash-banged or caught in a decoy trap.

H: `ScreenAlpha` is the WFC MaterialEffect blend weight against the unmodified scene (HM extension; exact blend not traced).
