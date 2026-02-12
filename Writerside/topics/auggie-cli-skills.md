# Auggie CLI Skills 技能指南

Auggie CLI 支援 **Skills**（技能）功能，讓 AI 助手能夠整合專業領域知識，提供更精準且符合特定技術領域的協助。

## 核心概念

**Skills** 是預先定義的知識包，涵蓋特定技術領域、框架或最佳實踐。與 [Rules](auggie-cli-rules.md) 不同，Skills 提供的是**結構化的領域知識**，而非專案特定的編碼規範。

### Skills vs Rules

| 特性 | Skills（技能） | Rules（規則） |
|------|---------------|--------------|
| **用途** | 專業領域知識與最佳實踐 | 專案編碼規範與慣例 |
| **範圍** | 技術框架、語言、工具 | 專案或團隊特定指引 |
| **範例** | React、TypeScript、AWS | 命名慣例、commit 格式 |
| **位置** | 系統內建或遠端載入 | `.augment/rules/` 目錄 |

## 可用的 Skills {id="available-skills"}

### 前端開發
- **React** - React 框架最佳實踐與常見模式
- **Vue.js** - Vue.js 生態系統指引
- **Angular** - Angular 框架開發規範
- **TypeScript** - TypeScript 型別系統與進階用法
- **Next.js** - Next.js 全端框架
- **Tailwind CSS** - Utility-first CSS 框架

### 後端開發
- **Node.js** - Node.js 伺服器端開發
- **Express** - Express.js 框架
- **NestJS** - NestJS 企業級框架
- **Django** - Python Web 框架
- **FastAPI** - Python 現代 API 框架
- **Spring Boot** - Java 企業應用框架

### 雲端與 DevOps
- **AWS** - Amazon Web Services 服務與最佳實踐
- **Azure** - Microsoft Azure 雲端平台
- **GCP** - Google Cloud Platform
- **Docker** - 容器化技術
- **Kubernetes** - 容器編排
- **Terraform** - 基礎設施即代碼

### 行動開發
- **React Native** - 跨平台行動開發
- **Flutter** - Google 跨平台 UI 框架
- **Swift** - iOS 原生開發
- **Kotlin** - Android 現代開發語言

### 資料庫與資料處理
- **PostgreSQL** - 關聯式資料庫
- **MongoDB** - NoSQL 文件資料庫
- **Redis** - 記憶體快取
- **Elasticsearch** - 全文搜尋引擎

## 使用方式 {id="usage"}

### 在命令中啟用 Skills {id="enable-skills-in-commands"}

```bash
# 啟用單一 Skill
auggie --skill react "幫我建立一個使用 hooks 的 React 元件"

# 啟用多個 Skills
auggie --skill react --skill typescript "建立型別安全的 React 元件"

# 結合 Rules 與 Skills
auggie --rules .augment/rules/coding-style.md --skill react "實作 TodoList 元件"
```

### 在互動模式中使用

```bash
# 進入互動模式並載入 Skills
auggie chat --skill aws --skill terraform

# 在互動模式中，Skills 會持續生效
> 幫我設計一個高可用的 AWS 架構
> 產生對應的 Terraform 配置檔
```

## 配置 Skills {id="configure-skills"}

### 專案層級配置

在專案的 `.augment/config.yml` 中定義預設 Skills：

```yaml
skills:
  - react
  - typescript
  - tailwindcss

# 當執行 auggie 時，自動載入這些 Skills
```

### 使用者層級配置

在 `~/.augment/config.yml` 中設定全域 Skills：

```yaml
skills:
  default:
    - git
    - docker
  
# 適用於所有專案的通用 Skills
```

## 實際應用範例

### 範例 1：React + TypeScript 專案

```bash
# 建立符合最佳實踐的 React 元件
auggie --skill react --skill typescript \
  "建立一個 UserProfile 元件，使用 TypeScript interface 定義 props"
```

**輸出範例**：

