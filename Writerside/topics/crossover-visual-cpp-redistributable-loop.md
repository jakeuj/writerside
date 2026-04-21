# CrossOver 重複提示安裝 Microsoft Visual C++ Redistributable

如果 CrossOver 裡的 Windows 應用程式每次啟動都跳出 `Microsoft Visual C++ 2015-2022 Redistributable (x64)` 安裝提示，即使已經安裝或修復過 runtime，通常可以在該 bottle 的 <ui-path>Wine 設定 | 函式庫</ui-path> 加入 VC++ Runtime 相關 DLL override，讓程式優先使用已安裝的原生 Microsoft DLL。

<tldr>
    <p>重點是設定同一個 bottle，而不是在 macOS 本機重裝 VC++ Runtime。</p>
    <p>在函式庫新增 `msvcp140`、`msvcp140_1`、`msvcp140_2`、`vcruntime140`、`vcruntime140_1`，並設成 Native first / Native then Builtin。</p>
    <p>`x64` 指的是 Windows 應用程式架構；Apple Silicon Mac 仍然要依 bottle 與 Windows 程式架構判斷。</p>
</tldr>

## 問題症狀

啟動應用程式時會反覆出現類似訊息：

```text
The following component(s) are required to run this program:

Microsoft Visual C++ 2015-2022 Redistributable (x64)

Would you like to install them now?
```

即使按下安裝、修復或重新啟動 CrossOver，下次開啟相同應用程式仍會再次提示。

![CrossOver 啟動 Windows 應用程式時重複提示需要 Microsoft Visual C++ 2015-2022 Redistributable](crossover-vcpp-redistributable-required.png){ width=552 }{border-effect=line}

## 解決方式

在 CrossOver 選取執行該應用程式的 bottle，開啟 <ui-path>Wine 設定 | 函式庫</ui-path>，把下列 DLL 加進 override：

```text
msvcp140
msvcp140_1
msvcp140_2
vcruntime140
vcruntime140_1
```

新增時通常不需要輸入 `.dll` 副檔名。加入後，確認這些項目的載入順序是 Native first、Native then Builtin，或 CrossOver 介面中等價的「優先使用 Windows 原生 DLL，再回退到 Wine 內建 DLL」設定。

## 操作步驟

1. 在 CrossOver 左側選取安裝該應用程式的 bottle。
2. 如果 VC++ Runtime 尚未安裝過，先在同一個 bottle 內安裝或修復 `Microsoft Visual C++ 2015-2022 Redistributable (x64)`。
3. 開啟 <ui-path>Control Panels | Wine Configuration</ui-path>。
4. 切到 <control>Libraries</control> / <control>函式庫</control>。
5. 在 <control>New override for library</control> 逐一輸入上方 DLL 名稱並加入。
6. 選取已加入的項目，確認載入順序是 Native first / Native then Builtin。
7. 套用設定後關閉 Wine Configuration，重新啟動應用程式。

完成後，正常情況下不會再看到 VC++ Runtime 安裝提示。

## 為什麼安裝後還是一直跳？

`Microsoft Visual C++ 2015-2022 Redistributable` 是 MSVC v14 系列 C/C++ runtime。許多用 Visual C++ 編譯的 Windows 程式會在啟動時檢查目標環境是否有對應 runtime，尤其常見於 Unreal Engine 遊戲、Steam/Epic 啟動流程或自帶 prerequisite installer 的應用程式。

在 CrossOver / Wine 裡，runtime 是安裝到特定 bottle 內。即使 DLL 檔案已經存在，程式實際載入時仍可能先碰到 Wine 內建 DLL、載入順序不符合程式預期，或 prerequisite checker 沒有正確判斷安裝狀態。這時重複執行安裝程式不一定會改變載入順序，所以問題會看起來像「裝了又沒裝」。

DLL override 的作用就是告訴 Wine：遇到這些 VC++ Runtime DLL 時，優先使用 bottle 裡的 Windows 原生版本。

<note>
    <p>CrossOver 的 bottle 彼此隔離。A bottle 裝好的 VC++ Runtime 或 DLL override，不會自動套用到 B bottle。</p>
</note>

## 可以補充檢查的項目

- **確認 bottle 架構**：錯誤訊息寫 `x64` 時，通常代表目標程式需要 64-bit VC++ Runtime。如果 launcher 是 32-bit、主程式是 64-bit，可能會同時需要 x86 與 x64 runtime。
- **確認不是裝到 macOS 本機**：Microsoft 的 `vc_redist.x64.exe` 要在 CrossOver bottle 內執行，裝在 macOS 本機沒有意義。
- **不要一次覆蓋所有 DLL**：DLL override 是排錯手段，設定錯誤可能讓其他程式壞掉。先針對錯誤訊息與 log 指到的 DLL 設定。
- **遇到其他 VC++ DLL 缺漏再補**：有些較新的程式可能還會提到 `msvcp140_atomic_wait`、`msvcp140_codecvt_ids`、`concrt140`、`vccorlib140`、`vcomp140` 等 DLL。除非錯誤訊息或 log 指向它們，否則先不要全部加。
- **必要時新建乾淨 bottle 測試**：如果同一個 bottle 已經裝過很多 runtime、DirectX、.NET 或自訂 override，新 bottle 反而比較容易判斷問題來源。

## 還原方式

如果加入 override 後應用程式反而無法啟動，回到 <ui-path>Wine 設定 | 函式庫</ui-path>，選取剛剛加入的 DLL override 後移除，或改回 CrossOver / Wine 預設值。這也是為什麼建議只在遇到問題的 bottle 裡調整，而不是把設定套到所有應用程式。

## 參考資料

- [Microsoft: Latest supported Visual C++ Redistributable downloads](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170)
- [CodeWeavers: Troubleshooting Unlisted Applications in CrossOver Mac](https://support.codeweavers.com/en_US/troubleshooting-unlisted-applications-cxmac)
- [CodeWeavers: CrossOver Mac User Guide](https://support.codeweavers.com/en_US/crossover-mac-user-guide)
- [Reddit: Hell is Us keeps asking to install Visual C++ in Crossover](https://www.reddit.com/r/macgaming/comments/1n9armq/hell_is_us_keeps_asking_to_install_visual_c_in/)
