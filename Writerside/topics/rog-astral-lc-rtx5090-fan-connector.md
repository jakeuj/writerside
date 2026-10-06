# ROG Astral LC RTX 5090 冷排風扇不亮、不轉：磁吸接頭暫時恢復後復發

<web-summary>ROG Astral LC RTX 5090 冷排風扇壓回磁吸接頭後僅暫時恢復，過一陣子又停止；負載截圖顯示 Fan 2 為 88% 卻是 0 RPM。此個案已復發，需檢查接頭固定、線組與風扇模組。</web-summary>

**2026-10-07 更新：冷排風扇再次停止，問題尚未解決。**前一次拆下固定螺絲、將黑色接頭用力重新插入並鎖緊後，通電會亮、會轉；但這次確認只是暫時恢復。作者觀察到壓回接頭會好一陣子，過一陣子疑似鬆掉，又失去供電般停止運作。

現在應先停止 GPU 重負載工作，並請店家或華碩檢查接頭固定、線組與風扇模組。壓回後能短暫恢復支持接觸不良的推論，但不能當成持續有效的修復。

首次記錄：2026-10-06；復發更新：2026-10-07。以下保留作者回報的操作與觀察，並區分官方資料、排查建議、短暫恢復及最新故障狀態。

## 原始症狀 {#symptoms}

