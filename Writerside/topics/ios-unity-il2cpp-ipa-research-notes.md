# Unity IL2CPP iOS IPA 研究筆記：從 Mach-O、runtime resolver 到 pre-sign hook

<web-summary>在 Apple Silicon Mac 研究 Unity IL2CPP iOS IPA 時，從 Mach-O、cryptid 與 runtime IL2CPP API 建立版本鎖定 registry，辨識既有 relay patch，並用 Mac-first A/B 測試與 pre-sign hook 釐清 iOS code signing 問題。</web-summary>

以前在 Android 上研究 Unity 遊戲時，我的主要工具鏈是 APK、Riru、Il2CppDumper、Magisk 與重新簽署。那套流程整理在早期的 [Riru-Il2CppDumper 使用筆記]([反編譯]-Riru-Il2CppDumper-使用筆記.md)。

這次換成 Apple Silicon Mac、iPhone、IPA 與 Unity 6 後，我原本以為只是把 `libil2cpp.so` 換成 `UnityFramework`，實際做下來才發現真正困難的地方已經變成：

- App 內有不只一個 Mach-O，必須先確認誰負責啟動、誰承載 IL2CPP、誰是注入模組。
- App Store 下載的 IPA 不一定能直接做靜態分析，必須逐一確認 `cryptid`。
- `global-metadata.dat` 可能不是 Il2CppDumper 能直接解析的標準格式。
- 已修改過的樣本可能先在 `UnityFramework` 寫入 relay，再由 dylib 初始化 dispatcher；只換 dylib 會直接閃退。
- iOS 的 runtime inline hook 會碰到 code signing，`DobbyHook()` 回傳成功也不代表目標頁面真的能安全執行。

所以這篇不是一份「照著輸入幾個命令就完成」的工具筆記，而是我目前整理出的研究方法：先建立可信樣本、辨識 patch 模型、用 runtime IL2CPP API 解析目標，再決定 hook 應該在簽名前還是執行期完成。

## 和 2021 年 Android 筆記有什麼不同

| Android 常見流程 | iOS／IPA 對應問題 |
|---|---|
| 從 APK 找 `libil2cpp.so` | 先分辨 launcher 與 `UnityFramework` |
| 讀取 `global-metadata.dat` | metadata 可能另有封裝，無法直接 dump |
| Magisk／Riru 在 runtime 注入 | 側載前須完成 Mach-O 與簽章處理 |
| 修改 ELF 後重新簽 APK | 修改 Mach-O 後須由 Sideloadly 等工具完整重簽 |
| 以固定 offset hook | 版本更新後應重新解析 method，不能沿用 RVA |
| Android 裝置作為主要測試環境 | Apple Silicon Mac 可先做快速啟動與互動測試 |

如果目標是先取得官方 IPA、解包並確認檔案結構，可以先看 [使用 ipatool 下載、解壓與驗證 App Store IPA](app-store-ipa-ipatool-download-extract.md)。本文從「已經有可研究的 `.app`」開始。

## 先建立可重現的樣本

第一個原則是：**不要直接修改唯一一份來源 App**。

我會將工作區分成三層：

```text
lab/
├── input/                 # 唯讀來源 IPA 或 .app
├── reports/<version>/     # SHA-256、UUID、簽章與分析紀錄
├── src/                   # 自製 dylib 與工具原始碼
├── build/staging/         # 每次重新建立的工作副本
└── dist/                  # 未簽署 IPA 與測試產物
```

版本報告至少保留：

- App 版本、build number、最低 iOS 版本與 Unity 版本。
- launcher、`UnityFramework`、原有 dylib、metadata 的 SHA-256。
- 每個 Mach-O 的 UUID、架構、`cryptid`、依賴與 install name。
- 原始簽章狀態與 entitlements；公開筆記時移除 Team ID、裝置 ID 與帳號資訊。
- 實際測試使用的 macOS／iOS、安裝工具版本與最後採用的 Bundle ID。

這些資料不是附帶文件，而是所有 RVA、patch bytes 與 crash log 能否互相比對的前提。

## 解包後先分清楚四個角色

Unity iOS App 常見的四個研究對象如下：

| 對象 | 常見位置 | 主要用途 |
|---|---|---|
| launcher | `.app` 根目錄 | 啟動 App、載入 framework 與 dylib |
| `UnityFramework` | `Frameworks/UnityFramework.framework/` | Unity engine 與 IL2CPP native code 主體 |
| `global-metadata.dat` | `Data/Managed/Metadata/` 等位置 | IL2CPP 型別與方法 metadata；路徑依版本而異 |
| app-local dylib／framework | `Frameworks/` | 原廠元件或第三方注入模組 |

