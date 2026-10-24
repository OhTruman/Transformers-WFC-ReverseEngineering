# DLC_RE plan (RE, 2026-10-23; plan only, runs after RELEASE and AssetTools' extraction)

**Scope:** the RE part of Rebuild docs/DLC_PLAN.md step 2. The deliverable is `work/handoff/DLC_RE.md`: what each pack adds and
how the original gates and lists it.

**Inputs (read-only):**
- AssetTools' extracted pack files (.xxx / .tfc / .ini / .int) and their inventory;
- the shipped TransGame / TransContent script (work/script/decomp, decomp_tc);
- the exe through the existing headless runner (no shared-server changes).
- Never the STFS folder in place, except as read-only; nothing is written there.

## Anchors already known (C, from the shipped script; found during the freeze with grep only)
- **Maps carry a `DlcId`:** `TnDataProvider_MapInfo.DlcId`, plus `HasRequiredAssets()`.
- **Playlist gating:**
  - `TnDataProvider_OnlinePlaylist.IsProviderDisabled` = !VisibleInMenu || !HasRequiredContent.
  - HasRequiredContent collects the DlcIds of every map provider whose assets are present, then asks
    `OnlinePlaylistManager.HasRequiredContentForPlaylist(PlaylistId, LocalContentIds)`.
  - So **a playlist is greyed out unless every content id it requires is installed.**
- **Lobby map choice:** `TnGameReplicationInfoGameLobby.MapCanBePlayed` = the map's DlcId is among the selected playlist's
  `GetContentIdsFromPlaylist` (any map when no playlist is selected).
- **Removal / corruption:**
  - TnPlayerController shows `DLCContentRemovedMessage` / `CorruptDLC*` popups via `TnGame.HandleContentAvailabilityChangeMessage`;
  - HmPlayerController re-reads all DLC when the storage device changes (Engine.OnlineContentInterface).

## Work list, in order
1. **Pack identity:** each pack's STFS display name, title / offer ids and license mask, from the headers, and its content id. Map
   these to the DlcId values used by the map providers.
2. **What each pack adds**, from the pack .ini / .int files and the packages:
   - the TnDataProvider_MapInfo entries (map name, game types, DlcId, preview image, localised name);
   - the playlist entries;
   - new characters (TnDataProvider / character-select entries, ROBODEF / chassis, abilities, weapons);
   - the Escalation maps and their SpawnList / wave data (same tables as ESCALATION_WAVES_RE);
   - any new script classes in the pack maps (decompile with the existing tools into work/script/decomp_dlc).
3. **How the original merges a pack at runtime:**
   - the OnlineContentInterface / DLC mount path in the exe (content enumeration, ini / int merge, package path add);
   - where the menu data store (TnDataStore_MenuItems.GetMapProviders) picks up the pack's providers;
   - how character select lists DLC characters, and what the gate is (DlcId, a license check or an unlock).
4. **Playlists:** the online playlist file's content-id requirements, if it's shipped in the dump or the packs (else marked
   UNKNOWN). Also whether the Quick Match pools mix DLC maps.
5. **For Frontend:** the rebuild treats every DlcId as owned (DLC_PLAN: no entitlement check). I'll list exactly which checks to
   short-circuit: HasRequiredAssets, HasRequiredContentForPlaylist, MapCanBePlayed, plus the character gate from step 3.

**Labels:** C / H / UNKNOWN as usual. One commit, plus a message to Integration and the owning lanes (Frontend for gating / lists,
Gameplay for characters / ESC, AssetTools for paths).
