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
   - C:\Windows\System32\drivers\etc\hosts 新增內網 IP 與 Redis 名稱的對應
   - 本地端連線 Redis：貼上剛才複製的連線字串

## 備註
Redis 只開私人端點時須使用 xxxxxxx.privatelink.redis.cache.windows.net
如果全開走外網也是連得到就是了 xxxxxxx.redis.cache.windows.net