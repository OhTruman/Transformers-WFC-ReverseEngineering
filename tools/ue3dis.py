"""UnrealScript bytecode decompiler for WFC cooked packages (UE3 v511 / licensee 144, big-endian).

Read-only. Layout CONFIRMED on TnPlayerController.PressJump / Object.Multiply_FloatFloat:
  UFunction export = i32 ? , FName None, i32 SuperField, i32 Next, i32 ScriptText, i32 Children,
                     i32 CppText, i32 Line, i32 TextPos, i32 ScriptSize, <script>, u16 iNative, u8 OperPrec, ...
  Context(0x19/0x12) = expr, u16 skip, u8 size, expr   (no field ref at this version)
  Switch(0x05) = u8 size, expr
Usage:  python ue3dis.py TransGame "TnPlayerController.PressJump" [...]
        python ue3dis.py TransGame --class TnFineAimManager      (all functions of a class)
"""
import os, sys, struct, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pkgload import load, find, CACHE

NATIVE_PKGS = ["Core", "Engine", "HM_Engine", "TransGame"]
OPS = {"Multiply": "*", "Divide": "/", "Add": "+", "Subtract": "-", "Less": "<", "Greater": ">",
       "LessEqual": "<=", "GreaterEqual": ">=", "EqualEqual": "==", "NotEqual": "!=", "AndAnd": "&&",
       "OrOr": "||", "XorXor": "^^", "And": "&", "Or": "|", "Xor": "^", "Percent": "%",
       "MultiplyEqual": "*=", "DivideEqual": "/=", "AddEqual": "+=", "SubtractEqual": "-=",
       "Concat": "$", "At": "@", "Dot": "dot", "Cross": "cross", "ComplementEqual": "~=",
       "MultiplyMultiply": "**", "LessLess": "<<", "GreaterGreater": ">>"}


def native_table():
    path = os.path.join(CACHE, "natives.json")
    if os.path.exists(path):
        return {int(k): v for k, v in json.load(open(path)).items()}
    tab = {}
    for pk in NATIVE_PKGS:
        p = load(pk)
        for i, e in enumerate(p.exports, 1):
            if p.class_name(e) != "Function": continue
            d = p.data[e["serial_offset"]:e["serial_offset"] + e["serial_size"]]
            if len(d) < 44: continue
            ss = struct.unpack_from(">i", d, 40)[0]
            o = 44 + ss
            if o + 3 > len(d): continue
            nat, prec = struct.unpack_from(">HB", d, o)
            if nat:
                tab.setdefault(nat, p.full_path(i))
    json.dump(tab, open(path, "w"), indent=0)
    return tab


