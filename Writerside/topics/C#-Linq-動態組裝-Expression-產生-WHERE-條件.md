# C# Linq 動態 Expression

> **原文發布日期:** 2023-06-20
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/06/20/CSharp-Linq-Expression-And-Where
> **標籤:** 無

---

Build a dynamic AND OR linq expression

結論

```
var testRepository = CachedServiceProvider
    .GetRequiredService<IReadOnlyRepository<Test, Guid>>();

Expression<Func<Test, bool>> expression = x => x.Id == id;

expression = age > 18
    ? expression.And(x => x.IsAdult == ture)
    : expression.And(x => x.IsBaby == true);

var entities = await testRepository.GetListAsync(expression);
```

* 如果 18 歲, where 條件為 `x.Id == id && x.IsAdult`
* 否則 (未滿18) where 條件為 `x.Id == id && x.IsBaby`

P.S. 情境是直接寫條件 Linq to SQL (case then) 撈出來的資料會是錯的

`GetListAsync(x => x.Id == id && age > 18 ? x.IsAdult == ture : x.IsBaby == true);`

MSDN

```
// Add the following directive to your file:
// using System.Linq.Expressions;

// This expression perfroms a logical AND operation
// on its two arguments. Both arguments must be of the same type,
// which can be boolean or integer.
Expression andExpr = Expression.And(
    Expression.Constant(true),
    Expression.Constant(false)
);

// Print out the expression.
Console.WriteLine(andExpr.ToString());

// The following statement first creates an expression tree,
// then compiles it, and then executes it.
Console.WriteLine(Expression.Lambda<Func<bool>>(andExpr).Compile()());

// This code example produces the following output:
//
// (True And False)
// False
```

參照

[Expression.And Method (System.Linq.Expressions) | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/system.linq.expressions.expression.and?view=net-7.0)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Linq

* 回首頁

---

*本文章從點部落遷移至 Writerside*
