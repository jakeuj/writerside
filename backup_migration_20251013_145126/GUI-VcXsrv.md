# GUI-VcXsrv

這是一個 Windows 上的 X Server，可以讓 Windows 上運行的程式顯示 Linux 的 GUI 界面。

## 安裝 VcXsrv
首先，於 Windows 下載 VcXsrv 安裝程式：

[VcXsrv](https://sourceforge.net/projects/vcxsrv/)

到這邊可以從 windows 右下角的通知區域找到 VcXsrv 的圖示，點擊 Application 裡面有計算機跟時鐘可以開出來。

如果要讓 WSL 2 使用 VcXsrv：

- 運行 VcXsrv 時，選擇 `Disable access control`。
- Windows 防火牆需要允許 VcXsrv (XLaunch.exe, VcXsrv.exe) 通過，或者直接關閉防火牆。

否則 WSL 2 會連不到 VcXsrv 或出現以下錯誤：

`Authorization required, but no authorization protocol specified`

## 設定 WSL
在 WSL 中，設定 `DISPLAY` 環境變數，

```bash
# 設置 DISPLAY 環境變量
export DISPLAY=$(ip route show | grep -i default | awk '{ print $3 }'):0
```

或設定到 .bashrc：

```bash
echo "export DISPLAY=$(ip route show | grep -i default | awk '{ print $3 }'):0" >> ~/.bashrc
source ~/.bashrc
```

REF: 
[從 Linux (主機 IP) 存取 Windows 網路應用程式](https://learn.microsoft.com/zh-tw/windows/wsl/networking#accessing-windows-networking-apps-from-linux-host-ip)

## 運行 GUI 程式
在 WSL 中運行 GUI 程式，例如 `xclock`：

```bash
sudo apt install x11-apps
xclock
```

這樣，你就可以在 Windows 上運行 Linux 的 GUI 程式了。

## 遠端桌面

如果需要遠端桌面，可以安裝 xfce4：

```bash
sudo apt-get install xfce4-terminal
sudo apt-get install xfce4
```

然後運行：

```bash
sudo startxfce4
```

![xfce4.png](xfce4.png)

這樣就可以在 Windows 11 上運行 Linux 的桌面了。

![image_11.png](image_11.png)