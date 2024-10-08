# VM GPU Driver

紀錄一下在 VM 安裝 GPU Driver 的過程

## 結論
將 VM 的 secure boot/TPM 先關閉，再安裝驅動，否則會因為開機需要輸入自定義臨時安全性密碼，導致無法開機，最終於法正常安裝驅動。

## VM
建立 GPU VM 有兩種方式

1. 選擇 Nvidia 官方映像，內置 GPU Driver，但 Driver 版本比較舊，可能需要自己再更新一下
2. 選擇 Ubuntu 官方映像，自己安裝 Nvidia Driver，建立時將開機選項選擇標準，禁用 secure boot/TPM (或建立後去組態裡關閉)

## 安裝驅動
- [Nvidia Driver](Nvidia-Driver.md)

## 安裝 CUDA
- [Nvidia CUDA](CUDA.md)

## 注意
- [ ] 安裝完驅動記得重開機 > sudo init 6
- [ ] 完成後記得編輯 ~/.bashrc 加入 nvcc 路徑

```bash
nano ~/.bashrc
```
添加以下內容:

```
# nvcc
export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```

## 驗證安裝:

```bash
source ~/.bashrc
nvidia-smi
nvcc --version
```

## 安全開機
Ubuntu 軟體包 NVIDIA 專有驅動程式。這些驅動程式直接來自 NVIDIA，由 Ubuntu 簡單地打包，以便它們可以由系統自動管理。
從其他來源下載和安裝驅動程式可能會導致系統損壞。此外，在啟用了 TrustedLaunch 和安全啟動的 VM 上安裝第三方驅動程式需要執行額外的步驟。
它們要求使用者添加新的 Machine Owner Key （電腦擁有者金鑰） 以便系統引導。Ubuntu 中的驅動程式由 Canonical 簽名，可與安全啟動配合使用。

1. 安裝實用程式：ubuntu-drivers

    ```bash
    sudo apt update && sudo apt install -y ubuntu-drivers-common
    ```
2. 安裝最新的 NVIDIA 驅動程式：

    ```bash
    sudo ubuntu-drivers install
    ```
3. 重啟系統：

    ```bash
    sudo reboot
    ```
   
4. 驗證驅動程式是否正確安裝：

    ```bash
    nvidia-smi
    ```
   
5. 安裝 CUDA

    ```bash
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb
    sudo apt install -y ./cuda-keyring_1.1-1_all.deb
    sudo apt update
    sudo apt -y install cuda-toolkit-12-4
    ```
   安裝可能需要幾分鐘時間。
6. 安裝完成後重新啟動 VM：

    ```bash
    sudo reboot
    ```
   
7. 驗證 CUDA 是否正確安裝：

    ```bash
    nvcc --version
    ```
   
8. NVIDIA 驅動程式更新

   建議您在部署后定期更新 NVIDIA 驅動程式。
    ```bash
    sudo apt update
    sudo apt full-upgrade
    ```

- 注意

    該示例顯示了Ubuntu 24.04 LTS的 CUDA 包路徑。

    替換特定於您計劃使用的版本的路徑。

    請訪問 [NVIDIA 下載中心](https://developer.download.nvidia.com/compute/cuda/repos/) 或 [NVIDIA CUDA 資源頁面](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=24.04&target_type=deb_network)，瞭解特定於每個版本的完整路徑。

## 參照
- [n-series-driver-setup#ubuntu](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/n-series-driver-setup#ubuntu)