# 下載圖片檔案上傳到遠端伺服器API轉存

> **原文發布日期:** 2020-11-20
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2020/11/20/MultipartFormDataContent
> **標籤:** 無

---

筆記下如何將圖片從對應網址下載並轉存到API

直上 Code

```

private async Task Save(
    string originUrl,
    string targetUrl,
    string filename,
    string token,
    CancellationToken cancellationToken)
{
    // download file from originUrl
    var uri = new UriBuilder(originUrl);
    using var client = _clientFactory.CreateClient();
    var jpg = await client.GetAsync(uri.Uri, cancellationToken);

    jpg.Content.Headers.Add(
        "Content-Disposition",
        "form-data; name=\"file\"; filename=\"" + filename + "\"");

    // MultipartFormDataContent
    using var content =
        new MultipartFormDataContent {{jpg.Content, "file", filename}};

    // RequestHeaders
    var boundary = DateTime.Now.Ticks.ToString("X");
    client.DefaultRequestHeaders.Add("ContentType",
        "multipart/form-data;charset=utf-8;boundary=" + boundary);

    // OAuth
    client.DefaultRequestHeaders.Authorization =
        new AuthenticationHeaderValue("Bearer",token);

    uri = new UriBuilder(targetUrl);
    var response = await client.PostAsync(uri.Uri, content, cancellationToken);
    if (response != null && response.IsSuccessStatusCode)
        Console.Write(await response.Content.ReadAsStringAsync());
    else Console.Write("Error...");
}
```

參照：[將圖片檔案上傳到遠端伺服器](https://csharpkh.blogspot.com/2019/05/CSharp-HttpClient-Upload-Image-Multipart-Content-MultipartFormDataContent.html)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [C#](/jakeuj/Tags?qq=C%23)
{ignore-vars="true"}
* [.Net Core](/jakeuj/Tags?qq=.Net%20Core)
{ignore-vars="true"}

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
