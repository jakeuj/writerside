# GGUF、半精度、模型蒸餾與 Q4_K_M 筆記

## 1. 總結 {#summary}

**GGUF、半精度、模型蒸餾、量化是不同層次的概念。**

最簡單的區分如下：

| 名詞 | 層次 | 說明 |
|---|---|---|
| GGUF | 檔案格式 | 用來封裝模型權重、tokenizer、metadata 等資訊 |
| FP16 / BF16 | 數值精度 | 權重用半精度格式儲存 |
| Quantization / 量化 | 權重壓縮方法 | 把 FP16/BF16 權重壓成 Q4、Q5、Q8 等低位元格式 |
| Distillation / 蒸餾 | 訓練方法 | 用大模型教小模型，讓小模型模仿大模型輸出 |

一句話整理：

```text
GGUF = 檔案格式
FP16 / BF16 = 半精度權重
Q4 / Q5 / Q8 = 量化後的權重格式
Distill = 經由老師模型訓練出來的學生模型
```

---

## 2. GGUF 跟半精度的關係 {#gguf-and-half-precision}

**GGUF 不是半精度。GGUF 是模型檔案格式；半精度是 GGUF 裡面可能使用的一種權重精度。**

例如：

```text
model-f16.gguf
```

代表：

```text
GGUF 格式 + FP16 半精度權重
```

再例如：

```text
model-q4_k_m.gguf
```

代表：

```text
GGUF 格式 + Q4_K_M 量化權重
```

所以副檔名 `.gguf` 只告訴你這是 GGUF 容器格式，不代表它一定是 FP16、BF16 或 Q4。

真正要看精度，要看檔名或 metadata 裡面的標記：

| 標記 | 意思 |
|---|---|
| F16 | FP16 半精度 |
| BF16 | BF16 半精度 |
| F32 | FP32 單精度，容量最大 |
| Q8_0 | 約 8-bit 量化 |
| Q6_K | 約 6-bit 等級 K-quant 量化 |
| Q5_K_M | 約 5-bit 等級 K-quant 量化，中等版本 |
| Q4_K_M | 約 4-bit 等級 K-quant 量化，中等版本 |
| Q3_K_M | 約 3-bit 等級 K-quant 量化，中等版本 |

---

## 3. 半精度是什麼 {#what-is-half-precision}

半精度通常指：

```text
FP16 或 BF16
```

它們都比 FP32 省空間。

| 格式 | 大約每個數值使用空間 | 說明 |
|---|---:|---|
| FP32 | 32 bit | 傳統單精度，容量大 |
| FP16 | 16 bit | 半精度，常見於 GPU 推理與訓練 |
| BF16 | 16 bit | 半精度，動態範圍通常比 FP16 友善 |
| Q8 | 約 8 bit | 量化，不是浮點半精度 |
| Q4 | 約 4 bit | 更強量化，不是浮點半精度 |

注意：

```text
FP16 / BF16 = 半精度
Q4 / Q5 / Q8 = 量化格式
```

半精度不是量化，但量化通常是從 FP16 或 BF16 權重轉換而來。

---

## 4. 模型蒸餾是什麼 {#what-is-model-distillation}

**模型蒸餾就是用一個較強、較大、較慢的老師模型，去教一個較小、較快、成本較低的學生模型。**

架構可以理解成：

```text
老師模型：大、強、貴、慢
        ↓
學生模型：小、快、便宜、較容易部署
```

學生模型不是直接複製老師模型的權重，而是透過訓練去模仿老師模型的輸出行為。

它可能學到：

```text
老師模型的答案
老師模型的答案排序
老師模型對不同答案的信心分布
老師模型的推理格式
老師模型的語氣與回答風格
老師模型在特定任務上的能力
```

---

## 5. Hard Label 與 Soft Label {#hard-label-and-soft-label}

一般監督式訓練可能只有硬標籤：

```text
問題：台灣的首都是哪裡？
正確答案：台北
```

這叫 hard label。

但模型蒸餾中，老師模型可能輸出一組機率分布：

| 答案 | 老師模型認為的可能性 |
|---|---:|
| 台北 | 92% |
| 新北 | 4% |
| 高雄 | 2% |
| 台中 | 1% |
| 其他 | 1% |

這種機率分布稱為 soft label。

soft label 比 hard label 有更多資訊，因為它不只告訴學生模型「正確答案是什麼」，也告訴學生模型「其他答案有多接近」。

