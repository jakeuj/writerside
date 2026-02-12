# ASP.NET WebSite 使用新版 C #

> **原文發布日期:** 2021-12-16
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/12/16/WebSite-CSharp-7
> **標籤:** 無

---

紀錄一下舊專案使用新語法的心路歷程

舊版 ASP.NET WebSite 只支援 C# 5.0

要使用新版 C# 7.3 語法就需要使用 roslyn

所以需要從 Nuget 安裝套件 `Microsoft.CodeDom.Providers.DotNetCompilerPlatform`

實際上我安裝的時候會顯示找不到 `system.codedom` 區段導致安裝失敗

所以最後我是直接在 web.config 加上面這段設定

並於 packages.config 直接加入 Microsoft.CodeDom.Providers.DotNetCompilerPlatform

packages.config

```
<?xml version="1.0" encoding="utf-8"?>
<packages>
  <package id="Microsoft.CodeDom.Providers.DotNetCompilerPlatform" version="3.6.0" targetFramework="net48" developmentDependency="true" />
</packages>
```

並於 web.config 指定要使用的 C# 版本 (`langversion:7.3`)

web.config

```
<?xml version="1.0"?>
<configuration xmlns="http://schemas.microsoft.com/.NetConfiguration/v2.0">
  <system.codedom>
    <compilers>
      <compiler extension=".cs" language="c#;cs;csharp" warningLevel="4"
        compilerOptions="/langversion:7.3 /nowarn:1659;1699;1701;612;618"
        type="Microsoft.CodeDom.Providers.DotNetCompilerPlatform.CSharpCodeProvider,
              Microsoft.CodeDom.Providers.DotNetCompilerPlatform,
              Version=3.6.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35" />
    </compilers>
  </system.codedom>
</configuration>
```

[How to use C# 6.0 or 7.0 in an old ASP.NET Website (not Website Project) - Stack Overflow](https://stackoverflow.com/questions/56130824/how-to-use-c-sharp-6-0-or-7-0-in-an-old-asp-net-website-not-website-project)

雖然在 IDE 可以使用新語法不會報錯

但實際執行的時候卻出現

## `找不到路徑 '\bin\roslyn\csc.exe' 的一部分。`

暫時解決方法是複製以下內容

/packages/Microsoft.CodeDom.Providers.DotNetCompilerPlatform.3.6.0/tools/Roslyn472/

到專案的

bin/roslyn/

[[沒有蠢問題] 找不到路徑 bin\roslyn\csc.exe | 聊聊程式 - 點部落 (dotblogs.com.tw)](https://dotblogs.com.tw/initials/2021/02/11/144248)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- .NET Framework
{ignore-vars="true"}

- 回首頁

---

*本文章從點部落遷移至 Writerside*
