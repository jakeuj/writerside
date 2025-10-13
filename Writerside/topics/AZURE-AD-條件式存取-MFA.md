# AZURE AD 條件式存取 MFA

> **原文發布日期:** 2021-09-10
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/09/10/azure-ad-conditional-access
> **標籤:** 無

---

AAD 有條件的要求特定使用者於特定應用必須使用二因素驗證

筆記一下流程還有踩坑紀錄

## 1.權限：具有條件式存取管理員權限的帳戶

企業應用程式：條件式存取

如果沒看到這東西，可能要從企業應用程式新建應用，再把原本專案轉移到這個應用 (重設CallbackUrl並更換AppId,Secret…ETC.)

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/0f457619-ba59-4083-ace3-2223a031d0e8/1631257188.png)

如果以上賊個按鈕是灰色的，那就要找管理員開權限

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/0f457619-ba59-4083-ace3-2223a031d0e8/1631256935.png)
> 我這邊是用我自己的Azure帳號先做測試
>
> 所以權限部分是全開的

## 2.Azure AD Premium

條件式存取需要有 Azure AD P1 以上授權

一般自己的 Azure 應該只有免費版

所以需要到 AAD > 安全性 > 上方會提示啟用 P2 試用

另外對於公司來說，如果有買 Office 365 企業版 (E3以上)

那也包含了 AAD Premium 授權

## 3.賦予使用者 AAD P1 授權

啟用 Azure AD Premium 後相關操作會發現還是不能使用

詢問微軟後說是要將 P1 授權至少給一個使用者

AZURE AD > User > 授權 > 工作分派 > Azure AD Premium

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/0f457619-ba59-4083-ace3-2223a031d0e8/1631257694.png)

※ P1 必須設定使用者的使用地區才能授權

AZURE AD > User > 個人資料 > 編輯 > 使用位置 > Taiwan

否則會收到錯誤：License cannot be assigned to a user without a usage location specified.

參照：[AZURE AD PREMIUM P2 License cannot be assigned to a user without a usage location specified.](https://www.dotblogs.com.tw/jakeuj/2021/09/10/AZURE-AD-PREMIUM-P2)

※ 一般登入 User 不用 P1 也可以設定 MFA

## 4.建立企業應用程式

應用程式註冊 > 新增註冊 => 好像不能

企業應用程式 > 新增應用程式 => 這會有條件式存取

5.設定條件式存取

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/0f457619-ba59-4083-ace3-2223a031d0e8/1631251665.png)

新增原則

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/0f457619-ba59-4083-ace3-2223a031d0e8/1631251881.png)

選擇目標使用者或群組

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/0f457619-ba59-4083-ace3-2223a031d0e8/1631251888.png)

選擇目標應用程式，如果是從應用程式裡面的條件存取點進來的，預設會選擇該應用

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/0f457619-ba59-4083-ace3-2223a031d0e8/1631251999.png)

這邊可以設定條件，比如：公司IP略過MFA或是台灣以外的地區才要MFA

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/0f457619-ba59-4083-ace3-2223a031d0e8/1632383342.png)

建立IP位置

上方搜尋 > Azure AD 具名位置 > +IP 範圍位置 > 標示為信任位置

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/0f457619-ba59-4083-ace3-2223a031d0e8/1632383373.png)

排除信任位置

然後就可以在 條件 > 位置 > 排除 > 選擇所有信任位置或選取剛剛建立的位置 (Ex: Offoce1)

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/0f457619-ba59-4083-ace3-2223a031d0e8/1631252009.png)

這邊可以設定一些限制，比如：登入時需要MFA

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/0f457619-ba59-4083-ace3-2223a031d0e8/1631251889.png)

最後可以設定 Session 相關，比如：6小時候需要重新登入

## 啟用原則

最後預設是報告，就只是看看影響範圍，實際上不會真的應用到登入，這邊看沒問題了話就要手動改成啟用，這條件才會發生作用。

## 測試

再來就用該帳號登入該應用程式看看會發生甚麼事

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/0f457619-ba59-4083-ace3-2223a031d0e8/1631252676.png)

登入時會卡住

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/0f457619-ba59-4083-ace3-2223a031d0e8/1631252695.png)

這邊可以選擇MFA方式

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/0f457619-ba59-4083-ace3-2223a031d0e8/1631253514.png)

可以改成用動態驗證碼或APP通知的方式進行2FA

這邊預設是可以用動態驗證碼或通知的方式進行2FA

但是啟用通知方式就只能使用 微軟驗證器

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/0f457619-ba59-4083-ace3-2223a031d0e8/1631253912.png)

這邊也可以選擇設定應用程式但不設定通知

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/0f457619-ba59-4083-ace3-2223a031d0e8/1631254082.png)

這樣就可以使用自己的驗證器來產生動態驗證碼

但也就沒有使用通知來允許登入的功能了

之後登入就會需要輸入動態驗證碼

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/0f457619-ba59-4083-ace3-2223a031d0e8/1631255137.png)

[Authy](https://authy.com/)

這邊安麗一個 APP 可以避免換手機時遺失驗證碼

[Authy | Two-factor Authentication (2FA) App & Guides](https://authy.com/)

有別於 Google 驗證器一旦重新安裝就會遺失全部已註冊的驗證碼

[Authy](https://authy.com/) 可以在 重裝App/重置手機/換新手機/電腦 取得已登陸之驗證碼

## MFA 設定

AAD > 安全性 > MFA > 其他雲端式 MFA 設定

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/0f457619-ba59-4083-ace3-2223a031d0e8/1631252949.png)

這裡面可以進行MFA相關設定

* 使用應用程式密碼而非帳號密碼進行登入
* IP白名單略過MFA
* 使用 手機/簡訊/APP通知/動態驗證碼 方式進行 MFA
* 設定通過MFA後一段時間內不用再次進行MFA驗證

## 延伸閱讀

AAD 的功能真的挺多的，剛接觸有種眼花撩亂的感覺

發現這邊可以讓限制使用者存取的應用自己申請存取權

並由指定人員核准

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/0f457619-ba59-4083-ace3-2223a031d0e8/1631265258.png)

感覺像是 google 共用文件沒權限的人員可以申請

然後寄一封進到你信箱看你要不要把他家到共用名單內

## 參照

[規劃 Azure Active Directory 條件式存取部署 | Microsoft Docs](https://docs.microsoft.com/zh-tw/azure/active-directory/conditional-access/plan-conditional-access)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Azure AD](/jakeuj/Tags?qq=Azure%20AD)
{ignore-vars="true"}
* [MFA](/jakeuj/Tags?qq=MFA)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
