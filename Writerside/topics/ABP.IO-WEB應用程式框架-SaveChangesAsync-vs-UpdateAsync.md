# ABP.IO WEB應用程式框架 SaveChangesAsync vs UpdateAsync

> **原文發布日期:** 2022-10-04
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/10/04/abp-SaveChangesAsync-UpdateAsync
> **標籤:** 無

---

筆記一下不同方法更新資料時的差異

## 結論

* SaveChangesAsync()
  + 只會更新實體部分有變更的欄位
* UpdateAsync(TEntity)
  + 會更新整個實體全部欄位
  + 當取得實體與更新實體之間，有其他東西改了其他欄位，會造成資料被複寫回舊的資料
    - A程序取得B欄位=C,D欄位=E
    - F程序更新D欄位=G
    - A程序改變B欄位=H, 並使用 UpdateAsync 更新實體, D會一併被更新成E
    - 預期 B=C, D=G, 實際會變成 B=C, D=E

### 範例程式碼

```
var e = await _repository.FirstOrDefaultAsync();

e.OrderNumber = DateTime.Now.ToString("yyyyMMddHHmmss");
await _repository.UpdateAsync(e);
await CurrentUnitOfWork.SaveChangesAsync();

e.OrderNumber = DateTime.Now.ToString("yyMMddHHmmss");
await CurrentUnitOfWork.SaveChangesAsync();
```

### 紀錄

```
UPDATE [AppOrders] SET [ConcurrencyStamp] = @p0, [CreationTime] = @p1, [CreatorId] = @p2, [DeleterId] = @p3, [DeletionTime] = @p4, [ExtraProperties] = @p5, [IsDeleted] = @p6, [LastModificationTime] = @p7, [LastModifierId] = @p8,
[OrderDate] = @p9, [OrderNumber] = @p10, [PartnerId] = @p11, [Status] = @p12
WHERE [Id] = @p13 AND [ConcurrencyStamp] = @p14;

UPDATE [AppOrders] SET [ConcurrencyStamp] = @p0, [LastModificationTime] = @p1, [OrderNumber] = @p2
WHERE [Id] = @p3 AND [ConcurrencyStamp] = @p4;
SELECT @@ROWCOUNT;
```

## 補充

當 entity 有某欄位是自動增量，

```
entity.Property(e => e.AutoId).ValueGeneratedOnAdd();
```

使用 `UpdateAsync` 會拋出例外

`Cannot update identity column 'AutoId'.`

請改用 `SaveChangesAsync`

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Entity Framework](/jakeuj/Tags?qq=Entity%20Framework)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
