"""Read-only: extract WFC multiplayer progression/scoring tables from the coalesced ini + INT localization JSON
(ExtractedAssets/config/Coalesced_ini.json, Coalesced_int.json) and authored.db, into notes/data/mp_*.json.

Outputs:
  mp_xp_events.json      XP event types: XpAmount, DeathmatchXpAmount, localized Announcement/Description
  mp_level_table.json    per-specialty level thresholds (TnXpManager.LevelTable) + derived level/XP table
  mp_challenges.json     TnDataProvider_Challenge: ids, stat ids, category, goals/XP per tier, prime flag, loc text
  mp_class_unlocks.json  skills/abilities/killstreaks/specialties/chassis with Specialty/Level restrictions + loc
  mp_game_modes.json     per-mode settings: game class, rules, points-to-win options/default, time limits, rounds
Usage: python mp_progression_extract.py
"""
import json, os, re, sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = r"F:\Transformers Rebuild\ExtractedAssets\config"
DB = r"F:\Transformers Rebuild\AssetTools\manifests\authored.db"
OUT = os.path.join(ROOT, "notes", "data")

ini = json.load(open(os.path.join(CFG, "Coalesced_ini.json"), encoding="utf-8"))
loc = json.load(open(os.path.join(CFG, "Coalesced_int.json"), encoding="utf-8"))


def ini_file(suffix):
    for k, v in ini.items():
        if k.endswith(suffix):
            return v
    raise KeyError(suffix)


def loc_file(suffix):
    for k, v in loc.items():
        if k.replace("\\", "/").endswith(suffix):
            return v
    return {}


def one(sec, key, default=None, conv=None):
    v = sec.get(key)
    if v is None:
        return default
    v = v[-1] if isinstance(v, list) else v
    return conv(v) if conv else v


def num(s):
    s = s.strip()
    return int(s, 16) if s.lower().startswith("0x") else (int(s) if re.fullmatch(r"-?\d+", s) else float(s))


game = ini_file("Xe-TransGame.ini")
tg_loc = loc_file("INT/TransGame.int")

# ---- XP events
base = game.get("TransGame.TnXpEventType", {})
xp = []
for sec, vals in game.items():
    m = re.fullmatch(r"TransGame\.(TnXpEventType\w+)", sec)
    if not m:
        continue
    n = m.group(1)
    L = tg_loc.get(n, {})
    xp.append({"class": n,
               "XpAmount": one(vals, "XpAmount", None, num),
               "DeathmatchXpAmount": one(vals, "DeathmatchXpAmount", None, num),
               "Announcement": one(L, "Announcement", ""), "Description": one(L, "Description", "")})
xp_doc = {"GlobalXpMultiplier": one(base, "GlobalXpMultiplier", 1, num),
          "DeathmatchXpAmount_default": one(base, "DeathmatchXpAmount", -1, num),
          "rule": "award = GlobalXpMultiplier * (DeathmatchXpAmount if DeathmatchXpAmount>=0 and !GRI.GameClass.bTeamGame else XpAmount); 0 if !GRI.CanGainXp()",
          "events": xp}
json.dump(xp_doc, open(os.path.join(OUT, "mp_xp_events.json"), "w"), indent=1)

# ---- level table
lt = [num(x) for x in game["TransGame.TnXpManager"]["LevelTable"]]
levels = [{"level": 0, "xp_min": 0}] + [{"level": i + 1, "xp_min": v} for i, v in enumerate(lt)]
cc = game.get("TransGame.TnCharacterCustomizationData", {})
json.dump({"LevelTable": lt, "max_level_per_specialty": len(lt), "xp_cap_per_specialty": lt[-1],
           "levels": levels,
           "UnlockCharacterSlotLevels": [num(x) for x in cc.get("UnlockCharacterSlotLevels", [])],
           "NumberOfColorPalettes": one(cc, "NumberOfColorPalettes", None, num),
           "displayed_player_level": "sum of the four specialty levels (TnPlayerReplicationInfo.SetPlayerLevel), 0..100"},
          open(os.path.join(OUT, "mp_level_table.json"), "w"), indent=1)

# ---- challenges
ch_ini = ini_file("TransChallenges.ini")
ch = []
for sec, vals in ch_ini.items():
    if not sec.endswith("TnDataProvider_Challenge"):
        continue
    key = sec.split(" ")[0]
    L = tg_loc.get(sec, {}) or tg_loc.get(key, {})
    ch.append({"key": key, "ChallengeId": one(vals, "ChallengeId", None, num),
               "StatPropertyId": one(vals, "StatPropertyId", None, num),
               "CategoryId": one(vals, "CategoryId"),
               "GoalValues": [num(x) for x in vals.get("GoalValues", [])],
               "XpRewardValues": [num(x) for x in vals.get("XpRewardValues", [])],
               "PrimeChallenge": one(vals, "PrimeChallenge", "false").lower() == "true",
               "ChallengeName": one(L, "ChallengeName", ""), "Description": one(L, "Description", "")})
json.dump(ch, open(os.path.join(OUT, "mp_challenges.json"), "w"), indent=1)

