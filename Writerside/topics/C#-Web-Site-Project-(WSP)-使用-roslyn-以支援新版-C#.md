# C# Web Site Project (WSP) 使用 roslyn 以支援新版 C#

> **原文發布日期:** 2023-12-28
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/12/28/WSP-Microsoft-CodeDom-Providers-DotNetCompilerPlatform-WebSites
> **標籤:** 無

---

安裝 bin\roslyn\csc.exe 以支援 C# 7.3 以上版本的正確新姿勢

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/3fcdd9f8-51f2-46b3-818e-5484f06cbc66/1704353581.png.png)

## 結論

~~**珍愛生命，遠離 Web Site Project**~~

改為安裝以下套件 (原本是 [Microsoft.CodeDom.Providers.DotNetCompilerPlatform](https://www.nuget.org/packages/Microsoft.CodeDom.Providers.DotNetCompilerPlatform))

[Microsoft.CodeDom.Providers.DotNetCompilerPlatform.WebSites](https://www.nuget.org/packages/Microsoft.CodeDom.Providers.DotNetCompilerPlatform.WebSites)

## 備註

找不到 `Bin\roslyn\csc.exe` 時，可以到 `套件管理器主控台` 執行以下命令

`Update-Package Microsoft.CodeDom.Providers.DotNetCompilerPlatform.WebSites -r`

## 說明

最近更新 [Microsoft.CodeDom.Providers.DotNetCompilerPlatform](https://www.nuget.org/packages/Microsoft.CodeDom.Providers.DotNetCompilerPlatform) 到 4.1.0 版本

發現找不到新編譯器 [bin\roslyn\csc.exe](https://stackoverflow.com/questions/32780315/could-not-find-a-part-of-the-path-bin-roslyn-csc-exe)

一路追查到官方 GITHUB

才發現新版本已經改用 csproj 來處理

但是舊專案是 Web Site Project (WSP)

並沒有 .csproj 專案檔可以用

好在？官方貼心的為我們準備了另一個套件

[Microsoft.CodeDom.Providers.DotNetCompilerPlatform.WebSites](https://www.nuget.org/packages/Microsoft.CodeDom.Providers.DotNetCompilerPlatform.WebSites)

專門給一些老不死的專案來用

總之我移除重新裝了之後 roslyn 又會出現在 bin 裡頭了

## 參考

完全遷移到基於 msbuild/targets 的模型將破壞無專案的 ASP.Net “網站” [Web Site Project (WSP)]。

###### 隨著 NuGet 的不斷發展，舊的 install.ps1 做事方式變得越來越站不住腳。 切換到 msbuild/targets 是一個簡單的選擇。 但是“網站”專案在 msbuild 中的支援非常有限。 我們創建了一個新包，該包恢復了僅適用於網站的 3.X 版本的“install.ps1”功能。 它被稱為 `Microsoft.CodeDom.Providers.DotNetCompilerPlatform.WebSites`。

## 來源

[GitHub - aspnet/RoslynCodeDomProvider: Roslyn CodeDOM provider](https://github.com/aspnet/RoslynCodeDomProvider)

## 延伸閱讀

[Convert Web site (WSP) to Web Application (WAP) with Visual Studio 2019 | 御用小本本 - 點部落 (dotblogs.com.tw)](https://dotblogs.com.tw/jakeuj/2021/03/02/Convert-Web-site-to-WebApplication-Visual-Studio-2019)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Roslyn
* WSP

* 回首頁

---

*本文章從點部落遷移至 Writerside*
