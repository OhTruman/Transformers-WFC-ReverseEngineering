"""Read-only: decode the native tail of HmInterpolatedLightMappedSkeletalMeshComponent (TnTransformingWorldActor meshes) in a
cooked map package. Layout (big-endian; verified on all 895 placed instances: 697 built + 198 unbuilt, every tail consumed exactly):
  GUID16 (= the LightingGuid property), u8 (1 on all), u32 N (0 = unbuilt: the tail ends here, 21 bytes),
  when N != 0: u32, u32, u32 (0, 0, 3 on all built), u32 n + n x GUID16 (union of the captures' baked lights, LightGuid),
  u32 (0), u32 C (captures; 2 on all built), C x capture, u32 m + m x GUID16 (static lights that do not affect it, LightGuid).
  capture = u32 type (2 = texture light map), u32 g + g x GUID16 (lights baked into this capture), u32 (0),
            3 x (u32 export index of a LightMapTexture2D, float4 scale vector), float2 CoordinateScale, float2 CoordinateBias.
Usage: python interp_lightmap.py <map package> [<out.json>]"""
import os, sys, json, struct
sys.dont_write_bytecode = True
sys.path.insert(0, r"F:\Transformers Rebuild\AssetTools\scripts\wfc")
import ue3pkg

DUMP = r"F:\Transformers Rebuild\Game Dump\TransGame\CookedXenon"
CLS = "HmInterpolatedLightMappedSkeletalMeshComponent"


def guid(b, k):
    return "%08x%08x%08x%08x" % struct.unpack_from(">4I", b, k)


def decode(p, nat):
    u = lambda k: struct.unpack_from(">I", nat, k)[0]
    f = lambda k: struct.unpack_from(">f", nat, k)[0]
    lst = lambda k: (k + 4 + 16 * u(k), [guid(nat, k + 4 + 16 * i) for i in range(u(k))])
    out = {"lighting_guid": guid(nat, 0), "flag": nat[16], "captures": []}
    if u(17) == 0:
        return out, 21
    k, out["baked_lights"] = lst(33)
    k += 4; ncap = u(k); k += 4
    for _ in range(ncap):
        cap = {"type": u(k)}; k, cap["lights"] = lst(k + 4); k += 4
        cap["textures"] = []
        for _ in range(3):
            cap["textures"].append({"texture": p.object_path(u(k)), "scale": [f(k + 4 + 4 * j) for j in range(4)]}); k += 20
        cap["coordinate_scale"] = [f(k), f(k + 4)]; cap["coordinate_bias"] = [f(k + 8), f(k + 12)]; k += 16
        out["captures"].append(cap)
    k, out["irrelevant_lights"] = lst(k)
    return out, k


if __name__ == "__main__":
    p = ue3pkg.Package(os.path.join(DUMP, sys.argv[1] + ".xxx")); d = p.data
    res = {}
    for i, e in enumerate(p.exports, 1):
        if p.class_name(e) != CLS: continue
        b = d[e["serial_offset"]:e["serial_offset"] + e["serial_size"]]
        # the tail starts at a copy of LightingGuid: take the offset (scanning back from the end) whose decode consumes it exactly
        lg = None
        for k in range(len(b) - 21, -1, -1):
            if k + 21 <= len(b) and b[k + 16] == 1:
                try:
                    r, end = decode(p, b[k:])
                except Exception:
                    continue
                if k + end == len(b) and (r["captures"] or end == 21): lg = r; break
        res[p.object_path(i)] = lg
    s = json.dumps(res, indent=1)
    open(sys.argv[2], "w").write(s) if len(sys.argv) > 2 else print(s)
