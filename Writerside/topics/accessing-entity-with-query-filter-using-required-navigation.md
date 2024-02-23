# accessing-entity-with-query-filter-using-required-navigation

Migration 時跳出警告

## Warning

```
Entity 'xxx' has a global query filter defined and is the required end of a relationship with the entity 'xxx'. 
This may lead to unexpected results when the required entity is filtered out. 
Either configure the navigation as optional, 
or define matching query filters for both entities in the navigation. 
See https://go.microsoft.com/fwlink/?linkid=2131316 for more information.
```

## 文件

[使用必要的導覽來存取具有查詢篩選的實體](https://go.microsoft.com/fwlink/?linkid=2131316)

## 結論

可能是因為使用 ISoftDelete 導致查詢時會包含篩選 IsDeleted=true 的條件，導致關聯的實體無法正確取得。