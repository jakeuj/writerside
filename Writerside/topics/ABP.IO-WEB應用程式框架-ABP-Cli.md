# ABP.IO WEB應用程式框架 ABP Cli

> **原文發布日期:** 2021-11-26
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/11/26/Abp-Cli
> **標籤:** 無

---

搬運一下 abp cli 的指令

安裝

`dotnet tool install -g Volo.Abp.Cli`

更新

`dotnet tool update -g Volo.Abp.Cli`

```
❯ dotnet tool update -g Volo.Abp.Cli --version "*-rc*"
已成功將工具 'volo.abp.cli' 從 '6.0.1' 版更新為 '7.0.0-rc.1' 版。
```

建立專案

`abp new WillProj -v 6.0.3`

```
❯ abp new EuOrder --ui none -csf --preview
[15:20:44 INF] ABP CLI (https://abp.io)
[15:20:45 INF] Creating your project...
[15:20:45 INF] Project name: Test
[15:20:45 INF] Preview: yes
[15:20:45 INF] UI Framework: None
[15:20:45 INF] Output folder: D:\repos\Test
[15:21:18 INF] Downloading template: app, version: 7.0.0-rc.1
```

建立 Angular 專案

`abp new MyProject -u angular --separate-identity-server --preview`

安裝指定版本專案

```
dotnet tool uninstall -g volo.abp.cli
dotnet tool install -g volo.abp.cli --version "5.0.*"
abp new Test501B -u blazor --separate-identity-server --version 5.0.1 -csf
```

參照

[CLI | Documentation Center | ABP.IO](https://docs.abp.io/zh-Hans/abp/latest/CLI)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ABP
* Angular

* 回首頁

---

*本文章從點部落遷移至 Writerside*
