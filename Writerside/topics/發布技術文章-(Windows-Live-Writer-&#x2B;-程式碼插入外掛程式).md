# 發布技術文章 (Windows Live Writer &#x2B; 程式碼插入外掛程式)

> **原文發布日期:** 2011-07-08
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2011/07/08/31325
> **標籤:** 無

---

以Windows Live Writer發布DotBlog文章+CODE編輯(外掛程式)

[![2](https://dotblogsfile.blob.core.windows.net/user/jakeuj/1107/080be9e92d5b_C86C/2_thumb.jpg "2")](https://dotblogsfile.blob.core.windows.net/user/jakeuj/1107/080be9e92d5b_C86C/2.jpg)

Code Snippet plugin for Windows Live Writer 產生之原始碼

```

   1: // Create Uri
```

```

   2: Uri uriAddress = new Uri("http://www.contoso.com/index.htm#search");
```

```

   3: Console.WriteLine(uriAddress.Fragment);
```

```

   4: Console.WriteLine("Uri {0} the default port ", uriAddress.IsDefaultPort ? "uses" : "does not use");
```

```

   5:
```

```

   6: Console.WriteLine("The path of this Uri is {0}", uriAddress.GetLeftPart(UriPartial.Path));
```

```

   7: Console.WriteLine("Hash code {0}", uriAddress.GetHashCode());
```

SyntaxHighlighter for Windows Live Writer 產生之原始碼

```

// Create Uri
Uri uriAddress = new Uri("http://www.contoso.com/index.htm#search");
Console.WriteLine(uriAddress.Fragment);
Console.WriteLine("Uri {0} the default port ", uriAddress.IsDefaultPort ? "uses" : "does not use");

Console.WriteLine("The path of this Uri is {0}", uriAddress.GetLeftPart(UriPartial.Path));
Console.WriteLine("Hash code {0}", uriAddress.GetHashCode());
```

說明：

第一天使用點部落 想用Windows Live Writer離線發布新技術文章 就遇到沒有插入程式碼功能

還好有好心人提醒我可以依照以下文章取得插入程式碼支援

<http://www.dotblogs.com.tw/dotblogs/archive/2008/05/01/3768.aspx>

而我則發現Windows Live Writer有”新增外掛程式”功能(在”插入”頁面)

Windows Live Writer 外掛程式網站

<http://plugins.live.com/writer/browse?orderby=featured&page=1>

從中找到編輯程式語言的外掛程式

#### Insert Code for Windows Live Writer

<http://plugins.live.com/writer/detail/insert-code-for-windows-live-writer>

依照點部落說法在程式碼過長會有點問題 故建議使用 [SyntaxHighlighter for Windows Live Writer](http://www.codeplex.com/wlwSyntaxHighlighter/Release/ProjectReleases.aspx?ReleaseId=8769)

發現Windows Live Writer 外掛程式網站裡尚有另一套外掛程式

#### Code Snippet plugin for Windows Live Writer

<http://plugins.live.com/writer/detail/code-snippet-plugin-for-windows-live-writer>

說明：Format and apply syntax highlighting to source code snippets before inserting into your Windows Live Writer posts. Please refer to the following post for details on what's new: <http://lvildosola.blogspot.com/2009/03/code-snippet-plugin-for-windows-live.html>

依照我不是很好的英文能力解讀此套外掛程式應該有支援 syntax highlighting 格式

作者網站：<http://lvildosola.blogspot.com/2009/03/code-snippet-plugin-for-windows-live.html>

於是乎我把三套外掛都掛上去之後發現

Insert Code for Windows Live Writer 既然有問題我就不用了(不知道有沒有更新之類的)

SyntaxHighlighter for Windows Live Writer 就是跳出一個視窗讓你插入CODE

Code Snippet plugin for Windows Live Writer 則比 SyntaxHighlighter for Windows Live Writer 多出一些東西可以按 (還沒測試)

不知道 Code Snippet plugin for Windows Live Writer 會不會有 Insert Code for Windows Live Writer 所發生的問題

話說 Code Snippet plugin for Windows Live Writer 支援Windows Live Writer 2.0 (我是用 Windows Live Writer 2011) 發布日期是2009年

而 SyntaxHighlighter for Windows Live Writer 發布日期則是2008年

不知道有沒有 SyntaxHighlighter for Windows Live Writer 的套件是支援 Windows Live Writer 2011 版本的

純粹只是喜歡用新版本的東西 @@

2011/07/08 PM 03:02

發現 Code Snippet plugin 還是沒有完好支援SyntaxHighlighter

以 Code Snippet plugin 編寫 會顯示 SyntaxHighlighter 的樣式

但是無法提供額外功能 例如：複製原始碼(不帶行號)

其他有待測試…

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* SOFTWARE

* 回首頁

---

*本文章從點部落遷移至 Writerside*
