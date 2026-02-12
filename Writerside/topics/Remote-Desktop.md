# Remote-Desktop

筆記一下 Ubuntu Desktop 22.04 遠端桌面

![rdp.png](rdp.png){style="block"}

## update && upgrade

```Bash
sudo apt-get update
sudo apt-get upgrade
```

## 安裝 xrdp (會自動安裝 xorgxrdp)

```Bash
sudo apt install xrdp -y
sudo adduser xrdp ssl-cert
sudo service xrdp restart
sudo ufw allow 3389
sudo systemctl enable xrdp
```

## 需要認證才能建立色彩描述檔

```Bash
sudo nano /etc/polkit-1/localauthority/50-local.d/45-allow-colord.pkla
```

```Ini
[Allow Colord all Users]
Identity=unix-user:*
Action=org.freedesktop.color-manager.create-device;org.freedesktop.color-manager.create-profile;org.freedesktop.color-manager.delete-device;org.freedesktop.color-manager.delete-profile;org.freedesktop.color-manager.modify-device;org.freedesktop.color-manager.modify-profile
ResultAny=no
ResultInactive=no
ResultActive=yes
```

## 需要認證才能 Refresh Repository

```Bash
sudo nano /etc/polkit-1/localauthority/50-local.d/46-allow-packagekit.pkla
```

```Ini
[Allow Refresh Repository all Users]
Identity=unix-user:*
Action=org.freedesktop.packagekit.system-sources-refresh
ResultAny=no
ResultInactive=no
ResultActive=yes
```

## 需要認證才能掃描 Wifi

```Bash
sudo nano /etc/polkit-1/localauthority/50-local.d/47-allow-wifi-scan.pkla
```

```Ini
[Allow Wifi Scan]
Identity=unix-user:*
Action=org.freedesktop.NetworkManager.wifi.scan;org.freedesktop.NetworkManager.enable-disable-wifi;org.freedesktop.NetworkManager.settings.modify.own;org.freedesktop.NetworkManager.settings.modify.system;org.freedesktop.NetworkManager.network-control
ResultAny=yes
ResultInactive=yes
ResultActive=yes
```

## 連線

使用 Windows 的遠端桌面連線到 Ubuntu。

(輸入帳號密碼後請耐心等待空無一物的綠色背景畫面)

## 參考

[如何在Ubuntu上安裝 Xrdp 伺服器 22.04](https://www.turbogeek.co.uk/how-to-install-xrdp-server-on-ubuntu-22-04/)

[需要認證才能建立色彩描述檔](https://zhuanlan.zhihu.com/p/515649815)

[解決Ubuntu“需要身份驗證。系統策略阻止WiFi掃描“問題](https://blog.yanjingang.com/?p=6258)

[用 Windows 遠端 Ubuntu 22.04](https://hhming.moe/post/windows-remote-ubuntu-22-04/)
