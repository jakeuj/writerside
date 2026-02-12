# 在 Windows PowerShell 中建立 SSH 金鑰並使用 SCP 傳輸到伺服器

以下是在 Windows PowerShell 中生成 SSH 金鑰並將其傳輸到 `jake@1.2.3.4`（Ubuntu 伺服器）的詳細步驟：

![ps-ssh.png](ps-ssh.png){style="block"}

## 1. 生成 SSH 金鑰對

在 PowerShell 中執行以下命令生成 SSH 金鑰對：

```Shell
ssh-keygen -t ed25519 -f $env:USERPROFILE\.ssh\id_ed25519
```

- 這將生成名為 `id_ed25519` 的金鑰檔案，存放於 `C:\Users\YourUsername\.ssh` 資料夾中。
- 按 Enter 來接受預設路徑，並選擇是否設置密碼短語。

## 2. 使用 SCP 傳輸公鑰到遠端伺服器

接著，將公鑰傳輸到 `jake@1.2.3.4` 的主目錄：

```Shell
scp $env:USERPROFILE\.ssh\id_ed25519.pub jake@1.2.3.4:~/
```

## 3. 登入 Ubuntu 伺服器並設定公鑰

使用密碼登入伺服器，並配置公鑰：

```Shell
ssh jake@1.2.3.4
```

登入後，執行以下命令將公鑰內容添加到 `authorized_keys` 檔案中：

```bash
mkdir -p ~/.ssh
cat ~/id_ed25519.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
rm ~/id_ed25519.pub  # 刪除傳輸過來的公鑰檔案
```

## 4. 測試 SSH 連線

回到 PowerShell，測試 SSH 無密碼連線：

```Shell
ssh jake@1.2.3.4
```

完成以上步驟後，應可無需密碼，直接從 Windows 透過 SSH 連線至 Ubuntu 伺服器 `1.2.3.4`。

---

# 在 Windows Terminal 中建立自動 SSH 連線設定檔

要在 Windows Terminal 中建立設定檔，讓其啟動時自動透過 PowerShell SSH 連線至 `jake@1.2.3.4`，請依照以下步驟：

## 1. 開啟 Windows Terminal 的設定檔

在 Windows Terminal 中，點擊右上角的下拉箭頭，選擇「設定」。

## 2. 新增自訂設定檔

在設定介面中，點擊左側的「新增設定檔」。

## 3. 設定新設定檔的詳細資訊

在右側的設定區域，填寫以下資訊：

- **名稱：** 輸入「SSH to jake@1.2.3.4」或其他您喜歡的名稱。
- **命令列：** 輸入以下指令，讓 PowerShell 啟動時自動執行 SSH 連線：

  ```Shell
  powershell.exe -NoExit -Command "ssh jake@1.2.3.4"
  ```

  此指令會啟動 PowerShell，並執行 `ssh jake@1.2.3.4`，同時保持終端機開啟狀態。

- **起始目錄：** 可以設為預設值，或指定其他目錄。
- **圖示：** 可以選擇一個圖示，方便在下拉選單中辨識。

## 4. 儲存設定

完成上述設定後，點擊「儲存」按鈕。

## 5. 使用新設定檔

在 Windows Terminal 的下拉選單中，您將看到剛新增的設定檔「SSH to jake@1.2.3.4」。選擇它，終端機將自動啟動 PowerShell 並連線至 `jake@1.2.3.4`。

透過上述步驟，您可以在 Windows Terminal 中建立一個自動 SSH 連線的設定檔，提升操作效率。
