# GCP 部屬 VUE

> **原文發布日期:** 2023-09-22
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/09/22/GCP-App-Engine-VUE
> **標籤:** 無

---

Deploy VUE 到 App Engine

GCP 建立 App Engine 選 Node.js

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/a5357981-8b70-44e5-8315-ebbff5ca01e7/1695364843.png.png)

app.yaml

```
runtime: nodejs20
handlers:
  # Serve all static files with urls ending with a file extension
  - url: /(.*\..+)$
    static_files: dist/\1
    upload: dist/(.*\..+)$
    # catch all handler to index.html
  - url: /.*
    static_files: dist/index.html
    upload: dist/index.html
```

將 dist 與 app.yaml 放一起

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/a5357981-8b70-44e5-8315-ebbff5ca01e7/1695365682.png.png)

執行 `gcloud app deploy`

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/a5357981-8b70-44e5-8315-ebbff5ca01e7/1695365979.png.png)

`gcloud app browse`

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/a5357981-8b70-44e5-8315-ebbff5ca01e7/1695366091.png.png)

參照

[到部署網站才開始從頭學起 - iT 邦幫忙::一起幫忙解決難題，拯救 IT 人的一天 (ithome.com.tw)](https://ithelp.ithome.com.tw/articles/10213655)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Vue](/jakeuj/Tags?qq=Vue)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
