"""CF-aware numeric emulator for WFC Xenos vertex-shader blobs (read-only analysis aid).
Caller supplies constants {reg: (x,y,z,w)} and vertex fetch values in vfetch order (list of 4-tuples).
NEGBOTH: src3 negate applies to both operands of *_CONST_* scalar ops (verified by symmetry on the beam VS).
Follows EXEC / COND_JMP (predicated + unconditional) and per-op predicate setting."""
import math, struct, sys, os
sys.path.insert(0, r'F:\Transformers Rebuild\RE-Workspace\tools')
import xenosdis as X
B = X.bits
NEGBOTH = True


def run(d, consts, fetches, trace=False, mstart=0x28):
    M, cfs = X.find_microcode(d, mstart, len(d))
    # literal constants just before microcode (same rule as xenosemu)
    C = {254: struct.unpack_from('>4f', d, M - 32), 255: struct.unpack_from('>4f', d, M - 16)}
    C.update(consts)
    R = {}
    P = [False]
    PS = [0.0]
    out = {}
    fetch_i = [0]

    def rd(reg, sel, neg, comp, absc):
        if sel:
            v = R.get((reg & 0x3F, comp), 0.0)
            if reg & 0x80: v = abs(v)
        else:
            v = C.get(reg, (0.0,) * 4)[comp]
            if absc: v = abs(v)
        return -v if neg else v

    def exec_instr(a, isf, w0, w1, w2):
        if isf:
            if B(w0, 0, 5) == 0:
                dr = B(w0, 12, 6); dsw = B(w1, 0, 12)
                vals = fetches[fetch_i[0]]; fetch_i[0] += 1
                for i in range(4):
                    s = B(dsw, 3 * i, 3)
                    if s < 4: R[(dr, i)] = vals[s]
                    elif s == 4: R[(dr, i)] = 0.0
                    elif s == 5: R[(dr, i)] = 1.0
            return
        if B(w1, 28, 1) and (B(w1, 27, 1) != P[0]):
            return
        vdst = B(w0, 0, 6); absc = B(w0, 7, 1); sdst = B(w0, 8, 6); exp = B(w0, 15, 1)
        vmask = B(w0, 16, 4); smask = B(w0, 20, 4); vcl = B(w0, 24, 1); scl = B(w0, 25, 1); sop = B(w0, 26, 6)
        sws = [B(w1, 16, 8), B(w1, 8, 8), B(w1, 0, 8)]; negs = [B(w1, 26, 1), B(w1, 25, 1), B(w1, 24, 1)]
        regs_ = [B(w2, 16, 8), B(w2, 8, 8), B(w2, 0, 8)]; sels = [B(w2, 31, 1), B(w2, 30, 1), B(w2, 29, 1)]
        vop = B(w2, 24, 5)
        sat = lambda x: min(max(x, 0.0), 1.0)

        def sv(si, cd):
            return rd(regs_[si], sels[si], negs[si], (B(sws[si], 2 * cd, 2) + cd) & 3, absc)
        newR = {}
        if vmask:
            for i in range(4):
                if not (vmask >> i & 1): continue
                if vop in (15, 16):
                    n = 4 if vop == 15 else 3
                    e = sum(sv(0, j) * sv(1, j) for j in range(n))
                else:
                    a0, b0, c0 = sv(0, i), sv(1, i), sv(2, i)
                    e = {0: lambda: a0 + b0, 1: lambda: a0 * b0, 2: lambda: max(a0, b0), 3: lambda: min(a0, b0),
                         4: lambda: 1.0 if a0 == b0 else 0.0, 5: lambda: 1.0 if a0 > b0 else 0.0,
                         6: lambda: 1.0 if a0 >= b0 else 0.0, 7: lambda: 1.0 if a0 != b0 else 0.0,
                         8: lambda: a0 - math.floor(a0), 10: lambda: math.floor(a0), 11: lambda: a0 * b0 + c0,
                         12: lambda: b0 if a0 == 0 else c0, 13: lambda: b0 if a0 >= 0 else c0,
                         14: lambda: b0 if a0 > 0 else c0}[vop]()
                if vcl: e = sat(e)
                newR[(vdst, i)] = e
        a_c = (B(sws[2], 6, 2) + 3) & 3; b_c = B(sws[2], 0, 2) & 3
        se = None
        if sop in (42, 43, 44, 45, 46, 47):
            tr = (sws[2] & 0x3C) | (sels[2] << 1) | (sop & 1)
            ca = rd(regs_[2], 0, negs[2], a_c, absc); tb = rd(tr, 1, negs[2] if NEGBOTH else 0, b_c, 0)
            se = {42: ca * tb, 43: ca * tb, 44: ca + tb, 45: ca + tb, 46: ca - tb, 47: ca - tb}[sop]
        elif sop != 50:
            A = rd(regs_[2], sels[2], negs[2], a_c, absc); Bv = rd(regs_[2], sels[2], negs[2], b_c, absc)
            ps = PS[0]
            if sop == 27:   # PRED_SETEs
                P[0] = (A == 0.0); se = 0.0 if P[0] else 1.0
            elif sop == 28:  # PRED_SETNEs
                P[0] = (A != 0.0); se = 0.0 if P[0] else 1.0
            elif sop == 29:  # PRED_SETGTs
                P[0] = (A > 0.0); se = 0.0 if P[0] else 1.0
            elif sop == 30:  # PRED_SETGTEs
                P[0] = (A >= 0.0); se = 0.0 if P[0] else 1.0
            else:
                se = {0: lambda: A + Bv, 1: lambda: A + ps, 2: lambda: A * Bv, 3: lambda: A * ps,
                      5: lambda: max(A, Bv), 6: lambda: min(A, Bv), 7: lambda: 1.0 if A == 0 else 0.0,
                      8: lambda: 1.0 if A > 0 else 0.0, 9: lambda: 1.0 if A >= 0 else 0.0,
                      10: lambda: 1.0 if A != 0 else 0.0, 17: lambda: 1.0 / A if A else 0.0,
                      18: lambda: 1.0 / A if A else 0.0, 19: lambda: 1.0 / A if A else float('inf'),
                      20: lambda: 1.0 / math.sqrt(A) if A > 0 else 0.0, 21: lambda: 1.0 / math.sqrt(A) if A > 0 else 0.0,
                      22: lambda: 1.0 / math.sqrt(A) if A > 0 else float('inf'),
                      11: lambda: A - math.floor(A), 12: lambda: float(math.trunc(A)), 13: lambda: math.floor(A),
                      48: lambda: math.sin(A), 49: lambda: math.cos(A),
                      25: lambda: A - Bv, 26: lambda: A - ps, 40: lambda: math.sqrt(A)}.get(sop, lambda: float("nan"))()
        else:
            se = PS[0]
        if scl and se is not None: se = sat(se)
        if se is not None: PS[0] = se
        if smask:
            for i in range(4):
                if smask >> i & 1: newR[(sdst, i)] = se
        for k2, v in newR.items():
            if exp: out[(k2[0], k2[1])] = v
            else: R[k2] = v
        if trace:
            print(a, X.alu(w0, w1, w2), {k: round(v, 4) for k, v in newR.items()}, 'P', P[0])

    pc = 0
    steps = 0
    while pc < len(cfs) and steps < 1000:
        steps += 1
        c = cfs[pc]
        op = B(c, 44, 4)
        if op in (1, 2):
            addr, cnt, seq = B(c, 0, 12), B(c, 12, 3), B(c, 16, 12)
            for i in range(cnt):
                w = struct.unpack_from('>3I', d, M + 12 * (addr + i))
                exec_instr(addr + i, B(seq, 2 * i, 1), *w)
            if op == 2: break
            pc += 1
        elif op == 11:  # COND_JMP
            tgt = B(c, 0, 13); uncond = B(c, 13, 1); pred = B(c, 14, 1); cond = B(c, 42, 1)
            if uncond or (pred and (P[0] == bool(cond))):
                pc = tgt
            else:
                pc += 1
        else:
            pc += 1
    return out, R


