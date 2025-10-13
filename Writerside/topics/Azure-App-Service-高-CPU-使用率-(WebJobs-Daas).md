# Azure App Service 高 CPU 使用率 (WebJobs Daas)

> **原文發布日期:** 2022-11-17
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/11/17/AzureAppService-CPU-High-Usage-WebJobs-Daas
> **標籤:** 無

---

筆記下 App Service 異常 CPU 使用率飆高的疑難排解

## 結論

刪除 App Service > WebJobs > Daas

![enter image description here](https://i.stack.imgur.com/YeKgh.jpg)

### 症狀

同一隻程式在不同 Slot 中的某個特定 Slot 特別緩慢

排查後發現該 plan 中特定 app 有高 cpu 使用率的情況

但是同一隻程式在其他 Slot 又表現正常 (推斷 code 沒問題)

最後找到 WebJobs 中有不明 Job (Daas) 想說砍了會不會比較快

查了一下 Daas 是 Azure 診斷問題用的 Job

不需要診斷了話就可以把它砍了

所以就把她刪除了

後來發現 CPU 就降下來了

所以應該是某次想看看程式有沒有異常時點過診斷

Azure 自動新增 Daas 作業協助診斷問題

但該作業會造成 CPU 占用過高的問題

不知道這東西的情況下就會得到 CPU 使用率異常的結果

### 參照

[Mystery? Azure DaaS Webjob - Stack Overflow](https://stackoverflow.com/questions/53242391/mystery-azure-daas-webjob)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [App Service](/jakeuj/Tags?qq=App%20Service)
{ignore-vars="true"}

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
