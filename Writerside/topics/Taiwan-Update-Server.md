# Taiwan Update Server

將 WSL 中的 Ubuntu 的 APT 更新伺服器改為台灣的伺服器。

## 編輯

```bash
sudo sed -i 's|http://archive.ubuntu.com/ubuntu/|http://tw.archive.ubuntu.com/ubuntu/|g' /etc/apt/sources.list
```

## 更新

```bash
sudo apt update
```

這樣你就將 WSL 的 Ubuntu APT 更新伺服器改為台灣的伺服器了。
