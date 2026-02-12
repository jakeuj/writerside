# ABP.IO WEB應用程式框架 Export Excel

> **原文發布日期:** 2022-02-10
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/02/10/Abp-how-to-export-excel-files
> **標籤:** 無

---

筆記下匯出 Excel 給下載

- 參照：[How to export Excel files from the ABP framework | ABP Community](https://community.abp.io/posts/how-to-export-excel-files-from-the-abp-framework-wm7nnw3n)
- Nuget：只要安裝 documentformat.openxml
  `dotnet add package documentformat.openxml`
- Return：原本是輸出 Byte[]，這邊改用 RemoteStreamContent，好處是可以直接下載

```
public Task<RemoteStreamContent> ExportToExcel()
{
    var fs = new ExcelFileGenerator().Generate();
    fs.Position = 0;
    return Task.FromResult(
        new RemoteStreamContent(fs,$"test_{DateTime.Now:yyyyMMdd_HHmmss}.xlsx","application/octet-stream"));
}
```

- 注意：`fs.Position = 0;`
- `RemoteStreamContent` 是吃 Stream，所以 ExcelFileGenerator 要從 `Byte[]` 改回傳 `MemoryStream`

```
public MemoryStream Generate()
{
    var memoryStream = new MemoryStream();

    using (var document = SpreadsheetDocument.Create(memoryStream, SpreadsheetDocumentType.Workbook))
    {
        var workbookPart = document.AddWorkbookPart();
        workbookPart.Workbook = new Workbook();

        var worksheetPart = workbookPart.AddNewPart<WorksheetPart>();
        worksheetPart.Worksheet = new Worksheet(new SheetData());

        var sheets = workbookPart.Workbook.AppendChild(new Sheets());

        sheets.AppendChild(new Sheet
        {
            Id = workbookPart.GetIdOfPart(worksheetPart),
            SheetId = 1,
            Name = "Sheet 1"
        });

        var sheetData = worksheetPart.Worksheet.GetFirstChild<SheetData>();

        var row1 = new Row();
        row1.AppendChild(
            new Cell
            {
                CellValue = new CellValue("Abp Framework"),
                DataType = CellValues.String
            }

        );
        sheetData.AppendChild(row1);

        var row2 = new Row();
        row2.AppendChild(
            new Cell
            {
                CellValue = new CellValue("Open Source"),
                DataType = CellValues.String
            }
        );
        sheetData.AppendChild(row2);

        var row3 = new Row();
        row3.AppendChild(
            new Cell
            {
                CellValue = new CellValue("WEB APPLICATION FRAMEWORK"),
                DataType = CellValues.String
            }
        );
        sheetData.AppendChild(row3);

        document.Save();
        document.Close();

        return memoryStream;
    }
}
```

主要就把 `return memoryStream.ToArray();`  的 `ToArray()` 拿掉

延伸閱讀

[ABP.IO WEB應用程式框架 使用 Azure Storage 上傳圖片 | Jakeuj - 點部落 (dotblogs.com.tw)](https://www.dotblogs.com.tw/jakeuj/2021/10/29/Abp-Blob-Storing-Azure)

[[DotnetCore] 讀取 excel 套件整理 | Secret Note (jiaming0708.github.io)](https://jiaming0708.github.io/2022/08/22/dotnet-core-read-excel-library/)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- ABP
- Excel

- 回首頁

---

*本文章從點部落遷移至 Writerside*
