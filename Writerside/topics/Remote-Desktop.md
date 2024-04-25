# Remote-Desktop

筆記一下 Ubuntu Desktop 22.04 遠端桌面

![rdp.png](rdp.png)

## update

```Bash
sudo apt-get update
```

## 安裝 xrdp (會自動安裝 xorgxrdp)

```Bash
sudo apt-get -y install xrdp
sudo systemctl enable xrdp
sudo adduser xrdp ssl-cert
echo gnome-session --session=ubuntu >~/.xsession
sudo service xrdp restart
sudo ufw allow 3389
sudo reboot
```

在 Ubuntu Desktop 系統上設置 xrdp 以允許 Windows 透過遠端桌面連線的步驟如下:

1. 首先,更新套件庫並安裝 xrdp 和 xorgxrdp:

```
sudo apt update
sudo apt install xrdp xorgxrdp
```

2. 設置 xrdp 使用的埠 (預設為 3389)。編輯 /etc/xrdp/xrdp.ini 檔案:

```
sudo nano /etc/xrdp/xrdp.ini
```

找到這一行並確保未被註解:

```
port=3389
```

3. 設置會話啟用 Ubuntu Desktop:

```
sudo nano /etc/xrdp/startwm.sh
```

在檔案末尾加上:

```
startgnome
```

### Gnome

如果您偏好使用其他桌面環境如 GNOME 或 KDE，只需將 `startxfce4` 改為 `startgnome` 或 `startplasma-x11` 即可。

4. 設置遠端桌面安全性層級。編輯 /etc/xrdp/xrdp.ini:

```
sudo nano /etc/xrdp/xrdp.ini
```

找到這一行並確保未被註解:

```
crypt_level=high
```

5. 重啟 xrdp 服務:

```
sudo systemctl restart xrdp
```

6. 開放防火牆埠 (如果有的話)，允許 RDP 連線:

```
sudo ufw allow 3389
```

7. RDP
現在您可以從 Windows 電腦使用內建的遠端桌面連線來連線 Ubuntu Desktop。只需輸入 Ubuntu 電腦的 IP 位址和使用者憑證即可。
這樣就設置完成了，您應該能夠順利透過 Windows 遠端桌面連線到 Ubuntu 桌面環境了。

### xorgxrdp 是什麼?

xorgxrdp 是一個 X.Org 遠端桌面會話代理程式,它的目的是為了提供圖形化的遠端桌面環境。當搭配 xrdp 使用時,它允許遠端客戶端(如 Windows 遠端桌面連線)透過 RDP 協定連線到 Linux 桌面會話。

安裝 xorgxrdp 的主要原因是為了讓 Windows 遠端桌面連線可以顯示完整的 Linux 桌面環境,而不僅僅是命令列界面。它充當了在遠端和本地 X Server 之間的橋樑,將圖形化的桌面繪製輸出傳送給遠端客戶端。

總的來說,xorgxrdp 在 xrdp 遠端桌面環境中扮演了下列角色:

啟動 X Server 以提供圖形化桌面界面。
與 xrdp 服務整合,接收來自遠端客戶端的圖形指令。
將桌面顯示輸出壓縮並傳送給遠端客戶端。
從遠端客戶端接收鍵盤/滑鼠輸入,並將其轉譯到本地 X Server。
因此,在設置允許 Windows 透過 RDP 連線 Linux 桌面環境時,安裝 xorgxrdp 是必要的一步,以確保遠端桌面能正確顯示並與圖形界面互動。

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
[Authentication required. System policy prevents WiFi scans](https://blog.yanjingang.com/?p=6258)