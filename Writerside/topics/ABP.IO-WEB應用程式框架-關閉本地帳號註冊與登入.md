# ABP.IO WEB應用程式框架 關閉本地帳號註冊與登入

> **原文發布日期:** 2021-08-19
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/08/19/AbpAccountIsSelfRegistrationEnabledFalse
> **標籤:** 無

---

筆記一下不開放路人註冊

## 結論

appsettings.json 設定以下內容

```
"Settings": {
    "Abp.Account.IsSelfRegistrationEnabled": false,
    "Abp.Account.EnableLocalLogin": false
}
```

* `IsSelfRegistrationEnabled` 本地註冊
* `EnableLocalLogin` 本地登入

外部登入比如 AzureAd, FB, Google, MS…ETC. 就會自動導到OAuth登入頁

## Identity Server Clients Enable Local Login

這邊值得注意的是如果 Blazor, Angular, 或其他系統有使用我們自己的 is4 OAuth 登入

**則每個 clinet 有各自對應的** `EnableLocalLogin`

設定在資料庫的 [IdentityServerClients].[EnableLocalLogin]

也要改成 false 不然還是會停在登入選擇畫面哦

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [ABP](/jakeuj/Tags?qq=ABP)
* [Azure AD](/jakeuj/Tags?qq=Azure%20AD)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
