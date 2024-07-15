# AI Search Service

Azure 提供向量搜尋服務

## 服務介紹
[search-get-started-vector](https://learn.microsoft.com/zh-tw/azure/search/search-get-started-vector)

## 使用方式

### 1. 建立服務

![ai-search-create.png](ai-search-create.png)

### 2. 取得搜尋服務端點

![ai-search-url.png](https://learn.microsoft.com/zh-tw/azure/search/media/search-get-started-rest/get-endpoint.png)

### 3. 取得金鑰

![ai-search-key.png](https://learn.microsoft.com/zh-tw/azure/search/media/search-get-started-rest/get-api-key.png)

### 4. 下載範例程式碼

[az-search-vector-quickstart.rest](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-vectors)

### 5. 下載並安裝 VsCode 與 REST Client 擴充

[Visual Studio Code](https://code.visualstudio.com/)

[REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)

### 6. 修改範例程式碼
將 `az-search-vector-quickstart.rest` 檔案中的 `@baseUrl` 與 `@apiKey` 替換為自己的服務端點與金鑰

```
@baseUrl = PUT-YOUR-SEARCH-SERVICE-URL-HERE
@apiKey = PUT-YOUR-SEARCH-SERVICE-ADMIN-API-KEY-HERE
```

### 7. 執行範例程式碼建立索引
類似建立資料表的結構
- HotelId: 主索引鍵
- HotelName: 旅館名稱
- HotelNameVector: 旅館名稱的向量(用以模糊搜尋)
- Description: 描述
- DescriptionVector: 描述的向量(用以模糊搜尋)
- Category: 類別
- Tags: 標籤
- ParkingIncluded: 停車位
- LastRenovationDate: 最後整修日期
- Rating: 評分
- Address: 地址
- Location: 地理位置

```http request
### Create a new index
POST  {{baseUrl}}/indexes?api-version=2023-11-01  HTTP/1.1
    Content-Type: application/json
    api-key: {{apiKey}}
```
Request
```json
{
  "name": "hotels-vector-quickstart",
  "fields": [
    {
      "name": "HotelId",
      "type": "Edm.String",
      "searchable": false,
      "filterable": true,
      "retrievable": true,
      "sortable": false,
      "facetable": false,
      "key": true
    },
    {
      "name": "HotelName",
      "type": "Edm.String",
      "searchable": true,
      "filterable": false,
      "retrievable": true,
      "sortable": true,
      "facetable": false
    },
    {
      "name": "HotelNameVector",
      "type": "Collection(Edm.Single)",
      "searchable": true,
      "retrievable": true,
      "dimensions": 1536,
      "vectorSearchProfile": "my-vector-profile"
    },
    {
      "name": "Description",
      "type": "Edm.String",
      "searchable": true,
      "filterable": false,
      "retrievable": true,
      "sortable": false,
      "facetable": false
    },
    {
      "name": "DescriptionVector",
      "type": "Collection(Edm.Single)",
      "searchable": true,
      "retrievable": true,
      "dimensions": 1536,
      "vectorSearchProfile": "my-vector-profile"
    },
    {
      "name": "Description_fr",
      "type": "Edm.String",
      "searchable": true,
      "filterable": false,
      "retrievable": true,
      "sortable": false,
      "facetable": false,
      "analyzer": "en.microsoft"
    },
    {
      "name": "Description_frvector",
      "type": "Collection(Edm.Single)",
      "searchable": true,
      "retrievable": true,
      "dimensions": 1536,
      "vectorSearchProfile": "my-vector-profile"
    },
    {
      "name": "Category",
      "type": "Edm.String",
      "searchable": true,
      "filterable": true,
      "retrievable": true,
      "sortable": true,
      "facetable": true
    },
    {
      "name": "Tags",
      "type": "Collection(Edm.String)",
      "searchable": true,
      "filterable": true,
      "retrievable": true,
      "sortable": false,
      "facetable": true
    },
    {
      "name": "ParkingIncluded",
      "type": "Edm.Boolean",
      "searchable": false,
      "filterable": true,
      "retrievable": true,
      "sortable": true,
      "facetable": true
    },
    {
      "name": "LastRenovationDate",
      "type": "Edm.DateTimeOffset",
      "searchable": false,
      "filterable": true,
      "retrievable": true,
      "sortable": true,
      "facetable": true
    },
    {
      "name": "Rating",
      "type": "Edm.Double",
      "searchable": false,
      "filterable": true,
      "retrievable": true,
      "sortable": true,
      "facetable": true
    },
    {
      "name": "Address",
      "type": "Edm.ComplexType",
      "fields": [
        {
          "name": "StreetAddress",
          "type": "Edm.String",
          "searchable": true,
          "filterable": false,
          "retrievable": true,
          "sortable": false,
          "facetable": false
        },
        {
          "name": "City",
          "type": "Edm.String",
          "searchable": true,
          "filterable": true,
          "retrievable": true,
          "sortable": true,
          "facetable": true
        },
        {
          "name": "StateProvince",
          "type": "Edm.String",
          "searchable": true,
          "filterable": true,
          "retrievable": true,
          "sortable": true,
          "facetable": true
        },
        {
          "name": "PostalCode",
          "type": "Edm.String",
          "searchable": true,
          "filterable": true,
          "retrievable": true,
          "sortable": true,
          "facetable": true
        },
        {
          "name": "Country",
          "type": "Edm.String",
          "searchable": true,
          "filterable": true,
          "retrievable": true,
          "sortable": true,
          "facetable": true
        }
      ]
    },
    {
      "name": "Location",
      "type": "Edm.GeographyPoint",
      "searchable": false,
      "filterable": true,
      "retrievable": true,
      "sortable": true,
      "facetable": false
    }
  ],
  "vectorSearch": {
    "algorithms": [
      {
        "name": "my-hnsw-vector-config-1",
        "kind": "hnsw",
        "hnswParameters": {
          "m": 4,
          "efConstruction": 400,
          "efSearch": 500,
          "metric": "cosine"
        }
      },
      {
        "name": "my-hnsw-vector-config-2",
        "kind": "hnsw",
        "hnswParameters": {
          "m": 4,
          "metric": "euclidean"
        }
      },
      {
        "name": "my-eknn-vector-config",
        "kind": "exhaustiveKnn",
        "exhaustiveKnnParameters": {
          "metric": "cosine"
        }
      }
    ],
    "profiles": [
      {
        "name": "my-vector-profile",
        "algorithm": "my-hnsw-vector-config-1"
      }
    ]
  },
  "semantic": {
    "configurations": [
      {
        "name": "my-semantic-config",
        "prioritizedFields": {
          "titleField": {
            "fieldName": "HotelName"
          },
          "prioritizedContentFields": [
            {
              "fieldName": "Description"
            }
          ],
          "prioritizedKeywordsFields": [
            {
              "fieldName": "Category"
            }
          ]
        }
      }
    ]
  }
}
```

### 8. 執行範例程式碼上傳資料
類似新增資料到資料表

其中 HotelNameVector 與 DescriptionVector 

是將 HotelName 與 Description 向量化後的結果

這邊範例是直接將向量化後的結果填入

也有提供 Azure OpenAI 服務，使用嵌入模型 text-embedding-ada-002 來向量化的範例程式碼

但目前好像要以組織名義填表單申請才能夠使用該服務

![az-open-ai.png](az-open-ai.png)

```http request
### Upload documents
POST  {{baseUrl}}/indexes/hotels-vector-quickstart/docs/index?api-version=2023-11-01  HTTP/1.1
    Content-Type: application/json
    api-key: {{apiKey}}
```
Request
```json
{
    "value": [
        {
            "@search.action": "mergeOrUpload",
            "HotelId": "1",
            "HotelName": "Secret Point Hotel",
            "HotelNameVector": [0.0040753875,0.004081966,0.007854742],
            "Description": "The hotel is ideally located on the...",
            "DescriptionVector": [-0.020142354,0.017661706],
            "Category": "Boutique",
            "Tags": [
                "pool",
                "air conditioning",
                "concierge"
            ],
            "ParkingIncluded": false,
            "LastRenovationDate": "1970-01-18T00:00:00Z",
            "Rating": 3.60,
            "Address": {
                "StreetAddress": "677 5th Ave",
                "City": "New York",
                "StateProvince": "NY",
                "PostalCode": "10022",
                "Country": "USA"
            },
            "Location": {
                "type": "Point",
                "coordinates": [
                    -73.975403,
                    40.760586
                ]
            }
        }
    ]
}
```
這邊資料很長，所以只貼一筆資料，並且縮減向量，方便瀏覽，實際請到 Github 範例程式碼中查看

### 9. 執行單一向量查詢
類似查詢資料表
- count: 是否回傳筆數
- select: 回傳的欄位
- vectorQueries: 向量查詢
  - vector: 向量
  - k: 回傳筆數
  - fields: 欄位
  - kind: 向量
  - exhaustive: 是否完整搜尋

```http request
### Run a single vector query
POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version=2023-11-01  HTTP/1.1
    Content-Type: application/json
    api-key: {{apiKey}}
```
Request
```json
{
  "count": true,
  "select": "HotelId, HotelName, Description, Category",
  "vectorQueries": [
    {
      "vector": [0.01944167, 0.0040178085, -0.007816401, 0.009330357],
      "k": 7,
      "fields": "DescriptionVector",
      "kind": "vector",
      "exhaustive": true
    }
  ]
}
```
Response
```json
{
  "@odata.context": "https://ai-jakeuj.search.windows.net/indexes('hotels-vector-quickstart')/$metadata#docs(*)",
  "@odata.count": 7,
  "value": [
    {
      "@search.score": 0.8577363,
      "HotelId": "48",
      "HotelName": "Nordick's Motel",
      "Description": "Only 90 miles (about 2 hours) from the nati...",
      "Category": "Boutique"
    },
    {
      "@search.score": 0.8399121,
      "HotelId": "49",
      "HotelName": "Old Carrabelle Hotel",
      "Description": "Spacious rooms, glamorous suites and reside...",
      "Category": "Luxury"
    },
    {
      "@search.score": 0.8383955,
      "HotelId": "13",
      "HotelName": "Historic Lion Resort",
      "Description": "Unmatched Luxury.  Visit our downtown hotel...",
      "Category": "Resort and Spa"
    },
    {
      "@search.score": 0.82543427,
      "HotelId": "4",
      "HotelName": "Sublime Cliff Hotel",
      "Description": "Sublime Cliff Hotel is located in the heart...",
      "Category": "Boutique"
    },
    {
      "@search.score": 0.82380015,
      "HotelId": "1",
      "HotelName": "Secret Point Hotel",
      "Description": "The hotel is ideally located on the main co...",
      "Category": "Boutique"
    },
    {
      "@search.score": 0.81514114,
      "HotelId": "2",
      "HotelName": "Twin Dome Hotel",
      "Description": "The hotel is situated in a  nineteenth cent...",
      "Category": "Boutique"
    },
    {
      "@search.score": 0.813376,
      "HotelId": "3",
      "HotelName": "Triple Landscape Hotel",
      "Description": "The Hotel stands out for its gastronomic ...",
      "Category": "Resort and Spa"
    }
  ]
}
```

### 10. 執行向量查詢並加上過濾器
類似帶過濾條件查詢資料表
- filter: 篩選條件
- vectorFilterMode: 向量篩選模式

```http request
### Run a vector query with a filter
POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version=2023-11-01  HTTP/1.1
    Content-Type: application/json
    api-key: {{apiKey}}
```
Request
```json
{
  "count": true,
  "select": "HotelId, HotelName, Category, Tags, Description",
  "filter": "Tags/any(tag: tag eq 'free wifi')",
  "vectorFilterMode": "postFilter",
  "vectorQueries": [
    {
      "vector": [0.01944167, 0.0040178085, -0.007816401, 0.009330357],
      "k": 7,
      "fields": "DescriptionVector",
      "kind": "vector",
      "exhaustive": true
    }
  ]
}
```
Response
```json
{
  "@odata.context": "https://ai-jakeuj.search.windows.net/indexes('hotels-vector-quickstart')/$metadata#docs(*)",
  "@odata.count": 3,
  "value": [
    {
      "@search.score": 0.8577363,
      "HotelId": "48",
      "HotelName": "Nordick's Motel",
      "Description": "Only 90 miles (about 2 hours) from the nati...",
      "Category": "Boutique",
      "Tags": [
        "continental breakfast",
        "air conditioning",
        "free wifi"
      ]
    },
    {
      "@search.score": 0.8383955,
      "HotelId": "13",
      "HotelName": "Historic Lion Resort",
      "Description": "Unmatched Luxury.  Visit our downtown hotel...",
      "Category": "Resort and Spa",
      "Tags": [
        "view",
        "free wifi",
        "pool"
      ]
    },
    {
      "@search.score": 0.81514114,
      "HotelId": "2",
      "HotelName": "Twin Dome Hotel",
      "Description": "The hotel is situated in a  nineteenth cent...",
      "Category": "Boutique",
      "Tags": [
        "pool",
        "free wifi",
        "air conditioning",
        "concierge"
      ]
    }
  ]
}
```

### 11. 執行混合查詢
同時運行全文和向量查詢

```http request
### Run a hybrid query
POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version=2023-11-01  HTTP/1.1
    Content-Type: application/json
    api-key: {{apiKey}}
```
Request
```json
{
  "count": true,
  "search": "historic hotel walk to restaurants and shopping",
  "select": "HotelId, HotelName, Category, Tags, Description",
  "top": 7,
  "vectorQueries": [
    {
      "vector": [0.01944167, 0.0040178085, -0.007816401, 0.009330357],
      "k": 7,
      "fields": "DescriptionVector",
      "kind": "vector",
      "exhaustive": true
    }
  ]
}
```
Response
```json
{
  "@odata.context": "https://ai-jakeuj.search.windows.net/indexes('hotels-vector-quickstart')/$metadata#docs(*)",
  "@odata.count": 7,
  "value": [
    {
      "@search.score": 0.03306011110544205,
      "HotelId": "49",
      "HotelName": "Old Carrabelle Hotel",
      "Description": "Spacious rooms, glamorous suites and reside...",
      "Category": "Luxury",
      "Tags": [
        "air conditioning",
        "laundry service",
        "24-hour front desk service"
      ]
    },
    {
      "@search.score": 0.032522473484277725,
      "HotelId": "13",
      "HotelName": "Historic Lion Resort",
      "Description": "Unmatched Luxury.  Visit our downtown hotel...",
      "Category": "Resort and Spa",
      "Tags": [
        "view",
        "free wifi",
        "pool"
      ]
    },
    {
      "@search.score": 0.03205128386616707,
      "HotelId": "48",
      "HotelName": "Nordick's Motel",
      "Description": "Only 90 miles (about 2 hours) from the nati...",
      "Category": "Boutique",
      "Tags": [
        "continental breakfast",
        "air conditioning",
        "free wifi"
      ]
    },
    {
      "@search.score": 0.0320020467042923,
      "HotelId": "4",
      "HotelName": "Sublime Cliff Hotel",
      "Description": "Sublime Cliff Hotel is located in the heart...",
      "Category": "Boutique",
      "Tags": [
        "concierge",
        "view",
        "24-hour front desk service"
      ]
    },
    {
      "@search.score": 0.03125763311982155,
      "HotelId": "2",
      "HotelName": "Twin Dome Hotel",
      "Description": "The hotel is situated in a  nineteenth cent...",
      "Category": "Boutique",
      "Tags": [
        "pool",
        "free wifi",
        "air conditioning",
        "concierge"
      ]
    },
    {
      "@search.score": 0.03077651560306549,
      "HotelId": "1",
      "HotelName": "Secret Point Hotel",
      "Description": "The hotel is ideally located on the main ...",
      "Category": "Boutique",
      "Tags": [
        "pool",
        "air conditioning",
        "concierge"
      ]
    },
    {
      "@search.score": 0.03077651560306549,
      "HotelId": "3",
      "HotelName": "Triple Landscape Hotel",
      "Description": "The Hotel stands out for its gastronomic ...",
      "Category": "Resort and Spa",
      "Tags": [
        "air conditioning",
        "bar",
        "continental breakfast"
      ]
    }
  ]
}
```

### 12. 執行混合查詢並進行語意重新排序
混合查詢(全文和向量查詢)與語義重新排序功能，以提升搜索結果的相關性和質量
- queryType: 查詢類型
- semanticConfiguration: 語義配置
- facets: 分類

```http request
### Run a hybrid query with semantic reranking (requires Basic tier or above)
POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version=2023-11-01  HTTP/1.1
    Content-Type: application/json
    api-key: {{apiKey}}
```
Request
```json
{
  "count": true,
  "search": "historic hotel walk to restaurants and shopping",
  "select": "HotelId, HotelName, Category, Description,Address/City, Address/StateProvince",
  "vectorFilterMode": null,
  "filter": "geo.distance(Location, geography'POINT(-77.03241 38.90166)') le 300",
  "facets": [ "Address/StateProvince"],
  "top": 7,
  "queryType": "semantic",
  "semanticConfiguration": "my-semantic-config",
  "vectorQueries": [
    {
      "vector": [0.01944167, 0.0040178085, -0.007816401, 0.009330357, -0.014920352, 0.03203286],
      "k": 7,
      "fields": "DescriptionVector",
      "kind": "vector",
      "exhaustive": true
    }
  ]
}
```
Response
```json
{
  "error": {
    "code": "FeatureNotSupportedInService",
    "message": "Semantic search is not enabled for this service.\r\nParameter name: queryType",
    "details": [
      {
        "code": "SemanticQueriesNotAvailable",
        "message": "Semantic search is not enabled for this service."
      }
    ]
  }
}
```
這邊我用免費層，所以無法使用該功能

- requires Basic tier or above

### 13. 執行範例程式碼刪除索引
類似刪除資料表

```http request
### Delete an index
DELETE  {{baseUrl}}/indexes/hotels-vector-quickstart?api-version=2023-11-01 HTTP/1.1
    Content-Type: application/json
    api-key: {{apiKey}}
```