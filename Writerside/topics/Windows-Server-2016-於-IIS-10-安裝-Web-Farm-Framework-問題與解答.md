# Windows Server 2016 於 IIS 10 安裝  Web Farm Framework 問題與解答

> **原文發布日期:** 2016-01-14
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2016/01/14/wff
> **標籤:** 無

---

Windows Server 2016 install Web Farm Framework got an error that "iis version 7.0 or greater is required to install Web Farm Framework 2.2"

依照官方安裝步驟於Windos Server 2016時會遭遇無法正常安裝的問題

主要是 Windos Server 2016 使用 IIS 10 而 WFF 安裝時檢測 IIS版本時過不了

他會認為 IIS 的版本不滿足最低需求 IIS 7 以上

所以可行的方法是於安裝時暫時修改登陸檔的IIS版本資訊騙過 WFF 安裝程式

安裝完成後再修改回來

目前於 Windos Server 2016 預覽版 第四版 中文系統 中

發現 安裝 UrlRewrite 2.0 也有相同情形出現

預計升級到 Windos Server 2016 之後會有不少相依於IIS版本的套件

都有可能出現類似情形

可能可以嘗試採用相同方式處理看看

至於會不會有衍伸問題

就需要各位在自己後續進行追蹤檢測了

以下是修改登陸檔的位置與步驟

Try changing the registry setting  install the module and change the registry back to the original value.

1. Open Regedit > HKEY\_LOCAL\_MACHINE\SOFTWARE\Microsoft\InetStp
2. Edit "MajorVersion" and set the "DECIMAL" value to 9
3. Hit F5 while in Regedit
4. Now go install the WebFarm 2.2 module.
5. Change the "MajorVersion" back to "DECIMAL" value of 10
6. Hit F5 while in Regedit
7. Close Regedit

It is a kind of work around also I suggest you to make a back up of full registry before changing.

以下是我用破英文去找問題的原文

Before installing Web Farm Framework 2.2, you need to install the following prerequisites:

* [Web Platform Installer 3.0](http://www.microsoft.com/en-us/download/details.aspx?id=6164)
* [WebDeploy 2.0](http://www.microsoft.com/en-us/download/details.aspx?id=25230)

To download and install Web Farm Framework 2.2, click on the link for your server type:

* English: [x86](http://download.microsoft.com/download/F/E/2/FE2E2E07-22B5-4875-9A36-8B778D157F91/WebFarm2_x86.msi) / [x64](http://download.microsoft.com/download/F/E/2/FE2E2E07-22B5-4875-9A36-8B778D157F91/WebFarm2_x64.msi)

But I got an error message "iis version 7.0 or greater is required to install Web Farm Framework 2.2".

My question is that does Web Farm Framework 2.2 still support IIS 10?

[![Microsoft Web Farm Framework Error](http://i.imgur.com/8qsbLoK.png)](http://www.microsoft.com/en-us/download/details.aspx?id=6164)

這次的新版Server可能會遭遇更多以往更新系統所遇到的更多問題

升級正式環境之前請各位先於開發測試環境好好測試原本的系統是否可以正常運作

以上

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* IIS
* Server

* 回首頁

---

*本文章從點部落遷移至 Writerside*
