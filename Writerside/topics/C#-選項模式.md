# C# 選項模式

> **原文發布日期:** 2022-10-21
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/10/21/CSharp-IOptions-appsettings
> **標籤:** 無

---

註冊 ``IOptions<T>`` 繫結 appsettings.json

結論

建立選項類別

```
public class TestOptions
{
    public const string Position = "Position";

    public string Title { get; set; } = String.Empty;
    public int Age { get; set; } = 0;
}
```

appsettings.json

```
"Position": {
    "Title": "Editor",
    "Age": 18
  }
```

ABP Module (原 Startup.cs)

```
public override void ConfigureServices(ServiceConfigurationContext context)
{
    var configuration = context.Services.GetConfiguration();
    // 繫結設定值到選項
    Configure<TestOptions>(configuration.GetSection(TestOptions.Position));
}
```

使用

```
[Fact]
public void Should_Get_Options()
{
    // Arrange
    var options = GetRequiredService<IOptions<TestOptions>>().Value;

    // Act
    var result = options.Age;

    // Assert
    result.ShouldBe(18);
}
```

參照

[ASP.NET Core 中的選項模式 | Microsoft Learn](https://learn.microsoft.com/zh-tw/aspnet/core/fundamentals/configuration/options?view=aspnetcore-6.0#use-ioptionssnapshot-to-read-updated-data)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- C#
{ignore-vars="true"}

- 回首頁

---

*本文章從點部落遷移至 Writerside*
