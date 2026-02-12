# Azure VPN 憑證錯誤 798

> **原文發布日期:** 2022-09-05
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/09/05/AzureVpnError798
> **標籤:** 無

---

Azure VPN 憑證過期處理筆記

徵狀

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/54839d6e-18f5-499a-b59f-3be692a5fa2d/1662345571.jpg.jpg)

798

問題

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/54839d6e-18f5-499a-b59f-3be692a5fa2d/1662345915.png.png)

MMC

處置

其實就是要重新跑一次產憑證的流程

參照

[產生及匯出 P2S 的憑證：PowerShell - Azure VPN Gateway | Microsoft Docs](https://docs.microsoft.com/zh-tw/azure/vpn-gateway/vpn-gateway-certificates-point-to-site#rootcert)

```
$cert = New-SelfSignedCertificate -Type Custom -KeySpec Signature `
-Subject "CN=P2SRootCert" -KeyExportPolicy Exportable `
-HashAlgorithm sha256 -KeyLength 2048 `
-CertStoreLocation "Cert:\CurrentUser\My" -KeyUsageProperty Sign -KeyUsage CertSign

New-SelfSignedCertificate -Type Custom -DnsName P2SChildCert -KeySpec Signature `
-Subject "CN=P2SChildCert" -KeyExportPolicy Exportable `
-HashAlgorithm sha256 -KeyLength 2048 `
-CertStoreLocation "Cert:\CurrentUser\My" `
-Signer $cert -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.2")

```

匯出根憑證 (之後到 Azure VPN 上新增)

![螢幕擷取畫面顯示 [憑證] 視窗，已依序選取 [所有工作] 及 [匯出]。](https://docs.microsoft.com/zh-tw/azure/includes/media/vpn-gateway-certificates-export-public-key-include/export.png)![螢幕擷取畫面顯示不要匯出私密金鑰。](https://docs.microsoft.com/zh-tw/azure/includes/media/vpn-gateway-certificates-export-public-key-include/not-private-key.png)![螢幕擷取畫面顯示匯出 Base-64 編碼。](https://docs.microsoft.com/zh-tw/azure/includes/media/vpn-gateway-certificates-export-public-key-include/base-64.png)![螢幕擷取畫面顯示記事本中開啟 CER 檔案，並醒目提示憑證資料。](https://docs.microsoft.com/zh-tw/azure/includes/media/vpn-gateway-certificates-export-public-key-include/notepad-file.png)

匯出用戶端憑證 (給其他要用 VPN 的人安裝到他們電腦上用)

![螢幕擷取畫面顯示 [憑證] 視窗，已選取 [所有工作] 和 [匯出]。](https://docs.microsoft.com/zh-tw/azure/includes/media/vpn-gateway-certificates-export-client-cert-include/export-certificate.png)![螢幕擷取畫面顯示已選取 [是，匯出私密金鑰]。](https://docs.microsoft.com/zh-tw/azure/includes/media/vpn-gateway-certificates-export-client-cert-include/yes-export.png)![匯出檔案格式頁面的螢幕擷取畫面。](https://docs.microsoft.com/zh-tw/azure/includes/media/vpn-gateway-certificates-export-client-cert-include/personal-information-exchange.png)![螢幕擷取畫面顯示輸入並確認密碼。](https://docs.microsoft.com/zh-tw/azure/includes/media/vpn-gateway-certificates-export-client-cert-include/password.png)

TODO: 後面這幾步如果可以用 PowerShell 指定操作，日後可能比較方便

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- Azure VPN
{ignore-vars="true"}

- 回首頁

---

*本文章從點部落遷移至 Writerside*
