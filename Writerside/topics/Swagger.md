# Swagger UI 顯示 C# 集合型別範例值

<web-summary>記錄 C# 產生 Swagger / OpenAPI 文件時，如何用 XML &lt;example&gt; 標註集合型別預設值，讓 Swagger UI 顯示範例資料。</web-summary>

C# 產生 Swagger 文件的設定。

## Default Value

ICollection 的預設值可以用 `<example>[3]</example>` 這樣的方式來表示。

```C#
///<summary>
/// 選擇的 Id 清單
///</summary>
///<example>[3]</example>
public ICollection<long> SelectedIdList { get; set; }
```