```typescript
// UserProfile.tsx
import React from 'react';

interface UserProfileProps {
  userId: string;
  name: string;
  email: string;
  avatar?: string;
}

export const UserProfile: React.FC<UserProfileProps> = ({ 
  userId, 
  name, 
  email, 
  avatar 
}) =&gt; {
  return (
    &lt;div className="user-profile"&gt;
      {avatar &amp;&amp; &lt;img src={avatar} alt={name} /&gt;}
      &lt;h2&gt;{name}&lt;/h2&gt;
      &lt;p&gt;{email}&lt;/p&gt;
    &lt;/div&gt;
  );
};
```

### 範例 2：AWS + Terraform 基礎設施

```bash
# 產生雲端基礎設施代碼
auggie --skill aws --skill terraform \
  "建立一個包含 VPC、EC2 和 RDS 的基礎架構"
```

### 範例 3：Flutter + Material Design

```bash
# 行動應用開發
auggie --skill flutter \
  "建立一個登入頁面，使用 Material Design 3"
```

## 最佳實踐 {id="best-practices"}

### 1. 選擇相關的 Skills {id="select-relevant-skills"}

只啟用與當前任務相關的 Skills，避免資訊過載：

```bash
# ✅ 好的做法 - 相關技術棧
auggie --skill react --skill typescript

# ❌ 不好的做法 - 無關技術混雜
auggie --skill react --skill django --skill swift
```

### 2. 與 Rules 搭配使用

結合專案規則與領域知識：

```bash
# 使用專案規則 + 技術 Skills
auggie --rules .augment/rules/ --skill react --skill nextjs \
  "實作產品列表頁面"
```

### 3. 在專案初期設定預設 Skills

在 `.augment/config.yml` 中定義專案使用的技術棧：

```yaml
# .augment/config.yml
skills:
  - react
  - typescript
  - tailwindcss
  - nextjs

# 團隊成員執行 auggie 時自動載入這些 Skills
```

### 4. 使用描述性的提示詞

明確說明需求，讓 Skills 知識能精準應用：

```bash
# ✅ 好的提示詞
auggie --skill react "建立一個使用 Context API 管理狀態的購物車元件，包含新增、刪除、更新數量功能"

# ❌ 模糊的提示詞
auggie --skill react "做一個購物車"
```

## 自訂 Skills（進階） {id="custom-skills"}

### 建立自訂 Skill {id="create-custom-skill"}

如果您的專案使用特定框架或內部工具，可以建立自訂 Skill：

1. **建立 Skill 定義檔**

```yaml
# .augment/skills/internal-framework.yml
name: internal-framework
version: 1.0.0
description: 公司內部框架最佳實踐

knowledge:
  - |
    ## 框架概述
    我們的內部框架基於 React，但有以下特殊規範：
    
    1. 所有元件必須使用 `useCompanyHook` 進行狀態管理
    2. API 呼叫統一使用 `CompanyAPIClient`
    3. 錯誤處理遵循 `ErrorBoundary` 模式
    
  - |
    ## 元件結構
    ```typescript
    import { useCompanyHook } from '@company/hooks';
    import { CompanyAPIClient } from '@company/api';
    
    export const MyComponent = () => {
      const { state, dispatch } = useCompanyHook();
      // ...
    };
    ```

examples:
  - prompt: "建立一個使用者資料元件"
    response: |
      使用公司框架的標準模式...
```

2. **在配置中引用**

```yaml
# .augment/config.yml
skills:
  - react
  - typescript
  - file:./.augment/skills/internal-framework.yml
```

### 分享自訂 Skills {id="share-custom-skills"}

將 Skill 定義檔提交到版本控制，讓團隊成員共享：

```bash
git add .augment/skills/
git commit -m "feat: 新增內部框架 Skill 定義"
```

## 疑難排解 {id="troubleshooting"}

### Skill 未載入 {id="skill-not-loaded"}

