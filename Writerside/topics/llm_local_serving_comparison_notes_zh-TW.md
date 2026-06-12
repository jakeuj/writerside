# llama.cpp、Ollama、LM Studio、vLLM

<web-summary>比較 llama.cpp、Ollama、LM Studio 與 vLLM 的定位、模型格式、部署場景與企業內部 LLM serving 選型建議。</web-summary>

整理日期：2026-06-12  
適用情境：本地 LLM、內網部署、開發者工作站、GPU 推論服務選型

---

## 一句話結論

**llama.cpp、Ollama、LM Studio 偏向本機與輕量部署；vLLM 偏向 GPU server 上的高併發推論服務。**

更精準地說：

- **llama.cpp**：底層 C/C++ 推論引擎，主打可控、輕量、GGUF、CPU/GPU 混合推論。
- **Ollama**：開發者友善的本地模型管理與 API 服務，適合快速拉模型、跑模型、串 API。
- **LM Studio**：圖形化本地 LLM 工作站，適合非工程使用者、PoC、模型挑選、文件聊天。
- **vLLM**：高吞吐 GPU serving engine，適合多人併發、RAG backend、內部 Copilot、正式 API 服務。

---

## 最快選型規則

| 需求 | 建議工具 |
|---|---|
| 單機聊天、主管展示、非工程使用者試模型 | **LM Studio** |
| 工程師本機開發、快速串本地 API | **Ollama** |
| 內網小型服務、普通 PC、CPU/消費級 GPU、GGUF 可控部署 | **llama.cpp** |
| GPU server、多人併發、高吞吐、正式 API serving | **vLLM** |
| 模型挑選與 PoC | **LM Studio + Ollama** |
| 正式上線、需要壓測與可控維運 | **llama.cpp 或 vLLM** |

---

## 四者的層級關係

這四個工具不是完全同類型產品，應該分層看。

```text
使用者 / 系統
  ├─ Web UI / RAG / Agent / VS Code / 內部系統
  │
  ├─ OpenAI-compatible API
  │
  ├─ 後端推論服務
  │    ├─ PoC / 本機：LM Studio 或 Ollama
  │    ├─ 輕量正式服務：llama.cpp server
  │    └─ 高併發 GPU 服務：vLLM
  │
  └─ 模型
       ├─ GGUF：llama.cpp / Ollama / LM Studio 主場
       └─ Hugging Face safetensors / AWQ / GPTQ / FP8：vLLM 主場
```

簡化理解：

```text
桌面使用 / 本機開發：LM Studio、Ollama
底層輕量推論：llama.cpp
正式 GPU Serving：vLLM
```

---

## 總表比較

| 項目 | llama.cpp | Ollama | LM Studio | vLLM |
|---|---|---|---|---|
| 定位 | 底層推論引擎 | 本地模型管理 + API daemon | GUI 本地 LLM 工作站 | 高吞吐 GPU serving engine |
| 主要使用者 | MIS、DevOps、平台工程師 | 開發者 | 一般使用者、PM、PoC 團隊 | AI 平台、後端、MLOps |
| 典型場景 | 內網小服務、邊緣部署、效能調校 | 本機 API、開發測試、Coding tools | 聊天、文件問答、模型試跑 | 多人 API、RAG backend、agent backend |
| 易用性 | 低 | 高 | 最高 | 中低 |
| 控制力 | 最高 | 中高 | 中 | 高 |
| GUI | 無，CLI/server 為主 | 無，CLI/API 為主 | 強項 | 無，server/API 為主 |
| API | llama-server 可提供 OpenAI-compatible API | 內建本地 API | 內建本地 API server | OpenAI-compatible server |
| 模型格式主場 | GGUF | Ollama model store / Modelfile / GGUF | GGUF / Hugging Face 模型下載 | Hugging Face / safetensors / AWQ / GPTQ / FP8 |
| CPU 支援 | 強 | 可用 | 可用 | 非主戰場 |
| 消費級 GPU | 可用 | 可用 | 可用 | 可用但更偏 server GPU |
| 多 GPU / 高併發 | 可做但不是主強項 | 不是主強項 | 不適合正式多人 serving | 強項 |
| 正式企業 serving | 適合小中型、可控部署 | 適合快速落地、開發者服務 | 不建議當正式多人後端核心 | 適合高併發正式服務 |
| 學習成本 | 高 | 低 | 低 | 中高 |
| 授權/開源 | MIT 開源 | MIT 開源 | Desktop app 較封閉，需看條款 | Apache-2.0 開源 |

---

## llama.cpp

### 定位

