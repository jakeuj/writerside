# ABP.IO WEB應用程式框架 新手教學 No.01 快速開始

> **原文發布日期:** 2021-07-20
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/07/20/abpio01
> **標籤:** 無

---

使用 ABP.IO 以 Angular + EF Core 簡單建立  API

著重在 .Net Core API 新增部分

前端 Angular 不在本次重點會先快速帶過

### [[2021] ABP.IO WEB應用程式框架 新手教學 No.0 全篇索引](https://dotblogs.com.tw/jakeuj/2021/07/15/abpio0)

---

本篇會以官方文件 [快速開始](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index) 為依據中文化並附圖加以說明的方式進行

## [快速開始](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#quick-start)

這是一個單一部分的快速入門教程，用於使用 ABP 框架構建一個簡單的待辦事項應用程序。這是最終應用程序的屏幕截圖：

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bd1a5116-2353-47cb-988a-bbb78058c450/1626744807.png)

preview

您可以[在此處](https://github.com/abpframework/abp-samples/tree/master/TodoApp)找到已完成應用程序的源代碼。

## [先決條件](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#pre-requirements)

支持[.NET 5.0+](https://dotnet.microsoft.com/download/dotnet) 開發的 IDE （例如:[Rider](https://www.jetbrains.com/rider/), [Visual Studio](https://visualstudio.microsoft.com/vs/)）

[Node.js v14.x](https://nodejs.org/)

// 本篇不實作 Angular, 可以不用裝 Node.js

// Redis，可以安裝 [docker](https://www.docker.com/products/docker-desktop) 後執行，`docker pull redis` & `docker run --name some-redis -d redis -p 6379:6379`

## [創建新解決方案](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#creating-a-new-solution)

我們將使用 [ABP CLI](https://docs.abp.io/zh-Hans/abp/latest/CLI) 通過 ABP 框架創建新的解決方案。您可以在命令行終端中運行以下命令來安裝它：

// 命令行終端: PowerShell, CMD, Bash

```
dotnet tool install -g Volo.Abp.Cli
```

然後創建一個空文件夾，打開命令行終端，在終端中執行以下命令：

```
abp new TodoApp -u angular
```

這將創建一個新的解決方案，名為*TodoApp*與`angular`和`aspnet-core`文件夾。解決方案準備就緒後，在您喜歡的 IDE 中打開 ASP.NET Core 解決方案。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bd1a5116-2353-47cb-988a-bbb78058c450/1626746994.png)

Aspnet-core

### [創建數據庫](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#create-the-database)

如果您使用的是 Visual Studio，請右鍵單擊該`TodoApp.DbMigrator`項目，選擇*Set as StartUp Project*，然後*按 Ctrl+F5* 運行它而不進行調試。它將創建初始數據庫並建立初始種子資料(SeedData)。

> 由於 *DbMigrator* 添加了初始遷移並重新編譯項目，因此某些 IDE（例如 Rider）在第一次運行時可能會出現問題。在這種情況下，在`.DbMigrator`項目文件夾中打開命令行終端並執行`dotnet run`命令。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bd1a5116-2353-47cb-988a-bbb78058c450/1626746248.png)

PowerShell

### [運行應用程序](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#run-the-application)

在開始開發之前運行應用程序是很好的。該解決方案有兩個主要應用；

* `TodoApp.HttpApi.Host` （在 .NET 解決方案中）託管服務器端 HTTP API。
* `angular` 文件夾包含 Angular 應用程序。

// 因為專案預設會啟用 Redis，如果沒有可以先關閉，在 appsettings.json 中的 Redis 裡面加上 "IsEnabled": "true", 請參考 [Redis 快取設定 說明文件](https://docs.abp.io/en/abp/latest/Redis-Cache#configuration),很重要所以我會說三次以上

確保`TodoApp.HttpApi.Host`項目是啟動項目，然後運行應用程序（Visual Studio 中的 Ctrl+F5）以在 [Swagger UI](https://swagger.io/tools/swagger-ui/) 上查看服務器端 HTTP API ：

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bd1a5116-2353-47cb-988a-bbb78058c450/1626746348.png)

TodoAPI

您可以使用此 UI 探索和測試您的 HTTP API。如果可行，我們可以運行 Angular 客戶端應用程序。

// 至此已完成 API 的運行，以下表現層這邊就先不安裝並執行 Angular 了，如果要跑記得先安裝 node.js。

首先，運行以下命令恢復 NPM 包；

```
npm install
```

安裝所有軟件包需要一些時間。然後，您可以使用以下命令運行該應用程序：

```
npm start
```

此命令需要時間，但最終會在默認瀏覽器中運行並打開應用程序：

![todo-ui-initial](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/en/Tutorials/Todo/todo-ui-initial.png)

您可以單擊 *登錄(Login)* 按鈕，將`admin`用作其用戶名和`1q2w3E*`密碼來登錄應用程序。

一切準備就緒。我們可以開始編碼了！

## [領域層](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#domain-layer)

這個應用程序只有一個[實體](https://docs.abp.io/zh-Hans/abp/latest/Entities)(Entity)，我們從創建它開始。`TodoItem`在 *TodoApp.Domain* 項目中創建一個新類：

```
using System;
using Volo.Abp.Domain.Entities;

namespace TodoApp
{
    public class TodoItem : BasicAggregateRoot<Guid>
    {
        public string Text { get; set; }
    }
}
```

`BasicAggregateRoot` (內含 Id 欄位當作主鍵) 是創建聚合根實體的最簡單的基類之一，這裡實體的主鍵 ( `Id`) 是 `Guid`型別 (目前 Abp 推薦使用 Guid 作為 PK)。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bd1a5116-2353-47cb-988a-bbb78058c450/1626747076.png)

TodoItem

// 這邊我建了資料夾來放，主要是實戰時不會把全部東西散落在各專案的根目錄，同一個聚合應該建立一個資料夾來放相關物件

// 在其他層的專案也一樣，盡量保持同名方便理解，要移除時也比較清楚該刪除那些東西

## [數據庫集成](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#database-integration)

下一步是設置 [Entity Framework Core](https://docs.abp.io/zh-Hans/abp/latest/Entity-Framework-Core) 配置。

### [映射配置](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#mapping-configuration)

打開 *TodoApp.EntityFrameworkCore* 項目文件夾中的`TodoAppDbContext`類，給這個類添加一個新的屬性：`EntityFrameworkCoreDbSet`

// 科普：私有唯讀叫欄位，公開有 get, set 叫屬性！

```
public DbSet<TodoItem> TodoItems { get; set; }
```

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bd1a5116-2353-47cb-988a-bbb78058c450/1626747272.png)

DbSet

然後`TodoAppDbContextModelCreatingExtensions`在同一個文件夾中打開類，為類添加映射配置，`TodoItem`如下圖：

```
public static void ConfigureTodoApp(this ModelBuilder builder)
{
    Check.NotNull(builder, nameof(builder));

    builder.Entity<TodoItem>(b =>
    {
        b.ToTable("TodoItems");
    });
}
```

我們已經將`TodoItem`實體映射到`TodoItems`數據庫中的一個表。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bd1a5116-2353-47cb-988a-bbb78058c450/1626747524.png)

TodoAppDbContextModelCreatingExtensions

// 這邊 `ToTable` 用來指定資料表名稱，可以參考 EF Core 的官方文件

### [程式碼優先遷移](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#code-first-migrations)

啟動解決方案配置為使用 Entity Framework Core [Code First Migrations](https://docs.microsoft.com/en-us/ef/core/managing-schemas/migrations)。由於我們已經更改了數據庫映射配置，我們應該創建一個新的遷移並將更改應用於數據庫。

// Code First 程式碼優先：Entity Framework 提供從程式碼建立資料庫的功能，不必親自到資料庫伺服器建資料庫或資料表，也不用寫SQL，如此可以先由程式碼開始定義實體

在 *TodoApp.EntityFrameworkCore.DbMigrations* 項目的目錄中打開命令行終端並鍵入以下命令：

```
dotnet ef migrations add Added_TodoItem
```

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bd1a5116-2353-47cb-988a-bbb78058c450/1626747795.png)

migrations add

這將向項目添加一個新的遷移類：

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bd1a5116-2353-47cb-988a-bbb78058c450/1626747863.png)

