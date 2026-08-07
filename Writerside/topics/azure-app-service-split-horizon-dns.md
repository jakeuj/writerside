# Azure App Service Web、API 與 OAuth 2.0 Server 以 Split-horizon DNS 走 Private Endpoint

<web-summary>Azure App Service 的 Web、API 與 OAuth 2.0 Authorization Server 可用 Split-horizon DNS，讓瀏覽器經 WAF、服務間呼叫則以相同 FQDN 走 Private Endpoint。</web-summary>

Web、API 與 OAuth 2.0 / OpenID Connect Authorization Server 分別部署在 Azure App Service，且同時需要公開 WAF 防護與內網服務間呼叫時，建議保留同一組正式 FQDN：Internet 查詢解析到 WAF，VNet 內的 App Service 則透過 Azure Private DNS 解析到 Private Endpoint。這樣應用程式不必維護內外兩套 Authority 或 API URL，也不必讓後端 metadata request 繞回公開 WAF。

<tldr>
<p>公開 DNS：<code>web.example.com</code>、<code>api.example.com</code> 與 <code>auth.example.com</code> 指向 WAF。</p>
<p>Web 與 API 作為呼叫端時需要 VNet Integration；API 與 Authorization Server 作為私有目的端時需要 Private Endpoint。</p>
<p><code>api.example.com</code> 與 <code>auth.example.com</code> 各自建立精確 Private DNS Zone，並 link 到實際發出呼叫的 VNet。</p>
</tldr>

> 本文由實際部署情境整理，但 subscription ID、resource group、VNet、subnet、App Service、FQDN、IP、憑證、client 與公司資訊均已去識別化。範例網域使用 `example.com`，其餘值使用占位符。

## 適用情境

這套設計適合以下需求同時存在的環境：

- Authorization Server、API 與 Web 分別部署在 Azure App Service。
- 對外流量必須先經 Akamai、Azure Front Door 或其他 WAF。
- App Service 公開來源只允許 WAF origin CIDR。
- API 需要讀取 Authorization Server 的 OpenID Connect discovery document 與 JWKS。
- Web 後端需要呼叫 API，也可能需要以 OIDC backchannel 呼叫 Authorization Server。
- 希望外部與內部統一使用 `web.example.com`、`api.example.com`、`auth.example.com` 這類正式 FQDN。

這裡要先分清楚兩個 Azure App Service 網路功能：

| 功能 | 方向 | 用途 |
| --- | --- | --- |
| VNet Integration | App Service outbound | 讓 Web/API 後端查詢 Private DNS，並連到 VNet、Private Endpoint 或內網資源。 |
| Private Endpoint | App Service inbound | 讓 VNet 內的呼叫端透過 private IP 進入 Authorization Server 或 API。 |

Web 後端呼叫 API 時，Web 需要 VNet Integration，API 則需要 Private Endpoint。API 讀取 Authorization Server metadata/JWKS 時，API 需要 VNet Integration，Authorization Server 則需要 Private Endpoint。Web 不會因為要發出這些 outbound request，就需要替自己建立 Private Endpoint。

## 三站台的最小網路矩陣

先用「呼叫端走 outbound、目的端提供 inbound」判斷需要哪些元件：

| 呼叫路徑 | 呼叫端需要 | 目的端需要 | Private DNS Zone 與 VNet Link |
| --- | --- | --- | --- |
| Web backend → API | Web VNet Integration | API Private Endpoint | `api.example.com` link 到 Web 所在 VNet |
| Web backend → Authorization Server | Web VNet Integration | Auth Private Endpoint | `auth.example.com` link 到 Web 所在 VNet |
| API → Authorization Server | API VNet Integration | Auth Private Endpoint | `auth.example.com` link 到 API 所在 VNet |
| Browser → Web/API/Auth | 不使用 App Service VNet Integration | App Service public endpoint 經 WAF | 使用 public DNS，不使用 Private DNS Zone |

因此三個 App Service 的最小配置通常是：

