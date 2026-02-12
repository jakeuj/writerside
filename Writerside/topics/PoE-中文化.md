# Path of Exile 中文化

## 簡介

Path of Exile (流亡黯道) 是一款免費的動作角色扮演遊戲，由 Grinding Gear Games 開發。遊戲提供了豐富的內容和複雜的遊戲機制，但官方並未提供完整的繁體中文支援。

## PoEDB 中文化資源

[PoEDB 台灣](https://poedb.tw/tw/chinese) 提供了完整的 Path of Exile 繁體中文化資源，包括：

- 物品名稱翻譯
- 技能寶石翻譯
- 天賦樹翻譯
- 任務對話翻譯
- 遊戲介面翻譯
- 中文化工具下載

## Mac 系統中文化安裝步驟

### 1. 下載中文字型檔

前往 [Google Fonts - Noto Sans TC](https://fonts.google.com/noto/specimen/Noto+Sans+TC) 下載繁體中文字型。

### 2. 準備字型檔

Mac 系統需要先找任意中文字型檔，將其改名為 `Font.ttf`，並放在 `PoeChinese_osx-x64` 旁邊。

### 3. 賦予執行權限

使用終端機執行以下指令，賦予中文化工具執行權限：

```bash
chmod +x ./PoeChinese3_osx-x64
```

### 4. 執行中文化工具

執行中文化工具，指定遊戲的 `Content.ggpk` 檔案路徑：

```bash
./PoeChinese3_osx-x64 '/Users/jakeuj/Applications/Sikarugir/PoE.app/Contents/SharedSupport/prefix/drive_c/Program Files (x86)/Grinding Gear Games/Path of Exile/Content.ggpk'
```

> **注意**：請根據你的實際安裝路徑修改上述指令中的路徑。

### 5. 建立自動化腳本（可選）

為了方便日後重複執行中文化工具，可以建立一個可執行腳本。

#### 建立腳本檔案

將以下內容存成 `~/Desktop/run-poe-chinese.command`：

```bash
#!/bin/bash

# 切換到 PoeChinese3 的資料夾
cd "/Users/jakeuj/Downloads/Heebo,Montserrat,Noto_Sans_Mono,Noto_Sans_TC 2/Noto_Sans_TC/PoeChinese3_osx-x64"

# ggpk 檔案路徑
GGPK_PATH="/Users/jakeuj/Applications/Sikarugir/PoE.app/Contents/SharedSupport/prefix/drive_c/Program Files (x86)/Grinding Gear Games/Path of Exile/Content.ggpk"

# 主程式
EXEC="./PoeChinese3_osx-x64"

echo "Running PoeChinese3..."
$EXEC "$GGPK_PATH"

echo ""
echo "=== Done ==="
read -n 1 -s -r -p "Press any key to close"
```

#### 設定執行權限

建立檔案後，在終端機執行：

```bash
chmod +x ~/Desktop/run-poe-chinese.command
```

#### 解除 macOS 安全性限制

若雙擊出現「無法打開、因為無法確認開發者身分」，請解除隔離：

```bash
xattr -d com.apple.quarantine ~/Desktop/run-poe-chinese.command
```

#### 使用方式

完成後直接雙擊 `run-poe-chinese.command` 即可啟動 PoeChinese3，並自動套用正體中文資料。

### 線上查詢

直接訪問 [https://poedb.tw/tw/chinese](https://poedb.tw/tw/chinese) 即可查詢各種遊戲內容的中文翻譯。

### 主要功能

1. **物品資料庫**
   - 裝備
   - 通貨
   - 寶石
   - 命運卡

2. **遊戲機制**
   - 天賦樹
   - 昇華職業
   - 傳奇物品
   - 製作配方

3. **賽季資訊**
   - 當前賽季機制
   - 賽季獎勵
   - 挑戰任務

## 相關資源

- [PoEDB 官網](https://poedb.tw/)
- [Path of Exile 官方網站](https://www.pathofexile.com/)
- [Path of Exile 台灣社群](https://www.ptt.cc/bbs/PathofExile/index.html)

## 常見問題

### 找不到 Content.ggpk 檔案？

遊戲檔案路徑可能因安裝方式不同而有所差異：

- **Steam 版本**：通常在 Steam 資料庫中
- **獨立版本**：在遊戲安裝目錄下
- **Mac 版本**：在 `.app` 應用程式套件內部

### 字型顯示異常？

確保使用的是完整的繁體中文字型檔（如 Noto Sans TC），並且檔名正確為 `Font.ttf`。

### 更新遊戲後中文化失效？

遊戲更新後可能會覆蓋中文化檔案，需要重新執行中文化工具。

## 注意事項

- PoEDB 的中文化內容由社群維護，可能會有更新延遲
- 建議搭配遊戲英文原文一起參考，以確保理解正確
- 新賽季內容通常需要一段時間才會完成中文化
- 每次遊戲更新後可能需要重新執行中文化工具
- 使用中文化工具前建議先備份原始的 `Content.ggpk` 檔案
