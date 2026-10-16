# Wi-Fi 7 路由器單房間升級：1G 光世代該買哪一台

<web-summary>從 Wi-Fi 6 路由器升級 Wi-Fi 7 時，單房間搭配 1G 光世代的效益來自 6GHz 而不是網速；只挑含 6GHz 的三頻機，不必追 10G 網路孔或 320MHz，並附 2026-10 原價屋與 PChome 價格比較，以及 PS5 Pro、Quest 3 的頻段設定。</web-summary>

單房間、1G 光世代的情況下，換 Wi-Fi 7 不會讓網路變快，真正的改善是讓無線裝置改走干擾較少的 6GHz。所以只挑**含 6GHz 的三頻機**，不必為 10G 網路孔或 320MHz 多付錢。2026-10-16 查價時，CP 值最高的是原價屋的 TP-Link Archer BE550（5,599 元）；想繼續用 ASUS 管理介面就選 RT-BE92U（7,699 元）。

<tldr>
<p>只買含 6GHz 的三頻機；雙頻 Wi-Fi 7 對 Wi-Fi 6E 裝置來說，幾乎等於原本的 5GHz Wi-Fi 6。</p>
<p>Mac 是否支援 Wi-Fi 7：看 system_profiler SPAirPortDataType 的 Supported PHY Modes 有沒有 be。</p>
<p>Quest 3 找不到 6GHz：6GHz 頻寬設 160MHz 以下並開啟 PSC，仍不行再改 802.11ax only。</p>
</tldr>

本文情境：原本使用 ASUS RT-AX82U（Wi-Fi 6，5GHz 為 4x4、160MHz，網路孔全部是 Gigabit），只在約 15 坪的單一房間使用，網路是 1G 光世代，沒有 NAS。PC 用 Cat 7 接有線，PS5 Pro、Quest 3、手機與筆電走無線。

![單房間 PC VR 情境：PC 以網路線連接架上的路由器，Quest 3 在同房間透過無線連線接收串流](wifi-7-single-room-pcvr.png){thumbnail="true" width="900"}

AI 生成情境示意：PC 與路由器之間走有線，頭盔與路由器之間走無線；設備外觀與藍色波紋不代表特定產品或實測覆蓋範圍。

## 換機會改善什麼 {#what-improves}

| 項目 | 換 Wi-Fi 7 三頻機之後 |
| --- | --- |
| 對外網速 | 不變。1G 方案的上限約 940 Mbps，原本的 Gigabit WAN 已經跑得滿 |
| 有線裝置 | 不變。PC、主機接有線時，延遲由線路與 ISP 決定 |
| 無線裝置 | 可改走 6GHz，鄰居訊號少、延遲較穩；Wi-Fi 7 裝置還能用 MLO |
| 覆蓋範圍 | 6GHz 穿牆較差，但只在單一房間使用，這個缺點不影響 |

判斷方式：

- **主要裝置都接有線：** 可以不換，把錢省下來。
- **有 PS5 Pro、VR 頭盔、手機或筆電走無線：** 換含 6GHz 的三頻機值得，因為這些裝置能直接受益。

## 先查裝置支援什麼 {#client-capabilities}

| 裝置 | Wi-Fi | 最高頻寬 | 有線 | 換機後 |
| --- | --- | --- | --- | --- |
| PC（ASUS X870 MAX GAMING WIFI7） | Wi-Fi 7，2x2 | 160MHz | 2.5G | 接有線時不變；主機板 Wi-Fi 7 需要 Windows 11 24H2 以上 |
| PS5 Pro | Wi-Fi 7（含 6GHz） | 官方未公開 | 1G | 走無線時可改用 6GHz 或 5GHz Wi-Fi 7 |
| iPhone 16 Pro Max | Wi-Fi 7，2x2，支援 MLO | 160MHz | 無 | 可用 6GHz 與 MLO |
| MacBook Pro（M4 Max） | Wi-Fi 6E | 160MHz | 無 | 可走 6GHz，但用不到 Wi-Fi 7 功能 |
| Meta Quest 3 | Wi-Fi 6E | 160MHz | 無 | 可走 6GHz；用 PC VR 串流時最受益 |
| Nintendo Switch 2 | Wi-Fi 6，只有 2.4／5GHz | 80MHz | 接底座 | 幾乎不變 |

這些裝置**沒有一台能用 320MHz**，所以 BE9300 等級的三頻機就夠用，BE9700 或更高等級多出來的頻寬用不到。

在 macOS 可以直接查本機 Wi-Fi 能力與目前連線：

```bash
system_profiler SPAirPortDataType | grep -E 'Supported PHY Modes|PHY Mode:|Channel:'
```

