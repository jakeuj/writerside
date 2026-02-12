# Azure VPN 筆記

## 1. VPN Gateway SKU 降級限制

- Azure 不允許直接從高階 SKU（如 VpnGw2）降級為低階 SKU（如 VpnGw1）。
- 若要降級，必須刪除並重新建立 Gateway。
- 可升級但不可降級（只能重建）。

### 常見指令範例

```bash
# 刪除原 Gateway
az network vnet-gateway delete -g MyResourceGroup -n MyVpnGateway

# 建立新 Gateway (降級後)
az network vnet-gateway create \
  -g MyResourceGroup \
  -n MyVpnGateway \
  --public-ip-address MyPublicIP \
  --vnet MyVnet \
  --gateway-type Vpn \
  --vpn-type RouteBased \
  --sku VpnGw1
```

---

## 2. Generation 相容性

| Generation | 支援的 SKU |
|-------------|-------------|
| Generation 1 | Basic、VpnGw1、VpnGw2、VpnGw3 |
| Generation 2 | VpnGw2、VpnGw3、VpnGw5、ErGw1AZ、ErGw2AZ、ErGw3AZ |

> ⚠️ 錯誤訊息「VpnGw1 不支援 Generation2」表示目前的 Gateway 為 Gen2，而 VpnGw1 僅支援 Gen1。

### 若要使用 VpnGw1

```bash
az network vnet-gateway create \
  -g MyResourceGroup \
  -n MyVpnGateway \
  --public-ip-address MyPublicIP \
  --vnet MyVnet \
  --gateway-type Vpn \
  --vpn-type RouteBased \
  --sku VpnGw1 \
  --gateway-generation Generation1
```

---

## 3. macOS 相容性

| VPN 類型 | macOS 支援 | Azure 支援 | 建議 |
|-----------|-------------|-------------|------|
| IKEv2 | ✅ | ✅ | 💡 建議使用 |
| OpenVPN | ✅ (需軟體) | ✅ | 跨平台方案 |
| SSTP | ❌ | ✅ | 僅 Windows 可用 |

### 建議設定

- 使用 **Point-to-Site (P2S)** 模式。
- Tunnel type: `IKEv2` 或 `IKEv2 and OpenVPN (SSL)`。
- 驗證方式可選：
  - 憑證 (Azure certificate)
  - Azure AD / RADIUS

---

## 4. macOS 連線步驟

### (1) 下載設定

在 Azure Portal → Virtual Network Gateway → Point-to-site configuration → Download VPN client  
取得 `Generic/VpnSettings.xml`。

### (2) 系統內建設定

1. 系統設定 → 網路 → 新增 VPN → 選 IKEv2。
2. 伺服器位址填入 Gateway 公網 IP。
3. 匯入使用者憑證。
4. 儲存並連線。

---

## 5. 常見建議

| 需求 | 建議設定 |
|------|-----------|
| MacBook 連線 | IKEv2 P2S |
| 多平台共用 | IKEv2 + OpenVPN |
| 降低成本 | 使用 Generation1 + VpnGw1 |
| 高可用性 | 保留 Generation2 + VpnGw2 |