class Dis:
    def __init__(self, pkg, nat):
        self.p = pkg; self.nat = nat

    def obj(self, idx):
        if idx == 0: return "None"
        try:
            return self.p.full_path(idx)
        except Exception:
            return "?obj%d" % idx

    def short(self, idx):
        return self.obj(idx).split(".")[-1]

    def name(self, o):
        i, n = struct.unpack_from(">ii", self.s, o)
        nm = self.p.names[i] if 0 <= i < len(self.p.names) else "?n%d" % i
        return (nm if n == 0 else "%s_%d" % (nm, n - 1)), o + 8

    def u8(self, o): return self.s[o], o + 1
    def u16(self, o): return struct.unpack_from(">H", self.s, o)[0], o + 2
    def i32(self, o): return struct.unpack_from(">i", self.s, o)[0], o + 4

    def parms(self, o):
        args = []
        while self.s[o] != 0x16:
            a, o = self.expr(o); args.append(a)
        return args, o + 1

    def native_call(self, idx, o):
        args, o = self.parms(o)
        fn = self.nat.get(idx, "native%d" % idx)
        short = fn.split(".")[-1]
        base = short.split("_")[0]
        if base in OPS and len(args) == 2:
            return "(%s %s %s)" % (args[0], OPS[base], args[1]), o
        if short.startswith("Not_Pre") and len(args) == 1: return "!" + args[0], o
        if short.startswith("Subtract_Pre") and len(args) == 1: return "-" + args[0], o
        return "%s(%s)" % (short, ", ".join(args)), o

    def expr(self, o):
        s = self.s; t = s[o]; o += 1
        if t == 0x00: v, o = self.i32(o); return self.short(v), o
        if t == 0x01: v, o = self.i32(o); return "self." + self.short(v), o
        if t == 0x02: v, o = self.i32(o); return "default." + self.short(v), o
        if t == 0x03: v, o = self.i32(o); return "state." + self.short(v), o
        if t == 0x04: e, o = self.expr(o); return "return " + e, o
        if t == 0x05:
            sz, o = self.u8(o); e, o = self.expr(o); return "switch (%s)" % e, o
        if t == 0x06: v, o = self.u16(o); return "goto 0x%04x" % v, o
        if t == 0x07:
            v, o = self.u16(o); e, o = self.expr(o); return "if !(%s) goto 0x%04x" % (e, v), o
        if t == 0x08: return "stop", o
        if t == 0x09:
            ln, o = self.u16(o); dbg, o = self.u8(o); e, o = self.expr(o); return "assert(%s)" % e, o
        if t == 0x0A:
            v, o = self.u16(o)
            if v == 0xFFFF: return "default:", o
            e, o = self.expr(o); return "case %s: (next 0x%04x)" % (e, v), o
        if t == 0x0B: return "nothing", o
        if t == 0x0C:
            out = []
            while True:
                n, o = self.name(o); off, o = self.i32(o)
                if n == "None": break
                out.append("%s@0x%04x" % (n, off))
            return "labels[%s]" % ", ".join(out), o
        if t == 0x0D: e, o = self.expr(o); return "goto label " + e, o
        if t == 0x0E: v, o = self.i32(o); e, o = self.expr(o); return e, o
        if t == 0x0F: a, o = self.expr(o); b, o = self.expr(o); return "%s = %s" % (a, b), o
        if t == 0x10: a, o = self.expr(o); b, o = self.expr(o); return "%s[%s]" % (a, b), o
        if t == 0x11:
            parts = []
            for _ in range(5):
                e, o = self.expr(o); parts.append(e)
            return "new(%s)" % ", ".join(parts), o
        if t in (0x12, 0x19):
            a, o = self.expr(o); sk, o = self.u16(o); sz, o = self.u8(o); b, o = self.expr(o)
            if b.startswith("self."): b = b[5:]
            return ("%s.static.%s" if t == 0x12 else "%s.%s") % (a, b), o
        if t == 0x13: v, o = self.i32(o); e, o = self.expr(o); return "class<%s>(%s)" % (self.short(v), e), o
        if t == 0x14: a, o = self.expr(o); b, o = self.expr(o); return "%s = %s" % (a, b), o
        if t == 0x15: return "<endparm>", o
        if t == 0x16: return "<endparms>", o
        if t == 0x17: return "self", o
        if t == 0x18: v, o = self.u16(o); e, o = self.expr(o); return e, o
        if t == 0x1A: a, o = self.expr(o); b, o = self.expr(o); return "%s[%s]" % (a, b), o
        if t == 0x1B:
            n, o = self.name(o); args, o = self.parms(o); return "%s(%s)" % (n, ", ".join(args)), o
        if t == 0x1C:
            v, o = self.i32(o); args, o = self.parms(o)
            fp = self.obj(v); sh = fp.split(".")[-1]
            return "%s(%s)" % (fp if fp.count(".") <= 1 else sh, ", ".join(args)), o
        if t == 0x1D: v, o = self.i32(o); return str(v), o
        if t == 0x1E: v = struct.unpack_from(">f", s, o)[0]; return repr(round(v, 7)), o + 4
        if t == 0x1F:
            e = s.index(b"\0", o); return '"%s"' % s[o:e].decode("latin1"), e + 1
        if t == 0x20: v, o = self.i32(o); return "obj'%s'" % self.obj(v), o
        if t == 0x21: n, o = self.name(o); return "'%s'" % n, o
        if t == 0x22: v = struct.unpack_from(">3i", s, o); return "rot(%d,%d,%d)" % v, o + 12
        if t == 0x23: v = struct.unpack_from(">3f", s, o); return "vect(%g,%g,%g)" % v, o + 12
        if t == 0x24: v, o = self.u8(o); return "%d" % v, o
        if t == 0x25: return "0", o
        if t == 0x26: return "1", o
        if t == 0x27: return "true", o
        if t == 0x28: return "false", o
        if t == 0x29: v, o = self.i32(o); return self.short(v), o
        if t == 0x2A: return "none", o
        if t == 0x2C: v, o = self.u8(o); return "%d" % v, o
        if t == 0x2D: e, o = self.expr(o); return e, o
        if t == 0x2E: v, o = self.i32(o); e, o = self.expr(o); return "%s(%s)" % (self.short(v), e), o
        if t == 0x2F: e, o = self.expr(o); v, o = self.u16(o); return "foreach %s (end 0x%04x)" % (e, v), o
        if t == 0x30: return "iterpop", o
        if t == 0x31: return "iternext", o
        if t in (0x32, 0x33):
            v, o = self.i32(o); a, o = self.expr(o); b, o = self.expr(o)
            return "(%s %s %s)" % (a, "==" if t == 0x32 else "!=", b), o
        if t == 0x34:
            e = o
            while s[e] or s[e + 1]: e += 2
            return 'u"%s"' % s[o:e].decode("utf-16-be", "replace"), e + 2
        if t == 0x35:
            pr, o = self.i32(o); st, o = self.i32(o); b1, o = self.u8(o); b2, o = self.u8(o); e, o = self.expr(o)
            return "%s.%s" % (e, self.short(pr)), o
        if t == 0x36: e, o = self.expr(o); return "%s.Length" % e, o
        if t == 0x37:
            n, o = self.name(o); args, o = self.parms(o); return "global.%s(%s)" % (n, ", ".join(args)), o
        if t == 0x38:
            c, o = self.u8(o); e, o = self.expr(o); return "cast%02x(%s)" % (c, e), o
        if t == 0x39:
            a, o = self.expr(o); b, o = self.expr(o); c, o = self.expr(o); return "%s.Insert(%s,%s)" % (a, b, c), o
        if t == 0x3A: v, o = self.i32(o); return "return", o
        if t in (0x3B, 0x3C, 0x3D, 0x3E):
            a, o = self.expr(o); b, o = self.expr(o); return "(%s %s %s)" % (a, "==" if t in (0x3B, 0x3D) else "!=", b), o
        if t == 0x3F: return "emptydelegate", o
        if t == 0x40:
            a, o = self.expr(o); b, o = self.expr(o); c, o = self.expr(o); return "%s.Remove(%s,%s)" % (a, b, c), o
        if t == 0x41: return "debuginfo", o + 13
        if t == 0x42:
            b, o = self.u8(o); v, o = self.i32(o); n, o = self.name(o); args, o = self.parms(o)
            return "%s(%s)" % (n, ", ".join(args)), o
        if t == 0x43: n, o = self.name(o); return "delegate." + n, o
        if t == 0x44: a, o = self.expr(o); b, o = self.expr(o); return "%s = %s" % (a, b), o
        if t == 0x45:
            c, o = self.expr(o); s1, o = self.u16(o); a, o = self.expr(o); s2, o = self.u16(o); b, o = self.expr(o)
            return "(%s ? %s : %s)" % (c, a, b), o
        if t == 0x46:
            a, o = self.expr(o); sk, o = self.u16(o); b, o = self.expr(o); return "%s.Find(%s)" % (a, b), o
        if t == 0x47:
            a, o = self.expr(o); sk, o = self.u16(o); b, o = self.expr(o); c, o = self.expr(o)
            return "%s.Find(%s,%s)" % (a, b, c), o
        if t == 0x48: v, o = self.i32(o); return self.short(v), o
        if t == 0x49:
            sk, o = self.u16(o); e, o = self.expr(o)
            if s[o] == 0x15: o += 1
            return "default=" + e, o
        if t == 0x4A: return "", o
        if t == 0x4B: n, o = self.name(o); return "delegate." + n, o
        if t == 0x51: e, o = self.expr(o); return e, o
        if t == 0x52: v, o = self.i32(o); e, o = self.expr(o); return "%s(%s)" % (self.short(v), e), o
        if t == 0x53: return "<eos>", o
        if t == 0x54: a, o = self.expr(o); b, o = self.expr(o); return "%s.Add(%s)" % (a, b), o
        if t == 0x55:
            a, o = self.expr(o); sk, o = self.u16(o); b, o = self.expr(o); return "%s.AddItem(%s)" % (a, b), o
        if t == 0x56:
            a, o = self.expr(o); sk, o = self.u16(o); b, o = self.expr(o); return "%s.RemoveItem(%s)" % (a, b), o
        if t == 0x57:
            a, o = self.expr(o); sk, o = self.u16(o); b, o = self.expr(o); c, o = self.expr(o)
            return "%s.InsertItem(%s,%s)" % (a, b, c), o
        if t == 0x58:
            a, o = self.expr(o); b, o = self.expr(o); u, o = self.u8(o); c, o = self.expr(o); sk, o = self.u16(o)
            return "foreach %s(%s,%s) (end 0x%04x)" % (a, b, c, sk), o
        if 0x60 <= t < 0x70:
            b, o = self.u8(o); return self.native_call(((t - 0x60) << 8) | b, o)
        if t >= 0x70:
            return self.native_call(t, o)
        raise ValueError("unknown token 0x%02x at 0x%x" % (t, o - 1))

    def function(self, idx):
        e = self.p.exports[idx - 1]
        d = self.p.data[e["serial_offset"]:e["serial_offset"] + e["serial_size"]]
        ss = struct.unpack_from(">i", d, 40)[0]
        self.s = d[44:44 + ss] + b"\x53" * 8
        out = []
        o = 0
        while o < ss:
            st = o
            try:
                txt, o = self.expr(o)
            except Exception as ex:
                out.append("  %04x: !! %s ; raw %s" % (st, ex, self.s[st:st + 24].hex()))
                break
            out.append("  %04x: %s" % (st, txt))
        tail = d[44 + ss:]
        nat = struct.unpack_from(">H", tail, 0)[0] if len(tail) >= 2 else 0
        hdr = "function %s  (script %d bytes%s)" % (self.p.full_path(idx), ss, ", native %d" % nat if nat else "")
        return hdr + "\n" + "\n".join(out)


