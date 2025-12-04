# Aram 大混戰海克斯增幅維護說明（給未來的 AI / 作者）

> 本文件說明：之後若要重新爬巴哈 / Blitz 的資料來更新 `Aram.md`，請依照以下流程操作。

## 1. 資料來源與範圍

### 1.1 巴哈姆特討論串

- 主題：`【討論】隨機單中：大混戰 討論串`
- 基底網址範例：
  - `https://forum.gamer.com.tw/C.php?bsn=17532&snA=705476&page=1`
  - `page=2, 3, ...` 依此類推。
- 建議策略：
  - 初版整理：抓 1～15 頁。
  - 後續更新：
    - 可先偵測最大頁數，只抓「上次整理後」的新頁（例如 16～最新）。
    - 或視情況重新抓 1～最新頁（較耗 token，但最保險）。

### 1.2 Blitz ARAM Mayhem 資料

- Augments：`https://blitz.gg/lol/aram-mayhem-augments`
  - 取得各顆海克斯的名稱、稀有度、描述、Tier 排名（S/A/B/C/D）、推薦英雄。
  - **重要**：頁面右上角可切換語言為「繁體中文」，切換後所有增幅名稱、描述、英雄名稱都會顯示台服正確的繁體中文。
- Tier List：`https://blitz.gg/lol/tierlist/aram-mayhem`
  - 取得各英雄在 ARAM Mayhem 模式下的 Tier（S/A/B…）與大致定位。

#### 1.2.1 抓取繁體中文資料的方法

由於 Blitz.gg 是 JavaScript 渲染的 SPA 頁面，無法直接用 `requests` 或 `web-fetch` 抓取，需要使用瀏覽器自動化工具：

1. **使用 Chrome DevTools MCP**（推薦）：
   - 開啟 `https://blitz.gg/lol/aram-mayhem-augments`
   - 點擊右上角設定圖示 → 選擇「繁體中文」→ 等待頁面重新載入
   - 使用 JavaScript 評估抓取 DOM 內容：
     ```javascript
     // 抓取所有增幅資料
     Array.from(document.querySelectorAll('[class*="AugmentRow"]')).map(row => ({
       name_zh: row.querySelector('[class*="Name"]')?.textContent?.trim(),
       tier: row.querySelector('[class*="Tier"]')?.textContent?.trim(),
       description: row.querySelector('[class*="Description"]')?.textContent?.trim(),
       champions: Array.from(row.querySelectorAll('[class*="Champion"] img'))
         .map(img => img.alt).slice(0, 5)
     }))
     ```

2. **稀有度判斷**：
   - 頁面上增幅按稀有度分組顯示（Prismatic / Gold / Silver）
   - 可透過 DOM 結構或 CSS class 判斷當前增幅屬於哪個稀有度區塊

3. **資料欄位對應**：
   | Blitz 欄位 | JSON 欄位 | 說明 |
   |-----------|----------|------|
   | 增幅名稱 | `augment_name_zh` | 繁體中文名稱（如「巨人殺手」） |
   | Tier | `tier` | S/A/B/C/D 排名 |
   | 描述 | `summary` | 增幅效果說明 |
   | 推薦英雄 | `strong_for` | Top 5 推薦英雄（繁體中文） |
   | 稀有度 | `rarity` | Prismatic / Gold / Silver |

---

## 2. 從巴哈抓取與解析留言的邏輯

### 2.1 抓取

1. 對目標頁面（`page=N`）使用網頁抓取工具取得 HTML。
2. 僅保留「主文 + 各樓層留言」區塊：
   - 含：樓層編號、作者、時間、GP、留言內容。
   - 忽略：JS、CSS、廣告、導覽列等。

### 2.2 結構化留言

把每一則留言整理成類似下列結構（示意）：

```json
{
  "page": 3,
  "floor": 41,
  "author": "某ID",
  "time": "2024-01-01 12:34",
  "content": "這則留言的純文字內容（可視情況去掉引用與表情圖片）。"
}
```

> 目的：讓之後可以在所有 `content` 中搜尋特定海克斯名稱、英雄名稱，做分類與統計。

---

## 3. 從留言中抽出「海克斯相關資訊」

### 3.1 抽取邏輯

- 只處理含有明確「海克斯增幅裝置」資訊的句子，例如：
  - 描述效果、觸發條件。
  - 搭配哪些英雄、哪種出裝。
  - 實戰體感（強、弱、雷、娛樂流）。
  - Bug、翻譯錯誤、任務失效等。
