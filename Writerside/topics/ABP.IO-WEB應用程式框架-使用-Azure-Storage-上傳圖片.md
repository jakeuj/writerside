# ABP.IO WEB應用程式框架 使用 Azure Storage 上傳圖片

> **原文發布日期:** 2021-10-29
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/10/29/Abp-Blob-Storing-Azure
> **標籤:** 無

---

筆記下 ABP Storage 用法與上傳圖片相關資訊

## Blob Storing Azure

首先參照官方文件安裝並設定 Azure Storage

[Blob Storing Azure | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/5.0/Blob-Storing-Azure)

我是把 `volo.abp.blobstoring.azure` 套件裝在 Domain 層

然後把 Azure Storage 連接字串設定在 HttpApi.Host (Web)

## Save

基本用法請參考以下文件

[Blob Storing | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/5.0/Blob-Storing)

## 範例

SaveImagesAsync (Application)

```
public async Task SaveImageAsync([FromForm]SaveImageDto input)
{
    var fromFile = input.FormFile;
    await using var stream = fromFile.OpenReadStream();
    await _blobContainer.SaveAsync(fromFile.FileName, stream);
}
```

* 如果不是直接輸入 IFormFile 則要記得加 `[FromForm]`
* `SaveAsync` 可以輸入 stream
* `OpenReadStream` 記得 using 不然可能要自己 close ?

SaveImageDto (Application.Contracts)

```
public class SaveImageDto : IValidatableObject
{
    [Required]
    public IFormFile FormFile { get; set; }

    public IEnumerable<ValidationResult> Validate(ValidationContext validationContext)
    {
        if (!StorageHelper.IsImage(FormFile))
        {
            yield return new ValidationResult(
                "Extension must be .jpg, .png, .gif, .jpeg!",
                new[] { "FormFile" }
            );
        }
    }
}
```

* `IValidatableObject` 會自動驗證輸入資料，需實作 Validate
  [Validation | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Validation#ivalidatableobject)
* `ValidationResult` 第一個參數是 message，可以自己調整
* `StorageHelper` 這個類要自己建出來，如下所示

Application.Contracts.Helpers.StorageHelper.cs

```
public static bool IsImage(IFormFile file)
{
  if (file.ContentType.Contains("image"))
  {
     return true;
  }

  string[] formats = new string[] { ".jpg", ".png", ".gif", ".jpeg" };

  return formats.Any(item => file.FileName.EndsWith(item, StringComparison.OrdinalIgnoreCase));
}
```

* 檢查 `ContentType` 或是副檔名是否合乎規定
* 如果不要 .gif 可以自己從 `formats` 拿掉

[storage-blob-upload-from-webapp/StorageHelper.cs at master · Azure-Samples/storage-blob-upload-from-webapp (github.com)](https://github.com/Azure-Samples/storage-blob-upload-from-webapp/blob/master/ImageResizeWebApp/ImageResizeWebApp/Helpers/StorageHelper.cs#L17)

## Get

```
public async Task<IRemoteStreamContent> GetImageAsync(string name)
{
    var fs = await _blobContainer.GetAsync(name);
    fs.Position = 0;
    if (!_contentTypeProvider.TryGetContentType(name, out var contentType))
    {
        contentType = "application/octet-stream";
    }
    return new RemoteStreamContent(fs,name,contentType);
}
```

* `fs.Position = 0;` => 不加這行會不能下載，是不是 Bug 我不知道，但絕對是個坑！
  [How to user IRemoteStreamContent with BLOB Storing Azure Provider · Issue #7418 · abpframework/abp (github.com)](https://github.com/abpframework/abp/issues/7418)
* `IContentTypeProvider` => 這邊DI `FileExtensionContentTypeProvider` 來判斷 ContentType

```
public class YourProjectApplicationModule : AbpModule
{
    public override void ConfigureServices(ServiceConfigurationContext context)
    {
        context.Services.AddSingleton<IContentTypeProvider, FileExtensionContentTypeProvider>();
    }
}
```

如果不管 ContentType 那就改成以下這樣也就不用設定 DI 了

`return new RemoteStreamContent(fs,name,"application/octet-stream");`

參照

[Application Services | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/5.0/Application-Services#working-with-streams)

[File Upload/Download with BLOB Storage System in ASP.NET Core & ABP Framework | ABP Community](https://community.abp.io/articles/file-uploaddownload-with-blob-storage-system-in-asp.net-core-abp-framework-d01cbe12)

## 備註

如果無法儲存可能要去 Azure 手動建立 container

名稱需與設定一致 `azure.ContainerName = "your azure container name";`

## 單元測試

剛測試發現整合測試其他 API 過不了

到 TestBase 設定 DI 可以先正常測試

test\YourProject.TestBase.YourProjectTestBaseModule.cs

```
public override void ConfigureServices(ServiceConfigurationContext context)
{
    Configure<AbpBlobStoringOptions>(options =>
    {
        options.Containers.ConfigureDefault(container =>
        {
            container.UseAzure(azure =>
            {
                azure.ConnectionString = "your azure connection string";
                azure.ContainerName = "your azure container name";
                azure.CreateContainerIfNotExists = true;
            });
        });
    });
}
```

// TODO: context.Services.Replace(ServiceDescriptor.Singleton<IBlobContainer, NullBlobContainer>());

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ABP

* 回首頁

---

*本文章從點部落遷移至 Writerside*
