"""Read-only: per player weapon, the data the multiplayer game actually uses (MultiplayerData, falling back to PlayerData like
TnWeapon.GivenTo), flattened to the fields that drive damage, rate, spread, recoil, aim snap and switching.
Projectile weapons take damage / radius from the first WeaponProjectiles class default.
Usage: python weapon_mp_table.py <out.json> [<out.md>] [--hp N]  (TTK column uses N hit points, default 300)"""
import sys, json, sqlite3
sys.dont_write_bytecode = True
db = sqlite3.connect(r"F:\Transformers Rebuild\AssetTools\manifests\authored.db")
args = [a for a in sys.argv[1:]]
HP = 300.0
if "--hp" in args:
    i = args.index("--hp"); HP = float(args[i + 1]); del args[i:i + 2]


def P(o):
    r = db.execute("select props from objects where opath=?", (o,)).fetchone()
    return json.loads(r[0] or "{}") if r else {}


BASE = P("TransGame.Default__TnWeaponData")


def get(d, k, default=None):
    return d[k] if k in d else BASE.get(k, default)


rows = []
for o, p in db.execute("select opath, props from objects where opath like 'TransContent.Default__TnWeapon%'"):
    w = json.loads(p or "{}")
    src = "MultiplayerData" if w.get("MultiplayerData") else ("PlayerData" if w.get("PlayerData") else None)
    if not src: continue
    dpath = w[src]; d = P(dpath)
    if not d: continue
    proj = (get(d, "WeaponProjectiles") or [None])[0]
    pc = P(proj.replace(".", ".Default__", 1)) if proj else {}
    pd = P(pc.get("MultiplayerData") or pc.get("Data") or "") if pc else {}   # projectile tuning lives in *_PROJDATA
    ih = get(d, "InstantHitDamage") or []
    dmg = ih[0] if ih else pd.get("Damage")
    fi = get(d, "FireIntervalModifier", {}).get("IntervalRange", {})
    interval = fi.get("Min")
    shots = get(d, "NumShotsToFire", 1)
    burst = get(d, "ShotsPerBurst")
    sp = get(d, "PerShotSpreadModifier", {}) or {}
    rc = get(d, "RecoilCameraParams", {}) or {}
    row = {"weapon": o.split("__")[1], "data": dpath, "source": src,
           "damage": dmg, "damage_radius": pd.get("DamageRadius"), "projectile": proj,
           "fire_interval_s": interval, "fire_interval_max_s": fi.get("Max"), "interval_ramp_s": get(d, "FireIntervalModifier", {}).get("RampTime"),
           "auto": get(d, "bAutoFire"), "shots_per_burst": burst, "burst_delay": get(d, "BurstDelay"), "pellets": shots,
           "clip": get(d, "MaxAmmoClipCount"), "max_ammo": get(d, "MaxAmmoCount"), "reload_s": get(d, "WeaponReloadAnimTime"),
           "spread_min": sp.get("Modifier", {}).get("Min"), "spread_max": sp.get("Modifier", {}).get("Max"),
           "spread_per_shot": sp.get("ModifierChangePerShot"), "spread_cooldown_s": sp.get("Cooldown"),
           "fine_aim_spread": get(d, "FineAimSpreadModifier"),
           "recoil_pitch_deg": rc.get("PitchAdjustmentDeg"), "recoil_time_s": rc.get("RecoilTime"), "recoil_delay_s": rc.get("RecoilDelay"),
           "snap_range": get(d, "TargetSnapRange"), "stickiness": get(d, "TargetStickinessFactor"),
           "range_mods": get(d, "RangeDamageModifiers"), "weapon_range": get(d, "WeaponRange"),
           "equip_s": get(d, "EquipTime"), "putdown_s": get(d, "PutDownTime"), "attach_delay_s": get(d, "AttachDelay"),
           "detach_delay_s": get(d, "DetachDelay"), "owner_anims": get(d, "OwnerAnimations")}
    if isinstance(dmg, (int, float)) and interval:
        per = dmg * (shots or 1)
        row["dps"] = round(per / interval, 1)
        row["shots_to_kill"] = -(-HP // per) if per else None
        row["ttk_s"] = round((row["shots_to_kill"] - 1) * interval, 2) if per else None
    rows.append(row)
rows.sort(key=lambda r: r["weapon"])
json.dump({"hp_for_ttk": HP, "rows": rows}, open(args[0], "w"), indent=1)
if len(args) > 1:
    cols = ["weapon", "source", "damage", "pellets", "fire_interval_s", "auto", "clip", "reload_s", "dps", "shots_to_kill", "ttk_s",
            "spread_min", "spread_max", "spread_per_shot", "spread_cooldown_s", "fine_aim_spread", "recoil_pitch_deg", "snap_range",
            "equip_s", "putdown_s"]
    with open(args[1], "w", encoding="utf-8") as f:
        f.write("| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n")
        for r in rows:
            def fmt(v):
                if isinstance(v, float): return "%g" % round(v, 4)
                if isinstance(v, dict): return "%g–%g" % (v.get("Min", 0), v.get("Max", 0))
                return "" if v is None else str(v)
            f.write("| " + " | ".join(fmt(r.get(c)) for c in cols) + " |\n")
print(len(rows), "weapons")
