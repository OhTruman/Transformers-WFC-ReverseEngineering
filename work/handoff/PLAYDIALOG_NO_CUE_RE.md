# SeqAct_PlayDialog with no SoundCue (answer to Systems, RE, 2026-10-23)

**Answer: (a), nothing plays and the Stopped output fires (C, bytecode).**

**The chain, all in HM_Engine script:**
1. `SeqAct_PlayDialog.PlayDialog`: `HmDialogInterface(Target).PlayDialog(Cue = None, true, DialogType, false, DialogEventCallback)`.
   Target = HmDialogEmitter_8722.
2. `HmDialogEmitter.PlayDialog` → `DialogComp.Play(...)` → `HmDialogComponentImpl.PlayInternal`.
3. **`PlayInternal`: `if (None == _SoundCue) { if callback: DialogEventCallback(1); return; }`.** That happens before the
   SoundInterceptor, the dialog-type check, the priority check, replication and any state change.
   - **No line is picked from a bank.** The only random choice in the component is `GetRandomDialogCharacter` (in Playing.BeginState),
     and it's never reached.
   - The emitter's current dialog isn't stopped or interrupted.
4. `SeqAct_PlayDialog.DialogEventCallback(1)`:
   - **`OutputLinks[0].bHasImpulse = true`**. The CDO's outputs are **[0] Stopped, [1] Finished**.
   - `PlayingCount--` → −1 → clamped to 0. DisableDuckingMixerPreset is skipped on that branch.
   - Event 0 (started) never comes, so **EnableDuckingMixerPreset is never called: no ducking**.
   - **Finished never fires**: it needs event 2, a played-to-the-end cue, which also starts the PostDelay timer.

**Timing:** the Stopped impulse is set synchronously inside the op's activation, so the Stopped chain runs **in the same Kismet tick**,
depth-first (KISMET_VM_CORE_RE §4).
- H: the native op then completes on its UpdateOp because nothing is playing.

**Your current runtime behaviour (no sound, Stopped output) is exactly right.** Add: no ducking, and the same-tick output.
The same applies to events 3 (lower priority than the current line) and 4 (the component can't play that DialogType): Stopped
immediately, no sound.
