# Visual Studio 2017 全新安裝之後無法正常開啟 DotNetCore 1.x 專案

> **原文發布日期:** 2017-10-16
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2017/10/16/dotnetcore1
> **標籤:** 無

---

'[7332] dotnet.exe' 程式以返回碼 -2147450749 (0x80008083) 結束。

先下結論

* 移除 VS2017
* 移除 DotNetCore 全版本
* 刪除資料夾 C:\Program Files\dotnet
* 安裝 DotNetCore 1.x (1.1 or 1.0)
* 安裝 VS2017

搞定

---

主要是新版VS2017 Update 3 之後自帶 DotNetCore 2.x

但是安裝之後 DotNet.exe 只會認得 2.x

即使自行安裝 1.x 版本 DotNet.exe 一樣無法關聯

導致 VS 呼叫 DotNet.exe 去跑 1.x 專案時會失敗

解決方法是先裝好舊版的 DotNetCore 1.0 or 1.1

這時候再安裝 vs2017 他會把 2.x 加上去

這時候 1.0 1.1 2.0 就可以正常跑了

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* C#
{ignore-vars="true"}
* VisualStudio
* .Net Core
{ignore-vars="true"}

* 回首頁

---

*本文章從點部落遷移至 Writerside*