| App Service | VNet Integration | Private Endpoint |
| --- | --- | --- |
| Web | 需要，用來私下呼叫 API/Auth | 選用；只有內部 workload 也需要私下呼叫 Web 時才建立 |
| API | 需要，用來讀取 Auth metadata/JWKS 或呼叫其他私有服務 | 需要，讓 Web backend 私下呼叫 API |
| Authorization Server | 單純作為被呼叫端時不需要；若它還要呼叫其他私有資源才需要 | 需要，讓 Web/API 私下存取 OIDC backchannel endpoint |

如果 Web 與 API 的 VNet Integration 都在同一個 VNet，兩個 Private DNS Zone 各 link 一次該 VNet 即可。如果它們在不同 VNet，`auth.example.com` 必須讓 Web 與 API 兩邊都能解析；可分別建立 VNet Link，或透過企業 custom DNS / Azure DNS Private Resolver 集中轉送。

## 最終拓樸

外部使用者仍然走公開路徑：

```text
Browser
  -> Public DNS: web.example.com / auth.example.com / api.example.com
  -> WAF
  -> Azure App Service public endpoint
```

Azure App Service 之間改走私有路徑：

```text
Web App Service
  -> api.example.com  -> API Private Endpoint
  -> auth.example.com -> Auth Private Endpoint

API App Service
  -> auth.example.com -> Auth Private Endpoint
```

同一個 `auth.example.com` 會依 DNS 查詢位置得到不同結果：

| 查詢位置 | DNS 回覆 | 實際路徑 |
| --- | --- | --- |
| Internet | WAF hostname 或 edge IP | Client → WAF → App Service public endpoint |
| 已 link Private DNS Zone 的 VNet | Auth Private Endpoint IP | API/Web backend → Private Endpoint → Authorization Server |

這就是 Split-horizon DNS，也常稱為 Split-brain DNS。

<note>
<p>瀏覽器中的 JavaScript 不在 Azure VNet 裡。即使 Web App Service 已啟用 VNet Integration，使用者瀏覽器直接呼叫 <code>api.example.com</code> 時，仍會走公開 DNS 與 WAF。只有從 Web App Service 後端發出的 server-to-server request 才會使用 VNet Private DNS。</p>
</note>

## Private DNS Zone 命名策略

假設正式網域是：

```text
auth.example.com
api.example.com
```

最小配置建議建立兩個精確的 Private DNS Zone：

| Private DNS Zone | Record | Value |
| --- | --- | --- |
| `auth.example.com` | `@` A | `<auth-private-endpoint-ip>` |
| `api.example.com` | `@` A | `<api-private-endpoint-ip>` |

兩個 Zone 都 link 到呼叫端 App Service VNet Integration 所在的 VNet，並關閉 Auto registration。

`web.example.com` 不一定需要 Private DNS Zone。若 Web 只提供瀏覽器入口並由 WAF 回源，保留 public DNS 即可；只有其他內部 workload 也要透過 Web Private Endpoint 呼叫它時，才需要建立 `web.example.com` Private DNS Zone 與對應 A record。

不能在 `auth.example.com` Zone 裡新增名為 `api` 的 record 來表示 `api.example.com`。那會得到：

```text
api.auth.example.com
```

不是原本需要的 `api.example.com`。

### 為什麼不直接建立 `example.com`

技術上可以建立一個 `example.com` Private DNS Zone，再新增：

```text
auth  A  <auth-private-endpoint-ip>
api   A  <api-private-endpoint-ip>
```

但 Private DNS Zone 會成為該 VNet 中整個 `example.com` namespace 的權威來源。任何沒有建立的公開名稱都可能得到 `NXDOMAIN`，例如 `www.example.com` 或 `mail.example.com`。

Azure Private DNS 的 `NxDomainRedirect` 公開 DNS fallback 只適用 Private Link zone，不適用一般註冊網域。因此除非企業 DNS 團隊願意完整管理 `example.com` 的 split-brain 記錄，不建議為了少一個 Zone 而接管整個 parent domain。

如果還在規劃網域，也可以改成有共同子網域的結構：

```text
auth.partner.example.com
api.partner.example.com
```

