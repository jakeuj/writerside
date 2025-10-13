# Azure 持續部署 (CI/CD) 至 Azure App Service (DevOps Git Repo 替代方案)

> **原文發布日期:** 2021-08-30
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/08/30/AzureDevOpsGitRepoCiCdAppService
> **標籤:** 無

---

筆記下 Azure   App Service 部屬設定 DevOps 時找不到帳號的替代方案

## 2021/9/1

部屬失敗看了一下紀錄是 TimeOut

可以到 App Service Setting 加入以下設定

SCM\_COMMAND\_IDLE\_TIMEOUT = 3600

增加 Build 的逾時時間，單位為：秒

---

## 結論

於 App Service 部屬時選擇 其他Git

輸入 DevOps 的位置 去掉開頭的 xxxxxx@ 字段

Example: <https://dev.azure.com/jakeuj/TestCiCd/_git/TestCiCd>

帳號密碼到 DevOps 右上角 Clone 裡面產生帳號密碼貼到 App Service CI/CD

## 參照

[設定連續部署 - Azure App Service | Microsoft Docs](https://docs.microsoft.com/zh-tw/azure/app-service/deploy-continuous-deployment?tabs=repos)

## 補充

如果你在 App Service 自動部屬時選擇 DevOps 可以直接找到 Repo

那就照教學文件流程直接選就好了

這篇主要是針對某種原因找不到 Repo 的處理方式

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [App Service](/jakeuj/Tags?qq=App%20Service)
{ignore-vars="true"}
* [Azure](/jakeuj/Tags?qq=Azure)
* [CI/CD](/jakeuj/Tags?qq=CI%2FCD)
{ignore-vars="true"}

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
