# GCP Vector Search

> **原文發布日期:** 2023-10-31
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/10/31/GCP-Vector-Search-Namespace-Filtering
> **標籤:** 無

---

向量搜尋時過濾命名空間的筆記

## 簡介

藉由建立向量索引時指定命名空間

來達到向量搜尋時作為過濾條件使用

### 範例

#### 新增

[新增向量資料](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/use-cases/document-qa/utils/matching_engine.py#L138)時指定 restricts [{color: red, blue}, {shape: square}]

```
def add_texts(
        self,
        texts: Iterable[str],
        metadatas: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> List[str]:
        """Run more texts through the embeddings and add to the vectorstore.

        Args:
            texts: Iterable of strings to add to the vectorstore.
            metadatas: Optional list of metadatas associated with the texts.
            kwargs: vectorstore specific parameters.

        Returns:
            List of ids from adding the texts into the vectorstore.
        """
        logger.debug("Embedding documents.")
        embeddings = self.embedding.embed_documents(list(texts))
        insert_datapoints_payload = []
        ids = []

        # Streaming index update
        for idx, (embedding, text, metadata) in enumerate(
            zip(embeddings, texts, metadatas)
        ):
            id = uuid.uuid4()
            ids.append(id)
            self._upload_to_gcs(text, f"documents/{id}")
            metadatas[idx]
            insert_datapoints_payload.append(
                aiplatform_v1.IndexDatapoint(
                    datapoint_id=str(id),
                    feature_vector=embedding,
                    restricts=metadata if metadata else [],
```

P.S. 例如：`metadatas:[{color: red, blue}, {shape: square}]`

#### 搜尋

[搜尋](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/use-cases/document-qa/utils/matching_engine.py#L188)時指定 restricts : [{"namespace": "class", "allow": ["cat", "pet"]},{"namespace": "category", "allow": ["feline"]}]

```
def get_matches(
        self,
        embeddings: List[str],
        n_matches: int,
        index_endpoint: MatchingEngineIndexEndpoint,
    ) -> str:
        """
        get matches from matching engine given a vector query
        Uses public endpoint

        """
        import requests
        import json

        request_data = {
            "deployed_index_id": index_endpoint.deployed_indexes[0].id,
            "return_full_datapoint": True,
            "queries": [
                {
                    "datapoint": {
                        "datapoint_id": f"{i}",
                        "feature_vector": emb,
                        "restricts": [{"namespace": "class", "allow": ["cat", "pet"]},{"namespace": "category", "allow": ["feline"]}]
                        },
                    "neighbor_count": n_matches,
                }
                for i, emb in enumerate(embeddings)
            ],
        }
```

P.S. 實際上這邊應該將 restricts 改由 function Parameter 帶入 (例如：metadatas: Optional[List[dict]] = None,)

### 參照

[过滤矢量匹配  |  Vertex AI  |  Google Cloud](https://cloud.google.com/vertex-ai/docs/matching-engine/filtering?hl=zh-cn)

[Google Cloud Ai Platform V1 Client - Class IndexDatapoint (0.26.1)](https://cloud.google.com/php/docs/reference/cloud-ai-platform/latest/V1.IndexDatapoint)

[generative-ai/language/use-cases/document-qa/utils/matching\_engine.py at main · GoogleCloudPlatform/generative-ai · GitHub](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/use-cases/document-qa/utils/matching_engine.py#L138)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- GCP
- Matching Engine
{ignore-vars="true"}
- Vector Search
{ignore-vars="true"}
- Vertex AI
{ignore-vars="true"}

- 回首頁

---

*本文章從點部落遷移至 Writerside*
