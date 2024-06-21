# GUI-VcXsrv

記錄下 Windows 11 使用 VcXsrv 來運行 Linux GUI 程式的方法。

## 安裝 VcXsrv
這是一個 Windows 上的 X Server，可以讓 Windows 上運行的程式顯示 Linux 的 GUI 界面。

首先，於 Windows 下載 VcXsrv 安裝程式：

[VcXsrv](https://sourceforge.net/projects/vcxsrv/)

安裝時，選擇 `Multiple windows`，其他選項保持默認即可。

到這邊可以從 windows 右下角的通知區域找到 VcXsrv 的圖示，點擊 Application 裡面有計算機跟時鐘可以開出來。

如果要讓 WSL 2 使用 VcXsrv：

- Windows 防火牆需要允許 VcXsrv (XLaunch.exe, VcXsrv.exe) 通過，或者直接關閉防火牆。
- 運行 VcXsrv 時，選擇 `Disable access control`，並附加參數 `-ac`。

否則 WSL 2 會連不到 VcXsrv 或出現以下錯誤：

`Authorization required, but no authorization protocol specified`

## 取得 IP
在 Windows 11 中，打開 PowerShell，輸入：

```bash
ipconfig
```

找到 `WSL` 的網卡，記下 `IPv4 Address`。

例如：192.168.1.2

## 設定 WSL
在 WSL 中，設定 `DISPLAY` 環境變數，

將上面查到的 IP 填進去，以 192.168.1.2 為例：

```bash
export DISPLAY=192.168.1.2:0
```

## 運行 GUI 程式
在 WSL 中運行 GUI 程式，例如 `gedit`：

```bash
gedit
```

這樣，你就可以在 Windows 11 上運行 Linux 的 GUI 程式了。

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