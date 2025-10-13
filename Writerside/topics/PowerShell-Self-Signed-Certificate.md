# PowerShell Self Signed Certificate

> **原文發布日期:** 2023-06-09
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/06/09/PowerShell-Self-Signed-Certificate
> **標籤:** 無

---

Azure VPN Gateway 每年要更新憑證

## 產生憑證

```
$RootFriendlyName = "Azure Vpn Root 2025"
$ClinetFriendlyName = "Azure Vpn Child 2025"

$params = @{
    Type = 'Custom'
    Subject = 'CN=RootSubject'
    KeySpec = 'Signature'
    KeyExportPolicy = 'Exportable'
    KeyUsage = 'CertSign'
    KeyUsageProperty = 'Sign'
    KeyLength = 2048
    HashAlgorithm = 'sha256'
    NotAfter = (Get-Date).AddMonths(24)
    CertStoreLocation = 'Cert:\CurrentUser\My'
    FriendlyName = $RootFriendlyName
}
$cert = New-SelfSignedCertificate @params

$params = @{
       Type = 'Custom'
       Subject = 'CN=P2SChildCert'
       DnsName = 'P2SChildCert'
       KeySpec = 'Signature'
       KeyExportPolicy = 'Exportable'
       KeyLength = 2048
       HashAlgorithm = 'sha256'
       NotAfter = (Get-Date).AddMonths(18)
       CertStoreLocation = 'Cert:\CurrentUser\My'
       Signer = $cert
       TextExtension = @('2.5.29.37={text}1.3.6.1.5.5.7.3.2')
       FriendlyName = $ClinetFriendlyName
   }
New-SelfSignedCertificate @params

certmgr.msc
```

## 匯出根憑證公開金鑰 (.cer)

[產生及匯出 P2S 的憑證：PowerShell - Azure VPN Gateway | Microsoft Learn](https://learn.microsoft.com/zh-tw/azure/vpn-gateway/vpn-gateway-certificates-point-to-site#cer)

```
certmgr.msc
```

![螢幕擷取畫面顯示 [憑證] 視窗，已依序選取 [所有工作] 及 [匯出]。](https://learn.microsoft.com/zh-tw/azure/includes/media/vpn-gateway-certificates-export-public-key-include/export.png#lightbox)![螢幕擷取畫面顯示不要匯出私密金鑰。](https://learn.microsoft.com/zh-tw/azure/includes/media/vpn-gateway-certificates-export-public-key-include/not-private-key.png#lightbox)![螢幕擷取畫面顯示匯出 Base-64 編碼。](https://learn.microsoft.com/zh-tw/azure/includes/media/vpn-gateway-certificates-export-public-key-include/base-64.png#lightbox)![螢幕擷取畫面顯示記事本中開啟 CER 檔案，並醒目提示憑證資料。](https://learn.microsoft.com/zh-tw/azure/includes/media/vpn-gateway-certificates-export-public-key-include/notepad-file.png)

## 匯出用戶端憑證

![螢幕擷取畫面顯示 [憑證] 視窗，已選取 [所有工作] 和 [匯出]。](https://learn.microsoft.com/zh-tw/azure/includes/media/vpn-gateway-certificates-export-client-cert-include/export-certificate.png#lightbox)![螢幕擷取畫面顯示已選取 [是，匯出私密金鑰]。](https://learn.microsoft.com/zh-tw/azure/includes/media/vpn-gateway-certificates-export-client-cert-include/yes-export.png#lightbox)![匯出檔案格式頁面的螢幕擷取畫面。](https://learn.microsoft.com/zh-tw/azure/includes/media/vpn-gateway-certificates-export-client-cert-include/personal-information-exchange.png#lightbox)![螢幕擷取畫面顯示輸入並確認密碼。](https://learn.microsoft.com/zh-tw/azure/includes/media/vpn-gateway-certificates-export-client-cert-include/password.png#lightbox)

### 安裝匯出的用戶端憑證

透過 P2S 連線連接的每個用戶端都需要以本機方式安裝用戶端憑證。

若要安裝用戶端憑證，請參閱[安裝點對站連線的用戶端憑證](https://learn.microsoft.com/zh-tw/azure/vpn-gateway/point-to-site-how-to-vpn-client-install-azure-cert)。

[產生及匯出 P2S 的憑證：PowerShell - Azure VPN Gateway | Microsoft Learn](https://learn.microsoft.com/zh-tw/azure/vpn-gateway/vpn-gateway-certificates-point-to-site#install)

### 設定 VNet Gateway P2S 憑證

將上面匯出的根憑證用記事本打開後的內容 (MIIxxxx=)

填到 虛擬網路閘道 > 點對站設定 > 根憑證 > 公開憑證資料

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/983bb28a-2500-432b-88b9-02fff9a68f46/1686736782.png.png)

要撤銷某個用戶端憑證，可以填到已撤銷的憑證中的指紋欄位

如果要撤銷整個根憑證下的全部用戶端，則直接刪除根憑證

## 憑證位置

憑證 > 位置
AzureClient.pfx > 目前的使用者\個人\憑證
AzureRoot.cer > 本機電腦\受信任的根憑證授權單位

[疑難排解 Azure 點對站連線問題 - Azure VPN Gateway | Microsoft Learn](https://learn.microsoft.com/zh-tw/azure/vpn-gateway/vpn-gateway-troubleshoot-vpn-point-to-site-connection-problems#solution)

## 參照

[Azure SQL 透過 Azure VPN Gateway 實現內網連接 | 御用小本本 - 點部落 (dotblogs.com.tw)](https://dotblogs.com.tw/jakeuj/2021/08/13/AzureSqlVpnGetway)

[如何使用 PowerShell 建立開發測試用途的自簽憑證 (Self-Signed Certificate) | The Will Will Web (miniasp.com)](https://blog.miniasp.com/post/2018/04/24/Using-PowerShell-to-build-Self-Signed-Certificate)

[[Day24] 第二十四課 Azure 點對站(P2S)安全連線[安全] - iT 邦幫忙::一起幫忙解決難題，拯救 IT 人的一天 (ithome.com.tw)](https://ithelp.ithome.com.tw/articles/10251275)

[New-SelfSignedCertificate (pki) | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/pki/new-selfsignedcertificate?view=windowsserver2022-ps)

[產生及匯出 P2S 的憑證：PowerShell - Azure VPN Gateway | Microsoft Learn](https://learn.microsoft.com/zh-tw/azure/vpn-gateway/vpn-gateway-certificates-point-to-site#ex2)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Azure SQL](/jakeuj/Tags?qq=Azure%20SQL)
* [Azure VPN](/jakeuj/Tags?qq=Azure%20VPN)
* [Certificate](/jakeuj/Tags?qq=Certificate)
* [PowerShell](/jakeuj/Tags?qq=PowerShell)
* [SSL](/jakeuj/Tags?qq=SSL)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
