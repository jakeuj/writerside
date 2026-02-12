# GUID 輸入不含連字號 處理

> **原文發布日期:** 2016-03-30
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2016/03/30/GUID
> **標籤:** 無

---

有時候我們會利用DB的NEWID()來產生uniqueidentifier資料型態的資料當主鍵

這時又會遇到需要處理使用者輸入這個GUID但可能不想讓USER輸入連字號

但是SQL又必須用有連字號的GUID格式才能做INDEX查詢

當然土法煉鋼可以拆字串自己加上連字號的方式來處理但總是覺得不太美觀

有時候我們會利用DB的NEWID()來產生uniqueidentifier資料型態的資料當主鍵

這時又會遇到需要處理使用者輸入這個GUID但可能不想讓USER輸入連字號

但是SQL又必須用有連字號的GUID格式才能做INDEX查詢

當然土法煉鋼可以拆字串自己加上連字號的方式來處理但總是覺得不太美觀

總之結論就是以下語法做個筆記

```

string ConvertGuid(string inputGuid)
        {
            System.Guid outputGuid1;
            System.Guid.TryParse(inputGuid, out outputGuid1);
            return outputGuid1.ToString();
        }
```

```

Response.Write(ConvertGuid("6F9619FF8B86D011B42D00C04FC964FF"));

//OUTPUT：6f9619ff-8b86-d011-b42d-00c04fc964ff
```

參照：http://kevintsengtw.blogspot.tw/2010/08/guid-tryparse.html

以上

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- C#
{ignore-vars="true"}
- MSSQL

- 回首頁

---

*本文章從點部落遷移至 Writerside*
