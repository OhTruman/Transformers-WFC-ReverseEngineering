"""Read-only AS2 (SWF action bytecode) disassembler with light expression folding, for WFC Scaleform .gfx.
usage: as2dis.py movie.gfx [filter-substring]
Prints every DoAction / DoInitAction / PlaceObject2-3 clip-event block (top level and inside DefineSprite),
as folded pseudo-statements:  obj.method(args)  /  a.b = v  /  if !(cond) goto L  /  function f(p) { ... }.
Folding is a straight symbolic stack walk (no CFG); branch targets are printed as byte offsets.
"""
import sys, struct
sys.path.insert(0, __import__('os').path.dirname(__file__))
import gfxpool

NOARG = {0x04: 'nextFrame', 0x05: 'prevFrame', 0x06: 'play', 0x07: 'stop', 0x08: 'toggleQuality', 0x09: 'stopSounds',
         0x0A: '+', 0x0B: '-', 0x0C: '*', 0x0D: '/', 0x0E: '==', 0x0F: '<', 0x10: '&&', 0x11: '||', 0x12: '!',
         0x13: 'eq', 0x14: 'length', 0x15: 'substring', 0x17: 'pop', 0x18: 'int', 0x1C: 'getVariable', 0x1D: 'setVariable',
         0x20: 'setTarget2', 0x21: 'concat', 0x22: 'getProperty', 0x23: 'setProperty', 0x24: 'cloneSprite', 0x25: 'removeSprite',
         0x26: 'trace', 0x27: 'startDrag', 0x28: 'endDrag', 0x29: 'lt', 0x2A: 'throw', 0x2B: 'cast', 0x2C: 'implements',
         0x30: 'random', 0x34: 'getTimer', 0x3A: 'delete', 0x3B: 'delete2', 0x3C: 'defineLocal', 0x3D: 'callFunction',
         0x3E: 'return', 0x3F: '%', 0x40: 'new', 0x41: 'defineLocal2', 0x42: 'initArray', 0x43: 'initObject', 0x44: 'typeof',
         0x45: 'targetPath', 0x46: 'enumerate', 0x47: '+', 0x48: '<', 0x49: '==', 0x4A: 'Number', 0x4B: 'String',
         0x4C: 'dup', 0x4D: 'swap', 0x4E: 'getMember', 0x4F: 'setMember', 0x50: '++', 0x51: '--', 0x52: 'callMethod',
         0x53: 'newMethod', 0x54: 'instanceof', 0x55: 'enumerate2', 0x60: '&', 0x61: '|', 0x62: '^', 0x63: '<<', 0x64: '>>',
         0x65: '>>>', 0x66: '===', 0x67: '>', 0x68: 'gt', 0x69: 'extends'}
BIN = {'+', '-', '*', '/', '==', '<', '&&', '||', 'eq', 'concat', 'lt', '%', '&', '|', '^', '<<', '>>', '>>>', '===', '>', 'gt', 'instanceof'}

def cstr(b, o):
    e = b.index(b'\0', o); return b[o:e].decode('latin1'), e + 1

def q(v):
    return repr(v) if isinstance(v, str) and not v.startswith('\x00') else str(v).lstrip('\x00')

class Expr(str):
    pass

