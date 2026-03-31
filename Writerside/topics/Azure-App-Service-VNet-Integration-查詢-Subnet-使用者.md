# Azure App Service VNet Integration 查詢哪個 Subnet 正在被使用

先講結論：要查哪個 Azure App Service / Function App 正在使用某個 VNet subnet 做 VNet Integration，先把目標 subnet 組成完整 resource ID，然後優先用 `az webapp list` 或 `az functionapp list` 比對 `virtualNetworkSubnetId`；如果還要跨多個 subscription 盤點，再補 `az graph query` 驗證。不要先假設 `az resource list --resource-type Microsoft.Web/sites` 一定查得到。

<tldr>
<p>單一 subscription：優先用 <code>az webapp list</code> / <code>az functionapp list</code> 查 <code>virtualNetworkSubnetId</code>。</p>
<p><code>az resource list</code> 可能回空結果，不適合當唯一依據。</p>
<p>跨多個 subscription 盤點時，再補 <code>az graph query</code> 驗證。</p>
</tldr>

> 本文中的 subscription ID、resource group、VNet、subnet、App Service 與 App Service Plan 名稱皆已去識別化，請替換成你自己的 Azure 資源。

## 這次案例直接查到的結果

這次實際查到的 App Service 有 2 個，以下列出去識別化後的名稱：

- `app-frontend-prod`
- `app-api-prod`

兩個都使用同一個 App Service Plan：

```text
/subscriptions/<subscription-id>/resourceGroups/<app-rg>/providers/Microsoft.Web/serverfarms/<shared-app-service-plan>
```

## 問題描述

當 Azure Portal 或變更流程提到某個 subnet 已被 App Service VNet Integration 使用時，常見需求是：

- 想知道到底是哪個 Web App 在用這個 subnet
- 想評估 subnet 能不能回收、改名或調整設定
- 想確認 App Service VNet Integration 是否真的已經綁到指定 subnet

這次要查的 subnet 範例如下：

```text
/subscriptions/<subscription-id>/resourceGroups/<network-rg>/providers/Microsoft.Network/virtualNetworks/<shared-vnet>/subnets/<appservice-integration-subnet>
```

## 為什麼不要只用 az resource list

一開始很直覺會想這樣查：

```bash
az resource list \
  --resource-type Microsoft.Web/sites \
  --query "[?properties.virtualNetworkSubnetId=='<subnet-resource-id>']"
```

但這次實際測到，即使 Web App 真的有綁 VNet Integration，這條查詢仍然可能回傳空結果。

也就是說：

- `Microsoft.Web/sites` 的 generic ARM listing 不一定會把你要的欄位完整帶出來
- 至少在 App Service VNet Integration 這個情境，`az webapp list` 比 `az resource list` 更可靠

## 建議查詢流程

### 1. 先確認目前 Azure CLI 的 subscription

```bash
az account show -o json
```

如果你有多個 subscription，先切到正確的那個：

```bash
az account list -o table
az account set --subscription <subscription-id>
```

### 2. 用 az webapp list 查 App Service

```bash
SUBSCRIPTION_ID="<subscription-id>"
NETWORK_RG="<network-rg>"
VNET_NAME="<shared-vnet>"
SUBNET_NAME="<appservice-integration-subnet>"

TARGET="/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${NETWORK_RG}/providers/Microsoft.Network/virtualNetworks/${VNET_NAME}/subnets/${SUBNET_NAME}"

az webapp list \
  --query "[?virtualNetworkSubnetId=='${TARGET}'].{name:name,resourceGroup:resourceGroup,state:state,kind:kind,location:location,appServicePlanId:appServicePlanId}" \
  -o table
```

這次回傳結果整理如下，表格內容同樣已去識別化：

| Name | Resource Group | State | Location | App Service Plan |
| ---- | ---- | ---- | ---- | ---- |
| `app-frontend-prod` | `rg-portal-prod` | `Running` | `Southeast Asia` | `asp-shared-prod` |
| `app-api-prod` | `rg-sales-prod` | `Running` | `Southeast Asia` | `asp-shared-prod` |

### 3. 如果懷疑有 Function App，也一起查

```bash
SUBSCRIPTION_ID="<subscription-id>"
NETWORK_RG="<network-rg>"
VNET_NAME="<shared-vnet>"
SUBNET_NAME="<appservice-integration-subnet>"

TARGET="/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${NETWORK_RG}/providers/Microsoft.Network/virtualNetworks/${VNET_NAME}/subnets/${SUBNET_NAME}"

az functionapp list \
  --query "[?virtualNetworkSubnetId=='${TARGET}'].{name:name,resourceGroup:resourceGroup,state:state,kind:kind,location:location}" \
  -o table
```

這次查詢沒有找到使用這個 subnet 的 Function App。

### 4. 需要再確認時，用 az webapp show 驗證單一 App

如果你已經查到候選 App，可以再對單一 Web App 做確認：

```bash
APP_RESOURCE_GROUP="<app-rg>"
APP_NAME="<app-name>"

az webapp show -g "${APP_RESOURCE_GROUP}" -n "${APP_NAME}" -o json
```

重點看這些欄位：

- `virtualNetworkSubnetId`
- `appServicePlanId`
- `outboundVnetRouting`

如果你要查更細的網站設定，也可以補查：

```bash
az webapp config show -g "${APP_RESOURCE_GROUP}" -n "${APP_NAME}" -o json
```

### 5. 要做跨多個 subscription 的盤點時，改用 Resource Graph

如果你不是只查單一 subscription，或是想做大範圍盤點，建議再補一條 Azure Resource Graph 查詢：

```bash
az extension add --name resource-graph
```

```bash
SUBSCRIPTION_ID="<subscription-id>"
NETWORK_RG="<network-rg>"
VNET_NAME="<shared-vnet>"
SUBNET_NAME="<appservice-integration-subnet>"

TARGET="/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${NETWORK_RG}/providers/Microsoft.Network/virtualNetworks/${VNET_NAME}/subnets/${SUBNET_NAME}"

az graph query -q "
Resources
| where type =~ 'microsoft.web/sites'
| where tostring(properties.virtualNetworkSubnetId) =~ '${TARGET}'
| project name, resourceGroup, kind, location, appServicePlan=tostring(properties.serverFarmId), subnetId=tostring(properties.virtualNetworkSubnetId)
" -o json
```

這次查詢結果同樣回傳 2 筆，和 `az webapp list` 的結果一致。

## 這次案例的重點整理

這次查指定 subnet 時，最有用的判斷點有三個：

1. 先確認 Azure CLI 目前切到正確 subscription。
2. 查 App Service VNet Integration 時，優先用 `az webapp list` / `az functionapp list` 看 `virtualNetworkSubnetId`。
3. 如果 generic ARM listing 查不到，不要立刻下結論，改用 service-specific command 或 Resource Graph 再驗一次。

## 補充說明

- 如果問題提到 deployment slot，記得另外查 `Microsoft.Web/sites/slots` 或直接檢查對應 slot。
- 如果 subnet 可能不是給 App Service 用，而是 VM、Private Endpoint 或其他 NIC-based 資源在用，就要改查 `az network nic list`、Private Endpoint 或 subnet delegation。
- App Service VNet Integration 是 outbound network path 的常見查法，不代表網站本身一定是 private inbound only。

## 參考

- [Azure App Service Deploy](Azure-App-Service-Deploy.md)
- [AzureSql Vnet AppService](AzureSqlVnetAppService.md)
