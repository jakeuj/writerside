# Cli

8.2 版把部分功能鎖起來要付費 (所以沒事可以用 8.1 版？)

Example: --tiered
```
需要 團隊 或更高級別的許可證才能使用此選項。
Auth Server 專案作為一個單獨的專案並在不同的端點上運行。
它將身份驗證伺服器與 API 主機應用程式分開。
如果未指定，您將在伺服器端有一個端點。 
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
abp new MyProject
```

## Samples

```Shell
abp new Jake.Proj -t app-nolayers -dbms PostgreSQL --theme basic -csf 
```

```Shell
abp new Jake.Proj -u mvc --tiered --version 8.1.* -csf
```

## 專案名稱
不能是 ABP，也不能是 CompanyName.Abp

因為 template 會用最後的 Abp 來當作 Module 名稱

但是 Module 又會繼承 AbpModule

最後演變成

AbpModule.cs

`    AbpModule : AbpModule`

然後會報錯

## Ref
- [Cli latest](https://docs.abp.io/en/abp/latest/CLI)
- [Cli 8.1](https://abp.io/docs/8.1/cli)
- [生成式範本](https://abp.io/get-started)