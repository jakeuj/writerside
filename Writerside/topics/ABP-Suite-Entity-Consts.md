# ABP Suite：自訂 Entity Consts 的最佳做法

## 為什麼要修改 Server.Entity.EntityConsts.txt

ABP Suite 會根據「實體欄位」自動產生：

- `XXXConsts` 類別
- `MaxLength` 常數（例如 `PoNoMaxLength = 50`）
- 預設排序方法（`GetDefaultSorting`）

但是：

- **每次重新產生 CRUD 時，`XXXConsts.cs` 都會被覆寫**
- 如果你在其中加入自訂常數（例如工廠代號、固定清單、domain rule），就會消失

為了避免覆蓋，你需要：

1. 調整 Suite 的模板，讓 `XXXConsts` 改成 `partial class`
2. 使用外部 `partial` 擴充檔案放常數

## 修改 Server.Entity.EntityConsts.txt

在 Suite 介面中編輯模板：

**Templates → MVC → EfCore → Server.Entity.EntityConsts.txt**

確保模板內容為：

```csharp
namespace %%solution-namespace%%.%%entity-namespace%%
{
    public static partial class %%entity-name%%Consts
    {
        private const string DefaultSorting = "%%default-sorting%%";
        
        public static string GetDefaultSorting(bool withEntityName)
        {
            return string.Format(DefaultSorting, withEntityName ? "%%entity-name%%." : string.Empty);
        }
        
        %%consts%%
    }
}
```

> **重點**
> 
> 將類別改為 `static partial class`（ABP 預設沒有 `partial`）
> 
> 這樣 Suite 建檔時不會擋住你自己額外的 Consts 擴充
{style="note"}

## 使用 Partial Class 擴充自訂常數（最佳實務）

新增檔案：

`/VenderPortal/PurchaseOrders/PurchaseOrderConsts.Extensions.cs`

寫入：

```csharp
namespace VenderPortal.PurchaseOrders
{
    public static partial class PurchaseOrderConsts
    {
        public const string PlantChongqing = "重慶";
        public const string PlantKunshan = "昆山";
        
        public static readonly HashSet<string> ValidPlants = new HashSet<string>
        {
            PlantChongqing,
            PlantKunshan,
        };
    }
}
```

### 優點

- ✅ 永不被 ABP Suite 覆寫
- ✅ 不修改 Suite 的自動產生邏輯
- ✅ 適合放 domain rule、固定字串、固定清單
- ✅ 維持清楚的分層（產生 vs 自定義）

## Suite 模板修改後實際生成結果

### ABP Suite 生成：

```csharp
public static partial class PurchaseOrderConsts
{
    private const string DefaultSorting = "{0}CreationTime desc";
    
    public static string GetDefaultSorting(bool withEntityName)
    {
        return string.Format(DefaultSorting, withEntityName ? "PurchaseOrder." : string.Empty);
    }
    
    public const int PoNoMaxLength = 50;
    public const int WorkOrderMaxLength = 50;
    public const int PoPnMaxLength = 50;
    // ...
}
```

### 你的擴充：

```csharp
public static partial class PurchaseOrderConsts
{
    public const string PlantChongqing = "重慶";
    public const string PlantKunshan = "昆山";
    
    public static readonly HashSet<string> ValidPlants = new HashSet<string>
    {
        PlantChongqing,
        PlantKunshan,
    };
}
```

> **編譯後會合併成一個類別**
> 
> 無須額外設定
{style="tip"}

## 延伸用法（可選）

### 在 DTO 驗證中引用常數

```csharp
[Required]
[MaxLength(PurchaseOrderConsts.PlantMaxLength)]
[AllowedValues(PurchaseOrderConsts.ValidPlants)]
public string Plant { get; set; }
```

### 在 Domain Layer 使用

```csharp
if (!PurchaseOrderConsts.ValidPlants.Contains(plant))
{
    throw new BusinessException("InvalidPlant").WithData("Plant", plant);
}
```

### 在 AppService 中做 mapping 或 filter

```csharp
var validItems = query.Where(po => 
    PurchaseOrderConsts.ValidPlants.Contains(po.Plant)
);
```

## 注意事項

> **重要提醒**
> 
> - ❌ 不要修改 Suite 自動產生的檔案（會被覆蓋）
> - ✅ 自訂內容請全部放在 `*.Extensions.cs`（或你喜歡的命名）
> - ✅ 若你以後換 ABP 版本、更新 Suite，不會影響擴充檔案
> - ✅ 如果你有多個模組，可以用相同結構統一管理常數
> - ✅ 若有大量常數，可分拆成多個 partial 段落（例如 Enum-like 常數群組）
{style="warning"}

## 結論

使用：

1. **修改模板** → `partial class`
2. **自訂常數放到外部 partial 檔案**

是目前 ABP Suite 最穩定、不會被覆寫、可維護性最高的做法。

