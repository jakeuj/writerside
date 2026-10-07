# ROG Astral LC RTX 5090 冷排風扇不亮、不轉：磁吸接頭暫時恢復後復發

<web-summary>ROG Astral LC RTX 5090 冷排風扇壓回磁吸接頭後僅暫時恢復，過一陣子又停止；負載截圖顯示 Fan 2 為 88% 卻是 0 RPM。此個案已復發，需檢查接頭固定、線組與風扇模組。</web-summary>

**2026-10-07 更新：冷排風扇再次停止，問題尚未解決。**前一次拆下固定螺絲、將黑色接頭用力重新插入並鎖緊後，通電會亮、會轉；但這次確認只是暫時恢復。作者觀察到壓回接頭會好一陣子，過一陣子疑似鬆掉，又失去供電般停止運作。

現在應先停止 GPU 重負載工作，並請店家或華碩檢查接頭固定、線組與風扇模組。壓回後能短暫恢復支持接觸不良的推論，但不能當成持續有效的修復。

**2026-10-07 補充查證：ROG 官方論壇與 Reddit 有多個不同帳號回報相似的冷排風扇／磁吸接頭異常。**部分回報同樣出現「重新接合後暫時恢復，隨後再停止」，足以支持這類現象並非只有本次作者回報；故障率、批次與共通設計缺陷仍需原廠檢測及統計資料確認。案例與來源整理於下方。

首次記錄：2026-10-06；復發與相似案例查證更新：2026-10-07。以下保留作者回報的操作與觀察，並區分官方資料、排查建議、短暫恢復及最新故障狀態。

## 原始症狀 {#symptoms}

