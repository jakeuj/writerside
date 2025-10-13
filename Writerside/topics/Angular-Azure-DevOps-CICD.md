# Angular Azure DevOps CI/CD

> **原文發布日期:** 2019-02-19
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/02/19/angular_ci_cd
> **標籤:** 無

---

Angular Azure DevOps CI/CD 持續整合/發布

CI/CD 的基本操作這篇講蠻清楚了

[在Azure DevOps從無到有建立CI/CD專案](https://itweihan.azurewebsites.net/blog/10207833/)

微軟自家的DotNetCore專案頗容易就可以搭配期推出的DevOps做到CI/CD

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/2300d2c9-4fef-49ef-a3b6-0db1727e4490/1554107038_17495.jpg)

這邊主要針對Angular的CI/CD做補充說明

1.build (+Yarn)

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/2300d2c9-4fef-49ef-a3b6-0db1727e4490/1550575349_27524.jpg)

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/2300d2c9-4fef-49ef-a3b6-0db1727e4490/1550575363_10611.jpg)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/2300d2c9-4fef-49ef-a3b6-0db1727e4490/1550575363_18212.jpg)

2.Release (注意 deploy folder 要選正確路徑)
![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/2300d2c9-4fef-49ef-a3b6-0db1727e4490/1550575362_94773.jpg)

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/2300d2c9-4fef-49ef-a3b6-0db1727e4490/1550577239_36116.jpg)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/2300d2c9-4fef-49ef-a3b6-0db1727e4490/1550575363_11962.jpg)

3.Test

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/2300d2c9-4fef-49ef-a3b6-0db1727e4490/1550575363_24462.jpg)

收回前言，先上圖，有需要再稍作說明...

NPM：<https://dotblogs.com.tw/jamesfu/2017/08/02/vsts_angular4>

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Angular
* DevOps
* Azure

* 回首頁

---

*本文章從點部落遷移至 Writerside*
