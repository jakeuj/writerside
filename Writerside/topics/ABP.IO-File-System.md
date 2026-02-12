# ABP.IO File System

> **原文發布日期:** 2025-04-09
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2025/04/09/Abp-File-System
> **標籤:** 無

---

Get Files from Directory

## Install

```
abp add-package Volo.Abp.BlobStoring.FileSystem
```

## Configure

```
private void ConfigureBlobStoring(IConfiguration configuration)
{
    Configure<AbpBlobStoringOptions>(options =>
    {
        options.Containers.ConfigureDefault(container =>
        {
            container.UseFileSystem(fileSystem =>
            {
                fileSystem.BasePath = configuration["Path"];
            });
        });
        // temp is a container name
        options.Containers.Configure("temp", container =>
            {
                container.UseFileSystem(fileSystem =>
                {
                    fileSystem.BasePath = configuration["BlobOptions:BlobPath"];
                });
            });
    });
}
```

## Usage

```
private readonly IBlobContainer _blobContainer;
private readonly IConfiguration _configuration;

public TestFileSystemAppService(IBlobContainerFactory blobContainerFactory, IConfiguration configuration)
{
    _configuration = configuration;
    _blobContainer = blobContainerFactory.Create("temp");
}

public async Task SaveBytesAsync(byte[] bytes)
{
    await _blobContainer.SaveAsync("my-blob-1", bytes, true);
}

public async Task<byte[]?> GetBytesAsync()
{
    return await _blobContainer.GetAllBytesOrNullAsync("my-blob-1");
}

public async Task SaveStreamAsync(IRemoteStreamContent Content)
{
    await _blobContainer.SaveAsync(Content.FileName ?? "my-blob-2", Content.GetStream(), true);
}

public async Task<IRemoteStreamContent?> GetStreamAsync(string? fileName = "my-blob-2")
{
    if (string.IsNullOrEmpty(fileName))
    {
        throw new ArgumentNullException(nameof(fileName));
    }

    var s = await _blobContainer.GetOrNullAsync(fileName);
    if (s == null)
    {
        throw new NotFoundException();
    }

    return new RemoteStreamContent(s, fileName,
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
}

public async Task SaveDirectoryAsync(IRemoteStreamContent Content)
{
    await _blobContainer.SaveAsync(Path.Combine("DirName", "SubDir", Content.FileName), Content.GetStream(), true);
}

public async Task GetEdisync(string name)
{
    var s = await _blobContainer.GetOrNullAsync(Path.Combine("DirName", "SubDir",name));
    if (s == null)
    {
        throw new NotFoundException();
    }
}

public async Task<IEnumerable<string>> GetDirectoryAsync()
{
    return _blobContainer.GetFileNameList(Path.Combine(_configuration["Path"], "host", "DirName", "SubDir"));
}
```

## GetDirectoryFiles

Retrieve all file names in a folder using the `GetFileNameList` extension method, and then iterate through the list to access the file contents.

### extension

Create a extension method to get file name list from directory.

`public static class NbEdiExtensions`

```
public static List<string> GetFileNameList(
    this IBlobContainer blobContainer,
    string blobPath,
    string? subPath = null)
{
    if (!string.IsNullOrWhiteSpace(subPath))
    {
        blobPath = Path.Combine(blobPath, subPath);
    }

    if (!Directory.Exists(blobPath))
    {
        return new List<string>();
    }

    var di = new DirectoryInfo(blobPath);

    return di.GetFiles().Select(x => x.Name).ToList();
}
```

P.S. You can also add checks for TenantId and UserId to retrieve file lists for different tenants and users.

该方法 `GetFileNameList` 是一个扩展方法，用于从指定的本地文件系统路径中获取文件名列表。它接受三个参数： `IBlobContainer` 接口实例（尽管未在方法中直接使用）、 `blobPath` （文件夹路径）以及可选的子路径 `subPath`。

### 参数处理

首先，方法检查 `subPath` 是否为空或仅包含空白字符：

```
if (!string.IsNullOrWhiteSpace(subPath))
{
    blobPath = Path.Combine(blobPath, subPath);
}
```

如果 `subPath` 有效，则将其与 `blobPath` 合并，生成完整的路径。

### 路径验证

接下来，方法验证合并后的路径是否存在：

```
if (!Directory.Exists(blobPath))
{
    return new List<string>();
}
```

如果路径不存在，则返回一个空的字符串列表，表示没有可用的文件。

### 获取文件名列表

如果路径存在，方法会创建一个 `DirectoryInfo` 实例来表示该目录：

```
var di = new DirectoryInfo(blobPath);
```

然后通过调用 `GetFiles` 方法获取目录中的所有文件，并使用 LINQ 将每个文件的名称提取为字符串列表：

```
return di.GetFiles().Select(x => x.Name).ToList();
```

### 总结

该方法的主要功能是从指定的本地目录中获取文件名列表。它通过路径合并和验证确保了输入路径的有效性，并使用 `DirectoryInfo` 和 LINQ 提供了简洁的文件名提取逻辑。如果路径无效或不存在，则返回空列表。

## Ref

[file-system](https://abp.io/docs/latest/framework/infrastructure/blob-storing/file-system)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- ABP

- 回首頁

---

*本文章從點部落遷移至 Writerside*
