# ABP.IO WEB應用程式框架 新手教學 No.12 建立專案

> **原文發布日期:** 2021-07-19
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/07/19/abpio1
> **標籤:** 無

---

[ABP.IO WEB應用程式框架 新手教學 No.0 索引](https://dotblogs.com.tw/jakeuj/2021/07/15/abpio0)

這次教學大致上會先照著 [官方教學文檔](https://docs.abp.io/en/abp/latest/Tutorials/Part-1?UI=NG&DB=EF) 來走一遍

這邊選用 Angular + EF Core 的組合來過一遍流程

首先下載基本樣板專案

<https://abp.io/get-started>

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/87bcc78e-ff0f-4121-8da5-3e2426d8cc84/1626662989.jpg)

這邊就先快速帶過，有興趣可以看一下有甚麼選項可以選，選好後會開始下載，解壓縮完長這樣

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/87bcc78e-ff0f-4121-8da5-3e2426d8cc84/1626340629.png)

這邊選 Angular 的原因是因為不屬於 .Net 體系，所以必定會將前後端分離到兩個不同的專案

這邊主要著重在後端 API 的開發，前端部分先不講 (有興趣可以加減參考2016版)

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/87bcc78e-ff0f-4121-8da5-3e2426d8cc84/1626340850.png)

打開專案大概長這樣

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/87bcc78e-ff0f-4121-8da5-3e2426d8cc84/1626341001.png)

上面是主要開發的專案，下面是做測試，這篇重點就先不放在怎麼做測試  (一樣有興趣可以加減參考2016版)

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/87bcc78e-ff0f-4121-8da5-3e2426d8cc84/1626663106.png)

這邊相比舊版多了不少專案檔，有稍微做過分層的應該不是非常陌生，這邊有DDD的概念會比較容易理解

可以了話 官方文檔 針對這部分會講得比較清楚，可以了話建議看一下

[DDD 領域驅動設計 ABP官方說明](https://docs.abp.io/zh-Hans/abp/latest/Domain-Driven-Design-Implementation-Guide)

關於文中提到的 SOLID 如果還不清楚的建議了解一下 [Wiki](https://zh.wikipedia.org/wiki/SOLID_(%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1%E8%AE%BE%E8%AE%A1))

其實這邊如果有localdb (沒有自己改 appsettings)，直接 [dotnet ef migrations add InitialCreate](https://docs.microsoft.com/zh-tw/ef/core/managing-schemas/migrations/?tabs=dotnet-core-cli#create-your-first-migration)，

然後執行DbMigrator專案建立資料庫，就可以跑Host專案開出Swagger畫面了

---

這邊簡單稍微介紹一下 DDD 分層

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/87bcc78e-ff0f-4121-8da5-3e2426d8cc84/1626343159.png)

DDD 將業務邏輯分為兩層,分別為 領域(Domain) 層和 應用(Application) 層,它們包含不同類型的業務邏輯.

* 領域層:只實現領域業務邏輯,與用例無關.
* 應用層:基於領域層來實現滿足用例的業務邏輯.用例可以看作是用戶界面(UI)或外部應用程序的交互.
* 展現層(Presentation):包含應用程序的UI元素.
* 基礎設施層(Infra):通過對第三方庫的集成或抽象,來滿足其它層的非核心業務邏輯的實現.

要說明專案檔之前需要先大概了解一下他們各自的相依性

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/87bcc78e-ff0f-4121-8da5-3e2426d8cc84/1626343025.png)

這邊重點先不放在DDD太多，所以放一張DDD的圖片看能不能稍微體會一下為什麼要這樣相依

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/87bcc78e-ff0f-4121-8da5-3e2426d8cc84/1626343151.png)

總之因為DDD內圈不能相依外圈，所以專案檔是不能隨便參照的

ABP.IO 實際將.Net Solution 依照 DDD 拆成以下 Projects

領域層:

* Domain：領域核心，主要包含實體,領域服務,倉儲介面,值對象,規約…等
* Domain.Shared：這是新版增加的，將領域層與其它層需要共用的東西抽出來(例如:列舉,常量等)
  這主要是因為表現層、Controllers、WebAPI所會用到的DTO不能直接依賴Domain(比如實體)，
  但是DTO又很常會用到實體定義的enum(列舉)或是欄位最大長度定義const(常量)

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/87bcc78e-ff0f-4121-8da5-3e2426d8cc84/1626345050.png)

應用層

* Application：是應用層中必需的,它實現了 Application.Contracts 項目中定義的接口.
* Application.Contracts：應用合約，包含接口的定義(Interface)及接口依賴的DTO,此項目可以被展現層或其它客戶端應用程序引用.
  這也是新版新增的，主要也是讓表現層、Controllers、WebAPI…等不直接依賴應用層
  例如：Unity (相當於表現層) 使用 c# 就可以直接拿這層 dll 去呼叫，不然要自己再寫一遍 DTO 或從專案原始碼複製過去
  這樣容易產生不同步的問題，以前DTO是放在應用層，相依一堆東西，又不可能拿去給 Unity直接用

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/87bcc78e-ff0f-4121-8da5-3e2426d8cc84/1626345000.png)

基礎設施層

* EntityFrameworkCore：資料持久保存是放在基礎設施，這邊使用EF Core會有這專案。
  應用程序的數據庫上下文(DbContext),數據庫對象映射,倉儲介面的實現,以及其它與EF Core相關的內容都位於此項目中.
* EntityFrameworkCore.DbMigrations：新版新增的專案，Migrations add 生成的檔案會放在這裡，不太需要動到這專案
  是管理Code First方式數據庫遷移記錄的特殊項目.此項目定義了一個獨立的DbContext來追踪遷移記錄.
  只有當添加一個新的數據庫遷移記錄或添加一個新的應用模塊時,才會使用此項目,否則,其它情況無需修改此項目內容.

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/87bcc78e-ff0f-4121-8da5-3e2426d8cc84/1626345024.png)

其他專案

* DbMigrator：建立領域實體然後 Migrations add 之後來執行這個專案就會生出資料庫/表，也可以產生SeedData
  目前用感覺不錯，要用記得裡面 appsettings 的連線字串要是正確的。(理論上直接 ef update database 應該也是可以)
  它是一個簡單的控制台程序,用來執行數據庫遷移,包括初始化數據庫及創建種子數據.這是一個非常實用的應用程序,
  你可以在開發環境或生產環境中使用它.

展現層

* Web (與HttpApi.Host擇一)：是一個ASP.NET Core MVC / Razor Pages應用程序.它是提供UI元素及API服務的可執行程序.
  展現層如果是前後端分離的就不會在方案內看到這一個專案：Blazor,Angular,Vue,React,Unity…ETC.
  反之提供另一個專案 HttpApi.Host 使用 Swagger API UI 介面給外部呼叫

遠程服務層

* HttpApi：新版新增的東西，目前實作上不需要動到這個專案 (用不到可能可以刪除？) 包含了HTTP API的定義.它通常包含MVC Controller 和 Model(如果有).因此,你可以在此項目中提供HTTP API.
* HttpApi.Host (與Web擇一)：ABP框架还支持其它类型的UI框架,包括Angular和Blazor.当选择Angular或Blazor时,解决方案不会有Web项目.但是会添加HttpApi.Host在解决方案中,
  此项目会提供HTTP API供UI调用.它是提供API服務的可執行程序. 執行這個就會跑出 Swagger API UI 介面給外部呼叫
* HttpApi.Client：新版新增的東西，目前實作上不需要動到這個專案 (感覺類似以前 WCF Client)
  就目前看起來比較像是提供這個dll給Unity這種C#的專案直接參照方便呼叫API用的。
  當C#客戶端應用程序需要調用HttpApi的API時,這個項目非常有用.
  客戶端程序僅需引用此項目就可以通過依賴注入方式,遠程調用應用服務.
  它是通過ABP框架的動態C#客戶端API代理系統來實現的.

---

[ABP.IO WEB應用程式框架 新手教學 No.2 建立實體 Entity](https://dotblogs.com.tw/jakeuj/2021/07/19/aaboio2)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [ABP](/jakeuj/Tags?qq=ABP)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
