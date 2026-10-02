# MILESTONE 03 — Audio native fidelity (WFC, Xbox 360)

Pass date: 2026-10-02. Scope: priorities 11–15 of the narrow gameplay + audio pass.

WFC audio is High Moon's **FmodAudioDevice**, a native-only class. It is built on FMOD Ex, with:
- `SoundNodeRoot` (HM_Engine) carrying the per-cue spatialization parameters;
- `SoundMixerProperties` (`SoundConfig.SoundMixerProperties`) carrying categories, DSP presets and mixer presets.

The evidence comes from:
- the read-only Ghidra snapshot (`tools/wfcq.ps1`; the new `dis` command disassembles undefined bytes in memory only, and the project is opened `-readOnly`);
- HM_Engine/Engine package metadata (enum names via `tools/pkgload.py`);
- AssetTools `authored.db`, read-only.

### Recovered layouts (anchor for everything below)
**SoundNodeRoot** fields, CONFIRMED. Schema order matches the offsets the code uses:
| off | field | off | field |
|---|---|---|---|
| 0x4C | bool bitfield (bit 0x01 / 0x02000000 / 0x04000000 / 0x00800000 seen; 0x00800000 = PlayMixerPresetOnlyIfLocalPlayerSound) | 0x6C | ChanceToPlayNone |
| 0x50 | NonLocalPlayerPitch | 0x70 | DopplerFactor |
| 0x54 | **SpatializationType** (byte) | 0x74/0x78 | DelayMin/Max |
| 0x58 | DistanceMin | 0x7C | **SmartPanDistance2D** |
| 0x5C | DistanceMax | 0x80 | **SmartPanDistance3D** |
| 0x60 | RolloffFactor | 0x84 | **SmartPanAttenuation3D** |
| 0x64 | RearAttenuation | 0x88/0x8C | Category / SecondaryCategory |
| 0x68 | Priority | 0x90 | SecondaryCategoryDistance; 0x94 PlayMixerPreset |

`SoundNodeRoot.Spatialization` enum (HM_Engine export), CONFIRMED:
- 0 `k3D`
- 1 `k2D`
- 2 `kSmartPan`
- 3 `kSmartPan_PreferPlayer`

`SoundCue.InstanceLimitType` enum (Engine), CONFIRMED:
- 0 `kKillOldest`
- 1 `kKillNewest`
- 2 `kKillFarthest`

FmodAudioDevice config:
- **SmartPanPreferPlayerTransitionTime at +0x134** and **MaxPlayerSmartPanRadius at +0x138**. CONFIRMED by the property registration in `0x827415C8` (`li r5,0x134` beside the string 0x8209E3E0; `li r5,0x138` beside 0x8209E3B0).
- The values 0.5 / 1400 come from the request's config input. The coalesced ini was not re-read here.

---

## P11 — Player-preferred SmartPan: where is an Optimus-owned sound spatialized from?
- **CONFIDENCE:** CONFIRMED (native)
- **ADDRESSES:**
  - `0x8275F658` FmodAudioDevice vt+0x1FC — proposed `UpdatePreferPlayerLocation`.
  - `0x82742C70` vt+0x248 — `GetLocalPlayerPawnLocation`.
  - `0x827B4520` vt+0x19C — `GetPreferPlayerLocation`.
  - `0x827560A8` / `0x827560F8` — linear ramp `SetTarget` / `Update`. The ramp object lives at device+0x188, vtable 0x820A1C48.
  - `0x82759B08` — per-source spatialization (see P15). Its caller `0x827881D8` is the per-source update.
