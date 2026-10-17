
### Hud_GFX.gfx (72 entry points)

| Entry point | Ours | Sounds | Animation (interp: target time easing {props}) / timeline | Spawned symbols / timers / engine calls |
|---|---|---|---|---|
| AbilityType0Jammed | - | - | - | - |
| AbilityType1Jammed | - | - | - | - |
| AbilityType2Jammed | - | - | - | - |
| AddObjective | C | HUD_OBJECTIVE_ADDED | - | mc_objectiveNew{GlyphLine 0.5s easeout {_yscale: 0, _alpha: 0}; ObjectiveLine 0.5s easeout {_yscale: 100, _alpha: 100}; GlyphLine 0.5s easeout {_alpha: 100, _x: 0}} |
| ApplyBuff | C | - | - | - |
| ApplyKillstreakBuff | - | - | KillstreakBuffs[i] 0.3s easeout {_y: (i * IconSpacing)} | mc_killstreakBuffIcon{thisElement 0.4s easeout {callback: removeMe, _yscale: 150, _xscale: 150, _alpha: 0}} |
| CausedDamage | C | HUD_POSITIVE_HIT_INDICATOR | - | mc_causeDamage |
| DisplayRangeFinder | - | - | - | mc_rangeFinderCrosshair{thisElement 0.5s easeout {callback: removeMe, _alpha: 0}} |
| DisplayTurretReticule | - | - | - | mc_turretReticule{this 1s easeout {_rotation: 0}; petal1_mc.base_mc 0.2s easeout {_y: -20}; petal2_mc.base_mc 0.2s easeout {_y: -60}} |
| FinishMarkerUpdate | C | - | - | - |
| GameAnnouncement | C | - | announcement_mc 0.4s easeout {_yscale: 100, _xscale: 100, _alpha: 100} | - |
| GameMessage | C | - | messageQueue[i] 0.2s easeout {_y: (i * -22)} | mc_gameMessage_default{this 1s easeout {callback: removeMe, _alpha: 0}} |
| GameMessageSpectatorMode | C | - | thisElement 0.5s easeout {_y: (initialPosY - 160)}; thisElement 0.5s easeout {_y: initialPosY} | - |
| NotifyAbilityType0Changed | C | - | - | - |
| NotifyAbilityType0UpdateCooldown | C | - | - | - |
| NotifyAbilityType1Changed | C | - | - | - |
| NotifyAbilityType1UpdateCooldown | C | - | - | - |
| NotifyAbilityType2Changed | C | - | - | - |
| NotifyAbilityType2UpdateCooldown | C | - | - | - |
| NotifyActiveGrenadeCount | C | - | - | mc_activeGrenadePromptText{this 0.2s easeout {_alpha: 100, _x: -10}; thisElement 0.5s easeout {callback: removeMe, _alpha: 0}} |
| NotifyAmmoAdded | C | - | - | mc_ammoPickupNotification{_parent.AmmoPickupArray[i] 0.2s easeout {_y: (i * _parent.NotifySpacing)}; thisElement 0.8s easeout {callback: removeMe, _alpha: 0, _y: -50}; this 0.4s easeout {_alpha: 100, _x: 0}} |
| NotifyBadConnection | - | - | - | mc_networkConnectivityAlert |
| NotifyCantTransform | C | - | - | mc_cantTransform{this 1s easeout {callback: removeMe, _alpha: 0}; this 0.2s easeout {color: 16724787, _alpha: 100, _yscale: 100}} |
| NotifyContextualCommand | C | - | NotifyArray[i] 0.2s easeout {_y: ((i * NotifySpacing) + NotifySpacing)} | mc_notify{this 0.2s easeout {_alpha: 100}; this 0.5s easeout {callback: removeMe, _alpha: 0}} |
| NotifyCurrentFormChanged | C | - | - | - |
| NotifyCurrentWeaponChanged | C | - | - | mc_currentWeaponIcon{this 0.5s easeout {_alpha: 100, _x: 0}; thisElement 0.3s easeout {callback: removeMe, _alpha: 0, _x: 10}}, mc_currentWeaponText{this 0.5s easeout {_alpha: 100, _x: 0}; thisElement 0.5s easeout {callback: removeMe, _alpha: 0, _y: 10}} |
| NotifyDamageIncrease | C | - | - | mc_crosshairIncreaseDamage |
| NotifyDamageIndicatorAdded | C | - | - | mc_damageArrow{this 1s easein {callback: this.deleteMe, _alpha: 0}} |
| NotifyDownedWarningFade | - | - | - | mc_hurt{tunnelVision_mc 3s easeout {_alpha: 0}; sideEffect_mc 3s easeout {_alpha: 0}; tunnelVision_mc 3s easeout {_alpha: 30}} |
| NotifyFineAimChanged | C | - | - | - |
| NotifyGrenadeAmmoChanged | C | - | - | mc_grenadeIcon{thisElement 0.4s easeout {callback: removeMe, _yscale: 150, _xscale: 150, _alpha: 0}; this 0.4s easeout {_rotation: 0, _yscale: 100, _xscale: 100, _alpha: 100}} |
| NotifyHudScrambledChanged | C | - | midCenter_mc 0.5s easeout {_alpha: 0}; midCenter_mc 0.5s easeout {_alpha: 100} | - |
| NotifyKillstreakChanged | C | - | thisElement 0.2s easeout {_alpha: 100}; thisElement 0.2s easeout {_alpha: 0} | mc_killstreakIcon{iconContainer 0.5s easeout {_x: 20}; thisElement 0.5s easeout {callback: removeMe, _alpha: 0}} |
| NotifyLevelUp | C | MP_LEVEL_UP_MX_STNG | gotoAndPlay(fadeOut) | mc_levelUpNotify |
| NotifyLockOnStateChanged | C | - | gotoAndPlay(r1) | mc_missileWarningVictimBrackets |
| NotifyNormalizedDownedHealthChanged | C | - | - | mc_incapacitatedScreen{thisElement 0.1s easeout {_alpha: prcnt}; thisElement 0.1s easeout {_alpha: 100}; incapWidgets_mc 0.5s easeout {_alpha: 100}; gotoAndPlay(1)} |
| NotifyOnAttackingTeamChanged | C | - | RewardAnnouncement: reward_mc 0.4s easeout {_y: 18, _alpha: 100} | - |
| NotifyOverShieldChanged | C | - | healthNumber_txt 0.5s easeout {color: 16777215}; healthNumber_txt 0.5s easeout {color: 9105663}; gotoAndPlay(loop), gotoAndStop(1) | - |
| NotifyPlayerRotationChanged | C | - | - | - |
| NotifyProgressBarChanged | C | - | thisElement 0.5s easeout {_y: -140, _alpha: 100}; thisElement 0.5s easeout {_y: -120, _alpha: 0} | - |
| NotifyScoringMultiplierChanged | C | PICKUP_DMG_MULTIPLIER, PICKUP_DMG_MULTIPLIER_DECREASE | thisElement 0.4s easeout {color: _global.GetPointMultiplierColor(), _yscale: 100, _xsc}; thisElement 0.8s easeout {color: _global.GetPointMultiplierColor(), _yscale: 100, _xsc} | - |
| NotifySegmentedHealthChanged | C | - | gotoAndPlay(loop), gotoAndStop(1) | mc_vitalBarActiveBarDrained{thisElement 0.2s easeout {_width: drainedBarEndWidth, _x: drainedBarEndX}; thisElement 0.5s easeout {callback: thisElement.removeMe, _width: 0}}, mc_vitalBarHealthSegment{thisElement 0.5s easeout {color: SegmentColor, _yscale: 100}; highlight_mc 0.2s easeout {_alpha: (100 / segmentIndex)}; bar_mc 0.2s easeout {_alpha: 90}} |
| NotifySpectating | C | - | - | - |
| NotifyTargetHealthChanged | C | - | thisClip 0.1s linear {color: healthColor} | - |
| NotifyTargetNameChanged | C | - | - | - |
| NotifyTargetTypeChanged | C | - | crosshairAnchor_mc 0.2s easeout {color: r1} | - |
| NotifyTutorialMessage | C | - | - | mc_tutorialMessage{_parent.MinimizedTutorialQueue[i] 0.5s easeout {_y: (midRightCoord.y + (i * 25))}; thisElement 0.5s easeout {callback: removeMe, _y: (thisElement._y - 40), _alpha: 0}; thisElement 0.5s easeout {_y: (midRightCoord.y + (_parent.MinimizedTutorialQueue.lengt}; gotoAndPlay(minimize)} |
| NotifyWeaponClipAmmoChanged | C | - | AmmoBarClip 0.2s easeout {_yscale: 100, color: BarColor}; updateStatus: AmmoBarClip 0.5s easeout {color: BarColor}; updateStatus: ammoNumber_txt 0.5s easeout {color: 16724787}; updateStatus: ammoNumber_txt 0.5s easeout {color: 16777215}; updateStatus: currentWeapon_mc.iconAnchor_mc 0.5s easeout {color: 16724787}; updateStatus: currentWeapon_mc.iconAnchor_mc 0.5s easeout {color: 16769331} …(+2); gotoAndPlay(loop), gotoAndStop(1) | mc_ammoBar{bar_mc 0.2s easeout {_width: r2}; highlight_mc 0.2s easeout {_alpha: r1, _width: r3}}, mc_vitalBarAmmoSegment |
| NotifyWeaponJammedChanged | C | - | - | - |
| NotifyWeaponMessageChanged | C | - | gotoAndPlay(charging), gotoAndPlay(ready) | mc_chargingIndicator |
| NotifyWeaponReserveAmmoChanged | C | - | thisElement 0.5s easeout {_alpha: 0}; thisElement 0.5s easeout {_alpha: 100}; updateStatus: AmmoBarClip 0.5s easeout {color: BarColor}; updateStatus: ammoNumber_txt 0.5s easeout {color: 16724787}; updateStatus: ammoNumber_txt 0.5s easeout {color: 16777215}; updateStatus: currentWeapon_mc.iconAnchor_mc 0.5s easeout {color: 16724787} …(+3); gotoAndPlay(loop), gotoAndStop(1) | - |
| NotifyWeaponSpreadChanged | C | - | - | - |
| PointEvent | C | MP_REWARD_DIALOG_BOX | - | mc_pointTransaction{snd MP_REWARD_DIALOG_BOX; points_mc 0.5s easeout {_yscale: 100, _xscale: 100}; points_mc 1s easeout {_y: (this._y - 100)}; this 1s easeout {callback: removeMe, _alpha: 0}} |
| ReapplyBuff | - | - | - | - |
| RewardAnnouncement | C | - | reward_mc 0.4s easeout {_y: 18, _alpha: 100} | - |
| SetWeaponCrosshair | - | - | CrosshairClip 0.3s easeout {_rotation: 0} | - |
| ShowAbilityType0 | - | - | thisClip 0.5s easeout {_alpha: 100}; thisClip 0.5s easeout {_alpha: 0} | - |
| ShowAbilityType1 | - | - | thisClip 0.5s easeout {_alpha: 100}; thisClip 0.5s easeout {_alpha: 0} | - |
| ShowAbilityType2 | - | - | thisClip 0.5s easeout {_alpha: 100}; thisClip 0.5s easeout {_alpha: 0} | - |
| ShowCrosshair | C | - | - | - |
| ShowGrenades | - | - | thisElement 0.2s easeout {_alpha: 100}; thisElement 0.2s easeout {_alpha: 0} | - |
| StartMarkerUpdate | C | - | - | - |
| ToggleSpectatorHudMode | - | - | - | - |
| TransformDisrupted | C | - | DisruptedClip 0.2s easeout {_alpha: 100} | mc_transformDisrupt |
| UnapplyBuff | C | - | - | - |
| UnapplyKillstreakBuff | - | - | KillstreakBuffs[i] 0.3s easeout {_y: (i * IconSpacing)} | - |
| UpdateAbilityCooldown | - | - | - | - |
| UpdateMarker | C | - | addMarker: r1 1s easeout {_alpha: 100}; trackOffScreen: r1 1s easeout {_alpha: 100} | - |
| displayReloadPrompt | - | - | - | - |
| hideScope | - | - | thisElement.zoomScope_mc 0.5s easeout {callback: thisElement.removeScope, _alpha: 0}; _root.hud_mc.topLeft_mc 0.5s linear {_alpha: 100}; _root.hud_mc.topCenter_mc 0.5s linear {_alpha: 100}; _root.hud_mc.topRight_mc 0.5s linear {_alpha: 100}; _root.hud_mc.midLeft_mc 0.5s linear {_alpha: 100}; _root.hud_mc.midRight_mc 0.5s linear {_alpha: 100} …(+3) | - |
| showScope | - | - | thisElement.zoomScope_mc 0.2s linear {_alpha: 100}; _root.hud_mc.topLeft_mc 0.2s linear {_alpha: 0}; _root.hud_mc.topCenter_mc 0.2s linear {_alpha: 0}; _root.hud_mc.topRight_mc 0.2s linear {_alpha: 0}; _root.hud_mc.midLeft_mc 0.2s linear {_alpha: 0}; _root.hud_mc.midRight_mc 0.2s linear {_alpha: 0} …(+3) | mc_zoomScope |
| updateAmmoWarning | - | - | - | - |

### PlayerList_GFX.gfx (2 entry points)

| Entry point | Ours | Sounds | Animation (interp: target time easing {props}) / timeline | Spawned symbols / timers / engine calls |
|---|---|---|---|---|
| GivePlayerListInput | - | - | - | - |
| UpdatePlayerListData | C | - | BuildPlayerList: r2 0.4s easeout {_y: ListElementPosition} | - |

### MultiplayerRespawn_GFX.gfx (1 entry points)

| Entry point | Ours | Sounds | Animation (interp: target time easing {props}) / timeline | Spawned symbols / timers / engine calls |
|---|---|---|---|---|
| SetSpectateTarget | - | - | currentlySpectating_mc 0.5s easeout {_alpha: 100}; currentlySpectating_mc 0.5s easeout {_alpha: 0} | - |

### ChallengeNotify_GFX.gfx (1 entry points)

| Entry point | Ours | Sounds | Animation (interp: target time easing {props}) / timeline | Spawned symbols / timers / engine calls |
|---|---|---|---|---|
| ChallengeUnlocked | C | - | - | mc_notifyChallenge{thisElement 0.5s easeout {callback: closeMovie, _y: 20, _alpha: 0}; content_mc 0.2s easeout {_alpha: 100}; ChallengeIconClip 0.5s easeout {_yscale: 60, _xscale: 60, _alpha: 100}} |

### PauseMenu_GFX.gfx (1 entry points)

| Entry point | Ours | Sounds | Animation (interp: target time easing {props}) / timeline | Spawned symbols / timers / engine calls |
|---|---|---|---|---|
| DisplayCharacterSelect | - | - | - | - |
