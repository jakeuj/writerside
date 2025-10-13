# Azure SQL 新增使用者並授予讀寫權限

> **原文發布日期:** 2021-09-23
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/09/23/Azure-SQL-CREATE-LOGIN-USER
> **標籤:** 無

---

以往有 GUI 到了 Az 忽然不好使了…

## 結論

```
USE master
CREATE LOGIN TestAccount WITH PASSWORD='@pa1xc*xMfkrv^~y_nqy'
CREATE USER TestApp FOR LOGIN TestAccount
GO

USE MyAppDb
CREATE USER TestApp FOR LOGIN TestAccount
EXEC sp_addrolemember 'db_datareader', TestApp;
EXEC sp_addrolemember 'db_datawriter', TestApp;
GO
```

* `LOGIN` 是登入帳號，包含密碼、原則、過期、禁用…ETC.
  單純登入資料庫伺服器並無法存取資料庫
* `USER` 是使用者，包含角色、權限…ETC.
  關聯登入帳號到資料庫的使用者後，才能夠以對應資料庫的權限來存取，
  每個資料庫權限不同，須個別設定使用者權限

首先登入帳號/密碼跟使用者是分開的

登入 => 使用者 => 權限 => 資料庫

這邊先建立登入帳號與密碼 (這部分是存在 master)

帳號：`NewLoginAccount`

密碼：`donthackmeplz`

```
USE master
CREATE LOGIN [NewLoginAccount] WITH PASSWORD='donthackmeplz'
GO
```

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/169980c2-8359-4a4c-ba1b-606bb9fe53ef/1682410424.png.png)

Login

然後ssms登入之後會到master進行一些查詢

如果沒幫這個登入建立 master 的使用者，到時候 ssms 雖然可以登入但重整會跳錯誤

所以接著用剛剛的新登入帳號來創建 master 的使用者

帳號：`NewLoginAccount`

使用者名稱：`NewUserName`

```
USE master
CREATE USER [NewUserName] FOR LOGIN [NewLoginAccount]
GO
```

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/169980c2-8359-4a4c-ba1b-606bb9fe53ef/1682410480.png.png)

User

接著切換到你真正要存取的資料庫

再建一次使用者

```
USE MyAppDb
CREATE USER [NewUserName] FOR LOGIN [NewLoginAccount]
GO
```

到這邊雖然新帳號可以登入也看得到這個DB

但是會發現裡面資料表都看不到

這是因為沒有讀取權限

所以最後我們需要針對該使用者進行授權 (基於角色)

```
USE MyAppDb
EXEC sp_addrolemember 'db_datareader', [NewUserName];
GO

```

如果同時需要增刪修，就一併授予寫入權限

```
USE MyAppDb
EXEC sp_addrolemember 'db_datawriter', [NewUserName];
GO
```

到這邊一般應用程式應該差不多使用這帳號來設定連線字串就可以了

開發時如果需要 db migrations 進行資料表的增刪修

則建議使用另一個較高權限的帳號來進行操作

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/169980c2-8359-4a4c-ba1b-606bb9fe53ef/1632377410.png)

參照

[在Azure SQL上新增使用者 (andy51002000.blogspot.com)](http://andy51002000.blogspot.com/2017/12/azure-sql.html)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Azure SQL](/jakeuj/Tags?qq=Azure%20SQL)
{ignore-vars="true"}
* [MSSQL](/jakeuj/Tags?qq=MSSQL)
* [SQL](/jakeuj/Tags?qq=SQL)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
