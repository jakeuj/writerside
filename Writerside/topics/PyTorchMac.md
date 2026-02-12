# PyTorch macOS 常見問題與解決方案

## 修正日期

2025-11-21

## 適用環境

- macOS (Apple Silicon / Intel)
- PyTorch / MONAI

---

## 問題: DataLoader worker 崩潰 (macOS multiprocessing 問題)

### 錯誤訊息

```
RuntimeError: DataLoader worker (pid 23120) exited unexpectedly with exit code 1.
Details are lost due to multiprocessing. Rerunning with num_workers=0 may give better error trace.
```

### 根本原因

macOS 使用 `fork` 機制進行 multiprocessing,在某些情況下會導致 PyTorch DataLoader 的 worker process 崩潰。這是 macOS 特有的問題,在 Linux/Windows 上較少發生。

### 解決方案

**方法 1: 設定 num_workers=0 (最穩定)**

```python
# 在主進程中載入資料,不使用額外的 worker processes
dl_train = torch.utils.data.DataLoader(ds_train, batch_size=batch_size, num_workers=0)
dl_val = torch.utils.data.DataLoader(ds_val, batch_size=batch_size, num_workers=0)
```

**方法 2: 使用較小的 num_workers (平衡效能與穩定性)**

```python
# 使用 2 個 workers,在效能和穩定性之間取得平衡
dl_train = torch.utils.data.DataLoader(ds_train, batch_size=batch_size, num_workers=2)
dl_val = torch.utils.data.DataLoader(ds_val, batch_size=batch_size, num_workers=2)
```

### 效能影響

| num_workers | 穩定性 | 載入速度 | 建議使用情境 |
|------------|--------|---------|-------------|
| 0 | ⭐⭐⭐⭐⭐ | ⭐⭐ | 小型資料集、除錯時 |
| 2 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 中型資料集、一般訓練 |
| 4-8 | ⭐⭐ | ⭐⭐⭐⭐⭐ | 大型資料集 (可能不穩定) |

---

## macOS 特定注意事項

### 1. Multiprocessing 問題

- **問題**: macOS 的 `fork` 機制與某些 Python 套件不相容
- **症狀**: DataLoader worker 崩潰、程序卡住、記憶體洩漏
- **解決**: 降低或停用 `num_workers`

### 2. Apple Silicon (M1/M2/M3/M4) GPU 支援

```python
# 檢查並使用 MPS (Metal Performance Shaders) 加速
if torch.backends.mps.is_available():
    device = torch.device("mps")
    print("使用 Apple Silicon GPU (MPS)")
else:
    device = torch.device("cpu")
```

**注意事項**:

- MPS 不支援所有 CUDA 操作
- 某些操作會自動 fallback 到 CPU
- 建議先在 CPU 上測試,確認程式正確後再切換到 MPS

### 3. Jupyter Notebook 路徑問題

```python
# ❌ 錯誤: 使用相對路徑,可能因 %cd 指令而混淆
project_dir = Path("segmentation")

# ✅ 正確: 使用絕對路徑
import os
workspace_dir = Path("/Users/username/Documents/Projects/ML")
os.chdir(workspace_dir)
project_dir = workspace_dir / "segmentation"
```

### 4. 檔案下載與解壓縮

```python
# 避免重複下載,節省時間
if not (project_dir / "images").exists():
    print("下載資料集...")
    gdown.download(url, output)
    !unzip -o temp.zip  # -o 自動覆蓋,不詢問
    !rm temp.zip
else:
    print("資料集已存在,跳過下載")
```

---

## 實際修改範例 (pytorch實作2_影像分割.ipynb)

### 修改位置 1: DataLoader (第 208-211 行)

```python
ds_train = monai.data.Dataset(data_train, transform=trans)
# macOS 修正: 降低 num_workers 避免 multiprocessing 問題
dl_train = torch.utils.data.DataLoader(ds_train, batch_size=batch_size, num_workers=0)
ds_val = monai.data.Dataset(data_val, transform=val_trans)
dl_val = torch.utils.data.DataLoader(ds_val, batch_size=batch_size, num_workers=0)
```

### 修改位置 2: DataLoader (第 348-354 行)

```python
ds_train = monai.data.CacheDataset(data_train, transform=trans)
# macOS 修正: 降低 num_workers 避免 multiprocessing 問題
dl_train = monai.data.DataLoader(ds_train, batch_size=batch_size, num_workers=0)

ds_val = monai.data.CacheDataset(data_val, transform=val_trans)
dl_val = monai.data.DataLoader(ds_val, batch_size=batch_size, num_workers=0)
```

---

## 除錯技巧

### 1. 確認錯誤來源

```python
# 設定 num_workers=0 獲得完整錯誤訊息
dl_train = DataLoader(dataset, batch_size=16, num_workers=0)
```

### 2. 測試不同的 num_workers 值

```python
for num_workers in [0, 1, 2, 4]:
    print(f"測試 num_workers={num_workers}")
    try:
        dl = DataLoader(dataset, batch_size=16, num_workers=num_workers)
        for batch in dl:
            break  # 只測試第一個 batch
        print(f"  ✅ 成功")
    except Exception as e:
        print(f"  ❌ 失敗: {e}")
```

### 3. 檢查 MPS 可用性

```python
print(f"MPS 可用: {torch.backends.mps.is_available()}")
print(f"MPS 已建置: {torch.backends.mps.is_built()}")
```

---

## 參考資源

- [PyTorch MPS Backend](https://pytorch.org/docs/stable/notes/mps.html)
- [DataLoader multiprocessing](https://pytorch.org/docs/stable/data.html#multi-process-data-loading)
- [macOS fork() issues](https://bugs.python.org/issue33725)
