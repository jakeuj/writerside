# Azure SQL 透過 Azure VPN Gateway 實現內網連接

> **原文發布日期:** 2021-08-13
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/08/13/AzureSqlVpnGetway
> **標籤:** 無

---

Error *40532* 坑，趕緊紀錄一下！

新增或更新憑證的語法

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

---

2022/4/27 坑

開發時會遇到連線失敗，主體名稱不正確之類的訊息

結論：到 host 檔新增 DNS 或於開發時信任伺服器端憑證

TrustServerCertificate=true

```
Server=10.10.0.2;Database=test;user id=test;password=test;TrustServerCertificate=true;
```

說明：

應該是因為原本憑證是發給 database.windows.net

但是我們這邊用的是用 IP 導致憑證驗證失敗

所以在地端開發時直接信任伺服器端憑證

發佈到 Azure App Service 時

如果是直接連 TestDbServerName.database.windows.net

就不需要設定 TrustServerCertificate=true

---

2021/8/31 坑

[VPN 連線後 SQL Server 發生「無法產生 SSPI 內容」錯誤 | The Will Will Web (miniasp.com)](https://blog.miniasp.com/post/2011/01/18/Cannot-Generate-SSPI-Context-and-VPN-connection)

---

結論：到 host 檔新增 DNS 或於 SQL 登入帳號後面要加上 @伺服器名稱

例如原本 SQL Server = TestDbServerName.database.windows.net

登入帳號為 Admin

用 VPN 在 SSMS 的帳號欄位要輸入 Admin@TestDbServerName

否則會得到錯誤：*40532*

參照：[在使用者名中明確提供伺服器名稱，用於Azure SQL DB、MySQL 和后格雷斯QL - 微軟技術社區 (microsoft.com)](https://techcommunity.microsoft.com/t5/azure-database-support-blog/providing-the-server-name-explicitly-in-user-names-for-azure-sql/ba-p/368942)

---

Step 1：建立 Azure VPN Getway

這邊見的時候可能先看一下目前自己的內網 IP 網段是甚麼

在建立 Vnet 的時候網段要錯開

比如公司內網 10.0.0.x

手機分享網路 192.168.0.x

那建立 Vnet 的時候就不要用 10.0.x.x or 192.168.x.x

參照：[使用 P2S VPN 連線至 VNet & 憑證驗證：入口網站 - Azure VPN Gateway | Microsoft Docs](https://docs.microsoft.com/zh-tw/azure/vpn-gateway/vpn-gateway-howto-point-to-site-resource-manager-portal?ranMID=24542&ranEAID=je6NUbpObpQ&ranSiteID=je6NUbpObpQ-ve16QxMGvVJ..ucUbCtprQ&epi=je6NUbpObpQ-ve16QxMGvVJ..ucUbCtprQ&irgwc=1&OCID=AID2200057_aff_7593_1243925&tduid=%28ir__p1u96bibkskfqgpn1ah0e2el0e2xruyu3tdry3jc00%29%287593%29%281243925%29%28je6NUbpObpQ-ve16QxMGvVJ..ucUbCtprQ%29%28%29&irclickid=_p1u96bibkskfqgpn1ah0e2el0e2xruyu3tdry3jc00)
{ignore-vars="true"}

---

Step 2：建立 SQL 私人端點

建完就有個內網 IP 稍微記一下等等連到資料庫的時候要用

參照：[Tutorial: Connect to an Azure SQL server using an Azure Private Endpoint - Portal | Microsoft Docs](https://docs.microsoft.com/en-us/azure/private-link/tutorial-private-endpoint-sql-portal#create-an-azure-sql-server-and-private-endpoint)

---

Step 3：安裝 VPN 並連線

就把 Step 1 的私人憑證匯入到每個要連線的電腦

然後把從 Azure 下載回來的 CA 可能也要匯入到信任的根憑證

再安裝 Azure 下載的 x64 VPN Clinet

就會在電腦右下網路裡面看到該 VPN

按連線理論上就可以成功了

---

Step 4：測試連線

設定完並連結 VPN 後可以在 PowerShell (電源殼？) 輸入以下命令測試連線

Test-NetConnection 10.0.0.4 -Port 1433

P.S. 這邊假定 SQL 私人端點分配的內網 IP 為 10.0.0.4 請依照實際分配位置輸入

注意：這邊一定要指定 1433 Port, ping 應該是關掉不會過的, 回想起來我因此卡了很久

---

Step 5：使用 SSMS 登入

輸入 SQL 私人端點分配的內網 IP 當作 SQL Server Host

然後將帳號後面加上 @SQL伺服器名稱 (參照開頭的結論部分)

密碼就一樣

理論上就可以不用開 WAN IP 白名單

也可以連到 Azure SQL

---

Note：

* Win 10 如果要用 IKEv2 連線可能要改 登錄檔 (預設 SSTP 不用)
* WIn 7 之類的要連 VPN 要啟用 TLS 1.2 (也要改登錄檔)
* 有人登入遇到錯誤 說甚麼 主體 xxx SSL xxx 還不確定甚麼問題
* VPN 協議有很多種，目前手機分享網路貌似只有 SSTP 可以通
* 承上，MIS封鎖各種 VPN，但以我目前 SSTP 是可以用的
* 如果連線失敗，可以確認一下 MIS 是否把 1433 封死了

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Azure SQL](/jakeuj/Tags?qq=Azure%20SQL)
{ignore-vars="true"}

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
