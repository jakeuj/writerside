# Writerside Math Reference

在下列情況讀這份參考：

- 想在 Writerside topic 裡加入數學公式
- 想使用 ` ```tex ` block 顯示獨立公式
- 想在段落內放 inline math
- 不確定該用 `<math>` 還是 Markdown `$...$`

這份筆記依據 JetBrains 官方文件整理：

- `Math expressions`

## 先判斷該不該用數學公式

- 只有在內容真的包含公式、符號推導、變數關係或數學表示時，再用 math support。
- 如果只是一般變數名、參數名、路徑或指令，仍然用 inline code，不要硬切成數學公式。
- 如果是長篇理論推導，記得先用文字交代上下文，不要整段只剩公式。

## Block math

- Writerside 用 `tex` language 的 code block 渲染獨立數學公式。
- 這種公式會以 block element 顯示，不是正文行內的一部分。

Markdown 範例：

````markdown
```tex
\begin{equation}
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
\end{equation}
```
````

XML 範例：

```xml
<code-block lang="tex">
\begin{equation}
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
\end{equation}
</code-block>
```

- 公式語法使用 Tex / LaTeX 數學表示法。
- 官方頁面提到可包含希臘字母、operators、trigonometric functions 和其他數學符號。

## Inline math

- 如果公式要放在段落內，不要用 block code，改用 inline math。
- XML 用 `<math>...</math>`。
- Markdown topic 可以直接用 `$...$`。

XML 範例：

```xml
Pythagorean theorem: <math>x^2 + y^2 = z^2</math>
```

Markdown 範例：

```markdown
Pythagorean theorem: $x^2 + y^2 = z^2$
```

## `<math>` 還是 `$...$`

- XML 結構裡，或你想明確表達 semantic markup 時，用 `<math>`。
- 純 Markdown topic 中，短公式直接用 `$...$` 最自然。
- 如果同一段內容本來就大量混用 XML semantic markup，使用 `<math>` 通常更一致。

## 和其他機制的分工

- math vs inline code
  - 數學關係、公式、上下標：math
  - 變數名、函式名、參數名、指令：inline code
- math vs 一般 code block
  - 要渲染公式：`tex` block
  - 要顯示可複製程式碼：一般 code block
- block math vs inline math
  - 獨立公式、推導主式：block math
  - 句子中的短公式：inline math

## 寫作建議

- 公式前先交代它代表什麼，不要直接丟一坨 Tex。
- 行內公式保持短小；太長就改成 block math。
- 如果文章主要不是數學或科學筆記，不要過度使用公式格式，免得可讀性下降。
- 寫完要回頭看 markdown 原文是否仍然容易維護，不要把簡單描述全部變成符號。

## 在這個 repo 的採用建議

- 目前 repo 內沒有明顯的 `tex` block 或 `<math>` 既有範例。
- 這代表可以導入，但建議先從簡單、短小的公式開始，確認文章風格仍然自然。
- 一般技術筆記大多不需要數學公式；只有在 AI、資料科學、工程或演算法主題真的需要時再用。
- 如果只是提到變數名稱如 `x`、`y`、`n`，通常 inline code 就夠了，不一定要上 math。
