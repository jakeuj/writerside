# Fultter Build Version

Start typing here...
# Flutter Build Version（CI/CD 最佳實踐）

本文整理 Flutter 專案在 CI/CD 中管理 **build number（建置版本）** 的最佳實踐，目標是：

- 避免手動修改版本號造成上架失敗
- 避免 CI 內 commit 回 repo 產生競態條件
- 確保 iOS / Android build number 單調遞增，符合商店規則

---

## 1. Flutter 版本號結構說明

Flutter 使用 `pubspec.yaml` 中的 `version` 欄位：

```yaml
version: 1.2.3+456
```

| 區段 | 說明 |
|---|---|
| `1.2.3` | **Build Name**（給人看的版本）<br/>iOS：CFBundleShortVersionString<br/>Android：versionName |
| `456` | **Build Number**（給商店看的流水號）<br/>iOS：CFBundleVersion<br/>Android：versionCode |

### 重點原則

- `build name` 可人工控制（語意化版本）
- `build number` **必須持續遞增**（同一個 `build name` 下，上傳新建置也必須更大）

---

## 2. 為什麼不建議在 CI 內 commit 回 repo 改版本號

過往常見做法：

- CI 讀取 `pubspec.yaml`
- build number +1
- commit 回 repo（並排除本次 pipeline）

### 實務上的問題

- 平行 pipeline 會產生 **競態條件**（兩條都讀到舊號碼 → +1 撞號）
- Re-run / Retry 容易撞號或倒退
- 版本變更混在功能 commit 中，不利 review / rollback
- 需要額外規則避免無限觸發 CI

👉 **結論：不建議**（維護成本高、風險大）。

---

## 3. 建議的 CI/CD Build Number 策略（由推薦到次推薦）

### ✅ 方案 A：使用 CI 系統內建的遞增序號（最推薦）

直接使用 CI 提供的 build 序號作為 Flutter build number。

常見例子：

- GitHub Actions：`GITHUB_RUN_NUMBER`
- 其他 CI（Azure DevOps / Bitrise / Codemagic）：各自提供的 build number env

#### 優點

- 天然單調遞增
- 不怕平行建置
- 不需修改 repo
- 實作最簡單

👉 **團隊首選方案**。

### ⚠️ 方案 B：使用 Git commit 數量

```bash
BUILD_NUMBER=$(git rev-list --count HEAD)
```

#### 優點

- 不依賴 CI 平台（可跨平台）

#### 風險

- rebase / squash 會改變數量
- shallow clone 需注意 fetch depth
- 多分支併行時可能產生倒退

👉 僅適合 **主幹單線開發** 或已控管流程的專案。

### ⚠️ 方案 C：查詢商店最新 build 再 +1

- App Store Connect / Google Play API
- 常搭配 fastlane 使用

#### 優點

- 與商店狀態 100% 對齊，不會撞號

#### 缺點

- 需要 API 金鑰與權限
- pipeline 複雜度提高
- 外部服務失敗會影響建置

---

## 4. 關於 `build_version` 套件的評估

`build_version` 這類套件通常偏向：

- 將 package version 產生為程式碼（或產生常數）
- 方便在 App UI 顯示版本資訊

### 不適合用來解決的問題

- ❌ build number 自動遞增
- ❌ App Store / Google Play 的版本管理

### 可能衍生的成本

- 引入 `build_runner`/codegen
- CI 建置時間、快取複雜度增加
- 產生檔案是否 commit 的團隊規範問題

👉 **建議定位**：

- 版本顯示：可用
- CI build number 管理：不建議

---

## 5. GitHub Actions（iOS → TestFlight）建議做法

### 5.1 建議規範

- `pubspec.yaml` 的 `+<build>` 僅保留 placeholder（例如 `+1`）
- 每次 CI 用 `GITHUB_RUN_NUMBER` 產生 **單調遞增** 的 build number
- 透過 `flutter build ipa` 的 `--build-number` 覆蓋（不回寫 repo）

> `GITHUB_RUN_NUMBER` 在同一個 repo 會持續遞增，適合作為 iOS/Android 的 build number。

### 5.2 工作流程需求

