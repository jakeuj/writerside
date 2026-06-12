# Ollama DiffusionGemma

日期：2026-06-12  
結論狀態：依目前公開文件與模型卡整理，後續可能隨 llama.cpp / Ollama runner 更新而改變。

## 1. 結論

**目前不建議用一般版 Ollama 跑 DiffusionGemma；標準 Ollama 流程基本上不能穩定／正常支援 DiffusionGemma。**

建議操作：

1. **要做服務化或比較正式測試：用 vLLM。**
2. **要跑 GGUF 本機 CLI：用 DiffusionGemma 專用 llama.cpp PR 分支，加 `llama-diffusion-cli`。**
3. **只想用 Ollama 跑 Gemma 系列：改跑一般 Gemma 4，例如 `gemma4` 或 `gemma4:26b`，但那不是 DiffusionGemma。**

簡單判斷：

| 需求 | 建議做法 | 備註 |
|---|---|---|
| 跑 DiffusionGemma 測試 / serving | vLLM | 目前較適合，已有 DiffusionGemma 支援與部署 recipe |
| 跑 GGUF 本機 CLI | llama.cpp PR #24423 + `llama-diffusion-cli` | 標準 `llama-cli` / `llama-server` 不行 |
| 用 Ollama 一行指令跑 | 暫不建議 | 一般 Ollama runner 不支援 DiffusionGemma 的 diffusion decoding |
| 只想跑 Gemma 類模型 | `ollama run gemma4` | 這是一般 Gemma 4，不是 DiffusionGemma |

## 2. 為什麼 Ollama 不適合直接跑

DiffusionGemma 不是一般 autoregressive LLM。一般 LLM 是由左到右逐 token 產生；DiffusionGemma 是文字 diffusion / block diffusion 模型，會把一段 token canvas 反覆 denoise，再提交成輸出。

DiffusionGemma 的推論路徑需要：

- bidirectional attention；
- iterative denoising / refinement；
- block-based generation；
- diffusion 專用 sampler；
- encoder / decoder phase 的狀態切換；
- 對 256-token canvas 的特殊處理。

所以問題不是單純「有沒有 GGUF 檔」而已，而是 runner 必須支援 DiffusionGemma 的 decoding loop。

## 3. DiffusionGemma 模型重點

DiffusionGemma 是 Google DeepMind 發布的實驗性 open-weight 文字生成模型，基於 Gemma 4 26B A4B Mixture-of-Experts 架構。它採用 discrete diffusion 產生文字，支援文字、圖片、影片輸入，輸出文字。

核心特性：

- 架構：Gemma 4 MoE backbone。
- 規模：約 26B total / 約 4B active。
- 生成方式：block diffusion，不是逐 token autoregressive decoding。
- Canvas：常見設定為 256 tokens。
- 適合場景：低 batch、互動式、追求高輸出吞吐的本機或單機 GPU 推論。
- 注意：它是實驗性模型；品質與穩定性不一定取代一般 Gemma 4。

## 4. 推薦方案 A：vLLM

vLLM 已有 DiffusionGemma 支援與官方 recipe。這是目前最乾淨的測試方向。

### 4.1 vLLM Docker 範例

```bash
docker pull vllm/vllm-openai:gemma

docker run -itd --name diffusiongemma \
    --ipc=host --network host --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    vllm/vllm-openai:gemma \
        --model google/diffusiongemma-26B-A4B-it \
        --max-model-len 262144 \
        --max-num-seqs 4 \
        --gpu-memory-utilization 0.85 \
        --host 0.0.0.0 --port 8000
```

### 4.2 vLLM OpenAI-compatible client 範例

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="EMPTY")

response = client.chat.completions.create(
    model="google/diffusiongemma-26B-A4B-it",
    messages=[{"role": "user", "content": "Explain what DiffusionGemma is in two sentences."}],
    max_tokens=512,
    temperature=0.7,
)

print(response.choices[0].message.content)
```

### 4.3 vLLM 部署注意事項

vLLM recipe 對 DiffusionGemma 特別建議：

- `--max-num-seqs 4`：避免 diffusion state buffer 太大造成 OOM。
- `--gpu-memory-utilization 0.85`：保留 activation / denoising headroom。
- 視需求加入 multimodal、tool-call、reasoning parser 相關參數。

## 5. 推薦方案 B：llama.cpp DiffusionGemma PR + GGUF

如果目標是跑 GGUF，本機 CLI 測試可用 DiffusionGemma 專用 llama.cpp PR 分支。

### 5.1 建置 llama.cpp DiffusionGemma 分支

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp

# 方法一：使用 GitHub CLI
gh pr checkout 24423

# 方法二：不用 GitHub CLI
# git fetch origin pull/24423/head:diffusiongemma
# git checkout diffusiongemma

# CUDA build；CPU-only 可移除 -DGGML_CUDA=ON
cmake -B build -DGGML_CUDA=ON
cmake --build build -j --config Release --target llama-diffusion-cli
```

