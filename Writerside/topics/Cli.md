# Cli

Start typing here...

## Install

```Shell
dotnet install tool -g Volo.Abp.Cli
```

## Update

```Shell
dotnet update tool -g Volo.Abp.Cli
```

## Usage

```Shell
abp new MyProject
```

## Samples

```Shell
abp new Jakeuj.TestProj -t app-nolayers -dbms PostgreSQL --theme basic -csf 
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
- [Cli](https://docs.abp.io/en/abp/latest/CLI)
- [生成式範本](https://abp.io/get-started)