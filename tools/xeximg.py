"""Offline access to the default.xex memory image dumped by DumpMemoryImage.java.

All values are big-endian (Xenon PPC). Addresses are virtual addresses.
"""
import os, struct

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "work", "image")


class Image:
    def __init__(self, path=IMG):
        self.blocks = []
        with open(os.path.join(path, "blocks.tsv"), encoding="utf-8") as f:
            next(f)
            for line in f:
                fn, start, size, ex = line.rstrip("\n").split("\t")
                with open(os.path.join(path, fn), "rb") as bf:
                    data = bf.read()
                self.blocks.append((fn[:-4], int(start, 16), data, ex == "true"))

    def block(self, name):
        for b in self.blocks:
            if b[0] == name:
                return b
        raise KeyError(name)

    def find(self, va):
        for name, start, data, ex in self.blocks:
            if start <= va < start + len(data):
                return data, va - start
        return None, None

    def range(self, name):
        _, s, d, _ = self.block(name)
        return s, s + len(d)

    def u32(self, va):
        d, o = self.find(va)
        return None if d is None or o + 4 > len(d) else struct.unpack_from(">I", d, o)[0]

    def f32(self, va):
        d, o = self.find(va)
        return None if d is None or o + 4 > len(d) else struct.unpack_from(">f", d, o)[0]

    def f64(self, va):
        d, o = self.find(va)
        return None if d is None or o + 8 > len(d) else struct.unpack_from(">d", d, o)[0]

    def wstr(self, va, maxlen=512):
        d, o = self.find(va)
        if d is None:
            return None
        out = []
        while o + 1 < len(d) and len(out) < maxlen:
            c = (d[o] << 8) | d[o + 1]
            if c == 0:
                return "".join(out)
            if c < 0x20 or c > 0x7E:
                return None
            out.append(chr(c))
            o += 2
        return None

    def astr(self, va, maxlen=512):
        d, o = self.find(va)
        if d is None:
            return None
        e = d.find(b"\0", o, o + maxlen)
        if e < 0:
            return None
        s = d[o:e]
        try:
            t = s.decode("ascii")
        except UnicodeDecodeError:
            return None
        return t if all(0x20 <= ord(c) < 0x7F for c in t) else None
