"""Minimal read-only GLB loader + numpy ray caster (analysis aid; no external deps).
load(path, skip=lambda node_name: False) -> (tris Nx3x3 world, owner names list per tri)
cast(tris, origins Mx3, dirs Mx3, tmax) -> (t, tri_index) nearest hit per ray (inf / -1 if none)
"""
import json, struct
import numpy as np

CT = {5120: 'i1', 5121: 'u1', 5122: '>i2', 5123: 'u2', 5125: 'u4', 5126: 'f4'}
NC = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}

def _acc(g, binb, i):
    a = g['accessors'][i]; bv = g['bufferViews'][a['bufferView']]
    dt = np.dtype(CT[a['componentType']]).newbyteorder('<')
    n = NC[a['type']]; off = bv.get('byteOffset', 0) + a.get('byteOffset', 0)
    stride = bv.get('byteStride', 0)
    if stride and stride != n * dt.itemsize:
        raw = np.frombuffer(binb, 'u1', a['count'] * stride, off).reshape(a['count'], stride)[:, :n * dt.itemsize]
        return np.frombuffer(raw.tobytes(), dt).reshape(a['count'], n)
    return np.frombuffer(binb, dt, a['count'] * n, off).reshape(a['count'], n) if n > 1 else np.frombuffer(binb, dt, a['count'], off)

def load(path, skip=lambda name: False):
    d = open(path, 'rb').read()
    jl = struct.unpack_from('<I', d, 12)[0]
    g = json.loads(d[20:20 + jl]); bo = 20 + jl
    binb = d[bo + 8:bo + 8 + struct.unpack_from('<I', d, bo)[0]]
    tris, owners = [], []
    for node in g['nodes']:
        if 'mesh' not in node or skip(node.get('name', '')): continue
        M = np.array(node.get('matrix', [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]), 'f8').reshape(4, 4).T
        for pr in g['meshes'][node['mesh']]['primitives']:
            P = _acc(g, binb, pr['attributes']['POSITION']).astype('f8')
            I = _acc(g, binb, pr['indices']).astype('i8').reshape(-1, 3) if 'indices' in pr else np.arange(len(P)).reshape(-1, 3)
            W = P @ M[:3, :3].T + M[:3, 3]
            tris.append(W[I]); owners += [node.get('name', '')] * len(I)
    return np.concatenate(tris), owners

def cast(tris, O, D, tmax=np.inf, chunk=200000):
    best_t = np.full(len(O), np.inf); best_i = np.full(len(O), -1)
    for s in range(0, len(tris), chunk):
        T = tris[s:s + chunk]; v0 = T[:, 0]; e1 = T[:, 1] - v0; e2 = T[:, 2] - v0
        for k in range(len(O)):
            p = np.cross(D[k], e2); det = np.einsum('ij,ij->i', e1, p)
            ok = np.abs(det) > 1e-12; inv = np.where(ok, 1.0 / np.where(ok, det, 1), 0)
            tv = O[k] - v0; u = np.einsum('ij,ij->i', tv, p) * inv
            q = np.cross(tv, e1); v = (q @ D[k]) * inv; t = np.einsum('ij,ij->i', e2, q) * inv
            m = ok & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > 1e-4) & (t < tmax)
            if m.any():
                j = np.argmin(np.where(m, t, np.inf))
                if t[j] < best_t[k]: best_t[k] = t[j]; best_i[k] = s + j
    return best_t, best_i
