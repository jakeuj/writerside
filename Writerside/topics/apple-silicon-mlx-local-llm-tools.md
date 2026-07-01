# Apple Silicon Mac 跑本地 LLM 時，MLX、Ollama、LM Studio、oMLX 怎麼選

<web-summary>Apple Silicon Mac 跑本地 LLM 或 VLM 時，先分清楚 MLX、mlx-lm、mlx-vlm、oMLX、LM Studio、Ollama 與 GGUF 的定位，再依聊天、Hugging Face MLX 模型、coding agent 或跨平台部署選工具。</web-summary>

在 Apple Silicon Mac 上，MLX 是底層加速框架，不是直接拿來聊天的 App。想最少設定直接聊天，用 Ollama 或 LM Studio；想跑 Hugging Face 上 `mlx-community/...` 這類 MLX 模型，優先用 `mlx-lm` 或 `mlx-vlm`；想把本機模型長期接給 coding agent 或 OpenAI / Anthropic-compatible client，用 oMLX 會比較像完整後端。

<tldr>
    <p>MLX 是 Apple Silicon 的機器學習底層框架；mlx-lm 與 mlx-vlm 才是直接跑模型的工具。</p>
    <p>Ollama 在 Apple Silicon 上已預覽使用 MLX 加速，但不要把它理解成 Hugging Face MLX repo 的通用載入器。</p>
    <p>文字模型先試 mlx-lm；圖文模型先試 mlx-vlm；coding agent 長期後端優先評估 oMLX。</p>
</tldr>

## 先看結論

最簡單的選法是：

| 情境 | 建議 |
|------|------|
| 想最少設定、直接聊天 | LM Studio 或 Ollama |
| 想跑 Hugging Face 上 `mlx-community/...` 模型 | `mlx-lm` 或 `mlx-vlm` |
| 純文字 LLM | `mlx-lm` |
| 圖文或 VLM，例如 Ornith VL、Qwen-VL、InternVL | `mlx-vlm` |
| 要接 Open WebUI、Aider、Codex、Claude Code、OpenCode | oMLX 或 LM Studio Server |
| 要給 coding agent 長上下文多輪使用 | oMLX 優先 |
| 要跨平台，Linux、NVIDIA、Windows 也能用 | Ollama、llama.cpp、LM Studio |
| 要最透明地 debug 模型相容性 | `mlx-lm` 或 `mlx-vlm` |
| 要 GUI 管理模型 | LM Studio |
| 要 CLI 簡單部署 | Ollama |

一句話版：**MLX 是底層；`mlx-lm` / `mlx-vlm` 是原生推論工具；LM Studio 是 GUI 包裝；oMLX 是 server / agent 後端；Ollama 是本機模型管理與 API 工具，Apple Silicon 版開始預覽 MLX 加速，但不是 MLX Hugging Face 模型的萬用載入器。**

## 工具定位比較

| 名稱 | 它是什麼 | 主要用途 | 模型格式或來源 |
|------|----------|----------|----------------|
| MLX | Apple 的機器學習框架 | 底層加速框架 | 不是模型管理器 |
| `mlx-lm` | MLX 的文字 LLM 套件 | 文字生成、量化、fine-tune、簡易 OpenAI-like server | Hugging Face MLX 模型 |
| `mlx-vlm` | MLX 的圖文 / VLM 套件 | 圖片加文字、VLM、omni model 推論與 fine-tune | Hugging Face MLX VLM 模型 |
| oMLX | MLX 推論伺服器 | 本機 API server、coding agent、多模型、dashboard | MLX-format model |
| LM Studio MLX | LM Studio 的 Apple Silicon MLX 後端 | GUI 管理、聊天、OpenAI-compatible server | LM Studio 下載的 MLX / GGUF 等模型 |
| Ollama | 本機模型管理與推論工具 | 最簡單 CLI / API、模型拉取、工具整合 | Ollama library、Modelfile、支援的 GGUF / Safetensors import |
| GGUF / llama.cpp | 另一套格式與推論生態 | 跨平台、CPU / GPU、Ollama 常見路線 | GGUF 模型 |

## MLX 是底層，不是 App

MLX 是 Apple machine learning research 做的 Apple Silicon array framework，重點是 Apple silicon 的 unified memory 架構、NumPy-like API，以及 Python、Swift、C++、C bindings。它比較像「引擎核心」，不是平常直接開來聊天或管理模型的產品。

所以看到某個工具寫「powered by MLX」時，要先判斷它是在說：

- 底層用 MLX 做 Apple Silicon 加速。
- 可以直接載入 Hugging Face MLX-format model。
- 有沒有模型管理、API server、GUI、agent 整合。

這三件事不一定同時成立。

## mlx-lm 是純文字 LLM 路線

