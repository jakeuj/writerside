# Azure App Service 經 VNet Integration 與 S2S VPN 連內網時 `tcpping` timeout 排錯筆記

這篇筆記整理 Azure App Service 已啟用 VNet Integration，並透過 Site-to-Site VPN 連到內網時，從 Kudu console 測試 `tcpping` 卻一直 timeout 的排查順序。

> 本文中的 subscription ID、resource group、VNet、subnet、IP、主機名稱與 App Service 名稱皆已去識別化，請替換成你自己的 Azure 資源。

## 問題症狀

常見情境是：

- Azure App Service 已完成 VNet Integration
- Azure VNet 已經和內網透過 Site-to-Site VPN 連線
- 想從 App Service 驗證是否真的能連到內網某台主機的 TCP port

在 Windows App Service 的 Kudu console 中，常見測試方式如下：

```cmd
tcpping.exe <private-ip> <target-port>
```

如果回傳類似下面的結果：

```text
Connection attempt failed: Connection timed out.
Complete: 0/4 successful attempts (0%).
```

通常代表 TCP 連線沒有拿到成功回應。

## 先講結論

當 `tcpping` 對內網 IP 與指定 port 回傳 timeout 時，先把它解讀成：

- App Service 已經嘗試建立 TCP 連線
- 如果你測的是直接 IP，這通常不是 DNS 問題
- 問題多半落在路由、VPN prefix、firewall、回程路由，或目標服務本身沒有正常 listen

最常被忽略的點有兩個：

1. 內網 firewall 放行的來源通常應該是 **App Service Integration Subnet CIDR**，不是 App Service 公網 IP。
2. 就算封包成功進到內網，如果 on-prem 沒有回程路由指回 Integration Subnet，一樣會看到 timeout。

## 適用情境

這篇筆記適合用在以下情境：

- App Service 已設定 VNet Integration
- 目標是內網 private IP，而不是公開網址
- 中間有 Site-to-Site VPN 或 ExpressRoute
- 想驗證 SQL Server、內部 API 或其他 TCP 服務是否可達

## 先從 App Service 自己的角度驗證

## 1. 確認真的有拿到 VNet Integration 的 private IP

在 Kudu console 中先看 `WEBSITE_PRIVATE_IP`。

Windows App Service：

```cmd
SET WEBSITE_PRIVATE_IP
```

Linux App Service：

```bash
set | egrep --color 'WEBSITE_PRIVATE_IP'
```

如果這個值不存在，就先不要急著看 VPN 或 firewall，先回 Azure Portal 檢查：

- App Service
- Networking
- VNet Integration

確認：

- 狀態是 connected
- 掛到正確的 VNet
- 掛到正確的 integration subnet

## 2. 用正確的 Kudu 工具驗證

Windows App Service 的 Kudu console，實務上應該優先用：

- `nameresolver.exe` 檢查 DNS
- `tcpping.exe` 檢查 TCP 連線

例如：

```cmd
nameresolver.exe <target-hostname>
tcpping.exe <private-ip> <target-port>
```

如果你測的是直接 IP，代表你是在驗證「TCP 路徑」而不是 DNS。

> 有些範例會寫成 `tcpping <private-ip>:<port>`，但本文示範採用比較清楚的 `tcpping.exe <host> <port>` 形式。

Linux App Service 則改用：

```bash
nslookup <target-hostname>
curl <private-ip>:<target-port>
```

## 3. 解讀 `timeout`、`connection refused` 與 `success`

### `timeout`

通常表示：

- Azure 路由不對
- VPN prefix 沒宣告到位
- firewall 直接 drop
- on-prem 沒有回程路由
- 目標主機不可達

### `connection refused`

通常表示：

- 網路路徑其實有通
- 但目標服務沒有在那個 port listen
- 或主機/防火牆明確拒絕連線

### `success`

通常表示：

- App Service 出站路徑是通的
- 路由與 VPN 大致正確
- 目標服務真的有在監聽該 port

## Azure 端建議排查順序

## 1. 確認 App Service 綁的是正確 subnet

```bash
APP_RESOURCE_GROUP="<app-rg>"
APP_NAME="<app-name>"

az webapp show -g "${APP_RESOURCE_GROUP}" -n "${APP_NAME}" \
  --query "{name:name,resourceGroup:resourceGroup,plan:appServicePlanId,subnet:virtualNetworkSubnetId,outboundVnetRouting:outboundVnetRouting}" \
  -o json
```

必要時再補查：

```bash
az webapp config show -g "${APP_RESOURCE_GROUP}" -n "${APP_NAME}" -o json
```

重點看：

- `virtualNetworkSubnetId`
- `outboundVnetRouting`
- `vnetRouteAllEnabled`

## 2. 確認 integration subnet 設定

```bash
az network vnet subnet show \
  --ids <integration-subnet-resource-id> \
  -o json
```

重點確認：

- subnet CIDR
- 是否 delegated 到 `Microsoft.Web/serverFarms`
- 是否掛了 NSG
- 是否掛了 route table

## 3. 確認 VPN 端是否真的知道目標網段

先看 VPN connection：

```bash
az network vpn-connection show -g <network-rg> -n <vpn-connection-name> -o json
```

再看 Local Network Gateway：

```bash
az network local-gateway show -g <network-rg> -n <local-network-gateway-name> -o json
```

這裡要確認：

- 連線狀態是 connected
- Local Network Gateway 包含目標 on-prem subnet
- 如果你用 BGP，實際學到的路由也有包含目標網段

## On-Prem 端要確認什麼

如果 Azure 端看起來都正常，下一步就要找網路或 infra 團隊確認：

- 是否允許 **Integration Subnet CIDR** 連到 `<private-ip>:<target-port>`
- 目標 on-prem subnet 是否真的經由 VPN 回傳 Azure
- 目標主機的服務是否有在正確 port listen
- 內網是不是還有其他 firewall 或 ACL

## 可直接丟給網路團隊的確認訊息

```text
Azure App Service 已完成 VNet Integration。
我從 App Service 的 Kudu console 測試 TCP 連線，結果 timeout。

請協助確認：
1. App Service Integration Subnet 的 CIDR 是否已被允許連到目標 IP:Port
2. Local Network Gateway 或 BGP 是否包含目標 on-prem subnet
3. On-prem 是否有回程路由返回 App Service Integration Subnet
4. VPN tunnel 是否穩定且實際承載該網段流量
5. 目標主機上的服務是否確實在對應 TCP port listen
```

## 常見誤解

- 不要把 App Service 公網 IP 當成這條混合式連線的來源
- 不要因為 VPN 顯示 connected 就假設路由一定正確
- 不要因為是 direct IP 測試還把問題先怪到 DNS
- 不要只檢查 Azure 端，卻忘記 on-prem 的回程路由

## 相關筆記

- [Azure App Service VNet Integration 查詢哪個 Subnet 正在被使用](Azure-App-Service-VNet-Integration-查詢-Subnet-使用者.md)
- [AzureSql Vnet AppService](AzureSqlVnetAppService.md)
- [Azure VPN 筆記](Azure-VPN.md)

## 參考資料

- [Troubleshoot virtual network integration apps in Azure App Service](https://learn.microsoft.com/zh-tw/troubleshoot/azure/app-service/troubleshoot-vnet-integration-apps)