# ---- class unlocks
cu = ini_file("TransCustomization.ini")
prov = []
for sec, vals in cu.items():
    m = re.fullmatch(r"(\S+) (TnDataProvider_\w+)", sec)
    if not m:
        continue
    L = tg_loc.get(sec, {})
    d = {"key": m.group(1), "type": m.group(2)}
    for k, v in vals.items():
        d[k] = v[-1] if isinstance(v, list) and len(v) == 1 else v
    d["FriendlyName"] = one(L, "FriendlyName", "")
    d["Description"] = one(L, "Description", "")
    prov.append(d)
json.dump(prov, open(os.path.join(OUT, "mp_class_unlocks.json"), "w"), indent=1)

# ---- game modes (authored.db CDOs + ini time limits)
db = sqlite3.connect(DB)
modes = {}
for tag in ("TDM", "DM", "DOM", "CTF", "EXT", "KOTH", "SV"):
    d = json.loads(db.execute("select props from objects where opath=?",
                              ("TransGame.Default__TnOnlineGameSettings" + tag,)).fetchone()[0])
    pub = db.execute("select props from objects where opath=?", ("TransGame.Default__TnOnlineGameSettings" + tag + "Public",)).fetchone()
    priv = db.execute("select props from objects where opath=?", ("TransGame.Default__TnOnlineGameSettings" + tag + "Private",)).fetchone()
    props = {p["PropertyId"]: p["Data"].get("Value1") for p in d.get("Properties", [])}
    maps = {m["Name"]: [x.get("Value1") for x in m.get("PredefinedValues", [])] for m in d.get("PropertyMappings", [])}
    tl_ini = [num(x) for x in game.get("TransGame.TnOnlineGameSettings" + tag, {}).get("TimeLimits", [])]
    locs = {s["Id"]: s["ValueIndex"] for s in d.get("LocalizedSettings", [])}
    modes[tag] = {"FriendlyName": d.get("FriendlyName"), "Description": d.get("Description"),
                  "RulesFormat": d.get("RulesFormat"), "GameClass": d.get("GameClass"),
                  "TeamType": d.get("TeamType"), "NumRequiredPlayers": d.get("NumRequiredPlayers"),
                  "Rules": d.get("Rules"),
                  "PointsToWin_options": maps.get("PointsToWin"), "PointsToWin_default": props.get(1073741832),
                  "Rounds_options": maps.get("Rounds"), "Rounds_default": props.get(1073741830),
                  "TimeLimit_options_s": maps.get("TimeLimit") or tl_ini,
                  "TimeLimit_default_s": props.get(1073741831) or (tl_ini[locs[1073741831]] if 1073741831 in locs and tl_ini else None),
                  "public": json.loads(pub[0]) if pub else None, "private": json.loads(priv[0]) if priv else None}
json.dump(modes, open(os.path.join(OUT, "mp_game_modes.json"), "w"), indent=1)
print("xp", len(xp), "levels", len(lt), "challenges", len(ch), "providers", len(prov), "modes", len(modes))

# ---- kill award rules (TnGameRules_TrackKillsMP.KillAwardManager0 -> rule archetypes = TnKillAwardManager CDO rules)
def P(o):
    r = db.execute("select class,props from objects where opath=?", (o,)).fetchone()
    return (r[0], json.loads(r[1] or "{}")) if r else (None, {})
_, mgr = P("TransGame.Default__TnKillAwardManager")
rules = []
for r in mgr.get("Rules", []):
    c, d = P(r)
    _, cdo = P("TransGame.Default__" + c)
    merged = dict(cdo); merged.update(d)
    merged = {k: v for k, v in merged.items() if k not in ("Components",)}
    rules.append({"name": r.split(".")[-1], "class": c, "config": merged})
json.dump({"manager": "TransGame.Default__TnGameRules_TrackKillsMP.KillAwardManager0 (rules = archetypes of TnKillAwardManager CDO)",
           "base_kill_xp": "TnXpEventTypeKill always first, inside one XP transaction (popup group)",
           "rules": rules}, open(os.path.join(OUT, "mp_kill_awards.json"), "w"), indent=1)

# ---- navigation audit (inventory.db export classes per MP base map)
inv = sqlite3.connect(r"F:\Transformers Rebuild\AssetTools\manifests\inventory.db")
navk = ("path", "pylon", "navmesh", "navigation", "reachspec", "cover", "playerstart", "spawnpoint", "tactical", "jump")
nav = {}
for pkg, cls, n in inv.execute("select package,class,count(*) from exports where substr(package,1,3)='MP_' "
                                "and (package like '%BASE_m' or package like '%Base_m') group by package,class"):
    if any(k in cls.lower() for k in navk) or cls in ("TnKingOfTheHillZoneBase", "TnDominationPointBase", "TnFlagCapturePointBase",
                                                     "TnBombPlantPointBase", "TnGameObjectivePickupFactoryFlag", "TnGameObjectivePickupFactoryBomb"):
        nav.setdefault(pkg, {})[cls] = n
json.dump(nav, open(os.path.join(OUT, "mp_navigation_audit.json"), "w"), indent=1, sort_keys=True)
print("kill award rules", len(rules), "nav maps", len(nav))
