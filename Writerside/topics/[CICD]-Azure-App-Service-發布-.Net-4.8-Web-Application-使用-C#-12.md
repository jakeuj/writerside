# [CI/CD] Azure App Service 發布 .Net 4.8 Web Application 使用 C# 12

> **原文發布日期:** 2023-12-25
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/12/25/Azure-App-Service-DevOps-deploy-ps1
> **標籤:** 無

---

舊專案預設只能用 C# 6 語法，用新語法部署一直不支援，最後終於可以字串插值啦！

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/d07efac4-7211-458d-943c-27e59ce4c15c/1703484955.png.png)

## 結論

以 `NewSRM.sln` 專案為例，方案根目錄加入以下兩個檔案

.deployment

```
[config]
command = powershell -NoProfile -NoLogo -ExecutionPolicy Unrestricted -Command "& "$pwd\deploy.ps1" 2>&1 | echo"
```

deploy.ps1

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

# if ($MSBUILD_PATH -eq $null) {
  $MSBUILD_PATH = "${env:ProgramFiles(x86)}\MSBuilds\17.8.6\MSBuild\Current\Bin\MSBuild.exe"
# }

##################################################################################################################################
# Deployment
# ----------

echo "Handling .NET Web Application deployment."

# 1. Restore NuGet packages
if (Test-Path "NewSRM.sln") {
  nuget restore "$DEPLOYMENT_SOURCE\NewSRM.sln"
  exitWithMessageOnError "NuGet restore failed"
}

# 2. Build to the temporary path
if ($env:IN_PLACE_DEPLOYMENT -ne "1") {
  & "$MSBUILD_PATH" "$DEPLOYMENT_SOURCE\NewSRM\NewSRM.csproj" /nologo /verbosity:m /t:Build /t:pipelinePreDeployCopyAllFilesToOneFolder /p:_PackageTempDir="$DEPLOYMENT_TEMP"`;AutoParameterizationWebConfigConnectionStrings=false`;Configuration=Release`;UseSharedCompilation=false /p:SolutionDir="$DEPLOYMENT_SOURCE\.\\" $env:SCM_BUILD_ARGS
} else {
  & "$MSBUILD_PATH" "$DEPLOYMENT_SOURCE\NewSRM\NewSRM.csproj" /nologo /verbosity:m /t:Build /p:AutoParameterizationWebConfigConnectionStrings=false`;Configuration=Release`;UseSharedCompilation=false /p:SolutionDir="$DEPLOYMENT_SOURCE\.\\" $env:SCM_BUILD_ARGS
}

exitWithMessageOnError "MSBuild failed"

# 3. KuduSync
if ($env:IN_PLACE_DEPLOYMENT -ne "1") {
  & $KUDU_SYNC_CMD -v 50 -f "$DEPLOYMENT_TEMP" -t "$DEPLOYMENT_TARGET" -n "$NEXT_MANIFEST_PATH" -p "$PREVIOUS_MANIFEST_PATH" -i ".git;.hg;.deployment;deploy.ps1"
  exitWithMessageOnError "Kudu Sync failed"
}

##################################################################################################################################
echo "Finished successfully."
```

其中 `NewSRM.sln` 為方案名稱，須改為自己的專案名字。

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/d07efac4-7211-458d-943c-27e59ce4c15c/1703485008.png.png)

## 步驟

```
kuduscript -y --aspWAP .\NewSRM\NewSRM.csproj -s .\NewSRM.sln -t posh
```

1. 將原本 MSBuild 14 改成新 MSBuild 17
   * MSBuild\14.0\Bin\MSBuild.exe
   * MSBuilds\17.8.6\MSBuild\Current\Bin\MSBuild.exe
2. `MSBUILD_PATH`
   * `$MSBUILD_PATH = "${env:ProgramFiles(x86)}\MSBuilds\17.8.6\MSBuild\Current\Bin\MSBuild.exe"`
   * 這樣才有 roslyn 的 csc.exe 可以編譯 C# 7以上語法
3. 註解 `if ($MSBUILD_PATH -eq $null) { }`
   * 強制更新路徑變數
   * 查看路徑是否正確 `echo $MSBUILD_PATH`

## 備註

.csproj

```
<LangVersion>Default</LangVersion>
```

web.config

```
<compiler
        language="c#;cs;csharp"
        extension=".cs"
        warningLevel="4"
        compilerOptions="/langversion:latest /nowarn:1659;1699;1701;612;618"
        type="Microsoft.CodeDom.Providers.DotNetCompilerPlatform.CSharpCodeProvider, Microsoft.CodeDom.Providers.DotNetCompilerPlatform, Version=4.1.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35" />
```

## 延伸閱讀

[神祕的ASP.NET bin\roslyn目錄-黑暗執行緒 (darkthread.net)](https://blog.darkthread.net/blog/aspnet-bin-roslyn-folder/)

## 參照

[ABP.IO Azure App Service 解決 Could not find the bundle file '/libs/abp/core/abp.css' | 御用小本本 - 點部落 (dotblogs.com.tw)](https://dotblogs.com.tw/jakeuj/2023/12/06/abp-Azure-App-Service-DevOps-deploy-cmd)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [App Service](/jakeuj/Tags?qq=App%20Service)
{ignore-vars="true"}

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