- 純抱怨隊友／炫耀戰績的留言可忽略。

### 3.2 建議資料結構

每偵測到一個有意義的「海克斯資訊」，建立一筆記錄，欄位包括：

```json
{
  "augment_name_zh": "拔劍吧",
  "augment_name_en": null,
  "rarity": "Prismatic | Gold | Silver | Unknown",
  "mentioned_heroes": ["汎", "葛雷夫"],
  "usage_type": ["核心玩法", "娛樂流派"],
  "effects_summary": "遠程改近戰，近戰普攻變強，可搭配高爆擊、高攻速裝出刺客型打法。",
  "pros": ["對特定射手能大幅提高進場瞬間爆發"],
  "cons": ["改成近戰導致有些技能判定變難用"],
  "bugs_or_remarks": null,
  "source": {
    "from": "Bahamut",
    "page": 3,
    "floor": 41,
    "url": "https://forum.gamer.com.tw/C.php?bsn=17532&snA=705476&page=3"
  }
}
```

> 同一則留言若提到多顆海克斯，請拆成多筆記錄，各自標註來源頁與樓層。

---

## 4. 從 Blitz 抽出「數據面資訊」

### 4.1 Augments 頁面

- 對每顆 Augment 抽出（**建議切換為繁體中文後抓取**）：
  - `augment_name_zh`：繁體中文名稱（如「巨人殺手」、「靈光一閃」）
  - `rarity`：Prismatic / Gold / Silver
  - `tier`：S / A / B / C / D（Blitz 評分）
  - `description`：增幅效果說明（繁體中文）
  - `strong_for`：推薦英雄列表（繁體中文，如「剛普朗克」、「雷茲」）

> **注意**：Blitz 頁面是 JavaScript 渲染，需使用瀏覽器自動化工具抓取。
> 詳見 1.2.1 節的抓取方法說明。

### 4.2 Tier List 頁面

- 對每個英雄抽出：
  - `hero_name_en` / `hero_name_zh`（若可對照）
  - `tier`（S / A / B…）
  - `role`（射手、法師、坦克、刺客等，若頁面有標示）

---

## 5. 彙總成「中介資料」後再生成 Markdown

### 5.1 中介 JSON 建議結構

建議先彙總成一份中介資料，再依據當前是否已存在 `Aram.md` 來「建立或更新」該檔案，以利未來重複執行。範例：

```json
{
  "coverage": {
    "bahamut": {
      "bsn": 17532,
      "snA": 705476,
      "from_page": 1,
      "to_page": 15,
      "last_updated": "2025-12-04"
    },
    "blitz": {
      "url": "https://blitz.gg/lol/aram-mayhem-augments",
      "language": "zh-TW",
      "augment_count": 156,
      "last_updated": "2025-12-04"
    }
  },
  "augments_summary": [
    {
      "augment_name_zh": "巨人殺手",
      "rarity": "Prismatic",
      "tier": "S",
      "strong_for": ["剛普朗克", "莉莉亞", "婕莉", "燼", "杰西"],
      "summary": "體型變小，增加跑速，並根據目標英雄與你的體型差距造成額外傷害。",
      "bugs": []
    },
    {
      "augment_name_zh": "基本功夫",
      "rarity": "Prismatic",
      "tier": "D",
      "strong_for": ["雷茲", "塔莉雅", "剛普朗克", "逆命", "潘森"],
      "summary": "增加技能傷害、治療、護盾，並獲得技能加速，但無法使用大絕。",
      "bugs": []
    }
  ],
  "hero_synergy": [
    {
      "hero": "札克",
      "hero_en": "Zac",
      "core_augments": ["死亡循環", "回血類海克斯"],
      "build_notes": "全坦 + 高回血裝，靠死亡循環把治療量轉為爆炸輸出。"
    }
  ],
  "bugs_and_traps": [
    {
      "type": "bug",
      "title": "升級彎刀說明與實際不符",
      "detail": "描述寫命脈系列被動冷卻減半，但實際上沒有生效。"
    }
  ],
  "macro_tips": [
    "前中期以線權與清線為優先，爆水晶後特別重要",
    "大後期注意關鍵主 C 的買一送一概念（一起死一起生）"
  ],
  "raw_floors": [
    { "page": 1, "floor": 1, "author": "xxx", "content": "..." }
  ]
}
```

