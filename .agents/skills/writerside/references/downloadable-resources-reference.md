# Writerside Downloadable Resources Reference

在下列情況讀這份參考：

- 想讓讀者下載 ZIP、CSV、TXT、JSON、範例設定檔或其他附件
- 想使用 `<resource src="..."/>`
- 不確定 downloadable resources 和圖片、程式碼 sample、一般超連結有什麼差別
- 想確認 `writerside.cfg` 要怎麼設定 resources directory

這份筆記依據 JetBrains 官方文件整理：

- `Downloadable resources`
- `Semantic markup reference` 中的 `<resource>`

若你需要的是 resources directory 在 help module 結構中的位置、多 module 專案或 module-level 目錄分工，改讀 `help-modules-reference.md`。

## `<resource>` 是做什麼的

- `<resource>` 會產生一個可下載檔案的連結。
- 適合教學中要附上：
  - project template ZIP
  - sample CSV / TXT
  - 範例設定檔
  - 需要讀者另外下載的素材

範例：

```xml
Download <resource src="sample-resource.txt"/> and open it.
```

建置後，Writerside 會把對應檔案一起打包到網站的 resources 目錄，並生成下載連結。

## 先判斷該不該用 downloadable resources

- 讀者需要把檔案抓下來本地使用時，用 `<resource>`。
- 只是要導到另一篇 topic 或外部網站時，用一般 `<a>` 或 Markdown link。
- 只是要展示程式碼內容時，優先用 fenced code 或 `code-block`，不要把它變成下載附件。
- 圖片、GIF、影片屬於媒體資產，優先走 `images` 目錄與圖片/影片標記，不要混到 downloadable resources。

## resources directory

- 官方要求：可下載檔案要放在 resources directory。
- `<resource src="..."/>` 的 `src` 指向的是 resources directory 裡的檔名。
- 如果檔案不在 resources directory，就算 topic 寫了 `<resource>`，也不會是正確的做法。

## 這個 repo 目前的狀態

目前 [writerside.cfg](/Users/jakeuj/WritersideProjects/writerside/Writerside/writerside.cfg) 只有：

- `<topics dir="topics" web-path="topics"/>`
- `<images dir="images" web-path="images"/>`

目前沒有宣告 `<resources .../>`。

這代表：

- 這個 repo 現在還沒有既定的 downloadable resources 目錄配置。
- 如果未來真的要用 `<resource>`，要先補上對應的 resources directory 設定，再把檔案放進去。

## `writerside.cfg` 設定方向

若未來要導入 downloadable resources，通常會需要在 `writerside.cfg` 補一個 resources 設定，例如：

```xml
<resources dir="resources" web-path="resources"/>
```

然後在 `Writerside/` 下建立對應目錄，讓要下載的檔案放在裡面。

這份 reference 先記錄判斷原則，不直接替 repo 預設建立該目錄，因為目前使用者的需求只是更新 skill，不是修改站台資產結構。

## `<resource>` 的使用方式

- 最基本就是在段落中直接插入：

```xml
<p>Download <resource src="sample-resource.txt"/> and open it.</p>
```

- `src` 應填 resources directory 中的檔名。
- 如果檔名本身沒有足夠上下文，記得在句子裡補充這個檔案是做什麼的。

## 和其他機制的分工

- `<resource>` vs Markdown / XML link
  - 要下載站內附檔：`<resource>`
  - 要跳去 topic 或外部頁面：link
- `<resource>` vs `code-block src="..."`
  - 要顯示程式碼內容：`code-block`
  - 要讓讀者拿到原始檔：`<resource>`
- `<resource>` vs 圖片
  - 要內嵌顯示媒體：Markdown image 或 `<img>`
  - 要提供檔案下載：`<resource>`

## 寫作建議

- 不要只丟一個裸檔名連結，前後要有一句說明，告訴讀者下載後要做什麼。
- 檔名要有意義，例如 `sample-config.json`、`demo-data.csv`，避免 `file1.zip` 這種看不出用途的名稱。
- 如果附件只是一小段文字或幾行設定，先想想直接寫進正文會不會更省事。
- 只有在下載附件真的能降低讀者操作成本時，才導入 downloadable resources。

## 在這個 repo 的採用建議

- 目前這個 repo 以文章、圖片與程式碼範例為主，downloadable resources 不是預設需求。
- 真要使用時，先檢查 `writerside.cfg` 是否已宣告 resources directory。
- 若只是單篇文章需要附檔，不要偷偷把檔案塞進 `images/` 假裝下載連結；媒體和 downloadable resources 要分開。
- 如果需求變成站台設定調整，而不只是 topic 編寫，記得同步檢查 build / deploy 流程是否也要一起驗證。
