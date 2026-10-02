# WFC multiplayer / network architecture — 2026-10-01

Sources: default.xex natives via headless Ghidra (read-only snapshot; ReVa was down) and UnrealScript bytecode decompiled
with `tools/ue3dis.py` from Engine, IpDrv, OnlineSubsystemLive, OnlineSubsystemDemonware, Demonware, TransGame and the lobby maps
(`work/script/decomp*/`). Cooked config was read from `ExtractedAssets/config/.../Xe-TransEngine.ini` (read-only).
Native registration table: `data/native_functions_full.tsv`, 2451 entries, about 2424 resolved, from `tools/scan_natives_full.py` + emulation.
Labels: CONFIRMED / HIGH / INFERRED / UNKNOWN.

Corrections to the earlier (conversation-only) findings:
- The LSP service id in the code is **0x415607E9**. "0x41560E79" was a digit transposition.
- The Demonware title id literal in the login code is **0x14B3** (5299), not 0x1483.
- TCP port **1020** is CONFIRMED.

---

## 1. Layering (CONFIRMED)
| Layer | 360 implementation | Role |
|---|---|---|
| Online subsystem | `OnlineSubsystemLive.OnlineSubsystemLiveDemonware` (`DefaultOnlineSubsystemName`) | Live (XSession/XUser) **plus** Demonware services |
| Sessions / matchmaking search | **Xbox Live**: `UOnlineSubsystemLive::CreateOnlineGame/FindOnlineGames/JoinOnlineGame/...` natives (0x829DFAE0, 0x829E33E0, 0x829DFD18, ...) | session create/search/join, host address (XNADDR/XNKID/XNKEY) |
| Demonware (via LSP) | `DemonwareLobbyServiceLive` + `bdLobbyService` | login, stats mirror, key archive, storage, global counters, groups, event recorder, **chat channels (used as the reservation transport)**, session advertising (UpdateOnlineGame) |
| Reservation ("party beacon") | UE3 `PartyBeaconHost/Client` with `ConnectionTypeName=Demonware.PartyBeaconConnectionDemonware` | slot reservation, join/travel instructions, heartbeats; carried as Demonware **chat whisper** messages |
| Gameplay transport | UE3 `NetworkDevice=OnlineSubsystemLive.IpNetDriverLive`, `IpConnectionLive`, URL `Port=1000`, `[LiveSock] bUseVDP=True bUseSecureConnections=true` | stock UE3 bunch protocol over Xbox VDP/UDP, listen-server topology |
| PC build path (unused on 360) | `OnlineSubsystemDemonware` + `DemonwareAccountService`: auth `tf2010-pc-auth.mmp3.demonware.net:3074`, LSG `tf2010-pc-lsg-dev...:3074`, PlatformTitleId **5173**; `TDwNetDriver` with STUN `stun.{us,eu,jp,au}.demonware.net` | reference only |

Topology: **player-hosted listen server**. The party leader hosts the party lobby map. The match host hosts the game lobby and then the match.
There is **no host migration**: none of the online/game script contains migration code, and `OnlineSessionJoiner` and `OnlineDisconnector` have no migration path. HIGH: when the host leaves, the session ends.

