# 免費 Azure SQL DB 定價層 Free

> **原文發布日期:** 2021-08-16
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/08/16/AzureSqlDbFree
> **標籤:** 無

---

最近才知道原來 Azure SQL 也有免費的可以用

加上原本就可以選的 App Service F1 Free

有時候想測試一些東西可以省一些額度

這邊記錄一下

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/5f4ada0d-336c-4133-aa79-391602cf434e/1629782873.png)

結論：

```
az group create --name testRg --location southeastasia
az sql server create --name testServer --resource-group testRg --location southeastasia --admin-user azureuser --admin-password YourPassword123!
az sql db create -g testRg -s testServer -n testDb --service-objective Free --backup-storage-redundancy Local
```

* g：資源群組名稱
* s：SQL Server 名稱
* n：DB 名稱
* service-objective：定價層

```
# 定義變數
$resourceGroup = "testRg"
$location = "southeastasia"
$sqlServer = "testServer"
$sqlAdminUser = "azureuser"
$sqlAdminPassword = "YourPassword123!"  # 請確保符合密碼規則
$databaseName = "testDb"
$serviceObjective = "Free"
$backupStorageRedundancy = "Local"
$firewallRuleName = "AllowMyIP"

# 取得目前公網 IP
$myIp = (Invoke-RestMethod -Uri "https://api.ipify.org?format=json").ip

# 建立 Resource Group
az group create --name $resourceGroup --location $location

# 建立 SQL Server
az sql server create `
  --name $sqlServer `
  --resource-group $resourceGroup `
  --location $location `
  --admin-user $sqlAdminUser `
  --admin-password $sqlAdminPassword

# 建立 SQL Database
az sql db create `
  --resource-group $resourceGroup `
  --server $sqlServer `
  --name $databaseName `
  --service-objective $serviceObjective
  --backup-storage-redundancy $backupStorageRedundancy

# 建立防火牆規則，允許目前用戶 IP
az sql server firewall-rule create `
  --resource-group $resourceGroup `
  --server $sqlServer `
  --name $firewallRuleName `
  --start-ip-address $myIp `
  --end-ip-address $myIp
```

總之重點就是最後的 Free 就可以開免費的 DB

至於 App Service 就是開定價層的時候選測試開發用的 F1 就是免費了

雖然每個 App Service 每天只能跑一小時

但我目前自己測試起來是還夠用

---

延伸閱讀

App Service Plan **基本**、**標準**、**進階版 =>** **無論有多少個應用程式都是同樣價錢**

除了 **免費** 層之外，App Service 方案會對其使用的計算資源收費。

* 在 **共用** 層中，每個應用程式都會收到 cpu 分鐘的配額，因此 *每個應用程式* 都需支付 cpu 配額的費用。
* 在專用計算層 (**基本**、**標準**、**進階版**、 **>premiumv2**、 **PremiumV3**) ，App Service 計畫會定義應用程式所調整的 vm 實例數目，因此會收取 App Service 方案中的 *每個 vm 實例* 的費用。 無論有多少個應用程式在 VM 執行個體上執行，這些 VM 執行個體皆採相同收費。 為了避免產生非預期的費用，請參閱[清除 App Service 方案](https://docs.microsoft.com/zh-tw/azure/app-service/app-service-plan-manage#delete)。

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Azure SQL](/jakeuj/Tags?qq=Azure%20SQL)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
