# GCE 安裝 Nvidia Driver 

> **原文發布日期:** 2023-09-19
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/09/19/GCE-Nvidia-Driver
> **標籤:** 無

---

筆記下

目前

[使用 GPU 加速器运行实例  |  Container-Optimized OS  |  Google Cloud](https://cloud.google.com/container-optimized-os/docs/how-to/run-gpus?hl=zh-cn#shell)

可用版本

```
sudo cos-extensions list
```

output

```
jakeuj@instance-1 ~ $ sudo cos-extensions list
Available extensions for COS version 101-17162.279.42:

[gpu]
gpu installer: asia.gcr.io/cos-cloud/cos-gpu-installer:v2.1.7
470.199.02 [default]
525.125.06
535.104.05 [latest]
```

備註

* Driver Version: 470.199.02 CUDA Version: 11.4
* Driver Version: 525.125.06   CUDA Version: 12.0
* Driver Version: 535.104.05   CUDA Version: 12.2

安裝

```
#! /bin/bash

sudo cos-extensions install gpu -- -version=535.104.05
```

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/5d0ae565-dc84-4577-b4f5-912cbfa8a332/1695181968.png.png)

驗證安裝

```
# Make the driver installation path executable by re-mounting it.
sudo mount --bind /var/lib/nvidia /var/lib/nvidia
sudo mount -o remount,exec /var/lib/nvidia
/var/lib/nvidia/bin/nvidia-smi
```

output

```
jakeuj@instance-2 ~ $ sudo mount --bind /var/lib/nvidia /var/lib/nvidia
jakeuj@instance-2 ~ $ sudo mount -o remount,exec /var/lib/nvidia
jakeuj@instance-2 ~ $ /var/lib/nvidia/bin/nvidia-smi
Wed Sep 20 03:55:31 2023
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.104.05             Driver Version: 535.104.05   CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  NVIDIA L4                      On  | 00000000:00:03.0 Off |                    0 |
| N/A   53C    P8              13W /  72W |      4MiB / 23034MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+

+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|  No running processes found                                                           |
+---------------------------------------------------------------------------------------+
jakeuj@instance-2 ~ $
```

參照

[Install GPU drivers  |  Compute Engine Documentation  |  Google Cloud](https://cloud.google.com/compute/docs/gpus/install-drivers-gpu)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [LLM](/jakeuj/Tags?qq=LLM)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