## 2. End-to-end flow (CONFIRMED unless noted)
```
boot -> Live sign-in (XUser)
     -> OnlineSubsystemLiveDemonware.Init: InitializeDemonwareLibrary, TaskList, Lobby, SessionAdvertiser(TransformersSessionAdvertiser),
        Stats/KeyArchive/EventRecorder/Storage/Group/Chat readers, RegisterEventHandler
     -> Demonware login (LoginToOnlineService -> Lobby.Login):
          StartEnumeratingServers (0x829EC020 -> 0x829EB5A8):
             XAM msg 0x58007 (service-info check) for service 0x415607E9
             XTitleServerCreateEnumerator("", 50) ; XEnumerate -> up to 50 x XTITLE_SERVER_INFO (0xD0 bytes)
          ConnectToEnumeratedServers (0x829EC0C8 -> 0x829EB730):
             pick a RANDOM server (rand % n, removed from list)               [0x829CEC88]
             XNetServerToInAddr(server.ina, 0x415607E9) -> secure IP
             bdAddr(secureIP, port 1020 = 0x3FC)
             build bdAuthTicket (title 0x14B3, XUID, gamertag[64]) -> 128-byte LE ticket   [0x8357D878 / 0x8357D920]
             async task "Connect to Demonware Lobby" -> bdLobbyService connect   [0x8357BA18]
     -> UI_PartyLobby_m (TnPartyLobbyGame, listen server hosted by the party leader; session 'Party')
          party leader: CreatingPartySessions -> reservation host = Demonware chat channel -> Live sessions (persistent + presence)
          PlayPlaylist(PlaylistId):
             playlist settings from TnOnlinePlaylistManager (downloaded title file)
             HostType==1 -> HostOnlineGame directly
             else Live search 'VERSUS' (FindOnlineGames) with:
                  string context 32779 (0x800B) = game mode
                  property 0x10000023 = PlaylistId
                  property 0x10000046 = matchmaking region (WorldInfo.GetRegionCode; 0 or 6 -> 1)
             FindingGames -> ReservingSpace: for each result in order:
                  ReservationInterface.RequestReservation(result, IncludeAllPartyMembers=true)   (beacon, section 4)
                  accepted (result 4) -> JoiningGame ; rejected -> next result
             none left -> HostPlaylist: HostOnlineGameInternal(settings + playlist + region)
     -> party members get beacon packet 5 (JoinSession) -> PC.ClientJoinSession -> OnlineSessionJoiner
     -> OnlineSessionJoiner (Engine): Reserving -> [Disconnecting old sessions] -> JoinOnlineGame (Live)
          -> GetResolvedConnectString -> ClientTravel("a.b.c.d?UniqueId=<netid>")
     -> UI_Lobby_m (TnGameLobbyGame on the match host; session 'Game'; LobbyIntermissionTime 45 s)
     -> TnGame.ServerTravelToMap(MapURL, absolute) : SEAMLESS server travel into the MP map
     -> gameplay replication (UE3)
     -> end: GameInfo.EndOnlineGame -> OnlineSubsystemLiveDemonware.WriteOnlineStats / FlushOnlineStats
             (Live stats first; Demonware stats only if Live succeeded)
          -> ServerTravel(GameLobbyURL?MapId=<id>, seamless) back to the game lobby
```
Two named sessions are used throughout: **'Party'** and **'Game'**.

## 3. Host address and connect string (CONFIRMED)
`PlatformSpecificInfo` (88 bytes, `UOnlineSubsystemLive::ReadPlatformSpecificSessionInfo` → 0x829CF430):
```
+0x00 XNADDR   (36)   host title address
+0x24 XNKID    (8)    session key id
+0x2C XNKEY    (16)   session key
+0x3C UniqueNetId x3 (24)  (session owner / related ids)
+0x54 u32 BE   packed settings: ((NumPublicConnections<<8 | NumPrivateConnections)<<16) | 10 flag bits (shared packer 0x82D24278, also used by OnlineGameSettings::PackData)
```
`GetResolvedConnectString` (0x829CF998) finds the named session and, if secure networking is on, calls `XNetXnAddrToInAddr(XNADDR, XNKID)`. Otherwise it takes the raw IP.
It formats `"%i.%i.%i.%i"` **with no port**, so the client uses URL `Port=1000`. `OnlineSessionJoiner` appends `?UniqueId=<UniqueNetIdToString>`.

