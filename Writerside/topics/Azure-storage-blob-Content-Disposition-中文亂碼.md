# Azure storage blob Content-Disposition 中文亂碼

> **原文發布日期:** 2023-02-09
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/02/09/Azure-storage-blob-Content-Disposition
> **標籤:** 無

---

筆記下載檔案 API 回傳 SAS 下載中文檔案連結的那話兒

## 結論

```
var displayName = "中文 檔案.txt";
dislayName = UrlEncoder.Default.Encode(displayName);
sasBuilder.ContentDisposition =
    $"attachment; filename* = UTF-8''{displayName} ";
```

### 說明

首先使用 .Net 7 的 UrlEncoder 來對中文進行網址編碼

然後把 `filename = {displayName}` 改成 `filename* = UTF-8''{displayName}`

### 參照

[探究 Content-Disposition：解决下载中文文件名乱码\_liuyaqi1993的博客-CSDN博客](https://blog.csdn.net/liuyaqi1993/article/details/78275396)

[UrlEncode() 與空白變加號問題-黑暗執行緒 (darkthread.net)](https://blog.darkthread.net/blog/urlencode-in-dotnet/)

[UrlEncoder Class (System.Text.Encodings.Web) | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/system.text.encodings.web.urlencoder?view=net-7.0)

[建立容器或 blob 的服務 SAS - Azure Storage | Microsoft Learn](https://learn.microsoft.com/zh-tw/azure/storage/blobs/sas-service-create?tabs=dotnet)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Azure](/jakeuj/Tags?qq=Azure)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
