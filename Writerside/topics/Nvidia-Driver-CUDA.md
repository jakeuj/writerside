# Nvidia Driver CUDA
更新一下跑模型的驅動安裝心得，主要是針對 Nvidia Driver 和 CUDA 的安裝步驟，特別是針對 Ubuntu 系統。

## 驅動程式種類
Nvidia 驅動程式有兩種：
1. **open kernel**：開源驅動程式，適合大多數使用者。
   - 例如：`nvidia-open-kernel-535`。
   - 安裝後會在 `/usr/lib/nvidia-open` 目錄下。
   - 這個驅動程式通常已經包含在 Ubuntu 的官方軟體庫中，可以通過 `apt` 直接安裝。
   - 安裝指令：
     ```bash
     sudo apt install nvidia-open-kernel-535
     ```
2. **proprietary kernel**：專有驅動程式，提供更好的性能和功能，但需要手動安裝。
   - 例如：`nvidia-kernel-535`。
   - 安裝後會在 `/usr/lib/nvidia` 目錄下。
   - 需要從 Nvidia 官方網站下載並安裝。
   - 安裝指令：
     ```bash
     sudo apt install nvidia-kernel-535
     ```
     
## 切換驅動程式
Ubuntu 20.04/22.04/24.04 如果需要切換到專有驅動程式，可以使用以下指令：
- 切換到開源驅動程式：
```bash
apt install --autoremove --purge nvidia-open-575 nvidia-driver-575-open
```
- 切換到專有驅動程式：
```bash
apt install --autoremove --purge cuda-drivers-575 nvidia-driver-575
```
### 參照
[witching-between-driver-module-flavors](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/#switching-between-driver-module-flavors)

## 全新安裝
擇一安裝，一般使用可以用開源，要跑 CUDA 的話，建議使用專有驅動程式。
- open kernel
```Bash
sudo apt-get install -y nvidia-open
```
- proprietary kernel
```Bash
sudo apt-get install -y cuda-drivers
```
- 參照：[Driver Installer](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=24.04&target_type=deb_network#:~:text=detailed%20here.-,Driver%20Installer,-NVIDIA%20Driver%20Instructions)
{ignore-vars="true"}

## PyTorch CUDA 驅動程式
![PyTorch.png](PyTorch.png)
- 使用 PyTorch 2.7.1 對應的 CUDA 12.8 wheel。
- **不用額外安裝 CUDA Toolkit**，安裝 PyTorch 時它會 **帶自己的 CUDA runtime**（如果你用 pip install torch 裝的是 CUDA 版本）。
- 安裝指令：
```bash
pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128
```
### 參照
[pytorch](https://pytorch.org/get-started/locally/)

## CUDA Toolkit 安裝
![Cuda-Toolkit.png](Cuda-Toolkit.png){style="auto"}
如果你不是用 PyTorch 需要安裝 CUDA Toolkit，可以到官網選擇找你要的版本與作業系統

以 Ubuntu 24.04 安裝 CUDA Toolkit 12.9 為例，可以使用以下指令安裝：
```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-9
```

### CUDA Toolkit Installer Type
安裝方式有分為以下三種：
- **Network Installer**：透過網路下載安裝，適合網路連線穩定的情況。
  - 例如：開發環境需要快速安裝，且網路連線良好，安裝完成後不留檔案，不佔空間。
- **Local Installer**：下載完整的安裝包，適合網路不穩定或需要離線安裝的情況。
  - 例如：開發環境需要重複安裝在不同機器，又不想每次重新下載，可以將安裝檔保留在 USB 之類的省去下載時間。
- **Runfile Installer**：使用 `.run` 檔案安裝，適合需要自訂安裝選項的情況。
    - 例如：需要自訂安裝路徑或選擇安裝的組件，可以使用這種方式。
    - 安裝指令：
        ```bash
        sudo sh cuda_<version>_linux.run
        ```
      
### NVCC 編譯器
`NVCC` 是 CUDA 的編譯器，但安裝 CUDA Toolkit 後，並不會自動將路徑加到環境變數，導致 nvcc 指令無法直接使用。
解法步驟如下：

1. 確認 nvcc 是否有被安裝（通常會在這）
    ```bash
    sudo find / -name nvcc 2>/dev/null
    ```
   你應該會看到類似這樣的輸出：
    ```bash
    /usr/local/cuda-12.9/bin/nvcc
    /usr/local/cuda-12.6/bin/nvcc
    ```
2. 永久加入 PATH
    ```bash
    echo 'export PATH=/usr/local/cuda-12.9/bin:$PATH' >> ~/.bashrc
    echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.9/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
    source ~/.bashrc
    ```
3. 確認 nvcc 是否可以使用
    ```bash
    nvcc --version
    ```
   會顯示像：
    ```bash
    nvcc: NVIDIA (R) Cuda compiler driver
    Copyright (c) 2005-2025 NVIDIA Corporation
    Built on Tue_May_27_02:21:03_PDT_2025
    Cuda compilation tools, release 12.9, V12.9.86
    Build cuda_12.9.r12.9/compiler.36037853_0
   ```

✅ 什麼時候一定要加？
- 自己手動安裝 CUDA 且沒使用 runfile installer 建立 symlink
- 使用多版本 CUDA 切換時（例如有 /usr/local/cuda-11.8、cuda-12.9 等）
- 在編譯 CUDA 應用程式或使用某些需要 LD_LIBRARY_PATH 的應用時

#### 參照
[CUDA Toolkit](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=24.04&target_type=deb_network)

## 顯示卡相容性
Nvidia 驅動程式和 CUDA 的相容性取決於你的顯示卡型號。
- [全本版CUDA Toolkit 列表](https://developer.nvidia.com/cuda-toolkit-archive)
### 參照
[上一篇關於 Nvidia Driver 的文章](Nvidia-Driver.md)