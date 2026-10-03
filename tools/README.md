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
| `WfcQuery.java rawdis <addr> <n>` | linear per-instruction disassembly (in memory, read-only). Use it where Ghidra stops at callers of 0x830101E0, which it wrongly treats as no-return |
- `xenosemu.py` — numeric emulator for straight-line Xenos pixel-shader ALU code (pre-load fetched values per fetch address); used to verify the BlurShadowMask kernel.
- `streets_smca_scale.py` — emits the per-component Scale·Scale3D (and Translation/Rotation) that UE3 applies on top of StaticMeshCollectionActor CachedParentToWorld; writes `notes/data/streets_smca_component_scale.json`.
