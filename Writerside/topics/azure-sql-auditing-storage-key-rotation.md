# Azure SQL 稽核寫不進儲存體：金鑰重新產生後要重新儲存稽核設定

<web-summary>Azure SQL 稽核告警顯示無法寫入儲存體帳戶時，用 Azure CLI 比對稽核驗證方式與儲存體金鑰建立時間找出原因，重新儲存稽核設定並關閉重複的資料庫層稽核。</web-summary>

收到「SQL Audit logs ... are not being recorded in storage account」告警時，先查稽核是不是用**儲存體存取金鑰**寫入，以及該金鑰最近有沒有重新產生。兩者都成立時，到伺服器層稽核頁面重新按一次「儲存」即可恢復；如果資料庫層也開了相同的稽核，順便關掉，只保留伺服器層。

> 本文的 server、database、storage account、resource group 與 subscription 名稱皆已去識別化。

## 問題描述

Azure 寄出的告警大意是：

- 某個資料庫的稽核無法寫入指定的儲存體帳戶。
- 可能原因有三種：儲存體金鑰重新產生、儲存體設定了 VNet 或防火牆規則、訂用帳戶被停用（儲存體變成唯讀）。
- 建議到資料庫的稽核設定重新儲存一次。

告警只列出可能原因，不會告訴你是哪一種。直接按「儲存」通常能解決金鑰問題，但如果是防火牆造成的，存完很快又會失敗，所以先花幾分鐘確認原因。

## 根本原因

稽核設定選擇「儲存體存取金鑰」驗證時，SQL 會在儲存設定的當下記住那把金鑰。之後有人在儲存體帳戶重新產生該金鑰，SQL 手上的舊金鑰就失效，稽核記錄從那一刻起都寫不進去，直到重新儲存稽核設定為止。

本次案例的證據：

- 伺服器層與資料庫層稽核的 `isManagedIdentityInUse` 都是 `false`、`isStorageSecondaryKeyInUse` 是 `false`，代表用主要金鑰 `key1` 寫入。
- 儲存體帳戶的 `keyCreationTime.key1` 比最後一次儲存稽核設定還晚，表示金鑰換過、稽核設定沒跟著更新。
- 儲存體防火牆 `defaultAction` 是 `Allow`，訂用帳戶狀態是 `Enabled`，排除另外兩個原因。

## 用 Azure CLI 確認原因

以下指令都是唯讀查詢。先設定變數：

```bash
SUB="<subscription>"
RG="<resource-group>"
SERVER="<server-name>"
DB="<database-name>"
STORAGE="<storage-account>"
```

### 查稽核的驗證方式 {#check-audit-auth}

```bash
az sql server audit-policy show -g "$RG" -n "$SERVER" --subscription "$SUB" \
  --query "{state:state,blob:blobStorageTargetState,mi:isManagedIdentityInUse,secondaryKey:isStorageSecondaryKeyInUse,endpoint:storageEndpoint}" -o json

az sql db audit-policy show -g "$RG" -s "$SERVER" -n "$DB" --subscription "$SUB" \
  --query "{state:state,blob:blobStorageTargetState,mi:isManagedIdentityInUse,secondaryKey:isStorageSecondaryKeyInUse,endpoint:storageEndpoint}" -o json
```

`mi` 為 `false` 時是用存取金鑰；`secondaryKey` 為 `false` 是 `key1`，`true` 是 `key2`。

### 查儲存體金鑰與防火牆 {#check-storage}

```bash
az storage account show -n "$STORAGE" --subscription "$SUB" \
  --query "{keyCreationTime:keyCreationTime,allowSharedKeyAccess:allowSharedKeyAccess,network:networkRuleSet}" -o json
```

判讀方式：

| 欄位 | 代表的原因 |
| --- | --- |
| `keyCreationTime` 中稽核使用的那把金鑰時間很新 | 金鑰重新產生過，重新儲存稽核設定 |
| `allowSharedKeyAccess` 是 `false` | 儲存體禁止金鑰存取，要改用受控識別 |
| `networkRuleSet.defaultAction` 是 `Deny` 且 `bypass` 沒有 `AzureServices` | 防火牆擋住，改用受控識別並允許受信任的 Azure 服務 |

再確認訂用帳戶不是停用狀態：

```bash
az account show --subscription "$SUB" --query state -o tsv
```

