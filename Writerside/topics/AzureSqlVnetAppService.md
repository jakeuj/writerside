# AzureSql Vnet AppService

![azurePrivate.png](azurePrivate.png)

App Service 啟用虛擬網路整合後連不到 Azure SQL Database 的解決方法

![azureZone.png](azureZone.png)

## 問題描述

在 Azure App Service 上啟用虛擬網路整合後，無法連線到 Azure SQL Database，並且在進階管理工具中無法解析資料庫 FQDN。

## 解決方法

到 **私人 DNS 區域** 中找到 privatelink.database.windows.net 的 A 記錄，並將其解析為私人 IP 位址。
例如：test-sqlserver.database.windows.net 解析為 10.1.0.2

## 確認連線

使用 `nameresolver.exe` 和 `tcpping.exe` 確認解析是否正確。

```powershell
C:\home>nameresolver.exe test-sqlserver.database.windows.net
Server: 168.63.129.16

Non-authoritative answer:
Name: test-sqlserver.privatelink.database.windows.net
Addresses:
10.1.0.2
Aliases:
test-sqlserver.privatelink.database.windows.net

C:\home>tcpping.exe test-sqlserver.database.windows.net:1433
Connected to test-sqlserver.database.windows.net:1433, time taken: 1ms
Complete: 1/1 successful attempts (100%). Average success time: 7.75ms
```

{ignore-vars="true"}

## 參照

[troubleshoot-outbound-connectivity-on-windows-apps](https://learn.microsoft.com/zh-tw/troubleshoot/azure/app-service/troubleshoot-vnet-integration-apps#troubleshoot-outbound-connectivity-on-windows-apps)
