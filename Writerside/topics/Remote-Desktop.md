# Remote-Desktop

筆記一下 Ubuntu Desktop 22.04 遠端桌面的使用方式。

## update

```Bash
sudo apt-get update
```

## 安裝 xrdp

```Bash
sudo apt install xrdp -y
sudo adduser xrdp ssl-cert
sudo systemctl enable --now xrdp
sudo ufw allow from any to any port 3389 proto tcp
sudo reboot
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

## Refresh Repository

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

## Wifi

```Bash
sudo nano /etc/polkit-1/localauthority/50-local.d/47-allow-wifi.pkla
```

```Ini
[Allow Refresh Repository all Users]
Identity=unix-user:*
Action=org.freedesktop.NetworkManager.wifi.scan;org.freedesktop.NetworkManager.enable-disable-wifi;org.freedesktop.NetworkManager.settings.modify.own;org.freedesktop.NetworkManager.settings.modify.system;org.freedesktop.NetworkManager.network-control;
ResultAny=yes
ResultInactive=yes
ResultActive=yes
```


## 新建帳號 (Optional)

```Bash
sudo adduser newuser
sudo visudo -f /etc/sudoers.d/newuser
```

`/etc/sudoers.d/newuser`

```
newuser ALL=(ALL:ALL) ALL
```

### 切換身分

```Bash
sudo - newuser
```


## 連線

使用 Windows 的遠端桌面連線到 Ubuntu。

## 參考
[需要認證才能建立色彩描述檔](https://zhuanlan.zhihu.com/p/515649815)
[Set Up xrdp on Ubuntu 22.04 With the Gnome Desktop Environment](https://luppeng.wordpress.com/2024/03/12/set-up-xrdp-on-ubuntu-22-04-with-the-gnome-desktop-environment/)
[Ubuntu Remote Desktop Access from Windows](https://linuxconfig.org/ubuntu-20-04-remote-desktop-access-from-windows-10)
[安裝和設定 xrdp 以搭配 Ubuntu 使用遠端桌面](https://learn.microsoft.com/zh-tw/azure/virtual-machines/linux/use-remote-desktop?tabs=azure-cli)
[https://hhming.moe/post/windows-remote-ubuntu-22-04/](https://hhming.moe/post/windows-remote-ubuntu-22-04/)
[How to Access Ubuntu via Remote Desktop from Windows](https://phoenixnap.com/kb/ubuntu-remote-desktop-from-windows)