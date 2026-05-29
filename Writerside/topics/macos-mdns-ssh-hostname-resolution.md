# macOS SSH 連線遇到 hostname 無法解析時，用 mDNS 或 hosts 處理

在 macOS 用 SSH 連區網設備時，如果出現 `Could not resolve hostname`，先把問題拆成「SSH 服務是否可連」和「主機名稱是否能解析」。最快的判斷方式是先用設備 IP 連線；如果 IP 可連但 hostname 不可連，再改試 mDNS 的 `.local` 名稱，或把固定 IP 寫進 `/etc/hosts`。

> 本文中的 hostname、IP、MAC address、網路設備名稱與管理介面資訊皆已去識別化，請替換成你自己的環境值。

<tldr>
<ul>
<li>IP 可連、hostname 不可連，通常是 DNS 或本機名稱解析問題。</li>
<li>同一個 LAN 或 VLAN 內，可以先試 `example-device.local` 這類 mDNS 名稱。</li>
<li>如果設備 IP 會固定，`/etc/hosts` 是最直接的本機別名修法。</li>
</ul>
</tldr>

## 問題症狀

在 Terminal 執行 SSH：

```bash
ssh user@example-device
```

出現類似錯誤：

```text
ssh: Could not resolve hostname example-device: nodename nor servname provided, or not known
```

這代表 macOS 無法把 `example-device` 解析成 IP address。此時 SSH 還沒有真的連到遠端主機，所以問題不一定是帳號、密碼、金鑰或 SSH daemon 設定。

## 先用 IP 判斷 SSH 本身是否可連

先從路由器、DHCP server、網管介面或設備本機查到目前 IP，然後直接用 IP 測試：

```bash
ssh user@192.0.2.203
```

如果用 IP 可以連線，代表：

- SSH client 和 server 基本上可用
- 網路路徑大致正常
- 問題集中在 hostname 解析

如果用 IP 也不能連，才往 SSH 服務、防火牆、帳號權限、port 或路由方向查。

## mDNS 是什麼

mDNS 是 multicast DNS，常見實作包含 Apple Bonjour 和 Linux Avahi。它不依賴中央 DNS server，而是在同一個區域網路內用 multicast 詢問：

```text
誰是 example-device.local？
```

如果目標設備支援並啟用 mDNS，它會回覆自己的 IP。macOS 對 `.local` 名稱有內建支援，所以可以直接試：

```bash
ssh user@example-device.local
```

適合 mDNS 的情境：

- 兩台設備在同一個 LAN 或同一個 VLAN
- 目標設備支援 Bonjour、mDNS 或 Avahi
- 不想為少量家用或實驗室設備維護 DNS record

不適合或容易失敗的情境：

- 跨 VLAN、跨 subnet，且沒有 mDNS reflector 或 gateway 轉送
- 防火牆擋住 UDP 5353 multicast
- 目標設備沒有啟用 mDNS
- 網管介面顯示的 hostname 不等於設備實際公告的 mDNS 名稱

## 查詢與驗證指令

確認一般名稱解析：

```bash
ping example-device
nslookup example-device
```

確認 mDNS 名稱：

```bash
ping example-device.local
dns-sd -G v4 example-device.local
```

查看 macOS 目前 DNS 狀態：

```bash
scutil --dns
```

清除 macOS DNS 與 mDNS 快取：

```bash
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

## 固定別名：寫入 `/etc/hosts`

如果設備 IP 已經透過 DHCP reservation 或 static IP 固定，可以在 Mac 本機加一筆 hosts 對應：

```bash
sudo nano /etc/hosts
```

加入：

```text
192.0.2.203 example-device
```

存檔後再測：

```bash
ssh user@example-device
```

`/etc/hosts` 的優點是簡單、立即、只影響目前這台 Mac。缺點是如果設備 IP 變更，這份本機設定也要同步更新。

## 建議處理順序

<procedure>
<step>
<p>先從路由器、DHCP server 或設備管理介面確認設備目前 IP。</p>
</step>
<step>
<p>用 IP 測試 SSH，確認問題是不是只發生在 hostname。</p>
</step>
<step>
<p>同一個 LAN 或 VLAN 內，先試 `example-device.local`。</p>
</step>
<step>
<p>如果 mDNS 不通，但 IP 固定，就把 `192.0.2.203 example-device` 加到 `/etc/hosts`。</p>
</step>
<step>
<p>如果要讓多台電腦都能用同一個 hostname，改在路由器、內部 DNS 或 DHCP DNS integration 上處理。</p>
</step>
</procedure>

## 小結

`Could not resolve hostname` 的重點是「名稱還沒變成 IP」，不是 SSH 驗證失敗。家用或小型實驗室環境通常先試 `.local` 最快；正式一點的做法則是固定 IP，再用內部 DNS 或 `/etc/hosts` 管理名稱。