---

## 6. Distill 不等於 Quantized {#distill-vs-quantized}

這點很重要。

| 技術 | 改的是什麼 | 範例 |
|---|---|---|
| 蒸餾 Distillation | 訓練一個較小模型模仿大模型 | 70B 老師教 7B 學生 |
| 量化 Quantization | 把同一個模型的權重用較低位元表示 | FP16 轉 Q4、Q5、Q8 |
| 微調 Fine-tuning | 讓模型針對特定資料或任務再訓練 | 用公司 FAQ 微調客服模型 |
| 剪枝 Pruning | 移除模型中較不重要的結構或參數 | 刪除部分權重或神經元 |

簡單區分：

```text
蒸餾：換成一個小學生模型
量化：同一個模型改用比較省空間的數字格式
微調：同一個模型學新資料或新任務
```

所以這種檔名：

```text
Model-7B-Distill-Q4_K_M.gguf
```

可以拆解為：

| 片段 | 意思 |
|---|---|
| 7B | 約 70 億參數 |
| Distill | 蒸餾模型，模仿某個更強模型 |
| Q4_K_M | 約 4-bit 等級的 K-quant 中等量化版本 |
| GGUF | llama.cpp / Ollama / LM Studio 常見模型格式 |

---

## 7. Q4_K_M 是什麼 {#what-is-q4-k-m}

**Q4_K_M 是 GGUF / llama.cpp 生態中很常見的 4-bit 等級量化格式。**

但它不是每個權重都剛好只佔 4 bit。

更精確地說：

```text
Q4_K_M = 以 4-bit 權重碼為主
         + K-quant 分塊量化
         + 額外 scale / min 等 metadata
         + 部分重要 tensor 可能使用較高 bit 格式
```

所以稱它為：

```text
4-bit 左右量化
```

比說「嚴格 4-bit」更準確。

---

## 8. Q4_K_M 三段拆解 {#q4-k-m-parts}

`Q4_K_M` 可以拆成三段：

| 片段 | 意思 |
|---|---|
| Q4 | 主要權重用 4-bit 量化表示 |
| K | 使用 K-quant 分塊量化方法 |
| M | Medium，中等折衷版本 |

### 8.1 Q4 {#q4-part}

Q4 表示主要權重用 4-bit 代碼表示。

4 bit 可以表示：

```text
2^4 = 16 種值
```

原本 FP16 權重可能是：

```text
-0.8123, -0.3015, 0.0421, 0.5378, 1.2042
```

量化後可能變成類似：

```text
3, 6, 8, 11, 15
```

再搭配 scale / min 等資訊，近似還原原本的值。

概念公式：

```text
原始權重 ≈ 量化代碼 × scale + offset/min
```

量化的核心就是：

```text
用少量 bit 存近似值，而不是完整小數。
```

---

### 8.2 K {#k-part}

K 指的是 K-quant。

K-quant 的重點是分塊量化，不是整個 tensor 只用一組 scale。

概念如下：

```text
一批原始 FP16/BF16 權重
        ↓
分成多個 block / superblock
        ↓
每個權重用 4-bit 代碼保存
        ↓
每個 block 額外保存 scale / min 等資訊
        ↓
推理時用代碼 + scale/min 近似還原
```

分塊量化的好處是可以降低誤差。

如果整個 tensor 只用一組 scale，大值可能會把範圍撐開，導致小值被壓得很粗糙。

分塊後，每個區塊各自有自己的量化範圍：

```text
block A：權重範圍 -0.5 到 0.5，用自己的 scale
block B：權重範圍 -3.0 到 3.0，用自己的 scale
block C：權重範圍 -0.1 到 0.1，用自己的 scale
```

因此通常比全域量化更準。

---

### 8.3 M {#m-part}

M 是 Medium。

它代表中等折衷版本，不是最小，也不是最高品質。

通常可以理解成：

```text
大部分權重：用 Q4_K
部分敏感 tensor：可能使用 Q5_K / Q6_K 等較高精度
整體平均：大約 4.x bits/weight
```

因此 `Q4_K_M` 通常比 `Q4_K_S` 大一點，但品質通常也比較穩。

| 格式 | 特性 |
|---|---|
| Q4_K_S | Small，較小，品質略低 |
| Q4_K_M | Medium，容量與品質折衷 |
| Q5_K_M | 品質更穩，檔案更大 |
| Q6_K | 更接近原始品質，但更吃記憶體 |