使用的顯卡是 [ROG Astral LC GeForce RTX 5090 32GB GDDR7 OC](https://rog.asus.com/tw/graphics-cards/graphics-cards/rog-astral/rog-astral-lc-rtx5090-o32g-gaming/)，型號為 `ROG-ASTRAL-LC-RTX5090-O32G-GAMING`。

- 360 mm 冷排上的三顆原廠風扇全部不亮，也不轉。
- 顯卡本體上的風扇正常運轉。
- 看不到需要另外接上的風扇供電線或 RGB 線，因此一開始懷疑是否漏接線材。

顯卡本體風扇正常，只能確認該風扇有運作，不能據此判斷冷排風扇與它們的共用線路正常。

## 共用磁吸接頭在哪裡 {#connector-location}

接頭位於**冷排接水管的那一端、第一顆風扇的角落**。下圖上方紅框是固定螺絲，下方紅框是連著線材的黑色接頭。

![ROG Astral LC RTX 5090 冷排磁吸接頭位置，黃色箭頭標示朝圖片左上方壓回接頭的施力方向，可暫時改善風扇不亮、不轉](rog-astral-lc-rtx5090-magnetic-connector-annotated.png){width="450" thumbnail="true"}

黃色箭頭標示本次個案的施力方向：將下方紅框內的黑色接頭**朝圖片左上方壓回，使接頭重新接合**。作者回報這樣可暫時改善接觸不良造成的風扇不亮、不轉，但過一陣子仍會復發，不能視為已修復。

原始圖片來源：[華碩官方磁吸頭說明](https://www.asus.com/tw/support/faq/1055700/)。箭頭與文字為依本次個案觀察加上的標註；操作紀錄與官方注意事項見下節。

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

## 多位使用者的相似停轉回報 {#similar-cases}

2026-10-07 核對第一手貼文後，找到以下同型號回報。日期採論壇明確顯示的發文日期；Reddit 頁面只顯示相對時間的回報，不推算精確日期。表中整理的是持有人自述，沒有取得各張顯卡的序號或維修檢測報告。

| 回報者與來源 | 回報現象 | 後續與驗證範圍 |
| --- | --- | --- |
| [Nartaq，2025-08-23](https://rog-forum.asus.com/t5/gaming-graphics-cards/rog-astral-lc-geforce-rtx-5090-32gb-gddr7-oc-fan-rgb-issue-fix/td-p/1112690) | 冷排風扇與 RGB 異常；晃動磁吸接頭可恢復，但接頭又失去穩定接合。 | 稱送店約一個月、取回仍不亮不轉；後來增加接頭保持壓力，回報恢復，未提供長期追蹤。 |
| [lxspector，2025-10-18](https://rog-forum.asus.com/t5/gaming-graphics-cards/rog-astral-lc-rtx-5090-radiator-fans-not-spinning-due-to-loose/td-p/1120426) | 本體風扇正常、RGB 仍亮；冷排風扇因接頭失去接合而停止，推回後幾分鐘又退出。 | 同串 zanozza 於 2025-10-24 也回報相同問題；客服願意轉交支援，未見修復完成回報。 |
| [angeli662，2026-02-26](https://rog-forum.asus.com/t5/gaming-graphics-cards/rog-astral-lc-rtx-5090-radiator-fans-not-spinning/td-p/1140409) | 卡很新、使用不多，RGB 亮但冷排風扇停；搖接頭有時啟動，隨即又停。 | 版主建議排查驅動，若持續發生則聯繫維修；沒有持有人回報修復成功。 |
| [Ahmed0Alkathiri，2026-03-21](https://rog-forum.asus.com/t5/gaming-graphics-cards/rog-astral-lc-rtx-5090-radiator-fans-not-spinning-due-to-loose/td-p/1143214) | 冷排風扇隨機停止，輕碰線材有時恢復；另有轉速暴衝與不合理 RPM 讀值。 | 版主要求送修檢查，客服提供聯絡管道；接頭根因尚未確認。 |
| [ROGn97dhxc55gkq，2026-06-29](https://rog-forum.asus.com/t5/gaming-graphics-cards/rog-astral-lc-geforce-rtx-5090-oc-32gb-rad-fans-stop-spinning/td-p/1153022) | 三顆冷排風扇停止；關機後微推水管旁黑色接頭，再開機可恢復，之後又停止。 | 版主確認那是 RGB 與風扇的磁吸接頭，建議減輕線材拉力；未見長期恢復結果。 |
| [MrAskani，Reddit](https://www.reddit.com/r/ASUSROG/comments/1kcqxeh/5090_rog_astral_lc_oc_radiator_power_issues/) | 主文附影片，稱軟體顯示約 5000 RPM，實體冷排風扇卻沒有轉動，也沒有 RGB。 | 後續稱 RMA 換卡後正常；沒有維修報告或長期追蹤。 |
| [YorVeX，同串另一帳號](https://www.reddit.com/r/ASUSROG/comments/1kcqxeh/comment/nglq4c6/) | 起初 RGB 亮、風扇不轉，軟體回報 500+ RPM；施力接頭後風扇與 RGB 恢復，一放手兩者停止。 | 稱增加接頭保持壓力後暫時恢復，自己也不確定能維持多久。 |

其中 ROGn97dhxc55gkq 的「重新接合後恢復、過一陣子再次停止」，以及 YorVeX 的「施力才恢復、放手又失效」，與本次個案尤其接近。這些回報支持檢查接頭接合與固定可靠性的方向；各回報者自行增加固定壓力的作法，是個案經過，不代表已驗證的維修方案。

## 華碩客服與論壇版主的處理方向 {#asus-support-responses}

在 [DonShani 的接頭自行鬆脫回報](https://rog-forum.asus.com/t5/gaming-graphics-cards/rog-astral-lc-rtx-5090-aio-cable-loose/td-p/1136052)中，Customer Service Agent Falcon2_ROG 於 **2026-01-23** 回覆：依照描述，接頭自行鬆脫並造成冷排風扇停止，屬於異常硬體連接的表現，建議儘快安排保固檢修，由服務中心檢查並視情況更換相關線組或模組。

[Ahmed0Alkathiri 的討論串](https://rog-forum.asus.com/t5/gaming-graphics-cards/rog-astral-lc-rtx-5090-radiator-fans-not-spinning-due-to-loose/td-p/1143214)中，Super Moderator Silent_Scone 於 **2026-03-21** 要求將顯卡交由維修檢查，Falcon2_ROG 於 **2026-04-02** 提供當地客服管道。這些回覆支持安排檢修，但不是已完成的故障根因鑑定，也不等於華碩正式承認全系列設計缺陷。

本次作者仍沒有店家或華碩實際檢測結果，不把其他人的客服建議或 RMA 結果寫成本次已完成的處理。

## 案例差異、重複來源與判讀限制 {#case-evidence-limits}

**可以確認的是，多個不同公開帳號回報了相似的冷排風扇／磁吸接頭異常；不能把文章或留言篇數直接當作故障顯卡台數。**核對時保留以下差異：

- **RGB 狀態不同。**部分案例燈光仍亮但風扇停止，本次最初則是三顆不亮、不轉。Ahmed0Alkathiri 另有一次本體風扇也停止的回報，不能把所有細節套成本次已確認狀態。
- **Solved 不等於已修妥。**angeli662 的頁面標為 Solved／Accepted Solution，但被採納的是版主的驅動排查與維修建議，沒有作者確認問題已解決。
- **相似文字可能參考其他貼文。**lxspector 與 DonShani 雖為不同帳號，主文段落高度相似，僅安裝方向及部分細節不同；不單靠這兩篇證明兩張不同故障顯卡。
- **跨站發文可能是同一個案。**[Digitec 的 Lloyd C.](https://www.digitec.ch/en/s1/questionandanswer/beware-when-sending-in-high-end-hardware-under-warranty-are-defective-cards-simply-retained-despite--920919?referrerProductId=54237902)與 [ROG 的 daxx219](https://rog-forum.asus.com/t5/gaming-graphics-cards/rog-astral-lc-rtx-5090-oc-minor-fan-connector-issue-declared/td-p/1156687)都描述冷排接頭接觸不良，以及瑞士零售商送修後發還原價額度、未歸還卡的情節，可能是同一個案，不另計。售後說法仍是當事人主張；ROG 客服要求 RMA 資訊查核，沒有公開確認此處理由華碩授權。

另有 [Reddit 的 carnagegtfo](https://www.reddit.com/r/ASUS/comments/1wqolmo/rog_astral_lc_rtx_5090_radiator_fans_randomly_go/)回報待機約 33 至 35°C 時冷排風扇突然高速，碰動磁吸接頭後恢復。這屬於相關的轉速控制異常，與停轉症狀不同；PWM 控制訊號間歇失效只是該作者推測，不能直接併成同一種已確認故障。

綜合第一手回報，可說**這類現象並非只有本次作者回報，值得華碩進一步說明接頭固定與接觸可靠性**。目前沒有總銷量、序號比對或統一維修檢測資料，仍不能據此推算故障率、認定特定批次問題、正式召回或全系列都有設計缺陷。熱造成失效、接點長度不足等論壇說法也屬持有人推論，尚未取得工程鑑定佐證。

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
- [ROG 論壇：Nartaq 的冷排風扇與 RGB 接頭失效回報](https://rog-forum.asus.com/t5/gaming-graphics-cards/rog-astral-lc-geforce-rtx-5090-32gb-gddr7-oc-fan-rgb-issue-fix/td-p/1112690)
- [ROG 論壇：angeli662 的 RGB 亮但冷排風扇停止回報](https://rog-forum.asus.com/t5/gaming-graphics-cards/rog-astral-lc-rtx-5090-radiator-fans-not-spinning/td-p/1140409)
- [ROG 論壇：Ahmed0Alkathiri 的停轉與轉速異常回報](https://rog-forum.asus.com/t5/gaming-graphics-cards/rog-astral-lc-rtx-5090-radiator-fans-not-spinning-due-to-loose/td-p/1143214)
- [ROG 論壇：ROGn97dhxc55gkq 的接合後暫時恢復與復發回報](https://rog-forum.asus.com/t5/gaming-graphics-cards/rog-astral-lc-geforce-rtx-5090-oc-32gb-rad-fans-stop-spinning/td-p/1153022)
- [Reddit：MrAskani 的冷排風扇異常與 RMA 後續](https://www.reddit.com/r/ASUSROG/comments/1kcqxeh/5090_rog_astral_lc_oc_radiator_power_issues/)
- [Reddit：YorVeX 的施力接頭恢復、放手後失效回報](https://www.reddit.com/r/ASUSROG/comments/1kcqxeh/comment/nglq4c6/)
- [Digitec：Lloyd C. 的冷排接頭與售後回報](https://www.digitec.ch/en/s1/questionandanswer/beware-when-sending-in-high-end-hardware-under-warranty-are-defective-cards-simply-retained-despite--920919?referrerProductId=54237902)
- [ROG 論壇：daxx219 的接頭送修與售後回報](https://rog-forum.asus.com/t5/gaming-graphics-cards/rog-astral-lc-rtx-5090-oc-minor-fan-connector-issue-declared/td-p/1156687)
- [Reddit：carnagegtfo 的冷排轉速暴衝與磁吸接頭回報](https://www.reddit.com/r/ASUS/comments/1wqolmo/rog_astral_lc_rtx_5090_radiator_fans_randomly_go/)
- [GPU Tweak III 官方頁面](https://www.asus.com/campaign/GPU-Tweak-III/tw/index.php)
