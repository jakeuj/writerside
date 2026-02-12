# [Git] stash 和 shelve 的區別

> **原文發布日期:** 2023-12-25
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/12/25/git-stash-shelve
> **標籤:** 無

---

Jetbrains IDE 內建 stash 和 shelve

## 結論

我不知道差在哪

- stash
  - 會把改的檔案還原回未變更之前的檔案，同時將差異的部分暫存起來
  - 之後可以再 unstash，把檔案在從原始版本變成剛剛修改後的內容
- shelve
  - 會把改的檔案還原回未變更之前的檔案，同時將差異的部分暫存起來
  - 之後可以再 unshelve，把檔案在從原始版本變成剛剛修改後的內容

## Shelve

    1. Shelve

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/557af885-41dc-407f-b223-cba71951bdb1/1703499873.png.png)

    2. 檔案會被還原

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/557af885-41dc-407f-b223-cba71951bdb1/1703499903.png.png)

    3. UnShelve

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/557af885-41dc-407f-b223-cba71951bdb1/1703499940.png.png)

    4. 檔案會被復原

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/557af885-41dc-407f-b223-cba71951bdb1/1703499963.png.png)

    5. 這些操作都不會在版控上留下紀錄

## Stash

1. 修改 appsettings.secrets.json

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/557af885-41dc-407f-b223-cba71951bdb1/1703498250.png.png)

    2. 選擇 git stash changes

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/557af885-41dc-407f-b223-cba71951bdb1/1703498295.png.png)

    3. 輸入 stash 的訊息並建立該 stash

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/557af885-41dc-407f-b223-cba71951bdb1/1703497497.png.png)

    4. appsettings.secrets.json 已被還原回未更改的內容

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/557af885-41dc-407f-b223-cba71951bdb1/1703497536.png.png)

    5. 選擇 git unstash changes

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/557af885-41dc-407f-b223-cba71951bdb1/1703497692.png.png)

    6. 選擇欲還原的 stash 並 Apply Stash

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/557af885-41dc-407f-b223-cba71951bdb1/1703497723.png.png)

    7. appsettings.secrets.json 會再變成該 stash 的內容

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/557af885-41dc-407f-b223-cba71951bdb1/1703497761.png.png)

    8. 這些操作都不會在版控上留下紀錄

### 參照

[idea中好用的git shelve changes和stash changes-CSDN博客](https://blog.csdn.net/eclipse1024/article/details/116352777)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- Git
- JetBrains

- 回首頁

---

*本文章從點部落遷移至 Writerside*
