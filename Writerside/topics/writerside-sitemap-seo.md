# Writerside Sitemap 與 SEO 修正筆記

<web-summary>記錄 jakeuj.com 使用 Writerside 部署到 GitHub Pages 時，修正 sitemap、robots.txt、OG URL、Schema URL 與 Search Console 提交流程的 SEO 筆記。</web-summary>

Writerside 部署到 GitHub Pages 並使用 custom domain 時，sitemap、OG URL 與 Schema URL 要和實際公開頁面路徑一致；如果站台實際頁面在根目錄，就要讓 sitemap 產出 `https://jakeuj.com/<topic>.html`，並在 Search Console 提交 `https://jakeuj.com/sitemap.xml`。

<tldr>
<p>正式 URL 採根目錄短網址，例如 <code>https://jakeuj.com/abp.html</code>。</p>
<p>Search Console 提交 <code>https://jakeuj.com/sitemap.xml</code>，目前不需要 <code>sitemap-index.xml</code>。</p>
<p>若 sitemap 指到 404，先檢查線上 artifact 是否已更新，再檢查 Writerside URL 設定。</p>
</tldr>

## 問題症狀

這次遇到的狀況是：

- Google Search Console 要求提供 sitemap。
- 線上 `https://jakeuj.com/robots.txt` 原本是 404。
- 線上 `https://jakeuj.com/sitemap.xml` 回傳 200，但裡面的 URL 是舊路徑。
- sitemap 的 `<loc>` 指向 `https://jakeuj.com/writerside/master/*.html`。
- 實際公開頁面在 `https://jakeuj.com/*.html`，所以舊路徑會 404。

例如：

```text
https://jakeuj.com/writerside/master/a-second-operation-started-on-this-context.html
```

會回傳 404，而真正可用的 URL 是：

```text
https://jakeuj.com/a-second-operation-started-on-this-context.html
```

這種狀況會讓 Search Console 看到 sitemap 內有大量不存在頁面，也會讓 OG metadata、Schema URL 和實際 canonical URL 不一致。

## 先確認正式 URL 策略

這個站台的正式 URL 策略是根目錄短網址：

- 首頁：`https://jakeuj.com/`
- 文章：`https://jakeuj.com/<topic-web-file-name>.html`
- Sitemap：`https://jakeuj.com/sitemap.xml`
- robots.txt：`https://jakeuj.com/robots.txt`

不把 `/writerside/master/` 視為正式公開路徑。

所以 Writerside 設定應維持這個方向：

```xml
<instance src="hi.tree"/>
```

不要重新加回：

```xml
<instance src="hi.tree" web-path="writerside" version="master"/>
```

否則 Writerside metadata 和 sitemap 會傾向產生 `/writerside/master/` 前綴。

## Writerside 的 sitemap 設定

Writerside 預設不一定會產生 sitemap，需要在 `buildprofiles.xml` 保留 `<sitemap>` 設定。

目前重點設定如下：

```xml
<buildprofiles>
    <variables>
        <web-root>https://jakeuj.com/</web-root>
        <generate-sitemap-url-prefix>https://jakeuj.com/</generate-sitemap-url-prefix>
    </variables>

    <build-profile instance="hi">
        <sitemap priority="1" change-frequency="weekly" />
        <variables>
            <product-web-url>https://jakeuj.com/</product-web-url>
            <noindex-content>false</noindex-content>
        </variables>
    </build-profile>
</buildprofiles>
```

這幾個設定的分工是：

| 設定 | 用途 |
| --- | --- |
| `web-root` | 影響站台 metadata，例如 OG / Schema 相關 URL |
| `generate-sitemap-url-prefix` | 影響 sitemap `<loc>` 的 URL prefix |
| `sitemap` | 啟用 sitemap 產生，並設定 priority / change frequency |
| `product-web-url` | 站台產品或文件根 URL |
| `noindex-content` | 是否要求搜尋引擎不要索引內容 |

這次沒有啟用 `generate-canonicals`，因為 Writerside 產生的 canonical 會指向設定的 web root；沒有先抽測輸出前，不要為了修 sitemap 就貿然開啟。

## 真正的根本原因

一開始看起來像是 Writerside sitemap 設定錯誤，但檢查 build artifact 後發現不是這樣。

實際狀況是：

- repo 內的 `writerside.cfg` 和 `buildprofiles.xml` 已經能產生正確 root URL。
- GitHub Actions 的 build artifact 裡，`sitemap.xml` 已經是 `https://jakeuj.com/*.html`。
- 線上 GitHub Pages 還停在舊 artifact。
- 原因是 deploy job 在複製 `robots.txt` 與 `CNAME` 時失敗，Pages artifact 沒有被重新上傳。

失敗點是 deploy job 只有下載 Writerside build artifact，沒有 checkout repo，因此工作目錄裡沒有 repo root 的 `robots.txt` 和 `CNAME`。

錯誤會像這樣：

```text
cp: cannot stat 'robots.txt': No such file or directory
```

這代表要修的是 GitHub Actions deploy job，不是再去改 Writerside 的 URL prefix。

## 修正 deploy workflow

deploy job 需要在下載 artifact 前 checkout repo，讓 repo root 的 metadata 檔案存在。

