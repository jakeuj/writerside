# AMD-GPU-Driver-Install

筆記下研究 Ubuntu 22.04.6 LTS 安裝 AMD GPU 的過程。

## 搜尋 AMD 顯卡型號

[Drivers and Support for Processors and Graphics](https://www.amd.com/en/support/professional-graphics/amd-radeon-pro/amd-radeon-pro-w7000-series/amd-radeon-pro-w7900)

![7900XT.png](7900XT.png){style="block"}

## 安裝 Driver

```Shell
sudo apt update
wget https://repo.radeon.com/amdgpu-install/23.40.2/ubuntu/jammy/amdgpu-install_6.0.60002-1_all.deb
sudo apt install ./amdgpu-install_6.0.60002-1_all.deb
sudo amdgpu-install -y --usecase=graphics,rocm --accept-eula
sudo usermod -a -G render,video $LOGNAME
```

![7900Driver.png](7900Driver.png){style="block"}

### Use Case
[Installing the Workstation Use Case](https://amdgpu-install.readthedocs.io/en/latest/install-installing.html#installing-the-workstation-use-case)

### ROCm

- ROCm: ROCm 之於 AMD GPU，基本上相當於 CUDA 之於 NVIDIA GPU
- ROCr: ROC Runtime

## REF

[Installing the Installer Package](https://amdgpu-install.readthedocs.io/en/latest/install-prereq.html#installing-the-installer-package)

[ubuntu-install-nvidia-drivers](https://ivonblog.com/posts/ubuntu-install-nvidia-drivers/)