不要只對 launcher 執行一次 `otool` 就下結論。launcher 可能只是很薄的入口，真正的 gameplay code 與 patch 都在 `UnityFramework`。

### 最小靜態盤點

下面是一組適合放進版本報告的基本檢查。變數請換成自己的檔名：

```bash
APP_DIR="./Payload/Example.app"
MAIN_BINARY="$APP_DIR/Example"
UNITY_BINARY="$APP_DIR/Frameworks/UnityFramework.framework/UnityFramework"

plutil -p "$APP_DIR/Info.plist"
file "$MAIN_BINARY" "$UNITY_BINARY"
otool -L "$MAIN_BINARY"
otool -L "$UNITY_BINARY"
dwarfdump --uuid "$MAIN_BINARY" "$UNITY_BINARY"
otool -l "$MAIN_BINARY" | grep -A 5 LC_ENCRYPTION_INFO_64
otool -l "$UNITY_BINARY" | grep -A 5 LC_ENCRYPTION_INFO_64
codesign -dvvv "$APP_DIR" 2>&1
codesign -d --entitlements :- "$APP_DIR" 2>&1
shasum -a 256 "$MAIN_BINARY" "$UNITY_BINARY"
```

`cryptid 1` 代表該 Mach-O 仍是 FairPlay 加密狀態；即使 IPA 可以解壓，也不等於 binary 已適合靜態分析。要作為研究基線，應確認實際承載 IL2CPP 的檔案是 `cryptid 0`，而不是只檢查 launcher。

## Metadata 失效時改走 runtime IL2CPP API

這次遇到的 `global-metadata.dat` 並非 Il2CppDumper 能直接接受的標準格式，但 `UnityFramework` 仍匯出了完整的 `il2cpp_*` API。這時與其猜測 metadata 加密方式，我更傾向先做 runtime resolver：

```text
dylib constructor
  → 等待 UIApplication active
  → 以 RTLD_NOLOAD 取得 UnityFramework
  → dlsym 載入 il2cpp_* API
  → 等待 domain 與 assemblies 就緒
  → il2cpp_thread_attach
  → 枚舉 image／class／method／field
  → 驗證 native pointer
  → 安裝 hook 或只輸出 observer 診斷
```

constructor 不應直接安裝所有 hook。Unity domain、scene 與 UIApplication lifecycle 可能尚未就緒；比較穩定的做法是啟動狀態機，定期檢查 readiness，並以 atomic flag 保證同一個 registry 只安裝一次。

每個方法應使用完整查詢條件：

- assembly／image 名稱。
- namespace、class 與 method 名稱。
- 參數數量與各參數型別。
- 回傳型別；有 overload 時尤其重要。

解析成功後還要驗證：

1. 簽章只能得到唯一匹配。
2. `MethodInfo` 的 native pointer 位於 `UnityFramework` 可執行區段。
3. `dladdr()` 回報的 image 確實是 `UnityFramework`。
4. hook backend 回報成功，且 original pointer 非空。

任何一步失敗都只停用該功能並顯示原因，不回退到上一版 RVA。這樣版本更新時，失敗會是可診斷的 `unavailable`，而不是在未知位置寫入指令後閃退。

## 最大的坑：來源 UnityFramework 可能早已被 prepatch

我一開始做了最直覺的實驗：移除來源 mod，再放入自製 dylib。App 可以啟動到某些畫面，進入特定流程時卻跳到接近 null 的位址。

最後還原出的控制流不是「乾淨 Unity + dylib runtime hook」，而是：

```text
Unity callsite
  → 已寫入 UnityFramework 的 relay
  → 依 LR 推導 writable dispatcher slot
  → 原 mod 初始化的 dispatcher
  → hook record／trampoline
  → 原函式 continuation
```

只移除原 mod 時，Unity 內的 relay 仍存在，但 writable slot 沒有人初始化。等到 gameplay 第一次走到該 callsite，便會經由空 dispatcher 跳到無效位址。

這種問題很容易被誤判為「登入 SDK 閃退」、「Dobby 不相容」或「少了一個 framework」。真正有效的證據鏈應該包含：

- crash 的 fault address 與 exception registers。
- fault 前的 `PC`、`LR` 與反組譯。
- `LR` 正規化成 `UnityFramework` RVA 後落在哪個 callsite。
- callsite 是否先跳到 relay。
- relay 是否讀取一個原本應由舊 dylib 初始化的 slot。

看到這條完整鏈，才知道應該還原 Unity bytes、保留相容 loader，或重建原 dispatcher，而不是繼續盲改 entitlements。

## Relay 與 trampoline 不能一律當成 8 bytes

另一個容易踩到的坑，是假設所有 patch 都覆寫相同寬度。

