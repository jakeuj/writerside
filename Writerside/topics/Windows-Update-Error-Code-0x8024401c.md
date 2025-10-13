# Windows Update Error Code 0x8024401c

> **原文發布日期:** 2021-03-17
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/03/17/8024401c
> **標籤:** 無

---

今天按了 Windows Update 一直錯誤

先下結論，公司組織管理 Windows Update，所以要內網才能進行更新

所以如果你在公司看到這個錯誤，先確定網路目前是不是公司內部

不然外部無法解析公司 Windows Update Server 的位置會導致更新失敗

如果還是不能可以試試以下搬運過來的方法

我也是從這打開 regedit 看到 WUServer (Windows Update Server)

裡面設定值是一個公司 domain 才想到是無法解析 DNS 的

---

以系統管理員身分執行命令提示字元，然後執行下列三行指令：

net stop wuauserv
reg delete HKEY\_LOCAL\_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate
net start wuauserv

操作如下：
C:\Windows\system32>net stop wuauserv
Windows Update 服務正在停止.
Windows Update 服務已經成功停止。

C:\Windows\system32>reg delete HKEY\_LOCAL\_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate
是否要永久刪除登錄機碼 HKEY\_LOCAL\_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate (是/否)? y
操作順利完成。

C:\Windows\system32>
C:\Windows\system32>net start wuauserv
Windows Update 服務正在啟動 .
Windows Update 服務已經啟動成功。

完成重開機後，再試一次更新就成功了。

參照：https://blog.twtnn.com/2017/12/win-10-update-0x8024401c.html

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Windows](/jakeuj/Tags?qq=Windows)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
