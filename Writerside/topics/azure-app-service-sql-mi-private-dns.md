# Azure App Service VNet Integration 連 Azure SQL Managed Instance Private Endpoint 的 DNS 筆記

Azure App Service 透過 VNet Integration 連到 Azure SQL Managed Instance 的 Private Endpoint 時，重點通常不是只建好 Private Endpoint，而是要讓 App Service 查詢 Managed Instance 的 FQDN 時解析到 Private Endpoint 的 private IP。Azure SQL Managed Instance 的 Private Endpoint DNS 需要手動處理，常見做法是在 App Service 所整合的 VNet 可解析範圍內建立 `privatelink.<mi-dns-zone>.database.windows.net`。

<tldr>
<p>SQL Managed Instance Private Endpoint 不要直接套用一般 Azure SQL Database 的 <code>privatelink.database.windows.net</code>。</p>
<p>不同 VNet 情境常見 zone pattern 是 <code>privatelink.&lt;mi-dns-zone&gt;.database.windows.net</code>，並手動建立 A record。</p>
<p>排查時先用 <code>nslookup</code> 或 Kudu 的 <code>nameresolver.exe</code> 確認 FQDN 是否解析到 Private Endpoint IP。</p>
</tldr>

> 本文中的 subscription ID、resource group、VNet、subnet、IP、主機名稱與 DNS zone 值皆已去識別化，請替換成你自己的 Azure 資源。

## 適用情境

這篇筆記適合用在以下情境：

- App Service 已設定 VNet Integration
- App Service 要連 Azure SQL Managed Instance
- SQL Managed Instance 的 Private Endpoint 建在另一個 VNet，例如 hub VNet 或共用網路 VNet
- App Service 使用 Managed Instance FQDN 連線時，連線失敗或仍解析不到 Private Endpoint IP

如果你連的是一般 Azure SQL Database，也就是 `Microsoft.Sql/servers`，DNS zone 通常是：

```text
privatelink.database.windows.net
```

但 Azure SQL Managed Instance 是 `Microsoft.Sql/managedInstances`，它的 FQDN 會帶有 Managed Instance 自己的 DNS zone：

```text
<mi-name>.<mi-dns-zone>.database.windows.net
```

因此不同 VNet 的 Private Endpoint DNS zone 常見會是：

```text
privatelink.<mi-dns-zone>.database.windows.net
```

## 為什麼不能只靠自動整合

SQL Managed Instance 的 Private Endpoint 有幾個容易踩到的限制：

1. 連線字串應該使用 Managed Instance 的 hostname，不建議長期用 Private Endpoint IP。
2. SQL Managed Instance Private Endpoint 的 DNS automatic registration 尚未支援，需要依文件手動設定 DNS。
3. Private Endpoint 對 SQL Managed Instance 只處理標準 TDS 連線，也就是 TCP 1433。

所以 Private Endpoint 建好之後，還要確認 App Service 查詢：

```text
<mi-name>.<mi-dns-zone>.database.windows.net
```

最後能解析到 Private Endpoint 的 private IP。

## 建議設定方式

### 1. 找出 Managed Instance 的 FQDN 與 DNS zone

可以先查 Managed Instance：

```bash
az sql mi show \
  -g <mi-resource-group> \
  -n <mi-name> \
  --query "{fqdn:fullyQualifiedDomainName,dnsZone:dnsZone}" \
  -o json
```

你會需要兩個值：

- `<mi-name>`
- `<mi-dns-zone>`

FQDN 會長得像：

```text
<mi-name>.<mi-dns-zone>.database.windows.net
```

### 2. 建立 Private DNS Zone

在 Private Endpoint 與 App Service integration subnet 所在的解析範圍中，建立 Private DNS Zone：

```bash
az network private-dns zone create \
  -g <dns-resource-group> \
  -n "privatelink.<mi-dns-zone>.database.windows.net"
```

<note>
<p>這裡的 <code>&lt;mi-dns-zone&gt;</code> 不是固定字串，每個 Managed Instance 可能不同。不要把 SQL Managed Instance 的 record 建到 <code>privatelink.database.windows.net</code>，那是一般 Azure SQL Database 常見的 zone。</p>
</note>

### 3. Link 到 App Service 整合的 VNet

Private DNS Zone 要 link 到 App Service VNet Integration 使用的 VNet。

```bash
az network private-dns link vnet create \
  -g <dns-resource-group> \
  -z "privatelink.<mi-dns-zone>.database.windows.net" \
  -n "link-<appservice-vnet-name>" \
  -v <appservice-vnet-resource-id> \
  -e false
```

這類 Private Endpoint DNS zone 通常不要啟用 auto registration，因為它不是拿來讓 VM 自動註冊 hostname 的 zone。

### 4. 建立 A record

Record name 只放 Managed Instance 名稱，不要放完整 FQDN。

```bash
az network private-dns record-set a add-record \
  -g <dns-resource-group> \
  -z "privatelink.<mi-dns-zone>.database.windows.net" \
  -n "<mi-name>" \
  -a "<private-endpoint-ip>"
```

