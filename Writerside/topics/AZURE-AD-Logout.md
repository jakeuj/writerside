# AZURE AD Logout

> **原文發布日期:** 2021-09-28
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/09/28/AZURE-AD-OIDC-Logout
> **標籤:** 無

---

筆記下 AAD 與 **OpenID Connect  (OIDC)** 的登出相關操作

## 結論

到 <https://your.domain/.well-known/openid-configuration>

找 end\_session\_endpoint 的網址

就可以登出了

---

OIDC (**OpenID Connect**)

OpenID Connect (OIDC) 是建置於 OAuth 2.0 的驗證通訊協定，可用來安全地將使用者登入應用程式。

當您使用 Microsoft 身分識別平臺的 OpenID Connect 執行時，可以將登入及 API 存取新增至您的應用程式。

### 註釋

如果你或第三方驗證使用OAuth流程並使用OIDC協定，那就跟Oauth依樣會有一些統一個規範，方便導入到支援 OIDC的 Application 中。

比如你開發的系統符合 OIDC，那你網站就會有一份 .well-known/openid-configuration ，沒意外可能在根目錄

Example: <https://app.azurewebsites.net/.well-known/openid-configuration>

再來依照 OIDC 的規範，該文件內描述了登入/登出相關的一些資訊，端點位置…ECT.

其中 end\_session\_endpoint 這個端點就是用來登出應用程式的

### 流程

假設我有一個前端網站 (A) 和一個 Identity Server 4 登入驗證網站 (B)，登入使用 AAD (C)

那前端 (A) 要登出時需要依照我們登入驗證網站 (B) 的描述檔 .well-known/openid-configuration

取得 end\_session\_endpoint 內指定網址並進行呼叫來開始登出

此時 (B) 需要再使用 AAD (C) 的 .well-known/openid-configuration => end\_session\_endpoint 來進行登出

### 例如

<https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration>

裡面可以找到 "end\_session\_endpoint": "<https://login.microsoftonline.com/common/oauth2/v2.0/logout>"

所以登出網址就是 <https://login.microsoftonline.com/common/oauth2/v2.0/logout>

### 範例

```
GET https://login.microsoftonline.com/common/oauth2/v2.0/logout?post_logout_redirect_uri=http%3A%2F%2Flocalhost%2Fmyapp%2F
```

其中 `post_logout_redirect_uri` 是登出後跳轉的地址，必須包含在你設定的 Oauth 回傳網址清單中

### 參照

[Microsoft 身分識別平台和 OpenID Connect 通訊協定 - Microsoft identity platform | Microsoft Docs](https://docs.microsoft.com/zh-tw/azure/active-directory/develop/v2-protocols-oidc#send-a-sign-out-request)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Azure AD
{ignore-vars="true"}

* 回首頁

---

*本文章從點部落遷移至 Writerside*
