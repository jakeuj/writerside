# Azure SQL Managed Instance 之 Database Copy 連線排錯筆記

> 更新日期：2026-03-12

## 背景
- 來源 Managed Instance：`source-mi`
- 目標 Managed Instance：`target-mi`
- Database Copy 失敗訊息指出「source 與 target 之間沒有網路連線」。
- 先前曾因 subnet CIDR 重疊導致 copy 失敗，因此已將 target VNet 調整到 `10.210.0.0/23`，來源仍在 `10.0.0.0/16`。
- **規劃提醒**：Azure SQL MI 的 subnet 無法直接縮放或修改 CIDR，若一開始規劃錯誤，後續必須建立新的 subnet（甚至 VNet）再把 MI 重新掛上，過程會觸發重啟並牽涉大量資源調整，因此在建置時就要確認 VNet/子網範圍充足且不重疊。

## 問題根因
- 兩個 VNet 調整後尚未建立 peering，所以 SQL MI 之間仍無法透過 Azure backbone 溝通。
- Route table 與 NSG 尚殘留舊的 `10.0.0.0/24` 設定，導致 redirect / GeoDR / MI 管理連線被擋或走錯路由，即便 peering 成功仍會觸發 45669/45670 error。

## 處理步驟
1. **確認 VNet 狀態**
   ```bash
   az network vnet show -g <rg-source> -n vnet-source-mi
   az network vnet show -g <rg-target> -n vnet-target-mi
   ```
   - 確認各自的 `addressSpace` 與子網 CIDR 無重疊。

2. **建立雙向 VNet Peering**
   ```bash
   # source -> target
   az network vnet peering create \
     --resource-group <rg-source> \
     --vnet-name vnet-source-mi \
     --name source-to-target-peering \
     --remote-vnet /subscriptions/<sub>/resourceGroups/<rg-target>/providers/Microsoft.Network/virtualNetworks/vnet-target-mi \
     --allow-vnet-access --allow-forwarded-traffic

   # target -> source
   az network vnet peering create \
     --resource-group <rg-target> \
     --vnet-name vnet-target-mi \
     --name target-to-source-peering \
     --remote-vnet /subscriptions/<sub>/resourceGroups/<rg-source>/providers/Microsoft.Network/virtualNetworks/vnet-source-mi \
     --allow-vnet-access --allow-forwarded-traffic
   ```
   - 需求：雙方皆允許 VNet Access 與 Forwarded Traffic。若需經 hub Gateway，再分別啟用 `allow-gateway-transit` / `use-remote-gateways`。

3. **驗證連線**
   - 在已連線的 VM 執行 `Test-NetConnection <target FQDN> -Port 1433` 或 `tcpping` 9000~9024。
   - 確認 `hosts` 或 DNS 設定已更新，避免指向舊 IP。

4. **同步 NSG 與 Route Table**
   - 將 NSG 規則的 `source/destinationAddressPrefix` 更新為實際子網（例：`10.210.0.0/24`），並新增 MI 管理埠 `9000-9024` 的 inbound/outbound 規則。
   - 移除不再使用的 UDR（例如舊 `10.0.0.0/24` 導至 `VnetLocal` 的路由），避免私網流量被錯誤吸走。
   - 若透過 hub-vnet DNS，確認 private DNS zone 連結到兩個 VNet 並同步 A 記錄。

5. **重新嘗試資料庫複製**
   - 透過 Portal、`az sql midb copy` 或 `Start-AzSqlInstanceDatabaseCopy` 執行。
   - 監看 `az sql midb copy list` 與 `az sql midb list ... --query "[?name=='<db>'].status"`，當狀態變成 `ReadyToComplete`/`DbCopying` 結束時，再執行 `az sql midb copy complete`。
   - 成功後檢查監控計量，確保沒有封包遺失或 RTD 飆高。

## 後續建議
- 為所有 SQL MI 建立一份網路拓撲表，記錄 VNet / Subnet / Peering 狀態與 CIDR。
- 任何 subnet 調整後要列入 CICD 變更流程，避免忘記同步 peering。
- 若還需 GEO DR，可提早在預備區域建立對等路徑與 NSG 規則。
