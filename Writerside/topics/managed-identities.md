# Azure Managed Identity 受控識別

> **重要提醒：使用者指派身份識別的環境變數設定**
>
> 在 Azure App Service 使用**使用者指派的受控識別**時，必須在應用程式的**環境變數**中設定：
>
> ```
> AZURE_CLIENT_ID = <使用者指派身份識別的用戶端識別碼>
> ```
>
> 若未設定此環境變數，會導致以下錯誤：
>
> ```
> ManagedIdentityCredential authentication failed: Unable to load the proper Managed Identity.
> ```
>
> **如何取得用戶端識別碼：**
>
> 1. 在 Azure Portal 中開啟您的**受控識別**資源
> 2. 在**概觀**頁面中複製**用戶端識別碼**（Client ID）
> 3. 在 App Service 的**設定** > **環境變數**中新增 `AZURE_CLIENT_ID`
>
> **注意：** 系統指派的受控識別不需要此設定。
>
{style="warning"}

這是一篇關於 Azure App Service 裡面設定身份識別的說明文件，
主要說明由 Azure Portal 搜尋 `受控識別`，來建立使用者指派的管理型身分識別，
如此可以到 Key Vault 裡面授權該身分識別存取金鑰。
另外也說明系統指派的管理型身分識別的設定方式。

## 什麼是 Managed Identity？

Managed Identity（受控識別）是 Microsoft Entra ID（前身為 Azure Active Directory）提供的一項功能，讓 Azure 服務（如 Azure App Service、Azure Functions、Azure VM 等）能夠自動獲得一個由 Azure 平台管理的身分識別。

**主要優勢：**

- **無需管理憑證或密碼**：Azure 平台自動管理身分識別的生命週期
- **提升安全性**：不需要在程式碼或設定檔中儲存敏感的連線字串或金鑰
- **簡化存取控制**：透過 Azure RBAC（角色型存取控制）輕鬆管理權限
- **支援多種 Azure 資源**：可用於存取 Key Vault、Storage、SQL Database 等服務

## 受控識別的類型

Azure 提供兩種類型的受控識別：

### 1. 系統指派的受控識別（System-assigned Managed Identity）

- **生命週期綁定資源**：與 Azure 資源（如 App Service）同生共滅
- **一對一關係**：每個資源只能有一個系統指派的受控識別
- **自動管理**：當資源被刪除時，身分識別也會自動刪除
- **適用場景**：單一應用程式需要存取 Azure 資源

### 2. 使用者指派的受控識別（User-assigned Managed Identity）

- **獨立的 Azure 資源**：可以獨立建立和管理
- **可重複使用**：一個使用者指派的身分識別可以指派給多個 Azure 資源
- **彈性管理**：刪除應用程式不會影響身分識別的存在
- **適用場景**：多個應用程式需要共用相同的權限，或需要在資源刪除後保留身分識別

**兩者比較：**

| 特性 | 系統指派 | 使用者指派 |
|------|---------|-----------|
| 建立方式 | 在 Azure 資源上啟用 | 獨立建立 Azure 資源 |
| 生命週期 | 與資源綁定 | 獨立管理 |
| 數量限制 | 每個資源一個 | 每個資源可多個 |
| 共享性 | 不可共享 | 可跨多個資源共享 |

## 在 Azure App Service 中啟用受控識別

### 啟用系統指派的受控識別

**透過 Azure Portal：**

