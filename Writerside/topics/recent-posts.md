# 最新文章

<web-summary>依發布日期瀏覽 Jakeuj 的近期技術文章，涵蓋雲端、開發工具與實作排錯筆記。</web-summary>

這裡收錄已整理發布日期的文章，尚未涵蓋全部歷史文章；其他筆記可從左側分類瀏覽。

[訂閱新文章 RSS](https://jakeuj.com/feed.xml) · [返回首頁](Default.md)

## 2026 {#year-2026-1}

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

- [FramePack Windows 一鍵包支援 RTX 5090：升級 PyTorch cu128 與 SageAttention](framepack-rtx-5090-windows.md) — 2026-10-06

  FramePack Windows 一鍵包內建 torch 2.6.0+cu126，在 RTX 5090 等 Blackwell（sm_120）顯卡會出現 no kernel image 錯誤；用一鍵包內建 Python 升級到 torch 2.10.0+cu128，再加裝 triton-windows 與 SageAttention 即可正常生成並加速。

- [Gradio 在 Windows 反覆出現 WinError 10022 的原因與修正](gradio-asyncio-winerror-10022.md) — 2026-10-06

  在 Windows 用 Python 3.10 執行 Gradio（例如 FramePack）時，console 反覆出現 _call_connection_lost 的 OSError WinError 10022；這是 asyncio Proactor 在連線已斷開後呼叫 shutdown 失敗，可以用 sitecustomize.py 只包住這個呼叫來修正。

- [ROG Astral LC RTX 5090 冷排風扇不亮、不轉：磁吸接頭暫時恢復後復發](rog-astral-lc-rtx5090-fan-connector.md) — 2026-10-06

  ROG Astral LC RTX 5090 冷排風扇壓回磁吸接頭後僅暫時恢復，過一陣子又停止；負載截圖顯示 Fan 2 為 88% 卻是 0 RPM。此個案已復發，需檢查接頭固定、線組與風扇模組。

## 2026（續 1） {#year-2026-2}

- [Ghostty 搭配 Herdr：macOS 滑鼠點擊、選字與安裝設定](ghostty-herdr-mouse-reporting-macos.md) — 2026-09-17

  在 macOS 使用 Ghostty 執行 Herdr 時，保留 mouse reporting 即可點擊 pane、tab、Space 與 Agent，並用 Shift 拖曳切換成終端機原生選字。

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

## 2026（續 2） {#year-2026-3}

- [Codex App 搭配 oMLX 伺服器運行 Qwen3.6 35B 設定筆記](codex-app-omlx-qwen3-6-setup.md) — 2026-07-01

  說明如何在本機利用 oMLX 伺服器提供 Qwen3.6 35B 模型給 Codex App 使用，包含 sampling 設定、認證機制與模型目錄的對應關係。

- [35B 級距 Coding Agent 模型比較：Ornith-1.0、Qwen3.6、Gemma 4](ornith-qwen-gemma-35b-model-comparison.md) — 2026-07-01

  比較 Ornith-1.0-35B、Qwen3.6-35B 與 Gemma 4 31B 在 coding agent benchmark 與企業內部 MIS 場景的選型差異。

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

## 2026（續 3） {#year-2026-4}

- [Azure App Service VNet Integration 連 Azure SQL Managed Instance Private Endpoint 的 DNS 筆記](azure-app-service-sql-mi-private-dns.md) — 2026-04-30

  設定 App Service 連線 Azure SQL Managed Instance Private Endpoint 所需的私人 DNS，並驗證名稱解析。

- [Azure App Service VNet Integration 後如何查內網 IP](azure-app-service-vnet-private-ip.md) — 2026-04-30

  使用 WEBSITE_PRIVATE_IP 查詢 App Service VNet Integration 的出站內網 IP，分辨與 Private Endpoint 入站位址的差異。

- [Evennia 開發 MUD 遊戲起手筆記](evennia-mud-development.md) — 2026-04-20

  用 Python 3.14 與 uv 建立 Evennia 6.1 遊戲專案，完成初始化、資料庫 migration 與第一個繁體中文指令，並理解 game dir、CmdSets、Typeclasses 與持久化資料的分工。
