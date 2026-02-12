# SQL

一次刪除多個 DB 並避免使用中無法刪除的問題

## 刪除多個 DB

```sql
DECLARE @DBName NVARCHAR(100)

DECLARE db_cursor CURSOR FOR
SELECT name 
FROM sys.databases 
WHERE name IN ('AbpSolution1', 'AbpSolution2', 'AbpSolution3')

OPEN db_cursor
FETCH NEXT FROM db_cursor INTO @DBName

WHILE @@FETCH_STATUS = 0
BEGIN
    DECLARE @SQL NVARCHAR(MAX)
    SET @SQL = 'ALTER DATABASE [' + @DBName + '] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;'
    SET @SQL = @SQL + 'DROP DATABASE [' + @DBName + '];'
    
    EXEC sp_executesql @SQL
    
    FETCH NEXT FROM db_cursor INTO @DBName
END

CLOSE db_cursor
DEALLOCATE db_cursor
```
