# DbMigrator app settings environmentVariables

DbMigrator 預設其實是可以直接吃到不同環境的 appsettings.json 設定檔的，只要在啟動時指定環境變數即可。

但這邊要注意因為該專案不是 AspDotNet 專案，而是 Console 專案，

所以要特別注意環境變數是吃 DOTNET_ENVIRONMENT 而不是 ASPNETCORE_ENVIRONMENT。

```bash
# Windows
set DOTNET_ENVIRONMENT=Development
# Linux
export DOTNET_ENVIRONMENT=Development
```

## csproj
我複製了一份 appsettings.json 並命名為 appsettings.Dev.json，但這樣的話在 publish 時該檔案不會被複製到 publish 資料夾中。

所以在 csproj 中把自動產生的 Content Update 改成 Include，讓該檔案在 publish 時一併複製到 publish 資料夾中。

```
<None Remove="appsettings.Dev.json" />
<Content Include="appsettings.Dev.json">
  <CopyToPublishDirectory>PreserveNewest</CopyToPublishDirectory>
  <CopyToOutputDirectory>Always</CopyToOutputDirectory>
</Content>
```

## launchSettings
建立 Properties/launchSettings.json 檔案，
並在 launchSettings.json 中加入環境變數的設定，
這樣在 Rider 中執行時就會帶入該環墖變數。

```json
{
  "profiles": {
    "BookStore.DbMigrator": {
      "commandName": "Project",
      "environmentVariables": {
        "DOTNET_ENVIRONMENT": "Development"
      }
    },
    "BookStore.DbMigrator.Dev": {
      "commandName": "Project",
      "environmentVariables": {
        "DOTNET_ENVIRONMENT": "Dev"
      }
    }
  }
}
```

![launchSettings.png](launchSettings.png)

這樣就可以在不同環境下使用不同的設定檔了。

![run-proj.png](run-proj.png)