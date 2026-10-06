# FramePack Windows 一鍵包支援 RTX 5090：升級 PyTorch cu128 與 SageAttention

<web-summary>FramePack Windows 一鍵包內建 torch 2.6.0+cu126，在 RTX 5090 等 Blackwell（sm_120）顯卡會出現 no kernel image 錯誤；用一鍵包內建 Python 升級到 torch 2.10.0+cu128，再加裝 triton-windows 與 SageAttention 即可正常生成並加速。</web-summary>

RTX 5090 跑不動 FramePack 一鍵包，原因是包內的 PyTorch 太舊，沒有 Blackwell 架構（sm_120）的 CUDA kernel。改 bf16、fp32 或程式碼都沒有用。只要用一鍵包**內建的 Python** 把 PyTorch 換成 CUDA 12.8 以上的版本即可；想再加速，就補上 triton-windows 與 SageAttention。

<tldr>
<p>升級：用 <code>system\python\python.exe -m pip</code> 安裝 torch 2.10.0、torchvision 0.25.0、torchaudio 2.10.0（cu128 index），並固定 numpy 1.26.2。</p>
<p>加速：補 Python include/libs，再裝 triton-windows 3.6 與 SageAttention 2.2.0 post6。</p>
<p>驗證：<code>torch.cuda.get_arch_list()</code> 要包含 <code>sm_120</code>。</p>
</tldr>

以下步驟於 2026 年 10 月在 Windows 11、RTX 5090（32 GB）、NVIDIA driver 616.92 上實測；路徑以 `C:\framepack_cu126_torch26` 為例，請換成自己的解壓目錄。

## 症狀 {#symptoms}

啟動 `run.bat` 後先出現警告：

```text
UserWarning: NVIDIA GeForce RTX 5090 with CUDA capability sm_120 is not compatible with the current PyTorch installation.
The current PyTorch install supports CUDA capabilities sm_50 sm_60 sm_61 sm_70 sm_75 sm_80 sm_86 sm_90.
```

按下 Start Generation 後，在 `diffusers_helper/hunyuan.py` 的 `encode_prompt_conds()` 失敗：

```text
File "...\webui\diffusers_helper\hunyuan.py", line 31, in encode_prompt_conds
    llama_attention_length = int(llama_attention_mask.sum())
RuntimeError: CUDA error: no kernel image is available for execution on the device
```

這行只是第一個在 GPU 上執行的運算，任何 CUDA 運算都會在同一個地方失敗。

## 根本原因 {#root-cause}

