# 35B 級距 Coding Agent 模型比較：Ornith-1.0、Qwen3.6、Gemma 4

<web-summary>比較 Ornith-1.0-35B、Qwen3.6-35B 與 Gemma 4 31B 在 coding agent benchmark 與企業內部 MIS 場景的選型差異。</web-summary>

如果目標是修 repo、跑 coding agent、處理 SWE-bench 類任務，先評估 **Ornith-1.0-35B**；如果目標是企業內部中文助理、SOP 問答、RAG 與多人服務，優先評估 **Qwen3.6-35B-A3B**；如果重點在多模態、Google 生態或通用推理，再把 **Gemma 4 31B** 列入候選。

整理日期：2026-07-01  
主要資料來源：[Ornith-1.0: Self-Scaffolding LLMs for Agentic Coding](https://deep-reinforce.com/ornith_1_0.html)

## 一句話結論

**35B 級距裡，Ornith-1.0-35B 是 coding agent benchmark 最強；Qwen3.6-35B-A3B 是企業內部實用性最平衡；Gemma 4 31B 則適合多模態與 Google 生態方向的備選評估。**

若只比較 coding / agentic coding 能力：

1. **Ornith-1.0-35B**
2. **Qwen3.6-35B-A3B**
3. **Gemma 4 31B**

若從企業內部部署、中文能力、長上下文、成本與 MIS 使用場景綜合判斷：

1. **Qwen3.6-35B-A3B**
2. **Ornith-1.0-35B**
3. **Gemma 4 31B**

## 官方 benchmark 圖表

下圖是 Deep Reinforce 官方頁面針對 Ornith-1.0-35B 的 LLM performance evaluation。圖中的 Qwen3.6 欄位以官方圖表名稱 `Qwen3.6-35B` 呈現；實際部署時仍要回到你採用的權重、量化格式與 serving backend 驗證。

![Ornith-1.0-35B、Qwen3.6-35B、Gemma4-31B 在 Terminal-Bench、SWE-bench、NL2Repo、ClawEval 與 SWE Atlas 的效能比較圖](ornith-1-0-35b-llm-performance.png){thumbnail="true" width="720"}

## 三個模型定位

### Ornith-1.0-35B

Ornith-1.0 是 Deep Reinforce 推出的 coding agent 專用模型，主打 repository-level coding、terminal task、bug fixing 與 agentic coding workflow。它不是一般聊天模型優先，而是針對 coding agent 後訓練與強化的模型。

適合用途：

- 程式碼修 bug
- Repo-level agent
- 自動化 coding workflow
- OpenHands / Claude Code 類型任務
- Shell / terminal 任務
- 程式碼庫理解與修改

不適合優先用途：

- 一般中文客服
- 大量內部文件問答
- 低成本多人服務
- 需要多模態或長上下文的企業知識庫

### Qwen3.6-35B-A3B {#qwen3-6-35b-a3b-positioning}

Qwen3.6-35B-A3B 的重點是 35B total / 約 3B active 的 MoE 架構，也就是模型總容量較大，但每個 token 實際啟用的參數較少。這讓它在推理成本與延遲上比較有機會做出實務部署優勢。

適合用途：

- 中文 MIS 助理
- IT Helpdesk 問答
- SOP / KB / RAG
- AD、M365、網路、資安流程查詢
- PowerShell / Python 腳本輔助
- 長文件分析
- 內部系統操作說明
- 多人併發服務

可能限制：

- 純 coding agent benchmark 略低於 Ornith-1.0-35B
- 仍需要實測部署框架、量化版本與 GPU / Apple Silicon 配置

### Gemma 4 31B {#gemma-4-31b-positioning}

Gemma 4 是 Google DeepMind 的開放模型系列。35B 級距附近可對應 Gemma 4 31B，強項比較偏多模態、數學、推理、長上下文與 Google 生態整合。

適合用途：

- 圖文理解
- 多模態問答
- 文件摘要
- 通用推理
- Google / TPU 生態
- 輕量或端側部署評估

不適合優先用途：

- Repo agent
- SWE-bench 類修 bug 任務
- Terminal automation
- 專門 coding agent 工作流

## 35B 級距 coding benchmark 比較

依 Ornith-1.0 官方頁面列出的同級比較，Ornith-1.0-35B 在多數 coding / agent benchmark 上領先 Qwen3.6-35B 與 Gemma4-31B。

| Benchmark | Ornith-1.0-35B | Qwen3.6-35B | Gemma4-31B | 判斷 |
|---|---:|---:|---:|---|
| Terminal-Bench 2.1 | **64.2** | 52.5 | 42.1 | Ornith 明顯領先 |
| Terminal-Bench 2.1 Claude Code | **62.8** | 49.2 | - | Ornith 明顯領先 |
| SWE-Bench Verified | **75.6** | 73.4 | 52.0 | Ornith 小幅領先 Qwen，明顯領先 Gemma |
| SWE-Bench Pro | **50.4** | 49.5 | 35.7 | Ornith 與 Qwen 接近，Ornith 略高 |
| SWE-Bench Multilingual | **69.3** | 67.2 | 51.7 | Ornith 小幅領先 Qwen |
| NL2Repo | **34.6** | 29.4 | 15.5 | Ornith 明顯領先 |
| ClawEval Avg | **69.8** | 68.7 | 48.5 | Ornith 小幅領先 Qwen |

Ornith-1.0-35B 在 Terminal-Bench、NL2Repo 這類更接近 agent 實作能力的任務上優勢明顯。Qwen3.6-35B 雖然在多數 coding benchmark 略低於 Ornith，但差距並非全面懸殊；再加上 MoE 架構、中文能力與部署成本，企業內部的實務價值仍然很高。

Gemma 4 31B 在 coding agent 任務中明顯落後，但這不代表模型本身弱，而是它的強項不在這組 benchmark。

## 依使用場景選型

| 使用場景 | 建議模型 | 原因 |
|---|---|---|
| 修 bug、repo agent、SWE-bench 類任務 | **Ornith-1.0-35B** | coding agent benchmark 最強 |
| 終端機任務、shell automation | **Ornith-1.0-35B** | Terminal-Bench 表現最佳 |
| 企業內部中文助理 | **Qwen3.6-35B-A3B** | 中文、成本、部署彈性較佳 |
| MIS SOP / KB / RAG | **Qwen3.6-35B-A3B** | 長文件與中文問答更適合 |
| PowerShell / Python 腳本輔助 | **Qwen3.6-35B-A3B 或 Ornith-1.0-35B** | 一般腳本 Qwen 足夠，複雜 repo 修復 Ornith 更強 |
| 多模態圖文理解 | **Gemma 4 31B 或 Qwen3.6-35B-A3B** | Gemma 與 Qwen 都可列入評估 |
| Google 生態 / TPU | **Gemma 4 31B** | Google 生態整合優勢 |
| 多人併發內部服務 | **Qwen3.6-35B-A3B** | 約 3B active，推理成本較有利 |

## MIS 場景建議

以企業 MIS 內部使用來看，不要只看單一 benchmark，可以拆成兩種模型角色。

### 主模型：Qwen3.6-35B-A3B {#qwen3-6-35b-a3b-mis-main}

Qwen3.6-35B-A3B 適合作為內部 AI 助理的主要模型，負責 IT Helpdesk、內部 SOP 查詢、AD / M365 / Exchange / VPN / 防火牆設定說明、PowerShell / Python / SQL 腳本產生、資安事件初步說明、Log 解讀與知識庫 RAG。

選它的主要原因是中文能力、MoE 成本優勢、長文件能力與通用能力比較平衡。企業內部服務通常不是追求單項 benchmark 最高，而是希望穩定、便宜、多人可用，還要能處理中文文件與內部操作脈絡。

### 專用 coding agent：Ornith-1.0-35B

Ornith-1.0-35B 適合作為第二模型，專門處理程式碼與 repo-level 任務，例如修復內部工具 bug、分析 Git repo、產生 PR patch、解釋大型程式碼庫、自動化 terminal workflow 或重構複雜腳本。

它的價值在於 coding agent benchmark 明顯強，尤其是 Terminal-Bench、SWE-Bench、NL2Repo 這類接近實際 agent 工作流的任務。

### 輔助評估模型：Gemma 4 31B {#gemma-4-31b-mis-evaluation}

Gemma 4 31B 可作為多模態或 Google 生態方向的備選，例如圖片 / 文件混合問答、通用推理、Google 生態整合、TPU 或端側部署測試。

但若目標是 MIS 內部 AI 助理或 coding agent，Gemma 4 31B 不建議作為第一優先。

## 最終建議

如果只能選一個，選 **Qwen3.6-35B-A3B**。原因是它在中文、部署成本、長上下文、通用能力與 coding 能力之間最平衡，對企業內部服務比較像能長期使用的主力模型。

如果可以選兩個，建議組合：

1. **Qwen3.6-35B-A3B**：內部中文助理 / RAG / SOP / Helpdesk 主模型。
2. **Ornith-1.0-35B**：coding agent / repo 修 bug / terminal automation 專用模型。

不建議只因為 Gemma 4 是 Google 系列就優先拿來做 coding agent。Gemma 4 可以評估，但它在目前這組 35B 級距的 coding agent benchmark 中不是最強選項。

## 參考資料

- [Ornith-1.0: Self-Scaffolding LLMs for Agentic Coding](https://deep-reinforce.com/ornith_1_0.html)
