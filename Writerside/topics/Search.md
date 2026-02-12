# Search

Writeside 本身沒有搜尋功能，但可以利用 Algolia search 來做搜尋。

## Algolia search

首先參照官方說明文件來註冊 Algolia 帳號，並取得 API key。
[Algolia search](https://www.jetbrains.com/help/writerside/algolia-search.html)

1. 註冊 [Algolia](https://www.algolia.com/) 帳號，並取得 API key。

2. 登入後應該會有預設的應用程式，如果沒有就新增一個，地區目前不支援亞洲。
[App](https://dashboard.algolia.com/account/applications)

3. 在 Algolia 應用程式頁面，點選 Data sources | Indices，然後點選 Create Index。

![datasources.png](datasources.png){style="block"}

1. 提供一個有意義的名稱並建立索引。

2. 在索引頁面，點選 Configuration | Facets，然後點選 Attributes for faceting 下的 Add an attribute。

![Facets.png](Facets.png){style="block"}

1. 新增兩個屬性：product 和 version。

2. 點選 Review and Save Settings 並確認。

3. 在左下角點 Settings 到設定頁面，點選 API Keys。

![ApiKeys.png](ApiKeys.png){style="block"}

1. 然後找到 Application ID, Search API Key, Admin API Key，這些資訊會用在 Writeside 的設定。

![ApiKey.png](ApiKey.png){style="block"}

## Add search to config

繼續參照 [官方文件](https://www.jetbrains.com/help/writerside/algolia-search.html#add-search-to-config)
來設定 [buildprofiles.xml](https://github.com/jakeuj/writerside/blob/master/Writerside/cfg/buildprofiles.xml#L15)

```xml
<variables>
    <algolia-id>YourAppId</algolia-id>
    <algolia-index>YourIndexName</algolia-index>
    <algolia-api-key>YourSearchApiKey</algolia-api-key>
</variables>
```

## Github Action

1. 到 Github repo 的 Settings | Secrets，新增以下變數：
   - ALGOLIA_KEY: YourAdminApiKey

2. 參考官方文件 [Upload search indexes](https://www.jetbrains.com/help/writerside/deploy-docs-to-github-pages.html#search)
建立 [.github/workflows/deploy.yml](https://github.com/jakeuj/writerside/blob/master/.github/workflows/deploy.yml)
並確保以下設定有被正確設置

```yaml
ALGOLIA_ARTIFACT: 'algolia-indexes-HI.zip'
ALGOLIA_APP_NAME: 'YourAppId'
ALGOLIA_INDEX_NAME: 'YourIndexName'
ALGOLIA_KEY: '${{ secrets.ALGOLIA_KEY }}'
CONFIG_JSON_PRODUCT: 'writerside'
CONFIG_JSON_VERSION: 'master'
```

### 注意事項

- CONFIG_JSON_PRODUCT 需要與 [v.list](https://github.com/jakeuj/writerside/blob/master/Writerside/v.list#L4)
的 `vars.product` 設定一致。

- CONFIG_JSON_VERSION 需要與 [writerside.cfg](https://github.com/jakeuj/writerside/blob/master/Writerside/writerside.cfg#L9)
的 `instance.version` 設定一致。

否則會導致 Algolia search Filter `product`與 `version` 條件不符而搜尋不到。

## 結果

完成後，就可以在 Writeside 網站右上角點放大鏡來使用搜尋功能了。

![search-results.png](search-results.png){style="block"}
