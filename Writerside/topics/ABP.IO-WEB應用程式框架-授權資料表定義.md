# ABP.IO WEB應用程式框架 授權資料表定義

> **原文發布日期:** 2021-07-26
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/07/26/ABP-Authorization-DB
> **標籤:** 無

---

以實際資料表的資料、前端畫面與 Chrome F12 Network XHR

來看 ABP 的權限管理系統是如何運作的

## .Net Core Identity

ABP 授權基於微軟官方 .Net Core Identity，這邊先看一下實體相關訊息

### [實體類型](https://docs.microsoft.com/zh-tw/aspnet/core/security/authentication/customize-identity-model?view=aspnetcore-5.0#entity-types)

此 Identity 模型包含下列實體類型：

* User 代表使用者。
* Role 代表角色。
* UserClaim 表示使用者擁有的宣告。
* UserToken 表示使用者的驗證權杖。
* UserLogin 將使用者與登入產生關聯。
* RoleClaim 代表授與角色內所有使用者的宣告。
* UserRole 關聯使用者和角色的聯結實體。

### [實體類型關聯性](https://docs.microsoft.com/zh-tw/aspnet/core/security/authentication/customize-identity-model?view=aspnetcore-5.0#entity-type-relationships)

實體類型會以下列方式彼此相關：

* 每個都 User 可以有許多 UserClaims 。
* 每個都 User 可以有許多 UserLogins 。
* 每個都 User 可以有許多 UserTokens 。
* 每個都 Role 可以有許多相關聯的 RoleClaims 。
* 每個都 User 可以有許多相關聯 Roles ，而且每個都 Role 可以與許多相關聯 Users 。 這是多對多關聯性，需要資料庫中的聯結資料表。 聯結資料表是由 UserRole 實體表示。

## ABP 授權

ABP 在 .Net Core Identity 的使用者與角色之外又加了一個授權表，授權相關資料表如下

1. [AbpUsers]：使用者
2. [AbpRoles]：角色
3. [AbpUserRoles]：使用者角色關係
4. [AbpPermissionGrants]：權限授予

使用者與角色應該沒有甚麼問題，這邊主要介紹一下 AbpPermissionGrants 這張表

### AbpPermissionGrants (權限授予表)

* [Name]：賦予權限名稱
  + BookStore.Books：讀取
  + BookStore.Books.Create：建立
  + BookStore.Books.Edit：更新
  + BookStore.Books.Delete：刪除
* [ProviderName]：決定 [ProviderKey] 的種類
  + R：Role(角色)
  + U：User(使用者)
  + (應該還有個C代表Client)
* [ProviderKey]：紀錄實際賦予權限的目標
  + [AbpRoles].[Name]：角色名稱
    - Admin
    - Tester
  + [AbpUsers].[Id]：使用者唯一識別碼
    - 0bac35fb-50b2-b79c-ca02-39fdf320f3f7

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/6fd09af3-b898-487f-9d4c-07560af3b657/1627279013.png)

從關聯性可以看出使用者與角色中間透過使用者角色建立關係

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/6fd09af3-b898-487f-9d4c-07560af3b657/1627278831.png)

從資料可以看出全賦予的ProviderKey對應到角色的名稱

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/6fd09af3-b898-487f-9d4c-07560af3b657/1627278835.png)

而前端如何知道系統有哪些權限，使用者又取得了甚麼權限，則是透過 application-configuration 這支 API 回傳 Auth 的 Policies 與 GrantedPolicies

Auth

* GrantedPolicies
  + BookStore.Authors
  + BookStore.Authors.Create
* Policies
  + BookStore.Authors
  + BookStore.Authors.Create
  + BookStore.Authors.Edit
  + BookStore.Authors.Delete

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/6fd09af3-b898-487f-9d4c-07560af3b657/1627278841.png)

然後前端可以根據這些權限資料來決定menu與按鈕要不要顯示給使用者操作對應功能

比如：Admin 登入會顯示管理，Tester 登入責管理不會出現在 menu 中

(應該也可以透過 claim 來看)

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/6fd09af3-b898-487f-9d4c-07560af3b657/1627278847.png)

[以角色為基礎的存取控制](https://zh.wikipedia.org/wiki/%E4%BB%A5%E8%A7%92%E8%89%B2%E7%82%BA%E5%9F%BA%E7%A4%8E%E7%9A%84%E5%AD%98%E5%8F%96%E6%8E%A7%E5%88%B6)

1.會先建立角色

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/6fd09af3-b898-487f-9d4c-07560af3b657/1627278854.png)

2.賦予角色權限

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/6fd09af3-b898-487f-9d4c-07560af3b657/1627278861.png)

3.修改使用者

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/6fd09af3-b898-487f-9d4c-07560af3b657/1627278870.png)

4.賦予使用者角色

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/6fd09af3-b898-487f-9d4c-07560af3b657/1627278906.png)

也可以直接給使用者特定權限

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/6fd09af3-b898-487f-9d4c-07560af3b657/1627278919.png)

直接將權限賦予使用者Id

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/6fd09af3-b898-487f-9d4c-07560af3b657/1627278923.png)

這邊的U代表使用者，R代表角色，冒號後面則是對應的Key

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/6fd09af3-b898-487f-9d4c-07560af3b657/1627278926.png)

回資料庫可以看到權限賦予時直接將使用者的Id當作Key存進了權限賦予表中。

參照：

[ABP.IO WEB應用程式框架 新手教學 No.06 開發教學 第 5 部分 授權](https://dotblogs.com.tw/jakeuj/2021/07/23/ABP-Tutorials-Part-5)

[官方說明文件 - 權限](https://docs.abp.io/zh-Hans/abp/latest/Authorization)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [ABP](/jakeuj/Tags?qq=ABP)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
