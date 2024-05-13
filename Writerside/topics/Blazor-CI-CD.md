# Blazor CI/CD

紀錄一下 Blazor 的 CI/CD 設定。

## Yml

基本設定如下：

```yaml
trigger:
  - blazor/main

pool:
  vmImage: ubuntu-latest

steps:
  - checkout: self
    submodules: true

  - task: AzureStaticWebApp@0
    inputs:
      app_location: '/src/MyProject.Blazor'
      output_location: 'wwwroot'
      azure_static_web_apps_api_token: $(deployment_token)
```

其中 `deployment_token` 是從 Azure Portal 取得的。
並需要設定到 DevOps 的 variable 中。

## 不同環境的 appsettings.json

如果想在 CI/CD 時根據不同環境 (正式/測試) 使用不同的 `appsettings.json`，可以透過以下方式設定：

```yaml
- task: Bash@3
  inputs:
    targetType: 'inline'
    script: |
      echo 'Copy appsettings.$(deployment_environment).json to wwwroot/appsettings.json'
      cp 'src/MyProject.Blazor/wwwroot/appsettings.$(deployment_environment).json' '$(build.sourcesdirectory)/src/MyProject.Blazor/wwwroot/appsettings.json' -rf
```

其中 `deployment_environment` 是從 DevOps 的 variable 中取得。

需要設定 `deployment_environment=Production` 到 variable 中。

## 發佈到不同環境

如果想要發佈到不同環境，可以透過以下方式設定：

```yaml
- task: AzureStaticWebApp@0
  inputs:
    app_location: '/src/MyProject.Blazor'
    output_location: 'wwwroot'
    azure_static_web_apps_api_token: $(deployment_token)
    deployment_environment: $(deployment_environment)
```

其中 `deployment_environment` 是從 DevOps 的 variable 中取得。

需要設定 `deployment_environment=Staging` 到 variable 中。

## Sample

```yaml
trigger:
  - blazor/staging

pool:
  vmImage: ubuntu-latest

steps:
  - checkout: self
    submodules: true

  - task: Bash@3
    inputs:
      targetType: 'inline'
      script: |
        echo 'Copy appsettings.$(deployment_environment).json to wwwroot/appsettings.json'
        cp 'src/MyProject.Blazor/wwwroot/appsettings.$(deployment_environment).json' '$(build.sourcesdirectory)/src/MyProject.Blazor/wwwroot/appsettings.json' -rf

  - task: AzureStaticWebApp@0
    inputs:
      app_location: '/src/MyProject.Blazor'
      output_location: 'wwwroot'
      azure_static_web_apps_api_token: $(deployment_token)
      deployment_environment: $(deployment_environment)
```

## 限制 IP

如果想要限制 Azure Static Web App 的存取 IP，

可以在 app_location 的根目錄下新增 `staticwebapp.config.json` 檔案，

並透過以下方式設定：

`/src/MyProject.Blazor/staticwebapp.config.json`
```JSON
{
  "networking": {
    "allowedIpRanges": [
      "10.0.0.0/24",
      "100.0.0.0/32",
      "192.168.100.0/22"
    ]
  },
  "navigationFallback": {
    "rewrite": "/index.html"
  }
}
```

[allowedIpRanges](https://learn.microsoft.com/zh-tw/azure/static-web-apps/configuration#networking)

## REF

[Deploy a Blazor WebAssembly app to Azure Static Web Apps](https://learn.microsoft.com/en-us/azure/static-web-apps/deploy-blazor)