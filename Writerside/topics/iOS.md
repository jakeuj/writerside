# Flutter iOS TestFlight

本文档描述如何使用 GitHub Actions 自动构建 Flutter iOS 应用、递增构建号，并上传到 TestFlight。

## 備註

1. 簽發憑證需要用 KeyChain, 但在 /Applications/Utilities/ 中找不到 KeyChain, 可以在 Finder 中搜尋 `KeyChain` 來找到。

        打開會提示請使用`密碼`取代`鑰匙串`，但新的`密碼`就真的只有儲存密碼的功能，憑證還是要由`鑰匙串`

2. 導出 p12 憑證時，需選擇 `登入` 裡面的 `憑證` Tab，選擇對應的憑證，右鍵選擇`導出`，選擇 `p12` 格式，並設定密碼。

        直接在 `登入` 裡面選憑證是不會有導出選項的，一定要切到 `憑證` Tab 才會有。
3. 雖然 Github 可以做 CI/CD，但是憑證還是需要有一台 Mac 才有辦法產生，所以這邊的 CI/CD 只是用來自動化流程，不是完全不需要 Mac。
4. p12 無法直接打開並複製到 Github Action Secrets，需要先轉成 base64 格式，再複製到 Github Secrets。
5. `cedvdb/action-flutter-build-ios@v1` 會去吃 `pubspec.yaml` 裡面的 environment > flutter > sdk 版本，所以要確保這個版本是正確的。

    ```yaml
    environment:
      sdk: ">=3.5.0 <4.0.0"
      flutter: 3.24.3 
    ```

6. ipa 上傳後，Apple 會自動檢查，需要依照檢查後的指示，到 `ios/Runner/Info.plist` 裡面增加對應的聲明設定值，例如：

```xml
<key>ITSAppUsesNonExemptEncryption</key>
<false/>
<key>NSPhotoLibraryUsageDescription</key>
<string>我們需要訪問您的照片庫來讓您上傳和分享圖片。</string>
```

