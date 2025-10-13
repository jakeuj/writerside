# ABP.IO WEB應用程式框架 Swagger Default Value

> **原文發布日期:** 2022-09-30
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/09/30/abp-Swagger-Default-Value
> **標籤:** 無

---

筆記下 Swagger Input 提供 預設值 的方法

## 參照

[Get started with Swashbuckle and ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/tutorials/getting-started-with-swashbuckle?view=aspnetcore-6.0&tabs=visual-studio-code#xml-comments)

### 產生 xml

YourProject.Application.Contracts.csproj

```
<PropertyGroup>
   <GenerateDocumentationFile>true</GenerateDocumentationFile>
</PropertyGroup>
```

### 設定 Swagger

YourProject.HttpApi.Host/YourProjectHttpApiHostModule.cs => ConfigureServices => ConfigureSwaggerServices

```
options =>
{
   // using System.Reflection;
   var xmlFilename = "YourProject.Application.Contracts.xml";
   options.IncludeXmlComments(Path.Combine(AppContext.BaseDirectory, xmlFilename));
});
```

### 加上預設值

YourProject.Application.Contracts/YourDto.cs

```
[DefaultValue("HelloWorld")]
public string Message { get; set; }

[DefaultValue(new string[] { "a", "b" })]
public List<string> Users { get; set; }
```

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/3d8e3847-8620-45cf-8a75-bc0f7cf98713/1669104103.png.png)
![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Swagger](/jakeuj/Tags?qq=Swagger)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
