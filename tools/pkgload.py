"""Read-only loader for cooked script packages (reuses AssetTools' ue3pkg parser, in place).
Caches decompressed package bytes under work/script/<pkg>.bin for speed."""
import os, sys, pickle
sys.path.insert(0, r"F:\Transformers Rebuild\AssetTools\scripts\wfc")
import ue3pkg
from xeximg import ROOT
DUMP = r"F:\Transformers Rebuild\Game Dump\TransGame\CookedXenon"
CACHE = os.path.join(ROOT, "work", "script")

def load(name):
    os.makedirs(CACHE, exist_ok=True)
    c = os.path.join(CACHE, name + ".pkl")
    if os.path.exists(c):
        with open(c, "rb") as f: return pickle.load(f)
    p = ue3pkg.Package(os.path.join(DUMP, name + ".xxx"))
    with open(c, "wb") as f: pickle.dump(p, f)
    return p

def find(p, path):
    for i, e in enumerate(p.exports, 1):
        if p.full_path(i) == path: return i, e
    return None, None