使用的顯卡是 [ROG Astral LC GeForce RTX 5090 32GB GDDR7 OC](https://rog.asus.com/tw/graphics-cards/graphics-cards/rog-astral/rog-astral-lc-rtx5090-o32g-gaming/)，型號為 `ROG-ASTRAL-LC-RTX5090-O32G-GAMING`。

- 360 mm 冷排上的三顆原廠風扇全部不亮，也不轉。
- 顯卡本體上的風扇正常運轉。
- 看不到需要另外接上的風扇供電線或 RGB 線，因此一開始懷疑是否漏接線材。

顯卡本體風扇正常，只能確認該風扇有運作，不能據此判斷冷排風扇與它們的共用線路正常。

## 共用磁吸接頭在哪裡 {#connector-location}

接頭位於**冷排接水管的那一端、第一顆風扇的角落**。下圖上方紅框是固定螺絲，下方紅框是連著線材的黑色接頭。

![ROG Astral LC RTX 5090 冷排水管旁的固定螺絲與黑色磁吸接頭](rog-astral-lc-rtx5090-magnetic-connector.png){width="450" thumbnail="true"}

圖片來源：[華碩官方磁吸頭說明](https://www.asus.com/tw/support/faq/1055700/)，為本次提供的定位參考圖。

原廠冷排採用磁吸串接風扇。ROG 論壇管理員也說明，這個磁吸接頭同時負責 RGB 與風扇；燈光線路沿著水管連回顯卡，控制 Aura 不需要另外接外部 RGB 線。[共用接頭說明](https://rog-forum.asus.com/t5/gaming-graphics-cards/rog-astral-lc-geforce-rtx-5090-oc-32gb-rad-fans-stop-spinning/m-p/1153026)、[燈光線路說明](https://rog-forum.asus.com/t5/nvidia-graphics-cards/aura-system-rog-astral-rtx5090-lc/m-p/1108766)

因此，三顆風扇同時失去轉動與燈光時，共用接頭與線組是值得優先檢查的位置。這是依症狀與線路設計做的排查推論，不能直接認定三顆風扇都已損壞。

## 2026-10-06 首次處理：暫時恢復 {#successful-fix}

作者首次回報的實際操作順序如下，後續已確認會復發：

1. 拆下冷排共用磁吸接頭的固定螺絲。
2. 將黑色接頭**用力重新插入，使接頭充分接合**。
3. 重新鎖緊固定螺絲。
4. 再次通電，確認冷排風扇恢復亮燈與轉動。

重新接合並固定黑色接頭後，燈光與轉動曾一起恢復。回報中沒有另外接上主機板風扇線或 RGB 線，也沒有以升高 GPU 溫度作為修復方式。2026-10-07 再次停止，故這段操作只能記為暫時恢復。

華碩[官方說明](https://www.asus.com/tw/support/faq/1055700/)不建議自行拆卸這裡的螺絲與磁吸頭，因為可能損壞內部組件並影響散熱或運作。以上是本次個案的實際紀錄，不是華碩提供的標準維修步驟；需要處理接頭時，應先關機、關閉電源供應器並拔掉電源線。若接頭無法正常接合或反覆鬆脫，交由店家或華碩檢查。

## 風扇要幾度才轉，燈光要幾度才亮 {#temperature-and-lighting}

風扇轉動與 RGB 燈光是分開控制的功能。

| 功能 | 官方資料與判斷方式 |
| --- | --- |
| 風扇啟動 | 華碩 RTX 50 系列通用資料列出：GPU 溫度高於 55°C，或顯卡功耗高於 100 W 時啟動。 |
| 0dB 停轉 | 同一份資料列出：GPU 溫度低於 50°C、功耗低於 50 W，且啟用 0dB 模式時停轉，三項條件需同時成立。 |
| RGB 燈光 | 由 Aura／Armoury Crate 控制。一般亮燈沒有等待 GPU 升溫的門檻，待機時也可以亮；關閉燈效則可能使燈光熄滅。 |

溫度與功耗條件來源：[華碩 RTX 30／40／50 系列風扇運轉與停轉說明](https://www.asus.com/tw/support/faq/1044879/)。燈光控制來源：[GPU Tweak III 官方頁面的 Aura 說明](https://www.asus.com/campaign/GPU-Tweak-III/tw/index.php)。

**55°C 是通用參考值。**這份 FAQ 沒有單獨列出 Astral LC 三顆冷排風扇的獨立啟動門檻，實際行為也可能受 BIOS、0dB 模式、自訂風扇曲線與電源管理設定影響。不能把三顆風扇同時不亮、不轉，一律解釋成溫度還沒到。

## GPU Tweak III 畫面與排查建議 {#gpu-tweak-observations}

排查時提供的 GPU Tweak III v2.2.0.1 畫面如下：

![GPU Tweak III 顯示 0dB 關閉、散熱排風扇 30% Auto，並回報 515 RPM](rog-astral-lc-rtx5090-gpu-tweak.png){thumbnail="true"}

畫面中可讀到：

- 中央溫度為 26°C，其他熱區約 30 至 31°C。
- 「0dB 風扇」開關呈現關閉狀態。
- 「鼓風扇轉速」與「散熱排風扇轉速」都顯示 30%，並有 Auto 按鈕。
- 上方三顆風扇圖示旁回報 515 RPM。

這些數字是軟體畫面上的設定或回報，仍需以實體風扇是否轉動交叉確認。若軟體顯示 RPM，但眼睛看到三顆完全不轉，讀值就與現場狀態不一致，不能僅憑該數字認定風扇正常。

當時提出的排查建議是：關閉 0dB，將**散熱排風扇**切換成手動並設為 60%，套用後等幾秒觀察實際轉動。GPU Tweak III 支援自訂風扇曲線與固定轉速設定。[官方風扇控制說明](https://www.asus.com/campaign/GPU-Tweak-III/index.php)

這項 60% 測試是當時的排查建議；目前沒有作者執行該測試後的獨立結果。前述重新插入接頭並鎖緊螺絲曾暫時恢復，不應把兩者混寫成同一項實測。既然現已確認在負載下仍停止，就不需要再用燒機升溫來重現。

## 2026-10-07 復發與負載讀值 {#recurrence-2026-10-07}

作者最新回報：

> 剛發現風扇又不轉了，壓回去會好一陣子，過一陣子她鬆掉的樣子就又沒電了。

「疑似鬆掉」與「像是沒電」是作者對現場狀態的描述；目前沒有接頭位移量測或電壓量測，不能進一步確認是機械鬆脫、接點接觸不良，還是線組或模組本身異常。

這次提供的截圖同時包含 GPU-Z 2.69.0、GPU Tweak III v2.2.0.1 與 NVIDIA App。以下摘錄本次截圖中的數值：

| 軟體與欄位 | 截圖讀值 |
| --- | --- |
| GPU-Z：GPU Temperature | 76.5°C |
| GPU-Z：Memory Temperature | 84.0°C |
| GPU-Z：GPU Load | 100% |
| GPU-Z：Board Power Draw | 611.9 W |
| GPU-Z：Fan 1 Speed (%) | 100% |
| GPU-Z：Fan 1 Speed (RPM) | 3331 RPM |
| GPU-Z：Fan 2 Speed (%) | 88% |
| GPU-Z：Fan 2 Speed (RPM) | **0 RPM** |
| GPU Tweak III：鼓風扇轉速 | 100% |
| GPU Tweak III：散熱排風扇轉速 | **88%** |
| GPU Tweak III：0dB 風扇 | 畫面開關為關閉狀態 |

GPU-Z 的 Fan 2 百分比與 GPU Tweak III 的散熱排風扇百分比相符；配合作者看到冷排風扇停止，符合「有要求風扇轉動，卻沒有正常轉動或轉速回報」的故障表現。不同軟體可能有不同的欄位映射與更新時間，判斷時仍以實體風扇和對應 RPM 交叉確認。

此時 GPU 溫度與功耗已高於華碩通用 0dB 啟動條件，且畫面中的 0dB 已關閉，因此不能用待機溫度低來解釋這次停止。Fan 1 的約 3331 RPM 也不能代替冷排風扇的運作證據。

當冷排風扇停止時，先停止遊戲、生成或燒機等 GPU 重負載工作。需要碰觸接頭前，先關機、關閉電源供應器並拔掉電源線；不要將通電按壓接頭當成常態操作。

## 相似論壇案例與客服處理方向 {#similar-cases}

作者指出，[ROG 論壇這篇接頭鬆脫案例](https://rog-forum.asus.com/t5/gaming-graphics-cards/rog-astral-lc-rtx-5090-radiator-fans-not-spinning-due-to-loose/td-p/1120426)與本次情況基本一致：

- 原發文者回報顯卡本體風扇正常，冷排風扇會停止；將接頭壓回後能恢復，但幾分鐘後又逐漸退出。
- 同串另一位使用者也回報相同問題，並對磁吸接頭與固定設計提出質疑。
- 華碩客服表示願意轉交支援團隊協助。

兩個案例共有的模式是「重新接合後暫時恢復，過一陣子再停止」。論壇原發文者當時仍有 RGB，本次最初則是三顆不亮、不轉；不能因此把兩案的所有細節視為完全相同。其他人的垂直安裝方式與水泵振動也不能套用成本次已確認的狀態。

這些回報能證明有其他使用者遇到相似症狀，尚不能據此判定故障比例、正式召回或所有同型號都有設計缺陷。

另在[接頭自行鬆脫的同類案例](https://rog-forum.asus.com/t5/gaming-graphics-cards/rog-astral-lc-rtx-5090-aio-cable-loose/td-p/1136052)中，華碩客服認為這種表現屬於異常硬體連接，建議儘快安排保固檢修，由服務中心檢查並視情況更換相關線組或模組。這是該案的客服建議，本次仍待店家或華碩實際檢查。

## 目前結果與驗證範圍 {#result}

| 時點 | 作者觀察 | 紀錄狀態 |
| --- | --- | --- |
| 最初 | 三顆冷排風扇不亮、不轉，顯卡本體風扇正常 | 故障 |
| 2026-10-06 首次處理 | 重新插入接頭並鎖緊後，通電會亮、會轉 | 暫時恢復 |
| 2026-10-07 更新 | 過一陣子再次停止；壓回接頭後只能好一陣子 | **已復發、尚未修復** |
| 復發截圖 | Fan 2 為 88%，卻回報 0 RPM；顯卡功耗約 612 W | 負載下風扇異常證據 |

目前的判斷是**高度懷疑共用接頭接觸不良或固定不穩**。反覆按回能短暫恢復，支持連接問題的推論；仍需檢查才能確定哪個接點、線組或模組有問題。

本次尚無送修、換件或長時間穩定運轉的結果，也沒有新的 RGB 狀態單獨回報。保留「暫時恢復後復發」的完整時間線，將截圖與接頭復發影片提供給店家或華碩，請其檢查；在冷排恢復持續穩定運作前，避免 GPU 重負載。

## 參考資料 {#references}

- [ROG Astral LC GeForce RTX 5090 32GB GDDR7 OC 產品頁](https://rog.asus.com/tw/graphics-cards/graphics-cards/rog-astral/rog-astral-lc-rtx5090-o32g-gaming/)
- [華碩：ROG-ASTRAL-LC-RTX5090 系列水冷散熱器磁吸頭相關說明](https://www.asus.com/tw/support/faq/1055700/)
- [華碩：RTX 30／40／50 系列風扇運轉和停轉的情境](https://www.asus.com/tw/support/faq/1044879/)
- [ROG 論壇：冷排風扇停止轉動，共用磁吸接頭與線材拉力說明](https://rog-forum.asus.com/t5/gaming-graphics-cards/rog-astral-lc-geforce-rtx-5090-oc-32gb-rad-fans-stop-spinning/m-p/1153026)
- [ROG 論壇：Astral LC 冷排燈光線路與 Armoury Crate 控制](https://rog-forum.asus.com/t5/nvidia-graphics-cards/aura-system-rog-astral-rtx5090-lc/m-p/1108766)
- [ROG 論壇：壓回接頭後暫時恢復，但接頭再次鬆脫](https://rog-forum.asus.com/t5/gaming-graphics-cards/rog-astral-lc-rtx-5090-radiator-fans-not-spinning-due-to-loose/td-p/1120426)
- [ROG 論壇：同類接頭自行鬆脫案例與華碩保固檢修建議](https://rog-forum.asus.com/t5/gaming-graphics-cards/rog-astral-lc-rtx-5090-aio-cable-loose/td-p/1136052)
- [GPU Tweak III 官方頁面](https://www.asus.com/campaign/GPU-Tweak-III/tw/index.php)
