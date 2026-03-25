# Windows 11 啟用 Native NVMe

這篇筆記的重點不是討論新聞本身，而是整理截至 2026 年 3 月 25 日，Windows 11 上已知還能怎麼啟用 Native NVMe、哪些舊方法已失效，以及啟用後要怎麼驗證與回退。

## 先講結論

如果你只是想知道現在該用哪一招：

- Windows Server 2025 的官方啟用方式是 registry key，但那是 Server 功能，不是 Windows 11 正式支援路徑。
- Windows 11 24H2、25H2 上先前流傳的 registry override，依 2026 年 3 月 23 日 Tom's Hardware 整理，已經在最近的 Insider builds 失效。
- 目前社群仍有一條可行 workaround，是用 ViVeTool 啟用 feature IDs `60786016` 與 `48433719`，但同樣屬於非官方支援作法。

<warning>

以下做法不屬於 Microsoft 正式支援的 Windows 11 啟用流程。已知風險包含 BitLocker recovery prompt、備份軟體偵測異常，以及 Samsung Magician、WD Dashboard 這類 SSD 工具相容性問題。請只在測試機或可承受回退的環境操作。

</warning>

## 啟用前先確認

先確認這幾件事，再去碰 Native NVMe：

1. 先備份重要資料，並確認 BitLocker Recovery Key 已保存。
2. 目前系統碟或測試碟最好是使用 Windows 內建 NVMe driver，也就是 `StorNVMe.sys` 路線。
3. 如果你有使用備份代理、磁碟監控或 SSD 原廠管理工具，先記錄現在是否能正常辨識磁碟。

可以先做這兩個檢查：

```powershell
manage-bde -status
driverquery /v | findstr /i "stornvme nvmedisk"
```

## 如何在 Windows 11 啟用 Native NVMe

目前比較值得寫進筆記的，不是舊 registry hack，而是 ViVeTool workaround。

1. 從 ViVeTool 的 GitHub Releases 下載最新版本，解壓縮到本機。
2. 用系統管理員身分開啟 Terminal、PowerShell 或命令提示字元。
3. 切換到 ViVeTool 所在目錄。
4. 執行以下指令啟用兩個 Native NVMe 相關 feature IDs。
5. 重新開機。

```powershell
.\ViVeTool.exe /enable /id:60786016,48433719
```

<note>

上面的指令是根據 Tom's Hardware 在 2026 年 3 月 23 日文章中列出的 feature IDs，搭配 ViVeTool 一般使用語法整理而成。如果 ViVeTool 日後變更參數格式，請以官方 GitHub release 說明為準。

</note>

## 啟用後怎麼驗證 {#verify-native-nvme}

最重要的是不要只看「有沒有開成功」，還要看「有沒有真的切到對的 driver path」。

可以用這幾種方式交叉檢查：

1. 先跑 `driverquery /v | findstr /i "stornvme nvmedisk"`，確認系統中能看到 `nvmedisk`。
2. 到裝置管理員的磁碟機裝置，打開目標 SSD 的內容，檢查 Driver Details 是否已經看到 `nvmedisk.sys`。
3. 用同一套 benchmark 做前後對照，重點看 4K random read、4K random write 和 latency，不要只看 sequential throughput。

常用快速檢查：

```powershell
driverquery /v | findstr /i "stornvme nvmedisk"
```

## 如何回退 {#rollback-native-nvme}

如果啟用後出現 BitLocker 提示、備份工具看不到磁碟，或 SSD 原廠工具開始異常，先回退再說。

```powershell
.\ViVeTool.exe /disable /id:60786016,48433719
```

執行完後重新開機，再確認：

1. BitLocker 保護狀態是否恢復正常。
2. 備份軟體能否重新辨識系統碟與資料碟。
3. SSD 原廠工具是否恢復正常。

## 為什麼不建議再追舊 registry hack

很多舊文還在寫 registry，是因為一開始這波 Native NVMe 消息，確實是從 Windows Server 2025 的官方 registry key 延伸出來的。

但現在要分清楚兩件事：

- Microsoft 在 2025 年 12 月 15 日公開的是 Windows Server 2025 的官方 opt-in 啟用方式。
- Tom's Hardware 在 2026 年 3 月 23 日整理到的，是 Windows 11 最近 Insider builds 已經讓舊 registry override 不再生效。

所以如果你現在是要寫「Windows 11 怎麼開」，就不該把 Server 的正式 registry key 直接當成 Windows 11 標準做法。

## 我會怎麼建議

如果你是一般桌機、筆電或遊戲機使用者，我會把這件事當成「可以觀察、可以測，但還不適合當成日常預設設定」。

如果你是測試機、lab 或非關鍵工作站，則可以依上面的 ViVeTool 步驟試，但要先接受這幾件事：

- 不是每顆 SSD 都會有同樣幅度的提升。
- random I/O 通常比 sequential throughput 更容易看到差異。
- 相容性風險目前比操作本身更值得擔心。

## 參考資料

- [Neowin: Report: Microsoft quietly blocks Windows 11 25H2/24H2 performance boost hack for SSDs](https://www.neowin.net/news/report-microsoft-quietly-blocks-windows-11-25h2-24h2-performance-boost-hack-for-ssds/)
- [Microsoft Community Hub: Announcing Native NVMe in Windows Server 2025](https://techcommunity.microsoft.com/blog/windowsservernewsandbestpractices/announcing-native-nvme-in-windows-server-2025-ushering-in-a-new-era-of-storage-p/4477353)
- [Tom's Hardware: Microsoft blocks registry trick that unlocked performance-boosting native NVMe driver on Windows 11](https://www.tomshardware.com/software/windows/microsoft-blocks-the-registry-hack-trick-that-unlocked-native-nvme-performance-on-windows-11)
- [Tom's Hardware: Registry hack enables new performance-boosting native NVMe support on Windows 11](https://www.tomshardware.com/software/windows/registry-hack-enables-new-performance-boosting-native-nvme-support-on-windows-11-windows-server-2025-feature-can-be-unlocked-for-consumer-pcs-but-at-your-own-risk)
- [StorageReview: Windows Server 2025 Native NVMe: Storage Stack Overhaul and Benchmark Results](https://www.storagereview.com/review/windows-server-native-nvme)
- [ViVeTool Releases](https://github.com/thebookisclosed/ViVe/releases)
