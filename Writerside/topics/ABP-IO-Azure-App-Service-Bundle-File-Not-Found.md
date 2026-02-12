# ABP.IO Azure App Service 解決 Could not find the bundle file '/libs/abp/core/abp.css' {id="ABP-IO-Azure-App-Service-Bundle-File-Not-Found"}

> **原文發布日期:** 2023-12-06
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/12/06/abp-Azure-App-Service-DevOps-deploy-cmd
> **標籤:** 無

---

Azure App Service 部屬中心 (Azure DevOps Repos) 自定義 .deployment 安裝 ABP CLI

執行 abp install-libs 以解決錯誤 `Could not find the bundle file '/libs/abp/core/abp.css'`

## 坑

Powershell Script 中的 `"%DEPLOYMENT_TEMP%"` 最終會變成 `ÞPLOYMENT_TEMP%` 目錄，必須改成 `"$DEPLOYMENT_TEMP"`
{ignore-vars="true"}

## 結論

設定 Azure App Service 組態，[指定 Node.js 版本](https://stackoverflow.com/questions/45515421/which-versions-of-node-js-are-available-on-azure-web-sites) (Yarn 需要 4.0 以上)：`WEBSITE_NODE_DEFAULT_VERSION=18.20.4`

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/0c5b0fc6-b26a-4129-9682-fc4e37f3bb9f/1701856246.png.png)

於方案目錄新增以下部署設定檔 `.deployment` `deploy.ps1`

.deployment

```
[config]
command = powershell -NoProfile -NoLogo -ExecutionPolicy Unrestricted -Command "& "$pwd\deploy.ps1" 2>&1 | echo"
```

