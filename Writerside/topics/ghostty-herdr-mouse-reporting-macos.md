# Ghostty 搭配 Herdr：macOS 滑鼠點擊、選字與安裝設定

<web-summary>在 macOS 使用 Ghostty 執行 Herdr 時，保留 mouse reporting 即可點擊 pane、tab、Space 與 Agent，並用 Shift 拖曳切換成終端機原生選字。</web-summary>

Ghostty 很適合執行 Herdr，但解決「滑鼠只能選字、不能點 TUI」的關鍵不是更換終端機，而是讓外層終端機保留 mouse reporting。Ghostty 預設已開啟此功能；安裝穩定版後先維持零設定，通常就能直接操作 Herdr。

<tldr>
<p>Ghostty 的 <code>mouse-reporting</code> 與 Herdr 的 <code>ui.mouse_capture</code> 都要保持開啟。</p>
<p>一般點擊交給 Herdr；想用 Ghostty 原生選字時，按住 Shift 再拖曳。</p>
<p>剪貼簿允許提示只控制 clipboard，不等於 mouse reporting。</p>
</tldr>

## 問題症狀

在 Herdr 畫面中，滑鼠拖曳可以反白並複製文字，但無法完成下列操作：

- 切換 tab
- 選擇 Space 或 Agent
- 聚焦不同 pane
- 拖曳 pane 分隔線
- 開啟 Herdr 的右鍵選單

這通常代表外層終端機攔下滑鼠，把它當成文字選取工具，而沒有把 click、drag 或 scroll event 傳給 Herdr。

## 根本原因：滑鼠事件有兩層開關

Herdr 的滑鼠介面必須同時通過兩層設定：

1. **Ghostty** 必須允許終端程式要求 mouse reporting。對應設定是 `mouse-reporting = true`，而且預設就是 `true`。
2. **Herdr** 必須擷取滑鼠輸入。對應設定是 `ui.mouse_capture = true`，預設也是 `true`。

只要 Ghostty 設成 `mouse-reporting = false`，Herdr 就收不到點擊。此時畫面仍會正常繪製，但滑鼠只剩終端機自己的選字與複製行為。

## 安裝 Ghostty {#install-ghostty}

Ghostty 官方提供 Apple Silicon 與 Intel 都能使用的 Universal Binary。Ghostty 1.3.1 需要 macOS 13 Ventura 以上。

### 官方 DMG

