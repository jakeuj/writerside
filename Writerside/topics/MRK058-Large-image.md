# MRK058 Large image

放截圖常遇到警告

WriteSide MRK058:

Large image in paragraph rendered as a block element by default.

Put it outside the paragraph or set the 'style' attribute to indicate your intent.

## 解決方法

1. 將圖片放在段落外
2. 在圖片標籤加上 `style` 屬性，設定 `display: inline;`，讓圖片在段落內顯示

```Markup
![flutter-project.png](flutter-project.png){ style="inline" }
```

## 參照

[Inline and block images](https://www.jetbrains.com/help/writerside/images.html#img-style)
