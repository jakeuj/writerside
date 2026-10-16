# Writerside Images Reference

在下列情況讀這份參考：

- 要插入截圖、圖示、GIF、SVG 或外部圖片
- 不確定該用 Markdown 圖片還是 `<img>`
- 想設定 `width`、`thumbnail`、`preview-src`、`style="inline"`、`style="block"`
- 遇到 `MRK058`、大圖被當成 block、圖示被當成 inline image
- 想處理 dark theme 對應圖片、相對路徑或外部圖片限制

這份筆記依據 JetBrains 官方文件整理：

- `Images`
- `Semantic markup reference` 中的 `<img>`、`<video>`

## 先判斷圖片來源與寫法

- 預設把本地圖片放在 `Writerside/images/`。
- 圖片在指定 images 目錄時，優先直接用檔名引用，例如 `image.png`。
- 如果圖片刻意放在 topic 相對位置，也可以用相對路徑：
  - `./image.png`
  - `../myMediaDir/image.png`
  - `$PROJECT_DIR$/allImages/image.png`
- 這個 repo 的預設做法仍然是放進 `Writerside/images/`，除非有明確理由，不要把媒體分散到其他位置。

## Markdown 圖片還是 `<img>`

- 一般截圖、沒有特殊控制需求時，直接用 Markdown 圖片。
- 需要更明確的屬性控制時改用 `<img>`。
- 兩種寫法在 Writerside 都能工作：

```markdown
![Alt Text](image.png){ width="450" }
```

```xml
<img src="image.png" alt="Alt text" width="450"/>
```

判斷準則：

- 只是插一張普通截圖：Markdown 優先
- 需要 XML 區塊內統一結構或語意一致性：改用 `<img>`
- 需要跟其他 semantic markup 一起包在 `<step>`、`<tab>` 等容器內：可直接用 `<img>`

## 圖片格式

- Writerside 支援 `PNG`、`JPG`、`GIF`、`SVG`。
- UI 截圖通常優先用 `PNG`。
- 圖示或向量素材可用 `SVG`，但仍要注意在淺色/深色主題中的對比。

## Inline 與 Block Images

- Writerside 預設會把大於 32px 的圖片當成 block element，就算你把它寫在段落裡也一樣。
- 如果想把大圖留在段落內，明確加上 `style="inline"`。
- 如果是小圖示，放在段落內時通常會被當成 inline image。
- 若要把小圖示獨立成區塊，改成 `style="block"`，或直接把它放到段落外。

Markdown 範例：

```markdown
![check icon](check-icon.png){ width="16" }
![large screenshot](big-shot.png){ style="inline" }
![small icon](check-icon.png){ style="block" }
```

這和 repo 內的 `MRK058-Large-image.md` 直接相關：

- 遇到 `MRK058: Large image in paragraph rendered as a block element by default`
- 優先做法：
  - 把圖片移到段落外
  - 或明確加上 `style="inline"` 表達意圖

## Thumbnail

- 寬度超過 700px 的圖片，Writerside 會自動縮到 viewport 內。
- 若圖片很寬而且細節很多，優先加 `thumbnail="true"`，讓它變成可點開的大圖縮圖。
- 可以再搭配 `width` 把 thumbnail 縮得更小。
- 如果想用另一張圖當縮圖預覽，使用 `preview-src`。

範例：

```markdown
![wide image](image.png){ thumbnail="true" }
![wide image](image.png){ thumbnail="true" width="200" }
![wide image](image.png){ thumbnail="true" preview-src="thumbnail-preview.png" }
```

## Animated GIF

- GIF 當一般圖片插入即可。
- Writerside 會把第一幀當預覽，加上 `Gif` 標記，讀者點了才開始播放。
- 如果不想用第一幀當預覽，可加 `preview-src="some-preview.png"`。

## Dark Theme Images

- 如果圖片在 dark theme 下會看不清楚，應準備 light/dark 兩個版本。
- dark 版本檔名使用 `_dark` suffix，例如：
  - `example.png`
  - `example_dark.png`
- 兩張都放進 `Writerside/images/`。
- 寫 markup 時只引用 light 版本檔名，Writerside 會自動對應 dark 版本。

這個 repo 的建議：

- 一般終端截圖、淺色背景畫面通常不一定要做 dark 版。
- 如果圖片本身有透明背景、深色文字、或會被網站 dark theme 吃掉邊界，優先補 dark 版。

## 外部圖片

- 可以直接引用外部圖片 URL。
- 目前官方文件有已知限制：外部圖片無法設定尺寸。
- 所以需要穩定尺寸、thumbnail、dark theme 對應或長期可用性時，優先下載到本 repo 再引用。