Migrations

您可以在同一命令行終端中使用以下命令對數據庫應用更改：

```
dotnet ef database update
```

> 如果您使用的是 Visual Studio，則可能需要在*包管理器控制台 (PMC) 中*使用`Add-Migration Added_TodoItem`和`Update-Database`命令。
>
> 在這種情況下，請確保是啟動項目並且是PMC 中的*默認項目*。`TodoApp.HttpApi.HostTodoApp.EntityFrameworkCore.DbMigrations`

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bd1a5116-2353-47cb-988a-bbb78058c450/1626748005.png)

database update

現在，我們可以使用 ABP 存儲庫來保存和檢索待辦事項，我們將在下一節中進行。

## [應用層](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#application-layer)

一個 [應用服務](https://docs.abp.io/zh-Hans/abp/latest/Application-Services) 被用來執行應用程序的使用情況。我們需要執行以下用例；

* 獲取待辦事項列表
* 創建一個新的待辦事項
* 刪除現有的待辦事項

// 下面我將會調換原文說明順序，將應用服務合約中的資料傳輸物件與應用服務介面互換，因為 Application Service Interface 會用到 DTO

### [數據傳輸對象](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#data-transfer-object)

`GetListAsync`和`CreateAsync`方法返回`TodoItemDto`。

應用程序服務通常獲取和返回 DTO（[數據傳輸對象](https://docs.abp.io/zh-Hans/abp/latest/Data-Transfer-Objects)）而不是實體。

所以，我們應該在這裡定義 DTO 類。

在*TodoApp.Application.Contracts* 項目中創建一個新類 `TodoItemDto`：

```
using System;

namespace TodoApp
{
    public class TodoItemDto
    {
        public Guid Id { get; set; }
        public string Text { get; set; }
    }
}
```

這是一個非常簡單的 DTO 類，與我們的`TodoItem`實體相匹配。我們已準備好實施`ITodoAppService`.

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bd1a5116-2353-47cb-988a-bbb78058c450/1626748382.png)

TodoItemDto

### [應用服務接口](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#application-service-interface)

我們可以從為應用程序服務定義一個接口開始。在 *TodoApp.Application.Contracts* 項目中新建一個界面 `ITodoAppService`，如下：

```
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Volo.Abp.Application.Services;

namespace TodoApp
{
    public interface ITodoAppService : IApplicationService
    {
        Task<List<TodoItemDto>> GetListAsync();
        Task<TodoItemDto> CreateAsync(string text);
        Task DeleteAsync(Guid id);
    }
}
```

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bd1a5116-2353-47cb-988a-bbb78058c450/1626748518.png)

