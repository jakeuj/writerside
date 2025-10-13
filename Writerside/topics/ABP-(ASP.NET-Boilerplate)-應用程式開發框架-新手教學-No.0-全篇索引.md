# ABP (ASP.NET Boilerplate) 應用程式開發框架 新手教學 No.0 全篇索引

> **原文發布日期:** 2016-07-28
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2016/07/28/abp0
> **標籤:** 無

---

ABP是「ASP.NET Boilerplate Project (ASP.NET樣板項目)」的簡稱。
ABP不僅僅是一個框架，更提供了一個基於DDD和最佳實踐方案
ABP的官方網站：<http://aspnetboilerplate.com/>

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/c2fe5da0-4ee1-4667-bb1a-15f28153f5e4/1567752189_41268.png)

應用程式常有許多重複性的功能例如：**授權，驗證，異常處理，日誌，本地化，數據庫連接管理，設置管理，審計日誌等**。
應用程式也需要規劃**分層**和**模塊化**架構，**領域驅動設計（DDD），依賴注入等等**。

因為開發這些都是非常耗時的，並且對於每個項目單獨創建是很困難的，所以很多公司都會創建自己私有的框架。通過使用私有的框架，他們總是可以快速地開發新的應用，同時應用的Bug又會更少。當然了，不是所有的公司都是那麼幸運了，大多數公司還是沒有**時間，預算和團隊**來開發他們自己的私人框架。即使他們有可能構建這麼一個框架，**寫文檔，培訓開發者以及維護**也是很難的。

ABP是一個**開源的且文檔友好的應用框架**，起始的想法是，“開發一款為所有公司和開發者通用的框架！”。它不僅僅是一個框架，更提供了一個基於**DDD**和**最佳實踐**的健壯的**體系模 ​​型**。

---

### [No.1 建立專案](https://dotblogs.com.tw/jakeuj/2016/07/26/abp1)

### [No.2 建立實體 Entity](https://dotblogs.com.tw/jakeuj/2016/07/26/abp2)

### [No.3 建立資料庫上下文 DbContext](https://dotblogs.com.tw/jakeuj/2016/07/27/abp3)

### [No.4 資料庫遷移 Migration](https://dotblogs.com.tw/jakeuj/2016/07/27/abp4)

### [No.5 建立倉儲 Repository](https://dotblogs.com.tw/jakeuj/2016/07/28/abp5)

### [No.6 建立應用服務](https://dotblogs.com.tw/jakeuj/2016/07/28/abp6)

### [No.7 建立WebApi](https://dotblogs.com.tw/jakeuj/2016/07/28/abp7)

### [No.8 單元測試](https://dotblogs.com.tw/jakeuj/2016/07/28/abp8)

### [No.9 全篇後記](https://dotblogs.com.tw/jakeuj/2016/07/28/abp9)

#### [No.10 範例程式](https://dotblogs.com.tw/jakeuj/2019/01/15/abp10)

### [No.11 Client Proxies (Angular Service)](https://dotblogs.com.tw/jakeuj/2019/01/18/abp11)

### [No.12 複數資料庫(DBContext)](https://dotblogs.com.tw/jakeuj/2019/01/30/abp12)

### [No.13 Angular Service](https://dotblogs.com.tw/jakeuj/2019/04/23/abp13)

### [No.14 SignalR with Angular](https://dotblogs.com.tw/jakeuj/2019/08/26/abp14)

### [No.15 Angular DateTime UTC Offset](https://dotblogs.com.tw/jakeuj/2019/09/17/abp15)

---

> ## ABP框架已實現了以下特性：
>
> * 多語言/本地化支持
> * 多租戶支持（每個租戶的數據自動隔離，業務模塊開發者不需要在保存和查詢數據時寫相應代碼）
> * 軟刪除支持（繼承相應的基類或實現相應接口，會自動實現軟刪除）
> * 統一的異常處理（應用層幾乎不需要處理自己寫異常處理代碼）
> * 數據有效性驗證（Asp.NET MVC只能做到Action方法的參數驗證，ABP實現了Application層方法的參數有效性驗證）
> * 日誌記錄（自動記錄程序異常）
> * 模塊化開發（每個模塊有獨立的EF DbContext，可單獨指定數據庫）
> * Repository倉儲模式（已實現了Entity Framework、NHibernate、MangoDB、內存數據庫）
> * Unit Of Work工作單元模式（為應用層和倉儲層的方法自動實現數據庫事務）
> * EventBus實現領域事件(Domain Events)
> * DLL嵌入資源管理
> * 通過Application Services自動創建Web Api層（不需要寫ApiController層了）
> * 自動創建Javascript 的代理層來更方便使用Web Api
> * 封裝一些Javascript 函數，更方便地使用ajax、消息框、通知組件、忙狀態的遮罩層等等

參照

[官方英文說明文件](http://www.aspnetboilerplate.com/Pages/Documents)

[一步一步使用ABP框架搭建正式項目系列教程](http://www.cnblogs.com/farb/p/4849791.html)

[基於DDD的現代ASP.NET開發框架](http://www.cnblogs.com/mienreal/p/4528470.html)

[GitHub文件翻譯](https://github.com/ABPFrameWorkGroup/AbpDocument2Chinese)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* C#
{ignore-vars="true"}
* ABP

* 回首頁

---

*本文章從點部落遷移至 Writerside*
