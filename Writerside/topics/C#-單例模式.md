# C# 單例模式

> **原文發布日期:** 2017-10-30
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2017/10/30/Singleton
> **標籤:** 無

---

C# 單例模式

```

public sealed class Singleton
{
    public static Singleton Instance { get; private set; } = null;

    static Singleton()
    {
        Instance = new Singleton();
    }

    private Singleton()
    {
    }
}
```

Lazy (.Net 4.0 +)

```

public sealed class Singleton
{
    private static readonly Lazy<Singleton> lazy = new Lazy<Singleton>();
    private Singleton() { }
    public static Singleton Instance => lazy.Value;
}
```

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [C#](/jakeuj/Tags?qq=C%23)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
