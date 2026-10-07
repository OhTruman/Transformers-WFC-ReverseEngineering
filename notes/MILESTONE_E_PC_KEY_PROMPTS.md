# PC keyboard prompt text vs pad glyphs (Milestone E, 2026-10-07)

Labels: C = from 360 script / config / Hud AS; H = high confidence; U = unknown. **Our dump is the Xbox 360 SKU.** The PC executable and the PC input ini (`DefaultInput.ini` / PC `TransInput.ini` with keyboard bindings) are **not** available. Only the PC localisation files `TransGame_PC.int` / `UIText_PC.int` are present (shipped inside the 360 coalesced data).

## Mechanism (C, `TransGame.TnInputCommandToBindingMapper`)
- Text with input tokens uses **`^COMMAND`** tokens, e.g. "^THROW_GRENADE", in localised strings.
- `TranslateCommandsInString(PC, S)`:
  - `ExtractInputCommandsInString` splits on `^` and takes the token up to a space / comma / period;
  - each token is looked up in `InputCommandToKeyBindings` (config, `Xe-TransInput.ini`: 46 entries `(InputCommand="^X", Key="XboxTypeS_…", KeyAlt=…)`);
  - `InputCommandToKeyBindingRemappedBasedControllerProfile`: profile `UseAlternateControlScheme` → `KeyAlt` if set; `SwitchRightThumbstickAndB` swaps XboxTypeS_B ↔ XboxTypeS_RightThumbstick;
  - `FindKeyToActionScriptBinding(Key)` looks up **`KeyToActionScriptBindings`** (localised, section `[TnInputCommandToBindingMapper]`) and replaces the `^COMMAND` token with its `ActionScript` string;
  - **if the key has no KeyToActionScriptBinding, the token is left untouched (the raw "^COMMAND" stays in the text)**.
- **360:** `TransGame.int` maps `XboxTypeS_A` → "{a}", B → "{b}", … (14 entries). The movie's `TextField.setImageSubstitutions(buttonIconArray)` turns those into Gamepad* glyph images.
- **PC (H, inferred from the data):** UE3 loads platform-suffixed localisation, so `TransGame_PC.int` overrides the same section with **19 entries whose ActionScript is orange HTML text** (`<font color='#FF9333'>Q</font>`, "W, S, A, D", "Mouse", "Left Mouse Button", …). Its Key strings ("Q", "Move", "Turn", "MouseWheel/PageUp/PageDown", "BarrelRollDirection", …) must equal the `Key` values of the **PC** `InputCommandToKeyBindings` (the comment says "must match … DefaultInput.ini"), which we don't have (U).
  - So on PC the same `^COMMAND` → key → ActionScript path yields HTML text instead of `{a}`.
  - **No device switching:** nothing in script queries the last input device or offers a keyboard / pad prompt option; `KeyToActionScriptBindings` is a static localised array. H: the PC SKU always showed keyboard text (pad glyph switching U, not evidenced).
- **Callers (C):**
  - `TnHudDataObserverContextualCommands` → HUD contextual commands (`Movie.Invoke(CallbackBindingName, [0, action, text])`);
  - `TnTutorialMessageDisplayer` (tutorial / hint messages);
  - `TnXpEventTypeKillStreak` (kill-streak reward description).
  - Nothing else in script.
- **Not covered by the mapper (C, Hud AS):** several HUD widgets contain hard-coded glyph tokens with their own `buttonIconArray` (`{B}`, `{X}`, `{LT}`, `{dleft}`; text from UIText / AS). The ability label is chosen by `HmUtility.Platform`: XBOX360 "LB", PS3 "L2", other (PC) "".
  - U: how PC handled these hard-coded `{B}` / `{X}` widgets and the menu button bars. H: separate PC SWF / UIText_PC changes not in this dump; `UIText_PC.int` here contains only texture-restart prompts.
- **Refresh:** none event-driven. The translation happens when each string is produced (per notification / tutorial / kill-streak event).
