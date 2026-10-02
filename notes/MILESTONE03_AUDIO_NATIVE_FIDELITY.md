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


---

# Follow-up (2026-10-02): narrow runtime-semantics gaps for Systems checkpoint 7b42621

Sources:
- Read-only Ghidra snapshot via `tools/wfcq.ps1`, including `dis` (in-memory disassembly).
- `authored.db`, read-only.
- Bool bitfields are MSB-first, as established earlier.

Runtime mixer structures recovered here:
- **Runtime mixer preset entry** (0x20 bytes, built by mixer Init `0x82782A18` from `SoundMixerProperties.MixerPresets`):

| off | field |
|---|---|
| +0x00 | Name |
| +0x04 | Priority |
| +0x08 | FadeInTime |
| +0x0C | FadeOutTime |
| +0x10 | Duration |
| +0x14 | IsPlayerPOV |
| +0x18 | **RefCount** |
| +0x1C | **Elapsed** |

- Init also registers and enables a built-in **"Default"** preset: Priority 0, FadeIn/FadeOut 0.5, Duration −1.
- **Mixer object** vtable `0x820B3688`:

| slot | address | role |
|---|---|---|
| +0x0C | 0x82756180 | Tick(dt) |
| +0x20 | 0x8276AB60 | Flush |
| +0x24 | 0x82772778 | Enable |
| +0x28 | 0x827728E0 | Disable(name, force) |
| +0x3C | 0x82772A60 | RegisterPreset (sorted by priority) |
| +0x44 | 0x827665F0 | AdvanceTimers |
| +0x48 | 0x82756490 | UpdateCategories |

- **Category node** (one per SoundCategory, a tree): vtable `0x820A3F80`.
  - +0x04 = 0x82765EA8 Update(dt)
  - +0x1C = 0x8276A868 SetActive(activeList)
  - Target selection = 0x827661C8
- **Linear ramp** used for every mixer parameter: vtable `0x820A1C48`, created by FmodAudioDevice vt+0x1B4 `0x82759490`.
  - SetTarget = 0x827560A8
  - Update = 0x827560F8

## A1. Zone exit / previous-preset switch-off
- **CONFIDENCE:** CONFIRMED (native + Streets Kismet data)
- **ADDRESS:**
  - `SeqAct_Reverb::Activated` **0x82764858** (vtable 0x820B8C58)
  - `SeqAct_AmbientAudioZone` input handler **0x827892D8**
  - per-tick zone update **0x82763F10** (vtable 0x820B6A98)
  - local-PC lookup 0x8274CDE0
  - set zone 0x82797EE8 → `PlayerController.SetAmbientAudioZone` (script; replicated as ServerSetAmbientAudioZone)
- **CLASS / FUNCTION:** HM_Engine SeqAct_Reverb, SeqAct_AmbientAudioZone; Engine PlayerController.AmbientAudioZone (+0x518)
- **CALLERS / CALLEES:**
  - SeqEvent_Touch (Touched) → Zone input "Enter".
  - Zone output "Scene 0 Begun" → SeqAct_Reverb "Activate" plus the zone's ambience sub-Sequence.
  - "Scene 0 Ended" → the same sub-Sequence.
  - SeqAct_Reverb → FmodAudioDevice vt+0x130 EnableMixerPreset / vt+0x134 DisableMixerPreset.
- **CONSTANTS / DATA:**
  - **Streets Touch events:** `bLocalPlayerOnly`, `bClientSideOnly`, `bForceOverlapping`, ignore TnCamera, MaxTriggerCount 0, ReTriggerDelay 0. **The UnTouched output has no links in all 9 zones.**
  - **Global "current reverb" slot:** `0x8374FCCC` (one name). It is reset to None by mixer Flush (0x8276AB60, at level change).
