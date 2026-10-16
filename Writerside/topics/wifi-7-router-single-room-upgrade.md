# Wi-Fi 7 路由器單房間升級：1G 光世代該買哪一台

<web-summary>單房間搭配 1G 光世代，升級 Wi-Fi 7 優先看 6GHz 與裝置能力；比較 2026-10 台灣三頻路由器價格，整理 Quest 3 無線 PC VR、PS5 Pro 頻段分配，以及 ASUS RT-AX82U 的 AiMesh 接線與限制。</web-summary>

單房間、1G 光世代的情況下，換 Wi-Fi 7 不會提高申辦方案的速率上限，主要升級價值是讓相容裝置改走 6GHz、分散頻段負載。因此，這套設備優先挑**含 6GHz 的三頻機**，不必為目前用不到的 10G 網路孔或 320MHz 多付錢。2026-10-16 查價時，CP 值最高的是原價屋的 TP-Link Archer BE550（5,599 元）；想繼續用 ASUS 管理介面並保留舊 RT-AX82U 作 AiMesh 節點，就選 RT-BE92U（7,699 元）。實際速度與穩定性仍須依房間內的訊號、干擾與裝置連線確認。

<tldr>
<p>以 Quest 3 無線 PC VR 與 6GHz 分流為目標時，優先選三頻機；雙頻 Wi-Fi 7 無法替 Wi-Fi 6E 裝置增加 6GHz。</p>
<p>Mac 是否支援 Wi-Fi 7：看 system_profiler SPAirPortDataType 的 Supported PHY Modes 有沒有 be。</p>
<p>Quest 3 找不到 6GHz：6GHz 頻寬設 160MHz 以下並開啟 PSC，仍不行再改 802.11ax only。</p>
</tldr>

本文情境：原本使用 ASUS RT-AX82U（Wi-Fi 6，5GHz 為 4x4、160MHz，網路孔全部是 Gigabit），只在約 15 坪的單一房間使用，網路是 1G 光世代，沒有 NAS。PC 用 Cat 7 接有線，PS5 Pro、Quest 3、手機與筆電走無線。

![單房間 PC VR 情境：PC 以網路線連接架上的路由器，Quest 3 在同房間透過無線連線接收串流](wifi-7-single-room-pcvr.png){thumbnail="true" width="900"}

AI 生成情境示意：PC 與路由器之間走有線，頭盔與路由器之間走無線；設備外觀與藍色波紋不代表特定產品或實測覆蓋範圍。

## 換機會改善什麼 {#what-improves}

| 項目 | 換 Wi-Fi 7 三頻機之後 |
| --- | --- |
| 對外網速 | 申辦方案仍是 1G。單一 1GbE 連線常見 TCP 實效約 940 Mbps；這是連接埠與協定開銷，不能當成所有 1G 光世代接法的固定上限 |
| 有線裝置 | PC 接 2.5G LAN 可提高內網連線速率，但需另一端與傳輸路徑也支援；對外仍受方案、路由器處理能力與服務端限制 |
| 無線裝置 | 支援 6GHz 的裝置可增加一個分流頻段；Wi-Fi 7 裝置能否使用 MLO，還須看終端、韌體與設定 |
| 覆蓋範圍 | 6GHz 穿牆較差；單房間也應避開櫃體、牆壁與人體遮擋，不能保證一定比原本快或穩 |

判斷方式：

- **主要裝置都接有線：** 可以不換，把錢省下來。
- **有支援 6GHz 的 PS5 Pro、VR 頭盔、手機或筆電走無線：** 若原本 5GHz 擁擠，或需要持續串流 PC VR，含 6GHz 的三頻機更值得考慮。

## 先查裝置支援什麼 {#client-capabilities}