**llama.cpp 是底層 C/C++ LLM 推論引擎。**  
它的核心價值是可攜、輕量、可控，特別適合在 CPU、Apple Silicon、消費級 GPU、邊緣設備或內網伺服器上執行 GGUF 模型。

### 優點

- 控制力最高，可細調 GPU offload、context、batch、threads、KV cache 等參數。
- 支援 GGUF 與多種量化格式，適合在有限 VRAM/RAM 下跑模型。
- 可透過 `llama-server` 開 HTTP API，支援 OpenAI-compatible API。
- 適合離線部署、內網部署、資安可控環境。
- C/C++ 實作，部署相對輕量，不一定需要完整 Python/MLOps stack。

### 缺點

- 使用門檻較高。
- 模型下載、量化、路徑、參數、效能調校多半要自己處理。
- 對大量併發與高吞吐 GPU serving，不是最省事的選擇。

### 適合情境

- 單機或小型內網 LLM 服務。
- CPU/消費級 GPU 環境。
- 對部署可控性、離線性、可稽核性要求較高。
- 想直接掌控 GGUF 模型與推論參數。

---

## Ollama

### 定位

**Ollama 是開發者友善的本地模型管理與 API 服務。**  
它把模型下載、執行、服務化包裝起來，讓開發者用很少指令就能在本機跑 LLM。

常見用法：

```bash
ollama pull llama3.1
ollama run llama3.1
ollama serve
```

### 優點

- 上手最快，CLI 很直覺。
- 內建本地 API，適合程式串接。
- 可用 `Modelfile` 自訂 system prompt、template、參數、adapter。
- 適合 VS Code、RAG demo、agent、LangChain、內部工具快速整合。
- 對工程師而言，比直接操作 llama.cpp 省很多時間。

### 缺點

- 抽象層較高，底層參數可控性不如 llama.cpp。
- 大量併發、高吞吐、多 GPU serving 不是主要強項。
- 模型與 runtime 管理由 Ollama 包起來，企業正式部署時需額外規劃版本、模型來源、cache 路徑與權限。

### 適合情境

- 工程師本機開發。
- 快速建立本地 OpenAI-like API endpoint。
- 小型內部工具、PoC、RAG demo。
- 想快速測模型，而不想管理底層推論細節。

---

## LM Studio

### 定位

**LM Studio 是圖形化本地 LLM 工作站。**  
它的核心價值是使用體驗：模型搜尋、下載、聊天、調參、文件聊天、本地 API server 都能透過 GUI 完成。

### 優點

- GUI 體驗最好。
- 適合非工程使用者直接試用模型。
- 可搜尋與下載 Hugging Face 模型。
- 支援本地聊天、文件聊天、prompt/config 管理。
- 可啟用本地 API server，供其他程式呼叫。
- 適合 PoC、demo、模型比較、內部展示。

### 缺點

- Desktop app 不是像 llama.cpp / Ollama / vLLM 那樣完整開源的基礎設施元件。
- 不建議當正式多人服務後端核心。
- 企業資安稽核時，要特別確認授權、版本更新、runtime 下載、模型下載來源、local logs 與資料保存位置。

### 適合情境

- 主管、PM、客服、內部使用者試用本地模型。
- 模型挑選、prompt 測試、文件聊天 demo。
- 不想先寫程式，只想先確認模型效果。

---

## vLLM

### 定位

**vLLM 是高吞吐 LLM serving engine。**  
它跟 llama.cpp 一樣屬於推論/serving 後端，但設計目標不同：vLLM 的重點是 GPU server 上的多人併發、高 throughput、OpenAI-compatible API、KV cache 管理與 serving 效率。

### 核心價值

vLLM 的代表性技術是 **PagedAttention**。  
PagedAttention 的目的，是改善 LLM serving 時 KV cache 動態成長、記憶體碎片、batch size 受限等問題，讓 GPU 在多請求併發時可以更有效率地被使用。

### 優點

- 適合正式 API serving。
- 適合多人併發、高吞吐場景。
- 支援 OpenAI-compatible HTTP server。
- 適合 RAG backend、內部 Copilot、客服助理、agent gateway。
- 支援 tensor parallel、pipeline parallel 等 server-side scaling 能力。
- 生態偏向 Hugging Face / MLOps / Kubernetes / Ray / GPU cluster。

### 缺點

- 部署複雜度高於 Ollama、LM Studio。
- 通常需要較完整的 Python/GPU/MLOps 環境。
- 不適合拿來取代 LM Studio 的 GUI 體驗。
- 也不應把它簡單視為「更快的 GGUF llama.cpp」；vLLM 對 GGUF 的支援不是它的主場。

