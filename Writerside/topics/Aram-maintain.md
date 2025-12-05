# ARAM 大混戰海克斯增幅 - ChatGPT 機器人建置與維護說明

本文件說明如何建立與維護「ARAM 大混戰海克斯增幅顧問」ChatGPT 機器人，以及相關知識庫的更新流程。

## 相關連結

- 🤖 **ChatGPT 機器人**：https://chatgpt.com/g/g-693125eb56948191ac6777f98b6eceb9-aram
- 🛠️ **GPTs 建立頁面**：https://chatgpt.com/gpts
- 📝 **巴哈姆特分享文章**：https://forum.gamer.com.tw/C.php?bsn=17532&snA=706284&tnum=1

---

## 1. ChatGPT 機器人建置指南

### 1.1 建立 GPT

1. 前往 [ChatGPT GPTs](https://chatgpt.com/gpts) 頁面
2. 點擊「建立」按鈕
3. 填寫基本資訊：
   - **名稱**：`Aram`
   - **說明**：`LoL ARAM 大混戰海克斯增幅顧問`

### 1.2 設定指令（Instructions）

將以下內容貼到「指令」欄位：

```text
你是一位「LoL ARAM 大混戰（ARAM Mayhem）海克斯增幅裝置顧問」。

【核心任務】
玩家會輸入英雄名稱（中文或英文），你要立即提供：
1. 該英雄的 Tier 排名（S/A/B/C/D）
2. 推薦的海克斯增幅裝置組合（按優先順序）
3. 簡短的選擇理由

【回答格式】
因為選完角色馬上就要開打，請用以下「重點先行」格式回覆：

---

## 🎮 [英雄名稱] - [Tier 等級]

### ⭐ 核心增幅（優先拿）
1. **[增幅名稱]**（[稀有度]）
2. **[增幅名稱]**（[稀有度]）
3. **[增幅名稱]**（[稀有度]）

### 💡 一句話打法
[10 字以內的核心策略]

---

<details>
<summary>📖 詳細說明（有空再看）</summary>

**定位**：[英雄定位與玩法風格]

**Prismatic 推薦**
- **[增幅名稱]**：[為什麼適合這個英雄]
- ...

**Gold / Silver 推薦**
- **[增幅名稱]**：[效果與適配理由]
- ...

**不推薦 / 地雷**
- [增幅名稱]：[為什麼不適合]

</details>

---

【查詢邏輯】
1. 優先查《英雄攻略索引》找該英雄的完整推薦
2. 若找不到，查《英雄 Tier 排名》確認強度，再查《Augment 對照表》依英雄類型推薦
3. 回答時使用繁體中文，語氣簡潔實戰向

【重要原則】
- 重點放最上面，詳細說明放 <details> 裡
- 不要含糊其詞，要給出具體的增幅名稱
- 先看英雄機制與玩法，再看稀有度
- 放大英雄既有強項優先，補短板其次
```

### 1.3 上傳知識庫

在「知識庫」區塊上傳以下檔案：

| 檔案 | 說明 |
|------|------|
| `Aram-kb.md` | **主要知識庫**（必須上傳） |

> **注意**：只需要上傳 `Aram-kb.md`，這是專門為 ChatGPT 設計的知識庫格式。

### 1.4 其他設定

- **對話啟動器**：可留空或設定常見問題
- **推薦的模型**：建議使用 GPT-4o 以獲得最佳效果

---

## 2. 檔案架構說明

### 2.1 檔案用途對照表

| 檔案 | 用途 | 上傳給 ChatGPT？ |
|------|------|-----------------|
| `Aram-kb.md` | ChatGPT 知識庫（機器人用） | ✅ **必須** |
| `Aram.md` | Writerside 網站文章（人類閱讀） | ❌ |
| `Aram.generated.md` | 自動生成的 Writerside 文章 | ❌ |
| `Aram-data.json` | 整合資料（給腳本用） | ❌ |
| `Aram-baha-raw.json` | 巴哈姆特原始留言 | ❌ |
| `Aram-blitz-augments.json` | Blitz 增幅資料（英文） | ❌ |
| `Aram-blitz-tierlist.json` | Blitz 英雄 Tier 資料 | ❌ |

### 2.2 資料流向圖

```
資料來源                原始資料 JSON              整合資料              輸出檔案
───────────────────────────────────────────────────────────────────────────────────
巴哈姆特討論串 ───→ Aram-baha-raw.json ──┐
                                         │
Blitz 增幅 ───────→ Aram-blitz-augments.json ├──→ Aram-data.json ──┬──→ Aram-kb.md
                                         │                        │   (ChatGPT 用)
Blitz Tier ───────→ Aram-blitz-tierlist.json ┘                    │
                                                                   └──→ Aram.generated.md
                                                                       (Writerside 用)
```

### 2.3 原始資料檔案說明

| 檔案 | 來源 | 內容 | 更新時機 |
|------|------|------|----------|
| `Aram-baha-raw.json` | 巴哈姆特 | 討論串原始留言（樓 + 留言） | 有新討論時 |
| `Aram-blitz-augments.json` | Blitz.gg | 增幅名稱、Tier、推薦英雄 | 版本更新時 |
| `Aram-blitz-tierlist.json` | Blitz.gg | 英雄 Tier 排名 | 版本更新時 |
| `Aram-data.json` | 整合 | 整合上述資料 + 人工標註 | 任一來源更新時 |

**優點**：
- 原始資料與整合資料分離，除錯時可追溯來源
- 不需重複爬取，節省 token
- 各來源可獨立更新

### 2.4 知識庫結構要求（Aram-kb.md）

為了讓 ChatGPT 能回答詳細的英雄攻略，`Aram-kb.md` 必須包含以下章節：

| 章節 | 內容 | 用途 |
|------|------|------|
| 英雄 Tier 排名 | S/A/B/C/D 分級 | 快速判斷英雄強度 |
| **英雄攻略索引** | 每個英雄的詳細推薦 | **核心章節** |
| Augment 對照表 | 增幅 → 適合英雄 | 反向查詢 |
| Bug / 坑點整理 | 已知問題 | 避雷用 |

#### 英雄攻略索引格式

每個英雄應包含以下資訊（以札克為例）：

```markdown
### 札克 Zac

- **Tier**：C
- **定位**：高機動坦克兼開團者，依賴位移與自我治療
- **核心關鍵字**：治療轉輸出、坦度、開團能力

**Prismatic 推薦**
- **死亡循環（Circle of Death）**：將自身治療量轉為範圍傷害，札克先天大量自我治療，這顆能把坦度轉化成輸出
- 任何增加最大生命、治療量或強化開團能力的稜鏡

**Gold / Silver 推薦**
- **黎明使者之決意**：低血量時回復 30% 最大生命，配合被動更難死
- **惡趣味**：硬控場時回復生命，開團同時補血
- 提供生命、護甲、魔抗、治療加成的增幅

**不推薦**
- 純輸出型增幅（札克不是 Carry）
- 需要疊層的任務型增幅（坦克難完成）
```

> **重點**：這個格式讓 ChatGPT 能回答「重點 + 詳細說明」兩層資訊。

---

## 3. 資料來源與抓取方法

### 3.1 巴哈姆特討論串

- 主題：`【討論】隨機單中：大混戰 討論串`
- 基底網址範例：
  - `https://forum.gamer.com.tw/C.php?bsn=17532&snA=705476&page=1`
  - `page=2, 3, ...` 依此類推。
- 建議策略：
  - 初版整理：抓 1～15 頁。
  - 後續更新：
    - 可先偵測最大頁數，只抓「上次整理後」的新頁（例如 16～最新）。
    - 或視情況重新抓 1～最新頁（較耗 token，但最保險）。

### 3.2 Blitz ARAM Mayhem 資料

- Augments：`https://blitz.gg/lol/aram-mayhem-augments`
  - 取得各顆海克斯的名稱、稀有度、描述、Tier 排名（S/A/B/C/D）、推薦英雄。
  - **重要**：頁面右上角可切換語言為「繁體中文」，切換後所有增幅名稱、描述、英雄名稱都會顯示台服正確的繁體中文。
  - 資料存放：`Aram-blitz-augments.json`（英文）、`Aram-data.json` 的 `augments_summary`（繁體中文）
- Tier List：`https://blitz.gg/lol/tierlist/aram-mayhem`
  - 取得各英雄在 ARAM Mayhem 模式下的 Tier（S/A/B/C/D）排名。
  - 資料存放：`Aram-blitz-tierlist.json`

#### 3.2.1 抓取增幅資料的方法

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

#### 3.2.2 抓取英雄 Tier List 的方法

1. **使用 Chrome DevTools MCP**：
   - 開啟 `https://blitz.gg/lol/tierlist/aram-mayhem`
   - 確認語言為「繁體中文」
   - 使用 JavaScript 評估抓取 DOM 內容：
     ```javascript
     (() => {
       const result = {
         patch: "25.24 (15.24)", // 從頁面標題取得
         source: "https://blitz.gg/lol/tierlist/aram-mayhem",
         last_updated: new Date().toISOString().split('T')[0],
         tiers: { S: [], A: [], B: [], C: [], D: [] }
       };

       const links = Array.from(document.querySelectorAll('a[href*="/champions/"][href*="/aram-mayhem"]'));

       links.forEach(link => {
         const href = link.getAttribute('href');
         const match = href.match(/\/champions\/([^/]+)\/aram-mayhem/);
         if (match) {
           const name_en = match[1];
           const name_zh = link.textContent.trim();
           // 找到前面最近的 h2 標題判斷 Tier
           let el = link;
           let tier = null;
           while (el && !tier) {
             el = el.previousElementSibling || el.parentElement;
             if (el && el.tagName === 'H2') {
               const t = el.textContent.trim();
               if (['S', 'A', 'B', 'C', 'D'].includes(t)) tier = t;
             }
           }
           if (tier && result.tiers[tier] && !result.tiers[tier].some(c => c.name_en === name_en)) {
             result.tiers[tier].push({ name_zh, name_en });
           }
         }
       });

       return result;
     })()
     ```

2. **資料存放**：
   - 抓取後存入 `Writerside/topics/Aram-blitz-tierlist.json`
   - 同時更新 `Aram-data.json` 的 `coverage.blitz_tierlist` 區塊

---

## 4. 從巴哈抓取與解析留言的邏輯

### 4.1 巴哈姆特論壇結構

巴哈姆特論壇採用三層結構：

```
頁面 (Page)
├── 樓 (Floor/Post) - 每頁約 20 樓
│   ├── 主文內容
│   └── 留言區 (Comments) - 預設隱藏，需展開
│       ├── B1 留言
│       ├── B2 留言
│       └── ... (可能有數十則)
```

**重要**：每樓下方的留言預設是隱藏的，會顯示「還有 X 則留言」按鈕。

### 4.2 抓取步驟（使用腳本 + AJAX API）

腳本 `scrape_bahamut_aram.py` 已整合留言抓取功能，透過巴哈姆特的 AJAX API 自動取得所有留言：

**留言 API**：
```
GET https://forum.gamer.com.tw/ajax/moreCommend.php?bsn=17532&snB={樓層ID}&returnHtml=1
```

**執行指令**：
```bash
# 完整抓取（包含留言）
python3 scripts/scrape_bahamut_aram.py --force

# 只更新留言（不抓取新樓層）
python3 scripts/scrape_bahamut_aram.py --comments-only

# 快速抓取（不抓留言）
python3 scripts/scrape_bahamut_aram.py --no-comments
```

**腳本會自動**：
1. 抓取每頁的樓層主文
2. 從樓層連結取得 `snB`（樓層 ID）
3. 呼叫 AJAX API 取得該樓的所有留言
4. 解析 HTML 回應中的 `data-comment` JSON 屬性
5. 儲存到 `Aram-baha-raw.json`

### 4.3 資料結構

`Aram-baha-raw.json` 的樓層結構：

```json
{
  "page": 1,
  "floor": "樓主",
  "snB": "6276939",
  "author": "猛姜",
  "time": "2025-10-25 21:22:49",
  "content": "大混戰模式因為沒有符文的關係...",
  "comments": [
    { "floor": "B1", "author": "松鼠放電", "content": "雪球兔子有奇效" },
    { "floor": "B2", "author": "那泥溝咧", "content": "確定有像競技場那樣的免控嗎？" },
    ...
  ]
}
```

| 欄位 | 說明 |
|------|------|
| `snB` | 樓層 ID，用於呼叫留言 API |
| `comments` | 該樓的所有留言（透過 AJAX API 取得） |

### 4.4 抽取海克斯相關資訊

- 只處理含有明確「海克斯增幅裝置」資訊的句子
- 純抱怨隊友／炫耀戰績的留言可忽略
- **重點關注**：
  - 英雄 + 增幅組合（如「札克 + 死亡循環」）
  - 增幅效果說明或 Bug 回報
  - 裝備搭配建議（如「終末戰戟 + 爆擊治療」）
  - 不推薦的增幅（避雷資訊）

---

## 5. 中介資料與生成流程

### 5.1 中介 JSON 結構

所有資料彙總到 `Aram-data.json`，主要欄位：

| 欄位 | 說明 |
|------|------|
| `coverage` | 記錄資料來源與抓取範圍 |
| `augments_summary` | 從 Blitz 抓取的增幅資料（繁體中文） |
| `hero_synergy` | 英雄 × 增幅搭配（**詳細結構見下方**） |
| `raw_floors` | 巴哈原始留言（供後續萃取用） |

#### hero_synergy 結構（重要）

為了讓知識庫能呈現完整的英雄攻略，`hero_synergy` 每個英雄應包含：

```json
{
  "hero": "札克",
  "hero_en": "Zac",
  "tier": "C",
  "role": "高機動坦克兼開團者，依賴位移與自我治療",
  "keywords": ["治療轉輸出", "坦度", "開團能力"],
  "prismatic": [
    {
      "name": "死亡循環",
      "name_en": "Circle of Death",
      "reason": "將自身治療量轉為範圍傷害，札克先天大量自我治療，這顆能把坦度轉化成輸出"
    },
    {
      "name": "蛋白飲",
      "name_en": "Protein Shake",
      "reason": "根據物防魔防增加治療量，坦裝越多回越多"
    }
  ],
  "gold_silver": [
    {
      "name": "黎明使者之決意",
      "reason": "低血量時回復 30% 最大生命，配合被動更難死"
    },
    {
      "name": "惡趣味",
      "reason": "硬控場時回復生命，開團同時補血"
    }
  ],
  "not_recommended": [
    {
      "name": "純輸出型增幅",
      "reason": "札克不是 Carry"
    }
  ],
  "sources": [
    { "from": "Bahamut", "page": 5, "floor": 23 },
    { "from": "Aram.md", "section": "3.3" }
  ]
}
```

> **關鍵**：這個結構讓生成腳本可以自動產出「重點 + 詳細說明」兩層資訊的知識庫。

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

## 6. Writerside 網站文章

除了 ChatGPT 知識庫外，本專案也維護給人類閱讀的 Writerside 文章：

### 6.1 文章檔案

| 檔案 | 說明 |
|------|------|
| `Aram.md` | 手動撰寫的攻略文章（人類閱讀用） |
| `Aram.generated.md` | 從 JSON 自動生成的文章 |

### 6.2 資料覆蓋標記

`Aram.md` 開頭包含資料覆蓋標記，用於追蹤已處理的巴哈頁數：

```markdown
<!--
ARAM-DATA-COVERAGE:
{
  "bahamut": { "from_page": 1, "to_page": 15, "last_floor": 30 },
  "last_updated": "2025-12-04"
}
-->
```

---

## 7. 更新流程總結

### 7.1 環境設定（首次執行）

macOS 需要使用虛擬環境：

```bash
# 建立虛擬環境（只需執行一次）
python3 -m venv .venv

# 啟用虛擬環境
source .venv/bin/activate

# 安裝依賴
pip install requests beautifulsoup4
```

之後每次執行腳本前，記得先啟用虛擬環境：

```bash
source .venv/bin/activate
```

### 7.2 完整更新流程（腳本執行順序）

```bash
# 1. 抓取巴哈姆特最新資料（增量更新，只抓新內容）
python3 scripts/scrape_bahamut_aram.py

# 2. 從原始資料萃取英雄/增幅資訊，更新到 Aram-data.json
python3 scripts/extract_aram_insights.py

# 3. 生成 ChatGPT 知識庫
python3 scripts/generate_aram_kb_from_json.py

# 4. 生成 Writerside 文章
python3 scripts/generate_aram_from_json.py
```

### 7.3 腳本說明

| 腳本 | 輸入 | 輸出 | 說明 |
|------|------|------|------|
| `scrape_bahamut_aram.py` | 巴哈姆特網頁 | `Aram-baha-raw.json` | 增量抓取，記錄進度 |
| `extract_aram_insights.py` | `Aram-baha-raw.json` | `Aram-data.json` | 萃取英雄/增幅資訊 |
| `generate_aram_kb_from_json.py` | `Aram-data.json` | `Aram-kb.md` | 生成 ChatGPT 知識庫 |
| `generate_aram_from_json.py` | `Aram-data.json` | `Aram.generated.md` | 生成 Writerside 文章 |

### 7.4 增量更新選項

```bash
# 預設：從上次進度繼續
python3 scripts/scrape_bahamut_aram.py

# 只抓新頁面
python3 scripts/scrape_bahamut_aram.py --new-only

# 強制重新抓取全部
python3 scripts/scrape_bahamut_aram.py --force

# 指定頁面範圍
python3 scripts/scrape_bahamut_aram.py --from-page 10 --to-page 15
```

### 7.5 上傳 ChatGPT 知識庫

1. 前往 [ChatGPT GPTs](https://chatgpt.com/gpts)
2. 編輯你的 GPT
3. 在「知識」區塊上傳 `Writerside/topics/Aram-kb.md`
4. 儲存並發布

### 7.6 更新 Writerside 文章

```bash
# 推送到 GitHub，自動部署到 GitHub Pages
git add .
git commit -m "更新 ARAM 資料"
git push
```
