# C#11 Raw String Literals

> **原文發布日期:** 2023-01-11
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/01/11/CSharp-11-Raw-string-literals-string-Format
> **標籤:** 無

---

筆記 Input string was not in a correct format.

錯誤

```
public const string Id = "123";

public const string TestFormat = """
}
BEG*00*SA*{0}
""";

void Main()
{
 string.Format(TestFormat,Id).Dump();
}
```

修正

```
public const string Id = "123";

public const string TestFormat = """
}}
BEG*00*SA*{0}
""";

void Main()
{
 string.Format(TestFormat,Id).Dump();
}
```

結論

遇到 `{` 或 `}` 是文本原始內容時要重複打一次變成 `{{` 或 `}}`

要插值時則使用單一 `{` 或 `}` ，例如：`"{0}"` or `$"{Id}"`

參照

[彙整從 C# 1.0 到 C# 11.0 的字串格式變化 | The Will Will Web (miniasp.com)](https://blog.miniasp.com/post/2023/01/10/CSharp-String-Literals-Syntax-Collection)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- C#
{ignore-vars="true"}

- 回首頁

---

*本文章從點部落遷移至 Writerside*
