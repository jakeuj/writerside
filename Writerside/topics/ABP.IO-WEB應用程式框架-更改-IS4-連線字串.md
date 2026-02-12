# ABP.IO WEB應用程式框架 更改 IS4 連線字串

> **原文發布日期:** 2021-08-26
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/08/26/Abp-IdentityServer-connection-string
> **標籤:** 無

---

將 Identify Server 4 的資料庫與我們自己 App 的資料庫分離

ABP 專案預設使用同一個資料庫，Appsettings 連接字串名稱為 Default.

但如果想把 Identify Server 4 相關的實體 (Tables) 分離出去

讓我們預設資料庫只剩下我們自己定義的實體

那麼就需要讓 IS4 使用另一個連接字串

在 ABP 其實只需要在 Appsettings.json 新增連接字串 AbpIdentityServer 就可以了

---

##### 連接字串

此模組用 `AbpIdentityServer` 於連接字串名稱。如果您沒有定義此名稱的連接字串，則它會回溯到 `Default` 連接字串。

有關詳細資訊，請參閱[連接字串](https://docs.abp.io/en/abp/latest/Connection-Strings)文檔。

參照：[Modules/IdentityServer | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Modules/IdentityServer#connection-string)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- IdentityServer

- 回首頁

---

*本文章從點部落遷移至 Writerside*