**症狀**：AI 回應不符合預期的技術框架

**解決方案**：
```bash
# 檢查 Skill 是否正確載入
auggie --skill react --verbose

# 確認配置檔案
cat .augment/config.yml
```

### Skills 衝突 {id="skills-conflict"}

**症狀**：多個 Skills 提供矛盾的建議

**解決方案**：
- 移除不相關的 Skills
- 在提示詞中明確指定使用哪個框架

```bash
# 明確指定使用 React（即使同時載入 Vue Skill）
auggie --skill react --skill vue \
  "使用 React 建立元件（不要用 Vue）"
```

### 自訂 Skill 格式錯誤 {id="custom-skill-format-error"}

**症狀**：自訂 Skill 無法載入

**解決方案**：
```bash
# 驗證 YAML 格式
yq eval .augment/skills/custom.yml

# 檢查必要欄位
# - name
# - version
# - description
# - knowledge
```

## 進階技巧 {id="advanced-tips"}

### 1. 動態選擇 Skills {id="dynamic-skill-selection"}

根據檔案類型自動選擇 Skills：

```bash
# Shell script
if [[ $file == *.tsx ]]; then
  auggie --skill react --skill typescript "重構此元件"
elif [[ $file == *.py ]]; then
  auggie --skill python --skill fastapi "優化此 API"
fi
```

### 2. 結合 MCP（Model Context Protocol）

整合外部工具與 Skills：

```bash
# 使用 GitHub MCP + React Skill
auggie --mcp github --skill react \
  "分析此 PR 的 React 元件是否符合最佳實踐"
```

### 3. Skill 組合模板

建立常用的 Skill 組合別名：

```bash
# ~/.zshrc
alias auggie-web="auggie --skill react --skill typescript --skill tailwindcss"
alias auggie-backend="auggie --skill nodejs --skill postgresql --skill docker"
alias auggie-cloud="auggie --skill aws --skill terraform --skill kubernetes"

# 使用
auggie-web "建立登入表單元件"
```

## 與其他功能整合

### Skills + Rules + MCP

完整的工作流程範例：

```bash
# 1. 載入專案規則（編碼規範）
# 2. 載入技術 Skills（React/TypeScript）
# 3. 整合 GitHub MCP（存取 PR 資訊）

auggie \
  --rules .augment/rules/ \
  --skill react \
  --skill typescript \
  --mcp github \
  "檢視 PR #123 並提供符合我們編碼規範的改進建議"
```

### Skills 在 CI/CD 中使用

在 GitHub Actions 中整合：

```yaml
# .github/workflows/code-review.yml
name: AI Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Auggie
        run: npm install -g @augmentcode/cli
      
      - name: Review with Skills
        run: |
          auggie --skill react --skill typescript \
            "分析此 PR 的變更並提供建議" \
            --format markdown > review.md
      
      - name: Post Review
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: review
            });
```

## 相關資源

- [Auggie CLI Rules](auggie-cli-rules.md) - 專案規則設定指南
- [Auggie MCP Guide](auggie-mcp-guide.md) - Model Context Protocol 整合
- [Auggie User Rules Example](auggie-user-rules-example.md) - 使用者規則範例
- [官方文檔 - Skills](https://docs.augmentcode.com/cli/skills) - 完整的 Skills 參考
- [官方文檔 - CLI Reference](https://docs.augmentcode.com/cli/cli-reference) - 命令列參考

## 更新日誌

- **2026-02-12**: 初始版本創建
  - 添加 Skills 概念說明
  - 提供常見技術棧 Skills 列表
  - 包含使用範例與最佳實踐
  - 說明自訂 Skills 的方法
  - 整合 CI/CD 工作流程範例

---

**提示**：Skills 功能讓 Auggie 能夠理解特定技術領域的最佳實踐，與 Rules 結合使用可以獲得最佳效果。建議在專案初期就在 `.augment/config.yml` 中定義預設 Skills，確保團隊協作一致性。












