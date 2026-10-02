"""Symbolic forward trace of selected inputs through a Xenos pixel shader (straight-line, ignores predication).
Seeds: a float constant register (e.g. DynamicShadowLuminanceScale) and a texture sampler (e.g. ShadowMaskTexture).
Every register component that depends on a seed holds an expression string; everything else is an opaque leaf.
Prints the expression of every write that depends on a seed, ending with the oC0 export.
Usage: python xenostrace.py <blob.bin> <container_offset>
"""
import struct, sys
import xenosdis as X
B = X.bits
C = 'xyzw'

def run(d, H, seed_const_name='DynamicShadowLuminanceScale', seed_sampler_name='ShadowMaskTexture', maxlen=400):
    ver, tgt, cs = X.parse_ctab(d, H + 0x28)
    creg = {c[0]: c[2] for c in cs}
    sc = creg.get(seed_const_name); ss = creg.get(seed_sampler_name)
    M, cfs = X.find_microcode(d, H + 0x28, H + 0x6000)
    # literal constants: vectors immediately before M, assigned c(256-n)..c255 (n = nonzero-ending run)
    lit = {}
    k = 1
    while k < 16:
        v = struct.unpack_from('>4f', d, M - 16 * k)
        if all(x == 0 for x in v) and k > 1 and all(x == 0 for x in struct.unpack_from('>4f', d, M - 16 * (k + 1))):
            break
        k += 1
    vecs = [struct.unpack_from('>4f', d, M - 16 * j) for j in range(k - 1, 0, -1)]
    while vecs and all(x == 0 for x in vecs[0]): vecs.pop(0)
    for i, v in enumerate(vecs): lit[256 - len(vecs) + i] = v
    R = {}   # (reg, comp) -> expr or None
    PS = [None]
    def cval(reg, comp, absc=False):
        if reg == sc: return 'DSLS' if comp == 0 else None
        return None
    def get(reg, sel, neg, comp, absc):
        if sel:
            e = R.get((reg & 0x3F, comp))
        else:
            e = cval(reg, comp)
            if e is None: return None
        if e is None: return None
        if reg & 0x80 and sel: e = '|%s|' % e
        return ('-(%s)' % e) if neg else e
    def leaf(reg, sel, comp):
        return ('r%d.%s' % (reg & 0x3F, C[comp])) if sel else ('c%d.%s' % (reg, C[comp]))
    def val(reg, sel, neg, comp, absc):
        e = get(reg, sel, neg, comp, absc)
        if e is not None: return e, True
        if not sel and reg in lit: return '%g' % ((-1 if neg else 1) * lit[reg][comp]), False
        l = leaf(reg, sel, comp); return ('-' + l if neg else l), False
    out = []
    instrs = []
    for c in cfs:
        op = B(c, 44, 4)
        if op in (1, 2, 3, 4, 5, 6, 13, 14):
            addr, cnt, seq = B(c, 0, 12), B(c, 12, 3), B(c, 16, 12)
            for i in range(cnt):
                instrs.append((addr + i, B(seq, 2 * i, 1), struct.unpack_from('>3I', d, M + 12 * (addr + i))))
            if op in (2, 4, 6, 14): break
    for a, isf, (w0, w1, w2) in instrs:
        if isf:
            op = B(w0, 0, 5)
            if op == 1:
                dr = B(w0, 12, 6); ci = B(w0, 20, 5); dsw = B(w1, 0, 12)
                for i in range(4):
                    s = B(dsw, 3 * i, 3)
                    if s < 4:
                        R[(dr, i)] = ('SHADOWMASK.%s' % C[s]) if ci == ss else None
                    elif s in (4, 5):
                        R[(dr, i)] = None
            continue
        vdst = B(w0, 0, 6); absc = B(w0, 7, 1); sdst = B(w0, 8, 6); exp = B(w0, 15, 1)
        vmask = B(w0, 16, 4); smask = B(w0, 20, 4); vcl = B(w0, 24, 1); scl = B(w0, 25, 1); sop = B(w0, 26, 6)
        sws = [B(w1, 16, 8), B(w1, 8, 8), B(w1, 0, 8)]; negs = [B(w1, 26, 1), B(w1, 25, 1), B(w1, 24, 1)]
        regs = [B(w2, 16, 8), B(w2, 8, 8), B(w2, 0, 8)]; sels = [B(w2, 31, 1), B(w2, 30, 1), B(w2, 29, 1)]
        vop = B(w2, 24, 5)
        def sv(si, comp_dst):
            comp = (B(sws[si], 2 * comp_dst, 2) + comp_dst) & 3
            return val(regs[si], sels[si], negs[si], comp, absc)
        newR = {}
        if vmask:
            for i in range(4):
                if not (vmask >> i & 1): continue
                if vop in (15, 16):
                    n = 4 if vop == 15 else 3
                    terms = [(sv(0, j), sv(1, j)) for j in range(n)]
                    if any(t[0][1] or t[1][1] for t in terms):
                        e = 'dot(%s)' % ' + '.join('%s*%s' % (t[0][0], t[1][0]) for t in terms)
                    else: e = None
                else:
                    a0, b0, c0 = sv(0, i), sv(1, i), sv(2, i)
                    if vop == 0: e = '(%s + %s)' % (a0[0], b0[0]) if (a0[1] or b0[1]) else None
                    elif vop == 1: e = '(%s * %s)' % (a0[0], b0[0]) if (a0[1] or b0[1]) else None
                    elif vop == 2: e = 'max(%s, %s)' % (a0[0], b0[0]) if (a0[1] or b0[1]) else None
                    elif vop == 3: e = 'min(%s, %s)' % (a0[0], b0[0]) if (a0[1] or b0[1]) else None
                    elif vop == 11: e = '(%s * %s + %s)' % (a0[0], b0[0], c0[0]) if (a0[1] or b0[1] or c0[1]) else None
                    elif vop in (12, 13, 14): e = 'cnd%d(%s ? %s : %s)' % (vop, a0[0], b0[0], c0[0]) if (a0[1] or b0[1] or c0[1]) else None
                    else: e = ('%s(%s)' % (X.VOP[vop], a0[0])) if a0[1] else None
                if e is not None and vcl: e = 'sat(%s)' % e
                if e is not None and len(e) > maxlen: e = e[:maxlen] + '...'
                newR[(vdst, i, 'v')] = e
                if e is not None:
                    out.append('%3d %s%s.%s = %s' % (a, 'oC' if exp else 'r', vdst, C[i], e))
        # scalar
        a_c = (B(sws[2], 6, 2) + 3) & 3; b_c = B(sws[2], 0, 2) & 3
        se = None
        if sop in (42, 43, 44, 45, 46, 47):
            tr = (sws[2] & 0x3C) | (sels[2] << 1) | (sop & 1)
            ca = val(regs[2], 0, negs[2], a_c, absc); tb = val(tr, 1, 0, b_c, 0)
            o = {42: '*', 43: '*', 44: '+', 45: '+', 46: '-', 47: '-'}[sop]
            if ca[1] or tb[1]: se = '(%s %s %s)' % (ca[0], o, tb[0])
        elif sop == 50:
            se = PS[0]
        else:
            A = val(regs[2], sels[2], negs[2], a_c, absc); Bv = val(regs[2], sels[2], negs[2], b_c, absc)
            ps = PS[0]
            if sop == 0: se = '(%s + %s)' % (A[0], Bv[0]) if (A[1] or Bv[1]) else None
            elif sop == 2: se = '(%s * %s)' % (A[0], Bv[0]) if (A[1] or Bv[1]) else None
            elif sop in (5, 6): se = A[0] if (A[1] and A[0] == Bv[0]) else (('%s(%s, %s)' % (X.SOP[sop], A[0], Bv[0])) if (A[1] or Bv[1]) else None)
            elif sop == 1: se = '(%s + PS[%s])' % (A[0], ps) if (A[1] or ps) else None
            elif sop == 3: se = '(%s * %s)' % (A[0], ps if ps else 'ps') if (A[1] or ps) else None
            elif sop == 25: se = '(%s - %s)' % (A[0], Bv[0]) if (A[1] or Bv[1]) else None
            else: se = ('%s(%s)' % (X.SOP[sop], A[0])) if A[1] else None
        if se is not None and scl: se = 'sat(%s)' % se
        if se is not None and len(se) > maxlen: se = se[:maxlen] + '...'
        PS[0] = se
        if smask:
            for i in range(4):
                if smask >> i & 1:
                    newR[(sdst, i, 's')] = se
                    if se is not None:
                        out.append('%3d %s%s.%s = %s   [scalar %s]' % (a, 'oC' if exp else 'r', sdst, C[i], se, X.SOP[sop]))
        for (r, i, _), e in newR.items():
            if not exp: R[(r, i)] = e
    return tgt, sc, ss, lit, out

if __name__ == '__main__':
    d = open(sys.argv[1], 'rb').read(); H = int(sys.argv[2], 0)
    tgt, sc, ss, lit, out = run(d, H)
    print(tgt, 'DSLS=c%s' % sc, 'ShadowMask=tf%s' % ss, 'literals', {k: tuple(round(x, 5) for x in v) for k, v in lit.items()})
    print('\n'.join(out))
