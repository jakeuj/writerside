# Migration database update in Rider

> **原文發布日期:** 2018-12-25
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2018/12/25/jetbrains_rider_migration
> **標籤:** 無

---

Migration database update in Rider

dotnet 3.0 把 ef 移除了

所以要先另外安裝ef才能下指令

```

dotnet tool install --global dotnet-ef --version 3.0.0
```

`dotnet ef migrations add Init -s ..\MyProject.DbMigrator\`

For Abp.io https://github.com/abpframework/abp/issues/1920#issuecomment-543551659

---

朋友推薦 jetbrains 的 C# IDE Rider 2018 給我

剛好裝的VS 2019開不了我想開的專案

就裝來試試，然後就卡關了，migration不知道怎下才能建db

查了一下，結論是先到terminal然後切到有放migration檔案的專案目錄

然後下 dotnet ef migrations add "Name"

dotnet ef database update 就可以了

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/1d12e461-d70c-4c54-920c-8458964654b5/1545725088_10347.jpg)

參照：[Running Entity Framework (Core) commands in Rider](https://blog.jetbrains.com/dotnet/2017/08/09/running-entity-framework-core-commands-rider/)

* 如果冒出要你安裝  [Microsoft.EntityFrameworkCore.Design]
  就去nuget搜尋然後在DbContext專案補上該套件
* 如果抓不到appsetting.json就加上參數 --startup-project  (-s)
  啟始專案的專案資料夾的相對路徑。 預設值為目前的資料夾。

參照：<https://docs.microsoft.com/zh-tw/ef/core/miscellaneous/cli/dotnet#common-options>

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Rider

* 回首頁

---

*本文章從點部落遷移至 Writerside*
