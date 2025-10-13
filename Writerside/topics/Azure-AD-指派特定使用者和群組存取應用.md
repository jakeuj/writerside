# Azure AD 指派特定使用者和群組存取應用

> **原文發布日期:** 2021-09-09
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/09/09/Azure-AD-User-Assigned
> **標籤:** 無

---

限制特定使用者和群組才能登入到我們網站

## 結論

Azure > AAD > 企業應用程式 > MyApp > 使用者和群組 > 新增使用者/群組 > 選你要允許登入的User/Group

Azure > AAD > 企業應用程式 > MyApp > 屬性 > 需要使用者指派嗎？ > 是

這樣只要不在事先指定名單的人/群組，登入網站時就會看到以下錯誤畫面

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/cdb64d1b-0a86-4a2c-880f-c0a7ef65c5cb/1631177406.png)

如果你把各種網站登入都使用同一個應用

然後把各網站的callback url 都設定進去

那這邊的登入限制就會套用到全部網站

因為這個控制是 By App

所以如果你有兩個不同的網站

分別需要允許不同的人可以登入

那就要在 Azure AD 註冊兩個不同的應用程式

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Azure AD](/jakeuj/Tags?qq=Azure%20AD)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
