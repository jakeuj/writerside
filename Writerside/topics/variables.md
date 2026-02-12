# variables

變數是具有唯一名稱的命名值，可以在文檔中的不同位置使用。

因此，當您更改其值時，它將在所有文檔中更改。

事情經常會發生變化，值得放入變數中：

版本;

產品或公司名稱;

公司聯繫方式：電子郵件或電話號碼;

指向支援服務的連結。

## 全域變數

v.list

```XML
<vars>
<var name="latest_version"
     instance="hi"
     value="1.8"
     type="string"
/>
</vars>
```

其中 instance 須改為自己的 instance id

## 本地變數

```XML
<var name="latest_version" value="1.8"/>
```

## 變數的使用

```Markup
%latest_version%
```

{ignore-vars="true"}

## 忽略

% 後面加上反斜線 \ 可以跳脫

![Ignore.png](Ignore.png){style="block"}

或使用 `ignore-vars="true"` 來忽略

![image.png](image.png){style="block"}

## 輸出

> We recommend switching to the version %latest%.
>
{style="note"}

## 參考

[variables](https://www.jetbrains.com/help/writerside/variables.html)
