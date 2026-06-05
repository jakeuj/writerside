# Build And Deploy

在下列情況讀這份參考：

- 使用者問 Writerside build、GitHub Actions、deploy 失敗
- 使用者問文件為什麼本地過了、CI 卻失敗
- 使用者問 GitHub Pages 怎麼部署 Writerside
- 使用者問 sitemap、robots.txt、CNAME 或 Search Console 抓不到 GitHub Pages 站台檔案
- 使用者問 Algolia index 發布流程

這份筆記依據 JetBrains 官方文件整理：

- `Build and publish on GitHub`

如果問題已經聚焦在 `buildprofiles.xml` 本身，例如 header/footer、social links、shortcut switcher、OG metadata、sitemap、Algolia 參數或 `ignore-problems`，改讀 `buildprofiles-reference.md`。
如果問題已經聚焦在 `llms.txt`、`<llms-txt>` 或 LLM export 產物，改讀 `llms-reference.md`。
如果問題已經聚焦在 `writerside.cfg` 的 `<images>`、`<instance>`、`web-path` 或 build config 位置，改讀 `writerside-cfg-reference.md`。

## 官方 GitHub Pages 流程重點

官方文件把流程拆成三到四層：

1. `build`
   - 用 `JetBrains/writerside-github-action@v4`
   - 產出網站 ZIP、`report.json`，以及可選的 Algolia artifact
2. `test`
   - 用 `JetBrains/writerside-checker-action@v1`
   - 解析 `report.json`，有錯就 fail
3. `deploy`
   - 解壓網站產物
   - 複製根目錄 metadata 檔案，例如 `robots.txt` 與 `CNAME`
   - 用 `actions/configure-pages@v4`
   - 用 `actions/upload-pages-artifact@v3`
   - 用 `actions/deploy-pages@v4`
4. `publish-indexes`
   - 如果有 Algolia，再把 index artifact 發出去

另外還有兩個容易漏掉的前置條件：

- GitHub repository 的 `Settings | Pages` 要把 Source 設成 `GitHub Actions`
- workflow 權限至少要涵蓋 `id-token: write`、`pages: write`，官方範例也有 `contents: read`

## 幾個關鍵環境值怎麼看

### `INSTANCE`

- 格式是 `module/instance-id`
- 例如 starter project 會是 `Writerside/hi`
- 如果要 build group，還要配合 `IS_GROUP: 'true'`

### `DOCKER_VERSION`

- 代表 Writerside Docker builder 版本
- 升級 Writerside 後，這個值也應跟著更新，盡量和本地預覽 / 本地 build 對齊

### `ARTIFACT`

- 一般 single instance 會是 `webHelp<INSTANCE_ID_UPPER>2-all.zip`
- 官方範例會用 shell 先算出來，也可以像這個 repo 一樣直接寫死當前 instance 的檔名

### `ALGOLIA_*`

- 只有啟用 Algolia search 才需要
- 常見包括：
  - `ALGOLIA_ARTIFACT`
  - `ALGOLIA_APP_NAME`
  - `ALGOLIA_INDEX_NAME`
  - `ALGOLIA_KEY`
- `CONFIG_JSON_PRODUCT`
- `CONFIG_JSON_VERSION`

### `llms.txt` 相關產物

- Writerside 的 `llms.txt` 不是 workflow env 變數，而是 `buildprofiles.xml` 裡的 `<llms-txt>` 設定控制。
- 一旦啟用，它會跟著 Writerside builder 產物一起生成。
- 所以 deploy workflow 通常不用特別多加一個 job；重點是 build 後的 artifact 內有沒有帶出對應檔案。

## `writerside.cfg` 和 GitHub Pages 的交會點

官方文件特別提醒一件事：

- 部署到 GitHub Pages 時，要確認 `<images>` 的 `web-path` 是否符合實際發佈路徑

官方範例是 repo-name based Pages，因此建議把：

```xml
<images dir="images" web-path="my-docs-repo"/>
```

但這不是所有站台都能直接照抄。判斷原則是：

- 如果網站是掛在 `https://<user>.github.io/<repo>/` 這種 repo 子路徑下，要特別檢查圖片 URL 基底
- 如果有 custom domain、反向代理，或站點掛在不同根路徑，應以實際部署路徑為準

所以不要看到官方範例就直接把 `web-path` 改成 repo 名稱；先看目前站台實際怎麼發。

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
   - 解壓文件產物
   - 複製 `robots.txt` 與 `CNAME` 到 Pages artifact 根目錄
   - 發布到 GitHub Pages
4. `publish-indexes`
   - 讀取 Algolia artifact
   - 更新 Algolia 索引

## 這個 repo 目前的實際設定

目前 workflow 關鍵值是：

