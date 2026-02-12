# Directory.Packages.props

`Directory.Packages.props` 是 .NET 的一個功能檔案，主要用於集中管理專案中共用的 NuGet 套件版本。

從 .NET 6 開始，這種集中管理的方式被稱為 **Central Package Management (CPM)**，目的是減少各個專案檔案重複定義套件版本的麻煩，讓版本管理更容易一致化。

## 說明

- `Directory.Packages.props` 中央包管理檔內主要定義 **PackageVersion** 來指定版本資訊

- `.csproj` 專案檔內則是定義 **PackageReference** 來引用套件

※ 如果在 `Directory.Packages.props` 寫了 PackageReference 會造成全專案都會引用此包進而造成錯誤

### 基本功能

1. **集中管理 NuGet 套件版本：**  
   在 `Directory.Packages.props` 中定義套件的版本，所有子專案都可以直接引用而不需要再指定版本。

2. **子專案中簡化引用：**  
   子專案只需使用 `<PackageReference Include="PackageName" />` 即可，不需要指定版本。

3. **版本控制一致性：**  
   所有專案使用的套件版本由一個檔案管理，避免版本衝突。

---

### `Directory.Packages.props` 文件的結構範例

```xml
<Project>
  <ItemGroup>
    <!-- 定義共用的套件版本 -->
    <PackageVersion Include="Newtonsoft.Json" Version="13.0.1" />
    <PackageVersion Include="Serilog" Version="2.12.0" />
    <PackageVersion Include="Dapper" Version="2.0.123" />
  </ItemGroup>
</Project>
```

### 子專案的引用方式

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <ItemGroup>
    <!-- 引用套件但不需要指定版本 -->
    <PackageReference Include="Newtonsoft.Json" />
    <PackageReference Include="Serilog" />
  </ItemGroup>
</Project>
```

---

### 如何啟用 Central Package Management

1. 在解決方案的根目錄新增 `Directory.Packages.props` 文件。
2. 在子專案中，刪除原有的版本號，改為使用集中管理。

### 注意事項

1. **支援範圍：**  
   Central Package Management 支援的是以 .NET SDK 為基礎的專案格式（即 `*.csproj` 使用 `<Project Sdk="Microsoft.NET.Sdk">` 的專案）。

2. **優先級：**  
   如果某個專案需要覆寫集中管理的版本，可以在該專案檔案中直接指定版本號，此時會以專案檔案的版本為主。

---

透過使用 `Directory.Packages.props`，可以顯著提高專案的可維護性和版本控制的效率，是 .NET 開發中很實用的工具之一。