- **CLASS:** FmodAudioDevice (native-only)
- **PSEUDOCODE:**
```
UpdatePreferPlayerLocation():               // once per device update
  L = Listener.Location                     // device+0x9C -> listener
  pref = L
  if GetLocalPlayerPawnLocation(&P):        // PlayerController(+0x1C8 pawn) .Location (Actor+0xD8)
     target = (|L - P| >= MaxPlayerSmartPanRadius(1400)) ? 1 : 0
     if Ramp.Target != target: Ramp.SetTarget(target, SmartPanPreferPlayerTransitionTime(0.5))
     Ramp.Update(dt)
     pref = P + (L - P) * Ramp.Value        // alpha 0 = pawn origin, 1 = listener
  device.PreferPlayerLocation(+0x1A0) = pref
Ramp.SetTarget(t, T): Target=t; if T>0 {Rate=(t-Value)/T; Remaining=T; Active=1} else {Value=t; Active=0}
Ramp.Update(dt): if Active { Remaining-=dt; Value += Rate*dt; if Remaining<=0 or overshoot: Value=Target, Active=0 }
```
- **ORIGINAL WFC BEHAVIOR (answer to A/B/C/D/E):** **D, a blend, but only for the 2D↔3D SmartPan amount, and only for `kSmartPan_PreferPlayer` cues.**
  - The sound's **position** stays the AudioComponent's own world location, i.e. the component or socket it plays on (AC+0xF0 is used for the distance and direction maths).
  - **Volume distance attenuation and rear attenuation** always use **listener (camera) → sound** distance.
  - For `kSmartPan_PreferPlayer` (type 3) only, the distance that drives the 2D↔3D pan mix is measured from a **reference point**:
    - the reference point is the **local player pawn origin** (Actor.Location) while the camera is within 1400 UU of the pawn;
    - it ramps **linearly over 0.5 s** to the **listener position** when the camera is ≥1400 UU from the pawn, and back again.
  - For an Optimus-owned sound with the camera at its normal ~800 orbit, the reference point is therefore the **pawn origin (B)**. The sound's own 3D position (A) is still what FMOD positions.
  - For `kSmartPan` (type 2), the pan-mix distance is listener → sound.
- **CURRENT REBUILD COMPARISON:** Not inspected.
  - Implement PreferPlayer as a reference point used **only** for the SmartPan distance.
  - Do not move the emitter, and do not use pawn distance for volume rolloff.
- **PRIMARY HANDOFF:** Systems (audio).
- **EXPERIMENTAL ASSERTION:**
  - Pan-mix distance for type-3 cues = |PreferPlayerLocation − sound|.
  - The 1400 / 0.5 s linear switch uses a hard threshold, not a distance-proportional blend.

## P12 — Audio concurrency replacement semantics
- **CONFIDENCE:** CONFIRMED (native)
- **ADDRESS:**
  - `USoundCue::RegisterInstanceLimiting` `0x82E767B8` (exec 0x82C6F778; called from `UAudioComponent` Play internal `0x82E76D18`).
  - Unregister `0x82E53338` (exec 0x82C6F820).
  - Purge `0x82E498A0`.
  - Stop `0x82E766E0`.
- **FIELDS:**
  - SoundCue+0x30 MaxConcurrentPlayCount.
  - +0x38 InstanceLimiting (byte).
  - +0x3C/+0x40 PlayingAudioComponents array/count.
- **PSEUDOCODE:**
```
Register(cue, newAC):
  if no engine/client/listener: return 0 (refuse)
  if Max == 0: return 1                       // unlimited, not tracked
  Purge(cue)                                  // drop dead/finished entries first
  switch mode:
   kKillOldest(0): if Count >= Max: Stop(Playing[0])            // oldest registered
   kKillNewest(1): if Count >= Max: return 0                    // the NEW sound is refused
   kKillFarthest(2): if Count >= Max:
        dNew = dist²(listener, newAC.loc); best=-1; bestD=dNew
        for i = Count-1 .. 0:                                   // newest -> oldest
           d = dist²(listener, Playing[i].loc)
           if d - bestD >= 0 or |d - bestD| < eps: best=i; bestD=d
        if best == -1: return 0                                 // new one is the farthest -> refused
        Stop(Playing[best])
  Playing.Add(newAC); return 1
Unregister(cue, AC): Playing.RemoveItem(AC); Purge(cue)
```
- **ORIGINAL WFC BEHAVIOR:**
  - Replacement is a **stop**, not a fade.
  - kKillNewest refuses the incoming sound.
  - kKillFarthest compares against the incoming sound's distance. If the incoming sound is the farthest it is refused; on ties the **oldest** equal instance is killed.
  - The listener location is the client viewport listener.
