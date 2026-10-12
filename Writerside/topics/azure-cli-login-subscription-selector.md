# Azure CLI az login 訂閱選擇器：觸發條件、關閉方式與快速登入

<web-summary>Azure CLI az login 出現 Announcements 與訂閱選擇器時，依互動登入、TTY 與 core.login_experience_v2 判斷觸發條件，並用 --subscription、--skip-subscription-discovery 或關閉設定讓登入更快、腳本不卡住。</web-summary>

`az login` 結尾出現 `[Announcements] With the new Azure CLI login experience...` 不是錯誤，而是 Azure CLI 2.61.0 起預設開啟的訂閱選擇器。只想沿用上次的訂閱就直接按 Enter；想跳過選擇就在登入時用 `--subscription` 指定；需要完全回到舊行為時，把 `core.login_experience_v2` 設為 `off`。

> 本文依 Azure CLI 2.90.0 原始碼、2.91.0 變更紀錄與 2026 年 10 月的 Microsoft Learn 文件整理；tenant、subscription 皆為示意值。

<tldr>
<p>關閉選擇器：<code>az config set core.login_experience_v2=off</code></p>
<p>登入時直接指定預設訂閱（2.86.0+）：<code>az login --subscription &lt;subscription-id&gt;</code></p>
<p>訂閱很多時只抓一個訂閱：<code>az login --tenant &lt;tenant-id&gt; --skip-subscription-discovery --subscription &lt;subscription-id&gt;</code></p>
</tldr>

## 公告與選擇器長什麼樣子

互動登入完成後，Azure CLI 會列出可用的 tenant 與 subscription，等你輸入編號：

```text
Retrieving tenants and subscriptions for the selection...

[Tenant and subscription selection]

No     Subscription name    Subscription ID       Tenant
-----  -------------------  --------------------  ------------
[1]    Dev Subscription     <subscription-id-1>   <tenant-name>
[2] *  Prod Subscription    <subscription-id-2>   <tenant-name>

The default is marked with an *; the default tenant is '<tenant-name>' and subscription is 'Prod Subscription' (<subscription-id-2>).

Select a subscription and tenant (Type a number or Enter for no changes):
```

選完後會印出 `[Announcements]` 公告，再加一行 `[Warning] The login output has been updated...`，提醒登入輸出不再預設列出完整訂閱清單。

選擇器的細節：

- 清單依 subscription 名稱排序，名稱超過 36 個字元會截斷。
- `*` 標示目前的預設訂閱，也就是上次選過的訂閱；直接按 Enter 代表不變更。
- 輸入不存在的編號會顯示 `Invalid selection.` 並重新詢問。
- 沒有 tenant 顯示名稱時，`Tenant` 欄位改顯示 tenant ID。

## 什麼時候會出現選擇器 {#selector-conditions}

依 `az login` 的原始碼，必須**同時**符合以下三個條件才會顯示選擇器：

1. 使用者互動登入：瀏覽器 authorization code flow 或 device code flow。
2. stdin 與 stdout 都是 TTY，也就是沒有被 pipe、重導或用 `$(...)` 擷取。
3. `core.login_experience_v2` 沒有被關閉；未設定時預設為開啟。

| 登入方式或參數 | 是否顯示選擇器 |
| --- | --- |
| `az login`（互動，無篩選） | 會，即使只有 1 個訂閱也會顯示 |
| `az login --tenant <tenant-id>` | 會，只列出該 tenant 的訂閱 |
| `az login --subscription <id 或名稱>` | 只有符合的訂閱超過 1 個時才會 |
| `az login --tenant <tenant-id> --skip-subscription-discovery` | 不會，只建立 tenant 層級帳戶 |
| `--service-principal`、`--identity` 或 `--username` | 不會 |
| 用 `SUBS=$(az login)` 擷取或 pipe 給其他指令 | 不會，stdout 不是 TTY，照舊輸出 JSON |
| `core.login_experience_v2=off` | 不會，照舊輸出 JSON |

Microsoft Learn 寫到「某些環境」要先關閉選擇器才能使用 `--tenant`，但沒有說明是哪些環境。從 2.90.0 原始碼看，`--tenant` 與選擇器可以同時使用，提示文字會改成 `Retrieving subscriptions for the selection...`。

## 對腳本與 CI 的影響

- 擷取 `az login` 輸出的腳本不受影響：stdout 不是 TTY 時，選擇器會自動略過，仍回傳 JSON 陣列。
- 直接在終端機執行、又沒有擷取輸出的腳本，會停在選擇提示等待輸入。需要無人值守時，改用 `--subscription` 或關閉選擇器。
- CI 應改用 service principal、managed identity 或 workload identity federation，本來就不會出現選擇器。
- 登入後要取得目前訂閱，改用 `az account show`，不要依賴 `az login` 在終端機印出的內容。

只想在單次執行或 CI job 關閉時，可以依 Azure CLI 的 `AZURE_{section}_{name}` 環境變數命名規則設定：

