# Azure Static Web Apps 設定 IP 限制

> **原文發布日期:** 2023-11-09
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/11/09/azure-static-web-apps-configuration-networking
> **標籤:** 無

---

筆記下前端自己設定允許特定 IP 訪問

## 簡介

Azure Static Web Apps 在 DevOps 的 CI/CD 會建立 pipeline 設定檔 azure-pipelines.yml

其中會指定 `app_location` 預設為根目錄 ('/')

而針對靜態網站本身的額外設定

則需要在上述指定目錄中的 staticwebapp.config.json 裡頭設定 `networking` 的 `allowedIpRanges`

## 範例

azure-pipelines.yml

```
trigger:
- master

pool:
  vmImage: ubuntu-latest

steps:
  - checkout: self
    submodules: true
  - task: AzureStaticWebApp@0
    inputs:
      app_location: '/'
      output_location: 'dist'
      app_build_command: 'npm run build'
      azure_static_web_apps_api_token: $(deployment_token)
```

staticwebapp.config.json

```
{
  "networking": {
    "allowedIpRanges": [
      "10.0.0.0/24",
      "100.0.0.0/32",
      "192.168.100.0/22"
    ]
  }
}
```

## 參照

[設定 Azure Static Web Apps | Microsoft Learn](https://learn.microsoft.com/zh-tw/azure/static-web-apps/configuration#networking)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- Azure Static Web Apps
{ignore-vars="true"}

- 回首頁

---

*本文章從點部落遷移至 Writerside*