| 裝置 | Wi-Fi | 最高頻寬 | 有線 | 換機後 |
| --- | --- | --- | --- | --- |
| PC（ASUS X870 MAX GAMING WIFI7 W） | Wi-Fi 7，2x2，含 6GHz | 160MHz | 2.5G | 可接新路由器的 2.5G LAN；完整 Wi-Fi 7 功能需要 Windows 11 24H2 以上 |
| PS5 Pro | Wi-Fi 7（含 6GHz） | 官方未公開 | 1G | 走無線時可改用 6GHz 或 5GHz Wi-Fi 7 |
| iPhone 16 Pro Max | Wi-Fi 7，2x2，支援 MLO | 160MHz | 無 | 可用 6GHz 與 MLO |
| MacBook Pro（M4 Max） | Wi-Fi 6E | 160MHz | 無 | 可走 6GHz，但用不到 Wi-Fi 7 功能 |
| Meta Quest 3 | Wi-Fi 6E | 160MHz | 無 | 可走 6GHz；用 PC VR 串流時最受益 |
| Nintendo Switch 2 | Wi-Fi 6，只有 2.4／5GHz | 80MHz | 接底座 | 幾乎不變 |

PC 的 160MHz、2.5G LAN 與作業系統需求見 [ASUS 台灣主機板規格](https://www.asus.com/tw/motherboards-components/motherboards/others/x870-max-gaming-wifi7-w/techspec/)；iPhone 的 160MHz、2x2 與 MLO 見 [Apple Wi-Fi 規格](https://support.apple.com/zh-tw/guide/deployment/dep268652e6c/web)。[Meta 官方規格](https://www.meta.com/quest/quest-3/#specs)將 Quest 3 列為 Wi-Fi 6E，它可連相容的 Wi-Fi 7 路由器，但不會取得 Wi-Fi 7 的 MLO 或 320MHz 功能。

![六款現有裝置的無線規格、最高頻寬與建議連線方式資訊表，並整理 PC 有線接路由器、Quest 3 走 6GHz 的內網串流路徑](wifi-7-single-room-device-capabilities.png){thumbnail="true" width="900"}

AI 生成資訊圖：整理上表的裝置能力與連線建議；PS5 Pro 最高頻寬仍標示「官方未公開」，Quest 3 的 6GHz 可用性依地區與實際連線確認。

已確認規格的 PC、iPhone、MacBook 與 Quest 3 最高頻寬為 160MHz，Switch 2 為 80MHz；PS5 Pro 則因官方未公開，不推定是否支援 320MHz。因此，這套設備選購時不必以 320MHz 作為優先條件，BE9300 等級的三頻機已值得考慮。

在 macOS 可以直接查本機 Wi-Fi 能力與目前連線：

```bash
system_profiler SPAirPortDataType | grep -E 'Supported PHY Modes|PHY Mode:|Channel:'
```

- `Supported PHY Modes` 只到 `802.11 a/b/g/n/ac/ax`：本機是 Wi-Fi 6 或 6E，不支援 Wi-Fi 7；出現 `be` 才是 Wi-Fi 7。
- `Channel:` 顯示 `6GHz`：目前連在 6GHz。M4 世代的 Mac 仍是 Wi-Fi 6E。

## 台灣 6GHz 能用多寬 {#taiwan-6ghz}

依[數位發展部的頻段說明](https://moda.gov.tw/press/dictionary/11728)，台灣開放的 6GHz 是 5945–6425 MHz，共 480MHz；以下以室內低功率設備討論。這段頻譜可以排：

- 3 個互不重疊的 160MHz 頻道，或
- 1 個 320MHz 頻道（有兩個可選位置，但彼此重疊，同時只能用一個）

所以 Wi-Fi 7 的 320MHz 在台灣可用。只是如上一節所示，常見的手機、筆電、主機與 VR 頭盔最多只到 160MHz。

## 以 6GHz 為目標時排除雙頻機 {#avoid-dual-band}

下面這些是 Wi-Fi 7，但**沒有 6GHz**：

- ASUS RT-BE86U（BE6800，7,199 元）
- ASUS RT-BE88U（BE7200，9,999 元）
- ASUS RT-BE82U、RT-BE58U，以及各家 BE3600 系列

Mac、Quest 3 這類 Wi-Fi 6E 裝置連上雙頻 Wi-Fi 7，只能走 5GHz Wi-Fi 6，跟原本的 Wi-Fi 6 路由器差不多。RT-BE86U 的價錢和三頻的 RT-BE92U 很接近，特別容易買錯。

這項篩選限於本文的 6GHz 與無線 PC VR 需求。若主要裝置接有線，只想把舊 RT-AX82U 的 1G 埠升為 2.5G，雙頻 RT-BE82U 的 1 個 2.5G WAN 與 4 個 2.5G LAN 仍有用途；不要把「沒有 6GHz」解讀成所有升級情境都不值得。[RT-BE82U 官方規格](https://www.asus.com/tw/networking-iot-servers/wifi-routers/asus-wifi-routers/rt-be82u/techspec/)

## 候選機種與價格（2026-10-16） {#candidates}

| 型號 | 等級 | 網路孔 | 原價屋 | PChome | 說明 |
| --- | --- | --- | --- | --- | --- |
| **TP-Link Archer BE550** | BE9300 三頻 | 5×2.5G | **5,599 元** | 5,999 元 | CP 值最高；原價屋品名註明支援 320MHz、高通晶片 |
| Mercusys MR47BE | BE9300 三頻 | 4×2.5G | 4,999 元，送 1,000 酷幣 | 4,999 元 | 最便宜；管理介面較陽春 |
| TP-Link Archer BE600 | BE9700 三頻 | 1×10G＋4×2.5G | 6,999 元 | 6,999 元 | 和 RT-BE92U 同級 |
| ASUS RT-BE92U | BE9700 三頻 | 1×10G＋4×2.5G | 7,699 元（特價到 10/19） | 7,699 元 | 可沿用 ASUS 管理介面與 AiMesh |
| TP-Link Archer GE550 | BE9300 電競版 | 2×5G＋3×2.5G | 6,999 元，送 1,000 酷幣 | 6,999 元 | 1G 網路用不到 5G 網路孔 |
| ASUS TUF-BE9400 | 三頻 | 4×2.5G | 7,999 元 | 7,999 元 | 比 RT-BE92U 貴，又少了 10G 網路孔 |

![六款含 6GHz 三頻路由器的資訊比較表，列出無線等級、有線網路埠、2026 年 10 月 16 日原價屋與 PChome 價格，以及三種選購方向](wifi-7-single-room-router-comparison.png){thumbnail="true" width="900"}

AI 生成資訊圖：價格沿用上表的 2026-10-16 紀錄，酷幣未折抵表內售價；不是即時報價。

- 價格會變動，以上是 2026-10-16 兩家的報價，下單前再確認。
- 酷幣是原價屋的回饋點數，下次在原價屋消費可以折抵。
- 目前 1G 外網、2.5G PC 網卡且沒有 NAS，沒有非買 10G 埠不可的需求；價差也應一起比較 AiMesh、生態系、管理與安全功能，不能只按埠速決定。
- RT-BE92U 的 5GHz 是 2x2（2882 Mbps），帳面數字比 RT-AX82U 的 4x4（4804 Mbps）低。不過常見的手機和筆電本來就是 2x2，在同一個房間裡差異不大。

BE9700、BE9300 是各頻段理論 PHY 速率的加總，不能當成單台手機的下載速度，也不能用來判斷家中實際吞吐量。RT-BE92U 的 10G 埠只有一個：作 WAN 時，其餘有線埠各為 2.5G；若以 2.5G 埠作 WAN，則可把 10G 留給 LAN 的電腦、NAS 或交換器。10G 實體埠也不代表啟用 PPPoE、VPN 或 QoS 後必然有 10Gbps 吞吐量。[ASUS 官方規格](https://shop.asus.com/tw/90ig0950-mt1a0v-asus-rt-be92u.html)

## 頻段分配建議 {#band-plan}

| 裝置 | 建議連線方式 |
| --- | --- |
| PC | Cat 7 有線，接 2.5G 網路孔 |
| Quest 3 | 6GHz，給 6GHz 一個獨立的網路名稱 |
| PS5 Pro | 優先接有線（1G 網路孔剛好跑滿 1G 方案）；不方便拉線就連 5GHz |
| iPhone、MacBook | 6GHz 或 5GHz 都可以，用量小 |
| Switch 2 | 5GHz；放在底座時可以接有線 |

PC VR 的影音路徑是「PC → 網路線 → 路由器 → 6GHz → Quest 3」。同房間串流走內網，1G 光世代不是這段傳輸的速率上限；重點是 PC 的有線連接、頭盔的無線訊號與兩端編解碼能力。[Virtual Desktop 官方](https://www.vrdesktop.net/)也建議 PC 以網路線接路由器，並與頭盔保持在同一區網；不要把頭盔放進禁止存取內網裝置的隔離訪客網路。

6GHz 只有一個頻段，所有連上去的裝置共用頻寬。玩 VR 串流時，如果 PS5 Pro 也在 6GHz 背景下載遊戲，串流就可能卡頓，所以 6GHz 優先留給 Quest 3。

沒有 VR 頭盔、PS5 Pro 又必須走無線時，就反過來讓 PS5 Pro 固定連 6GHz 的獨立網路名稱，避免它自己跳回 5GHz。

設定頻段之外，也要確認擺位：路由器放在開放、架高且接近遊玩區的位置，讓頭盔到路由器之間盡量少有櫃體、牆壁或大型物品阻擋。

![路由器擺位比較：左圖放在開放的高處層架，右圖放在靠地面的櫃內；兩邊 PC 都以網路線連接路由器](wifi-7-single-room-router-placement.png){thumbnail="true" width="900"}

AI 生成擺位示意：左圖保留開放的無線路徑，右圖示範櫃體與低處擺放造成的遮擋；波紋不代表實測訊號強度，不能據此推算速度或延遲。

## RT-BE92U 與舊 RT-AX82U 組 AiMesh {#aimesh-ax82u}

可以混搭。RT-AX82U 鋼彈版支援 AiMesh 主路由器與節點模式；[ASUS 官方相容性說明](https://www.asus.com/tw/support/faq/1053365/)也允許 Wi-Fi 7 路由器搭配既有 AiMesh 機種。建議讓 BE92U 當主路由器，舊 AX82U 當補訊號的節點；15 坪單房間先試新機單台，有死角再加入舊機。

| 設備 | 角色 | 連接方式與能力 |
| --- | --- | --- |
| RT-BE92U | 主路由器 | WAN 接光世代設備，PC 接它的 2.5G LAN；在 VR 遊玩區提供 6GHz |
| RT-AX82U | AiMesh 節點 | 優先用 BE92U 的 LAN 接 AX82U 的 WAN，提供 Wi-Fi 6 的 2.4／5GHz 覆蓋 |

上述 LAN 到 WAN 的接法是 [ASUS 有線回程教學](https://www.asus.com/tw/support/faq/1035140/)的配置。現有 Cat 7 若運作正常即可沿用；回程會受 AX82U 的 Gigabit WAN 限制，連線速率最高 1Gbps。這個限制只影響經過舊節點的路徑，不會把直接接 BE92U 的 PC、6GHz 裝置或其他埠全部降成 1G。

AX82U 也可以用無線回程，但沒有 6GHz 與 Wi-Fi 7 MLO，且無線回程會使用無線資源。玩 PC VR 時，讓 Quest 3 在同房間直接連 BE92U 的 6GHz，PC 也直接接 BE92U，避免串流繞過舊節點。Quest 3 若連到 AX82U，就只能使用舊機的 2.4／5GHz。

設定順序：

1. 兩台先更新韌體，保存舊機的寬頻帳號與需要沿用的設定。
2. 先把 BE92U 設成主路由器，確認上網正常，再將 AX82U 恢復出廠設定。
3. 在 BE92U 的 AiMesh 頁面搜尋並加入 AX82U；需要操作細節時依 [ASUS AiMesh 設定教學](https://www.asus.com/tw/support/faq/1035087/)處理。
4. 接上有線回程後，在 AiMesh 拓樸確認連線方式；需要固定走線時，將節點的回程連線優先設為 WAN 優先。

MLO 與舊節點混搭可能有相容性限制；若加入後出現節點斷線或裝置無法連線，再依 [ASUS MLO FAQ](https://www.asus.com/tw/support/faq/1053342/)調整設定，必要時暫停 MLO 交叉測試。AX82U 本來就不支援 6GHz，不能把官方對舊節點的限制誤讀成「加入 AX82U 後，BE92U 的 6GHz 一律失效」，也不必一開始就關掉整台主路由器的 Wi-Fi 7。

## Quest 3 找不到 6GHz 時 {#quest-3-6ghz}

Quest 3 只支援 Wi-Fi 6E，常見問題是找不到 Wi-Fi 7 路由器的 6GHz 網路。TP-Link 官方建議依序處理：

1. Quest 3 和路由器都更新到最新韌體。
2. 6GHz 加密方式用 WPA3-Personal，頻寬設成 160MHz 以下（不要用 320MHz），開啟 PSC，頻道設成自動。
3. 還是找不到，把 6GHz 的模式改成 802.11ax only。這會讓連 6GHz 的 PS5 Pro、iPhone 失去 Wi-Fi 7 功能，PS5 Pro 可以改連 5GHz。

社群另外整理的做法：

- 6GHz 使用獨立的網路名稱與密碼，不要隱藏 SSID；掃不到時在 Quest 3 手動新增網路。
- 排查時保留 2.4GHz 與 5GHz 開啟。
- 連上後會斷線時，在 Quest 3 的 Wi-Fi 隱私設定改用裝置 MAC，或在路由器替它設定固定 IP。

Quest 3 在台灣能否使用 6GHz，目前找不到 Meta 的官方說明。同樣在台灣使用的 Mac 可以看到 6GHz 頻道，但頭盔仍以實際連線為準。

## 驗證方式 {#verify}

- **PS5 Pro：** 換機前後在相同位置與相近負載下，到「設定 → 網路 → 連線狀態 → 測試網際網路連線」測試並記下下載速度；單次 PSN 測速也受服務端與外網影響，不能單獨證明 Wi-Fi 的性能。
- **Quest 3：** 在頭盔、Virtual Desktop 連線資訊或路由器用戶端列表交叉確認頻段、連線節點與速率。2x2、160MHz 的 Wi-Fi 6E 最高 PHY 約為 2400 Mbps，不等於 VR 串流碼率或實際吞吐量；再以相同遊戲、編碼與碼率比較延遲及掉幀。
- **Mac：** 重跑上面的 `system_profiler` 指令，確認目前連線的 `Channel:` 是 6GHz、160MHz。
- **AiMesh：** 確認 AX82U 的回程是有線或無線，以及 Quest 3 是否直接連到 BE92U；只看到同一個 Wi-Fi 名稱，不能判斷實際連線路徑。
- **iPhone 或 PS5 Pro 常斷線：** 先在路由器關閉 MLO，或替 6GHz 另外設獨立網路名稱，再測一次。

## 補充說明 {#notes}

- **PS5 Pro 的 Wi-Fi 規格：** Sony 沒有公開 MLO 與最高頻寬。法國媒體實測 PS5 Pro 連 Wi-Fi 7 路由器時，下載接近 1000 Mb/s，舊款 PS5 連 Wi-Fi 6 約 500 Mb/s；但同一篇測試中，PS5 Pro 連另一台 Wi-Fi 7 路由器只跑出 78 Mb/s，相容性有差，買回來一定要實測。
- **退換貨：** 網購通訊交易原則上有 7 日解除權，但仍有法定例外，不能當成保證可任意試用後退貨。必要檢查與使用造成價值減損的界線，依個案與法規判斷；購買前先看清楚通路的退換貨及瑕疵處理方式。[行政院消保會說明](https://cpc.ey.gov.tw/Page/BC16ACF0BBB9CCC2/2055825e-e262-47da-9f56-398a71c92c5b)

## 參考資料 {#references}

- [PChome：ASUS RT-BE92U](https://24h.pchome.com.tw/prod/DRAFJ5-A900I3EKW)
- [PChome：TP-Link Archer BE550](https://24h.pchome.com.tw/prod/DRAN5B-A900H2KB5)
- [PChome：Mercusys MR47BE](https://24h.pchome.com.tw/prod/DRAFJ9-A900H3SL0)
- [原價屋線上估價](https://www.coolpc.com.tw/evaluate.php)
- [ASUS RT-AX82U 鋼彈版規格](https://www.asus.com/tw/networking-iot-servers/wifi-routers/asus-gaming-routers/rt-ax82u-gundam-edition/techspec/)
- [ASUS RT-BE92U 台灣官方規格](https://shop.asus.com/tw/90ig0950-mt1a0v-asus-rt-be92u.html)
- [ASUS：Wi-Fi 7 與既有 AiMesh 的相容性](https://www.asus.com/tw/support/faq/1053365/)
- [ASUS：AiMesh 有線回程接法](https://www.asus.com/tw/support/faq/1035140/)
- [ASUS：AiMesh 設定步驟](https://www.asus.com/tw/support/faq/1035087/)
- [ASUS：MLO 設定與混搭限制](https://www.asus.com/tw/support/faq/1053342/)
- [RTINGS：ASUS RT-BE92U 評測](https://www.rtings.com/router/reviews/asus/rt-be92u)
- [TP-Link：Archer BE600 規格](https://hk.store.tp-link.com/products/archer-be600-be9700-wifi-7-router)
- [ASUS X870 MAX GAMING WIFI7 W 台灣規格](https://www.asus.com/tw/motherboards-components/motherboards/others/x870-max-gaming-wifi7-w/techspec/)
- [Apple：裝置的 Wi-Fi 與乙太網路規格](https://support.apple.com/zh-tw/guide/deployment/dep268652e6c/web)
- [Sony：PS5 Pro 有線與無線網路規格](https://blog.playstation.com/2024/11/07/getting-started-with-playstation-5-pro-out-today/)
- [Meta：Quest 3 官方規格](https://www.meta.com/quest/quest-3/#specs)
- [任天堂：Switch 2 支援的無線頻段與模式](https://en-americas-support.nintendo.com/app/answers/detail/a_id/498/p/696)
- [Tom's Guide：Switch 2 FCC 文件顯示 Wi-Fi 6](https://www.tomsguide.com/gaming/nintendo/nintendo-switch-2-key-specs-just-revealed-in-new-fcc-filing)
- [Business Today：PS5 Pro 需要 6GHz 開放才上市](https://www.businesstoday.in/amp/technology/news/story/sony-ps5-pro-will-not-be-launched-in-india-due-to-wi-fi-7-restrictions-453020-2024-11-08)
- [Presse-Citron：PS5 Pro Wi-Fi 7 實測](https://www.presse-citron.net/le-wifi-7-de-la-ps5-pro-a-t-il-vraiment-un-interet-notre-comparatif/)
- [TP-Link 社群：Quest 3 找不到 Wi-Fi 7 路由器的 6GHz 網路](https://community.tp-link.com/en/smart-home/forum/topic/669728)
- [Virtual Desktop：電腦有線連接與同區網要求](https://www.vrdesktop.net/)
- [Meta 社群：Quest 3 連線問題討論](https://communityforums.atmeta.com/pairing-connection-12/quest-2-3-pro-connectivity-issues-133186/index10.html)
- [數位發展部：Wi-Fi 頻段與台灣 6GHz 頻譜配置](https://moda.gov.tw/press/dictionary/11728)
- [數位發展部：6GHz 頻段開放簡報](https://www-api.moda.gov.tw/File/Get/moda/zh-tw/ID1AEFSxRjM72DU)
