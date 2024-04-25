# CUDA

主要是說 CUDA 應用程式可以直接在 WSL 上跑
然後 唯一需要安裝驅動的只有 Windows (NVIDIA GeForce Game Ready Driver)
重點是 WSL 裡面絕對不要再安裝 Driver
大概是說 WSL 裡面就已經會使用 Winidows 的 Driver 了
如果再從裡面安裝會覆蓋掉 balabalabala...
所以裡頭只要安裝 CUDA Toolkit 就好了

## WSL 2
這邊不贅述

## 安裝 CUDA Toolkit
[WSL-Ubuntu](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_local)

![CudaToolKitWsl2.png](CudaToolKitWsl2.png)

```bash
wget https://developer.download.nvidia.com/compute/cuda/12.4.1/local_installers/cuda_12.4.1_550.54.15_linux.run
sudo sh cuda_12.4.1_550.54.15_linux.run
```

## REF
[wsl-user-guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html)