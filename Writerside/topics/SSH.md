# SSH

筆記一下自動啟動 SSH 服務的方法。

## 安裝 SSH 服務

```bash
sudo apt-get install openssh-server
sudo systemctl enable ssh
sudo ufw allow ssh
sudo systemctl start ssh
```

## REF
[How to Enable SSH Server on Ubuntu](https://www.cyberciti.biz/faq/how-to-install-ssh-on-ubuntu-linux-using-apt-get/)