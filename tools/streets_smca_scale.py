"""Emit the per-component scale that UE3 applies on top of StaticMeshCollectionActor CachedParentToWorld.

Native rule (UPrimitiveComponent::SetTransformedToWorld 0x82DC3508):
    LocalToWorld = FScaleRotationTranslationMatrix(Scale*Scale3D, Rotation, Translation) * ParentToWorld
For SMCA members ParentToWorld = the serialized CachedParentToWorld (pure rotation+translation in Streets),
and the component carries Scale/Scale3D (Translation/Rotation are default for every Streets SMCA member).

Read-only: uses AssetTools' readers in place and the cooked packages; writes one JSON under RE-Workspace.
Usage: python streets_smca_scale.py [out.json]
Output: {component_object_path: {"scale": [sx,sy,sz], "translation": [...], "rotation": [...]}}
Corrected UE row-vector matrix = diag(sx,sy,sz) @ R(rotation) @ T(translation) @ props.json ue_matrix.
"""
import json, os, sys
sys.path.insert(0, r"F:\Transformers Rebuild\AssetTools\scripts\wfc")
sys.argv = [sys.argv[0], 'MP_IAC_Streets'] + sys.argv[1:]
import vs_map  # noqa: E402
from vs_map import Level, ref  # noqa: E402

out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                              'notes', 'data', 'streets_smca_component_scale.json')
res = {}
for name in vs_map.sublevels():
    L = Level(name)
    for a in L.actors():
        if L.cls[a - 1] != 'StaticMeshCollectionActor':
            continue
        d = L.P(a)
        for cr in [ref(x) for x in (d.get('StaticMeshComponents') or [])]:
            ci = L.idx(cr)
            cd = L.P(ci) if ci else {}
            s = cd.get('Scale', 1.0)
            s3 = cd.get('Scale3D', [1, 1, 1])
            res[cr] = {'scale': [round(s * v, 6) for v in s3],
                       'translation': cd.get('Translation', [0, 0, 0]),
                       'rotation': cd.get('Rotation', [0, 0, 0])}
os.makedirs(os.path.dirname(out_path), exist_ok=True)
json.dump(res, open(out_path, 'w'), indent=0, sort_keys=True)
print(len(res), 'components ->', out_path)
