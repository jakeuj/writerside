# Azure Vpn Cret

紀錄一下生憑證的語法

## Root Cert

```shell
$RootFriendlyName = "Azure Vpn Root 2025"
$ClinetFriendlyName = "Azure Vpn Child 2025"

$params = @{
    Type = 'Custom'
    Subject = 'CN=P2SRootdCert'
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

## 參照
- [Azure Vpn Getway](https://dotblogs.com.tw/jakeuj/2021/08/13/AzureSqlVpnGetway)
- [設定 P2S VPN 閘道憑證驗證的伺服器設定](https://learn.microsoft.com/zh-tw/azure/vpn-gateway/point-to-site-certificate-gateway)