## 4. Reservation beacon over Demonware chat (CONFIRMED)
Transport `PartyBeaconConnectionDemonware`:
- **Host** `InitAsHost`: `OnlineChat.CreateChatChannel()`. The channel id becomes `GameSettings.ReservationChannel` (advertised with the session). The host never sends or receives on its own connection.
- **Client** `InitAsClient(DesiredHost)`: `TargetUserId = GameSettings.OwningPlayerId`, `SubscribeToChatChannel(ReservationChannel)`.
- The host's `OnChatChange(status 0 = joined)` creates a child connection per joining user (`InitAsChild(UserId, channel)`). A leave notify from the peer puts that connection into the error state.
- `Send`: max **1024 bytes**, `SendChatWhisperMessage(ReservationChannel, TargetUserId, data)`. `Recv` drains the per-connection receive buffer filled by `OnChatMessage` (sender must equal TargetUserId).
- An alternative stock transport exists: `PartyBeaconConnectionSocket` with `PartyBeaconPort=8675`, plus `HeartbeatTimeout=60`, `ReservationRequestTimeoutRange=(4..10)` s and `ConnectionBacklog=9`.

Packet types (byte 0). Multi-byte fields are **big-endian**; FString uses UE3 FString serialisation (`0x829C6B78`).

| id | dir | name | payload |
|---|---|---|---|
| 1 | C→H | ReservationRequest (0x82B01920) | `u64 PartyLeaderNetId` · `u32 NumPlayers` · NumPlayers × {`u64 NetId` · `FString` · `u32` · `u64`(f64) · `u64`(f64)} (FPlayerReservation 0x28: NetId, name?, Skill/XpLevel, Mu, Sigma; INFERRED field names) |
| 2 | C→H | CancelReservation (0x82B01828) | |
| 3 | H→C | ReservationResponse (0x82AFFF18) | `u8 Result` (**4 = accepted**); if 4: `FString SessionName` · 88-byte PlatformSpecificInfo |
| 4 | C→H | (update request; ignored by client) | INFERRED |
| 5 | H→C | TellClientsToJoinSession (0x82B02218) | `FString SessionName` · `FString SearchClass` · `u8 PostJoinSessionOption` · 88-byte PlatformSpecificInfo |
| 6 | H→C | HostIsReady (0x82AFEC88) | — |
| 7 | H→C | HostHasCancelled (0x82AFED38) | — |
| 8 | both | Heartbeat — client echoes 8 | — |
| 9 | C→H | RequestReturnToSession (0x82B01D68) | — |
| 10 | H→C | ReturnToSessionResponse | `u8` (0 = ok) |

Client dispatcher: 0x82B01E80 (accepts 3,5,6,7,8,10). The client stops caring about heartbeats once it has a game connection (`NotifyPlayerConnected`).

## 5. Gameplay transport (CONFIRMED)
- Driver and connection: `UIpNetDriverLive` (class size 0x164), `UIpConnectionLive` (0x51D8, vtable 0x821F87F8, base UIpConnection 0x821F8320). `sockaddr_in` is at +0x4FAC.
- `UIpConnectionLive::InitConnection` (0x829EC1E8): VDP mode comes from the socket subsystem. **MaxPacket defaults to 510 (0x1FE).**
- `LowLevelSend` (0x829D6D18): in VDP mode the datagram is `u16 BE GameDataLen` + game data, with voice appended (0x829D14F0) only if ≥113 bytes remain under 510. Non-VDP falls back to base `UIpConnection::LowLevelSend` (raw UDP).
  Send errors (WSA 0x2743+{0,2,3,9,14}) close the connection with an error message.
- `UNetConnection::ReceivedPacket` (0x82D98788) is the **stock UE3 bitstream**:
  ```
  PacketId = ReadInt(16384) (relative)
  loop until end:
    bIsAck = ReadBit
    ack:    AckPacketId = ReadInt(16384)
    bunch:  bControl; [bOpen, bClose]; bReliable; ChIndex = ReadInt(1023);
            if bReliable: ChSequence = ReadInt(1024) (relative)
            if bReliable || bOpen: ChType = ReadInt(8)
            BunchDataBits = ReadInt(MaxPacket*8); data
  SendAck(PacketId)
  ```
  Channel types are looked up in a table at 0x83832100 (8 entries).
