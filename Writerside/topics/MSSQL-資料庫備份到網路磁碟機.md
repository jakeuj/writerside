# MSSQL 資料庫備份到網路磁碟機

> **原文發布日期:** 2016-03-22
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2016/03/22/mssqlbackup
> **標籤:** 無

---

MSSQL 資料庫備份 網路磁碟機

資料庫常常磁碟空間不足而且又有備份需求時，

把資料庫備份到網路磁碟機應該是比較方便的選擇，

但實際上無法用一般的備份維護計畫來選取網路儲存裝置，

需要使用以下語法來讓SQL連到網路磁碟機達到備份目的，

以下是實際操作的語法，其中的網域名稱讓我卡了一會兒。

1.啟用xp\_cmdshell

```

-- To allow advanced options to be changed.
EXEC sp_configure 'show advanced options', 1
GO
-- To update the currently configured value for advanced options.
RECONFIGURE
GO
-- To enable the feature.
EXEC sp_configure 'xp_cmdshell', 1
GO
-- To update the currently configured value for this feature.
RECONFIGURE
GO
```

2.執行備份

```

-- 宣告
DECLARE @ConnectDriveCmd varchar(100)
DECLARE @DisconnectDriveCmd varchar(100)
DECLARE @TargetDriveName varchar(100)

-- 初始化(IP,目錄,密碼,帳號)
SET @ConnectDriveCmd = 'net use z: \\[IP]\[目錄] [密碼] /user:[IP]\[帳號]'
SET @DisconnectDriveCmd = 'net use z: /d'
SET @TargetDriveName = 'z:\\Bak_' + DATENAME(Weekday,GETDATE()) + '_Full.BAK'

-- 連接網路磁碟機
EXEC Master..xp_cmdShell @ConnectDriveCmd

-- 備份資料庫([資料庫名])
BACKUP DATABASE [資料庫名] TO DISK = @TargetDriveName
WITH NOFORMAT, INIT,  NAME = N'Bak-完整 資料庫 備份', SKIP, NOREWIND, NOUNLOAD,  STATS = 10

-- 中斷網路磁碟機
EXEC Master..xp_cmdShell @DisconnectDriveCmd

GO
```

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- MSSQL

- 回首頁

---

*本文章從點部落遷移至 Writerside*
