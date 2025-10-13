# ABP.IO WEB應用程式框架 BLOB Storing File System Provider

> **原文發布日期:** 2023-01-13
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/01/13/ABP-BLOB-Storing-File-System-Provider
> **標籤:** 無

---

筆記一下存檔的步驟

## 簡介

ABP 存檔使用兩個部份來達成

1. [BLOB Storing](https://docs.abp.io/zh-Hans/abp/latest/Blob-Storing)
   提供 IBlobContainer 介面來提供存檔的抽象方法
   建議安裝到領域層：讓領域服務可以進行檔案處理
2. [BLOB Storing Provider](https://docs.abp.io/en/abp/latest/Blob-Storing-File-System)
   實作實際要存放的位置
   (目前是安裝到Host專案與TestBase專案)
   ABP框架已經有以下存儲提供程序的實現：
   * File System：將BLOB作為標準檔案儲存在本地文件系統的資料夾中
   * Database：將BLOB存儲在資料庫中
   * Azure：將BLOB存儲在 Azure BLOB storage中
   * Aliyun：將BLOB存儲在Aliyun Storage Service中
   * Minio：將BLOB存儲在MinIO Object storage中
   * Aws：將BLOB存儲在Amazon Simple Storage Service中

### BLOB Storing

參考文檔：[BLOB Storing](https://docs.abp.io/zh-Hans/abp/latest/Blob-Storing)

首先安裝 [Volo.Abp.BlobStoring](https://www.nuget.org/packages/Volo.Abp.BlobStoring) 到 Domain

dotnet add package [Volo.Abp.BlobStoring](https://www.nuget.org/packages/Volo.Abp.BlobStoring)

並添加依賴到模組

DomainModule

`Volo.Abp.BlobStoring[DependsOn(typeof(AbpBlobStoringModule))]`

即可使用 `IBlobContainer` 來寫入或讀取檔案 (實際上還不行)

```
using System.Threading.Tasks;
using Volo.Abp.BlobStoring;
using Volo.Abp.DependencyInjection;

namespace AbpDemo
;

public class MyService : ITransientDependency
{
  private readonly IBlobContainer _blobContainer;

  public MyService(IBlobContainer blobContainer)
  {
    _blobContainer = blobContainer;
  }

  public async Task SaveBytesAsync(byte[] bytes)
  {
    await _blobContainer.SaveAsync("my-blob-1", bytes);
  }

  public async Task<byte[]> GetBytesAsync()
  {
    return await _blobContainer.GetAllBytesOrNullAsync("my-blob-1");
  }
}

```

### [BLOB Storing Provider](https://docs.abp.io/en/abp/latest/Blob-Storing-File-System)

然後安裝存儲提供者到 Host 專案，這裡以檔案系統為例

dotnet add package [Volo.Abp.BlobStoring.FileSystem](https://www.nuget.org/packages/Volo.Abp.BlobStoring.FileSystem)

HostModule

`[DependsOn(typeof(AbpBlobStoringFileSystemModule))]`

並進行服務註冊與設定

```
Configure<AbpBlobStoringOptions>(options =>
{
    options.Containers.ConfigureDefault(container =>
    {
        container.UseFileSystem(fileSystem =>
        {
            fileSystem.BasePath = "C:\\my-files";
        });
    });
});
```

### Testing

測試時需要再把 Provider 裝到測試專案並再設定一次

TestBaseModule

`[DependsOn(typeof(AbpBlobStoringFileSystemModule))]`

然後就可以寫測試並執行應該會看到檔案在指定位置

### 備註

儲存路徑如果以反斜線 / 開頭，會跑到磁碟槽跟目錄

### 參照

[Blob Storing | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Blob-Storing)

[Blob Storing File System | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Blob-Storing-File-System)

[EasyAbp/FileManagement](https://github.com/EasyAbp/FileManagement)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ABP
* C#
{ignore-vars="true"}

* 回首頁

---

*本文章從點部落遷移至 Writerside*
