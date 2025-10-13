# Azure Cache for Redis

直接建立 Redis 以前一直連不到，記錄下成功步驟

1. 建立 Redis
    - 進入 Azure Portal
    - 搜尋 Redis Cache
    - 點選建立
    - 設定網路，連線方式選擇私人端點
      - 新增私人端點
      - 位置：與 App Service 相同
      - 私人 DNS 整合：是
      - 記住選擇的虛擬網路(VNet)名稱
    - 進階設定
      - 存取金鑰驗證：啟用 (尚不確定本地端如何使用 Microsoft Entra 驗證)
    - 建立
2. 取得 Redis 連線字串
   - 到剛才建立的 Redis
   - 設定 > 驗證 > 存取金鑰 > 主要連接字串 (StackExchange.Redis) > 複製
3. Azure App Service
   - 設定
     - 網路：輸出流量設定 > 虛擬網路整合 > 選擇 Redis 虛擬網路(VNet)名稱
     - 環境變數：新增 Redis:Configuration > 貼上剛才複製的連線字串
4. 本地端
   - 於 Azure 建立 VPN 網路 
      [Azure SQL 透過 Azure VPN Gateway 實現內網連接](https://dotblogs.com.tw/jakeuj/2021/08/13/AzureSqlVpnGetway)
   - 本地端連上 Azure VPN
   - 到 虛擬網路(VNet) 找到 Redis 私人端點的內網 IP
   - 本地端連線 Redis：貼上剛才複製的連線字串
   - VPN 如果沒有將 Redis 連線字串解析 Azure VNet 內網私人端點 IP，可以到 hosts 新增內網 IP 與 Redis 名稱的對應
   - hosts = C:\Windows\System32\drivers\etc\hosts

## 虛擬網路整合
App Service 未設定時虛擬網路整合時， 解析 Redis 會取到公開 IP，但 Redis 不開放公開連線，所以會連不到 Redis。
設定後，即使設定的 Redis Configuration 連線字串中的 Server 位置不變，但實際再 App Service 會解析成內網 IP，這樣就可以連線到 Redis 了。
原理是整合虛擬網路後，App Service 網路中的輸出 DNS 繼承 (來自虛擬網路)，此時會套用該 VNet 的 DNS 解析，所以會解析成內網 IP。

## 備註
虛擬網路整合同樣會影響 SQL Server 的連線，所以設定好 Azure SQL 的 私人端點後，也要設定 App Service 的虛擬網路整合，實現內網連接。
可以到 App Service 主控台中使用 nslookup 指令查詢 DNS 解析結果，確認是否有解析到內網 IP。
