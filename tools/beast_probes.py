"""Read-only: decode WFC Beast light-probe grids (BeastLightEnvironmentBox native data) from cooked map packages.

Format (CONFIRMED, default.xex 0x82FC6DB8 lookup / 0x82CCB228 volume pick / 0x82CBE520 SH->ambient cube):
  BeastLightEnvironmentBox native tail after tagged props: int32 BE count, then count x FSHVectorRGB
  FSHVectorRGB = 27 BE float32 = R[9], G[9], B[9] (planar), stock UE3 L2 SH basis order (index = L*(L+1)+M).
  count = PointsX*PointsY*PointsZ; point index = (z*PointsY + y)*PointsX + x.
Usage: python beast_probes.py <package> [--dump out.json]   (package e.g. MP_ORB_Art_m_LM)
"""
import sys, struct, json, math
sys.path.insert(0, r"F:\Transformers Rebuild\AssetTools\scripts\wfc")
import objtree

# stock UE3 real SH basis, Condon-Shortley phase, M<0 -> sin, M>0 -> cos (0x82B20168)
def basis(d):
    x, y, z = d
    return [0.282095, -0.488603 * y, 0.488603 * z, -0.488603 * x,
            1.092548 * x * y, -1.092548 * y * z, 0.315392 * (3 * z * z - 1), -1.092548 * x * z, 0.546274 * (x * x - y * y)]

FACES = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

def ambient_cube(sh):
    """0x82CBE520: face_rgb = dot(SH_rgb, B(dir)) / |B(dir)|^2 for +X,-X,+Y,-Y,+Z,-Z."""
    out = []
    for f in FACES:
        b = basis(f); n = sum(v * v for v in b)
        out.append([sum(sh[c * 9 + i] * b[i] for i in range(9)) / n for c in range(3)])
    return out

def read(pkg):
    p = objtree.package(pkg)
    boxes = {}
    for i, e in enumerate(p.exports, 1):
        if p.class_name(e) != 'BeastLightEnvironmentBox':
            continue
        props, used = p._tr.read_object(i)
        pr = {x['name']: x.get('value') for x in props}
        nat = p.data[e['serial_offset'] + used:e['serial_offset'] + e['serial_size']]
        n = struct.unpack_from('>i', nat, 0)[0]
        assert n == pr['PointsX'] * pr['PointsY'] * pr['PointsZ'] and len(nat) == 4 + n * 108, (n, len(nat))
        pts = [struct.unpack_from('>27f', nat, 4 + k * 108) for k in range(n)]
        boxes[p.object_path(i)] = {'PointsX': pr['PointsX'], 'PointsY': pr['PointsY'], 'PointsZ': pr['PointsZ'],
                                   'Distance': pr.get('Distance'), 'm_worldToLocal': pr.get('m_worldToLocal'),
                                   'BoxSampleGenerator': pr.get('BoxSampleGenerator'), 'points': pts}
    return boxes

if __name__ == '__main__':
    boxes = read(sys.argv[1])
    for k, b in boxes.items():
        dc = [p[0] * 0.282095 for p in b['points']]
        print(k, b['PointsX'], b['PointsY'], b['PointsZ'], 'R DC radiance min/mean/max %.4f %.4f %.4f' % (min(dc), sum(dc) / len(dc), max(dc)))
        mid = b['points'][len(b['points']) // 2]
        print('  mid point ambient cube', [[round(v, 4) for v in f] for f in ambient_cube(mid)])
    if '--dump' in sys.argv:
        json.dump(boxes, open(sys.argv[sys.argv.index('--dump') + 1], 'w'))
