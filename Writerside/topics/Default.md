# Jakeuj 筆記本

<web-summary>Jakeuj 筆記本整理 .NET、ABP、Azure、GCP、Docker、AI 工具、macOS 與開發環境疑難排解，提供可公開查閱的實作筆記與排錯紀錄。</web-summary>

Jakeuj 筆記本整理 .NET、ABP、Azure、GCP、Docker、AI 工具、macOS 與開發環境疑難排解筆記，作為日常實作與問題追蹤的公開知識庫。

[訂閱新文章 RSS](https://jakeuj.com/feed.xml)

<!-- publications:start -->

## 最新文章

- [用 GitHub Actions 自動發布 Chrome 與 Edge 擴充套件到商店](chrome-edge-extension-cd-github-actions.md) — 2026-09-14

  瀏覽器擴充套件打 tag 後由 GitHub Actions 打包 zip、建 GitHub Release，並用 Edge Add-ons Publish API v1.1 與 Chrome Web Store API v2 自動上傳送審；本文整理憑證申請、workflow 寫法與常見坑。

- [DataGrip 連線 Azure SQL：Microsoft Entra Default 驗證 20 秒逾時排錯](datagrip-azure-sql-entra-auth-timeout.md) — 2026-08-17

  DataGrip 使用 Microsoft Entra ID Default 連線 Azure SQL 出現 switchIfEmpty 20 秒逾時時，可從 macOS GUI PATH 與 Azure CLI 自動更新輸出污染快速定位並修復。

- [Azure App Service Private Endpoint：Web、API、Auth 的 Split-horizon DNS](azure-app-service-split-horizon-dns.md) — 2026-08-07

  Azure App Service Web、API、Auth 以 Private Endpoint 與 Private DNS Zone 實作 Split-horizon DNS，讓外部經 WAF、內部沿用相同 FQDN 走私網。

- [使用 ipatool 下載、解壓與驗證 App Store IPA](app-store-ipa-ipatool-download-extract.md) — 2026-08-05

  在 macOS 使用 ipatool 從 App Store 下載官方加密 IPA，透過 unzip 指定解壓路徑，並檢查版本、簽章 metadata 與 Mach-O cryptid。

- [在 macOS CrossOver 的 Guild Wars 2 啟用 arcdps](crossover-guild-wars-2-arcdps.md) — 2026-07-15

  在 macOS 使用 CrossOver 執行 Guild Wars 2 時，除了把 arcdps 的 d3d11.dll 放到遊戲目錄，還要在 Wine 設定加入 Native then Builtin DLL override 才能正常載入。

- [oMLX Ornith-1.0-35B-8bit 給 Codex 使用的設定紀錄](omlx-ornith-codex-settings.md) — 2026-07-08

  整理在 MacBook Pro M4 Max 128 GB 上用 oMLX 執行 Ornith-1.0-35B-8bit 給 Codex 使用時，context window、thinking、reasoning parser、Responses API、model catalog 與 CC Switch 遠端壓縮的已知問題與建議設定。

- [Codex Plugin 建立指南](codex-plugin-build-guide.md) — 2026-07-02

  從零開始建立一個 Codex plugin：了解 repo 結構、plugin.json、agents/openai.yaml、skills、MCP、apps、hooks 與 marketplace 的完整工作流程。

- [在 oMLX 設定 Claude Code Desktop 與 CLI 使用本地模型](omlx-claude-code-desktop-setup.md) — 2026-07-02

  說明如何在 oMLX 設定 claude-\* 模型別名，讓 Claude Code Desktop 與 Claude Code CLI 直接連線到本地 macOS Apple Silicon 上運行的 Claude 系列模型，包含 API 連線設定、環境變數與 cc-switch 模型切換工具。

- [Apple Silicon Mac 跑本地 LLM 時，MLX、Ollama、LM Studio、oMLX 怎麼選](apple-silicon-mlx-local-llm-tools.md) — 2026-07-01

  Apple Silicon Mac 跑本地 LLM 或 VLM 時，先分清楚 MLX、mlx-lm、mlx-vlm、oMLX、LM Studio、Ollama 與 GGUF 的定位，再依聊天、Hugging Face MLX 模型、coding agent 或跨平台部署選工具。

- [Codex App 搭配 oMLX 伺服器運行 Qwen3.6 35B 設定筆記](codex-app-omlx-qwen3-6-setup.md) — 2026-07-01

  說明如何在本機利用 oMLX 伺服器提供 Qwen3.6 35B 模型給 Codex App 使用，包含 sampling 設定、認證機制與模型目錄的對應關係。

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

<!-- publications:end -->

## 關於 Jakeuj

我在這裡分享開發工具、雲端服務與日常實作的技術筆記。

- [作品與開源專案](Side-Projects.md)
- [相關連結](links.md)
- [渥吉遊戲股份有限公司(67038125)](https://www.twfile.com/item.aspx?no=67038125#:~:text=10609-,%E8%91%A3%E4%BA%8B%E9%95%B7%20%E6%9C%B1%E7%AB%8B%E6%81%86){ignore-vars="true"}
- 用 [Writerside](https://www.jetbrains.com/writerside/) 取代 [點部落](https://www.dotblogs.com.tw/jakeuj/)
- [抖內](https://www.paypal.com/ncp/payment/PLYGLLUS2Z8VS)
- [贊助](https://paypal.me/jakeuj)
