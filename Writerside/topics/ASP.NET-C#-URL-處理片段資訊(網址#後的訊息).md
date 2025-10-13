# ASP.NET C# URL 處理片段資訊(網址#後的訊息)

> **原文發布日期:** 2011-07-08
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2011/07/08/31335
> **標籤:** 無

---

ASP.NET C# URL 處理片段資訊(網址#後的訊息)

```

Fragment 屬性會取得 URI 中片段標記 (#) 後面的任何文字，包括片段標記本身在內。 以 URI http://www.contoso.com/index.htm#main, 為例，Fragment 屬性會傳回 #main。
```

```

// Create Uri
Uri uriAddress = new Uri("http://www.contoso.com/index.htm#search");
Console.WriteLine(uriAddress.Fragment);
Console.WriteLine("Uri {0} the default port ", uriAddress.IsDefaultPort ? "uses" : "does not use");

Console.WriteLine("The path of this Uri is {0}", uriAddress.GetLeftPart(UriPartial.Path));
Console.WriteLine("Hash code {0}", uriAddress.GetHashCode());
```

日前在處理FB資料時會回傳#後帶參數之資料

當時FB範例只提供JAVASCRIPT的擷取方式

最近在逛MSDN時發現原來C#也是可以取得 片段標記# 的資料

於是乎就記下來供以後查閱！

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* C#
{ignore-vars="true"}

* 回首頁

---

*本文章從點部落遷移至 Writerside*
