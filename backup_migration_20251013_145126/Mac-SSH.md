# Mac SSH

在 macOS 產生 SSH 金鑰並設定到 Linux 主機登入

## 1. 在 macOS 產生 SSH 金鑰

打開 Terminal，執行以下指令：

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

若你偏好使用 RSA 金鑰，則使用：

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

出現提示時可直接按 Enter 使用預設儲存路徑：

```
Enter file in which to save the key (/Users/yourname/.ssh/id_ed25519):
```

---

## 2. 查看並複製公鑰內容

```bash
cat ~/.ssh/id_ed25519.pub
```

複製整段開頭為 `ssh-ed25519`（或 `ssh-rsa`）的內容。

---

## 3. 登入 Linux 並新增公鑰

```bash
ssh username@linux_ip
```

登入後執行：

```bash
mkdir -p ~/.ssh
nano ~/.ssh/authorized_keys
```

貼上剛剛複製的公鑰，儲存並離開（Ctrl + X → Y → Enter）。

接著設定權限：

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

---

## 4. 回到 mac 測試 SSH 無密碼登入

```bash
ssh username@linux_ip
```

如果成功就可以無密碼登入。

---

## 備註