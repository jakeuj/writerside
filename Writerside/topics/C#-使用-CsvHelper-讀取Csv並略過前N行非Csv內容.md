# C# CsvHelper 讀取技巧

> **原文發布日期:** 2022-03-11
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/03/11/CsvHelper
> **標籤:** 無

---

筆記一下檔案有髒東西的時候如何讀取特定範圍Csv

結論

```
// 定義如何找出正確 Header，這邊使用開頭兩個逗號分隔的欄位來查找
const string headerPrefix = "date,time,";
using (var reader = new StreamReader(@"D:\Test.log"))
using (var csv = new CsvReader(reader, CultureInfo.InvariantCulture))
{
    csv.Context.RegisterClassMap<TestMapProfile>();
    // 用來判斷是不是要找 Header
    var isHeader = true;
    while (csv.Read())
    {
        if (isHeader)
        {
            // 使用特定文字內容來判斷這行是不是正確 Header
            if(csv.Parser.RawRecord.Contains(headerPrefix))
            {
                csv.ReadHeader();
                // Header 只會出現一次，後面正常應該緊接著資料
                isHeader = false;
            }
            continue;
        }
        // 至此已找到正確 Csv 開頭 (Header)，所以可以開始正常讀取資料
        Logger.LogInformation("{@input}", csv.GetRecord<TestRecord>());
    }
}
```

Test.log

```

/// <summary>
/// 測試紀錄 By Jakeuj
/// </summary>

date,time,data
3/11,18:00,OK
3/12,8:00,Fail
```

參照

[Reading Multiple Data Sets | CsvHelper (joshclose.github.io)](https://joshclose.github.io/CsvHelper/examples/reading/reading-multiple-data-sets/)

[【C#】CsvHelper 使用手冊 | IT人 (iter01.com)](https://iter01.com/506823.html)

※ 非官方的使用手冊內文中關於自訂映射有錯誤，應為：`csv.Context.RegisterClassMap`

## 同場加映

如果來源 CSV 有空格會報錯

`CsvHelper.BadDataException: You can ignore bad data by setting BadDataFound to null.`

```
Id,Name,Type
1, "Jake",User
```

需要加上設定

```
var config = new CsvConfiguration(CultureInfo.InvariantCulture)

{
    TrimOptions = TrimOptions.Trim
};
```

[c# - CsvHelper - How to config the setting about quote? - Stack Overflow](https://stackoverflow.com/questions/71481331/csvhelper-how-to-config-the-setting-about-quote)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- CsvHelper
- Excel

- 回首頁

---

*本文章從點部落遷移至 Writerside*
