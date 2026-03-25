# Writerside Labels Reference

在下列情況讀這份參考：

- 想在 topic 或 chapter 標題旁加上版本、方案、WIP、experimental 等標記
- 想建立或修改 `labels.list`
- 想使用 `<primary-label>`、`<secondary-label>`
- 想判斷 `short-name`、`href`、`color`、tooltip 各自做什麼

這份筆記依據 JetBrains 官方文件整理：

- `Topic and chapter labels`

## labels 是做什麼的

- labels 用來標記某篇 topic 或某個 chapter 的適用性與狀態。
- 很適合表達：
  - 商業版 / 付費方案功能
  - internal only 功能
  - still in development / WIP
  - 某個特定版本才適用
  - 某項特定技術或平台標記

- 目的是讓讀者一眼看出這段內容跟自己有沒有關係。

## primary label 與 secondary labels

- 每個 header 最多只能有一個 primary label。
- 同一個 header 可以有多個 secondary labels。
- 讀者可以 hover label 看 tooltip 說明。
- primary label 如果有定義 `href`，讀者還可以點 label 跳到指定網址。

## `labels.list`

- labels 要先定義在 `labels.list`。
- 官方要求把這個檔案放在 help module root，也就是和 `writerside.cfg` 同層。
- 在這個 repo，位置會是：
  - [Writerside/labels.list](/Users/jakeuj/WritersideProjects/writerside/Writerside/labels.list)

目前這個 repo 還沒有 `labels.list`。

所以實務上：

- 如果要開始使用 labels，第一步不是直接在 topic 裡插 label tag。
- 要先建立 `labels.list`，把可用 label 定義好。

## `labels.list` 基本結構

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE labels SYSTEM "https://resources.jetbrains.com/writerside/1.0/labels-list.dtd">
<labels xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="https://resources.jetbrains.com/writerside/1.0/labels.xsd">
    <primary-label id="label" short-name="L" name="Label">
        This is an example label
    </primary-label>
    <primary-label id="jetbrains" short-name="JB" name="JetBrains"
                   href="https://www.jetbrains.com" color="red">
        Go to www.jetbrains.com
    </primary-label>
    <secondary-label id="wip" name="WIP" color="purple">
        Work in progress
    </secondary-label>
    <secondary-label id="beta" name="β" color="tangerine">
        Beta
    </secondary-label>
</labels>
```

## 各屬性怎麼分工

### `id`

- 每個 label 都必須有 `id`。
- 這是後續在 topic / chapter 中用 `ref` 指向它的鍵。

### `name`

- 這是實際顯示在 header 旁邊的文字。

### `short-name`

- 只用在 primary labels。
- 會用在 topic navigation block。
- 適合做較短的縮寫，避免導覽區太長。

### `href`

- 只在 primary label 有特別價值。
- 可讓使用者點 label 跳去某個外部說明頁，例如方案比較、版本頁面。
- 如果沒有明確目標頁，不要為了可點擊而硬加。

### `color`

- 用來指定 label 顏色。
- 顏色是幫助辨識，不是拿來做品牌設計比賽。
- 寫作時優先考慮一致性，不要每篇都自創一套色彩語意。

### tooltip 文字

- 寫在 label 元素開關標籤之間的文字，就是 hover 後顯示的說明。
- 這段應簡短、明確，直接解釋這個標記代表什麼。

## 怎麼把 labels 插到 topic / chapter

- 在 `<topic>` 或 `<chapter>` 內加入 `<primary-label>` 與 `<secondary-label>`。
- 實際使用時用 `ref` 指向 `labels.list` 裡定義好的 `id`。

範例：

```xml
<topic title="Labels" id="labels">
    <primary-label ref="label"/>
    <secondary-label ref="wip"/>
    <secondary-label ref="beta"/>
    <p>This is a labeled topic.</p>

    <chapter title="Some chapter" id="some-chapter">
        <primary-label ref="jetbrains"/>
        <secondary-label ref="2023.3"/>
        <secondary-label ref="experimental"/>
        <p>This chapter is labeled.</p>
    </chapter>
</topic>
```

## 適合的使用情境

- primary label 適合標示「這是什麼類型的功能或方案」這種主要分類。
- secondary labels 適合補充狀態，例如：
  - `WIP`
  - `Beta`
  - `Experimental`
  - `2023.3`

簡單判斷：

- 需要主標記、而且可能想做縮寫或點擊連結：primary label
- 只是補充狀態與版本：secondary label

## 和其他機制的分工

- labels vs `toc-title`
  - `toc-title` 是改側欄顯示名稱
  - labels 是加在 topic / chapter 標題旁的語意標記
- labels vs title 本文
  - 標題本身描述主題
  - label 描述適用性、版本或狀態
- labels vs admonition
  - label 是持續存在於 header 的 metadata
  - admonition 是正文內的提醒區塊

## 在這個 repo 的採用建議

- 目前 repo 還沒有 `labels.list`，也沒有既定 label 規範。
- 這表示可以導入，但最好先從少量、明確的 label 開始，例如：
  - `WIP`
  - `Experimental`
  - 某個版本號
- 不要一開始就替大量既有文章補 labels，否則很容易造成維護負擔。
- 如果真的要導入，先定義一套少數、可重複使用的 labels，再決定哪些 topic 值得加。
- 個人技術筆記通常不需要大量 labels；只有在讀者真的會因版本、方案、內部功能狀態而誤判時，labels 才特別有價值。