### 查最近誰改過稽核設定 {#check-activity-log}

```bash
az monitor activity-log list --subscription "$SUB" --resource-group "$RG" --offset 90d \
  --query "[?authorization.action && contains(authorization.action,'auditingSettings')].{time:eventTimestamp,op:authorization.action,status:status.value}" \
  -o table
```

activity log 只保留 90 天。金鑰換的時間更早時查不到，就以 `keyCreationTime` 與稽核設定的對照為準。

## 解決方案

### 重新儲存伺服器層稽核 {#resave-server-audit}

在 Azure Portal 開啟 SQL 伺服器的「安全性 > 稽核」，不改任何欄位，直接按「儲存」。Portal 會讀取儲存體目前的金鑰，寫回稽核設定。

也可以用 CLI 重新套用，只指定儲存體帳戶名稱時，CLI 會自行取得目前的金鑰：

```bash
az sql server audit-policy update -g "$RG" -n "$SERVER" --subscription "$SUB" \
  --state Enabled --blob-storage-target-state Enabled --storage-account "$STORAGE"
```

### 關閉重複的資料庫層稽核 {#disable-db-audit}

伺服器層稽核會套用到該伺服器上的所有資料庫。同一個資料庫如果又開了資料庫層稽核，同樣的事件會寫兩份。除非資料庫需要不同的稽核事件或不同的保存位置，否則只保留伺服器層。

先列出哪些資料庫有開資料庫層稽核：

```bash
for db in $(az sql db list -g "$RG" -s "$SERVER" --subscription "$SUB" --query "[?name!='master'].name" -o tsv); do
  echo "$db: $(az sql db audit-policy show -g "$RG" -s "$SERVER" -n "$db" --subscription "$SUB" --query state -o tsv)"
done
```

在 Portal 開啟該資料庫的「安全性 > 稽核」，頁面上方會顯示「伺服器層級的稽核：已啟用」。把「啟用 Azure SQL 稽核」關掉後按「儲存」。CLI 等效指令：

```bash
az sql db audit-policy update -g "$RG" -s "$SERVER" -n "$DB" --subscription "$SUB" --state Disabled
```

關閉資料庫層稽核不會刪除已寫入儲存體的稽核記錄。

> 順序很重要：先修好伺服器層，再關資料庫層。伺服器層還在用舊金鑰時就關資料庫層，等於整台伺服器都沒有可用的稽核。

## 驗證方式

```bash
az sql server audit-policy show -g "$RG" -n "$SERVER" --subscription "$SUB" \
  --query "[state,blobStorageTargetState,storageEndpoint]" -o tsv

az sql db audit-policy show -g "$RG" -s "$SERVER" -n "$DB" --subscription "$SUB" \
  --query "[state,blobStorageTargetState]" -o tsv
```

預期伺服器層為 `Enabled Enabled <storage-endpoint>`，資料庫層為 `Disabled Disabled`。

要確認記錄真的恢復寫入，可在伺服器的稽核頁面按「檢視稽核記錄」，或在有 `Storage Blob Data Reader` 權限時查看 `sqldbauditlogs` container 底下最新 blob 的修改時間。

## 避免下次再發生

存取金鑰驗證只要有人輪替金鑰就會再壞一次。有兩種做法：

- **改用受控識別（建議）**：在儲存體帳戶授予 SQL 伺服器的受控識別 `Storage Blob Data Contributor` 角色，再把稽核的「儲存體驗證類型」改成「受控識別」。之後輪替金鑰不會影響稽核，儲存體也能維持防火牆限制。
- **繼續用金鑰時照順序輪替**：先把稽核改用次要金鑰並儲存，再重新產生主要金鑰；改回主要金鑰並儲存後，才重新產生次要金鑰。這樣輪替過程中稽核不會中斷。

## 參考資料

- [Auditing for Azure SQL Database and Azure Synapse Analytics](https://learn.microsoft.com/azure/azure-sql/database/auditing-overview)
- [Set up auditing for Azure SQL Database](https://learn.microsoft.com/azure/azure-sql/database/auditing-setup)
- [az sql server audit-policy](https://learn.microsoft.com/cli/azure/sql/server/audit-policy)
- [az sql db audit-policy](https://learn.microsoft.com/cli/azure/sql/db/audit-policy)