- 需要一台 macOS runner 來產 ipa
- TestFlight 上傳通常建議用 **fastlane**（`pilot upload`），或你團隊既有的上傳方式
- 建議用 GitHub Environments / Secrets 管理憑證、App Store Connect API key

### 5.3 範例 `.github/workflows/ios-testflight.yml`

> 下列範例以「CI 覆蓋 build number、不改 repo」為核心；你只要把簽章與上傳段落接上你們既有做法即可。

```yaml
name: iOS TestFlight

on:
  workflow_dispatch:
  push:
    branches: [ main ]

jobs:
  build-and-upload:
    runs-on: macos-14

    env:
      # 人工控制的版本（build name）：建議由 release 流程決定
      BUILD_NAME: "1.0.0"
      # 商店用的 build number：使用 GitHub Actions 的遞增序號
      BUILD_NUMBER: ${{ github.run_number }}

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: "stable"
          cache: true

      - name: Flutter pub get
        run: flutter pub get

      # 如有 codegen，才需要這段；否則可移除
      # - name: Build runner
      #   run: dart run build_runner build --delete-conflicting-outputs

      - name: Build IPA (Release)
        run: |
          flutter build ipa \
            --release \
            --build-name "$BUILD_NAME" \
            --build-number "$BUILD_NUMBER"

      # 你可以在這裡加入：簽章、匯入 provisioning、或使用 fastlane match
      # 建議把憑證/密鑰放 GitHub Secrets 或用 keychain 匯入

      # 上傳 TestFlight（建議用 App Store Connect API Key）
      - name: Upload to TestFlight (fastlane)
        env:
          # 以下請改成你們的 Secrets 名稱
          APP_STORE_CONNECT_API_KEY_JSON: ${{ secrets.APP_STORE_CONNECT_API_KEY_JSON }}
        run: |
          gem install fastlane -N
          # 建議：把 API Key 寫到檔案（僅在 runner 暫存）
          echo "$APP_STORE_CONNECT_API_KEY_JSON" > /tmp/asc_key.json
          # 假設 flutter build ipa 輸出在 build/ios/ipa/*.ipa
          IPA_PATH=$(ls -1 build/ios/ipa/*.ipa | head -n 1)
          fastlane pilot upload \
            --api_key_path /tmp/asc_key.json \
            --ipa "$IPA_PATH" \
            --skip_waiting_for_build_processing true
```

#### 你一定會想調整的幾點

- `BUILD_NAME`：建議由 tag / release / 手動輸入參數決定
- 憑證與簽章：如果你們不是用 fastlane match，要加上 keychain import 與 provisioning 設定
- 若同時要 Android：可用同一個 `BUILD_NUMBER` 一次產出 aab

---

## 6. iOS TestFlight / App Store（build number）注意事項

### 6.1 同一個版本號（build name）下，build number 必須往上

例如：

- `1.0.0 (70)` 上傳過了
- 下一次仍是 `1.0.0` 時，必須用 `71`、`72`…

這也是最常見的「忘記改 build number → 上傳失敗」原因。

### 6.2 建議策略

- **不要**靠手動改 `pubspec.yaml`
- **不要**在 CI 回寫 repo 版本
- **要**用 CI 的遞增序號覆蓋 `--build-number`

### 6.3 若你們有多條 workflow / 多分支

- 建議「上傳 TestFlight」只允許從 `main`（或 release branch）觸發
- 或用 GitHub Environments 做 gate（避免 feature branch 不小心上傳）

---

## 7. 團隊建議落地做法（Recommended）

### pubspec.yaml

```yaml
version: 1.0.0+1 # +1 只當 placeholder，CI 會覆蓋
```

### CI/CD 規範

1. build number 一律由 CI 提供（GitHub Actions：`github.run_number`）
2. build 時使用 `--build-number` 覆蓋
3. 不在 CI 中 commit 回 repo
4. App 顯示版本：建議用 `package_info_plus` 讀取即可（或其他純讀取方案）

---

## 8. 總結

| 項目 | 建議 |
|---|---|
| Build Name（1.2.3） | 人工控管（語意化版本 / release 流程） |
| Build Number（+456） | CI 自動產生（GitHub：run_number） |
| CI commit 版本 | ❌ 不建議 |
| `build_version` 套件 | 僅用於顯示，不用於遞增 |