# ABP.IO WEB應用程式框架 Setting

> **原文發布日期:** 2022-11-04
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/11/04/Abp-Setting-Manager
> **標籤:** 無

---

筆記下 ABP 內建的設置管理系統

## 簡介

開發系統時我們很常需要設定一些值

稍微列舉一些可能的做法

- 寫死在程式碼中
- appsetting.json
  - IConfiguration
  - ``IOptions<T>``
- Database
  - 自訂 Table 在需要時當作資料讀出來

## ABP

ABP 提供了內建的 Settings 功能來處理設定值

好處是可以用比較統一的方式來使用這些設定

提供彈性的設定值管理機制提高後續系統的可維護性與擴充性

免去自己設計相關 table 來存取這些設定的功夫

P.S. 另外會自動對設定值進行快取

## 概念

- Settings: 目前正在介紹的東西 (功能與模組)
- SettingProvider: 建立這個東西來定義設定名稱 (key)
- ISettingProvider: 注入這東西來讀取設定值 (寫死唯讀)
- ISettingManager: 注入這東西來寫入設定值

### Settings

要用這功能起手式是先 create 一個 xxxSettingProvider.cs

### SettingProvider

主要是提供設定值的key名稱，之後要讀取就靠這名子

也有提供一些額外功能比如：預設值，自動加解密

這邊簡單提一下加密，就是會用 appsetting 裡面的 StringEncryption 當作加解密的鑰匙

反過來說就是你把smtp密碼存到 appsetting 或是資料庫時必須先加密

不然讀取的時候，因為會先進行解密動作，最後的值會是錯的！

```
public class MySettingProvider : SettingDefinitionProvider
{
    public override void Define(ISettingDefinitionContext context)
    {
        context.Add(
            new SettingDefinition("MyMoney", "999999999")
        );
    }
}
```

### ISettingProvider

設定完上面的 xxxSettingProvider 後其實就可以讀取設定值了

簡單搬一段 Sample Code 抄一抄應該沒甚麼好講的

```
public class MyService
{
    private readonly ISettingProvider _settingProvider;

    //Inject ISettingProvider in the constructor
    public MyService(ISettingProvider settingProvider)
    {
        _settingProvider = settingProvider;
    }

    public async Task FooAsync()
    {
        //Get an int value or the default value (0) if not set
        int port = (await _settingProvider.GetAsync<int>("MyMoney"));
    }
}

```

但是寫到這邊其實我們還只是把值寫死在程式碼裡面

這時候我們可以來了解一下 ABP Setting 讀取設定值大概做了甚麼事情

1. DefaultValueSettingValueProvider:
   Gets the value from the default value of the setting definition, if set (see the SettingDefinition section above).
2. ConfigurationSettingValueProvider:
   Gets the value from the IConfiguration service.
3. GlobalSettingValueProvider:
   Gets the global (system-wide) value for a setting, if set.
4. TenantSettingValueProvider:
   Gets the setting value for the current tenant, if set (see the multi-tenancy document).
5. UserSettingValueProvider:
   Gets the setting value for the current user, if set (see the current user document).

承1) 講中文就是會先把剛剛我們寫死在程式裡面的值讀出來當作預設值

用以上的例子來說，此時我們直接讀取就會拿到 `999999999`

承2) But, 實際上會接著讀取 appsetting.json 裡面的 Settings 區塊

所以其實我們此時可以在 appsetting 加入以下設定就會拿到新的設定值了

```
"Settings": {
    "MyMoney": "987654321"
  }
```

承3) 這邊會開始嘗試讀取資料庫內的資料

實際上我們可以在資料庫中看到一張表 [AbpSettings]

裡頭大概長這樣

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/fcfa9927-4627-4bca-a516-bee17968b4db/1667552265.png.png)

其中 Name 就是設定值的名稱，拿剛剛上面的範例來說就是 `MyMoney`

如果沒有對應的資料，那就會拿到剛剛 appsetting 中的 987654321

此時我們就可以用資料庫來管理設定值

簡單介紹一下 [ProviderName] 對應如下

- `DefaultValueSettingValueProvider`: "**D**".
- `ConfigurationSettingValueProvider`: "**C**".
- `GlobalSettingValueProvider`: "**G**".
- `TenantSettingValueProvider`: "**T**".
- `UserSettingValueProvider`: "**U**".

講中文就是全局設定或是 By 使用者個人的設定

如果是 By 使用者，則 ProviderKey 就會是 UserId

### ISettingManager

手動建 DB 設定資料畢竟不是人做的事情

此時我們就可以使用 ISettingManager 來進行設定值的寫入操作

P.S. 因為會自動對設定值進行快取，所以建議統一由 ISettingManager 修改設定

```
using System;
using System.Threading.Tasks;
using Volo.Abp.DependencyInjection;
using Volo.Abp.SettingManagement;

namespace Demo
{
    public class MyService : ITransientDependency
    {
        private readonly ISettingManager _settingManager;

        //Inject ISettingManager service
        public MyService(ISettingManager settingManager)
        {
            _settingManager = settingManager;
        }

        public async Task FooAsync()
        {
            //Get/set a global and default setting value

            await _settingManager.SetGlobalAsync("MyMoney", "123456789");

            string money =
                await _settingManager.GetOrNullGlobalAsync("MyMoney");
        }
    }
}
```

執行 `SetGlobalAsync` 就會在資料庫 AbpSettings 建立/修改 資料

{Name: "MyMoney", ProviderName: "G", Value: "123456789"}

也可以依照需求 設定/讀取，By 租戶/用戶 的設定值

提供相對彈性的 設定/讀取 功能

### 參照

[Settings | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Settings)

[Modules/Setting Management | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Modules/Setting-Management)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- Setting

- 回首頁

---

*本文章從點部落遷移至 Writerside*
