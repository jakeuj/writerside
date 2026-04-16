# Codex 的 skill 與 plugin 有何差別

如果你的目標只是讓 Codex 更會做某一類工作，先建立 `skill` 就夠了；如果你要把多種能力包成可安裝、可分享、可整合的擴充套件，才需要建立 `plugin`。

本文依目前可見的 `skill-creator`、`plugin-creator` 與 `plugin.json` 模板整理。實際欄位與支援能力仍可能隨版本調整，但判斷邏輯大致可以這樣理解。

<tldr>
<p><code>skill</code> 比較像工作手冊，重點是流程知識與操作指引。</p>
<p><code>plugin</code> 比較像封裝外殼，重點是安裝、整合、分發與能力組合。</p>
<p>大多數情況可以先做 <code>skill</code>，成熟後再包成 <code>plugin</code>。</p>
</tldr>

## 為什麼這兩個概念很容易混在一起

最常見的混淆點是：`plugin-creator` 本身也是一個 `skill`。

這代表兩件事：

- `skill` 是 Codex 用來學習特定工作流程的基本單位。
- `plugin` 則是更外層的能力包裝，可以把 `skills`、`hooks`、`scripts`、`MCP` 設定和 apps 一起收進來。

所以它們不是互斥關係，而是不同層次的概念。

## 先講結論

| 面向 | `skill` | `plugin` |
| ------ | --------- | ---------- |
| 核心目的 | 教 Codex 怎麼完成某類任務 | 把一組能力包成可安裝的擴充套件 |
| 必要檔案 | `SKILL.md` | `.codex-plugin/plugin.json` |
| 典型內容 | 流程說明、參考資料、輔助腳本 | `skills`、`hooks`、`scripts`、`assets`、`.mcp.json`、`.app.json` |
| 著重點 | 知識、步驟、判斷方式 | 封裝、整合、安裝、上架 |
| 是否可單獨存在 | 可以 | 可以，但通常會搭配其他能力一起用 |
| 常見使用時機 | 想讓 Codex 更懂某個任務 | 想做成完整擴充套件給自己或團隊安裝 |

## `skill` 是什麼 {#skill-definition}

`skill` 可以把它想成「專門教 Codex 做某件事的說明書」。它的核心通常是 `SKILL.md`，裡面會說明：

- 什麼情況要觸發這個 skill
- 面對這類任務時要先看什麼
- 應該怎麼操作
- 哪些 `scripts/`、`references/`、`assets/` 要在需要時再讀

典型結構像這樣：

```text
my-skill/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

重點不在「安裝包」，而在「把經驗、規則和流程整理成 Codex 可重複使用的知識」。

如果你只是想讓 Codex 更會做 Azure 排障、Writerside 筆記整理、特定專案工作流，通常建立 `skill` 就夠了。

## `plugin` 是什麼 {#plugin-definition}

`plugin` 可以把它想成「可安裝的能力容器」。它最少會有一份 `.codex-plugin/plugin.json`，用來描述這個擴充套件是什麼、有哪些能力、怎麼在 Codex 介面裡呈現。

典型結構像這樣：

```text
my-plugin/
├── .codex-plugin/
│   └── plugin.json
├── skills/
├── hooks/
├── scripts/
├── assets/
├── .mcp.json
└── .app.json
```

如果需要讓 plugin 出現在安裝或排序清單中，還可能搭配 `.agents/plugins/marketplace.json`。

和 `skill` 相比，`plugin` 比較著重這幾件事：

- 如何被安裝或管理
- 如何組合多種能力
- 是否要附帶 `MCP server`、apps 或 hooks
- 是否要進 marketplace 或 UI 排序

## `skill` 與 `plugin` 的關係

最實用的理解方式是：

- `skill` 是能力內容本身
- `plugin` 是包裝與交付方式

換句話說：

- 一個 `plugin` 可以包含一個或多個 `skill`
- 一個 `skill` 不一定需要被包成 `plugin`
- 如果你的需求只有知識與流程，直接做 `skill` 會比較輕
- 如果你的需求已經擴大到整合多個能力元件，做 `plugin` 會比較合理

## 什麼情況該先做 `skill` {#when-to-start-with-skill}

這幾種情況，通常先做 `skill` 最省力：

1. 你想整理某個領域的工作流程。
2. 你需要讓 Codex 在特定任務上更穩定。
3. 你只需要 `SKILL.md` 加上一些輔助腳本或參考資料。
4. 你還在摸索需求，不想太早設計安裝結構。

這類任務的核心是「把 know-how 教給 Codex」，不是做成套件。

## 什麼情況該做 `plugin` {#when-to-build-plugin}

這幾種情況，比較適合直接做 `plugin`：

1. 你希望能力可以被安裝、管理或分享。
2. 你要把 `skills`、`hooks`、`MCP`、apps 一起打包。
3. 你需要明確的 manifest 與顯示資訊。
4. 你想把這組能力放進 marketplace 或讓 UI 能辨識。

這類任務的核心是「把能力整理成產品化的包裝」。

## 實務建議

如果你還在猶豫，預設可以採用這個順序：

1. 先做 `skill`
2. 確認流程真的穩定、內容真的有重用價值
3. 需要安裝、分發、整合時，再升級成 `plugin`

這樣的好處是你不會太早把心力花在封裝與結構設計上，也比較容易先把真正有價值的流程知識整理出來。

## 一句話總結

`skill` 是教 Codex 做事的方法，`plugin` 是把一組能力包裝成可安裝擴充套件的方法。

如果你的目標是讓 Codex「更懂怎麼做」，先做 `skill`；如果你的目標是讓這些能力「更好裝、更好管、更好分享」，再做 `plugin`。