這時可以只建立 `partner.example.com` Private DNS Zone，並新增 `auth`、`api` 兩筆 A record，不會影響其他 `example.com` 名稱。

## Resource Group 與 VNet 怎麼選

Private DNS Zone 是 global resource，放在哪個 Resource Group 不影響解析結果。Resource Group 應依管理與生命週期決定，常見做法是放在共用 Network/DNS Resource Group，與 VNet、Private Endpoint 或既有 Private DNS Zone 一起管理。

真正決定誰能解析 Private DNS 的是 Virtual Network Link：

- Link 到「發出 DNS 查詢的 workload」所使用的 VNet。
- 對 App Service 而言，就是 VNet Integration 指向的 VNet。
- 同一個 Zone 可以 link 多個 consumer VNet；例如 Web 與 API 分屬不同 VNet 時，Auth Zone 要讓兩邊都可解析。
- Private Endpoint 和呼叫端在不同 VNet 時，仍應優先 link 呼叫端 VNet；另外確認 VNet peering、route、NSG 與 TCP 443。
- Link 的範圍是整個 VNet，不能只 link 某個 subnet。

如果 Auth/API Private Endpoint 與 API/Web VNet Integration 都在同一個 VNet，就不需要額外 VNet peering。

## 建立前先盤點

### 查 App Service VNet Integration

```bash
az webapp vnet-integration list \
  --resource-group <app-resource-group> \
  --name <app-service-name> \
  --output table
```

確認 API 與 Web 實際整合到哪個 VNet/subnet，不要只看 Private Endpoint 所在 subnet。

### 查 Private Endpoint FQDN 與 IP

```bash
az network private-endpoint show \
  --resource-group <network-resource-group> \
  --name <private-endpoint-name> \
  --query "customDnsConfigs" \
  --output json
```

輸出應包含已去識別化後類似的內容：

```json
[
  {
    "fqdn": "auth.example.com",
    "ipAddresses": [
      "<auth-private-endpoint-ip>"
    ]
  }
]
```

Private Endpoint NIC 的 `customDnsConfigs` 是建立 DNS 記錄的依據，但看到這個欄位不代表 Private DNS Zone 與 A record 已經自動建立完成。

### 確認 VNet 使用哪一套 DNS

```bash
az network vnet show \
  --resource-group <network-resource-group> \
  --name <vnet-name> \
  --query "dhcpOptions.dnsServers"
```

- 回傳 `[]` 或 `null`：使用 Azure-provided DNS，VNet Link 建好後通常可直接解析 Private DNS Zone。
- 回傳 DNS Server IP：App Service 會跟著使用 VNet 的 custom DNS；自訂 DNS 必須能解析該 private zone，或透過 conditional forwarder / Azure DNS Private Resolver 轉送。

### 檢查是否已有同名 Zone

```bash
az network private-dns zone list \
  --query "[?name=='auth.example.com'].{Name:name,ResourceGroup:resourceGroup}" \
  --output table
```

若已有同名 Zone，應優先重用並確認 VNet Link，不要再建立第二份同名 namespace。

### Azure Portal 建立時的常見誤區

Azure Portal 建立 Private DNS Zone 時會看到「Private DNS 區域編輯器」。這個欄位是用來匯入標準 DNS zone file，不是一般設定表單，因此不要把下列 YAML 貼進去：

```yaml
Name: "@"
Type: A
TTL: 300
IP address: <auth-private-endpoint-ip>
```

沒有既有 zone file 要匯入時，讓編輯器保持空白即可。等 Zone 建立完成後，再到 **Recordsets** 新增記錄：

| 欄位 | 值 |
| --- | --- |
| Name | `@` |
| Type | `A` |
| TTL | `300` |
| TTL unit | Seconds |
| IP address | `<auth-private-endpoint-ip>` |

TTL 數字與單位是分開的欄位。若填入 `300` 卻保留 Portal 預設的 Hours，TTL 會變成 300 小時；應選擇 Seconds，或改用 `5 Minutes`。

如果確實要透過 Private DNS Zone Editor 匯入，內容必須使用 zone file 格式，例如：

