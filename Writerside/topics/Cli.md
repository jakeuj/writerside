# Cli

8.2 版把部分功能鎖起來要付費 (所以沒事可以用 8.1.x 版？)

Example: --tiered

```
需要 團隊 或更高級別的許可證才能使用此選項。
Auth Server 專案作為一個單獨的專案並在不同的端點上運行。
它將身份驗證伺服器與 API 主機應用程式分開。
如果未指定，您將在伺服器端有一個端點。
```

## Dotnet

```Shell
winget install Microsoft.DotNet.SDK.8
```

## Install

```Shell
dotnet tool install -g Volo.Abp.Cli --version "8.1.*"
```

## Update

```Shell
dotnet tool update -g Volo.Abp.Cli --version "8.1.*"
```

## Usage

```Shell
abp new MyProject -v 8.1.5
```

## 比較不同的模板

```Shell
$project = "MyProject"
$version = "8.1.5"

abp new $project -v $version -u mvc -o m --tiered
abp new $project -v $version -u blazor-server -o bs --tiered
abp new $project -v $version -u angular -o a --separate-auth-server
abp new $project -v $version -u blazor -o b --separate-auth-server
abp new $project -v $version -u none -o n --separate-auth-server
```

### skip-installing-libs

單純看後端程式碼可以加上 -sib 跳過安裝客戶端軟體包，省去下載幾萬的檔案

```Shell
abp new $project -v $version -u mvc -o m --tiered -sib
```

## 專案名稱問題

不能是 ABP，也不能是 CompanyName.Abp

因為 template 會用最後的 Abp 來當作 Module 名稱

但是 Module 又會繼承 AbpModule

最後演變成

AbpModule.cs

`AbpModule : AbpModule`

然後會報錯

## Ref

- [Cli latest](https://docs.abp.io/en/abp/latest/CLI)
- [Cli 8.1](https://abp.io/docs/8.1/cli)
- [生成式範本](https://abp.io/get-started)