## Alt Text 與可讀性

- 每張圖片都要有能說明內容的 alt text。
- 不要只寫 `image`、`screenshot` 或留空，除非真的是純裝飾圖。
- 圖片若承載操作資訊，alt text 至少要讓人知道畫面主體是什麼。

## Markdown 圖片工具與重複引用

- 在 Markdown topic 裡可用 `Alt+Insert` 插入圖片。
- 也可用 `Ctrl+U` 開啟 Insert Image dialog。
- 若同一張小圖示要在同篇文章反覆使用，可用 reference-style image links。

範例：

```markdown
Click the ![check icon][check]{width="16"} icon to mark an item as done.

[check]: check-icon.png
```

## 在這個 repo 的採用建議

- 本地圖片預設放 `Writerside/images/`，並用有意義檔名。
- 單純截圖：Markdown 圖片優先。
- 需要 `thumbnail`、`preview-src`、`style`、或與 XML 結構混用時，再切換成 `<img>`。
- 遇到大圖在段落裡的警告，先回頭看 `Writerside/topics/MRK058-Large-image.md`。
- 如果圖片是教學核心內容，優先確保可讀性與路徑穩定，再追求花式屬性。

## 截圖加註

截圖給人看，文字給搜尋與 AI：正文與 alt text 要能獨立說清楚結論，截圖讓讀者一眼對到位置。畫面元素多、結論只靠其中幾格，或步驟要讀者點某個按鈕時，先加註再放進文章；單純示意或整個畫面就是重點時不必加註。

### 顏色與標籤

- 紅框標原因、異常值或「不要做」的項目，綠框標結果或要確認的正常值，灰框標背景補充，藍框標要操作的按鈕或欄位。
- 標籤以 ①②③ 編號，一句話寫「值 → 意義」或「位置 → 動作」，例如「① 組織點數 US$200.00 → 已領到本月額度」；用語與正文一致。
- 一張圖最多三到四個標註；超過就拆成兩張截圖或改用文字清單。
- 圖片前一段文字或 alt text 要交代紅框、藍框各代表什麼；讀者看不到顏色時也能理解。

### 去識別化

- 畫面上有帳號、email、組織名稱、卡號、金鑰、token、內部網域或客戶資料時，先用 `mask` 蓋掉，再存進 `Writerside/images/`；遮罩不是加註的附屬，沒有加註需求也要做。
- 識別資料落在證據區域之外（視窗標題、側欄、分頁）時直接裁掉。
- 使用者提供時已打碼的圖仍要再看一次，確認沒有漏掉的角落。

### 操作流程

1. 先用 `sips -g pixelWidth -g pixelHeight` 取得原圖尺寸，開圖找出要框的區域座標；座標一律是原圖像素，左上為 `0,0`。
2. 用 [scripts/annotate_screenshot.py](../scripts/annotate_screenshot.py) 依 JSON 規格畫框、標籤、箭頭與遮罩，規格格式見腳本開頭：

    ```bash
    python3 .agents/skills/writerside/scripts/annotate_screenshot.py \
      <scratchpad>/原圖.png Writerside/images/<topic-slug>-<重點>.png - <<'JSON'
    {"items": [
      {"box": [612, 97, 918, 243], "color": "green", "width": 5},
      {"label": "① 組織點數 US$200.00 → 已領到本月額度", "at": [940, 110], "color": "green", "size": 28, "arrow_to": [918, 170]}
    ]}
    JSON
    ```

3. 產出後一定要開圖檢查：框對到目標、標籤沒蓋住要看的值、中文字正常顯示、遮罩完全蓋住識別資料；不對就調座標重畫。
4. 原圖留在 scratchpad，只把加註後的版本存進 `Writerside/images/`；檔名沿用 `<topic-slug>-<重點>.png`，不加 `_annotated` 之類的後綴，避免之後重做時又多一份。
5. 使用者提供的圖是 webp 或其他 Writerside 不支援的格式時，先用 `sips -s format png` 轉成 PNG 再加註。
6. 腳本需要 Pillow 與本機 CJK 字型；缺字型時依腳本提示在 `FONT_CANDIDATES` 補路徑。

### 在正文中放置

- 圖片放在它佐證的步驟或段落旁，不集中堆在文末。
- alt text 寫「畫面主體 + 標註重點」，例如「Claude Console 儀表板，綠框標出組織點數 US$200.00，紅框標出不要開啟的自動儲值」。
- 寬圖加 `thumbnail="true"`，讓讀者能點開看清標籤文字。