我在同一個樣本裡還原出兩種模型：

| 模型 | 案例數 | 原 callsite 覆寫寬度 | 特徵 |
|---|---:|---:|---|
| inline relay | 105 | 8 bytes | 保存兩條原指令，再跳回 continuation |
| relocated trampoline | 10 | 4 bytes | 保存一條原指令，trampoline 另有重定位語意 |

也就是說，115 筆 registry 實際對應 125 個 patch site，而且不能用同一種 restore 規則處理。

更麻煩的是 AArch64 的 PC-relative 指令。從 relocated trampoline 讀到的 `B`、`BL` 或條件分支，不能直接把 raw bytes 複製回原 callsite；同一組 immediate 放到另一個位址，目標也會跟著改變。正確流程是先推導語意，再以原 callsite 為基準重新編碼。

我現在會在版本鎖定 registry 保存：

- `UnityFramework` SHA-256 與 UUID。
- callsite RVA、目前 bytes、預期原始 bytes。
- patch model 與 overwrite width。
- continuation、relay／trampoline RVA。
- PC-relative 指令的目標與必要 invariant。

### 還原工具要採 all-or-nothing

pre-sign 修補工具應先完成所有驗證，才寫入 staging：

1. 驗證來源 SHA-256 與 Mach-O UUID。
2. 驗證每個 RVA 都能透過 segment 的 `vmaddr`／`fileoff`／`filesize` 映射到檔案。
3. 驗證所有 current bytes 與預期一致。
4. 驗證 patch site 唯一、互不重疊，數量符合 registry。
5. 任一項不符就拒絕產出，不能只修成功的一半。
6. 全部寫入後重新掃描，記錄新 SHA-256 與實際修補數量。

這比「看到像 branch 就改回 NOP」慢一些，但可以避免產生一個能簽、能裝、卻在深層流程才爆炸的混合樣本。

## 用 Mac-first A/B 階梯縮短測試週期

Apple Silicon Mac 可以直接執行部分側載的 iOS App，因此很適合做第一層 smoke test。不必每次都先拿 iPhone 安裝、點擊與匯出 crash report。

我使用的版本階梯如下：

| 階段 | 唯一新增的變數 | 驗收重點 |
|---|---|---|
| source baseline | 不修改 | 確認來源本身可進入目標流程 |
| packaging control | 只解包、重封與重簽 | 排除封裝工具造成的差異 |
| loader-only | 只載入最小 dylib | 驗證 load command 與初始化時機 |
| framework removal | 移除可疑 framework | 分離 UI／Auth 與實際 patch 依賴 |
| restored loader | 還原既有 callsite 或相容 dispatcher | 驗證 prepatch 假設 |
| observer | overlay + resolver，不裝 gameplay hook | 驗證 lifecycle 與 IL2CPP 查詢 |
| functional | 每次只開一組 hook | 定位 code signing 或 ABI 問題 |

「看到標題畫面」不算所有版本的通過。測試里程碑必須覆蓋這次改動會經過的控制流：如果 crash 發生在登入，就測到登入；如果只在歌曲開始後觸發，就一定要實際開始歌曲。

Mac 與 iPhone 的 termination label 可能不同，因此我不直接比對錯誤文字，而是：

1. 確認 crash log 內的 binary UUID 與實際安裝檔一致。
2. 確認 `UnityFramework` 實際載入路徑。
3. 將 fault virtual address 正規化成 module RVA。
4. 比較兩端是否落在相同 callsite、relay 或 code page。

Mac 測試通過後再上 iPhone，可以節省大量來回；但 Mac pass 仍不能取代真機最後驗收。

## Dobby 回傳成功，不代表 hook 能執行

在 observer 版中，13 個方法都能唯一解析；functional 版甚至可能顯示 13/13 installed，但進入 gameplay 後仍收到 `CODESIGNING Invalid Page`。

原因是 hook 有多個階段：

```text
resolved
  → trampoline allocated
  → target page writable／remapped
  → branch activated
  → instruction cache invalidated
  → installed
  → target actually executed
```

只記錄 `DobbyHook()` 的回傳值，會把「建立 trampoline 成功」與「已安全修改 file-backed `__TEXT`」混在一起。診斷紀錄至少要包含：

- backend 與版本。
- runtime page size。
- target module、RVA 與所在 VM region。
- 每一個 stage 的開始／成功／失敗。
- Dobby status 與 original pointer。
- crash 時 fault page 是否屬於 `UnityFramework` 的 signed code。

第一版最好保留 JSONL 診斷檔，判定類 hook 則只累計統計，不要對每個 note 都同步寫檔。

## 為什麼可安裝的 mod 不代表有 JIT