- **PRIMARY HANDOFF:** Systems (audio).
- **EXPERIMENTAL ASSERTION:**
  - MaxConcurrentPlayCount 0 = unlimited.
  - kKillFarthest never kills a nearer sound to admit a farther one.

## P13 — Mixer preset fade / interpolation / ducking
- **CONFIDENCE:** PARTIAL
  - CONFIRMED: activation stack, priority ordering, ref-counting, data.
  - UNKNOWN: the per-tick fade curve inside the DSP applier object.
- **ADDRESSES:**
  - `UAudioDevice::EnableMixerPreset` exec `0x82C7EE88` → FmodAudioDevice vt+0x130 `0x82742400` → mixer object (device+0x160, created by vt+0x234 `0x8277D2B0`, size 0x50, vtable **0x820B3688**) vt+0x24 `0x82772778` **Enable**.
  - vt+0x28 `0x827728E0` **Disable**.
  - vt+0x3C `0x82772A60` register preset (sorted insert).
  - vt+0x40 `0x82772B38` remove preset.
  - vt+0x20 `0x8276AB60` flush (keeps `UnflushableMixerPresets`).
  - Disable exec `0x82C7EF80` → vt+0x134 `0x82742490`.
  - Cue-driven presets: `0x8277FE88` (device vt+0x190), called on AC play/stop. It uses SoundNodeRoot.PlayMixerPreset (+0x94). With `PlayMixerPresetOnlyIfLocalPlayerSound` (+0x4C bit 0x800000) set, it applies only if the owner is locally controlled.
- **PSEUDOCODE:**
```
Enable(name):  p = Find(name); if !p return 0
  p.Elapsed(+0x1C) = 0
  if name not in Active[]:
     insert name before the first active preset with lower Priority (else append)   // Active sorted by Priority desc
     Applier(+0x18)->SetActive(Active[])  (vt+0x1C) ; notify callback
  p.RefCount(+0x18) += 1 ; return 1
Disable(name, force):
  if name in Active[]: if force: p.RefCount = 1
     if p.RefCount == 1: Active.Remove(name); Applier->SetActive(Active[]); notify
     p.RefCount = max(0, p.RefCount - 1)
```
- **DATA (CONFIRMED, `SoundConfig.SoundMixerProperties`):**
  - 47 categories and 547 mixer presets, each with {Priority, FadeInTime, FadeOutTime, Duration, IsPlayerPOV}.
  - Most common fade pairs: 0.25/0.25 (150 presets), 1.0/1.0 (51), 0/0 (42), 0.5/0.5 (35).
  - Ducking is authored as mixer presets: per-category DSPPresets with Volume, EQ, LowPass and so on.
    - `SeqAct_PlayDialog` has native `EnableDuckingMixerPreset` / `DisableDuckingMixerPreset`.
    - Examples: Streets `D3_STREETS_DUCK_AMB_EXT_0{1,2,3}` fade 1.5/1.5, priorities 440–442; Category `SFX_WET_AMB_EXTERIOR`, Volume 1.0/1.0/0.0.
- **ORIGINAL WFC BEHAVIOR:**
  - Presets **stack**. They are ref-counted per name and ordered by Priority, highest first.
  - Re-enabling an active preset only bumps the ref-count and resets its elapsed timer.
  - The applier receives the whole ordered stack.
  - How it blends overlapping presets per category, and whether the fade is linear in dB or in linear gain, was **not recovered** in this pass.