```text
@ 300 IN A <auth-private-endpoint-ip>
```

接著在 **Virtual Network Links** 選擇呼叫端 App Service VNet Integration 使用的 VNet，並關閉 Auto registration。Zone 建在哪個 Resource Group 不會決定解析範圍；Virtual Network Link 才會讓整個 VNet 內的 workload 看見該 Private DNS Zone。

## 建立 Auth Private DNS Zone

以下指令使用中性範例與變數，不包含真實 Azure resource ID：

```bash
NETWORK_RG="<network-resource-group>"
VNET_NAME="<app-service-vnet>"
ZONE_NAME="auth.example.com"
AUTH_PE_IP="<auth-private-endpoint-ip>"

VNET_ID=$(az network vnet show \
  --resource-group "$NETWORK_RG" \
  --name "$VNET_NAME" \
  --query id \
  --output tsv)

az network private-dns zone create \
  --resource-group "$NETWORK_RG" \
  --name "$ZONE_NAME"

az network private-dns link vnet create \
  --resource-group "$NETWORK_RG" \
  --zone-name "$ZONE_NAME" \
  --name "link-${VNET_NAME}-auth" \
  --virtual-network "$VNET_ID" \
  --registration-enabled false

az network private-dns record-set a create \
  --resource-group "$NETWORK_RG" \
  --zone-name "$ZONE_NAME" \
  --name @ \
  --ttl 300

az network private-dns record-set a add-record \
  --resource-group "$NETWORK_RG" \
  --zone-name "$ZONE_NAME" \
  --record-set-name @ \
  --ipv4-address "$AUTH_PE_IP"
```

API 採用同樣流程，但改成：

```text
ZONE_NAME=api.example.com
API_PE_IP=<api-private-endpoint-ip>
```

Custom domain 的 Private DNS A record 是手動管理的。如果 Private Endpoint 被刪除後重建，private IP 可能改變，必須同步更新 A record。

## App Service 與 WAF 設定

### App Service custom domain

AuthServer 與 API 都要先綁定正式 custom domain，並準備涵蓋該 hostname 的 TLS 憑證：

```text
auth.example.com
api.example.com
```

Private DNS 只改變名稱解析，不會自動建立 App Service custom domain binding，也不會替 App Service 準備 TLS 憑證。即使 DNS 已解析到 Private Endpoint，App Service 仍會依 TLS SNI 與 HTTP `Host` 判斷要服務哪個 hostname。

### WAF origin

對登入、redirect、cookie 或會產生絕對 URL 的動態站台，建議：

| 欄位 | 建議值 |
| --- | --- |
| Origin Server Hostname | App Service 預設 hostname 或專用 origin hostname |
| Forward Host Header | `Incoming Host Header` |
| Cache Key Hostname | `Incoming Host Header` |
| Origin protocol | HTTPS |

`Forward Host Header = Origin Hostname` 會讓應用程式看到 Azure origin hostname，常見結果是 OAuth/OIDC `redirect_uri`、cookie domain 或絕對 URL 出現 `*.azurewebsites.net`。

### App Service Access Restrictions

公開端點保留 Enabled，並限制來源：

```yaml
Access Restrictions:
  Allow: <waf-origin-cidrs>
  Default unmatched action: Deny
```

不要把 WAF staging edge IP 當成 origin egress CIDR。應使用 WAF 官方提供的 Origin IP ACL、Site Shield 或對應 origin CIDR 清單。

Private Endpoint 流量不會套用 App Service 公開端點的 Access Restrictions，因此 API/Web 仍可從 VNet 走私有入口。SCM/Kudu 有獨立的 access restriction 設定，部署前也要另外確認。

## OAuth/OIDC 前台與 backchannel 如何分流

Split-horizon DNS 不會改變公開 Authority，而是依「誰發出 DNS 查詢」決定網路路徑：

