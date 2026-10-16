# Jakeuj 筆記本

<web-summary>Jakeuj 筆記本整理 .NET、ABP、Azure、GCP、Docker、AI 工具、macOS 與開發環境疑難排解，提供可公開查閱的實作筆記與排錯紀錄。</web-summary>

Jakeuj 筆記本整理 .NET、ABP、Azure、GCP、Docker、AI 工具、macOS 與開發環境疑難排解筆記，作為日常實作與問題追蹤的公開知識庫。

[訂閱新文章 RSS](https://jakeuj.com/feed.xml)

<!-- publications:start -->

## 最新文章

- [Wi-Fi 7 路由器單房間升級：1G 光世代該買哪一台](wifi-7-router-single-room-upgrade.md) — 2026-10-16

  從 Wi-Fi 6 路由器升級 Wi-Fi 7 時，單房間搭配 1G 光世代的效益來自 6GHz 而不是網速；只挑含 6GHz 的三頻機，不必追 10G 網路孔或 320MHz，並附 2026-10 原價屋與 PChome 價格比較，以及 PS5 Pro、Quest 3 的頻段設定。

- [領取 Claude Max 與 Team 方案每月免費 API 額度](claude-max-team-monthly-api-credits.md) — 2026-10-13

  說明 Claude Max 5x、Max 20x 與 Team 方案每月附贈的 Claude Platform API 額度金額、資格、如何把 claude.ai 帳號連結到 Console 組織完成領取，以及自動儲值與額度不累積等注意事項。

- [Azure CLI az login 訂閱選擇器：觸發條件、關閉方式與快速登入](azure-cli-login-subscription-selector.md) — 2026-10-12

  Azure CLI az login 出現 Announcements 與訂閱選擇器時，依互動登入、TTY 與 core.login_experience_v2 判斷觸發條件，並用 --subscription、--skip-subscription-discovery 或關閉設定讓登入更快、腳本不卡住。

- [C# 狀態機、狀態模式與策略模式：差異與選擇](csharp-state-machine-state-pattern.md) — 2026-10-07

  以同一套 C# 訂單規則比較 switch、轉移表與 State Pattern，說明狀態機和策略模式的差異，並依行為複雜度、轉移規則及共存效果選擇設計。

- [Evennia 中文指令解析與 CmdSet 實作](evennia-chinese-commands-cmdsets.md) — 2026-10-07

  在 Evennia 6.1 實作繁體中文玩家指令，用 arg_regex 決定空格與緊密式輸入，並以 CmdSet 的 priority、Union 與持久化設定處理指令覆寫及暫時互動。

- [Evennia 時間與狀態更新機制怎麼選](evennia-time-state-updates.md) — 2026-10-07

  在 Evennia 6.1 依玩法選擇時間戳、delay、Script、TickerHandler 或 OnDemandHandler，用冷卻、延後通知、天氣與植物生長範例說明持久化、停止訂閱和伺服器停機時間的差異。

- [用 graphify 把 repo 做成知識圖，發布到 GitHub Pages](graphify-knowledge-graph-github-pages.md) — 2026-10-07

  用 graphify 把 repo 的程式、文件與截圖整理成可互動的知識圖，補上 viewport、noindex 與返回連結後發布到 GitHub Pages；附建圖 token 成本實測、增量更新做法，以及 AST 與 LLM 節點 ID 對不上的修法。

- [Unity IL2CPP iOS IPA 研究筆記：從 Mach-O、runtime resolver 到 pre-sign hook](ios-unity-il2cpp-ipa-research-notes.md) — 2026-10-07

  在 Apple Silicon Mac 研究 Unity IL2CPP iOS IPA 時，從 Mach-O、cryptid 與 runtime IL2CPP API 建立版本鎖定 registry，辨識既有 relay patch，並用 Mac-first A/B 測試與 pre-sign hook 釐清 iOS code signing 問題。

- [Unity 回合制戰鬥核心設計：狀態機、技能、Buff 與單例](unity-turn-based-battle-core.md) — 2026-10-07

  Unity 手遊同時只有一場玩家戰鬥時，單例可以合理代表目前戰鬥；透過狀態機安排時序、技能公式重用運算、Buff 集合保存效果，並以獨立情境測試保護已運作的規則。

- [聖火降魔錄 萬縷千絲（萬紫千紅）培養計算器：成長率公式與坐騎加成](fire-emblem-fortunes-weave-growth-calculator.md) — 2026-10-06

  《聖火降魔錄 萬縷千絲》（萬紫千紅）的角色成長是個人、職業與坐騎成長率逐級擲骰，職業補正只在當下職業生效；從遊戲內目前的等級、職業與實際能力值出發預測轉職路線，並整理凱伊篇坐騎與戰車兵的成長加成規則。

[查看所有近期文章](recent-posts.md)

## 精選文章

- [DataGrip 連線 Azure SQL：Microsoft Entra Default 驗證 20 秒逾時排錯](datagrip-azure-sql-entra-auth-timeout.md) — 2026-08-17

  DataGrip 使用 Microsoft Entra ID Default 連線 Azure SQL 出現 switchIfEmpty 20 秒逾時時，可從 macOS GUI PATH 與 Azure CLI 自動更新輸出污染快速定位並修復。

- [Apple Silicon Mac 跑本地 LLM 時，MLX、Ollama、LM Studio、oMLX 怎麼選](apple-silicon-mlx-local-llm-tools.md) — 2026-07-01

  Apple Silicon Mac 跑本地 LLM 或 VLM 時，先分清楚 MLX、mlx-lm、mlx-vlm、oMLX、LM Studio、Ollama 與 GGUF 的定位，再依聊天、Hugging Face MLX 模型、coding agent 或跨平台部署選工具。

- [Apple Silicon Mac 用 Docker 跑 SQL Server 2025 避開 AVX crash](sql-server-2025-docker-apple-silicon.md) — 2026-07-01

  Apple Silicon Mac 使用 Docker Desktop 跑 SQL Server 2025 時，如果遇到 AVX assertion crash，優先改用固定 SQL Server 2025 CU tag、開啟 Rosetta amd64 emulation，並避免吃到舊的 2025-latest cache。

## 主題入口

- [.NET／C#](C-Sharp.md)
- [ABP](ABP.md)
- [Azure](Azure.md)
- [Docker](Docker.md)
- [AI／LLM](LLM.md)
- [macOS：開發環境設定](macOS_dotfiles_guide.md)

## 重大更新

- [Evennia 開發 MUD 遊戲起手筆記](evennia-mud-development.md) — 2026-10-07

  更新 Evennia 6.1.0 與 Python 版本依據、中文文件範圍，補上 uv lock 專案與套件升級流程，串接中文指令及時間狀態實作筆記。

- [ROG Astral LC RTX 5090 冷排風扇不亮、不轉：磁吸接頭暫時恢復後復發](rog-astral-lc-rtx5090-fan-connector.md) — 2026-10-07

  冷排風扇再次停止；壓回磁吸接頭只暫時恢復。補上 Fan 2 為 88% 卻回報 0 RPM 的負載讀值與相似論壇案例，狀態改為已復發、待檢修。

<!-- publications:end -->

## 關於 Jakeuj

我在這裡分享開發工具、雲端服務與日常實作的技術筆記。

- [作品與開源專案](Side-Projects.md)
- [相關連結](links.md)
- [渥吉遊戲股份有限公司(67038125)](https://www.twfile.com/item.aspx?no=67038125#:~:text=10609-,%E8%91%A3%E4%BA%8B%E9%95%B7%20%E6%9C%B1%E7%AB%8B%E6%81%86){ignore-vars="true"}
- 用 [Writerside](https://www.jetbrains.com/writerside/) 取代 [點部落](https://www.dotblogs.com.tw/jakeuj/)
- [抖內](https://www.paypal.com/ncp/payment/PLYGLLUS2Z8VS)
- [贊助](https://paypal.me/jakeuj)
