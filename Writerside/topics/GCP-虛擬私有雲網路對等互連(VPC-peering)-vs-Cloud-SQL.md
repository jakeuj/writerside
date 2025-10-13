# GCP 虛擬私有雲網路對等互連(VPC peering) vs Cloud SQL

> **原文發布日期:** 2024-02-19
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2024/02/19/unable-to-recreate-private-service-access-on-gcp
> **標籤:** 無

---

筆記下誤刪 虛擬私有雲網路對等互連 後的處理

結論

```
gcloud services vpc-peerings update --service=servicenetworking.googleapis.com --ranges=default-ip-range --network=default --project=my-test-project-20240219 --force
```

說明

Cloud SQL 設定私有 IP 時會需要建立 VPC peering 來連線

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/ea03c786-6f71-46c4-8c78-e0c7d6d6269c/1708311279.png.png)

否則好像連 IP 白名單都開不了

但是直接從 Cloud SQL 網路設定重建會失敗

只能用指令來更新

更新後會在 VPC peering 畫面看到原本刪除的 `servicenetworking.googleapis.com`

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/ea03c786-6f71-46c4-8c78-e0c7d6d6269c/1708314114.png.png)

參照

https://stackoverflow.com/a/56743836/4104545

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [CloudSQL](/jakeuj/Tags?qq=CloudSQL)
* [GCP](/jakeuj/Tags?qq=GCP)
* [VPC](/jakeuj/Tags?qq=VPC)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
