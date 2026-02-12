# Nvidia-Driver

筆記下研究 Ubuntu 24.04 LTS 安裝 Nvidia Driver 的過程。

## 更新到最新版本驅動

目前心得是一般使用，不需要特別更新驅動版本，直接從 Ubuntu Desktop 自帶的 `額外驅動程式` 裡面安裝即可。

再來是需要 CUDA，則需要更新到驅動最新版本，則需要從官方 CUDA Toolkit 下載並安裝密鑰包，更新 Ubuntu 軟體包清單以取得最新版本驅動程式。

1. 先到 [CUDA 官網](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=24.04&target_type=deb_network)
2. 選擇自己的系統版本 (我這邊是 Ubuntu 24.04)
3. 安裝方式選 deb (network)
4. 執行前三行指令來更新 Ubuntu Repository

  ```Bash
  wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb
  sudo dpkg -i cuda-keyring_1.1-1_all.deb
  sudo apt-get update
  ```

1. 如果是內含 cuda-toolkit 的 container 則建議略過 (例如: NIM 容器內會自帶)，反之執行第四行來安裝 cuda-toolkit 到本機

  ```Bash
  sudo apt-get -y install cuda-toolkit-12-6
  ```

1. 如果是 WSL 則必須略過，反之執行以下語法更新到最新版本的 NVIDIA Driver (目前版本 560) 以支援最新 CUDA 版本

  ```Bash
  sudo apt-get install -y nvidia-open
  ```

## 黑屏

目前測試裝新顯卡後，開機(登入)後會黑畫面

此時可以按 CTRL+ALT+F1 (我是把 F2, F3 都按一次才出來) 進入文字模式

透過以下指令安裝驅動，重開機後可以正常顯示圖形化介面。

```Bash
sudo apt update
sudo apt upgrade
sudo apt purge *nvidia*
sudo ubuntu-drivers autoinstall
```

## 確認顯卡最新驅動版本

[官網](https://www.nvidia.com/download/index.aspx) 搜尋最新驅動版本號。

![search-driver.png](search-driver.png){style="block"}

以 3090 Ti 為例，最新版本為 555

![lastest-driver.png](lastest-driver.png){style="block"}

最後可以看到 555 版本支援 20, 30, 40 系列顯卡

所以舊版顯卡可能不支援新版驅動，需要自行到官網搜尋可用的最新驅動版本號。

同時也決定了 20 以下顯卡無法支援 CUDA 12.5 以上版本，因為 CUDA 12.5 要求驅動版本 555 以上。

由此可知 CUDA 版本越低，可以支援的顯卡越多。

詳細驅動對應 CUDA 版本可以參照官方文件

[CUDA Application Compatibility Support Matrix](https://docs.nvidia.com/deploy/cuda-compatibility/#id3)

找到自己顯卡的最新驅動版本可以對應到的最高 CUDA 版本

進而瞭解可以支援的 Container 的 CUDA 最高版本

換句話說 **Container 的 CUDA 版本要小於等於 Host 顯示卡所支援的驅動版本對應的 CUDA 版本**

## 參照

[Ubuntu LTS如何安裝Nvidia顯示卡驅動、CUDA、cuDNN、NVIDIA Container Toolkit套件](https://ivonblog.com/posts/ubuntu-install-nvidia-drivers/)

[CUDA Toolkit Driver Installer](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=24.04&target_type=deb_network)

![cuda-driver.png](cuda-driver.png){style="block"}
