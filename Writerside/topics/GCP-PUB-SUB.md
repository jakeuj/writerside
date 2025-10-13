# GCP PUB SUB

> **原文發布日期:** 2023-08-22
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/08/22/Google-Cloud-PUB-SUB-IAM
> **標籤:** 無

---

筆記下 IAM

結論

對方應用程式 > 對方服務帳戶 > GCP > Project > 主題 > 權限 > 發布者 (PUB/SUB 發布者)

我方應用程式 > 我方服務帳戶 > GCP > Project > 訂閱 > 權限 > 訂閱者 (PUB/SUB 訂閱者)

P.S. GCP > IAM > 服務帳戶 > Create > Key

流程

我方 POST 我方 PUB 資訊給對方 API (Project:主題)

對方就會將事件發布到我們指定的 PUB/SUB 服務中的主題

我方程式會讀取訂閱(對應主題)來取得對方發布事件的相關資訊來處理

參照

[使用 IAM 控制访问权限  |  Cloud Pub/Sub 文档  |  Google Cloud](https://cloud.google.com/pubsub/docs/access-control?hl=zh-cn)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Cloud](/jakeuj/Tags?qq=Cloud)
* [GCP](/jakeuj/Tags?qq=GCP)
* [Google](/jakeuj/Tags?qq=Google)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
