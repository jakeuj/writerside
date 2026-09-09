# 最新文章

<web-summary>依發布日期瀏覽 Jakeuj 的近期技術文章，涵蓋雲端、開發工具與實作排錯筆記。</web-summary>

這裡收錄已整理發布日期的文章，尚未涵蓋全部歷史文章；其他筆記可從左側分類瀏覽。

[訂閱新文章 RSS](https://jakeuj.com/feed.xml) · [返回首頁](Default.md)

## 2026 {#year-2026-1}

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

- [35B 級距 Coding Agent 模型比較：Ornith-1.0、Qwen3.6、Gemma 4](ornith-qwen-gemma-35b-model-comparison.md) — 2026-07-01

  比較 Ornith-1.0-35B、Qwen3.6-35B 與 Gemma 4 31B 在 coding agent benchmark 與企業內部 MIS 場景的選型差異。

## 2026（續 1） {#year-2026-2}

- [Apple Silicon Mac 用 Docker 跑 SQL Server 2025 避開 AVX crash](sql-server-2025-docker-apple-silicon.md) — 2026-07-01

  Apple Silicon Mac 使用 Docker Desktop 跑 SQL Server 2025 時，如果遇到 AVX assertion crash，優先改用固定 SQL Server 2025 CU tag、開啟 Rosetta amd64 emulation，並避免吃到舊的 2025-latest cache。

- [GGUF、半精度、模型蒸餾與 Q4_K_M 筆記](gguf_fp16_distill_q4km_notes.md) — 2026-06-12

  理解 GGUF、FP16/BF16、Distill 與 Q4_K_M 的差異，判斷本地 LLM 下載時該選半精度、蒸餾模型或量化格式。

- [llama.cpp、Ollama、LM Studio、vLLM](llm_local_serving_comparison_notes_zh-TW.md) — 2026-06-12

  比較 llama.cpp、Ollama、LM Studio 與 vLLM 的定位、模型格式、部署場景與企業內部 LLM serving 選型建議。

- [Ollama DiffusionGemma](ollama_diffusiongemma_notes_2026-06-12.md) — 2026-06-12

  判斷 DiffusionGemma 目前是否適合用 Ollama 執行，並比較 vLLM、llama.cpp DiffusionGemma 分支與 GGUF CLI 的可行路線。

- [bizhub C651i Mac 印表機驅動安裝說明](bizhub-c651i-macos-driver-install.md) — 2026-06-11

  在 macOS 安裝 KONICA MINOLTA bizhub C651i 印表機驅動，並用固定 IP、IPP 佇列與 C651i PS driver 重新加入印表機。

- [ABP 分離 Auth/API 專案部署到 Azure 與 Akamai 檢查表](abp-azure-akamai-deployment-checklist.md) — 2026-06-10

  ABP 分離式 Auth/API 專案部署到 Azure App Service 並經 Akamai 對外服務時，用這份檢查表對齊 hostname、TLS/SNI、OpenIddict redirect URI、SelfUrl 與前端 OIDC 設定。

- [Akamai Forward Host Header 對 App Service redirect 與 cookie 的影響](akamai-origin-host-header-app-service.md) — 2026-06-10

  釐清 Akamai Forward Host Header 如何影響 App Service 登入轉址、cookie 與公開網域設定。

- [macOS SSH 連線遇到 hostname 無法解析時，用 mDNS 或 hosts 處理](macos-mdns-ssh-hostname-resolution.md) — 2026-05-29

  排查 macOS SSH 主機名稱無法解析問題，依情境使用 mDNS 的 .local 名稱或 hosts 固定別名。

- [Azure App Service VNet Integration 連 Azure SQL Managed Instance Private Endpoint 的 DNS 筆記](azure-app-service-sql-mi-private-dns.md) — 2026-04-30

  設定 App Service 連線 Azure SQL Managed Instance Private Endpoint 所需的私人 DNS，並驗證名稱解析。

- [Azure App Service VNet Integration 後如何查內網 IP](azure-app-service-vnet-private-ip.md) — 2026-04-30

  使用 WEBSITE_PRIVATE_IP 查詢 App Service VNet Integration 的出站內網 IP，分辨與 Private Endpoint 入站位址的差異。
