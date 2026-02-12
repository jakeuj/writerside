# macOS WiFi DNS 設定問題與解決方案

## 問題描述

在 macOS 上使用多個 WiFi 網路時，遇到 DNS 設定衝突的問題：

- **Office-Network**: 內網環境，需要使用內網 DNS (192.168.1.1) 來解析內部網域
- **Home-Network**: 一般網路環境，希望使用公共 DNS (8.8.8.8, 1.1.1.1) 獲得更好的解析速度

### 遇到的問題

當在 Home-Network 網路上手動設定 DNS 為 8.8.8.8 後，切換到 Office-Network 網路時，DNS 設定被共用，導致：

- 無法解析內網網域
- 內網服務無法存取
- 需要手動切換 DNS 設定，非常麻煩

### 根本原因

macOS 的 DNS 設定是針對**網路服務**（如 Wi-Fi）而非特定的 SSID，因此所有透過 Wi-Fi 連接的網路都會共用相同的 DNS 設定。

## 解決方案

### 方案一：設定多個 DNS 伺服器（推薦） {#multiple-dns-servers}

使用 DNS 的容錯機制，同時設定內網和公網 DNS：

```bash
sudo networksetup -setdnsservers Wi-Fi 192.168.1.1 8.8.8.8 1.1.1.1
```

**優點：**

- 一次設定，適用所有網路
- 內網 DNS (192.168.1.1) 優先處理內網網域
- 公網 DNS (8.8.8.8, 1.1.1.1) 作為備援，處理外網網域
- 無需手動切換

#### DNS 查詢順序與運作機制 {#dns-query-order}

macOS 採用**循序查詢**機制，DNS 伺服器的順序至關重要：

**正確順序（推薦）：**

```bash
192.168.1.1 → 8.8.8.8 → 1.1.1.1
```

1. **優先使用 192.168.1.1** 查詢
2. 如果無回應或查詢失敗，使用 **8.8.8.8**
3. 最後使用 **1.1.1.1**

**運作情境分析：**

| 網路環境 | 查詢流程 | 解析時間 |
|---------|---------|---------|
| **Office-Network**<br/>（內網） | `internal.company.com`<br/>→ 192.168.1.1 查詢成功 ✓ | **< 50ms** |
| **Home-Network**<br/>（外網） | `google.com`<br/>→ 192.168.1.1 快速失敗<br/>→ 8.8.8.8 查詢成功 ✓ | **< 150ms** |

#### ⚠️ 錯誤順序的影響 {#wrong-dns-order}

**錯誤順序：**

```bash
# ❌ 不推薦
sudo networksetup -setdnsservers Wi-Fi 8.8.8.8 1.1.1.1 192.168.1.1
```

**問題：**

| 網路環境 | 查詢流程 | 解析時間 | 影響 |
|---------|---------|---------|------|
| **Office-Network**<br/>（內網） | `internal.company.com`<br/>→ 8.8.8.8 查詢失敗（不認識內網域名）<br/>→ 1.1.1.1 查詢失敗（不認識內網域名）<br/>→ 192.168.1.1 查詢成功 ✓ | **2000-5000ms** | 🐌 內網服務變慢<br/>⏱️ 需等待兩次超時 |
| **Home-Network**<br/>（外網） | `google.com`<br/>→ 8.8.8.8 查詢成功 ✓ | **< 50ms** | ✅ 外網正常 |

#### 🎯 為什麼必須將內網 DNS 放第一位？ {#why-internal-dns-first}

1. **循序查詢特性**：macOS 不會平行查詢多個 DNS，而是依序嘗試
2. **失敗時間差異**：
   - 內網 DNS 在外網環境：快速失敗（< 100ms）
   - 公網 DNS 在內網環境：緩慢超時（2-5 秒）
3. **最佳化結果**：內網 DNS 優先可確保兩種環境都有最佳效能

#### 效能比較總結 {#performance-summary}