`mlx-lm` 是 MLX 生態裡跑文字 LLM 的 Python package，功能包含文字生成、chat REPL、從 Hugging Face Hub 載入模型、量化與 fine-tuning。它適合拿來先驗證 `mlx-community/...` 文字模型能不能在你的 Mac 上正常跑。

常用指令：

```bash
mlx_lm.generate \
  --model mlx-community/Qwen3-8B-4bit \
  --prompt "請用繁體中文說明你適合做哪些 coding agent 任務。"
```

如果要開簡易 OpenAI-like HTTP server，可以用：

```bash
mlx_lm.server --model mlx-community/Qwen3-8B-4bit
```

不過 `mlx_lm.server` 官方文件明確提醒不建議當 production server，因為它只做基本安全檢查。拿它來本機測試、驗證 prompt、確認模型相容性很適合；要長期給工具或多人服務，通常要換成更完整的 serving layer。

## mlx-vlm 是圖文模型路線

`mlx-vlm` 是針對 Vision-Language Models / Omni Models 的 MLX 套件，可以處理圖片、文字，以及部分 omni model 場景，並支援 CLI、Python API、Gradio chat UI 與 FastAPI server。只要模型需求包含圖片輸入，優先先從 `mlx-vlm` 驗證。

用已安裝的環境執行：

```bash
python -m mlx_vlm.generate \
  --model mlx-community/Qwen2-VL-2B-Instruct-4bit \
  --prompt "Describe this image." \
  --image ./example.png \
  --max-tokens 200 \
  --temperature 0
```

如果想用 `uv` 一次性建立環境執行：

```bash
uv run --with mlx-vlm \
  python -m mlx_vlm.generate \
  --model mlx-community/Qwen2-VL-2B-Instruct-4bit \
  --prompt "Describe this image." \
  --image ./example.png \
  --max-tokens 200 \
  --temperature 0
```

你要測 Ornith 這類 VLM 或 omni model 時，先走 `mlx-vlm` 比直接丟到一般文字 LLM server 更合理。確認圖片能力、processor、chat template、tokenizer 都正常後，再考慮搬到 oMLX 或其他長期服務層。

## LM Studio MLX 是 GUI 加 server 包裝

LM Studio 的 MLX engine 是它自己的後端架構，底層整合 `mlx-lm` 與 `mlx-vlm` 等 MLX 生態元件。LM Studio 0.3.4 之後 Mac 版已內建 MLX engine，所以一般使用者不需要自己處理 Python package、模型路徑與 server 啟動細節。

LM Studio MLX 的優點是：

- GUI 下載與管理模型很省心。
- 可直接聊天、測 prompt、切模型。
- 可以開本機 OpenAI-compatible server。
- 對非工程使用者或 PoC 展示友善。

它的缺點是抽象層比較多。遇到新模型相容性、VLM processor、template 或推論錯誤時，比直接用 `mlx-lm` / `mlx-vlm` 不透明。

## oMLX 是偏 server 和 agent 的 MLX 後端

oMLX 的定位比較像完整本機推論服務平台，而不是單純 command-line runner。它主打 Apple Silicon、OpenAI-compatible 與 Anthropic-compatible API、本機 dashboard、多模型載入、LLM / VLM / embedding / reranker、continuous batching 與 SSD KV cache。

常見啟動方式：

```bash
omlx serve --model-dir ~/.omlx/models
```

或用背景服務：

```bash
omlx start
omlx stop
omlx restart
```

這類工具適合接：

- Codex
- Claude Code
- OpenCode
- Aider
- Open WebUI
- 其他支援 OpenAI-compatible 或 Anthropic-compatible API 的 client

不過新 VLM 模型仍建議先用 `mlx-vlm` 做模型本體驗證。確認模型能吃圖片、輸出正常、processor 沒問題後，再放到 oMLX 當長期後端，排錯成本會低很多。

## Ollama 支援 MLX，但不是 MLX Hugging Face repo 的萬用載入器

Ollama 在 2026-03-30 公告 Apple Silicon 版預覽由 MLX 驅動，目的是利用 Apple unified memory 來提升 Apple Silicon 上的速度；公告也提到在 M5、M5 Pro、M5 Max 上會利用 GPU Neural Accelerators 加速 TTFT 與 generation speed。

但這不等於你可以把任何 `mlx-community/Ornith-1.0-35B-8bit` 直接丟給 Ollama 跑。Ollama 的核心使用方式仍是：

```bash
ollama run <model>
```

或透過 `Modelfile` 建立自訂模型：

```text
FROM ./model.gguf
```

```bash
ollama create my-model -f Modelfile
ollama run my-model
```

