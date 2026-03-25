# Writerside Variables Reference

在下列情況讀這份參考：

- 想設定 `v.list` 或宣告 `<var>`
- 想使用 `%product%`、`%latest%` 這類變數插值
- 想理解 built-in variables、`ignore-vars`、`smart-ignore-vars`
- 想在 `<snippet>` / `<include>` 裡帶入變數，或做 instance-conditioned variables

這份筆記依據 JetBrains 官方文件整理：

- `Variables`

這個 repo 另外有一篇較精簡的本地示範：

- [Writerside/topics/variables.md](/Users/jakeuj/WritersideProjects/writerside/Writerside/topics/variables.md)

若你需要的是 `writerside.cfg` 的 `<vars>` 註冊位置或 `<smart-ignore-vars>` 所在層級，改讀 `writerside-cfg-reference.md`。  
若你需要的是 code block 的 `ignore-vars="true"`、`prompt`、`src` 或 `CDATA`，改讀 `code-reference.md`。  
若你需要的是 `<snippet>`、`<include>`、`<if>` 這些 reusable content 標記本身，改讀 `markup-reference.md`。

## 先分清楚三種變數

### 1. Global variables

- 宣告在 `v.list`
- 在整個 help module 內都可用
- 適合：
  - product name
  - version
  - company / support contact
  - 穩定重複出現的連結或名詞

### 2. Local variables

- 直接在 topic 或某個 element 內宣告 `<var>`
- 只在目前作用域有效
- 也可用來覆寫同名 global variable

### 3. Built-in variables

- Writerside 內建提供
- 不需要自己在 `v.list` 先宣告

## `v.list` 在哪裡

- `v.list` 是 help module 的全域變數檔
- 要在 [writerside.cfg](/Users/jakeuj/WritersideProjects/writerside/Writerside/writerside.cfg) 用 `<vars src="v.list"/>` 註冊

這個 repo 目前已經有：

- [v.list](/Users/jakeuj/WritersideProjects/writerside/Writerside/v.list)
- [writerside.cfg](/Users/jakeuj/WritersideProjects/writerside/Writerside/writerside.cfg) 內的 `<vars src="v.list"/>`

目前 `v.list` 內容是：

```xml
<vars>
    <var name="product" value="Writerside"/>
    <var name="latest"
         instance="hi"
         value="1.8"
         type="string"
    />
</vars>
```

這表示目前 repo 已經有：

- 通用的 `%product%`
- 只對 `hi` instance 生效的 `%latest%`

## Global variables 寫法

最基本範例：

```xml
<vars>
    <var name="latest_version" value="1.8"/>
</vars>
```

之後在 topic 裡可直接用：

```markdown
We recommend switching to version %latest_version%.
```

## Local variables 寫法

- 可直接宣告在 topic 內
- 或宣告在某個容器元素內，讓作用域只限該區塊

範例：

```xml
<var name="latest_version" value="2.0"/>
<note>
    <p>Upgrade to beta version %latest_version%.</p>
</note>
```

使用準則：

- 只在單一區塊臨時改值時，用 local variable
- 真正跨篇共用的值，回到 `v.list`

## Built-in variables

官方頁面列出幾個常見 built-in variables：

- `%instance%`
  - 目前 instance 的名稱
- `%instance-lowercase%`
  - 目前 instance 名稱的小寫
- `%currentId%`
  - 目前 instance 的 ID
- `%thisTopic%`
  - 目前 topic 的 ID

實務上：

- 想引用目前 instance / topic 身分時可直接用
- 但如果只是在單篇筆記硬塞動態文字，先想一下是否真的比直接寫死更清楚

## Variable interpolation

- Writerside 會把 `%var%` 視為變數插值
- 所以只要內容裡有 `%foo%`，就可能被解析

### 想原樣顯示 `%var%`

有兩種常見方式：

1. 在第一個 `%` 後面加反斜線

```text
%\var%
```

1. 用 HTML entity

```html
&percnt;var&percnt;
```

## `ignore-vars`