> **欄位說明**：
> - `coverage`：記錄資料來源與抓取範圍，方便追蹤更新進度
> - `augments_summary`：從 Blitz 抓取的增幅資料（繁體中文）
>   - `tier`：Blitz 評分（S/A/B/C/D）
>   - `strong_for`：推薦英雄（繁體中文名稱）
> - `hero_synergy`：從巴哈討論串萃取的英雄 × 增幅搭配
> - `raw_floors`：巴哈原始留言（供後續萃取用）

### 5.2 Python 腳本說明

專案中已建立以下 Python 腳本，用於自動化資料抓取與生成流程：

| 腳本 | 用途 |
|------|------|
| `scripts/scrape_bahamut_aram.py` | 爬取巴哈討論串，存入 `Aram-data.json` 的 `raw_floors` |
| `scripts/extract_aram_insights.py` | 從 `raw_floors` 萃取英雄 × 增幅資訊 |
| `scripts/merge_blitz_augments.py` | 合併 Blitz 增幅資料（需先手動抓取繁體中文資料） |
| `scripts/generate_aram_from_json.py` | 從 JSON 生成 `Aram.generated.md`（Writerside 文章） |
| `scripts/generate_aram_kb_from_json.py` | 從 JSON 生成 `Aram-kb.md`（ChatGPT 知識庫） |

#### 執行流程

```bash
# 進入專案目錄
cd /path/to/writerside

# 啟動虛擬環境
source .venv/bin/activate

# 1. 抓取巴哈資料（例如抓 1~15 頁）
python3 scripts/scrape_bahamut_aram.py --from-page 1 --to-page 15

# 2. 萃取結構化資料
python3 scripts/extract_aram_insights.py

# 3. 重新生成 Markdown
python3 scripts/generate_aram_from_json.py
python3 scripts/generate_aram_kb_from_json.py
```

> **注意**：Blitz 繁體中文資料需透過瀏覽器自動化抓取（見 1.2.1 節），
> 抓取後可使用 `merge_blitz_augments.py` 合併到 `Aram-data.json`。

### 5.3 生成 / 更新 Aram.md 的邏輯

1. 檢查 `Writerside/topics/Aram.md` 是否存在與是否有實質內容：
   - 若「檔案不存在」或內容仍為預設 placeholder（例如只有 `# Aram` / `Start typing here...`），則視為**首次建立**：
     - 以建議的基礎章節結構產生新檔案，例如：
       - 模式簡介與規則說明
       - 海克斯選擇原則
       - 英雄 × 海克斯推薦表
       - Blitz Augments 結構化節錄
       - Bug / 坑點整理
       - 如何搭配 Blitz / 其它工具說明
     - 並在檔案最開頭加上一段「資料覆蓋標記」（見 5.4 節），紀錄目前已處理的巴哈頁數與樓層。
   - 若「檔案已存在且有內容」，則視為**更新既有文件**：
     - 以現有 `Aram.md` 的章節結構為基準（模式簡介、選擇原則、強勢海克斯、Bug & 坑點、英雄搭配、團隊觀念、Blitz 使用方式）。
     - 使用中介 JSON 更新其中的：
       - 新增或調整的強勢海克斯與代表玩法。
       - 新發現的 Bug / 坑點（例如新版本任務或翻譯問題）。
       - 英雄與海克斯的組合（hero_synergy）。
     - 盡量保留原本文章的寫作風格（中文、略偏口語、實戰向），只更新內容本身。

2. 無論是首次建立或更新，都應維護 `Aram.md` 開頭的「資料覆蓋標記」區塊，使其反映目前中介 JSON 已涵蓋的巴哈頁數與樓層（見 5.4、5.5 節）。
3. 用「局部補丁（apply_patch）」方式建立或更新 `Writerside/topics/Aram.md`，不要動到其他 Writerside 設定檔。

---

### 5.4 Aram.md 開頭的資料覆蓋標記格式

建議在 `Aram.md` 檔案的最開頭（主標題前或後）保留一段**機器與人類皆易讀的資料覆蓋標記**，用來記錄目前已整理到巴哈該串的哪一頁哪一樓。例如：

