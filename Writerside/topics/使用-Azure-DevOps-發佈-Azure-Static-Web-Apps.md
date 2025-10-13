# 使用 Azure DevOps 發佈 Azure Static Web Apps

> **原文發布日期:** 2021-08-25
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/08/25/static-web-apps-publish-devops
> **標籤:** 無

---

新發現一個專門 for 前端的服務 Azure Static Web Apps

這邊以 Vue 筆記一下 Azure DevOps CI/CD 到該服務的流程

## VUE

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
      # routes_location: 'public/json'
      azure_static_web_apps_api_token: $(deployment_token)
```

## Blazor

```
# Starter pipeline
# Start with a minimal pipeline that you can customize to build and deploy your code.
# Add steps that build, run tests, deploy, and more:
# https://aka.ms/yaml

trigger:
  - develop

pool:
  vmImage: ubuntu-latest

steps:
  - checkout: self
    submodules: true
  - task: AzureStaticWebApp@0
    inputs:
      app_location: '/src/PlmAPI.Blazor'
      output_location: 'wwwroot'
      azure_static_web_apps_api_token: $(deployment_token)
```

Blazor 專案根目錄放 staticwebapp.config.json

```
{
  "navigationFallback": {
    "rewrite": "/index.html"
  }
}
```

## Angualr

```
# Node.js with Angular
# Build a Node.js project that uses Angular.
# Add steps that analyze code, save build artifacts, deploy, and more:
# https://docs.microsoft.com/azure/devops/pipelines/languages/javascript

trigger:
- master

pool:
  vmImage: ubuntu-latest

steps:
- task: AzureStaticWebApp@0
  inputs:
    app_location: '/'
    output_location: 'dist/MyApp'
    azure_static_web_apps_api_token: '$(deployment_token)'
    routes_location: '/'
```

注意：`output_location: 'dist/MyApp'`

2021/10/8

---

參照：[教學課程：使用 Azure DevOps 發佈 Azure 靜態 Web Apps | Microsoft Docs](https://docs.microsoft.com/zh-tw/azure/static-web-apps/publish-devops)

## Step 1 建立靜態 Web 應用程式

首先到 Azure Portal 建立一個新的 靜態 Web 應用程式

Git 來源選 Other 稍後自行設定使用 DevOps 部屬

建立完後 概觀 (上方) 管理部署權杖 複製 部署權杖 稍後會用到

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/0f3596f6-4d67-40c9-9a8c-1cc2c02fdad3/1629884840.png)

## Step 2 準備 Vue 專案 Git Repo

建立自己的前端應用，我這邊是用 Vue 建了一個預設專案

然後到 Devops 建立一個測試專案的 Git Repo

把手上的前端原始碼 push 上去

## Step 3 建立 DevOps CI/CD

在 Repo 右上角可以按 set build pipeline

也可以到 pipeline 按新增

然後搜尋 static 會找到一個範本

輸入以下參數

```
app_location: '/'
output_location: 'dist'
azure_static_web_apps_api_token: $(deployment_token)
```

會自動生成以下內容

azure-pipelines.yml

```
trigger:
- main

pool:
  vmImage: ubuntu-latest

steps:
  - checkout: self
    submodules: true
  - task: AzureStaticWebApp@0
    inputs:
      app_location: '/'
      output_location: 'dist'
      azure_static_web_apps_api_token: $(deployment_token)
```

這邊必須右上角設定環境變數 `deployment_token` 把 Azure Static Web Apps 的發布權杖密碼設定進去

說明一下參數

* `app_location` => 程式原始碼所在目錄 ex: /app
* `output_location` => 編譯完後的靜態網頁相對於app的路徑 ex: dist
  例如：`app_location` + `output_location` = /app/dist
  也就是最後部屬時會把這路徑裡面的東西拿去打包 (ZIP) 並上傳
* `azure_static_web_apps_api_token` 就 Azure 那邊應用的發布權杖
  因為這邊實際上會在 git repo 建立 yml 檔案，所以為了安全性建議使用環境變數 `$(deployment_token)`
* App Build Command => 預設是 npm run build, 有需要可以使用自己的指令
* Routes Location => routes.json 的位置，如果不是用 hash route 需要設定轉址，
  則需要建立並指定該設定檔(routes.json)位置，
  參照 [Configure Azure Static Web Apps | Microsoft Learn](https://learn.microsoft.com/en-us/azure/static-web-apps/configuration#example-configuration-file)
  routes.json

```
{
  "routes": [
    {
      "route": "/*",
      "serve": "/index.html",
      "statusCode": 200
    }
  ]
}
```

* skip\_app\_build => 上面自訂 build 不夠可以直接略過這裡 build，但這就要在這個 task 之前先打包好放到 dist 資料夾
  這時候可以設定 `app_location`=/app/dist ,`output_location` 不要設定或留空白, skip\_app\_build = true
  大概會長以下這樣，其中 `script` 的部分就可以自己多打幾行？

```
trigger:
- main