### 適合情境

- 一整個部門或多系統共用 LLM API。
- 需要高併發、低延遲、高吞吐。
- 有 NVIDIA/AMD/Intel server GPU。
- 要部署 RAG、內部 Copilot、客服助理、agent backend。
- 要把 LLM 服務納入正式監控、壓測、擴縮容與平台治理。

---

## vLLM 與 llama.cpp 的關係

**兩者同屬推論/serving 引擎，但最佳場景不同。**

| 比較點 | llama.cpp | vLLM |
|---|---|---|
| 主戰場 | 本機、邊緣、CPU/消費級 GPU、GGUF | GPU server、高併發 API serving |
| 模型格式 | GGUF | Hugging Face / safetensors / AWQ / GPTQ / FP8 |
| 部署難度 | 中，高度可控 | 中高，偏 MLOps |
| 效能方向 | 輕量、可攜、低資源可跑 | 高吞吐、高併發、GPU utilization |
| 適合角色 | MIS、DevOps、平台工程師 | AI 平台、MLOps、後端工程師 |
| 正式服務 | 適合小中型服務 | 適合中大型服務 |

簡單判斷：

- **普通 PC / CPU / 消費級 GPU / GGUF：優先 llama.cpp。**
- **GPU server / 多人 API / 高吞吐：優先 vLLM。**

---

## vLLM 與 Ollama 的關係

**Ollama 偏開發者本機工具，vLLM 偏正式服務後端。**

Ollama 解決的是「如何快速在本機把模型跑起來並開 API」。  
vLLM 解決的是「如何在 GPU server 上高效率地服務大量請求」。

| 比較點 | Ollama | vLLM |
|---|---|---|
| 主要用途 | 本機開發、快速 API | 正式 serving、高併發 API |
| 上手難度 | 低 | 中高 |
| 模型管理 | 內建 model pull / Modelfile | 多依賴 Hugging Face / MLOps 流程 |
| 高併發能力 | 非主強項 | 強項 |
| 適合部署 | 工程師工作站、小型服務 | GPU server、平台服務 |

簡單判斷：

- **開發者本機：Ollama。**
- **正式多人服務：vLLM。**

---

## vLLM 與 LM Studio 的關係

**LM Studio 是前台工作站，vLLM 是後台 serving engine。**

LM Studio 重點在 GUI、聊天、模型下載、文件問答、使用者體驗。  
vLLM 重點在 HTTP API、GPU 效率、併發、batching、KV cache、服務治理。

| 比較點 | LM Studio | vLLM |
|---|---|---|
| 主要用途 | GUI 試用、PoC、模型挑選 | 正式 API serving |
| 使用者 | 非工程使用者、PM、測試者 | 後端、MLOps、AI 平台 |
| GUI | 強 | 無 |
| 文件聊天 | 內建體驗佳 | 通常由上層 RAG 系統處理 |
| 多人正式服務 | 不建議當核心 | 適合 |

簡單判斷：

- **要給人直接操作：LM Studio。**
- **要給系統大量呼叫：vLLM。**

---

## 模型格式與部署注意事項

### GGUF 生態

GGUF 是 llama.cpp 生態的主力格式。  
以下工具都很常見於 GGUF 場景：

- llama.cpp
- Ollama
- LM Studio

GGUF 的優勢是方便量化、方便本地跑、對 CPU/消費級 GPU 友善。

### Hugging Face / safetensors 生態

vLLM 的主場通常是 Hugging Face 模型格式與 serving-oriented quantization，例如：

- safetensors
- AWQ
- GPTQ
- FP8
- INT8 / INT4

這類格式與生態更常見於正式 GPU serving、MLOps、Kubernetes、Ray、模型倉庫與 CI/CD 流程。

### 不建議的誤解

不要把 vLLM 視為「更快的 Ollama」或「更快的 LM Studio」。  
也不要直接把 vLLM 視為「更快的 GGUF llama.cpp」。

比較合理的理解是：

```text
llama.cpp：本機與輕量部署的底層引擎
Ollama：包裝好的開發者本機模型服務
LM Studio：GUI 本地模型工作站
vLLM：正式 GPU API serving 引擎
```

---

## 企業內部導入建議

### PoC 階段

建議使用：

```text
LM Studio + Ollama
```

原因：

- LM Studio 給非工程人員快速試模型、試 prompt、試文件聊天。
- Ollama 給工程師快速串 API、做 RAG demo、測 agent flow。
- 這個階段重點是驗證模型效果，不是追求最終效能。

### 小型正式服務

建議使用：

