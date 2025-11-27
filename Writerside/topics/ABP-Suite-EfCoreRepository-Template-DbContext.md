# ABP Suite：EfCoreRepository Template 強制指定使用特定 DbContext

在多 DbContext 的 ABP 專案架構中，ABP Suite 會自動判斷某個實體應該綁定哪個 DbContext，但判斷邏輯不一定準確。

若專案中包含多個 DbContext（例如 `MainDbContext`、`DigitalDbContext`、`ModuleXDbContext`），Suite 有機會選錯。

最簡單、最可靠的方式，就是透過修改 Template，手動指定 Repository 永遠使用你要的主 DbContext。

## 情境說明

ABP Suite 預設 Repository Template 會使用：

```
%%only-project-name%%DbContext
```

來生成 DbContext 類別名稱。例如：`SampleProjectNameDbContext`

但若你的主 DbContext 實際名稱並非遵循這個預設格式，例如：

- `SampleProjectNameAppDbContext`
- `MainDbContext`
- `MyCompanyMainEfCoreDbContext`
- `CoreHostDbContext`

那麼 Suite 將會持續生成到錯誤的 DbContext。

## 解決方式（通用做法）

修改 Template：`Server.Repository.EfCoreRepository.txt`

搜尋：`%%only-project-name%%DbContext`

通常會出現 **兩個位置**：

1. `EfCoreRepository` 基底類別的 DbContext
2. 建構子中 `IDbContextProvider<>` 的 DbContext

將它替換成你真正想要綁定的 DbContext 名稱，例如：

- `MainDbContext`

或你專案採用 Token 風格，也可改成：

- `%%only-project-name%%AppDbContext`
- `%%project-prefix%%EfCoreDbContext`
- `%%my-custom-dbcontext-token%%`

你只需要 **依照自己專案的實際主 DbContext 名稱來調整**。

## 最終成功版本範例

以下展示修改後的樣板（此處使用 `YourActualDbContextName` 作為示例，請替換成你專案的真實名稱）：

```c#
using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Dynamic.Core;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Volo.Abp.Domain.Repositories.EntityFrameworkCore;
using Volo.Abp.EntityFrameworkCore;
using %%solution-namespace%%.%%dbcontext-namespace%%;

namespace %%solution-namespace%%.%%entity-namespace%%
{
    public %%custom-code-abstract-modifier%% class EfCore%%entity-name%%Repository%%custom-code-base%% 
        : EfCoreRepository<YourActualDbContextName, %%entity-name%%, %%primary-key%%>
        %%<if:PreserveCustomCodeNotEnabled>%%, I%%entity-name%%Repository%%</if:PreserveCustomCodeNotEnabled>%%
    {
        public EfCore%%entity-name%%Repository%%custom-code-base%%(
            IDbContextProvider<YourActualDbContextName> dbContextProvider)
            : base(dbContextProvider)
        {

        }
        
        %%bulk-delete-all-method%%
        
        %%child-master-list-methods%%
        
        %%child-master-navigation-methods%%
        
        %%navigation-methods%%
        public virtual async Task<List<%%entity-name%%>> GetListAsync(
            string? filterText = null, %%dto-field-names-with-type%%%%<if:HasFilterableProperties>%%,%%</if:HasFilterableProperties>%%
            string? sorting = null,
            int maxResultCount = int.MaxValue,
            int skipCount = 0,
            CancellationToken cancellationToken = default)
        {
            var query = ApplyFilter(
                (await GetQueryableAsync()),
                 filterText%%<if:HasFilterableProperties>%%, %%</if:HasFilterableProperties>%%%%dto-field-names%%);

            query = query.OrderBy(
                string.IsNullOrWhiteSpace(sorting)
                    ? %%entity-name%%Consts.GetDefaultSorting(false)
                    : sorting
            );

            return await query.PageBy(skipCount, maxResultCount)
                              .ToListAsync(cancellationToken);
        }

        public virtual async Task<long> GetCountAsync(
            string? filterText = null, %%dto-field-names-with-type-include-navigation-properties%%%%<if:HasAnyFilterableProperties>%%,%%</if:HasAnyFilterableProperties>%%
            CancellationToken cancellationToken = default)
        {
            %%get-count-query%%
            return await query.LongCountAsync(GetCancellationToken(cancellationToken));
        }

        protected virtual IQueryable<%%entity-name%%> ApplyFilter(
            IQueryable<%%entity-name%%> query,
            string? filterText = null%%<if:HasFilterableProperties>%%,%%</if:HasFilterableProperties>%% %%dto-field-names-with-type%%)
        {
            return query
                %%apply-filter-text%%%%filter-fields%%;
        }
    }
}
```

## 重點總結

| 項目 | 說明 |
|------|------|
| ✔ 修改非常簡單 | 只要取代 `%%only-project-name%%DbContext` 成你想要綁定的 DbContext 名稱即可 |
| ✔ 不依賴具體專案名稱 | 可用真實名稱，也可用 Token，完全由開發者決定 |
| ✔ 避免 ABP Suite 選錯 DbContext | 強制將 Repository 生到你指定的位置 |
| ✔ 適用於所有多 DbContext 場景 | 例如 Domain 模組拆分、Microservice 模組、各模組獨立 DbContext |

