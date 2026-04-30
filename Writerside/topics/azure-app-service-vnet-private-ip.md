# Azure App Service VNet Integration 後如何查內網 IP

Azure App Service 啟用 VNet Integration 後，可以在 Kudu 透過 `WEBSITE_PRIVATE_IP` 查到目前 App Service instance 從 integration subnet 拿到的 private IP。這個 IP 是 App Service 出站連到 VNet、Private Endpoint、內網或 on-prem 資源時使用，不是讓內網 client 連進 App Service 的 inbound IP。

<tldr>
<p><code>WEBSITE_PRIVATE_IP</code> 會從 App Service Integration Subnet 的位址範圍指派，而且可能改變。</p>
<p>Firewall 不要只放行目前看到的單一 IP，應該放行整個 integration subnet CIDR，例如 <code>&lt;integration-subnet-cidr&gt;</code>。</p>
<p>如果要讓內網連進 App Service，要看 App Service Private Endpoint 的 NIC private IP，不是 <code>WEBSITE_PRIVATE_IP</code>。</p>
</tldr>

> 本文中的 resource group、VNet、subnet、App Service 名稱、IP 與 CIDR 皆已去識別化，請替換成你自己的 Azure 資源。

## 先分清楚兩種 private IP

| 情境 | 要看的 IP | 用途 |
| --- | --- | --- |
| App Service VNet Integration | `WEBSITE_PRIVATE_IP` | App Service 出站連到 VNet、Private Endpoint、VPN、ExpressRoute 或 on-prem 資源 |
| App Service Private Endpoint | Private Endpoint NIC 的 private IP | 內網 client 透過 Private Link 入站連進 App Service |

這兩個 IP 很容易被混在一起，但方向完全不同：

- VNet Integration 解決的是 **App Service 往外連**。
- Private Endpoint 解決的是 **內網往 App Service 連進來**。

## 查法一：在 Kudu Debug Console 查 `WEBSITE_PRIVATE_IP`

從 Azure Portal 開啟：

1. 進入 App Service。
2. 開啟 **Development Tools** > **Advanced Tools**。
3. 選 **Go**。
4. 在 Kudu 頁面開 **Tools** > **Debug Console**。

也可以直接開：

```text
https://<app-name>.scm.azurewebsites.net/DebugConsole
```

如果是 slot，SCM 網址通常會是：

```text
https://<app-name>-<slot-name>.scm.azurewebsites.net/DebugConsole
```

Windows App Service 執行：

```batch
SET WEBSITE_PRIVATE_IP
```

成功時會看到類似：

```text
WEBSITE_PRIVATE_IP=<private-ip>
```

Linux App Service 執行：

```bash
set | egrep --color 'WEBSITE_PRIVATE_IP'
```

如果完全查不到這個環境變數，先回到 App Service 的 **Networking** > **VNet Integration** 檢查是否真的已連上 VNet，以及是否選到正確的 integration subnet。

## 查法二：在 Kudu Environment 查

Kudu 也可以直接看環境變數頁面：

```text
https://<app-name>.scm.azurewebsites.net/Env
```

進去後搜尋 `WEBSITE_PRIVATE_IP`。這個方式適合只想確認目前值，不想進 Debug Console 執行指令的情境。

## 查 integration subnet CIDR

`WEBSITE_PRIVATE_IP` 只用來確認 App Service 目前確實有拿到 VNet Integration 的 private IP。要提供給 firewall 或網路團隊時，重點通常是 integration subnet 的整段 CIDR。

先查 App Service 目前整合到哪個 subnet：

```bash
APP_RESOURCE_GROUP="<app-resource-group>"
APP_NAME="<app-name>"

az webapp show \
  --resource-group "${APP_RESOURCE_GROUP}" \
  --name "${APP_NAME}" \
  --query "{name:name, subnet:virtualNetworkSubnetId}" \
  --output json
```

如果是 slot，加上 `--slot`：

```bash
az webapp show \
  --resource-group "${APP_RESOURCE_GROUP}" \
  --name "${APP_NAME}" \
  --slot "<slot-name>" \
  --query "{name:name, subnet:virtualNetworkSubnetId}" \
  --output json
```

拿到 `virtualNetworkSubnetId` 後，再查 subnet address prefix：

```bash
az network vnet subnet show \
  --ids "<integration-subnet-resource-id>" \
  --query "{name:name, addressPrefixes:addressPrefixes, addressPrefix:addressPrefix, delegation:delegations[].serviceName}" \
  --output json
```

這裡要確認：

- `addressPrefixes` 或 `addressPrefix` 是你要給 firewall 放行的來源範圍。
- subnet delegation 應該是 `Microsoft.Web/serverFarms`。
- 若 integration subnet 掛了 NSG 或 route table，也要一起檢查 outbound 規則與路由。

## Firewall 應該放行整個 integration subnet

不要把目前查到的 `WEBSITE_PRIVATE_IP=<private-ip>` 當成固定來源 IP 去開 firewall。Azure 官方文件也提醒這個值可能改變，但會落在 integration subnet 的位址範圍內。

比較穩定的做法是放行整段 App Service Integration Subnet CIDR：

```text
Source: <integration-subnet-cidr>
Destination: <target-private-ip-or-subnet>
Port: <target-port>
```

