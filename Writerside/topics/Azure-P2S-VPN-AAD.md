# Azure P2S VPN AAD
要透過 AAD 來登入 VPN 大概就是微軟有建好一個應用 Azure VPN Client，
這應用對應有個 Id: [41b23e61-6c1e-4545-b367-cd054e0ed4b4](https://learn.microsoft.com/en-us/azure/vpn-gateway/openvpn-azure-ad-tenant#:~:text=Entra%20Enterprise%20App.-,Azure%20Public,-%3A%2041b23e61%2D6c1e)，
然後你需要提供你要用哪個租戶來進行 AAD 認證，
一般來說可以直接查你目前使用的租戶 Id，
然後需要用他產的一個類似 OAuth 2.0 授權連結來進行預授權，
最後就可以下載設定檔然後匯入微軟出的 Azure VPN Client 進行 VPN 登入

## 設定
- 租用戶 (Tenant)
    `https://login.microsoftonline.com/您要用來驗證使用者身份的 Microsoft Entra ID tenant 的 Tenant ID/`
- 對象 (Audience)
    `41b23e61-6c1e-4545-b367-cd054e0ed4b4`
- 簽發者 (Issuer)
    `https://sts.windows.net/您要用來驗證使用者身份的 Microsoft Entra ID tenant 的 Tenant ID/`

**簽發者 值的結尾包括斜線**

## 範例
Tenant ID：右上角 切換目錄 目前目錄 目錄識別碼

![aad-tenant-id.png](aad-tenant-id.png)

![vpn-aad.png](vpn-aad.png)

## 組織授權
總之需要用畫面上的連結來對 Azure VPN Client 授權，你如果沒權限就要找管理員才有辦法成功設定

![grant.png](grant.png)

## Client
[MAC Azure VPN Client](https://apps.apple.com/us/app/azure-vpn-client/id1553936137?mt=12)

## 參照
[在Azure P2S VPN使用Microsoft Entra ID驗證](https://www.uuu.com.tw/Public/content/article/25/20250512.htm)