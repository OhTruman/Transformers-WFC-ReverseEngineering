"""Minimal Xenos (Xbox 360 GPU) shader microcode disassembler for WFC cooked shader blobs.

Blob layout (as observed in WFC ShaderCache exports, big-endian):
  +0x00 u32 magic 0x102A1100 (pixel) / 0x102A1101 (vertex)
  +0x24 u32 ctab_size, +0x28 D3DX constant table (no 'CTAB' fourcc; offsets relative to +0x28)
  ... literal-constant block ...
  microcode: control-flow pairs (3 dwords = 2 CF instrs) followed by ALU / fetch instructions (3 dwords each).
Microcode start is located by scanning for a CF list whose first EXEC address points just past the CF block.

Instruction bit layouts follow the public Xenia ucode.h definitions (LSB-first bitfields on host-order dwords).
Usage: python xenosdis.py <blob.bin> [blob_offset]
"""
import struct, sys

VOP = ['ADDv','MULv','MAXv','MINv','SETEv','SETGTv','SETGTEv','SETNEv','FRACv','TRUNCv','FLOORv','MULADDv',
       'CNDEv','CNDGTEv','CNDGTv','DOT4v','DOT3v','DOT2ADDv','CUBEv','MAX4v','PRED_SETE_PUSHv','PRED_SETNE_PUSHv',
       'PRED_SETGT_PUSHv','PRED_SETGTE_PUSHv','KILLEv','KILLGTv','KILLGTEv','KILLNEv','DSTv','MOVAv','?30','?31']
VNSRC = {0:2,1:2,2:2,3:2,4:2,5:2,6:2,7:2,8:1,9:1,10:1,11:3,12:3,13:3,14:3,15:2,16:2,17:3,18:2,19:1,20:2,21:2,
         22:2,23:2,24:2,25:2,26:2,27:2,28:2,29:1}
SOP = ['ADDs','ADD_PREVs','MULs','MUL_PREVs','MUL_PREV2s','MAXs','MINs','SETEs','SETGTs','SETGTEs','SETNEs',
       'FRACs','TRUNCs','FLOORs','EXP_IEEE','LOG_CLAMP','LOG_IEEE','RECIP_CLAMP','RECIP_FF','RECIP_IEEE',
       'RECIPSQ_CLAMP','RECIPSQ_FF','RECIPSQ_IEEE','MOVAs','MOVA_FLOORs','SUBs','SUB_PREVs','PRED_SETEs',
       'PRED_SETNEs','PRED_SETGTs','PRED_SETGTEs','PRED_SET_INVs','PRED_SET_POPs','PRED_SET_CLRs',
       'PRED_SET_RESTOREs','KILLEs','KILLGTs','KILLGTEs','KILLNEs','KILLONEs','SQRT_IEEE','?41',
       'MUL_CONST_0','MUL_CONST_1','ADD_CONST_0','ADD_CONST_1','SUB_CONST_0','SUB_CONST_1','SIN','COS',
       'RETAIN_PREV'] + ['?%d' % i for i in range(51, 64)]
SCALAR_2OP = {0,2,5,6,7,8,9,10,25}       # use a,b
SCALAR_PREV = {1,3,4,26}
SCALAR_NONE = {32,33,34,50}
CF_OP = ['NOP','EXEC','EXEC_END','COND_EXEC','COND_EXEC_END','COND_PRED_EXEC','COND_PRED_EXEC_END','LOOP_START',
         'LOOP_END','COND_CALL','RETURN','COND_JMP','ALLOC','COND_EXEC_PRED_CLEAN','COND_EXEC_PRED_CLEAN_END',
         'MARK_VS_FETCH_DONE']
C = 'xyzw'

VFMT = {6: '8_8_8_8', 7: '2_10_10_10', 25: '16_16', 26: '16_16_16_16', 31: '16_16_FLOAT', 32: '16_16_16_16_FLOAT',
        33: '32', 34: '32_32', 35: '32_32_32_32', 36: '32_FLOAT', 37: '32_32_FLOAT', 38: '32_32_32_32_FLOAT',
        57: '32_32_32_FLOAT'}

def bits(v, lo, n): return (v >> lo) & ((1 << n) - 1)

def vswz(s):
    r = ''.join(C[(bits(s, 2*i, 2) + i) & 3] for i in range(4))
    return '' if r == 'xyzw' else '.' + r

def sswz(s):
    a = (bits(s, 6, 2) + 3) & 3; b = (bits(s, 0, 2) + 0) & 3
    return C[a], C[b]

