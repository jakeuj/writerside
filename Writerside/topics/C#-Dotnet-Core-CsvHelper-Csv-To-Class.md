# C# Dotnet Core CsvHelper Csv To Class

> **原文發布日期:** 2022-02-10
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/02/10/aspnet-core-csvhelper-c-csv
> **標籤:** 無

---

總之筆記下 CsvHelper 用法

示意

```
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using CsvHelper;
using CsvHelper.Configuration;
using CsvHelper.Configuration.Attributes;

namespace AbpToExcel.CsvImport;

public class ImportFromCsvAppService : AbpToExcelAppService
{
    public Task<List<string>> ImportFromCsv()
    {
        var readConfiguration = new CsvConfiguration(CultureInfo.InvariantCulture)
        {
            HasHeaderRecord = true
        };
        using (var reader = new StreamReader(@"D:\\Example.csv"))
        using (var csv = new CsvReader(reader, readConfiguration))
        {
            var records = csv.GetRecords<Employee>();
            return Task.FromResult(records.Select(x => x.Name).Take(10).ToList()) ;
        }
    }
}

public class Employee
{
    [Name("CsvName")]
    public string Name { get; set; }
}
```

參照

[[C#][.NET Core] CsvHelper : 透過 C# 讀寫 csv 檔案 (dog0416.blogspot.com)](http://dog0416.blogspot.com/2019/11/aspnet-core-csvhelper-c-csv.html)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [.Net Core](/jakeuj/Tags?qq=.Net%20Core)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
