# GCP Vertex AI

> **原文發布日期:** 2023-08-21
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/08/21/Google-Cloud-Vertex-AI
> **標籤:** 無

---

筆記下 Google Machine Learning 的那些事

筆記一下

AutoML 訓練用於分類/迴歸的每節點時數價格 $21.252 美元

[定價  |  Vertex AI  |  Google Cloud](https://cloud.google.com/vertex-ai/pricing?hl=zh-tw#tabular-data)

流程

<https://console.cloud.google.com/>

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1692602056.png.png)

啟用 API

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1692603583.png.png)

新建資料集

這邊會定義資料集名稱與種類，並可以直接從這邊選本機檔案上傳到 Storage

※ 反過來可以先把資料上傳到 Storage 再來這裡直接設定資料集來源 from Storage

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1692603639.png.png)

DataSet

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1692603683.png.png)

上傳資料

<https://github.com/dsindy/kaggle-titanic/blob/master/data/train.csv>

※ 這份資料只有八百多筆，Azure可以用，GCP說要一千筆以上資料才能跑

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1692603767.png.png)

Storage

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1692604484.png.png)

新建 Storage

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1692604348.png.png)

主畫面會有最近的資料

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1692604921.png.png)

在資料集內可以訓練新模型

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1692609909.png.png)

AutoML

目標這邊要改回歸

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1692611916.png.png)

選擇欄位

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1692612185.png.png)

提交

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1692612317.png.png)

結果

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1692612421.png.png)

成功畫面

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1692958867.png.png)

pipelines

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1692612678.png.png)

跑完之後可以到模型園地

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1693210351.png.png)

我的模型中找到剛剛(兩個多小時)訓練好的模型

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1693210327.png.png)

點進去可以看參數

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1693210580.png.png)

Deploy

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1693210638.png.png)

Endpoint

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1693210802.png.png)

Spec

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1693210899.png.png)

模型監控

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1693211029.png.png)

監控目標

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1693211071.png.png)

也可以關閉監控直接部署

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1693211166.png.png)

Rest

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1693213065.png.png)

## Batch

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1693213137.png.png)

最後可以在線上預測中找到端點

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1693213264.png.png)

## 注意

線上預測端點一但部署就會開始算錢(因為要起一台機器隨時提供Rest API)

練習完千萬記得刪除端點(要先到端點裡面取消模型註冊方可刪除)

## Error

資料少於1000筆會失敗

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/2f488a4a-3cd3-47c0-b0b3-c442defc5a3a/1692669438.png.png)

`Invalid CSV file: 'utf-8' codec can't decode byte 0xad in position 129: invalid start byte`

上傳資料遇到錯誤，看了一下手上是 Big5，我改成 UTF8 後可以正常分析統計資料，但訓練會失敗，最後改成UTF8BOM。

1. 資料筆數最少要1000筆以上。
2. 權重欄位不重複值不能超過10000筆以上。
3. 欄位名稱無法解析(每個欄位開頭要用英文字母，『-』、『?』、『:』和中文好像有問題)。

`Required column(s) not included in the provided schema: ['A', 'B', 'C']`

我最終重建 DataSet 來重跑 AutoML 之後就成功了

猜測一開始建立 DataSet 時的欄位就已經固定了，後續改 csv 欄位會導致錯誤？

## 參照

[介紹Vertex(1) | ML#Day18 - iT 邦幫忙::一起幫忙解決難題，拯救 IT 人的一天 (ithome.com.tw)](https://ithelp.ithome.com.tw/articles/10261465)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- ML
- GCP

- 回首頁

---

*本文章從點部落遷移至 Writerside*
