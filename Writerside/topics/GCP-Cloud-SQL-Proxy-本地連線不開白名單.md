# GCP Cloud SQL Proxy 本地連線不開白名單

> **原文發布日期:** 2023-12-08
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/12/08/gcp-cloud-sql-onnect-auth-proxy
> **標籤:** 無

---

筆記下浮動 IP 連 Google Cloud SQL 的代理連線方法

結論

1. 下載 [使用 Cloud SQL Auth 代理连接  |  Cloud SQL for PostgreSQL  |  Google Cloud](https://cloud.google.com/sql/docs/postgres/connect-auth-proxy?hl=zh-cn#install)
2. 驗證 gcloud auth application-default login
3. 執行 ./cloud-sql-proxy.x64.exe --address 0.0.0.0 --port 1234 myproject:myregion:myinstance
4. 連線 127.0.0.1,1234
5. P.S. 加 --address 0.0.0.0 可以用 localhost 連，省略則只能用 127.0.0.1 才連得到哦！

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/bb1646dd-8343-445e-9fef-85e6c4a30d32/1702017271.png.png)

參照

[GCP - Cloud SQL 的連線方式（cloud sql proxy） : Aaron Jen's Blog](https://aaronjen.github.io/2020-08-25-cloud_sql/)

[SQL Server 透過 TCP/IP 遠端連線時如何使用非 1433 埠號 | The Will Will Web (miniasp.com)](https://blog.miniasp.com/post/2009/03/29/How-to-connect-to-SQL-Server-using-non-default-1433-port)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [CloudSQL](/jakeuj/Tags?qq=CloudSQL)
* [GCP](/jakeuj/Tags?qq=GCP)
* [Proxy](/jakeuj/Tags?qq=Proxy)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