ITodoAppService

// 雖然不建立介面也可以直接實作應用服務，但最佳實踐建一位每個應用服務建立各自的 Interface

### [應用服務實現](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#application-service-implementation)

在*TodoApp.Application*項目裡面創建一個類 `TodoAppService`，如下：

```
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Volo.Abp.Application.Services;
using Volo.Abp.Domain.Repositories;

namespace TodoApp
{
    public class TodoAppService : ApplicationService, ITodoAppService
    {
        private readonly IRepository<TodoItem, Guid> _todoItemRepository;

        public TodoAppService(IRepository<TodoItem, Guid> todoItemRepository)
        {
            _todoItemRepository = todoItemRepository;
        }

        // TODO: Implement the methods here...
    }
}
```

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bd1a5116-2353-47cb-988a-bbb78058c450/1626748824.png)

TodoAppService

該類繼承自ABP 框架的類`ApplicationService`並實現了之前定義的`ITodoAppService` 。

ABP 為實體提供默認的通用[存儲庫](https://docs.abp.io/zh-Hans/abp/latest/Repositories) (Repository)。我們可以使用它們來執行基本的數據庫操作。

這個類[註入](https://docs.abp.io/zh-Hans/abp/latest/Dependency-Injection) `IRepository<TodoItem, Guid>`，它是`TodoItem`實體的默認存儲庫。我們將使用它來實現之前描述的用例。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bd1a5116-2353-47cb-988a-bbb78058c450/1626748964.png)

Implement

#### [獲取 Todo 項目](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#getting-todo-items)

讓我們從實現該`GetListAsync`方法開始：

```
public async Task<List<TodoItemDto>> GetListAsync()
{
    var items = await _todoItemRepository.GetListAsync();
    return items
        .Select(item => new TodoItemDto
        {
            Id = item.Id,
            Text = item.Text
        }).ToList();
}
```

我們只是從數據庫中獲取 `TodoItem` 完整列表，將它們映射到`TodoItemDto`對象並作為結果返回。

// 這邊範例為了快速開始所以使用手動方式手動將 Entity 映射到 DTO, ABP 也有整合 AutoMapper，請參考 [連結](https://docs.abp.io/zh-Hans/abp/latest/Object-To-Object-Mapping)

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bd1a5116-2353-47cb-988a-bbb78058c450/1626749022.png)

GetListAsync

#### [創建一個新的 Todo 項目](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#creating-a-new-todo-item)

下一個方法是`CreateAsync`，我們可以實現它，如下所示：

```
public async Task<TodoItemDto> CreateAsync(string text)
{
    var todoItem = await _todoItemRepository.InsertAsync(
        new TodoItem {Text = text}
    );

    return new TodoItemDto
    {
        Id = todoItem.Id,
        Text = todoItem.Text
    };
}
```

Repository 的`InsertAsync`方法將給定的`TodoItem`物件插入數據庫並返回相同的 `TodoItem` 物件。

它還設置了`Id`，因此我們可以在返回的物件上使用它。

我們只是從新建的`TodoItem`實體返回一個`TodoItemDto`。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bd1a5116-2353-47cb-988a-bbb78058c450/1626749202.png)