- **PSEUDOCODE:**
```
Touch(trigger volume) [local player pawn, client side] -> Zone.Enter:
Zone.OnInput(Enter):                                         // 0x827892D8
  pc = first local PlayerController
  if pc.AmbientAudioZone != this.Name:
     prev = FindObject(pc.AmbientAudioZone); if prev is SeqAct_AmbientAudioZone: prev.IsEntered = false
     pc.SetAmbientAudioZone(this.Name)                       // script; also ServerSetAmbientAudioZone
  this.IsEntered = true
Zone.OnInput(Scene k): SceneIndexNext = k                    // unused in Streets (only Scene 0)
Zone.Update() each tick while active:                        // 0x82763F10
  if IsEntered:
     if SceneIndexCurrent != SceneIndexNext:
        if SceneIndexCurrent >= 0: fire "Scene <cur> Ended"
        fire "Scene <next> Begun"; SceneIndexCurrent = SceneIndexNext
     keep active
  else:
     if SceneIndexCurrent >= 0: fire "Scene <cur> Ended"
     SceneIndexCurrent = -1 ; finish
SeqAct_Reverb.Activated():                                   // 0x82764858
  if InputLinks[0] impulse:
     new = ReverbMixerPreset.PresetName
     if new != gCurrentReverb:
        if EnableMixerPreset(new) == 1:
           if gCurrentReverb != None: DisableMixerPreset(gCurrentReverb, force=0)
           gCurrentReverb = new
     clear impulse
```
- **ORIGINAL WFC BEHAVIOR:**
  - **Previous preset:** WFC **explicitly disables** the previous reverb preset when a zone with a *different* preset fires. It does not rely on priority or ref-count replacement.
  - **Ref-count:** each reverb preset is enabled once (RefCount 1) and disabled once (RefCount → 0, removed). Re-entering the zone whose preset is already current does nothing: no Enable, no ref-count change, no timer reset.
  - **Priority:** while both are briefly in the active stack, priority only orders them. The new preset becomes the category target only if it outranks every other active preset that defines MASTER_WET.
    - Streets zones 182–223 all outrank `Default` (0).
    - Disabling the previous preset then retargets MASTER_WET to the new zone, using the fade rules in A2.
  - **Overlapping or nested trigger volumes:** the **last Touch wins**.
    - Moving from an inner volume back into the still-overlapping outer volume generates no new Touch, so **the inner zone's reverb persists** until another volume is touched.
  - **Leaving all zones:** nothing happens. UnTouched is unlinked. The last reverb remains active, and its ambience sub-sequence keeps running until another zone is entered.
  - **Default / no-zone state:** only at map start before the first Touch, or after a mixer Flush (level transition). In that state MASTER_WET's target is the `Default` DSP preset, which has Room −10000, i.e. no reverb.
- **SYSTEMS HANDOFF:**
  - Keep one global current-reverb name.
  - On zone enter: enable the new preset, then explicitly disable the old one.
  - Never disable on exit.
  - Make zone enter a local-client event.
- **EXPERIMENTAL CHECK NOW SAFE TO PROMOTE:**
  - Walking out of a Streets zone into open space keeps that zone's reverb.
  - Re-entering the same zone is a no-op.
- **STILL UNKNOWN:** nothing for Streets. Other maps may link UnTouched or use multiple scenes; check per map.

## A2. Mixer preset fade curve
- **CONFIDENCE:** CONFIRMED
- **ADDRESS:**
  - target selection 0x827661C8
  - category SetActive 0x8276A868, category Update 0x82765EA8
  - Volume effect SetTarget 0x82755F00, Update 0x82755FD0 (vtable 0x820A1C28)
  - Reverb effect SetTarget 0x82755618 (vtable 0x820A1C0C)
  - ramp 0x827560A8 / 0x827560F8
