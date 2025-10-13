# ABP.IO WEB應用程式框架 新手教學 No.10 開發教學 第 9 部分&#xFF1A;作者&#xFF1A;用戶界面

> **原文發布日期:** 2021-07-23
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/07/23/ABP-Tutorials-Part-9
> **標籤:** 無

---

主要是之前做的 Author 使用 Anuglar 做展示層

先快速帶過

## Web 應用程序開發教程 - 第 9 部分：作者：用戶界面

## 關於本教程

在本系列教程中，您將構建一個名為`Acme.BookStore`. 此應用程序用於管理書籍及其作者的列表。它是使用以下技術開發的：

* **Entity Framework Core**作為 ORM 提供者。
* **Angular**作為 UI 框架。

本教程分為以下幾個部分；

* [第 1 部分：創建服務器端](https://docs.abp.io/en/abp/latest/Tutorials/Part-1)
* [第 2 部分：圖書列表頁面](https://docs.abp.io/en/abp/latest/Tutorials/Part-2)
* [第 3 部分：創建、更新和刪除書籍](https://docs.abp.io/en/abp/latest/Tutorials/Part-3)
* [第 4 部分：集成測試](https://docs.abp.io/en/abp/latest/Tutorials/Part-4)
* [第 5 部分：授權](https://docs.abp.io/en/abp/latest/Tutorials/Part-5)
* [第 6 部分：作者：領域層](https://docs.abp.io/en/abp/latest/Tutorials/Part-6)
* [第 7 部分：作者：數據庫集成](https://docs.abp.io/en/abp/latest/Tutorials/Part-7)
* [第 8 部分：作者：應用程序層](https://docs.abp.io/en/abp/latest/Tutorials/Part-8)
* **第 9 部分：作者：用戶界面（本部分）**
* [第 10 部分：書與作者的關係](https://docs.abp.io/en/abp/latest/Tutorials/Part-10)

### 下載源代碼

本教程根據您的**UI**和**數據庫**首選項有多個版本。我們準備了幾個要下載的源代碼組合：

* [帶有 EF Core 的 MVC（Razor Pages）UI](https://github.com/abpframework/abp-samples/tree/master/BookStore-Mvc-EfCore)
* [帶有 EF Core 的 Blazor UI](https://github.com/abpframework/abp-samples/tree/master/BookStore-Blazor-EfCore)
* [帶有 MongoDB 的 Angular UI](https://github.com/abpframework/abp-samples/tree/master/BookStore-Angular-MongoDb)

## 介紹

這部分解釋瞭如何為`Author`前面部分介紹的實體創建 CRUD 頁面。

## 作者管理頁面

運行以下命令行以創建一個新模塊，`AuthorModule`在 angular 應用程序的根文件夾中命名：

```
yarn ng generate module author --module app --routing --route authors
```

此命令應產生以下輸出：

```
> yarn ng generate module author --module app --routing --route authors

yarn run v1.19.1
$ ng generate module author --module app --routing --route authors
CREATE src/app/author/author-routing.module.ts (344 bytes)
CREATE src/app/author/author.module.ts (349 bytes)
CREATE src/app/author/author.component.html (21 bytes)
CREATE src/app/author/author.component.spec.ts (628 bytes)
CREATE src/app/author/author.component.ts (276 bytes)
CREATE src/app/author/author.component.scss (0 bytes)
UPDATE src/app/app-routing.module.ts (1396 bytes)
Done in 2.22s.
```

### 作者模塊

打開`/src/app/author/author.module.ts`並替換如下內容：

```
import { NgModule } from '@angular/core';
import { SharedModule } from '../shared/shared.module';
import { AuthorRoutingModule } from './author-routing.module';
import { AuthorComponent } from './author.component';
import { NgbDatepickerModule } from '@ng-bootstrap/ng-bootstrap';

@NgModule({
  declarations: [AuthorComponent],
  imports: [SharedModule, AuthorRoutingModule, NgbDatepickerModule],
})
export class AuthorModule {}
```

* 添加了`SharedModule`. `SharedModule`導出一些創建用戶界面所需的常用模塊。
* `SharedModule`已經導出了`CommonModule`，所以我們已經刪除了`CommonModule`.
* 添加`NgbDatepickerModule`了稍後將在作者創建和編輯表單中使用的內容。

### 菜單定義

打開`src/app/route.provider.ts`文件並添加以下菜單定義：

```
{
  path: '/authors',
  name: '::Menu:Authors',
  parentName: '::Menu:BookStore',
  layout: eLayoutType.application,
  requiredPolicy: 'BookStore.Authors',
}
```

最終的`configureRoutes`函數聲明應該如下：

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
        requiredPolicy: 'BookStore.Books',
      },
      {
        path: '/authors',
        name: '::Menu:Authors',
        parentName: '::Menu:BookStore',
        layout: eLayoutType.application,
        requiredPolicy: 'BookStore.Authors',
      },
    ]);
  };
}
```

### 服務代理生成

[ABP CLI](https://docs.abp.io/en/abp/latest/CLI)提供了`generate-proxy`為您的 HTTP API 生成客戶端代理的命令，以便從客戶端輕鬆使用您的 HTTP API。在運行`generate-proxy`命令之前，您的主機必須已啟動並正在運行。

在`angular`文件夾中運行以下命令：

```
abp generate-proxy
```

此命令為作者服務和相關模型 (DTO) 類生成服務代理：

![書店角度服務代理作者](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/en/Tutorials/images/bookstore-angular-service-proxy-author-2.png)

### 作者組件

打開`/src/app/author/author.component.ts`文件並替換如下內容：

```
import { Component, OnInit } from '@angular/core';
import { ListService, PagedResultDto } from '@abp/ng.core';
import { AuthorService, AuthorDto } from '@proxy/authors';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { NgbDateNativeAdapter, NgbDateAdapter } from '@ng-bootstrap/ng-bootstrap';
import { ConfirmationService, Confirmation } from '@abp/ng.theme.shared';

@Component({
  selector: 'app-author',
  templateUrl: './author.component.html',
  styleUrls: ['./author.component.scss'],
  providers: [ListService, { provide: NgbDateAdapter, useClass: NgbDateNativeAdapter }],
})
export class AuthorComponent implements OnInit {
  author = { items: [], totalCount: 0 } as PagedResultDto<AuthorDto>;

  isModalOpen = false;

  form: FormGroup;

  selectedAuthor = {} as AuthorDto;

  constructor(
    public readonly list: ListService,
    private authorService: AuthorService,
    private fb: FormBuilder,
    private confirmation: ConfirmationService
  ) {}

  ngOnInit(): void {
    const authorStreamCreator = (query) => this.authorService.getList(query);

    this.list.hookToQuery(authorStreamCreator).subscribe((response) => {
      this.author = response;
    });
  }

  createAuthor() {
    this.selectedAuthor = {} as AuthorDto;
    this.buildForm();
    this.isModalOpen = true;
  }

  editAuthor(id: string) {
    this.authorService.get(id).subscribe((author) => {
      this.selectedAuthor = author;
      this.buildForm();
      this.isModalOpen = true;
    });
  }

  buildForm() {
    this.form = this.fb.group({
      name: [this.selectedAuthor.name || '', Validators.required],
      birthDate: [
        this.selectedAuthor.birthDate ? new Date(this.selectedAuthor.birthDate) : null,
        Validators.required,
      ],
    });
  }

  save() {
    if (this.form.invalid) {
      return;
    }

    if (this.selectedAuthor.id) {
      this.authorService
        .update(this.selectedAuthor.id, this.form.value)
        .subscribe(() => {
          this.isModalOpen = false;
          this.form.reset();
          this.list.get();
        });
    } else {
      this.authorService.create(this.form.value).subscribe(() => {
        this.isModalOpen = false;
        this.form.reset();
        this.list.get();
      });
    }
  }

  delete(id: string) {
    this.confirmation.warn('::AreYouSureToDelete', '::AreYouSure')
        .subscribe((status) => {
          if (status === Confirmation.Status.confirm) {
            this.authorService.delete(id).subscribe(() => this.list.get());
          }
	    });
  }
}
```

打開`/src/app/author/author.component.html`並替換如下內容：

```
<div class="card">
  <div class="card-header">
    <div class="row">
      <div class="col col-md-6">
        <h5 class="card-title">
          {{ '::Menu:Authors' | abpLocalization }}
        </h5>
      </div>
      <div class="text-right col col-md-6">
        <div class="text-lg-right pt-2">
          <button id="create" class="btn btn-primary" type="button" (click)="createAuthor()">
            <i class="fa fa-plus mr-1"></i>
            <span>{{ '::NewAuthor' | abpLocalization }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="card-body">
    <ngx-datatable [rows]="author.items" [count]="author.totalCount" [list]="list" default>
      <ngx-datatable-column
        [name]="'::Actions' | abpLocalization"
        [maxWidth]="150"
        [sortable]="false"
      >
        <ng-template let-row="row" ngx-datatable-cell-template>
          <div ngbDropdown container="body" class="d-inline-block">
            <button
              class="btn btn-primary btn-sm dropdown-toggle"
              data-toggle="dropdown"
              aria-haspopup="true"
              ngbDropdownToggle
            >
              <i class="fa fa-cog mr-1"></i>{{ '::Actions' | abpLocalization }}
            </button>
            <div ngbDropdownMenu>
              <button ngbDropdownItem (click)="editAuthor(row.id)">
                {{ '::Edit' | abpLocalization }}
              </button>
              <button ngbDropdownItem (click)="delete(row.id)">
                {{ '::Delete' | abpLocalization }}
              </button>
            </div>
          </div>
        </ng-template>
      </ngx-datatable-column>
      <ngx-datatable-column [name]="'::Name' | abpLocalization" prop="name"></ngx-datatable-column>
      <ngx-datatable-column [name]="'::BirthDate' | abpLocalization">
        <ng-template let-row="row" ngx-datatable-cell-template>
          {{ row.birthDate | date }}
        </ng-template>
      </ngx-datatable-column>
    </ngx-datatable>
  </div>
</div>

<abp-modal [(visible)]="isModalOpen">
  <ng-template #abpHeader>
    <h3>{{ (selectedAuthor.id ? '::Edit' : '::NewAuthor') | abpLocalization }}</h3>
  </ng-template>

  <ng-template #abpBody>
    <form [formGroup]="form" (ngSubmit)="save()">
      <div class="form-group">
        <label for="author-name">Name</label><span> * </span>
        <input type="text" id="author-name" class="form-control" formControlName="name" autofocus />
      </div>

      <div class="form-group">
        <label>Birth date</label><span> * </span>
        <input
          #datepicker="ngbDatepicker"
          class="form-control"
          name="datepicker"
          formControlName="birthDate"
          ngbDatepicker
          (click)="datepicker.toggle()"
        />
      </div>
    </form>
  </ng-template>

  <ng-template #abpFooter>
    <button type="button" class="btn btn-secondary" abpClose>
      {{ '::Close' | abpLocalization }}
    </button>

    <button class="btn btn-primary" (click)="save()" [disabled]="form.invalid">
      <i class="fa fa-check mr-1"></i>
      {{ '::Save' | abpLocalization }}
    </button>
  </ng-template>
</abp-modal>
```

### 本地化

這個頁面使用了一些我們需要聲明的本地化鍵。打開項目文件夾`en.json`下的`Localization/BookStore`文件`Acme.BookStore.Domain.Shared`並添加以下條目：

```
"Menu:Authors": "Authors",
"Authors": "Authors",
"AuthorDeletionConfirmationMessage": "Are you sure to delete the author '{0}'?",
"BirthDate": "Birth date",
"NewAuthor": "New author"
```

### 運行應用程序

運行並登錄到應用程序。**由於您還沒有權限，因此您無法看到菜單項。**轉到`identity/roles`頁面，單擊*操作*按鈕並為**管理員角色**選擇*權限*操作：

![書店作者權限](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/en/Tutorials/images/bookstore-author-permissions.png)

如您所見，admin 角色還沒有*作者管理*權限。單擊複選框並保存模式以授予必要的權限。**刷新頁面**後，您將在主菜單中的*Book Store*下看到*Authors*菜單項：

![書店作者頁面](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/en/Tutorials/images/bookstore-angular-authors-page.png)

就這樣！這是一個完整的 CRUD 頁面，您可以創建、編輯和刪除作者。

> **提示**：如果您`.DbMigrator`在定義新權限後運行控制台應用程序，它會自動將這些新權限授予 admin 角色，您無需自己手動授予權限。

## 下一部分

請參閱本教程的[下一部分](https://docs.abp.io/en/abp/latest/Tutorials/Part-10)。

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [ABP](/jakeuj/Tags?qq=ABP)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
