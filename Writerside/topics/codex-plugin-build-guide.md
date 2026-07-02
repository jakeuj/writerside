# Codex Plugin 建立指南

<web-summary>從零開始建立一個 Codex plugin：了解 repo 結構、plugin.json、agents/openai.yaml、skills、MCP、apps、hooks 與 marketplace 的完整工作流程。</web-summary>

在 Codex 裡，`plugin` 是最外層的能力包裝單位。一篇 plugin 可以包含多個 `skill`、MCP server 設定、apps（connectors）、hooks 與 scripts。本文從官方範例與社群實作整理出 plugin 的完整結構與建立方法。

## 前置背景

這篇筆記假設你已經了解 skill 與 plugin 的基本差異（可參考 [Codex Skill vs Plugin](codex-skill-vs-plugin.md)），重點放在「如何動手做一個 plugin」。

## Plugin 在 Codex 中的定位

一個 `plugin` 包含以下幾層能力：

| 元件 | 說明 | 必要？ |
| ------ | ------ | ------ |
| `.codex-plugin/plugin.json` | manifest，描述插件元資料與能力 | **必要** |
| `skills/` | 多個 `skill` 的集合，每個 skill 含 `SKILL.md` | 可選 |
| `.mcp.json` | 定義一個或多個 MCP server | 可選 |
| `.app.json` | 定義 Codex apps（connectors） | 可選 |
| `hooks.json` | 定義 post-tool 或其他生命週期 hook | 可選 |
| `agents/openai.yaml` | 定義 plugin 層級的介面呈現 | 可選 |
| `assets/` | 圖示、品牌相關資源 | 可選 |
| `commands/` | 自訂 CLI 命令 | 可選 |
| `scripts/` | 輔助腳本 | 可選 |

## 基本目錄結構

官方範例（figma plugin）的典型結構：

```text
figma/
├── .codex-plugin/
│   └── plugin.json
├── .mcp.json
├── .app.json
├── agents/                # plugin 層級的 openai.yaml
│   └── openai.yaml
├── assets/                # logo、icon
├── commands/              # CLI 命令
├── hooks.json             # 生命週期 hook
├── scripts/               # 腳本
├── skills/                # 多個 skill 目錄
│   ├── figma-use/
│   │   └── SKILL.md
│   ├── figma-generate-design/
│   │   └── SKILL.md
│   └── figma-swiftui/
│       └── SKILL.md
├── ui/                    # UI 相關資源
├── plugin.lock.json
└── README.md
```