例如 App Service 要連到內網 SQL Server、內部 API、Azure SQL Managed Instance Private Endpoint，或經 ExpressRoute / Site-to-Site VPN 連 on-prem 服務時，網路團隊應該檢查的是 integration subnet CIDR 是否被允許進入目標端，以及目標端是否有回程路由回到這個 CIDR。

## 用多個 integration subnet 限縮 firewall 範圍

如果不能鎖定單一 `WEBSITE_PRIVATE_IP`，但又不想讓所有 App Service 都共用同一段 firewall 來源範圍，可以把 App Service 依照存取權限分組，建立多個專用 integration subnet。這樣 firewall 仍然是放行 subnet CIDR，但每個 CIDR 只代表一組特定用途的 App Service。

常見切法如下：

| App Service 群組 | Integration subnet | Firewall 開放方向 |
| --- | --- | --- |
| 對外 API | `<public-api-integration-subnet>` | 只允許連到必要的內部 API 或資料庫 |
| 後台管理服務 | `<admin-integration-subnet>` | 只允許連到後台管理端需要的內部服務 |
| 報表或批次服務 | `<report-integration-subnet>` | 只允許連到 read-only DB、報表 API 或批次端點 |

防火牆規則可以寫成：

```text
Allow <public-api-integration-subnet-cidr> -> <target-private-endpoint-or-service>:<port>
Allow <admin-integration-subnet-cidr> -> <admin-private-service>:<port>
Allow <report-integration-subnet-cidr> -> <reporting-private-service>:<port>
```

這種設計的重點是把 integration subnet 當成 App Service outbound 的 security boundary。`WEBSITE_PRIVATE_IP` 可以用來驗證目前 instance 是否真的從正確 subnet 拿到 IP，但不應該被當成 firewall 規則的唯一來源。

實務上會建議：

- 不同安全等級或不同資料存取權限的 App Service，優先放在不同 App Service Plan。
- 不同 App Service Plan 再分別整合到不同 `Microsoft.Web/serverFarms` delegated subnet。
- 同一個 integration subnet 只放同一類信任邊界的 App Service。
- 若多個 App Service Plan 共用同一個 integration subnet，對 firewall 來說它們就是同一個來源群組，適合用在權限相同的服務，不適合混放 admin、public API 與 batch job。

設計時也要保留容量。Integration subnet 是 App Service VNet Integration 專用 subnet，必須 delegated 到 `Microsoft.Web/serverFarms`，而且要預留 scale out、scale up/down 與平台升級時的暫時 IP 使用量。Production 環境通常不要把 subnet 切到剛剛好，避免日後擴充或 App Service Plan 調整時卡住。

## 不要把它當成 App Service inbound IP

`WEBSITE_PRIVATE_IP` 不是讓別人從內網連進 App Service 的 IP。它代表 App Service instance 透過 VNet Integration 對外連線時使用的來源 private IP。

如果需求是「公司內網、VPN、ExpressRoute 或另一個 VNet 的 client 要用 private IP 連進 App Service」，應該建立 App Service Private Endpoint，然後看 Private Endpoint NIC 拿到的 private IP。

Private Endpoint 建好後，也要確認 private DNS，例如 App Service 常見會用到：

```text
privatelink.azurewebsites.net
```

讓內網解析 `<app-name>.azurewebsites.net` 時能導到 Private Endpoint 的 private IP。

## 常見誤解

- `WEBSITE_PRIVATE_IP` 可能會變，不適合寫死在 firewall 或應用程式設定中。
- App Service 的 public outbound IP 不是 VNet Integration 連 private resource 時的主要判斷依據。
- VNet Integration 不能提供 inbound private access；inbound 要用 Private Endpoint。
- Integration subnet 和 Private Endpoint subnet 不能是同一個 subnet。
- 不同用途的 App Service 如果共用同一個 integration subnet，防火牆無法只靠來源 CIDR 分辨是哪一類 App Service。
- 若 `WEBSITE_PRIVATE_IP` 沒出現，通常要先查 VNet Integration 狀態、App Service Plan 等級、subnet delegation 與 subnet 是否仍有可用 IP。

## 相關筆記

- [Azure App Service VNet Integration 查詢哪個 Subnet 正在被使用](Azure-App-Service-VNet-Integration-查詢-Subnet-使用者.md)
- [Azure App Service 經 VNet Integration 與 S2S VPN 連內網時 `tcpping` timeout 排錯筆記](Azure-App-Service-VNet-tcpping-timeout.md)
- [Azure App Service VNet Integration 連 Azure SQL Managed Instance Private Endpoint 的 DNS 筆記](azure-app-service-sql-mi-private-dns.md)

## 參考資料

- [Integrate your app with an Azure virtual network](https://learn.microsoft.com/azure/app-service/overview-vnet-integration#manage-virtual-network-integration)
- [Troubleshoot virtual network integration with Azure App Service](https://learn.microsoft.com/troubleshoot/azure/app-service/troubleshoot-vnet-integration-apps#summary)
- [Use private endpoints for Azure App Service apps](https://learn.microsoft.com/azure/app-service/overview-private-endpoint)
- [Environment variables and app settings in Azure App Service](https://learn.microsoft.com/azure/app-service/reference-app-settings#networking)
