# Nvidia-Driver

筆記下研究 Ubuntu 24.04 LTS 安裝 Nvidia Driver 的過程。

## 黑屏

目前測試裝新顯卡後，開機(登入)後會黑畫面

此時可以按 CTRL+ALT+F1 (我是把 F2, F3 都按一次才出來) 進入文字模式

透過以下指令安裝驅動，重開機後可以正常顯示圖形化介面。

## 確認顯卡最新驅動版本

[官網](https://www.nvidia.com/download/index.aspx) 搜尋最新驅動版本號。

![search-driver.png](search-driver.png)

以 3090 Ti 為例，最新版本為 555

![lastest-driver.png](lastest-driver.png)

最後可以看到 555 版本支援 20, 30, 40 系列顯卡

所以舊版顯卡可能不支援新版驅動，需要自行到官網搜尋可用的最新驅動版本號。

同時也決定了 20 以下顯卡無法支援 CUDA 12.5 以上版本，因為 CUDA 12.5 要求驅動版本 555 以上。

詳細驅動對應 CUDA 版本可以參照官方文件

[CUDA Application Compatibility Support Matrix](https://docs.nvidia.com/deploy/cuda-compatibility/#id3)

找到自己顯卡的最新驅動版本可以對應到的最高 CUDA 版本

進而瞭解可以支援的 Container 的 CUDA 最高版本

換句話說 **Container 的 CUDA 版本要小於等於 Host 顯示卡所支援的驅動版本對應的 CUDA 版本**

## 安裝 Driver

1. 更新系統，移除舊版驅動
```Bash
sudo apt update
sudo apt upgrade
sudo apt purge *nvidia*
```

2. 將最新驅動版本號帶入以下指令，這裡以 555 為例

```Bash
# 手動指定最新 Nvidia 驅動版本號
sudo ubuntu-drivers install nvidia:555
```

否則自動安裝會裝到舊版驅動，導致不支援新版 CUDA。

3. 驗證安裝結果

```Bash
sudo lshw -C display
nvidia-smi
```

![lshw.png](lshw.png)

![nvidia-555.png](nvidia-555.png)

## 更新到最新版本驅動
目前心得是

- 一般使用，不需要特別更新驅動版本，直接用自動安裝即可。 `sudo ubuntu-drivers autoinstall`
- 需要 CUDA，則需要更新到驅動最新版本，但 Ubuntu 自帶 repo 不包含最新驅動，所以要下載並安裝 NVIDIA CUDA 軟體的密鑰包，然後更新軟體包清單。
  1. 先到 [CUDA 官網](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=24.04&target_type=deb_network)
  2. 選擇自己的系統版本
  3. 安裝方式選 deb (network)
  4. 執行前三行指令來更新 Ubuntu Repository
    ```Bash
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb
    sudo dpkg -i cuda-keyring_1.1-1_all.deb
    sudo apt-get update 
    ```
  5. 如果不是使用內含 cuda-toolkit 的 container (例如: NIM)，則需要把上一步驟的第四行也一併執行，來安裝 cuda-toolkit
    ```Bash
    sudo apt-get -y install cuda-toolkit-12-6
    ```
  6. 最後就可以更新到最新版本的 NVIDIA Driver (目前可以安裝到 560 版)
    ```Bash
    sudo apt-get install -y nvidia-open
    ```

## 參照
[Ubuntu LTS如何安裝Nvidia顯示卡驅動、CUDA、cuDNN、NVIDIA Container Toolkit套件](https://ivonblog.com/posts/ubuntu-install-nvidia-drivers/)

[CUDA Toolkit Driver Installer](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=24.04&target_type=deb_network)

![cuda-driver.png](cuda-driver.png)