# Akamai Forward Host Header 對 App Service redirect 與 cookie 的影響

Akamai 的 `Forward Host Header` 如果設成 `Origin Hostname`，後端 App Service 可能會看到 origin hostname，而不是使用者瀏覽器上的公開網域。這種設定比較適合無狀態的靜態資源；如果網站有登入、OIDC redirect URL、session cookie 或依 Host 判斷租戶與路由，優先保留 `Incoming Host Header`，並讓後端正式支援公開網域。

<tldr>
<p><code>Forward Host Header</code> 會決定 Akamai 送到 origin 的 HTTP <code>Host</code> header。</p>
<p><code>Cache Key Hostname</code> 只影響 Akamai 快取怎麼分桶，不等於送到 origin 的 <code>Host</code>。</p>
<p><code>Forward Host Header = Incoming Host Header</code> 的前提，是 origin 平台與 TLS 憑證也已正式支援該公開 hostname。</p>
</tldr>

> 本文中的 property、hostname、App Service 名稱、帳號、合約與環境資訊皆已去識別化。範例只使用 `<public-hostname>`、`<origin-hostname>` 與 `<app-name>.azurewebsites.net` 這類占位符。

## 名詞差異

| Akamai 欄位 | 影響範圍 | 簡單說明 |
| --- | --- | --- |
| `Origin Server Hostname` | Akamai edge 要連線的 origin DNS 名稱 | 例如後端 App Service 的預設 hostname，或另外準備的 origin hostname。 |
| `Forward Host Header` | Akamai 轉送到 origin 的 HTTP `Host` header | 後端 Web App、TLS SNI、憑證驗證、redirect 與 cookie 很常會受這個值影響。 |
| `Cache Key Hostname` | Akamai 快取 key 的 hostname 部分 | 只決定快取物件用哪個 hostname 分桶，不代表 origin 會收到同一個 `Host`。 |

## Forward Host Header 的選項

`Forward Host Header` 是 Akamai 傳給 origin 的 `Host` header。origin Web Server 或 App Service 常會用它決定要回哪個站台內容。

| 選項 | Origin 收到的 `Host` | 適合情境 |
| --- | --- | --- |
| `Incoming Host Header` | 使用者瀏覽器請求的公開網域，例如 `<public-hostname>` | 後端已綁定公開網域，且應用程式需要知道對外 hostname。 |
| `Origin Hostname` | `Origin Server Hostname` 的值，例如 `<origin-hostname>` 或 `<app-name>.azurewebsites.net` | origin 只接受這個 hostname，或內容是無狀態靜態資源。 |
| `Custom Value` | 手動指定的 hostname | origin 或中間層 reverse proxy 需要固定的第三個 hostname。 |

## TLS / SNI 不是附帶條件

如果 Akamai 對 origin 使用 HTTPS，`Forward Host Header` 也會牽動 TLS 驗證與 SNI。

Akamai 啟用 SNI TLS Extension 時，送到 origin 的 SNI 值會和 `Forward Host Header` 相同。Origin TLS Certificate Verification 使用平台設定時，origin 憑證的 CN 或 SAN 也必須和 `Forward Host Header` 匹配。

所以如果設定：

```text
Forward Host Header = Incoming Host Header
```

代表 origin 必須正式接受公開 hostname：

- TLS certificate 的 CN 或 SAN 要包含 `<public-hostname>`。
- SNI 要能用 `<public-hostname>` 選到正確憑證。
- App Service custom domain binding 要能接受 `<public-hostname>` 這個 `Host`。

如果這些條件做不到，不應直接套用 `Incoming Host Header` 模式。這時要改用專用 origin hostname，或保留 `Origin Hostname` 並讓應用程式正確信任 `Forwarded` / `X-Forwarded-Host` 類 header。

<warning>
<p>不要只是為了讓 Akamai 到 origin 的 TLS 驗證通過，就把 <code>Forward Host Header</code> 改成 <code>Origin Hostname</code> 後結案。這可以修掉 origin 連線，但可能把 redirect URI、cookie domain、外部 URL 與 App Service Authentication 問題留到應用層。</p>
</warning>

## Cache Key Hostname 不等於 Forward Host Header

`Cache Key Hostname` 是快取維度，不是 origin request 的 `Host` header。

