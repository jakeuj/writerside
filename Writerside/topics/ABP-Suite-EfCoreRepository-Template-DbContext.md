# ABP Suite：EfCoreRepository Template 強制指定使用特定 DbContext

在多 DbContext 的 ABP 專案架構中，ABP Suite 會自動判斷某個實體應該綁定哪個 DbContext，但判斷邏輯不一定準確。

若專案中包含多個 DbContext（例如 `MainDbContext`、`DigitalDbContext`、`ModuleXDbContext`），Suite 有機會選錯。

最簡單、最可靠的方式，就是透過修改 Template，手動指定 Repository 永遠使用你要的主 DbContext。

## 情境說明

ABP Suite 預設 Repository Template 會使用以下 Token 來生成 DbContext 類別名稱：

<code-block ignore-vars="true">
%%only-project-name%%DbContext
</code-block>

例如：`SampleProjectNameDbContext`

但若你的主 DbContext 實際名稱並非遵循這個預設格式，例如：

- `SampleProjectNameAppDbContext`
- `MainDbContext`
- `MyCompanyMainEfCoreDbContext`
- `CoreHostDbContext`

那麼 Suite 將會持續生成到錯誤的 DbContext。

## 解決方式（通用做法）

修改 Template：`Server.Repository.EfCoreRepository.txt`

搜尋以下 Token：

<code-block ignore-vars="true">
%%only-project-name%%DbContext
</code-block>

通常會出現 **兩個位置**：

1. `EfCoreRepository` 基底類別的 DbContext
2. 建構子中 `IDbContextProvider&lt;&gt;` 的 DbContext

將它替換成你真正想要綁定的 DbContext 名稱，例如：

- `MainDbContext`

或你專案採用 Token 風格，也可改成其他 Token（依照自己專案的實際主 DbContext 名稱來調整）。

## 最終成功版本範例

以下展示修改後的樣板（此處使用 `YourActualDbContextName` 作為示例，請替換成你專案的真實名稱）：

<code-block lang="c#" ignore-vars="true">
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
        : EfCoreRepository&lt;YourActualDbContextName, %%entity-name%%, %%primary-key%%&gt;
        %%&lt;if:PreserveCustomCodeNotEnabled&gt;%%, I%%entity-name%%Repository%%&lt;/if:PreserveCustomCodeNotEnabled&gt;%%
    {
        public EfCore%%entity-name%%Repository%%custom-code-base%%(
            IDbContextProvider&lt;YourActualDbContextName&gt; dbContextProvider)
            : base(dbContextProvider)
        {

        }

        %%bulk-delete-all-method%%

        %%child-master-list-methods%%

        %%child-master-navigation-methods%%

        %%navigation-methods%%
        public virtual async Task&lt;List&lt;%%entity-name%%&gt;&gt; GetListAsync(
            string? filterText = null, %%dto-field-names-with-type%%%%&lt;if:HasFilterableProperties&gt;%%,%%&lt;/if:HasFilterableProperties&gt;%%
            string? sorting = null,
            int maxResultCount = int.MaxValue,
            int skipCount = 0,
            CancellationToken cancellationToken = default)
        {
            var query = ApplyFilter(
                (await GetQueryableAsync()),
                 filterText%%&lt;if:HasFilterableProperties&gt;%%, %%&lt;/if:HasFilterableProperties&gt;%%%%dto-field-names%%);

            query = query.OrderBy(
                string.IsNullOrWhiteSpace(sorting)
                    ? %%entity-name%%Consts.GetDefaultSorting(false)
                    : sorting
            );

            return await query.PageBy(skipCount, maxResultCount)
                              .ToListAsync(cancellationToken);
        }

        public virtual async Task&lt;long&gt; GetCountAsync(
            string? filterText = null, %%dto-field-names-with-type-include-navigation-properties%%%%&lt;if:HasAnyFilterableProperties&gt;%%,%%&lt;/if:HasAnyFilterableProperties&gt;%%
            CancellationToken cancellationToken = default)
        {
            %%get-count-query%%
            return await query.LongCountAsync(GetCancellationToken(cancellationToken));
        }

        protected virtual IQueryable&lt;%%entity-name%%&gt; ApplyFilter(
            IQueryable&lt;%%entity-name%%&gt; query,
            string? filterText = null%%&lt;if:HasFilterableProperties&gt;%%,%%&lt;/if:HasFilterableProperties&gt;%% %%dto-field-names-with-type%%)
        {
            return query
                %%apply-filter-text%%%%filter-fields%%;
        }
    }
}
</code-block>

## 重點總結

| 項目 | 說明 |
|------|------|
| ✔ 修改非常簡單 | 只要取代 Token 成你想要綁定的 DbContext 名稱即可 |
| ✔ 不依賴具體專案名稱 | 可用真實名稱，也可用 Token，完全由開發者決定 |
| ✔ 避免 ABP Suite 選錯 DbContext | 強制將 Repository 生到你指定的位置 |
| ✔ 適用於所有多 DbContext 場景 | 例如 Domain 模組拆分、Microservice 模組、各模組獨立 DbContext |

