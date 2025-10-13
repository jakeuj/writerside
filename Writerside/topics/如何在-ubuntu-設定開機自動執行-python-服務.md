# 如何在 ubuntu 設定開機自動執行 python 服務

> **原文發布日期:** 2023-10-04
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/10/04/ubuntu-systemctl-python
> **標籤:** 無

---

筆記下 python 虛擬環境與環境變數

## 前置作業

1. 環境設定
   [设置 Python 开发环境  |  Google Cloud](https://cloud.google.com/python/docs/setup?hl=zh-cn#linux)
2. 取得專案程式碼
   [如何在 linux 從 github clone repo | 御用小本本 - 點部落 (dotblogs.com.tw)](https://www.dotblogs.com.tw/jakeuj/2023/10/04/ssh-git-clone)

## 新增服務

### 新增服務設定檔

sudo nano /etc/systemd/system/my\_python\_script.service

```
[Unit]
Description=MyProject Service
After=multi-user.target

[Service]
Type=idle

# 執行時的工作目錄
WorkingDirectory=/home/jake/MyProject/src

ExecStart=python /home/jake/MyProject/src/main.py --serve-in-foreground

# 執行服務的使用者（名稱或 ID 皆可）
User=jake

[Install]
WantedBy=multi-user.target
```

### 啟用服務

```
# 修改權限讓此檔可以執行
sudo chmod 644 /etc/systemd/system/my_python_script.service
# 啟用服務 (開機自動執行)
sudo systemctl enable my_python_script.service
# 執行服務 (現在立刻執行一次)
sudo systemctl start my_python_script.service
# 查看服務狀態 (看服務輸出 LOG)
sudo systemctl status my_python_script.service
```

完成上述步驟後，每次Ubuntu開機時，您的Python腳本都會被自動執行。

確保您的Python腳本在被執行時不需要任何用戶互動，以免開機時出現問題。

### 其他服務設定

```
[Unit]
Description=MyProject Service
After=multi-user.target

[Service]
Type=idle
ExecStart=/home/jake/MyProject/env/bin/python /home/jake/MyProject/src/main.py --serve-in-foreground

# 執行時的工作目錄
WorkingDirectory=/home/jake/MyProject

# 執行服務的使用者（名稱或 ID 皆可）
User=jake

# 執行服務的群組（名稱或 ID 皆可）
Group=jake

# 環境變數設定
Environment="PYTHON_ENVIRONMENT=development"

[Install]
WantedBy=multi-user.target
```

### 參照

[Linux 建立自訂 Systemd 服務教學與範例 - G. T. Wang (gtwang.org)](https://blog.gtwang.org/linux/linux-create-systemd-service-unit-for-python-echo-server-tutorial-examples/)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Python

* 回首頁

---

*本文章從點部落遷移至 Writerside*
