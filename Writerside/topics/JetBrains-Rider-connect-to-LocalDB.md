# JetBrains Rider connect to LocalDB

> **原文發布日期:** 2019-07-17
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/07/17/RiderLocalDB
> **標籤:** 無

---

JetBrains Rider 連接開發用的本地資料庫 LocalDB 要點

有鑑於 Rider 要連開發用的 localdb 不是那麼直覺?
重點提示選完Data Source> MSSQL Server之後
Driver要記得點下去改用 jTds
要記得點下去改用 jTds
點下去改用 jTds
改用 jTds
jTds

這樣還不夠 還要記得 Connection type 要點下去改成 LocalDB
記得 Connection type 要點下去改成 LocalDB
Connection type 要點下去改成 LocalDB
點下去改成 LocalDB
改成 LocalDB
LocalDB

如果設完提示 LocalDB 是 stop 狀態
要到 LocalDB 執行檔所在位置
PS/CMD 執行 sqllocaldb start

P.S. 首次使用要點一下下方 下載驅動

![P.S. 首次使用要點一下下方 下載驅動](https://dotblogsfile.blob.core.windows.net/user/jakeuj/b5e7cb7b-ba3c-468d-a448-7ca945b53f6b/1563353518_32263.png)![P.S. 首次使用要點一下下方 下載驅動 2](https://dotblogsfile.blob.core.windows.net/user/jakeuj/b5e7cb7b-ba3c-468d-a448-7ca945b53f6b/1563353523_65684.png)![P.S. 首次使用要點一下下方 下載驅動 3](https://dotblogsfile.blob.core.windows.net/user/jakeuj/b5e7cb7b-ba3c-468d-a448-7ca945b53f6b/1563353528_22475.png)![P.S. 首次使用要點一下下方 下載驅動 4](https://dotblogsfile.blob.core.windows.net/user/jakeuj/b5e7cb7b-ba3c-468d-a448-7ca945b53f6b/1563353532_16522.png)![P.S. 首次使用要點一下下方 下載驅動 5](https://dotblogsfile.blob.core.windows.net/user/jakeuj/b5e7cb7b-ba3c-468d-a448-7ca945b53f6b/1563353534_93502.png)![P.S. 首次使用要點一下下方 下載驅動 6](https://dotblogsfile.blob.core.windows.net/user/jakeuj/b5e7cb7b-ba3c-468d-a448-7ca945b53f6b/1563353538_47191.png)![P.S. 首次使用要點一下下方 下載驅動 7](https://dotblogsfile.blob.core.windows.net/user/jakeuj/b5e7cb7b-ba3c-468d-a448-7ca945b53f6b/1563353541_03609.png)![P.S. 首次使用要點一下下方 下載驅動 8](https://dotblogsfile.blob.core.windows.net/user/jakeuj/b5e7cb7b-ba3c-468d-a448-7ca945b53f6b/1563353544_3776.png)![P.S. 首次使用要點一下下方 下載驅動 9](https://dotblogsfile.blob.core.windows.net/user/jakeuj/b5e7cb7b-ba3c-468d-a448-7ca945b53f6b/1563353547_77041.png)

connectionString="Server=(LocalDb)\\MSSQLLocalDB;Database=TestDB;Trusted\_Connection=True;MultipleActiveResultSets=true"

參照：<https://stackoverflow.com/questions/13287252/cannot-start-localdb>

延伸閱讀：[HeidiSQL連接LocalDB](https://stackoverflow.com/questions/25881084/heidisql-connection-to-ms-sql-server-localdb)

![PSNProfiles 卡片](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- MSSQL
- Rider
- SQL

- 回首頁

---

*本文章從點部落遷移至 Writerside*
