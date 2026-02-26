---
name: writerside
description: JetBrains Writerside 技術文件專案的撰寫、維護與發布指南，包含檔案結構、TOC 管理、Markdown 規範、語義標記語法及 GitHub Actions 部署流程。
---

# Writerside 技術筆記專案技能

## 專案概覽

此專案使用 JetBrains Writerside 建構中文技術筆記網站，發布於 GitHub Pages：

- **網站**: <https://jakeuj.github.io/writerside/>
- **文件目錄**: `Writerside/topics/` (Markdown `.md` 檔案)
- **圖片目錄**: `Writerside/images/`
- **目錄結構**: `Writerside/hi.tree` (XML 格式 TOC)
- **專案設定**: `Writerside/writerside.cfg`
- **建構設定**: `Writerside/cfg/buildprofiles.xml`

## 新增文件的標準流程

### 1. 建立 Markdown 檔案

在 `Writerside/topics/` 建立 `.md` 檔案：

```markdown
# 標題

內容說明...

## 子章節

程式碼範例：

\```bash
echo "Hello World"
\```
```

### 2. 更新 hi.tree 目錄結構

在 `Writerside/hi.tree` 加入對應的 `<toc-element>`：

```xml
<!-- 基本格式 -->
<toc-element topic="my-topic.md"/>

<!-- 自訂顯示名稱 -->
<toc-element topic="my-topic.md" toc-title="自訂標題"/>

<!-- 外部連結 -->
<toc-element href="https://example.com" toc-title="外部資源"/>

<!-- 巢狀結構（分類群組） -->
<toc-element toc-title="分類名稱">
    <toc-element topic="topic1.md"/>
    <toc-element topic="topic2.md"/>
</toc-element>
```

### 3. 執行 Markdown 格式檢查（必要步驟）

```bash
# 自動修復格式問題
markdownlint --fix Writerside/topics/my-topic.md

# 或使用專案腳本
./scripts/check-markdown.sh --fix

# 驗證修復結果（確認無錯誤）
markdownlint Writerside/topics/my-topic.md
```

## Markdown 格式規範

專案使用 `.markdownlint.json` 定義規則：

- **標題風格**: ATX 風格（`#` 符號），避免 Setext 底線風格
- **列表符號**: 破折號 `-`
- **行長度**: 不限制（中文文件需求）
- **HTML 標籤**: 允許（Writerside 語義標記需求）
- **重複標題**: 允許（不同章節可重複）
- **程式碼區塊**: 必須指定語言（e.g., ` ```bash `）

### 常見格式問題

```markdown
<!-- ❌ 錯誤：標題前後缺少空行 -->
內容
# 標題
內容

<!-- ✅ 正確 -->
內容

# 標題

內容

<!-- ❌ 錯誤：列表縮排不一致 -->
* 項目一
  * 子項目

<!-- ✅ 正確 -->
- 項目一
  - 子項目
```

## Writerside 語義標記（Semantic Markup）

可在 Markdown 中直接嵌入 Writerside XML 語義元素：

### 分頁籤（Tabs）

在 Markdown 檔案中嵌入 `<tabs>` 元素，內部可用 Markdown 程式碼區塊：

```xml
<tabs>
    <tab title="macOS">
    (此處放 Markdown 程式碼區塊，brew install xxx)
    </tab>
    <tab title="Windows">
    (此處放 Markdown 程式碼區塊，winget install xxx)
    </tab>
</tabs>
```

**注意**：`<tab>` 內的 Markdown 內容不能縮排，XML 標籤與 Markdown 之間需留空行。

### 步驟程序（Procedure）

```xml
<procedure title="安裝步驟">
    <step>下載安裝檔</step>
    <step>執行安裝程式</step>
    <step>重啟系統</step>
</procedure>
```

### 提示框（Admonitions）

```xml
<note>這是一般提示</note>
<tip>這是技巧提示</tip>
<warning>這是警告訊息</warning>
<caution>這是注意事項</caution>
```

### UI 控制項語義標記

```xml
<control>OK</control>        <!-- UI 控制項 -->
<path>~/.config/app</path>  <!-- 路徑 -->
<shortcut>Ctrl+S</shortcut> <!-- 快捷鍵 -->
```

## hi.tree 結構說明

`hi.tree` 是 XML 格式的目錄樹，定義整個文件站的導覽結構：

```xml
<?xml version='1.0' encoding='utf-8'?>
<instance-profile id="hi" name="Jakeuj's Notes" start-page="Default.md">
    <toc-element topic="Default.md">
        <!-- 頂層分類（無 topic，只有 toc-title） -->
        <toc-element toc-title="分類名稱">
            <toc-element topic="topic-file.md"/>
            <toc-element topic="topic-file-2.md" toc-title="自訂名稱"/>
        </toc-element>
    </toc-element>
</instance-profile>
```

**重要規則**：

- `topic` 屬性必須對應 `Writerside/topics/` 下實際存在的檔案名稱
- `toc-title` 可覆蓋文件的 H1 標題作為側邊欄顯示名稱
- 純 `toc-title`（無 `topic`）表示分類群組（不可點擊）

## 建構與部署

### GitHub Actions 自動部署

推送到 `master` 分支後自動觸發：

1. 使用 JetBrains Writerside Docker builder 建構
2. 使用 `writerside-checker-action` 驗證文件品質
3. 部署到 GitHub Pages
4. 更新 Algolia 搜索索引

### 本地 Docker 建構

```bash
docker pull jetbrains/writerside-builder:2025.04.8412
docker run --rm \
  -v $(pwd)/Writerside:/opt/sources \
  -v $(pwd)/artifacts:/opt/artifacts \
  jetbrains/writerside-builder:2025.04.8412 \
  hi
```

## 圖片使用規範

```markdown
![圖片說明](screenshot.png)
```

- 圖片放在 `Writerside/images/` 目錄
- 在 Markdown 中使用相對路徑引用（不需要 `images/` 前綴）
- 建議使用有意義的描述性檔名

## 常見問題排除

### markdownlint 錯誤

```bash
# 查看詳細錯誤
markdownlint Writerside/topics/*.md

# 批次修復所有文件
markdownlint --fix Writerside/topics/*.md
```

### hi.tree 找不到 topic 檔案

確認 `<toc-element topic="xxx.md"/>` 中的檔名與 `Writerside/topics/` 目錄中的實際檔名完全吻合（區分大小寫）。

### GitHub Actions 建構失敗

1. 檢查 Markdown 格式是否通過 markdownlint
2. 確認 hi.tree 中引用的所有 topic 檔案都存在
3. 查看 Actions 日誌中的具體錯誤訊息
