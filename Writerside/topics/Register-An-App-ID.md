# Register An App ID

紀錄建立新 App ID 的過程。

## 建立 App

[Apps](https://appstoreconnect.apple.com/apps)
![ios_app_add.png](ios_app_add.png){ style="inline" }
在憑證、識別碼及描述檔註冊新的套件識別碼。

## 建立 App ID

[Identifiers](https://developer.apple.com/account/resources/identifiers/bundleId/add/bundle)
![ios_app_id_add.png](ios_app_id_add.png){ style="inline" }

### Capabilities

App 會用到哪些 iOS 系統權限/服務（Entitlements

- In-App Purchases
  - 沒要內購應該不勾，但我這邊不知道為什麼不讓我取消勾選，反灰，可能其實是 disabled 狀態？
- Push Notifications
  - 推播 （APNs entitlement）
  - 到 Certificates/Keys 建 APNs Auth Key（.p8）（通常比憑證好維護）
  - 後端用該 key 呼叫 APNs，App 端取 device token 並註冊到後端（依使用者/裝置）
- Associated Domains
  - 點 email/Teams/Line 的連結直接開 App（Universal Links）
  - 或未來有 Web 端 + App 端的深連結整合
  - applinks:你的網域（例如 applinks:portal.yourcompany.com）
  - 你的網域要放 AASA 檔（/.well-known/apple-app-site-association），內容要包含你的 Team ID + Bundle ID 與 paths（例如 /approvals/*）
- Sign In with Apple
  - 使用 Apple ID 登入功能

#### Universal Links（說明）

要跑起來：你需要 3 個東西

1) App 端（Xcode Capability）

在 Xcode 專案的 Signing & Capabilities 加上 Associated Domains，填：

applinks:portal.xxx.com

（有多環境就再加 applinks:portal-dev.xxx.com 之類）

1) 網站端：AASA 檔案（你最常卡的地方）

在你的網域放這個檔案（不能有副檔名）：

https://portal.xxx.com/.well-known/apple-app-site-association

AASA 範本（把 TEAMID 換成你頁面上的 Team ID：BDVWC3XQ35，Bundle ID 換你實際的）：

```json
{
    "applinks": {
        "apps": [],
        "details": [
            {
            "appID": "BDVWC3XQ35.com.jakeuj.demo",
            "paths": [
                "/approvals/*"
                ]
            }
        ]
    }
}
```

✅ 你這種 https://portal.xxx.com/approvals/{id} 會命中 /approvals/*。

AASA 伺服器注意：

Content-Type 建議：application/json

不能 302/301 轉址（最好直接 200）

不能被登入頁擋住（要公開可存取）

檔名就是 apple-app-site-association（無 .json）

1) 後端推播 / 信件連結的格式（帶你要的 deep link）
   推播 payload 範例（APNs）

你在 payload 放一個自訂欄位，例如 url：

```json
{
    "aps": {
    "alert": {
    "title": "待簽核",
    "body": "你有一筆新的簽核單"
    },
    "sound": "default"
    },
    "url": "https://portal.xxx.com/approvals/123456"
}
```

App 收到後（使用者點推播）就用這個 URL 導頁；因為是 Universal Links，iOS 會直接把它導進 App。

Email / Teams 連結

直接放同樣 URL：

https://portal.xxx.com/approvals/123456

MSAL（Entra ID）這邊提醒 1 件事

MSAL 的 redirect URI（例如 `msauth.<bundleId>://auth`{ignore-vars="true"} 那種）不是 Universal Links，不需要 Associated Domains；兩者可以並存、互不衝突。

## Face ID / Touch ID

[App IDs](https://developer.apple.com/account/resources/identifiers/bundleId)

### 必做：Info.plist 加這個

NSFaceIDUsageDescription（Face ID 使用說明）

範例文案（你可直接用）：

「用於身分驗證，以保護報表與簽核操作。」

「用於快速登入與確認簽核，確保資料安全。」

沒有這個 key：只要你呼叫 Face ID（LocalAuthentication）就會直接失敗。

### 實作層面（你要的簽核情境很常見）

通常做法是：

登入仍用 MSAL（Entra ID）

App 內開啟「使用 Face ID」後，用 Keychain 存放 refresh token / session，並用 LAContext 做解鎖

做到「再次開啟 App / 進入簽核詳細頁 / 送出簽核」時要求 Face ID

## 送審

[App Store Connect](https://appstoreconnect.apple.com/apps)

Apple 的核心審核原則（很重要）：審核人員必須能實際進入 App，看到主要功能。

你現在的情境：企業內部 App + AAD（Azure AD / Entra ID）。這類情況 Apple 常見且可接受，但你必須配合審核流程。

Apple 接受的作法有 3 種（依推薦順序）：

### ✅ 作法一（最推薦）：提供「審核用 AAD 測試帳號」

這是通過率最高且最乾淨的方式。

你需要做的事：

1. 在 Entra ID Tenant 建一組測試帳號（例如 `apple.review@yourcompany.com`）。
2. 指派最小權限（例如：只能查看報表、只有一筆測試簽核）。
3. 在 App Store Connect 的 **App Review Information** 中填入：
   - Username
   - Password
   - 登入流程說明（例如是否有 MFA、是否需同意條款等）

關於 MFA：

- MFA 很重要，但審核人員可能拿不到 SMS 或 Authenticator 的驗證碼。
- 請**不要**為審核帳號開啟 SMS / Authenticator 類型的 MFA。
- 可行做法：
  - 暫時關閉該帳號的 MFA；或
  - 在條件式存取（Conditional Access）中排除該審核帳號。

> 小提醒：這是企業 App 最常見、Apple 官方也建議的做法。

---

### ⚠️ 作法二：提供「Review Mode / Demo Mode」

可行但要小心實作方式：

方式範例：

- 在 App 內提供一個「Review Mode」按鈕，或提供特殊帳號（例如 `review@demo`）以載入 Demo 資料。
- Review Mode 可繞過 AAD 登入，直接展示功能範例畫面。

Apple 接受條件：

- Demo 內容必須能完整展示主要功能，不能只是空畫面或靜態截圖。
- 不能刻意隱藏真實功能或規避審核流程。

若 Apple 判定你在「規避登入審查」，仍有機會被拒。

---

### ❌ 作法三（不建議）：完全不提供登入方式

- 僅在備註寫 `This app is for internal employees only`。
- 高機率直接被 Reject，Apple 不會因為「企業內部」就免除審核。

---

## 建議的實作流程（報表、簽核、推播）

建議步驟：

1. 建立一組 Apple Review 專用的 AAD 帳號，關閉該帳號的 MFA。
2. 在測試帳號中放入假資料 / 測試簽核單，確保能展示完整流程（含推播/點擊後的跳轉）。
3. 在 App Store Connect 填寫清楚的 Sign-in Information：
   - `Username`
   - `Password`
   - 任何登入注意事項（例如「第一次登入會要求同意條款」、是否需要 VPN 或公司網路等）
4. 確認審核帳號不受公司 VPN / IP 限制或其他訪問限制（審核人員應能直接登入）。

這樣做可大幅提高一次通過審核的機率。

---

## 額外注意事項

- 如果你選擇走「Unlisted App / Custom App（ABM）」，審核規則仍然相同，Apple 仍會完整檢查登入流程。
- 一句話總結：**只用 AAD 登入時，Apple 幾乎一定要求可登入的審核帳號。企業內部 App ≠ 可以不讓 Apple 登入。**
