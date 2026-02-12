# ABP.IO 最佳實踐 Entity

> **原文發布日期:** 2023-06-28
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/06/28/ABP-Best-Practices-Entities
> **標籤:** 無

---

搬運一下官方文件

## 參照

[Best Practices/Entities | Documentation Center | ABP. IO](https://docs.abp.io/zh-Hans/abp/latest/Best-Practices/Entities)

## 實體最佳實踐 & 約定

### 實體

每個聚合根也是一個實體， 所以這些規則對聚合根也是有效的， 除非聚合根的某些規則覆蓋了它們.

- **推薦** 在 **領域層** 中定義實體.

#### 主構造函數

- **推薦** 定義一個 **主構造函數** 確保實體在創建時的有效性， 在代碼中通過主構造函數創建實體的新實例.
- **推薦** 根據需求把主構造函數定義為`public` ， `internal`或 `protected internal`. 如果它不是 `public` 的， 那麼應該由領域服務來創建實體.
- **推薦** 總是在主構造函數中初始化子集合.
- **不推薦** 在主構造函數中生成 `Guid` 鍵， 應該將其做為參數獲取， 在調用時推薦使用 `IGuidGenerator`生成新的`Guid` 值做為參數.

#### 無參構造函數

- **推薦** 總是定義 `protected` 無參構造函數與ORM兼容.

#### 引用

- **推薦** 總是通過 **id** **引用** 其他聚合根， 不要將導航屬性添加到其他聚合根中.

#### 類的其他成員

- **推薦** 總是將屬性與方法定義為 `virtual`（除了方法 `私有`）. 因為有些ORM和動態代理工具需要.
- **推薦** 保持實體在自身邊界內始終 **有效** 和 **一致**.
  - **推薦** 使用 `private`，`protected`，`internal`或 `protected internal` setter 定義屬性， 保護實體的一致性和有效性.
  - **推薦** 定義 `public`， `internal`或 `protected internal`（virtual）**方法**在必要時更改屬性值（使用非public setters時）.

### 聚合根

#### 主鍵

- **推薦** 總是使用**Id**屬性做為聚合根主鍵.
- **不推薦** 在聚合根中使用 **複合主鍵**.
- **推薦** 所有的聚合根都使用 **Guid** 類型 **主鍵**.

#### 基類

- **推薦** 根據需求繼承 `AggregateRoot<TKey>` 或以下一個審計類 （`CreationAuditedAggregateRoot<TKey>`，`AuditedAggregateRoot<TKey>` 或 `FullAuditedAggregateRoot<TKey>`）.

#### 聚合邊界

- **推薦** 聚合**盡可能小**. 大多數聚合只有原始屬性， 不會有子集合. 把這些視為設計決策：
  - 載入和保存聚合的 **性能** 與**記憶體** 成本 （請記住，聚合通常是做為一個單獨的單元被載入和保存的）. 較大的聚合會消耗更多的CPU和記憶體.
  - **一致性** & **有效性** 邊界.

### 示例

#### 聚合根

```
public class Issue : FullAuditedAggregateRoot<Guid> //使用Guid作为键/标识符
{
    public virtual string Title { get; private set; } //使用 SetTitle() 方法set
    public virtual string Text { get; set; } //可以直接set,null值也是允许的
    public virtual Guid? MilestoneId { get; set; } //引用其他聚合根
    public virtual bool IsClosed { get; private set; }
    public virtual IssueCloseReason? CloseReason { get; private set; } //一个枚举类型
    public virtual Collection<IssueLabel> Labels { get; protected set; } //子集合

    protected Issue()
    {
        /* 此构造函数是提供给ORM用来从数据库中获取实体.
         * - 无需初始化Labels集合
             因为它会被来自数据库的值覆盖.
           - It's protected since proxying and deserialization tools
             可能不适用于私有构造函数.
         */
    }

    //主构造函数
    public Issue(
        Guid id, //从调用代码中获取Guid值
        [NotNull] string title, //表示标题不能为空.
        string text = null,
        Guid? milestoneId = null) //可选参数
    {
        Id = id;
        Title = Check.NotNullOrWhiteSpace(title, nameof(title)); //验证
        Text = text;
        MilestoneId = milestoneId;

        Labels = new Collection<IssueLabel>(); //总是初始化子集合
    }

    public virtual void SetTitle([NotNull] string title)
    {
        Title = Check.NotNullOrWhiteSpace(title, nameof(title)); //验证
    }

    /* AddLabel和RemoveLabel方法管理Labels集合
     * 安全的方式(防止两次添加相同的标签) */

    public virtual void AddLabel(Guid labelId)
    {
        if (Labels.Any(l => l.LabelId == labelId))
        {
            return;
        }

        Labels.Add(new IssueLabel(Id, labelId));
    }

    public virtual void RemoveLabel(Guid labelId)
    {
        Labels.RemoveAll(l => l.LabelId == labelId);
    }

    /* Close和ReOpen方法可保护一致性
     * IsClosed 与 CloseReason 属性. */

    public virtual void Close(IssueCloseReason reason)
    {
        IsClosed = true;
        CloseReason = reason;
    }

    public virtual void ReOpen()
    {
        IsClosed = false;
        CloseReason = null;
    }
}
```

#### 實體

```
public class IssueLabel : Entity
{
    public virtual Guid IssueId { get; private set; }
    public virtual Guid LabelId { get; private set; }

    protected IssueLabel()
    {

    }

    public IssueLabel(Guid issueId, Guid labelId)
    {
        IssueId = issueId;
        LabelId = labelId;
    }
}
```

### 參考文獻

- Effective Aggregate Design by Vaughn Vernon <http://dddcommunity.org/library/vernon_2011>

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- 回首頁

---

*本文章從點部落遷移至 Writerside*