假設同一個 Akamai property 服務多個 hostname，如果 `Cache Key Hostname` 使用 `Incoming Host Header`，那麼不同公開網域會分開快取：

```text
<public-hostname-a>/assets/app.css
<public-hostname-b>/assets/app.css
```

如果 `Cache Key Hostname` 使用 `Origin Hostname`，多個公開網域可能共用同一份 origin hostname 對應的快取物件。這可以提高 cache hit ratio，但前提是不同公開網域的內容真的完全等價。

<warning>
<p>不要把 <code>Cache Key Hostname = Origin Hostname</code> 用在會依 hostname 回不同內容、不同語系、不同租戶或不同品牌樣式的站台。快取命中率提高的同時，也可能把 A 網域的內容回給 B 網域。</p>
</warning>

## 為什麼 Origin Hostname 可能影響登入與 cookie

當 Akamai 到後端時送出 `Host: <app-name>.azurewebsites.net`，後端應用程式可能會推導出錯誤的外部網址。

常見症狀包含：

- OIDC / OAuth 產生的 `redirect_uri` 變成 origin hostname，導致 identity provider 拒絕 callback。
- 登入成功後被導回 origin hostname，使用者看到後端預設網域，而不是公開網域。
- Cookie 的 `Domain`、`Path`、`Secure` 或 `SameSite` 判斷不符合瀏覽器實際造訪的公開網域，造成 session 遺失。
- 應用程式產生絕對 URL 時暴露 origin hostname。
- 多租戶或多站台程式依 `Host` 判斷 tenant，結果判斷成 origin 站台。

這些問題不是 Akamai 快取本身造成，而是 reverse proxy 和後端應用程式看到的 hostname 不一致。

## 建議判斷方式

### 有登入或動態應用程式

如果 App Service 有以下任一情境，優先讓後端正式綁定公開網域，並使用 `Incoming Host Header`：

- 使用 OIDC、OAuth、SAML 或 App Service Authentication
- 需要 session cookie 或登入狀態
- 後端會產生 redirect URL、callback URL 或絕對 URL
- 依 hostname 決定 tenant、語系、品牌、CORS 或 cookie domain
- 需要避免 origin hostname 暴露給使用者

建議方向：

1. 在 App Service 加上公開 custom domain。
2. 若 Akamai 對 origin 使用 HTTPS 且 `Forward Host Header = Incoming Host Header`，origin 必須接受公開 hostname；TLS 憑證 CN/SAN、SNI、App Service custom domain binding 都要能對應公開 hostname。
3. Akamai `Forward Host Header` 設為 `Incoming Host Header`。
4. `Cache Key Hostname` 也優先使用 `Incoming Host Header`，除非明確確認多個 hostname 內容完全相同。
5. ASP.NET Core 等框架若在 proxy 後方，另外確認 forwarded headers 與 trusted proxy 設定。

### App Service Managed Certificate 的限制

App Service 可以用 TXT record 先驗證 custom domain，不一定要把公開 DNS A/CNAME 直接指到 App Service。這點很適合 reverse proxy 架構，因為公開 DNS 通常應該指向 Akamai 或其他前端 proxy。

但如果需要 Akamai 到 App Service 之間也使用 HTTPS，也就是 end-to-end TLS，憑證來源要另外規劃。Microsoft 的 host name preservation 文件明確提醒：免費 App Service Managed Certificate 需要該網域 DNS record 直接解析到 App Service，因此公開 DNS 指向 reverse proxy 時通常不適用。

可行方向通常是：

- 匯入既有憑證，例如從 Key Vault 匯入。
- 使用 App Service Certificate 或其他可匯入 App Service 的憑證來源。
- 改用專用 origin hostname，讓 origin TLS、SNI 與 Host header 一致，再由應用程式或平台正確處理外部 hostname。

## 不得不用 Origin Hostname 時

有些情境短期內無法讓 App Service 接受公開 hostname，例如：

- App Service 尚未完成公開 custom domain binding。
- Origin TLS 憑證只涵蓋 `<app-name>.azurewebsites.net` 或專用 origin hostname。
- 平台或網路限制要求 Akamai 到 origin 必須送固定 origin hostname。

這時可以暫時使用：

```text
Forward Host Header = Origin Hostname
```

但要把它視為「例外路徑」，並補上外部 hostname 邏輯：

