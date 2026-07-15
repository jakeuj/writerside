# 在 macOS CrossOver 的 Guild Wars 2 啟用 arcdps

<web-summary>在 macOS 使用 CrossOver 執行 Guild Wars 2 時，除了把 arcdps 的 d3d11.dll 放到遊戲目錄，還要在 Wine 設定加入 Native then Builtin DLL override 才能正常載入。</web-summary>

在 CrossOver 安裝 arcdps 時，只有把 `d3d11.dll` 放到 `Gw2-64.exe` 旁邊通常還不夠；還要進入該 bottle 的 <ui-path>Wine 設定 | 函式庫</ui-path>，加入 `d3d11` override，並設成 <control>Native, then Builtin</control>。完成後重新啟動 Guild Wars 2，即可正常載入 arcdps。

<tldr>
    <p>把官方 `d3d11.dll` 放在 `C:\Program Files\Guild Wars 2\`，與 `Gw2-64.exe` 同一層。</p>
    <p>在 Wine 設定的函式庫新增 `d3d11`，並設為 Native, then Builtin。</p>
    <p>本文已在 CrossOver 26.2 搭配 DXVK 實測可正常使用。</p>
</tldr>

<warning>
    <p>arcdps 是第三方工具。官方網站明確提醒，使用第三方工具修改 Guild Wars 2 不受 ArenaNet 或 NCSoft 支援，使用者需自行承擔風險。遊戲或 arcdps 更新後也可能暫時失效。</p>
</warning>

## 問題症狀

依照 arcdps 官方說明下載 `d3d11.dll`，並放到 Guild Wars 2 安裝目錄後，遊戲可以正常啟動，但看不到 arcdps 介面，也沒有產生 `addons/arcdps/arcdps.log`。

檔案位置可能已經正確，真正缺少的是 CrossOver / Wine 的 DLL 載入設定。

## 根本原因

arcdps 官方安裝方式是把 `d3d11.dll` 放在 `Gw2-64.exe` 旁邊。這個 DLL 必須先被遊戲載入，arcdps 才能介入 Direct3D 11 的啟動流程。

CrossOver 預設會使用 Wine 內建的 DLL 實作與 bottle 選定的圖形 backend。即使遊戲目錄中已經存在 arcdps 提供的 `d3d11.dll`，如果沒有 DLL override，Wine 仍可能直接使用內建的 D3D11 實作，導致 arcdps 完全沒有被載入。

把 `d3d11` 設成 <control>Native, then Builtin</control>，就是要求 Wine 優先載入遊戲目錄中的 Windows 原生 DLL；若無法使用，才回退到 Wine 內建版本。

## 操作步驟

1. 完全關閉 Guild Wars 2。
2. 從 [arcdps 官方網站](https://www.deltaconnected.com/arcdps/)下載最新的 [`d3d11.dll`](https://www.deltaconnected.com/arcdps/x64/d3d11.dll)。
3. 在 CrossOver 選取安裝 Guild Wars 2 的 bottle，使用 <control>Open C: Drive</control> 開啟虛擬 C 槽。
4. 進入 `C:\Program Files\Guild Wars 2\`，把 `d3d11.dll` 放到 `Gw2-64.exe` 同一層。
5. 回到 CrossOver，開啟 <ui-path>Control Panels | Wine Configuration</ui-path>。
6. 切換到 <control>Libraries</control> / <control>函式庫</control>。
7. 在 <control>New override for library</control> 輸入 `d3d11`，不需要輸入 `.dll` 副檔名，然後按下 <control>Add</control> / <control>新增</control>。
8. 在既有 override 清單中選取 `d3d11`，按下 <control>Edit</control>，確認載入順序為 <control>Native, then Builtin</control>。
9. 套用設定並關閉 Wine Configuration，再重新啟動 Guild Wars 2。

![在 CrossOver 的 Wine 設定函式庫頁面輸入 d3d11 並按下新增](crossover-gw2-arcdps-d3d11-override.png){thumbnail="true" width="600"}{border-effect=line}

如果這個 bottle 除了 Guild Wars 2 還裝了其他程式，可以先在 Wine Configuration 的 <control>Applications</control> 頁面選取 `Gw2-64.exe`，再建立 `d3d11` override，避免設定影響 bottle 內的其他應用程式。

## 圖形 backend 要選 DXVK 還是 DXMT？

DLL override 才是這次能否載入 arcdps 的核心設定，圖形 backend 則屬於效能與版本相容性變數：

- 本次使用 CrossOver 26.2，啟動紀錄顯示 Guild Wars 2 使用 DXVK；加入 `d3d11` override 後，arcdps 可以正常運作。
- Reddit 討論中的更新解法使用 DXMT 搭配 MSync，也有人在 CrossOver 24、25 使用 DXVK 成功。
- 討論中曾有人回報 D3DMetal 無法載入 arcdps，但這不代表所有 CrossOver、GW2 與 arcdps 版本都會有相同行為。

因此建議先保留目前可以正常啟動遊戲的 backend，只新增 DLL override。如果仍無法載入，再一次只改一個變數，依序測試：

1. DXVK。
2. DXMT。
3. DXMT 搭配 MSync。

CodeWeavers 對 CrossOver 26 的定義是：DXVK 將 Direct3D 10 / 11 轉為 Vulkan；DXMT 是基於 Metal 的 Direct3D 11 實作；MSync 則是 macOS 的 semaphore-based synchronization。不同 Mac、CrossOver 版本與遊戲更新可能有不同結果，應以穩定性和 frame time 實測為準。

## 如何確認已載入？

啟動 Guild Wars 2 後可以用以下方式確認：

- 在角色選擇畫面按 <shortcut>Alt + Shift + T</shortcut>；Mac 鍵盤上的 <shortcut>Option</shortcut> 通常對應 Windows 的 <shortcut>Alt</shortcut>。
- 檢查遊戲目錄是否建立 `addons/arcdps/`。
- 檢查 `addons/arcdps/arcdps.log` 是否產生並持續更新。

如果完全沒有 arcdps 視窗，也沒有 `arcdps.log`，優先回頭檢查 DLL 檔名、所在目錄與 `d3d11` override，而不是先調整遊戲內的 UI 選項。

## 常見問題

### 遊戲更新後突然不能用

Guild Wars 2 更新可能改動 arcdps 使用的遊戲元件。先完全關閉遊戲，再從官方網站下載新版 DLL 覆蓋舊檔。

### `d3d11.dll` 還是無法載入

arcdps 官方允許把 DLL 改名為 `dxgi.dll`。若要測試這條路徑，應把 override 一起改成 `dxgi = Native, then Builtin`，不要同時保留兩份 arcdps DLL，以免重複載入或干擾判斷。

### 遊戲在角色選擇畫面崩潰

先移除其他 arcdps extension、chainload DLL 或會注入遊戲的 overlay，只保留官方 arcdps DLL 測試。官方也建議先修復遊戲客戶端，再用最小組合重現問題。

### 如何更新、重設或移除？

- **更新**：遊戲關閉時，以最新版 `d3d11.dll` 覆蓋舊檔。
- **重設設定**：遊戲關閉時，刪除遊戲目錄下的 `addons/arcdps/`。
- **移除**：遊戲關閉時，刪除 arcdps 的 `d3d11.dll`，並移除 Wine Configuration 裡新增的 `d3d11` override。

## 實測結論

這次遇到的問題不是 DLL 下載錯誤，也不是檔案放錯位置，而是 CrossOver 沒有優先載入遊戲目錄中的 arcdps DLL。設定 `d3d11 = Native, then Builtin` 後，在 CrossOver 26.2、DXVK 環境下已確認可以正常啟動與使用。

## 參考資料

- [arcdps 官方安裝與疑難排解說明](https://www.deltaconnected.com/arcdps/)
- [CodeWeavers：Troubleshooting Unlisted Applications in CrossOver Mac](https://support.codeweavers.com/troubleshooting-unlisted-applications-cxmac)
- [CodeWeavers：Advanced Settings in CrossOver Mac 26](https://support.codeweavers.com/en_US/miscellanous/advanced-settings-in-crossover-mac-26)
- [Reddit：Has anyone figured out how to get Arc DPS working on Crossover for Mac?](https://www.reddit.com/r/Guildwars2/comments/1lldf6z/has_anyone_figured_out_how_to_get_arc_dps_working/)