def dump_all(pk, outdir):
    p = load(pk); nat = native_table(); D = Dis(p, nat)
    os.makedirs(outdir, exist_ok=True)
    by = {}
    bad = 0
    for i, e in enumerate(p.exports, 1):
        if p.class_name(e) != "Function": continue
        fp = p.full_path(i)
        txt = D.function(i)
        if "!!" in txt: bad += 1
        by.setdefault(fp.split(".")[0], []).append(txt)
    for c, fs in by.items():
        with open(os.path.join(outdir, "%s.%s.txt" % (pk, c)), "w", encoding="utf-8") as f:
            f.write("\n\n".join(fs))
    print(pk, "classes", len(by), "functions", sum(map(len, by.values())), "decode failures", bad)


def main():
    if sys.argv[1] == "--all":
        for pk in sys.argv[3:]: dump_all(pk, sys.argv[2])
        return
    pk = sys.argv[1]
    p = load(pk); nat = native_table(); D = Dis(p, nat)
    args = sys.argv[2:]
    if args and args[0] == "--class":
        cls = args[1]
        for i, e in enumerate(p.exports, 1):
            if p.class_name(e) == "Function":
                fp = p.full_path(i)
                if fp.split(".")[0] == cls:
                    print(D.function(i)); print()
        return
    for a in args:
        i, e = find(p, a)
        if not e: print("not found", a); continue
        print(D.function(i)); print()


if __name__ == "__main__":
    main()