- 一鍵包 `framepack_cu126_torch26` 內建 `torch 2.6.0+cu126`，編譯的架構只到 `sm_90`。
- RTX 50 系列（Blackwell）是 compute capability 12.0，也就是 `sm_120`。CUDA 12.8 才支援，PyTorch 2.7 起的 `cu128` 版本才有對應 kernel。
- [Issue #339](https://github.com/lllyasviel/FramePack/issues/339) 標題寫的「sm_90」是誤解；PyTorch 回報 `sm_120` 才是正確的。
- 不需要另外安裝 CUDA Toolkit：Windows 版 PyTorch wheel 已內含 CUDA runtime。driver 版本要求為 `cu128` 需 R570 以上，`cu130` 需 R580 以上。

## 版本選擇 {#version-matrix}

PyTorch、torchvision、triton-windows 與 SageAttention wheel 必須成對，以下組合皆已確認有 Python 3.10 Windows wheel：

| torch | torchvision | triton-windows | SageAttention wheel |
|-------|-------------|----------------|---------------------|
| 2.7.1 | 0.22.1 | `>=3.3,<3.4` | 2.2.0 post3 `cu128torch2.7.1` |
| 2.8.0 | 0.23.0 | `>=3.4,<3.5` | 2.2.0 post3 `cu128torch2.8.0` |
| 2.9.1 | 0.24.1 | `>=3.5,<3.6` | 2.2.0 post6 `cu128torch2.9.1` |
| **2.10.0** | **0.25.0** | `>=3.6,<3.7` | 2.2.0 post6 `cu128torch2.10.0andhigher` |

建議使用 **torch 2.10.0 + cu128**，原因如下：

- 2.10.0 是 triton-windows 相容表中最新的版本，也能使用 SageAttention post6。post6 修正了會造成黑畫面或雜訊輸出的越界問題。
- FramePack 用 `torchvision.io.write_video` 輸出 mp4。torchvision 自 0.22 起提示這個函式將被移除，但 0.25 實測仍可使用。升到更新版本前，要先確認這個函式還存在。
- torchvision 版本固定是 `0.(torch minor + 15)`，torchaudio 與 torch 同版號；三者要在同一個指令、同一個 index 一起安裝。

torch 2.10 cu128 支援的架構是 `sm_70` 到 `sm_120`，已不含 GTX 10 系列（Pascal）。若一鍵包之後要搬到更舊的顯卡，需要另外處理。

## 升級 PyTorch {#upgrade-pytorch}

先關閉 FramePack，再開 PowerShell 執行。所有 `pip` 都要透過一鍵包內建的 `python.exe` 執行；直接打 `pip` 或 `python` 可能會裝到系統上另一套 Python。

```powershell
$py = 'C:\framepack_cu126_torch26\system\python\python.exe'

# 備份目前套件清單，方便還原
& $py -m pip freeze > C:\framepack_cu126_torch26\system\pip-freeze-before.txt

& $py -m pip install --upgrade torch==2.10.0 torchvision==0.25.0 torchaudio==2.10.0 numpy==1.26.2 --index-url https://download.pytorch.org/whl/cu128 --extra-index-url https://pypi.org/simple
```

實測只會變動 torch、torchvision、torchaudio 與 sympy；`webui` 程式碼與 `hf_download` 模型都不受影響。torch wheel 約 2.9 GB。

不要照 issue 留言使用 `--force-reinstall`。它會連同所有相依套件重裝，把 NumPy 升到 2.x，導致一鍵包內以 NumPy 1.x 編譯的套件出錯，事後還得再降回 `numpy==1.26.2`。

安裝結束時看到下列訊息可以忽略，它們來自一鍵包附帶、FramePack 用不到的套件：

```text
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. ...
onnxruntime 1.17.0 requires flatbuffers, which is not installed.
```

## 加裝 SageAttention 加速 {#install-sageattention}

FramePack 偵測 attention 後端的順序是 SageAttention、flash-attn、xformers，最後才用 PyTorch SDPA。只做完上一節就能正常生成；SageAttention 是額外加速。flash-attn 沒有官方 Windows wheel，裝了 SageAttention 之後 xformers 也不會被用到，兩者都不必裝。

### 補上 Python include 與 libs {#python-include-libs}

SageAttention 依賴 triton，而 triton 執行時需要編譯小段 C 程式。一鍵包內的 Python 沒有 `include\Python.h` 與 `libs\python310.lib`，所以要從 triton-windows 的 release 下載補齊。這個 zip 的最上層就是 `include` 與 `libs`，可以直接解壓到 Python 目錄：

```powershell
$dir = 'C:\framepack_cu126_torch26\system\python'
Invoke-WebRequest https://github.com/woct0rdho/triton-windows/releases/download/v3.0.0-windows.post1/python_3.10.11_include_libs.zip -OutFile "$env:TEMP\python_3.10.11_include_libs.zip"
Expand-Archive "$env:TEMP\python_3.10.11_include_libs.zip" -DestinationPath $dir -Force
```

一鍵包的 Python 是 3.10.6；3.10.x 的 headers 與 import library 相容，所以 3.10.11 的版本可以直接使用。

### 安裝 triton-windows 與 SageAttention {#install-triton-sage}

triton-windows 的版本要對應 torch 2.10：

```powershell
& $py -m pip install --upgrade "triton-windows>=3.6,<3.7"
```

SageAttention 使用 woct0rdho 編譯的 Windows wheel，檔名中的 `cu128torch2.10.0andhigher` 必須與 torch 版本相符：

<code-block lang="powershell" ignore-vars="true"><![CDATA[
& $py -m pip install "https://github.com/woct0rdho/SageAttention/releases/download/v2.2.0-windows.post6/sageattention-2.2.0%2Bcu128torch2.10.0andhigher.post6-cp310-abi3-win_amd64.whl"
]]></code-block>

如果之前裝過其他版本的 triton，或升級後 triton 出現奇怪的編譯錯誤，先清除 JIT 快取：

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.triton\cache", "$env:TEMP\torchinductor_$env:USERNAME" -ErrorAction SilentlyContinue
```

## 驗證 {#verify}

先確認 PyTorch 已有 `sm_120` kernel：

```powershell
& $py -c "import torch; print(torch.__version__, torch.cuda.get_device_capability(), torch.cuda.get_arch_list())"
```

```text
2.10.0+cu128 (12, 0) ['sm_70', 'sm_75', 'sm_80', 'sm_86', 'sm_90', 'sm_100', 'sm_120']
```

再執行 `run.bat`，console 應出現：

```text
Sage Attn is installed!
Free VRAM 30.2646484375 GB
High-VRAM Mode: False
```

`High-VRAM Mode: False` 是正常的：FramePack 只有在可用 VRAM 超過 60 GB 時才會把模型全部常駐。文字編碼器約 14 GB、主模型約 24 GB，32 GB 放不下，所以會改用動態載入。介面上的「GPU Inference Preserved Memory」維持最小值 6 速度最快，遇到 OOM 再調高。

實測 1 秒影片、25 steps、開啟 TeaCache：

- 前 3 步因為暖機與 triton JIT 編譯較慢，之後約 1 it/s，25 步平均約 1.28 s/it。
- 一個 section（33 幀）約 31 秒，換算約 0.95 秒/幀；作者在 RTX 4090 開 TeaCache 的數據為 1.5 秒/幀。
- SageAttention 與 PyTorch SDPA 的輸出 cosine similarity 約 0.9993。官方 README 仍建議先在不開 SageAttention 的情況下確認結果，再比較畫質差異。

## 常見問題 {#faq}

| 症狀 | 原因與處理 |
|------|------------|
| `Torch not compiled with CUDA enabled`，或版本顯示 `+cpu` | 安裝時沒有指定 `--index-url`，從 PyPI 裝到 CPU 版；改用 cu128 index 重裝三個套件 |
| `Failed to initialize NumPy: _ARRAY_API not found` | NumPy 被升到 2.x；執行 `pip install numpy==1.26.2` |
| torchvision 是 CPU 版或版本對不上（例如 torch 2.7 搭 torchvision 0.17） | torchvision 必須是 `0.(minor+15)`，並與 torch 從同一個 index 一起安裝 |
| pip 顯示已安裝 sageattention，console 卻顯示 `Sage Attn is not installed!` | FramePack 用空的 `except` 吞掉 import 錯誤；執行 `& $py -c "from sageattention import sageattn"` 查看真正的原因，通常是缺 triton 或 wheel 版本不符 |
| triton 報 `Python.h` 找不到或缺 `python310.lib` | 回到上一節補 include 與 libs |
| 影片全黑或滿是雜訊 | 介面的 MP4 Compression 設為 16；SageAttention 使用 post6 以上版本 |
| `The video decoding and encoding capabilities of torchvision are deprecated` | 預期內的警告，仍可正常輸出；只是別在未確認的情況下把 torchvision 升過 0.25 |
| console 反覆出現 `_call_connection_lost` 與 `WinError 10022` | 與顯卡無關，是 Python 3.10 asyncio 的問題，見 [Gradio 在 Windows 反覆出現 WinError 10022 的原因與修正](gradio-asyncio-winerror-10022.md) |

升級完成後照常執行 `update.bat` 即可。它只會 `git pull` 更新 `webui`，不會動到 `system\python` 的套件；但 pull 失敗時會執行 `git reset --hard`，所以不要直接修改 `webui` 內被 Git 追蹤的檔案。

## 參考資料

- [FramePack 圖生影](FramePack-圖生影.md)
- [FramePack Issue #339：CUDA Error on RTX 5070 Ti (Blackwell)](https://github.com/lllyasviel/FramePack/issues/339)
- [FramePack Issue #267：no kernel image is available on 5070 Ti](https://github.com/lllyasviel/FramePack/issues/267)
- [FramePack Issue #151：速度過慢的排查方向](https://github.com/lllyasviel/FramePack/issues/151#issuecomment-2817054649)
- [triton-windows](https://github.com/woct0rdho/triton-windows)
- [SageAttention Windows wheels](https://github.com/woct0rdho/SageAttention/releases)
- [PyTorch Get Started](https://pytorch.org/get-started/locally/)
