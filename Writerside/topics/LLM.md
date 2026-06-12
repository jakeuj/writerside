# LLM 本地模型與推論筆記

<web-summary>整理 LLM 本地推論、模型格式、量化、Ollama、llama.cpp、LM Studio 與 vLLM 選型，協助判斷開發、PoC 與正式 serving 的工具路線。</web-summary>

這個分類集中放本地 LLM、模型格式、量化、推論工具與 serving 選型筆記。若只是想快速判斷工具路線，先看比較表；若正在下載 GGUF 模型，再看量化與檔名判讀。

## 建議閱讀順序

1. [llama.cpp、Ollama、LM Studio、vLLM](llm_local_serving_comparison_notes_zh-TW.md)：先判斷本機開發、PoC、小型正式服務與高併發 GPU serving 該選哪個工具。
2. [GGUF、半精度、模型蒸餾與 Q4_K_M 筆記](gguf_fp16_distill_q4km_notes.md)：理解 GGUF、FP16/BF16、Distill、Quantization 與 Q4_K_M 的差異。
3. [Ollama DiffusionGemma](ollama_diffusiongemma_notes_2026-06-12.md)：確認 DiffusionGemma 目前不適合直接用一般 Ollama runner 當主要執行方式。
4. [Ollama 安裝 DeepSeek R1 與 API 使用筆記](Ollama.md)：快速安裝 Ollama、執行模型並開放本機 API。
