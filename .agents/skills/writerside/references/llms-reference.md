# Writerside llms.txt Reference

在下列情況讀這份參考：

- 想產生 `llms.txt`
- 想設定 `buildprofiles.xml` 的 `<llms-txt>`
- 想判斷 single-file 和每 topic 一份 LLM export 的差別
- 想把 Writerside 文件輸出給 LLM agent 或其他 AI ingestion 流程使用

這份筆記依據 JetBrains 官方文件整理：

- `Generate llms.txt`

若你需要的是一般 `buildprofiles.xml` 站台設定、header/footer、OG、Algolia 或 sitemap，改讀 `buildprofiles-reference.md`。  
若你需要的是 GitHub Actions、artifact、GitHub Pages deploy 或 CI workflow，改讀 `build-deploy.md`。

## `llms.txt` 是做什麼的

- Writerside 可以把整份文件輸出成較鬆散的 Markdown 格式，生成 `llms.txt`。
- 這份輸出可以：
  - 跟網站一起上傳
  - 作為 LLM agent 的資料來源
  - 提供文件內容給其他 AI ingestion 流程

它不是一般 topic 內容元素，而是 build output 層級功能。

## 在哪裡設定

- 要到 [buildprofiles.xml](/Users/jakeuj/WritersideProjects/writerside/Writerside/cfg/buildprofiles.xml) 設定。
- 用的是 `<llms-txt>` 元素。

最基本寫法：

```xml
<llms-txt single-file="true"/>
```

## 三種輸出模式怎麼選

### 1. 只產生單一 `llms.txt`

```xml
<llms-txt single-file="true"/>
```

- 會輸出一份包含整個 instance 內容的 `llms.txt`
- 適合：
  - 想快速提供單一文件入口給 LLM
  - ingestion 流程偏好一份總檔

### 2. 每個 topic 各自輸出

```xml
<llms-txt single-file="false"/>
```

- 會改成每個 topic 各自一份
- 產物會放在 build artifact 內的 `_llms/` 目錄
- 適合：
  - 想做較細粒度的索引或切片
  - 下游流程偏好逐 topic 處理

### 3. 兩種都要

```xml
<llms-txt/>
```

- 不指定 `single-file` 時，官方表示會同時產生：
  - `llms.txt`
  - `_llms/` 內的逐 topic 檔案

## 判斷準則

- 想簡單、入口單一：`single-file="true"`
- 想細粒度處理 topic：`single-file="false"`
- 想兩邊都保留：省略 `single-file`

但要注意：

- 輸出越多，artifact 體積與後續檢查面也可能變大
- 如果目前根本沒有 LLM ingestion 需求，不要為了跟風先打開

## 和 deploy / artifact 的關係

- `llms.txt` 是 Writerside builder 產物的一部分。
- 只要 build 時有啟用 `<llms-txt>`，它就會出現在 build 產物裡。
- 如果 deploy 流程是直接把 builder 產物部署出去，通常不需要再額外寫一套專門產生 `llms.txt` 的 job。

實務上要確認的是：

- build 後 artifact 裡有沒有 `llms.txt`
- 若設定成 per-topic，artifact 裡有沒有 `_llms/`
- deploy 後實際站台或產物下載位置是否能拿到這些檔案

## 這個 repo 目前的狀態

目前 [buildprofiles.xml](/Users/jakeuj/WritersideProjects/writerside/Writerside/cfg/buildprofiles.xml) 還沒有設定 `<llms-txt>`。

這代表：

- 現在不會額外產生 `llms.txt`
- 也不會產生 `_llms/` 逐 topic 輸出
- 如果未來要導入，需要先在 `buildprofiles.xml` 明確開啟

另外，這個 repo 的 `.github/workflows/deploy.yml` 目前已有：

- build
- checker
- GitHub Pages deploy
- Algolia publish

因此如果要導入 `llms.txt`，通常先確認 build artifact 內容即可，不一定需要先改 workflow 結構。

## 和其他參考檔的分工

- `llms.txt`、`<llms-txt>`、single-file / per-topic 輸出、`_llms/`：這份檔案
- `buildprofiles.xml` 其他站台輸出設定：`buildprofiles-reference.md`
- GitHub Actions、artifact、GitHub Pages deploy、Algolia：`build-deploy.md`
- summary / card / web description：`summary-reference.md`

## 在這個 repo 的採用建議

- 目前 repo 還沒有既定 llms export 慣例，導入時先保守驗證。
- 如果只是一般文章維護，不需要動這層。
- 真要導入時，先決定你要：
  - 一份總檔
  - 每 topic 一份
  - 兩者都要
- 驗證時除了看本地與 CI build 成功，也要實際確認 artifact 內輸出結果是否符合預期。
