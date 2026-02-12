# Swagger

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
