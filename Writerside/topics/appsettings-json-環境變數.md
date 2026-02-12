# appsettings.json 與環境變數載入重點

## 1️⃣ ASP.NET Core 環境設定原理

ASP.NET Core 會依據環境變數 `ASPNETCORE_ENVIRONMENT` 的值載入對應的設定檔：

```
appsettings.json  
appsettings.{EnvironmentName}.json
```

例如：

```bash
setx ASPNETCORE_ENVIRONMENT "Testing"
```

則系統會嘗試載入 `appsettings.Testing.json`。

---

## 2️⃣ Program.cs 設定範例

確保載入邏輯中包含環境設定：

```c#
var builder = WebApplication.CreateBuilder(args);

builder.Configuration
    .SetBasePath(Directory.GetCurrentDirectory())
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
    .AddJsonFile($"appsettings.{builder.Environment.EnvironmentName}.json", optional: true, reloadOnChange: true)
    .AddEnvironmentVariables();
```

---

## 3️⃣ 為什麼會讀不到 appsettings.Testing.json

原因通常有：

1. 沒設定 `ASPNETCORE_ENVIRONMENT=Testing`
2. `Program.cs` 沒有 `.AddJsonFile(...)` 的載入邏輯
3. 檔案名稱或大小寫不一致（Linux 部署特別要注意）
4. 檔案沒被包含進輸出（未正確標記為 Content）

---

## 4️⃣ .csproj 設定差異說明

### 原本寫法（可能無效）

```xml
<Content Update="appsettings.Testing.json">
  <CopyToOutputDirectory>Always</CopyToOutputDirectory>
</Content>
```

`Update` 只會修改已存在的項目，但 `appsettings.Testing.json` 不一定被自動識別，因此可能沒效果。

### 改成這樣就能正常載入

```xml
<None Remove="appsettings.Testing.json" />
<Content Include="appsettings.Testing.json">
  <CopyToOutputDirectory>Always</CopyToOutputDirectory>
  <CopyToPublishDirectory>PreserveNewest</CopyToPublishDirectory>
</Content>
```

這樣可以確保該檔案確實被編入輸出。

---

## ✅ 建議最終穩定寫法

```xml
<ItemGroup>
  <None Remove="appsettings.*.json" />
  <Content Include="appsettings.*.json">
    <CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>
    <CopyToPublishDirectory>PreserveNewest</CopyToPublishDirectory>
  </Content>
</ItemGroup>
```

這樣所有環境設定檔都會正確被複製與發佈，避免遺漏。
