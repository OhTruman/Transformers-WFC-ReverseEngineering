# RE-Workspace tools

Python: use `F:\Transformers Rebuild\AssetTools\bin\py\python.exe`. System python is not installed.

| tool | purpose |
|---|---|
| `ue3dis.py` | UnrealScript bytecode decompiler for cooked WFC packages (read-only). `python ue3dis.py TransGame "TnPawn.CalcVelocity"`, `--class TnFineAimManager`, or `--all <outdir> TransGame HM_Engine Engine Core` |
| `pkgload.py` | loads cooked packages from Game Dump through AssetTools' `ue3pkg.py` (in place); caches pickles in `work/script/` |
| `fname_globals.py` | rebuilds `data/fname_globals.tsv` (hardcoded FName globals from 0x83612160) |
| `lohi.py` | loose lis/addi address-reference search (wider window than ppcrefs) |
| `ppcrefs.py`, `xeximg.py`, `xcemu.py`, `scan_native_lookup.py` | offline image access / refs / CRT-init emulation / native table scan |
| `wfcq.ps1` + `ghidra_scripts/WfcQuery.java` | headless **read-only** Ghidra queries against `work/ghidra-snapshot` (refs/decomp/asm/strs/func) when ReVa is unavailable. `powershell -File tools\wfcq.ps1 <queries.txt> <out.txt>` |

Decompiled script dump: `work/script/decomp/` (regenerate with `ue3dis.py --all`).

Added in the step-up/ledge pass:
| `fnref.py` | find code refs to hardcoded FName globals (base 0x83826580, base+offset addressing) |
| `floatref.py` / `floatref2.py` | find functions loading given float constants (strict / loose lis tracking) |
| `scan_natives_full.py` | full `int<Class>exec<Func>` native table scan → `data/native_functions_full.tsv` (2451 entries); unresolved slots were filled by emulating their CRT initializers with `xcemu.Emu` |
| `WfcQuery.java` extra commands | `named`, `comments`, `bookmarks`, `labels <substr>` (import labels such as `__imp__NetDll_XNet*` survive in the snapshot) |
| `rpc_dump.py` | list every UnrealScript RPC (FUNC_Net) with side/reliability → `data/rpcs.tsv` |

Added in Milestone 03:
| `WfcQuery.java dis <addr> <n>` | disassemble undefined bytes in memory only (snapshot opened `-readOnly`, never saved). Use it for vtable targets Ghidra never disassembled |
| `xenosdis.py` / `xenostrace.py` | Xenos shader microcode disassembler and symbolic constant tracer for WFC ShaderCache blobs (read-only) |
| `xenosvsemu.py` | CF-aware numeric emulator for Xenos vertex shaders (COND_JMP + predicates, `mstart` microcode override); used for Beam/Trail side expansion (pass 5 §13) and sprite alignment (§15) |
| `hover_pitch_est.py` | Pitch-plane estimate of the original hover car/truck crossing a step riser (TnSpring law, diagonal probes, no grounded pitch correction) (pass 4 A4 addendum) |
| `WfcQuery.java rawdis <addr> <n>` | linear per-instruction disassembly (in memory, read-only). Use it where Ghidra stops at callers of 0x830101E0, which it wrongly treats as no-return |
- `xenosemu.py` — numeric emulator for straight-line Xenos pixel-shader ALU code (pre-load fetched values per fetch address); used to verify the BlurShadowMask kernel.
- `streets_smca_scale.py` — emits the per-component Scale·Scale3D (and Translation/Rotation) that UE3 applies on top of StaticMeshCollectionActor CachedParentToWorld; writes `notes/data/streets_smca_component_scale.json`.
- `glbray.py` — read-only GLB loader + numpy ray caster (used for gameplay-viewpoint visibility tests of map faces).
- `gfxpool.py` — read-only Scaleform .gfx/.swf reader: dumps AS2 constant pools of DoAction/DoInitAction (incl. sprites) and ExportAssets.
- `gfxcallgraph.py` — builds `notes/data/frontend_gfx_callbacks.json`: per-movie AS→engine ExternalInterface calls (pool-level), data-store bindings, and engine→AS `_global.*` callbacks from decompiled script + authored defaults.
- `as2dis.py` — read-only AS2 bytecode disassembler for Scaleform .gfx with expression folding (DefineFunction2 registers, constant pools, CallMethod/SetMember). `as2dis.py movie.gfx [filter]`. Used for `notes/data/frontend_menu_graph.json`.
- `gfxplace.py` — read-only: named PlaceObject placements (sprite, depth, char, matrix translate/scale) for a Scaleform .gfx; used for the HUD anchor/layout map.
- `ghidra_scripts/WfcDispScan.java` — read-only headless scan: functions using ALL given displacements/immediates (find field users, e.g. Scale/Scale3D offsets).
- `ghidra_scripts/WfcStoreScan.java` — read-only headless scan: instructions with a mnemonic prefix and displacement inside functions that also use other displacements (find field writers).
- `ghidra_scripts/WfcDecompAt.java` — read-only: create a function in memory (explicit `addr:size` body; clears false no-return flags in memory) and decompile code Ghidra never defined. Never saves.
| `matgraph.py` | print a material input (e.g. EmissiveColor) as an expression tree from authored.db; used for TR_Defrag_MAT (pass 5 §12 add. 24/26) |
| `physprop.py` | parse TnPhysicalMaterialProperty / HmPhysicalMaterialProperty exports (missing from authored.db) → `notes/data/physical_material_properties.json` (pass 5 §12 add. 29) |
| `mp_progression_extract.py` | XP events, level table, challenges, class unlocks, game modes, kill awards, MP nav audit → `notes/data/mp_*.json` (MP_PROGRESSION_SCORING_AI_2026-10-06.md) |
- `work/script/decomp_tc/` — TransContent script (game classes) decompiled from MP map packages: `python ue3dis.py --all ../work/script/decomp_tc MP_ORB_Debris_BASE_m MP_IAC_Streets_BASE_m`.