以你的 [jakeuj/CodexPlugins](https://github.com/jakeuj/CodexPlugins) 為例：

```text
CodexPlugins/
├── .agents/
│   └── plugins/
│       └── marketplace.json      # 個人 marketplace 定義
├── .agents/skills/
│   └── plugin-creator/           # 用於建立 plugin 的 skill
├── plugins/
│   └── evennia/
│       ├── .codex-plugin/
│       │   └── plugin.json
│       ├── assets/
│       ├── plugin.lock.json
│       └── skills/
│           ├── SKILL.md
│           ├── evennia-typeclasses/
│           ├── evennia-commands/
│           └── ... (共 28 個 skills)
└── README.md
```

## `plugin.json` — 核心 Manifest

`.codex-plugin/plugin.json` 是最必要的檔案，決定 plugin 在 Codex 介面裡如何呈現。

參考官方範例（figma）：

```json
{
  "name": "figma",
  "version": "2.0.12",
  "description": "Figma workflows for design implementation, Code Connect templates, and design system rule generation.",
  "author": {
    "name": "Figma",
    "url": "https://www.figma.com"
  },
  "homepage": "https://www.figma.com",
  "repository": "https://github.com/openai/plugins",
  "license": "LicenseRef-Figma-Developer-Terms",
  "keywords": [
    "figma",
    "design-to-code",
    "ui-implementation",
    "code-connect",
    "design-system"
  ],
  "skills": "./skills/",
  "apps": "./.app.json",
  "mcpServers": "./.mcp.json",
  "interface": {
    "displayName": "Figma",
    "shortDescription": "Design-to-code workflows powered by the Figma integration",
    "longDescription": "Figma workflows for implementing designs in code, creating Code Connect templates for published Figma components, and generating project-specific design system rules for repeatable Figma-to-code work.",
    "developerName": "Figma",
    "category": "Creativity",
    "capabilities": [
      "Interactive",
      "Read",
      "Write"
    ],
    "websiteURL": "https://www.figma.com",
    "privacyPolicyURL": "https://www.figma.com/legal/privacy/",
    "termsOfServiceURL": "https://www.figma.com/legal/developer-terms/",
    "defaultPrompt": [
      "Inspect a Figma design and implement it in code",
      "Create Code Connect templates for my components",
      "Build or update a screen in Figma"
    ],
    "brandColor": "#1ABCFE",
    "composerIcon": "./assets/logo-padded.png",
    "logo": "./assets/logo-padded.png",
    "screenshots": []
  }
}
```

以你的 evennia plugin 為例：

```json
{
  "name": "evennia",
  "version": "1.0.0+codex.20260702023623",
  "description": "Evennia MUD game development skills — 28 comprehensive skills for learning and building with Evennia.",
  "author": {
    "name": "Jakeuj",
    "email": "jakeuj@example.com",
    "url": "https://github.com/jakeuj"
  },
  "homepage": "https://www.evennia.com",
  "repository": "https://github.com/jakeuj/evennia-codex-plugin",
  "license": "MIT",
  "keywords": [
    "evennia",
    "mud",
    "game-dev",
    "python",
    "text-adventure"
  ],
  "skills": "./skills/",
  "interface": {
    "displayName": "Evennia MUD Development",
    "shortDescription": "Learn and build MUD games with Evennia — 28 skills",
    "longDescription": "A comprehensive skill set for learning and developing with Evennia...",
    "developerName": "Jakeuj",
    "category": "Productivity",
    "capabilities": [
      "Interactive",
      "Write"
    ],
    "websiteURL": "https://www.evennia.com",
    "privacyPolicyURL": "https://www.evennia.com/privacy/",
    "termsOfServiceURL": "https://www.evennia.com/terms/",
    "brandColor": "#00AA00",
    "composerIcon": "./assets/evennia-logo.png",
    "logo": "./assets/evennia-logo.png",
    "screenshots": [],
    "defaultPrompt": [
      "Read the Evennia documentation page by page",
      "Create a new Evennia typeclass",
      "Build a custom command for my MUD game"
    ]
  }
}
```

### 必填欄位

| 欄位 | 說明 |
| ------ | ------ |
| `name` | plugin 唯一識別名稱 |
| `version` | SemVer 版本（可含 `+codex.20260702023623` 這類 build metadata） |
| `description` | 一句话说清楚 plugin 在做什麼 |
| `interface.displayName` | 在 Codex UI 顯示的名稱 |
| `interface.shortDescription` | 簡短描述（出現在 marketplace 卡片） |
| `interface.longDescription` | 完整描述 |
| `interface.category` | 分類（Productivity, Developer Tools, Creativity 等） |
| `interface.capabilities` | 能力類別（Interactive, Read, Write） |

### 可選欄位

| 欄位 | 說明 |
| ------ | ------ |
| `skills` | 指向 skills 目錄（相對路徑） |
| `apps` | 指向 `.app.json`（apps / connectors 配置） |
| `mcpServers` | 指向 `.mcp.json`（MCP server 配置） |
| `defaultPrompt` | 列出一串 prompt 範例（出現在 Codex composer） |
| `brandColor` | 品牌主色 hex 值 |
| `composerIcon` / `logo` | 圖示路徑 |
| `screenshots` | 截圖路徑陣列 |

## `agents/openai.yaml` — Plugin 與 Skill 層級的區別

這是很多人容易混淆的部分。`openai.yaml` 可以出現在兩個不同的層級：

### 1. Plugin 層級：`plugins/<name>/agents/openai.yaml`

定義整個 plugin 在 Codex 裡的介面呈現。例如 figma 的 plugin-level openai.yaml：

```yaml
interface:
  display_name: "Figma"
  short_description: "Use Figma for design-to-code work"
  icon_small: "./assets/figma-small.svg"
  icon_large: "./assets/figma.png"
  default_prompt: "Use Figma to inspect the target design and translate it into implementable UI decisions."
```

這跟 `plugin.json` 的 `interface` 區塊功能重疊，是另一個維度的宣告方式。

### 2. Skill 層級：`plugins/<name>/skills/<skill-name>/agents/openai.yaml`

定義 plugin 內某個特定 skill（子能力）的介面。例如 codex-security 裡的 attack-path-analysis skill：

```yaml
interface:
  display_name: "Attack Path Analysis"
  short_description: "Perform attack-path analysis for a security finding"
  default_prompt: "Use $attack-path-analysis to trace a given security finding from source to sink and calibrate severity accordingly."
```

### 兩者的關鍵差異

- Plugin 層的 `openai.yaml` 描述這個「套件」長什麼樣。
- Skill 層的 `openai.yaml` 描述套件裡某一個「子功能」長什麼樣。
- 同一個 plugin 內可以有多個 skill，每個 skill 都有自己的 `agents/openai.yaml`。
- Skill 層的 `default_prompt` 可以引用 plugin 層級的變數（例如 `$skill-name`），建立子能力與母件之間的關聯。

## Skills 在 Plugin 中的角色

Plugin 可以包含多個 skills，每個 skill 就是一套獨立的工作流程知識。

以 evennia plugin 為例，28 個 skills 各自獨立：

```
plugins/evennia/skills/
├── evennia-typeclasses/SKILL.md
├── evennia-commands/SKILL.md
├── evennia-attributes/SKILL.md
├── evennia-tags/SKILL.md
├── evennia-rooms/SKILL.md
├── evennia-objects/SKILL.md
├── evennia-exits/SKILL.md
├── evennia-characters/SKILL.md
├── evennia-accounts/SKILL.md
├── evennia-scripts/SKILL.md
├── evennia-locks/SKILL.md
├── evennia-channels/SKILL.md
├── evennia-commandsets/SKILL.md
├── evennia-default-commands/SKILL.md
├── evennia-help-system/SKILL.md
├── evennia-nicks/SKILL.md
├── evennia-evmenu/SKILL.md
├── evennia-eveditor/SKILL.md
├── evennia-coding-utils/SKILL.md
├── evennia-sessions/SKILL.md
├── evennia-signals/SKILL.md
├── evennia-ticker-handler/SKILL.md
├── evennia-monitor-handler/SKILL.md
├── evennia-on-demand-handler/SKILL.md
├── evennia-prototypes/SKILL.md
├── evennia-web-api/SKILL.md
├── evennia-web-admin/SKILL.md
└── evennia-doc-reader/SKILL.md
```

每個 skill 目錄內的結構：

```
skills/evennia-typeclasses/
├── SKILL.md           # 核心指令檔
├── references/        # 補充參考資料
└── scripts/           # 輔助腳本
```

## MCP Server 整合

如果 plugin 要提供 MCP server 功能，透過 `.mcp.json` 宣告。figma 範例：

```json
{
  "mcpServers": {
    "figma": {
      "type": "http",
      "url": "https://mcp.figma.com/mcp",
      "oauth_resource": "https://mcp.figma.com/mcp"
    }
  }
}
```

plugin.json 中的 `mcpServers: "./.mcp.json"` 把這個檔案連結進去。

## Apps（Connectors）整合

Codex 的 apps 系統允許 plugin 接入外部服務。figma 範例：

```json
{
  "apps": {
    "figma": {
      "id": "connector_68df038e0ba48191908c8434991bbac2"
    }
  }
}
```

plugin.json 中的 `apps: "./.app.json"` 連結此檔案。

## Hooks — 生命週期事件

`hooks.json` 允許 plugin 在 tool 執行前後觸發自訂邏輯。figma 範例：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/post_write_figma_parity_check.sh"
          }
        ]
      }
    ]
  }
}
```

這代表：當 Codex 使用了 Write 或 Edit tool 之後，自動執行 `post_write_figma_parity_check.sh`。

## 個人 Marketplace — 如何註冊你的 plugin

要在 Codex 中看到你的 plugin，需要在 repo 裡建立 `marketplace.json`。你的 jakeuj/CodexPlugins 結構：

```text
CodexPlugins/
├── .agents/
│   └── plugins/
│       └── marketplace.json     ← 個人 marketplace
├── plugins/
│   └── evennia/
│       └── ...
```

`marketplace.json`：

```json
{
  "name": "personal",
  "interface": {
    "displayName": "Personal"
  },
  "plugins": [
    {
      "name": "evennia",
      "source": {
        "source": "local",
        "path": "./plugins/evennia"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

官方範例庫也有類似的結構，放在 `.agents/plugins/marketplace.json`。

### policy 欄位說明

| 欄位 | 值 | 說明 |
| ------ | ------ | ------ |
| `installation` | `AVAILABLE` | 可供安裝 |
| `authentication` | `ON_INSTALL` | 安裝時需要驗證 |
| `authentication` | `ON_USE` | 使用時才需要驗證 |
| `products` | `["CODEX"]` | 限制只適用於特定產品 |

### 從 GitHub repo 安裝 marketplace plugin

當 plugin 與 `.agents/plugins/marketplace.json` 都已經推到 GitHub repo 後，其他電腦不需要手動 clone 整個 repo。依照官方 [Add a marketplace from the CLI](https://developers.openai.com/codex/plugins/build#add-a-marketplace-from-the-cli) 說明，可以先把 GitHub repo 加成 Codex marketplace，再從該 marketplace 安裝指定 plugin。

以 `jakeuj/CodexPlugins` 的 `evennia` plugin 為例：

```bash
codex plugin marketplace add jakeuj/CodexPlugins --ref main
codex plugin add evennia --marketplace personal
```

這裡的 `personal` 是 `marketplace.json` 最上層的 `name`，`evennia` 則是 `plugins[]` 裡的 plugin `name`。如果 marketplace 名稱或 plugin 名稱不同，安裝時要替換成實際值。

安裝後可以用以下指令查看、更新或移除已設定的 marketplace：

```bash
codex plugin marketplace list
codex plugin marketplace upgrade
codex plugin marketplace upgrade marketplace-name
codex plugin marketplace remove marketplace-name
```

其中 `upgrade` 會刷新已設定的 Git marketplace snapshot；只傳 `marketplace-name` 時會更新指定 marketplace。

## 建立 Plugin 的實作步驟

### 方法一：使用 plugin-creator skill

```bash
# 建立基本 plugin（不含 marketplace entry）
python3 .agents/skills/plugin-creator/scripts/create_basic_plugin.py my-plugin-name

# 包含 marketplace entry
python3 .agents/skills/plugin-creator/scripts/create_basic_plugin.py my-plugin-name --with-marketplace
```

### 方法二：手動建立

1. 建立 plugin 目錄與 manifest：

```bash
mkdir -p plugins/my-plugin/.codex-plugin
```

1. 填寫 `plugins/my-plugin/.codex-plugin/plugin.json`，參考上方 figma 或 evennia 的範例。

2. 建立 skills（每個 skill 一個子目錄）：

```bash
mkdir -p plugins/my-plugin/skills/my-skill
# 在 skills/my-skill/ 內放 SKILL.md
```

1. 可選：加入 `agents/openai.yaml` 定義 plugin 層級的介面。

2. 可選：加入 `.mcp.json`、`.app.json`、`hooks.json` 等檔案。

3. 在 `.agents/plugins/marketplace.json` 中註冊這個 plugin。

## 重要提醒：如何維護 Plugin 內的 Skills

根據社群建議（GPT 提供的經驗）：

**不要直接修改已安裝到本地之後的 skills 副本。**

正確做法是：

1. 在 plugins repo 裡更新 `plugins/<name>/skills/<skill-name>/SKILL.md`。
2. 重新安裝 plugin，Codex 會拉取最新版本。

這類似其他插件系統的更新模型：本地安裝的副本是 snapshot，原始來源才是 source of truth。直接改安裝後的副本，下次安裝時會被覆蓋。

## 完整目錄結構一覽

```
my-codex-plugins/
├── .agents/
│   └── plugins/
│       └── marketplace.json      # 把 plugin 掛到個人 marketplace
├── plugins/
│   └── my-plugin/
│       ├── .codex-plugin/
│       │   └── plugin.json       # 必要：manifest
│       ├── .mcp.json             # 可選：MCP server
│       ├── .app.json             # 可選：apps/connectors
│       ├── agents/
│       │   └── openai.yaml       # 可選：plugin 層級介面
│       ├── assets/               # 可選：圖示品牌
│       │   ├── logo.png
│       │   └── logo-padded.png
│       ├── commands/             # 可選：CLI 命令
│       ├── hooks.json            # 可選：生命週期 hook
│       ├── scripts/              # 可選：輔助腳本
│       ├── skills/               # 可選：多個 skill 目錄
│       │   ├── skill-a/
│       │   │   └── SKILL.md
│       │   └── skill-b/
│       │       ├── SKILL.md
│       │       └── agents/
│       │           └── openai.yaml   # skill 層級介面
│       └── plugin.lock.json      # lock 檔
└── README.md
```

## 參考資料

- [Codex Plugins Build Guide (官方)](https://developers.openai.com/codex/plugins/build)
- [openai/plugins 範例庫](https://github.com/openai/plugins)
- [jakeuj/CodexPlugins](https://github.com/jakeuj/CodexPlugins)
- [Codex Skill vs Plugin](codex-skill-vs-plugin.md)
