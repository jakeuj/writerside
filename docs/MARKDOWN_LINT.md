# Markdown Lint 使用指南

## 工具安裝

專案使用 `markdownlint-cli2` 進行 Markdown 格式檢查。

```bash
# 安裝依賴（已在 package.json 中定義）
npm install
```

## 使用方法

### 1. 使用 npm scripts（推薦）

```bash
# 檢查格式
npm run lint:md

# 自動修復格式問題
npm run lint:md:fix
```

### 2. 使用檢查腳本

```bash
# 只檢查不修復
./scripts/check-markdown.sh

# 自動修復
./scripts/check-markdown.sh --fix
```

### 3. 直接使用 npx

```bash
# 檢查
npx markdownlint-cli2 "Writerside/topics/**/*.md"

# 修復
npx markdownlint-cli2 --fix "Writerside/topics/**/*.md"
```

## 配置文件

`.markdownlint-cli2.jsonc` - 專案的 markdownlint 規則配置

### 主要規則

- **MD001**: 標題層級遞增 - ❌ 關閉（Writerside 有自己的層級管理）
- **MD003**: 標題樣式 - ✅ 使用 ATX 風格 (`#`)
- **MD004**: 列表樣式 - ✅ 使用破折號 (`-`)
- **MD013**: 行長度限制 - ❌ 關閉（中文文檔）
- **MD033**: 內聯 HTML - ✅ 允許（Writerside 需要）
- **MD041**: 第一行必須為標題 - ❌ 關閉
- **MD047**: 文件必須以換行符結尾 - ✅ 啟用

## GitHub Actions

專案配置了自動化的 Markdown lint 檢查（`.github/workflows/markdown-lint.yml`）：

- 在 push 或 pull request 時自動觸發
- 檢查 `Writerside/topics/**/*.md` 下的所有文件
- 使用 `DavidAnson/markdownlint-cli2-action@v16`

## 常見問題修復

### 文件末尾缺少換行符

```bash
# 使用 Python 腳本批量修復
python3 scripts/fix-markdown-endings.py
```

### 列表格式問題

- 確保列表項目使用 `-` 而不是 `*` 或 `+`
- 確保 `-` 和內容之間有空格：`- 項目` 而不是 `-項目`

### 標題格式問題

- 確保標題使用 `#` 符號（ATX 風格）
- 確保 `#` 和標題文字之間有空格：`# 標題` 而不是 `#標題`

## 相關連結

- [markdownlint](https://github.com/DavidAnson/markdownlint)
- [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2)
- [Markdown 規則說明](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)

