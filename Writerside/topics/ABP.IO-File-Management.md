# ABP.IO File Management

> **原文發布日期:** 2025-04-09
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2025/04/09/ABP-File-Management
> **標籤:** 無

---

Must have pro license to use this module.

## Configure

```
private void ConfigureBlobStoring(IConfiguration configuration)
{
    Configure<AbpBlobStoringOptions>(options =>
    {
        options.Containers.Configure<FileManagementContainer>(c =>
        {
            c.UseFileSystem(fileSystem =>
            {
                fileSystem.BasePath = configuration["Path"];
            }); // You can use Database or Azure providers also.
        });
    });
}
```

## Usage

```
private readonly IRepository<DirectoryDescriptor> _directoryDescriptorRepository;
private readonly FileManager _fileManager;

public TestFileManagementAppService(IRepository<DirectoryDescriptor> directoryDescriptorRepository,
    FileManager fileManager)
{
    _directoryDescriptorRepository = directoryDescriptorRepository;
    _fileManager = fileManager;
}

public async Task<Guid?> CreateBackupAsync(IRemoteStreamContent Content)
{
    var backup = await _directoryDescriptorRepository.FirstOrDefaultAsync(x =>
        x.Name == "Backup" && x.ParentId == null && x.TenantId == null);
    if (backup == null)
    {
        backup = await _directoryDescriptorRepository.InsertAsync(
            new DirectoryDescriptor(GuidGenerator.Create(), "Backup"),
            true);
    }

    var f = await _fileManager.CreateAsync(Content.FileName, Content.ContentType, Content, backup.Id, null, true);
    return f.DirectoryId;
}
```

### 代码解释

该代码定义了一个名为 `TestFileManagementAppService` 的类，它继承自 `NbEdiAppService` ，并提供了一个方法用于创建备份文件夹并将文件存储到其中。以下是代码的详细解释：

### 构造函数

```
public TestFileManagementAppService(IRepository<DirectoryDescriptor> directoryDescriptorRepository,
    FileManager fileManager)
```

构造函数接收两个依赖项： `IRepository<DirectoryDescriptor>` 和 `FileManager`。

`IRepository<DirectoryDescriptor>` 用于操作 `DirectoryDescriptor` 实体（目录描述符），例如查询或插入目录。

`FileManager` 用于管理文件的创建和存储。

这些依赖项通过依赖注入传递给类，并存储在私有字段 `_directoryDescriptorRepository` 和 `_fileManager` 中。

### `CreateBackupAsync` 方法

```
public async Task<Guid?> CreateBackupAsync(IRemoteStreamContent Content)
```

该方法的目的是在一个名为 "Backup" 的目录中创建备份文件。如果目录不存在，则会先创建该目录。

**查找或创建备份目录**：

```
var backup = await _directoryDescriptorRepository.FirstOrDefaultAsync(x =>
    x.Name == "Backup" && x.ParentId == null && x.TenantId == null);
```

这里通过 `FirstOrDefaultAsync` 方法查询名为 "Backup" 的根目录（`ParentId == null` 且 `TenantId == null` ）。如果目录不存在：

```
backup = await _directoryDescriptorRepository.InsertAsync(
    new DirectoryDescriptor(GuidGenerator.Create(), "Backup"),
    true);
```

使用 `InsertAsync` 方法创建一个新的 `DirectoryDescriptor` 实体，并将其插入到存储库中。

**创建文件**：

```
var f = await _fileManager.CreateAsync(Content.FileName, Content.ContentType, Content, backup.Id, null, true);
```

使用 `FileManager` 的 `CreateAsync` 方法将文件存储到备份目录中。方法参数包括文件名、内容类型、文件内容、目标目录 ID 等。

**返回目录 ID**：

```
return f.DirectoryId;
```

方法返回文件所属目录的 ID（即备份目录的 ID）。

### 总结

该类的主要功能是确保存在一个名为 "Backup" 的目录，并将传入的文件存储到该目录中。通过依赖注入的方式，代码实现了对目录和文件的解耦管理，便于扩展和测试。

## Ref

[file-management](https://abp.io/docs/latest/modules/file-management)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- ABP

- 回首頁

---

*本文章從點部落遷移至 Writerside*
