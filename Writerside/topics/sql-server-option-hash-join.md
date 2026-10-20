# SQL Server OPTION (HASH JOIN)：用途、執行計畫與效能驗證

<web-summary>說明 SQL Server OPTION (HASH JOIN) 的作用範圍、與 INNER HASH JOIN 的差異，並用虛構圖書借閱範例，示範如何從實際執行計畫確認重複掃描、記憶體與查詢耗時。</web-summary>

當實際執行計畫顯示 Nested Loops 讓昂貴的內側來源反覆掃描時，可以用 `OPTION (HASH JOIN)` 做對照實驗。若確實減少重複工作，再評估索引、統計資訊或查詢改寫；是否保留 hint，應看不同參數與負載下的結果。

Microsoft 建議由有經驗的開發者或 DBA，在一般調校仍不足時才使用 query hints。它會縮小 optimizer 的選擇範圍，不是加上就一定比較快。[官方 Query hints 文件](https://learn.microsoft.com/en-us/sql/t-sql/queries/hints-transact-sql-query)

本文全部使用虛構的圖書目錄與借閱紀錄，示意數字不代表實測結果，也不需要連接任何遠端系統。

## 最短用法 {#basic-usage}

在原查詢的最後、分號之前加上 `OPTION (HASH JOIN)`：

```sql
SELECT b.BookID, COUNT_BIG(*) AS BorrowCount
FROM dbo.Books AS b
INNER JOIN dbo.BorrowEvents AS e
    ON e.BookID = b.BookID
WHERE b.BookID IN (10, 20, 30)
GROUP BY b.BookID
OPTION (HASH JOIN);
```

這是 query hint，會限制整個 statement 中的 join 策略，不只是文字上最後一組 `JOIN`。如果只指定 `HASH JOIN`，就要求使用該策略產生可行計畫；若限制使 optimizer 無法產生合法計畫，可能回錯誤 `8622`。原查詢若已有 `OPTION`，把提示放進同一個括號內。[Query hints 的作用範圍](https://learn.microsoft.com/en-us/sql/t-sql/queries/hints-transact-sql-query)

`HASH JOIN` 也不等於 `HASH GROUP`。前者限制連接策略，後者處理 `GROUP BY`／`DISTINCT` 的彙總方式；看到 `Hash Match` 節點時，還要看它的 Logical Operation 是 Join 還是 Aggregate。

## 為什麼改 Join 策略可能改善耗時 {#join-strategies}

Nested Loops 可以想成「外側每來一列，就向內側找匹配資料」。外側很小、內側有適合的索引時，這種方式通常很有效；若內側每次都要做昂貴掃描，成本就可能隨重複執行放大。

Hash Join 則先用一側資料建立 hash table，再用另一側的連接鍵查找匹配。它適合處理某些大量、未排序的輸入，但需要記憶體；放不下時可能分割資料並使用磁碟，產生 spill。[SQL Server Join 演算法說明](https://learn.microsoft.com/en-us/sql/relational-databases/performance/joins)

| 策略 | 可以先檢查的條件 | 可能的成本 |
| --- | --- | --- |
| Nested Loops | 外側列數、內側是否能有效 seek | 內側被反覆掃描或呼叫 |
| Hash Join | 等值連接、輸入大小、可用記憶體 | 建立 hash table、memory grant、spill |
| Merge Join | 連接鍵是否已有合適排序 | 額外排序、重複鍵處理 |

把這張表當成調查入口即可，最終仍要看實際計畫。即使加上彙總後變慢，也可能是整體 join 計畫改變，不能只把原因歸到 `SUM` 或 `GROUP BY`。

## 用暫存表練習比較 {#temporary-table-example}

以下範例只建立本次連線的暫存表。請在同一個測試連線依序執行；重新建立資料時，會刪除本連線內同名的兩張暫存表。

### 建立虛構資料 {#create-sample-data}

```sql
DROP TABLE IF EXISTS #BorrowEvents;
DROP TABLE IF EXISTS #Books;

CREATE TABLE #Books (
    BookID INT NOT NULL PRIMARY KEY,
    Title NVARCHAR(100) NOT NULL
);

CREATE TABLE #BorrowEvents (
    BorrowID INT NOT NULL PRIMARY KEY,
    BookID INT NOT NULL
);

;WITH n AS (
    SELECT TOP (1000)
        ROW_NUMBER() OVER (ORDER BY a.object_id, b.object_id) AS Number
    FROM sys.all_objects AS a
    CROSS JOIN sys.all_objects AS b
)
INSERT INTO #Books (BookID, Title)
SELECT Number, N'Book ' + CONVERT(NVARCHAR(10), Number)
FROM n;

;WITH n AS (
    SELECT TOP (100000)
        ROW_NUMBER() OVER (ORDER BY a.object_id, b.object_id) AS Number
    FROM sys.all_objects AS a
    CROSS JOIN sys.all_objects AS b
)
INSERT INTO #BorrowEvents (BorrowID, BookID)
SELECT Number, ((Number - 1) % 1000) + 1
FROM n;
```

資料量取決於系統目錄是否提供足夠列數。這組範例用來練習語法與計畫判讀，**不保證能重現慢查詢，也不保證 hint 會加速**；optimizer 原本就可能選 Hash Join。

### 執行相同查詢的兩個版本 {#compare-queries}

先在 SSMS 開啟 **Include Actual Execution Plan**（`Ctrl+M`），再執行下列兩個版本。`STATISTICS IO` 與 `STATISTICS TIME` 提供額外的讀取量及 CPU／耗時資訊。[官方慢查詢診斷步驟](https://learn.microsoft.com/en-us/troubleshoot/sql/database-engine/performance/troubleshoot-slow-running-queries)

```sql
SET STATISTICS IO ON;
SET STATISTICS TIME ON;

-- Baseline: optimizer chooses the join strategy.
SELECT b.BookID, COUNT_BIG(*) AS BorrowCount
FROM #Books AS b
INNER JOIN #BorrowEvents AS e ON e.BookID = b.BookID
WHERE b.BookID IN (10, 20, 30)
GROUP BY b.BookID;

-- Comparison: only add the query hint.
SELECT b.BookID, COUNT_BIG(*) AS BorrowCount
FROM #Books AS b
INNER JOIN #BorrowEvents AS e ON e.BookID = b.BookID
WHERE b.BookID IN (10, 20, 30)
GROUP BY b.BookID
OPTION (HASH JOIN);

SET STATISTICS IO OFF;
SET STATISTICS TIME OFF;
```

比對時保留相同的條件、投影與彙總。拿「無 hint、含 GROUP BY」和「有 hint、移除 GROUP BY」相比，就無法單獨判斷是哪個改動有效。

兩份結果的鍵與計數應一致；沒有 `ORDER BY` 時，列順序不同不代表資料不同。先確認結果正確，再比較效能。

## SHOWPLAN 權限遭拒時怎麼處理 {#showplan-permission}

開啟實際或預估執行計畫時，如果看到這類訊息：

```text
訊息 262，層級 14
於資料庫 'LibraryDemo' 中，SHOWPLAN 的權限遭拒。
```

表示目前使用者缺少該資料庫的 `SHOWPLAN` 權限。請由 DBA 或具有適當授權權限的帳號，在目標資料庫授權給實際執行查詢的 **database user**；不必為了看計畫把使用者加入 `db_owner`。

以下的 `LibraryDemo` 與 `plan_reader` 都是示意名稱，請替換為實際資料庫與已存在的資料庫使用者：

```sql
USE [LibraryDemo];
GO
GRANT SHOWPLAN TO [plan_reader];
GO
```

`SHOWPLAN` 是資料庫層級權限，這段語法授權目前資料庫，不是整台 SQL Server。[GRANT Database Permissions](https://learn.microsoft.com/en-us/sql/t-sql/statements/grant-database-permissions-transact-sql)

授權後，用原本執行查詢的帳號，在同一個資料庫檢查：

```sql
SELECT DB_NAME() AS DatabaseName,
       USER_NAME() AS DatabaseUser,
       HAS_PERMS_BY_NAME(DB_NAME(), 'DATABASE', 'SHOWPLAN') AS HasShowplan;
```

`HasShowplan = 1` 代表目前帳號有此權限；`0` 代表沒有。確認後重新執行需要計畫的查詢。

如果查詢或 View 參照多個 SQL Server 資料庫，需要對各個被參照的資料庫確認 `SHOWPLAN`，不能只處理目前 `USE` 的資料庫。實際執行計畫也會執行 SQL，因此原本需要的 `SELECT`／`EXECUTE` 等權限仍須具備；`SHOWPLAN` 不會代替它們。Oracle linked server 的連線與物件權限則是另外一層。[執行計畫的權限需求](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-an-actual-execution-plan)

診斷結束後，若只需暫時授權，可由 DBA 撤回這次直接授予的權限：

```sql
USE [LibraryDemo];
GO
REVOKE SHOWPLAN FROM [plan_reader];
GO
```

如果帳號仍透過其他角色或群組取得同一權限，撤回直接授權後，權限檢查仍可能回 `1`。

## 執行計畫要看哪些數字 {#execution-plan-checks}

先查看耗時節點的執行次數與實際列數，再看它是否位於 Nested Loops 的內側。以下是**虛構的單執行緒示意資料**，用來說明重複掃描的量級：

| 指標 | 原計畫示意 | Hash Join 計畫示意 |
| --- | ---: | ---: |
| 昂貴內側節點執行次數 | 40 | 1 |
| 該節點每次輸出列數 | 800 | 800 |
| 該節點累計輸出列數 | 32,000 | 800 |

這組數字顯示的是節點工作量，不是整個查詢的最終結果。實際工具可能顯示每次平均值或全部執行的累計值，讀取 XML 時也要注意各執行緒的統計，避免把累計列數再乘上執行次數。

對含遠端資料來源的查詢，`Remote Scan` 的執行次數也不能直接當成遠端 SQL 完整重送次數；SQL Server 顯示的讀取資訊，不能代替遠端資料庫本身的 I/O 量測。

除了重掃，還要核對：

- Estimated Rows 與 Actual Rows 的差距。
- 整段查詢的 elapsed time、CPU 與 logical reads。
- Memory grant 與 spill 警告。
- 不同參數、少量與大量資料的表現。
- 應用程式完整請求的延遲，而不只單一 SQL 的耗時。

Hash Join 不保證所有來源只讀一次；平行執行、spill 或其他節點仍可能產生額外工作。計畫上的成本百分比是估算值，也不能代替實際耗時。

## OPTION (HASH JOIN) 與 INNER HASH JOIN 的差異 {#query-hint-vs-join-hint}

如果只想在 SQL 文字中指定一組表的 join，可以寫成：

```sql
SELECT b.BookID, COUNT_BIG(*) AS BorrowCount
FROM #Books AS b
INNER HASH JOIN #BorrowEvents AS e
    ON e.BookID = b.BookID
WHERE b.BookID IN (10, 20, 30)
GROUP BY b.BookID;
```

| 寫法 | 指定位置 | 作用與注意事項 |
| --- | --- | --- |
| `OPTION (HASH JOIN)` | 整個查詢末尾 | 限制 statement 的 join 策略；不等同 `FORCE ORDER` |
| `INNER HASH JOIN` | `FROM` 裡的一組 join | 指定該組表的策略，也會約束查詢中所有表的 join order |

第二種寫法雖然只在一組表旁邊出現，影響不一定局限在那一組。Microsoft 文件指出，使用這類 join hint 後，optimizer 會依 `ON` 的位置約束整個查詢的 join order；多表查詢尤其需要重新檢查計畫。[Join hints 官方說明](https://learn.microsoft.com/en-us/sql/t-sql/queries/hints-transact-sql-join)

### View 裡可以放哪一種 {#hints-in-view}

`CREATE VIEW` 的查詢定義不能直接包含 `OPTION` 子句，但允許在 `FROM` 使用 join hints。也就是可以在查詢 View 的外層 statement 加 `OPTION (HASH JOIN)`，或由 DBA 評估是否將適當的 join hint 放進 View 定義；這是兩個不同的變更。[CREATE VIEW 的限制](https://learn.microsoft.com/en-us/sql/t-sql/statements/create-view-transact-sql)

View 也不能參照本篇的暫存表；要練習建立 View，需另外在測試資料庫準備永久資料表。

共用 View 內的調整會影響其他 caller。外層 hint 測試變快後，仍須重跑真正呼叫端的 SQL，確認它不帶額外測試 hint 時，也能得到預期結果與效能。

## 什麼時候值得保留這個 Hint {#when-to-keep-hint}

可以先依下列順序決定：

1. 確認問題真的在 join 計畫，例如內側重掃；若主要在鎖定、來源全量運算或網路等待，先處理對應階段。
2. 檢查索引、統計資訊、條件選擇性及型別轉換，評估能否讓 optimizer 自己選出更好的計畫。
3. 比較不同參數與重複執行的結果，分開記錄第一次及後續查詢，避免把快取差異全算成 hint 的效果。
4. 確認 memory grant、spill、並行負載與其他 caller 沒有明顯退步。
5. 保留原定義與移除 hint 的方式；資料分布、索引或版本改變後，重新評估。

若既有 View／查詢的小幅調整已足以解決問題，可以先採用較小的改動；若真正瓶頸是遠端全量處理，就繼續評估條件下推或來源調校。測試 `HASH JOIN` 的價值，在於驗證 join 策略是否是關鍵因素。

## 參考資料 {#references}

- [Query hints：HASH JOIN 的範圍與限制](https://learn.microsoft.com/en-us/sql/t-sql/queries/hints-transact-sql-query)
- [Join hints：FROM 子句與 join order](https://learn.microsoft.com/en-us/sql/t-sql/queries/hints-transact-sql-join)
- [SQL Server Join 演算法](https://learn.microsoft.com/en-us/sql/relational-databases/performance/joins)
- [CREATE VIEW：OPTION 與暫存表限制](https://learn.microsoft.com/en-us/sql/t-sql/statements/create-view-transact-sql)
- [SQL Server 慢查詢診斷](https://learn.microsoft.com/en-us/troubleshoot/sql/database-engine/performance/troubleshoot-slow-running-queries)
- [SHOWPLAN 等資料庫權限的授權語法](https://learn.microsoft.com/en-us/sql/t-sql/statements/grant-database-permissions-transact-sql)
- [實際執行計畫的權限需求](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-an-actual-execution-plan)
