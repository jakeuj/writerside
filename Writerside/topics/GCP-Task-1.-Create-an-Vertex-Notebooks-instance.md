# GCP Task 1. Create an Vertex Notebooks instance

> **原文發布日期:** 2023-08-24
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/08/24/GCP-Vertex-NoteBook
> **標籤:** 無

---

建立筆記本實例

## BYOS和BYOC

這邊先搬運 [AWS 官方文件](https://aws.amazon.com/cn/blogs/china/on-amazon-sagemaker-from-the-perspective-of-software-philosophy/) 來科普一下兩種方式

1. BYOS：基於預置的機器學習框架來自定義演算法 (內建演算法)
2. BYOC：自定義演算法設計並自己來打包容器鏡像 (自定義演算法)
3. 第三方應用市場（在AWS Marketplace中挑選第三方演算法包，直接在Amazon SageMaker中使用）。

BYOS和BYOC是SageMaker中實際用的最多的兩種選擇。

那如何選擇BYOS和BYOC？

總的來說，**優先看BYOS是否能滿足需求**。

BYOS相對於BYOC要容易，需要遷移到SageMaker的工作量也少。

而選擇BYOC，常見的是如下的情景：

|  |  |
| --- | --- |
| 情景 1 | SageMaker中的內置框架的python及框架版本不是你需要的版本 |
| 情景2 | 你需要一個完全不同於SageMaker的那些內置框架比如paddlepaddle |
| 情景3 | 有些用戶習慣使用基於docker image的容器跑ML，那麼BYOC可能對他們來說比較容易過渡。 |
| 情景4 | 有些用戶代碼分為兩部分：底層基礎平臺級別代碼，上層使用者定製代碼。 底層代碼打包為docker image並push到ECR以BYOC方式跑通。 上層使用者指定docker image為上面打包好的image，然後跑自己的定製代碼。 這樣做的好處是，**代碼管理分離**，不會發生純BYOS方式上層用戶誤修改底層代碼的問題。 |
| 情景5 | BYOC一次性安裝了相關的套件; 如果用到的軟體包並不在SageMaker內置的容器鏡像中，BYOS每次都有安裝軟體包的過程。 |

除了上面這些情景，盡量優先考慮BYOS的方式，它使用方式簡單，學習曲線也相對平緩。

---

## 教學

參照 Google 官方文件

[Build and Deploy Machine Learning Solutions with Vertex AI: Challenge Lab | Google Cloud Skills Boost](https://www.cloudskillsboost.google/focuses/22019?parent=catalog)

Navigate to **Vertex AI** > **Workbench** > **User-Managed Notebooks**.

Click on the **Create Notebook** button on the middle of the screen. Select the following options:

* **Name:** `vertex-ai-challenge`
* **Region:** `filled in at lab start`
* **Zone:** `filled in at lab start`

Click **Continue**.

Select **TensorFlow Enterprise 2.11** as the Environment.

Select **Use a previous version**. In the **Version** dropdown, select `tf-2-11-cu113-notebooks-v20230615-debian-11-py310 (M109)`. Click **Continue**.

Select **e2-standard-4** as the Machine Type. Click **Create**.

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/3a778f3c-4c62-43cc-8a9b-12b589313749/1692868790.png.png)

## 建立 Instance

### 類型

* **執行個體(預覽版)：預設值，**環境可以指定特定版本(舊版)，但我當下是跑不出來(愛的魔力轉圈圈)
  將代管式筆記本實例的面向工作流的集成與使用者管理的筆記本實例的自定義功能相結合的選項。
* **代管型(舊版)：可以通過提供您自己的自訂 Docker 映像來創建和存取更多的自定義 Jupyter 內核。 系統將導入該容器上的所有可用 Jupyter 內核。**
* **使用者管理筆記本(舊版)：按照**教學文件，這邊應該選擇此種類

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/3a778f3c-4c62-43cc-8a9b-12b589313749/1692869032.png.png)

環境

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/3a778f3c-4c62-43cc-8a9b-12b589313749/1692873374.png.png)

規格

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/3a778f3c-4c62-43cc-8a9b-12b589313749/1692873613.png.png)

價格

[VM 執行個體定價  |  Compute Engine 說明文件  |  Google Cloud](https://cloud.google.com/compute/vm-instance-pricing?hl=zh-tw#e2_predefined)

N1標準4 = $0.22/H (預設)

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/3a778f3c-4c62-43cc-8a9b-12b589313749/1693898885.png.png)

E2標準4=$0.15/H (本教程)

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/3a778f3c-4c62-43cc-8a9b-12b589313749/1693898911.png.png)

創建後可以開始使用 Notebooks

---

參照

[Google Cloud Vertex AI | 御用小本本 - 點部落 (dotblogs.com.tw)](https://www.dotblogs.com.tw/jakeuj/2023/08/21/Google-Cloud-Vertex-AI)

[Build and Deploy Machine Learning Solutions with Vertex AI: Challenge Lab | Google Cloud Skills Boost](https://www.cloudskillsboost.google/focuses/22019?parent=catalog)

[從軟體哲學角度談Amazon SageMaker | 亞馬遜AWS官方博客](https://aws.amazon.com/cn/blogs/china/on-amazon-sagemaker-from-the-perspective-of-software-philosophy/)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* AI
* GCP
* Google

* 回首頁

---

*本文章從點部落遷移至 Writerside*