```markdown
<!--
ARAM-DATA-COVERAGE:
{
  "bahamut": {
    "bsn": 17532,
    "snA": 705476,
    "from_page": 1,
    "to_page": 15,
    "last_page": 15,
    "last_floor": 30,
    "last_url": "https://forum.gamer.com.tw/C.php?bsn=17532&snA=705476&page=15"
  },
  "last_updated": "2025-01-01"
}
-->
> 資料來源覆蓋範圍（巴哈 ARAM 大混戰討論串）
> - 已處理頁數：1–15 頁
> - 最後處理樓層：第 15 頁 第 30 樓
> - 最後更新時間：2025-01-01
```

- 上方 HTML 註解區塊中的 JSON 方便未來的 AI / 工具程式自動解析「已處理到哪一頁哪一樓」。
- 下方引言區塊則是給人類作者 / 讀者快速知道目前整理進度用。

未來每次重新整理資料（無論是全量重跑或增量補充）後，都應同步更新這一段標記。

### 5.5 依資料覆蓋標記進行「增量爬取」的邏輯

當下次要更新資料時，可以先讀取 `Aram.md` 開頭的 `ARAM-DATA-COVERAGE` 註解，決定要從哪裡開始補抓：

1. 嘗試在 `Aram.md` 中尋找 `ARAM-DATA-COVERAGE:` 這段 JSON 註解：
   - 若找到且能成功解析出 `last_page`、`last_floor` 等欄位：
     - 則 **只需要抓取「該樓層之後」的新留言**：
       - 對於 `page > last_page` 的所有頁面：抓取全部樓層。
       - 對於 `page == last_page` 的那一頁：只處理「樓層編號 > last_floor」的留言。
   - 若找不到這段註解或格式無法解析：
     - 則視為「首次或未知狀態」，**從 `page=1` 開始全量抓取到最新頁**。

2. 將新抓到的留言再依 3.2 節的資料結構抽取海克斯相關資訊，納入最新一版中介 JSON 中：
   - 可以在中介 JSON 內額外紀錄這次「最後處理的 page 與 floor」，供之後覆寫 `ARAM-DATA-COVERAGE` 使用。

3. 完成 `Aram.md` 的建立或更新後：
   - 覆寫檔案開頭的 `ARAM-DATA-COVERAGE` 區塊：
     - 更新 `from_page` / `to_page`（若首次建立則 `from_page` 通常為 1）。
     - 更新 `last_page` / `last_floor` 為這次實際處理到的最後一則留言位置。
     - 更新 `last_url` 為該樓層所在頁面的 URL。
     - 更新 `last_updated` 為本次更新日期（ISO 格式即可，例：`2025-01-01`）。

如此一來，即使你中途把舊的 `Aram.md` 刪除、整個重跑，只要新一版照規格重建並寫入最新的覆蓋標記，
下一次要做「增量更新」時，AI 只要讀這段標記就知道從巴哈哪一頁哪一樓開始往後補就好。

---

## 6. ChatGPT 專案用 ARAM 知識庫生成 Prompt（新版）

這一段是「直接給 ChatGPT 專案用」的長 prompt 範本，目標是：

- **輸入**：我會把 `Writerside/topics/Aram.md`（以及其他相關筆記）當作 context 給 ChatGPT。
- **輸出**：請 ChatGPT 幫我生成一份「給聊天機器人使用的 ARAM 大混戰知識庫 Markdown」，之後當作聊天上下文，
  讓我問「這把隨機到某英雄，有哪些好用的海克斯增幅裝置組合？」時，可以立刻查表給出具體建議，而不是含糊其詞。

可以直接把下面這整段貼到 ChatGPT 專案的 system prompt / instructions：