```yaml
deploy:
  needs: [build, test]
  runs-on: ubuntu-latest
  steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 1

    - name: Download artifact
      uses: actions/download-artifact@v4
      with:
        name: docs

    - name: Unzip artifact
      run: unzip -O UTF-8 -qq "${{ env.ARTIFACT }}" -d dir

    - name: Add root site metadata
      run: |
        cp robots.txt dir/robots.txt
        cp CNAME dir/CNAME
```

然後在 upload Pages artifact 前加上 guard，避免錯誤 sitemap 再次部署出去。

```yaml
- name: Validate Pages artifact SEO metadata
  run: |
    test -f dir/sitemap.xml
    test -f dir/robots.txt
    test -f dir/CNAME

    if grep -q "/writerside/master/" dir/sitemap.xml; then
      echo "::error file=dir/sitemap.xml::sitemap.xml still contains /writerside/master/ URLs"
      exit 1
    fi

    if ! grep -q "<loc>https://jakeuj.com/" dir/sitemap.xml; then
      echo "::error file=dir/sitemap.xml::sitemap.xml does not contain root jakeuj.com URLs"
      exit 1
    fi

    if ! grep -q "Sitemap: https://jakeuj.com/sitemap.xml" dir/robots.txt; then
      echo "::error file=dir/robots.txt::robots.txt is missing the sitemap directive"
      exit 1
    fi
```

這樣如果 Writerside 設定或 deploy artifact 又產生錯誤 URL，CI 會在部署前停下來。

## robots.txt

repo root 的 `robots.txt` 內容保持簡單即可：

```text
User-agent: *
Allow: /

Sitemap: https://jakeuj.com/sitemap.xml
```

重點不是 `robots.txt` 本身很複雜，而是 GitHub Pages artifact 來自 Writerside build zip，不會自動包含 repo root 的一般檔案。

所以 deploy workflow 必須把 `robots.txt` 複製到 Pages artifact 根目錄。

## sitemap.xml 與 sitemap-index.xml

目前站台只有數百篇文章，使用單一 sitemap 就夠了。

Search Console 應提交：

```text
https://jakeuj.com/sitemap.xml
```

目前不需要提交：

```text
https://jakeuj.com/sitemap-index.xml
```

`sitemap-index.xml` 回傳 404 是預期狀態，不是錯誤。

只有符合下列任一條件時，才需要改用 sitemap index：

- 單一 sitemap 超過 50,000 URLs。
- 單一 sitemap 未壓縮超過 50MB。
- 明確要拆成多個 sitemap，例如文章、圖片、文件版本分開提交。

如果未來改用 sitemap index，`robots.txt` 和 Search Console 都要一起改指向 index；否則就維持 `sitemap.xml`。

## 驗證指令

部署後先看根目錄 metadata：

```bash
curl -I https://jakeuj.com/robots.txt
curl -I https://jakeuj.com/sitemap.xml
curl -I https://jakeuj.com/sitemap-index.xml
```

預期結果：

- `robots.txt` 回傳 200。
- `sitemap.xml` 回傳 200。
- `sitemap-index.xml` 回傳 404。

確認 sitemap 沒有舊 prefix：

```bash
curl -L https://jakeuj.com/sitemap.xml | grep -o '/writerside/master/' | head
```

正常情況下不應輸出任何內容。

抽測 sitemap URL：

```bash
curl -L -s -o /dev/null -w '%{http_code}\n' https://jakeuj.com/a-second-operation-started-on-this-context.html
curl -L -s -o /dev/null -w '%{http_code}\n' https://jakeuj.com/abp.html
curl -L -s -o /dev/null -w '%{http_code}\n' https://jakeuj.com/macos-mdns-ssh-hostname-resolution.html
```

這些根目錄文章 URL 應回傳 200。

如果要檢查 HTML head，可以抽 `og:url` 和 Schema `url`：

```bash
curl -L -s https://jakeuj.com/default.html |
  rg 'og:url|"url"|/writerside/master'
```

`og:url` 和 Schema `url` 應該使用 `https://jakeuj.com/default.html` 這類根目錄 URL。

## 排查順序

以後遇到 sitemap 或 SEO URL 指錯時，先照這個順序判斷：

1. 確認正式 URL 策略是 root path 還是子路徑。
2. 檢查線上 `sitemap.xml` 的 `last-modified`，判斷是不是舊 artifact。
3. 檢查最新 GitHub Actions run 是否成功到 deploy。
4. 下載或解開 build artifact，確認 artifact 內的 `sitemap.xml` 是否正確。
5. 如果 artifact 正確但線上錯，修 deploy workflow。
6. 如果 artifact 本身錯，再回頭修 `writerside.cfg` 和 `buildprofiles.xml`。
7. 最後再到 Search Console 重新提交 sitemap 並做 URL Inspection live test。

關鍵是不要只看到線上 sitemap 錯，就立刻改 Writerside 設定；先分清楚「建置輸出錯」還是「部署沒有成功更新」。

## 參考資料

- [JetBrains Writerside: Generate sitemap](https://www.jetbrains.com/help/writerside/generate-sitemap.html)
- [JetBrains Writerside: buildprofiles.xml](https://www.jetbrains.com/help/writerside/buildprofiles-xml.html)
- [Google Search Central: Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Google Search Central: Manage sitemaps with sitemap index files](https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps)
