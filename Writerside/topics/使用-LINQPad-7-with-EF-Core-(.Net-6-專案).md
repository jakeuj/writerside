# LINQPad 7 with EF Core

> **原文發布日期:** 2021-06-24
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/06/24/LINQPadEFCore
> **標籤:** 無

---

紀錄一下怎麼快速試寫專案要用的 Linq

1. 首先下載安裝支援 .Net Core 的 LINQPad 7
   https://www.linqpad.net/Download.aspx
2. 參照官方連結建立與專案檔 .dll 的連結
   https://www.linqpad.net/EntityFramework.aspx
3. 既然是參照 dll 記得案文章所描述先 bulid 一次
   Example: `bin\Debug\netcoreapp3.1\Test.dll`
4. 如果 appsettings 裡面的連結字串不是你要測試用的可以自己改
   Example: `Server=(LocalDb)\MSSQLLocalDB;Database=Test;Trusted_Connection=True;MultipleActiveResultSets=true`
5. Add connection 如下圖所示

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/98f0f921-d4d2-40ec-8edc-83c7587c1e69/1624526064.png)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/98f0f921-d4d2-40ec-8edc-83c7587c1e69/1635322907.png)

然後應該就會看到實體的資料

接著參照以下文章使用

https://peterhpchen.github.io/DigDeeperLINQ/03_LINQPad.html#%E7%94%A8%E6%B3%95
{ignore-vars="true"}

使用預設 Language => C# Expression (單行語法) 測試

這邊假設我有個實體叫做 Test

直接輸入以下基本語法

`Test.ToList()`

執行就可以看到結果

剩下就可以自己測試自己想要的語法

然後看看結果是不是自己要的

並檢查 SQL 語法是不是有效率的

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- Linq
- LINQPad

- 回首頁

---

*本文章從點部落遷移至 Writerside*
