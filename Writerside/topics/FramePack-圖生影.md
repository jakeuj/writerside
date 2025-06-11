# FramePack 圖生影

## FramePack 是什麼？

FramePack 是一款革命性的本地端 AI 影片生成工具，能夠僅憑一張靜態圖片和簡單的文字描述，在 NVIDIA 顯卡上生成高品質、超長的動態影片。它最大特色是「固定長度時域上下文」設計，讓影片生成的計算量與記憶體需求不再隨影片長度線性增加，極大降低了硬體門檻[8][11][12][13]。

---

## 主要特色與技術亮點

**1. 超長影片生成**
- 支援生成長達 60 秒甚至 120 秒的影片（30fps 可達 1800~3600 幀），遠超過多數線上平台僅能生成十幾秒短片的限制[8][12][13][17]。

**2. 低硬體門檻**
- 僅需 6GB VRAM（如 RTX 3060），主流筆電顯卡即可流暢運行 13B 參數等級模型[8][12][13][14]。
- 支援 NVIDIA RTX 30/40/50 系列顯卡，需支援 FP16/BF16 計算[12]。

**3. 穩定連貫的動態效果**
- 利用創新的「下一幀預測」神經網路架構，將過去所有畫面的重點濃縮為固定大小的「記憶池」，有效解決長影片常見的「遺忘」與「漂移」問題，畫面一致性極高，細節穩定不變形[7][8][9][11]。

**4. 支援多元應用場景**
- 可將靜態人物照片動畫化，讓角色自然舞動或互動
- 生活場景模擬（如靜止吃飯照變成進食動作）
- 藝術風格轉換（如水墨畫動態化）
- 產品宣傳、創意短片等[8][10][11]。

**5. 開源、免費、易於安裝**
- 完全免費、無審查，適合創作者與企業內容創作
- 提供 GitHub 安裝包，安裝流程簡單[8][17]。

---

## 工作原理

FramePack 採用「下一幀預測」模型，核心在於：
- **上下文壓縮**：將前面所有生成的畫面資訊壓縮成固定長度的上下文，不論影片多長，生成每一幀時所需參考的資訊量始終不變[7][9][11][12]。
- **Patchify 技術**：將每一幀畫面分割成小 patch，進行壓縮與編碼，極大減少運算量並提升 Transformer 模型處理效率[9]。
- **抗漂移/抗遺忘設計**：透過壓縮策略與「倒置抗漂移」取樣法，讓生成過程中細節不易失真，動作流暢且語意一致[7][9]。

---

## 使用方式簡介

1. 安裝 FramePack（GitHub 下載安裝包，解壓後依說明安裝依賴）[8][17]。
2. 上傳一張靜態圖片，或用文字生成圖片。
3. 用自然語言描述想要的動作、場景或風格（如「女孩跳舞」、「貓咪伸懶腰」）。
4. 啟動生成，預覽並導出影片[7][8][17]。

---

## 實際效能與用戶體驗

- 13B 模型僅用 6GB 顯存即可生成 60 秒 30fps 影片，RTX 4090 開啟優化後每秒約 0.6 幀[12][13][14]。
- 支援逐幀預覽，生成過程可即時視覺回饋[12]。
- 畫面穩定、細節豐富、動作自然，適合動畫、創意短片、產品推廣等多種用途[8][10][11]。

---

