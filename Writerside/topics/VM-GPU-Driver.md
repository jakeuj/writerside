# VM GPU Driver

紀錄一下在 VM 安裝 GPU Driver 的過程

## 結論
將 VM 的安全開機/TPM 先關閉，再安裝驅動，否則會因為開機需要輸入自定義臨時安全性密碼，導致無法開機，最終於法正常安裝驅動。

## VM
建立 GPU VM 有兩種方式

1. 選擇 Nvidia 官方映像，內置 GPU Driver，但 Driver 版本比較舊，可能需要自己再更新一下
2. 選擇 Ubuntu 官方映像，自己安裝 Nvidia Driver，建立時將開機選項選擇標準，禁用安全開機 (或建立後去組態裡關閉)

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