| 流量 | 查詢位置 | 路徑 |
| --- | --- | --- |
| Browser 開啟登入頁或 `/connect/authorize` | 使用者網路 | Public DNS → WAF → Authorization Server public endpoint |
| MVC/BFF Web 讀取 discovery、交換 authorization code | Web App Service | Private DNS → Auth Private Endpoint |
| API 讀取 discovery/JWKS 驗證 token | API App Service | Private DNS → Auth Private Endpoint |
| SPA 在瀏覽器呼叫 token/API endpoint | 使用者網路 | Public DNS → WAF → public endpoint |

這些流量仍使用同一個 `https://auth.example.com` Authority，因此 token 的 `iss`、TLS SNI、OIDC discovery URL 與 callback 設定可以保持一致。不要為了讓 API 走 Private Endpoint，就把 issuer 改成 private IP、`privatelink.azurewebsites.net` 或另一個內部 hostname。

<note>
<p>Private DNS 只影響 server-side request。瀏覽器被 redirect 到 <code>https://auth.example.com</code> 時，仍使用使用者所在網路的 public DNS，因此依舊會經過 WAF。</p>
</note>

## ABP 與 OpenIddict 設定

完成 Private DNS 分流後，內外都可以使用相同正式 Authority。

AuthServer：

```text
App__SelfUrl=https://auth.example.com
AuthServer__Authority=https://auth.example.com
AuthServer__RequireHttpsMetadata=true
```

API：

```text
AuthServer__Authority=https://auth.example.com
AuthServer__MetaAddress=https://auth.example.com
AuthServer__RequireHttpsMetadata=true
```

Web 後端：

```text
AuthServer__Authority=https://auth.example.com
RemoteServices__Default__BaseUrl=https://api.example.com
```

API 或 Web 後端查詢 `auth.example.com`、`api.example.com` 時，Private DNS 會讓 request 直接進 Private Endpoint；瀏覽器仍透過公開 DNS 與 WAF 使用相同 URL。

另外檢查：

- DbMigrator / seed data 內的 OpenIddict client RootUrl。
- redirect URI 與 post logout redirect URI。
- Swagger OAuth callback URL。
- Microsoft Entra ID 或其他外部 identity provider 的 callback URL。
- CORS origins 與 redirect allowed URLs。

切換 Authority 後，舊 token 的 `iss` 仍是舊 hostname，通常需要重新登入取得新 token。

## 短期過渡與混合 discovery document

短期可以讓 WAF 使用 `Incoming Host Header`，但暫時保留 AuthServer issuer 與 API Authority 為舊 Azure hostname。這能降低一次切換的範圍，但 discovery document 可能出現混合狀態：

```text
issuer: https://<old-app-name>.azurewebsites.net
authorization_endpoint: https://auth.example.com/connect/authorize
token_endpoint: https://auth.example.com/connect/token
```

這種狀態只適合受控過渡期：

- API 必須繼續信任舊 issuer。
- 嚴格的 OIDC client 可能拒絕 issuer 與 discovery URL 不一致。
- 對外文件與實際 endpoint 不一致，會增加維運複雜度。

最終仍應讓 discovery document 的 `issuer` 與所有 endpoint 都統一成 `https://auth.example.com`。

## WAF 造成 metadata 403

若 WAF 規則要求 User-Agent 必須像瀏覽器，`JwtBearer`、Swagger 或 OIDC client 讀取以下 endpoint 時可能得到 403：

```text
/.well-known/openid-configuration
/.well-known/jwks
/connect/token
```

Private DNS 可以讓 Azure 內部 server-to-server request 避開 WAF，但公開 OIDC client 仍需要符合標準的存取方式。建議針對必要 method/path 設計 WAF 例外，不要只靠偽裝 Browser User-Agent：

- `GET` / `HEAD` `/.well-known/openid-configuration`
- `GET` / `HEAD` `/.well-known/jwks`
- 合法 client 的 `POST /connect/token`

登入、token 與 metadata path 也不應被 CDN 快取。

## 驗證方式

### 從 Web App Service 同時驗證 API 與 Auth

Windows App Service 的 Kudu Console：

```batch
nslookup api.example.com
nslookup auth.example.com
curl.exe -v https://api.example.com/health
curl.exe -v https://auth.example.com/.well-known/openid-configuration
```