```text
你現在是一位「LoL ARAM 大混戰（ARAM Mayhem）海克斯增幅裝置顧問 & 知識庫產生器」，
也是一個專門幫我生成靜態知識庫（KB）的工具。

【你的輸入與資料來源】

我會在同一個對話 / 專案 context 裡提供給你以下檔案內容（以繁體中文為主）：

1. `Writerside/topics/Aram.md`
   - 內含：
     - 模式規則與特殊機制說明（例如等級 1/6/11 選增幅、爆水晶後雙超兵、近戰/遠程 buff、反連控機制等）。
     - 海克斯增幅選擇的大原則（放大優勢、看英雄機制勝過看稀有度等）。
     - **英雄 × 海克斯推薦表**（部分代表英雄已經列出：雷茲、剛普拉克、札克、賽恩、煞蜜拉、吉茵珂絲、伊澤瑞爾、凱特琳、燼、汎、蒙多、樹人、瑪爾札哈…）。
     - **Blitz ARAM Mayhem Augments 的結構化節錄表**（包含常見稜鏡增幅：Draw Your Sword / Back To Basics / Circle of Death / Protein Shake / Omni Soul / Infernal Conduit / Giant Slayer / Jeweled Gauntlet / Dual Wield / Final Form / Scopiest Weapons / Tap Dancer / Ultimate Revolution / Trueshot Prodigy / Biggest Snowball Ever / Snowball Roulette / Sneakerhead / Pandora's Box / King Me / Upgrade Mikael's Blessing 等；
       以及一些重要的 Gold / Silver 增幅摘要：Bread And Butter、Recursion、Magic Missile、Skilled Sniper、Critical Rhythm、Firebrand、Perseverance、Tank Engine、Executioner、Witchful Thinking、Deft、Goredrink、Infernal Soul、Ocean Soul、Mountain Soul、ADAPt、escAPADe…）。
     - 各種 Bug / 坑點與翻譯雷區（如升級彎刀描述與實作不符、任務/疊層問題等）。

未來我也可能加入其他輔助說明檔，但 **你在這個任務中必須優先以 `Aram.md` 內的資訊為主**，
把那份整理過的內容轉寫成「對聊天機器人友善的知識庫」。

【你的目標】

請根據我提供的 context（特別是 `Aram.md`）產生一份 **單一 Markdown 文件（使用繁體中文）**，
內容要能被之後的 ChatGPT 專案當作「只讀知識庫」，來回答這類問題：

- 「這把隨機到 XX 英雄，在 ARAM 大混戰模式下，我要怎麼選海克斯增幅裝置？」
- 「現在等級 6 / 11 抽到 A / B / C 三個增幅，對這個英雄來說該怎麼排序？」

重點要求：

1. **不要含糊其詞**：回答時要能直接說出具體、明確的海克斯名稱（中/英文）、優先順序和理由，不可以只說「選適合你英雄的輸出增幅」。
2. **盡量英雄化、具體化**：
   - 對於 `Aram.md` 已經整理過的英雄，請給出 **清晰的推薦清單**（而不是只有抽象原則）。
   - 一個英雄至少要有 2～3 顆優先稜鏡、3～5 顆常見 Gold/Silver 好選擇；如果真的很少，就把能找到的全部列出並說明。
3. **統一結構，方便未來 GPT 查表**：
   - 請使用固定的 Markdown 結構與小節標題，讓未來聊天模型可以用關鍵字檢索特定英雄 / 增幅。
4. **嚴格基於提供的 context，不要亂發明**：
   - 你可以合理推論「哪類英雄適合哪種增幅」，但 **不要創造實際遊戲中不存在的 Augment 名稱或效果**。
   - 如果在 context 裡找不到某英雄的明確資訊，可以退一步給「依英雄類型的建議」，但請明講是類型推論，不要假裝有數據支持。

【輸出格式與章節規劃】

請輸出一份 Markdown 文件，建議包含以下幾個主要章節（標題文字可以微調，但請保持結構與語意）：

1. 《查詢說明（給未來 GPT 看）》
   - 用 3～5 行說明：未來聊天模型在使用這份 KB 時，應該如何查表與解讀權重。
   - 明講：
     - 優先查「英雄 × 海克斯建議索引」。
     - 找不到英雄時，可以退而用「英雄類型 × 海克斯」的建議。
     - Augment 專章則是從「增幅 → 適合英雄 / 流派」反查。

2. 《英雄 × 海克斯建議索引》

   - 這一章是 **最重要的核心**，請對每個英雄建立獨立小節。
   - 對 `Aram.md` 已經有列出的英雄，必須至少包含：

   範例結構（以雷茲為例）：

   ### 英雄：雷茲 Ryze

   - Blitz ARAM Mayhem Tier：S / A / B...（如果 `Aram.md` 或其他 context 沒有，請標註為 `Unknown`）
   - 主要定位：例如「持續輸出型法師、短 CD 技能連發」
   - 建議玩法關鍵字：例如「短 CD Q 連發、黏著打、配合坦克前排」

   - 建議海克斯（請分成 Prismatic、Gold/Silver，並對每顆標註等級與理由）：

     - **Prismatic**
       - `Back To Basics（基本功）` — **T0 核心**  
         理由：根據 Aram.md，中後期雷茲幾乎不靠大絕開團，而是靠 Q/W/E 高頻率輸出；基本功大幅提升這三招的傷害與急速，是雷茲最關鍵的稜鏡之一。
       - `Omni Soul` — T1 推薦  
         理由：給予多種龍魂效果，整體提升輸出與續戰，適合雷茲這種持續作戰型角色。
       - ...（再補充 1～2 顆，如 Infernal Conduit 等，依照 Aram.md 實際內容）

     - **Gold / Silver**
       - `Recursion` — T1 推薦  
         理由：提供大量泛用技能急速，與雷茲的短 CD 技能機制高度相容。
       - `Bread And Butter` — T1 推薦  
         理由：加速 Q 技能冷卻，使主力輸出更密集。
       - `Witchful Thinking` — T2 可用  
         理由：單純補 AP，雖然沒有特別連動，但在缺乏更好選擇時依然合理。
       - ...

   - 不推薦 / 僅娛樂增幅（可選，但建議列出明顯雷點）：
     - `Sneakerhead（球鞋收藏家）` — Fun 娛樂  
       理由：主要提供任務鞋娛樂玩法，對雷茲整體強度幫助有限，除非你只是想玩有趣的移動速度套路。

   - 最後用 1～2 句話總結：
     - 例如：「雷茲優先考慮所有能提升 Q/W/E 輸出與技能急速的增幅，其次才是純 AP 或泛用型防禦增幅。」

   - 請對 `Aram.md` 表中已有的每位英雄都依此格式補滿（如果 context 中有更多英雄，也一併處理）。

3. 《Augment → 英雄／類型 對照表》

   - 以「每顆增幅」為主軸，建立另一種查詢視角，方便未來聊天模型從「已抽到的增幅」反推哪些英雄適合。
   - 每顆增幅的小節建議格式（以 Draw Your Sword 為例）：

   ### Augment：Draw Your Sword（拔劍吧）

   - 稀有度：Prismatic
   - 功能摘要：例如「將射手轉為近戰，依照放棄射程給予 AD / 攻速 / 血量 / 吸血 / 移速加成」。
   - 適合英雄類型：例如「近戰輸出射手 / 戰士」，可列舉幾個代表英雄（Samira、Sivir 近戰流、Jhin 娛樂爆發流…）。
   - 推薦等級：例如「整體評價：T0 / T1 / T2 / Fun」，可以根據 `Aram.md` 與 Blitz 資料合理歸類。
   - 協同玩法關鍵字：例如「拔劍射手、近戰爆發流、全能吸血疊高」。
   - 注意事項 / 雷點：例如「對高度依賴射程的 poke 射手常規玩法來說，會犧牲過多優勢，不建議。」

   - 這個章節中，請優先處理 `Aram.md` 內已有整理的稜鏡與金銀增幅；若有餘裕可延伸到更多 Augments，但請確保不要杜撰不存在的效果。

4. 《模式與增幅整體原則摘要》（可簡短）

   - 用條列方式再濃縮一次最關鍵的「通則」，例如：
     - 先看英雄機制與玩法，再看稀有度。
     - 爆水晶後每波雙超兵 → 清線與線權非常重要。
     - 坦克並非無用，但要與回血 / 护盾 / 轉傷害增幅與裝備搭配。
   - 這一章的目的，是給未來聊天模型在解釋建議時可以引用的「說明文字素材」，
     但真正的推薦邏輯應該優先來自前面兩章的結構化清單。

【其它約束】

- 語言全部使用「台灣正體中文」，技能 / 英雄 / 增幅名稱同時保留英文原名以利查找（例如：雷茲 Ryze、Back To Basics（基本功））。
- 若你需要自行歸納 Augment 的「強度等級」或「適合類型」，請以我提供的 `Aram.md` 內容為主，再輔以一般 LoL ARAM 常識推論；
  不要隨意捏造完全沒有根據的結論。
- 產生的 Markdown 應該 **可以獨立閱讀**，也就是說未來聊天模型只看這份文件就能理解建議邏輯，
  不需要再回頭看這個 Prompt 或其他說明。

請依以上規格，產出最終的「ARAM 大混戰海克斯增幅知識庫」Markdown。
```

> 備註：若未來 Riot 或 Blitz 大幅更改 Augments / ARAM Mayhem 機制，
> 可以先更新 `Writerside/topics/Aram.md` 本身的內容，再重新用這個 Prompt 生成新版知識庫。

