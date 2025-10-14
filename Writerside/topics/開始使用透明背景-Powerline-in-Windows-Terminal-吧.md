# Windows Terminal Powerline

> **原文發布日期:** 2021-02-01
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/02/01/WindowsTerminal
> **標籤:** 無

---

用了一陣子Mac之後

用回Windows差異還是不少

其中 Terminal 也是一項

看看如何改成較相似的 Powerline

背景也可以設定成半透明

2021/8/24 補充

將 dotnet core 的 Powershell 設定到 Rider 的 Terminal 路徑

`pwsh`

(`%USERPROFILE%\.dotnet\tools\pwsh.exe`)
{ignore-vars="true"}

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/ebafa58a-d66d-46c8-9056-462b4bc8d04f/1634788135.png)

---

今天收到微軟一封信

https://devblogs.microsoft.com/commandline/getting-started-with-windows-terminal/

![](https://store-images.s-microsoft.com/image/apps.64156.14050269303149694.7b8b314c-8217-47f4-8ecc-7a4c0b4488d2.e5859e84-ce21-48d7-a66d-7a864026df13?w=1399&h=792&q=90&format=jpg)

其中這張預覽圖正中我心

* 總之先照著下載一下 Windows Terminal

[取得 Windows Terminal - Microsoft Store zh-TW](https://www.microsoft.com/zh-tw/p/windows-terminal/9n0dx20hk701?activetab=pivot:overviewtab)

* 安裝新版 PowerShell

[取得 PowerShell - Microsoft Store zh-TW](https://www.microsoft.com/zh-tw/p/powershell/9mz1snwt0n5d?rtc=1#activetab=pivot:overviewtab)

* 安裝 Powerline 字型

[Releases · microsoft/cascadia-code · GitHub](https://github.com/microsoft/cascadia-code/releases)

* 設定 PowerShell

[Windows Terminal Powerline Setup | Microsoft Docs](https://docs.microsoft.com/en-us/windows/terminal/tutorials/powerline-setup)

```
Install-Module posh-git -Scope CurrentUser
Install-Module oh-my-posh -Scope CurrentUser
```

```
notepad $PROFILE
```

> Import-Module posh-git
> Import-Module oh-my-posh
> Set-PoshPrompt Paradox

最後一行可以改成自己要的主題樣式名稱

https://github.com/JanDeDobbeleer/oh-my-posh#themes

※ **重要的**

腳本執行策略必須設置為**RemoteSigned**或**Unrestricted**才能運行配置文件腳本。運行此命令以查看當前的執行策略`Get-ExecutionPolicy`。[**了解有關執行策略的更多信息**](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies)

[使用管理員權限執行 Windows PowerShell 並輸入以下命令允許遠端簽屬指令碼執行](https://ithelp.ithome.com.tw/articles/10028377)

```
Set-ExecutionPolicy RemoteSigned
```

* 設定 Windows Terminal

畫面上方 Tab 向下箭頭按進去 > 設定 > 開啟Json設定檔 (左下方)

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/ebafa58a-d66d-46c8-9056-462b4bc8d04f/1612145191.png)

於 profiles > defaults 加入設定

```
"profiles": {
  "defaults": {
    // Put settings here that you want to apply to all profiles.
    // 啟用視窗透明度(這邊開了背景圖會比較白)
    // "useAcrylic": true,
    // "acrylicOpacity": 0.5,
    // 背景透明度
    "backgroundImageOpacity": 0.2,
    // 背景圖片
    "backgroundImage": "C:\\Users\\jake.chu\\Pictures\\332769.jpg",
    // 主題設定
    "colorScheme": "Tango Dark",
    // 字型設定(請找PowerLine字型)
    "fontFace": "Cascadia Code PL"
  }
}
```

主要是字型，不然會亂碼，其他隨意

背景圖如果不註解，記得把路徑 backgroundImage 改成自己要的圖片

這邊可以順便把 defaultProfile 改成下方 list 中的新版 PowerShell's GUID

其中主題 colorScheme 可以改成自己要的樣式名稱

https://docs.microsoft.com/en-us/windows/terminal/custom-terminal-gallery/custom-schemes

這邊會覆蓋 PowerShell 的配色設定，也可以不設吃原本 PS 的主題配色

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/ebafa58a-d66d-46c8-9056-462b4bc8d04f/1612521497.png)

acrylicOpacity 0.5 會比較亮

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/ebafa58a-d66d-46c8-9056-462b4bc8d04f/1612521140.png)
![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* PowerShell
* Terminal

* 回首頁

---

*本文章從點部落遷移至 Writerside*