- `INSTANCE: Writerside/hi`
- `IS_GROUP: false`
- `ARTIFACT: webHelpHI2-all.zip`
- `DOCKER_VERSION: 2026.04.8711`
- `ALGOLIA_ARTIFACT: algolia-indexes-HI.zip`
- `ALGOLIA_APP_NAME: 8VA5LCDZGD`
- `ALGOLIA_INDEX_NAME: Default`
- `CONFIG_JSON_PRODUCT: writerside`
- `CONFIG_JSON_VERSION: master`

這表示目前 repo 已經不是只有 build，而是完整跑：

- Writerside build
- Writerside checker
- GitHub Pages deploy
- Algolia indexes publish

另外，這個 repo 的 [writerside.cfg](/Users/jakeuj/WritersideProjects/writerside/Writerside/writerside.cfg) 目前是：

- `<images dir="images" web-path="images"/>`
- `<instance src="hi.tree"/>`

我從設定推論：

- 這個 repo 的公開文章 URL 採用根目錄短網址，例如 `https://jakeuj.com/abp.html`
- 不要把 `CONFIG_JSON_PRODUCT` / `CONFIG_JSON_VERSION` 誤解成公開 URL 前綴；公開 URL 仍以建置輸出、`writerside.cfg`、`web-root` 和 sitemap 設定為準
- 這個 repo 的部署模式不完全等於官方文件中的「repo 名稱直接當圖片 web-path」範例，因為它有 custom domain 與既定根目錄 URL 策略

所以之後遇到圖片、sitemap 或 OG/Schema URL 在 Pages 上失效時，先比對實際網站路徑，不要機械式套官方範例。

## 根目錄 metadata 檔案

這個 repo 的 Pages artifact 來自 Writerside build zip，不會自動包含 repo root 的一般檔案。若需要站台根目錄檔案，要在 deploy job 解壓後、upload artifact 前複製。

目前 workflow 會複製：

- `robots.txt` -> `dir/robots.txt`
- `CNAME` -> `dir/CNAME`

部署後應驗證：

```bash
curl -I https://jakeuj.com/robots.txt
curl -I https://jakeuj.com/sitemap.xml
```

`robots.txt` 應包含：

```text
Sitemap: https://jakeuj.com/sitemap.xml
```

另外，這個 repo 目前的 [buildprofiles.xml](/Users/jakeuj/WritersideProjects/writerside/Writerside/cfg/buildprofiles.xml) 還沒有啟用 `<llms-txt>`，表示現況並不會額外產生 llms export。

## 目前 workflow 和官方範例的比對重點

- 相同點：
  - 已使用 `JetBrains/writerside-github-action@v4`
  - 已使用 `JetBrains/writerside-checker-action@v1`
  - 已使用 GitHub Pages 三件套：`configure-pages`、`upload-pages-artifact`、`deploy-pages`
  - 已有 Algolia 發布 job
- 需要特別記得比對的點：
  - 官方範例把 `contents: read` 也列進 workflow permissions
  - 官方範例特別提醒 Pages Source 要選 `GitHub Actions`
  - build group 時，artifact path 與 `IS_GROUP` 寫法會不同

## 本地檢查與 CI 的落差

- `npm run pre-deploy` 只做 Markdown、必要檔案存在、`hi.tree` XML 檢查
- 本地流程不會真的跑 `writerside-github-action` 也不會跑 `writerside-checker-action`
- 本地流程也不會真的做 GitHub Pages 打包、`deploy-pages` 或 Algolia 發布
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

常見切點：

- checkout / token / permission 問題
- `INSTANCE`、artifact 名稱、`IS_GROUP` 設錯
- Pages Source 沒切到 `GitHub Actions`
- deploy 成功但圖片路徑不對，通常回頭看 `writerside.cfg` 的 `<images web-path>`
- sitemap `<loc>` 或 OG/Schema URL 指到 404，通常回頭看 `writerside.cfg` 的 instance `web-path` / `version` 和 `buildprofiles.xml` 的 `generate-sitemap-url-prefix`
- `robots.txt` 或 `CNAME` 線上 404，通常檢查 deploy job 是否把根目錄 metadata 複製到 Pages artifact

### Algolia 問題

優先看 workflow 裡這些環境值：

- `ALGOLIA_ARTIFACT`
- `ALGOLIA_APP_NAME`
- `ALGOLIA_INDEX_NAME`
- `ALGOLIA_KEY`

如果使用者只是要新增或修文，通常不需要主動展開這一層。

## 在這個 repo 的採用建議

- 一般寫文章時，不要主動改 `.github/workflows/deploy.yml`。
- 只有在 CI / deploy / search index 真有問題時，才進到這層。
- 遇到 GitHub Pages 問題時，先分清楚是：
  - 內容錯
  - checker 錯
- workflow 權限或 artifact 錯
- Pages 設定錯
- 圖片 / 路徑 / `web-path` 錯
- `llms.txt` 沒啟用，或啟用後沒有在 artifact / 部署輸出中驗到