從 [Ghostty 官方下載頁](https://ghostty.org/download) 下載 macOS Universal Binary，開啟 DMG 後把 Ghostty 拖進 Applications。官方文件說明此版本已由 Ghostty 專案簽署並公證。

### Homebrew

也可以安裝 Homebrew cask：

```bash
brew install --cask ghostty
```

Homebrew cask 由社群維護，但封裝的是 Ghostty 官方 DMG。若安裝後 macOS 報告簽章異常，先不要自行移除 quarantine 或重新簽章；改用官方 DMG 重新安裝，並用 Gatekeeper 驗證來源。

```bash
codesign --verify --deep --strict --verbose=2 /Applications/Ghostty.app
spctl --assess --type execute --verbose=2 /Applications/Ghostty.app
```

正常結果應包含 `valid on disk` 與 `source=Notarized Developer ID`。

## 建議先維持零設定

Ghostty 主打開箱即用，Herdr 需要的 mouse reporting 預設已經開啟。第一次使用時，先不要搬入整套 iTerm2 設定，也不必急著建立 Ghostty 設定檔。

如果想明確固定滑鼠行為，可以在 Ghostty 設定加入：

```text
mouse-reporting = true
mouse-shift-capture = never
```

`mouse-shift-capture = never` 會永久保留 Shift 加滑鼠給 Ghostty 原生選取，不讓 TUI 改寫這個行為。

macOS 可使用下列任一設定檔位置：

- `~/.config/ghostty/config.ghostty`
- `~/Library/Application Support/com.mitchellh.ghostty/config.ghostty`

按 <shortcut>Cmd+Shift+,</shortcut> 可以重新載入設定；部分設定仍需要完全重開 Ghostty。

## 在 Herdr 裡怎麼點擊與選字 {#use-mouse-in-herdr}

一般滑鼠點擊會傳給 Herdr，可以用來選擇 pane、tab、Space 與 Agent。這是 Herdr 預期的 mouse-native 操作方式。

想暫時繞過 Herdr、改用 Ghostty 選字時：

1. 按住 Shift。
2. 用滑鼠拖曳要複製的文字。
3. 放開滑鼠完成選取。

Ghostty 的 `copy-on-select` 與 mouse reporting 是不同設定：

- `mouse-reporting` 決定滑鼠事件是否送進 Herdr。
- `copy-on-select` 決定 Ghostty 完成原生選取後是否自動複製。
- Herdr 自己也有 `ui.copy_on_select`，處理 Herdr 擷取滑鼠時的 pane 選取。

因此，看到剪貼簿讀取或寫入提示時，不要把「永久允許 clipboard」誤認為啟用 TUI 點擊；兩者是獨立功能。

## 安裝後驗證

<procedure>
<step>
<p>開啟 Ghostty，在 shell 執行 <code>herdr</code>。</p>
</step>
<step>
<p>依序點擊 pane、tab、Space 與 Agent，確認焦點會跟著移動。</p>
</step>
<step>
<p>如果有 split pane，拖曳分隔線確認 Herdr 能調整大小。</p>
</step>
<step>
<p>按住 Shift 拖曳一段文字，確認 Ghostty 原生選字正常。</p>
</step>
<step>
<p>如果點擊仍只會選字，檢查 Ghostty 是否設了 <code>mouse-reporting = false</code>，以及 Herdr 是否設了 <code>ui.mouse_capture = false</code>。</p>
</step>
</procedure>

## 仍然不能點擊時

### 檢查 Ghostty readonly 狀態

Ghostty 的 `toggle_readonly` 會停止把鍵盤與滑鼠送進 PTY，但仍允許捲動、選取與複製。如果鍵盤輸入和 Herdr 點擊同時失效，卻還能反白文字，要檢查是否誤觸 readonly action。

### 檢查 Ghostty 設定 {#check-ghostty-settings}

執行下列指令可以查看目前生效的設定：

```bash
/Applications/Ghostty.app/Contents/MacOS/ghostty +show-config
```

如果輸出包含：

```text
mouse-reporting = false
```

請移除這一行，或改成 `true`，再完全關閉並重新開啟 Ghostty。官方文件特別註明，在 macOS 變更此設定後需要完整重啟 Ghostty。

### 檢查 Herdr 設定 {#check-herdr-settings}

Herdr 的預設值原本就能使用滑鼠。如果設定檔有以下內容：

```toml
[ui]
mouse_capture = false
```

請移除這項覆寫，或改成：

```toml
[ui]
mouse_capture = true
```

接著在 Herdr 按預設快捷鍵 <shortcut>Ctrl+B</shortcut>，放開後再按 <shortcut>Shift+R</shortcut> 重新載入設定。

## Ghostty 與 iTerm2 怎麼選

| 項目 | Ghostty | iTerm2 |
|------|---------|--------|
| Herdr 滑鼠點擊 | 預設可用 | 開啟 mouse reporting 後可用 |
| 暫時原生選字 | Shift 加拖曳 | Option 加拖曳 |
| 設定方式 | 目前以文字設定檔為主 | 完整 GUI 與 Profiles |
| 滑鼠細部控制 | 總開關加 Shift policy | 可分開控制 wheel、click 與 drag |
| 介面與渲染 | macOS 原生 UI、Metal | 成熟且高度客製化 |

兩者都能正確執行 Herdr。只為修復「只能選字、不能點」時，重新開啟 iTerm2 mouse reporting 就足夠；如果也想要較精簡的原生介面、GPU 加速與較少的初始設定，Ghostty 值得嘗試。

## SSH 與遠端主機注意事項

Ghostty 使用 `TERM=xterm-ghostty`。較舊的遠端主機若沒有對應 terminfo，可能出現 `unknown terminal type` 或 `terminal is not fully functional`。

遇到這類錯誤時，優先使用 Ghostty 提供的 SSH 整合：

```bash
ghostty +ssh example-host
```

也可以參考官方 [Terminfo 說明](https://ghostty.org/docs/help/terminfo)，把必要的 terminfo 安裝到遠端主機。不要直接把 `TERM` 永久硬改成不相符的值，否則其他 TUI 功能可能顯示錯誤。

## 版本提醒

Ghostty 1.3.0 曾在 macOS 發生切換焦點後的 phantom mouse event，可能造成幽靈拖曳、選取或捲動。官方已在 1.3.1 修正，因此應使用 1.3.1 或更新的 stable 版本，不要為了測試滑鼠問題退回 1.3.0。

## 參考資料

- [Ghostty Download](https://ghostty.org/download)
- [Ghostty Binaries and Packages](https://ghostty.org/docs/install/binary)
- [Ghostty Configuration](https://ghostty.org/docs/config)
- [Ghostty Option Reference：mouse-reporting](https://ghostty.org/docs/config/reference#mouse-reporting)
- [Ghostty 1.3.1 Release Notes](https://ghostty.org/docs/install/release-notes/1-3-1)
- [Ghostty Terminfo Help](https://ghostty.org/docs/help/terminfo)
- [Herdr Quick Start](https://herdr.dev/docs/quick-start/)
- [Herdr Config Reference](https://herdr.dev/docs/config-reference/)
- [Herdr Keyboard](https://herdr.dev/docs/keyboard/)
- [iTerm2 Terminal Profile Preferences](https://iterm2.com/documentation-preferences-profiles-terminal.html)
