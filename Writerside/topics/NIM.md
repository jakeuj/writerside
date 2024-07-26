# NIM

[NVIDIA NIM](https://www.nvidia.com/zh-tw/ai/) 是一組易於使用的微服務，旨在加速企業的生成式 AI 部署。
它支持多種 AI 模型，包括 NVIDIA AI 基礎模型和自定義模型，提供無縫、可擴展的 AI 推論功能，無論是在本地環境還是在雲端環境。

NVIDIA NIM 也提供了預建的容器，方便使用者快速部署大型語言模型（LLMs），例如聊天機器人、內容分析器等應用。
每個 NIM 都包含一個容器和一個模型，使用 CUDA 加速的執行環境，對 NVIDIA GPU 提供特殊優化。

特別提到的是，NVIDIA NIM 支持 Llama 3.1 8B-Instruct 模型，
這是一種優化的語言理解、推理和文本生成用途的模型，超越了許多開源聊天機器人的業界基準。

## 登入
使用 Docker 拉取並執行 meta/llama-3_1-8b-instruct（這將下載完整模型並在本機環境中執行）。

```Shell
$ docker login nvcr.io
Username: $oauthtoken
Password: <Your Key>
```
![nvcr.png](nvcr.png)

其中 `<Your Key>` 可以在註冊時取得，或是到 [NVIDIA NGC](https://org.ngc.nvidia.com/setup) 中獲取。

![ngc-setup.png](ngc-setup.png)

## 拉取並執行
使用下面的命令調出並運行英偉達 NIM。這將為您的基礎架構下載最佳化模型。

```Shell
export NGC_API_KEY=<PASTE_API_KEY_HERE>
export LOCAL_NIM_CACHE=~/.cache/nim
mkdir -p "$LOCAL_NIM_CACHE"
docker run -it --rm \
    --gpus all \
    --shm-size=16GB \
    -e NGC_API_KEY \
    -v "$LOCAL_NIM_CACHE:/opt/nim/.cache" \
    -u $(id -u) \
    -p 8000:8000 \
    nvcr.io/nim/meta/llama-3.1-8b-instruct:1.1.0
```
## 呼叫
現在，您可以使用以下 curl 命令進行本機 API 呼叫

```Shell
curl -X 'POST' \
'http://0.0.0.0:8000/v1/chat/completions' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
    "model": "meta/llama-3.1-8b-instruct",
    "messages": [{"role":"user", "content":"可以講中文嗎"}],
    "max_tokens": 64
}'
```

## 參考
[getting-started](https://docs.nvidia.com/nim/large-language-models/latest/getting-started.html)