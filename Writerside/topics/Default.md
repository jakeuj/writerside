# Jakeuj 筆記本

<web-summary>Jakeuj 筆記本整理 .NET、ABP、Azure、GCP、Docker、AI 工具、macOS 與開發環境疑難排解，提供可公開查閱的實作筆記與排錯紀錄。</web-summary>

Jakeuj 筆記本整理 .NET、ABP、Azure、GCP、Docker、AI 工具、macOS 與開發環境疑難排解筆記，作為日常實作與問題追蹤的公開知識庫。

[訂閱新文章 RSS](https://jakeuj.com/feed.xml)

<!-- publications:start -->

## 最新文章

- [GitHub Projects 草稿不顯示：用 gh 查證與原地轉成 Issue](github-projects-draft-issue-not-visible.md) — 2026-10-23

  GitHub Projects 清單為空但草稿仍能依 ID 讀取時，先排除篩選與封存，再用 gh 原地轉換單張 Draft issue，分別驗證資料、清單與畫面，避免重複新增。

- [AdGuard 不過濾 localhost：User rules 的 $document 例外規則（Mac／Windows）](adguard-localhost-allowlist.md) — 2026-10-22

  在 AdGuard 的 User rules 加入 @@||localhost^$document、@@||127.0.0.1^$document，Windows 再補 @@|http://127.0.0.1:$document，讓本機開發網站在任何 port 都不被封鎖、隱藏元素或改寫 HTML。

- [Azure SQL 稽核寫不進儲存體：金鑰重新產生後要重新儲存稽核設定](azure-sql-auditing-storage-key-rotation.md) — 2026-10-22

  Azure SQL 稽核告警顯示無法寫入儲存體帳戶時，用 Azure CLI 比對稽核驗證方式與儲存體金鑰建立時間找出原因，重新儲存稽核設定並關閉重複的資料庫層稽核。

- [SQL Server OPTION (HASH JOIN)：用途、執行計畫與效能驗證](sql-server-option-hash-join.md) — 2026-10-20

  說明 SQL Server OPTION (HASH JOIN) 的作用範圍、與 INNER HASH JOIN 的差異，並用虛構圖書借閱範例，示範如何從實際執行計畫確認重複掃描、記憶體與查詢耗時。

- [線上課程背景播放 JavaScript：套用、還原與計時驗證](elearning-progress-api-visibility.md) — 2026-10-19

  保留可直接複製的線上課程背景播放 JavaScript，暫時停用 CourseReader 的頁面可見性處理與定期回應確認，附執行條件、還原指令，以及 API 回存和伺服器時數認列的驗證限制。

- [Wi-Fi 7 路由器單房間升級：1G 光世代該買哪一台](wifi-7-router-single-room-upgrade.md) — 2026-10-16

  單房間搭配 1G 光世代，升級 Wi-Fi 7 優先看 6GHz 與裝置能力；比較台灣三頻路由器價格、Wi-Fi 8 草案產品與等待價值，整理 Quest 3 無線 PC VR、頻段分配及 RT-AX82U 的 AiMesh 接線。

- [領取 Claude Max 與 Team 方案每月免費 API 額度](claude-max-team-monthly-api-credits.md) — 2026-10-13

  說明 Claude Max 5x、Max 20x 與 Team 方案每月附贈的 Claude Platform API 額度金額、資格、如何把 claude.ai 帳號連結到 Console 組織完成領取，以及自動儲值與額度不累積等注意事項。

- [Azure CLI az login 訂閱選擇器：觸發條件、關閉方式與快速登入](azure-cli-login-subscription-selector.md) — 2026-10-12

  Azure CLI az login 出現 Announcements 與訂閱選擇器時，依互動登入、TTY 與 core.login_experience_v2 判斷觸發條件，並用 --subscription、--skip-subscription-discovery 或關閉設定讓登入更快、腳本不卡住。

- [C# 狀態機、狀態模式與策略模式：差異與選擇](csharp-state-machine-state-pattern.md) — 2026-10-07

  以同一套 C# 訂單規則比較 switch、轉移表與 State Pattern，說明狀態機和策略模式的差異，並依行為複雜度、轉移規則及共存效果選擇設計。

- [Evennia 中文指令解析與 CmdSet 實作](evennia-chinese-commands-cmdsets.md) — 2026-10-07

  在 Evennia 6.1 實作繁體中文玩家指令，用 arg_regex 決定空格與緊密式輸入，並以 CmdSet 的 priority、Union 與持久化設定處理指令覆寫及暫時互動。

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

- [AdGuard 不過濾 localhost：User rules 的 $document 例外規則（Mac／Windows）](adguard-localhost-allowlist.md) — 2026-10-24

  補上 AdGuard for Windows 實測：||127.0.0.1^ 的 $document 例外擋不住 HTML 改寫，改加 |http://127.0.0.1: 前綴規則後所有 port 才恢復原檔；新增改寫偵測與 PWA 雜湊失敗症狀。

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