也就是：

| 項目 | 值 |
| --- | --- |
| Private DNS Zone | `privatelink.<mi-dns-zone>.database.windows.net` |
| A record name | `<mi-name>` |
| A record value | `<private-endpoint-ip>` |
| VNet link | App Service VNet Integration 使用的 VNet |

## 連線字串建議

App Service 的 connection string 建議保留 hostname，並明確指定 TCP 與 1433：

```text
Server=tcp:<mi-name>.<mi-dns-zone>.database.windows.net,1433;Database=<database-name>;...
```

不要長期使用這種寫法：

```text
Server=<private-endpoint-ip>;Database=<database-name>;...
```

原因是 SQL Managed Instance 需要 SQL client 帶著正確 hostname 連線；直接用 IP 除了不利於 DNS 與憑證，也容易把問題藏到應用程式層才爆出來。

## 用 nslookup 排查 DNS

先從 App Service 能看到的網路位置測試 DNS。Windows App Service 可以用 Kudu console；如果 `nslookup` 可用，可以先查原始 FQDN：

```batch
nslookup <mi-name>.<mi-dns-zone>.database.windows.net
```

如果要直接確認 private zone 內的 A record：

```batch
nslookup <mi-name>.privatelink.<mi-dns-zone>.database.windows.net
```

期望結果是最後能看到 Private Endpoint 的 private IP：

```text
Name:    <mi-name>.privatelink.<mi-dns-zone>.database.windows.net
Address: <private-endpoint-ip>
```

在 Windows App Service 的 Kudu console 中，也可以使用 `nameresolver.exe`：

```batch
nameresolver.exe <mi-name>.<mi-dns-zone>.database.windows.net
```

如果 DNS 解析正確，再測 TCP 1433：

```batch
tcpping.exe <mi-name>.<mi-dns-zone>.database.windows.net:1433
```

## 常見判斷

### 解析到 public IP 或不是 Private Endpoint IP

通常代表：

- Private DNS Zone 沒建立
- Private DNS Zone 沒 link 到 App Service VNet Integration 所在 VNet
- A record name 寫成完整 FQDN，導致 record 放錯位置
- VNet 使用 custom DNS，但 custom DNS 沒轉送 private zone 查詢

### `nslookup` 正確，但 `tcpping` timeout

這時 DNS 大致正確，問題改往網路路徑看：

- Private Endpoint connection 是否 approved
- App Service integration subnet 是否正確
- VNet peering、UDR、NSG 或 firewall 是否阻擋
- 目標 Managed Instance 是否允許 Private Endpoint 連線

### Kudu 查不到 private zone

如果 VNet 使用自訂 DNS server，App Service 會跟著使用 VNet DNS 設定。這時只 link Azure Private DNS Zone 還不一定夠，還需要：

- custom DNS server 能解析或轉送 `privatelink.<mi-dns-zone>.database.windows.net`
- 或使用 Azure DNS Private Resolver / DNS forwarder 把 private zone 查詢導到 Azure DNS

## 和一般 Azure SQL Database 的差異

| 項目 | Azure SQL Database | Azure SQL Managed Instance |
| --- | --- | --- |
| Resource type | `Microsoft.Sql/servers` | `Microsoft.Sql/managedInstances` |
| 常見 subresource | `sqlServer` | `managedInstance` |
| 常見 Private DNS Zone | `privatelink.database.windows.net` | `privatelink.<mi-dns-zone>.database.windows.net` |
| DNS record | `<server-name>` | `<mi-name>` |
| 連線 port | TCP 1433 | TCP 1433 |

## 補充提醒

- 如果 Private Endpoint 和 SQL Managed Instance 在同一個 VNet，DNS 與憑證行為有額外限制，請依 Microsoft Learn 的 SQL Managed Instance Private Endpoint 文件處理。
- 不要把真實 subscription ID、resource ID、內部 IP、完整 private DNS zone 或環境名稱直接寫進公開筆記。
- 若只是臨時驗證，可以用 hosts file，但正式環境應使用 Private DNS Zone、custom DNS 或 Azure DNS Private Resolver。

## 相關筆記

- [AzureSql Vnet AppService](AzureSqlVnetAppService.md)
- [Azure App Service 經 VNet Integration 與 S2S VPN 連內網時 `tcpping` timeout 排錯筆記](Azure-App-Service-VNet-tcpping-timeout.md)
- [Azure App Service VNet Integration 查詢哪個 Subnet 正在被使用](Azure-App-Service-VNet-Integration-查詢-Subnet-使用者.md)

## 參考資料

- [Azure Private Link for Azure SQL Managed Instance](https://learn.microsoft.com/azure/azure-sql/managed-instance/private-endpoint-overview)
- [Integrate your app with an Azure virtual network](https://learn.microsoft.com/azure/app-service/overview-vnet-integration#private-endpoints)
- [Azure Private Endpoint private DNS zone values](https://learn.microsoft.com/azure/private-link/private-endpoint-dns)
- [Name resolution in Azure App Service](https://learn.microsoft.com/azure/app-service/overview-name-resolution)
