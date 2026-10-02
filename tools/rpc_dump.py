"""List UnrealScript RPCs (FUNC_Net) per package -> data/rpcs.tsv.
Flags: u32 BE at script_end+7 (CONFIRMED on ServerTransform/ClientTeleport). Bits: 0x40 Net, 0x80 Reliable, 0x100 Simulated,
0x200000 NetServer, 0x1000000 NetClient, 0x800000 HasDefaults, 0x400000 HasOutParms."""
import os, struct
from pkgload import load
from xeximg import ROOT
rows = []
for pk in ["Engine", "HM_Engine", "TransGame", "IpDrv", "OnlineSubsystemLive", "Demonware"]:
    p = load(pk)
    for i, e in enumerate(p.exports, 1):
        if p.class_name(e) != "Function": continue
        d = p.data[e["serial_offset"]:e["serial_offset"] + e["serial_size"]]
        if len(d) < 44: continue
        ss = struct.unpack_from(">i", d, 40)[0]
        if 44 + ss + 11 > len(d): continue
        fl = struct.unpack_from(">I", d, 44 + ss + 7)[0]
        if fl & 0x40:
            side = "server" if fl & 0x200000 else ("client" if fl & 0x1000000 else "multicast?")
            rows.append((pk, p.full_path(i), side, "reliable" if fl & 0x80 else "unreliable", "0x%08x" % fl))
with open(os.path.join(ROOT, "data", "rpcs.tsv"), "w", encoding="utf-8") as f:
    f.write("package\tfunction\tside\treliability\tflags\n")
    for r in rows: f.write("\t".join(r) + "\n")
print(len(rows))
