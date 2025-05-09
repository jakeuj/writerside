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

## 備註

- 目前測試 MacBook Pro M4 128GB RAM 跑起來約 8~10s/it
- 目前測試 Nvidia 3090 Ti Linux + Sageattention 跑起來約 2~5s/it