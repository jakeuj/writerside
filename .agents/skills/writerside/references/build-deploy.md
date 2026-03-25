# Build And Deploy

在下列情況讀這份參考：

- 使用者問 Writerside build、GitHub Actions、deploy 失敗
- 使用者問文件為什麼本地過了、CI 卻失敗
- 使用者問 Algolia index 發布流程

## CI 流程摘要

這個 repo 的 `.github/workflows/deploy.yml` 大致分成四段：

1. `build`
   - 使用 `JetBrains/writerside-github-action@v4`
   - instance 是 `Writerside/hi`
   - 會產出 `webHelpHI2-all.zip`、`report.json`、Algolia artifact
2. `test`
   - 下載 build artifact
   - 使用 `JetBrains/writerside-checker-action@v1`
   - 這一層會抓 Writerside 專屬問題
3. `deploy`
   - 解壓文件產物並發布到 GitHub Pages
4. `publish-indexes`
   - 讀取 Algolia artifact
   - 更新 Algolia 索引

## 本地檢查與 CI 的落差

- `npm run pre-deploy` 只做 Markdown、必要檔案存在、`hi.tree` XML 檢查
- 本地流程不會真的跑 `writerside-github-action` 也不會跑 `writerside-checker-action`
- 所以本地全綠，不代表 CI 一定全綠

## 遇到部署相關問題時的讀法

### 文件內容問題

先看：

- `references/checker-errors.md`
- `references/validation-flow.md`

### CI / workflow 設定問題

直接看：

- `.github/workflows/deploy.yml`
- `Writerside/writerside.cfg`
- `Writerside/hi.tree`
- `Writerside/cfg/buildprofiles.xml`

### Algolia 問題

優先看 workflow 裡這些環境值：

- `ALGOLIA_ARTIFACT`
- `ALGOLIA_APP_NAME`
- `ALGOLIA_INDEX_NAME`
- `ALGOLIA_KEY`

如果使用者只是要新增或修文，通常不需要主動展開這一層。
