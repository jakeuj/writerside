# ABP.IO 新手教學 No.03 開發教學 第 2 部分 圖書列表頁面

> **原文發布日期:** 2021-07-21
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/07/21/abpio03
> **標籤:** 無

---

這篇接續上一篇 [開發教學 Part  1 創建服務端](https://dotblogs.com.tw/jakeuj/2021/07/21/abpio02)

主要介紹 ABP Dynamic JavaScript API Client Proxies

可以自動根據 API 生成 JavaScript 呼叫 API 的函式

另外是關於 ABP 多國語言的部分如何使用

至於 Angular 實際實作的部分這邊就快速帶過

## Web應用程序開發教程 - 第二章：圖書列表頁面

## 關於本教程

在本系列教程中，您將構建一個名稱`Acme.BookStore`的用於管理書籍及其作者列表的基於 ABP 的程序。是使用以下技術開發的：

* **Entity Framework Core 為**ORM 提供程序。
* **MVC / Razor Pages**做為 UI 框架。

本教程分為以下部分：

* [第 1 部分：創建服務器端](https://docs.abp.io/en/abp/latest/Tutorials/Part-1)
* [第 2 部分：圖書列表頁面](https://docs.abp.io/en/abp/latest/Tutorials/Part-2)
* [第 3 部分：創建、更新和刪除書籍](https://docs.abp.io/en/abp/latest/Tutorials/Part-3)
* [第 4 部分：集成測試](https://docs.abp.io/en/abp/latest/Tutorials/Part-4)
* [第 5 部分：授權](https://docs.abp.io/en/abp/latest/Tutorials/Part-5)
* [第 6 部分：作者：領域層](https://docs.abp.io/en/abp/latest/Tutorials/Part-6)
* [第 7 部分：作者：數據庫集成](https://docs.abp.io/en/abp/latest/Tutorials/Part-7)
* [第 8 部分：作者：應用程序層](https://docs.abp.io/en/abp/latest/Tutorials/Part-8)
* [第 9 部分：作者：用戶界面](https://docs.abp.io/en/abp/latest/Tutorials/Part-9)
* [第 10 部分：圖書到作者的關係](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-10)

## 下載源碼

本教程根據你的**UI**和**數據庫**首選項有多個版本，我們準備了一個模型下載的源碼組件：

* [MVC (Razor Pages) UI 與 EF Core](https://github.com/abpframework/abp-samples/tree/master/BookStore-Mvc-EfCore)
* [Angular UI 與 MongoDB](https://github.com/abpframework/abp-samples/tree/master/BookStore-Angular-MongoDb)

## 動態JavaScript代理

// 執行 API 後，到 https://HttpApiHost/Abp/ServiceProxyScript ，可以看到 動態JS API 客戶端代理 產生的 js，請參照[Service Proxy Script Endpoint](https://docs.abp.io/en/abp/latest/UI/AspNetCore/Dynamic-JavaScript-Proxies#service-proxy-script-endpoint)

// 上面會用到 abp.js, abp.jquery.js，這些 JS 位置在 https://IdentityServerHost/libs/abp/core/abp.js，並且相依於 jQuery

// 想測試可以在 Google Chrome F12 Console 輸入以下指令之後就可以在 Swagger 頁面呼叫到 API (沒分離 Identity Server 可能可以直接呼叫)

```
javascript:(function(e,s){e.src=s;e.onload=function(){jQuery.noConflict();$=jQuery;console.log('jQuery injected')};document.head.appendChild(e);})(document.createElement('script'),'https://code.jquery.com/jquery-latest.min.js');
javascript:(function(e,s){e.src=s;document.head.appendChild(e);})(document.createElement('script'),'https://IdentityServerHost/libs/abp/core/abp.js');
javascript:(function(e,s){e.src=s;document.head.appendChild(e);})(document.createElement('script'),'https://IdentityServerHost/libs/abp/jquery/abp.jquery.js');
javascript:(function(e,s){e.src=s;document.head.appendChild(e);})(document.createElement('script'),'https://HttpApiHost/Abp/ServiceProxyScript');
acme.bookStore.books.book.getList({}).done(function (result) { console.log(result); });
```

// 如果上面找不到 JS，檢查 wwwroot/libs/abp/core/abp.js 是否存在，如果沒有可能需要安裝 [Node.js](https://nodejs.org/zh-tw/download/),[Yarn](https://yarnpkg.com/getting-started/install)，然後到 IdentityServerHost 專案目錄去執行 `Yarn Install` 裝一下ABP 的 JS Lib ([Rider](https://www.jetbrains.com/rider/) 會自動幫你完成這個動作)

經常在**JavaScript**調用HTTP端通過AJAX API訪問。你可以使用`$.ajax`或其他工具來增加土壤。但是 ABP 提供了更好的方法。

ABP**動態**為所有API創建[**JavaScript代理**](https://docs.abp.io/zh-Hans/abp/latest/UI/AspNetCore/Dynamic-JavaScript-Proxies)。所以你可以像調用**本地方法**一樣使用任何**地方**。

### 在開發者中進行測試

你可以在自己的瀏覽器的**開發者示範中**測試JavaScript代理。運行應用程序，打開瀏覽器的**開發人員**（*快捷方式通常是F12*），切換到**驗證工具**選項卡，輸入以下代碼然後回車：

```
acme.bookStore.books.book.getList({}).done(function (result) { console.log(result); });
```

* `acme.bookStore.books`是`BookAppService`的命令空間轉換成[小駝峰](https://en.wikipedia.org/wiki/Camel_case)形式。
* `book`是`BookAppService`的約定名稱（刪除`AppService`後綴並且轉換為小駝峰）。
* `getList`是`CrudAppService`基類定義的`GetListAsync`方法的約定名稱（刪除`Async`後綴並且轉換為小駝峰）。
* `{}`參數將空對象發送到`GetListAsync`該方法，該方法通常需要一個類型為`PagedAndSortedResultRequestDto`對象，用於將分頁和排序選項發送到服務器（所有屬性都是可選的，具有默認值。因此你可以發送一個空對象）。
* `getList`函數返回一個`promise`。你可以傳遞一個結果到`then`（或`done`）函數來獲取從服務器返回的結果。

運行該代碼會產生以下輸出：

![書店-javascript-代理-控制台](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/zh-Hans/Tutorials/images/bookstore-javascript-proxy-console.png)

您可以查看服務端返回的**圖書列表**。你也可以在開發人員工具的**網絡**選項卡上查看客戶端到服務端的通信：

![書店-getlist-result-network](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/zh-Hans/Tutorials/images/bookstore-getlist-result-network.png)

讓我們使用該函數**創建一本新書**`create`：

我們讓使用`create`函數**創建³³一本書**：

```
acme.bookStore.books.book.create({
        name: 'Foundation',
        type: 7,
        publishDate: '1951-05-24',
        price: 21.5
    }).then(function (result) {
        console.log('successfully created the book with id: ' + result.id);
    });
```

您應該在中發現類似以下的消息：

```
successfully created the book with id: 439b0ea8-923e-8e1e-5d97-39f2c7ac4246
```

檢查數據庫中的`Books`表你會看到新的一行。你可以自己嘗試使用`get`，`update`和`delete`函數。

我們將利用這些動態代理功能在下游的故事來與服務器通信。

## 本地化

開始的 UI 開發之前，我們首先要準備本地化的文本（這是你通常在開發應用程序時需要做的）。

本地化文本所在`Acme.BookStore.Domain.Shared`的`Localization/BookStore`文件夾下：

![書店本地化文件](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/zh-Hans/Tutorials/images/bookstore-localization-files-v2.png)

打開`en.json`（*英文翻譯*）文件並更改內容，如下所示：

```
{
  "Culture": "en",
  "Texts": {
    "Menu:Home": "Home",
    "Welcome": "Welcome",
    "LongWelcomeMessage": "Welcome to the application. This is a startup project based on the ABP framework. For more information, visit abp.io.",
    "Menu:BookStore": "Book Store",
    "Menu:Books": "Books",
    "Actions": "Actions",
    "Close": "Close",
    "Delete": "Delete",
    "Edit": "Edit",
    "PublishDate": "Publish date",
    "NewBook": "New book",
    "Name": "Name",
    "Type": "Type",
    "Price": "Price",
    "CreationTime": "Creation time",
    "AreYouSure": "Are you sure?",
    "AreYouSureToDelete": "Are you sure you want to delete this item?",
    "Enum:BookType:0": "Undefined",
    "Enum:BookType:1": "Adventure",
    "Enum:BookType:2": "Biography",
    "Enum:BookType:3": "Dystopia",
    "Enum:BookType:4": "Fantastic",
    "Enum:BookType:5": "Horror",
    "Enum:BookType:6": "Science",
    "Enum:BookType:7": "Science fiction",
    "Enum:BookType:8": "Poetry"
  }
}
```

* 本地化關鍵字名稱是任意的。你可以設置任何名稱。對於特定的文本類型，我們更喜歡遵循一些約定：
  + 為按鈕添加添加`Menu:`。
  + 使用`Enum:<enum-type>:<enum-value>`同一來本地化的枚舉成員。當您銷毀ABP可以在某些適當的情況下自動將枚舉本地化。

如果未在本地化文件中定義文本，字幕：則將**回退**到本地化鍵（作為ASP.NET核心的標準行為）。

> ABP本地化系統建立在[ASP.NET Core標準](https://docs.microsoft.com/en-us/aspnet/core/fundamentals/localization)本地化系統之上，並以多種方式進行了擴展。有關詳細信息請參見當地化[文檔](https://docs.abp.io/zh-Hans/abp/latest/Localization)。

// 以下

## 安裝 NPM 包

> 注意：本教程基於ABP Framework v3.1.0+ 如果您的項目版本較舊，請升級您的解決方案。如果您使用 v2.x 升級現有項目，請參閱[遷移指南](https://docs.abp.io/en/abp/latest/UI/Angular/Migration-Guide-v3)。

如果您以前沒有這樣做過，請打開一個新的命令行界面（終端窗口）並轉到您的`angular`文件夾，然後運行`yarn` 命令來安裝 NPM 包：

```
yarn
```

## 創建圖書頁面

是時候創造一些可見和可用的東西了！在開發 Angular 前端應用程序時，我們將使用一些工具：

* [Ng Bootstrap](https://ng-bootstrap.github.io/#/home)將用作 UI 組件庫。
* [Ngx-Datatable](https://swimlane.gitbook.io/ngx-datatable/)將用作[數據表](https://swimlane.gitbook.io/ngx-datatable/)庫。

運行以下命令行以創建一個新模塊，`BookModule`在 angular 應用程序的根文件夾中命名：

```
yarn ng generate module book --module app --routing --route books
```

此命令應產生以下輸出：

```
> yarn ng generate module book --module app --routing --route books

yarn run v1.19.1
$ ng generate module book --module app --routing --route books
CREATE src/app/book/book-routing.module.ts (336 bytes)
CREATE src/app/book/book.module.ts (335 bytes)
CREATE src/app/book/book.component.html (19 bytes)
CREATE src/app/book/book.component.spec.ts (614 bytes)
CREATE src/app/book/book.component.ts (268 bytes)
CREATE src/app/book/book.component.scss (0 bytes)
UPDATE src/app/app-routing.module.ts (1289 bytes)
Done in 3.88s.
```

### 圖書模塊

打開`/src/app/book/book.module.ts`並替換如下內容：

```
import { NgModule } from '@angular/core';
import { SharedModule } from '../shared/shared.module';
import { BookRoutingModule } from './book-routing.module';
import { BookComponent } from './book.component';

@NgModule({
  declarations: [BookComponent],
  imports: [
    BookRoutingModule,
    SharedModule
  ]
})
export class BookModule { }
```

* 添加了`SharedModule`. `SharedModule`導出一些創建用戶界面所需的常用模塊。
* `SharedModule`已經導出了`CommonModule`，所以我們已經刪除了`CommonModule`.

### 路由

生成的代碼將新的路由定義放置到`src/app/app-routing.module.ts`文件中，如下所示：

```
const routes: Routes = [
  // other route definitions...
  { path: 'books', loadChildren: () => import('./book/book.module').then(m => m.BookModule) },
];
```

現在，打開`src/app/route.provider.ts`文件替換`configureRoutes`函數聲明，如下所示：

```
function configureRoutes(routes: RoutesService) {
  return () => {
    routes.add([
      {
        path: '/',
        name: '::Menu:Home',
        iconClass: 'fas fa-home',
        order: 1,
        layout: eLayoutType.application,
      },
      {
        path: '/book-store',
        name: '::Menu:BookStore',
        iconClass: 'fas fa-book',
        order: 2,
        layout: eLayoutType.application,
      },
      {
        path: '/books',
        name: '::Menu:Books',
        parentName: '::Menu:BookStore',
        layout: eLayoutType.application,
      },
    ]);
  };
}
```

`RoutesService` 是 ABP 框架提供的一項服務，用於配置主菜單和路由。

* `path` 是路由的 URL。
* `name`是本地化的菜單項名稱（有關詳細信息，請參閱[本地化文檔](https://docs.abp.io/en/abp/latest/UI/Angular/Localization)）。
* `iconClass`是菜單項的圖標（默認情況下可以使用[Font Awesome](https://fontawesome.com/)圖標）。
* `order` 是菜單項的順序。
* `layout`是 BooksModule 路由的佈局（有三種類型的預定義佈局：`eLayoutType.application`、`eLayoutType.account`或`eLayoutType.empty`）。

有關更多信息，請參閱[RoutesService 文檔](https://docs.abp.io/en/abp/latest/UI/Angular/Modifying-the-Menu#via-routesservice)。

### 服務代理生成

[ABP CLI](https://docs.abp.io/en/abp/latest/CLI)提供了`generate-proxy`為您的 HTTP API 生成客戶端代理的命令，以便從客戶端輕鬆使用您的 HTTP API。在運行`generate-proxy`命令之前，您的主機必須已啟動並正在運行。

> **警告**：IIS Express 存在問題；它不允許從另一個進程連接到應用程序。如果您使用的是Visual Studio，請`Acme.BookStore.HttpApi.Host`在運行按鈕下拉列表中選擇代替IIS Express，如下圖所示：

![vs-run-without-iisexpress](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/en/Tutorials/images/vs-run-without-iisexpress.png)

主機應用程序運行後，在`angular`文件夾中執行以下命令：

```
abp generate-proxy
```

此命令將在文件`/src/app/proxy/books`夾下創建以下文件：

![生成的文件](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/en/Tutorials/images/generated-proxies-3.png)

### 書本組件

打開`/src/app/book/book.component.ts`文件並替換如下內容：

```
import { ListService, PagedResultDto } from '@abp/ng.core';
import { Component, OnInit } from '@angular/core';
import { BookService, BookDto } from '@proxy/books';

@Component({
  selector: 'app-book',
  templateUrl: './book.component.html',
  styleUrls: ['./book.component.scss'],
  providers: [ListService],
})
export class BookComponent implements OnInit {
  book = { items: [], totalCount: 0 } as PagedResultDto<BookDto>;

  constructor(public readonly list: ListService, private bookService: BookService) {}

  ngOnInit() {
    const bookStreamCreator = (query) => this.bookService.getList(query);

    this.list.hookToQuery(bookStreamCreator).subscribe((response) => {
      this.book = response;
    });
  }
}
```

* 我們導入並註入了生成的`BookService`.
* 我們正在使用[ListService](https://docs.abp.io/en/abp/latest/UI/Angular/List-Service)，這是 ABP 框架的實用服務，它提供了簡單的分頁、排序​​和搜索。

打開`/src/app/book/book.component.html`並替換如下內容：

```
<div class="card">
  <div class="card-header">
    <div class="row">
      <div class="col col-md-6">
        <h5 class="card-title">
          {{ '::Menu:Books' | abpLocalization }}
        </h5>
      </div>
      <div class="text-right col col-md-6"></div>
    </div>
  </div>
  <div class="card-body">
    <ngx-datatable [rows]="book.items" [count]="book.totalCount" [list]="list" default>
      <ngx-datatable-column [name]="'::Name' | abpLocalization" prop="name"></ngx-datatable-column>
      <ngx-datatable-column [name]="'::Type' | abpLocalization" prop="type">
        <ng-template let-row="row" ngx-datatable-cell-template>
          {{ '::Enum:BookType:' + row.type | abpLocalization }}
        </ng-template>
      </ngx-datatable-column>
      <ngx-datatable-column [name]="'::PublishDate' | abpLocalization" prop="publishDate">
        <ng-template let-row="row" ngx-datatable-cell-template>
          {{ row.publishDate | date }}
        </ng-template>
      </ngx-datatable-column>
      <ngx-datatable-column [name]="'::Price' | abpLocalization" prop="price">
        <ng-template let-row="row" ngx-datatable-cell-template>
          {{ row.price | currency }}
        </ng-template>
      </ngx-datatable-column>
    </ngx-datatable>
  </div>
</div>
```

現在您可以在瀏覽器上看到最終結果：

![書單最終結果](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/en/Tutorials/images/bookstore-book-list.png)

## 下一部分

請參閱本教程的[下一部分](https://docs.abp.io/en/abp/latest/Tutorials/Part-3)。

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ABP

* 回首頁

---

*本文章從點部落遷移至 Writerside*
