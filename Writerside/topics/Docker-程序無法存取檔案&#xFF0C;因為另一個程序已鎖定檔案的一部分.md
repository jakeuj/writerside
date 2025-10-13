# Docker 程序無法存取檔案&#xFF0C;因為另一個程序已鎖定檔案的一部分

> **原文發布日期:** 2024-03-07
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2024/03/07/docker-java-io-IOException
> **標籤:** 無

---

Preparing build context archive…

Failed to deploy

`java.io.IOException: 程序無法存取檔案，因為另一個程序已鎖定檔案的一部分。`

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/42fe5267-9c55-4c3d-80c5-1786f903b25b/1709797808.png.png)

結論

將 Context folder 設為專案路徑 (等同於不設定 Context folder)

原因

Rider 直接執行專案內的 dockerfile 時，會把 Context folder 設為方案路徑 (也就是專案的上一層目錄)，導致路徑錯誤

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/42fe5267-9c55-4c3d-80c5-1786f903b25b/1709796319.png.png)

錯誤訊息

```
Deploying '<unknown> Dockerfile: Platform/Dockerfile'…
Building image…
Preparing build context archive…
[====>                                              ]15/159 files
Failed to deploy '<unknown> Dockerfile: Platform/Dockerfile': java.io.IOException: 程序無法存取檔案，因為另一個程序已鎖定檔案的一部分。
```

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Rider

* 回首頁

---

*本文章從點部落遷移至 Writerside*
