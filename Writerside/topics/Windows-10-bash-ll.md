# Windows 10 bash ll

> **原文發布日期:** 2019-12-16
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/12/16/bash
> **標籤:** 無

---

紀錄一下Windows使用Bash支援LL指令

的修改步驟這樣

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/0992e9aa-c2f6-41fe-88f4-40006a0405e3/1576469218_21726.png)

以管理員身分執行powershell

$ vim /etc/bash.bashrc

附加一行

(vim不熟的提示：先打 i 才能新增內容)

alias ll='ls -l'

存檔

這邊沒有用管理員身分執行會顯示無法儲存檔案

但也沒有 sudo 可以用來執行 vim

結論：用管理員身分執行powershell

(vim不熟的提示：ESC 加上 :wq)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [PowerShell](/jakeuj/Tags?qq=PowerShell)
* [Bash](/jakeuj/Tags?qq=Bash)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
