# DotNetCore IIS Hosting Bundle

> **原文發布日期:** 2021-05-10
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/05/10/DotNetCoreHostingBundleIIS
> **標籤:** 無

---

首先認明以下安裝套件

ASP.NET Core Runtime - Windows Hosting Bundle Installer

重點是 Runtime 不等於 Hosting Bundle

## 流程

正確流程應該是先安裝 IIS 再安裝 Hosting Bundle

## IIS

伺服器角色新增IIS功能，一直下一步即可

## Hosting Bundle

各版本下載位置：https://dotnet.microsoft.com/download

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/66a63053-da7e-468b-b76f-c2782e9f4d08/1620637926.png)

Download .Net Core Runtime => Hosting Bundle

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/66a63053-da7e-468b-b76f-c2782e9f4d08/1620637980.png)

這沒裝好會跑出 web.config 解析錯誤，大概是 IIS 不認識 AspNetCore Module V2

**若裝載套件組合 (Hosting Bundle) 在 IIS 之前安裝，則必須對該套件組合安裝進行修復 (Repair)。**

**請在安裝 IIS 之後，再次執行裝載套件組合安裝程式。**

再點一次安裝檔然後選擇修復，再不行移除重裝吧

## 500.19

權限不足

然後建立一個資料夾把 publish 出來的檔案丟進去

把這站台右鍵內容安全性新增 IIS\_USER 賦予 完全控制 權限

## 應用程式集區

再到 IIS 新增站台 路徑選剛剛建立的資料夾

到 應用程式集區 把新的應用程式  CLR 改成 沒有 Managed 程式碼

## HTTP Error 502.5 - Process Failure

我重啟站台是沒執行這段也可以正常運行

如果你遇到 502.5，可以用管理員身分執行以下命令

```
net stop was /y
net start w3svc
```

參照：

https://docs.microsoft.com/zh-tw/aspnet/core/host-and-deploy/iis/hosting-bundle?view=aspnetcore-5.0

https://blog.johnwu.cc/article/iis-run-asp-net-core.html

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* .Net Core
{ignore-vars="true"}
* IIS

* 回首頁

---

*本文章從點部落遷移至 Writerside*