[deploy.ps1](https://github.com/jakeuj/AbpAzureSample/blob/main/deploy.ps1)

```
# ----------------------
# KUDU Deployment Script
# Version: 1.0.17
# ----------------------

# Helpers
# -------

function exitWithMessageOnError($1) {
  if ($? -eq $false) {
    echo "An error has occurred during web site deployment."
    echo $1
    exit 1
  }
}

# Prerequisites
# -------------

# Verify node.js installed
where.exe node 2> $null > $null
exitWithMessageOnError "Missing node.js executable, please install node.js, if already installed make sure it can be reached from current environment."

# Setup
# -----

$SCRIPT_DIR = $PSScriptRoot
$ARTIFACTS = "$SCRIPT_DIR\..\artifacts"

$KUDU_SYNC_CMD = $env:KUDU_SYNC_CMD

$DEPLOYMENT_SOURCE = $env:DEPLOYMENT_SOURCE
$DEPLOYMENT_TARGET = $env:DEPLOYMENT_TARGET

$NEXT_MANIFEST_PATH = $env:NEXT_MANIFEST_PATH
$PREVIOUS_MANIFEST_PATH = $env:PREVIOUS_MANIFEST_PATH

if ($DEPLOYMENT_SOURCE -eq $null) {
  $DEPLOYMENT_SOURCE = $SCRIPT_DIR
}

if ($DEPLOYMENT_TARGET -eq $null) {
  $DEPLOYMENT_TARGET = "$ARTIFACTS\wwwroot"
}

if ($NEXT_MANIFEST_PATH -eq $null) {
  $NEXT_MANIFEST_PATH = "$ARTIFACTS\manifest"

  if ($PREVIOUS_MANIFEST_PATH -eq $null) {
    $PREVIOUS_MANIFEST_PATH = $NEXT_MANIFEST_PATH
  }
}

if ($KUDU_SYNC_CMD -eq $null) {
  # Install kudu sync
  echo "Installing Kudu Sync"
  npm install kudusync -g --silent
  exitWithMessageOnError "npm failed"

  # Locally just running "kuduSync" would also work
  $KUDU_SYNC_CMD = "$env:APPDATA\npm\kuduSync.cmd"
}

$DEPLOYMENT_TEMP = $env:DEPLOYMENT_TEMP
$MSBUILD_PATH = $env:MSBUILD_PATH

if ($DEPLOYMENT_TEMP -eq $null) {
  $DEPLOYMENT_TEMP = "$env:temp\___deployTemp$env:random"
  $CLEAN_LOCAL_DEPLOYMENT_TEMP = $true
}

if ($CLEAN_LOCAL_DEPLOYMENT_TEMP -eq $true) {
  if (Test-Path $DEPLOYMENT_TEMP) {
    rd -Path $DEPLOYMENT_TEMP -Recurse -Force
  }
  mkdir "$DEPLOYMENT_TEMP"
}

if ($MSBUILD_PATH -eq $null) {
  $MSBUILD_PATH = "${env:ProgramFiles(x86)}\MSBuild\14.0\Bin\MSBuild.exe"
}

##################################################################################################################################
# Deployment
# ----------

echo "Handling ABP Libs install."

# Install Yarn
echo "Installing Yarn"
npm install yarn -g --silent

# Install ABP CLI
echo "Installing ABP CLI"
dotnet tool update -g Volo.Abp.Cli --prerelease
# Locally just running "abp" would also work
$env:Path += "$env:USERPROFILE\.dotnet\tools\;"

# Install ABP Libs
echo "Installing ABP Libs"
abp install-libs -wd "$DEPLOYMENT_SOURCE\src/TestCiCd.HttpApi.Host"

echo "Handling ASP.NET Core Web Application deployment."

# 1. Restore nuget packages
dotnet restore "$DEPLOYMENT_SOURCE\TestCiCd.sln"
exitWithMessageOnError "Restore failed"

# 2. Build and publish
dotnet publish "$DEPLOYMENT_SOURCE\src/TestCiCd.HttpApi.Host/TestCiCd.HttpApi.Host.csproj" --output "$DEPLOYMENT_TEMP" --configuration Release
exitWithMessageOnError "dotnet publish failed"

# 3. KuduSync
& $KUDU_SYNC_CMD -v 50 -f "$DEPLOYMENT_TEMP" -t "$DEPLOYMENT_TARGET" -n "$NEXT_MANIFEST_PATH" -p "$PREVIOUS_MANIFEST_PATH" -i ".git;.hg;.deployment;deploy.ps1"
exitWithMessageOnError "Kudu Sync failed"

##################################################################################################################################
echo "Finished successfully."
```

最後將上面腳本中的 `TestCiCd` 改成實際的方案名稱

## 範例

[jakeuj/AbpAzureSample (github.com)](https://github.com/jakeuj/AbpAzureSample)

## 詳細步驟

1. 參照 Azure App Service 自訂部署文檔
   [自訂部署文稿 ·projectkudu/kudu 維基 (github.com)](https://github.com/projectkudu/kudu/wiki/Custom-Deployment-Script#custom-deployment-script-generator)
2. 安裝 node.js
3. 安裝 kuduscript
   `npm install kuduscript -g`
4. 生成專案部署腳本
   `kuduscript -y --aspNetCore .\src\TestCiCd.HttpApi.Host\TestCiCd.HttpApi.Host.csproj -s .\TestCiCd.sln -t posh`
5. 修改自動生成的部署腳本 `deploy.ps1`中的 `Deployment` 區塊
   1. `dotnet publish` 的 `"%DEPLOYMENT_TEMP%"` 必須改成 `"$DEPLOYMENT_TEMP"` 否則會輸出到 `ÞPLOYMENT_TEMP%` 導致最後產生空的網站！
   {ignore-vars="true"}
   2. 加入代碼來安裝並執行 `abp install-libs` 以產生缺少的靜態資源，例如： `/libs/abp/core/abp.css` …ETC.

```
##################################################################################################################################
# Deployment
# ----------

echo "Handling ABP Libs install."

# Install Yarn
echo "Installing Yarn"
npm install yarn -g --silent

# Install ABP CLI
echo "Installing ABP CLI"
dotnet tool update -g Volo.Abp.Cli --prerelease
# Locally just running "abp" would also work
$env:Path += "$env:USERPROFILE\.dotnet\tools\;"

# Install ABP Libs
echo "Installing ABP Libs"
abp install-libs -wd "$DEPLOYMENT_SOURCE\src/TestCiCd.HttpApi.Host"

echo "Handling ASP.NET Core Web Application deployment."

# 1. Restore nuget packages
dotnet restore "$DEPLOYMENT_SOURCE\TestCiCd.sln"
exitWithMessageOnError "Restore failed"

# 2. Build and publish
dotnet publish "$DEPLOYMENT_SOURCE\src/TestCiCd.HttpApi.Host/TestCiCd.HttpApi.Host.csproj" --output "$DEPLOYMENT_TEMP" --configuration Release
```

※ 其中 `dotnet publish` 的 `"%DEPLOYMENT_TEMP%"` 改成 `"$DEPLOYMENT_TEMP"`
{ignore-vars="true"}

`kuduscript -y --aspNetCore .\src\TestCiCd.HttpApi.Host\TestCiCd.HttpApi.Host.csproj -s .\TestCiCd.sln -t posh`

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/0c5b0fc6-b26a-4129-9682-fc4e37f3bb9f/1701917408.png.png)

`.deployment` & `deploy.ps1`

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/0c5b0fc6-b26a-4129-9682-fc4e37f3bb9f/1701917442.png.png)

最後 Git Commit & Push 觸發 CI/CD

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/0c5b0fc6-b26a-4129-9682-fc4e37f3bb9f/1701936565.png.png)