- 如果 code block、外部連結、圖片引用內的 `%` 應該照字面保留，就加 `ignore-vars="true"`
- 常見場景：
  - shell / Windows PATH
  - URL percent-encoding
  - 模板語法
  - 不該被展開的 placeholder

範例：

```xml
<code-block lang="console" ignore-vars="true">set PATH=c:\;%PATH%</code-block>
```

```xml
<a href="https://example.com/?q=%E5%8F%83%E6%95%B8" ignore-vars="true"/>
```

```xml
<img src="https://example.com/demo%20image.png" alt="demo" ignore-vars="true"/>
```

這個 repo 的 skill 已把它當成常見防呆規則，但若需要更深入理解變數系統本身，就回到這份 reference。

## `<smart-ignore-vars>`

- `smart-ignore-vars` 是 `writerside.cfg` 的 `<settings>` 子元素
- 它會改變預設行為：
  - 開啟後，某些位置會預設不展開變數
  - 需要明確 `ignore-vars="false"` 才展開

這個 repo 目前：

- [writerside.cfg](/Users/jakeuj/WritersideProjects/writerside/Writerside/writerside.cfg) 還沒有 `<settings>`
- 也沒有開啟 `<smart-ignore-vars>`

所以目前仍應假設 Writerside 會照預設規則嘗試解析 `%var%`。

## Variables in snippets

- 如果變數出現在 `<snippet>` 裡，值可在 `<include>` 內用子 `<var>` 傳入

官方概念大致是：

```xml
<snippet id="save-options">
    <var name="button" value="OK"/>
    Select the necessary options and click <control>%button%</control>.
</snippet>
```

然後 include 時可以：

```xml
<include from="lib.topic" element-id="save-options"/>
```

或覆寫：

```xml
<include from="lib.topic" element-id="save-options">
    <var name="button" value="Save"/>
</include>
```

判斷準則：

- 真正跨篇重用、又只差幾個字時，這招很實用
- 單篇筆記若只是偶爾重複一句話，通常不需要導入這層複雜度

## Conditional variables

- `<var>` 可加 `instance="..."`，讓同一變數在不同 instance 有不同值

範例：

```xml
<var name="product" value="MyWebApp" instance="web"/>
<var name="product" value="MyMobApp" instance="mob"/>
```

這個 repo 目前的 [v.list](/Users/jakeuj/WritersideProjects/writerside/Writerside/v.list) 已有同類型寫法：

- `latest` 只對 `instance="hi"` 生效

因為目前 repo 只有一個 instance，所以：

- 可以先把它理解成「限定 hi instance」
- 暫時不用為了未來多 instance 需求大改變數策略

## 在這個 repo 的採用建議

- 真正跨篇共用的穩定文字，再放進 `v.list`
- 單篇、單區塊特例，優先用 local `<var>`
- 看到 `%foo%` 時，先判斷它是 Writerside 變數，還是字面上的 placeholder / PATH / URL encoding
- 若只是模板示意或 shell 百分號，先考慮 `ignore-vars="true"` 或跳脫，不要等 checker 或輸出結果出錯
- 目前 repo 沒開 `smart-ignore-vars`，因此對 `%...%` 要更敏感一些
- 想快速回想最小範例時，可先看 [Writerside/topics/variables.md](/Users/jakeuj/WritersideProjects/writerside/Writerside/topics/variables.md)；要判斷 CI / checker 層級行為時，再回來讀這份 reference。

## 和其他參考檔的分工

- `v.list`、`<var>`、built-in variables、`%var%` 插值、`ignore-vars`、snippet 變數傳值：這份檔案
- `writerside.cfg` 的 `<vars>`、`<settings>`、`<smart-ignore-vars>`：`writerside-cfg-reference.md`
- code block 的 `ignore-vars`、`src`、`prompt`、`CDATA`：`code-reference.md`
- `<snippet>`、`<include>`、`<if>` 與其他 reusable content 標記：`markup-reference.md`
- instances 與 `instance="..."` 背後的 instance 脈絡：`instances-reference.md`