### 5.2 下載 GGUF

```bash
pip install -U "huggingface_hub[cli]"

hf download unsloth/diffusiongemma-26B-A4B-it-GGUF \
    --local-dir unsloth/diffusiongemma-26B-A4B-it-GGUF \
    --include "*Q4_K_M*"
```

常見量化檔大小可抓概念：

| Quant | 約略大小 | 說明 |
|---|---:|---|
| Q4_K_M | 約 16 GB | 最小、較容易放入消費級 GPU |
| Q5_K_M | 約 18 GB | 品質較好 |
| Q6_K | 約 21 GB | 更高品質 |
| Q8_0 | 約 25 GB | 接近 reference |
| BF16 | 約 47 GB | full precision reference |

### 5.3 執行 CLI

```bash
./build/bin/llama-diffusion-cli \
  -m unsloth/diffusiongemma-26B-A4B-it-GGUF/diffusiongemma-26B-A4B-it-Q4_K_M.gguf \
  -ngl 99 \
  -cnv \
  -n 2048 \
  --diffusion-visual
```

參數說明：

- `-ngl 99`：盡量將 layers offload 到 GPU。
- `-cnv`：conversation mode。
- `-n 2048`：目標輸出 token 數。
- `--diffusion-visual`：顯示 canvas denoise 過程。

## 6. Ollama 可以跑什麼？

Ollama 官方 library 有一般 Gemma 4，例如：

```bash
ollama run gemma4
```

或指定版本：

```bash
ollama run gemma4:26b
```

但這是一般 Gemma 4 模型，不是 DiffusionGemma。若你的需求是「在 Ollama 裡用 Gemma 系列做日常推論」，用 `gemma4` 是合理選項；若需求明確是 DiffusionGemma，就不要把它放進目前的 Ollama production 流程。

## 7. 實務建議

### 7.1 目前建議路線

1. 先用 vLLM Docker 跑通 `google/diffusiongemma-26B-A4B-it`。
2. 若要比較 GGUF / local CLI，再測 `unsloth/diffusiongemma-26B-A4B-it-GGUF` + `llama-diffusion-cli`。
3. Ollama 先維持跑一般 Gemma 4，等待後續 runner 支援。

### 7.2 不建議做法

- 不建議直接把 DiffusionGemma GGUF 丟給標準 Ollama。
- 不建議用標準 `llama-cli` / `llama-server` 測 DiffusionGemma GGUF。
- 不建議把目前 DiffusionGemma + Ollama 當 production 方案。

### 7.3 何時可以重新評估 Ollama

可以觀察三件事：

1. llama.cpp DiffusionGemma PR 是否正式 merge 到 master。
2. Ollama 是否更新底層 llama.cpp runner，並明確標示支援 `diffusion-gemma` 架構。
3. Ollama library 是否出現官方或高可信度的 DiffusionGemma 條目與可重現執行範例。

在這三件事完成前，結論維持：**Ollama 不適合作為 DiffusionGemma 的主要執行方式。**

## 8. 參考來源

- Google AI for Developers：DiffusionGemma model overview  
  https://ai.google.dev/gemma/docs/diffusiongemma

- Google / DiffusionGemma Hugging Face model card  
  https://huggingface.co/google/diffusiongemma-26B-A4B-it

- vLLM Blog：DiffusionGemma native support  
  https://vllm.ai/blog/2026-06-10-diffusion-gemma

- vLLM Recipe：Google/diffusiongemma-26B-A4B-it  
  https://recipes.vllm.ai/Google/diffusiongemma-26B-A4B-it

- Unsloth GGUF README：DiffusionGemma GGUF / llama.cpp PR #24423 / llama-diffusion-cli  
  https://huggingface.co/unsloth/diffusiongemma-26B-A4B-it-GGUF/blob/main/README.md

- Atomic Chat GGUF model card：DiffusionGemma GGUF compatibility notes  
  https://huggingface.co/AlexAtomic/diffusiongemma-26B-A4B-it-GGUF

- Ollama library：Gemma 4  
  https://www.ollama.com/library/gemma4
