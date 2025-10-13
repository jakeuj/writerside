# 透過 Proxy 使用 Azure HCM (混合式連線管理員)

> **原文發布日期:** 2022-03-14
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/03/14/Proxy-Azure-Relay-Hybrid-Connections
> **標籤:** 無

---

公司防火牆連外不開或只開有限IP時的疑難雜症

## 結論

C:\Program Files\Microsoft\HybridConnectionManager 0.7\Microsoft.HybridConnectionManager.Listener.exe.config

```
<configuration>
  <!-- 保留原本設定並增加以下區段來設定 Proxy -->
  <system.net>
    <defaultProxy>
      <proxy
        usesystemdefault="True"
        proxyaddress="http://192.168.1.10:3128"
        bypassonlocal="True" />
    </defaultProxy>
  </system.net>
</configuration>
```

### 備註

設好 Proxy 之後，如果原本有混合式連線有設定限制 IP，則記得將 proxy server public IP 加上去白名單

### 參照

[Azure App Service 混合式連線 (HCM) | Jakeuj - 點部落 (dotblogs.com.tw)](https://www.dotblogs.com.tw/jakeuj/2021/08/27/Azure-Relay-Hybrid-Connections)

[<defaultProxy> 項目 (網路設定) - .NET Framework | Microsoft Docs](https://docs.microsoft.com/zh-tw/dotnet/framework/configure-apps/file-schema/network/defaultproxy-element-network-settings#example)

[Hybrid Connection behind Proxy Server (microsoft.com)](https://social.msdn.microsoft.com/Forums/azure/en-US/388b266f-2d56-4b41-a6f8-321c77d2a94b/hybrid-connection-behind-proxy-server?forum=servbus)

[What IP addresses do I need to add to allowlist? (FAQ) | Microsoft Docs](https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-faq#what-ip-addresses-do-i-need-to-add-to-allowlist-)

[Windows 環境 PowerShell 設定 proxy 方法 - I'm Ryan. (mvpdw06.github.io)](https://mvpdw06.github.io/Blog/2016/11/14/Windows-%E7%92%B0%E5%A2%83-PowerShell-%E8%A8%AD%E5%AE%9A-proxy-%E6%96%B9%E6%B3%95/)
{ignore-vars="true"}

### 概要

* HCM 需要 outbound Port 443
* HCM 需要 outbound 包含但不限於動態IP區段
  + 52.187.0.0/17
* HCM 需要 outbound 包含但不限於 Domain
  + https://sea-bus.servicebus.windows.net
  + g\*-prod-sg3-001-sb.servicebus.windows.net
* HCM 可以設定 Proxy 連線

### 情境

公司將對外全鎖，並只開放可以連到指定 IP

按照 Azure 文件大概只會找到需要開放 Endpoint 與 Gateway

但實際上只開放對這些目標進行 443 連線

會在 HCM 上顯示已連接但實際上 App Service 卻連不到 Db 的情況

在與 Azure Support 聯繫之後表示目前尚無切確文件指出 HCM 需要連那些目標

所以只能使用 HCM 觀察他嘗試連到哪一些 IP 來逐步開放

開放後會發現當下測試連線可以正常，但過一陣子或是其他混合連線還是會失敗

初步研判是 HCM 會往 52.187.0.0/17 這個動態 IP 區段產生連線

所以得出以下可能的解決方案

1. 開放此網段供 HCM 連出去
2. 採用透過 Proxy Server 的方式來連外

### Log port

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/4ef224f2-a958-4940-8d7f-b4dc51e99d16/1647241786.png.png)

參照

[Azure WCF Relay DNS Support - Microsoft Tech Community](https://techcommunity.microsoft.com/t5/messaging-on-azure-blog/azure-wcf-relay-dns-support/ba-p/370775)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [App Service](/jakeuj/Tags?qq=App%20Service)
{ignore-vars="true"}
* [Azure](/jakeuj/Tags?qq=Azure)
* [Cloud](/jakeuj/Tags?qq=Cloud)
* [HCM](/jakeuj/Tags?qq=HCM)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
