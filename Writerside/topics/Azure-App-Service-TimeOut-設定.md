# Azure App Service TimeOut 設定

> **原文發布日期:** 2021-08-23
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/08/23/AzureAppServiceTimeOut
> **標籤:** 無

---

筆記下解決連線逾時的相關設定

applicationHost.xdt & web.config

## applicationHost.xdt

就 App Service 沒有直接開放 IIS 相關設定給我們去調整

所以要使用以上文件來進行設定

並放到 D:\home\site\applicationHost.xdt

內容如下

```
<?xml version="1.0"?>
<configuration xmlns:xdt="http://schemas.microsoft.com/XML-Document-Transform">
  <system.applicationHost>
    <webLimits xdt:Transform="SetAttributes(connectionTimeout)" connectionTimeout="00:15:00">
  </system.applicationHost>
</configuration>
```

其中 `connectionTimeout` 就設定自己需要的時間

## web.config

```
<system.web>
    <httpRuntime maxRequestLength="2097151" executionTimeout="900" />
    <!--单位：KB 3072=3MB   默认是4MB,最大支持2GB, executionTimeout單位是秒-->
</system.web>
<system.webServer>
    <security>
      <requestFiltering>
        <requestLimits maxAllowedContentLength="2147483648" />
        <!--单位：Bytes  2147483648=2 GB 默认是4MB,最大支持2GB-->
      </requestFiltering>
    </security>
</system.webServer>
```

參照：[ASP.NET中maxRequestLength和maxAllowedContentLength的区别；上传大文件设置IIS7文件上传的最大大小\_慢谈人生-CSDN博客](https://blog.csdn.net/qq_23663693/article/details/89920039)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [.NET Framework](/jakeuj/Tags?qq=.NET%20Framework)
* [Azure](/jakeuj/Tags?qq=Azure)
* [IIS](/jakeuj/Tags?qq=IIS)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
