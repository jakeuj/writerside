# 阿里雲 RAM 使用筆記

> **原文發布日期:** 2021-05-06
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/05/06/AliRam
> **標籤:** 無

---

訪問控制RAM（Resource Access Management）

是阿里雲提供的一項管理用戶身份與資源訪問權限的服務。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/3e7e6c8c-484f-479b-a392-7f8d275f161b/1620290814.png)

0.前言

如果要讓其他開發人員到阿里雲上進行一些基本操作

應該遵循最小權限原則來降低資安風險

因此可以考慮採用RAM來建立個別帳號並賦予其所需最小權限

避免多人共用主帳號，出事也不知道是誰弄的窘境

因此下面將介紹一下 RAM 的操作流程~

1.建立用戶

先到 [訪問控制 RAM](https://ram.console.aliyun.com/) 頁面左側找到 用户 點進去 創建用戶

輸入帳號名稱，點下面添加用戶可以一次新增多個帳號

訪問方式選擇控制台訪問 (網頁登入操作阿里雲)

密碼可以自動生成並讓用戶之後登入時自己改密碼

(當然如果你只建立一個自己用的帳號可以直接打好密碼不要重置)

MFA 部分是使用 OTOP (Time-based One-Time Password)

可以透過 [Authy](https://authy.com) 或 [Google Authenticator](https://en.wikipedia.org/wiki/Google_Authenticator) 動態產生六位數驗證碼

在帳號密碼外洩時可以多一層認證保護，防止駭客入侵

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/3e7e6c8c-484f-479b-a392-7f8d275f161b/1620288420.png)

2.[创建用户组](https://ram.console.aliyun.com/groups)

一樣到 用户组 點進去 創建用戶組

阿里雲建議不要直接使用主帳號來操作阿里雲

所以可以先建立一個 Admin 用戶組 準備取代主帳號

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/3e7e6c8c-484f-479b-a392-7f8d275f161b/1620287369.jpg)

3.設定權限

到剛剛建立的用戶組右側 添加权限

這邊以建立管理者子帳號來取代原本主帳號為例

選擇 整個雲帳號 (預設值) 並加入以下權限

AdministratorAccess [管理所有阿里云资源的权限]

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/3e7e6c8c-484f-479b-a392-7f8d275f161b/1620288953.png)

如果要建立一般開發者權限 (非全域管理員)

可以再新建一個用戶組 (例如：WebPlus)

然後賦予對應權限

AliyunWebPlusFullAccess [管理Web应用托管服务(WebPlus)的权限]

這個權限可以進行 Web+ 的應用布署作業

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/3e7e6c8c-484f-479b-a392-7f8d275f161b/1620288963.png)

4.添加組成員

到剛剛建立的用戶組右側 添加組成員

將第一步建立好的 用戶 加入對應 用戶組

EX: admin => Admin , Jake => WebPlus

如此一來就可以開始在登入時改用 RAM 帳號 登入

https://signin.aliyun.com/domain.onaliyun.com/login.htm

Id=admin@domain.onaliyun.com, Pwd={自動生成密碼}

降低直接使用主帳號權限過高產生的安全疑慮

Id=jake@domain.onaliyun.com, Pwd={自動生成密碼}

除此之外還有一些選擇性的設定可以做調整

以下作為選擇性的補充

5.域名

回到 [訪問控制 RAM](https://ram.console.aliyun.com/) 頁面

右側找到 編輯默認域名

這邊原本可能是一串隨機長整數

在這可以編輯成自己的域名

比如 jakeuj

這樣以後在登入的時候可以改用以下帳號登入

[admin@jakeuj.onaliyun.com](mailto:admin@jakeuj.onaliyun.com)

(https://signin.aliyun.com/jakeuj.onaliyun.com/login.htm)

6.設置 密碼錯誤次數

到 [訪問控制 RAM](https://ram.console.aliyun.com/) 頁面左側找到 設置 > **密碼強度設置 密碼重試約束**

裡面有一些密碼跟安全設定可以做調整

這邊建議設定 密碼重試約束 一小時內只能幾次 (1~32)

預設 0 是不去擋密碼錯誤 比較容易被破解

雖然 MFA 還會在擋一層，但安全性不嫌高嘛

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/3e7e6c8c-484f-479b-a392-7f8d275f161b/1620290478.png)

7.設置 保存 MFA 狀態

同樣在 [訪問控制 RAM](https://ram.console.aliyun.com/) 設置 > 用戶安全設置 保存 MFA 登錄狀態7 天

這裡可以選擇要不要開啟這個功能，

MFA 認證過的瀏覽器一個禮拜內不用再每次輸入動態驗證碼

(Google 擴充套件也有提供 Authy 直接在電腦瀏覽器取得OTOP)

8.其他

其他設定就稍微自己看一下有沒有需要調整

比如 登錄掩碼設置

如果你固定在公司IP來操作

可以用這個來設定 IP 白名單

只有這些 IP 可以來登入阿里雲

忘記改域名也可以從這邊的高級設置來編輯域名

也提供 domain 別名 的功能可以自己視情況調整設定

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- 阿里雲
{ignore-vars="true"}
- 阿里雲
{ignore-vars="true"}

- 回首頁

---

*本文章從點部落遷移至 Writerside*
