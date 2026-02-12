# C# Using Stream Flush

> **原文發布日期:** 2023-02-07
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/02/07/184530
> **標籤:** 無

---

筆記下 Using 陳述式與 StreamWriter 空白的那些事

## Using

using namespace 甚麼的就不贅述了

這邊主要描述 using 包物件的用法

目前 using 有兩種寫法

有大括弧包起來的跟直接分號結尾的

既有寫法 (大括弧)

```
void Test()
{
    using(var stream = new MemoryStream())
    {
        // do something...
    }
}
```

新增寫法 (分號)

```
void Test()
{
    using var stream = new MemoryStream();
    // do something...
}
```

差別是有大括弧包起來的有 scope 的功能

而分號寫法等同大括弧直接包到方法結尾

所以以上述例子中的寫法來說是等價的

## StreamWriter

以下是將 Stream 寫入檔案的程式碼

```
var fileName = @"D:\file.bin";

using var stream = new MemoryStream();
using (var writer = new StreamWriter(stream, leaveOpen:true))
{
    await writer.WriteAsync(fileName);
};

using (var file = new FileStream(fileName, FileMode.Create, FileAccess.Write))
{
    stream.WriteTo(file);
}

await File.ReadAllTextAsync(fileName).Dump();
```

以上會正確存到檔案並讀取後輸出內容 `D:\file.bin`

此時如果把大括弧改成分號的寫法

```
var fileName = @"D:\file.bin";

using var stream = new MemoryStream();
using var writer = new StreamWriter(stream);
await writer.WriteAsync(fileName);

using var file = new FileStream(fileName, FileMode.Create, FileAccess.Write);
stream.WriteTo(file);

await File.ReadAllTextAsync(fileName).Dump();
```

首先會發生例外

`The process cannot access the file 'D:\file.bin' because it is being used by another process.`

需要在讀取檔案之前先關閉原本因為要寫入資料所打開的檔案

`file.Close();`

原本 `using` 結束時會自動觸發該方法

但是這邊我們把大括弧拿到之後

`using` 的結束位置變移動到了方法最後

導致在寫檔案的時候其實還沒有觸發

所以這邊需要手動呼叫 `file.Close();`

接著會發現檔案雖然有成功被建立

但是其內容為為空

這邊就必須提到 `StreamWriter` 的 `WriteAsync()`

並不會立即將資料寫入資料流中

實際寫入檔案是發生在 `FlushAsync()`

跟上面一樣，這邊需要手動 `FlushAsync()`

所以修正完畢後大概是這樣

```
var fileName = @"D:\file.bin";

using var stream = new MemoryStream();
using var writer = new StreamWriter(stream);
await writer.WriteAsync(fileName);
await writer.FlushAsync();

using var file = new FileStream(fileName, FileMode.Create, FileAccess.Write);
stream.WriteTo(file);
file.Close();

await File.ReadAllTextAsync(fileName).Dump();
```

或加上大括弧來觸發 `file.Close();` & `FlushAsync`

```
var fileName = @"D:\file.bin";

using var stream = new MemoryStream();
using (var writer = new StreamWriter(stream))
{
    await writer.WriteAsync(fileName);
};

using (var file = new FileStream(fileName, FileMode.Create, FileAccess.Write))
{
    stream.WriteTo(file);
};

await File.ReadAllTextAsync(fileName).Dump();
```

但上面這段程式會發生 例外 Cannot access a closed Stream

因為大括弧結束時 `StreamWriter` 會一併把變數 stream 釋放

導致雖然依舊可以使用 stream 變數

但其實已經被 dispose

這邊我們可以使用 `leaveOpen:true` 告訴 `StreamWriter` 保持 `Stream` Open

所以就會回到最上方的範例程式碼

```
var fileName = @"D:\file.bin";

using var stream = new MemoryStream();
using (var writer = new StreamWriter(stream, leaveOpen:true))
{
    await writer.WriteAsync(fileName);
};

using (var file = new FileStream(fileName, FileMode.Create, FileAccess.Write))
{
    stream.WriteTo(file);
}

await File.ReadAllTextAsync(fileName).Dump();
```

另外我們也可以直接把 using 移除防止被釋放

反過來說就是要自己呼叫 `Dispose()`

### 補充

```
var fileName = @"D:\file.bin";

var utf8WithoutBom = new UTF8Encoding(false);

using var stream = new MemoryStream();
using (var writer = new StreamWriter(stream, utf8WithoutBom, leaveOpen:true))
{
    await writer.WriteAsync(fileName);
};

using (var file = new FileStream(fileName, FileMode.Create, FileAccess.Write))
{
    stream.WriteTo(file);
}

await File.ReadAllTextAsync(fileName).Dump();
```

## 參照

[using 陳述式 - C# 參考 | Microsoft Learn](https://learn.microsoft.com/zh-tw/dotnet/csharp/language-reference/keywords/using-statement?redirectedfrom=MSDN)

[關於 C# 的 using 陳述式在實務應用上的基本觀念 | The Will Will Web (miniasp.com)](https://blog.miniasp.com/post/2009/10/12/About-CSharp-using-Statement-misunderstanding-on-try-catch-finally)

[Stream 類別 (System.IO) | Microsoft Learn](https://learn.microsoft.com/zh-tw/dotnet/api/system.io.stream?view=net-7.0)

[c# - 使用 StreamWriter 寫入 MemoryStream 傳回空 - 堆棧溢出 (stackoverflow.com)](https://stackoverflow.com/questions/5652993/writing-to-memorystream-with-streamwriter-returns-empty)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- 回首頁

---

*本文章從點部落遷移至 Writerside*
