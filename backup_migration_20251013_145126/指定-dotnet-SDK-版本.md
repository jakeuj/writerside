# 指定 dotnet SDK 版本

最近裝了 .NET 9.0，但專案是 .NET 8，所以想要指定 .NET SDK 版本

## global.json
Rider 設定方式
```mermaid
graph LR
A[Rider] -->B(Solution)
    B -->  |右鍵| C(管理 .NET SDK...)
    C -->  |.NET SDK| D(8.0)
    C -->  |前滾策略| E(latestMajor)
```
![sdk.png](sdk.png)
![latest.png](latest.png)
## REF
[使用 global.json 精準的選擇 .NET SDK 版本](https://blog.miniasp.com/post/2021/06/04/Choose-the-right-DotNet-SDK-version-using-global-json)