- **PRIMARY HANDOFF:** Systems (audio).
- **EXPERIMENTAL ASSERTION:**
  - Ref-count semantics.
  - Priority ordering.
  - FadeIn/FadeOut times from data.
  - Do not assert the fade curve shape yet.

## P14 — Streets / Kismet zone audio + reverb
- **CONFIDENCE:** CONFIRMED (data + script). The `SeqAct_Reverb` native activation is HIGH: it goes through the mixer-preset path in P13.
- **FINDING:** **Conventional reverb exists.** It is an FMOD I3DL2-style reverb DSP on the **MASTER_WET** category (DSPEffectConfig 280), selected by **mixer presets named `REVERB_*`**.
  - The premise "no conventional reverb" is **false**.
- **DATA:**
  - `MP_IAC_Streets_AUDIO_m` contains:
    - **9 `SeqAct_Reverb`**, each with a `ReverbMixerPreset` (SoundMixerPresetName);
    - SeqAct_AmbientAudioZone actions whose "Enter" outputs link to those SeqAct_Reverb actions (for example AmbientAudioZone_119 → SeqAct_Reverb_4639, DEC_ROOM_UPPER).
    - There are 616 AmbientAudioZone actions game-wide.
  - Streets reverb presets:
    - All have FadeIn = FadeOut = **0.25 s** and Duration −1 (until disabled).
    - Priorities: EXTERIOR 182, NEU_BASE 183, AUTO_ROOM_01 216, DEC_ROOM_LOWER 217, NEU_HALL 218, TRAIN_DEPOT 219, AUTO_ROOM_02 220, TRAIN_TUNNEL 221, NEU_STAIRWELL 222, DEC_ROOM_UPPER 223.
  - MASTER_WET reverb parameters (mB / s):
| preset | Room | RoomHF | Decay | DecayHF | Refl | Rev Level | Delay | Diff | Dens | HFRef |
|---|---|---|---|---|---|---|---|---|---|---|
| EXTERIOR | −800 | −985 | 2.65 | 0.73 | −900 | −600 | 0.05 | 33 | 65 | 6122 |
| NEU_BASE | −650 | −700 | 2.06 | 0.62 | −760 | −600 | 0.01 | 6 | 4 | 8288 |
| NEU_HALL | −900 | −850 | 2.75 | 0.86 | −600 | −600 | 0.01 | 3 | 6 | 8386 |
| NEU_STAIRWELL | −650 | −800 | 3.33 | 1.00 | −750 | −650 | 0.01 | 4 | 2 | 7992 |
| AUTO_ROOM_01 | −850 | −700 | 2.35 | 0.57 | −650 | −600 | 0.01 | 4 | 46 | 6024 |
| AUTO_ROOM_02 | −900 | −700 | 4.81 | 1.64 | −780 | −800 | 0.03 | 9 | 56 | 9173 |
| DEC_ROOM_LOWER | −630 | −800 | 3.24 | 1.25 | −750 | −600 | 0.03 | 16 | 64 | 8977 |
| DEC_ROOM_UPPER | −936 | −887 | 3.14 | 0.81 | −600 | −600 | 0.05 | 59 | 39 | 7008 |
| TRAIN_DEPOT | −700 | −900 | 2.65 | 0.69 | −800 | −600 | 0.01 | 49 | 31 | 6713 |
| TRAIN_TUNNEL | −900 | −1400 | 4.32 | 0.32 | −1100 | −800 | 0.02 | 26 | 14 | 2185 |

  - RoomRolloffFactor, ReflectionsDelay, DryLevel 0 and the full set of fields are in authored.db. `REVERB_NONE` has Room −10000.
- **ORIGINAL WFC BEHAVIOR:**
  - Entering a Kismet ambient zone fires SeqAct_Reverb, which enables a REVERB_* mixer preset.
  - Zone presets stack by priority: interior presets 216–223 outrank EXTERIOR 182.
  - They cross-fade 0.25 s.
  - Wet signal is routed through *_WET categories.
