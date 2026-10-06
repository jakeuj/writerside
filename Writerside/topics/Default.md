# Jakeuj 筆記本

<web-summary>Jakeuj 筆記本整理 .NET、ABP、Azure、GCP、Docker、AI 工具、macOS 與開發環境疑難排解，提供可公開查閱的實作筆記與排錯紀錄。</web-summary>

Jakeuj 筆記本整理 .NET、ABP、Azure、GCP、Docker、AI 工具、macOS 與開發環境疑難排解筆記，作為日常實作與問題追蹤的公開知識庫。

[訂閱新文章 RSS](https://jakeuj.com/feed.xml)

<!-- publications:start -->

## 最新文章

- [聖火降魔錄 萬縷千絲（萬紫千紅）培養計算器：成長率公式與坐騎加成](fire-emblem-fortunes-weave-growth-calculator.md) — 2026-10-06

  《聖火降魔錄 萬縷千絲》（萬紫千紅）的角色成長是個人、職業與坐騎成長率逐級擲骰，職業補正只在當下職業生效；從遊戲內目前的等級、職業與實際能力值出發預測轉職路線，並整理凱伊篇坐騎與戰車兵的成長加成規則。

- [FramePack Windows 一鍵包支援 RTX 5090：升級 PyTorch cu128 與 SageAttention](framepack-rtx-5090-windows.md) — 2026-10-06

  FramePack Windows 一鍵包內建 torch 2.6.0+cu126，在 RTX 5090 等 Blackwell（sm_120）顯卡會出現 no kernel image 錯誤；用一鍵包內建 Python 升級到 torch 2.10.0+cu128，再加裝 triton-windows 與 SageAttention 即可正常生成並加速。

- [Gradio 在 Windows 反覆出現 WinError 10022 的原因與修正](gradio-asyncio-winerror-10022.md) — 2026-10-06

  在 Windows 用 Python 3.10 執行 Gradio（例如 FramePack）時，console 反覆出現 _call_connection_lost 的 OSError WinError 10022；這是 asyncio Proactor 在連線已斷開後呼叫 shutdown 失敗，可以用 sitecustomize.py 只包住這個呼叫來修正。

- [ROG Astral LC RTX 5090 冷排風扇不亮、不轉：磁吸接頭暫時恢復後復發](rog-astral-lc-rtx5090-fan-connector.md) — 2026-10-06

  ROG Astral LC RTX 5090 冷排風扇壓回磁吸接頭後僅暫時恢復，過一陣子又停止；負載截圖顯示 Fan 2 為 88% 卻是 0 RPM。此個案已復發，需檢查接頭固定、線組與風扇模組。

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
