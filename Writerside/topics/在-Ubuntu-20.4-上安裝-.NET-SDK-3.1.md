# 在 Ubuntu 20.4 上安裝 .NET SDK 3.1

> **原文發布日期:** 2021-04-22
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/04/22/UbuntuDotNetCore
> **標籤:** 無

---

原本都用 CentOS

筆記一下 Ubuntu 安裝 DotNet Core 3.1 SDK

其實官方文件也是挺清楚的

<https://docs.microsoft.com/zh-tw/dotnet/core/install/linux-ubuntu#2004->

總之直接下 install 會說找不到這套件

1.要先乖乖按照文件先執行以下命令

```
wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
```

將 Microsoft 套件簽署金鑰新增至您的受信賴起點清單，並新增套件存放庫。

2. 安裝 .NET SDK

```
sudo apt-get update; \
  sudo apt-get install -y apt-transport-https && \
  sudo apt-get update && \
  sudo apt-get install -y dotnet-sdk-3.1
```

版本目前支援 2.1、3.1、5.0

3. 確認版本

```
dotnet --info
```

> .NET Core SDK (reflecting any global.json):
> Version:   3.1.408
> Commit:    88530ea5c9
>
> Runtime Environment:
> OS Name:     ubuntu
> OS Version:  20.04
> OS Platform: Linux
> RID:         ubuntu.20.04-x64
> Base Path:   /usr/share/dotnet/sdk/3.1.408/
>
> Host (useful for support):
>  Version: 3.1.14
>  Commit:  826c2c2f8f
>
> .NET Core SDKs installed:
>  3.1.408 [/usr/share/dotnet/sdk]
>
> .NET Core runtimes installed:
>  Microsoft.AspNetCore.App 3.1.14 [/usr/share/dotnet/shared/Microsoft.AspNetCore.App]
>  Microsoft.NETCore.App 3.1.14 [/usr/share/dotnet/shared/Microsoft.NETCore.App]
>
> To install additional .NET Core runtimes or SDKs:
>  https://aka.ms/dotnet-download

4. 建置

`dotnet publish -c:Release -o ./publish`

5. Zip

`apt-get install zip unzip`

`zip -r webplusdemo.zip ./publish/`

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* .Net Core
{ignore-vars="true"}
* Linux
* Ubuntu

* 回首頁

---

*本文章從點部落遷移至 Writerside*