| DNS 順序配置 | 內網域名 | 外網域名 | 推薦度 |
|------------|---------|---------|-------|
| `192.168.1.1` `8.8.8.8` `1.1.1.1` | ⚡ 快速 | ✓ 正常 | ✅ **推薦** |
| `8.8.8.8` `1.1.1.1` `192.168.1.1` | 🐌 很慢 | ⚡ 快速 | ❌ 不推薦 |
| 只設定 `192.168.1.1` | ⚡ 快速 | ✓ 正常 | ⚠️ 缺乏備援 |
| 只設定 `8.8.8.8` | ❌ 無法解析 | ⚡ 快速 | ❌ 內網不可用 |

### 方案二：手動切換 DNS {#manual-dns-switch}

#### 設定為公網 DNS {#set-public-dns}

```bash
sudo networksetup -setdnsservers Wi-Fi 8.8.8.8 1.1.1.1
```

#### 設定為自動取得 {#set-auto-dns}

```bash
sudo networksetup -setdnsservers Wi-Fi Empty
```

#### 設定為內網 DNS {#set-internal-dns}

```bash
sudo networksetup -setdnsservers Wi-Fi 192.168.1.1
```

### 方案三：使用網路位置

在「系統偏好設定」>「網路」中建立不同的網路位置：

1. 建立「辦公室」位置：使用內網 DNS
2. 建立「家用」位置：使用公網 DNS
3. 透過選單列快速切換

## 常用指令 {#common-commands}

### 查看當前 DNS 設定 {#view-current-dns}

```bash
networksetup -getdnsservers Wi-Fi
```

### 查看當前連接的 WiFi {#view-current-wifi}

```bash
networksetup -getairportnetwork en0
```

### 查看詳細 DNS 資訊 {#view-detailed-dns}

```bash
scutil --dns
```

### 清除 DNS 快取 {#flush-dns-cache}

```bash
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

### 列出所有網路服務 {#list-network-services}

```bash
networksetup -listallnetworkservices
```

## 測試 DNS 解析 {#test-dns-resolution}

### 測試特定 DNS 伺服器 {#test-specific-dns}

```bash
nslookup example.com 8.8.8.8
```

### 測試當前 DNS 設定 {#test-current-dns}

```bash
nslookup example.com
```

### 使用 dig 指令 {#use-dig-command}

```bash
dig example.com
```

## 注意事項 {#important-notes}

1. **DNS 設定範圍**：macOS 的 `networksetup` 指令設定的是整個 Wi-Fi 服務，而非特定 SSID
2. **需要管理員權限**：修改 DNS 設定需要使用 `sudo` 並輸入管理員密碼
3. **DNS 快取**：修改 DNS 後建議清除快取，確保設定立即生效
4. **VPN 影響**：連接 VPN 時，VPN 可能會覆蓋 DNS 設定
5. **⚠️ DNS 順序很重要**：macOS 採用循序查詢，務必將內網 DNS 放在第一位，避免內網服務存取延遲

## 參考資源

- [Apple 官方文件：networksetup](https://support.apple.com/guide/mac-help/welcome/mac)
- Google Public DNS: 8.8.8.8, 8.8.4.4
- Cloudflare DNS: 1.1.1.1, 1.0.0.1

## 總結 {#conclusion}

對於需要同時存取內網和外網的情況，**推薦使用方案一**，設定多個 DNS 伺服器：

```bash
sudo networksetup -setdnsservers Wi-Fi 192.168.1.1 8.8.8.8 1.1.1.1
```

**重點提醒：**

- ✅ 內網 DNS 必須放第一位（192.168.1.1）
- ✅ 公網 DNS 作為備援（8.8.8.8, 1.1.1.1）
- ✅ 解析內網域名快速（< 50ms）
- ✅ 解析外網域名正常（< 150ms）
- ✅ 無需手動切換
- ✅ 適用所有 WiFi 網路

**❌ 避免錯誤順序：**

```bash
# 不要這樣設定，會導致內網服務延遲 2-5 秒
sudo networksetup -setdnsservers Wi-Fi 8.8.8.8 1.1.1.1 192.168.1.1
```

---

*最後更新：2026-01-13*
