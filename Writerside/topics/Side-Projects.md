# Side Projects

<web-summary>精選 Jakeuj 近期維護並已公開發布的 side projects 與開源貢獻，涵蓋 Guild Wars 2 Nexus addon、Path of Exile 瀏覽器擴充、Codex plugins、遊戲攻略、MUD 保存與 oMLX。</web-summary>

這裡精選我近期維護或具有代表性的 side projects，包含自有作品、社群在地化與可驗證的開源貢獻。資料更新日期為 2026-08-20；完整清單請見 [GitHub repositories](https://github.com/jakeuj?tab=repositories)。

> 精選名單以目前仍在維護、具備可使用成果，或能清楚說明貢獻內容的專案為主，不是所有公開 repository 的自動鏡像。

## 近期主力專案

### Upgrade Value

已通過 Raidcore 初始審查並公開列於 Nexus Addon Library（ID 128）的 Guild Wars 2 addon。它透過官方 API 掃描帳號內裝備的符文與法印，比較 Trading Post 即時價格並提供拆解建議；目前穩定版為 `v1.0.5`，支援英文與繁體中文，可直接從 Nexus 遊戲內的 Addon Library 安裝。

- 連結：[GitHub](https://github.com/jakeuj/GW2-Nexus-Upgrade-Value)｜[專案網站](https://gw2-value.jakeuj.com/)｜[Nexus Addon Library](https://raidcore.gg/gw2/addons/upgrade-value)｜[穩定版 v1.0.5](https://github.com/jakeuj/GW2-Nexus-Upgrade-Value/releases/tag/v1.0.5)
- 語言與技術：`C++` `GW2 Nexus` `GW2 API` `GitHub Actions`

![GW2-Nexus-Upgrade-Value last commit](https://img.shields.io/github/last-commit/jakeuj/GW2-Nexus-Upgrade-Value)

### PoE Ninja to Chronicles PoB Sharer

支援 Path of Exile 1 與 2 的瀏覽器擴充功能，可在 poe.ninja 角色頁面一鍵讀取 PoB、上傳至編年史、開啟中文 PoB 頁面，並將分享連結複製至剪貼簿。

- 發布狀態：截至 2026-08-20，[Chrome Web Store](https://chromewebstore.google.com/detail/poe-ninja-to-chronicles-p/aidenhnleibhchnhilkpbpkgeanmeedh?hl=zh-TW) 約有 1,000 位使用者、5.0 評分（2 則評分），目前版本為 `1.2.1`
- 連結：[GitHub](https://github.com/jakeuj/ChromeExtensionPobZh)｜[產品網站](https://poe.jakeuj.com/)｜[Chrome Web Store](https://chromewebstore.google.com/detail/poe-ninja-to-chronicles-p/aidenhnleibhchnhilkpbpkgeanmeedh?hl=zh-TW)｜[Microsoft Edge Add-ons](https://microsoftedge.microsoft.com/addons/detail/ilpjikgeonkegldnjdgpmcdiibmlabng)｜[v1.2.1 release](https://github.com/jakeuj/ChromeExtensionPobZh/releases/tag/v1.2.1)
- 語言與技術：`JavaScript` `Manifest V3` `Chrome Extension` `Edge Extension` `GitHub Actions`

![ChromeExtensionPobZh last commit](https://img.shields.io/github/last-commit/jakeuj/ChromeExtensionPobZh)

### CodexPlugins

供個人使用的 Codex plugin marketplace，集中管理 plugin manifest、skills、agents、commands 與相關資源，目前包含 Evennia MUD 開發技能集。

- 連結：[GitHub](https://github.com/jakeuj/CodexPlugins)
- 語言與技術：`Shell` `Codex` `Plugin` `Skill` `Evennia`

![CodexPlugins last commit](https://img.shields.io/github/last-commit/jakeuj/CodexPlugins)

### NevergrindOnline

以 Astro Starlight 建立的 Nevergrind Online 繁體中文攻略資料庫，整理攻略、職業、裝備、配方與互動式武器 DPS 計算工具。

- 連結：[GitHub](https://github.com/jakeuj/NevergrindOnline)｜[攻略網站](https://ngo.jakeuj.com/)
- 語言與技術：`Astro` `JavaScript` `MDX` `SEO` `GitHub Pages`

![NevergrindOnline last commit](https://img.shields.io/github/last-commit/jakeuj/NevergrindOnline)

### writerside

本站的 JetBrains Writerside 原始碼，包含繁體中文技術筆記、內容檢查、搜尋索引與 GitHub Pages 自動化發布流程。

- 連結：[GitHub](https://github.com/jakeuj/writerside)｜[Jakeuj's Notes](https://jakeuj.com/)
- 語言與技術：`JetBrains Writerside` `Markdown` `Docs` `CI/CD` `SEO`

![writerside last commit](https://img.shields.io/github/last-commit/jakeuj/writerside)

## 遊戲、MUD 與在地化

### gw2-pathing-zh-tw

Guild Wars 2 Blish HUD Pathing marker packs 的繁體中文在地化專案，先追蹤各 marker pack 的授權與書面許可，再進行非商業翻譯與發布。

- 連結：[GitHub](https://github.com/jakeuj/gw2-pathing-zh-tw)
- 語言與技術：`Guild Wars 2` `Blish HUD` `Pathing` `zh-TW` `License Tracking`

![gw2-pathing-zh-tw last commit](https://img.shields.io/github/last-commit/jakeuj/gw2-pathing-zh-tw)

### Community-Module-Pack

維護自 Blish HUD Community Module Pack 的 fork，加入繁體中文 Events module、遊戲術語、事件獎勵資訊、可自訂聊天訊息與 fork release 自動更新流程。

- 連結：[維護中的 fork](https://github.com/jakeuj/Community-Module-Pack)｜[upstream](https://github.com/blish-hud/Community-Module-Pack)
- 語言與技術：`C#` `Blish HUD` `Guild Wars 2` `Localization` `Release Automation`

![Community-Module-Pack last commit](https://img.shields.io/github/last-commit/jakeuj/Community-Module-Pack)

### merc-fju-3.0

以 Merc 2.2 為核心重寫「輔大三國歪傳之降龍伏虎」，延續 UTF-8 轉換成果，並整理 Docker、Apple Silicon 與現代 Linux／macOS 開發環境。

- 連結：[GitHub](https://github.com/jakeuj/merc-fju-3.0)｜[2.0 UTF-8 歷史版本](https://github.com/jakeuj/merc-fju-2.0-utf8)
- 語言與技術：`C` `MUD` `UTF-8` `Docker` `Apple Silicon`

![merc-fju-3.0 last commit](https://img.shields.io/github/last-commit/jakeuj/merc-fju-3.0)

### 3yWebsite

維護自三國歪傳網站的 fork，補上 GitHub Pages 入口、玩家指南、技能文件與可展開的知識庫內容。

- 連結：[維護中的 fork](https://github.com/jakeuj/3yWebsite)｜[upstream](https://github.com/EndeavorYen/3yWebsite)｜[文件網站](https://3y.jakeuj.com/)
- 語言與技術：`HTML` `MUD` `Documentation` `GitHub Pages`

![3yWebsite last commit](https://img.shields.io/github/last-commit/jakeuj/3yWebsite)

### rpg

使用 Flutter 與 Dart 製作的公會管理 RPG 原型，以 Clean Architecture 與 DDD 拆分冒險者、任務、裝備和公會系統。

- 連結：[GitHub](https://github.com/jakeuj/rpg)
- 語言與技術：`Dart` `Flutter` `DDD` `Clean Architecture` `Game`

![rpg last commit](https://img.shields.io/github/last-commit/jakeuj/rpg)

## 工具與應用

### pixerDotnet

以 .NET 9 重寫 Pixer 電子相框上傳工具，處理圖片縮放與灰階封裝、TCP 傳輸、裝置狀態檢查及韌體升級。

- 連結：[GitHub](https://github.com/jakeuj/pixerDotnet)｜[原始 pixer 專案](https://github.com/kasperis7/pixer)
- 語言與技術：`C#` `.NET 9` `IoT` `Image Processing` `TCP`

![pixerDotnet last commit](https://img.shields.io/github/last-commit/jakeuj/pixerDotnet)

### poe_production_Config

提供 Path of Exile 與 Path of Exile 2 在 Apple Silicon Mac 執行 Windows client 時使用的 DirectX 12 設定檔範本。

- 連結：[GitHub](https://github.com/jakeuj/poe_production_Config)｜[設定檔網站](https://poe-mac.jakeuj.com/)
- 語言與技術：`Path of Exile` `macOS` `Apple Silicon` `DirectX 12` `Configuration`

![poe_production_Config last commit](https://img.shields.io/github/last-commit/jakeuj/poe_production_Config)

## 開源貢獻

### oMLX

為 oMLX upstream 修正記憶體限制建議與模型 profile 套用流程，兩項變更均於 2026-08-18 合併：

- [PR #2799](https://github.com/jundot/omlx/pull/2799)：將 wired-memory 建議值統一為核心可接受的整數 MiB，避免前後端產生無法滿足的警告循環。
- [PR #2806](https://github.com/jundot/omlx/pull/2806)：解決 VLM-MTP profile 套用衝突、保留有效設定，並以 HTTP 400 回傳剩餘的驗證錯誤，避免部分寫入。
- 連結：[upstream](https://github.com/jundot/omlx)｜[個人 fork](https://github.com/jakeuj/omlx)
- 語言與技術：`Python` `JavaScript` `MLX` `Profile Validation` `Web Dashboard`

### GW2-ArcDPS-TChineseUI

維護自 GW2 ArcDPS 繁體中文介面的 fork，補上設定保存、啟動與 hook lifecycle 修正、建置發布流程，以及網站與安裝文件。

- 連結：[維護中的 fork](https://github.com/jakeuj/GW2-ArcDPS-TChineseUI)｜[upstream](https://github.com/m21248074/GW2-ArcDPS-TChineseUI)｜[專案網站](https://gw2.jakeuj.com/)
- 語言與技術：`C++` `Guild Wars 2` `ArcDPS` `Traditional Chinese` `CI/CD`

![GW2-ArcDPS-TChineseUI last commit](https://img.shields.io/github/last-commit/jakeuj/GW2-ArcDPS-TChineseUI)

### Nexus-Translations 繁體中文翻譯

透過 PR #48 為 Raidcore Nexus 初次加入繁體中文語系；後續 PR #49 依目前的簡體中文資源重新產生翻譯，使用 OpenCC `s2twp` 轉換台灣用字，並保留所有 localization keys、placeholders 與控制字元。PR #49 已合併並取代 #48 的版本。

- 連結：[初始 PR #48](https://github.com/RaidcoreGG/Nexus-Translations/pull/48)｜[更新 PR #49](https://github.com/RaidcoreGG/Nexus-Translations/pull/49)｜[upstream](https://github.com/RaidcoreGG/Nexus-Translations)｜[個人 fork](https://github.com/jakeuj/Nexus-Translations)
- 語言與技術：`Guild Wars 2` `Nexus` `Localization` `Traditional Chinese` `OpenCC`

![Nexus-Translations last commit](https://img.shields.io/github/last-commit/jakeuj/Nexus-Translations)

### LibGGPK3

維護自 LibGGPK3 的 fork，持續改善 Path of Exile Content.ggpk library 的相容性、效能與工具使用體驗，並將變更回饋 upstream。

- 連結：[維護中的 fork](https://github.com/jakeuj/LibGGPK3)｜[upstream](https://github.com/aianlinb/LibGGPK3)｜[upstream PR #50](https://github.com/aianlinb/LibGGPK3/pull/50)
- 語言與技術：`C#` `.NET` `Path of Exile` `Parser` `Library`

![LibGGPK3 last commit](https://img.shields.io/github/last-commit/jakeuj/LibGGPK3)

## 其他專案索引

以下保留過往自有專案與曾維護 fork 的快速入口；最新狀態與完整清單仍以 GitHub 為準。

- **MUD 與遊戲**：[JakeMud](https://github.com/jakeuj/JakeMud)、[JakeMudDotNet](https://github.com/jakeuj/JakeMudDotNet)、[JakeujMud](https://github.com/jakeuj/JakeujMud)、[MyKirito](https://github.com/jakeuj/MyKirito)
- **.NET 與 ABP**：[Microsoft.Extensions.Logging.Log4Net](https://github.com/jakeuj/Microsoft.Extensions.Logging.Log4Net)、[AbpAzureSample](https://github.com/jakeuj/AbpAzureSample)、[abp-console-samples](https://github.com/jakeuj/abp-console-samples)、[BlazorOnGitHubPages](https://github.com/jakeuj/BlazorOnGitHubPages)、[PowerShellNetCoreQueue](https://github.com/jakeuj/PowerShellNetCoreQueue)、[MyAbpProject](https://github.com/jakeuj/MyAbpProject)、[LINQPad-Queries](https://github.com/jakeuj/LINQPad-Queries)、[Drone](https://github.com/jakeuj/Drone)
- **Web、DevOps 與實驗工具**：[DockerSys](https://github.com/jakeuj/DockerSys)、[AiPlaform](https://github.com/jakeuj/AiPlaform)、[TestDocker](https://github.com/jakeuj/TestDocker)、[electron](https://github.com/jakeuj/electron)、[edge-extension](https://github.com/jakeuj/edge-extension)
- **曾維護的 fork**：[pixer](https://github.com/jakeuj/pixer)、[FramePack](https://github.com/jakeuj/FramePack)

## 合作與交流

如果你對任何專案有建議，歡迎在對應 repository 開 Issue 或 Pull Request。也可以直接瀏覽 [jakeuj 的 GitHub repositories](https://github.com/jakeuj?tab=repositories) 查看完整清單與最新提交。