Ollama 官方文件也有支援匯入特定 Safetensors 或 GGUF 模型的流程；但實務上你仍要看該架構、量化格式、template、tool calling 與 multimodal 支援是否被 Ollama runner 正確支援。MLX 在 Ollama 這裡比較像「Mac 上的後端加速路線」，不是 `mlx-lm` / `mlx-vlm` 對 Hugging Face MLX community weights 的完整替代。

## Ornith 這類模型怎麼測

以 `mlx-community/Ornith-1.0-35B-8bit` 這種大型 MLX 模型為例，我會這樣分階段測。

第一步，先用 `mlx-vlm` 測模型本體與圖片能力：

```bash
uv run --with mlx-vlm \
  python -m mlx_vlm.generate \
  --model mlx-community/Ornith-1.0-35B-8bit \
  --prompt "請用繁體中文解釋你適合做哪些 coding agent 任務。" \
  --max-tokens 512
```

如果要測圖片能力，再補 `--image`：

```bash
uv run --with mlx-vlm \
  python -m mlx_vlm.generate \
  --model mlx-community/Ornith-1.0-35B-8bit \
  --image ./screenshot.png \
  --prompt "請描述這張截圖中的 UI 問題，並用繁體中文回答。" \
  --max-tokens 512
```

第二步，如果只要純文字 API，可以試 `mlx_lm.server`：

```bash
mlx_lm.server --model mlx-community/Ornith-1.0-35B-8bit
```

但如果你的重點是 VLM 圖片能力，`mlx_lm.server` 不一定是最佳路徑。

第三步，如果要長期給 coding agent 使用，改用 oMLX：

```bash
omlx serve --model-dir ~/.omlx/models
```

第四步，如果只是日常聊天、測 prompt、比較模型，LM Studio 載 MLX 版會最省心。

## 常見誤解

### MLX 模型是不是一定比 GGUF 好

不一定。MLX 在 Apple Silicon 上很有優勢，尤其能吃 unified memory 路線；但 GGUF / llama.cpp 生態更跨平台，模型量、工具整合、部署案例也更多。你要在 Mac 本機榨效能，可以看 MLX；你要跨 Windows、Linux、NVIDIA、CPU-only，GGUF 通常比較好搬。

### LM Studio MLX 和 mlx-lm 是不是同一個東西

不是。LM Studio MLX 是桌面 App 的後端包裝，底層使用 MLX 生態元件；`mlx-lm` 是你可以直接安裝與執行的 Python package。LM Studio 適合日常使用與 GUI 管理，`mlx-lm` 適合透明驗證與 debug。

### Ollama 用 MLX 後，是否就能取代 mlx-lm 和 mlx-vlm

目前不要這樣理解。Ollama 是模型管理、CLI、API 與工具整合體驗；`mlx-lm` / `mlx-vlm` 是 MLX community 模型最直接的原生驗證路線。尤其是新 VLM、omni model、特殊 processor 或特殊 template，先用原生工具測會比較清楚。

### oMLX 和 mlx_lm.server 差在哪裡

`mlx_lm.server` 是方便測試的基本 HTTP server；oMLX 比較像完整服務平台，包含 OpenAI / Anthropic-compatible API、dashboard、多模型管理、KV cache 與 agent 整合。短測用 `mlx_lm.server`；長期服務或 coding agent 後端用 oMLX。

## 實務建議

如果你今天只是想快速知道某個模型能不能跑，先不要急著接 GUI 或 agent。先用最靠近模型格式的工具確認：

1. `mlx-community/...` 純文字模型：先用 `mlx_lm.generate`。
2. `mlx-community/...` VLM 或 omni model：先用 `python -m mlx_vlm.generate`。
3. 確認模型正常後，再搬到 LM Studio 或 oMLX。
4. 如果模型本來就在 Ollama library，或你需要最簡單 CLI / API，才優先用 Ollama。

這樣排錯時會比較乾淨：模型本體、推論工具、API server、GUI / agent client 各自分層，不會一開始就混在一起。

## 參考資料

- [Apple Open Source: MLX](https://opensource.apple.com/projects/mlx/)
- [MLX LM GitHub repository](https://github.com/ml-explore/mlx-lm)
- [MLX LM HTTP Model Server](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/SERVER.md)
- [MLX-VLM GitHub repository](https://github.com/Blaizzy/mlx-vlm)
- [MLX Community on Hugging Face](https://huggingface.co/mlx-community)
- [LM Studio 0.3.4 ships with Apple MLX](https://lmstudio.ai/blog/lmstudio-v0.3.4)
- [oMLX official site](https://omlx.ai/)
- [oMLX GitHub repository](https://github.com/jundot/omlx)
- [Ollama: MLX on Apple Silicon preview](https://ollama.com/blog/mlx)
- [Ollama documentation: Importing a Model](https://docs.ollama.com/import)
