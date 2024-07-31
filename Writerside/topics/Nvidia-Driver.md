# Nvidia-Driver

筆記下研究 Ubuntu 24.04 LTS 安裝 Nvidia Driver 的過程。

## 黑屏

目前測試裝新顯卡後，開機(登入)後會黑畫面

此時可以按 CTRL+ALT+F1 (我是把 F2, F3 都按一次才出來) 進入文字模式

透過以下指令安裝驅動，重開機後可以正常顯示圖形化介面。

## 安裝 Driver
```Bash
sudo apt update
sudo apt upgrade
sudo apt purge *nvidia*
sudo ubuntu-drivers autoinstall
sudo lshw -C display
nvidia-smi
```
![lshw.png](lshw.png)

## 參照
[Ubuntu LTS如何安裝Nvidia顯示卡驅動、CUDA、cuDNN、NVIDIA Container Toolkit套件](https://ivonblog.com/posts/ubuntu-install-nvidia-drivers/)