def mask(m): return ''.join(C[i] if m >> i & 1 else '_' for i in range(4))

def parse_ctab(d, base):
    size, creator, ver, n, info, flags, tgt = struct.unpack_from('>7I', d, base)
    def cstr(o):
        e = d.index(b'\0', base + o); return d[base + o:e].decode('latin1')
    out = []
    for i in range(n):
        nm, rs, ri, rc, _, ti, dv = struct.unpack_from('>IHHHHII', d, base + info + 20*i)
        out.append((cstr(nm), ['bool','int4','float4','sampler'][rs], ri, rc))
    return ver, cstr(tgt), out

def find_microcode(d, start, end):
    """Find M such that CF list at M decodes with first EXEC address A and an EXEC_END is reached
    before M + 12*A."""
    for M in range(start, end - 12, 4):
        cfs = []
        ok = False
        for g in range(0, 64):
            o = M + 12*g
            if o + 12 > end: break
            w0, w1, w2 = struct.unpack_from('>3I', d, o)
            c0 = w0 | ((w1 & 0xFFFF) << 32); c1 = (w1 >> 16) | (w2 << 16)
            cfs += [c0, c1]
            ex = [c for c in cfs if bits(c, 44, 4) in (1, 2, 3, 4, 5, 6)]
            if ex and any(bits(c, 44, 4) in (2, 4, 6, 14) for c in cfs):
                first = bits(ex[0], 0, 12)
                if first == g + 1 and all(bits(c, 44, 4) < 16 for c in cfs):
                    ok = True
                break
        if ok:
            return M, cfs
    return None, None

def src(reg, sel, neg, swz, absc, kind='v'):
    s = ('-' if neg else '')
    if sel:  # temp
        r = 'r%d' % (reg & 0x3F); a = reg & 0x80
        t = r + (vswz(swz) if kind == 'v' else '')
        return s + ('|%s|' % t if a else t)
    t = 'c%d' % reg + (vswz(swz) if kind == 'v' else '')
    return s + ('|%s|' % t if absc else t)

def alu(w0, w1, w2):
    vdst = bits(w0, 0, 6); absc = bits(w0, 7, 1); sdst = bits(w0, 8, 6); exp = bits(w0, 15, 1)
    vmask = bits(w0, 16, 4); smask = bits(w0, 20, 4); vcl = bits(w0, 24, 1); scl = bits(w0, 25, 1)
    sop = bits(w0, 26, 6)
    s3sw, s2sw, s1sw = bits(w1, 0, 8), bits(w1, 8, 8), bits(w1, 16, 8)
    n3, n2, n1 = bits(w1, 24, 1), bits(w1, 25, 1), bits(w1, 26, 1)
    pc, pr = bits(w1, 27, 1), bits(w1, 28, 1)
    r3, r2, r1 = bits(w2, 0, 8), bits(w2, 8, 8), bits(w2, 16, 8)
    vop = bits(w2, 24, 5); s3, s2, s1 = bits(w2, 29, 1), bits(w2, 30, 1), bits(w2, 31, 1)
    pred = ('(%sp0) ' % ('' if pc else '!')) if pr else ''
    out = []
    dname = (('oC%d' % vdst) if vdst < 4 else ('oDepth' if vdst == 61 else 'export%d' % vdst)) if exp else 'r%d' % vdst
    if vmask or vop in (20, 21, 22, 23, 24, 25, 26, 27):
        n = VNSRC.get(vop, 2)
        ss = [src(r1, s1, n1, s1sw, absc), src(r2, s2, n2, s2sw, absc), src(r3, s3, n3, s3sw, absc)][:n]
        out.append('%s%s%s %s.%s, %s' % (pred, VOP[vop], '_sat' if vcl else '', dname, mask(vmask), ', '.join(ss)))
    if smask or sop in (27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39):
        sd = (('oC%d' % sdst) if sdst < 4 else 'export%d' % sdst) if exp else 'r%d' % sdst
        if sop in (42, 43, 44, 45, 46, 47):
            # const variants: a = constant (src3 reg, component from swizzle x-slot), b = temp
            treg = (bits(s3sw, 0, 2) | (bits(sop, 0, 1) << 2) | (bits(s3sw, 2, 4) << 2)) & 0x3F
            ca, cb = sswz(s3sw)
            sa = ('-' if n3 else '') + 'c%d.%s' % (r3, ca)
            # Xenia: temp register index is ((src3_swiz & 0x3C) >> 2) | (scalar_opc & 1) << 4 ... approximate:
            tr = (s3sw & 0x3C) | (s3 << 1) | (sop & 1)
            sb = 'r%d.%s' % (tr, cb)
            ops = {42: '*', 43: '*', 44: '+', 45: '+', 46: '-', 47: '-'}[sop]
            out.append('%s%s%s %s.%s, %s %s %s' % (pred, SOP[sop], '_sat' if scl else '', sd, mask(smask), sa, ops, sb))
        else:
            a, b = sswz(s3sw)
            base = src(r3, s3, n3, 0, absc, kind='s')
            if sop in SCALAR_2OP:
                args = '%s.%s, %s.%s' % (base, a, base, b)
            elif sop in SCALAR_NONE:
                args = ''
            else:
                args = '%s.%s' % (base, a)
            out.append('%s%s%s %s.%s, %s' % (pred, SOP[sop], '_sat' if scl else '', sd, mask(smask), args))
    return out or ['nop']