- `Supported PHY Modes` 只到 `802.11 a/b/g/n/ac/ax`：本機是 Wi-Fi 6 或 6E，不支援 Wi-Fi 7；出現 `be` 才是 Wi-Fi 7。
- `Channel:` 顯示 `6GHz`：目前連在 6GHz。M4 世代的 Mac 仍是 Wi-Fi 6E。

## 台灣 6GHz 能用多寬 {#taiwan-6ghz}

台灣開放的 6GHz 是 5945–6425 MHz，共 480MHz，限室內低功率使用。這段頻譜可以排：

- 3 個互不重疊的 160MHz 頻道，或
- 1 個 320MHz 頻道（有兩個可選位置，但彼此重疊，同時只能用一個）

所以 Wi-Fi 7 的 320MHz 在台灣可用。只是如上一節所示，常見的手機、筆電、主機與 VR 頭盔最多只到 160MHz。

## 不要買雙頻 Wi-Fi 7 {#avoid-dual-band}

下面這些是 Wi-Fi 7，但**沒有 6GHz**：

- ASUS RT-BE86U（BE6800，7,199 元）
- ASUS RT-BE88U（BE7200，9,999 元）
- ASUS RT-BE82U、RT-BE58U，以及各家 BE3600 系列

Mac、Quest 3 這類 Wi-Fi 6E 裝置連上雙頻 Wi-Fi 7，只能走 5GHz Wi-Fi 6，跟原本的 Wi-Fi 6 路由器差不多。RT-BE86U 的價錢和三頻的 RT-BE92U 很接近，特別容易買錯。

## 候選機種與價格（2026-10-16） {#candidates}

| 型號 | 等級 | 網路孔 | 原價屋 | PChome | 說明 |
| --- | --- | --- | --- | --- | --- |
| **TP-Link Archer BE550** | BE9300 三頻 | 5×2.5G | **5,599 元** | 5,999 元 | CP 值最高；原價屋品名註明支援 320MHz、高通晶片 |
| Mercusys MR47BE | BE9300 三頻 | 4×2.5G | 4,999 元，送 1,000 酷幣 | 4,999 元 | 最便宜；管理介面較陽春 |
| TP-Link Archer BE600 | BE9700 三頻 | 1×10G＋4×2.5G | 6,999 元 | 6,999 元 | 和 RT-BE92U 同級 |
| ASUS RT-BE92U | BE9700 三頻 | 1×10G＋4×2.5G | 7,699 元（特價到 10/19） | 7,699 元 | 可沿用 ASUS 管理介面與 AiMesh |
| TP-Link Archer GE550 | BE9300 電競版 | 2×5G＋3×2.5G | 6,999 元，送 1,000 酷幣 | 6,999 元 | 1G 網路用不到 5G 網路孔 |
| ASUS TUF-BE9400 | 三頻 | 4×2.5G | 7,999 元 | 7,999 元 | 比 RT-BE92U 貴，又少了 10G 網路孔 |

- 價格會變動，以上是 2026-10-16 兩家的報價，下單前再確認。
- 酷幣是原價屋的回饋點數，下次在原價屋消費可以折抵。
- 1G 網路、沒有 NAS 時，10G 網路孔用不到。RT-BE92U 和 Archer BE600 多出來的價差，主要就是花在這個孔上。
- RT-BE92U 的 5GHz 是 2x2（2882 Mbps），帳面數字比 RT-AX82U 的 4x4（4804 Mbps）低。不過常見的手機和筆電本來就是 2x2，在同一個房間裡差異不大。

## 頻段分配建議 {#band-plan}

| 裝置 | 建議連線方式 |
| --- | --- |
| PC | Cat 7 有線，接 2.5G 網路孔 |
| Quest 3 | 6GHz，給 6GHz 一個獨立的網路名稱 |
| PS5 Pro | 優先接有線（1G 網路孔剛好跑滿 1G 方案）；不方便拉線就連 5GHz |
| iPhone、MacBook | 6GHz 或 5GHz 都可以，用量小 |
| Switch 2 | 5GHz；放在底座時可以接有線 |