CreateAsync

#### [刪除到每個項目](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#deleting-a-todo-item)

最後，我們可以實現`DeleteAsync`如下代碼塊：

```
public async Task DeleteAsync(Guid id)
{
    await _todoItemRepository.DeleteAsync(id);
}
```

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bd1a5116-2353-47cb-988a-bbb78058c450/1626749287.png)

DeleteAsync

應用程序服務已準備好從 UI 層使用。

// 因為專案預設會啟用 Redis，如果沒有可以先關閉，在 appsettings.json 中的 Redis 裡面加上 "IsEnabled": "true", 請參考 [Redis 快取設定 說明文件](https://docs.abp.io/en/abp/latest/Redis-Cache#configuration),很重要所以我會說三次以上

// 至此已完成 API 的新增，以下表現層這邊就先不繼續實作 Angular 了，如果要跑記得先安裝 node.js。

// 特別提一下[服務代理 (Service Proxy)](https://docs.abp.io/zh-Hans/abp/latest/UI/Angular/Service-Proxies)，大致功能是自動根據最新 API 的 JSON 生成 Client 呼叫用的 TypeScript，個人用 Angular 開發時覺得很方便。

## [用戶界面層](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#user-interface-layer)

是時候在 UI 上顯示待辦事項了！在開始編寫代碼之前，最好記住我們正在嘗試構建的內容。這是最終用戶界面的示例屏幕截圖：

![全部列表](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/en/Tutorials/Todo/todo-list.png)
> **我們將在本教程中盡量減少 UI 方面，以使教程簡單而集中。請參閱**[**Web 應用程序開發教程**](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-1)**以構建具有各個方面的真實頁面。**

### [服務代理生成](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#service-proxy-generation)

ABP 提供了一個方便的功能來自動創建客戶端服務，以輕鬆使用服務器提供的 HTTP API。

您首先需要運行該`TodoApp.HttpApi.Host`項目，因為代理生成器從服務器應用程序讀取 API 定義。

// 因為專案預設會啟用 Redis，如果沒有可以先關閉，在 appsettings.json 中的 Redis 裡面加上 "IsEnabled": "true", 請參考 [Redis 快取設定 說明文件](https://docs.abp.io/en/abp/latest/Redis-Cache#configuration),很重要所以我會說三次以上

> **警告**：IIS Express 存在問題；它不允許從另一個進程連接到應用程序。如果您使用的是Visual Studio，請`TodoApp.HttpApi.Host`在運行按鈕下拉列表中選擇代替IIS Express，如下圖所示：