- `UNetConnection::FlushNet` (0x82D8E718): stock UE3. Terminator bit 1 then zero-pad to byte, packet-loss/dup/lag simulation, keep-alive when idle > KeepAliveTime.
- `UNetConnection::Tick` (0x82D93660): stock timeouts and bandwidth.
- Config `[IpDrv.TcpNetDriver]`: ConnectionTimeout **8**, InitialConnectTimeout **50**, AckTimeout 1.0, KeepAliveTime **0.1**, MaxClientRate 15000, MaxInternetClientRate 10000, NetServerMaxTickRate **30**, LanServerMaxTickRate 35, RelevantTimeout 5, SpawnPrioritySeconds 1, ServerTravelPause 4, AllowDownloads False. `ConfiguredInternetSpeed=10000`, `bDynamicNetSpeed=true`.
- WFC-specific vs stock UE3: the protocol bit layout, FlushNet and Tick are stock. WFC/Live-specific pieces are the VDP framing, MaxPacket 510, secure-address resolution, the reservation beacon over Demonware, seamless lobby↔match travel, and the custom lobby games.

## 6. System link / LAN (CONFIRMED config, HIGH behaviour)
`[OnlineSubsystemLive] LiveSystemLinkPort=14000`, `LanAnnouncePort=14001`, `LanPacketPlatformMask=4`, `LanQueryTimeout=2.0`.
`[IpDrv.OnlineGameInterfaceImpl] LanGameUniqueId=0x000B100D`. `UdpBeacon` ServerBeaconPort 8777 / BeaconPort 9777 (stock UE3 LAN beacon; DoBeacon=True).

## 7. Demonware services used (natives CONFIRMED addresses, see `data/native_functions_full.tsv`)
Lobby (0x82AEB810 ConnectToLobbyServiceGateway, 0x82AF5E28 PumpLobby, ...), AsyncTaskList, ChatService (CreateChatChannel 0x82AF95A0, Subscribe 0x82AF9620, Unsubscribe 0x82AF96C0, SendChatMessage 0x82AF9760, **SendChatWhisperMessage 0x82AF9868**), SessionAdvertiser (Create/Update/Destroy/Start/End/Register/Unregister), StatsReaderWriter (Write/Flush/Read*), StorageReaderWriter (title/user files), KeyArchiveReaderWriter, GlobalCounterReaderWriter, GroupReaderWriter, EventRecorder.
LiveDemonware's own natives: Register/UnregisterPlayer, Read/WriteProfileSettings, Initialize/ShutDownDemonwareLibrary, RegisterEventHandler, AddAsyncTask, CancelAllLobbyTasks, OnSecondaryOnlineServiceLoginChange (resolved by emulating initializer 0x835E02B8).

## 8. Gameplay replication — first layer (CONFIRMED)
Full RPC inventory: `data/rpcs.tsv` (282 RPCs: Engine 145, HM_Engine 30, TransGame 107), produced by `tools/rpc_dump.py`.
FunctionFlags are a u32 BE at script_end+7; bits 0x40 Net, 0x80 Reliable, 0x200000 NetServer, 0x1000000 NetClient.
- **Instant-hit weapons are client-authoritative ("favor the shooter").** Engine.Weapon.InstantFire is WFC-modified:
  - The owning client (Role < Authority) traces, sets `HitInfo.Item = HitActor.MapHitComponentToIndex(comp)`, runs local `ProcessInstantHit` and effects.
  - It then calls `ServerImpact(FireMode, Impact, bFirst)` (TnWeapon override, **reliable**).
  - The server (`Weapon.ServerImpact`) rebuilds HitComponent from the index and calls `ProcessInstantHit` (damage) without re-tracing. If bFirst, it also calls `SetFlashImpact` + `ConsumeAmmo`.
  - `HmWeapon.ShouldRegisterDamage` only applies damage on the client for torn-off pawns and crowd agents. `HmWeapon.InstantFire` on the server sends "nearly shot" notifications.
  Projectiles use `TnWeapon.ServerFireProjectile` (reliable). Heat is synced with `ServerSyncWeaponheat`.