使用 Azure-provided DNS 時，`nslookup` 可能顯示以下結果：

```text
Server:  UnKnown
Address:  168.63.129.16

Name:    auth.example.com
Address: <auth-private-endpoint-ip>

Name:    api.example.com
Address: <api-private-endpoint-ip>
```

`168.63.129.16` 是 Azure 平台提供 DNS 等服務的虛擬 IP；`Server: UnKnown` 不代表查詢失敗。兩個 FQDN 分別解析到自己的 Private Endpoint IP，代表 Web 所在 VNet 已能看見 API 與 Auth 的 Private DNS Zone。

Linux App Service：

```bash
nslookup api.example.com
nslookup auth.example.com
curl -v https://api.example.com/health
curl -v https://auth.example.com/.well-known/openid-configuration
```

預期結果：

- `api.example.com` 解析到 `<api-private-endpoint-ip>`。
- `auth.example.com` 解析到 `<auth-private-endpoint-ip>`。
- API health endpoint 回傳預期的成功狀態。
- TLS certificate 對應 `auth.example.com`。
- discovery document 回傳 HTTP 200。
- response 沒有 WAF/CDN 特有 header。
- `issuer`、`authorization_endpoint`、`token_endpoint` 與 `jwks_uri` 都是 `auth.example.com`。

`nslookup` 成功只代表 DNS 分流正確，還不能單獨證明 TLS、HTTP `Host`、App Service custom domain binding 或應用程式本身正常，因此仍要執行 HTTPS request。

### 從 API App Service 驗證 Authorization Server

API 不需要解析自己的 FQDN 才能驗證 token，但必須能私下連到 Authorization Server：

```batch
nslookup auth.example.com
curl.exe -v https://auth.example.com/.well-known/openid-configuration
```

若 Web 和 API 位於不同 VNet，Web 的雙查詢都成功，不代表 API 所在 VNet 也能看到 Auth Zone；必須從 API 自己的 Kudu/SSH 再測一次。

### 從 Internet 驗證

外部 DNS 查詢應該回到 WAF，而不是 Private Endpoint IP：

```bash
nslookup auth.example.com
nslookup api.example.com
```

再確認：

- 公開 FQDN 經 WAF 可以正常登入與呼叫 API。
- 直接存取 App Service 預設公開 hostname 得到 403。
- OAuth/OIDC `redirect_uri` 沒有出現 Azure origin hostname。
- 新 token 的 `iss` 是 `https://auth.example.com`。
- API 使用新 token 能回傳成功，不再出現 issuer mismatch 401。

## 常見錯誤判斷

| 症狀 | 優先檢查 |
| --- | --- |
| VNet 內仍解析到 WAF/public IP | Private DNS Zone 是否 link 到呼叫端 VNet；VNet 是否使用 custom DNS。 |
| 解析到 private IP，但 HTTPS certificate mismatch | App Service custom domain 與 TLS binding 是否包含正式 FQDN。 |
| discovery document 403 | 是否仍走 WAF；WAF User-Agent、path、method 或 cache rule 是否阻擋 metadata。 |
| discovery issuer 是舊 hostname，endpoint 是新 hostname | OpenIddict issuer 仍被明確設成舊 Authority，但 request Host 已是新 FQDN。 |
| Token 可以取得，但 API 回 401 | Token `iss`、API Authority、metadata/JWKS 可達性與 signing key 是否一致。 |
| 改完 DNS 後暫時仍得到舊結果 | App Service、DNS resolver 或 client negative cache 尚未過期；等待 TTL 或重啟 App Service 再測。 |

Redis 通常不是 issuer 或 metadata/JWKS 驗證失敗的主因。ABP 常用 Redis 保存 distributed cache、Data Protection key 或 distributed lock；不要在沒有證據時清空 Redis。401 應先檢查 token `iss`、Authority、discovery、JWKS 與 signing key。

## 成本概念

以下為公開零售價的概略值，實際費用依 Azure 合約、區域與匯率為準：

