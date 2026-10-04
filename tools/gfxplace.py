"""Read-only: list named PlaceObject2/3 instances in a Scaleform .gfx with their matrix (translate in pixels, scale, rotate skew)
and the containing sprite id / export name. Root timeline = sprite None.
usage: gfxplace.py movie.gfx [name-filter]
"""
import sys, struct, os
sys.path.insert(0, os.path.dirname(__file__))
import gfxpool

class BR:
    def __init__(s, d, o): s.d = d; s.o = o * 8
    def u(s, n):
        v = 0
        for _ in range(n): v = (v << 1) | ((s.d[s.o >> 3] >> (7 - (s.o & 7))) & 1); s.o += 1
        return v
    def sb(s, n):
        if n == 0: return 0
        v = s.u(n)
        return v - (1 << n) if v & (1 << (n - 1)) else v

def matrix(b, p):
    r = BR(b, p); sx = sy = 1.0; r0 = r1 = 0.0
    if r.u(1): n = r.u(5); sx = r.sb(n) / 65536.0; sy = r.sb(n) / 65536.0
    if r.u(1): n = r.u(5); r0 = r.sb(n) / 65536.0; r1 = r.sb(n) / 65536.0
    n = r.u(5); tx = r.sb(n) / 20.0; ty = r.sb(n) / 20.0
    return (tx, ty, sx, sy, r0, r1), (r.o + 7) // 8

def placements(path):
    b = gfxpool.load(path); off = 8 + gfxpool.rect_len(b, 8) + 4
    out = []
    def walk(o0, end, sid):
        for code, o, ln in gfxpool.tags(b, o0, end):
            if code == 39: walk(o + 4, o + ln, struct.unpack_from('<H', b, o)[0])
            elif code in (26, 70):
                p = o; fl = b[p]; p += 1; fl2 = 0
                if code == 70: fl2 = b[p]; p += 1
                depth = struct.unpack_from('<H', b, p)[0]; p += 2
                if code == 70 and (fl2 & 8): e = b.index(b'\0', p); p = e + 1
                cid = None
                if fl & 2: cid = struct.unpack_from('<H', b, p)[0]; p += 2
                m = None
                if fl & 4: m, p = matrix(b, p)
                if fl & 8:
                    r = BR(b, p); ha = r.u(1); hm = r.u(1); n = r.u(4)
                    for _ in range(4 * (ha + hm)): r.u(n)
                    p = (r.o + 7) // 8
                if fl & 16: p += 2
                name = None
                if fl & 32: e = b.index(b'\0', p); name = b[p:e].decode('latin1'); p = e + 1
                if name: out.append((sid, depth, cid, name, m))
    walk(off, len(b), None)
    return out

if __name__ == '__main__':
    exports = {}
    b = gfxpool.load(sys.argv[1]); off = 8 + gfxpool.rect_len(b, 8) + 4
    for kind, sid, pl in gfxpool.walk(b, off, len(b), 0):
        if kind == 'Export':
            for cid, nm in pl[0]: exports[cid] = nm
    flt = sys.argv[2] if len(sys.argv) > 2 else ''
    for sid, depth, cid, name, m in placements(sys.argv[1]):
        if flt and flt not in name: continue
        ms = 'tx=%.1f ty=%.1f sx=%.3f sy=%.3f' % (m[0], m[1], m[2], m[3]) if m else '-'
        print('sprite=%s(%s) depth=%d char=%s(%s) %s %s' % (sid, exports.get(sid, ''), depth, cid, exports.get(cid, ''), name, ms))
