# Visual Studio 2012 .Net 4.5 Validator Error 解決方案

> **原文發布日期:** 2012-10-04
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2012/10/04/75269
> **標籤:** 無

---

Visual Studio 2012 .Net 4.5 Validator Error 解決方案
WebForms UnobtrusiveValidationMode 需要 'jquery' 的 ScriptResourceMapping。

Visual Studio 2012 .Net 4.5 Validator Error

不知道 Visual Studio 2012 .Net 4.5 Validator 驗證元件的人生出了甚麼意外...
一旦用了驗證元件就會跳出錯誤，錯誤訊息如下

## *WebForms UnobtrusiveValidationMode 需要 'jquery' 的 ScriptResourceMapping。請加入 ScriptResourceMapping 命名的 jquery (區分大小寫)。*

總之解決方是>工具>程式庫管理員>Package Manager Console>輸入命令
"Install-Package Microsoft.ScriptManager.jQuery"
之後我的驗證元件考試都拿一百分呢！

參考來源：

<http://nuget.org/packages/Microsoft.ScriptManager.jQuery>

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- VisualStudio

- 回首頁

---

*本文章從點部落遷移至 Writerside*
