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
  - 取得各顆海克斯的英文名稱、稀有度、描述、簡要勝率／出場率（如有）。
- Tier List：`https://blitz.gg/lol/tierlist/aram-mayhem`
  - 取得各英雄在 ARAM Mayhem 模式下的 Tier（S/A/B…）與大致定位。

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

- 對每顆 Augment 抽出：
  - `augment_name_en`
  - `rarity`
  - `description`（簡短即可）
  - `win_rate`、`pick_rate`（若頁面有提供，可只記大約值或等級分群）

### 4.2 Tier List 頁面

- 對每個英雄抽出：
  - `hero_name_en` / `hero_name_zh`（若可對照）
  - `tier`（S / A / B…）
  - `role`（射手、法師、坦克、刺客等，若頁面有標示）

---

## 5. 彙總成「中介資料」後再生成 Markdown

### 5.1 中介 JSON 建議結構

建議先彙總成一份中介資料，再用這份資料去改寫 `Aram.md`，以利未來重複執行。範例：

```json
{
  "augments_summary": [
    {
      "augment_name_zh": "基本功",
      "augment_name_en": "Back To Basics",
      "rarity": "Prismatic",
      "strong_for": ["雷茲", "剛普拉克"],
      "summary": "大幅提升 Q/W/E 技能輸出，在吃技能係數的英雄身上上限極高。",
      "bugs": [
        "剛普拉克桶子會疊加增傷，使 3 連桶 > 2 連 > 單桶，接近 Bug 級互動。"
      ]
    }
  ],
  "hero_synergy": [
    {
      "hero": "札克",
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
  ]
}
```

### 5.2 生成 / 更新 Aram.md 的邏輯

1. 以現有 `Aram.md` 的章節結構為基準（模式簡介、選擇原則、強勢海克斯、Bug & 坑點、英雄搭配、團隊觀念、Blitz 使用方式）。
2. 使用中介 JSON 更新其中的：
   - 新增或調整的強勢海克斯與代表玩法。
   - 新發現的 Bug / 坑點（例如新版本任務或翻譯問題）。
   - 英雄與海克斯的組合（hero_synergy）。
3. 盡量保留原本文章的寫作風格（中文、略偏口語、實戰向），只更新內容本身。
4. 用「局部補丁（apply_patch）」方式更新 `Writerside/topics/Aram.md`，不要動到其他 Writerside 設定檔。

---

## 6. 未來給 AI 的簡短指令範本

未來若要請 AI 幫忙重新整理，可以給它以下說明作為起點：

> 請依照 `Writerside/topics/Aram-maintain.md` 所描述的流程：
> 1. 重新爬取巴哈討論串 1～最新頁與 Blitz ARAM Mayhem Augments / Tier List 頁面。
> 2. 產生一份中介 JSON（augments_summary、hero_synergy、bugs_and_traps、macro_tips）。
> 3. 以目前 `Aram.md` 的章節結構與寫作風格為基準，更新內容（而非整份重寫）。
> 4. 只修改 `Writerside/topics/Aram.md` 內容，不變更 hi.tree 及其他設定檔。

> 若有版本變動（例如 Riot 或 Blitz 大改 Augments 機制），可在本檔案最上方加註「最近一次重大版本更新說明」。