這次另一個誤區，是看到原有 mod 可以執行，就推論它一定具備特殊 entitlements 或 JIT。

`Custom Entitlements` 是簽署時向系統宣告 App 所需 capability；最終是否生效，仍取決於 signing identity 與 provisioning profile。它不是繞過 code signing 的開關。

Apple 的 `allow-jit` entitlement 允許 App 以 `MAP_JIT` 建立可寫、可執行的記憶體，主要服務 JIT compiler。它不等於可以任意改寫已簽署、file-backed 的 `UnityFramework.__TEXT`。

我的 positive control 最後顯示，原 mod 能執行的關鍵是：Unity executable bytes 在 Sideloadly 最終簽署前就已被 patch；runtime dylib 主要負責初始化 writable dispatcher 與 records。這證明的是 **pre-sign static patch 可行**，不是 runtime JIT 已解鎖。

因此 iOS 上較穩定的設計通常是：

1. 在 staging 內驗證並完成版本鎖定的 Mach-O patch。
2. 清除舊 code signature。
3. 封裝 unsigned IPA。
4. 交給側載工具一次完成最終簽署。
5. runtime 模組只操作資料、dispatcher 與已規劃的可寫區域。

若真的需要 runtime code generation，再個別研究 `MAP_JIT`、write protection 與 provisioning；不要把它當成修復所有 inline hook 的通用選項。

## 可重現封裝流程

我目前會把封裝工具固定成以下步驟：

1. 驗證輸入版本、SHA-256 與 UUID，不符立即停止。
2. 將來源 App 複製到新的 staging。
3. 依 registry 驗證並執行必要的 pre-sign patch。
4. 用 Mach-O 工具移除不需要的 load command 或舊 code signature。
5. 刪除不再使用的 framework，放入自製 dylib。
6. 檢查 dylib install name 與所有相依 framework 都存在。
7. 正規化 executable 權限，移除舊 `_CodeSignature`。
8. 封裝成 unsigned IPA，輸出 manifest 與 SHA-256。
9. 由同一版側載工具簽署並安裝；不在封裝腳本內混入帳號資料。

封裝前的最低驗收包括：

- launcher 的相依項目不再包含已刪除的 framework。
- `UnityFramework` 仍能找到自製 dylib。
- IPA 內只有一份同名 dylib。
- 沒有依賴不存在的 app-local framework 或未預期的 Swift runtime。
- 所有 registry site 的 post-patch bytes 都符合預期。
- staging 與 dist 的 hash 已寫入版本報告。

處理 Mach-O load command 時可使用 [LIEF 的 Mach-O modification API](https://lief.re/doc/stable/tutorials/11_macho_modification.html)，但仍要在輸出後用 `otool`、`codesign` 與實際安裝交叉驗證。

## 最後心得

從 Android 的 Riru／Il2CppDumper 轉到 iOS，最重要的轉變不是換一套工具，而是把研究對象視為一條完整供應鏈：

```text
來源 IPA
  → 解密狀態與版本身分
  → Mach-O 相依與既有 patch
  → IL2CPP runtime 解析
  → hook／restore 模型
  → pre-sign staging
  → 最終簽署
  → Mac smoke test
  → iPhone 實機驗收
```

只要其中一層沒有被版本化，就很容易把不同原因混在一起：metadata 解析失敗被當成方法不存在、空 dispatcher 被當成登入 SDK 問題、signed code page 被當成 Dobby ABI 問題。

目前對我最有用的三個原則是：

1. **所有 offset 都要綁定 SHA-256 與 UUID。**
2. **observer 先證明解析與 lifecycle，functional 再一次增加一組 hook。**
3. **能在簽署前完成的 executable patch，就不要假設 runtime 一定能改 signed `__TEXT`。**

這樣即使下一版遊戲更新、method RVA 全部改變，舊報告仍然能告訴我「上一版為什麼成立」，而不是留下一包只能祈禱它剛好還能跑的固定 offset。

## 參考資料

- [Perfare/Il2CppDumper](https://github.com/Perfare/Il2CppDumper)
- [Perfare/Riru-Il2CppDumper](https://github.com/Perfare/Riru-Il2CppDumper)
- [jmpews/Dobby](https://github.com/jmpews/Dobby)
- [Apple：Allow execution of JIT-compiled code entitlement](https://developer.apple.com/documentation/BundleResources/Entitlements/com.apple.security.cs.allow-jit)
- [Apple：Porting just-in-time compilers to Apple silicon](https://developer.apple.com/documentation/Apple-Silicon/porting-just-in-time-compilers-to-apple-silicon)
- [Sideloadly changelog](https://sideloadly.io/changelog)
