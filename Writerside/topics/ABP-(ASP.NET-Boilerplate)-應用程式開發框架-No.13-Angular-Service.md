# ABP No.13 Angular Service

> **原文發布日期:** 2019-04-23
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/04/23/abp13
> **標籤:** 無

---

記錄從ABP做好應用服務後到Angular新增出頁面的過程

Server 端 - 專案領域層

這裡假設已準備好一個應用服務層 (PayEventAppService)

權限設定在各別聚合根內較好管理，但為了方便記錄這裡用內建的使用者授權設定

1.設定權限名稱

Core.Authorization.PermissionNames.cs

```

public const string Pages_Events = "Pages.Events";
```

2.於資料庫新增權限資料

Core.Authorization.OBManAuthorizationProvider.cs

```

context.CreatePermission(PermissionNames.Pages_Events, L("Events"));
```

3.多國語系檔

英文：Core.Localization.SourceFiles.OBMan.xml

```

<text name="Filter">Filter</text>
<text name="Events">Events</text>
```

中文：Core.Localization.SourceFiles.OBMan-zh-Hans.xml

```

<text name="EditTenant">编辑租户</text>
<text name="Events">活動</text>
```

裡面就XML文件，Key Value Pair，

這邊先把剛剛OBManAuthorizationProvider.cs裡面的L("Events")做一下翻譯，

之後Angular裡面有用到L('XXX')的有需要可以自己加到這邊來翻譯

4.應用服務層-檢查權限

使用AbpAuthorize屬性

```

[AbpAuthorize("Pages.Events")]
public void CreateUser(CreateUserInput input)
{
    //A user can not execute this method if he is not granted the "Pages.Events" permission.
}
```

---

Client 端 - Angular專案

事前準備：[Angular Application](https://dotblogs.com.tw/jakeuj/2018/12/26/angularapplication)

1.增加巡覽設定

>.\angular\src\app\layout\sidebar-nav.component.ts

```

new MenuItem(this.l('Roles'), 'Pages.Roles', 'local_offer', '/app/roles'),
// add
new MenuItem(this.l('Events'), 'Pages.Events', 'local_offer', '/app/events'),
new MenuItem(this.l('About'), '', 'info', '/app/about'),
```

2.新增component

>ng g component Events

3.routing設定

>.\angular\src\app\app-routing.module.ts

```

import { ChangePasswordComponent } from './users/change-password/change-password.component';
//add
import {EventsComponent} from "@app/events/events.component";

// ...
{ path: 'tenants', component: TenantsComponent, data: { permission: 'Pages.Tenants' }, canActivate: [AppRouteGuard] },
// add
{ path: 'events', component: EventsComponent, data: { permission: 'Pages.Events' }, canActivate: [AppRouteGuard] },
{ path: 'about', component: AboutComponent },
```

4.Start

參照：[JetBrains Rider Angular NPM Yarn Launch Settings Profile](https://dotblogs.com.tw/jakeuj/2019/03/26/riderangularlaunch)

這邊應該可以看到左側有出現Events並可以點進去看到右邊有events works!

右上角切換中文語系應該會看到左邊顯示 "活動"

到"用戶"新增一個非 admin 角色的帳號

然後重登之後應該會看不到左側 events

然後再用admin登入，點"角色"來新增一個新角色"Player"，並賦予權限 "活動"(Events)
再到"用戶"把剛剛建立的新帳號設定角色為"Player"，再重登應該就可以看到左側"活動"

---

API Proxy

前面準備了API跟顯示組件，接著要開始實作組件之前需要先處理API呼叫相關設定

5.用 nswag 更新 app service proxy

>.\angular\nswag\refresh.bat

參照：[ABP (ASP.NET Boilerplate) 應用程式開發框架 No.11 Client Proxies](https://dotblogs.com.tw/jakeuj/2019/01/18/abp11)

6.新增應用服務

>.\angular\src\shared\service-proxy.module.ts

```

ApiServiceProxies.ConfigurationServiceProxy,
// add
ApiServiceProxies.PayEventServiceProxy,
{ provide: HTTP_INTERCEPTORS, useClass: AbpHttpInterceptor, multi: true }
```

7.組件注入

```

constructor(
    injector: Injector,
    private _payEventServiceProxy: PayEventServiceProxy,
) {}
```

8.使用服務

```

ngOnInit(): void {
    _payEventServiceProxy.getAll()
    .subscribe((result: PagedResultDtoOfPayEventDto) => {
        this.result = result;
    });
}
```

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ABP
* Angular

* 回首頁

---

*本文章從點部落遷移至 Writerside*
