# FramePack 圖生影

Start typing here...

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
FramePack-F1 是一種新型的視頻生成模型，專門設計用於從歷史幀中預測未來幀。這個模型的「F1」代表「前向」版本1，意指其預測方向是向前，而非雙向。這種單向模型相較於傳統的雙向模型，具有更大的靈活性和動態變化，能夠生成更具變化性的視頻內容。
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