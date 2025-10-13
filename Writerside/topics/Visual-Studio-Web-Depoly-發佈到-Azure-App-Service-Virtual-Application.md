# Visual Studio Web Depoly 發佈到 Azure App Service Virtual Application

> **原文發布日期:** 2021-08-16
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/08/16/VsDepolyVirtualApplication
> **標籤:** 無

---

筆記下怎麼透過修改自動生成的 pubxml 達到發佈到指定虛擬應用程式

首先要先到 Azure App Service 建立虛擬應用程式的路徑

虛擬路徑 (網址後面的路徑)

範例：/test

實體路徑 (windows放檔案的路徑)

範例：site\test

記得儲存！

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/5c9f8a59-8d4d-48b4-8696-0e10967be384/1629095767.png)

VS 對著專案按右鍵選"發佈"

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/5c9f8a59-8d4d-48b4-8696-0e10967be384/1629095883.png)

選 Azure

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/5c9f8a59-8d4d-48b4-8696-0e10967be384/1629095924.png)

選你要發佈的 App Service

如果想發佈完直接打開 https://host/test 可以這邊改 (或之後從xml改)

然後一直下一步最後先不要 publish (按關閉就會儲存設定檔)

先找到自動產生的發佈設定檔 XML (.pubxml)

找到 DeployIisAppPath 把裡面的值後面加上剛剛設定的虛擬路徑 \test

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/5c9f8a59-8d4d-48b4-8696-0e10967be384/1629096220.png)

如果要發佈完直接打開 \test 可以改 SiteUrlToLaunchAfterPublish 把後面加上/test

最後按發佈就可以了

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [IIS](/jakeuj/Tags?qq=IIS)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
