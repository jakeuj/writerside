# Install 8.1

Start typing here...

## 需求

* [Rider](https://www.jetbrains.com/rider/download/#section=windows) / Visual Studio 2022 (v17.3+) for Windows / Visual Studio for Mac. 1
* [.NET 8.0+](https://dotnet.microsoft.com/zh-tw/download/dotnet/8.0)
* [Node](Node-js.md) v16 or v18
* [Yarn v1.20+](https://classic.yarnpkg.com/lang/en/docs/install/#windows-stable) (not v2) 2 or npm v6+ (already installed with Node)
* [Redis](Redis.md) (as the distributed cache).

## 安裝

```Shell
dotnet tool install -g Volo.Abp.Cli
abp login <username>
abp suite install
abp suite
```

![suite.png](suite.png)