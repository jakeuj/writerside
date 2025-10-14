# Windows Docker TensorFlow GPU

> **原文發布日期:** 2024-01-29
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2024/01/29/ml-tensorflow-windows-gpu
> **標籤:** 無

---

筆記下目前抓寶的心得感想

## 重點

1. TensorFlow 2.10 是**最後一個**原生 Windows 上支援 GPU 的 TensorFlow 版本 。
   從 TensorFlow 2.11 開始，您需要[在 WSL2 中安裝 TensorFlow](https://tensorflow.org/install/pip#windows-wsl2)， 或安裝或嘗試 [TensorFlow-DirectML-Plugin](https://github.com/microsoft/tensorflow-directml-plugin#tensorflow-directml-plugin-)
   [Install TensorFlow with pip](https://www.tensorflow.org/install/pip#windows-native)
2. [TensorFlow Docker 鏡像](https://hub.docker.com/r/tensorflow/tensorflow/)
   已配置為運行 TensorFlow。Docker 容器在 虛擬環境，是設置 GPU 支援的最簡單方法。
   [安裝 TensorFlow 2](https://www.tensorflow.org/install)
3. 利用 Docker 可以用到目前最新 tensorflow 2.15 版本
4. 記得執行 docker run 時增加選項 `--gpus all` 否則會顯示 0 GPU 哦！

## 前提

* 安裝最新 Nvidia 顯卡驅動
  Docker 只需要 Host 裝好顯卡驅動即可
* Windows 更新到最新版本
  某一版更新後 WSL 才支援 CUDA

## 結論

`Dockerfile`

```
FROM tensorflow/tensorflow:latest-gpu

RUN python3 -m pip install --upgrade pip

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

CMD python main.py
```

`main.py`

```
import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
```

`--gpus all`

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/e655befd-00ba-426f-a1bd-b5172f7ce3c1/1706510625.png.png)

Output:

```
Num GPUs Available:  1
```

其中 `main.py` 可以替換成訓練用的 script

```
import tensorflow as tf
# 訓練程式碼...
```

另外 `requirements.txt` 裡面不需要 `tensorflow<2.11`

## 說明

1. 安裝 [Docker Desktop: The #1 Containerization Tool for Developers | Docker](https://www.docker.com/products/docker-desktop/)
2. 安裝 [Windows Subsystem for Linux - Microsoft 應用程式](https://apps.microsoft.com/detail/9P9TQF7MRM4R?hl=zh-tw&gl=US)
3. 安裝 [Ubuntu - Microsoft Apps](https://apps.microsoft.com/detail/9PDXGNCFSCZV?ocid=pdpshare&hl=en-us&gl=US)
4. 建立 [Dockerfile](https://docs.docker.com/engine/reference/builder/)
5. docker build
6. docker run --gpus all

Dockerfile

```
FROM tensorflow/tensorflow:latest-gpu

CMD python -c "import tensorflow as tf; print('Num GPUs Available: ', len(tf.config.list_physical_devices('GPU')))"
```

docker build & run

```
docker build -t foo . && docker run --gpus all -it foo
```

Output:

`Num GPUs Available:  1`

備註

* NoteBook 有內顯要切獨顯來跑
* 獨顯有省電模式要切慣用最大效能 P0 來跑
* 可以指定掛載檔案路徑讓 Model 輸出時可以在外頭直接拿到新的檔案
  例如輸出到 /output 並直接由 D:\models 看到輸出的模型 \*.h5
  docker run -v D:\models:/output

參照

[Install TensorFlow 2](https://www.tensorflow.org/install)

參考來源

[How to Deploy GPU-Accelerated Applications on Amazon ECS with Docker Compose | Docker](https://www.docker.com/blog/deploy-gpu-accelerated-applications-on-amazon-ecs-with-docker-compose/)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Docker
* ML

* 回首頁

---

*本文章從點部落遷移至 Writerside*