- **Vehicles are owner-simulated.** Each physics update, `TnVehicleForm.PackVehiclePhysicsState` packs `{Location, LinearVelocity×10, RotationQuat, AngularVelocity×1000}` and sends `ServerSetVehiclePhysicsState` (**unreliable**).
  The server stores it in replicated `_PhysicsState`. On other machines (`MotionIsKeyframed` = !LocallyControlled && !dead), `ExtrapolateVehiclePhysicsState` zeroes RB velocities.
  On a fresh state it sets RB pos = state.Location − vel·dt (rot likewise); otherwise it advances pos += vel·dt and rot by angvel·dt.
  Car-form input flags are packed into `ServerSetLocationAndRotation(Location, Rotation, PackedFlags)` (**unreliable**) from `PlayerInCarForm.SetRemoteInputs`.
- Robot movement: stock UE3 PlayerController ServerMove / ClientAdjustPosition family (Engine RPCs), plus `TnPlayerController.LongClientAdjustPosition` (unreliable).
- Transform: `ServerTransform(TargetForm, ClientLocation, ClientRotation)` (reliable). For robot targets the server first snaps to the client location/rotation, then runs DoTransform.
- Other notable gameplay RPCs: ServerPickup, ServerInteractCommand, ServerHardLock, revive (ServerGiveRevive/GetRevive/ServerAbortGiveRevive), DownedSuicide, ServerDetonate/ServerSetGuidedMissileInput, ClientTeleport (pawn and vehicle), ClientNotifyCausedDamage (unreliable hit-marker), ClientNotifyXpEvent/ScoreEvent, ClientReturnToParty / ClientPartyDisbanded.
- Replicated property conditions (`replication {}` blocks) are not decoded yet. They live in each class's script; the next step is to extend ue3dis to class-level bytecode.

---

## REQUIRED FOR LOCAL / LAN MULTIPLAYER (rebuild)
1. A UE3-compatible (or behaviour-equivalent) listen-server net layer: UDP, packets ≤ 510 bytes, PacketId/ack/bunch semantics as in §5, timeouts 8 s (50 s initial), keepalive 0.1 s, server tick 30 Hz (LAN 35).
   Plain UDP is fine: VDP framing is a Live artifact.
2. Discovery: a LAN broadcast equivalent of LanAnnouncePort 14001 / UdpBeacon 8777/9777. Join by `ip:1000`.
3. The lobby flow (party lobby → game lobby → seamless travel to the map → back to the lobby after the match). Reservations can be local (direct socket, as the stock PartyBeaconConnectionSocket on 8675).

## REQUIRED FOR INTERNET MULTIPLAYER
1. **Session directory** replacing XSession: create/update/search/join/destroy. Search results must carry:
   OwningPlayerId/Name, host public address and port, ReservationChannel (or relay endpoint), open public/private slots, playlist id (0x10000023), region (0x10000046), game mode (0x800B), and the packed settings flags.
2. **Reservation relay** replacing the Demonware chat channel: a per-host channel, client subscribe, ≤1024-byte whisper to the host, join/leave notifications. Packet formats in §4 can be carried verbatim.
3. NAT traversal or relay for UDP game traffic (on 360 this was XNet secure addresses; on PC Demonware used STUN for TDwNetDriver).
4. Identity: a stable 64-bit UniqueNetId per player (it replaces the XUID in reservations, `?UniqueId=` and the stats keys).

## OPTIONAL LEGACY ONLINE SERVICES
Demonware stats mirror, key archive, title/user storage (playlist and title files can ship locally), global counters, groups, event recorder, rich presence (TnDemonwarePresence), Live achievements/skill (TrueSkill Mu/Sigma in reservations), voice (VDP voice appended to packets).

## Unknown / next
- `bdLobbyService` wire framing on TCP 1020 was mapped in the prior session but not re-verified here (connect entry 0x8357BA18).
- Exact FPlayerReservation field names; packet 4 semantics; the host-side packet handler (counterpart of 0x82B01E80).
- Gameplay replication per class (Tn* replicated properties and RPCs) is the next layer.