1. 在 [Azure Portal](https://portal.azure.com) 中，導航到您的 App Service
2. 在左側選單選擇 **設定** > **身分識別**（Identity）
3. 在 **系統指派** 分頁中，將 **狀態** 切換為 **開啟**
4. 點擊 **儲存**

**透過 Azure CLI：**

```bash
az webapp identity assign \
  --resource-group <resource-group-name> \
  --name <app-name>
```

**透過 Azure PowerShell：**

```powershell
Set-AzWebApp -AssignIdentity $true `
  -ResourceGroupName <resource-group-name> `
  -Name <app-name>
```

### 建立並指派使用者指派的受控識別

**透過 Azure Portal：**

1. 在 Azure Portal 搜尋 **受控識別**（Managed Identities）
2. 點擊 **+ 建立** 來建立新的使用者指派受控識別
3. 填寫資源群組、區域和名稱
4. 點擊 **檢閱 + 建立**

![userAssignedIdentities.png](userAssignedIdentities.png)

1. 建立完成後，導航到您的 App Service
2. 選擇 **設定** > **身分識別**
3. 切換到 **使用者指派** 分頁
4. 點擊 **+ 新增**
5. 搜尋並選擇剛才建立的受控識別
6. 點擊 **新增**

**透過 Azure CLI：**

```bash
# 建立使用者指派的受控識別
az identity create \
  --resource-group <resource-group-name> \
  --name <identity-name>

# 將受控識別指派給 App Service
az webapp identity assign \
  --resource-group <resource-group-name> \
  --name <app-name> \
  --identities <identity-resource-id>
```

## 使用受控識別存取 Azure 資源

### 授予權限

在使用受控識別存取 Azure 資源之前，必須先授予適當的權限。以下以常見的 Azure 服務為例：

#### 存取 Azure Key Vault

1. 在 Azure Portal 中，導航到您的 **Key Vault**
2. 選擇 **存取控制 (IAM)**
3. 點擊 **+ 新增角色指派**
4. 選擇適當的角色（例如：**Key Vault Secrets User** 或 **Key Vault Secrets Officer**）
5. 在 **成員** 頁面，選擇 **受控識別**
6. 搜尋並選擇您的 App Service 或使用者指派的受控識別
7. 點擊 **檢閱 + 指派**

#### 存取 Azure Storage

1. 導航到您的 **儲存體帳戶**
2. 選擇 **存取控制 (IAM)**
3. 點擊 **+ 新增角色指派**
4. 選擇適當的角色（例如：**Storage Blob Data Reader** 或 **Storage Blob Data Contributor**）
5. 選擇您的受控識別並完成指派

#### 存取 Azure SQL Database

1. 在 SQL Database 中執行以下 T-SQL 指令：

```sql
-- 建立使用者（使用受控識別的名稱）
CREATE USER [<managed-identity-name>] FROM EXTERNAL PROVIDER;

-- 授予權限
ALTER ROLE db_datareader ADD MEMBER [<managed-identity-name>];
ALTER ROLE db_datawriter ADD MEMBER [<managed-identity-name>];
```

### 程式碼範例

#### .NET / C# 範例

使用 Azure Identity 函式庫的 `DefaultAzureCredential` 是最簡單的方式：

**存取 Key Vault：**

```c#
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;

// 系統指派的受控識別
var credential = new DefaultAzureCredential();

// 使用者指派的受控識別（需指定 Client ID）
// var credential = new DefaultAzureCredential(
//     new DefaultAzureCredentialOptions
//     {
//         ManagedIdentityClientId = "<user-assigned-client-id>"
//     });

var client = new SecretClient(
    new Uri("https://<your-key-vault-name>.vault.azure.net/"),
    credential);

KeyVaultSecret secret = await client.GetSecretAsync("<secret-name>");
string secretValue = secret.Value;
```

**存取 Azure Storage：**

```c#
using Azure.Identity;
using Azure.Storage.Blobs;

var credential = new DefaultAzureCredential();

var blobServiceClient = new BlobServiceClient(
    new Uri("https://<storage-account-name>.blob.core.windows.net"),
    credential);

var containerClient = blobServiceClient.GetBlobContainerClient("<container-name>");
```

**存取 Azure SQL Database：**

```c#
using Azure.Identity;
using Microsoft.Data.SqlClient;

var credential = new DefaultAzureCredential();

var connectionString =
    "Server=<server-name>.database.windows.net;" +
    "Database=<database-name>;" +
    "Authentication=Active Directory Default;";

using var connection = new SqlConnection(connectionString);
await connection.OpenAsync();
```

#### Python 範例

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# 系統指派的受控識別
credential = DefaultAzureCredential()

# 使用者指派的受控識別
# credential = DefaultAzureCredential(
#     managed_identity_client_id="<user-assigned-client-id>"
# )

# 存取 Key Vault
vault_url = "https://<your-key-vault-name>.vault.azure.net/"
client = SecretClient(vault_url=vault_url, credential=credential)

secret = client.get_secret("<secret-name>")
print(f"Secret value: {secret.value}")
```

#### Node.js / JavaScript 範例

```javascript
const { DefaultAzureCredential } = require("@azure/identity");
const { SecretClient } = require("@azure/keyvault-secrets");

// 系統指派的受控識別
const credential = new DefaultAzureCredential();

// 使用者指派的受控識別
// const credential = new DefaultAzureCredential({
//     managedIdentityClientId: "<user-assigned-client-id>"
// });

const vaultUrl = "https://<your-key-vault-name>.vault.azure.net/";
const client = new SecretClient(vaultUrl, credential);

async function getSecret() {
    const secret = await client.getSecret("<secret-name>");
    console.log(`Secret value: ${secret.value}`);
}

getSecret();
```

## 實際應用場景

### 場景 1：App Service 存取 Key Vault 中的連線字串

傳統做法需要在應用程式設定中儲存連線字串，使用受控識別後：

1. 將連線字串儲存在 Key Vault 中
2. 為 App Service 啟用系統指派的受控識別
3. 在 Key Vault 中授予該身分識別 **Key Vault Secrets User** 角色
4. 在程式碼中使用 `DefaultAzureCredential` 讀取密碼

### 場景 2：多個應用程式共用相同的 Storage 存取權限

1. 建立一個使用者指派的受控識別
2. 在 Storage Account 中授予該身分識別 **Storage Blob Data Contributor** 角色
3. 將此受控識別指派給多個 App Service
4. 所有應用程式都能使用相同的身分識別存取 Storage

### 場景 3：無密碼連線到 Azure SQL Database

1. 為 App Service 啟用受控識別
2. 在 SQL Database 中建立對應的使用者並授予權限
3. 使用 `Authentication=Active Directory Default` 連線字串
4. 不需要在任何地方儲存資料庫密碼

## 注意事項與最佳實務

1. **權限最小化原則**：只授予應用程式所需的最小權限
2. **快取機制**：受控識別的權限變更可能需要最多 24 小時才會生效
3. **本地開發**：`DefaultAzureCredential` 在本地開發時會自動使用 Azure CLI 或 Visual Studio 的認證
4. **跨租戶限制**：受控識別不支援跨目錄/租戶的存取場景
5. **監控與稽核**：透過 Azure Monitor 和 Activity Log 追蹤受控識別的使用情況

## 參考資源

- [Azure App Service 受控識別概觀](https://learn.microsoft.com/zh-tw/azure/app-service/overview-managed-identity)
- [Azure 受控識別文件](https://learn.microsoft.com/zh-tw/entra/identity/managed-identities-azure-resources/overview)
- [Azure Identity 用戶端程式庫](https://learn.microsoft.com/zh-tw/dotnet/api/overview/azure/identity-readme)
