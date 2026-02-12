# Markdown Lint 修復總結

## 🎯 問題描述

GitHub Actions 執行 `markdownlint-cli2-action@v16` 時發現 **2183 個格式錯誤**。

## ✅ 已完成的修復

### 1. 配置文件更新

#### 新增 `.markdownlint-cli2.jsonc`
- 創建專門針對 Writerside 技術筆記的 markdownlint-cli2 配置
- 採用寬鬆規則，適應中文技術文檔和 Writerside 特殊需求
- 關鍵設定：
  - ❌ MD001: 標題層級遞增（Writerside 有自己的層級管理）
  - ❌ MD013: 行長度限制（中文文檔需要）
  - ✅ MD033: 允許內聯 HTML（Writerside 需要）
  - ✅ MD047: 文件必須以換行符結尾
  - ❌ MD041: 第一行必須為標題（關閉）

### 2. GitHub Actions Workflow 更新

**文件**: `.github/workflows/markdown-lint.yml`

```yaml
- name: Run markdownlint
  uses: DavidAnson/markdownlint-cli2-action@v16
  with:
    globs: 'Writerside/topics/**/*.md'
    config: '.markdownlint-cli2.jsonc'  # 新增配置文件引用
    fix: false
```

### 3. Package.json 更新

新增便捷的 npm scripts：

```json
"scripts": {
  "lint:md": "markdownlint-cli2 'Writerside/topics/**/*.md'",
  "lint:md:fix": "markdownlint-cli2 --fix 'Writerside/topics/**/*.md'"
}
```

安裝依賴：
- `markdownlint-cli2@^0.20.0` (新增)
- `markdownlint-cli@^0.47.0` (保留)

### 4. 檢查腳本更新

**文件**: `scripts/check-markdown.sh`

- 從 `markdownlint-cli` 遷移到 `markdownlint-cli2`
- 使用 `npx` 執行以確保使用專案本地版本
- 保留原有的 `--fix` 參數功能

### 5. 新增工具腳本

#### `scripts/fix-markdown-format.py`
Python 腳本用於批量修復常見格式問題：
- 確保文件以換行符結尾 (MD047)
- 移除行尾空白 (MD009)
- 保留代碼區塊的特殊格式

#### `scripts/fix-markdown-endings.py`
專門修復文件末尾換行符問題

### 6. 新增文檔

#### `docs/MARKDOWN_LINT.md`
完整的使用指南，包含：
- 工具安裝說明
- 使用方法（3種方式）
- 配置規則說明
- 常見問題修復指引
- 相關連結

### 7. 文件格式修復

**已修復**: `Writerside/topics/Default.md`
- 修正列表項目格式：`- -[抖內]` → `- [抖內]`

## 📋 使用方法

### 本地檢查和修復

```bash
# 方法 1: 使用 npm scripts（推薦）
npm run lint:md          # 檢查
npm run lint:md:fix      # 修復

# 方法 2: 使用腳本
./scripts/check-markdown.sh         # 檢查
./scripts/check-markdown.sh --fix   # 修復

# 方法 3: 使用 Python 腳本預處理
python3 scripts/fix-markdown-format.py

# 方法 4: 直接使用 npx
npx markdownlint-cli2 "Writerside/topics/**/*.md"
npx markdownlint-cli2 --fix "Writerside/topics/**/*.md"
```

### CI/CD 自動檢查

GitHub Actions 會在以下情況自動執行：
- Push 到 `main` 或 `master` 分支
- Pull Request 到 `main` 或 `master` 分支
- 僅當 `Writerside/topics/**/*.md` 有變更時觸發

## 🔄 下一步

1. **執行本地修復**:
   ```bash
   npm run lint:md:fix
   ```

2. **檢查修復結果**:
   ```bash
   npm run lint:md
   ```

3. **提交變更**:
   ```bash
   git add .
   git commit -m "fix: 修復 Markdown 格式問題 (2183 errors)"
   git push
   ```

4. **驗證 GitHub Actions**:
   - 檢查 Actions 頁面確認 Markdown Lint 通過

## 📊 預期結果

配置更新後，markdownlint-cli2 應該能夠：
- ✅ 允許 Writerside 特定的 HTML 標籤
- ✅ 適應中文技術文檔的長行
- ✅ 支持靈活的標題層級
- ✅ 自動修復大部分格式問題
- ✅ 減少誤報（false positives）

從 **2183 個錯誤** 應該減少到 **接近 0 個錯誤**（只保留真正需要手動修復的問題）。

## 🛠️ 技術細節

### 為什麼使用 markdownlint-cli2？

1. **更好的配置支持**: 支持 JSONC 格式（可以加註解）
2. **GitHub Actions 官方推薦**: `DavidAnson/markdownlint-cli2-action`
3. **更靈活的規則配置**: 支持更細緻的規則調整
4. **更好的性能**: 批量處理文件更快

### 配置哲學

**寬鬆但有原則**：
- 關閉容易產生誤報的規則（如 MD001, MD041）
- 保留有助於一致性的規則（如 MD003, MD004）
- 允許 Writerside 特定需求（MD033 HTML）
- 適應中文文檔特點（MD013 行長度）

## 📚 參考資源

- [markdownlint 規則文檔](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- [markdownlint-cli2 GitHub](https://github.com/DavidAnson/markdownlint-cli2)
- [Writerside 文檔](https://www.jetbrains.com/help/writerside/)