- **PRIMARY HANDOFF:** Systems (audio) + level scripting.
- **EXPERIMENTAL ASSERTION:**
  - Streets has 9 reverb zones with the parameters above.
  - The reverb switch fade is 0.25 s.
  - Priority decides overlaps.

## P15 — Audio spatialization cross-check
- **CONFIDENCE:** CONFIRMED (native `0x82759B08`, proposed `FmodAudioDevice::ComputeSourceSpatialization`)
- **CALLER:** `0x827881D8`, the per-source update. It also handles random-delay/start time, pitch/volume clamps, the virtual flag and DSP children.
- **PSEUDOCODE (r = SoundNodeRoot, AC = AudioComponent, Lst = listener {Loc, Up, Right, Front}):**
```
out.SomeParam(+0x60) = r.+0xA8
d = |Lst.Loc - AC.Loc| ; out.ListenerDist = d
dc = max(d, DistanceMin)
if dc > DistanceMax: out.Culled = 1 ; out.Vol = 0 ; return
out.Vol = DistanceMin / ((dc - DistanceMin)*RolloffFactor + DistanceMin)              // inverse-distance rolloff
dir = normalize(AC.Loc - Lst.Loc) ; f = dot(Lst.Front, dir)
if f < 0: out.Vol *= 1 - (1 - dBToLin(RearAttenuation)) * (-f)                         // behind-listener attenuation
[occlusion block: if AC flag 0x08000000 and root bits 0x02000000/0x04000000 and device flag: periodic trace
   (0x82E337A0) -> interpolate occlusion volume/LPF params over the occluder's fade time]
ds = (SpatializationType == kSmartPan_PreferPlayer) ? |PreferPlayerLocation - AC.Loc| : d
if SmartPanDistance2D == SmartPanDistance3D: pan = (ds < D2D) ? 0 : 1
else: t = clamp((clamp(ds,lo,hi) - lo)/(hi - lo), 0, 1); pan = (D2D < D3D) ? t : 1 - t
out.Pan3D = pan                                     // 0 = fully 2D (centred), 1 = fully 3D
out.SmartPanGain = 1 - (1 - dBToLin(SmartPanAttenuation3D)) * pan
if bit0 of root+0x4C and d > SecondaryCategoryDistance: out.Category = SecondaryCategory    // (+0x90 / +0xAC)
```
- **ORIGINAL WFC BEHAVIOR:**
  - The rolloff is **inverse-distance**, `Min/((d−Min)·Rolloff+Min)`, with a hard cull beyond DistanceMax. It is not linear.
  - Rear attenuation scales linearly with how far behind the listener the source is.
  - SmartPan mixes 2D↔3D linearly between SmartPanDistance2D and SmartPanDistance3D. It applies extra gain toward SmartPanAttenuation3D as it becomes 3D.
  - Secondary category switching happens by distance.
  - `k3D`/`k2D` do not use the pan path. Their exact FMOD mode switch lives elsewhere and was not traced.
- **PRIMARY HANDOFF:** Systems (audio).
- **EXPERIMENTAL ASSERTION:** Rolloff formula; cull at DistanceMax; linear 2D↔3D SmartPan; type-3 distance from the PreferPlayer point.

## Still unknown (audio)
- The mixer applier (mixer+0x18, vt+0x1C SetActive) per-tick fade curve, and how overlapping presets combine per category (override by priority vs. multiply).
- What `Duration > 0` presets do on expiry (Elapsed +0x1C is reset on Enable; the tick that consumes it was not found).
- `dBToLin` (`0x82CBED00`) / `0x82CBEE20` exact formulas. They are assumed to be 10^(x/20) and its pair, which is HIGH, not verified.
- The k2D/k3D FMOD channel-mode switch.
