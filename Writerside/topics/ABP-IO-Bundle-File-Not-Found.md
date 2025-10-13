# ABP.IO Could not find the bundle file &#x27;/libs/abp/core/abp.css&#x27; {id="ABP-IO-Bundle-File-Not-Found"}

> **原文發布日期:** 2022-07-21
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/07/21/abp-NPM-not-installed
> **標籤:** 無

---

Abp開新專案發生例外解決方案

## 結論

使用管理者權限開啟 PowerShell 執行以下 Script

```
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
npm install -g npm-windows-upgrade
npm-windows-upgrade
```

1. 以後使用 Abp Cli 新建專案就會正常
   `abp new {專案名稱}`
2. 或是在既有專案的 Web (Host) csproj 所在目錄重新執行安裝套件命令
   `abp install-libs`

## 例外訊息

`AbpException: Could not find the bundle file '/libs/abp/core/abp.css' for the bundle 'Lepton.Global'!`

![](https://support.abp.io/QA/files/998fe814606042e8e84e3a0471ff0106.png)

## 特徵

`abp new` 或 `abp install-libs` 時出現 NPM is not installed 警告訊息

![](https://user-images.githubusercontent.com/15319947/173512022-54ed085a-a088-4a9f-a44c-00ca9174b3bd.png)

## 參照

[NPM is not installed #3238 | Support Center | ABP Commercial](https://support.abp.io/QA/Questions/3238/NPM-is-not-installed)

[It warns NPM is not installed when run abp install-libs,but I have installed . · Issue #12995 · abpframework/abp (github.com)](https://github.com/abpframework/abp/issues/12995)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* NPM

* 回首頁

---

*本文章從點部落遷移至 Writerside*
