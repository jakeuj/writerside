# SSH

筆記一下自動啟動 SSH 服務的方法。

## 安裝 SSH 服務

```bash
sudo apt-get install openssh-server
sudo systemctl enable ssh
sudo ufw allow ssh
sudo systemctl start ssh
```

## 新增使用者

在 Ubuntu 中新增使用者並將其加入 sudo 群組的步驟如下:

1. 以 root 身份或使用 `sudo` 命令打開終端機。

2. 使用 `adduser` 命令新增新的使用者帳戶,系統會詢問新使用者的相關資訊(全名、用戶名、密碼等)。

```bash
sudo adduser 新使用者名稱
```

1. 將新使用者加入 sudo 群組,以賦予其 root 權限。

```bash
sudo usermod -aG sudo 新使用者名稱
```

1. 檢查新使用者是否已成功加入 sudo 群組。

```bash
groups 新使用者名稱
```

輸出結果應該會包含 `sudo` 這個群組。

1. 現在,新使用者可以使用 `sudo` 命令來執行需要 root 權限的任務了。

例如,如果新增了一個名為 `newuser` 的使用者,步驟如下:

```bash
sudo adduser newuser
sudo usermod -aG sudo newuser
groups newuser
```

注意,將一個使用者加入 sudo 群組意味著賦予該使用者執行管理任務的權限,因此請謹慎操作。如果只需要賦予新用戶有限的 root 權限,可以考慮使用 `sudo visudo` 命令來編輯 /etc/sudoers 文件,為該用戶分配特定的權限。

## 切換使用者

要切換到新建立的使用者帳號,您可以使用以下命令:

```bash
su - 新使用者名稱
```

例如,如果新使用者名稱為 `newuser`，您可以執行:

```bash
su - newuser
```

然後系統會要求您輸入該用戶的密碼。輸入正確的密碼後,您就能切換到該用戶的shell環境。

注意 `su` 命令後面的 `-` 參數,它會將您的工作環境完全切換到新用戶,包括載入該用戶的環境變數設定等。如果沒有 `-` 參數,它只會變更您目前的使用者ID。

另一種切換方式是使用 `sudo` 命令搭配 `-i` 選項,它會啟動一個模擬 root 用戶的交互式 shell:

```bash
sudo -i -u 新使用者名稱
```

例如:

```bash
sudo -i -u newuser
```

這種方式下,您的工作環境將保持原狀,只是獲得了該用戶的權限和環境變數。

切換回您原本的用戶帳號,只需在新用戶的 shell 視窗中輸入 `exit` 或按下 `Ctrl+D` 組合鍵即可。

這些命令允許您臨時切換到其他用戶身份,對於檢查新用戶權限或模擬其工作環境非常有用。

## REF

[How to Enable SSH Server on Ubuntu](https://www.cyberciti.biz/faq/how-to-install-ssh-on-ubuntu-linux-using-apt-get/)
