# AnythingLLM

記錄一下使用心得？

## 安裝

```bash
export STORAGE_LOCATION=$HOME/anythingllm && \
mkdir -p $STORAGE_LOCATION && \
touch "$STORAGE_LOCATION/.env" && \
docker run -d -p 3001:3001 \
--cap-add SYS_ADMIN \
-v ${STORAGE_LOCATION}:/app/server/storage \
-v ${STORAGE_LOCATION}/.env:/app/server/.env \
-e STORAGE_DIR="/app/server/storage" \
mintplexlabs/anythingllm
```

## REF

[AnythingLLM + Ollama輕鬆架設多人用的客製化 RAG](https://medium.com/@pang2258/anythingllm-ollama%E8%BC%95%E9%AC%86%E6%9E%B6%E8%A8%AD%E5%A4%9A%E4%BA%BA%E7%94%A8%E7%9A%84%E5%AE%A2%E8%A3%BD%E5%8C%96-rag-2d05954bf771){ignore-vars="true"}
