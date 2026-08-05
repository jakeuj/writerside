# 使用 ipatool 下載、解壓與驗證 App Store IPA

<web-summary>在 macOS 使用 ipatool 從 App Store 下載官方加密 IPA，透過 unzip 指定解壓路徑，並檢查版本、簽章 metadata 與 Mach-O cryptid。</web-summary>

需要保存 App Store 的 `.ipa` 檔案時，可以使用 `ipatool` 以自己的 Apple Account 取得授權並下載，再用 `unzip -q -o -d` 解壓到指定目錄。下載結果是官方**加密 IPA**；能正常解壓、讀取 `Info.plist` 或瀏覽資產，不代表 Mach-O 已經解密。

最短流程如下：

1. 以 Homebrew 安裝 `ipatool`，互動式登入 Apple Account。
2. 使用 App Store 的數字 App ID 下載 IPA。
3. 用 `unzip -t` 驗證封裝，再以 `unzip -q -o ... -d ...` 解壓。
4. 從 `Info.plist` 核對版本，並用 `otool -l` 檢查每個目標 Mach-O 的 `cryptid`。

## 實測案例

以下使用 [hololive Dreams 台灣 App Store 頁面](https://apps.apple.com/tw/app/hololive-dreams/id6756641249) 作為範例。App Store URL 中的數字 App ID 是 `6756641249`；本次實測日期為 2026-08-05。

| 項目 | 實測值 |
|---|---|
| App | hololive Dreams |
| App ID | `6756641249` |
| Bundle ID | `game.qualiarts.hololive.dreams.com` |
| Marketing version | `1.0.100` |
| `CFBundleVersion` | `1785213472` |
| External version ID | `888716347` |
| 最低系統版本 | iOS 16.0 |
| IPA 大小 | 533,056,312 bytes，約 508 MiB |
| IPA SHA-256 | `521a5a74db7daa3f08ddd5f76038e0c9858a59c93e1dfbb1f3bfb2da2affe4a3` |
| 主程式 | arm64，`cryptid 1` |
| `UnityFramework` | arm64，`cryptid 1` |
| 簽章 metadata | Apple iPhone OS Application Signing，Team ID `KE3FLS6MZB` |

SHA-256 只代表這次取得的檔案，不應假設不同帳號、地區或下載時間會得到完全相同的雜湊。

## 前置條件

- macOS 與 Homebrew。
- 已能正常使用 App Store 的 Apple Account。
- 該 Apple Account 所屬商店區域能取得目標 App。
- 足夠的磁碟空間；解壓後通常會比 IPA 更大。

密碼與 2FA 驗證碼應只在本機互動式提示中輸入，不要寫進 shell history、腳本、環境變數或文件。

## 安裝與登入 ipatool

安裝 `ipatool`：

```bash
brew install ipatool
```

登入 App Store：

```bash
ipatool auth login --email "your-apple-account-email"
```

依提示輸入密碼與 2FA 驗證碼。登入完成後可以確認目前帳號狀態：

```bash
ipatool auth info
```

`ipatool` 的參數可能隨版本變動；實際操作前先查看目前安裝版本的說明：

```bash
ipatool auth login --help
ipatool download --help
```

## 下載官方加密 IPA

使用 App Store URL 中的 App ID 下載最新版：

```bash
ipatool download \
  --app-id 6756641249 \
  --purchase \
  --platform iphone \
  --output "hololive-Dreams-official-encrypted.ipa"
```

參數用途：

- `--app-id`：App Store 的數字 App ID。
- `--purchase`：帳號尚未取得授權時，先取得免費或付費 App 的授權。
- `--platform iphone`：下載 iPhone 平台套件。
- `--output`：指定輸出 IPA 路徑。

沒有指定 `--external-version-id` 時會下載當前可取得的最新版。因此即使輸出檔名包含預期版本，仍應從解壓後的 `Info.plist` 再確認實際版本。

## 驗證並解壓到指定目錄

先設定這次操作使用的檔案與目錄：

```bash
IPA_PATH="./hololive-Dreams-official-encrypted.ipa"
EXTRACT_DIR="./hololive-Dreams-official-encrypted"
```

驗證 ZIP 結構與 SHA-256：

```bash
unzip -t "$IPA_PATH"
shasum -a 256 "$IPA_PATH"
```

解壓到指定目錄：

```bash
unzip -q -o "$IPA_PATH" -d "$EXTRACT_DIR"
```

這三個參數分別表示：

- `-q`：quiet，減少一般解壓輸出。
- `-o`：overwrite，直接覆寫目的地中的同名檔案。
- `-d`：directory，指定輸出目錄。

解壓後，App bundle 通常位於：

```text
<extract-directory>/Payload/<app-name>.app/
```

IPA 也可能包含 `iTunesMetadata.plist`、`META-INF/`，以及 App bundle 內的 `SC_Info/`、`_CodeSignature/`、`Frameworks/` 與 `Data/`。

## 核對 Bundle ID 與版本

設定 App bundle 路徑：

```bash
APP_DIR="$EXTRACT_DIR/Payload/hololiveDreams.app"
```

使用 macOS 內建的 `PlistBuddy` 讀取必要欄位：

```bash
/usr/libexec/PlistBuddy -c 'Print :CFBundleIdentifier' "$APP_DIR/Info.plist"
/usr/libexec/PlistBuddy -c 'Print :CFBundleShortVersionString' "$APP_DIR/Info.plist"
/usr/libexec/PlistBuddy -c 'Print :CFBundleVersion' "$APP_DIR/Info.plist"
/usr/libexec/PlistBuddy -c 'Print :MinimumOSVersion' "$APP_DIR/Info.plist"
/usr/libexec/PlistBuddy -c 'Print :CFBundleExecutable' "$APP_DIR/Info.plist"
```

本次輸出為：

```text
game.qualiarts.hololive.dreams.com
1.0.100
1785213472
16.0
hololiveDreams
```

如果 IPA 根目錄含有 `iTunesMetadata.plist`，還可以讀取 external version ID，但不要把整份 plist 直接貼到公開文件，避免意外帶出帳號相關 metadata：

```bash
/usr/libexec/PlistBuddy \
  -c 'Print :softwareVersionExternalIdentifier' \
  "$EXTRACT_DIR/iTunesMetadata.plist"
```

## 檢查 cryptid

`cryptid` 要逐一檢查，不能只看主程式後就假設所有 framework 狀態相同。對 Unity IL2CPP 遊戲，原生遊戲程式碼常在 `UnityFramework`：

```bash
MAIN_BINARY="$APP_DIR/hololiveDreams"
UNITY_BINARY="$APP_DIR/Frameworks/UnityFramework.framework/UnityFramework"

otool -l "$MAIN_BINARY" | grep -A 5 LC_ENCRYPTION_INFO_64
otool -l "$UNITY_BINARY" | grep -A 5 LC_ENCRYPTION_INFO_64
```

本次兩個檔案都顯示：

```text
cmd LC_ENCRYPTION_INFO_64
cryptid 1
```

判讀方式：

| 狀態 | 意義 |
|---|---|
| `cryptid 0` | 該 Mach-O slice 未標示加密，可以繼續靜態分析；仍要另外確認來源與簽章。 |
| `cryptid 1` 或非零 | 執行內容仍受保護，可先盤點 plist、資產、依賴與簽章，但不能把它當成已解密 Mach-O。 |
| 沒有 encryption command | 記錄為未知或不適用，不要直接推論成官方原版或已解密。 |

因此這次成功下載與解壓，代表已取得完整官方封裝；不代表主程式或 `UnityFramework` 已能直接交給 IL2CPP dumper 做完整原生分析。

## 查看簽章 metadata

讀取 Identifier、簽章鏈與 TeamIdentifier：

```bash
codesign -dvvv "$APP_DIR" 2>&1 | \
  grep -E '^(Identifier|Authority|TeamIdentifier)'
```

本次可看到：

```text
Identifier=game.qualiarts.hololive.dreams.com
Authority=Apple iPhone OS Application Signing
Authority=Apple iPhone Certification Authority
Authority=Apple Root CA
TeamIdentifier=KE3FLS6MZB
```

簽章 metadata、ZIP 完整性與 `cryptid` 是不同檢查面向，不能互相替代。若 `codesign --verify` 顯示 resource envelope、封裝或簽章錯誤，應保存原始訊息並結合乾淨樣本判讀，不要只靠單一錯誤下結論。

## 下載指定舊版

先列出 App Store 仍提供的版本：

```bash
ipatool list-versions --app-id 6756641249
```

取得目標 external version ID 後再下載：

```bash
EXTERNAL_VERSION_ID="replace-with-external-version-id"

ipatool download \
  --app-id 6756641249 \
  --external-version-id "$EXTERNAL_VERSION_ID" \
  --platform iphone \
  --output "hololive-Dreams-old-version-official-encrypted.ipa"
```

Marketing version、`CFBundleVersion` 與 external version ID 是不同欄位。版本列表中出現某個項目，也不保證所有帳號、平台或商店區域都仍能下載。

## 常見問題

### 為什麼 Apple Configurator 安裝成功，卻找不到 IPA

Apple Configurator 的正式操作是把 App 加入連接裝置或 Blueprint。若目標是取得有明確輸出路徑的 `.ipa` 檔案，直接使用 `ipatool`，不要依賴可能隨版本改變的暫存 cache 路徑。

### 解壓成功是否代表已解密

不是。ZIP 層、資產檔與 Mach-O 加密狀態是不同層次。以這次樣本為例，IPA 可以完整解壓，但主程式與 `UnityFramework` 都是 `cryptid 1`。

### 為什麼 IPA 大小與 App Store 顯示不同

App Store 顯示的大小、實際下載套件大小與解壓後磁碟占用可能採用不同計算方式，也可能受裝置平台與商店回傳內容影響。記錄時要明確標示是商店顯示值、IPA bytes 還是解壓後大小。

## 參考資料

- [majd/ipatool](https://github.com/majd/ipatool)
- [hololive Dreams 台灣 App Store](https://apps.apple.com/tw/app/hololive-dreams/id6756641249)
- [Apple Configurator：Add apps to a device](https://support.apple.com/guide/apple-configurator-mac/cad4cd08c03/mac)
- [Apple iTunes Search API：Lookup Examples](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/LookupExamples.html)