PC VR 的影音路徑是「PC → 網路線 → 路由器 → 6GHz → Quest 3」。同房間串流走內網，1G 光世代不是這段傳輸的速率上限；重點是 PC 的有線連接、頭盔的無線訊號與兩端編解碼能力。[Virtual Desktop 官方](https://www.vrdesktop.net/)也建議 PC 以網路線接路由器，並與頭盔保持在同一區網。

6GHz 只有一個頻段，所有連上去的裝置共用頻寬。玩 VR 串流時，如果 PS5 Pro 也在 6GHz 背景下載遊戲，串流就可能卡頓，所以 6GHz 優先留給 Quest 3。

沒有 VR 頭盔、PS5 Pro 又必須走無線時，就反過來讓 PS5 Pro 固定連 6GHz 的獨立網路名稱，避免它自己跳回 5GHz。

設定頻段之外，也要確認擺位：路由器放在開放、架高且接近遊玩區的位置，讓頭盔到路由器之間盡量少有櫃體、牆壁或大型物品阻擋。

![路由器擺位比較：左圖放在開放的高處層架，右圖放在靠地面的櫃內；兩邊 PC 都以網路線連接路由器](wifi-7-single-room-router-placement.png){thumbnail="true" width="900"}

AI 生成擺位示意：左圖保留開放的無線路徑，右圖示範櫃體與低處擺放造成的遮擋；波紋不代表實測訊號強度，不能據此推算速度或延遲。

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

- **PS5 Pro：** 換機前後各到「設定 → 網路 → 連線狀態 → 測試網際網路連線」測一次，記下下載速度。
- **Quest 3：** 在 Virtual Desktop 的連線資訊確認實際連到 6GHz；2x2、160MHz 的連線速率約為 2400 Mbps。手臂或物品擋在路由器前就可能讓速率下降，保持視線通暢。
- **Mac：** 重跑上面的 `system_profiler` 指令，確認目前連線的 `Channel:` 是 6GHz、160MHz。
- **iPhone 或 PS5 Pro 常斷線：** 先在路由器關閉 MLO，或替 6GHz 另外設獨立網路名稱，再測一次。

## 補充說明 {#notes}

- **PS5 Pro 的 Wi-Fi 規格：** Sony 沒有公開 MLO 與最高頻寬。法國媒體實測 PS5 Pro 連 Wi-Fi 7 路由器時，下載接近 1000 Mb/s，舊款 PS5 連 Wi-Fi 6 約 500 Mb/s；但同一篇測試中，PS5 Pro 連另一台 Wi-Fi 7 路由器只跑出 78 Mb/s，相容性有差，買回來一定要實測。
- **退貨保障：** 網路購物依消保法有 7 天猶豫期；在門市現場購買沒有這項保障。擔心頭盔或主機連不上 6GHz 時，網購的價差可以當作保險。
- **舊路由器：** 換成 ASUS 的機種時，RT-AX82U 可以設成 AiMesh 節點；只用一個房間時，通常不需要。

## 參考資料 {#references}

- [PChome：ASUS RT-BE92U](https://24h.pchome.com.tw/prod/DRAFJ5-A900I3EKW)
- [PChome：TP-Link Archer BE550](https://24h.pchome.com.tw/prod/DRAN5B-A900H2KB5)
- [PChome：Mercusys MR47BE](https://24h.pchome.com.tw/prod/DRAFJ9-A900H3SL0)
- [原價屋線上估價](https://www.coolpc.com.tw/evaluate.php)
- [ASUS RT-AX82U 鋼彈版規格](https://www.asus.com/tw/networking-iot-servers/wifi-routers/asus-gaming-routers/rt-ax82u-gundam-edition/techspec/)
- [RTINGS：ASUS RT-BE92U 評測](https://www.rtings.com/router/reviews/asus/rt-be92u)
- [TP-Link：Archer BE600 規格](https://hk.store.tp-link.com/products/archer-be600-be9700-wifi-7-router)
- [ASUS X870 MAX GAMING WIFI7 規格](https://www.asus.com/me-en/motherboards-components/motherboards/others/x870-max-gaming-wifi7/techspec/)
- [MacRumors：M4 Mac 沒有 Wi-Fi 7，iPhone 16 支援 Wi-Fi 7](https://macrumors.com/2024/10/30/m4-mac-models-no-wi-fi-7)
- [Tom's Guide：Switch 2 FCC 文件顯示 Wi-Fi 6](https://www.tomsguide.com/gaming/nintendo/nintendo-switch-2-key-specs-just-revealed-in-new-fcc-filing)
- [Business Today：PS5 Pro 需要 6GHz 開放才上市](https://www.businesstoday.in/amp/technology/news/story/sony-ps5-pro-will-not-be-launched-in-india-due-to-wi-fi-7-restrictions-453020-2024-11-08)
- [Presse-Citron：PS5 Pro Wi-Fi 7 實測](https://www.presse-citron.net/le-wifi-7-de-la-ps5-pro-a-t-il-vraiment-un-interet-notre-comparatif/)
- [TP-Link 社群：Quest 3 找不到 Wi-Fi 7 路由器的 6GHz 網路](https://community.tp-link.com/en/smart-home/forum/topic/669728)
- [Virtual Desktop：電腦有線連接與同區網要求](https://www.vrdesktop.net/)
- [Meta 社群：Quest 3 連線問題討論](https://communityforums.atmeta.com/pairing-connection-12/quest-2-3-pro-connectivity-issues-133186/index10.html)
- [iThome：台灣開放 6GHz 頻段](https://www.ithome.com.tw/news/159623)
- [數位發展部：6GHz 頻段開放簡報](https://www-api.moda.gov.tw/File/Get/moda/zh-tw/ID1AEFSxRjM72DU)
