# ABP No.11 Client Proxies

> **原文發布日期:** 2019-01-18
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/01/18/abp11
> **標籤:** 無

---

ABP (ASP.NET Boilerplate) 應用程式開發框架 No.11 Client Proxies (Angular Service)

2019/05/16

```

<!-- Dynamic scripts of ABP system (They are created on runtime and can not be bundled) -->
<script src="/AbpServiceProxies/GetAll?v=636936233930104767" type="text/javascript"></script>
<script src="/AbpScripts/GetScripts?v=636936233930109610" type="text/javascript"></script>
<!-- View specific scripts -->

<script type="text/javascript">
 abp.services.app.user.getUser({
  "id": 0,
  "retryNumber": 0
 },{ //override jQuery's ajax parameters
  async: false,
  timeout: 30000
 }).done(function (result) {
  abp.notify.success('successfully created a task!');
  console.log(result);
 });
</script>
```

---

結論，更新完web api之後執行angular專案內的NSWAG更新批次檔

.\angular\nswag\refresh.bat

就會自動更新 service-proxies.ts

如果API網址有改了話

要到 service.config.nswag 裡面改 url

```

"url": "http://localhost:21021/swagger/v1/swagger.json",
```

如果是在既有服務內新增方法了話

以上步驟就可以更新出新方法來給組件使用

But!人生中最重要的就是這個But!

但如果是新增一個服務

那就還要到 service-proxy.module.ts 裡面註冊

例如 API 新增 WalletService 這個服務

那就要加上一行

```

ApiServiceProxies.WalletServiceProxy,
```

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/e7037ec3-b3b6-4a18-96bd-e3915df0c9d1/1554200821_12006.jpg)

ABP對這部分的說明文檔如下

https://aspnetboilerplate.com/Pages/Documents/AspNet-Core#client-proxies

EX:http://localhost:21021/AbpServiceProxies/GetAll?type=jquery

但沒有針對angular的TypeScript做說明

微軟Dotnet Core使用NSWAG studio動態產生用戶端的文檔

https://docs.microsoft.com/zh-tw/aspnet/core/tutorials/getting-started-with-nswag?view=aspnetcore-2.2&tabs=visual-studio%2Cvisual-studio-xml#generate-code-with-nswagstudio

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- ABP
- Angular

- 回首頁

---

*本文章從點部落遷移至 Writerside*
