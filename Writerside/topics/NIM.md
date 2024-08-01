# NIM

[NVIDIA NIM](https://www.nvidia.com/zh-tw/ai/) 是一組易於使用的微服務，旨在加速企業的生成式 AI 部署。
它支持多種 AI 模型，包括 NVIDIA AI 基礎模型和自定義模型，提供無縫、可擴展的 AI 推論功能，無論是在本地環境還是在雲端環境。

NVIDIA NIM 也提供了預建的容器，方便使用者快速部署大型語言模型（LLMs），例如聊天機器人、內容分析器等應用。
每個 NIM 都包含一個容器和一個模型，使用 CUDA 加速的執行環境，對 NVIDIA GPU 提供特殊優化。

特別提到的是，NVIDIA NIM 支持 Llama 3.1 8B-Instruct 模型，
這是一種優化的語言理解、推理和文本生成用途的模型，超越了許多開源聊天機器人的業界基準。

## 需求
參照：[prerequisites](https://docs.nvidia.com/nim/large-language-models/latest/getting-started.html#prerequisites)

- NVIDIA GPU
- CPU: x86_64
- OS: any Linux distributions
- NVIDIA GPU 相容的 CUDA 驅動程式 (不需要 CUDA toolkit 因為 container 已經包含)：[cuda-installation-guide-linux](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/)
- [Docker](https://docs.docker.com/engine/install/)
- NVIDIA Container Toolkit：[installing-with-apt](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installing-the-nvidia-container-toolkit)

![nim-cuda.png](nim-cuda.png)

## 登入
使用 Docker 拉取並執行 meta/llama-3_1-8b-instruct（這將下載完整模型並在本機環境中執行）。

```Shell
$ docker login nvcr.io
Username: $oauthtoken
Password: <Your Key>
```
![nvcr.png](nvcr.png)

- `<Your Key>`

![nim-key.png](nim-key.png)

## 拉取並執行
使用下面的命令調出並運行英偉達 NIM。這將為您的基礎架構下載最佳化模型。

- Linux Bash
    ```Bash
    export NGC_API_KEY=<PASTE_API_KEY_HERE>
    export LOCAL_NIM_CACHE=~/.cache/nim
    mkdir -p "$LOCAL_NIM_CACHE"
    docker run -it --rm \
        --gpus all \
        --shm-size=16GB \
        -e NGC_API_KEY \
        -v "$LOCAL_NIM_CACHE:/opt/nim/.cache" \
        -u $(id -u) \
        -p 8000:8000 \
        nvcr.io/nim/meta/llama3-8b-instruct:1.0.0
    ```

- Windows PowerShell
    ```Shell
    # 設定環境變數
    $env:NGC_API_KEY = "<PASTE_API_KEY_HERE>"
    $env:LOCAL_NIM_CACHE = "$env:USERPROFILE\.cache\nim"
    
    # 建立目錄
    New-Item -ItemType Directory -Force -Path $env:LOCAL_NIM_CACHE
    
    # 執行 Docker 容器
    docker run -it --rm `
        --gpus all `
        --shm-size=16GB `
        -e NGC_API_KEY `
        -v "$env:LOCAL_NIM_CACHE:/opt/nim/.cache" `
        -u "$((Get-WmiObject -Class Win32_UserAccount | Where-Object {$_.Name -eq $env:USERNAME}).SID)" `
        -p 8000:8000 `
        nvcr.io/nim/meta/llama3-8b-instruct:1.0.0
    ```

![nim-ps1.png](nim-ps1.png)

## 呼叫
現在，您可以使用以下 curl 命令進行本機 API 呼叫
- Linux Bash
```Bash
curl -X 'POST' \
'http://0.0.0.0:8000/v1/chat/completions' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
    "model": "meta/llama3-8b-instruct",
    "messages": [{"role":"user", "content":"可以講中文嗎"}],
    "max_tokens": 64
}'
```
- Windows PowerShell
```Shell
# 準備請求的數據
$jsonData = @{
    model = "meta/llama3-8b-instruct"
    messages = @(
        @{
            role = "user"
            content = "Write a limerick about the wonders of GPU computing."
        }
    )
    max_tokens = 64
} | ConvertTo-Json

# 發送 POST 請求
$response = Invoke-RestMethod -Uri 'http://localhost:8000/v1/chat/completions' `
                              -Method Post `
                              -Headers @{
                                  'accept' = 'application/json'
                                  'Content-Type' = 'application/json'
                              } `
                              -Body $jsonData

# 輸出結果
$response | ConvertTo-Json -Depth 10
```

## GPU 記憶體不足
如果出現以下錯誤，表示 GPU 記憶體不足，無法執行模型。

`發現但目前不可運行的兼容配置文件數量：1 個（由於 GPU 記憶體不足）`

`Detected additional 1 compatible profile(s) that are currently not runnable due to low free GPU memory.`

```
===========================================
== NVIDIA Inference Microservice LLM NIM ==
===========================================

NVIDIA Inference Microservice LLM NIM Version 1.0.0
Model: nim/meta/llama-3_1-8b-instruct

Container image Copyright (c) 2016-2024, 
  NVIDIA CORPORATION & AFFILIATES. All rights reserved.

The use of this model is governed by the 
  NVIDIA AI Foundation Models Community License Agreement.

ADDITIONAL INFORMATION: Llama 3.1 Community License Agreement, 
  Built with Llama.

INFO 07-26 09:44:00.18 ngc_profile.py:222] Running NIM without LoRA. 
  Only looking for compatible profiles that do not support LoRA.
INFO 07-26 09:44:00.18 ngc_profile.py:224] 
  Detected 0 compatible profile(s).
INFO 07-26 09:44:00.18 ngc_profile.py:226] 
  Detected additional 1 compatible profile(s) that are currently not 
    runnable due to low free GPU memory.
ERROR 07-26 09:44:00.18 utils.py:21]
  Could not find a profile that is currently runnable 
    with the detected hardware. 
  Please check the system information below and make sure you have 
    enough free GPUs.
SYSTEM INFO
- Free GPUs: <None>
- Non-free GPUs:
  -  [2191:10de] (0) NVIDIA GeForce GTX 1660 Ti 
      [current utilization: 7%]
```
{ignore-vars="true"}

![rope.png](rope.png)

## 沒有權限訪問 Docker daemon
我在 Ubuntu 全新安裝 Docker 時，會遇到以下錯誤，表示沒有權限訪問 Docker daemon。

```
docker: permission denied while trying to connect to the Docker daemon
 socket at unix:///var/run/docker.sock: Head 
 "http://%2Fvar%2Frun%2Fdocker.sock/_ping": 
 dial unix /var/run/docker.sock: connect: permission denied.
See 'docker run --help'.
```

解決辦法是添加權限給目前使用者，重新登入後再次執行 docker run 命令。

```Bash
sudo usermod -aG docker $(whoami)
```

## could not select device driver
如果出現以下錯誤，表示 Docker 找不到 GPU 驅動程式。需要安裝 NVIDIA Container Toolkit。

```
docker: Error response from daemon: 
  could not select device driver "" with capabilities: [[gpu]].
```

首先你要先裝好驅動程式，如果沒有可以參考這篇筆記 → [Nvidia-Driver](Nvidia-Driver.md)

然後安裝 NVIDIA Container Toolkit，參考官方文件
[installing-with-apt](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installing-with-apt)

1. Configure the production repository
```Bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

2. Update the packages list from the repository
```Bash
sudo apt-get update
```

3. Install the NVIDIA Container Toolkit packages
```Bash
sudo apt-get install -y nvidia-container-toolkit
```

4. Restart the Docker daemon
```Bash
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

5. Verify the installation
```Bash
sudo docker run --rm --gpus all nvidia/cuda:12.5.1-base-ubuntu24.04 nvidia-smi
```

- 錯誤訊息

```
nvidia-container-cli: requirement error: 
unsatisfied condition: cuda>=12.5, please update your driver to a newer version, 
or use an earlier cuda container: unknown.
```

![nvidia-smi.png](nvidia-smi.png)

3090 Ti 預設安裝的驅動是 535 版本(CUDA 12.2)，CUDA 12.5 需要 555 版本以上，所以需要更新驅動程式。

```Bash
sudo ubuntu-drivers install nvidia:555
sudo init 6
```

更新驅動版本後重新開機應該就可以正常執行 Docker 容器了。

![nvidia-555.png](nvidia-555.png)

- 驅動程式版本對應 CUDA 版本
[CUDA Application Compatibility Support Matrix](https://docs.nvidia.com/deploy/cuda-compatibility/#id3)

- Nvidia CUDA Docker Image
[nvidia/cuda](https://hub.docker.com/r/nvidia/cuda/tags?page=&page_size=&ordering=&name=ubuntu24.04)

- 結論
舊顯卡 (3090 Ti) 也可以安裝最新版驅動 (555)，進而支援最新版本 CUDA (12.5) 和 Docker 容器。

## 未知的 RoPE (Rotary Position Embedding) scaling 類型 "extended"
目前 [Meta Llama 3.1 Know Issues & FAQ #6689](https://github.com/vllm-project/vllm/issues/6689)，會出現以下錯誤，說是會盡快修復。

```
ValueError: Unknown RoPE scaling type extended
```

## 參考
[getting-started](https://docs.nvidia.com/nim/large-language-models/latest/getting-started.html)