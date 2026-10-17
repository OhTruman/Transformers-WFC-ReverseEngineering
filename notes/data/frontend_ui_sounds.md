| UI cue | Ours | Movies | Where (function@sprite, first 4) |
|---|---|---|---|
| BUTTON_ACCEPT | C | Brightness, CampaignGameOver, CampaignSelect, ChallengeMenu, CharacterSelect, CustomTransformers, DifficultySelect, ExtrasMenu, FrontEnd, MessagePrompt, PauseMenu, PlayerList, SettingsMenu, SharedComponents, TextPrompt | <anon>@63; inputEvent@130; inputEvent@16; inputEvent@17 |
| BUTTON_BACK | C | Brightness, CampaignGameOver, CampaignSelect, ChallengeMenu, CharacterSelect, CustomTransformers, DifficultySelect, EndGameStats, ExtrasMenu, FrontEnd, MessagePrompt, PauseMenu, PlayerList, SettingsMenu, SharedComponents, TextPrompt | closeEndGameStats@None; inputEvent@130; inputEvent@17; inputEvent@173 |
| BUTTON_DOWN | C | Brightness, CampaignGameOver, CampaignSelect, ChallengeMenu, CharacterSelect, CustomTransformers, DifficultySelect, ExtrasMenu, FrontEnd, MessagePrompt, PauseMenu, PlayerList, SettingsMenu, SharedComponents, TextPrompt | <anon>@59; findDirectionalFocus@130; findDirectionalFocus@17; findDirectionalFocus@173 |
| BUTTON_START | C | FrontEnd | inputEvent@23 |
| BUTTON_UP | C | Brightness, CampaignGameOver, CampaignSelect, ChallengeMenu, CharacterSelect, CustomTransformers, DifficultySelect, ExtrasMenu, FrontEnd, MessagePrompt, PauseMenu, PlayerList, SettingsMenu, SharedComponents, TextPrompt | <anon>@59; customInputEvent@99; findDirectionalFocus@130; findDirectionalFocus@17 |

| Movie | Transition interps (open / close / show / hide / focus …) |
|---|---|
| FrontEnd_GFX | - |
| CampaignSelect_GFX | UpdateSelectorState: background_mc 0.5s easeout {callback: thisClip.assignSelectorFocus, _height: r}; UpdateSelectorState: frameBottom_mc 0.5s easeout {_y: (r1 / 2)}; UpdateSelectorState: frameTop_mc 0.5s easeout {_y: (r1 / -2)}; factionSelected: autobotBG_mc 0.5s easeout {_alpha: 0}; factionSelected: autobot_mc 0.5s easeout {_alpha: 0}; factionSelected: currentFocus 0.5s easeout {_yscale: 360, _xscale: 360, _alpha: 10, _x: -240}; factionSelected: currentFocus.glow_mc 0.5s easeout {_alpha: 0}; factionSelected: currentFocus.name_txt 0.5s easeout {_alpha: 0} |
| CharacterSelect_GFX | - |
| CustomTransformers_GFX | closeMenu: _parent.footer_mc.customizeButtonHints_mc 0.2s easeout {_alpha: 100}; closeMenu: _parent.header_mc 0.2s easeout {_alpha: 100}; occluderClose: topMenuElements[r3] 0.2s easeout {_alpha: 100}; onClick: topMenuElements[r3] 0.2s easeout {_alpha: 0}; setTabColor: tab_mc 0.2s easeout {color: parseInt(tabColor)}; shiftCenter: charLevel_txt 0.2s easeout {color: 9105663}; shiftCenter: thisClip 0.4s easeout {callback: thisClip.expandMenu, _y: _parent.overvie}; showCountdown: thisClip 0.5s easeout {_alpha: 0, _y: (InitPositionY + 10)} |
| DifficultySelect_GFX | - |
| ExtrasMenu_GFX | selectionUpdated: ConceptButtonArray[r2] 2s easeout {_alpha: 50}; selectionUpdated: ConceptImageClip 0.4s easeout {_alpha: 100, _x: 0}; selectionUpdated: centerFooter_mc 2s easeout {_alpha: 100}; selectionUpdated: leftArrow_mc 0.5s easeout {_alpha: 0}; selectionUpdated: r3 0.4s easeout {callback: r3.removeMe, _alpha: 0, _x: -50}; selectionUpdated: r3 0.4s easeout {callback: r3.removeMe, _alpha: 0, _x: 50}; selectionUpdated: rightArrow_mc 0.5s easeout {_alpha: 0} |
| SettingsMenu_GFX | closeMenu: _backMenuRef 0.2s easeout {_alpha: 100}; selectCloseMenu: _backMenuRef 0.2s easeout {_alpha: 100}; selectionUpdated: this 0.2s easeout {_y: (0 - this.currentFocus._y)} |
| PauseMenu_GFX | closeMenu: _root.bg2_mc 1s easeout {_alpha: 0}; selectionUpdated: this 0.2s easeout {_y: (0 - this.currentFocus._y)} |
| ChallengeMenu_GFX | - |
| Brightness_GFX | - |
| MessagePrompt_GFX | - |
| TextPrompt_GFX | - |
| SharedComponents_GFX | currentSelectionChanged: arrowLeft_mc 0.2s easeout {color: 16777215, _alpha: 100}; currentSelectionChanged: arrowLeft_mc 0.2s easeout {color: 5289429, _alpha: 50}; currentSelectionChanged: arrowLeft_mc 0.5s easeout {color: 5289429, _alpha: 25}; currentSelectionChanged: arrowRight_mc 0.2s easeout {color: 16777215, _alpha: 100}; currentSelectionChanged: arrowRight_mc 0.2s easeout {color: 5289429, _alpha: 50}; currentSelectionChanged: arrowRight_mc 0.5s easeout {color: 5289429, _alpha: 25}; currentSelectionChanged: seperator_mc.arrowLeft_mc 0.2s easeout {color: 16777215, _alpha: 100}; currentSelectionChanged: seperator_mc.arrowLeft_mc 0.3s easeout {color: 16777215, _alpha: 25} |
| EndGameStats_GFX | showXpTotal: xpBar_mc.xpEarned_mc 0.4s easeout {_alpha: 0, _yscale: 0}; showXpTotal: xpBar_mc.xpEarned_mc 0.4s easeout {_alpha: 100, _yscale: 100}; showXpTotal: xpBar_mc.xpToNextLevel_mc 0.4s easeout {_alpha: 0, _yscale: 0}; showXpTotal: xpBar_mc.xpToNextLevel_mc 0.4s easeout {_alpha: 100, _yscale: 100} |
| PlayerList_GFX | - |
| CampaignGameOver_GFX | - |
