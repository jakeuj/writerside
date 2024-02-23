# Composite Keys

組合鍵

## Entity

(entities-with-composite-keys)[https://docs.abp.io/en/abp/1.0/Entities#entities-with-composite-keys]

## Define the primary key

```C#
b.HasKey(c => new {c.FormId, c.OptionId});
```

### 注意
沒設定主鍵的話，會出現以下錯誤：

```
The entity type 'User' requires a primary key to be defined.
```

## Define the foreign key

[composite foreign key](https://learn.microsoft.com/en-us/ef/core/modeling/relationships/foreign-and-principal-keys#composite-foreign-keys)