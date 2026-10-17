"""Read-only: resolve a shader GUID inside a cooked package's ShaderCache to its Xenos blob and print the CTAB, the float words
around the literal block, and the microcode disassembly (tools/xenosdis.py).
Shader record = FName type (u32 index, u32 0), GUID (16), u32 end offset, u32, u16, then the blob (0x102A1100 PS / 0x102A1101 VS).
Usage: python shader_by_guid.py <package> <guid-hex> [<guid-hex> ...]"""
import os, sys, struct
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, r"F:\Transformers Rebuild\AssetTools\scripts\wfc")
import ue3pkg, xenosdis as X

DUMP = r"F:\Transformers Rebuild\Game Dump\TransGame\CookedXenon"


def blob_for(d, guid):
    g = bytes.fromhex(guid); k = d.find(g)
    while k != -1:
        b = d.find(b"\x10\x2a\x11", k + 16, k + 48)
        if b != -1: return b
        k = d.find(g, k + 1)
    return None


def dump(d, b):
    kind = "PS" if d[b + 3] == 0 else "VS"
    hdr = struct.unpack_from(">12I", d, b)
    out = ["blob @%#x %s hdr %s" % (b, kind, [hex(x) for x in hdr[:12]])]
    ver, tgt, cs = X.parse_ctab(d, b + 0x28)
    out.append("CTAB " + ", ".join("%s %s c%d x%d" % c for c in cs))
    off = hdr[1]
    words = []
    for q in range(off, off + 0x80, 4):
        f = struct.unpack_from(">f", d, b + q)[0]; u = struct.unpack_from(">I", d, b + q)[0]
        words.append("%g" % f if u and 1e-6 < abs(f) < 1e7 else ("0" if u == 0 else "."))
    out.append("float words from hdr[1]: " + " ".join(words))
    M, cfs = X.find_microcode(d, b + off, b + off + 0x2000)
    out += X.disasm(d, M, cfs) if M else ["(microcode not found)"]
    return "\n".join(out)


if __name__ == "__main__":
    p = ue3pkg.Package(os.path.join(DUMP, sys.argv[1] + ".xxx")); d = p.data
    for g in sys.argv[2:]:
        b = blob_for(d, g)
        print("== %s %s" % (g, dump(d, b) if b else "blob not in this package"))