pool:
  vmImage: ubuntu-latest

steps:
- task: NodeTool@0
  inputs:
    versionSpec: '10.x'
  displayName: 'Install Node.js'

- script: |
    npm install
    npm run build
  displayName: 'npm install and build'

- task: AzureStaticWebApp@0
  inputs:
    app_location: '/dist'
    skip_app_build: true
    azure_static_web_apps_api_token: '$(deployment_token)'
```

存檔之後就會觸發 CI/CD, 可以到 azure 提供的 app url 看到自己的網站，之後只要 psuh 到 main 就會自動 build & publish

## 簡介

[什麼是 Azure Static Web Apps？ | Microsoft Docs](https://docs.microsoft.com/zh-tw/azure/static-web-apps/overview#key-features)

## **主要功能**

* **Web 裝載**，適用於像是 HTML、CSS、JavaScript 與影像等靜態內容。
* Azure Functions 提供的 **整合式 API** 支援，以及使用標準帳戶連結現有 Azure Functions 應用程式的選項。
* **卓越的 GitHub 與 Azure DevOps 整合**，其中存放庫變更會觸發建置和部署。
* **全域散發** 靜態內容，將內容放在更接近使用者的範圍。
* **免費的 SSL 憑證**，會自動更新。
* **自訂網域**，為您的應用程式提供品牌的自訂。
* **無縫安全性模型**，會在呼叫 API 時使用反向 Proxy，這不需要 CORS 設定。
* Azure Active Directory、GitHub 和 Twitter 的 **驗證提供者** 整合。
* **可自訂的授權角色定義** 和指派。
* **後端路由規則** 能夠完全控制您所提供的內容和路由。
* **產生的暫存版本**，由提取要求提供支援，讓您的網站在發佈前先啟用預覽版本。

## **如何使用 Static Web Apps**

* **建置新式 Web 應用程式**，使用像是 [Angular](https://docs.microsoft.com/zh-tw/azure/static-web-apps/getting-started?tabs=angular)、[React](https://docs.microsoft.com/zh-tw/azure/static-web-apps/getting-started?tabs=react)、[Svelte](https://docs.microsoft.com/zh-tw/learn/modules/publish-app-service-static-web-app-api/)、[Vue](https://docs.microsoft.com/zh-tw/azure/static-web-apps/getting-started?tabs=vue) 的 JavaScript 架構和程式庫，或使用 [Blazor](https://docs.microsoft.com/zh-tw/azure/static-web-apps/deploy-blazor) 建立具有 [Azure Functions](https://docs.microsoft.com/zh-tw/azure/static-web-apps/apis) 後端的 WebAssembly 應用程式。
* **發佈靜態網站**，使用像是 [Gatsby](https://docs.microsoft.com/zh-tw/azure/static-web-apps/publish-gatsby)、[Hugo](https://docs.microsoft.com/zh-tw/azure/static-web-apps/publish-hugo)、[VuePress](https://docs.microsoft.com/zh-tw/azure/static-web-apps/publish-vuepress) 的架構。
* **部署 Web 應用程式**，使用像是 [Next.js](https://docs.microsoft.com/zh-tw/azure/static-web-apps/deploy-nextjs) 和 [Nuxt.js](https://docs.microsoft.com/zh-tw/azure/static-web-apps/deploy-nuxtjs) 的架構。

## 定價

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/0f3596f6-4d67-40c9-9a8c-1cc2c02fdad3/1629964907.png)
![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Angular](/jakeuj/Tags?qq=Angular)
* [Azure](/jakeuj/Tags?qq=Azure)
* [Blazor](/jakeuj/Tags?qq=Blazor)
* [CI/CD](/jakeuj/Tags?qq=CI%2FCD)
{ignore-vars="true"}
* [DevOps](/jakeuj/Tags?qq=DevOps)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
