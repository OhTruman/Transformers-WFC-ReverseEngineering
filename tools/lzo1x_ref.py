"""Read-only reference LZO1X decompressor (pure python, the lzo1x_decompress_safe state machine) for checking a block
that a native decoder handles differently. decompress(buf, trace=None) -> (bytes, input bytes consumed); trace collects (input pos, output len) per op."""


def decompress(src, trace=None):
    out = bytearray()
    ip, n = 0, len(src)

    def length(base, ip):
        t = 0
        while src[ip] == 0:
            t += 255; ip += 1
        return base + t + src[ip], ip + 1

    t = src[ip]
    state = 0
    if t > 17:
        t -= 17; ip += 1
        out += src[ip:ip + t]; ip += t
        state = 4 if t >= 4 else t
    while True:
        if trace is not None: trace.append((ip, len(out)))
        t = src[ip]; ip += 1
        if t < 16:
            if state == 0:                      # literal run
                if t == 0: t, ip = length(15, ip)
                t += 3
                out += src[ip:ip + t]; ip += t
                state = 4
                continue
            if state == 4:                      # M1 after a literal run of >= 4: 3-byte match, distance 2049..3072
                d = 1 + 0x0800 + (t >> 2) + (src[ip] << 2); ip += 1; ln = 3
            else:                               # M1 after a short literal: 2-byte match, distance 1..1024
                d = 1 + (t >> 2) + (src[ip] << 2); ip += 1; ln = 2
            s = t & 3
        elif t >= 64:                           # M2
            d = 1 + ((t >> 2) & 7) + (src[ip] << 3); ip += 1
            ln = (t >> 5) + 1; s = t & 3
        elif t >= 32:                           # M3
            ln = t & 31
            if ln == 0: ln, ip = length(31, ip)
            ln += 2
            v = src[ip] | (src[ip + 1] << 8); ip += 2
            d = 1 + (v >> 2); s = v & 3
        else:                                   # M4 (16..31), or end of stream
            ln = t & 7
            if ln == 0: ln, ip = length(7, ip)
            ln += 2
            v = src[ip] | (src[ip + 1] << 8); ip += 2
            d = ((t & 8) << 11) + (v >> 2)
            s = v & 3
            if d == 0: return bytes(out), ip
            d += 0x4000
        st = len(out) - d
        for k in range(ln): out.append(out[st + k])
        if s:
            out += src[ip:ip + s]; ip += s
        state = s