def dis(code, pool=None, indent='', out=None, regs=None):
    """Disassemble one action buffer; returns lines."""
    pool = list(pool or []); out = out if out is not None else []
    st = []; regs = dict(regs or {})
    def pop():
        return st.pop() if st else Expr('?')
    def emit(s, off):
        out.append('%s%04x: %s' % (indent, off, s))
    i = 0; ends = []
    while i < len(code):
        while ends and i >= ends[-1]:
            ends.pop(); out.append(indent[:-2 * (len(ends) + 1)] + '  ' * len(ends) + '}') if False else out.append('%s}' % ('  ' * (len(ends)) + indent))
        off = i; op = code[i]; i += 1
        if op == 0: break
        if op < 0x80:
            n = NOARG.get(op, 'op%02x' % op)
            if n in BIN:
                b_ = pop(); a_ = pop(); st.append(Expr('(%s %s %s)' % (a_, n, b_)))
            elif n == '!': st.append(Expr('!' + pop()))
            elif n in ('++', '--'): st.append(Expr('(%s %s 1)' % (pop(), n[0])))
            elif n == 'getVariable': st.append(Expr(str(pop()).strip("'")))
            elif n == 'setVariable': v = pop(); k = pop(); emit('%s = %s' % (str(k).strip("'"), v), off)
            elif n in ('defineLocal',): v = pop(); k = pop(); emit('var %s = %s' % (str(k).strip("'"), v), off)
            elif n == 'defineLocal2': emit('var %s' % str(pop()).strip("'"), off)
            elif n == 'getMember': k = pop(); o = pop(); st.append(Expr('%s.%s' % (o, str(k).strip("'")) if isinstance(k, str) and k.startswith("'") else '%s[%s]' % (o, k)))
            elif n == 'setMember': v = pop(); k = pop(); o = pop(); emit('%s.%s = %s' % (o, str(k).strip("'"), v), off)
            elif n == 'callMethod':
                m = pop(); o = pop(); na = pop()
                try: na = int(float(str(na)))
                except Exception: na = 0
                args = [pop() for _ in range(na)]
                ms = str(m).strip("'")
                st.append(Expr('%s(%s)' % ('%s.%s' % (o, ms) if ms not in ('', 'undefined') else o, ', '.join(args))))
            elif n == 'callFunction':
                f = pop(); na = pop()
                try: na = int(float(str(na)))
                except Exception: na = 0
                args = [pop() for _ in range(na)]
                st.append(Expr('%s(%s)' % (str(f).strip("'"), ', '.join(args))))
            elif n in ('new', 'newMethod'):
                if n == 'newMethod': m = pop(); o = pop(); f = '%s.%s' % (o, str(m).strip("'"))
                else: f = str(pop()).strip("'")
                na = pop()
                try: na = int(float(str(na)))
                except Exception: na = 0
                args = [pop() for _ in range(na)]
                st.append(Expr('new %s(%s)' % (f, ', '.join(args))))
            elif n == 'initArray':
                na = pop()
                try: na = int(float(str(na)))
                except Exception: na = 0
                st.append(Expr('[%s]' % ', '.join(pop() for _ in range(na))))
            elif n == 'initObject':
                na = pop()
                try: na = int(float(str(na)))
                except Exception: na = 0
                kv = []
                for _ in range(na): v = pop(); k = pop(); kv.append('%s: %s' % (str(k).strip("'"), v))
                st.append(Expr('{%s}' % ', '.join(kv)))
            elif n == 'pop':
                v = pop()
                if '(' in v: emit(v, off)
            elif n == 'dup':
                v = pop(); st += [v, v]
            elif n == 'swap':
                a_ = pop(); b_ = pop(); st += [a_, b_]
            elif n == 'return': emit('return %s' % pop(), off)
            elif n in ('typeof', 'Number', 'String', 'int', 'length', 'targetPath'): st.append(Expr('%s(%s)' % (n, pop())))
            elif n == 'delete': k = pop(); o = pop(); emit('delete %s.%s' % (o, k), off)
            elif n == 'delete2': emit('delete %s' % pop(), off)
            elif n == 'extends': s_ = pop(); c_ = pop(); emit('%s extends %s' % (c_, s_), off)
            elif n == 'trace': emit('trace(%s)' % pop(), off)
            elif n in ('enumerate', 'enumerate2'): emit('for-in %s' % pop(), off); st.append(Expr('null'))
            elif n == 'getProperty': p_ = pop(); t_ = pop(); st.append(Expr('getProperty(%s,%s)' % (t_, p_)))
            elif n == 'setProperty': v = pop(); p_ = pop(); t_ = pop(); emit('setProperty(%s,%s,%s)' % (t_, p_, v), off)
            elif n == 'cast': o = pop(); c_ = pop(); st.append(Expr('%s(%s)' % (c_, o)))
            elif n == 'implements':
                c_ = pop(); na = pop()
                try: na = int(float(str(na)))
                except Exception: na = 0
                ifs = [pop() for _ in range(na)]; emit('%s implements %s' % (c_, ', '.join(ifs)), off)
            elif n in ('play', 'stop', 'nextFrame', 'prevFrame', 'stopSounds'): emit(n + '()', off)
            elif n == 'random': st.append(Expr('random(%s)' % pop()))
            elif n == 'getTimer': st.append(Expr('getTimer()'))
            elif n == 'throw': emit('throw %s' % pop(), off)
            elif n == 'removeSprite': emit('removeMovieClip(%s)' % pop(), off)
            else: emit(n, off)
            continue
        ln = struct.unpack_from('<H', code, i)[0]; i += 2; body = code[i:i + ln]; i += ln
        if op == 0x88:
            n = struct.unpack_from('<H', body, 0)[0]; pool = [x.decode('latin1') for x in body[2:].split(b'\0')[:n]]
        elif op == 0x96:
            j = 0
            while j < len(body):
                t = body[j]; j += 1
                if t == 0: s, j = cstr(body, j); st.append(Expr(repr(s)))
                elif t == 1: st.append(Expr('%g' % struct.unpack_from('<f', body, j)[0])); j += 4
                elif t == 2: st.append(Expr('null'))
                elif t == 3: st.append(Expr('undefined'))
                elif t == 4: r = body[j]; j += 1; st.append(Expr(regs.get(r, 'r%d' % r)))
                elif t == 5: st.append(Expr('true' if body[j] else 'false')); j += 1
                elif t == 6:
                    hi, lo = struct.unpack_from('<II', body, j); j += 8
                    st.append(Expr('%g' % struct.unpack('<d', struct.pack('<II', lo, hi))[0]))
                elif t == 7: st.append(Expr(str(struct.unpack_from('<i', body, j)[0]))); j += 4
                elif t == 8: k = body[j]; j += 1; st.append(Expr(repr(pool[k]) if k < len(pool) else 'c%d' % k))
                elif t == 9: k = struct.unpack_from('<H', body, j)[0]; j += 2; st.append(Expr(repr(pool[k]) if k < len(pool) else 'c%d' % k))
                else: break
        elif op == 0x87:
            r = body[0]; v = st[-1] if st else Expr('?'); emit('%s = %s' % (regs.get(r, 'r%d' % r), v), off)
        elif op == 0x99:
            emit('goto %04x' % (i + struct.unpack_from('<h', body, 0)[0]), off)
        elif op == 0x9D:
            emit('if %s goto %04x' % (pop(), i + struct.unpack_from('<h', body, 0)[0]), off)
        elif op in (0x8E, 0x9B):
            name, j = cstr(body, 0); np_ = struct.unpack_from('<H', body, j)[0]; j += 2; params = []
            fregs = {}
            if op == 0x8E:
                j += 1; flags = struct.unpack_from('<H', body, j)[0]; j += 2
                k = 1
                for bit, nm in ((0x0001, 'this'), (0x0004, 'arguments'), (0x0010, 'super'), (0x0040, '_root'), (0x0080, '_parent'), (0x0100, '_global')):
                    if flags & bit: fregs[k] = nm; k += 1
                for _ in range(np_):
                    r = body[j]; j += 1; p, j = cstr(body, j); params.append(p)
                    if r: fregs[r] = p
            else:
                for _ in range(np_): p, j = cstr(body, j); params.append(p)
            size = struct.unpack_from('<H', body, j)[0]
            fcode = code[i:i + size]; i += size
            hdr = 'function %s(%s) {' % (name, ', '.join(params))
            if name: emit(hdr, off)
            else: st.append(Expr('function(%s)' % ', '.join(params))); emit('<anon> ' + hdr, off)
            dis(fcode, pool, indent + '    ', out, fregs)
            out.append(indent + '    }')
        elif op == 0x94:
            emit('with (%s) {' % pop(), off)
        elif op == 0x8B: emit('setTarget(%r)' % cstr(body, 0)[0], off)
        elif op == 0x8C: emit('gotoLabel(%r)' % cstr(body, 0)[0], off)
        elif op == 0x81: emit('gotoFrame(%d)' % struct.unpack_from('<H', body, 0)[0], off)
        elif op == 0x9F: emit('gotoAndPlay/Stop(%s) flags=%d' % (pop(), body[0]), off)
        elif op == 0x83:
            a, j = cstr(body, 0); b, _ = cstr(body, j); emit('getURL(%r, %r)' % (a, b), off)
        elif op == 0x9A: t = pop(); u = pop(); emit('getURL2(%s, %s) m=%d' % (u, t, body[0]), off)
        elif op == 0x8F: emit('try {...} (flags %d)' % body[0], off)
        else: emit('op%02x len %d' % (op, ln), off)
    return out

def blocks(path):
    b = gfxpool.load(path); off = 8 + gfxpool.rect_len(b, 8) + 4
    def walk(o0, end, sid):
        for code, o, ln in gfxpool.tags(b, o0, end):
            if code == 12: yield ('DoAction', sid, b[o:o + ln])
            elif code == 59: yield ('DoInitAction', struct.unpack_from('<H', b, o)[0], b[o + 2:o + ln])
            elif code == 39: yield from walk(o + 4, o + ln, struct.unpack_from('<H', b, o)[0])
    yield from walk(off, len(b), None)

if __name__ == '__main__':
    flt = sys.argv[2] if len(sys.argv) > 2 else None
    for kind, sid, code in blocks(sys.argv[1]):
        lines = dis(code)
        text = '\n'.join(lines)
        if flt and flt not in text: continue
        print('==== %s sprite=%s (%d bytes)' % (kind, sid, len(code)))
        print(text)