---

## 9. 為什麼說 Q4_K_M 是「4-bit 左右」 {#why-q4-k-m-around-4-bit}

因為模型不只需要儲存 4-bit 權重代碼，還需要儲存額外資訊：

```text
scale
min / offset
block metadata
部分較高精度 tensor
```

所以平均下來，每個權重的實際成本通常會超過 4 bit。

常見理解：

```text
Q4_K_M ≠ 每個權重剛好 4 bit
Q4_K_M = 主要用 4-bit 權重碼 + 額外縮放資訊 + 混合策略
```

所以實際上它通常會接近：

```text
4.x bits/weight
```

具體數字會依模型架構與量化工具而異。

---

## 10. 實務選型建議 {#practical-model-selection}

本地跑 LLM 時，可以這樣選：

| 情境 | 建議格式 |
|---|---|
| 第一次下載本地模型 | Q4_K_M |
| RAM / VRAM 很吃緊 | Q4_K_S 或更低 |
| 想要回答穩一點 | Q5_K_M |
| 記憶體夠、希望品質更高 | Q6_K 或 Q8_0 |
| 追求接近原始品質 | F16 / BF16 |
| 不建議一開始用 | Q2、Q3，除非硬體真的不夠 |

一般經驗：

```text
Q4_K_M 是本地 LLM 推理的常見起點。
```

它的定位是：

```text
比 Q3 穩
比 Q5/Q6 省空間
比 FP16 小很多
品質與容量折衷
```

---

## 11. 常見格式比較 {#format-comparison}

| 格式 | 大約定位 | 優點 | 缺點 |
|---|---|---|---|
| F16 / BF16 | 原始或接近原始品質 | 品質高 | 檔案大、吃記憶體 |
| Q8_0 | 高品質量化 | 品質接近 FP16 | 檔案仍偏大 |
| Q6_K | 高品質 K-quant | 穩定、失真少 | 比 Q4 大 |
| Q5_K_M | 品質與容量偏品質 | 比 Q4 穩 | 比 Q4 大 |
| Q4_K_M | 平衡型 | 省空間、品質尚可 | 比 Q5/Q6 容易失真 |
| Q4_K_S | 更小 | 更省記憶體 | 品質略低於 Q4_K_M |
| Q3 / Q2 | 極限壓縮 | 很省空間 | 品質下降明顯 |

---

## 12. 檔名判讀範例 {#filename-reading-examples}

### 範例 1 {#filename-example-f16}

```text
llama-8b-f16.gguf
```

解讀：

```text
8B 模型
GGUF 格式
FP16 半精度權重
容量大，品質高
```

### 範例 2 {#filename-example-q4-k-m}

```text
llama-8b-q4_k_m.gguf
```

解讀：

```text
8B 模型
GGUF 格式
Q4_K_M 量化
容量與品質折衷
適合一般本地推理
```

### 範例 3 {#filename-example-distill-q4-k-m}

```text
deepseek-r1-distill-7b-q4_k_m.gguf
```

解讀：

```text
DeepSeek R1 系列相關模型
Distill = 蒸餾版
7B = 約 70 億參數
Q4_K_M = 約 4-bit 等級量化
GGUF = 本地推理格式
```

---

## 13. 重要觀念整理 {#key-concepts}

### 13.1 GGUF 不等於半精度 {#gguf-not-half-precision}

```text
GGUF 是容器格式。
半精度是權重數值格式。
```

### 13.2 蒸餾不等於量化 {#distillation-not-quantization}

```text
蒸餾是訓練出一個小模型。
量化是壓縮同一個模型的權重表示。
```

### 13.3 Q4_K_M 不等於嚴格 4-bit {#q4-k-m-not-strict-4-bit}

```text
Q4_K_M 是 4-bit 等級量化。
實際平均 bits/weight 通常會超過 4。
```

### 13.4 本地模型選型建議 {#local-model-selection}

```text
不知道選哪個，先試 Q4_K_M。
記憶體夠就往 Q5_K_M / Q6_K / Q8_0 上調。
記憶體不夠才往 Q4_K_S / Q3 下調。
```

---

## 14. 一句話總結 {#one-sentence-summary}

```text
GGUF 是模型檔案格式；FP16/BF16 是半精度；Q4_K_M 是約 4-bit 等級的 K-quant 量化格式；Distill 是用大模型教小模型的訓練方法。
```