```bash
AZURE_CORE_LOGIN_EXPERIENCE_V2=off az login
```

## 指定訂閱與略過訂閱探索 {#subscription-discovery}

Azure CLI 2.86.0 為 `az login` 新增 `--subscription` 與 `--skip-subscription-discovery`，可以在登入時決定預設訂閱，或減少登入時的 ARM API 呼叫。

```bash
# 完整探索所有訂閱，但直接把指定訂閱設為預設
az login --subscription <subscription-id-or-name>

# 只用 1 個 API 呼叫抓指定訂閱，適合 tenant 內訂閱很多的情境
az login --tenant <tenant-id> --skip-subscription-discovery --subscription <subscription-id>

# 完全不抓訂閱，只做 tenant 層級操作，例如 az ad
az login --tenant <tenant-id> --skip-subscription-discovery
```

使用限制：

- `--skip-subscription-discovery` 必須搭配 `--tenant`，否則直接報錯。
- 與 `--skip-subscription-discovery` 一起使用時，`--subscription` 必須是 GUID，不能用名稱。
- 只用 `--subscription` 時可以填 ID 或名稱；找不到時會出現 `Subscription '<value>' not found`。
- 搭配 `--skip-subscription-discovery` 卻無法取得指定訂閱時會報錯；若另外加上 `--allow-no-subscriptions`，則只留下 tenant 層級帳戶並顯示警告。

## 常用設定與指令

| 需求 | 指令 |
| --- | --- |
| 永久關閉選擇器 | `az config set core.login_experience_v2=off` |
| 重新開啟選擇器 | `az config set core.login_experience_v2=on` |
| 查看目前設定 | `az config get core.login_experience_v2`；未設定時會回報 `is not set`，代表使用預設開啟 |
| 登入後切換訂閱 | `az account set --subscription <subscription-id-or-name>` |
| 重新整理訂閱清單 | `az account clear` 後再執行 `az login` |
| 確認目前訂閱 | `az account show --query "{name:name, id:id, tenantId:tenantId}" -o table` |

`az account clear` 會清掉本機的訂閱快取，執行後在重新登入前無法使用需要訂閱的指令。

## macOS 認證 broker（2.91.0 預覽） {#macos-broker}

Azure CLI 2.91.0 新增 macOS 的 broker-based authentication 預覽，預設關閉，需要自行開啟：

```bash
az config set core.enable_broker_on_mac=true
az account clear
az login
```

開啟前要先安裝 Microsoft Company Portal 這類相容的 broker；依官方文件，沒有安裝 broker 時會改回瀏覽器登入。要恢復預設行為：

```bash
az config unset core.enable_broker_on_mac
az account clear
az login
```

使用 Homebrew 安裝時要先確認安裝來源：

```bash
brew list --versions azure-cli
brew list --cask --versions azure-cli
```

這項功能的 PR 說明 Homebrew **formula** 只依賴一般的 `msal`，刻意不包含 broker 需要的 `pymsalruntime`；Homebrew **cask** 與 pip 安裝才會帶上 `msal[broker]`。MSAL 1.36.0 在缺少 `pymsalruntime` 時會丟出 `ImportError`，而初始化 broker 的程式只攔截 `RuntimeError`。

依此推論，formula 版開啟 `core.enable_broker_on_mac` 後，`az login` 很可能直接報出缺少 `msal[broker]` 的錯誤，而不是改回瀏覽器登入；這點尚未實測。想試用 macOS broker，建議改用 cask 版或 pip 安裝的 Azure CLI。

Windows 從 2.61.0 起預設使用 Web Account Manager（WAM）。遇到 `User cancelled the Accounts Control Operation` 這類問題時，可用 `az config set core.enable_broker_on_windows=false` 改回瀏覽器登入，並先執行 `az account clear`。

## 參考資料

- [Microsoft Learn：Sign in with Azure CLI interactively](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively)
- [Microsoft Learn：Azure CLI configuration](https://learn.microsoft.com/cli/azure/azure-cli-configuration)
- [Microsoft Learn：Azure CLI release notes](https://learn.microsoft.com/cli/azure/release-notes-azure-cli)
- [Azure CLI 2.90.0：az login 實作 custom.py](https://github.com/Azure/azure-cli/blob/azure-cli-2.90.0/src/azure-cli/azure/cli/command_modules/profile/custom.py)
- [Azure CLI 2.90.0：訂閱探索 _profile.py](https://github.com/Azure/azure-cli/blob/azure-cli-2.90.0/src/azure-cli-core/azure/cli/core/_profile.py)
- [Azure/azure-cli#33376：macOS broker 預覽](https://github.com/Azure/azure-cli/pull/33376)
- [MSAL Python 1.36.0：broker.py](https://github.com/AzureAD/microsoft-authentication-library-for-python/blob/1.36.0/msal/broker.py)
