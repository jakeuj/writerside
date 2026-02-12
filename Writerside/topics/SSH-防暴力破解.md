# Fail2Ban SSH 防暴力破解設定指南

## 📦 安裝 Fail2Ban

```bash
sudo apt update
sudo apt install fail2ban -y
```

## ⚙️ 建立與編輯設定檔

```bash
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local
```

## ✏️ 編輯 `[sshd]` 區段設定

在 `jail.local` 中加入或修改：

```ini
[sshd]
port    = ssh
logpath = %(sshd_log)s
backend = %(sshd_backend)s
# 上面是預設值，以下是需加上的設定
enabled = true
# 封鎖時間 (秒)
bantime = 3600
# 分析時間區間 (秒)
findtime = 600
# 幾次失敗就封鎖
maxretry = 5
```

## ▶️ 啟動

```bash
sudo systemctl restart fail2ban
sudo systemctl enable fail2ban
```

## 🔍 檢查狀態

```bash
sudo fail2ban-client status
sudo fail2ban-client status sshd
```

## 🧪 測試封鎖（從外網）

```bash
ssh -p 10422 fakeuser@your-public-ip
```

或強制密碼登入：

```bash
ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no -p 10422 youruser@your-public-ip
```

## 📜 檢查登入記錄

```bash
grep 'Failed' /var/log/auth.log
grep 'Ban' /var/log/fail2ban.log
```

## 🧹 強制解除封鎖

```bash
sudo fail2ban-client set sshd unbanip 1.2.3.4
```

## 🕵️ 檢查當前設定

```bash
sudo fail2ban-client -d
```

---

🔒 建議搭配變更 SSH port、停用密碼登入、設定 UFW 防火牆等方式強化伺服器安全。
