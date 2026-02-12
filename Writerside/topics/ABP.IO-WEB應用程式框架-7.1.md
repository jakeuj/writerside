# ABP.IO WEB應用程式框架 7.1

> **原文發布日期:** 2023-02-20
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/02/20/ABP-7-1
> **標籤:** 無

---

ABP 7.1 版本 新功能 摘要

## 簡介

1. 介面和基類 `IHasEntityVersion` `EntitySynchronizer`
   實體同步是一個重要的概念，尤其是在分散式應用程式和模塊開發中。
   如果我們有一個與其他模組相關的實體，我們需要在實體更改后對齊/同步它們的數據，
   並且版本控制實體更改也可以很好，這樣我們就可以知道它們是否已同步。
2. 介面的方法 `DeleteDirectAsyncIRepository`
   EF 7 引入了一種新的 ExecuteDeleteAsync 方法，該方法刪除實體而不涉及流程中的更改跟蹤器。
   因此，它要快得多。 我們已將該方法添加到介面，以充分利用 [EF 7](https://learn.microsoft.com/en-us/ef/core/what-is-new/ef-core-7.0/whatsnew#executeupdate-and-executedelete-bulk-updates) 的功能。
   它刪除符合給定謂詞的所有實體。它直接從資料庫中刪除實體，而不獲取它們。
   因此，一些功能不起作用，如軟刪除,多租戶和審計日誌，因此在需要時請謹慎使用此方法。
   如果需要這些功能，請使用該 DeleteAsync 方法。
3. 介面 `IAbpHostEnvironment`
   有時，在創建應用程式時，我們需要獲取當前的託管環境並據此採取措施。
   在這種情況下，我們可以在最終應用程式中使用一些服務，
   例如 .NET 提供的 IWebHostEnvironment 或 IWebAssemblyHostEnvironment。
   但是，我們不能在類庫中使用這些服務，該類庫由最終應用程式使用。
   ABP 架構提供服務， 它允許您隨時取得當前環境名稱. 被ABP框架在幾個地方用來執行環境的特定操作
   例如， ABP 框架減少了緩存持續時間 IAbpHostEnvironment IAbpHostEnvironment Development某些服務的環境。

### REF

[ABP.IO Platform 7.1 RC Has Been Published | ABP.IO](https://blog.abp.io/abp/ABP.IO-Platform-7.1-RC-Has-Been-Published)

[EF Core 7.0 的新功能 | Microsoft Learn](https://learn.microsoft.com/zh-tw/ef/core/what-is-new/ef-core-7.0/whatsnew#executeupdate-and-executedelete-bulk-updates)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- ABP

- 回首頁

---

*本文章從點部落遷移至 Writerside*