![運行無 iisexpress](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/en/Tutorials/Todo/run-without-iisexpress.png)

運行`TodoApp.HttpApi.Host`項目後，在`angular`文件夾中打開命令行終端並鍵入以下命令：

```
abp generate-proxy
```

如果一切順利，它應該生成如下所示的輸出：

```
CREATE src/app/proxy/generate-proxy.json (170978 bytes)
CREATE src/app/proxy/README.md (1000 bytes)
CREATE src/app/proxy/todo.service.ts (794 bytes)
CREATE src/app/proxy/models.ts (66 bytes)
CREATE src/app/proxy/index.ts (58 bytes)
```

然後我們可以使用`todoService`來使用服務器端 HTTP API，我們將在下一節中進行。

### [home.component.ts](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#home-component-ts)

打開`/angular/src/app/home/home.component.ts`文件並將其內容替換為以下代碼塊：

```
import { ToasterService } from '@abp/ng.theme.shared';
import { Component, OnInit } from '@angular/core';
import { TodoItemDto, TodoService } from '@proxy';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  todoItems: TodoItemDto[];
  newTodoText: string;

  constructor(
      private todoService: TodoService,
      private toasterService: ToasterService)
  { }

  ngOnInit(): void {
    this.todoService.getList().subscribe(response => {
      this.todoItems = response;
    });
  }

  create(): void{
    this.todoService.create(this.newTodoText).subscribe((result) => {
      this.todoItems = this.todoItems.concat(result);
      this.newTodoText = null;
    });
  }

  delete(id: string): void {
    this.todoService.delete(id).subscribe(() => {
      this.todoItems = this.todoItems.filter(item => item.id !== id);
      this.toasterService.info('Deleted the todo item.');
    });
  }
}
```

我們已經使用`todoService`來獲取待辦事項列表並將返回值分配給`todoItems`數組。我們還添加了`create`和`delete`方法。這些方法將在視圖端使用。

### [home.component.html](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#home-component-html)

打開`/angular/src/app/home/home.component.html`文件並將其內容替換為以下代碼塊：

```
<div class="container">
  <div class="card">
    <div class="card-header">
      <div class="card-title">TODO LIST</div>
    </div>
    <div class="card-body">
      <!-- FORM FOR NEW TODO ITEMS -->
      <form class="form-inline" (ngSubmit)="create()">
        <input
          name="NewTodoText"
          type="text"
          [(ngModel)]="newTodoText"
          class="form-control mr-2"
          placeholder="enter text..."
        />
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>

      <!-- TODO ITEMS LIST -->
      <ul id="TodoList">
        <li *ngFor="let todoItem of todoItems">
          <i class="fa fa-trash-o" (click)="delete(todoItem.id)"></i> {{ todoItem.text }}
        </li>
      </ul>
    </div>
  </div>
</div>
```

### [home.component.scss](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#home-component-scss)

最後，打開`/angular/src/app/home/home.component.scss`文件並將其內容替換為以下代碼塊：

```
#TodoList{
    list-style: none;
    margin: 0;
    padding: 0;
}

#TodoList li {
    padding: 5px;
    margin: 5px 0px;
    border: 1px solid #cccccc;
    background-color: #f5f5f5;
}

#TodoList li i
{
    opacity: 0.5;
}

#TodoList li i:hover
{
    opacity: 1;
    color: #ff0000;
    cursor: pointer;
}
```

這是 todo 頁面的簡單樣式。我們相信你可以做得更好:)

現在，您可以再次運行該應用程序以查看結果。

## [結論](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#conclusion)

在本教程中，我們構建了一個非常簡單的應用程序來預熱 ABP 框架。如果您希望構建一個嚴肅的應用程序，請查看[Web 應用程序開發教程](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-1)，該[教程](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-1)涵蓋了實際 Web 應用程序開發的所有方面。

## [源代碼](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#source-code)

您可以[在此處](https://github.com/abpframework/abp-samples/tree/master/TodoApp)找到已完成應用程序的源代碼。

## [也可以看看](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Todo/Index?UI=NG&DB=EF#see-also)

* [Web 應用程序開發教程](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-1)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [ABP](/jakeuj/Tags?qq=ABP)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
