# ABP

ASP.NET Boilerplate Project


## 需求

* [Rider](https://www.jetbrains.com/rider/download/#section=windows) / Visual Studio 2022 (v17.3+) for Windows / Visual Studio for Mac. 1
* [.NET 8.0+](https://dotnet.microsoft.com/zh-tw/download/dotnet/8.0)
* [Node](Node-js.md) v16 or v18
* [Yarn v1.20+](https://classic.yarnpkg.com/lang/en/docs/install/#windows-stable) (not v2) 2 or npm v6+ (already installed with Node)
* [Redis](Redis.md) (as the distributed cache).

### Redis
用 Studio 建立專案會自動使用 Docker 執行 Redis 並建立 network

### LocalDB
用 Studio 建立專案會自動使用 LocalDB，理論上 VS 2022 會自動安裝 LocalDB，但如果沒有安裝的話可以參考以下連結安裝

[下載MSSQL-Express安裝LocalDB](https://blog.miniasp.com/post/2020/02/16/install-and-upgrade-sql-server-express-localdb)

安裝後如果無法正常訪問或啟動 LocalDB

1. 移除 LocalDB 執行個體
  ```shell
  sqllocaldb stop mssqllocaldb
  sqllocaldb delete mssqllocaldb
  ```
2. 再重新建立 LocalDB 執行個體
  ```shell
  sqllocaldb create mssqllocaldb
  ```


## 安裝
目前正值改版，目前版本 Suite 裡面會建議去使用 Studio，但實際上 Studio 目前則是測試版本...

目前官方教學是說先用 Studio，如果有問題則改用 Cli

姑且就先照官方文件用 Studio，目前使用上是不用 key 指令

- 8.1 以下
  - 免費版：[Cli](Cli.md)
  - 付費版：[Suite](Install-8-1.md)
- 8.2 以上：[Studio](Studio.md)

