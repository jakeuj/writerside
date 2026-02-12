# MSSQL 遞迴 CTE (Common Table Expression) 說明文件

## 簡介

遞迴 CTE 是一種結構化查詢語言 (SQL) 功能，允許在表達式中定義遞迴查詢。這些查詢經常用於處理層次結構數據，例如組織結構、目錄路徑或圖狀結構。

## 語法

```sql
WITH cte_structure (column1, column2, ...) AS (
    -- 基礎查詢 (Anchor Query)
    SELECT column1, column2, ...
    FROM table_name
    WHERE condition

    UNION ALL

    -- 遞迴部分 (Recursive Query)
    SELECT column1, column2, ...
    FROM table_name
    INNER JOIN cte_structure ON table_name.column = cte_structure.column
    WHERE condition
)
SELECT *
FROM cte_structure;
```

## 組成部分

1. **基礎查詢 (Anchor Query)**
    - 定義遞迴的初始數據集。
    - 這是 CTE 的第一部分，必須是非遞迴的。
2. **遞迴部分 (Recursive Query)**
    - 基於 Anchor Query 的結果執行遞迴操作。
    - 通常包含對自身的引用。
3. **結合運算符 (UNION ALL)**
    - 將基礎查詢和遞迴部分的結果結合。
4. **終止條件**
    - MSSQL 會自動判斷遞迴的終止條件，根據查詢中不再返回任何新行時停止遞迴。

## 範例：組織結構的遞迴查詢

假設有一個 `Employees` 表，包含以下欄位：

- `EmployeeID`: 員工編號
- `EmployeeName`: 員工姓名
- `ManagerID`: 上級管理者的員工編號

表結構如下：

| EmployeeID | EmployeeName | ManagerID |
|------------|--------------|-----------|
| 1          | Alice        | NULL      |
| 2          | Bob          | 1         |
| 3          | Charlie      | 1         |
| 4          | David        | 2         |
| 5          | Eve          | 2         |

查詢組織結構樹：

```sql
WITH EmployeeHierarchy AS (
    -- 基礎查詢：找到所有沒有管理者的員工 (根節點)
    SELECT EmployeeID, EmployeeName, ManagerID, 0 AS Level
    FROM Employees
    WHERE ManagerID IS NULL

    UNION ALL

    -- 遞迴部分：找到所有下屬員工
    SELECT e.EmployeeID, e.EmployeeName, e.ManagerID, eh.Level + 1
    FROM Employees e
    INNER JOIN EmployeeHierarchy eh ON e.ManagerID = eh.EmployeeID
)
SELECT EmployeeID, EmployeeName, ManagerID, Level
FROM EmployeeHierarchy
ORDER BY Level, EmployeeID;
```

### 查詢結果

| EmployeeID | EmployeeName | ManagerID | Level |
|------------|--------------|-----------|-------|
| 1          | Alice        | NULL      | 0     |
| 2          | Bob          | 1         | 1     |
| 3          | Charlie      | 1         | 1     |
| 4          | David        | 2         | 2     |
| 5          | Eve          | 2         | 2     |

## 使用遞迴 CTE 的注意事項

1. **防止無限遞迴**
    - 確保遞迴查詢的條件正確，避免產生無限循環。
    - 可以使用 `OPTION (MAXRECURSION n)` 限制遞迴層數，`n` 是最大遞迴層數。

    ```sql
    OPTION (MAXRECURSION 100);
    ```

2. **效能問題**
    - 遞迴查詢可能會對大型數據集造成性能影響。
    - 儘量確保基礎查詢和遞迴部分經過索引優化。

## 結語

遞迴 CTE 是處理層次結構數據的強大工具，透過清晰的語法和靈活的設計，可以輕鬆實現複雜的遞迴邏輯。
