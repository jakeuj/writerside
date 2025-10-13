# Visual Studio 2012 Update 2 找不到 WinLibJS_CORE.msi

> **原文發布日期:** 2013-04-29
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2013/04/29/102467
> **標籤:** 無

---

Visual Studio 2012 Update 2 找不到 WinLibJS\_CORE.msi
它其實暫存在C:\ProgramData\Package Cache\

今天裝好 Visual Studio 2012
接著更新 Update 2 時一直顯示找不到 WinLibJS\_CORE.msi
Google一下發現國外也有不少人遇到這問題
原因目前還尚未釐清
但解決方法倒是有
直接搜尋WinLibJS\_CORE.msi
發現它其實暫存在
C:\ProgramData\Package Cache\{89B4532E-19CE-4FA9-9692-10BFD5A38532}v1.0.8514.0\packages\WinLibJS\_CORE
其中GUID部分會不一樣，一般來說只要搜尋
C:\ProgramData\Package Cache\
應該就可以找到該檔
就可以繼續更新了
以上
參考來源：[MSDN](http://blogs.msdn.com/b/visualstudio/archive/2013/04/04/visual-studio-2012-update-2-is-here.aspx?PageIndex=4#comments)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* VisualStudio

* 回首頁

---

*本文章從點部落遷移至 Writerside*
