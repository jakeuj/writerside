# CUDA

主要是說 CUDA 應用程式可以直接在 WSL 上跑
然後 唯一需要安裝驅動的只有 Windows (NVIDIA GeForce Game Ready Driver)
重點是 WSL 裡面絕對不要再安裝 Driver
大概是說 WSL 裡面就已經會使用 Winidows 的 Driver 了
如果再從裡面安裝會覆蓋掉
所以裡頭只要安裝 CUDA Toolkit 就好了

![image_8.png](image_8.png)

## WSL 2
用 WSL 安裝 Ubuntu, 這邊不贅述

[Ubuntu](https://www.microsoft.com/store/productId/9NZ3KLHXDJP5?ocid=pdpshare)

## CUDA

### 首先刪除舊的 GPG key:
```bash
sudo apt-key del 7FA2AF80
```

### 然後下載 CUDA Toolkit

[WSL-Ubuntu](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_local)

![CudaToolKitWsl2.png](CudaToolKitWsl2.png)

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-5
```

## nvidia-smi

編輯 `~/.bashrc`:

```bash
nano ~/.bashrc
```
添加以下內容:

```
export PATH=$PATH:/usr/lib/wsl/lib/
export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```

驗證安裝:

```bash
source ~/.bashrc
nvidia-smi
nvcc --version
```

![image_9.png](image_9.png)

## REF
[wsl-user-guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html)