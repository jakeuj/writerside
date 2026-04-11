# App Service 使用 Managed Identity 連 Azure SQL（完整實戰筆記）

> 適用：Azure App Service → Azure SQL Database  
> 目的：避免使用帳密，改用 Microsoft Entra / Managed Identity

---

## 🧩 Step 1：開啟 App Service Managed Identity

### 操作路徑
Azure Portal → App Service → Identity

### 設定
- System assigned → **On**

### 取得資訊
- Object ID（後面建立 DB user 會用到）

---

## 🧩 Step 2：讓 Azure SQL 支援 Microsoft Entra

### 操作路徑
Azure Portal → SQL Server → Microsoft Entra ID

### 設定
- 設定 **Microsoft Entra Admin（使用者或群組）**

---

## 🧩 Step 3：在 DB 建立「服務帳號」

### 範例（slot）

```sql
USE [your-database];
GO

CREATE USER [your-app/slots/dev_mi]
FROM EXTERNAL PROVIDER
WITH OBJECT_ID = '<your-object-id>';
GO

ALTER ROLE db_datareader ADD MEMBER [your-app/slots/dev_mi];
ALTER ROLE db_datawriter ADD MEMBER [your-app/slots/dev_mi];
GO
```

---

## 🧩 Step 4：App Service 連線字串

```text
Server=tcp:<your-server>.database.windows.net,1433;
Database=<your-db>;
Authentication=Active Directory Managed Identity;
Encrypt=True;
TrustServerCertificate=False;
```

---

## 🧩 Step 5：.NET 程式（EF / SqlClient）

```csharp
using var connection = new SqlConnection(connectionString);
await connection.OpenAsync();
```

---

## 🎯 總結

App Service (Managed Identity)
↓
Microsoft Entra (Object ID)
↓
Azure SQL (CREATE USER ... WITH OBJECT_ID)
↓
DB Role（db_datareader / writer）
