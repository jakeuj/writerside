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

## 與 ABP 官方 EF Core 做法的關聯

雖然這裡是修改 ABP Suite 的 Repository 樣板，但整體思路其實和 ABP 官方文件中的建議是一致的：

- 每個模組應該有自己的 `IXXXDbContext` 介面 + `XXXDbContext` 類別，介面繼承 `IEfCoreDbContext`，並加上 `ConnectionStringName`。
- DbContext 類別繼承 `AbpDbContext<TDbContext>`，實作對應的 `IXXXDbContext` 介面。
- 自訂的 Repository 一律繼承 `EfCoreRepository<IXXXDbContext, TEntity, TKey>`（注意：**優先使用 DbContext 介面，而不是直接綁具體 DbContext 類別**）。
- 如果需要，可以透過 `options.SetDefaultRepositoryClasses(...)` 自訂一個自己的 Repository Base 類別，統一讓所有 Repository 去繼承它。

本篇做法就是沿用這個精神，只是把「要綁定哪個 DbContext」這件事，**直接鎖死在 ABP Suite 的 EfCoreRepository 樣板裡**，避免 Suite 自行判斷 DbContext 時選錯。

### 實測補充：DbSet 會穩定生成到正確 DbContext

完成上述 Template 修改之後，實測結果如下：

- 每個模組有自己的 `IXxxDbContext` + `XxxDbContext`。
- ABP Suite 產生的 `EfCore%%entity-name%%Repository`{ignore-vars="true"} 一律繼承你指定的 `YourActualDbContextName` 對應的 Repository Base。
- 由於 Repository 參數型別已經**明確綁定到正確的 DbContext 介面 / 類別**，後續在 ABP Suite 中新增實體時，對應的 `DbSet<TEntity>` 也會**穩定地被產生到對的那個 DbContext**，不再出現「有時候被生到別的 DbContext」那種看似隨機的情況。

換句話說，這個 Template 調整不只是讓 Repository 不會綁錯 DbContext，同時也「順便修正了」 ABP Suite 產生 `DbSet` 時的歸屬問題，整體行為會變得更可預期、更符合模組化的設計。

### 已知限制：Manager.Extended override CRUD 的欄位變更問題

目前實測下來，這樣修改 Template 本身不會造成 build 問題，但有一個**與 ABP Suite 產生碼相關的已知限制**需要注意：

- 如果你有使用 `Manager.Extended`（或類似的 `*Manager` 擴充類別），並且在裡面 **override 了 CRUD 方法**（例如 `CreateAsync`, `UpdateAsync`）。
- 之後你透過 ABP Suite 對該實體「新增或刪減欄位」時，Suite 會更新基底 Manager 的方法簽章，但**不會自動更新你在 `Manager.Extended` 裡手寫的 override 方法參數列表**。
- 結果就是：基底類別的方法簽章已經包含新欄位，而 `Manager.Extended` 裡的 override 仍然是舊版本 → 簽章不相符 → 專案在編譯時會直接失敗。

目前的解方是：

1. 每次用 ABP Suite 調整實體欄位後，除了檢查實體 / DTO / AppService 之外，**要記得同步檢查所有 `*Manager.Extended` 的 override 方法**。
2. 依照最新產生的基底 Manager 類別，把 override 方法的參數補上新欄位（或移除不再存在的欄位），讓方法簽章重新對齊。

如果想減少這個問題的影響，可以考慮：

- 儘量不要在 Extended 類別中直接 override 大顆的 CRUD 方法，而是改成在 Extended 裡多包一層自己的方法，再呼叫基底 CRUD。
- 或者把「調整欄位後檢查 `Manager.Extended` override 簽章」當成固定流程的一部分，避免在 CI/CD 才發現 build 失敗。
## 重點總結

| 項目 | 說明 |
|------|------|
| ✔ 修改非常簡單 | 只要取代 Token 成你想要綁定的 DbContext 名稱即可 |
| ✔ 不依賴具體專案名稱 | 可用真實名稱，也可用 Token，完全由開發者決定 |
| ✔ 避免 ABP Suite 選錯 DbContext | 強制將 Repository 生到你指定的位置 |
| ✔ 適用於所有多 DbContext 場景 | 例如 Domain 模組拆分、Microservice 模組、各模組獨立 DbContext |

