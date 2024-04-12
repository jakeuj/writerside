# AMD-GPU-Driver-Install

筆記下研究 Ubuntu 22.04.6 LTS 安裝 AMD GPU 的過程。

## 下載

[amdgpu-install_6.0.60003-1_all.deb](https://www.amd.com/en/support/professional-graphics/amd-radeon-pro/amd-radeon-pro-w7000-series/amd-radeon-pro-w7900)

## 安裝 Cli
[Installing the Installer Package](https://amdgpu-install.readthedocs.io/en/latest/install-prereq.html#installing-the-installer-package)

## 安裝 Driver
[Installing the Workstation Use Case](https://amdgpu-install.readthedocs.io/en/latest/install-installing.html#installing-the-workstation-use-case)

## Install

- install.sh
```Shell
# For Ubuntu:
$ sudo apt-get update
$ sudo apt-get dist-upgrade

# For Ubuntu:
$ sudo apt-get install ./amdgpu-install_6.0.60003-1_all.deb
$ sudo apt-get update

amdgpu-install -y --accept-eula --usecase=workstation
export PATH=/opt/amdgpu-pro/bin:/opt/amdgpu/bin:$PATH
```

- Execute
```Shell
sudo chmod +x install.sh

sudo sh ./install.sh
```

## Nvidia
[ubuntu-install-nvidia-drivers](https://ivonblog.com/posts/ubuntu-install-nvidia-drivers/)