1. 確認 Akamai 或中間層會保留或注入原始公開 hostname，例如 `X-Forwarded-Host` 或標準 `Forwarded` header。
2. 應用程式要信任並使用這些 forwarded headers 產生外部 URL、redirect URL 與 cookie domain。
3. ASP.NET Core 要設定 Forwarded Headers Middleware，並限制 trusted proxy / known networks，避免 header spoofing。
4. 如果使用 App Service Authentication，確認 auth settings 的 `forwardProxy` 行為；在部分 reverse proxy 架構中，需要讓 Easy Auth 尊重 `X-Forwarded-Host`，否則 redirect URI 仍可能使用 App Service 自己的 FQDN。
5. Identity provider 裡註冊的 redirect URI 必須以公開 hostname 為準，不要把 origin hostname 當成正式 callback。

這個模式能讓 origin 連線與 TLS 比較容易成立，但它不是「保留原始 hostname」的等價替代方案。只要 forwarded host 沒有被正確傳遞或應用程式沒有信任它，登入與 cookie 問題還是會發生。

### 純靜態資源或無狀態 origin

如果 origin 只服務 CSS、JavaScript、圖片、下載檔，且不需要登入、cookie、redirect 或 hostname-based routing，`Forward Host Header = Origin Hostname` 通常比較可接受。

這種模式常見於：

- 靜態資源站
- 單純下載檔案
- origin 只接受預設 hostname 或專用 origin hostname
- 內容與公開 hostname 無關

仍要確認：

- origin TLS 憑證與 SNI 設定符合 Akamai 到 origin 的 hostname。
- `Cache Key Hostname` 不會讓不同公開 hostname 互相污染快取。
- 靜態資源 response header 沒有把 origin hostname 寫進 `Location`、`Set-Cookie` 或 HTML 內容。

## 快速設定矩陣

| 情境 | Forward Host Header | Cache Key Hostname | 備註 |
| --- | --- | --- | --- |
| App Service Web App，有登入與 cookie | `Incoming Host Header` | `Incoming Host Header` | 後端應綁定公開 hostname，避免 redirect 與 cookie domain 問題。 |
| 多個公開 hostname 指到同一套動態程式，但內容依 hostname 不同 | `Incoming Host Header` | `Incoming Host Header` | 避免 tenant 或品牌內容混用。 |
| 純靜態資源，內容與 hostname 無關 | `Origin Hostname` 或 `Incoming Host Header` | 視共用快取需求決定 | 使用 `Origin Hostname` 前仍要確認不會產生 redirect 或 cookie。 |
| Origin 只接受專用 origin hostname | `Origin Hostname` 或 `Custom Value` | 通常仍用 `Incoming Host Header` | 可讓 origin 連線成功，但動態應用必須處理 `Forwarded` / `X-Forwarded-Host`、redirect URI、cookie domain 與 App Service Authentication。 |

## 檢查清單

上線前可以用這份清單快速確認：

- 使用者瀏覽器網址列是否維持在 `<public-hostname>`。
- 登入流程送到 identity provider 的 `redirect_uri` 是否是公開 hostname。
- 登入 callback 後是否沒有跳到 `<origin-hostname>`。
- Response header 的 `Location` 是否沒有 origin hostname。
- Response header 的 `Set-Cookie` 是否沒有不合理的 `Domain`。
- HTML 或 API response 是否沒有把 origin hostname 寫死。
- 如果使用 `Origin Hostname` 轉送，應用程式或 Easy Auth 是否真的使用公開 hostname 產生 redirect URI。
- Akamai cache key 是否把需要隔離的公開 hostname 分開。

## 參考資料

- [Akamai TechDocs - Origin Server](https://techdocs.akamai.com/property-mgr/docs/origin-server)
- [Akamai TechDocs - Learn about Akamai's caching](https://techdocs.akamai.com/property-mgr/docs/know-caching)
- [Akamai TechDocs - Custom origin prerequisites](https://techdocs.akamai.com/property-mgr/docs/custom-origin-prerequisites)
- [Microsoft Learn - Preserve the original HTTP host name between a reverse proxy and its backend web application](https://learn.microsoft.com/en-us/azure/architecture/best-practices/host-name-preservation)
- [Microsoft Learn - Authentication and authorization in Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/overview-authentication-authorization)
- [Microsoft Learn - Configure ASP.NET Core to work with proxy servers and load balancers](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/proxy-load-balancer)
