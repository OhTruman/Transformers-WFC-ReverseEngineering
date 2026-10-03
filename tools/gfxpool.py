"""Read-only: dump AS2 constant pools (ActionConstantPool 0x88) from a Scaleform .gfx/.swf.
usage: gfxpool.py file.gfx  -> one line per DoAction/DoInitAction block: [tag sprite?] pool strings
Handles GFX/CFX (CFX = zlib after 8-byte header). Walks top-level and DefineSprite tags.
"""
import sys, struct, zlib

def load(path):
    d = open(path, 'rb').read()
    if d[:3] in (b'CFX', b'CWS'):
        d = d[:8] + zlib.decompress(d[8:])
    return d

def rect_len(b, off):
    nbits = b[off] >> 3
    return (5 + 4 * nbits + 7) // 8

def tags(b, off, end):
    while off < end:
        h = struct.unpack_from('<H', b, off)[0]; off += 2
        code, ln = h >> 6, h & 0x3f
        if ln == 0x3f:
            ln = struct.unpack_from('<I', b, off)[0]; off += 4
        yield code, off, ln
        off += ln

def pools(abuf):
    i = 0; out = []
    while i < len(abuf):
        op = abuf[i]; i += 1
        if op == 0: break
        if op >= 0x80:
            ln = struct.unpack_from('<H', abuf, i)[0]; i += 2
            body = abuf[i:i + ln]; i += ln
            if op == 0x88:
                n = struct.unpack_from('<H', body, 0)[0]; s = body[2:].split(b'\0')[:n]
                out.append([x.decode('latin1') for x in s])
    return out

def walk(b, off, end, depth, sid=None):
    for code, o, ln in tags(b, off, end):
        if code == 12: yield ('DoAction', sid, pools(b[o:o + ln]))
        elif code == 59: yield ('DoInitAction', struct.unpack_from('<H', b, o)[0], pools(b[o + 2:o + ln]))
        elif code == 39: yield from walk(b, o + 4, o + ln, depth + 1, struct.unpack_from('<H', b, o)[0])
        elif code == 56:  # ExportAssets
            n = struct.unpack_from('<H', b, o)[0]; p = o + 2; ex = []
            for _ in range(n):
                cid = struct.unpack_from('<H', b, p)[0]; p += 2; e = b.index(b'\0', p); ex.append((cid, b[p:e].decode('latin1'))); p = e + 1
            yield ('Export', None, [ex])

if __name__ == '__main__':
    b = load(sys.argv[1]); off = 8 + rect_len(b, 8) + 4
    for kind, sid, pl in walk(b, off, len(b), 0):
        for p in pl: print(kind, sid, '|'.join(map(str, p)))