## 官方 Github
[FramePack](https://github.com/lllyasviel/FramePack)

## 安裝
[安裝](https://github.com/lllyasviel/FramePack?tab=readme-ov-file#installation)

### Windows

[Windows](https://github.com/lllyasviel/FramePack/releases/download/windows/framepack_cu126_torch26.7z)

可以用 WSL 在 Windows 上跑 Linux 版本的 FramePack

好處是可以裝 sageattention 來加速

### linux

Python 3.10.
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev
python3.10 -m venv .venv310
source .venv310/bin/activate
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
pip install sageattention==1.0.6pip install sageattention==1.0.6
pip install -r requirements.txt
python demo_gradio.py
```

## Mac
[Mac](https://github.com/brandon929/FramePack)

FramePack recommends using Python 3.10. If you have homebrew installed, you can install Python 3.10 using brew.

```bash
brew install python@3.10

pip3.10 install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cpu
pip3.10 install -r requirements.txt

python3.10 demo_gradio.py
```

## 雙顯卡

目前沒有支援雙顯卡來加速處理，但是可以開兩個網站分別使用不同顯卡，以同時處理兩張圖各自產生影片

```bash
CUDA_VISIBLE_DEVICES=0 python demo_gradio.py --port 7860  # first card  
CUDA_VISIBLE_DEVICES=1 python demo_gradio.py --port 7861  # second card 
```

## F1
[FramePack-F1](https://github.com/lllyasviel/FramePack/discussions/459) 是一種新型的視頻生成模型，專門設計用於從歷史幀中預測未來幀。這個模型的「F1」代表「前向」版本1，意指其預測方向是向前，而非雙向。這種單向模型相較於傳統的雙向模型，具有更大的靈活性和動態變化，能夠生成更具變化性的視頻內容。
主要特點包括：

- 前向預測：FramePack-F1 僅依賴過去的幀來預測未來的幀，這使得模型在生成過程中能夠更專注於未來的內容，而不會受到過去幀的限制。
- 抗漂移調節：為了減少生成過程中的漂移（即錯誤累積），該模型採用了新的抗漂移調節方法，這一點在未來的研究中將會有更詳細的說明。
- 高效性能：FramePack-F1 能夠在普通的筆記本電腦上運行，並且對於 GPU 的需求相對較低，生成一分鐘的視頻僅需約6GB的顯存，這使得它在資源有限的情況下仍能高效運行。
- 即時反饋：由於其逐幀生成的特性，使用者可以在整個視頻生成過程中即時看到生成的幀，這提供了良好的視覺反饋，讓創作者能夠隨時調整和優化生成過程。

總的來說，FramePack-F1 是一個旨在提升視頻生成效率和質量的創新工具，特別適合需要快速生成高質量視頻內容的用戶。

```bash
python demo_gradio_f1.py
```


## 備註

- 目前測試 MacBook Pro M4 128GB RAM 跑起來約 8~10s/it
- 目前測試 Nvidia 3090 Ti Linux + Sageattention 跑起來約 2~5s/it

## 總結

FramePack 打破了 AI 影片生成對硬體的高門檻限制，讓一般創作者也能輕鬆在本地生成高質量、超長連貫的動態影片。無論是動畫、生活場景模擬還是藝術風格轉換，都能實現流暢自然的視覺效果，是目前 AI 影片生成領域的重大突破[8][9][13]。

## 參考資料
Citations:
1. [1] https://github.com/lllyasviel/FramePack
2. [2] https://the-walking-fish.com/p/framepack/
3. [3] https://www.youtube.com/watch?v=d9FCC_iNlok
4. [4] https://www.youtube.com/watch?v=4RqJL4Y9ODE
5. [5] https://www.toptool.app/en/product/framepack-co
6. [6] https://www.aitoolnet.com/framepack-ai
7. [7] https://frame-pack.org/frame-pack-en
8. [8] https://tenten.co/learning/framepack-ai-review/
9. [9] https://www.digitalocean.com/community/tutorials/framepack-video-generation
10. [10] https://framepack.club
11. [11] https://www.communeify.com/tw/blog/framepack-easy-video-generation
12. [12] https://forum.gamer.com.tw/C.php?bsn=60030&snA=666915
13. [13] https://www.techbang.com/posts/122707-framepack-6gb-gpu-60-sec-ai-video
14. [14] https://lllyasviel.github.io/frame_pack_gitpage/
15. [15] https://fal.ai/models/fal-ai/framepack
16. [16] https://frame-pack.org
17. [17] https://www.youtube.com/watch?v=pX9mvnjdqUw
18. [18] https://www.youtube.com/watch?v=6aeQmWxEr1I
