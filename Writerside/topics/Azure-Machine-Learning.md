# Azure Machine Learning

> **原文發布日期:** 2023-07-17
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/07/17/Azure-Machine-Learning-WorkSpace
> **標籤:** 無

---

Azure Machine Learning workspace

前言

此篇為補充方式呈現

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/ad68d565-2d25-4e05-82d3-8cefa1d5b947/1689927481.png.png)

其實主要出入是這篇舊文章是 V1 API

DAY03 建立 Datastore 和 Dataset （上） - 10 上傳資料檔

<https://github.com/dsindy/kaggle-titanic/blob/master/data/train.csv>

DAY04 建立 Datastore 和 Dataset （下）

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/ad68d565-2d25-4e05-82d3-8cefa1d5b947/1689583615.png.png)

## Data types vs. dataset types

### **Data asset types**

The Azure Machine Learning CLI v2 and Python SDK v2 now include the following data types:

* uri\_file (display name: File)
* uri\_folder (display name: Folder)
* mltable (display name: Table)

[Learn more about data asset types **](https://go.microsoft.com/fwlink/?linkid=2194922)

### **Dataset types**

Dataset types from Azure Machine Learning CLI v1 and Python SDK v1 can still be used, but will be mapped to the appropriate data type in the v2 systems:

* file dataset type: maps to Folder type
* tabular dataset type: maps to Table type

[Learn more about dataset types **](https://go.microsoft.com/fwlink/?linkid=2208157)

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/ad68d565-2d25-4e05-82d3-8cefa1d5b947/1689925912.png.png)

Compute

* NV6 (M60) 將於 2023/7/31 棄用

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/ad68d565-2d25-4e05-82d3-8cefa1d5b947/1689583668.png.png)

還有 serverless 可以選，但第一次按了要等三到五分鐘

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/ad68d565-2d25-4e05-82d3-8cefa1d5b947/1689585407.png.png)

看起來是閒置 20 min 釋放

![Expandable diagram that shows scenarios for Apache Spark session inactivity period and cluster teardown.](https://learn.microsoft.com/en-us/azure/machine-learning/media/apache-spark-azure-ml-concepts/spark-session-timeout-teardown.png?view=azureml-api-2#lightbox)

Lib 是用 pyspark，懂 Spark 可以研究一下

[在 Azure Machine Learning 中使用 Apache Spark 進行互動式資料整頓 - Azure Machine Learning | Microsoft Learn](https://learn.microsoft.com/zh-tw/azure/machine-learning/interactive-data-wrangling-with-apache-spark-azure-ml?view=azureml-api-2#import-and-wrangle-data-from-azure-machine-learning-datastore)

NoteBook Sample

```
import pandas as pd

df = pd.read_csv("azureml://subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourcegroups/MLRG/workspaces/TestWorkSpace/datastores/testdata/paths/test.csv")
df.head()
```

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/ad68d565-2d25-4e05-82d3-8cefa1d5b947/1689668278.png.png)

`azureml` 可以從設定好的 DataSet 中取得

Designer

6. select columns: Survived, Pclass, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked

13. 在右邊 asset library 輸入 train model，拖曳到 Canvas 中，用 filter based feature selection 左邊的點點連接到它。 Train model 的右邊方框，在 Label Column 選擇 Survived。(原文為  Survivde)

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/ad68d565-2d25-4e05-82d3-8cefa1d5b947/1689738324.png.png)

DAY08 部署用 Designer 做好的 Pipeline 到 Web API

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/ad68d565-2d25-4e05-82d3-8cefa1d5b947/1689923164.png.png)

`Create inference pipeline` 在 Job 結果裡面

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/ad68d565-2d25-4e05-82d3-8cefa1d5b947/1689929910.png.png)

SDK

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/ad68d565-2d25-4e05-82d3-8cefa1d5b947/1690182402.png.png)

azureml-sdk: This package has been tested with Python 3.7, 3.8, 3.9 and 3.10.

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/ad68d565-2d25-4e05-82d3-8cefa1d5b947/1690185757.png.png)

參照

[[DAY06] 開始用 Notebook 在 Azure Machine Learing 上寫程式 - iT 邦幫忙::一起幫忙解決難題，拯救 IT 人的一天 (ithome.com.tw)](https://ithelp.ithome.com.tw/articles/10269106)

[什麼是 Azure OpenAI 服務？ - Azure AI services | Microsoft Learn](https://learn.microsoft.com/zh-tw/azure/ai-services/openai/overview)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Azure](/jakeuj/Tags?qq=Azure)
* [ML](/jakeuj/Tags?qq=ML)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
