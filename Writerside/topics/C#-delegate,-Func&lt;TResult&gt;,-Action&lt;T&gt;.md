# C# delegate, Func&lt;TResult&gt;, Action&lt;T&gt; {id="C#-delegate,-Func&lt;TResult&gt;,-Action&lt;T&gt;"}

> **原文發布日期:** 2023-04-18
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/04/18/CSharp-delegate-Func-Action
> **標籤:** 無

---

簡介下委派的幾種使用方式

## 委派

delegate

相當於宣告一個 class 內的變數，其形態為 方法

[委派 delegate C# 基本概念具現化 | 御用小本本 - 點部落 (dotblogs.com.tw)](https://dotblogs.com.tw/jakeuj/2012/10/30/CSharp-delegate)

## `Func<TResult>`

相當於委派的區域變數版本

當作方法的傳入參數之一

只作用於該方法時使用

相對於委派的 class scope

可以理解為 function scope

### 範例

```
async Task Main()
{
  // 呼叫 DoSomethingAsync 處理一些事情，同時將如何輸出到檔案的方法傳入
  await DoSomethingAsync(
    "參數1",
    async Task (string message) =>
    {
      using (StreamWriter outputFile =
      new StreamWriter(Path.Combine(@"D:\logs", "WriteTextAsync.txt")))
      {
        await outputFile.WriteAsync(message);
      }
    }
  );
}

// You can define other methods, fields, classes and namespaces here

/// <summary>
/// 處理一些事情
/// </summary>
///	<param name="input">參數1</param>
///	<param name="outputFileFactory">輸出檔案的方法</param>
/// <returns></returns>
public async Task DoSomethingAsync(
  string input,
  Func<string, Task> outputFileFactory)
{
  // TODO: 處理一些事情

  // 將訊息輸出到檔案，但不關心如何輸出，輸出到哪裡
  await outputFileFactory($"訊息: {input}");

  // TODO: 繼續處理事情
}
```

### 對應關係圖

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/7bdeeccd-06ec-4edf-87f6-4520d8919414/1681801092.png.png)

對應關係圖

### 簡化版本

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/7bdeeccd-06ec-4edf-87f6-4520d8919414/1681803742.png.png)

## `Action<T>`

相當於 `Func<TResult>` 的 void 版本

也就是當你傳入的方法不需要回傳東西時改用 Action

剩下的泛型則一樣是該方法的傳入參數的型別

* void test() {} => `Action<T>` => `Action`
* int test() {return 1;} => `Func<TResult>` => `Func<int>`

先考慮要傳入的方法是否需要回傳東西 (Task, int, string … ETC.)

如都不需要則使用 Action

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/7bdeeccd-06ec-4edf-87f6-4520d8919414/1681804146.png.png)

Action

## 參照

[使用委派 - C# 程式設計手冊 | Microsoft Learn](https://learn.microsoft.com/zh-tw/dotnet/csharp/programming-guide/delegates/using-delegates)

[`Func<TResult>` 代理人 (System) | Microsoft Learn](https://learn.microsoft.com/zh-tw/dotnet/api/system.func-1?view=net-7.0)

[`Action<T>` 代理人 (System) | Microsoft Learn](https://learn.microsoft.com/zh-tw/dotnet/api/system.action-1?view=net-7.0)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* delegate

* 回首頁

---

*本文章從點部落遷移至 Writerside*