def fetch(w0, w1, w2):
    op = bits(w0, 0, 5)
    if op == 0:
        # Xenia VertexFetchInstruction: w1 dst_swiz:12 fmt_comp_all:1 num_fmt_all:1 signed_rf:1 rsv:1 format:6
        # rsv:2 exp_adjust:6 is_mini:1 is_pred:1; w2 stride:8 offset:23 (dwords)
        dsel = ''.join('xyzw01?_'[bits(w1, 3*i, 3)] for i in range(4))
        fmt = VFMT.get(bits(w1, 16, 6), 'fmt%d' % bits(w1, 16, 6))
        signed = '' if bits(w1, 12, 1) else 's'  # format_comp_all 0 = signed
        norm = '' if bits(w1, 13, 1) else 'n'    # num_format_all 0 = normalized
        mini = ' mini' if bits(w1, 30, 1) else ''
        return 'vfetch r%d.%s, r%d, vf%d  %s%s%s off=%d stride=%d%s' % (
            bits(w0, 12, 6), dsel, bits(w0, 5, 6), bits(w0, 20, 5), fmt, signed and '_'+signed, norm and '_'+norm,
            bits(w2, 8, 23), bits(w2, 0, 8), mini)
    sr = bits(w0, 5, 6); dr = bits(w0, 12, 6); ci = bits(w0, 20, 5); ssw = bits(w0, 26, 6)
    dsw = bits(w1, 0, 12)
    sw = ''.join(C[bits(ssw, 2*i, 2)] for i in range(3))
    dsel = ''.join('xyzw01?_'[bits(dsw, 3*i, 3)] for i in range(4))
    name = {1: 'tfetch', 16: 'getTextureBorderColorFrac', 17: 'getTextureComputedLod', 18: 'getTextureGradients',
            19: 'getTextureWeights', 24: 'setTextureLod', 25: 'setTextureGradientsHorz', 26: 'setTextureGradientsVert'}.get(op, 'fetch%d' % op)
    return '%s r%d.%s, r%d.%s, tf%d' % (name, dr, dsel, sr, sw, ci)

def disasm(d, M, cfs):
    lines = []
    for c in cfs:
        op = bits(c, 44, 4)
        if op in (1, 2, 3, 4, 5, 6, 13, 14):
            addr, cnt, seq = bits(c, 0, 12), bits(c, 12, 3), bits(c, 16, 12)
            lines.append('; %s addr=%d count=%d' % (CF_OP[op], addr, cnt))
            for i in range(cnt):
                o = M + 12*(addr + i)
                w0, w1, w2 = struct.unpack_from('>3I', d, o)
                isf = bits(seq, 2*i, 1)
                if isf:
                    lines.append('%3d  %s' % (addr + i, fetch(w0, w1, w2)))
                else:
                    for t in alu(w0, w1, w2):
                        lines.append('%3d  %s' % (addr + i, t))
            if op in (2, 4, 6, 14):
                break
        elif op == 12:
            lines.append('; ALLOC')
    return lines

if __name__ == '__main__':
    d = open(sys.argv[1], 'rb').read()
    off = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0
    ctab_base = off + 0x28
    ver, tgt, consts = parse_ctab(d, ctab_base)
    print('target', tgt, hex(ver))
    for c in consts: print('  ', c)
    M, cfs = find_microcode(d, ctab_base, ctab_base + 0x4000)
    print('microcode at', hex(M) if M else None)
    if M:
        print('\n'.join(disasm(d, M, cfs)))
