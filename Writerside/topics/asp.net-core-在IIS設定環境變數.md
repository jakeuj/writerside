# asp.net core 在IIS設定環境變數

> **原文發布日期:** 2019-06-05
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/06/05/EnvironmentVariables
> **標籤:** 無

---

Setting environment variables for asp.net core when publishing on IIS

IIS > 選主機或是站台 > 配置編輯器

> 上方選 system.webServer 裡面的 aspNetCore

> 內容出現 environmentVariables 選右邊的 ... 就可以開出設定

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/63e6f4fa-fcb4-4ac8-89c7-e06a1cd6fca0/1559740300_73616.PNG)

P.S. 選主機是全域，而站台是By Site

不是全域了話他是寫在站台的Web.Config

所以重新佈署時如果蓋掉該檔就會失效

Ref: <https://www.andrecarlucci.com/en/setting-environment-variables-for-asp-net-core-when-publishing-on-iis/>

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [IIS](/jakeuj/Tags?qq=IIS)
* [.Net Core](/jakeuj/Tags?qq=.Net%20Core)
* [EnvironmentVariables](/jakeuj/Tags?qq=EnvironmentVariables)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