- **PSEUDOCODE:**
```
Category.SetActive(activeList):                      // after every Enable/Disable that changes the list
  (newName, fadeTime) = SelectTarget(activeList)     // A3
  if newName == currentName: return                  // no retarget, no restart
  currentName = newName ; categoryTimer = 0
  for each DSP effect present on this category (Volume, Pitch, HighPass, LowPass, FastLowPass, Flange,
                                                Distortion, Compressor, FastEQ, EQ, Echo, Reverb):
      effect.SetTarget(fadeTime, &category.DSPPresets[newName].<field>)
  recurse into child categories
SelectTarget fade time:
  if newPreset.Priority < currentPreset.Priority : fadeTime = currentPreset.FadeOutTime   // stepping DOWN
  else                                           : fadeTime = newPreset.FadeInTime        // stepping UP / equal
Effect.SetTarget(T, value): for each parameter p: ramp_p.SetTarget(clampToFMODRange(value_p), T)
Ramp.SetTarget(t, T): Target=t; if T>0 { Rate=(t-Value)/T; Remaining=T; Active=1 } else { Value=t; Active=0 }
Ramp.Update(dt):  if Active { Remaining-=dt; Value+=Rate*dt; if Remaining<=0 or passed Target: Value=Target; Active=0 }
Volume effect apply each tick: FMOD ChannelGroup.setVolume( categoryVolume * clamp(rampValue,0,1) )
```
- **ORIGINAL WFC BEHAVIOR:**
  - **Shape:** linear in time.
  - **Domain:** each parameter is ramped in its **authored units**.
    - Volume is authored and ramped as a **linear amplitude** (e.g. 0.7079 = −3 dB). It is linear in amplitude, not in dB.
    - Reverb Room/RoomHF/Reflections/Reverb levels are in **millibels**, ramped linearly in mB, i.e. linear in dB.
    - Decay/delay times are in seconds; filter frequencies are in Hz (linear).
  - **Attack and release** use the same linear ramp. The only difference is which time is used: FadeIn when moving to a higher-or-equal-priority preset, the outgoing FadeOut when moving to a lower one.
  - **Interruption/restart:** a new target restarts from the **current value**, with the **full** new fade time (the rate is recomputed). There is no snap.
  - **Crossfade:** there is no simultaneous mix of two presets. Each parameter glides from where it is to the new target.
  - **Granularity:** per category, per parameter. Categories whose target did not change are untouched.
  - **0.25 s Streets presets:** entering a higher-priority zone glides MASTER_WET reverb parameters to the new values over the new preset's FadeInTime (0.25 s). Falling back to a lower one uses the outgoing preset's FadeOutTime (0.25 s).
- **SYSTEMS HANDOFF:** implement exactly one linear ramp per DSP parameter per category, with the rules above.
- **EXPERIMENTAL CHECK NOW SAFE TO PROMOTE:**
  - Fade shape is linear.
  - Volume is linear in amplitude.
  - Reverb levels are linear in mB.
  - Restart from the current value with the full duration.
- **STILL UNKNOWN:** the per-parameter FMOD clamp constants for non-reverb effects; they are available at the listed SetTarget addresses if needed.

