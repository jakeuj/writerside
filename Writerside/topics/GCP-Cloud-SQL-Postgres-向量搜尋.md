# GCP Cloud SQL Postgres 向量搜尋

> **原文發布日期:** 2024-01-24
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2024/01/24/using-pgvector-llms-and-langchain-with-google-cloud-databases
> **標籤:** 無

---

筆記一下 在 GCP 上使用 Cloud SQL 建立 Postgres 實例並擴充 向量搜尋的步驟

並加入 namespace 字串陣列以達到原本 Vertext AI 向量搜尋中的篩選限制命名空間

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/bee17aac-33fa-45bc-aa33-20ce4dc99000/1706066202.png.png)

## 結論

```
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE embeddings(
      id INTEGER,
      embedding vector(3)
);

INSERT INTO embeddings
           VALUES
                   (1, '[1, 0, -1]'),
                   (2, '[1, 1, 1]'),
                   (3, '[1, 1, 50]');

SELECT id,1 - (embedding <=> '[1, 0, -1]') AS similarity
FROM embeddings
WHERE 1 - (embedding <=> '[1, 0, -1]') > 0.5
ORDER BY similarity DESC
LIMIT 1
```

## 說明

使用 GCP Cloud SQL Postgres 向量搜尋

## 補充

參考 [Filter vector matches  |  Vertex AI  |  Google Cloud](https://cloud.google.com/vertex-ai/docs/vector-search/filtering) 加入限制條件

1. 於向量表加入新文字陣列欄位 namespace

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/bee17aac-33fa-45bc-aa33-20ce4dc99000/1706069069.png.png)

    2. 更新 namespace 資料 1, {val1,val2}

    3. 新增資料 4, [1.0.-1.5], {val3,val2}

    4 搜尋向量 [1, 0.5. -0.5]

```
SELECT id,1 - (embedding <=> '[1, 0.5, -0.5]') AS similarity, namespace
FROM embeddings
WHERE 1 - (embedding <=> '[1, 0.5, -0.5]') > 0.5
ORDER BY similarity DESC
LIMIT 2;
```

可以看到會找到符合的資料 1 與 4

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/bee17aac-33fa-45bc-aa33-20ce4dc99000/1706069540.png.png)

    5. 加入 where 條件 `AND 'val1' =  ANY (namespace)`

```
SELECT id,1 - (embedding <=> '[1, 0.5, -0.5]') AS similarity, namespace
FROM embeddings
WHERE 1 - (embedding <=> '[1, 0.5, -0.5]') > 0.5
AND 'val1' =  ANY (namespace)
ORDER BY similarity DESC
LIMIT 2;
```

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/bee17aac-33fa-45bc-aa33-20ce4dc99000/1706069157.png.png)

可以看到資料 4 的 namespace 因為不包含 `val1` 所以不會出現在搜尋結果

[8.15. 陣列 - PostgreSQL 正體中文使用手冊](https://docs.postgresql.tw/the-sql-language/data-types/arrays#id-8.15.5.-searching-in-arrays)

## 參照

[將 pgvector、LLM 和 LangChain 與 Google Cloud 資料庫結合使用 |Google Cloud 博客](https://cloud.google.com/blog/products/databases/using-pgvector-llms-and-langchain-with-google-cloud-databases)

## 延伸閱讀

[GCP Cloud SQL Proxy 本地連線不開白名單 | 御用小本本 - 點部落 (dotblogs.com.tw)](https://www.dotblogs.com.tw/jakeuj/2023/12/08/gcp-cloud-sql-onnect-auth-proxy)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [CloudSQL](/jakeuj/Tags?qq=CloudSQL)
* [GCP](/jakeuj/Tags?qq=GCP)
* [LLM](/jakeuj/Tags?qq=LLM)
* [PostgreSQL](/jakeuj/Tags?qq=PostgreSQL)
* [Vector Search](/jakeuj/Tags?qq=Vector%20Search)
{ignore-vars="true"}

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