```text
llama.cpp server 或 Ollama service
```

適合條件：

- 使用者數量不多。
- 併發量有限。
- 單台工作站或單張消費級 GPU 即可承擔。
- 重視離線、簡單維運、內網部署。

### 中大型正式服務

建議使用：

```text
vLLM
```

適合條件：

- 多人同時使用。
- 多系統共用 LLM API。
- 有 GPU server。
- 需要監控、壓測、擴縮容、服務等級管理。
- 要支援 RAG、客服助理、內部 Copilot、agent gateway。

---

## MIS 角度的落地架構

建議分三層處理。

```text
第一層：使用者入口
  - Web UI
  - Chat UI
  - 文件問答系統
  - VS Code / IDE plugin
  - 內部系統 API

第二層：LLM Gateway
  - 權限控管
  - API key
  - rate limit
  - logging
  - prompt policy
  - model routing
  - audit trail

第三層：推論後端
  - PoC：LM Studio / Ollama
  - 小型正式：llama.cpp / Ollama
  - 高併發正式：vLLM
```

### 為什麼需要 LLM Gateway

不建議讓所有系統或所有使用者直接打推論服務。  
即使是內網，也應該透過 gateway 控制：

- 誰可以用哪個模型。
- 每個人或每個系統的呼叫量。
- 是否允許上傳文件。
- prompt 與回應是否要留存。
- 是否記錄 token usage。
- 是否允許敏感資料輸入。
- 是否要做內容過濾或遮罩。

---

## 資安與治理注意事項

### 1. 本地推論不等於零風險

即使模型在本機或內網跑，仍然可能有以下風險：

- prompt history
- chat log
- model cache
- runtime cache
- API logs
- crash logs
- 使用者上傳文件暫存
- 模型下載來源風險
- plugin / extension / MCP server 風險

### 2. 模型授權要獨立審查

工具可商用，不代表模型權重可商用。  
導入時至少要確認：

- 模型 license。
- 是否允許商業使用。
- 是否允許內部再散布。
- 是否允許 fine-tune。
- 是否要求標註來源。
- 是否有限制用途。

### 3. 固定版本與模型來源

正式服務建議固定：

- 模型名稱。
- 模型版本。
- quantization 格式。
- runtime 版本。
- container image。
- prompt template。
- context length。
- sampling parameters。

不要讓 production 服務自動抓 latest model 或 latest runtime。

### 4. 記錄與稽核

至少應規劃：

- API 呼叫者。
- 使用模型。
- token usage。
- 時間戳記。
- 錯誤碼。
- latency。
- 是否保留 prompt 與 completion。
- 敏感資料遮罩規則。

---

## 最終建議

若公司只是要先導入本地 LLM，建議路線如下：

```text
第一步：LM Studio
  用來讓非工程使用者測模型、測文件問答、測 prompt。

第二步：Ollama
  給工程師串 API，快速做內部工具、RAG、agent demo。

第三步：llama.cpp
  對小型正式服務做可控部署，尤其是 GGUF、CPU/消費級 GPU、離線內網場景。

第四步：vLLM
  當需求進入多人併發、GPU server、正式 API serving，再導入 vLLM。
```

簡化成一句話：

> **LM Studio 用來試，Ollama 用來開發，llama.cpp 用來可控部署，vLLM 用來正式高併發 serving。**

---

## 參考來源

以下為整理時參考的官方文件與技術資料：

1. llama.cpp GitHub repository  
   https://github.com/ggml-org/llama.cpp

2. llama.cpp server README  
   https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md

3. Ollama API documentation  
   https://docs.ollama.com/api/introduction

4. Ollama CLI documentation  
   https://docs.ollama.com/cli

5. Ollama GPU documentation  
   https://docs.ollama.com/gpu

6. Ollama GitHub repository  
   https://github.com/ollama/ollama

7. LM Studio documentation  
   https://lmstudio.ai/docs

8. LM Studio local server documentation  
   https://lmstudio.ai/docs/developer/core/server

9. LM Studio offline documentation  
   https://lmstudio.ai/docs/app/offline

10. LM Studio app terms  
    https://lmstudio.ai/app-terms

11. vLLM OpenAI-compatible server documentation  
    https://docs.vllm.ai/en/stable/serving/openai_compatible_server/

12. vLLM GPU installation documentation  
    https://docs.vllm.ai/en/stable/getting_started/installation/gpu/

13. vLLM GGUF documentation  
    https://docs.vllm.ai/en/latest/features/quantization/gguf/

14. vLLM / PagedAttention paper  
    https://arxiv.org/abs/2309.06180