## A3. Overlapping mixer presets
- **CONFIDENCE:** CONFIRMED
- **ADDRESS:** Enable 0x82772778, Disable 0x827728E0, SelectTarget 0x827661C8
- **PSEUDOCODE:**
```
Enable(name): p.Elapsed = 0
  if name not in Active: insert before the first active entry with LOWER priority (else append); notify categories
  p.RefCount += 1
Disable(name, force): if name in Active:
  if force: p.RefCount = 1
  if p.RefCount == 1: remove from Active; notify categories
  p.RefCount = max(0, p.RefCount - 1)
SelectTarget(category, Active):   // Active is ordered by priority, highest first
  for p in Active:
     if p.IsPlayerPOV and !deviceFlag(+0xC0 & 0x08000000): continue
     if category has a DSPPreset named p.Name: return p      // first match wins outright
  (no match -> keep current)
```
- **ORIGINAL WFC BEHAVIOR:**
  - **Stack model:** a priority-ordered active list, with a ref-count per preset name.
  - **Highest priority wins, per category.** Lower-priority presets contribute nothing to a category that a higher active preset defines.
  - **Independent categories:** a category not defined by the top preset falls through to the next active preset that defines it, and ultimately to `Default`.
  - There is **no additive or multiplicative combination** between presets.
  - The final category volume = the category's base Volume × the winning preset's volume. Category hierarchy is applied by FMOD channel-group nesting (HIGH).
  - **Equal priority:** a newly enabled preset is inserted *after* existing equals, so **the earlier-enabled preset wins**.
  - **Removal:** when a preset is removed, every affected category retargets to the next match, using the A2 fade rule (the outgoing preset's FadeOut, since it stepped down).
- **SYSTEMS HANDOFF:** use the pseudocode as-is.
- **EXPERIMENTAL CHECK NOW SAFE TO PROMOTE:** per-category highest-priority-wins with fall-through; ties go to the older preset.
- **STILL UNKNOWN:** which runtime flag (device +0xC0 bit 0x08000000) enables IsPlayerPOV presets.

## A4. Preset Duration
- **CONFIDENCE:** CONFIRMED
- **ADDRESS:** mixer Tick 0x82756180 → AdvanceTimers 0x827665F0 → expiry test 0x8279AA50
- **PSEUDOCODE:**
```
Tick(dt): for p in Active (iterated last -> first):
   p.Elapsed += dt
   if p.Name != "Default" and p.Duration >= 0 and p.Elapsed >= p.Duration: Disable(p, force=0)
```
- **ORIGINAL WFC BEHAVIOR:**
  - **Start:** Elapsed is reset to 0 on **every** Enable, including re-activation of an already-active preset.
  - **Countdown:** it counts only while the preset is in the Active list.
  - **Infinite:** **Duration < 0** (the authored −1). There is no special "infinite" meaning for 0.
  - **Duration 0:** expires on the next mixer tick.
  - **Expiry is a non-forced Disable:**
    - RefCount 1 → the preset is removed;
    - RefCount n > 1 → it decrements once per tick, because Elapsed stays ≥ Duration, so the preset is removed after n ticks.
  - **Restoration:** removal triggers the normal retarget to the next active preset, using the expiring preset's FadeOutTime.
  - **Explicit stop:** an explicit Disable also works; it is a plain ref-count decrement.
  - **Zone exit:** none (see A1).
- **SYSTEMS HANDOFF:** as pseudocode.
- **EXPERIMENTAL CHECK NOW SAFE TO PROMOTE:**
  - −1 means infinite.
  - Re-enable resets the timer.
  - Expiry restores the lower preset with the outgoing FadeOut.
- **STILL UNKNOWN:** none.

## A5. 2D / 3D channel mode
- **CONFIDENCE:** CONFIRMED
- **ADDRESS:**
  - SoundNodeRoot vtable 0x820A7A00; `IsSpatialized` (vt+0x164) **0x82743928**
  - wave-instance build 0x82788768 → init 0x8276C1E0
  - per-source spatialization 0x82759B08 (earlier report)
  - wave volume/pan assembly 0x82788CB0
  - FMOD voice: create **0x82768820**, update **0x82742D08** (voice vtable 0x820BBDC8)
- **PSEUDOCODE:**
```
type = (node override flag ? node.SpatializationType(+0x40) : root.SpatializationType(+0x54))
IsSpatialized = (type != k2D)                       // 0x82743928
wave.bUseSpatialization = IsSpatialized ; wave.bSmartPan = (type == kSmartPan || type == kSmartPan_PreferPlayer)
CreateChannel: mode = (bUseSpatialization ? FMOD_3D(0x10) : FMOD_2D(0x8)) | (looping ? LOOP_NORMAL(2) : LOOP_OFF(1))
               if 3D: Channel.set3DPanLevel(1.0)
               setSpeakerMix(six authored speaker dB values -> linear)
Per tick (wave build):
  if bUseSpatialization: Volume *= DistanceAtten (inverse rolloff, rear attenuation); occlusion; doppler velocity
  if bSmartPan: wave.PanLevel = Pan3D ; Volume *= SmartPanGain
FMOD update: set3DAttributes(pos*0.01, vel*0.01); setVolume(clamp(Volume,0,1));
             if bSmartPan: Channel.set3DPanLevel(PanLevel)
             set3DDopplerLevel(EnableDoppler ? 1 : 0)
```
- **ORIGINAL WFC BEHAVIOR:**
  - **Pure 2D (k2D):** FMOD_2D. No WFC distance attenuation, no 3D position.
  - **Pure 3D (k3D):** FMOD_3D with pan level fixed at 1.0. Volume = WFC inverse rolloff × rear attenuation; FMOD positions it.
  - **SmartPan / PreferPlayer:** FMOD_3D, with `3DPanLevel = Pan3D`.
    - Pan3D = 0 at SmartPanDistance2D (centred / 2D) and 1 at SmartPanDistance3D (fully positional), linear in between.
    - Volume additionally × `1 − (1 − dB(SmartPanAttenuation3D))·Pan3D`.
    - **Distance attenuation (WFC rolloff) still applies during the blend.** It is computed from the listener→emitter distance.
    - PreferPlayer changes only the distance used for Pan3D (earlier report P11).
  - **Granularity:** the mode is chosen per wave instance, i.e. per FMOD channel. It comes from the root unless a node overrides it.
  - All Optimus vehicle cues use `kSmartPan_PreferPlayer` with 2D 200 / 3D 1000 / −3 dB, DistanceMin 5000, DistanceMax 35000.
- **SYSTEMS HANDOFF:** use the FMOD-style 3D pan level directly as the 2D↔3D mix; do not swap modes mid-sound.
- **EXPERIMENTAL CHECK NOW SAFE TO PROMOTE:** k2D → no attenuation; SmartPan keeps attenuation and scales pan level linearly.
- **STILL UNKNOWN:**
  - FMOD's internal set3DPanLevel mixing law, which is FMOD Ex library code.
  - FMOD's own 3D rolloff settings for these channels. WFC applies its own attenuation in volume, so FMOD's rolloff is presumably neutral; that is not verified.

## A6. Looping vehicle cues: loop region
- **CONFIDENCE:**
  - CONFIRMED for the runtime path and the cue data.
  - PARTIAL for the sample loop points, which are in the FSB headers (not decoded in this lane).
- **ADDRESS:** channel create 0x82768820 (LOOP_NORMAL); playback-time wrap in per-source update 0x827881D8; vehicle script `HmVehicleAudioComponent.PlayLoopingSound` / `StopLoopingSound`
- **DATA (Optimus, via `SoundEvents_Vehicles_Trans.Veh_Optimus_Prime_SoundSet`):**
  - Events resolve to `BL_VEH_OPTIMUS_PRIME.VEH_OPTIMUS_*` SoundCues.
  - **Looping is per-wave** (`SoundNodeWaveEvent.bLooping = true`, waves named `*_LP`, e.g. `WL_TRUCK.AUTO_OPTIMUS_ENGINE_MID_LR_LP`, `SYNTH_ENERGY_MOD_PAN_LP`, `JET_TURBO_WHINE_LP`, `MECH_OPTIMUS_TIRE_NOISE_02_LP`).
  - Each wave event has a start delay `Time`, Volume dB, Pitch semitones, VolumeCurve/PitchCurve against a SoundParameter (`Optimus_Prime_Speed`), and an `Envelope` (time-based curves).
  - Root `bLooping` is **false** on DRIVE_ONLOAD/OFFLOAD, BOOST_START/LOOP/END, JUMP and RAM.
  - Root LoopStart/LoopEnd values exist (e.g. BOOST_LOOP 2.904–3.120 s, BOOST_START 6.621–7.198 s) but are unused, because root bLooping is false.
  - Start, end, land and ram cues are non-looping one-shots (their wave events have no bLooping).
- **PSEUDOCODE:**
```
FMOD channel mode |= LOOP_NORMAL for wave events with bLooping   // no WFC setLoopPoints call found
Root tracked playback time (drives Envelope curves): t += dt; if root.bLooping and t >= LoopEnd:
     t = fmod(t - LoopStart, LoopEnd - LoopStart) + LoopStart       // inactive for these cues (bLooping false)
PlayLoopingSound(ac, event, fadeIn): if ac playing the same cue: return (no restart)
     else StopLoopingSound(old, fadeIn); ac = CreateAudioComponent(cue); ac.FadeIn(fadeIn, 1.0)
StopLoopingSound(ac, fadeOut): ac.bAutoDestroy = true; ac.FadeOut(fadeOut, 0.0)
```
- **ORIGINAL WFC BEHAVIOR:**
  - **Loop region:** the FMOD sample's own loop points from the **FSB** (whole sample unless the FSB sample header carries loop start/end). There is no cue-driven loop region.
  - **Intro / outro:** there is no intro/outro inside a looping cue. Intro and outro are **separate cues**: BOOST_START → BOOST_LOOP → BOOST_END, and JUMP_START → JUMP_LOOP.
  - **Stop:** a linear volume fade over FadeOutTime, then destroy. It does **not wait for a loop boundary**.
  - **Optimus fade times:** EngineFadeOutTime 0.2, BoostFadeOutTime 0.15, BoostFadeInTime 0.1, EngineFadeInTime 0.1.
  - **State switch (e.g. OnLoad ↔ OffLoad, gear):** the new loop's component fades in while the old one fades out using the same time; it is a crossfade. Asking for a cue that is already playing is a no-op.
- **SYSTEMS HANDOFF:** read loop points from each FSB sample header. Do not use the root LoopStart/LoopEnd when root bLooping is false.
- **EXPERIMENTAL CHECK NOW SAFE TO PROMOTE:**
  - Loops are per wave event.
  - Stop is an immediate linear fade, not loop-boundary aware.
- **STILL UNKNOWN:**
  - Per-sample FSB loop start/end values. These need FSB header parsing in AssetTools.
  - The native AudioComponent FadeIn/FadeOut curve, assumed to be stock UE3 linear (HIGH, not re-verified here).

## A7. Line / Volume emitter placement
- **CONFIDENCE:** CONFIRMED
- **ADDRESS:**
  - LineEmitter tick **0x82760110** (vtable 0x820A8A80): endpoints **0x82745CD0**, closest point **0x8275A338**
  - VolumeEmitter tick **0x82760278** (vtable 0x820A8DB0): closest point **0x82745FA8**
  - listener = client viewport listener (GEngine client +0x34C → vt+0x144 → +0x9C)
- **CONSTANTS:** defaults LineLength 500, Radius 500 (field +0x1CC). Streets has 13 line emitters and 17 volume emitters.
- **PSEUDOCODE:**
```
every Tick (each frame):
  L = listener location
  P = ClosestPoint(L)
  for ac in Components: if ac is AudioComponent: ac.bUseOwnerLocation = false ; ac.Location = P
  if AudioComponent exists and is not playing (and not finished): Play()
Line:   M = LocalToWorld (includes DrawScale3D); A = M.origin - M.X * (LineLength*0.5); B = M.origin + M.X * (LineLength*0.5)
        t = clamp( dot(L-A, B-A) / |B-A|^2, 0, 1 ) ; P = A + t*(B-A)
Volume: l = WorldToLocal(L); l = clamp(l, -Radius, +Radius) per axis ; P = LocalToWorld(l)   // oriented BOX, not sphere
```
- **ORIGINAL WFC BEHAVIOR:**
  - **Placement:** closest point to the listener, **not** the actor origin. It is recomputed **every frame** before the sound update.
  - **Inside a volume emitter:** P = L. Distance is 0 (full volume). Pan follows whatever SmartPan/3D rules the cue's root specifies at distance 0.
  - **Line ends:** clamped to the endpoints.
  - **One position source:** pan, attenuation, SmartPan distance and occlusion all use P, since the AudioComponent location is P.
  - **Class differences:** only the shape. Line = segment along local X; Volume = oriented box with half-extent `Radius` on all three local axes, scaled by DrawScale3D.
- **SYSTEMS HANDOFF:** use the formulas verbatim. Note that the volume emitter is a box despite the `Radius` name.
- **EXPERIMENTAL CHECK NOW SAFE TO PROMOTE:**
  - Volume-emitter loudness is constant everywhere inside the box.
  - Line-emitter position slides along the segment.
- **STILL UNKNOWN:** none.

## A8. Exact dB → linear conversion
- **CONFIDENCE:** CONFIRMED
- **ADDRESS:**
  - `dBToLinear` **0x82CBED00**
  - `SemitonesToRatio` **0x82CBEE20**
  - `pow` = 0x830ECDE0
- **PSEUDOCODE:**
```
dBToLinear(x):  x = clamp(x, -96, 0) ; return (x > -96) ? (float)pow(10.0, x * 0.05) : 0.0
SemitonesToRatio(s): s = clamp(s, -36, 36) ; return (float)pow(2.0, s * (1/12))
```
- **ORIGINAL WFC BEHAVIOR:**
  - The conversion is done in **WFC code**, not FMOD: double-precision `pow`, rounded to float.
  - **Positive dB is clamped to 0**, so no boost is possible. **≤ −96 dB is a hard 0.**
  - **Used for:**
    - SoundNodeRoot RearAttenuation and SmartPanAttenuation3D;
    - occlusion volume;
    - SoundNodeWaveEvent Volume and the six speaker-pan dB values (0x8276C1E0);
    - random volume variation.
  - **Semitones are used for:** wave Pitch, PitchVariation and occlusion pitch.
  - **Mixer category / DSP-preset Volume is NOT dB.** It is authored as linear amplitude, clamped to [0, 1], and passed straight to FMOD `setVolume` (A2).
- **SYSTEMS HANDOFF:**
  - Use the two formulas exactly, including the clamps.
  - Do not convert mixer Volume values.
- **EXPERIMENTAL CHECK NOW SAFE TO PROMOTE:**
  - A +3 dB authored node gain plays at unity.
  - −96 dB is silent.
- **STILL UNKNOWN:** the root-level `Volume` dB (e.g. −12 on vehicle roots) goes through the same wave-volume chain (0x8275FD78 path). Its clamp was not separately re-checked.
