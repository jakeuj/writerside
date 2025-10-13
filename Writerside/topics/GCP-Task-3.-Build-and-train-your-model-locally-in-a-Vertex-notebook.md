# GCP Task 3. Build and train your model locally in a Vertex notebook

> **原文發布日期:** 2023-09-05
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/09/05/GCP-Build-and-train-your-model-locally-in-a-Vertex-notebook
> **標籤:** 無

---

訓練 Model

## 摘要

In this section, you will train your model locally using TensorFlow.

**Note:** This lab adapts and extends the official [TensorFlow BERT text classification tutorial](https://www.tensorflow.org/text/tutorials/classify_text_with_bert) to utilize Vertex AI services.

See the tutorial for additional coverage on fine-tuning BERT models using TensorFlow.

### Build and compile a TensorFlow BERT sentiment classifier

1. Fill out the `#TODO` section to add a `hub.KerasLayer` for BERT text preprocessing.
2. Fill out the `#TODO` section to add a `hub.KerasLayer` for BERT text encoding.
3. Fill out the `#TODO` section to save your BERT sentiment classifier locally.
   You should save it to the `./bert-sentiment-classifier-local` directory.

## 實作

1. Fill out the `#TODO` section to add a `hub.KerasLayer` for BERT text preprocessing.

※ 這邊要搜尋 `# TODO` 而不是 `#TODO` 否則會找不到正確位置 (我這邊是找 `TODO`)

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/c999bdd2-9d06-4929-93db-3e4a12333a0b/1693901944.png.png)

參照

[Build and Deploy Machine Learning Solutions with Vertex AI: Challenge Lab | Google Cloud Skills Boost](https://www.cloudskillsboost.google/focuses/22019?parent=catalog)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [GCP](/jakeuj/Tags?qq=GCP)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