| 項目 | 概略成本 |
| --- | --- |
| Private DNS Zone | 前 25 個約 US$0.50 / Zone / month |
| Private DNS query | 約 US$0.40 / 1 million queries |
| App Service VNet Integration | App Service Plan 以外無額外功能費用 |
| Private Endpoint | 約 US$0.01 / hour / endpoint，加上 data processed 費用 |

兩個精確 Private DNS Zone 通常約 US$1 / month。若 Auth 與 API Private Endpoint 已存在，新增 DNS Zone 不會再建立新的 Private Endpoint。

使用 Azure-provided DNS 時，不需要為同一個 VNet 的基本 Private DNS 解析另外建立 Azure DNS Private Resolver。Private Resolver 的成本遠高於 Zone，本來就使用 custom DNS、需要跨 on-premises 或集中式 conditional forwarding 時才評估。

## 上線檢查清單

- Public DNS 的 Web/Auth/API FQDN 指向 WAF。
- WAF `Forward Host Header` 使用 `Incoming Host Header`。
- Web/Auth/API App Service 已綁定對應 custom domain 與可用 TLS certificate。
- Web 有 VNet Integration，可私下呼叫 API/Auth。
- API 有 VNet Integration，可私下讀取 Auth discovery/JWKS。
- API/Auth 都有狀態為 Approved 的 Private Endpoint；Web Private Endpoint 則依是否有內部 inbound caller 決定。
- 每個精確 FQDN 的 Private DNS Zone 都有 `@` A record。
- Private DNS Zone 已 link 到呼叫端 VNet，Auto registration 關閉。
- VNet 內解析到 Private Endpoint IP，外部解析到 WAF。
- App Service 公開 Access Restrictions 只允許 WAF origin CIDR，default deny。
- OpenIddict discovery 的 issuer 與所有 endpoint 都是正式 Auth FQDN。
- API/Web 的 Authority、MetaAddress 與 RemoteServices URL 使用正式 FQDN。
- OpenIddict clients、Swagger 與外部 identity provider callback 已更新。
- 登入、logout、refresh token、Swagger authorize 與 API bearer token 都已驗證。

## 相關筆記

- [Akamai Forward Host Header 對 App Service redirect 與 cookie 的影響](akamai-origin-host-header-app-service.md)
- [ABP 分離 Auth/API 專案部署到 Azure 與 Akamai 檢查表](abp-azure-akamai-deployment-checklist.md)
- [Azure App Service VNet Integration 後如何查內網 IP](azure-app-service-vnet-private-ip.md)

## 參考資料

- [Use Private Endpoints for Apps](https://learn.microsoft.com/azure/app-service/overview-private-endpoint)
- [Integrate your app with an Azure virtual network](https://learn.microsoft.com/azure/app-service/overview-vnet-integration)
- [Web App with VNet Integration and Private Endpoint sample](https://learn.microsoft.com/samples/azure/azure-quickstart-templates/webapp-privateendpoint-vnet-injection/)
- [Name resolution in Azure App Service](https://learn.microsoft.com/azure/app-service/overview-name-resolution)
- [Azure Private DNS zone overview](https://learn.microsoft.com/azure/dns/private-dns-privatednszone)
- [Import and export a private DNS zone file using the Azure portal](https://learn.microsoft.com/azure/dns/private-dns-import-export-portal)
- [Azure IP address 168.63.129.16 overview](https://learn.microsoft.com/azure/virtual-network/what-is-ip-address-168-63-129-16)
- [Troubleshoot NXDOMAIN from an Azure Private DNS zone](https://learn.microsoft.com/troubleshoot/azure/dns/troubleshoot-private-dns-zone-override-nxdomain)
- [Azure App Service access restrictions](https://learn.microsoft.com/azure/app-service/overview-access-restrictions)
- [Azure DNS pricing](https://azure.microsoft.com/pricing/details/dns/)
- [Azure Private Link pricing](https://azure.microsoft.com/pricing/details/private-link/)
- [Akamai TechDocs - Origin Server](https://techdocs.akamai.com/property-mgr/docs/origin-server)
- [ABP OpenIddict deployment](https://abp.io/docs/latest/solution-templates/layered-web-application/deployment/openiddict-deployment)
