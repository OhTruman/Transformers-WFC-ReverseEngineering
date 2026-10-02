# Transformers-WFC-ReverseEngineering

Reverse-engineering notes and tooling for *Transformers: War for Cybertron* (Xbox 360), produced for a
reconstruction project from the author's own copy of the game.

This repository contains **notes, findings and analysis scripts only**. It contains no game executable,
no cooked packages, no extracted assets, no Ghidra databases and no decompiled game code. Everything under
`work/` (memory dumps, Ghidra snapshot, decompiled script output, query outputs) is ignored.

- `notes/` — findings (provenance-tagged CONFIRMED / HIGH / INFERRED / UNKNOWN)
  - `TARGETED_PASS_2026-10-01.md`, `TARGETED_PASS2_2026-10-01.md` — gameplay-native passes
  - `STEPUP_LEDGE_2026-10-01.md` — native walking/step-up/ledge/falling
  - `NETWORK_ARCHITECTURE_2026-10-01.md` — Live/Demonware/UE3 multiplayer architecture
  - `HANDOFF_2026-10-01.md` — handoffs for Gameplay / Systems / Rendering
- `tools/` — analysis scripts (UE3 bytecode decompiler, PPC reference scanners, headless Ghidra query runner); see `tools/README.md`
- `data/` — address/name tables (native function registrations, hardcoded FName globals, RPC list)
