# C# .Net Excel (MiniExcel)

> **原文發布日期:** 2023-06-13
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/06/13/CSharp-DotNet-MiniExcel
> **標籤:** 無

---

筆記下 MiniExcel

## 填充並存檔

使用 MiniExcel 填充 Excel 樣板來產生最終我們要的 Excel 檔案

P.S. 樣板填充支援 **合併欄位** 與 **多 Sheets** (會依序填充各個 Sheet 內的 {{xxxxx}} )

![](https://user-images.githubusercontent.com/12729184/117973630-3527d500-b35f-11eb-95c3-bde255f8114e.png)

### 安裝

使用 nuget 安裝 MiniExcel 套件

### 樣板

![](https://user-images.githubusercontent.com/12729184/114564652-14f2f080-9ca3-11eb-831f-09e3fedbc5fc.png)

樣板

### 結果

![](https://user-images.githubusercontent.com/12729184/114564204-b2015980-9ca2-11eb-900d-e21249f93f7c.png)

結果

### 範例程式碼 1

```
public async Task GenerateExcels(string path, string templatePath, List<Employee> input)
{
    await MiniExcel.SaveAsByTemplateAsync(path, templatePath, new { employees = input });
}
```

## 填充並回傳資料流

開發 API 時可以不實際儲存檔案，直接回傳 Stream

### 樣板

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/90268042-144f-4d7c-832a-d2017fa3242a/1686621414.png.png)

樣板

### 範例程式碼 2

```
public async Task<IRemoteStreamContent> GenerateExcels(List<User> input)
{
    var provider = CachedServiceProvider.GetRequiredService<IVirtualFileProvider>();
    var file = provider.GetFileInfo(UserConsts.TemplatePath);
    var template = await file.ReadBytesAsync();

    var memoryStream = new MemoryStream();
    await memoryStream.SaveAsByTemplateAsync(template , new { V = input });
    memoryStream.Seek(0, SeekOrigin.Begin);
    return new RemoteStreamContent(memoryStream, "Sample.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
}
```

## 官方範例

```
//1. By POCO
var value = new
{
    employees = new[] {
        new {name="Jack",department="HR"},
        new {name="Lisa",department="HR"},
        new {name="John",department="HR"},
        new {name="Mike",department="IT"},
        new {name="Neo",department="IT"},
        new {name="Loan",department="IT"}
    }
};
MiniExcel.SaveAsByTemplate(path, templatePath, value);

//2. By Dictionary
var value = new Dictionary<string, object>()
{
    ["employees"] = new[] {
        new {name="Jack",department="HR"},
        new {name="Lisa",department="HR"},
        new {name="John",department="HR"},
        new {name="Mike",department="IT"},
        new {name="Neo",department="IT"},
        new {name="Loan",department="IT"}
    }
};
MiniExcel.SaveAsByTemplate(path, templatePath, value);
```

## 複雜填充

```
// 1. By POCO
var value = new
{
    title = "FooCompany",
    managers = new[] {
        new {name="Jack",department="HR"},
        new {name="Loan",department="IT"}
    },
    employees = new[] {
        new {name="Wade",department="HR"},
        new {name="Felix",department="HR"},
        new {name="Eric",department="IT"},
        new {name="Keaton",department="IT"}
    }
};
MiniExcel.SaveAsByTemplate(path, templatePath, value);

// 2. By Dictionary
var value = new Dictionary<string, object>()
{
    ["title"] = "FooCompany",
    ["managers"] = new[] {
        new {name="Jack",department="HR"},
        new {name="Loan",department="IT"}
    },
    ["employees"] = new[] {
        new {name="Wade",department="HR"},
        new {name="Felix",department="HR"},
        new {name="Eric",department="IT"},
        new {name="Keaton",department="IT"}
    }
};
MiniExcel.SaveAsByTemplate(path, templatePath, value);
```

## 加總

利用複雜填充可以實現填充清單並在其下方顯示總和

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/90268042-144f-4d7c-832a-d2017fa3242a/1687257170.png.png)![](https://dotblogsfile.blob.core.windows.net/user/小小朱/90268042-144f-4d7c-832a-d2017fa3242a/1687257311.png.png)

## 注意

以下程式碼會拋例外

```

var value = new
{
    V = new List<(string name, string department)>
    {
        new()
        {
            name = "Jake",
            department = "C"
        },
        new()
        {
            name = "Yo",
            department = "D"
        },
    }
};

MiniExcel.SaveAsByTemplate(path, templatePath, value);
```

猜測可能不支援 Tuple

## 參照

[MiniExcel/README.zh-Hant.md at master · mini-software/MiniExcel · GitHub](https://github.com/mini-software/MiniExcel/blob/master/README.zh-Hant.md#getstart3)

[[筆記] C# Tuple與ValueTuple的差異 | 遇見零壹魔王 - 點部落 (dotblogs.com.tw)](https://dotblogs.com.tw/noncoder/2019/09/28/tuple-new-old)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- Excel

- 回首頁

---

*本文章從點部落遷移至 Writerside*
