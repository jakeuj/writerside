# Writerside Projects Reference

在下列情況讀這份參考：

- 想理解 Writerside 專案結構
- 不確定什麼是 project root、help module root、`writerside.cfg`
- 想新建 Writerside 專案，或把文件加進既有開發專案
- 想判斷 Starter Project、Playground、API Docs 模板各自適合什麼情境

這份筆記依據 JetBrains 官方文件整理：

- `Projects`

若你需要深入理解 help instance、多套輸出、tree file、instance ID 或跨 instance reuse，改讀 `instances-reference.md`。
若你需要深入理解 help module structure、多 module 專案、可選目錄或跨 module `origin` 重用，改讀 `help-modules-reference.md`。

## Writerside project 是什麼

- Writerside documentation project 由撰寫與建置文件需要的設定檔和內容檔組成。
- 可以是獨立文件專案，也可以把文件來源直接加進既有開發專案。

## project root 與 help module root

- 官方頁面特別提醒：Writerside 談的 project root，實際上是對應的 help module root。
- help module 就是存放文件設定與內容的那個目錄。
- 這個目錄名稱不一定要叫 `Writerside`，也可以叫 `docs` 或其他名字。

在這個 repo：

- [Writerside](/Users/jakeuj/WritersideProjects/writerside/Writerside) 就是 help module root。
- [writerside.cfg](/Users/jakeuj/WritersideProjects/writerside/Writerside/writerside.cfg) 在這個目錄底下。
- `topics/`、`images/`、`hi.tree`、`cfg/` 也都在這個 module 裡。

所以之後看到官方說「放在專案根目錄」，要優先理解成「放在 help module root」。

## 新建 documentation project

官方流程大意是：

1. `File | New | Project`
2. 左側選 `Writerside`
3. 選 `Starter Project`
4. 指定名稱與位置後建立

## 把文件加進既有開發專案

官方流程大意是：

1. 打開既有開發專案
2. 在 Writerside tool window 選 `Add documentation`
3. 選 `To Current Project`
4. 建立第一個 help instance

這表示 Writerside 不只適合獨立文件 repo，也可以作為應用程式 repo 裡的文件模組存在。

## 已知限制

- 官方頁面明講：Rider 和 DataGrip 目前有已知問題，無法建立新專案。
- 但這兩個 IDE 仍可用來編輯既有 Writerside 專案。
- 如果要新建專案，官方建議改在其他支援的 IDE 中建立後，再回來編輯。

## Project templates

官方頁面提到三種模板：

### Starter Project

- 最小可行的起始專案
- 一個 help instance
- 一篇示範 Markdown topic
- 適合剛開始、想先跑通最基本結構的人

### Playground

- 多個 instances 與 topics
- 適合拿來探索 markup 與各種 Writerside 功能
- 如果你的目的是學語法、看 feature 範例，這通常比 Starter 更有參考價值

### API Docs

- API documentation sample project
- 適合要做 API 文件的人

## Project structure 怎麼看

- Writerside tool window 比較偏文件工作流。
- Project tool window 比較適合看設定檔與資源檔。
- 官方頁面也特別提到，某些設定檔與資源不會直接出現在 Writerside tool window，需要從 Project tool window 查看。

對這個 repo 來說，常見重要位置是：

- [writerside.cfg](/Users/jakeuj/WritersideProjects/writerside/Writerside/writerside.cfg)：topics / images / instance 設定
- [hi.tree](/Users/jakeuj/WritersideProjects/writerside/Writerside/hi.tree)：TOC 與 instance 入口
- [cfg/buildprofiles.xml](/Users/jakeuj/WritersideProjects/writerside/Writerside/cfg/buildprofiles.xml)：建置與站台變數
- [topics](/Users/jakeuj/WritersideProjects/writerside/Writerside/topics)：文章內容
- [images](/Users/jakeuj/WritersideProjects/writerside/Writerside/images)：圖片資產

如果你需要深入理解 [writerside.cfg](/Users/jakeuj/WritersideProjects/writerside/Writerside/writerside.cfg) 的欄位，改讀 `writerside-cfg-reference.md`。
如果你需要深入理解 help module 應有哪些目錄與 optional files，改讀 `help-modules-reference.md`。
如果你需要深入理解 `hi.tree` 背後的 instance / tree file 規則，改讀 `instances-reference.md`。
如果你需要深入理解 `cfg/buildprofiles.xml` 的欄位，改讀 `buildprofiles-reference.md`。

## 和其他參考檔的分工

- project 結構 / help module root / templates / existing project 導入：這份檔案
- help module structure、多 module 專案、module rename/create、跨 module reuse：`help-modules-reference.md`
- help instance、multiple outputs、tree file、instance reuse：`instances-reference.md`
- `writerside.cfg` 欄位與 help module 主設定：`writerside-cfg-reference.md`
- markup / semantic elements 選擇：`markup-reference.md`
- topic 結構、chapter、show-structure：`structural-elements.md`
- build、deploy、CI checker：`build-deploy.md`
- 本地與 CI 驗證流程差異：`validation-flow.md`

## 在這個 repo 的採用建議

- 這個 repo 已經是既有 Writerside 專案，不是在「新建專案」階段。
- 因此日常工作大多不需要重新思考 template，而是直接在現有 help module 裡增修內容。
- 如果使用者問「哪裡算專案根目錄」，預設回答應是 [Writerside](/Users/jakeuj/WritersideProjects/writerside/Writerside) 這個 help module，而不是整個 git repo 根目錄。
- 如果未來要把 Writerside 文件移進另一個開發專案，先保留「module root 與內容目錄」這套結構，再談 build / deploy 的接線。
