# DotNetCore HttpClient User-Agent &amp; Encoding

> **原文發布日期:** 2019-01-29
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/01/29/173228
> **標籤:** 無

---

DotNetCore HttpClient User-Agent & Encoding

編碼部分 DotNetCore 只保留常用編碼 所以Big5需要額外安裝套件

```

Install-Package System.Text.Encoding.CodePages
```

在程式起始處 初始化該套件 Startup (Web) 或 Main (Console)

```

Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
```

之後就跟以往用法一樣

再來是 User-Agent 部分

有些網站會依照此設定值返回不同內容

不設定有時會拿到預期之外的Response

```

client.DefaultRequestHeaders.UserAgent.TryParseAdd(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36");
```

或是

```

client.DefaultRequestHeaders.Add(
    "User-Agent",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36");
```

其他Header也可以依序新增進去

最後應該長這樣 User-Agent

```

static async Task Main()
{
    Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
    using (HttpClient client = new HttpClient())
    {
        client.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36");
        try
        {
        HttpResponseMessage response = await client.GetAsync("https://tw.yahoo.com/");
        response.EnsureSuccessStatusCode();
        string responseBody = await response.Content.ReadAsStringAsync();
        File.WriteAllText(@"E:\Users\jakeu\Desktop\WriteText.txt", responseBody);
        }catch{}
    }
}
```

因為網頁內容太長所以我最後寫到檔案

Encoding Big5

```

static async Task Main()
{
    Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
    using (HttpClient client = new HttpClient())
    {
        client.DefaultRequestHeaders.UserAgent.TryParseAdd(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36");
        try
        {
        HttpResponseMessage response = await client.GetAsync("https://tw.yahoo.com/");
        response.EnsureSuccessStatusCode();
        var responseBytes = await response.Content.ReadAsByteArrayAsync();
        var responseBody = Encoding.GetEncoding("big5").GetString(responseBytes, 0, responseBytes.Length - 1); ;
        File.WriteAllText(@"E:\Users\jakeu\Desktop\WriteText.txt", responseBody);
        }catch{}
    }
}
```

這邊要把 Url 改到一個 Big5 的網站測試 (Yahoo不是Big5編碼)

相關文章：

### [小心.NET HttpClient](https://dotblogs.com.tw/jakeuj/2019/01/25/httpclient)

### [[ASP.NET][C#] 使用 HtmlAgilityPack 擷取新聞 (爬文機器人)](https://dotblogs.com.tw/jakeuj/2016/06/14/htmlagilitypack)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* C#
{ignore-vars="true"}
* .Net Core
{ignore-vars="true"}
* HttpClinet

* 回首頁

---

*本文章從點部落遷移至 Writerside*