1. 需要在 Mac 先 Build 一次，然後把 `build/ios/ipa/ExportOptions.plist` 複製到 `ios/GithubActionsExportOptions.plist`，並且把 `signingStyle` 改成 `manual`，這樣才能上傳到 TestFlight。
   - `com.myapp.app.dev` 是你的 Bundle ID
   - `{{ YOUR PROFIL NAME }}` 是你的 Provisioning Profile 名稱 [profiles](https://developer.apple.com/account/resources/profiles/list)
   - 參照：[flutter-build-ios](https://github.com/marketplace/actions/flutter-build-ios#3-build-locally)

      ```xml
      <key>signingStyle</key>
      <string>manual</string>
      <key>provisioningProfiles</key>
      <dict>
      <key>com.myapp.app.dev</key>
      <string>{{ YOUR PROFIL NAME }}</string>
      </dict> 
      ```

## 工作流程概览

此工作流程适用于推送到 `feature/testFlight` 分支时触发，并包含以下步骤：

1. **自动递增构建号**：确保每次上传到 TestFlight 时构建号都递增，避免重复上传错误。
2. **构建 Flutter iOS 应用**：使用 Flutter 构建命令生成 `.ipa` 文件。
3. **上传至 TestFlight**：通过 App Store Connect API 上传构建到 TestFlight。

## 先决条件

### 1. 设置 GitHub Secrets

为了使工作流成功运行，你需要在 GitHub 仓库中配置以下 Secrets：

- **CERTIFICATE_P12**：iOS Distribution 证书的 `.p12` 文件内容，使用 base64 编码。
- **CERTIFICATE_PASSWORD**：导出 `.p12` 文件时设置的密码。
- **PROVISIONING_PROFILE**：iOS Distribution 的 provisioning profile 文件内容，使用 base64 编码。
- **APP_STORE_CONNECT_ISSUER_ID**：从 App Store Connect 获取的 `Issuer ID`。
- **APP_STORE_CONNECT_KEY_ID**：App Store Connect 的 `Key ID`。
- **APP_STORE_CONNECT_PRIVATE_KEY**：App Store Connect API 的私钥内容。

### 2. 初始化构建号工具 `agvtool`

在本地的 iOS 项目中启用 `agvtool` 来自动递增构建号：

```bash
cd ios
agvtool new-version -all 1  # 初始化构建号为 1
```

### 3. 添加 `GithubActionsExportOptions.plist`

在 `ios` 目录中创建 `GithubActionsExportOptions.plist` 文件，内容如下：

```XML
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store</string>
    <key>uploadSymbols</key>
    <true/>
    <key>compileBitcode</key>
    <true/>
    <key>signingStyle</key>
    <string>automatic</string>
</dict>
</plist>
```

### 4. 工作流程 YAML

以下是 .github/workflows/testflight.yml 文件的完整内容：

```yaml
name: iOS Build and Deploy to TestFlight

on:
  push:
    branches:
      - feature/testFlight  # 在推送到 feature/testFlight 分支时触发工作流
  pull_request:

jobs:
  build:
    runs-on: macos-latest

    steps:
    - name: Checkout the code
      uses: actions/checkout@v3

    - name: Set up Ruby and install fastlane
      run: |
        sudo gem install fastlane

    - name: Increment build number
      run: |
        cd ios
        agvtool next-version -all  # 自动递增构建号

    - name: Flutter
      uses: cedvdb/action-flutter-build-ios@v1
      with:
        build-cmd: flutter build ipa --release --export-options-plist=ios/GithubActionsExportOptions.plist
        certificate-base64: ${{ secrets.CERTIFICATE_P12 }}
        certificate-password: ${{ secrets.CERTIFICATE_PASSWORD }}
        provisioning-profile-base64: ${{ secrets.PROVISIONING_PROFILE }}
        keychain-password: ${{ secrets.CERTIFICATE_PASSWORD }}

    - name: List IPA files
      run: ls -R build/ios/ipa

    - name: Upload app to TestFlight
      uses: henrik1/upload-testflight@v2
      with: 
        app-path: build/ios/ipa/demo.ipa
        issuer-id: ${{ secrets.APP_STORE_CONNECT_ISSUER_ID }}
        api-key-id: ${{ secrets.APP_STORE_CONNECT_KEY_ID }}
        api-private-key: ${{ secrets.APP_STORE_CONNECT_PRIVATE_KEY }}
```

### 5. 关键步骤说明

1. 自动递增构建号
   我们通过使用 agvtool next-version -all 来递增 Xcode 项目的构建号（CFBundleVersion），确保每次上传的构建号都高于之前的版本。

```yaml
- name: Increment build number
    run: |
        cd ios
        agvtool next-version -all
```

1. 构建 Flutter iOS 应用
   此步骤调用 Flutter 命令构建 .ipa 文件，使用 ios/GithubActionsExportOptions.plist 配置签名选项。

```yaml
- name: Flutter
    uses: cedvdb/action-flutter-build-ios@v1
    with:
        build-cmd: flutter build ipa --release --export-options-plist=ios/GithubActionsExportOptions.plist
        certificate-base64: ${{ secrets.CERTIFICATE_P12 }}
        certificate-password: ${{ secrets.CERTIFICATE_PASSWORD }}
        provisioning-profile-base64: ${{ secrets.PROVISIONING_PROFILE }}
        keychain-password: ${{ secrets.CERTIFICATE_PASSWORD }}
```

1. 上传至 TestFlight
   在生成 .ipa 文件后，使用 henrik1/upload-testflight@v2 上传到 TestFlight。

```yaml
- name: Upload app to TestFlight
    uses: henrik1/upload-testflight@v2
    with: 
        app-path: build/ios/ipa/demo.ipa
        issuer-id: ${{ secrets.APP_STORE_CONNECT_ISSUER_ID }}
        api-key-id: ${{ secrets.APP_STORE_CONNECT_KEY_ID }}
        api-private-key: ${{ secrets.APP_STORE_CONNECT_PRIVATE_KEY }}
```

### 注意事项

- 确保所有的密钥和证书已正确配置在 GitHub Secrets 中。
- 每次构建的应用版本号（CFBundleVersion）都需要递增，否则上传到 TestFlight 会失败。

### 参考资料

- [agvtool 文档](https://developer.apple.com/library/archive/qa/qa1827/_index.html)
- [Flutter 构建 iOS 应用](https://flutter-docs.dev.org.tw/deployment/ios)
- [App Store Connect API 密钥](https://developer.apple.com/documentation/appstoreconnectapi/creating-api-keys-for-app-store-connect-api)