## 備註

[ABP.IO Could not find the bundle file '/libs/abp/core/abp.css' | 御用小本本 - 點部落 (dotblogs.com.tw)](https://dotblogs.com.tw/jakeuj/2022/07/21/abp-NPM-not-installed)

至此已解決錯誤 `Could not find the bundle file '/libs/abp/core/abp.css'`

但注意還需要將網站網址加到 OpenIddictApplications 資料表的 RedirectUris 欄位中才能正常開出登入頁面

["https://localhost:44346/swagger/oauth2-redirect.html","https://cicd-jakeuj.azurewebsites.net/swagger/oauth2-redirect.html"]

至於另一個錯誤 `CryptographicException: Access is denied`

非免費層級 App Service Plan 可以在組態中加入  [WEBSITE\_LOAD\_USER\_PROFILE=1](https://dotblogs.azurewebsites.net/jakeuj/2022/10/13/OpenIddict-WindowsCryptographicException-Access-is-denied) 的設定

否則請參考以下文章修改程式碼

[ABP.IO WEB應用程式框架 Azure App Service CI/CD deployment | 御用小本本 - 點部落 (dotblogs.com.tw)](https://dotblogs.com.tw/jakeuj/2022/10/21/abp-Azure-App-Service-Github-CICD)

其他應注意的還有 Self, CORS, Auth Urls…等網址需要改成對應發布後的前後端網址

另外就是預設的 Admin 密碼記得上線前要修改一下，不然可能會有可怕的事情發生！

## 參照

[Configure continuous deployment - Azure App Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/app-service/deploy-continuous-deployment?tabs=repos#prepare-your-repository)

[node.js - Azure NodeJS version - Stack Overflow](https://stackoverflow.com/questions/54034084/azure-nodejs-version)

[Which versions of node.js are available on Azure Web Sites? - Stack Overflow](https://stackoverflow.com/questions/45515421/which-versions-of-node-js-are-available-on-azure-web-sites)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- ABP
- App Service
{ignore-vars="true"}
- Azure
- CI/CD
{ignore-vars="true"}
- DevOps

- 回首頁

---

*本文章從點部落遷移至 Writerside*
